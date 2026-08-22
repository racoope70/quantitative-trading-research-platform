"""Pure deterministic offline execution-plan filtering.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/filter_execution_plan.py``.

The historical implementation selected exactly one reviewed executable row
from an execution plan while retaining the other rows for audit visibility and
disabling non-selected executable rows. It also depended on pandas, CSV/JSON
filesystem artifacts, support-file copying, CLI behavior, paper-trading paths,
and implicit wall-clock access.

This C4 module preserves only the pure provider-neutral filtering
responsibility. It consumes a validated canonical TM-062 offline execution
plan plus explicit caller-supplied selection and timestamp evidence.

It performs no filesystem or network operations, obtains no provider or broker
state, submits no orders, performs no paper/live execution, performs no model
training or inference, and accesses no canonical dataset or final holdout.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from typing import Any

from .plan import (
    ExecutionPlanError,
    validate_execution_plan,
)


SCHEMA_ID = "C4_OFFLINE_EXECUTION_PLAN_FILTER_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_execution_plan_filter"
STATE_PROVENANCE = "validated_execution_plan_and_explicit_selection_evidence"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "filter_id",
    "filtered_at_utc",
    "source_plan_id",
    "selection_criteria",
    "selection_identity",
    "selected_intent_id",
    "source_execution_plan",
    "filtered_intents",
    "summary",
    "submission_authorized",
    "orders_submitted",
}

_SELECTION_KEYS = {
    "instrument_id",
    "side",
}

_FILTERED_INTENT_KEYS = {
    "source_intent_id",
    "instrument_id",
    "decision_id",
    "source_should_order",
    "source_side",
    "source_quantity",
    "source_planned_notional",
    "selected",
    "enabled",
    "effective_side",
    "effective_quantity",
    "effective_planned_notional",
    "filter_reason",
    "submission_authorized",
    "order_submitted",
}

_SUMMARY_KEYS = {
    "source_intent_count",
    "source_executable_intent_count",
    "source_hold_intent_count",
    "audit_intent_count",
    "enabled_intent_count",
    "disabled_executable_intent_count",
    "enabled_buy_count",
    "enabled_sell_count",
    "gross_enabled_planned_notional",
}


class ExecutionPlanFilterError(ValueError):
    """Fail-closed error for malformed or unsafe filtered-plan evidence."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionPlanFilterError(f"{name} must be a dict")
    return dict(value)


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExecutionPlanFilterError(
            f"{name} must be a non-empty string"
        )
    return value.strip()


