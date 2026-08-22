"""Pure deterministic offline submission-boundary validation.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/execution.py``.

The historical source combined reusable fail-closed execution guards with
rebalance-plan construction and an operational Alpaca order-submission call.
TM-062 now owns canonical execution-plan construction and TM-063 now owns
canonical execution-plan filtering. This C4 module preserves only the residual
provider-neutral submission-boundary responsibility: validate that canonical
filtered execution evidence is internally consistent and produce deterministic
NO_SUBMIT audit evidence.

This module performs no filesystem or network operations, obtains no provider
or broker state, reads no credentials, submits/cancels/replaces/polls no orders,
performs no paper/live execution, performs no model training or inference, and
accesses no canonical dataset or final holdout. The current C4 boundary always
keeps submission unauthorized and records zero submitted orders.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from .plan import ExecutionPlanError, validate_execution_plan
from .plan_filter import (
    ExecutionPlanFilterError,
    validate_filtered_execution_plan,
)


SCHEMA_ID = "C4_OFFLINE_SUBMISSION_BOUNDARY_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_submission_boundary"
STATE_PROVENANCE = "validated_canonical_execution_evidence"
SUBMISSION_ACTION = "NO_SUBMIT"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "boundary_id",
    "source_plan_id",
    "source_filter_id",
    "selection_identity",
    "selected_intent_id",
    "boundary_evidence",
    "source_filtered_execution_plan",
    "submission_action",
    "submission_authorized",
    "order_submitted",
    "orders_submitted",
}

_BOUNDARY_EVIDENCE_KEYS = {
    "source_intent_id",
    "instrument_id",
    "decision_id",
    "side",
    "quantity",
    "planned_notional",
    "filter_reason",
}


class SubmissionBoundaryError(ValueError):
    """Fail-closed error for malformed or unsafe submission-boundary evidence."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SubmissionBoundaryError(f"{name} must be a dict")
    return dict(value)


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
        raise SubmissionBoundaryError(
            "submission-boundary evidence is not canonically serializable"
        ) from exc


def _identity(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _validated_filtered_plan(value: Any) -> dict[str, Any]:
    filtered = deepcopy(
        _require_mapping("filtered_execution_plan", value)
    )

    try:
        validate_filtered_execution_plan(filtered)
    except ExecutionPlanFilterError as exc:
        raise SubmissionBoundaryError(
            f"filtered_execution_plan is invalid: {exc}"
        ) from exc

    if filtered["passed"] is not True:
        raise SubmissionBoundaryError(
            "filtered_execution_plan must remain passing"
        )
    if filtered["submission_authorized"] is not False:
        raise SubmissionBoundaryError(
            "filtered_execution_plan submission_authorized must remain False"
        )
    if filtered["orders_submitted"] != 0:
        raise SubmissionBoundaryError(
            "filtered_execution_plan orders_submitted must remain zero"
        )

    source_plan = filtered["source_execution_plan"]
    try:
        validate_execution_plan(source_plan)
    except ExecutionPlanError as exc:
        raise SubmissionBoundaryError(
            f"embedded source_execution_plan is invalid: {exc}"
        ) from exc

    if filtered["source_plan_id"] != source_plan["plan_id"]:
        raise SubmissionBoundaryError(
            "source_plan_id does not match embedded source execution plan"
        )
    if source_plan["submission_authorized"] is not False:
        raise SubmissionBoundaryError(
            "source execution plan submission_authorized must remain False"
        )
    if source_plan["orders_submitted"] != 0:
        raise SubmissionBoundaryError(
            "source execution plan orders_submitted must remain zero"
        )

    return filtered


def _selected_boundary_evidence(
    filtered: dict[str, Any],
) -> dict[str, Any]:
    selected = [
        intent
        for intent in filtered["filtered_intents"]
        if intent["selected"] is True
    ]
    enabled = [
        intent
        for intent in filtered["filtered_intents"]
        if intent["enabled"] is True
    ]

    if len(selected) != 1 or len(enabled) != 1:
        raise SubmissionBoundaryError(
            "submission boundary requires exactly one selected enabled intent"
        )

    selected_intent = selected[0]
    if selected_intent != enabled[0]:
        raise SubmissionBoundaryError(
            "selected and enabled filtered intents must be identical"
        )

    selected_intent_id = filtered["selected_intent_id"]
    if selected_intent["source_intent_id"] != selected_intent_id:
        raise SubmissionBoundaryError(
            "selected_intent_id does not match selected filtered intent"
        )

    if selected_intent["source_should_order"] is not True:
        raise SubmissionBoundaryError(
            "selected filtered intent must originate from executable evidence"
        )
    if selected_intent["filter_reason"] != "SELECTED_EXECUTABLE_INTENT":
        raise SubmissionBoundaryError(
            "selected filtered intent must retain selected filter evidence"
        )
    if selected_intent["source_side"] not in {"BUY", "SELL"}:
        raise SubmissionBoundaryError(
            "selected source side must be BUY or SELL"
        )
    if selected_intent["effective_side"] != selected_intent["source_side"]:
        raise SubmissionBoundaryError(
            "selected effective side must match source side"
        )
    if selected_intent["effective_quantity"] != selected_intent["source_quantity"]:
        raise SubmissionBoundaryError(
            "selected effective quantity must match source quantity"
        )
    if (
        selected_intent["effective_planned_notional"]
        != selected_intent["source_planned_notional"]
    ):
        raise SubmissionBoundaryError(
            "selected effective planned notional must match source evidence"
        )
    if selected_intent["effective_quantity"] <= 0:
        raise SubmissionBoundaryError(
            "selected effective quantity must be positive"
        )
    if selected_intent["effective_planned_notional"] == 0:
        raise SubmissionBoundaryError(
            "selected effective planned notional must be non-zero"
        )
    if selected_intent["submission_authorized"] is not False:
        raise SubmissionBoundaryError(
            "selected filtered intent submission_authorized must remain False"
        )
    if selected_intent["order_submitted"] is not False:
        raise SubmissionBoundaryError(
            "selected filtered intent order_submitted must remain False"
        )

    source_plan = filtered["source_execution_plan"]
    source_matches = [
        intent
        for intent in source_plan["intents"]
        if intent["intent_id"] == selected_intent_id
    ]
    if len(source_matches) != 1:
        raise SubmissionBoundaryError(
            "selected intent must correspond to exactly one source-plan intent"
        )

    source_intent = source_matches[0]
    correspondence = (
        source_intent["instrument_id"] == selected_intent["instrument_id"]
        and source_intent["decision_id"] == selected_intent["decision_id"]
        and source_intent["should_order"] is True
        and source_intent["side"] == selected_intent["effective_side"]
        and source_intent["quantity"] == selected_intent["effective_quantity"]
        and (
            source_intent["planned_notional"]
            == selected_intent["effective_planned_notional"]
        )
        and source_intent["submission_authorized"] is False
        and source_intent["order_submitted"] is False
    )
    if not correspondence:
        raise SubmissionBoundaryError(
            "selected filtered intent does not correspond to source-plan evidence"
        )

    return {
        "source_intent_id": selected_intent_id,
        "instrument_id": selected_intent["instrument_id"],
        "decision_id": selected_intent["decision_id"],
        "side": selected_intent["effective_side"],
        "quantity": selected_intent["effective_quantity"],
        "planned_notional": selected_intent["effective_planned_notional"],
        "filter_reason": selected_intent["filter_reason"],
    }


def _construct_submission_boundary(
    filtered: dict[str, Any],
) -> dict[str, Any]:
    evidence = _selected_boundary_evidence(filtered)

    boundary_id = _identity(
        "submission_boundary",
        {
            "source_plan_id": filtered["source_plan_id"],
            "source_filter_id": filtered["filter_id"],
            "selection_identity": filtered["selection_identity"],
            "selected_intent_id": filtered["selected_intent_id"],
            "boundary_evidence": evidence,
            "submission_action": SUBMISSION_ACTION,
        },
    )

    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": True,
        "boundary_id": boundary_id,
        "source_plan_id": filtered["source_plan_id"],
        "source_filter_id": filtered["filter_id"],
        "selection_identity": filtered["selection_identity"],
        "selected_intent_id": filtered["selected_intent_id"],
        "boundary_evidence": evidence,
        "source_filtered_execution_plan": filtered,
        "submission_action": SUBMISSION_ACTION,
        "submission_authorized": False,
        "order_submitted": False,
        "orders_submitted": 0,
    }


