"""Focused tests for the C4 TM-020 offline governed signal consumer."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from quantitative_trading_research.execution.quantconnect_signal_producer import (
    build_external_signal_package,
)
from quantitative_trading_research.execution.quantconnect_signal_consumer import (
    CHECKSUM_ALGORITHM,
    ELIGIBILITY_STATE,
    EVIDENCE_SCOPE,
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    ExternalSignalConsumerError,
    build_external_signal_consumption_evidence,
    canonical_serialize_external_signal_consumption_evidence,
    validate_external_signal_consumption_evidence,
)


PREDICTION_AT = "2026-08-23T15:00:00+00:00"
DECISION_AT = "2026-08-23T15:01:00+00:00"
PUBLICATION_AT = "2026-08-23T15:02:00+00:00"
AVAILABILITY_AT = "2026-08-23T15:03:00+00:00"
SOURCE_EVALUATION_AT = "2026-08-23T15:04:00+00:00"
VALID_UNTIL = "2026-08-23T16:00:00+00:00"

CONSUMER_EVALUATION_AT = "2026-08-23T15:30:00+00:00"
DECISION_BAR_END = "2026-08-23T15:10:00+00:00"
ELIGIBLE_AT = "2026-08-23T15:10:00+00:00"

PRODUCER_COMMIT = "a" * 40
MODEL_SHA = "b" * 64
ARTIFACT_SHA = "c" * 64
PREDICTION_SHA = "d" * 64


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _test_identity(prefix: str, value: object) -> str:
    digest = hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()
    return f"{prefix}:{digest}"


def _rebind_consumer_owned_integrity(evidence: dict) -> dict:
    """Recompute only TM-020-owned identities/checksum after test tampering."""

    record = evidence["record"]

    run_payload = {
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
    record["consumer_run_id"] = _test_identity(
        "external_signal_consumer_run",
        run_payload,
    )

    identity_payload = {
        "schema_id": record["schema_id"],
        "schema_version": record["schema_version"],
        "result_type": record["result_type"],
        "evidence_scope": record["evidence_scope"],
        "consumer_run_id": record["consumer_run_id"],
    }
    record["consumer_id"] = _test_identity(
        "external_signal_consumer",
        identity_payload,
    )
    evidence["consumer_sha256"] = hashlib.sha256(
        _canonical_json(record).encode("utf-8")
    ).hexdigest()

    return evidence


def _signal(
    *,
    instrument_id: str = "AAA",
    canonical_instrument_id: str = "AAA",
    signal: str = "BUY",
    confidence: float | None = 0.75,
    prediction_at_utc: str = PREDICTION_AT,
    decision_at_utc: str = DECISION_AT,
    valid_until_utc: str = VALID_UNTIL,
) -> dict:
    value = {
        "instrument_id": instrument_id,
        "canonical_instrument_id": canonical_instrument_id,
        "signal": signal,
        "prediction_at_utc": prediction_at_utc,
        "decision_at_utc": decision_at_utc,
        "valid_until_utc": valid_until_utc,
    }
    if confidence is not None:
        value["confidence"] = confidence
    return value


def _source_package(
    *,
    signals: list[dict] | None = None,
    producer_identity: str = "producer-source-a",
    aliases: list[dict[str, str]] | None = None,
    evaluation_at_utc: str = SOURCE_EVALUATION_AT,
    availability_at_utc: str = AVAILABILITY_AT,
) -> dict:
    return build_external_signal_package(
        producer_identity=producer_identity,
        producer_commit=PRODUCER_COMMIT,
        model_identity="model-a",
        model_sha256=MODEL_SHA,
        artifact_identity="artifact-a",
        artifact_sha256=ARTIFACT_SHA,
        prediction_identity="prediction-a",
        prediction_sha256=PREDICTION_SHA,
        signals=[_signal()] if signals is None else signals,
        publication_at_utc=PUBLICATION_AT,
        availability_at_utc=availability_at_utc,
        evaluation_at_utc=evaluation_at_utc,
        aliases=aliases,
    )


def _temporal(
    package: dict,
    *,
    decision_bar_end_at_utc: str = DECISION_BAR_END,
    eligible_reference_at_utc: str = ELIGIBLE_AT,
) -> list[dict]:
    return [
        {
            "signal_id": signal["signal_id"],
            "decision_bar_end_at_utc": decision_bar_end_at_utc,
            "eligible_reference_at_utc": eligible_reference_at_utc,
        }
        for signal in package["record"]["signals"]
    ]


def _consume(
    package: dict | None = None,
    *,
    consumer_evaluation_at_utc: str = CONSUMER_EVALUATION_AT,
    temporal_evidence: list[dict] | None = None,
) -> dict:
    source = _source_package() if package is None else package
    temporal = (
        _temporal(source)
        if temporal_evidence is None
        else temporal_evidence
    )
    return build_external_signal_consumption_evidence(
        package=source,
        consumer_evaluation_at_utc=consumer_evaluation_at_utc,
        temporal_evidence=temporal,
    )


class QuantConnectSignalConsumerTests(unittest.TestCase):
    def test_valid_single_signal_is_versioned_offline_and_nonoperational(self):
        package = _source_package()
        evidence = _consume(package)
        record = evidence["record"]
        signal = record["signals"][0]

        self.assertEqual(record["schema_id"], SCHEMA_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["result_type"], RESULT_TYPE)
        self.assertEqual(record["evidence_scope"], EVIDENCE_SCOPE)
        self.assertEqual(evidence["checksum_algorithm"], CHECKSUM_ALGORITHM)
        self.assertEqual(signal["eligibility_state"], ELIGIBILITY_STATE)

        self.assertEqual(
            record["source_package_id"],
            package["record"]["package_id"],
        )
        self.assertEqual(
            record["source_package_sha256"],
            package["package_sha256"],
        )
        self.assertEqual(
            record["source_run_id"],
            package["record"]["run_id"],
        )
        self.assertEqual(
            record["source_prediction_identity"],
            package["record"]["prediction_identity"],
        )
        self.assertEqual(
            record["source_prediction_sha256"],
            package["record"]["prediction_sha256"],
        )
        self.assertEqual(
            signal["signal_id"],
            package["record"]["signals"][0]["signal_id"],
        )
        self.assertEqual(
            signal["canonical_instrument_id"],
            package["record"]["signals"][0]["canonical_instrument_id"],
        )

        prohibited = {
            "order",
            "order_id",
            "fill",
            "fill_id",
            "position",
            "target_weight",
            "portfolio_weight",
            "broker_account",
            "execution_at_utc",
            "fill_at_utc",
            "submission_at_utc",
        }
        self.assertTrue(prohibited.isdisjoint(record))
        self.assertTrue(prohibited.isdisjoint(signal))

        validate_external_signal_consumption_evidence(evidence)

    def test_valid_multi_signal_is_canonical_and_temporal_input_order_independent(self):
        package = _source_package(
            signals=[
                _signal(
                    instrument_id="ZZZ",
                    canonical_instrument_id="ZZZ",
                    signal="SELL",
                    confidence=0.40,
                ),
                _signal(
                    instrument_id="AAA",
                    canonical_instrument_id="AAA",
                    signal="HOLD",
                    confidence=None,
                ),
            ]
        )

        temporal = _temporal(package)
        reversed_temporal = list(reversed(deepcopy(temporal)))

        first = _consume(package, temporal_evidence=temporal)
        second = _consume(package, temporal_evidence=reversed_temporal)

        self.assertEqual(first, second)
        self.assertEqual(
            [
                item["canonical_instrument_id"]
                for item in first["record"]["signals"]
            ],
            ["AAA", "ZZZ"],
        )

    def test_repeat_construction_and_canonical_serialization_are_deterministic(self):
        package = _source_package()
        temporal = _temporal(package)

        first = _consume(package, temporal_evidence=temporal)
        second = _consume(
            deepcopy(package),
            temporal_evidence=deepcopy(temporal),
        )

        self.assertEqual(first, second)
        self.assertEqual(
            first["record"]["consumer_run_id"],
            second["record"]["consumer_run_id"],
        )
        self.assertEqual(
            first["record"]["consumer_id"],
            second["record"]["consumer_id"],
        )
        self.assertEqual(
            first["consumer_sha256"],
            second["consumer_sha256"],
        )
        self.assertEqual(
            canonical_serialize_external_signal_consumption_evidence(first),
            canonical_serialize_external_signal_consumption_evidence(second),
        )

    def test_temporal_dictionary_order_does_not_affect_identity(self):
        package = _source_package()
        original = _temporal(package)[0]
        reversed_entry = dict(reversed(list(original.items())))

        first = _consume(package, temporal_evidence=[original])
        second = _consume(package, temporal_evidence=[reversed_entry])

        self.assertEqual(first, second)

    def test_invalid_or_tampered_source_package_fails_closed(self):
        package = _source_package()

        missing = deepcopy(package)
        del missing["record"]["model_identity"]

        checksum_tampered = deepcopy(package)
        checksum_tampered["package_sha256"] = "0" * 64

        package_id_tampered = deepcopy(package)
        package_id_tampered["record"]["package_id"] = (
            "external_signal_package:" + ("0" * 64)
        )

        run_id_tampered = deepcopy(package)
        run_id_tampered["record"]["run_id"] = (
            "external_signal_run:" + ("0" * 64)
        )

        signal_id_tampered = deepcopy(package)
        signal_id_tampered["record"]["signals"][0]["signal_id"] = (
            "external_signal:" + ("0" * 64)
        )

        for candidate in (
            missing,
            checksum_tampered,
            package_id_tampered,
            run_id_tampered,
            signal_id_tampered,
        ):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ExternalSignalConsumerError):
                    _consume(
                        candidate,
                        temporal_evidence=_temporal(package),
                    )

    def test_source_identities_and_instrument_evidence_are_preserved(self):
        package = _source_package(
            signals=[
                _signal(
                    instrument_id="BRK.B",
                    canonical_instrument_id="BRK-B",
                )
            ],
            aliases=[
                {
                    "alias": "BRK.B",
                    "canonical_instrument_id": "BRK-B",
                }
            ],
        )

        evidence = _consume(package)
        record = evidence["record"]
        source_record = package["record"]

        self.assertEqual(
            record["source_package_id"],
            source_record["package_id"],
        )
        self.assertEqual(
            record["source_package_sha256"],
            package["package_sha256"],
        )
        self.assertEqual(record["source_run_id"], source_record["run_id"])
        self.assertEqual(
            record["source_prediction_identity"],
            source_record["prediction_identity"],
        )
        self.assertEqual(
            record["source_prediction_sha256"],
            source_record["prediction_sha256"],
        )
        self.assertEqual(
            record["signals"][0]["signal_id"],
            source_record["signals"][0]["signal_id"],
        )
        self.assertEqual(
            record["signals"][0]["instrument_id"],
            "BRK.B",
        )
        self.assertEqual(
            record["signals"][0]["canonical_instrument_id"],
            "BRK-B",
        )

    def test_prediction_identity_crosslink_fails_closed_after_consumer_rehash(self):
        evidence = _consume()

        changed_identity = deepcopy(evidence)
        changed_identity["record"]["source_prediction_identity"] = (
            "prediction-tampered"
        )
        _rebind_consumer_owned_integrity(changed_identity)

        with self.assertRaises(ExternalSignalConsumerError):
            validate_external_signal_consumption_evidence(
                changed_identity
            )

        changed_sha = deepcopy(evidence)
        changed_sha["record"]["source_prediction_sha256"] = "e" * 64
        _rebind_consumer_owned_integrity(changed_sha)

        with self.assertRaises(ExternalSignalConsumerError):
            validate_external_signal_consumption_evidence(
                changed_sha
            )

    def test_exact_temporal_correspondence_rejects_missing_extra_duplicate_and_unknown(self):
        package = _source_package(
            signals=[
                _signal(
                    instrument_id="AAA",
                    canonical_instrument_id="AAA",
                ),
                _signal(
                    instrument_id="BBB",
                    canonical_instrument_id="BBB",
                    signal="SELL",
                ),
            ]
        )
        temporal = _temporal(package)

        missing = temporal[:1]

        extra = deepcopy(temporal)
        extra.append(
            {
                "signal_id": "external_signal:" + ("f" * 64),
                "decision_bar_end_at_utc": DECISION_BAR_END,
                "eligible_reference_at_utc": ELIGIBLE_AT,
            }
        )

        duplicate = deepcopy(temporal)
        duplicate.append(deepcopy(temporal[0]))

        unknown = deepcopy(temporal)
        unknown[0]["signal_id"] = "external_signal:" + ("e" * 64)

        for name, candidate in (
            ("missing", missing),
            ("extra", extra),
            ("duplicate", duplicate),
            ("unknown", unknown),
        ):
            with self.subTest(name=name):
                with self.assertRaises(ExternalSignalConsumerError):
                    _consume(package, temporal_evidence=candidate)

    def test_same_bar_exclusive_boundary_semantics(self):
        package = _source_package()

        before = _temporal(
            package,
            decision_bar_end_at_utc="2026-08-23T15:10:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:09:59+00:00",
        )
        with self.assertRaises(ExternalSignalConsumerError):
            _consume(package, temporal_evidence=before)

        equality = _temporal(
            package,
            decision_bar_end_at_utc="2026-08-23T15:10:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:10:00+00:00",
        )
        equal_result = _consume(package, temporal_evidence=equality)
        self.assertEqual(
            equal_result["record"]["signals"][0]["eligible_reference_at_utc"],
            "2026-08-23T15:10:00+00:00",
        )

        later = _temporal(
            package,
            decision_bar_end_at_utc="2026-08-23T15:10:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:11:00+00:00",
        )
        later_result = _consume(package, temporal_evidence=later)
        self.assertEqual(
            later_result["record"]["signals"][0]["eligibility_state"],
            ELIGIBILITY_STATE,
        )

    def test_source_decision_after_decision_bar_end_is_rejected(self):
        package = _source_package()

        temporal = _temporal(
            package,
            decision_bar_end_at_utc="2026-08-23T15:00:30+00:00",
            eligible_reference_at_utc="2026-08-23T15:00:30+00:00",
        )

        with self.assertRaises(ExternalSignalConsumerError):
            _consume(package, temporal_evidence=temporal)

    def test_consumer_evaluation_boundaries_and_staleness(self):
        package = _source_package()

        with self.assertRaises(ExternalSignalConsumerError):
            _consume(
                package,
                consumer_evaluation_at_utc="2026-08-23T15:03:59+00:00",
                temporal_evidence=_temporal(
                    package,
                    decision_bar_end_at_utc="2026-08-23T15:03:00+00:00",
                    eligible_reference_at_utc="2026-08-23T15:03:00+00:00",
                ),
            )

        valid_at_source_evaluation = _consume(
            package,
            consumer_evaluation_at_utc=SOURCE_EVALUATION_AT,
            temporal_evidence=_temporal(
                package,
                decision_bar_end_at_utc="2026-08-23T15:03:00+00:00",
                eligible_reference_at_utc="2026-08-23T15:03:00+00:00",
            ),
        )
        self.assertEqual(
            valid_at_source_evaluation["record"]["consumer_evaluation_at_utc"],
            SOURCE_EVALUATION_AT,
        )

        valid_at_expiry = _consume(
            package,
            consumer_evaluation_at_utc=VALID_UNTIL,
            temporal_evidence=_temporal(
                package,
                decision_bar_end_at_utc=DECISION_BAR_END,
                eligible_reference_at_utc="2026-08-23T15:59:00+00:00",
            ),
        )
        self.assertEqual(
            valid_at_expiry["record"]["consumer_evaluation_at_utc"],
            VALID_UNTIL,
        )

        with self.assertRaises(ExternalSignalConsumerError):
            _consume(
                package,
                consumer_evaluation_at_utc="2026-08-23T16:00:01+00:00",
                temporal_evidence=_temporal(package),
            )

    def test_future_eligible_reference_is_rejected(self):
        package = _source_package()
        temporal = _temporal(
            package,
            decision_bar_end_at_utc=DECISION_BAR_END,
            eligible_reference_at_utc="2026-08-23T15:31:00+00:00",
        )

        with self.assertRaises(ExternalSignalConsumerError):
            _consume(
                package,
                consumer_evaluation_at_utc=CONSUMER_EVALUATION_AT,
                temporal_evidence=temporal,
            )

    def test_consumer_timestamp_validation_is_fail_closed(self):
        package = _source_package()

        for bad_value in (
            "2026-08-23T15:30:00",
            "2026-08-23T11:30:00-04:00",
            "not-a-timestamp",
        ):
            with self.subTest(field="consumer_evaluation", value=bad_value):
                with self.assertRaises(ExternalSignalConsumerError):
                    _consume(
                        package,
                        consumer_evaluation_at_utc=bad_value,
                    )

        for field in (
            "decision_bar_end_at_utc",
            "eligible_reference_at_utc",
        ):
            for bad_value in (
                "2026-08-23T15:10:00",
                "2026-08-23T11:10:00-04:00",
                "not-a-timestamp",
            ):
                with self.subTest(field=field, value=bad_value):
                    temporal = _temporal(package)
                    temporal[0][field] = bad_value
                    with self.assertRaises(ExternalSignalConsumerError):
                        _consume(
                            package,
                            temporal_evidence=temporal,
                        )

    def test_consumer_strict_schema_and_numeric_validation(self):
        evidence = _consume()

        unexpected = deepcopy(evidence)
        unexpected["record"]["provider_response"] = {}

        bad_version = deepcopy(evidence)
        bad_version["record"]["schema_version"] = True

        bad_checksum = deepcopy(evidence)
        bad_checksum["consumer_sha256"] = "not-a-sha"

        bad_confidence = deepcopy(evidence)
        bad_confidence["record"]["signals"][0]["confidence"] = 1

        bad_signal = deepcopy(evidence)
        bad_signal["record"]["signals"][0]["signal"] = "STRONG_BUY"

        for candidate in (
            unexpected,
            bad_version,
            bad_checksum,
            bad_confidence,
            bad_signal,
        ):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ExternalSignalConsumerError):
                    validate_external_signal_consumption_evidence(candidate)

    def test_material_evidence_changes_identity_and_checksum(self):
        package = _source_package()

        base = _consume(package)

        changed_evaluation = _consume(
            package,
            consumer_evaluation_at_utc="2026-08-23T15:31:00+00:00",
        )

        changed_bar_end = _consume(
            package,
            temporal_evidence=_temporal(
                package,
                decision_bar_end_at_utc="2026-08-23T15:09:00+00:00",
                eligible_reference_at_utc=ELIGIBLE_AT,
            ),
        )

        changed_reference = _consume(
            package,
            temporal_evidence=_temporal(
                package,
                decision_bar_end_at_utc=DECISION_BAR_END,
                eligible_reference_at_utc="2026-08-23T15:11:00+00:00",
            ),
        )

        different_source = _source_package(
            producer_identity="producer-source-b"
        )
        changed_source = _consume(different_source)

        for candidate in (
            changed_evaluation,
            changed_bar_end,
            changed_reference,
            changed_source,
        ):
            with self.subTest(candidate=candidate):
                self.assertNotEqual(
                    base["record"]["consumer_run_id"],
                    candidate["record"]["consumer_run_id"],
                )
                self.assertNotEqual(
                    base["record"]["consumer_id"],
                    candidate["record"]["consumer_id"],
                )
                self.assertNotEqual(
                    base["consumer_sha256"],
                    candidate["consumer_sha256"],
                )

    def test_tampered_consumer_evidence_fails_closed(self):
        evidence = _consume()

        changed_time = deepcopy(evidence)
        changed_time["record"]["consumer_evaluation_at_utc"] = (
            "2026-08-23T15:31:00+00:00"
        )

        changed_signal = deepcopy(evidence)
        changed_signal["record"]["signals"][0]["eligible_reference_at_utc"] = (
            "2026-08-23T15:11:00+00:00"
        )

        changed_identity = deepcopy(evidence)
        changed_identity["record"]["consumer_run_id"] = (
            "external_signal_consumer_run:" + ("0" * 64)
        )

        changed_checksum = deepcopy(evidence)
        changed_checksum["consumer_sha256"] = "0" * 64

        for candidate in (
            changed_time,
            changed_signal,
            changed_identity,
            changed_checksum,
        ):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ExternalSignalConsumerError):
                    validate_external_signal_consumption_evidence(candidate)

    def test_builder_does_not_mutate_caller_inputs(self):
        package = _source_package()
        temporal = _temporal(package)

        original_package = deepcopy(package)
        original_temporal = deepcopy(temporal)

        _consume(package, temporal_evidence=temporal)

        self.assertEqual(package, original_package)
        self.assertEqual(temporal, original_temporal)

    def test_static_boundary_is_offline_nonoperational_and_dependency_neutral(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "quantconnect_signal_consumer.py"
        )
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        allowed_roots = {
            "__future__",
            "copy",
            "datetime",
            "hashlib",
            "hmac",
            "json",
            "math",
            "typing",
            "quantitative_trading_research",
        }
        observed_roots: set[str] = set()
        producer_imports: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                observed_roots.update(
                    alias.name.split(".")[0]
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                observed_roots.add(node.module.split(".")[0])
                if (
                    node.module
                    == "quantitative_trading_research.execution."
                    "quantconnect_signal_producer"
                ):
                    producer_imports.update(
                        alias.name for alias in node.names
                    )

        self.assertLessEqual(observed_roots, allowed_roots)
        self.assertIn(
            "validate_external_signal_package",
            producer_imports,
        )
        self.assertFalse(
            any(name.startswith("_") for name in producer_imports)
        )

        prohibited_tokens = (
            "datetime.now(",
            "datetime.utcnow(",
            "time.time(",
            "os.environ",
            "os.getenv(",
            "getenv(",
            "requests.",
            "urllib.",
            "socket.",
            "http.client",
            "AlgorithmImports",
            "QCAlgorithm",
            "AddEquity(",
            "SetHoldings(",
            "PortfolioTarget(",
            "SetBrokerageModel(",
            "GetParameter(",
            "self.Download(",
            "submit_order(",
            "submit_market_order",
            "market_order(",
            "limit_order(",
            "get_account(",
            "get_orders(",
            "read_csv(",
            "to_csv(",
            "write_text(",
            "write_bytes(",
            "open(",
            "model.predict(",
            ".fit(",
        )

        for token in prohibited_tokens:
            self.assertNotIn(token, source)

    def test_historical_attribution_and_residual_boundary_are_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "quantconnect_signal_consumer.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertIn("racoope70/ppo-trading-pipeline", source)
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source,
        )
        self.assertIn(
            "quantconnect/ExternalSignalConsumer.py",
            source,
        )
        self.assertIn(
            "deterministic offline temporal-eligibility evidence",
            source,
        )

        evidence = _consume()
        record = evidence["record"]

        prohibited_operational_fields = {
            "order",
            "order_id",
            "fill",
            "fill_id",
            "execution_at_utc",
            "submission_at_utc",
            "position",
            "quantity",
            "portfolio",
            "target_weight",
            "submission_authorized",
            "execution_authorized",
        }

        self.assertTrue(
            prohibited_operational_fields.isdisjoint(record)
        )
        for signal in record["signals"]:
            self.assertTrue(
                prohibited_operational_fields.isdisjoint(signal)
            )


if __name__ == "__main__":
    unittest.main()
