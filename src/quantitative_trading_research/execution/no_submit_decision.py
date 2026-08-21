"""Pure offline construction of deterministic no-submit decision packages.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/paper_trade_dry_run.py``.

The historical source combined useful target-versus-current-state decision
arithmetic with broker connectivity, market-data acquisition, artifact/model
loading, feature construction, PPO inference, filesystem logging, and CLI
execution. This C4 module preserves only the pure no-submit decision
responsibility.

All state is explicit caller-supplied or mocked/provider-neutral input. This
module does not obtain or establish live broker or market state, authorize or
submit orders, perform model training or inference, access canonical datasets
or final holdouts, or perform filesystem or network operations.
"""

from __future__ import annotations

import math
from typing import Any


SCHEMA_ID = "C4_NO_SUBMIT_DECISION_V1"
SCHEMA_VERSION = 1
DECISION_TYPE = "offline_no_submit_decision"
DECISION_ACTION = "NO_SUBMIT"
STATE_PROVENANCE = "caller_supplied_unverified"

_DECISION_KEYS = {
    "schema_id",
    "schema_version",
    "decision_type",
    "decision_id",
    "instrument_id",
    "metadata",
    "state_provenance",
    "target_weight",
    "current_weight",
    "intended_delta_weight",
    "equity",
    "intended_notional",
    "decision_action",
    "submission_authorized",
    "order_submitted",
}


class NoSubmitDecisionError(ValueError):
    """Fail-closed error for malformed canonical no-submit decisions."""


def _normalize_value(value: Any) -> Any:
    """Return a deterministic JSON-compatible provider-neutral value."""
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise NoSubmitDecisionError(
                "no-submit decision does not permit non-finite floats"
            )
        return value

    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise NoSubmitDecisionError(
                    "no-submit decision mapping keys must be strings"
                )
            normalized[key] = _normalize_value(item)
        return normalized

    if isinstance(value, (list, tuple)):
        return [_normalize_value(item) for item in value]

    raise NoSubmitDecisionError(
        "unsupported no-submit decision value type: "
        f"{type(value).__name__}"
    )


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NoSubmitDecisionError(f"{name} must be a dict")

    normalized = _normalize_value(value)
    if not isinstance(normalized, dict):
        raise NoSubmitDecisionError(f"{name} must normalize to a dict")

    return normalized


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NoSubmitDecisionError(
            f"{name} must be a non-empty string"
        )
    return value


def _require_finite_number(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise NoSubmitDecisionError(
            f"{name} must be a finite number"
        )

    numeric = float(value)
    if not math.isfinite(numeric):
        raise NoSubmitDecisionError(
            f"{name} must be a finite number"
        )

    return numeric


def build_no_submit_decision(
    *,
    decision_id: str,
    instrument_id: str,
    target_weight: float,
    current_weight: float,
    equity: float,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one deterministic offline no-submit decision package.

    ``target_weight``, ``current_weight``, and ``equity`` are explicit
    caller-supplied values. No provider or broker state is acquired here.

    The historical reusable arithmetic is preserved:

    ``intended_delta_weight = target_weight - current_weight``

    ``intended_notional = intended_delta_weight * equity``

    The resulting package always records that submission is unauthorized and
    no order was submitted.
    """
    normalized_decision_id = _require_nonempty_string(
        "decision_id",
        decision_id,
    )
    normalized_instrument_id = _require_nonempty_string(
        "instrument_id",
        instrument_id,
    )
    normalized_target_weight = _require_finite_number(
        "target_weight",
        target_weight,
    )
    normalized_current_weight = _require_finite_number(
        "current_weight",
        current_weight,
    )
    normalized_equity = _require_finite_number(
        "equity",
        equity,
    )

    intended_delta_weight = (
        normalized_target_weight - normalized_current_weight
    )
    intended_notional = intended_delta_weight * normalized_equity

    decision = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "decision_type": DECISION_TYPE,
        "decision_id": normalized_decision_id,
        "instrument_id": normalized_instrument_id,
        "metadata": _require_mapping(
            "metadata",
            {} if metadata is None else metadata,
        ),
        "state_provenance": STATE_PROVENANCE,
        "target_weight": normalized_target_weight,
        "current_weight": normalized_current_weight,
        "intended_delta_weight": intended_delta_weight,
        "equity": normalized_equity,
        "intended_notional": intended_notional,
        "decision_action": DECISION_ACTION,
        "submission_authorized": False,
        "order_submitted": False,
    }

    validate_no_submit_decision(decision)
    return decision


def validate_no_submit_decision(decision: Any) -> None:
    """Fail closed on malformed, operational, or inconsistent decisions."""
    if not isinstance(decision, dict):
        raise NoSubmitDecisionError(
            "no-submit decision must be a dict"
        )

    if set(decision) != _DECISION_KEYS:
        missing = sorted(_DECISION_KEYS - set(decision))
        unexpected = sorted(set(decision) - _DECISION_KEYS)

        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))

        raise NoSubmitDecisionError(
            "no-submit decision keys mismatch: " + "; ".join(details)
        )

    if decision["schema_id"] != SCHEMA_ID:
        raise NoSubmitDecisionError(
            "unsupported no-submit decision schema_id"
        )

    if type(decision["schema_version"]) is not int:
        raise NoSubmitDecisionError(
            "no-submit decision schema_version must be an int"
        )

    if decision["schema_version"] != SCHEMA_VERSION:
        raise NoSubmitDecisionError(
            "unsupported no-submit decision schema_version"
        )

    if decision["decision_type"] != DECISION_TYPE:
        raise NoSubmitDecisionError(
            "unsupported no-submit decision type"
        )

    _require_nonempty_string(
        "decision_id",
        decision["decision_id"],
    )
    _require_nonempty_string(
        "instrument_id",
        decision["instrument_id"],
    )
    _require_mapping(
        "metadata",
        decision["metadata"],
    )

    if decision["state_provenance"] != STATE_PROVENANCE:
        raise NoSubmitDecisionError(
            "state provenance must remain caller-supplied and unverified"
        )

    target_weight = _require_finite_number(
        "target_weight",
        decision["target_weight"],
    )
    current_weight = _require_finite_number(
        "current_weight",
        decision["current_weight"],
    )
    intended_delta_weight = _require_finite_number(
        "intended_delta_weight",
        decision["intended_delta_weight"],
    )
    equity = _require_finite_number(
        "equity",
        decision["equity"],
    )
    intended_notional = _require_finite_number(
        "intended_notional",
        decision["intended_notional"],
    )

    expected_delta_weight = target_weight - current_weight
    if intended_delta_weight != expected_delta_weight:
        raise NoSubmitDecisionError(
            "intended_delta_weight does not match target-current state"
        )

    expected_notional = expected_delta_weight * equity
    if intended_notional != expected_notional:
        raise NoSubmitDecisionError(
            "intended_notional does not match delta-weight and equity"
        )

    if decision["decision_action"] != DECISION_ACTION:
        raise NoSubmitDecisionError(
            "decision_action must remain NO_SUBMIT"
        )

    if decision["submission_authorized"] is not False:
        raise NoSubmitDecisionError(
            "submission_authorized must remain False"
        )

    if decision["order_submitted"] is not False:
        raise NoSubmitDecisionError(
            "order_submitted must remain False"
        )

    _normalize_value(decision)
