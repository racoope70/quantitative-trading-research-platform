"""Pure deterministic offline broker-neutral external-signal package producer.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/adapters/quantconnect.py``.

Only deterministic package construction and validation are preserved. Caller-
supplied publication/availability timestamps are evidence, not proof of remote
publication. No filesystem, network, credential, provider, broker, order,
training, inference, dataset, final-holdout, paper-, or live-trading behavior
is performed.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import hmac
import json
import math
from typing import Any

SCHEMA_ID = "C4_BROKER_NEUTRAL_EXTERNAL_SIGNAL_PACKAGE_V1"
SCHEMA_VERSION = 1
PACKAGE_TYPE = "broker_neutral_external_signal_package"
CHECKSUM_ALGORITHM = "sha256"
SUPPORTED_SIGNAL_VALUES = ("BUY", "SELL", "HOLD")
STORAGE_REQUIREMENT_STATUS = "DEFERRED__NOT_PERFORMED_IN_CURRENT_C4_COMPONENT"
PUBLICATION_EVIDENCE_STATUS = "CALLER_SUPPLIED_EVIDENCE_ONLY"

_RECORD_KEYS = {
    "schema_id", "schema_version", "package_type", "run_id", "package_id",
    "producer_identity", "producer_commit", "model_identity", "model_sha256",
    "artifact_identity", "artifact_sha256", "prediction_identity",
    "prediction_sha256", "alias_policy", "evaluation_at_utc",
    "publication_at_utc", "availability_at_utc", "signals",
    "storage_requirement_status",
    "publication_evidence_status", "authenticated_storage_completed",
    "remote_publication_completed", "provider_publication_completed",
}
_PACKAGE_KEYS = {"record", "checksum_algorithm", "package_sha256"}
_ALIAS_KEYS = {"alias", "canonical_instrument_id"}
_SIGNAL_INPUT_REQUIRED = {
    "instrument_id", "canonical_instrument_id", "signal",
    "prediction_at_utc", "decision_at_utc", "valid_until_utc",
}
_SIGNAL_INPUT_ALLOWED = _SIGNAL_INPUT_REQUIRED | {"confidence"}
_SIGNAL_KEYS = _SIGNAL_INPUT_ALLOWED | {"signal_id"}


class ExternalSignalPackageError(ValueError):
    """Fail-closed error for malformed or inconsistent TM-019 evidence."""


def _mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExternalSignalPackageError(f"{name} must be a dict")
    return deepcopy(value)


def _keys(name: str, value: dict[str, Any], expected: set[str]) -> None:
    if set(value) != expected:
        raise ExternalSignalPackageError(
            f"{name} keys mismatch: missing={sorted(expected - set(value))}; "
            f"unexpected={sorted(set(value) - expected)}"
        )


def _text(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ExternalSignalPackageError(
            f"{name} must be a non-empty string without surrounding whitespace"
        )
    return value


def _hex(name: str, value: Any, length: int) -> str:
    text = _text(name, value)
    if len(text) != length or any(c not in "0123456789abcdef" for c in text):
        raise ExternalSignalPackageError(
            f"{name} must be lowercase {length}-character hex"
        )
    return text


def _sha(name: str, value: Any) -> str:
    return _hex(name, value, 64)


def _commit(name: str, value: Any) -> str:
    return _hex(name, value, 40)


def _utc(name: str, value: Any) -> datetime:
    text = _text(name, value)
    candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ExternalSignalPackageError(
            f"{name} must be an ISO-8601 UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExternalSignalPackageError(f"{name} must be timezone-aware UTC")
    if parsed.utcoffset().total_seconds() != 0:
        raise ExternalSignalPackageError(f"{name} must be expressed in UTC")
    return parsed.astimezone(timezone.utc)


def _utc_text(name: str, value: Any) -> str:
    return _utc(name, value).isoformat()


def _confidence(name: str, value: Any) -> float | None:
    if value is None:
        return None
    if type(value) is not float:
        raise ExternalSignalPackageError(
            f"{name} must be null or a canonical float in [0, 1]"
        )
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ExternalSignalPackageError(
            f"{name} must be null or a finite canonical float in [0, 1]"
        )
    return value


def _json(value: Any) -> str:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ExternalSignalPackageError(
            "external-signal evidence is not canonically serializable"
        ) from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _identity(prefix: str, value: Any) -> str:
    return f"{prefix}:{_digest(value)}"


def _aliases(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ExternalSignalPackageError("aliases must be a list")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for i, raw in enumerate(value):
        item = _mapping(f"aliases[{i}]", raw)
        _keys(f"aliases[{i}]", item, _ALIAS_KEYS)
        alias = _text(f"aliases[{i}].alias", item["alias"])
        canonical = _text(
            f"aliases[{i}].canonical_instrument_id",
            item["canonical_instrument_id"],
        )
        if alias == canonical or alias in seen:
            raise ExternalSignalPackageError(
                f"ambiguous or malformed alias: {alias}"
            )
        seen.add(alias)
        result.append({"alias": alias, "canonical_instrument_id": canonical})
    return sorted(result, key=lambda item: item["alias"])


def _signal_payload(
    signal: dict[str, Any],
    prediction_identity: str,
    prediction_sha256: str,
) -> dict[str, Any]:
    return {
        "prediction_identity": prediction_identity,
        "prediction_sha256": prediction_sha256,
        "signal": {
            key: signal[key] for key in _SIGNAL_KEYS if key != "signal_id"
        },
    }


def _normalize_signal(
    raw: Any,
    index: int,
    prediction_identity: str,
    prediction_sha256: str,
) -> dict[str, Any]:
    item = _mapping(f"signals[{index}]", raw)
    missing = _SIGNAL_INPUT_REQUIRED - set(item)
    unexpected = set(item) - _SIGNAL_INPUT_ALLOWED
    if missing or unexpected:
        raise ExternalSignalPackageError(
            f"signals[{index}] keys mismatch: missing={sorted(missing)}; "
            f"unexpected={sorted(unexpected)}"
        )
    signal = {
        "signal_id": "",
        "instrument_id": _text(
            f"signals[{index}].instrument_id", item["instrument_id"]
        ),
        "canonical_instrument_id": _text(
            f"signals[{index}].canonical_instrument_id",
            item["canonical_instrument_id"],
        ),
        "signal": _text(f"signals[{index}].signal", item["signal"]),
        "prediction_at_utc": _utc_text(
            f"signals[{index}].prediction_at_utc", item["prediction_at_utc"]
        ),
        "decision_at_utc": _utc_text(
            f"signals[{index}].decision_at_utc", item["decision_at_utc"]
        ),
        "valid_until_utc": _utc_text(
            f"signals[{index}].valid_until_utc", item["valid_until_utc"]
        ),
        "confidence": _confidence(
            f"signals[{index}].confidence", item.get("confidence")
        ),
    }
    if signal["signal"] not in SUPPORTED_SIGNAL_VALUES:
        raise ExternalSignalPackageError(
            f"unsupported signal value: {signal['signal']}"
        )
    signal["signal_id"] = _identity(
        "external_signal",
        _signal_payload(signal, prediction_identity, prediction_sha256),
    )
    return signal


def _instrument_contract(
    signals: list[dict[str, Any]],
    alias_policy: list[dict[str, str]],
) -> None:
    alias_map = {
        item["alias"]: item["canonical_instrument_id"] for item in alias_policy
    }
    canonicals = [item["canonical_instrument_id"] for item in signals]
    if len(canonicals) != len(set(canonicals)):
        raise ExternalSignalPackageError(
            "duplicate canonical instruments are not permitted"
        )
    if set(alias_map) & set(canonicals):
        raise ExternalSignalPackageError(
            "alias identity collides with canonical instrument identity"
        )
    used: set[str] = set()
    for signal in signals:
        source = signal["instrument_id"]
        canonical = signal["canonical_instrument_id"]
        if source == canonical:
            continue
        if source not in alias_map:
            raise ExternalSignalPackageError(
                f"explicit alias required for instrument: {source}"
            )
        if alias_map[source] != canonical:
            raise ExternalSignalPackageError(
                f"alias does not resolve to supplied canonical instrument: {source}"
            )
        used.add(source)
    unused = set(alias_map) - used
    if unused:
        raise ExternalSignalPackageError(
            "alias policy contains unused aliases: " + ",".join(sorted(unused))
        )


def _temporal_contract(
    signals: list[dict[str, Any]],
    publication_at_utc: str,
    availability_at_utc: str,
    evaluation_at_utc: str,
) -> None:
    publication = _utc("publication_at_utc", publication_at_utc)
    availability = _utc("availability_at_utc", availability_at_utc)
    evaluation = _utc("evaluation_at_utc", evaluation_at_utc)
    if publication > availability:
        raise ExternalSignalPackageError(
            "publication_at_utc must not follow availability_at_utc"
        )
    if publication > evaluation:
        raise ExternalSignalPackageError(
            "publication_at_utc is future relative to evaluation_at_utc"
        )
    if availability > evaluation:
        raise ExternalSignalPackageError(
            "availability_at_utc is future relative to evaluation_at_utc"
        )
    for i, signal in enumerate(signals):
        prediction = _utc(
            f"signals[{i}].prediction_at_utc", signal["prediction_at_utc"]
        )
        decision = _utc(
            f"signals[{i}].decision_at_utc", signal["decision_at_utc"]
        )
        valid_until = _utc(
            f"signals[{i}].valid_until_utc", signal["valid_until_utc"]
        )
        if prediction > decision:
            raise ExternalSignalPackageError(
                "prediction_at_utc must not follow decision_at_utc"
            )
        if decision > publication:
            raise ExternalSignalPackageError(
                "decision_at_utc must not follow publication_at_utc"
            )
        if availability > valid_until:
            raise ExternalSignalPackageError(
                "availability_at_utc must not follow valid_until_utc"
            )
        if prediction > evaluation:
            raise ExternalSignalPackageError(
                "prediction_at_utc is future relative to evaluation_at_utc"
            )
        if decision > evaluation:
            raise ExternalSignalPackageError(
                "decision_at_utc is future relative to evaluation_at_utc"
            )
        if evaluation > valid_until:
            raise ExternalSignalPackageError(
                "signal evidence is stale at evaluation_at_utc"
            )


def _run_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        key: record[key]
        for key in (
            "producer_identity", "producer_commit", "model_identity",
            "model_sha256", "artifact_identity", "artifact_sha256",
            "prediction_identity", "prediction_sha256", "alias_policy",
            "evaluation_at_utc", "publication_at_utc",
            "availability_at_utc", "signals",
        )
    }


def _package_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        key: record[key]
        for key in (
            "schema_id", "schema_version", "package_type", "run_id",
            "storage_requirement_status", "publication_evidence_status",
            "authenticated_storage_completed", "remote_publication_completed",
            "provider_publication_completed",
        )
    }


def build_external_signal_package(
    *,
    producer_identity: str,
    producer_commit: str,
    model_identity: str,
    model_sha256: str,
    artifact_identity: str,
    artifact_sha256: str,
    prediction_identity: str,
    prediction_sha256: str,
    signals: list[dict[str, Any]],
    publication_at_utc: str,
    availability_at_utc: str,
    evaluation_at_utc: str,
    aliases: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Construct and validate deterministic immutable TM-019 evidence."""
    if not isinstance(signals, list) or not signals:
        raise ExternalSignalPackageError("signals must be a non-empty list")

    producer_identity = _text("producer_identity", producer_identity)
    producer_commit = _commit("producer_commit", producer_commit)
    model_identity = _text("model_identity", model_identity)
    model_sha256 = _sha("model_sha256", model_sha256)
    artifact_identity = _text("artifact_identity", artifact_identity)
    artifact_sha256 = _sha("artifact_sha256", artifact_sha256)
    prediction_identity = _text("prediction_identity", prediction_identity)
    prediction_sha256 = _sha("prediction_sha256", prediction_sha256)
    publication_at_utc = _utc_text("publication_at_utc", publication_at_utc)
    availability_at_utc = _utc_text("availability_at_utc", availability_at_utc)
    evaluation_at_utc = _utc_text("evaluation_at_utc", evaluation_at_utc)
    alias_policy = _aliases(aliases)

    normalized_signals = [
        _normalize_signal(
            raw, i, prediction_identity, prediction_sha256
        )
        for i, raw in enumerate(deepcopy(signals))
    ]
    normalized_signals.sort(key=lambda item: item["canonical_instrument_id"])
    _instrument_contract(normalized_signals, alias_policy)
    _temporal_contract(
        normalized_signals, publication_at_utc,
        availability_at_utc, evaluation_at_utc,
    )

    record: dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "package_type": PACKAGE_TYPE,
        "run_id": "",
        "package_id": "",
        "producer_identity": producer_identity,
        "producer_commit": producer_commit,
        "model_identity": model_identity,
        "model_sha256": model_sha256,
        "artifact_identity": artifact_identity,
        "artifact_sha256": artifact_sha256,
        "prediction_identity": prediction_identity,
        "prediction_sha256": prediction_sha256,
        "alias_policy": alias_policy,
        "evaluation_at_utc": evaluation_at_utc,
        "publication_at_utc": publication_at_utc,
        "availability_at_utc": availability_at_utc,
        "signals": normalized_signals,
        "storage_requirement_status": STORAGE_REQUIREMENT_STATUS,
        "publication_evidence_status": PUBLICATION_EVIDENCE_STATUS,
        "authenticated_storage_completed": False,
        "remote_publication_completed": False,
        "provider_publication_completed": False,
    }
    record["run_id"] = _identity("external_signal_run", _run_payload(record))
    record["package_id"] = _identity(
        "external_signal_package", _package_payload(record)
    )
    package = {
        "record": record,
        "checksum_algorithm": CHECKSUM_ALGORITHM,
        "package_sha256": _digest(record),
    }
    validate_external_signal_package(
        package, evaluation_at_utc=evaluation_at_utc
    )
    return package


