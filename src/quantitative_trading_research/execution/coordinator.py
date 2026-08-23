"""Pure deterministic offline guarded execution coordination.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/paper_trade_loop.py``.

The historical source coordinated plan validation, explicit submit opt-in,
broker-derived risk context, paper-order submission, and before/after broker
state. TM-031, TM-032, TM-062, TM-063, and TM-029 now own the canonical risk,
pre-trade, execution-plan, plan-filter, and submission-boundary contracts.

This C4 module preserves only the residual provider-neutral coordination
responsibility: validate the complete canonical offline execution-evidence
chain, enforce exact cross-contract correspondence and deterministic stage
ordering, and emit immutable NO_SUBMIT coordinator evidence.

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

from .risk_controls import RiskControlError, validate_risk_result
from .pre_trade import PreTradeEligibilityError, validate_pre_trade_result
from .plan import ExecutionPlanError, validate_execution_plan
from .plan_filter import (
    ExecutionPlanFilterError,
    validate_filtered_execution_plan,
)
from .submission import (
    SUBMISSION_ACTION,
    SubmissionBoundaryError,
    validate_submission_boundary,
)


SCHEMA_ID = "C4_OFFLINE_EXECUTION_COORDINATOR_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_execution_coordinator"
STATE_PROVENANCE = "validated_canonical_execution_chain"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "coordinator_id",
    "upstream_chain",
    "risk_result",
    "pre_trade_result",
    "execution_plan",
    "filtered_execution_plan",
    "submission_boundary",
    "submission_action",
    "submission_authorized",
    "order_submitted",
    "orders_submitted",
}

_CHAIN_ENTRY_KEYS = {
    "stage",
    "schema_id",
    "schema_version",
    "identity",
}

_STAGE_ORDER = (
    "TM_031_RISK",
    "TM_032_PRE_TRADE",
    "TM_062_PLAN",
    "TM_063_FILTER",
    "TM_029_SUBMISSION_BOUNDARY",
)


class ExecutionCoordinatorError(ValueError):
    """Fail-closed error for malformed or inconsistent coordinator evidence."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionCoordinatorError(f"{name} must be a dict")
    return deepcopy(value)


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
        raise ExecutionCoordinatorError(
            "execution-coordinator evidence is not canonically serializable"
        ) from exc


