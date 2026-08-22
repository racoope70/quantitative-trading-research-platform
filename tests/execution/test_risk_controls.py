"""Focused offline deterministic tests for canonical TM-031 risk controls."""

from __future__ import annotations

import ast
from copy import deepcopy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "src"
MODULE_PATH = (
    SOURCE_ROOT
    / "quantitative_trading_research"
    / "execution"
    / "risk_controls.py"
)

sys.path.insert(0, str(SOURCE_ROOT))

from quantitative_trading_research.execution.risk_controls import (
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    RiskControlError,
    evaluate_risk_controls,
    validate_risk_result,
)


class RiskControlsTests(unittest.TestCase):
    def _row(
        self,
        *,
        instrument_id: str = "SYNTHETIC_X",
        target_weight: float = 0.25,
        current_weight: float = 0.10,
        equity: float = 100_000.0,
        order_submitted: bool = False,
        observed_at_utc: str | None = None,
    ) -> dict:
        row = {
            "instrument_id": instrument_id,
            "target_weight": target_weight,
            "current_weight": current_weight,
            "equity": equity,
            "order_submitted": order_submitted,
        }

        if observed_at_utc is not None:
            row["observed_at_utc"] = observed_at_utc

        return row

    def _account(
        self,
        *,
        open_orders_count: int = 0,
        positions_count: int = 0,
    ) -> dict:
        return {
            "open_orders_count": open_orders_count,
            "positions_count": positions_count,
        }

    def _passing_result(self) -> dict:
        return evaluate_risk_controls(
            plan_rows=[self._row()],
            account_state=self._account(),
        )

    def _check(self, result: dict, name: str) -> dict:
        return next(
            check
            for check in result["checks"]
            if check["name"] == name
        )

    def test_normal_result_is_versioned_provider_neutral_and_passing(self):
        result = self._passing_result()

        self.assertEqual(SCHEMA_ID, result["schema_id"])
        self.assertEqual(SCHEMA_VERSION, result["schema_version"])
        self.assertEqual(RESULT_TYPE, result["result_type"])
        self.assertEqual(
            STATE_PROVENANCE,
            result["state_provenance"],
        )
        self.assertTrue(result["passed"])

        validate_risk_result(result)

    def test_canonical_arithmetic_is_derived_from_primitive_state(self):
        row = self._row()
        result = evaluate_risk_controls(
            plan_rows=[row],
            account_state=self._account(),
        )

        evaluated = result["evaluated_rows"][0]
        expected_delta = (
            row["target_weight"] - row["current_weight"]
        )
        expected_notional = expected_delta * row["equity"]

        self.assertEqual(
            expected_delta,
            evaluated["canonical_delta_weight"],
        )
        self.assertEqual(
            expected_notional,
            evaluated["canonical_intended_notional"],
        )

    def test_consistent_redundant_derivatives_are_accepted(self):
        row = self._row()
        delta = row["target_weight"] - row["current_weight"]

        row["intended_delta_weight"] = delta
        row["intended_notional"] = delta * row["equity"]

        result = evaluate_risk_controls(
            plan_rows=[row],
            account_state=self._account(),
        )

        self.assertTrue(result["passed"])

    def test_contradictory_delta_weight_fails_closed(self):
        row = self._row()
        row["intended_delta_weight"] = 999.0

        with self.assertRaisesRegex(
            RiskControlError,
            "intended_delta_weight.*contradicts",
        ):
            evaluate_risk_controls(
                plan_rows=[row],
                account_state=self._account(),
            )

    def test_contradictory_intended_notional_fails_closed(self):
        row = self._row()
        row["intended_notional"] = 1.0

        with self.assertRaisesRegex(
            RiskControlError,
            "intended_notional.*contradicts",
        ):
            evaluate_risk_controls(
                plan_rows=[row],
                account_state=self._account(),
            )

    def test_flat_start_rejects_nonflat_account_positions(self):
        row = self._row(current_weight=0.0)

        result = evaluate_risk_controls(
            plan_rows=[row],
            account_state=self._account(positions_count=1),
            config={"require_flat_start": True},
        )

        self.assertFalse(result["passed"])
        self.assertFalse(
            self._check(
                result,
                "account_positions_flat",
            )["passed"]
        )
        self.assertTrue(
            self._check(
                result,
                "plan_current_weights_flat",
            )["passed"]
        )

    def test_flat_start_rejects_nonflat_plan_current_weight(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row(current_weight=0.10)],
            account_state=self._account(positions_count=0),
            config={"require_flat_start": True},
        )

        self.assertFalse(result["passed"])
        self.assertTrue(
            self._check(
                result,
                "account_positions_flat",
            )["passed"]
        )
        self.assertFalse(
            self._check(
                result,
                "plan_current_weights_flat",
            )["passed"]
        )

    def test_flat_start_requires_both_account_and_plan_to_be_flat(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row(current_weight=0.0)],
            account_state=self._account(positions_count=0),
            config={"require_flat_start": True},
        )

        self.assertTrue(
            self._check(
                result,
                "account_positions_flat",
            )["passed"]
        )
        self.assertTrue(
            self._check(
                result,
                "plan_current_weights_flat",
            )["passed"]
        )
        self.assertTrue(result["passed"])

    def test_below_exact_and_above_symbol_weight_limit(self):
        cases = (
            ("below", 0.39, True),
            ("exact", 0.40, True),
            ("above", 0.41, False),
        )

        for label, target_weight, expected in cases:
            with self.subTest(label=label):
                result = evaluate_risk_controls(
                    plan_rows=[
                        self._row(
                            target_weight=target_weight,
                            current_weight=0.0,
                        )
                    ],
                    account_state=self._account(),
                    config={
                        "max_abs_symbol_weight": 0.40,
                        "max_gross_target_weight": 10.0,
                        "max_net_target_weight": 10.0,
                        "max_single_intended_notional_pct": 10.0,
                        "max_total_intended_notional_pct": 10.0,
                    },
                )

                self.assertIs(
                    expected,
                    self._check(
                        result,
                        "single_symbol_target_weight_within_limit",
                    )["passed"],
                )

    def test_below_exact_and_above_derived_notional_limit(self):
        cases = (
            ("below", 0.19, True),
            ("exact", 0.20, True),
            ("above", 0.21, False),
        )

        for label, target_weight, expected in cases:
            with self.subTest(label=label):
                result = evaluate_risk_controls(
                    plan_rows=[
                        self._row(
                            target_weight=target_weight,
                            current_weight=0.0,
                        )
                    ],
                    account_state=self._account(),
                    config={
                        "max_abs_symbol_weight": 10.0,
                        "max_gross_target_weight": 10.0,
                        "max_net_target_weight": 10.0,
                        "max_single_intended_notional_pct": 0.20,
                        "max_total_intended_notional_pct": 10.0,
                    },
                )

                self.assertIs(
                    expected,
                    self._check(
                        result,
                        "single_intended_notional_within_limit",
                    )["passed"],
                )

    def test_nonfinite_and_invalid_primitive_values_fail_closed(self):
        cases = (
            ("target_weight", float("nan")),
            ("target_weight", float("inf")),
            ("current_weight", float("-inf")),
            ("equity", float("nan")),
            ("equity", True),
            ("target_weight", "0.25"),
        )

        for field, value in cases:
            with self.subTest(field=field, value=value):
                row = self._row()
                row[field] = value

                with self.assertRaises(RiskControlError):
                    evaluate_risk_controls(
                        plan_rows=[row],
                        account_state=self._account(),
                    )

    def test_missing_open_order_state_fails_closed(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row()],
            account_state={"positions_count": 0},
        )

        check = self._check(result, "no_open_orders")

        self.assertFalse(result["passed"])
        self.assertFalse(check["passed"])
        self.assertTrue(
            check["evidence"]["required_state_missing"]
        )

    def test_missing_position_state_fails_closed_when_flat_start_required(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row(current_weight=0.0)],
            account_state={"open_orders_count": 0},
            config={"require_flat_start": True},
        )

        check = self._check(
            result,
            "account_positions_flat",
        )

        self.assertFalse(result["passed"])
        self.assertFalse(check["passed"])
        self.assertTrue(
            check["evidence"]["required_state_missing"]
        )

    def test_missing_clock_state_fails_closed_when_staleness_enabled(self):
        row = self._row(
            observed_at_utc="2026-08-21T12:00:00+00:00",
        )

        result = evaluate_risk_controls(
            plan_rows=[row],
            account_state=self._account(),
            config={"max_state_age_minutes": 30.0},
            now_utc=None,
        )

        evidence = self._check(
            result,
            "state_not_stale",
        )["evidence"]

        self.assertFalse(result["passed"])
        self.assertTrue(evidence["missing_now_utc"])

    def test_missing_timestamp_state_fails_closed_when_staleness_enabled(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row()],
            account_state=self._account(),
            config={"max_state_age_minutes": 30.0},
            now_utc="2026-08-21T12:00:00+00:00",
        )

        evidence = self._check(
            result,
            "state_not_stale",
        )["evidence"]

        self.assertFalse(result["passed"])
        self.assertEqual(1, evidence["missing_timestamp_count"])

    def test_invalid_explicit_clock_state_is_rejected(self):
        with self.assertRaises(RiskControlError):
            evaluate_risk_controls(
                plan_rows=[
                    self._row(
                        observed_at_utc=(
                            "2026-08-21T11:55:00+00:00"
                        ),
                    )
                ],
                account_state=self._account(),
                config={"max_state_age_minutes": 30.0},
                now_utc="not-a-timestamp",
            )

    def test_future_timestamp_evidence_is_explicit(self):
        result = evaluate_risk_controls(
            plan_rows=[
                self._row(
                    observed_at_utc=(
                        "2026-08-21T12:10:00+00:00"
                    ),
                )
            ],
            account_state=self._account(),
            config={"max_state_age_minutes": 30.0},
            now_utc="2026-08-21T12:00:00+00:00",
        )

        check = self._check(result, "state_not_stale")
        evidence = check["evidence"]

        self.assertFalse(check["passed"])
        self.assertEqual(
            -10.0,
            evidence["minimum_age_minutes"],
        )
        self.assertEqual(
            -10.0,
            evidence["maximum_age_minutes"],
        )
        self.assertTrue(
            evidence["future_timestamp_present"]
        )
        self.assertFalse(
            evidence["stale_timestamp_present"]
        )

    def test_stale_timestamp_evidence_is_explicit(self):
        result = evaluate_risk_controls(
            plan_rows=[
                self._row(
                    observed_at_utc=(
                        "2026-08-21T11:00:00+00:00"
                    ),
                )
            ],
            account_state=self._account(),
            config={"max_state_age_minutes": 30.0},
            now_utc="2026-08-21T12:00:00+00:00",
        )

        evidence = self._check(
            result,
            "state_not_stale",
        )["evidence"]

        self.assertEqual(
            60.0,
            evidence["minimum_age_minutes"],
        )
        self.assertEqual(
            60.0,
            evidence["maximum_age_minutes"],
        )
        self.assertFalse(
            evidence["future_timestamp_present"]
        )
        self.assertTrue(
            evidence["stale_timestamp_present"]
        )

    def test_mixed_future_and_stale_timestamp_evidence_is_explicit(self):
        rows = [
            self._row(
                instrument_id="FUTURE",
                target_weight=0.10,
                current_weight=0.0,
                observed_at_utc="2026-08-21T12:10:00+00:00",
            ),
            self._row(
                instrument_id="STALE",
                target_weight=0.10,
                current_weight=0.0,
                observed_at_utc="2026-08-21T11:00:00+00:00",
            ),
        ]

        result = evaluate_risk_controls(
            plan_rows=rows,
            account_state=self._account(),
            config={"max_state_age_minutes": 30.0},
            now_utc="2026-08-21T12:00:00+00:00",
        )

        check = self._check(result, "state_not_stale")
        evidence = check["evidence"]

        self.assertFalse(check["passed"])
        self.assertEqual(
            -10.0,
            evidence["minimum_age_minutes"],
        )
        self.assertEqual(
            60.0,
            evidence["maximum_age_minutes"],
        )
        self.assertEqual(
            30.0,
            evidence["configured_limit_minutes"],
        )
        self.assertTrue(
            evidence["future_timestamp_present"]
        )
        self.assertTrue(
            evidence["stale_timestamp_present"]
        )

    def test_unknown_check_identifier_is_rejected(self):
        result = self._passing_result()
        result["checks"][0]["name"] = "invented_check"

        with self.assertRaisesRegex(
            RiskControlError,
            "check-set mismatch",
        ):
            validate_risk_result(result)

    def test_duplicate_check_identifier_is_rejected(self):
        result = self._passing_result()
        result["checks"][1]["name"] = (
            result["checks"][0]["name"]
        )

        with self.assertRaisesRegex(
            RiskControlError,
            "duplicate check identifiers",
        ):
            validate_risk_result(result)

    def test_missing_mandatory_check_is_rejected(self):
        result = self._passing_result()
        result["checks"].pop()
        result["passed"] = all(
            check["passed"] for check in result["checks"]
        )

        with self.assertRaisesRegex(
            RiskControlError,
            "check-set mismatch",
        ):
            validate_risk_result(result)

    def test_missing_conditional_check_is_rejected(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row(current_weight=0.0)],
            account_state=self._account(),
            config={"require_flat_start": True},
        )

        result["checks"] = [
            check
            for check in result["checks"]
            if check["name"] != "plan_current_weights_flat"
        ]
        result["passed"] = all(
            check["passed"] for check in result["checks"]
        )

        with self.assertRaisesRegex(
            RiskControlError,
            "check-set mismatch",
        ):
            validate_risk_result(result)

    def test_tampered_structured_evidence_is_rejected(self):
        result = self._passing_result()
        result["checks"][0]["evidence"][
            "minimum_observed_equity"
        ] = 999_999.0

        with self.assertRaisesRegex(
            RiskControlError,
            "evidence does not match canonical evaluation",
        ):
            validate_risk_result(result)

    def test_forged_overall_pass_aggregation_is_rejected(self):
        result = evaluate_risk_controls(
            plan_rows=[self._row(order_submitted=True)],
            account_state=self._account(),
        )

        self.assertFalse(result["passed"])

        forged = deepcopy(result)
        forged["passed"] = True

        with self.assertRaisesRegex(
            RiskControlError,
            "passed does not match canonical check aggregation",
        ):
            validate_risk_result(forged)

    def test_identical_inputs_produce_identical_result_evidence(self):
        first = self._passing_result()
        second = self._passing_result()

        self.assertEqual(first, second)

    def test_static_ast_boundary_has_only_offline_stdlib_imports_and_calls(self):
        tree = ast.parse(
            MODULE_PATH.read_text(encoding="utf-8"),
            filename=str(MODULE_PATH),
        )

        allowed_import_roots = {
            "__future__",
            "datetime",
            "math",
            "typing",
        }

        imported_roots: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(
                    alias.name.split(".", 1)[0]
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imported_roots.add(
                    module.split(".", 1)[0]
                )

        self.assertLessEqual(
            imported_roots,
            allowed_import_roots,
        )

        forbidden_named_calls = {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
            "input",
        }

        forbidden_attribute_calls = {
            "connect",
            "create_connection",
            "request",
            "urlopen",
            "submit",
            "submit_order",
            "cancel_order",
            "get_account",
            "get_orders",
            "get_positions",
            "predict",
            "learn",
            "fit",
            "read_csv",
            "read_parquet",
            "write_text",
            "mkdir",
        }

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if isinstance(node.func, ast.Name):
                self.assertNotIn(
                    node.func.id,
                    forbidden_named_calls,
                )

            if isinstance(node.func, ast.Attribute):
                self.assertNotIn(
                    node.func.attr,
                    forbidden_attribute_calls,
                )

    def test_module_import_is_offline_and_side_effect_free(self):
        code = """
from unittest.mock import patch

with patch(
    "pathlib.Path.mkdir",
    side_effect=AssertionError("mkdir called"),
), patch(
    "pathlib.Path.write_text",
    side_effect=AssertionError("write called"),
), patch(
    "pathlib.Path.open",
    side_effect=AssertionError("Path.open called"),
), patch(
    "socket.socket.connect",
    side_effect=AssertionError("network connect called"),
), patch(
    "socket.create_connection",
    side_effect=AssertionError("network connection called"),
):
    import quantitative_trading_research.execution.risk_controls
"""

        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(SOURCE_ROOT)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"

        with tempfile.TemporaryDirectory() as temporary_directory:
            working_directory = Path(temporary_directory)
            before = sorted(working_directory.rglob("*"))

            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=working_directory,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            after = sorted(working_directory.rglob("*"))

        self.assertEqual(
            0,
            completed.returncode,
            msg=(
                f"stdout:\n{completed.stdout}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