def validate_external_signal_package(
    package: Any,
    *,
    evaluation_at_utc: str,
) -> None:
    """Reject malformed, stale, future, forged, or tampered package evidence."""
    value = _mapping("package", package)
    _keys("package", value, _PACKAGE_KEYS)
    if value["checksum_algorithm"] != CHECKSUM_ALGORITHM:
        raise ExternalSignalPackageError("unsupported checksum algorithm")
    package_sha256 = _sha("package_sha256", value["package_sha256"])

    record = _mapping("package.record", value["record"])
    _keys("package.record", record, _RECORD_KEYS)
    if record["schema_id"] != SCHEMA_ID:
        raise ExternalSignalPackageError("unsupported schema_id")
    if type(record["schema_version"]) is not int:
        raise ExternalSignalPackageError("schema_version must be an int")
    if record["schema_version"] != SCHEMA_VERSION:
        raise ExternalSignalPackageError("unsupported schema_version")
    if record["package_type"] != PACKAGE_TYPE:
        raise ExternalSignalPackageError("unsupported package_type")

    _text("run_id", record["run_id"])
    _text("package_id", record["package_id"])
    _text("producer_identity", record["producer_identity"])
    _commit("producer_commit", record["producer_commit"])
    _text("model_identity", record["model_identity"])
    _sha("model_sha256", record["model_sha256"])
    _text("artifact_identity", record["artifact_identity"])
    _sha("artifact_sha256", record["artifact_sha256"])
    _text("prediction_identity", record["prediction_identity"])
    _sha("prediction_sha256", record["prediction_sha256"])

    if record["storage_requirement_status"] != STORAGE_REQUIREMENT_STATUS:
        raise ExternalSignalPackageError("storage requirement must remain deferred")
    if record["publication_evidence_status"] != PUBLICATION_EVIDENCE_STATUS:
        raise ExternalSignalPackageError(
            "publication evidence must remain caller supplied"
        )
    for field in (
        "authenticated_storage_completed",
        "remote_publication_completed",
        "provider_publication_completed",
    ):
        if record[field] is not False:
            raise ExternalSignalPackageError(f"{field} must remain False")

    publication = _utc_text("publication_at_utc", record["publication_at_utc"])
    availability = _utc_text(
        "availability_at_utc", record["availability_at_utc"]
    )
    record_evaluation = _utc_text(
        "evaluation_at_utc", record["evaluation_at_utc"]
    )
    requested_evaluation = _utc_text(
        "evaluation_at_utc", evaluation_at_utc
    )
    if publication != record["publication_at_utc"]:
        raise ExternalSignalPackageError(
            "publication_at_utc must be canonical UTC"
        )
    if availability != record["availability_at_utc"]:
        raise ExternalSignalPackageError(
            "availability_at_utc must be canonical UTC"
        )
    if record_evaluation != record["evaluation_at_utc"]:
        raise ExternalSignalPackageError(
            "evaluation_at_utc must be canonical UTC"
        )
    if requested_evaluation != record_evaluation:
        raise ExternalSignalPackageError(
            "evaluation_at_utc does not match immutable package evidence"
        )

    alias_policy = _aliases(record["alias_policy"])
    if alias_policy != record["alias_policy"]:
        raise ExternalSignalPackageError(
            "alias_policy must use deterministic canonical ordering"
        )
    signals = record["signals"]
    if not isinstance(signals, list) or not signals:
        raise ExternalSignalPackageError("signals must be a non-empty list")

    checked: list[dict[str, Any]] = []
    for i, raw in enumerate(signals):
        signal = _mapping(f"signals[{i}]", raw)
        _keys(f"signals[{i}]", signal, _SIGNAL_KEYS)
        _text(f"signals[{i}].instrument_id", signal["instrument_id"])
        _text(
            f"signals[{i}].canonical_instrument_id",
            signal["canonical_instrument_id"],
        )
        if _text(f"signals[{i}].signal", signal["signal"]) not in (
            SUPPORTED_SIGNAL_VALUES
        ):
            raise ExternalSignalPackageError(
                f"unsupported signal value: {signal['signal']}"
            )
        for field in (
            "prediction_at_utc", "decision_at_utc", "valid_until_utc"
        ):
            canonical = _utc_text(
                f"signals[{i}].{field}", signal[field]
            )
            if canonical != signal[field]:
                raise ExternalSignalPackageError(
                    f"signals[{i}].{field} must be canonical UTC"
                )
        confidence = _confidence(
            f"signals[{i}].confidence", signal["confidence"]
        )
        if confidence != signal["confidence"]:
            raise ExternalSignalPackageError(
                f"signals[{i}].confidence must use canonical numeric form"
            )
        expected_signal_id = _identity(
            "external_signal",
            _signal_payload(
                signal,
                record["prediction_identity"],
                record["prediction_sha256"],
            ),
        )
        if signal["signal_id"] != expected_signal_id:
            raise ExternalSignalPackageError(
                f"signals[{i}].signal_id mismatch"
            )
        checked.append(signal)

    if checked != sorted(
        checked, key=lambda item: item["canonical_instrument_id"]
    ):
        raise ExternalSignalPackageError(
            "signals must use deterministic canonical instrument ordering"
        )
    _instrument_contract(checked, alias_policy)
    _temporal_contract(
        checked, publication, availability, record_evaluation
    )

    if record["run_id"] != _identity(
        "external_signal_run", _run_payload(record)
    ):
        raise ExternalSignalPackageError("run_id mismatch")
    if record["package_id"] != _identity(
        "external_signal_package", _package_payload(record)
    ):
        raise ExternalSignalPackageError("package_id mismatch")
    if not hmac.compare_digest(_digest(record), package_sha256):
        raise ExternalSignalPackageError("package SHA-256 mismatch")


def canonical_serialize_external_signal_package(
    package: dict[str, Any],
    *,
    evaluation_at_utc: str,
) -> str:
    """Return deterministic canonical JSON after full fail-closed validation."""
    validate_external_signal_package(
        package, evaluation_at_utc=evaluation_at_utc
    )
    return _json(package)
