"""Focused tests for the C4 pure offline submission-boundary contract."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.no_submit_decision import (
    build_no_submit_decision,
)
from quantitative_trading_research.execution.plan import build_execution_plan
from quantitative_trading_research.execution.plan_filter import filter_execution_plan
from quantitative_trading_research.execution.pre_trade import (
    evaluate_pre_trade_eligibility,
)
from quantitative_trading_research.execution.risk_controls import (
    evaluate_risk_controls,
)
from quantitative_trading_research.execution.submission import (
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    SUBMISSION_ACTION,
    SubmissionBoundaryError,
    build_submission_boundary,
    validate_submission_boundary,
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


def _plan() -> dict:
    pre_trade = _pre_trade()
    return build_execution_plan(
        pre_trade_result=pre_trade,
        price_evidence=[
            {
                "instrument_id": decision["instrument_id"],
                "price": 100.0,
                "observed_at_utc": PRICE_AT,
            }
            for decision in pre_trade["decisions"]
        ],
        configuration=_configuration(),
        plan_at_utc=PLAN_AT,
    )


def _filtered(
    *,
    instrument_id: str = "AAA",
    side: str | None = None,
) -> dict:
    return filter_execution_plan(
        execution_plan=_plan(),
        selection_criteria={
            "instrument_id": instrument_id,
            "side": side,
        },
        filtered_at_utc=FILTERED_AT,
    )


def _boundary(
    *,
    filtered: dict | None = None,
) -> dict:
    return build_submission_boundary(
        filtered_execution_plan=(
            _filtered() if filtered is None else filtered
        )
    )


class SubmissionBoundaryTests(unittest.TestCase):
    def test_normal_boundary_is_versioned_deterministic_and_no_submit(self):
        result = _boundary()

        self.assertEqual(result["schema_id"], SCHEMA_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(result["result_type"], RESULT_TYPE)
        self.assertEqual(result["state_provenance"], STATE_PROVENANCE)
        self.assertTrue(result["passed"])
        self.assertEqual(result["submission_action"], SUBMISSION_ACTION)
        self.assertFalse(result["submission_authorized"])
        self.assertFalse(result["order_submitted"])
        self.assertEqual(result["orders_submitted"], 0)

        validate_submission_boundary(result)

    def test_tm062_and_tm063_identities_are_preserved(self):
        filtered = _filtered()
        result = _boundary(filtered=filtered)

        self.assertEqual(result["source_filter_id"], filtered["filter_id"])
        self.assertEqual(result["source_plan_id"], filtered["source_plan_id"])
        self.assertEqual(
            result["source_plan_id"],
            filtered["source_execution_plan"]["plan_id"],
        )
        self.assertEqual(
            result["selection_identity"],
            filtered["selection_identity"],
        )
        self.assertEqual(
            result["selected_intent_id"],
            filtered["selected_intent_id"],
        )

    def test_boundary_evidence_matches_selected_filtered_and_source_intent(self):
        filtered = _filtered()
        result = _boundary(filtered=filtered)

        selected = next(
            intent
            for intent in filtered["filtered_intents"]
            if intent["selected"] is True
        )
        source = next(
            intent
            for intent in filtered["source_execution_plan"]["intents"]
            if intent["intent_id"] == filtered["selected_intent_id"]
        )
        evidence = result["boundary_evidence"]

        self.assertEqual(evidence["source_intent_id"], source["intent_id"])
        self.assertEqual(evidence["instrument_id"], source["instrument_id"])
        self.assertEqual(evidence["decision_id"], source["decision_id"])
        self.assertEqual(evidence["side"], source["side"])
        self.assertEqual(evidence["quantity"], source["quantity"])
        self.assertEqual(
            evidence["planned_notional"], source["planned_notional"]
        )
        self.assertEqual(evidence["side"], selected["effective_side"])
        self.assertEqual(evidence["quantity"], selected["effective_quantity"])
        self.assertEqual(
            evidence["planned_notional"],
            selected["effective_planned_notional"],
        )
        self.assertEqual(
            evidence["filter_reason"], "SELECTED_EXECUTABLE_INTENT"
        )

    def test_identical_evidence_produces_identical_boundary_and_identity(self):
        filtered = _filtered()
        first = _boundary(filtered=filtered)
        second = _boundary(filtered=filtered)

        self.assertEqual(first, second)
        self.assertEqual(first["boundary_id"], second["boundary_id"])

    def test_material_filter_selection_change_changes_boundary_identity(self):
        first = _boundary(filtered=_filtered(instrument_id="AAA"))
        second = _boundary(filtered=_filtered(instrument_id="BBB", side="SELL"))

        self.assertNotEqual(first["source_filter_id"], second["source_filter_id"])
        self.assertNotEqual(
            first["selected_intent_id"], second["selected_intent_id"]
        )
        self.assertNotEqual(first["boundary_id"], second["boundary_id"])

    def test_builder_does_not_mutate_filtered_input(self):
        filtered = _filtered()
        original = deepcopy(filtered)

        _boundary(filtered=filtered)

        self.assertEqual(filtered, original)

    def test_non_mapping_input_fails_closed(self):
        for value in (None, [], "filtered", 1):
            with self.subTest(value=value):
                with self.assertRaises(SubmissionBoundaryError):
                    build_submission_boundary(filtered_execution_plan=value)

    def test_missing_or_unexpected_filtered_input_fails_closed(self):
        filtered = _filtered()

        missing = deepcopy(filtered)
        del missing["summary"]
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=missing)

        unexpected = deepcopy(filtered)
        unexpected["broker_order"] = {}
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=unexpected)

    def test_tampered_filtered_intent_fails_closed(self):
        filtered = _filtered()
        selected = next(
            intent
            for intent in filtered["filtered_intents"]
            if intent["selected"] is True
        )
        selected["effective_quantity"] += 1.0

        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=filtered)

    def test_tampered_embedded_source_plan_fails_closed(self):
        filtered = _filtered()
        filtered["source_execution_plan"]["intents"][0]["quantity"] += 1.0

        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=filtered)

    def test_operational_filtered_plan_mutations_fail_closed(self):
        filtered = _filtered()

        authorized = deepcopy(filtered)
        authorized["submission_authorized"] = True
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=authorized)

        submitted = deepcopy(filtered)
        submitted["orders_submitted"] = 1
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=submitted)

        selected_authorized = deepcopy(filtered)
        chosen = next(
            intent
            for intent in selected_authorized["filtered_intents"]
            if intent["selected"] is True
        )
        chosen["submission_authorized"] = True
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=selected_authorized)

        selected_submitted = deepcopy(filtered)
        chosen = next(
            intent
            for intent in selected_submitted["filtered_intents"]
            if intent["selected"] is True
        )
        chosen["order_submitted"] = True
        with self.assertRaises(SubmissionBoundaryError):
            _boundary(filtered=selected_submitted)

    def test_forged_upstream_identities_fail_closed(self):
        filtered = _filtered()

        for field, forged in (
            ("filter_id", "plan_filter:forged"),
            ("source_plan_id", "plan:forged"),
            ("selection_identity", "selection:forged"),
            ("selected_intent_id", "intent:forged"),
        ):
            with self.subTest(field=field):
                tampered = deepcopy(filtered)
                tampered[field] = forged
                with self.assertRaises(SubmissionBoundaryError):
                    _boundary(filtered=tampered)

    def test_validator_rejects_tampered_boundary_evidence(self):
        result = _boundary()
        tampered = deepcopy(result)
        tampered["boundary_evidence"]["quantity"] += 1.0

        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(tampered)

    def test_validator_rejects_forged_boundary_or_upstream_ids(self):
        result = _boundary()

        for field, forged in (
            ("boundary_id", "submission_boundary:forged"),
            ("source_plan_id", "plan:forged"),
            ("source_filter_id", "plan_filter:forged"),
            ("selection_identity", "selection:forged"),
            ("selected_intent_id", "intent:forged"),
        ):
            with self.subTest(field=field):
                tampered = deepcopy(result)
                tampered[field] = forged
                with self.assertRaises(SubmissionBoundaryError):
                    validate_submission_boundary(tampered)

    def test_validator_rejects_operational_output_mutations(self):
        result = _boundary()

        for field, value in (
            ("submission_action", "SUBMIT"),
            ("submission_authorized", True),
            ("order_submitted", True),
            ("orders_submitted", 1),
        ):
            with self.subTest(field=field):
                tampered = deepcopy(result)
                tampered[field] = value
                with self.assertRaises(SubmissionBoundaryError):
                    validate_submission_boundary(tampered)

    def test_validator_rejects_missing_and_unexpected_result_keys(self):
        result = _boundary()

        missing = deepcopy(result)
        del missing["boundary_evidence"]
        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(missing)

        unexpected = deepcopy(result)
        unexpected["provider_response"] = {}
        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(unexpected)

    def test_validator_rejects_boundary_evidence_schema_mutations(self):
        result = _boundary()

        missing = deepcopy(result)
        del missing["boundary_evidence"]["decision_id"]
        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(missing)

        unexpected = deepcopy(result)
        unexpected["boundary_evidence"]["order_id"] = "forbidden"
        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(unexpected)

    def test_validator_rejects_tampered_embedded_filtered_evidence(self):
        result = _boundary()
        tampered = deepcopy(result)
        tampered["source_filtered_execution_plan"]["orders_submitted"] = 1

        with self.assertRaises(SubmissionBoundaryError):
            validate_submission_boundary(tampered)

    def test_historical_attribution_is_immutable_and_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "submission.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertIn("racoope70/ppo-trading-pipeline", source)
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a", source
        )
        self.assertIn("src/paper_trading/execution.py", source)

    def test_static_ast_boundary_is_offline_non_operational_and_nonduplicative(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "submission.py"
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
            "datetime",
        }

        imported_relative_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(
                        alias.name.split(".")[0], prohibited_import_roots
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.assertNotIn(
                        node.module.split(".")[0], prohibited_import_roots
                    )
                if node.level:
                    imported_relative_names.update(
                        alias.name for alias in node.names
                    )

        self.assertIn("validate_execution_plan", imported_relative_names)
        self.assertIn(
            "validate_filtered_execution_plan", imported_relative_names
        )
        self.assertNotIn("build_execution_plan", imported_relative_names)
        self.assertNotIn("filter_execution_plan", imported_relative_names)

        prohibited_tokens = (
            "datetime.now",
            "utc_now",
            "submit_market_order",
            "trading_client",
            "submit_order(",
            "cancel_order",
            "replace_order",
            "get_order",
            "paper_trade",
            "live_trade",
            "APCA_API_KEY_ID",
            "APCA_API_SECRET_KEY",
            "requests.",
            "socket.",
            "read_csv",
            "to_csv",
            "write_text",
            "read_text",
            "open(",
            "getenv",
            "environ",
        )

        for token in prohibited_tokens:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
