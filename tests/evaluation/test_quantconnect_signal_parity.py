"""Focused tests for C4 TM-021 offline TM-019/TM-020 parity."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from quantitative_trading_research.execution.quantconnect_signal_consumer import (
    ExternalSignalConsumerError,
    build_external_signal_consumption_evidence,
    validate_external_signal_consumption_evidence,
)
from quantitative_trading_research.execution.quantconnect_signal_producer import (
    ExternalSignalPackageError,
    build_external_signal_package,
    validate_external_signal_package,
)
from quantitative_trading_research.evaluation.quantconnect_signal_parity import (
    CHECKSUM_ALGORITHM,
    PARITY_STATE,
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    ExternalSignalParityError,
    build_external_signal_parity_evidence,
    canonical_serialize_external_signal_parity_evidence,
    validate_external_signal_parity_evidence,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    ROOT
    / "src"
    / "quantitative_trading_research"
    / "evaluation"
    / "quantconnect_signal_parity.py"
)

PREDICTION_AT = "2026-08-23T15:00:00+00:00"
DECISION_AT = "2026-08-23T15:01:00+00:00"
PUBLICATION_AT = "2026-08-23T15:02:00+00:00"
AVAILABILITY_AT = "2026-08-23T15:03:00+00:00"
SOURCE_EVALUATION_AT = "2026-08-23T15:04:00+00:00"
VALID_UNTIL = "2026-08-23T16:00:00+00:00"

DECISION_BAR_END = "2026-08-23T15:10:00+00:00"
ELIGIBLE_AT = "2026-08-23T15:10:00+00:00"
LATER_ELIGIBLE_AT = "2026-08-23T15:11:00+00:00"
CONSUMER_EVALUATION_AT = "2026-08-23T15:30:00+00:00"

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


def _digest(value: object) -> str:
    return hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _identity(prefix: str, value: object) -> str:
    return f"{prefix}:{_digest(value)}"


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


def _package(
    *,
    signals: list[dict] | None = None,
    aliases: list[dict[str, str]] | None = None,
    producer_identity: str = "producer-source-a",
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
            "signal_id": item["signal_id"],
            "decision_bar_end_at_utc": decision_bar_end_at_utc,
            "eligible_reference_at_utc": eligible_reference_at_utc,
        }
        for item in package["record"]["signals"]
    ]


def _consumer(
    package: dict,
    *,
    consumer_evaluation_at_utc: str = CONSUMER_EVALUATION_AT,
    temporal_evidence: list[dict] | None = None,
) -> dict:
    return build_external_signal_consumption_evidence(
        package=package,
        consumer_evaluation_at_utc=consumer_evaluation_at_utc,
        temporal_evidence=(
            _temporal(package)
            if temporal_evidence is None
            else temporal_evidence
        ),
    )


def _pair(
    *,
    signals: list[dict] | None = None,
    aliases: list[dict[str, str]] | None = None,
) -> tuple[dict, dict]:
    package = _package(signals=signals, aliases=aliases)
    return package, _consumer(package)


def _rebind_consumer_owned_integrity(evidence: dict) -> dict:
    """Recompute only TM-020-owned identities/checksum after test mutation."""

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
    record["consumer_run_id"] = _identity(
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
    record["consumer_id"] = _identity(
        "external_signal_consumer",
        identity_payload,
    )

    evidence["consumer_sha256"] = _digest(record)
    return evidence


def _rebind_parity_owned_integrity(evidence: dict) -> dict:
    """Recompute only TM-021-owned identity/checksum after test mutation."""

    record = evidence["record"]
    payload = {
        key: record[key]
        for key in sorted(record)
        if key != "parity_id"
    }
    record["parity_id"] = _identity(
        "external_signal_parity",
        payload,
    )
    evidence["parity_sha256"] = _digest(record)
    return evidence


def _consumer_source_signal_id(
    signal: dict,
    *,
    prediction_identity: str,
    prediction_sha256: str,
) -> str:
    payload = {
        "prediction_identity": prediction_identity,
        "prediction_sha256": prediction_sha256,
        "signal": {
            "instrument_id": signal["instrument_id"],
            "canonical_instrument_id": signal["canonical_instrument_id"],
            "signal": signal["signal"],
            "prediction_at_utc": signal["source_prediction_at_utc"],
            "decision_at_utc": signal["source_decision_at_utc"],
            "valid_until_utc": signal["source_valid_until_utc"],
            "confidence": signal["confidence"],
        },
    }
    return _identity("external_signal", payload)


class QuantConnectSignalParityTests(unittest.TestCase):
    def test_valid_single_signal_parity_is_exact_versioned_and_pass_only(self):
        package, consumer = _pair()

        parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )
        record = parity["record"]

        self.assertEqual(record["schema_id"], SCHEMA_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["result_type"], RESULT_TYPE)
        self.assertEqual(record["parity_state"], PARITY_STATE)
        self.assertEqual(parity["checksum_algorithm"], CHECKSUM_ALGORITHM)

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
            record["consumer_id"],
            consumer["record"]["consumer_id"],
        )
        self.assertEqual(
            record["consumer_run_id"],
            consumer["record"]["consumer_run_id"],
        )
        self.assertEqual(
            record["consumer_sha256"],
            consumer["consumer_sha256"],
        )

        self.assertEqual(
            record["signal_ids"],
            [package["record"]["signals"][0]["signal_id"]],
        )

        validate_external_signal_parity_evidence(
            parity,
            package=package,
            consumer_evidence=consumer,
        )

    def test_multi_signal_parity_is_bijective_deterministic_and_order_independent(self):
        signals = [
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
        package = _package(signals=signals)
        consumer = _consumer(
            package,
            temporal_evidence=list(reversed(_temporal(package))),
        )

        package_before = deepcopy(package)
        consumer_before = deepcopy(consumer)

        first = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )
        second = build_external_signal_parity_evidence(
            package=deepcopy(package),
            consumer_evidence=deepcopy(consumer),
        )

        reordered_package = {
            "package_sha256": package["package_sha256"],
            "checksum_algorithm": package["checksum_algorithm"],
            "record": dict(reversed(list(package["record"].items()))),
        }
        third = build_external_signal_parity_evidence(
            package=reordered_package,
            consumer_evidence=consumer,
        )

        self.assertEqual(first, second)
        self.assertEqual(first, third)
        self.assertEqual(package, package_before)
        self.assertEqual(consumer, consumer_before)

        expected_ids = sorted(
            item["signal_id"] for item in package["record"]["signals"]
        )
        self.assertEqual(first["record"]["signal_ids"], expected_ids)
        self.assertEqual(
            first["record"]["parity_id"],
            second["record"]["parity_id"],
        )
        self.assertEqual(
            first["parity_sha256"],
            second["parity_sha256"],
        )

        self.assertEqual(
            canonical_serialize_external_signal_parity_evidence(
                first,
                package=package,
                consumer_evidence=consumer,
            ),
            canonical_serialize_external_signal_parity_evidence(
                second,
                package=package,
                consumer_evidence=consumer,
            ),
        )

    def test_public_validator_composition_and_static_purity_boundary(self):
        source_text = SOURCE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source_text)

        self.assertIn("validate_external_signal_package", source_text)
        self.assertIn(
            "validate_external_signal_consumption_evidence",
            source_text,
        )

        upstream_modules = {
            "quantitative_trading_research.execution.quantconnect_signal_producer",
            "quantitative_trading_research.execution.quantconnect_signal_consumer",
        }
        private_imports: list[str] = []
        observed_roots: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    observed_roots.add(alias.name.split(".")[0])

            if isinstance(node, ast.ImportFrom) and node.module:
                observed_roots.add(node.module.split(".")[0])
                if node.module in upstream_modules:
                    for alias in node.names:
                        if alias.name.startswith("_"):
                            private_imports.append(alias.name)

        self.assertEqual(private_imports, [])

        prohibited_roots = {
            "argparse",
            "os",
            "pandas",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
        self.assertTrue(observed_roots.isdisjoint(prohibited_roots))

        self.assertNotIn("decision_bar_end_at_utc", source_text)
        self.assertNotIn("eligible_reference_at_utc", source_text)
        self.assertNotIn("AlgorithmImports", source_text)

        self.assertIn("racoope70/ppo-trading-pipeline", source_text)
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source_text,
        )
        self.assertIn(
            "src/model_selection/quantconnect_execution_retest.py",
            source_text,
        )
        self.assertIn(
            "Pure deterministic offline TM-019/TM-020 contract-parity harness",
            source_text,
        )

    def test_invalid_upstream_evidence_is_rejected_via_public_contracts(self):
        package, consumer = _pair()

        bad_package = deepcopy(package)
        bad_package["package_sha256"] = "0" * 64

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "INVALID_PRODUCER_PACKAGE",
        ):
            build_external_signal_parity_evidence(
                package=bad_package,
                consumer_evidence=consumer,
            )

        bad_consumer = deepcopy(consumer)
        bad_consumer["consumer_sha256"] = "0" * 64

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "INVALID_CONSUMER_EVIDENCE",
        ):
            build_external_signal_parity_evidence(
                package=package,
                consumer_evidence=bad_consumer,
            )

    def test_package_run_and_prediction_crosslink_mismatches_fail_closed(self):
        package, consumer = _pair()

        cases = (
            (
                "source_package_id",
                "external_signal_package:" + ("0" * 64),
                "PACKAGE_ID_MISMATCH",
            ),
            (
                "source_package_sha256",
                "0" * 64,
                "PACKAGE_CHECKSUM_MISMATCH",
            ),
            (
                "source_run_id",
                "external_signal_run:" + ("0" * 64),
                "RUN_ID_MISMATCH",
            ),
        )

        for field, replacement, expected_code in cases:
            with self.subTest(field=field):
                candidate = deepcopy(consumer)
                candidate["record"][field] = replacement
                _rebind_consumer_owned_integrity(candidate)

                validate_external_signal_consumption_evidence(candidate)

                with self.assertRaisesRegex(
                    ExternalSignalParityError,
                    expected_code,
                ):
                    build_external_signal_parity_evidence(
                        package=package,
                        consumer_evidence=candidate,
                    )

        other_package = _package(producer_identity="producer-source-b")
        other_consumer = _consumer(other_package)

        with self.assertRaises(ExternalSignalParityError):
            build_external_signal_parity_evidence(
                package=package,
                consumer_evidence=other_consumer,
            )

    def test_signal_correspondence_rejects_missing_extra_and_duplicate(self):
        package = _package(
            signals=[
                _signal(
                    instrument_id="AAA",
                    canonical_instrument_id="AAA",
                ),
                _signal(
                    instrument_id="ZZZ",
                    canonical_instrument_id="ZZZ",
                    signal="SELL",
                    confidence=0.50,
                ),
            ]
        )
        consumer = _consumer(package)

        missing = deepcopy(consumer)
        missing["record"]["signals"] = missing["record"]["signals"][:1]
        _rebind_consumer_owned_integrity(missing)
        validate_external_signal_consumption_evidence(missing)

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "MISSING_SIGNAL",
        ):
            build_external_signal_parity_evidence(
                package=package,
                consumer_evidence=missing,
            )

        extra = deepcopy(consumer)
        extra_signal = deepcopy(extra["record"]["signals"][-1])
        extra_signal["instrument_id"] = "YYY"
        extra_signal["canonical_instrument_id"] = "YYY"
        extra_signal["signal_id"] = _consumer_source_signal_id(
            extra_signal,
            prediction_identity=extra["record"][
                "source_prediction_identity"
            ],
            prediction_sha256=extra["record"][
                "source_prediction_sha256"
            ],
        )
        extra["record"]["signals"].append(extra_signal)
        extra["record"]["signals"].sort(
            key=lambda item: item["canonical_instrument_id"]
        )
        _rebind_consumer_owned_integrity(extra)
        validate_external_signal_consumption_evidence(extra)

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "EXTRA_SIGNAL",
        ):
            build_external_signal_parity_evidence(
                package=package,
                consumer_evidence=extra,
            )

        duplicate = deepcopy(consumer)
        duplicate["record"]["signals"].append(
            deepcopy(duplicate["record"]["signals"][0])
        )
        duplicate["record"]["signals"].sort(
            key=lambda item: item["canonical_instrument_id"]
        )
        _rebind_consumer_owned_integrity(duplicate)

        with self.assertRaises(ExternalSignalParityError):
            build_external_signal_parity_evidence(
                package=package,
                consumer_evidence=duplicate,
            )

    def test_per_signal_mutation_and_numeric_coercion_do_not_pass(self):
        package, consumer = _pair()

        mutations = (
            ("instrument_id", "BBB"),
            ("canonical_instrument_id", "BBB"),
            ("signal", "SELL"),
            ("confidence", 0.25),
        )

        for field, replacement in mutations:
            with self.subTest(field=field):
                candidate = deepcopy(consumer)
                candidate["record"]["signals"][0][field] = replacement
                _rebind_consumer_owned_integrity(candidate)

                with self.assertRaisesRegex(
                    ExternalSignalParityError,
                    "INVALID_CONSUMER_EVIDENCE",
                ):
                    build_external_signal_parity_evidence(
                        package=package,
                        consumer_evidence=candidate,
                    )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    {
                        **_signal(),
                        "confidence": 1,
                    }
                ]
            )

    def test_alias_identity_is_preserved_without_reresolution(self):
        package = _package(
            signals=[
                _signal(
                    instrument_id="BRK.B",
                    canonical_instrument_id="BRK-B",
                    signal="HOLD",
                    confidence=None,
                )
            ],
            aliases=[
                {
                    "alias": "BRK.B",
                    "canonical_instrument_id": "BRK-B",
                }
            ],
        )
        consumer = _consumer(package)
        parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )

        source_signal = package["record"]["signals"][0]
        consumed_signal = consumer["record"]["signals"][0]

        self.assertEqual(
            consumed_signal["instrument_id"],
            source_signal["instrument_id"],
        )
        self.assertEqual(
            consumed_signal["canonical_instrument_id"],
            source_signal["canonical_instrument_id"],
        )
        self.assertEqual(
            parity["record"]["signal_ids"],
            [source_signal["signal_id"]],
        )

    def test_producer_temporal_evidence_is_preserved_exactly(self):
        package, consumer = _pair()

        parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )

        source_record = package["record"]
        consumer_record = consumer["record"]
        source_signal = source_record["signals"][0]
        consumed_signal = consumer_record["signals"][0]

        self.assertEqual(
            consumer_record["source_evaluation_at_utc"],
            source_record["evaluation_at_utc"],
        )
        self.assertEqual(
            consumer_record["source_availability_at_utc"],
            source_record["availability_at_utc"],
        )
        self.assertEqual(
            consumed_signal["source_prediction_at_utc"],
            source_signal["prediction_at_utc"],
        )
        self.assertEqual(
            consumed_signal["source_decision_at_utc"],
            source_signal["decision_at_utc"],
        )
        self.assertEqual(
            consumed_signal["source_valid_until_utc"],
            source_signal["valid_until_utc"],
        )
        self.assertEqual(
            parity["record"]["source_evaluation_at_utc"],
            source_record["evaluation_at_utc"],
        )
        self.assertEqual(
            parity["record"]["source_availability_at_utc"],
            source_record["availability_at_utc"],
        )

    def test_temporal_semantics_are_owned_by_tm020_and_compose_statically(self):
        package = _package()

        same_bar_invalid = _temporal(
            package,
            eligible_reference_at_utc="2026-08-23T15:09:59+00:00",
        )
        with self.assertRaises(ExternalSignalConsumerError):
            _consumer(
                package,
                temporal_evidence=same_bar_invalid,
            )

        equality_consumer = _consumer(
            package,
            temporal_evidence=_temporal(
                package,
                eligible_reference_at_utc=DECISION_BAR_END,
            ),
        )
        equality_parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=equality_consumer,
        )
        self.assertEqual(
            equality_parity["record"]["parity_state"],
            PARITY_STATE,
        )

        later_consumer = _consumer(
            package,
            temporal_evidence=_temporal(
                package,
                eligible_reference_at_utc=LATER_ELIGIBLE_AT,
            ),
        )
        later_parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=later_consumer,
        )
        self.assertEqual(
            later_parity["record"]["parity_state"],
            PARITY_STATE,
        )

        with self.assertRaises(ExternalSignalConsumerError):
            _consumer(
                package,
                consumer_evaluation_at_utc=(
                    "2026-08-23T16:00:01+00:00"
                ),
            )

        with self.assertRaises(ExternalSignalConsumerError):
            _consumer(
                package,
                consumer_evaluation_at_utc=CONSUMER_EVALUATION_AT,
                temporal_evidence=_temporal(
                    package,
                    eligible_reference_at_utc=(
                        "2026-08-23T15:31:00+00:00"
                    ),
                ),
            )

    def test_parity_schema_identity_and_checksum_tampering_fail_closed(self):
        package, consumer = _pair()
        parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )

        bad_schema = deepcopy(parity)
        bad_schema["record"]["schema_id"] = "OTHER"
        with self.assertRaises(ExternalSignalParityError):
            validate_external_signal_parity_evidence(
                bad_schema,
                package=package,
                consumer_evidence=consumer,
            )

        bad_version = deepcopy(parity)
        bad_version["record"]["schema_version"] = 2
        with self.assertRaises(ExternalSignalParityError):
            validate_external_signal_parity_evidence(
                bad_version,
                package=package,
                consumer_evidence=consumer,
            )

        bad_identity = deepcopy(parity)
        bad_identity["record"]["parity_id"] = (
            "external_signal_parity:" + ("0" * 64)
        )
        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "PARITY_IDENTITY_MISMATCH",
        ):
            validate_external_signal_parity_evidence(
                bad_identity,
                package=package,
                consumer_evidence=consumer,
            )

        bad_checksum = deepcopy(parity)
        bad_checksum["parity_sha256"] = "0" * 64
        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "PARITY_CHECKSUM_MISMATCH",
        ):
            validate_external_signal_parity_evidence(
                bad_checksum,
                package=package,
                consumer_evidence=consumer,
            )

    def test_rehashed_parity_crosslink_tampering_still_fails(self):
        package, consumer = _pair()
        parity = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=consumer,
        )

        package_tamper = deepcopy(parity)
        package_tamper["record"]["source_package_sha256"] = "0" * 64
        _rebind_parity_owned_integrity(package_tamper)

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "PARITY_RECORD_CROSSLINK_MISMATCH",
        ):
            validate_external_signal_parity_evidence(
                package_tamper,
                package=package,
                consumer_evidence=consumer,
            )

        consumer_tamper = deepcopy(parity)
        consumer_tamper["record"]["consumer_id"] = (
            "external_signal_consumer:" + ("0" * 64)
        )
        _rebind_parity_owned_integrity(consumer_tamper)

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "PARITY_RECORD_CROSSLINK_MISMATCH",
        ):
            validate_external_signal_parity_evidence(
                consumer_tamper,
                package=package,
                consumer_evidence=consumer,
            )

        signal_tamper = deepcopy(parity)
        signal_tamper["record"]["signal_ids"] = [
            "external_signal:" + ("0" * 64)
        ]
        _rebind_parity_owned_integrity(signal_tamper)

        with self.assertRaisesRegex(
            ExternalSignalParityError,
            "PARITY_RECORD_CROSSLINK_MISMATCH",
        ):
            validate_external_signal_parity_evidence(
                signal_tamper,
                package=package,
                consumer_evidence=consumer,
            )

    def test_material_consumer_evidence_changes_parity_identity_and_checksum(self):
        package = _package()

        first_consumer = _consumer(
            package,
            consumer_evaluation_at_utc=(
                "2026-08-23T15:30:00+00:00"
            ),
        )
        second_consumer = _consumer(
            package,
            consumer_evaluation_at_utc=(
                "2026-08-23T15:31:00+00:00"
            ),
        )

        first = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=first_consumer,
        )
        second = build_external_signal_parity_evidence(
            package=package,
            consumer_evidence=second_consumer,
        )

        self.assertNotEqual(
            first["record"]["parity_id"],
            second["record"]["parity_id"],
        )
        self.assertNotEqual(
            first["parity_sha256"],
            second["parity_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
