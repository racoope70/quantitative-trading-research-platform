"""Pure deterministic offline TM-019/TM-020 contract-parity harness.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/model_selection/quantconnect_execution_retest.py``.

The historical retest mixed filesystem inputs and outputs, paper-execution
simulation, permissive coercion, CLI orchestration, and legacy QuantConnect
payload assumptions. None of that operational behavior is carried forward.

This C4 component accepts an already-complete TM-019 external-signal package
and an already-complete TM-020 consumption-evidence object. It reuses both
public validators and proves only their exact cross-contract correspondence.
A returned PASS means only that the offline TM-019 and TM-020 contracts are
coherent for the supplied controlled evidence.

No filesystem, network, credential, provider, QuantConnect/LEAN runtime,
broker, account, order, execution, fill, replay, training, inference,
data-acquisition, dataset, final-holdout, paper-, or live-trading behavior is
performed.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import hmac
import json
from typing import Any

from quantitative_trading_research.execution.quantconnect_signal_consumer import (
    ExternalSignalConsumerError,
    validate_external_signal_consumption_evidence,
)
from quantitative_trading_research.execution.quantconnect_signal_producer import (
    ExternalSignalPackageError,
    validate_external_signal_package,
)


SCHEMA_ID = "C4_OFFLINE_EXTERNAL_SIGNAL_PARITY_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_external_signal_producer_consumer_parity"
PARITY_STATE = "PASS"
CHECKSUM_ALGORITHM = "sha256"

_RESULT_KEYS = {
    "record",
    "checksum_algorithm",
    "parity_sha256",
}

_RECORD_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "parity_state",
    "parity_id",
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
    "consumer_schema_id",
    "consumer_schema_version",
    "consumer_id",
    "consumer_run_id",
    "consumer_sha256",
    "consumer_evaluation_at_utc",
    "signal_ids",
    "parity_assertions",
}

_PARITY_ASSERTIONS = {
    "package_crosslink": "PASS",
    "run_identity": "PASS",
    "prediction_identity": "PASS",
    "signal_correspondence": "PASS",
    "instrument_identity": "PASS",
    "signal_label": "PASS",
    "confidence": "PASS",
    "source_temporal_evidence": "PASS",
    "consumer_temporal_binding": "PASS",
}

_SOURCE_TO_CONSUMER_RECORD_FIELDS = (
    ("source_schema_id", "schema_id"),
    ("source_schema_version", "schema_version"),
    ("source_package_type", "package_type"),
    ("source_package_id", "package_id"),
    ("source_run_id", "run_id"),
    ("source_prediction_identity", "prediction_identity"),
    ("source_prediction_sha256", "prediction_sha256"),
    ("source_evaluation_at_utc", "evaluation_at_utc"),
    ("source_availability_at_utc", "availability_at_utc"),
)

_SIGNAL_FIELD_PARITY = (
    ("instrument_id", "instrument_id"),
    ("canonical_instrument_id", "canonical_instrument_id"),
    ("signal", "signal"),
    ("confidence", "confidence"),
    ("source_prediction_at_utc", "prediction_at_utc"),
    ("source_decision_at_utc", "decision_at_utc"),
    ("source_valid_until_utc", "valid_until_utc"),
)


class ExternalSignalParityError(ValueError):
    """Fail-closed error for invalid or mismatched TM-021 parity evidence."""


def _fail(code: str, detail: str = "") -> None:
    message = code if not detail else f"{code}: {detail}"
    raise ExternalSignalParityError(message)


def _mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("WRONG_TYPE", f"{name} must be a dict")
    return deepcopy(value)


def _keys(name: str, value: dict[str, Any], expected: set[str]) -> None:
    if set(value) != expected:
        _fail(
            "UNEXPECTED_FIELD",
            f"{name} keys mismatch: "
            f"missing={sorted(expected - set(value))}; "
            f"unexpected={sorted(set(value) - expected)}",
        )


def _text(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        _fail(
            "WRONG_TYPE",
            f"{name} must be a non-empty string without surrounding whitespace",
        )
    return value


def _integer(name: str, value: Any) -> int:
    if type(value) is not int:
        _fail("WRONG_TYPE", f"{name} must be an int")
    return value


def _sha(name: str, value: Any) -> str:
    text = _text(name, value)
    if len(text) != 64 or any(
        character not in "0123456789abcdef" for character in text
    ):
        _fail(
            "WRONG_TYPE",
            f"{name} must be lowercase 64-character SHA-256 hex",
        )
    return text


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
        raise ExternalSignalParityError(
            "NONCANONICAL_EVIDENCE: parity evidence is not canonically serializable"
        ) from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _identity(prefix: str, value: Any) -> str:
    return f"{prefix}:{_digest(value)}"


def _source_evaluation_at(package: dict[str, Any]) -> str:
    record = package.get("record")
    if not isinstance(record, dict):
        _fail(
            "INVALID_PRODUCER_PACKAGE",
            "package.record must be a dict before public validation",
        )

    evaluation = record.get("evaluation_at_utc")
    if not isinstance(evaluation, str) or not evaluation:
        _fail(
            "INVALID_PRODUCER_PACKAGE",
            "package.record.evaluation_at_utc is required for public validation",
        )

    return evaluation


def _validated_inputs(
    package: Any,
    consumer_evidence: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    source = _mapping("package", package)
    consumer = _mapping("consumer_evidence", consumer_evidence)

    evaluation_at_utc = _source_evaluation_at(source)

    try:
        validate_external_signal_package(
            source,
            evaluation_at_utc=evaluation_at_utc,
        )
    except ExternalSignalPackageError as exc:
        raise ExternalSignalParityError(
            f"INVALID_PRODUCER_PACKAGE: {exc}"
        ) from exc

    try:
        validate_external_signal_consumption_evidence(consumer)
    except ExternalSignalConsumerError as exc:
        raise ExternalSignalParityError(
            f"INVALID_CONSUMER_EVIDENCE: {exc}"
        ) from exc

    return source, consumer


def _expect_equal(
    code: str,
    name: str,
    actual: Any,
    expected: Any,
) -> None:
    if actual != expected or type(actual) is not type(expected):
        _fail(
            code,
            f"{name} mismatch: actual={actual!r}; expected={expected!r}",
        )


def _signal_correspondence(
    source_record: dict[str, Any],
    consumer_record: dict[str, Any],
) -> list[str]:
    source_signals = source_record["signals"]
    consumer_signals = consumer_record["signals"]

    source_ids = [signal["signal_id"] for signal in source_signals]
    consumer_ids = [signal["signal_id"] for signal in consumer_signals]

    if len(source_ids) != len(set(source_ids)):
        _fail(
            "DUPLICATE_SIGNAL_CORRESPONDENCE",
            "validated producer signals contain duplicate signal_id values",
        )

    if len(consumer_ids) != len(set(consumer_ids)):
        _fail(
            "DUPLICATE_SIGNAL_CORRESPONDENCE",
            "validated consumer signals contain duplicate signal_id values",
        )

    source_id_set = set(source_ids)
    consumer_id_set = set(consumer_ids)

    missing = sorted(source_id_set - consumer_id_set)
    extra = sorted(consumer_id_set - source_id_set)

    if missing:
        _fail(
            "MISSING_SIGNAL",
            f"consumer evidence is missing signal_id values: {missing}",
        )

    if extra:
        _fail(
            "EXTRA_SIGNAL",
            f"consumer evidence contains unknown signal_id values: {extra}",
        )

    if len(source_ids) != len(consumer_ids):
        _fail(
            "SIGNAL_COUNT_MISMATCH",
            "producer and consumer signal counts differ",
        )

    source_by_id = {
        signal["signal_id"]: signal for signal in source_signals
    }
    consumer_by_id = {
        signal["signal_id"]: signal for signal in consumer_signals
    }

    for signal_id in sorted(source_id_set):
        source_signal = source_by_id[signal_id]
        consumer_signal = consumer_by_id[signal_id]

        for consumer_field, source_field in _SIGNAL_FIELD_PARITY:
            if consumer_field == "canonical_instrument_id":
                code = "CANONICAL_INSTRUMENT_ID_MISMATCH"
            elif consumer_field == "instrument_id":
                code = "INSTRUMENT_ID_MISMATCH"
            elif consumer_field == "signal":
                code = "SIGNAL_LABEL_MISMATCH"
            elif consumer_field == "confidence":
                code = "CONFIDENCE_MISMATCH"
            else:
                code = "SOURCE_TEMPORAL_MISMATCH"

            _expect_equal(
                code,
                f"{signal_id}.{consumer_field}",
                consumer_signal[consumer_field],
                source_signal[source_field],
            )

    return sorted(source_id_set)


def _assert_cross_contract_parity(
    source: dict[str, Any],
    consumer: dict[str, Any],
) -> list[str]:
    source_record = source["record"]
    consumer_record = consumer["record"]

    for consumer_field, source_field in _SOURCE_TO_CONSUMER_RECORD_FIELDS:
        if consumer_field == "source_package_id":
            code = "PACKAGE_ID_MISMATCH"
        elif consumer_field == "source_run_id":
            code = "RUN_ID_MISMATCH"
        elif consumer_field == "source_prediction_identity":
            code = "PREDICTION_IDENTITY_MISMATCH"
        elif consumer_field == "source_prediction_sha256":
            code = "PREDICTION_CHECKSUM_MISMATCH"
        elif consumer_field in (
            "source_evaluation_at_utc",
            "source_availability_at_utc",
        ):
            code = "SOURCE_TEMPORAL_MISMATCH"
        elif consumer_field == "source_schema_id":
            code = "PRODUCER_SCHEMA_MISMATCH"
        elif consumer_field == "source_schema_version":
            code = "PRODUCER_VERSION_MISMATCH"
        else:
            code = "PACKAGE_ID_MISMATCH"

        _expect_equal(
            code,
            consumer_field,
            consumer_record[consumer_field],
            source_record[source_field],
        )

    _expect_equal(
        "PACKAGE_CHECKSUM_MISMATCH",
        "source_package_sha256",
        consumer_record["source_package_sha256"],
        source["package_sha256"],
    )

    return _signal_correspondence(
        source_record,
        consumer_record,
    )


def _parity_identity_payload(
    record: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: record[key]
        for key in sorted(record)
        if key != "parity_id"
    }


def _build_parity_record(
    source: dict[str, Any],
    consumer: dict[str, Any],
) -> dict[str, Any]:
    signal_ids = _assert_cross_contract_parity(source, consumer)

    source_record = source["record"]
    consumer_record = consumer["record"]

    record: dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "parity_state": PARITY_STATE,
        "parity_id": "",
        "source_schema_id": source_record["schema_id"],
        "source_schema_version": source_record["schema_version"],
        "source_package_type": source_record["package_type"],
        "source_package_id": source_record["package_id"],
        "source_package_sha256": source["package_sha256"],
        "source_run_id": source_record["run_id"],
        "source_prediction_identity": source_record["prediction_identity"],
        "source_prediction_sha256": source_record["prediction_sha256"],
        "source_evaluation_at_utc": source_record["evaluation_at_utc"],
        "source_availability_at_utc": source_record["availability_at_utc"],
        "consumer_schema_id": consumer_record["schema_id"],
        "consumer_schema_version": consumer_record["schema_version"],
        "consumer_id": consumer_record["consumer_id"],
        "consumer_run_id": consumer_record["consumer_run_id"],
        "consumer_sha256": consumer["consumer_sha256"],
        "consumer_evaluation_at_utc": consumer_record[
            "consumer_evaluation_at_utc"
        ],
        "signal_ids": signal_ids,
        "parity_assertions": deepcopy(_PARITY_ASSERTIONS),
    }

    record["parity_id"] = _identity(
        "external_signal_parity",
        _parity_identity_payload(record),
    )

    return record


def build_external_signal_parity_evidence(
    *,
    package: dict[str, Any],
    consumer_evidence: dict[str, Any],
) -> dict[str, Any]:
    """Build deterministic PASS evidence for exact TM-019/TM-020 parity."""

    source, consumer = _validated_inputs(
        package,
        consumer_evidence,
    )

    record = _build_parity_record(source, consumer)

    result = {
        "record": record,
        "checksum_algorithm": CHECKSUM_ALGORITHM,
        "parity_sha256": _digest(record),
    }

    validate_external_signal_parity_evidence(
        result,
        package=source,
        consumer_evidence=consumer,
    )
    return result


def validate_external_signal_parity_evidence(
    evidence: Any,
    *,
    package: dict[str, Any],
    consumer_evidence: dict[str, Any],
) -> None:
    """Fail closed unless evidence proves the supplied exact contract pair.

    The original TM-019 package and TM-020 consumer evidence are explicit
    validation inputs because the compact parity record intentionally carries
    content addresses rather than duplicating both complete upstream records.
    """

    source, consumer = _validated_inputs(
        package,
        consumer_evidence,
    )

    value = _mapping("parity evidence", evidence)
    _keys("parity evidence", value, _RESULT_KEYS)

    if value["checksum_algorithm"] != CHECKSUM_ALGORITHM:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "unsupported checksum_algorithm",
        )

    parity_sha256 = _sha(
        "parity_sha256",
        value["parity_sha256"],
    )

    record = _mapping(
        "parity evidence.record",
        value["record"],
    )
    _keys("parity evidence.record", record, _RECORD_KEYS)

    if record["schema_id"] != SCHEMA_ID:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "unsupported schema_id",
        )

    if _integer(
        "record.schema_version",
        record["schema_version"],
    ) != SCHEMA_VERSION:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "unsupported schema_version",
        )

    if record["result_type"] != RESULT_TYPE:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "unsupported result_type",
        )

    if record["parity_state"] != PARITY_STATE:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "parity_state must be PASS",
        )

    parity_id = _text(
        "record.parity_id",
        record["parity_id"],
    )
    expected_prefix = "external_signal_parity:"
    if not parity_id.startswith(expected_prefix):
        _fail(
            "PARITY_IDENTITY_MISMATCH",
            "parity_id uses an unsupported identity prefix",
        )
    _sha(
        "record.parity_id digest",
        parity_id[len(expected_prefix):],
    )

    _text(
        "record.source_schema_id",
        record["source_schema_id"],
    )
    _integer(
        "record.source_schema_version",
        record["source_schema_version"],
    )
    _text(
        "record.source_package_type",
        record["source_package_type"],
    )
    _text(
        "record.source_package_id",
        record["source_package_id"],
    )
    _sha(
        "record.source_package_sha256",
        record["source_package_sha256"],
    )
    _text(
        "record.source_run_id",
        record["source_run_id"],
    )
    _text(
        "record.source_prediction_identity",
        record["source_prediction_identity"],
    )
    _sha(
        "record.source_prediction_sha256",
        record["source_prediction_sha256"],
    )
    _text(
        "record.source_evaluation_at_utc",
        record["source_evaluation_at_utc"],
    )
    _text(
        "record.source_availability_at_utc",
        record["source_availability_at_utc"],
    )
    _text(
        "record.consumer_schema_id",
        record["consumer_schema_id"],
    )
    _integer(
        "record.consumer_schema_version",
        record["consumer_schema_version"],
    )
    _text(
        "record.consumer_id",
        record["consumer_id"],
    )
    _text(
        "record.consumer_run_id",
        record["consumer_run_id"],
    )
    _sha(
        "record.consumer_sha256",
        record["consumer_sha256"],
    )
    _text(
        "record.consumer_evaluation_at_utc",
        record["consumer_evaluation_at_utc"],
    )

    signal_ids = record["signal_ids"]
    if not isinstance(signal_ids, list) or not signal_ids:
        _fail(
            "SIGNAL_ID_MISMATCH",
            "signal_ids must be a non-empty list",
        )

    checked_signal_ids = [
        _text(f"record.signal_ids[{index}]", signal_id)
        for index, signal_id in enumerate(signal_ids)
    ]

    if len(checked_signal_ids) != len(set(checked_signal_ids)):
        _fail(
            "DUPLICATE_SIGNAL_CORRESPONDENCE",
            "parity signal_ids contain duplicates",
        )

    if checked_signal_ids != sorted(checked_signal_ids):
        _fail(
            "SIGNAL_ID_MISMATCH",
            "parity signal_ids must use deterministic canonical ordering",
        )

    assertions = _mapping(
        "record.parity_assertions",
        record["parity_assertions"],
    )
    if assertions != _PARITY_ASSERTIONS:
        _fail(
            "PARITY_RECORD_SCHEMA_MISMATCH",
            "parity_assertions must be the exact canonical PASS assertion set",
        )

    expected_record = _build_parity_record(
        source,
        consumer,
    )

    for field in sorted(_RECORD_KEYS - {"parity_id"}):
        if record[field] != expected_record[field] or (
            type(record[field]) is not type(expected_record[field])
        ):
            _fail(
                "PARITY_RECORD_CROSSLINK_MISMATCH",
                f"record.{field} does not match supplied validated evidence",
            )

    if record["parity_id"] != expected_record["parity_id"]:
        _fail(
            "PARITY_IDENTITY_MISMATCH",
            "parity_id does not match supplied validated evidence",
        )

    if not hmac.compare_digest(
        _digest(record),
        parity_sha256,
    ):
        _fail(
            "PARITY_CHECKSUM_MISMATCH",
            "parity SHA-256 does not match canonical record",
        )


def canonical_serialize_external_signal_parity_evidence(
    evidence: dict[str, Any],
    *,
    package: dict[str, Any],
    consumer_evidence: dict[str, Any],
) -> str:
    """Return canonical JSON after complete cross-contract parity validation."""

    validate_external_signal_parity_evidence(
        evidence,
        package=package,
        consumer_evidence=consumer_evidence,
    )
    return _canonical_json(evidence)
