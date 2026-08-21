"""Deterministic offline diagnostic-evidence utilities.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/diagnostics.py``.

This C4 module preserves only pure diagnostic evaluation over explicit,
caller-supplied observations. It does not discover project state, inspect
datasets or models, read or write files, access providers or networks, execute
training or inference, access a final holdout, or submit orders.
"""

from __future__ import annotations

import math
from typing import Any


DIAGNOSTIC_SCHEMA_ID = "C4_OFFLINE_DIAGNOSTIC_EVIDENCE_V1"
DIAGNOSTIC_SCHEMA_VERSION = 1
DIAGNOSTIC_SCOPE = "CALLER_SUPPLIED_OFFLINE_OBSERVATIONS"

PASS_OUTCOME = "PASS"
FAIL_REQUIRED_OBSERVATION_OUTCOME = "FAIL_REQUIRED_OBSERVATION"

_EVIDENCE_KEYS = {
    "schema_id",
    "schema_version",
    "scope",
    "diagnostic_id",
    "metadata",
    "required_observations",
    "optional_observations",
    "failed_required_observations",
    "terminal_outcome",
}


class DiagnosticEvidenceError(ValueError):
    """Fail-closed error for malformed offline diagnostic evidence."""


def normalize_diagnostic_value(value: Any) -> Any:
    """Return a deterministic structured representation of supported values."""
    if value is None or type(value) in (str, bool, int):
        return value

    if type(value) is float:
        if not math.isfinite(value):
            raise DiagnosticEvidenceError(
                "diagnostic evidence does not permit non-finite floats"
            )
        return value

    if type(value) is dict:
        if any(not isinstance(key, str) for key in value):
            raise DiagnosticEvidenceError(
                "diagnostic evidence mapping keys must be strings"
            )

        normalized: dict[str, Any] = {}
        for key in sorted(value):
            normalized[key] = normalize_diagnostic_value(value[key])
        return normalized

    if type(value) in (list, tuple):
        return [normalize_diagnostic_value(item) for item in value]

    raise DiagnosticEvidenceError(
        "unsupported diagnostic evidence value type: "
        f"{type(value).__name__}"
    )


def _require_metadata(value: Any) -> dict[str, Any]:
    if type(value) is not dict:
        raise DiagnosticEvidenceError("metadata must be a dict")

    normalized = normalize_diagnostic_value(value)
    if type(normalized) is not dict:
        raise DiagnosticEvidenceError("metadata must normalize to a dict")

    return normalized


def _require_observations(
    name: str,
    value: Any,
    *,
    allow_empty: bool,
) -> dict[str, bool]:
    if type(value) is not dict:
        raise DiagnosticEvidenceError(f"{name} must be a dict")

    if not allow_empty and not value:
        raise DiagnosticEvidenceError(f"{name} must not be empty")

    for key in value:
        if not isinstance(key, str) or not key.strip():
            raise DiagnosticEvidenceError(
                f"{name} keys must be non-empty strings"
            )

        if key != key.strip():
            raise DiagnosticEvidenceError(
                f"{name} keys must not contain surrounding whitespace"
            )

    normalized: dict[str, bool] = {}

    for key in sorted(value):
        observation = value[key]
        if type(observation) is not bool:
            raise DiagnosticEvidenceError(
                f"{name} values must be bool"
            )

        normalized[key] = observation

    return normalized


