"""Pure deterministic offline execution-plan construction.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/build_execution_plan.py``.

The historical implementation translated approved target/current-position
state into rebalance order intents, but also depended on pandas, filesystem
artifacts, environment configuration, paper-trading terminology, and a legacy
execution helper that contained broker submission behavior.

This C4 module preserves only the pure provider-neutral execution-plan
responsibility. It consumes a validated passing TM-032 pre-trade eligibility
result plus explicit caller-supplied price, sizing, and timestamp evidence.

It performs no filesystem or network operations, obtains no provider or broker
state, submits no orders, performs no paper/live execution, performs no model
training or inference, and accesses no canonical dataset or final holdout.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any

from .pre_trade import (
    PreTradeEligibilityError,
    validate_pre_trade_result,
)


SCHEMA_ID = "C4_OFFLINE_EXECUTION_PLAN_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_execution_plan"
STATE_PROVENANCE = "validated_and_explicit_offline_evidence"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "plan_id",
    "plan_at_utc",
    "configuration",
    "configuration_identity",
    "pre_trade_result",
    "price_evidence",
    "intents",
    "summary",
    "submission_authorized",
    "orders_submitted",
}

_CONFIG_KEYS = {
    "min_notional",
    "allow_shorts",
    "use_fractionals",
    "qty_precision",
}

_PRICE_KEYS = {
    "instrument_id",
    "price",
    "observed_at_utc",
}

_INTENT_KEYS = {
    "intent_id",
    "instrument_id",
    "decision_id",
    "decision_identity",
    "position_identity",
    "price_identity",
    "timestamp_identity",
    "target_weight",
    "current_weight",
    "equity",
    "intended_delta_weight",
    "intended_notional",
    "price",
    "state_observed_at_utc",
    "price_observed_at_utc",
    "transition",
    "side",
    "quantity",
    "planned_notional",
    "should_order",
    "reason",
    "submission_authorized",
    "order_submitted",
}

_SUMMARY_KEYS = {
    "intent_count",
    "order_intent_count",
    "hold_count",
    "buy_count",
    "sell_count",
    "gross_requested_notional",
    "gross_planned_notional",
}


class ExecutionPlanError(ValueError):
    """Fail-closed error for malformed or unsafe execution-plan evidence."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionPlanError(f"{name} must be a dict")
    return dict(value)


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExecutionPlanError(f"{name} must be a non-empty string")
    return value


