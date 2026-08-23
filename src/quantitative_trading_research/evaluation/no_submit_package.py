"""Pure deterministic offline evaluation of canonical no-submit packages.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/evaluate_dry_run.py``.

The historical source evaluated filesystem CSV/JSON dry-run artifacts, legacy
prediction fields, symbol completeness, and no-submit summaries. This C4
module preserves only the residual deterministic package-evaluation
responsibility. It consumes a canonical TM-033 checksummed execution-evidence
package whose ``record.execution_state`` is a validated TM-030 coordinator.

TM-033 owns package schema and checksum validation. TM-030 owns execution-chain
validation. This module does not reproduce either responsibility. Freshness is
computed only from the validated embedded TM-062 ``plan_at_utc`` timestamp and
explicit caller-supplied evaluation policy.

This module performs no filesystem or network operations, obtains no provider
or broker state, reads no credentials, submits no orders, performs no paper or
live trading, performs no training or inference, accesses no dataset or final
holdout, and does not perform economic or model qualification.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any

from quantitative_trading_research.artifacts.execution_evidence import (
    ExecutionEvidenceError,
    validate_checksummed_execution_evidence,
)
from quantitative_trading_research.execution.coordinator import (
    ExecutionCoordinatorError,
    validate_execution_coordinator,
)


SCHEMA_ID = "C4_OFFLINE_NO_SUBMIT_PACKAGE_EVALUATION_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_no_submit_package_evaluation"
STATE_PROVENANCE = "validated_canonical_offline_evidence_and_explicit_policy"

PASS_OUTCOME = "PASS"
FAIL_OUTCOME = "FAIL"
INCONCLUSIVE_OUTCOME = "INCONCLUSIVE"

ECONOMIC_QUALIFICATION = "NOT_EVALUATED"
MODEL_QUALITY = "NOT_EVALUATED"
EXECUTION_READINESS = "NOT_ESTABLISHED"
BROKER_STATE_PROVENANCE = "caller_supplied_unverified"

_REASON_STALE = "STALE_EVIDENCE"
_REASON_BROKER_AUTHORITY = "BROKER_STATE_AUTHORITY_NOT_ESTABLISHED"
_REASON_PASS = "OPERATIONAL_REQUIREMENTS_SATISFIED"

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "evaluation_id",
    "source_execution_evidence_checksum",
    "source_execution_evidence_id",
    "source_coordinator_id",
    "evaluation_policy",
    "freshness",
    "operational_evaluation",
    "reason_codes",
    "broker_state_authority",
    "submission_authorized",
    "order_submitted",
    "orders_submitted",
    "economic_qualification",
    "model_quality",
    "execution_readiness",
    "promotion_authorized",
    "order_authorized",
}

_POLICY_KEYS = {
    "evaluation_at_utc",
    "max_age_seconds",
    "require_broker_state_authority",
}

_FRESHNESS_KEYS = {
    "plan_at_utc",
    "evaluation_at_utc",
    "age_seconds",
    "max_age_seconds",
    "passed",
}

_BROKER_AUTHORITY_KEYS = {
    "required",
    "established",
    "source_provenance",
}


class NoSubmitPackageEvaluationError(ValueError):
    """Fail-closed error for malformed package evidence or evaluation policy."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NoSubmitPackageEvaluationError(f"{name} must be a dict")
    return deepcopy(value)


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NoSubmitPackageEvaluationError(
            f"{name} must be a non-empty string"
        )
    if value != value.strip():
        raise NoSubmitPackageEvaluationError(
            f"{name} must not contain surrounding whitespace"
        )
    return value