def build_diagnostic_evidence(
    *,
    diagnostic_id: str,
    required_observations: dict[str, bool],
    optional_observations: dict[str, bool] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build deterministic diagnostic evidence from explicit observations.

    Required observations control the terminal outcome. A false required
    observation produces ``FAIL_REQUIRED_OBSERVATION``. Optional observations
    are preserved as evidence but never alter the terminal outcome.
    """
    if not isinstance(diagnostic_id, str) or not diagnostic_id.strip():
        raise DiagnosticEvidenceError(
            "diagnostic_id must be a non-empty string"
        )

    if diagnostic_id != diagnostic_id.strip():
        raise DiagnosticEvidenceError(
            "diagnostic_id must not contain surrounding whitespace"
        )

    required = _require_observations(
        "required_observations",
        required_observations,
        allow_empty=False,
    )
    optional = _require_observations(
        "optional_observations",
        {} if optional_observations is None else optional_observations,
        allow_empty=True,
    )

    overlap = sorted(set(required) & set(optional))
    if overlap:
        raise DiagnosticEvidenceError(
            "required and optional observations must not overlap: "
            + ",".join(overlap)
        )

    failed_required = [
        name
        for name, passed in required.items()
        if not passed
    ]

    terminal_outcome = (
        PASS_OUTCOME
        if not failed_required
        else FAIL_REQUIRED_OBSERVATION_OUTCOME
    )

    evidence = {
        "schema_id": DIAGNOSTIC_SCHEMA_ID,
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "scope": DIAGNOSTIC_SCOPE,
        "diagnostic_id": diagnostic_id,
        "metadata": _require_metadata(
            {} if metadata is None else metadata
        ),
        "required_observations": required,
        "optional_observations": optional,
        "failed_required_observations": failed_required,
        "terminal_outcome": terminal_outcome,
    }

    validate_diagnostic_evidence(evidence)
    return evidence


def validate_diagnostic_evidence(evidence: Any) -> None:
    """Fail closed on malformed or internally inconsistent evidence."""
    if type(evidence) is not dict:
        raise DiagnosticEvidenceError(
            "diagnostic evidence must be a dict"
        )

    if set(evidence) != _EVIDENCE_KEYS:
        missing = sorted(_EVIDENCE_KEYS - set(evidence))
        unexpected = sorted(set(evidence) - _EVIDENCE_KEYS)
        details: list[str] = []

        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))

        raise DiagnosticEvidenceError(
            "diagnostic evidence keys mismatch: " + "; ".join(details)
        )

    if evidence["schema_id"] != DIAGNOSTIC_SCHEMA_ID:
        raise DiagnosticEvidenceError(
            "unsupported diagnostic schema_id"
        )

    if type(evidence["schema_version"]) is not int:
        raise DiagnosticEvidenceError(
            "diagnostic schema_version must be an int"
        )

    if evidence["schema_version"] != DIAGNOSTIC_SCHEMA_VERSION:
        raise DiagnosticEvidenceError(
            "unsupported diagnostic schema_version"
        )

    if evidence["scope"] != DIAGNOSTIC_SCOPE:
        raise DiagnosticEvidenceError(
            "unsupported diagnostic scope"
        )

    diagnostic_id = evidence["diagnostic_id"]
    if (
        not isinstance(diagnostic_id, str)
        or not diagnostic_id.strip()
        or diagnostic_id != diagnostic_id.strip()
    ):
        raise DiagnosticEvidenceError(
            "diagnostic_id must be a non-empty string without surrounding whitespace"
        )

    metadata = _require_metadata(evidence["metadata"])
    if metadata != evidence["metadata"]:
        raise DiagnosticEvidenceError(
            "diagnostic metadata is not deterministically normalized"
        )

    required = _require_observations(
        "required_observations",
        evidence["required_observations"],
        allow_empty=False,
    )
    optional = _require_observations(
        "optional_observations",
        evidence["optional_observations"],
        allow_empty=True,
    )

    overlap = sorted(set(required) & set(optional))
    if overlap:
        raise DiagnosticEvidenceError(
            "required and optional observations must not overlap: "
            + ",".join(overlap)
        )

    expected_failed = [
        name
        for name, passed in required.items()
        if not passed
    ]

    failed = evidence["failed_required_observations"]
    if type(failed) is not list or any(
        not isinstance(name, str)
        for name in failed
    ):
        raise DiagnosticEvidenceError(
            "failed_required_observations must be a list of strings"
        )

    if failed != expected_failed:
        raise DiagnosticEvidenceError(
            "failed_required_observations is inconsistent with required observations"
        )

    expected_outcome = (
        PASS_OUTCOME
        if not expected_failed
        else FAIL_REQUIRED_OBSERVATION_OUTCOME
    )

    if evidence["terminal_outcome"] != expected_outcome:
        raise DiagnosticEvidenceError(
            "terminal_outcome is inconsistent with required observations"
        )
