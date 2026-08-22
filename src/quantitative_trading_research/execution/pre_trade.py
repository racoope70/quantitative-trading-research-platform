"""Pure offline fail-closed pre-trade eligibility evaluation.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/pre_trade_checklist.py``.

The historical implementation combined reusable pre-trade safety invariants
with filesystem artifact discovery, pandas CSV loading, implicit wall-clock
access, optional Alpaca connectivity, report writing, and CLI execution.

This C4 module preserves only the pure provider-neutral eligibility
responsibility. It consumes already-constructed canonical offline evidence:

* a validated TM-031 risk-control result; and
* validated TM-028 no-submit decision packages.

It performs no filesystem or network operations, obtains no provider or broker
state, submits no orders, performs no paper/live execution, performs no
training or inference, and accesses no canonical dataset or final holdout.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .no_submit_decision import (
    DECISION_ACTION,
    SCHEMA_ID as NO_SUBMIT_SCHEMA_ID,
    SCHEMA_VERSION as NO_SUBMIT_SCHEMA_VERSION,
    NoSubmitDecisionError,
    validate_no_submit_decision,
)
from .risk_controls import (
    SCHEMA_ID as RISK_SCHEMA_ID,
    SCHEMA_VERSION as RISK_SCHEMA_VERSION,
    RiskControlError,
    validate_risk_result,
)


SCHEMA_ID = "C4_OFFLINE_PRE_TRADE_ELIGIBILITY_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_pre_trade_eligibility_result"
STATE_PROVENANCE = "validated_caller_supplied_offline_evidence"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "risk_result",
    "decisions",
    "checks",
}

_CHECK_KEYS = {
    "name",
    "passed",
    "severity",
    "evidence",
}

_CHECK_NAMES = (
    "risk_result_passed",
    "decision_set_non_empty",
    "decision_ids_unique",
    "decision_instruments_unique",
    "decision_instruments_match_risk",
    "decision_state_matches_risk",
    "submission_authority_absent",
    "orders_submitted_absent",
)

_STATE_FIELDS = (
    ("target_weight", "target_weight"),
    ("current_weight", "current_weight"),
    ("equity", "equity"),
    ("canonical_delta_weight", "intended_delta_weight"),
    ("canonical_intended_notional", "intended_notional"),
)


class PreTradeEligibilityError(ValueError):
    """Fail-closed error for malformed pre-trade evidence or results."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PreTradeEligibilityError(f"{name} must be a dict")
    return dict(value)