def build_submission_boundary(
    *,
    filtered_execution_plan: dict[str, Any],
) -> dict[str, Any]:
    """Build deterministic NO_SUBMIT evidence for the C4 submission boundary."""
    filtered = _validated_filtered_plan(filtered_execution_plan)
    result = _construct_submission_boundary(filtered)
    validate_submission_boundary(result)
    return result


def validate_submission_boundary(result: Any) -> None:
    """Reject malformed, tampered, inconsistent, or operational boundary evidence."""
    if not isinstance(result, dict):
        raise SubmissionBoundaryError("submission boundary result must be a dict")

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise SubmissionBoundaryError(
            "submission-boundary keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise SubmissionBoundaryError("unsupported submission-boundary schema_id")
    if type(result["schema_version"]) is not int:
        raise SubmissionBoundaryError(
            "submission-boundary schema_version must be an int"
        )
    if result["schema_version"] != SCHEMA_VERSION:
        raise SubmissionBoundaryError(
            "unsupported submission-boundary schema_version"
        )
    if result["result_type"] != RESULT_TYPE:
        raise SubmissionBoundaryError("unsupported submission-boundary result_type")
    if result["state_provenance"] != STATE_PROVENANCE:
        raise SubmissionBoundaryError(
            "submission-boundary state provenance is invalid"
        )
    if result["passed"] is not True:
        raise SubmissionBoundaryError(
            "submission-boundary passed must remain True"
        )
    if result["submission_action"] != SUBMISSION_ACTION:
        raise SubmissionBoundaryError(
            "submission_action must remain NO_SUBMIT"
        )
    if result["submission_authorized"] is not False:
        raise SubmissionBoundaryError(
            "submission_authorized must remain False"
        )
    if result["order_submitted"] is not False:
        raise SubmissionBoundaryError("order_submitted must remain False")
    if type(result["orders_submitted"]) is not int:
        raise SubmissionBoundaryError("orders_submitted must be an int")
    if result["orders_submitted"] != 0:
        raise SubmissionBoundaryError("orders_submitted must remain zero")

    evidence = result["boundary_evidence"]
    if not isinstance(evidence, dict) or set(evidence) != _BOUNDARY_EVIDENCE_KEYS:
        raise SubmissionBoundaryError(
            "boundary_evidence keys mismatch"
        )

    filtered = _validated_filtered_plan(
        result["source_filtered_execution_plan"]
    )
    expected = _construct_submission_boundary(filtered)

    if result != expected:
        raise SubmissionBoundaryError(
            "submission-boundary result does not match canonical reconstruction"
        )
