"""Focused tests for the C4 offline pre-trade eligibility contract."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.no_submit_decision import (
    build_no_submit_decision,
)
from quantitative_trading_research.execution.pre_trade import (
    PreTradeEligibilityError,
    evaluate_pre_trade_eligibility,
    validate_pre_trade_result,
)
from quantitative_trading_research.execution.risk_controls import (
    evaluate_risk_controls,
)


def _passing_risk_result() -> dict:
    return evaluate_risk_controls(
        plan_rows=[
            {
                "instrument_id": "AAA",
                "target_weight": 0.20,
                "current_weight": 0.00,
                "equity": 100_000.0,
                "order_submitted": False,
            },
            {
                "instrument_id": "BBB",
                "target_weight": -0.10,
                "current_weight": 0.00,
                "equity": 100_000.0,
                "order_submitted": False,
            },
        ],
        account_state={
            "open_orders_count": 0,
            "positions_count": 0,
        },
    )


def _decision_from_risk_row(
    row: dict,
    *,
    decision_id: str,
) -> dict:
    return build_no_submit_decision(
        decision_id=decision_id,
        instrument_id=row["instrument_id"],
        target_weight=row["target_weight"],
        current_weight=row["current_weight"],
        equity=row["equity"],
    )


def _passing_inputs() -> tuple[dict, list[dict]]:
    risk_result = _passing_risk_result()
    decisions = [
        _decision_from_risk_row(
            row,
            decision_id=f"decision-{index}",
        )
        for index, row in enumerate(
            risk_result["evaluated_rows"],
            start=1,
        )
    ]
    return risk_result, decisions


def _check_map(result: dict) -> dict[str, dict]:
    return {
        check["name"]: check
        for check in result["checks"]
    }


class PreTradeEligibilityTests(unittest.TestCase):
    def test_normal_result_is_versioned_offline_and_passing(self):
        risk_result, decisions = _passing_inputs()

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertTrue(result["passed"])
        self.assertEqual(
            result["schema_id"],
            "C4_OFFLINE_PRE_TRADE_ELIGIBILITY_V1",
        )
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(
            result["result_type"],
            "offline_pre_trade_eligibility_result",
        )
        self.assertEqual(
            result["state_provenance"],
            "validated_caller_supplied_offline_evidence",
        )

        checks = _check_map(result)
        self.assertTrue(all(check["passed"] for check in checks.values()))
        self.assertFalse(
            any(
                decision["submission_authorized"]
                for decision in result["decisions"]
            )
        )
        self.assertFalse(
            any(
                decision["order_submitted"]
                for decision in result["decisions"]
            )
        )

    def test_exact_canonical_check_set_and_order(self):
        risk_result, decisions = _passing_inputs()

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertEqual(
            [check["name"] for check in result["checks"]],
            [
                "risk_result_passed",
                "decision_set_non_empty",
                "decision_ids_unique",
                "decision_instruments_unique",
                "decision_instruments_match_risk",
                "decision_state_matches_risk",
                "submission_authority_absent",
                "orders_submitted_absent",
            ],
        )

    def test_valid_failed_risk_result_fails_closed(self):
        risk_result = evaluate_risk_controls(
            plan_rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.50,
                    "current_weight": 0.00,
                    "equity": 100_000.0,
                    "order_submitted": False,
                }
            ],
            account_state={
                "open_orders_count": 0,
                "positions_count": 0,
            },
        )
        self.assertFalse(risk_result["passed"])

        decisions = [
            _decision_from_risk_row(
                risk_result["evaluated_rows"][0],
                decision_id="decision-1",
            )
        ]

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertFalse(result["passed"])
        self.assertFalse(
            _check_map(result)["risk_result_passed"]["passed"]
        )

    def test_empty_decision_set_fails_closed(self):
        risk_result = _passing_risk_result()

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=[],
        )

        self.assertFalse(result["passed"])
        checks = _check_map(result)
        self.assertFalse(checks["decision_set_non_empty"]["passed"])
        self.assertFalse(
            checks["decision_instruments_match_risk"]["passed"]
        )
        self.assertFalse(
            checks["decision_state_matches_risk"]["passed"]
        )

    def test_duplicate_decision_ids_fail_closed(self):
        risk_result, decisions = _passing_inputs()
        decisions[1] = _decision_from_risk_row(
            risk_result["evaluated_rows"][1],
            decision_id=decisions[0]["decision_id"],
        )

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertFalse(result["passed"])
        check = _check_map(result)["decision_ids_unique"]
        self.assertFalse(check["passed"])
        self.assertEqual(
            check["evidence"]["duplicate_decision_ids"],
            ["decision-1"],
        )

    def test_duplicate_decision_instruments_fail_closed(self):
        risk_result, decisions = _passing_inputs()
        decisions[1] = _decision_from_risk_row(
            risk_result["evaluated_rows"][0],
            decision_id="decision-2",
        )

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertFalse(result["passed"])
        checks = _check_map(result)
        self.assertFalse(
            checks["decision_instruments_unique"]["passed"]
        )
        self.assertFalse(
            checks["decision_instruments_match_risk"]["passed"]
        )

    def test_missing_and_unexpected_instruments_fail_closed(self):
        risk_result, decisions = _passing_inputs()

        decisions[1] = build_no_submit_decision(
            decision_id="decision-2",
            instrument_id="CCC",
            target_weight=-0.10,
            current_weight=0.00,
            equity=100_000.0,
        )

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertFalse(result["passed"])
        check = _check_map(
            result
        )["decision_instruments_match_risk"]

        self.assertFalse(check["passed"])
        self.assertEqual(
            check["evidence"]["missing_decision_instruments"],
            ["BBB"],
        )
        self.assertEqual(
            check["evidence"]["unexpected_decision_instruments"],
            ["CCC"],
        )

    def test_decision_state_mismatch_fails_closed(self):
        risk_result, decisions = _passing_inputs()

        decisions[0] = build_no_submit_decision(
            decision_id="decision-1",
            instrument_id="AAA",
            target_weight=0.19,
            current_weight=0.00,
            equity=100_000.0,
        )

        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertFalse(result["passed"])
        check = _check_map(
            result
        )["decision_state_matches_risk"]

        self.assertFalse(check["passed"])
        self.assertTrue(check["evidence"]["comparison_possible"])
        self.assertTrue(check["evidence"]["mismatches"])

    def test_malformed_risk_result_is_rejected(self):
        risk_result, decisions = _passing_inputs()
        bad_risk = deepcopy(risk_result)
        del bad_risk["checks"]

        with self.assertRaises(PreTradeEligibilityError):
            evaluate_pre_trade_eligibility(
                risk_result=bad_risk,
                decisions=decisions,
            )

    def test_decisions_must_be_list(self):
        risk_result, decisions = _passing_inputs()

        with self.assertRaises(PreTradeEligibilityError):
            evaluate_pre_trade_eligibility(
                risk_result=risk_result,
                decisions=tuple(decisions),
            )

    def test_non_mapping_decision_is_rejected(self):
        risk_result, decisions = _passing_inputs()
        bad_decisions = list(decisions)
        bad_decisions[0] = "not-a-decision"

        with self.assertRaises(PreTradeEligibilityError):
            evaluate_pre_trade_eligibility(
                risk_result=risk_result,
                decisions=bad_decisions,
            )

    def test_submission_authority_mutation_is_rejected(self):
        risk_result, decisions = _passing_inputs()
        bad_decisions = deepcopy(decisions)
        bad_decisions[0]["submission_authorized"] = True

        with self.assertRaises(PreTradeEligibilityError):
            evaluate_pre_trade_eligibility(
                risk_result=risk_result,
                decisions=bad_decisions,
            )

    def test_order_submitted_mutation_is_rejected(self):
        risk_result, decisions = _passing_inputs()
        bad_decisions = deepcopy(decisions)
        bad_decisions[0]["order_submitted"] = True

        with self.assertRaises(PreTradeEligibilityError):
            evaluate_pre_trade_eligibility(
                risk_result=risk_result,
                decisions=bad_decisions,
            )

    def test_validator_rejects_forged_overall_pass(self):
        risk_result, decisions = _passing_inputs()
        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )
        forged = deepcopy(result)
        forged["passed"] = False

        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(forged)

    def test_validator_rejects_tampered_check_evidence(self):
        risk_result, decisions = _passing_inputs()
        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )
        forged = deepcopy(result)
        forged["checks"][0]["evidence"]["risk_passed"] = False

        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(forged)

    def test_validator_rejects_unknown_missing_and_duplicate_checks(self):
        risk_result, decisions = _passing_inputs()
        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        unknown = deepcopy(result)
        unknown["checks"][0]["name"] = "unknown_check"
        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(unknown)

        missing = deepcopy(result)
        missing["checks"].pop()
        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(missing)

        duplicate = deepcopy(result)
        duplicate["checks"].append(
            deepcopy(duplicate["checks"][0])
        )
        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(duplicate)

    def test_validator_rejects_tampered_embedded_upstream_evidence(self):
        risk_result, decisions = _passing_inputs()
        result = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        bad_risk = deepcopy(result)
        bad_risk["risk_result"]["passed"] = False
        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(bad_risk)

        bad_decision = deepcopy(result)
        bad_decision["decisions"][0]["order_submitted"] = True
        with self.assertRaises(PreTradeEligibilityError):
            validate_pre_trade_result(bad_decision)

    def test_evaluation_does_not_mutate_caller_inputs(self):
        risk_result, decisions = _passing_inputs()
        original_risk = deepcopy(risk_result)
        original_decisions = deepcopy(decisions)

        evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertEqual(risk_result, original_risk)
        self.assertEqual(decisions, original_decisions)

    def test_identical_inputs_produce_identical_result(self):
        risk_result, decisions = _passing_inputs()

        first = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )
        second = evaluate_pre_trade_eligibility(
            risk_result=risk_result,
            decisions=decisions,
        )

        self.assertEqual(first, second)

    def test_historical_attribution_is_immutable_and_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "pre_trade.py"
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
            "src/paper_trading/pre_trade_checklist.py",
            source,
        )

    def test_static_ast_boundary_is_offline_and_non_operational(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "pre_trade.py"
        )
        tree = ast.parse(source_path.read_text(encoding="utf-8"))

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
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(
                        alias.name.split(".")[0],
                        prohibited_import_roots,
                    )

            if isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(
                    node.module.split(".")[0],
                    prohibited_import_roots,
                )

        prohibited_call_names = {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
            "connect",
            "request",
            "urlopen",
            "submit_order",
            "create_order",
            "write_text",
            "write_bytes",
            "mkdir",
        }

        observed_calls: set[str] = set()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if isinstance(node.func, ast.Name):
                observed_calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                observed_calls.add(node.func.attr)

        self.assertTrue(
            prohibited_call_names.isdisjoint(observed_calls),
            sorted(prohibited_call_names & observed_calls),
        )


if __name__ == "__main__":
    unittest.main()
