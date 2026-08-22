"""Focused tests for the C4 pure offline execution-plan filter contract."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.no_submit_decision import (
    build_no_submit_decision,
)
from quantitative_trading_research.execution.plan import (
    build_execution_plan,
)
from quantitative_trading_research.execution.plan_filter import (
    ExecutionPlanFilterError,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    _select_exactly_one,
    filter_execution_plan,
    validate_filtered_execution_plan,
)
from quantitative_trading_research.execution.pre_trade import (
    evaluate_pre_trade_eligibility,
)
from quantitative_trading_research.execution.risk_controls import (
    evaluate_risk_controls,
)


PLAN_AT = "2026-08-22T15:02:00+00:00"
FILTERED_AT = "2026-08-22T15:03:00+00:00"
STATE_AT = "2026-08-22T15:00:00+00:00"
PRICE_AT = "2026-08-22T15:01:00+00:00"


def _configuration() -> dict:
    return {
        "min_notional": 25.0,
        "allow_shorts": True,
        "use_fractionals": True,
        "qty_precision": 6,
    }


def _rows() -> list[dict]:
    return [
        {
            "instrument_id": "AAA",
            "target_weight": 0.20,
            "current_weight": 0.00,
            "equity": 100_000.0,
        },
        {
            "instrument_id": "BBB",
            "target_weight": -0.10,
            "current_weight": 0.00,
            "equity": 100_000.0,
        },
        {
            "instrument_id": "CCC",
            "target_weight": 0.10,
            "current_weight": 0.10,
            "equity": 100_000.0,
        },
    ]


def _pre_trade(rows: list[dict] | None = None) -> dict:
    raw_rows = _rows() if rows is None else rows

    risk = evaluate_risk_controls(
        plan_rows=[
            {
                "instrument_id": row["instrument_id"],
                "target_weight": row["target_weight"],
                "current_weight": row["current_weight"],
                "equity": row["equity"],
                "order_submitted": False,
                "observed_at_utc": STATE_AT,
            }
            for row in raw_rows
        ],
        account_state={
            "open_orders_count": 0,
            "positions_count": sum(
                1
                for row in raw_rows
                if row["current_weight"] != 0
            ),
        },
    )

    decisions = [
        build_no_submit_decision(
            decision_id=f"decision-{index}",
            instrument_id=row["instrument_id"],
            target_weight=row["target_weight"],
            current_weight=row["current_weight"],
            equity=row["equity"],
        )
        for index, row in enumerate(raw_rows, start=1)
    ]

    return evaluate_pre_trade_eligibility(
        risk_result=risk,
        decisions=decisions,
    )


def _build_plan(
    *,
    rows: list[dict] | None = None,
    price: float = 100.0,
    plan_at_utc: str = PLAN_AT,
) -> dict:
    pre_trade = _pre_trade(rows)

    return build_execution_plan(
        pre_trade_result=pre_trade,
        price_evidence=[
            {
                "instrument_id": decision["instrument_id"],
                "price": price,
                "observed_at_utc": PRICE_AT,
            }
            for decision in pre_trade["decisions"]
        ],
        configuration=_configuration(),
        plan_at_utc=plan_at_utc,
    )


def _selection(
    instrument_id: str = "AAA",
    side: str | None = None,
) -> dict:
    return {
        "instrument_id": instrument_id,
        "side": side,
    }


def _filter(
    *,
    plan: dict | None = None,
    selection: dict | None = None,
    filtered_at_utc: str = FILTERED_AT,
) -> dict:
    return filter_execution_plan(
        execution_plan=_build_plan() if plan is None else plan,
        selection_criteria=(
            _selection() if selection is None else selection
        ),
        filtered_at_utc=filtered_at_utc,
    )


class ExecutionPlanFilterTests(unittest.TestCase):
    def test_normal_filter_is_versioned_deterministic_and_no_submit(self):
        result = _filter()

        self.assertEqual(result["schema_id"], SCHEMA_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            result["result_type"],
            "offline_execution_plan_filter",
        )
        self.assertEqual(
            result["state_provenance"],
            STATE_PROVENANCE,
        )
        self.assertTrue(result["passed"])
        self.assertFalse(result["submission_authorized"])
        self.assertEqual(result["orders_submitted"], 0)
        self.assertEqual(result["source_plan_id"],
                         result["source_execution_plan"]["plan_id"])
        self.assertEqual(result["summary"]["enabled_intent_count"], 1)

        validate_filtered_execution_plan(result)

    def test_selected_intent_is_preserved_in_effective_representation(self):
        source = _build_plan()
        source_selected = next(
            intent
            for intent in source["intents"]
            if intent["instrument_id"] == "AAA"
        )

        result = _filter(plan=source)
        selected = next(
            intent
            for intent in result["filtered_intents"]
            if intent["selected"] is True
        )

        self.assertEqual(
            selected["source_intent_id"],
            source_selected["intent_id"],
        )
        self.assertEqual(
            result["selected_intent_id"],
            source_selected["intent_id"],
        )
        self.assertEqual(
            selected["instrument_id"],
            source_selected["instrument_id"],
        )
        self.assertEqual(
            selected["decision_id"],
            source_selected["decision_id"],
        )
        self.assertEqual(
            selected["source_side"],
            source_selected["side"],
        )
        self.assertEqual(
            selected["source_quantity"],
            source_selected["quantity"],
        )
        self.assertEqual(
            selected["source_planned_notional"],
            source_selected["planned_notional"],
        )
        self.assertTrue(selected["enabled"])
        self.assertEqual(
            selected["effective_side"],
            source_selected["side"],
        )
        self.assertEqual(
            selected["effective_quantity"],
            source_selected["quantity"],
        )
        self.assertEqual(
            selected["effective_planned_notional"],
            source_selected["planned_notional"],
        )
        self.assertEqual(
            selected["filter_reason"],
            "SELECTED_EXECUTABLE_INTENT",
        )
        self.assertFalse(selected["submission_authorized"])
        self.assertFalse(selected["order_submitted"])

    def test_every_non_selected_executable_intent_is_disabled(self):
        result = _filter(selection=_selection("AAA"))

        disabled = [
            intent
            for intent in result["filtered_intents"]
            if (
                intent["source_should_order"] is True
                and intent["selected"] is False
            )
        ]

        self.assertEqual(len(disabled), 1)

        intent = disabled[0]
        self.assertEqual(intent["instrument_id"], "BBB")
        self.assertFalse(intent["enabled"])
        self.assertEqual(intent["effective_side"], "HOLD")
        self.assertEqual(intent["effective_quantity"], 0.0)
        self.assertEqual(intent["effective_planned_notional"], 0.0)
        self.assertEqual(
            intent["filter_reason"],
            "DISABLED_NON_SELECTED_EXECUTABLE_INTENT",
        )
        self.assertFalse(intent["submission_authorized"])
        self.assertFalse(intent["order_submitted"])

    def test_source_hold_intents_remain_visible_and_disabled(self):
        result = _filter()

        hold = next(
            intent
            for intent in result["filtered_intents"]
            if intent["instrument_id"] == "CCC"
        )

        self.assertFalse(hold["source_should_order"])
        self.assertFalse(hold["selected"])
        self.assertFalse(hold["enabled"])
        self.assertEqual(hold["effective_side"], "HOLD")
        self.assertEqual(hold["effective_quantity"], 0.0)
        self.assertEqual(hold["effective_planned_notional"], 0.0)
        self.assertEqual(
            hold["filter_reason"],
            "SOURCE_INTENT_NOT_EXECUTABLE",
        )

    def test_all_source_intents_are_retained_for_audit_visibility(self):
        source = _build_plan()
        result = _filter(plan=source)

        self.assertEqual(
            len(result["filtered_intents"]),
            len(source["intents"]),
        )
        self.assertEqual(
            result["summary"]["audit_intent_count"],
            len(source["intents"]),
        )
        self.assertEqual(
            [
                intent["source_intent_id"]
                for intent in result["filtered_intents"]
            ],
            [
                intent["intent_id"]
                for intent in source["intents"]
            ],
        )

    def test_summary_reconstructs_filter_state(self):
        result = _filter(selection=_selection("AAA"))

        summary = result["summary"]

        self.assertEqual(summary["source_intent_count"], 3)
        self.assertEqual(summary["source_executable_intent_count"], 2)
        self.assertEqual(summary["source_hold_intent_count"], 1)
        self.assertEqual(summary["audit_intent_count"], 3)
        self.assertEqual(summary["enabled_intent_count"], 1)
        self.assertEqual(
            summary["disabled_executable_intent_count"],
            1,
        )
        self.assertEqual(summary["enabled_buy_count"], 1)
        self.assertEqual(summary["enabled_sell_count"], 0)
        self.assertEqual(
            summary["gross_enabled_planned_notional"],
            20_000.0,
        )

    def test_sell_selection_preserves_sell_intent(self):
        result = _filter(
            selection=_selection("BBB", "SELL")
        )

        selected = next(
            intent
            for intent in result["filtered_intents"]
            if intent["selected"] is True
        )

        self.assertEqual(selected["instrument_id"], "BBB")
        self.assertEqual(selected["effective_side"], "SELL")
        self.assertEqual(
            result["summary"]["enabled_sell_count"],
            1,
        )
        self.assertEqual(
            result["summary"]["enabled_buy_count"],
            0,
        )

    def test_side_is_explicitly_normalized(self):
        result = _filter(
            selection=_selection("BBB", "sell")
        )

        self.assertEqual(
            result["selection_criteria"],
            {
                "instrument_id": "BBB",
                "side": "SELL",
            },
        )

    def test_optional_side_can_be_none(self):
        result = _filter(
            selection=_selection("AAA", None)
        )

        self.assertEqual(
            result["selection_criteria"]["side"],
            None,
        )
        self.assertEqual(
            result["summary"]["enabled_intent_count"],
            1,
        )

    def test_zero_matching_intents_fail_closed(self):
        with self.assertRaises(ExecutionPlanFilterError):
            _filter(
                selection=_selection("ZZZ")
            )

    def test_wrong_side_resolving_to_zero_fails_closed(self):
        with self.assertRaises(ExecutionPlanFilterError):
            _filter(
                selection=_selection("AAA", "SELL")
            )

    def test_multiple_matching_intents_fail_closed(self):
        source = {
            "intents": [
                {
                    "intent_id": "intent:one",
                    "instrument_id": "AAA",
                    "side": "BUY",
                    "quantity": 1.0,
                    "planned_notional": 100.0,
                    "should_order": True,
                },
                {
                    "intent_id": "intent:two",
                    "instrument_id": "AAA",
                    "side": "BUY",
                    "quantity": 2.0,
                    "planned_notional": 200.0,
                    "should_order": True,
                },
            ]
        }

        with self.assertRaises(ExecutionPlanFilterError):
            _select_exactly_one(
                source_plan=source,
                selection={
                    "instrument_id": "AAA",
                    "side": "BUY",
                },
            )

    def test_identical_inputs_produce_identical_result_and_ids(self):
        source = _build_plan()
        selection = _selection("AAA", "BUY")

        first = _filter(
            plan=source,
            selection=selection,
        )
        second = _filter(
            plan=source,
            selection=selection,
        )

        self.assertEqual(first, second)
        self.assertEqual(
            first["filter_id"],
            second["filter_id"],
        )
        self.assertEqual(
            first["selection_identity"],
            second["selection_identity"],
        )
        self.assertEqual(
            first["selected_intent_id"],
            second["selected_intent_id"],
        )

    def test_material_selection_change_changes_identity(self):
        source = _build_plan()

        first = _filter(
            plan=source,
            selection=_selection("AAA"),
        )
        second = _filter(
            plan=source,
            selection=_selection("BBB"),
        )

        self.assertNotEqual(
            first["selection_identity"],
            second["selection_identity"],
        )
        self.assertNotEqual(
            first["filter_id"],
            second["filter_id"],
        )
        self.assertNotEqual(
            first["selected_intent_id"],
            second["selected_intent_id"],
        )

    def test_filter_timestamp_changes_filter_id_not_selection_identity(self):
        source = _build_plan()
        selection = _selection("AAA")

        first = _filter(
            plan=source,
            selection=selection,
            filtered_at_utc="2026-08-22T15:03:00+00:00",
        )
        second = _filter(
            plan=source,
            selection=selection,
            filtered_at_utc="2026-08-22T15:04:00+00:00",
        )

        self.assertEqual(
            first["selection_identity"],
            second["selection_identity"],
        )
        self.assertEqual(
            first["selected_intent_id"],
            second["selected_intent_id"],
        )
        self.assertNotEqual(
            first["filter_id"],
            second["filter_id"],
        )

    def test_source_plan_change_changes_selection_and_filter_identity(self):
        first_source = _build_plan(price=100.0)
        second_source = _build_plan(price=101.0)

        first = _filter(plan=first_source)
        second = _filter(plan=second_source)

        self.assertNotEqual(
            first["source_plan_id"],
            second["source_plan_id"],
        )
        self.assertNotEqual(
            first["selection_identity"],
            second["selection_identity"],
        )
        self.assertNotEqual(
            first["filter_id"],
            second["filter_id"],
        )

    def test_filter_does_not_mutate_caller_inputs(self):
        source = _build_plan()
        selection = _selection("AAA", "BUY")

        original_source = deepcopy(source)
        original_selection = deepcopy(selection)

        _filter(
            plan=source,
            selection=selection,
        )

        self.assertEqual(source, original_source)
        self.assertEqual(selection, original_selection)

    def test_tampered_source_execution_plan_fails_closed(self):
        source = _build_plan()
        tampered = deepcopy(source)
        tampered["intents"][0]["quantity"] += 1.0

        with self.assertRaises(ExecutionPlanFilterError):
            _filter(plan=tampered)

    def test_operational_source_plan_mutation_fails_closed(self):
        source = _build_plan()
        tampered = deepcopy(source)
        tampered["submission_authorized"] = True

        with self.assertRaises(ExecutionPlanFilterError):
            _filter(plan=tampered)

    def test_selection_requires_exact_schema(self):
        missing = {
            "instrument_id": "AAA",
        }
        with self.assertRaises(ExecutionPlanFilterError):
            _filter(selection=missing)

        unexpected = {
            "instrument_id": "AAA",
            "side": None,
            "broker": "forbidden",
        }
        with self.assertRaises(ExecutionPlanFilterError):
            _filter(selection=unexpected)

    def test_selection_rejects_blank_instrument_and_invalid_side(self):
        bad_selections = [
            {
                "instrument_id": "",
                "side": None,
            },
            {
                "instrument_id": "   ",
                "side": None,
            },
            {
                "instrument_id": "AAA",
                "side": "",
            },
            {
                "instrument_id": "AAA",
                "side": "HOLD",
            },
            {
                "instrument_id": "AAA",
                "side": 1,
            },
        ]

        for selection in bad_selections:
            with self.subTest(selection=selection):
                with self.assertRaises(ExecutionPlanFilterError):
                    _filter(selection=selection)

    def test_filter_timestamp_must_be_explicit_timezone_aware_iso8601(self):
        for value in (
            "2026-08-22T15:03:00",
            "not-a-timestamp",
            "",
            None,
        ):
            with self.subTest(value=value):
                with self.assertRaises(ExecutionPlanFilterError):
                    _filter(filtered_at_utc=value)

    def test_filter_timestamp_must_not_precede_source_plan(self):
        with self.assertRaises(ExecutionPlanFilterError):
            _filter(
                filtered_at_utc=
                    "2026-08-22T15:01:59+00:00",
            )

    def test_filter_timestamp_equal_to_source_plan_is_allowed(self):
        result = _filter(filtered_at_utc=PLAN_AT)

        self.assertEqual(
            result["filtered_at_utc"],
            "2026-08-22T15:02:00+00:00",
        )
        validate_filtered_execution_plan(result)

    def test_validator_rejects_tampered_filtered_intent(self):
        result = _filter()

        tampered = deepcopy(result)
        selected = next(
            intent
            for intent in tampered["filtered_intents"]
            if intent["selected"] is True
        )
        selected["effective_quantity"] += 1.0

        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(tampered)

    def test_validator_rejects_tampered_summary(self):
        result = _filter()
        tampered = deepcopy(result)
        tampered["summary"]["enabled_intent_count"] = 2

        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(tampered)

    def test_validator_rejects_forged_filter_and_selection_ids(self):
        result = _filter()

        bad_filter = deepcopy(result)
        bad_filter["filter_id"] = "plan_filter:forged"
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(bad_filter)

        bad_selection = deepcopy(result)
        bad_selection["selection_identity"] = "selection:forged"
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(bad_selection)

    def test_validator_rejects_forged_source_plan_and_selected_intent_ids(self):
        result = _filter()

        bad_source = deepcopy(result)
        bad_source["source_plan_id"] = "plan:forged"
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(bad_source)

        bad_selected = deepcopy(result)
        bad_selected["selected_intent_id"] = "intent:forged"
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(bad_selected)

    def test_validator_rejects_operational_mutations(self):
        result = _filter()

        authorized = deepcopy(result)
        authorized["submission_authorized"] = True
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(authorized)

        submitted = deepcopy(result)
        submitted["orders_submitted"] = 1
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(submitted)

        intent_authorized = deepcopy(result)
        intent_authorized["filtered_intents"][0][
            "submission_authorized"
        ] = True
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(intent_authorized)

        intent_submitted = deepcopy(result)
        intent_submitted["filtered_intents"][0][
            "order_submitted"
        ] = True
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(intent_submitted)

    def test_validator_rejects_missing_and_unexpected_top_level_keys(self):
        result = _filter()

        missing = deepcopy(result)
        del missing["summary"]
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(missing)

        unexpected = deepcopy(result)
        unexpected["broker_order"] = {}
        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(unexpected)

    def test_validator_rejects_tampered_embedded_source_plan(self):
        result = _filter()
        tampered = deepcopy(result)
        tampered["source_execution_plan"]["orders_submitted"] = 1

        with self.assertRaises(ExecutionPlanFilterError):
            validate_filtered_execution_plan(tampered)

    def test_historical_attribution_is_immutable_and_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "plan_filter.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertIn(
            "racoope70/ppo-trading-pipeline",
            source,
        )
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source,
        )
        self.assertIn(
            "src/paper_trading/filter_execution_plan.py",
            source,
        )

    def test_static_ast_boundary_is_offline_and_non_operational(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "plan_filter.py"
        )
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        prohibited_import_roots = {
            "alpaca",
            "pandas",
            "requests",
            "urllib",
            "http",
            "socket",
            "subprocess",
            "pathlib",
            "os",
            "dotenv",
            "shutil",
            "argparse",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(
                        alias.name.split(".")[0],
                        prohibited_import_roots,
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.assertNotIn(
                        node.module.split(".")[0],
                        prohibited_import_roots,
                    )

        prohibited_tokens = (
            "datetime.now",
            "utc_now",
            "submit_market_order",
            "trading_client",
            "submit_order",
            "paper_trade",
            "live_trade",
            "requests.",
            "socket.",
            "read_csv",
            "to_csv",
            "write_text",
            "read_text",
            "copy2",
        )

        for token in prohibited_tokens:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