def _require_bool(name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise PreTradeEligibilityError(f"{name} must be a bool")
    return value


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PreTradeEligibilityError(
            f"{name} must be a non-empty string"
        )
    return value


def _check(
    name: str,
    passed: bool,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "severity": "ERROR",
        "evidence": evidence,
    }


def _validated_inputs(
    *,
    risk_result: Any,
    decisions: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    normalized_risk = deepcopy(
        _require_mapping("risk_result", risk_result)
    )

    try:
        validate_risk_result(normalized_risk)
    except RiskControlError as exc:
        raise PreTradeEligibilityError(
            f"risk_result is invalid: {exc}"
        ) from exc

    if not isinstance(decisions, list):
        raise PreTradeEligibilityError("decisions must be a list")

    normalized_decisions: list[dict[str, Any]] = []

    for index, raw_decision in enumerate(decisions):
        if not isinstance(raw_decision, dict):
            raise PreTradeEligibilityError(
                f"decisions[{index}] must be a dict"
            )

        decision = deepcopy(raw_decision)

        try:
            validate_no_submit_decision(decision)
        except NoSubmitDecisionError as exc:
            raise PreTradeEligibilityError(
                f"decisions[{index}] is invalid: {exc}"
            ) from exc

        normalized_decisions.append(decision)

    return normalized_risk, normalized_decisions


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()

    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)

    return sorted(duplicates)


def _build_checks(
    *,
    risk_result: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    risk_rows = risk_result["evaluated_rows"]

    risk_instruments = [
        row["instrument_id"]
        for row in risk_rows
    ]
    decision_ids = [
        decision["decision_id"]
        for decision in decisions
    ]
    decision_instruments = [
        decision["instrument_id"]
        for decision in decisions
    ]

    duplicate_decision_ids = _duplicates(decision_ids)
    duplicate_decision_instruments = _duplicates(
        decision_instruments
    )

    risk_instrument_set = set(risk_instruments)
    decision_instrument_set = set(decision_instruments)

    missing_decision_instruments = sorted(
        risk_instrument_set - decision_instrument_set
    )
    unexpected_decision_instruments = sorted(
        decision_instrument_set - risk_instrument_set
    )

    checks.append(
        _check(
            "risk_result_passed",
            risk_result["passed"] is True,
            {
                "risk_schema_id": risk_result["schema_id"],
                "risk_schema_version": risk_result[
                    "schema_version"
                ],
                "risk_passed": risk_result["passed"],
            },
        )
    )

    checks.append(
        _check(
            "decision_set_non_empty",
            len(decisions) > 0,
            {
                "decision_count": len(decisions),
            },
        )
    )

    checks.append(
        _check(
            "decision_ids_unique",
            not duplicate_decision_ids,
            {
                "decision_count": len(decision_ids),
                "unique_decision_id_count": len(
                    set(decision_ids)
                ),
                "duplicate_decision_ids": (
                    duplicate_decision_ids
                ),
            },
        )
    )

    checks.append(
        _check(
            "decision_instruments_unique",
            not duplicate_decision_instruments,
            {
                "decision_count": len(decision_instruments),
                "unique_instrument_count": len(
                    decision_instrument_set
                ),
                "duplicate_instruments": (
                    duplicate_decision_instruments
                ),
            },
        )
    )

    instruments_match = (
        not duplicate_decision_instruments
        and decision_instrument_set == risk_instrument_set
        and len(decision_instruments) == len(risk_instruments)
    )

    checks.append(
        _check(
            "decision_instruments_match_risk",
            instruments_match,
            {
                "risk_instruments": sorted(risk_instrument_set),
                "decision_instruments": sorted(
                    decision_instrument_set
                ),
                "missing_decision_instruments": (
                    missing_decision_instruments
                ),
                "unexpected_decision_instruments": (
                    unexpected_decision_instruments
                ),
            },
        )
    )

    state_mismatches: list[dict[str, Any]] = []
    state_comparison_possible = instruments_match

    if state_comparison_possible:
        risk_by_instrument = {
            row["instrument_id"]: row
            for row in risk_rows
        }
        decision_by_instrument = {
            decision["instrument_id"]: decision
            for decision in decisions
        }

        for instrument_id in sorted(risk_instrument_set):
            risk_row = risk_by_instrument[instrument_id]
            decision = decision_by_instrument[instrument_id]

            for risk_field, decision_field in _STATE_FIELDS:
                risk_value = risk_row[risk_field]
                decision_value = decision[decision_field]

                if risk_value != decision_value:
                    state_mismatches.append(
                        {
                            "instrument_id": instrument_id,
                            "risk_field": risk_field,
                            "decision_field": decision_field,
                            "risk_value": risk_value,
                            "decision_value": decision_value,
                        }
                    )

    checks.append(
        _check(
            "decision_state_matches_risk",
            (
                state_comparison_possible
                and not state_mismatches
            ),
            {
                "comparison_possible": (
                    state_comparison_possible
                ),
                "mismatches": state_mismatches,
            },
        )
    )

    submission_authorized_count = sum(
        1
        for decision in decisions
        if decision["submission_authorized"] is not False
    )
    non_no_submit_action_count = sum(
        1
        for decision in decisions
        if decision["decision_action"] != DECISION_ACTION
    )

    checks.append(
        _check(
            "submission_authority_absent",
            (
                submission_authorized_count == 0
                and non_no_submit_action_count == 0
            ),
            {
                "submission_authorized_count": (
                    submission_authorized_count
                ),
                "non_no_submit_action_count": (
                    non_no_submit_action_count
                ),
            },
        )
    )

    orders_submitted_count = sum(
        1
        for decision in decisions
        if decision["order_submitted"] is not False
    )

    checks.append(
        _check(
            "orders_submitted_absent",
            orders_submitted_count == 0,
            {
                "orders_submitted_count": (
                    orders_submitted_count
                ),
            },
        )
    )

    return checks


def evaluate_pre_trade_eligibility(
    *,
    risk_result: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate pure offline pre-trade eligibility.

    Malformed upstream evidence raises ``PreTradeEligibilityError``.
    Structurally valid but unsafe evidence returns a structured result whose
    ``passed`` field is ``False``.
    """
    normalized_risk, normalized_decisions = _validated_inputs(
        risk_result=risk_result,
        decisions=decisions,
    )

    checks = _build_checks(
        risk_result=normalized_risk,
        decisions=normalized_decisions,
    )

    result = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": all(check["passed"] for check in checks),
        "risk_result": normalized_risk,
        "decisions": normalized_decisions,
        "checks": checks,
    }

    validate_pre_trade_result(result)
    return result


def validate_pre_trade_result(result: Any) -> None:
    """Fail closed on malformed, incomplete, or forged eligibility evidence."""
    if not isinstance(result, dict):
        raise PreTradeEligibilityError(
            "pre-trade result must be a dict"
        )

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise PreTradeEligibilityError(
            "pre-trade result keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise PreTradeEligibilityError(
            "unsupported pre-trade result schema_id"
        )

    if type(result["schema_version"]) is not int:
        raise PreTradeEligibilityError(
            "pre-trade result schema_version must be an int"
        )

    if result["schema_version"] != SCHEMA_VERSION:
        raise PreTradeEligibilityError(
            "unsupported pre-trade result schema_version"
        )

    if result["result_type"] != RESULT_TYPE:
        raise PreTradeEligibilityError(
            "unsupported pre-trade result type"
        )

    if result["state_provenance"] != STATE_PROVENANCE:
        raise PreTradeEligibilityError(
            "pre-trade result state provenance is invalid"
        )

    passed = _require_bool(
        "pre-trade result passed",
        result["passed"],
    )

    risk_result, decisions = _validated_inputs(
        risk_result=result["risk_result"],
        decisions=result["decisions"],
    )

    checks = result["checks"]
    if not isinstance(checks, list) or not checks:
        raise PreTradeEligibilityError(
            "pre-trade result checks must be a non-empty list"
        )

    names: list[str] = []

    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise PreTradeEligibilityError(
                f"pre-trade result checks[{index}] must be a dict"
            )

        if set(check) != _CHECK_KEYS:
            raise PreTradeEligibilityError(
                f"pre-trade result checks[{index}] keys mismatch"
            )

        name = _require_nonempty_string(
            f"pre-trade result checks[{index}].name",
            check["name"],
        )
        names.append(name)

        _require_bool(
            f"pre-trade result checks[{index}].passed",
            check["passed"],
        )

        if check["severity"] != "ERROR":
            raise PreTradeEligibilityError(
                f"pre-trade result checks[{index}].severity "
                "must be ERROR"
            )

        if not isinstance(check["evidence"], dict):
            raise PreTradeEligibilityError(
                f"pre-trade result checks[{index}].evidence "
                "must be a dict"
            )

    if tuple(names) != _CHECK_NAMES:
        unknown = sorted(set(names) - set(_CHECK_NAMES))
        missing = sorted(set(_CHECK_NAMES) - set(names))

        raise PreTradeEligibilityError(
            "pre-trade result check-set mismatch: "
            f"unknown={unknown}; missing={missing}"
        )

    if len(names) != len(set(names)):
        raise PreTradeEligibilityError(
            "pre-trade result contains duplicate check identifiers"
        )

    expected_checks = _build_checks(
        risk_result=risk_result,
        decisions=decisions,
    )

    if checks != expected_checks:
        raise PreTradeEligibilityError(
            "pre-trade result check evidence does not match "
            "canonical evaluation"
        )

    expected_passed = all(
        check["passed"]
        for check in expected_checks
    )

    if passed is not expected_passed:
        raise PreTradeEligibilityError(
            "pre-trade result passed does not match canonical "
            "check aggregation"
        )

    if risk_result["schema_id"] != RISK_SCHEMA_ID:
        raise PreTradeEligibilityError(
            "unexpected TM-031 risk schema"
        )

    if risk_result["schema_version"] != RISK_SCHEMA_VERSION:
        raise PreTradeEligibilityError(
            "unexpected TM-031 risk schema version"
        )

    for decision in decisions:
        if decision["schema_id"] != NO_SUBMIT_SCHEMA_ID:
            raise PreTradeEligibilityError(
                "unexpected TM-028 decision schema"
            )

        if (
            decision["schema_version"]
            != NO_SUBMIT_SCHEMA_VERSION
        ):
            raise PreTradeEligibilityError(
                "unexpected TM-028 decision schema version"
            )