def _identity(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _validate_stage(
    *,
    name: str,
    value: Any,
    validator: Any,
    error_type: type[Exception],
) -> dict[str, Any]:
    normalized = _require_mapping(name, value)

    try:
        validator(normalized)
    except error_type as exc:
        raise ExecutionCoordinatorError(
            f"{name} is invalid: {exc}"
        ) from exc

    if normalized.get("passed") is not True:
        raise ExecutionCoordinatorError(
            f"{name} must remain passing"
        )

    return normalized


def _validated_chain_inputs(
    *,
    risk_result: Any,
    pre_trade_result: Any,
    execution_plan: Any,
    filtered_execution_plan: Any,
    submission_boundary: Any,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    risk = _validate_stage(
        name="risk_result",
        value=risk_result,
        validator=validate_risk_result,
        error_type=RiskControlError,
    )
    pre_trade = _validate_stage(
        name="pre_trade_result",
        value=pre_trade_result,
        validator=validate_pre_trade_result,
        error_type=PreTradeEligibilityError,
    )
    plan = _validate_stage(
        name="execution_plan",
        value=execution_plan,
        validator=validate_execution_plan,
        error_type=ExecutionPlanError,
    )
    filtered = _validate_stage(
        name="filtered_execution_plan",
        value=filtered_execution_plan,
        validator=validate_filtered_execution_plan,
        error_type=ExecutionPlanFilterError,
    )
    boundary = _validate_stage(
        name="submission_boundary",
        value=submission_boundary,
        validator=validate_submission_boundary,
        error_type=SubmissionBoundaryError,
    )

    if pre_trade["risk_result"] != risk:
        raise ExecutionCoordinatorError(
            "pre_trade_result does not embed the supplied risk_result"
        )

    if plan["pre_trade_result"] != pre_trade:
        raise ExecutionCoordinatorError(
            "execution_plan does not embed the supplied pre_trade_result"
        )

    if filtered["source_execution_plan"] != plan:
        raise ExecutionCoordinatorError(
            "filtered_execution_plan does not embed the supplied execution_plan"
        )

    if boundary["source_filtered_execution_plan"] != filtered:
        raise ExecutionCoordinatorError(
            "submission_boundary does not embed the supplied filtered_execution_plan"
        )

    if filtered["source_plan_id"] != plan["plan_id"]:
        raise ExecutionCoordinatorError(
            "TM-063 source_plan_id does not match TM-062 plan_id"
        )

    if boundary["source_plan_id"] != plan["plan_id"]:
        raise ExecutionCoordinatorError(
            "TM-029 source_plan_id does not match TM-062 plan_id"
        )

    if boundary["source_filter_id"] != filtered["filter_id"]:
        raise ExecutionCoordinatorError(
            "TM-029 source_filter_id does not match TM-063 filter_id"
        )

    if boundary["selection_identity"] != filtered["selection_identity"]:
        raise ExecutionCoordinatorError(
            "TM-029 selection_identity does not match TM-063 evidence"
        )

    if boundary["selected_intent_id"] != filtered["selected_intent_id"]:
        raise ExecutionCoordinatorError(
            "TM-029 selected_intent_id does not match TM-063 evidence"
        )

    if (
        boundary["boundary_evidence"]["source_intent_id"]
        != filtered["selected_intent_id"]
    ):
        raise ExecutionCoordinatorError(
            "TM-029 boundary evidence does not identify the selected TM-063 intent"
        )

    if plan["submission_authorized"] is not False:
        raise ExecutionCoordinatorError(
            "TM-062 submission_authorized must remain False"
        )
    if plan["orders_submitted"] != 0:
        raise ExecutionCoordinatorError(
            "TM-062 orders_submitted must remain zero"
        )
    if filtered["submission_authorized"] is not False:
        raise ExecutionCoordinatorError(
            "TM-063 submission_authorized must remain False"
        )
    if filtered["orders_submitted"] != 0:
        raise ExecutionCoordinatorError(
            "TM-063 orders_submitted must remain zero"
        )
    if boundary["submission_action"] != SUBMISSION_ACTION:
        raise ExecutionCoordinatorError(
            "TM-029 submission_action must remain NO_SUBMIT"
        )
    if boundary["submission_authorized"] is not False:
        raise ExecutionCoordinatorError(
            "TM-029 submission_authorized must remain False"
        )
    if boundary["order_submitted"] is not False:
        raise ExecutionCoordinatorError(
            "TM-029 order_submitted must remain False"
        )
    if boundary["orders_submitted"] != 0:
        raise ExecutionCoordinatorError(
            "TM-029 orders_submitted must remain zero"
        )

    return risk, pre_trade, plan, filtered, boundary


def _upstream_chain(
    *,
    risk: dict[str, Any],
    pre_trade: dict[str, Any],
    plan: dict[str, Any],
    filtered: dict[str, Any],
    boundary: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "stage": "TM_031_RISK",
            "schema_id": risk["schema_id"],
            "schema_version": risk["schema_version"],
            "identity": _identity("risk_evidence", risk),
        },
        {
            "stage": "TM_032_PRE_TRADE",
            "schema_id": pre_trade["schema_id"],
            "schema_version": pre_trade["schema_version"],
            "identity": _identity("pre_trade_evidence", pre_trade),
        },
        {
            "stage": "TM_062_PLAN",
            "schema_id": plan["schema_id"],
            "schema_version": plan["schema_version"],
            "identity": plan["plan_id"],
        },
        {
            "stage": "TM_063_FILTER",
            "schema_id": filtered["schema_id"],
            "schema_version": filtered["schema_version"],
            "identity": filtered["filter_id"],
        },
        {
            "stage": "TM_029_SUBMISSION_BOUNDARY",
            "schema_id": boundary["schema_id"],
            "schema_version": boundary["schema_version"],
            "identity": boundary["boundary_id"],
        },
    ]


def _construct_coordinator(
    *,
    risk: dict[str, Any],
    pre_trade: dict[str, Any],
    plan: dict[str, Any],
    filtered: dict[str, Any],
    boundary: dict[str, Any],
) -> dict[str, Any]:
    chain = _upstream_chain(
        risk=risk,
        pre_trade=pre_trade,
        plan=plan,
        filtered=filtered,
        boundary=boundary,
    )

    coordinator_id = _identity(
        "execution_coordinator",
        {
            "upstream_chain": chain,
            "source_plan_id": plan["plan_id"],
            "source_filter_id": filtered["filter_id"],
            "submission_boundary_id": boundary["boundary_id"],
            "selected_intent_id": filtered["selected_intent_id"],
            "submission_action": SUBMISSION_ACTION,
        },
    )

    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": True,
        "coordinator_id": coordinator_id,
        "upstream_chain": chain,
        "risk_result": risk,
        "pre_trade_result": pre_trade,
        "execution_plan": plan,
        "filtered_execution_plan": filtered,
        "submission_boundary": boundary,
        "submission_action": SUBMISSION_ACTION,
        "submission_authorized": False,
        "order_submitted": False,
        "orders_submitted": 0,
    }


