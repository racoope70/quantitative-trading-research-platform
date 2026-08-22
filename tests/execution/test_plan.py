"""Focused tests for the C4 pure offline execution-plan contract."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.no_submit_decision import (
    build_no_submit_decision,
)
from quantitative_trading_research.execution.plan import (
    ExecutionPlanError,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    build_execution_plan,
    validate_execution_plan,
)
from quantitative_trading_research.execution.pre_trade import (
    evaluate_pre_trade_eligibility,
)
from quantitative_trading_research.execution.risk_controls import (
    evaluate_risk_controls,
)


PLAN_AT = "2026-08-22T15:02:00+00:00"
STATE_AT = "2026-08-22T15:00:00+00:00"
PRICE_AT = "2026-08-22T15:01:00+00:00"


def _configuration(
    *,
    min_notional: float = 25.0,
    allow_shorts: bool = True,
    use_fractionals: bool = True,
    qty_precision: int = 6,
) -> dict:
    return {
        "min_notional": min_notional,
        "allow_shorts": allow_shorts,
        "use_fractionals": use_fractionals,
        "qty_precision": qty_precision,
    }


def _pre_trade(
    *,
    rows: list[dict] | None = None,
    include_state_timestamp: bool = True,
) -> dict:
    raw_rows = rows or [
        {
            "instrument_id": "AAA",
            "target_weight": 0.20,
            "current_weight": 0.05,
            "equity": 100_000.0,
        }
    ]

    risk_rows: list[dict] = []
    for row in raw_rows:
        risk_row = {
            "instrument_id": row["instrument_id"],
            "target_weight": row["target_weight"],
            "current_weight": row["current_weight"],
            "equity": row["equity"],
            "order_submitted": False,
        }
        if include_state_timestamp:
            risk_row["observed_at_utc"] = row.get(
                "observed_at_utc",
                STATE_AT,
            )
        risk_rows.append(risk_row)

    risk = evaluate_risk_controls(
        plan_rows=risk_rows,
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


def _prices(
    instruments: tuple[str, ...] = ("AAA",),
    *,
    price: float = 100.0,
    observed_at_utc: str = PRICE_AT,
) -> list[dict]:
    return [
        {
            "instrument_id": instrument,
            "price": price,
            "observed_at_utc": observed_at_utc,
        }
        for instrument in instruments
    ]


def _build(
    *,
    rows: list[dict] | None = None,
    prices: list[dict] | None = None,
    configuration: dict | None = None,
    plan_at_utc: str = PLAN_AT,
    include_state_timestamp: bool = True,
) -> dict:
    pre_trade = _pre_trade(
        rows=rows,
        include_state_timestamp=include_state_timestamp,
    )

    instruments = tuple(
        decision["instrument_id"]
        for decision in pre_trade["decisions"]
    )

    return build_execution_plan(
        pre_trade_result=pre_trade,
        price_evidence=(
            _prices(instruments)
            if prices is None
            else prices
        ),
        configuration=(
            _configuration()
            if configuration is None
            else configuration
        ),
        plan_at_utc=plan_at_utc,
    )


class ExecutionPlanTests(unittest.TestCase):
    def test_normal_plan_is_versioned_offline_and_no_submit(self):
        result = _build()

        self.assertEqual(result["schema_id"], SCHEMA_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            result["result_type"],
            "offline_execution_plan",
        )
        self.assertEqual(
            result["state_provenance"],
            STATE_PROVENANCE,
        )
        self.assertTrue(result["passed"])
        self.assertFalse(result["submission_authorized"])
        self.assertEqual(result["orders_submitted"], 0)

        intent = result["intents"][0]
        self.assertEqual(intent["transition"], "INCREASE_LONG")
        self.assertEqual(intent["side"], "BUY")
        self.assertTrue(intent["should_order"])
        self.assertEqual(intent["reason"], "REBALANCE_REQUIRED")
        self.assertFalse(intent["submission_authorized"])
        self.assertFalse(intent["order_submitted"])

        validate_execution_plan(result)

    def test_historical_rebalance_arithmetic_is_preserved(self):
        result = _build()
        intent = result["intents"][0]

        self.assertAlmostEqual(
            intent["intended_delta_weight"],
            0.15,
        )
        self.assertAlmostEqual(
            intent["intended_notional"],
            15_000.0,
        )
        self.assertEqual(intent["quantity"], 150.0)
        self.assertEqual(intent["planned_notional"], 15_000.0)

    def test_identical_inputs_produce_identical_plan_and_ids(self):
        first = _build()
        second = _build()

        self.assertEqual(first, second)
        self.assertEqual(first["plan_id"], second["plan_id"])
        self.assertEqual(
            first["intents"][0]["intent_id"],
            second["intents"][0]["intent_id"],
        )

    def test_plan_does_not_mutate_caller_inputs(self):
        pre_trade = _pre_trade()
        prices = _prices()
        configuration = _configuration()

        original_pre_trade = deepcopy(pre_trade)
        original_prices = deepcopy(prices)
        original_configuration = deepcopy(configuration)

        build_execution_plan(
            pre_trade_result=pre_trade,
            price_evidence=prices,
            configuration=configuration,
            plan_at_utc=PLAN_AT,
        )

        self.assertEqual(pre_trade, original_pre_trade)
        self.assertEqual(prices, original_prices)
        self.assertEqual(
            configuration,
            original_configuration,
        )

    def test_long_short_flatten_and_crossing_transitions(self):
        cases = [
            (0.00, 0.20, "OPEN_LONG", "BUY"),
            (0.10, 0.20, "INCREASE_LONG", "BUY"),
            (0.20, 0.10, "REDUCE_LONG", "SELL"),
            (0.20, 0.00, "FLATTEN_LONG", "SELL"),
            (0.20, -0.10, "CROSS_LONG_TO_SHORT", "SELL"),
            (0.00, -0.20, "OPEN_SHORT", "SELL"),
            (-0.10, -0.20, "INCREASE_SHORT", "SELL"),
            (-0.20, -0.10, "REDUCE_SHORT", "BUY"),
            (-0.20, 0.00, "FLATTEN_SHORT", "BUY"),
            (-0.20, 0.10, "CROSS_SHORT_TO_LONG", "BUY"),
        ]

        for current, target, transition, side in cases:
            with self.subTest(
                current=current,
                target=target,
                transition=transition,
            ):
                result = _build(
                    rows=[
                        {
                            "instrument_id": "AAA",
                            "target_weight": target,
                            "current_weight": current,
                            "equity": 100_000.0,
                        }
                    ]
                )
                intent = result["intents"][0]
                self.assertEqual(
                    intent["transition"],
                    transition,
                )
                self.assertEqual(intent["side"], side)
                self.assertTrue(intent["should_order"])

    def test_no_exposure_change_is_hold(self):
        result = _build(
            rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.10,
                    "current_weight": 0.10,
                    "equity": 100_000.0,
                }
            ]
        )

        intent = result["intents"][0]

        self.assertEqual(intent["transition"], "HOLD")
        self.assertEqual(intent["side"], "HOLD")
        self.assertEqual(intent["quantity"], 0.0)
        self.assertEqual(intent["planned_notional"], 0.0)
        self.assertFalse(intent["should_order"])
        self.assertEqual(intent["reason"], "NO_EXPOSURE_CHANGE")

    def test_below_exact_and_above_min_notional_boundary(self):
        cases = [
            (0.024, False, "BELOW_MIN_NOTIONAL"),
            (0.025, True, "REBALANCE_REQUIRED"),
            (0.026, True, "REBALANCE_REQUIRED"),
        ]

        for target, should_order, reason in cases:
            with self.subTest(target=target):
                result = _build(
                    rows=[
                        {
                            "instrument_id": "AAA",
                            "target_weight": target,
                            "current_weight": 0.0,
                            "equity": 1_000.0,
                        }
                    ],
                    configuration=_configuration(
                        min_notional=25.0,
                    ),
                )

                intent = result["intents"][0]
                self.assertIs(
                    intent["should_order"],
                    should_order,
                )
                self.assertEqual(intent["reason"], reason)

    def test_fractional_quantity_rounding_is_deterministic(self):
        result = _build(
            rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.10,
                    "current_weight": 0.0,
                    "equity": 1_000.0,
                }
            ],
            prices=_prices(price=30.0),
            configuration=_configuration(
                min_notional=0.0,
                use_fractionals=True,
                qty_precision=2,
            ),
        )

        self.assertEqual(
            result["intents"][0]["quantity"],
            3.33,
        )

    def test_whole_share_quantity_is_floored(self):
        result = _build(
            rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.10,
                    "current_weight": 0.0,
                    "equity": 1_000.0,
                }
            ],
            prices=_prices(price=30.0),
            configuration=_configuration(
                min_notional=0.0,
                use_fractionals=False,
                qty_precision=6,
            ),
        )

        self.assertEqual(
            result["intents"][0]["quantity"],
            3.0,
        )
        self.assertEqual(
            result["intents"][0]["planned_notional"],
            90.0,
        )

    def test_whole_share_rounding_to_zero_holds(self):
        result = _build(
            rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.01,
                    "current_weight": 0.0,
                    "equity": 1_000.0,
                }
            ],
            prices=_prices(price=100.0),
            configuration=_configuration(
                min_notional=0.0,
                use_fractionals=False,
            ),
        )

        intent = result["intents"][0]

        self.assertFalse(intent["should_order"])
        self.assertEqual(intent["quantity"], 0.0)
        self.assertEqual(
            intent["reason"],
            "ROUNDED_QUANTITY_ZERO",
        )

    def test_negative_target_requires_explicit_short_permission(self):
        with self.assertRaises(ExecutionPlanError):
            _build(
                rows=[
                    {
                        "instrument_id": "AAA",
                        "target_weight": -0.10,
                        "current_weight": 0.0,
                        "equity": 100_000.0,
                    }
                ],
                configuration=_configuration(
                    allow_shorts=False,
                ),
            )

    def test_missing_state_timestamp_fails_closed(self):
        with self.assertRaises(ExecutionPlanError):
            _build(include_state_timestamp=False)

    def test_future_state_timestamp_fails_closed(self):
        with self.assertRaises(ExecutionPlanError):
            _build(
                rows=[
                    {
                        "instrument_id": "AAA",
                        "target_weight": 0.20,
                        "current_weight": 0.05,
                        "equity": 100_000.0,
                        "observed_at_utc":
                            "2026-08-22T15:03:00+00:00",
                    }
                ]
            )

    def test_future_price_timestamp_fails_closed(self):
        with self.assertRaises(ExecutionPlanError):
            _build(
                prices=_prices(
                    observed_at_utc=
                        "2026-08-22T15:03:00+00:00",
                )
            )

    def test_naive_or_malformed_plan_timestamp_fails_closed(self):
        for value in (
            "2026-08-22T15:02:00",
            "not-a-timestamp",
            "",
        ):
            with self.subTest(value=value):
                with self.assertRaises(ExecutionPlanError):
                    _build(plan_at_utc=value)

    def test_price_evidence_requires_exact_instrument_set(self):
        rows = [
            {
                "instrument_id": "AAA",
                "target_weight": 0.10,
                "current_weight": 0.0,
                "equity": 100_000.0,
            },
            {
                "instrument_id": "BBB",
                "target_weight": 0.10,
                "current_weight": 0.0,
                "equity": 100_000.0,
            },
        ]

        with self.assertRaises(ExecutionPlanError):
            _build(
                rows=rows,
                prices=_prices(("AAA",)),
            )

        with self.assertRaises(ExecutionPlanError):
            _build(
                rows=rows,
                prices=_prices(("AAA", "BBB", "CCC")),
            )

    def test_duplicate_price_instrument_fails_closed(self):
        with self.assertRaises(ExecutionPlanError):
            _build(
                prices=[
                    {
                        "instrument_id": "AAA",
                        "price": 100.0,
                        "observed_at_utc": PRICE_AT,
                    },
                    {
                        "instrument_id": "AAA",
                        "price": 101.0,
                        "observed_at_utc": PRICE_AT,
                    },
                ]
            )

    def test_invalid_prices_fail_closed(self):
        for bad_price in (
            0.0,
            -1.0,
            float("inf"),
            float("nan"),
            "100",
            True,
        ):
            with self.subTest(price=bad_price):
                with self.assertRaises(ExecutionPlanError):
                    _build(
                        prices=_prices(price=bad_price)
                    )

    def test_price_schema_rejects_missing_and_unexpected_fields(self):
        missing = _prices()
        del missing[0]["price"]

        with self.assertRaises(ExecutionPlanError):
            _build(prices=missing)

        unexpected = _prices()
        unexpected[0]["provider"] = "forbidden"

        with self.assertRaises(ExecutionPlanError):
            _build(prices=unexpected)

    def test_configuration_fails_closed_on_malformed_values(self):
        bad_configurations = [
            {
                "min_notional": -1.0,
                "allow_shorts": True,
                "use_fractionals": True,
                "qty_precision": 6,
            },
            {
                "min_notional": 25.0,
                "allow_shorts": 1,
                "use_fractionals": True,
                "qty_precision": 6,
            },
            {
                "min_notional": 25.0,
                "allow_shorts": True,
                "use_fractionals": "yes",
                "qty_precision": 6,
            },
            {
                "min_notional": 25.0,
                "allow_shorts": True,
                "use_fractionals": True,
                "qty_precision": -1,
            },
            {
                "min_notional": 25.0,
                "allow_shorts": True,
                "use_fractionals": True,
                "qty_precision": 13,
            },
        ]

        for configuration in bad_configurations:
            with self.subTest(configuration=configuration):
                with self.assertRaises(ExecutionPlanError):
                    _build(configuration=configuration)

    def test_configuration_requires_exact_schema(self):
        missing = _configuration()
        del missing["qty_precision"]

        with self.assertRaises(ExecutionPlanError):
            _build(configuration=missing)

        unexpected = _configuration()
        unexpected["broker"] = "forbidden"

        with self.assertRaises(ExecutionPlanError):
            _build(configuration=unexpected)

    def test_failed_pre_trade_result_is_rejected(self):
        pre_trade = _pre_trade()
        failed = deepcopy(pre_trade)
        failed["passed"] = False

        with self.assertRaises(ExecutionPlanError):
            build_execution_plan(
                pre_trade_result=failed,
                price_evidence=_prices(),
                configuration=_configuration(),
                plan_at_utc=PLAN_AT,
            )

    def test_tampered_upstream_pre_trade_evidence_is_rejected(self):
        pre_trade = _pre_trade()
        tampered = deepcopy(pre_trade)
        tampered["decisions"][0]["order_submitted"] = True

        with self.assertRaises(ExecutionPlanError):
            build_execution_plan(
                pre_trade_result=tampered,
                price_evidence=_prices(),
                configuration=_configuration(),
                plan_at_utc=PLAN_AT,
            )

    def test_validator_rejects_operational_mutations(self):
        result = _build()

        authorized = deepcopy(result)
        authorized["submission_authorized"] = True
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(authorized)

        submitted = deepcopy(result)
        submitted["orders_submitted"] = 1
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(submitted)

        intent_submitted = deepcopy(result)
        intent_submitted["intents"][0]["order_submitted"] = True
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(intent_submitted)

    def test_validator_rejects_tampered_intent_and_summary(self):
        result = _build()

        bad_intent = deepcopy(result)
        bad_intent["intents"][0]["quantity"] += 1.0
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(bad_intent)

        bad_summary = deepcopy(result)
        bad_summary["summary"]["buy_count"] += 1
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(bad_summary)

    def test_validator_rejects_forged_plan_and_configuration_ids(self):
        result = _build()

        bad_plan_id = deepcopy(result)
        bad_plan_id["plan_id"] = "plan:forged"
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(bad_plan_id)

        bad_configuration_id = deepcopy(result)
        bad_configuration_id["configuration_identity"] = (
            "configuration:forged"
        )
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(bad_configuration_id)

    def test_validator_rejects_missing_and_unexpected_top_level_keys(self):
        result = _build()

        missing = deepcopy(result)
        del missing["summary"]
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(missing)

        unexpected = deepcopy(result)
        unexpected["broker_order"] = {}
        with self.assertRaises(ExecutionPlanError):
            validate_execution_plan(unexpected)

    def test_identity_changes_when_material_plan_evidence_changes(self):
        base = _build()

        changed_price = _build(
            prices=_prices(price=101.0)
        )
        self.assertNotEqual(
            base["plan_id"],
            changed_price["plan_id"],
        )
        self.assertNotEqual(
            base["intents"][0]["intent_id"],
            changed_price["intents"][0]["intent_id"],
        )

        changed_configuration = _build(
            configuration=_configuration(
                qty_precision=5,
            )
        )
        self.assertNotEqual(
            base["plan_id"],
            changed_configuration["plan_id"],
        )
        self.assertNotEqual(
            base["configuration_identity"],
            changed_configuration["configuration_identity"],
        )

        changed_timestamp = _build(
            plan_at_utc="2026-08-22T15:02:30+00:00"
        )
        self.assertNotEqual(
            base["plan_id"],
            changed_timestamp["plan_id"],
        )
        self.assertNotEqual(
            base["intents"][0]["timestamp_identity"],
            changed_timestamp["intents"][0]["timestamp_identity"],
        )

    def test_summary_is_reconstructed_from_intents(self):
        result = _build(
            rows=[
                {
                    "instrument_id": "AAA",
                    "target_weight": 0.20,
                    "current_weight": 0.00,
                    "equity": 100_000.0,
                },
                {
                    "instrument_id": "BBB",
                    "target_weight": 0.00,
                    "current_weight": 0.10,
                    "equity": 100_000.0,
                },
                {
                    "instrument_id": "CCC",
                    "target_weight": 0.10,
                    "current_weight": 0.10,
                    "equity": 100_000.0,
                },
            ],
            prices=_prices(
                ("AAA", "BBB", "CCC"),
            ),
        )

        summary = result["summary"]

        self.assertEqual(summary["intent_count"], 3)
        self.assertEqual(summary["order_intent_count"], 2)
        self.assertEqual(summary["hold_count"], 1)
        self.assertEqual(summary["buy_count"], 1)
        self.assertEqual(summary["sell_count"], 1)
        self.assertAlmostEqual(
            summary["gross_requested_notional"],
            30_000.0,
        )
        self.assertAlmostEqual(
            summary["gross_planned_notional"],
            30_000.0,
        )

    def test_historical_attribution_is_immutable_and_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "plan.py"
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
            "src/paper_trading/build_execution_plan.py",
            source,
        )

    def test_static_ast_boundary_is_offline_and_non_operational(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "plan.py"
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
            "submit_market_order",
            "trading_client",
            "submit_order",
            "paper_trade",
            "live_trade",
            "requests.",
            "socket.",
        )
        for token in prohibited_tokens:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