def _parse_utc_timestamp(name: str, value: Any) -> datetime:
    text = _require_nonempty_string(name, value)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ExecutionPlanFilterError(
            f"{name} must be an ISO-8601 timestamp"
        ) from exc

    if parsed.tzinfo is None:
        raise ExecutionPlanFilterError(
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
        raise ExecutionPlanFilterError(
            "filtered-plan evidence is not canonically serializable"
        ) from exc


def _identity(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _validated_source_plan(value: Any) -> dict[str, Any]:
    source = deepcopy(
        _require_mapping("execution_plan", value)
    )

    try:
        validate_execution_plan(source)
    except ExecutionPlanError as exc:
        raise ExecutionPlanFilterError(
            f"execution_plan is invalid: {exc}"
        ) from exc

    if source["passed"] is not True:
        raise ExecutionPlanFilterError(
            "execution_plan must remain passing"
        )
    if source["submission_authorized"] is not False:
        raise ExecutionPlanFilterError(
            "execution_plan submission_authorized must remain False"
        )
    if source["orders_submitted"] != 0:
        raise ExecutionPlanFilterError(
            "execution_plan orders_submitted must remain zero"
        )

    return source


def _validated_selection(value: Any) -> dict[str, Any]:
    supplied = _require_mapping("selection_criteria", value)

    if set(supplied) != _SELECTION_KEYS:
        missing = sorted(_SELECTION_KEYS - set(supplied))
        unexpected = sorted(set(supplied) - _SELECTION_KEYS)
        raise ExecutionPlanFilterError(
            "selection_criteria keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    instrument_id = _require_nonempty_string(
        "selection_criteria.instrument_id",
        supplied["instrument_id"],
    )

    side_value = supplied["side"]
    if side_value is None:
        side = None
    else:
        side = _require_nonempty_string(
            "selection_criteria.side",
            side_value,
        ).upper()
        if side not in {"BUY", "SELL"}:
            raise ExecutionPlanFilterError(
                "selection_criteria.side must be BUY, SELL, or None"
            )

    return {
        "instrument_id": instrument_id,
        "side": side,
    }


def _select_exactly_one(
    *,
    source_plan: dict[str, Any],
    selection: dict[str, Any],
) -> dict[str, Any]:
    executable = [
        intent
        for intent in source_plan["intents"]
        if intent["should_order"] is True
    ]

    matches = [
        intent
        for intent in executable
        if (
            intent["instrument_id"] == selection["instrument_id"]
            and (
                selection["side"] is None
                or intent["side"] == selection["side"]
            )
        )
    ]

    if len(matches) != 1:
        available = [
            {
                "intent_id": intent["intent_id"],
                "instrument_id": intent["instrument_id"],
                "side": intent["side"],
                "quantity": intent["quantity"],
                "planned_notional": intent["planned_notional"],
            }
            for intent in executable
        ]
        raise ExecutionPlanFilterError(
            "expected exactly one executable intent for "
            f"instrument_id={selection['instrument_id']!r}, "
            f"side={selection['side']!r}; "
            f"found {len(matches)}; "
            f"available_executable_intents={available}"
        )

    return matches[0]


def _filtered_intents(
    *,
    source_plan: dict[str, Any],
    selected_intent_id: str,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []

    for source_intent in source_plan["intents"]:
        source_should_order = source_intent["should_order"] is True
        selected = (
            source_should_order
            and source_intent["intent_id"] == selected_intent_id
        )
        enabled = selected

        if selected:
            effective_side = source_intent["side"]
            effective_quantity = source_intent["quantity"]
            effective_planned_notional = source_intent[
                "planned_notional"
            ]
            filter_reason = "SELECTED_EXECUTABLE_INTENT"
        elif source_should_order:
            effective_side = "HOLD"
            effective_quantity = 0.0
            effective_planned_notional = 0.0
            filter_reason = "DISABLED_NON_SELECTED_EXECUTABLE_INTENT"
        else:
            effective_side = "HOLD"
            effective_quantity = 0.0
            effective_planned_notional = 0.0
            filter_reason = "SOURCE_INTENT_NOT_EXECUTABLE"

        filtered.append(
            {
                "source_intent_id": source_intent["intent_id"],
                "instrument_id": source_intent["instrument_id"],
                "decision_id": source_intent["decision_id"],
                "source_should_order": source_should_order,
                "source_side": source_intent["side"],
                "source_quantity": source_intent["quantity"],
                "source_planned_notional": source_intent[
                    "planned_notional"
                ],
                "selected": selected,
                "enabled": enabled,
                "effective_side": effective_side,
                "effective_quantity": effective_quantity,
                "effective_planned_notional":
                    effective_planned_notional,
                "filter_reason": filter_reason,
                "submission_authorized": False,
                "order_submitted": False,
            }
        )

    return filtered


def _summary(
    filtered_intents: list[dict[str, Any]],
) -> dict[str, Any]:
    enabled = [
        intent
        for intent in filtered_intents
        if intent["enabled"] is True
    ]

    return {
        "source_intent_count": len(filtered_intents),
        "source_executable_intent_count": sum(
            1
            for intent in filtered_intents
            if intent["source_should_order"] is True
        ),
        "source_hold_intent_count": sum(
            1
            for intent in filtered_intents
            if intent["source_should_order"] is False
        ),
        "audit_intent_count": len(filtered_intents),
        "enabled_intent_count": len(enabled),
        "disabled_executable_intent_count": sum(
            1
            for intent in filtered_intents
            if (
                intent["source_should_order"] is True
                and intent["enabled"] is False
            )
        ),
        "enabled_buy_count": sum(
            1
            for intent in enabled
            if intent["effective_side"] == "BUY"
        ),
        "enabled_sell_count": sum(
            1
            for intent in enabled
            if intent["effective_side"] == "SELL"
        ),
        "gross_enabled_planned_notional": sum(
            abs(intent["effective_planned_notional"])
            for intent in enabled
        ),
    }


def _construct_filtered_result(
    *,
    source_plan: dict[str, Any],
    selection: dict[str, Any],
    filtered_at_utc: str,
) -> dict[str, Any]:
    selected_intent = _select_exactly_one(
        source_plan=source_plan,
        selection=selection,
    )
    selected_intent_id = selected_intent["intent_id"]

    selection_identity = _identity(
        "selection",
        {
            "source_plan_id": source_plan["plan_id"],
            "selection_criteria": selection,
        },
    )

    filtered_intents = _filtered_intents(
        source_plan=source_plan,
        selected_intent_id=selected_intent_id,
    )
    summary = _summary(filtered_intents)

    filter_id = _identity(
        "plan_filter",
        {
            "source_plan_id": source_plan["plan_id"],
            "selection_identity": selection_identity,
            "selected_intent_id": selected_intent_id,
            "filtered_at_utc": filtered_at_utc,
            "filtered_intents": filtered_intents,
        },
    )

    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": True,
        "filter_id": filter_id,
        "filtered_at_utc": filtered_at_utc,
        "source_plan_id": source_plan["plan_id"],
        "selection_criteria": selection,
        "selection_identity": selection_identity,
        "selected_intent_id": selected_intent_id,
        "source_execution_plan": source_plan,
        "filtered_intents": filtered_intents,
        "summary": summary,
        "submission_authorized": False,
        "orders_submitted": 0,
    }


def filter_execution_plan(
    *,
    execution_plan: dict[str, Any],
    selection_criteria: dict[str, Any],
    filtered_at_utc: str,
) -> dict[str, Any]:
    """Return one deterministic NO_SUBMIT single-intent filtered plan."""
    source_plan = _validated_source_plan(execution_plan)
    selection = _validated_selection(selection_criteria)

    normalized_filtered_at = _canonical_timestamp(
        "filtered_at_utc",
        filtered_at_utc,
    )

    source_plan_at = _parse_utc_timestamp(
        "execution_plan.plan_at_utc",
        source_plan["plan_at_utc"],
    )
    filtered_at = _parse_utc_timestamp(
        "filtered_at_utc",
        normalized_filtered_at,
    )

    if filtered_at < source_plan_at:
        raise ExecutionPlanFilterError(
            "filtered_at_utc must not precede execution_plan.plan_at_utc"
        )

    result = _construct_filtered_result(
        source_plan=source_plan,
        selection=selection,
        filtered_at_utc=normalized_filtered_at,
    )

    validate_filtered_execution_plan(result)
    return result


def validate_filtered_execution_plan(result: Any) -> None:
    """Reject malformed, operational, inconsistent, or forged filter evidence."""
    if not isinstance(result, dict):
        raise ExecutionPlanFilterError(
            "filtered execution plan must be a dict"
        )

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise ExecutionPlanFilterError(
            "filtered-plan keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise ExecutionPlanFilterError(
            "unsupported filtered-plan schema_id"
        )
    if type(result["schema_version"]) is not int:
        raise ExecutionPlanFilterError(
            "filtered-plan schema_version must be an int"
        )
    if result["schema_version"] != SCHEMA_VERSION:
        raise ExecutionPlanFilterError(
            "unsupported filtered-plan schema_version"
        )
    if result["result_type"] != RESULT_TYPE:
        raise ExecutionPlanFilterError(
            "unsupported filtered-plan result_type"
        )
    if result["state_provenance"] != STATE_PROVENANCE:
        raise ExecutionPlanFilterError(
            "filtered-plan state provenance is invalid"
        )
    if result["passed"] is not True:
        raise ExecutionPlanFilterError(
            "filtered-plan passed must remain True"
        )
    if result["submission_authorized"] is not False:
        raise ExecutionPlanFilterError(
            "filtered-plan submission_authorized must remain False"
        )
    if type(result["orders_submitted"]) is not int:
        raise ExecutionPlanFilterError(
            "filtered-plan orders_submitted must be an int"
        )
    if result["orders_submitted"] != 0:
        raise ExecutionPlanFilterError(
            "filtered-plan orders_submitted must remain zero"
        )

    source_plan = _validated_source_plan(
        result["source_execution_plan"]
    )

    if result["source_plan_id"] != source_plan["plan_id"]:
        raise ExecutionPlanFilterError(
            "source_plan_id does not match source_execution_plan"
        )

    selection = _validated_selection(
        result["selection_criteria"]
    )

    normalized_filtered_at = _canonical_timestamp(
        "filtered-plan filtered_at_utc",
        result["filtered_at_utc"],
    )

    source_plan_at = _parse_utc_timestamp(
        "source_execution_plan.plan_at_utc",
        source_plan["plan_at_utc"],
    )
    filtered_at = _parse_utc_timestamp(
        "filtered-plan filtered_at_utc",
        normalized_filtered_at,
    )

    if filtered_at < source_plan_at:
        raise ExecutionPlanFilterError(
            "filtered_at_utc must not precede source plan timestamp"
        )

    expected = _construct_filtered_result(
        source_plan=source_plan,
        selection=selection,
        filtered_at_utc=normalized_filtered_at,
    )

    filtered_intents = result["filtered_intents"]
    if not isinstance(filtered_intents, list):
        raise ExecutionPlanFilterError(
            "filtered_intents must be a list"
        )

    for index, intent in enumerate(filtered_intents):
        if not isinstance(intent, dict):
            raise ExecutionPlanFilterError(
                f"filtered_intents[{index}] must be a dict"
            )
        if set(intent) != _FILTERED_INTENT_KEYS:
            raise ExecutionPlanFilterError(
                f"filtered_intents[{index}] keys mismatch"
            )

    summary = result["summary"]
    if not isinstance(summary, dict):
        raise ExecutionPlanFilterError(
            "filtered-plan summary must be a dict"
        )
    if set(summary) != _SUMMARY_KEYS:
        raise ExecutionPlanFilterError(
            "filtered-plan summary keys mismatch"
        )

    if result != expected:
        raise ExecutionPlanFilterError(
            "filtered execution plan does not match canonical reconstruction"
        )
