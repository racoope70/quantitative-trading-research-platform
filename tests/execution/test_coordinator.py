"""Focused tests for the C4 pure offline guarded execution coordinator."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.coordinator import (
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    ExecutionCoordinatorError,
    build_execution_coordinator,
    validate_execution_coordinator,
)
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
    SUBMISSION_ACTION,
    build_submission_boundary,
)


PLAN_AT = "2026-08-22T15:02:00+00:00"
FILTERED_AT = "2026-08-22T15:03:00+00:00"
STATE_AT = "2026-08-22T15:00:00+00:00"
PRICE_AT = "2026-08-22T15:01:00+00:00"

EXPECTED_STAGE_ORDER = [
    "TM_031_RISK",
    "TM_032_PRE_TRADE",
    "TM_062_PLAN",
    "TM_063_FILTER",
    "TM_029_SUBMISSION_BOUNDARY",
]


def _rows(*, aaa_target: float = 0.20) -> list[dict]:
    return [
        {
            "instrument_id": "AAA",
            "target_weight": aaa_target,
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


def _configuration() -> dict:
    return {
        "min_notional": 25.0,
        "allow_shorts": True,
        "use_fractionals": True,
        "qty_precision": 6,
    }


def _chain(
    *,
    aaa_target: float = 0.20,
    selected: str = "AAA",
) -> dict[str, dict]:
    rows = _rows(aaa_target=aaa_target)

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
            for row in rows
        ],
        account_state={
            "open_orders_count": 0,
            "positions_count": sum(
                1
                for row in rows
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
        for index, row in enumerate(rows, start=1)
    ]

    pre_trade = evaluate_pre_trade_eligibility(
        risk_result=risk,
        decisions=decisions,
    )

    plan = build_execution_plan(
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

    filtered = filter_execution_plan(
        execution_plan=plan,
        selection_criteria={
            "instrument_id": selected,
            "side": None,
        },
        filtered_at_utc=FILTERED_AT,
    )

    boundary = build_submission_boundary(
        filtered_execution_plan=filtered,
    )

    return {
        "risk_result": risk,
        "pre_trade_result": pre_trade,
        "execution_plan": plan,
        "filtered_execution_plan": filtered,
        "submission_boundary": boundary,
    }


def _coordinator(
    chain: dict[str, dict] | None = None,
) -> dict:
    evidence = _chain() if chain is None else chain
    return build_execution_coordinator(**evidence)


class ExecutionCoordinatorTests(unittest.TestCase):
    def test_normal_result_is_versioned_deterministic_and_no_submit(self):
        result = _coordinator()

        self.assertEqual(result["schema_id"], SCHEMA_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(result["result_type"], RESULT_TYPE)
        self.assertEqual(result["state_provenance"], STATE_PROVENANCE)
        self.assertTrue(result["passed"])
        self.assertEqual(
            result["submission_action"],
            SUBMISSION_ACTION,
        )
        self.assertFalse(result["submission_authorized"])
        self.assertFalse(result["order_submitted"])
        self.assertEqual(result["orders_submitted"], 0)

        validate_execution_coordinator(result)

    def test_upstream_chain_is_exactly_ordered_and_five_stages(self):
        result = _coordinator()

        self.assertEqual(
            [
                entry["stage"]
                for entry in result["upstream_chain"]
            ],
            EXPECTED_STAGE_ORDER,
        )
        self.assertEqual(len(result["upstream_chain"]), 5)

        for entry in result["upstream_chain"]:
            self.assertIsInstance(entry["schema_id"], str)
            self.assertTrue(entry["schema_id"])
            self.assertIsInstance(entry["schema_version"], int)
            self.assertIsInstance(entry["identity"], str)
            self.assertTrue(entry["identity"])

    def test_identical_chain_produces_identical_result_and_identity(self):
        chain = _chain()

        first = _coordinator(chain)
        second = _coordinator(chain)

        self.assertEqual(first, second)
        self.assertEqual(
            first["coordinator_id"],
            second["coordinator_id"],
        )

    def test_material_upstream_change_changes_coordinator_identity(self):
        first = _coordinator(
            _chain(
                aaa_target=0.20,
                selected="AAA",
            )
        )
        second = _coordinator(
            _chain(
                aaa_target=0.25,
                selected="AAA",
            )
        )

        self.assertNotEqual(
            first["coordinator_id"],
            second["coordinator_id"],
        )

    def test_builder_does_not_mutate_upstream_inputs(self):
        chain = _chain()
        original = deepcopy(chain)

        _coordinator(chain)

        self.assertEqual(chain, original)

    def test_non_mapping_upstream_inputs_fail_closed(self):
        chain = _chain()

        for field in chain:
            with self.subTest(field=field):
                bad = deepcopy(chain)
                bad[field] = None

                with self.assertRaises(
                    ExecutionCoordinatorError
                ):
                    _coordinator(bad)

    def test_missing_upstream_evidence_fails_closed(self):
        chain = _chain()
        tampered = deepcopy(chain)
        del tampered["risk_result"]["checks"]

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(tampered)

    def test_tampered_upstream_evidence_fails_closed(self):
        chain = _chain()
        tampered = deepcopy(chain)
        tampered["execution_plan"]["intents"][0][
            "quantity"
        ] += 1.0

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(tampered)

    def test_cross_contract_risk_pretrade_mismatch_fails_closed(self):
        first = _chain(aaa_target=0.20)
        second = _chain(aaa_target=0.25)

        mismatched = deepcopy(first)
        mismatched["risk_result"] = second["risk_result"]

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(mismatched)

    def test_cross_contract_pretrade_plan_mismatch_fails_closed(self):
        first = _chain(aaa_target=0.20)
        second = _chain(aaa_target=0.25)

        mismatched = deepcopy(first)
        mismatched["pre_trade_result"] = second[
            "pre_trade_result"
        ]

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(mismatched)

    def test_cross_contract_plan_filter_mismatch_fails_closed(self):
        first = _chain(aaa_target=0.20)
        second = _chain(aaa_target=0.25)

        mismatched = deepcopy(first)
        mismatched["execution_plan"] = second[
            "execution_plan"
        ]

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(mismatched)

    def test_cross_contract_filter_boundary_mismatch_fails_closed(self):
        first = _chain(selected="AAA")
        second = _chain(selected="BBB")

        mismatched = deepcopy(first)
        mismatched["filtered_execution_plan"] = second[
            "filtered_execution_plan"
        ]

        with self.assertRaises(ExecutionCoordinatorError):
            _coordinator(mismatched)

    def test_validator_rejects_reordered_upstream_chain(self):
        result = _coordinator()
        tampered = deepcopy(result)

        (
            tampered["upstream_chain"][0],
            tampered["upstream_chain"][1],
        ) = (
            tampered["upstream_chain"][1],
            tampered["upstream_chain"][0],
        )

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(tampered)

    def test_validator_rejects_forged_upstream_identity(self):
        result = _coordinator()
        tampered = deepcopy(result)
        tampered["upstream_chain"][2][
            "identity"
        ] = "plan:forged"

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(tampered)

    def test_validator_rejects_forged_coordinator_identity(self):
        result = _coordinator()
        tampered = deepcopy(result)
        tampered[
            "coordinator_id"
        ] = "execution_coordinator:forged"

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(tampered)

    def test_validator_rejects_operational_output_mutations(self):
        result = _coordinator()

        for field, value in (
            ("submission_action", "SUBMIT"),
            ("submission_authorized", True),
            ("order_submitted", True),
            ("orders_submitted", 1),
        ):
            with self.subTest(field=field):
                tampered = deepcopy(result)
                tampered[field] = value

                with self.assertRaises(
                    ExecutionCoordinatorError
                ):
                    validate_execution_coordinator(
                        tampered
                    )

    def test_validator_rejects_missing_or_unexpected_result_keys(self):
        result = _coordinator()

        missing = deepcopy(result)
        del missing["upstream_chain"]

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(missing)

        unexpected = deepcopy(result)
        unexpected["provider_response"] = {}

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(unexpected)

    def test_validator_rejects_tampered_embedded_upstream_evidence(self):
        result = _coordinator()
        tampered = deepcopy(result)
        tampered["submission_boundary"][
            "orders_submitted"
        ] = 1

        with self.assertRaises(ExecutionCoordinatorError):
            validate_execution_coordinator(tampered)

    def test_historical_attribution_is_immutable_and_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "coordinator.py"
        )
        source = source_path.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "racoope70/ppo-trading-pipeline",
            source,
        )
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source,
        )
        self.assertIn(
            "src/paper_trading/paper_trade_loop.py",
            source,
        )

    def test_static_ast_boundary_is_offline_non_operational_and_nonduplicative(
        self,
    ):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "coordinator.py"
        )
        source = source_path.read_text(
            encoding="utf-8"
        )
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
                        alias.name.split(".")[0],
                        prohibited_import_roots,
                    )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.assertNotIn(
                        node.module.split(".")[0],
                        prohibited_import_roots,
                    )

                if node.level:
                    imported_relative_names.update(
                        alias.name
                        for alias in node.names
                    )

        for name in (
            "validate_risk_result",
            "validate_pre_trade_result",
            "validate_execution_plan",
            "validate_filtered_execution_plan",
            "validate_submission_boundary",
        ):
            self.assertIn(
                name,
                imported_relative_names,
            )

        for name in (
            "evaluate_risk_controls",
            "evaluate_pre_trade_eligibility",
            "build_execution_plan",
            "filter_execution_plan",
            "build_submission_boundary",
        ):
            self.assertNotIn(
                name,
                imported_relative_names,
            )

        prohibited_tokens = (
            "create_alpaca_clients",
            "trading_client",
            "submit_order(",
            "submit_market_order",
            "cancel_order",
            "replace_order",
            "get_account(",
            "get_all_positions(",
            "get_orders(",
            "snapshot_broker_state",
            "datetime.now",
            "utc_now",
            "os.environ",
            "getenv(",
            "read_text(",
            "write_text(",
            "open(",
        )

        for token in prohibited_tokens:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