def _require_bool(name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise NoSubmitPackageEvaluationError(f"{name} must be a bool")
    return value


def _require_max_age(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise NoSubmitPackageEvaluationError(
            "max_age_seconds must be a non-negative finite number"
        )
    normalized = float(value)
    if not math.isfinite(normalized) or normalized < 0.0:
        raise NoSubmitPackageEvaluationError(
            "max_age_seconds must be a non-negative finite number"
        )
    return normalized


def _parse_utc_timestamp(name: str, value: Any) -> datetime:
    text = _require_nonempty_string(name, value)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise NoSubmitPackageEvaluationError(
            f"{name} must be an ISO-8601 UTC timestamp"
        ) from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise NoSubmitPackageEvaluationError(
            f"{name} must include UTC timezone information"
        )

    if parsed.utcoffset().total_seconds() != 0.0:
        raise NoSubmitPackageEvaluationError(
            f"{name} must be expressed in UTC"
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
        raise NoSubmitPackageEvaluationError(
            "evaluation evidence is not canonically serializable"
        ) from exc


def _identity(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _evaluation_identity_payload(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_execution_evidence_checksum": result[
            "source_execution_evidence_checksum"
        ],
        "source_execution_evidence_id": result[
            "source_execution_evidence_id"
        ],
        "source_coordinator_id": result["source_coordinator_id"],
        "evaluation_policy": result["evaluation_policy"],
        "freshness": result["freshness"],
        "operational_evaluation": result["operational_evaluation"],
        "reason_codes": result["reason_codes"],
        "broker_state_authority": result["broker_state_authority"],
        "submission_authorized": result["submission_authorized"],
        "order_submitted": result["order_submitted"],
        "orders_submitted": result["orders_submitted"],
        "economic_qualification": result["economic_qualification"],
        "model_quality": result["model_quality"],
        "execution_readiness": result["execution_readiness"],
        "promotion_authorized": result["promotion_authorized"],
        "order_authorized": result["order_authorized"],
    }


def _validated_package(package: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized = _require_mapping("package", package)

    try:
        validate_checksummed_execution_evidence(normalized)
    except ExecutionEvidenceError as exc:
        raise NoSubmitPackageEvaluationError(
            f"execution-evidence package is invalid: {exc}"
        ) from exc

    record = _require_mapping("package.record", normalized["record"])
    coordinator = _require_mapping(
        "package.record.execution_state",
        record["execution_state"],
    )

    try:
        validate_execution_coordinator(coordinator)
    except ExecutionCoordinatorError as exc:
        raise NoSubmitPackageEvaluationError(
            f"execution_state coordinator is invalid: {exc}"
        ) from exc

    return normalized, coordinator


def evaluate_no_submit_package(
    *,
    package: dict[str, Any],
    evaluation_at_utc: str,
    max_age_seconds: float,
    require_broker_state_authority: bool = False,
) -> dict[str, Any]:
    """Evaluate one validated canonical no-submit execution-evidence package.

    ``evaluation_at_utc`` and ``max_age_seconds`` are explicit caller-supplied
    policy. There is no implicit current-time source.

    ``require_broker_state_authority=True`` demonstrates the explicit
    ``INCONCLUSIVE`` path: TM-033 broker-state fields are intentionally
    caller-supplied and unverified, so this evaluator refuses to pretend that
    they establish broker or account readiness.
    """

    validated_package, coordinator = _validated_package(package)

    evaluation_timestamp = _parse_utc_timestamp(
        "evaluation_at_utc",
        evaluation_at_utc,
    )
    normalized_evaluation_at = evaluation_timestamp.isoformat()
    normalized_max_age = _require_max_age(max_age_seconds)
    require_broker_authority = _require_bool(
        "require_broker_state_authority",
        require_broker_state_authority,
    )

    plan_at_value = coordinator["execution_plan"]["plan_at_utc"]
    plan_timestamp = _parse_utc_timestamp(
        "execution_plan.plan_at_utc",
        plan_at_value,
    )
    normalized_plan_at = plan_timestamp.isoformat()

    if evaluation_timestamp < plan_timestamp:
        raise NoSubmitPackageEvaluationError(
            "evaluation_at_utc must not precede execution_plan.plan_at_utc"
        )

    age_seconds = (evaluation_timestamp - plan_timestamp).total_seconds()
    freshness_passed = age_seconds <= normalized_max_age

    no_submit_preserved = (
        coordinator["submission_authorized"] is False
        and coordinator["order_submitted"] is False
        and coordinator["orders_submitted"] == 0
    )

    reasons: list[str] = []
    if not freshness_passed:
        reasons.append(_REASON_STALE)
    if require_broker_authority:
        reasons.append(_REASON_BROKER_AUTHORITY)

    if not no_submit_preserved or not freshness_passed:
        operational_evaluation = FAIL_OUTCOME
    elif require_broker_authority:
        operational_evaluation = INCONCLUSIVE_OUTCOME
    else:
        operational_evaluation = PASS_OUTCOME
        reasons.append(_REASON_PASS)

    record = validated_package["record"]
    result: dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "evaluation_id": "",
        "source_execution_evidence_checksum": validated_package[
            "checksum_sha256"
        ],
        "source_execution_evidence_id": record["evidence_id"],
        "source_coordinator_id": coordinator["coordinator_id"],
        "evaluation_policy": {
            "evaluation_at_utc": normalized_evaluation_at,
            "max_age_seconds": normalized_max_age,
            "require_broker_state_authority": require_broker_authority,
        },
        "freshness": {
            "plan_at_utc": normalized_plan_at,
            "evaluation_at_utc": normalized_evaluation_at,
            "age_seconds": age_seconds,
            "max_age_seconds": normalized_max_age,
            "passed": freshness_passed,
        },
        "operational_evaluation": operational_evaluation,
        "reason_codes": reasons,
        "broker_state_authority": {
            "required": require_broker_authority,
            "established": False,
            "source_provenance": BROKER_STATE_PROVENANCE,
        },
        "submission_authorized": False,
        "order_submitted": False,
        "orders_submitted": 0,
        "economic_qualification": ECONOMIC_QUALIFICATION,
        "model_quality": MODEL_QUALITY,
        "execution_readiness": EXECUTION_READINESS,
        "promotion_authorized": False,
        "order_authorized": False,
    }

    result["evaluation_id"] = _identity(
        "no_submit_package_evaluation",
        _evaluation_identity_payload(result),
    )

    validate_no_submit_package_evaluation(result)
    return result


def validate_no_submit_package_evaluation(result: Any) -> None:
    """Fail closed on malformed or internally inconsistent TM-061 results."""

    value = _require_mapping("result", result)

    if set(value) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(value))
        unexpected = sorted(set(value) - _RESULT_KEYS)
        raise NoSubmitPackageEvaluationError(
            "result keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if value["schema_id"] != SCHEMA_ID:
        raise NoSubmitPackageEvaluationError("unsupported schema_id")
    if type(value["schema_version"]) is not int:
        raise NoSubmitPackageEvaluationError(
            "schema_version must be an int"
        )
    if value["schema_version"] != SCHEMA_VERSION:
        raise NoSubmitPackageEvaluationError("unsupported schema_version")
    if value["result_type"] != RESULT_TYPE:
        raise NoSubmitPackageEvaluationError("unsupported result_type")
    if value["state_provenance"] != STATE_PROVENANCE:
        raise NoSubmitPackageEvaluationError("unsupported state_provenance")

    _require_nonempty_string("evaluation_id", value["evaluation_id"])
    checksum = _require_nonempty_string(
        "source_execution_evidence_checksum",
        value["source_execution_evidence_checksum"],
    )
    if len(checksum) != 64 or any(
        character not in "0123456789abcdefABCDEF" for character in checksum
    ):
        raise NoSubmitPackageEvaluationError(
            "source execution evidence checksum must be SHA-256 hex"
        )
    _require_nonempty_string(
        "source_execution_evidence_id",
        value["source_execution_evidence_id"],
    )
    _require_nonempty_string(
        "source_coordinator_id",
        value["source_coordinator_id"],
    )

    policy = _require_mapping("evaluation_policy", value["evaluation_policy"])
    if set(policy) != _POLICY_KEYS:
        raise NoSubmitPackageEvaluationError("evaluation_policy keys mismatch")

    evaluation_at = _canonical_timestamp(
        "evaluation_policy.evaluation_at_utc",
        policy["evaluation_at_utc"],
    )
    max_age = _require_max_age(policy["max_age_seconds"])
    require_broker = _require_bool(
        "evaluation_policy.require_broker_state_authority",
        policy["require_broker_state_authority"],
    )

    if policy["evaluation_at_utc"] != evaluation_at:
        raise NoSubmitPackageEvaluationError(
            "evaluation_at_utc must be canonical UTC"
        )

    freshness = _require_mapping("freshness", value["freshness"])
    if set(freshness) != _FRESHNESS_KEYS:
        raise NoSubmitPackageEvaluationError("freshness keys mismatch")

    plan_at = _canonical_timestamp(
        "freshness.plan_at_utc",
        freshness["plan_at_utc"],
    )
    freshness_evaluation_at = _canonical_timestamp(
        "freshness.evaluation_at_utc",
        freshness["evaluation_at_utc"],
    )
    if freshness_evaluation_at != evaluation_at:
        raise NoSubmitPackageEvaluationError(
            "freshness evaluation timestamp does not match policy"
        )

    plan_timestamp = _parse_utc_timestamp("freshness.plan_at_utc", plan_at)
    evaluation_timestamp = _parse_utc_timestamp(
        "freshness.evaluation_at_utc",
        freshness_evaluation_at,
    )
    if evaluation_timestamp < plan_timestamp:
        raise NoSubmitPackageEvaluationError(
            "freshness evaluation timestamp precedes plan timestamp"
        )

    expected_age = (evaluation_timestamp - plan_timestamp).total_seconds()
    if freshness["age_seconds"] != expected_age:
        raise NoSubmitPackageEvaluationError("freshness age_seconds mismatch")
    if freshness["max_age_seconds"] != max_age:
        raise NoSubmitPackageEvaluationError(
            "freshness max_age_seconds mismatch"
        )
    if type(freshness["passed"]) is not bool:
        raise NoSubmitPackageEvaluationError("freshness passed must be a bool")
    if freshness["passed"] is not (expected_age <= max_age):
        raise NoSubmitPackageEvaluationError("freshness passed is inconsistent")

    broker_authority = _require_mapping(
        "broker_state_authority",
        value["broker_state_authority"],
    )
    if set(broker_authority) != _BROKER_AUTHORITY_KEYS:
        raise NoSubmitPackageEvaluationError(
            "broker_state_authority keys mismatch"
        )
    if broker_authority["required"] is not require_broker:
        raise NoSubmitPackageEvaluationError(
            "broker authority requirement does not match policy"
        )
    if broker_authority["established"] is not False:
        raise NoSubmitPackageEvaluationError(
            "broker state authority must remain unestablished"
        )
    if broker_authority["source_provenance"] != BROKER_STATE_PROVENANCE:
        raise NoSubmitPackageEvaluationError(
            "broker state provenance must remain caller-supplied and unverified"
        )

    if not isinstance(value["reason_codes"], list) or not all(
        isinstance(reason, str) and reason for reason in value["reason_codes"]
    ):
        raise NoSubmitPackageEvaluationError(
            "reason_codes must be a list of non-empty strings"
        )

    expected_reasons: list[str] = []
    if not freshness["passed"]:
        expected_reasons.append(_REASON_STALE)
    if require_broker:
        expected_reasons.append(_REASON_BROKER_AUTHORITY)
    if not expected_reasons:
        expected_reasons.append(_REASON_PASS)

    if value["reason_codes"] != expected_reasons:
        raise NoSubmitPackageEvaluationError(
            "reason_codes are not in canonical deterministic order"
        )

    if not freshness["passed"]:
        expected_outcome = FAIL_OUTCOME
    elif require_broker:
        expected_outcome = INCONCLUSIVE_OUTCOME
    else:
        expected_outcome = PASS_OUTCOME

    if value["operational_evaluation"] != expected_outcome:
        raise NoSubmitPackageEvaluationError(
            "operational_evaluation is inconsistent with evidence"
        )

    if value["submission_authorized"] is not False:
        raise NoSubmitPackageEvaluationError(
            "submission_authorized must remain False"
        )
    if value["order_submitted"] is not False:
        raise NoSubmitPackageEvaluationError("order_submitted must remain False")
    if value["orders_submitted"] != 0:
        raise NoSubmitPackageEvaluationError("orders_submitted must remain zero")
    if value["economic_qualification"] != ECONOMIC_QUALIFICATION:
        raise NoSubmitPackageEvaluationError(
            "economic qualification must remain NOT_EVALUATED"
        )
    if value["model_quality"] != MODEL_QUALITY:
        raise NoSubmitPackageEvaluationError(
            "model quality must remain NOT_EVALUATED"
        )
    if value["execution_readiness"] != EXECUTION_READINESS:
        raise NoSubmitPackageEvaluationError(
            "execution readiness must remain NOT_ESTABLISHED"
        )
    if value["promotion_authorized"] is not False:
        raise NoSubmitPackageEvaluationError(
            "promotion_authorized must remain False"
        )
    if value["order_authorized"] is not False:
        raise NoSubmitPackageEvaluationError("order_authorized must remain False")

    expected_identity = _identity(
        "no_submit_package_evaluation",
        _evaluation_identity_payload(value),
    )
    if value["evaluation_id"] != expected_identity:
        raise NoSubmitPackageEvaluationError(
            "evaluation_id does not match canonical evaluation evidence"
        )