def build_execution_coordinator(
    *,
    risk_result: dict[str, Any],
    pre_trade_result: dict[str, Any],
    execution_plan: dict[str, Any],
    filtered_execution_plan: dict[str, Any],
    submission_boundary: dict[str, Any],
) -> dict[str, Any]:
    """Build deterministic NO_SUBMIT evidence for the guarded execution chain."""
    risk, pre_trade, plan, filtered, boundary = _validated_chain_inputs(
        risk_result=risk_result,
        pre_trade_result=pre_trade_result,
        execution_plan=execution_plan,
        filtered_execution_plan=filtered_execution_plan,
        submission_boundary=submission_boundary,
    )

    result = _construct_coordinator(
        risk=risk,
        pre_trade=pre_trade,
        plan=plan,
        filtered=filtered,
        boundary=boundary,
    )
    validate_execution_coordinator(result)
    return result


def validate_execution_coordinator(result: Any) -> None:
    """Reject malformed, reordered, operational, or forged coordinator evidence."""
    if not isinstance(result, dict):
        raise ExecutionCoordinatorError(
            "execution coordinator result must be a dict"
        )

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise ExecutionCoordinatorError(
            "execution-coordinator keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise ExecutionCoordinatorError(
            "unsupported execution-coordinator schema_id"
        )
    if type(result["schema_version"]) is not int:
        raise ExecutionCoordinatorError(
            "execution-coordinator schema_version must be an int"
        )
    if result["schema_version"] != SCHEMA_VERSION:
        raise ExecutionCoordinatorError(
            "unsupported execution-coordinator schema_version"
        )
    if result["result_type"] != RESULT_TYPE:
        raise ExecutionCoordinatorError(
            "unsupported execution-coordinator result_type"
        )
    if result["state_provenance"] != STATE_PROVENANCE:
        raise ExecutionCoordinatorError(
            "execution-coordinator state provenance is invalid"
        )
    if result["passed"] is not True:
        raise ExecutionCoordinatorError(
            "execution-coordinator passed must remain True"
        )
    if result["submission_action"] != SUBMISSION_ACTION:
        raise ExecutionCoordinatorError(
            "submission_action must remain NO_SUBMIT"
        )
    if result["submission_authorized"] is not False:
        raise ExecutionCoordinatorError(
            "submission_authorized must remain False"
        )
    if result["order_submitted"] is not False:
        raise ExecutionCoordinatorError(
            "order_submitted must remain False"
        )
    if type(result["orders_submitted"]) is not int:
        raise ExecutionCoordinatorError(
            "orders_submitted must be an int"
        )
    if result["orders_submitted"] != 0:
        raise ExecutionCoordinatorError(
            "orders_submitted must remain zero"
        )

    chain = result["upstream_chain"]
    if not isinstance(chain, list) or len(chain) != len(_STAGE_ORDER):
        raise ExecutionCoordinatorError(
            "upstream_chain must contain exactly five ordered stages"
        )

    for index, entry in enumerate(chain):
        if not isinstance(entry, dict) or set(entry) != _CHAIN_ENTRY_KEYS:
            raise ExecutionCoordinatorError(
                f"upstream_chain[{index}] keys mismatch"
            )
        if entry["stage"] != _STAGE_ORDER[index]:
            raise ExecutionCoordinatorError(
                "upstream_chain stage ordering is invalid"
            )
        if not isinstance(entry["schema_id"], str) or not entry["schema_id"]:
            raise ExecutionCoordinatorError(
                f"upstream_chain[{index}].schema_id must be non-empty"
            )
        if type(entry["schema_version"]) is not int:
            raise ExecutionCoordinatorError(
                f"upstream_chain[{index}].schema_version must be an int"
            )
        if not isinstance(entry["identity"], str) or not entry["identity"]:
            raise ExecutionCoordinatorError(
                f"upstream_chain[{index}].identity must be non-empty"
            )

    risk, pre_trade, plan, filtered, boundary = _validated_chain_inputs(
        risk_result=result["risk_result"],
        pre_trade_result=result["pre_trade_result"],
        execution_plan=result["execution_plan"],
        filtered_execution_plan=result["filtered_execution_plan"],
        submission_boundary=result["submission_boundary"],
    )

    expected = _construct_coordinator(
        risk=risk,
        pre_trade=pre_trade,
        plan=plan,
        filtered=filtered,
        boundary=boundary,
    )

    if result != expected:
        raise ExecutionCoordinatorError(
            "execution-coordinator result does not match canonical reconstruction"
        )
