"""Focused tests for the C4 TM-019 broker-neutral external-signal producer."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from quantitative_trading_research.execution.quantconnect_signal_producer import (
    CHECKSUM_ALGORITHM,
    PACKAGE_TYPE,
    PUBLICATION_EVIDENCE_STATUS,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STORAGE_REQUIREMENT_STATUS,
    ExternalSignalPackageError,
    build_external_signal_package,
    canonical_serialize_external_signal_package,
    validate_external_signal_package,
)


PREDICTION_AT = "2026-08-23T15:00:00+00:00"
DECISION_AT = "2026-08-23T15:01:00+00:00"
PUBLICATION_AT = "2026-08-23T15:02:00+00:00"
AVAILABILITY_AT = "2026-08-23T15:03:00+00:00"
EVALUATION_AT = "2026-08-23T15:04:00+00:00"
VALID_UNTIL = "2026-08-23T16:00:00+00:00"

PRODUCER_COMMIT = "a" * 40
MODEL_SHA = "b" * 64
ARTIFACT_SHA = "c" * 64
PREDICTION_SHA = "d" * 64


def _signal(
    *,
    instrument_id: str = "AAA",
    canonical_instrument_id: str = "AAA",
    signal: str = "BUY",
    prediction_at_utc: str = PREDICTION_AT,
    decision_at_utc: str = DECISION_AT,
    valid_until_utc: str = VALID_UNTIL,
    confidence: float | None = 0.75,
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


def _kwargs(
    *,
    signals: list[dict] | None = None,
    aliases: list[dict[str, str]] | None = None,
    evaluation_at_utc: str = EVALUATION_AT,
) -> dict:
    return {
        "producer_identity": "producer-source-a",
        "producer_commit": PRODUCER_COMMIT,
        "model_identity": "model-a",
        "model_sha256": MODEL_SHA,
        "artifact_identity": "artifact-a",
        "artifact_sha256": ARTIFACT_SHA,
        "prediction_identity": "prediction-a",
        "prediction_sha256": PREDICTION_SHA,
        "signals": [_signal()] if signals is None else signals,
        "publication_at_utc": PUBLICATION_AT,
        "availability_at_utc": AVAILABILITY_AT,
        "evaluation_at_utc": evaluation_at_utc,
        "aliases": aliases,
    }


def _package(**overrides) -> dict:
    values = _kwargs()
    values.update(overrides)
    return build_external_signal_package(**values)


class QuantConnectSignalProducerTests(unittest.TestCase):
    def test_valid_single_signal_construction_is_versioned_and_nonoperational(self):
        package = _package()
        record = package["record"]

        self.assertEqual(record["schema_id"], SCHEMA_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["package_type"], PACKAGE_TYPE)
        self.assertEqual(package["checksum_algorithm"], CHECKSUM_ALGORITHM)
        self.assertEqual(
            record["storage_requirement_status"],
            STORAGE_REQUIREMENT_STATUS,
        )
        self.assertEqual(
            record["publication_evidence_status"],
            PUBLICATION_EVIDENCE_STATUS,
        )
        self.assertFalse(record["authenticated_storage_completed"])
        self.assertFalse(record["remote_publication_completed"])
        self.assertFalse(record["provider_publication_completed"])
        self.assertEqual(len(record["signals"]), 1)
        validate_external_signal_package(package, evaluation_at_utc=EVALUATION_AT)

    def test_valid_multi_signal_construction_uses_canonical_signal_order(self):
        package = _package(
            signals=[
                _signal(
                    instrument_id="ZZZ",
                    canonical_instrument_id="ZZZ",
                    signal="SELL",
                ),
                _signal(
                    instrument_id="AAA",
                    canonical_instrument_id="AAA",
                    signal="BUY",
                ),
            ]
        )
        self.assertEqual(
            [
                item["canonical_instrument_id"]
                for item in package["record"]["signals"]
            ],
            ["AAA", "ZZZ"],
        )

    def test_repeat_construction_and_canonical_serialization_are_deterministic(self):
        first = _package()
        second = _package()

        self.assertEqual(first, second)
        self.assertEqual(
            first["record"]["signals"][0]["signal_id"],
            second["record"]["signals"][0]["signal_id"],
        )
        self.assertEqual(first["record"]["run_id"], second["record"]["run_id"])
        self.assertEqual(
            first["record"]["package_id"],
            second["record"]["package_id"],
        )
        self.assertEqual(first["package_sha256"], second["package_sha256"])
        self.assertEqual(
            canonical_serialize_external_signal_package(
                first, evaluation_at_utc=EVALUATION_AT
            ),
            canonical_serialize_external_signal_package(
                second, evaluation_at_utc=EVALUATION_AT
            ),
        )

    def test_caller_dictionary_order_does_not_affect_result(self):
        original = _signal()
        reversed_order = dict(reversed(list(original.items())))

        first = _package(signals=[original])
        second = _package(signals=[reversed_order])

        self.assertEqual(first, second)

    def test_provenance_and_prediction_identity_are_bound(self):
        package = _package()
        record = package["record"]

        self.assertEqual(record["producer_identity"], "producer-source-a")
        self.assertEqual(record["producer_commit"], PRODUCER_COMMIT)
        self.assertEqual(record["model_identity"], "model-a")
        self.assertEqual(record["model_sha256"], MODEL_SHA)
        self.assertEqual(record["artifact_identity"], "artifact-a")
        self.assertEqual(record["artifact_sha256"], ARTIFACT_SHA)
        self.assertEqual(record["prediction_identity"], "prediction-a")
        self.assertEqual(record["prediction_sha256"], PREDICTION_SHA)

        changed = _package(prediction_identity="prediction-b")
        self.assertNotEqual(record["run_id"], changed["record"]["run_id"])
        self.assertNotEqual(record["package_id"], changed["record"]["package_id"])
        self.assertNotEqual(package["package_sha256"], changed["package_sha256"])
        self.assertNotEqual(
            record["signals"][0]["signal_id"],
            changed["record"]["signals"][0]["signal_id"],
        )

    def test_missing_or_malformed_provenance_identity_fails_closed(self):
        cases = (
            ("producer_identity", ""),
            ("producer_commit", "a" * 39),
            ("model_identity", ""),
            ("model_sha256", "b" * 63),
            ("artifact_identity", ""),
            ("artifact_sha256", "c" * 63),
            ("prediction_identity", ""),
            ("prediction_sha256", "d" * 63),
        )
        for field, value in cases:
            with self.subTest(field=field):
                kwargs = _kwargs()
                kwargs[field] = value
                with self.assertRaises(ExternalSignalPackageError):
                    build_external_signal_package(**kwargs)

    def test_strict_schema_missing_unexpected_wrong_type_and_checksum_rejection(self):
        package = _package()

        bad_schema = deepcopy(package)
        bad_schema["record"]["schema_id"] = "OTHER"
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                bad_schema, evaluation_at_utc=EVALUATION_AT
            )

        bad_version = deepcopy(package)
        bad_version["record"]["schema_version"] = True
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                bad_version, evaluation_at_utc=EVALUATION_AT
            )

        missing = deepcopy(package)
        del missing["record"]["model_identity"]
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                missing, evaluation_at_utc=EVALUATION_AT
            )

        unexpected = deepcopy(package)
        unexpected["record"]["provider_response"] = {}
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                unexpected, evaluation_at_utc=EVALUATION_AT
            )

        malformed_checksum = deepcopy(package)
        malformed_checksum["package_sha256"] = "not-a-sha"
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                malformed_checksum, evaluation_at_utc=EVALUATION_AT
            )

    def test_checksum_and_identity_tampering_fail_closed(self):
        package = _package()

        checksum_tampered = deepcopy(package)
        checksum_tampered["record"]["producer_identity"] = "producer-source-b"
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                checksum_tampered, evaluation_at_utc=EVALUATION_AT
            )

        signal_identity_tampered = deepcopy(package)
        signal_identity_tampered["record"]["signals"][0][
            "signal_id"
        ] = "external_signal:" + ("0" * 64)
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                signal_identity_tampered, evaluation_at_utc=EVALUATION_AT
            )

        run_identity_tampered = deepcopy(package)
        run_identity_tampered["record"]["run_id"] = "external_signal_run:" + (
            "0" * 64
        )
        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                run_identity_tampered, evaluation_at_utc=EVALUATION_AT
            )

    def test_empty_signal_collection_and_unsupported_signal_fail_closed(self):
        with self.assertRaises(ExternalSignalPackageError):
            _package(signals=[])

        with self.assertRaises(ExternalSignalPackageError):
            _package(signals=[_signal(signal="STRONG_BUY")])

    def test_confidence_requires_one_canonical_float_representation(self):
        with self.assertRaises(ExternalSignalPackageError):
            _package(signals=[_signal(confidence=1)])

        accepted = _package(signals=[_signal(confidence=1.0)])
        self.assertEqual(accepted["record"]["signals"][0]["confidence"], 1.0)
        self.assertIs(
            type(accepted["record"]["signals"][0]["confidence"]),
            float,
        )

        with self.assertRaises(ExternalSignalPackageError):
            _package(signals=[_signal(confidence=True)])

        for value in (
            float("nan"),
            float("inf"),
            float("-inf"),
            -0.01,
            1.01,
        ):
            with self.subTest(value=value):
                with self.assertRaises(ExternalSignalPackageError):
                    _package(signals=[_signal(confidence=value)])

    def test_explicit_canonical_instrument_and_alias_policy(self):
        package = _package(
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
        self.assertEqual(
            package["record"]["signals"][0]["canonical_instrument_id"],
            "BRK-B",
        )
        self.assertEqual(
            package["record"]["alias_policy"],
            [{"alias": "BRK.B", "canonical_instrument_id": "BRK-B"}],
        )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(
                        instrument_id="BRK.B",
                        canonical_instrument_id="BRK-B",
                    )
                ],
                aliases=None,
            )

    def test_alias_policy_is_deterministic_and_identity_bound(self):
        first = _package(
            signals=[
                _signal(
                    instrument_id="B.ALIAS",
                    canonical_instrument_id="BBB",
                ),
                _signal(
                    instrument_id="A.ALIAS",
                    canonical_instrument_id="AAA",
                ),
            ],
            aliases=[
                {
                    "alias": "B.ALIAS",
                    "canonical_instrument_id": "BBB",
                },
                {
                    "alias": "A.ALIAS",
                    "canonical_instrument_id": "AAA",
                },
            ],
        )
        second = _package(
            signals=[
                _signal(
                    instrument_id="A.ALIAS",
                    canonical_instrument_id="AAA",
                ),
                _signal(
                    instrument_id="B.ALIAS",
                    canonical_instrument_id="BBB",
                ),
            ],
            aliases=[
                {
                    "alias": "A.ALIAS",
                    "canonical_instrument_id": "AAA",
                },
                {
                    "alias": "B.ALIAS",
                    "canonical_instrument_id": "BBB",
                },
            ],
        )
        self.assertEqual(first, second)

        canonical_only = _package(
            signals=[
                _signal(
                    instrument_id="AAA",
                    canonical_instrument_id="AAA",
                ),
                _signal(
                    instrument_id="BBB",
                    canonical_instrument_id="BBB",
                ),
            ],
            aliases=None,
        )
        self.assertNotEqual(
            first["record"]["run_id"],
            canonical_only["record"]["run_id"],
        )
        self.assertNotEqual(
            first["package_sha256"],
            canonical_only["package_sha256"],
        )

    def test_ambiguous_malformed_and_duplicate_alias_cases_fail_closed(self):
        signal = _signal(
            instrument_id="ALIAS",
            canonical_instrument_id="AAA",
        )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[signal],
                aliases=[
                    {"alias": "ALIAS", "canonical_instrument_id": "AAA"},
                    {"alias": "ALIAS", "canonical_instrument_id": "BBB"},
                ],
            )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[_signal()],
                aliases=[
                    {"alias": "AAA", "canonical_instrument_id": "AAA"},
                ],
            )

    def test_duplicate_canonical_and_duplicate_after_alias_resolution_fail_closed(self):
        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(instrument_id="AAA", canonical_instrument_id="AAA"),
                    _signal(
                        instrument_id="AAA.ALIAS",
                        canonical_instrument_id="AAA",
                    ),
                ],
                aliases=[
                    {
                        "alias": "AAA.ALIAS",
                        "canonical_instrument_id": "AAA",
                    }
                ],
            )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(instrument_id="AAA", canonical_instrument_id="AAA"),
                    _signal(
                        instrument_id="OTHER",
                        canonical_instrument_id="AAA",
                    ),
                ],
                aliases=[
                    {"alias": "OTHER", "canonical_instrument_id": "AAA"},
                ],
            )

    def test_temporal_evidence_is_retained_canonical_and_auditable(self):
        package = _package(evaluation_at_utc="2026-08-23T15:04:00Z")
        record = package["record"]
        signal = record["signals"][0]

        self.assertEqual(
            record["evaluation_at_utc"],
            "2026-08-23T15:04:00+00:00",
        )
        self.assertEqual(signal["prediction_at_utc"], PREDICTION_AT)
        self.assertEqual(signal["decision_at_utc"], DECISION_AT)
        self.assertEqual(signal["valid_until_utc"], VALID_UNTIL)
        self.assertEqual(record["publication_at_utc"], PUBLICATION_AT)
        self.assertEqual(record["availability_at_utc"], AVAILABILITY_AT)

    def test_changing_only_evaluation_time_changes_identity_and_checksum(self):
        first = _package(evaluation_at_utc="2026-08-23T15:04:00+00:00")
        second = _package(evaluation_at_utc="2026-08-23T15:05:00+00:00")

        self.assertNotEqual(first["record"]["run_id"], second["record"]["run_id"])
        self.assertNotEqual(
            first["record"]["package_id"],
            second["record"]["package_id"],
        )
        self.assertNotEqual(first["package_sha256"], second["package_sha256"])

        with self.assertRaises(ExternalSignalPackageError):
            validate_external_signal_package(
                first,
                evaluation_at_utc="2026-08-23T15:05:00+00:00",
            )

    def test_temporal_ordering_and_equality_at_valid_until(self):
        valid = _package(evaluation_at_utc=VALID_UNTIL)
        validate_external_signal_package(valid, evaluation_at_utc=VALID_UNTIL)

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(
                        prediction_at_utc="2026-08-23T15:01:30+00:00",
                        decision_at_utc="2026-08-23T15:01:00+00:00",
                    )
                ]
            )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(
                        decision_at_utc="2026-08-23T15:02:30+00:00"
                    )
                ]
            )

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(
                        valid_until_utc="2026-08-23T15:02:30+00:00"
                    )
                ]
            )

    def test_stale_and_mixed_freshness_packages_fail_closed(self):
        with self.assertRaises(ExternalSignalPackageError):
            _package(evaluation_at_utc="2026-08-23T16:00:01+00:00")

        with self.assertRaises(ExternalSignalPackageError):
            _package(
                signals=[
                    _signal(
                        instrument_id="AAA",
                        canonical_instrument_id="AAA",
                        valid_until_utc="2026-08-23T15:03:30+00:00",
                    ),
                    _signal(
                        instrument_id="BBB",
                        canonical_instrument_id="BBB",
                        valid_until_utc="2026-08-23T16:00:00+00:00",
                    ),
                ]
            )

    def test_future_event_evidence_relative_to_evaluation_fails_closed(self):
        cases = (
            {
                "signals": [
                    _signal(
                        prediction_at_utc="2026-08-23T15:00:00+00:00",
                        decision_at_utc="2026-08-23T15:01:00+00:00",
                    )
                ],
                "evaluation_at_utc": "2026-08-23T14:59:59+00:00",
            },
            {
                "signals": [_signal()],
                "evaluation_at_utc": "2026-08-23T15:00:30+00:00",
            },
            {
                "signals": [_signal()],
                "evaluation_at_utc": "2026-08-23T15:01:30+00:00",
            },
            {
                "signals": [_signal()],
                "evaluation_at_utc": "2026-08-23T15:02:30+00:00",
            },
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ExternalSignalPackageError):
                    _package(**case)

    def test_naive_and_non_utc_timestamps_fail_closed(self):
        for field in (
            "prediction_at_utc",
            "decision_at_utc",
            "valid_until_utc",
        ):
            with self.subTest(field=field, kind="naive"):
                signal = _signal()
                signal[field] = "2026-08-23T15:00:00"
                with self.assertRaises(ExternalSignalPackageError):
                    _package(signals=[signal])

            with self.subTest(field=field, kind="non_utc"):
                signal = _signal()
                signal[field] = "2026-08-23T15:00:00-04:00"
                with self.assertRaises(ExternalSignalPackageError):
                    _package(signals=[signal])

        for field in (
            "publication_at_utc",
            "availability_at_utc",
            "evaluation_at_utc",
        ):
            with self.subTest(field=field, kind="naive"):
                kwargs = _kwargs()
                kwargs[field] = "2026-08-23T15:00:00"
                with self.assertRaises(ExternalSignalPackageError):
                    build_external_signal_package(**kwargs)

            with self.subTest(field=field, kind="non_utc"):
                kwargs = _kwargs()
                kwargs[field] = "2026-08-23T15:00:00-04:00"
                with self.assertRaises(ExternalSignalPackageError):
                    build_external_signal_package(**kwargs)

    def test_builder_does_not_mutate_caller_owned_inputs(self):
        signals = [
            _signal(
                instrument_id="ALIAS",
                canonical_instrument_id="AAA",
            )
        ]
        aliases = [{"alias": "ALIAS", "canonical_instrument_id": "AAA"}]
        original_signals = deepcopy(signals)
        original_aliases = deepcopy(aliases)

        _package(signals=signals, aliases=aliases)

        self.assertEqual(signals, original_signals)
        self.assertEqual(aliases, original_aliases)

    def test_static_boundary_is_offline_nonoperational_and_dependency_neutral(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "quantconnect_signal_producer.py"
        )
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        allowed_import_roots = {
            "__future__",
            "copy",
            "datetime",
            "hashlib",
            "hmac",
            "json",
            "math",
            "typing",
        }
        observed_roots: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                observed_roots.update(
                    alias.name.split(".")[0] for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                observed_roots.add(node.module.split(".")[0])

        self.assertLessEqual(observed_roots, allowed_import_roots)

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
            "gist",
            "GITHUB_TOKEN",
            "GIST_ID",
            "submit_order(",
            "submit_market_order",
            "get_account(",
            "get_all_positions(",
            "get_orders(",
            "predict_symbols(",
            "model.predict(",
            "fit(",
            "read_csv(",
            "to_csv(",
            "write_text(",
            "write_bytes(",
            "open(",
        )
        for token in prohibited_tokens:
            self.assertNotIn(token, source)

    def test_historical_attribution_and_residual_boundary_are_explicit(self):
        source_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "quantitative_trading_research"
            / "execution"
            / "quantconnect_signal_producer.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertIn("racoope70/ppo-trading-pipeline", source)
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source,
        )
        self.assertIn("src/adapters/quantconnect.py", source)

        package = _package()
        record = package["record"]
        prohibited_execution_fields = {
            "portfolio_weight",
            "target_weight",
            "position",
            "quantity",
            "order",
            "submission_authorized",
            "execution_authorized",
            "risk_approved",
            "broker_target",
        }
        self.assertTrue(
            prohibited_execution_fields.isdisjoint(record.keys())
        )
        for signal in record["signals"]:
            self.assertTrue(
                prohibited_execution_fields.isdisjoint(signal.keys())
            )


if __name__ == "__main__":
    unittest.main()