def _require_bool(name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise ExecutionPlanError(f"{name} must be a bool")
    return value


def _require_finite_number(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ExecutionPlanError(f"{name} must be a finite number")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ExecutionPlanError(f"{name} must be a finite number")
    return numeric


def _parse_utc_timestamp(name: str, value: Any) -> datetime:
    text = _require_nonempty_string(name, value)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ExecutionPlanError(
            f"{name} must be an ISO-8601 timestamp"
        ) from exc
    if parsed.tzinfo is None:
        raise ExecutionPlanError(
            f"{name} must include timezone information"
        )
    return parsed.astimezone(timezone.utc)


def _canonical_timestamp(name: str, value: Any) -> str:
    return _parse_utc_timestamp(name, value).isoformat()


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ExecutionPlanError(
            "execution-plan evidence is not canonically serializable"
        ) from exc


def _identity(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _validated_config(config: Any) -> dict[str, Any]:
    supplied = _require_mapping("configuration", config)
    if set(supplied) != _CONFIG_KEYS:
        missing = sorted(_CONFIG_KEYS - set(supplied))
        unexpected = sorted(set(supplied) - _CONFIG_KEYS)
        raise ExecutionPlanError(
            "configuration keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    min_notional = _require_finite_number(
        "configuration.min_notional",
        supplied["min_notional"],
    )
    if min_notional < 0:
        raise ExecutionPlanError(
            "configuration.min_notional must be non-negative"
        )

    allow_shorts = _require_bool(
        "configuration.allow_shorts",
        supplied["allow_shorts"],
    )
    use_fractionals = _require_bool(
        "configuration.use_fractionals",
        supplied["use_fractionals"],
    )

    qty_precision = supplied["qty_precision"]
    if type(qty_precision) is not int or qty_precision < 0 or qty_precision > 12:
        raise ExecutionPlanError(
            "configuration.qty_precision must be an integer from 0 through 12"
        )

    return {
        "min_notional": min_notional,
        "allow_shorts": allow_shorts,
        "use_fractionals": use_fractionals,
        "qty_precision": qty_precision,
    }


def _validated_prices(
    price_evidence: Any,
    *,
    expected_instruments: set[str],
    plan_at: datetime,
) -> list[dict[str, Any]]:
    if not isinstance(price_evidence, list):
        raise ExecutionPlanError("price_evidence must be a list")
    if not price_evidence:
        raise ExecutionPlanError("price_evidence must not be empty")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, raw in enumerate(price_evidence):
        row = _require_mapping(f"price_evidence[{index}]", raw)
        if set(row) != _PRICE_KEYS:
            raise ExecutionPlanError(
                f"price_evidence[{index}] keys mismatch"
            )

        instrument_id = _require_nonempty_string(
            f"price_evidence[{index}].instrument_id",
            row["instrument_id"],
        )
        if instrument_id in seen:
            raise ExecutionPlanError(
                f"duplicate price instrument_id: {instrument_id}"
            )
        seen.add(instrument_id)

        price = _require_finite_number(
            f"price_evidence[{index}].price",
            row["price"],
        )
        if price <= 0:
            raise ExecutionPlanError(
                f"price_evidence[{index}].price must be positive"
            )

        observed_text = _canonical_timestamp(
            f"price_evidence[{index}].observed_at_utc",
            row["observed_at_utc"],
        )
        observed = _parse_utc_timestamp(
            f"price_evidence[{index}].observed_at_utc",
            observed_text,
        )
        if observed > plan_at:
            raise ExecutionPlanError(
                f"price_evidence[{index}] is future-dated"
            )

        normalized.append(
            {
                "instrument_id": instrument_id,
                "price": price,
                "observed_at_utc": observed_text,
            }
        )

    if seen != expected_instruments:
        missing = sorted(expected_instruments - seen)
        unexpected = sorted(seen - expected_instruments)
        raise ExecutionPlanError(
            "price instrument set mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    return normalized


def _transition(current_weight: float, target_weight: float) -> str:
    if target_weight == current_weight:
        return "HOLD"

    if current_weight == 0:
        return "OPEN_LONG" if target_weight > 0 else "OPEN_SHORT"

    if current_weight > 0:
        if target_weight > current_weight:
            return "INCREASE_LONG"
        if target_weight > 0:
            return "REDUCE_LONG"
        if target_weight == 0:
            return "FLATTEN_LONG"
        return "CROSS_LONG_TO_SHORT"

    if target_weight < current_weight:
        return "INCREASE_SHORT"
    if target_weight < 0:
        return "REDUCE_SHORT"
    if target_weight == 0:
        return "FLATTEN_SHORT"
    return "CROSS_SHORT_TO_LONG"


def _rounded_quantity(
    requested_quantity: float,
    *,
    use_fractionals: bool,
    qty_precision: int,
) -> float:
    if use_fractionals:
        return float(round(requested_quantity, qty_precision))
    return float(math.floor(requested_quantity))


def _intent_from_evidence(
    *,
    decision: dict[str, Any],
    risk_row: dict[str, Any],
    price_row: dict[str, Any],
    config: dict[str, Any],
    configuration_identity: str,
    plan_at_utc: str,
    plan_at: datetime,
) -> dict[str, Any]:
    instrument_id = decision["instrument_id"]

    if "observed_at_utc" not in risk_row:
        raise ExecutionPlanError(
            f"risk state timestamp missing for {instrument_id}"
        )

    state_observed_at_utc = _canonical_timestamp(
        f"risk state {instrument_id}.observed_at_utc",
        risk_row["observed_at_utc"],
    )
    state_observed = _parse_utc_timestamp(
        f"risk state {instrument_id}.observed_at_utc",
        state_observed_at_utc,
    )
    if state_observed > plan_at:
        raise ExecutionPlanError(
            f"risk state is future-dated for {instrument_id}"
        )

    target_weight = _require_finite_number(
        f"{instrument_id}.target_weight",
        decision["target_weight"],
    )
    current_weight = _require_finite_number(
        f"{instrument_id}.current_weight",
        decision["current_weight"],
    )
    equity = _require_finite_number(
        f"{instrument_id}.equity",
        decision["equity"],
    )
    if equity <= 0:
        raise ExecutionPlanError(
            f"equity must be positive for {instrument_id}"
        )

    intended_delta_weight = _require_finite_number(
        f"{instrument_id}.intended_delta_weight",
        decision["intended_delta_weight"],
    )
    intended_notional = _require_finite_number(
        f"{instrument_id}.intended_notional",
        decision["intended_notional"],
    )

    if target_weight < 0 and not config["allow_shorts"]:
        raise ExecutionPlanError(
            f"negative target requires allow_shorts for {instrument_id}"
        )

    price = price_row["price"]
    price_observed_at_utc = price_row["observed_at_utc"]

    transition = _transition(current_weight, target_weight)

    side = "HOLD"
    should_order = False
    quantity = 0.0
    planned_notional = 0.0
    reason = "NO_EXPOSURE_CHANGE"

    abs_notional = abs(intended_notional)

    if intended_notional != 0:
        if abs_notional < config["min_notional"]:
            reason = "BELOW_MIN_NOTIONAL"
        else:
            requested_quantity = abs_notional / price
            quantity = _rounded_quantity(
                requested_quantity,
                use_fractionals=config["use_fractionals"],
                qty_precision=config["qty_precision"],
            )

            if quantity <= 0:
                quantity = 0.0
                reason = "ROUNDED_QUANTITY_ZERO"
            else:
                side = "BUY" if intended_notional > 0 else "SELL"
                should_order = True
                reason = "REBALANCE_REQUIRED"
                planned_notional = (
                    quantity * price
                    if side == "BUY"
                    else -(quantity * price)
                )

    decision_identity = _identity("decision", decision)
    position_identity = _identity("position", risk_row)
    price_identity = _identity("price", price_row)
    timestamp_identity = _identity(
        "timestamps",
        {
            "state_observed_at_utc": state_observed_at_utc,
            "price_observed_at_utc": price_observed_at_utc,
            "plan_at_utc": plan_at_utc,
        },
    )

    identity_basis = {
        "instrument_id": instrument_id,
        "decision_identity": decision_identity,
        "position_identity": position_identity,
        "price_identity": price_identity,
        "configuration_identity": configuration_identity,
        "timestamp_identity": timestamp_identity,
    }
    intent_id = _identity("intent", identity_basis)

    return {
        "intent_id": intent_id,
        "instrument_id": instrument_id,
        "decision_id": decision["decision_id"],
        "decision_identity": decision_identity,
        "position_identity": position_identity,
        "price_identity": price_identity,
        "timestamp_identity": timestamp_identity,
        "target_weight": target_weight,
        "current_weight": current_weight,
        "equity": equity,
        "intended_delta_weight": intended_delta_weight,
        "intended_notional": intended_notional,
        "price": price,
        "state_observed_at_utc": state_observed_at_utc,
        "price_observed_at_utc": price_observed_at_utc,
        "transition": transition,
        "side": side,
        "quantity": quantity,
        "planned_notional": planned_notional,
        "should_order": should_order,
        "reason": reason,
        "submission_authorized": False,
        "order_submitted": False,
    }


def _summary(intents: list[dict[str, Any]]) -> dict[str, Any]:
    order_intents = [
        intent for intent in intents if intent["should_order"]
    ]
    return {
        "intent_count": len(intents),
        "order_intent_count": len(order_intents),
        "hold_count": sum(
            1 for intent in intents if not intent["should_order"]
        ),
        "buy_count": sum(
            1 for intent in order_intents if intent["side"] == "BUY"
        ),
        "sell_count": sum(
            1 for intent in order_intents if intent["side"] == "SELL"
        ),
        "gross_requested_notional": sum(
            abs(intent["intended_notional"])
            for intent in order_intents
        ),
        "gross_planned_notional": sum(
            abs(intent["planned_notional"])
            for intent in order_intents
        ),
    }


def build_execution_plan(
    *,
    pre_trade_result: dict[str, Any],
    price_evidence: list[dict[str, Any]],
    configuration: dict[str, Any],
    plan_at_utc: str,
) -> dict[str, Any]:
    """Build one deterministic provider-neutral NO_SUBMIT execution plan."""
    normalized_pre_trade = deepcopy(
        _require_mapping("pre_trade_result", pre_trade_result)
    )

    try:
        validate_pre_trade_result(normalized_pre_trade)
    except PreTradeEligibilityError as exc:
        raise ExecutionPlanError(
            f"pre_trade_result is invalid: {exc}"
        ) from exc

    if normalized_pre_trade["passed"] is not True:
        raise ExecutionPlanError(
            "pre_trade_result must pass before plan construction"
        )

    normalized_plan_at = _canonical_timestamp(
        "plan_at_utc",
        plan_at_utc,
    )
    plan_at = _parse_utc_timestamp(
        "plan_at_utc",
        normalized_plan_at,
    )

    config = _validated_config(configuration)
    configuration_identity = _identity("configuration", config)

    decisions = normalized_pre_trade["decisions"]
    risk_rows = normalized_pre_trade["risk_result"]["evaluated_rows"]

    decision_instruments = {
        decision["instrument_id"] for decision in decisions
    }

    prices = _validated_prices(
        price_evidence,
        expected_instruments=decision_instruments,
        plan_at=plan_at,
    )

    risk_by_instrument = {
        row["instrument_id"]: row
        for row in risk_rows
    }
    price_by_instrument = {
        row["instrument_id"]: row
        for row in prices
    }

    intents = [
        _intent_from_evidence(
            decision=decision,
            risk_row=risk_by_instrument[decision["instrument_id"]],
            price_row=price_by_instrument[decision["instrument_id"]],
            config=config,
            configuration_identity=configuration_identity,
            plan_at_utc=normalized_plan_at,
            plan_at=plan_at,
        )
        for decision in decisions
    ]

    summary = _summary(intents)

    plan_id = _identity(
        "plan",
        {
            "plan_at_utc": normalized_plan_at,
            "configuration_identity": configuration_identity,
            "pre_trade_result": normalized_pre_trade,
            "price_evidence": prices,
            "intent_ids": [
                intent["intent_id"]
                for intent in intents
            ],
        },
    )

    result = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": True,
        "plan_id": plan_id,
        "plan_at_utc": normalized_plan_at,
        "configuration": config,
        "configuration_identity": configuration_identity,
        "pre_trade_result": normalized_pre_trade,
        "price_evidence": prices,
        "intents": intents,
        "summary": summary,
        "submission_authorized": False,
        "orders_submitted": 0,
    }

    validate_execution_plan(result)
    return result


def validate_execution_plan(result: Any) -> None:
    """Reject malformed, operational, inconsistent, or forged plan evidence."""
    if not isinstance(result, dict):
        raise ExecutionPlanError("execution plan must be a dict")

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise ExecutionPlanError(
            "execution-plan keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise ExecutionPlanError("unsupported execution-plan schema_id")
    if type(result["schema_version"]) is not int:
        raise ExecutionPlanError(
            "execution-plan schema_version must be an int"
        )
    if result["schema_version"] != SCHEMA_VERSION:
        raise ExecutionPlanError(
            "unsupported execution-plan schema_version"
        )
    if result["result_type"] != RESULT_TYPE:
        raise ExecutionPlanError("unsupported execution-plan result_type")
    if result["state_provenance"] != STATE_PROVENANCE:
        raise ExecutionPlanError(
            "execution-plan state provenance is invalid"
        )
    if result["passed"] is not True:
        raise ExecutionPlanError(
            "execution-plan passed must remain True"
        )
    if result["submission_authorized"] is not False:
        raise ExecutionPlanError(
            "execution-plan submission_authorized must remain False"
        )
    if type(result["orders_submitted"]) is not int:
        raise ExecutionPlanError(
            "execution-plan orders_submitted must be an int"
        )
    if result["orders_submitted"] != 0:
        raise ExecutionPlanError(
            "execution-plan orders_submitted must remain zero"
        )

    expected = build_execution_plan.__wrapped__(result) if False else None
    del expected

    normalized_pre_trade = deepcopy(
        _require_mapping(
            "execution-plan pre_trade_result",
            result["pre_trade_result"],
        )
    )
    try:
        validate_pre_trade_result(normalized_pre_trade)
    except PreTradeEligibilityError as exc:
        raise ExecutionPlanError(
            f"execution-plan pre_trade_result is invalid: {exc}"
        ) from exc
    if normalized_pre_trade["passed"] is not True:
        raise ExecutionPlanError(
            "execution-plan pre_trade_result must remain passing"
        )

    normalized_plan_at = _canonical_timestamp(
        "execution-plan plan_at_utc",
        result["plan_at_utc"],
    )
    plan_at = _parse_utc_timestamp(
        "execution-plan plan_at_utc",
        normalized_plan_at,
    )

    config = _validated_config(result["configuration"])
    configuration_identity = _identity("configuration", config)
    if result["configuration_identity"] != configuration_identity:
        raise ExecutionPlanError(
            "configuration_identity does not match configuration"
        )

    decisions = normalized_pre_trade["decisions"]
    risk_rows = normalized_pre_trade["risk_result"]["evaluated_rows"]
    decision_instruments = {
        decision["instrument_id"] for decision in decisions
    }

    prices = _validated_prices(
        result["price_evidence"],
        expected_instruments=decision_instruments,
        plan_at=plan_at,
    )

    risk_by_instrument = {
        row["instrument_id"]: row
        for row in risk_rows
    }
    price_by_instrument = {
        row["instrument_id"]: row
        for row in prices
    }

    expected_intents = [
        _intent_from_evidence(
            decision=decision,
            risk_row=risk_by_instrument[decision["instrument_id"]],
            price_row=price_by_instrument[decision["instrument_id"]],
            config=config,
            configuration_identity=configuration_identity,
            plan_at_utc=normalized_plan_at,
            plan_at=plan_at,
        )
        for decision in decisions
    ]

    intents = result["intents"]
    if not isinstance(intents, list):
        raise ExecutionPlanError(
            "execution-plan intents must be a list"
        )
    for index, intent in enumerate(intents):
        if not isinstance(intent, dict):
            raise ExecutionPlanError(
                f"execution-plan intents[{index}] must be a dict"
            )
        if set(intent) != _INTENT_KEYS:
            raise ExecutionPlanError(
                f"execution-plan intents[{index}] keys mismatch"
            )

    if intents != expected_intents:
        raise ExecutionPlanError(
            "execution-plan intents do not match canonical reconstruction"
        )

    summary = result["summary"]
    if not isinstance(summary, dict) or set(summary) != _SUMMARY_KEYS:
        raise ExecutionPlanError(
            "execution-plan summary keys mismatch"
        )
    expected_summary = _summary(expected_intents)
    if summary != expected_summary:
        raise ExecutionPlanError(
            "execution-plan summary does not match canonical reconstruction"
        )

    expected_plan_id = _identity(
        "plan",
        {
            "plan_at_utc": normalized_plan_at,
            "configuration_identity": configuration_identity,
            "pre_trade_result": normalized_pre_trade,
            "price_evidence": prices,
            "intent_ids": [
                intent["intent_id"]
                for intent in expected_intents
            ],
        },
    )
    if result["plan_id"] != expected_plan_id:
        raise ExecutionPlanError(
            "plan_id does not match canonical plan evidence"
        )
