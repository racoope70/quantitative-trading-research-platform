"""Pure offline construction of checksummed execution-evidence records.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/logging_utils.py``.

This C4 module preserves only deterministic execution-evidence construction.
Broker-state values are opaque caller-supplied data and are never acquired,
validated as operationally authoritative, or used to submit orders.

The module performs no filesystem, network, provider, broker, training,
final-holdout, paper-trading, or live-trading operations.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
from typing import Any


SCHEMA_ID = "C4_EXECUTION_EVIDENCE_V1"
SCHEMA_VERSION = 1
EVIDENCE_TYPE = "offline_execution_evidence"
CHECKSUM_ALGORITHM = "sha256"
BROKER_STATE_PROVENANCE = "caller_supplied_unverified"

_RECORD_KEYS = {
    "schema_id",
    "schema_version",
    "evidence_type",
    "evidence_id",
    "metadata",
    "execution_state",
    "broker_state_before",
    "broker_state_after",
    "broker_state_provenance",
}

_PACKAGE_KEYS = {
    "record",
    "checksum_algorithm",
    "checksum_sha256",
}


class ExecutionEvidenceError(ValueError):
    """Fail-closed error for invalid canonical execution evidence."""


def normalize_evidence_value(value: Any) -> Any:
    """Return a deterministic JSON-compatible representation.

    Only explicitly supported data shapes are accepted. Unknown objects,
    non-string mapping keys, sets, non-finite floats, and other ambiguous
    values fail closed rather than being stringified implicitly.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ExecutionEvidenceError(
                "execution evidence does not permit non-finite floats"
            )
        return value

    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ExecutionEvidenceError(
                    "execution evidence mapping keys must be strings"
                )
            normalized[key] = normalize_evidence_value(item)
        return normalized

    if isinstance(value, (list, tuple)):
        return [normalize_evidence_value(item) for item in value]

    raise ExecutionEvidenceError(
        "unsupported execution evidence value type: "
        f"{type(value).__name__}"
    )


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize supported evidence data deterministically as canonical JSON."""
    normalized = normalize_evidence_value(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def checksum_sha256(value: Any) -> str:
    """Return the SHA-256 checksum of canonical serialized evidence data."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionEvidenceError(f"{name} must be a dict")
    normalized = normalize_evidence_value(value)
    if not isinstance(normalized, dict):
        raise ExecutionEvidenceError(f"{name} must normalize to a dict")
    return normalized


def build_execution_evidence_record(
    *,
    evidence_id: str,
    execution_state: dict[str, Any],
    broker_state_before: dict[str, Any] | None = None,
    broker_state_after: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one deterministic, non-operational execution-evidence record.

    ``broker_state_before`` and ``broker_state_after`` are opaque data supplied
    by the caller. This function does not obtain broker state or establish that
    supplied state is current, accepted, connected, or operationally valid.
    """
    if not isinstance(evidence_id, str) or not evidence_id.strip():
        raise ExecutionEvidenceError(
            "evidence_id must be a non-empty string"
        )

    record = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "evidence_type": EVIDENCE_TYPE,
        "evidence_id": evidence_id,
        "metadata": _require_mapping(
            "metadata",
            {} if metadata is None else metadata,
        ),
        "execution_state": _require_mapping(
            "execution_state",
            execution_state,
        ),
        "broker_state_before": _require_mapping(
            "broker_state_before",
            {} if broker_state_before is None else broker_state_before,
        ),
        "broker_state_after": _require_mapping(
            "broker_state_after",
            {} if broker_state_after is None else broker_state_after,
        ),
        "broker_state_provenance": BROKER_STATE_PROVENANCE,
    }

    validate_execution_evidence_record(record)
    return record


def validate_execution_evidence_record(record: Any) -> None:
    """Fail closed on malformed or unsupported execution-evidence records."""
    if not isinstance(record, dict):
        raise ExecutionEvidenceError(
            "execution evidence record must be a dict"
        )

    if set(record) != _RECORD_KEYS:
        missing = sorted(_RECORD_KEYS - set(record))
        unexpected = sorted(set(record) - _RECORD_KEYS)
        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))
        raise ExecutionEvidenceError(
            "execution evidence record keys mismatch: " + "; ".join(details)
        )

    if record["schema_id"] != SCHEMA_ID:
        raise ExecutionEvidenceError(
            "unsupported execution evidence schema_id"
        )

    if type(record["schema_version"]) is not int:
        raise ExecutionEvidenceError(
            "execution evidence schema_version must be an int"
        )

    if record["schema_version"] != SCHEMA_VERSION:
        raise ExecutionEvidenceError(
            "unsupported execution evidence schema_version"
        )

    if record["evidence_type"] != EVIDENCE_TYPE:
        raise ExecutionEvidenceError(
            "unsupported execution evidence type"
        )

    evidence_id = record["evidence_id"]
    if not isinstance(evidence_id, str) or not evidence_id.strip():
        raise ExecutionEvidenceError(
            "execution evidence evidence_id must be a non-empty string"
        )

    if record["broker_state_provenance"] != BROKER_STATE_PROVENANCE:
        raise ExecutionEvidenceError(
            "broker state provenance must remain caller-supplied and unverified"
        )

    for name in (
        "metadata",
        "execution_state",
        "broker_state_before",
        "broker_state_after",
    ):
        _require_mapping(name, record[name])

    normalize_evidence_value(record)


def build_checksummed_execution_evidence(
    *,
    evidence_id: str,
    execution_state: dict[str, Any],
    broker_state_before: dict[str, Any] | None = None,
    broker_state_after: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic execution-evidence record plus SHA-256 identity."""
    record = build_execution_evidence_record(
        evidence_id=evidence_id,
        execution_state=execution_state,
        broker_state_before=broker_state_before,
        broker_state_after=broker_state_after,
        metadata=metadata,
    )

    package = {
        "record": record,
        "checksum_algorithm": CHECKSUM_ALGORITHM,
        "checksum_sha256": checksum_sha256(record),
    }

    validate_checksummed_execution_evidence(package)
    return package


def validate_checksummed_execution_evidence(package: Any) -> None:
    """Fail closed on malformed evidence packages or checksum mismatches."""
    if not isinstance(package, dict):
        raise ExecutionEvidenceError(
            "checksummed execution evidence must be a dict"
        )

    if set(package) != _PACKAGE_KEYS:
        missing = sorted(_PACKAGE_KEYS - set(package))
        unexpected = sorted(set(package) - _PACKAGE_KEYS)
        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))
        raise ExecutionEvidenceError(
            "checksummed execution evidence keys mismatch: "
            + "; ".join(details)
        )

    if package["checksum_algorithm"] != CHECKSUM_ALGORITHM:
        raise ExecutionEvidenceError(
            "unsupported execution evidence checksum algorithm"
        )

    expected_checksum = package["checksum_sha256"]
    if not isinstance(expected_checksum, str):
        raise ExecutionEvidenceError(
            "execution evidence checksum must be a string"
        )

    normalized_checksum = expected_checksum.strip().lower()
    if len(normalized_checksum) != 64 or any(
        character not in "0123456789abcdef"
        for character in normalized_checksum
    ):
        raise ExecutionEvidenceError(
            "execution evidence checksum must be SHA-256 hex"
        )

    record = package["record"]
    validate_execution_evidence_record(record)

    actual_checksum = checksum_sha256(record)
    if not hmac.compare_digest(actual_checksum, normalized_checksum):
        raise ExecutionEvidenceError(
            "execution evidence checksum mismatch"
        )
