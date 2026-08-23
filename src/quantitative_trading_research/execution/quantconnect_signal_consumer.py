"""Pure deterministic offline governed external-signal consumer.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``quantconnect/ExternalSignalConsumer.py``.

The historical source depended on QuantConnect/Lean runtime behavior,
network-delivered signal JSON, platform clocks, portfolio state, brokerage
configuration, holdings mutation, and order/fill events. None of that
operational behavior is carried forward here.

This C4 component consumes a complete validated TM-019 external-signal package
plus explicit caller-supplied temporal-reference evidence. It emits only
deterministic offline temporal-eligibility evidence. It performs no filesystem,
network, credential, provider, broker, account, order, execution, fill,
training, inference, dataset, final-holdout, paper-, or live-trading behavior.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import hmac
import json
import math
from typing import Any

from quantitative_trading_research.execution.quantconnect_signal_producer import (
    PACKAGE_TYPE as SOURCE_PACKAGE_TYPE,
    SCHEMA_ID as SOURCE_SCHEMA_ID,
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
    SUPPORTED_SIGNAL_VALUES,
    ExternalSignalPackageError,
    validate_external_signal_package,
)


SCHEMA_ID = "C4_OFFLINE_GOVERNED_EXTERNAL_SIGNAL_CONSUMPTION_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_external_signal_consumption_evidence"
EVIDENCE_SCOPE = "OFFLINE_TEMPORAL_ELIGIBILITY_REFERENCE_ONLY"
ELIGIBILITY_STATE = "OFFLINE_ELIGIBILITY_REFERENCE_VALID"
CHECKSUM_ALGORITHM = "sha256"

_RESULT_KEYS = {
    "record",
    "checksum_algorithm",
    "consumer_sha256",
}

_RECORD_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "evidence_scope",
    "consumer_run_id",
    "consumer_id",
    "source_schema_id",
    "source_schema_version",
    "source_package_type",
    "source_package_id",
    "source_package_sha256",
    "source_run_id",
    "source_prediction_identity",
    "source_prediction_sha256",
    "source_evaluation_at_utc",
    "source_availability_at_utc",
    "consumer_evaluation_at_utc",
    "signals",
}

_TEMPORAL_INPUT_KEYS = {
    "signal_id",
    "decision_bar_end_at_utc",
    "eligible_reference_at_utc",
}

_CONSUMED_SIGNAL_KEYS = {
    "signal_id",
    "instrument_id",
    "canonical_instrument_id",
    "signal",
    "confidence",
    "source_prediction_at_utc",
    "source_decision_at_utc",
    "source_valid_until_utc",
    "decision_bar_end_at_utc",
    "eligible_reference_at_utc",
    "eligibility_state",
}


class ExternalSignalConsumerError(ValueError):
    """Fail-closed error for malformed or inconsistent TM-020 evidence."""


def _mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExternalSignalConsumerError(f"{name} must be a dict")
    return deepcopy(value)


def _keys(name: str, value: dict[str, Any], expected: set[str]) -> None:
    if set(value) != expected:
        raise ExternalSignalConsumerError(
            f"{name} keys mismatch: "
            f"missing={sorted(expected - set(value))}; "
            f"unexpected={sorted(set(value) - expected)}"
        )


def _text(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ExternalSignalConsumerError(
            f"{name} must be a non-empty string without surrounding whitespace"
        )
    return value


def _hex(name: str, value: Any, length: int) -> str:
    text = _text(name, value)
    if len(text) != length or any(
        character not in "0123456789abcdef" for character in text
    ):
        raise ExternalSignalConsumerError(
            f"{name} must be lowercase {length}-character hex"
        )
    return text


def _sha(name: str, value: Any) -> str:
    return _hex(name, value, 64)


def _prefixed_digest(name: str, value: Any, prefix: str) -> str:
    text = _text(name, value)
    expected_prefix = f"{prefix}:"
    if not text.startswith(expected_prefix):
        raise ExternalSignalConsumerError(
            f"{name} must use {expected_prefix} identity prefix"
        )
    _hex(name, text[len(expected_prefix):], 64)
    return text


def _utc(name: str, value: Any) -> datetime:
    text = _text(name, value)
    candidate = text[:-1] + "+00:00" if text.endswith("Z") else text

    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ExternalSignalConsumerError(
            f"{name} must be an ISO-8601 UTC timestamp"
        ) from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExternalSignalConsumerError(
            f"{name} must be timezone-aware UTC"
        )

    if parsed.utcoffset().total_seconds() != 0:
        raise ExternalSignalConsumerError(
            f"{name} must be expressed in UTC"
        )

    return parsed.astimezone(timezone.utc)


def _utc_text(name: str, value: Any) -> str:
    return _utc(name, value).isoformat()


def _confidence(name: str, value: Any) -> float | None:
    if value is None:
        return None

    if type(value) is not float:
        raise ExternalSignalConsumerError(
            f"{name} must be null or a canonical float in [0, 1]"
        )

    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ExternalSignalConsumerError(
            f"{name} must be null or a finite canonical float in [0, 1]"
        )

    return value


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
        raise ExternalSignalConsumerError(
            "consumer evidence is not canonically serializable"
        ) from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _identity(prefix: str, value: Any) -> str:
    return f"{prefix}:{_digest(value)}"


def _source_signal_identity(
    *,
    prediction_identity: str,
    prediction_sha256: str,
    instrument_id: str,
    canonical_instrument_id: str,
    signal: str,
    confidence: float | None,
    prediction_at_utc: str,
    decision_at_utc: str,
    valid_until_utc: str,
) -> str:
    """Reconstruct the public TM-019 source-signal identity correspondence."""

    return _identity(
        "external_signal",
        {
            "prediction_identity": prediction_identity,
            "prediction_sha256": prediction_sha256,
            "signal": {
                "instrument_id": instrument_id,
                "canonical_instrument_id": canonical_instrument_id,
                "signal": signal,
                "prediction_at_utc": prediction_at_utc,
                "decision_at_utc": decision_at_utc,
                "valid_until_utc": valid_until_utc,
                "confidence": confidence,
            },
        },
    )


def _source_evaluation_at(package: Any) -> str:
    if not isinstance(package, dict):
        raise ExternalSignalConsumerError(
            "source package must be a dict"
        )

    record = package.get("record")
    if not isinstance(record, dict):
        raise ExternalSignalConsumerError(
            "source package.record must be a dict"
        )

    if "evaluation_at_utc" not in record:
        raise ExternalSignalConsumerError(
            "source package is missing evaluation_at_utc"
        )

    return _text(
        "source package.record.evaluation_at_utc",
        record["evaluation_at_utc"],
    )


def _validated_source_package(package: Any) -> dict[str, Any]:
    source = _mapping("source package", package)
    source_evaluation = _source_evaluation_at(source)

    try:
        validate_external_signal_package(
            source,
            evaluation_at_utc=source_evaluation,
        )
    except ExternalSignalPackageError as exc:
        raise ExternalSignalConsumerError(
            f"source TM-019 package is invalid: {exc}"
        ) from exc

    return source


def _temporal_entries(value: Any) -> dict[str, dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ExternalSignalConsumerError(
            "consumer temporal evidence must be a non-empty list"
        )

    by_signal: dict[str, dict[str, str]] = {}

    for index, raw in enumerate(deepcopy(value)):
        item = _mapping(f"temporal_evidence[{index}]", raw)
        _keys(
            f"temporal_evidence[{index}]",
            item,
            _TEMPORAL_INPUT_KEYS,
        )

        signal_id = _text(
            f"temporal_evidence[{index}].signal_id",
            item["signal_id"],
        )

        if signal_id in by_signal:
            raise ExternalSignalConsumerError(
                f"duplicate temporal evidence for signal_id: {signal_id}"
            )

        by_signal[signal_id] = {
            "signal_id": signal_id,
            "decision_bar_end_at_utc": _utc_text(
                f"temporal_evidence[{index}].decision_bar_end_at_utc",
                item["decision_bar_end_at_utc"],
            ),
            "eligible_reference_at_utc": _utc_text(
                f"temporal_evidence[{index}].eligible_reference_at_utc",
                item["eligible_reference_at_utc"],
            ),
        }

    return by_signal


def _consumer_signal(
    *,
    source_signal: dict[str, Any],
    source_prediction_identity: str,
    source_prediction_sha256: str,
    temporal: dict[str, str],
    consumer_evaluation: datetime,
) -> dict[str, Any]:
    signal_id = _prefixed_digest(
        "source signal_id",
        source_signal["signal_id"],
        "external_signal",
    )

    prediction_at = _utc(
        "source signal.prediction_at_utc",
        source_signal["prediction_at_utc"],
    )
    decision_at = _utc(
        "source signal.decision_at_utc",
        source_signal["decision_at_utc"],
    )
    valid_until = _utc(
        "source signal.valid_until_utc",
        source_signal["valid_until_utc"],
    )
    decision_bar_end = _utc(
        "decision_bar_end_at_utc",
        temporal["decision_bar_end_at_utc"],
    )
    eligible_reference = _utc(
        "eligible_reference_at_utc",
        temporal["eligible_reference_at_utc"],
    )

    if decision_at > decision_bar_end:
        raise ExternalSignalConsumerError(
            f"decision_at_utc follows decision_bar_end_at_utc for {signal_id}"
        )

    if eligible_reference < decision_bar_end:
        raise ExternalSignalConsumerError(
            f"same-bar reference prohibited for {signal_id}"
        )

    if eligible_reference > consumer_evaluation:
        raise ExternalSignalConsumerError(
            f"eligible reference is future relative to consumer evaluation "
            f"for {signal_id}"
        )

    if consumer_evaluation > valid_until:
        raise ExternalSignalConsumerError(
            f"source signal is stale at consumer evaluation for {signal_id}"
        )

    instrument_id = _text(
        "source signal.instrument_id",
        source_signal["instrument_id"],
    )
    canonical_instrument_id = _text(
        "source signal.canonical_instrument_id",
        source_signal["canonical_instrument_id"],
    )
    signal_value = _text(
        "source signal.signal",
        source_signal["signal"],
    )
    if signal_value not in SUPPORTED_SIGNAL_VALUES:
        raise ExternalSignalConsumerError(
            f"unsupported source signal value: {signal_value}"
        )

    confidence = _confidence(
        "source signal.confidence",
        source_signal["confidence"],
    )

    expected_signal_id = _source_signal_identity(
        prediction_identity=source_prediction_identity,
        prediction_sha256=source_prediction_sha256,
        instrument_id=instrument_id,
        canonical_instrument_id=canonical_instrument_id,
        signal=signal_value,
        confidence=confidence,
        prediction_at_utc=prediction_at.isoformat(),
        decision_at_utc=decision_at.isoformat(),
        valid_until_utc=valid_until.isoformat(),
    )
    if signal_id != expected_signal_id:
        raise ExternalSignalConsumerError(
            f"source signal identity/prediction correspondence mismatch: "
            f"{signal_id}"
        )

    return {
        "signal_id": signal_id,
        "instrument_id": instrument_id,
        "canonical_instrument_id": canonical_instrument_id,
        "signal": signal_value,
        "confidence": confidence,
        "source_prediction_at_utc": prediction_at.isoformat(),
        "source_decision_at_utc": decision_at.isoformat(),
        "source_valid_until_utc": valid_until.isoformat(),
        "decision_bar_end_at_utc": decision_bar_end.isoformat(),
        "eligible_reference_at_utc": eligible_reference.isoformat(),
        "eligibility_state": ELIGIBILITY_STATE,
    }


def _run_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        key: record[key]
        for key in (
            "source_schema_id",
            "source_schema_version",
            "source_package_type",
            "source_package_id",
            "source_package_sha256",
            "source_run_id",
            "source_prediction_identity",
            "source_prediction_sha256",
            "source_evaluation_at_utc",
            "source_availability_at_utc",
            "consumer_evaluation_at_utc",
            "signals",
        )
    }


def _consumer_identity_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": record["schema_id"],
        "schema_version": record["schema_version"],
        "result_type": record["result_type"],
        "evidence_scope": record["evidence_scope"],
        "consumer_run_id": record["consumer_run_id"],
    }


def build_external_signal_consumption_evidence(
    *,
    package: dict[str, Any],
    consumer_evaluation_at_utc: str,
    temporal_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    """Consume one TM-019 package into deterministic offline eligibility evidence."""

    source = _validated_source_package(package)
    source_record = source["record"]

    consumer_evaluation_text = _utc_text(
        "consumer_evaluation_at_utc",
        consumer_evaluation_at_utc,
    )
    consumer_evaluation = _utc(
        "consumer_evaluation_at_utc",
        consumer_evaluation_text,
    )

    source_evaluation_text = _utc_text(
        "source package.evaluation_at_utc",
        source_record["evaluation_at_utc"],
    )
    source_evaluation = _utc(
        "source package.evaluation_at_utc",
        source_evaluation_text,
    )

    source_availability_text = _utc_text(
        "source package.availability_at_utc",
        source_record["availability_at_utc"],
    )
    source_availability = _utc(
        "source package.availability_at_utc",
        source_availability_text,
    )

    if consumer_evaluation < source_evaluation:
        raise ExternalSignalConsumerError(
            "consumer evaluation precedes source package evaluation"
        )

    if consumer_evaluation < source_availability:
        raise ExternalSignalConsumerError(
            "consumer evaluation precedes source package availability"
        )

    temporal_by_signal = _temporal_entries(temporal_evidence)

    source_signals = source_record["signals"]
    source_signal_ids = [signal["signal_id"] for signal in source_signals]

    if len(source_signal_ids) != len(set(source_signal_ids)):
        raise ExternalSignalConsumerError(
            "source package contains duplicate signal identities"
        )

    if set(temporal_by_signal) != set(source_signal_ids):
        missing = sorted(set(source_signal_ids) - set(temporal_by_signal))
        extra = sorted(set(temporal_by_signal) - set(source_signal_ids))
        raise ExternalSignalConsumerError(
            "consumer temporal signal_id correspondence mismatch: "
            f"missing={missing}; extra={extra}"
        )

    source_prediction_identity = _text(
        "source prediction_identity",
        source_record["prediction_identity"],
    )
    source_prediction_sha256 = _sha(
        "source prediction_sha256",
        source_record["prediction_sha256"],
    )

    consumed_signals = [
        _consumer_signal(
            source_signal=deepcopy(source_signal),
            source_prediction_identity=source_prediction_identity,
            source_prediction_sha256=source_prediction_sha256,
            temporal=temporal_by_signal[source_signal["signal_id"]],
            consumer_evaluation=consumer_evaluation,
        )
        for source_signal in source_signals
    ]
    consumed_signals.sort(
        key=lambda item: item["canonical_instrument_id"]
    )

    record: dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "evidence_scope": EVIDENCE_SCOPE,
        "consumer_run_id": "",
        "consumer_id": "",
        "source_schema_id": source_record["schema_id"],
        "source_schema_version": source_record["schema_version"],
        "source_package_type": source_record["package_type"],
        "source_package_id": source_record["package_id"],
        "source_package_sha256": source["package_sha256"],
        "source_run_id": source_record["run_id"],
        "source_prediction_identity": source_prediction_identity,
        "source_prediction_sha256": source_prediction_sha256,
        "source_evaluation_at_utc": source_evaluation_text,
        "source_availability_at_utc": source_availability_text,
        "consumer_evaluation_at_utc": consumer_evaluation_text,
        "signals": consumed_signals,
    }

    record["consumer_run_id"] = _identity(
        "external_signal_consumer_run",
        _run_payload(record),
    )
    record["consumer_id"] = _identity(
        "external_signal_consumer",
        _consumer_identity_payload(record),
    )

    result = {
        "record": record,
        "checksum_algorithm": CHECKSUM_ALGORITHM,
        "consumer_sha256": _digest(record),
    }

    validate_external_signal_consumption_evidence(result)
    return result


def validate_external_signal_consumption_evidence(
    evidence: Any,
) -> None:
    """Fail closed on malformed or tampered deterministic TM-020 evidence."""

    value = _mapping("consumer evidence", evidence)
    _keys("consumer evidence", value, _RESULT_KEYS)

    if value["checksum_algorithm"] != CHECKSUM_ALGORITHM:
        raise ExternalSignalConsumerError(
            "unsupported consumer checksum algorithm"
        )

    consumer_sha256 = _sha(
        "consumer_sha256",
        value["consumer_sha256"],
    )

    record = _mapping("consumer evidence.record", value["record"])
    _keys("consumer evidence.record", record, _RECORD_KEYS)

    if record["schema_id"] != SCHEMA_ID:
        raise ExternalSignalConsumerError(
            "unsupported consumer schema_id"
        )

    if type(record["schema_version"]) is not int:
        raise ExternalSignalConsumerError(
            "consumer schema_version must be an int"
        )

    if record["schema_version"] != SCHEMA_VERSION:
        raise ExternalSignalConsumerError(
            "unsupported consumer schema_version"
        )

    if record["result_type"] != RESULT_TYPE:
        raise ExternalSignalConsumerError(
            "unsupported consumer result_type"
        )

    if record["evidence_scope"] != EVIDENCE_SCOPE:
        raise ExternalSignalConsumerError(
            "unsupported consumer evidence_scope"
        )

    _prefixed_digest(
        "consumer_run_id",
        record["consumer_run_id"],
        "external_signal_consumer_run",
    )
    _prefixed_digest(
        "consumer_id",
        record["consumer_id"],
        "external_signal_consumer",
    )

    if record["source_schema_id"] != SOURCE_SCHEMA_ID:
        raise ExternalSignalConsumerError(
            "unsupported source TM-019 schema_id"
        )

    if type(record["source_schema_version"]) is not int:
        raise ExternalSignalConsumerError(
            "source schema_version must be an int"
        )

    if record["source_schema_version"] != SOURCE_SCHEMA_VERSION:
        raise ExternalSignalConsumerError(
            "unsupported source TM-019 schema_version"
        )

    if record["source_package_type"] != SOURCE_PACKAGE_TYPE:
        raise ExternalSignalConsumerError(
            "unsupported source TM-019 package_type"
        )

    _prefixed_digest(
        "source_package_id",
        record["source_package_id"],
        "external_signal_package",
    )
    _sha(
        "source_package_sha256",
        record["source_package_sha256"],
    )
    _prefixed_digest(
        "source_run_id",
        record["source_run_id"],
        "external_signal_run",
    )
    _text(
        "source_prediction_identity",
        record["source_prediction_identity"],
    )
    _sha(
        "source_prediction_sha256",
        record["source_prediction_sha256"],
    )

    source_evaluation_text = _utc_text(
        "source_evaluation_at_utc",
        record["source_evaluation_at_utc"],
    )
    source_availability_text = _utc_text(
        "source_availability_at_utc",
        record["source_availability_at_utc"],
    )
    consumer_evaluation_text = _utc_text(
        "consumer_evaluation_at_utc",
        record["consumer_evaluation_at_utc"],
    )

    if source_evaluation_text != record["source_evaluation_at_utc"]:
        raise ExternalSignalConsumerError(
            "source_evaluation_at_utc must be canonical UTC"
        )

    if source_availability_text != record["source_availability_at_utc"]:
        raise ExternalSignalConsumerError(
            "source_availability_at_utc must be canonical UTC"
        )

    if consumer_evaluation_text != record["consumer_evaluation_at_utc"]:
        raise ExternalSignalConsumerError(
            "consumer_evaluation_at_utc must be canonical UTC"
        )

    source_evaluation = _utc(
        "source_evaluation_at_utc",
        source_evaluation_text,
    )
    source_availability = _utc(
        "source_availability_at_utc",
        source_availability_text,
    )
    consumer_evaluation = _utc(
        "consumer_evaluation_at_utc",
        consumer_evaluation_text,
    )

    if source_availability > source_evaluation:
        raise ExternalSignalConsumerError(
            "source availability follows source evaluation"
        )

    if source_evaluation > consumer_evaluation:
        raise ExternalSignalConsumerError(
            "consumer evaluation precedes source evaluation"
        )

    if source_availability > consumer_evaluation:
        raise ExternalSignalConsumerError(
            "consumer evaluation precedes source availability"
        )

    signals = record["signals"]
    if not isinstance(signals, list) or not signals:
        raise ExternalSignalConsumerError(
            "consumer signals must be a non-empty list"
        )

    checked_signals: list[dict[str, Any]] = []
    seen_signal_ids: set[str] = set()
    seen_canonical_instruments: set[str] = set()

    for index, raw in enumerate(signals):
        signal = _mapping(f"signals[{index}]", raw)
        _keys(
            f"signals[{index}]",
            signal,
            _CONSUMED_SIGNAL_KEYS,
        )

        signal_id = _prefixed_digest(
            f"signals[{index}].signal_id",
            signal["signal_id"],
            "external_signal",
        )
        if signal_id in seen_signal_ids:
            raise ExternalSignalConsumerError(
                f"duplicate source signal identity: {signal_id}"
            )
        seen_signal_ids.add(signal_id)

        instrument_id = _text(
            f"signals[{index}].instrument_id",
            signal["instrument_id"],
        )
        canonical_instrument_id = _text(
            f"signals[{index}].canonical_instrument_id",
            signal["canonical_instrument_id"],
        )
        if canonical_instrument_id in seen_canonical_instruments:
            raise ExternalSignalConsumerError(
                "duplicate canonical instrument in consumer evidence"
            )
        seen_canonical_instruments.add(canonical_instrument_id)

        signal_value = _text(
            f"signals[{index}].signal",
            signal["signal"],
        )
        if signal_value not in SUPPORTED_SIGNAL_VALUES:
            raise ExternalSignalConsumerError(
                f"unsupported signal value: {signal_value}"
            )

        confidence = _confidence(
            f"signals[{index}].confidence",
            signal["confidence"],
        )
        if confidence != signal["confidence"]:
            raise ExternalSignalConsumerError(
                f"signals[{index}].confidence is not canonical"
            )

        prediction_text = _utc_text(
            f"signals[{index}].source_prediction_at_utc",
            signal["source_prediction_at_utc"],
        )
        decision_text = _utc_text(
            f"signals[{index}].source_decision_at_utc",
            signal["source_decision_at_utc"],
        )
        valid_until_text = _utc_text(
            f"signals[{index}].source_valid_until_utc",
            signal["source_valid_until_utc"],
        )
        decision_bar_end_text = _utc_text(
            f"signals[{index}].decision_bar_end_at_utc",
            signal["decision_bar_end_at_utc"],
        )
        eligible_reference_text = _utc_text(
            f"signals[{index}].eligible_reference_at_utc",
            signal["eligible_reference_at_utc"],
        )

        for field, canonical in (
            ("source_prediction_at_utc", prediction_text),
            ("source_decision_at_utc", decision_text),
            ("source_valid_until_utc", valid_until_text),
            ("decision_bar_end_at_utc", decision_bar_end_text),
            ("eligible_reference_at_utc", eligible_reference_text),
        ):
            if signal[field] != canonical:
                raise ExternalSignalConsumerError(
                    f"signals[{index}].{field} must be canonical UTC"
                )

        prediction = _utc(
            f"signals[{index}].source_prediction_at_utc",
            prediction_text,
        )
        decision = _utc(
            f"signals[{index}].source_decision_at_utc",
            decision_text,
        )
        valid_until = _utc(
            f"signals[{index}].source_valid_until_utc",
            valid_until_text,
        )
        decision_bar_end = _utc(
            f"signals[{index}].decision_bar_end_at_utc",
            decision_bar_end_text,
        )
        eligible_reference = _utc(
            f"signals[{index}].eligible_reference_at_utc",
            eligible_reference_text,
        )

        expected_signal_id = _source_signal_identity(
            prediction_identity=record["source_prediction_identity"],
            prediction_sha256=record["source_prediction_sha256"],
            instrument_id=instrument_id,
            canonical_instrument_id=canonical_instrument_id,
            signal=signal_value,
            confidence=confidence,
            prediction_at_utc=prediction_text,
            decision_at_utc=decision_text,
            valid_until_utc=valid_until_text,
        )
        if signal_id != expected_signal_id:
            raise ExternalSignalConsumerError(
                "source signal identity does not correspond to preserved "
                "prediction evidence"
            )

        if prediction > decision:
            raise ExternalSignalConsumerError(
                "source prediction follows source decision"
            )

        if decision > decision_bar_end:
            raise ExternalSignalConsumerError(
                "source decision follows decision-bar exclusive end"
            )

        if eligible_reference < decision_bar_end:
            raise ExternalSignalConsumerError(
                "same-bar reference is prohibited"
            )

        if eligible_reference > consumer_evaluation:
            raise ExternalSignalConsumerError(
                "eligible reference is future relative to consumer evaluation"
            )

        if consumer_evaluation > valid_until:
            raise ExternalSignalConsumerError(
                "source signal is stale at consumer evaluation"
            )

        if signal["eligibility_state"] != ELIGIBILITY_STATE:
            raise ExternalSignalConsumerError(
                "unsupported eligibility_state"
            )

        checked_signals.append(
            {
                "signal_id": signal_id,
                "instrument_id": instrument_id,
                "canonical_instrument_id": canonical_instrument_id,
                "signal": signal_value,
                "confidence": confidence,
                "source_prediction_at_utc": prediction_text,
                "source_decision_at_utc": decision_text,
                "source_valid_until_utc": valid_until_text,
                "decision_bar_end_at_utc": decision_bar_end_text,
                "eligible_reference_at_utc": eligible_reference_text,
                "eligibility_state": ELIGIBILITY_STATE,
            }
        )

    canonical_order = sorted(
        checked_signals,
        key=lambda item: item["canonical_instrument_id"],
    )
    if checked_signals != canonical_order:
        raise ExternalSignalConsumerError(
            "consumer signals must use canonical instrument ordering"
        )

    if record["consumer_run_id"] != _identity(
        "external_signal_consumer_run",
        _run_payload(record),
    ):
        raise ExternalSignalConsumerError(
            "consumer_run_id mismatch"
        )

    if record["consumer_id"] != _identity(
        "external_signal_consumer",
        _consumer_identity_payload(record),
    ):
        raise ExternalSignalConsumerError(
            "consumer_id mismatch"
        )

    if not hmac.compare_digest(
        _digest(record),
        consumer_sha256,
    ):
        raise ExternalSignalConsumerError(
            "consumer SHA-256 mismatch"
        )


def canonical_serialize_external_signal_consumption_evidence(
    evidence: dict[str, Any],
) -> str:
    """Return canonical deterministic JSON after strict TM-020 validation."""

    validate_external_signal_consumption_evidence(evidence)
    return _canonical_json(evidence)
