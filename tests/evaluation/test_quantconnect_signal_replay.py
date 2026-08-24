"""Focused tests for C4 TM-023 deterministic offline signal replay."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from quantitative_trading_research.execution.quantconnect_signal_consumer import (
    build_external_signal_consumption_evidence,
)
from quantitative_trading_research.execution.quantconnect_signal_producer import (
    build_external_signal_package,
)
from quantitative_trading_research.evaluation.quantconnect_signal_parity import (
    build_external_signal_parity_evidence,
)
from quantitative_trading_research.evaluation.quantconnect_signal_replay import (
    ALREADY_APPLIED,
    APPLIED,
    CHECKSUM_ALGORITHM,
    NOT_YET_ELIGIBLE,
    REPLAY_CLAIM,
    REPLAY_SCOPE,
    REPLAY_STATE,
    RESULT_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STALE_LATEST_SIGNAL,
    ExternalSignalReplayError,
    build_external_signal_replay_evidence,
    canonical_serialize_external_signal_replay_evidence,
    validate_external_signal_replay_evidence,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    ROOT
    / "src"
    / "quantitative_trading_research"
    / "evaluation"
    / "quantconnect_signal_replay.py"
)

PRODUCER_COMMIT = "a" * 40
MODEL_SHA = "b" * 64
ARTIFACT_SHA = "c" * 64


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _signal(
    *,
    instrument_id: str,
    canonical_instrument_id: str,
    signal: str,
    confidence: float | None,
    prediction_at_utc: str,
    decision_at_utc: str,
    valid_until_utc: str,
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


def _bundle(
    *,
    suffix: str,
    instrument: str = "AAA",
    signal: str = "BUY",
    confidence: float | None = 0.75,
    prediction_at_utc: str = "2026-08-23T15:00:00+00:00",
    decision_at_utc: str = "2026-08-23T15:01:00+00:00",
    publication_at_utc: str = "2026-08-23T15:02:00+00:00",
    availability_at_utc: str = "2026-08-23T15:03:00+00:00",
    source_evaluation_at_utc: str = "2026-08-23T15:04:00+00:00",
    decision_bar_end_at_utc: str = "2026-08-23T15:10:00+00:00",
    eligible_reference_at_utc: str = "2026-08-23T15:10:00+00:00",
    consumer_evaluation_at_utc: str = "2026-08-23T15:30:00+00:00",
    valid_until_utc: str = "2026-08-23T17:00:00+00:00",
    producer_identity: str | None = None,
    prediction_identity: str | None = None,
    prediction_sha256: str | None = None,
) -> dict:
    package = build_external_signal_package(
        producer_identity=(
            f"producer-{suffix}"
            if producer_identity is None
            else producer_identity
        ),
        producer_commit=PRODUCER_COMMIT,
        model_identity="model-a",
        model_sha256=MODEL_SHA,
        artifact_identity="artifact-a",
        artifact_sha256=ARTIFACT_SHA,
        prediction_identity=(
            f"prediction-{suffix}"
            if prediction_identity is None
            else prediction_identity
        ),
        prediction_sha256=(
            _sha(f"prediction-bytes-{suffix}")
            if prediction_sha256 is None
            else prediction_sha256
        ),
        signals=[
            _signal(
                instrument_id=instrument,
                canonical_instrument_id=instrument,
                signal=signal,
                confidence=confidence,
                prediction_at_utc=prediction_at_utc,
                decision_at_utc=decision_at_utc,
                valid_until_utc=valid_until_utc,
            )
        ],
        publication_at_utc=publication_at_utc,
        availability_at_utc=availability_at_utc,
        evaluation_at_utc=source_evaluation_at_utc,
    )

    consumer = build_external_signal_consumption_evidence(
        package=package,
        consumer_evaluation_at_utc=consumer_evaluation_at_utc,
        temporal_evidence=[
            {
                "signal_id": package["record"]["signals"][0]["signal_id"],
                "decision_bar_end_at_utc": decision_bar_end_at_utc,
                "eligible_reference_at_utc": eligible_reference_at_utc,
            }
        ],
    )

    parity = build_external_signal_parity_evidence(
        package=package,
        consumer_evidence=consumer,
    )

    return {
        "package": package,
        "consumer_evidence": consumer,
        "parity_evidence": parity,
    }


def _boundary(
    instrument: str,
    at_utc: str,
) -> dict:
    return {
        "canonical_instrument_id": instrument,
        "replay_boundary_at_utc": at_utc,
    }


def _selected_signal_id(bundle: dict) -> str:
    return bundle["consumer_evidence"]["record"]["signals"][0]["signal_id"]


def _rebind_replay_checksum(evidence: dict) -> dict:
    evidence["replay_sha256"] = hashlib.sha256(
        _canonical_json(evidence["record"]).encode("utf-8")
    ).hexdigest()
    return evidence


class QuantConnectSignalReplayTests(unittest.TestCase):
    def test_single_signal_explicit_boundary_semantics_and_idempotency(self):
        bundle = _bundle(suffix="single")

        evidence = build_external_signal_replay_evidence(
            evidence_bundles=[bundle],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:09:59+00:00"),
                _boundary("AAA", "2026-08-23T15:10:00+00:00"),
                _boundary("AAA", "2026-08-23T15:11:00+00:00"),
            ],
        )

        record = evidence["record"]
        states = [
            event["replay_event_state"]
            for event in record["replay_events"]
        ]

        self.assertEqual(
            states,
            [
                NOT_YET_ELIGIBLE,
                APPLIED,
                ALREADY_APPLIED,
            ],
        )
        self.assertFalse(
            record["replay_events"][0]["offline_application_recorded"]
        )
        self.assertTrue(
            record["replay_events"][1]["offline_application_recorded"]
        )
        self.assertFalse(
            record["replay_events"][2]["offline_application_recorded"]
        )

        self.assertEqual(record["schema_id"], SCHEMA_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["result_type"], RESULT_TYPE)
        self.assertEqual(record["replay_state"], REPLAY_STATE)
        self.assertEqual(record["replay_scope"], REPLAY_SCOPE)
        self.assertEqual(record["replay_claim"], REPLAY_CLAIM)
        self.assertEqual(evidence["checksum_algorithm"], CHECKSUM_ALGORITHM)

        metrics = record["metrics"]
        self.assertEqual(metrics["input_bundle_count"], 1)
        self.assertEqual(metrics["source_signal_count"], 1)
        self.assertEqual(metrics["replay_boundary_count"], 3)
        self.assertEqual(metrics["applied_event_count"], 1)
        self.assertEqual(metrics["not_yet_eligible_count"], 1)
        self.assertEqual(metrics["already_applied_count"], 1)
        self.assertEqual(metrics["stale_latest_count"], 0)

    def test_multiple_same_instrument_bundles_replay_newer_signal(self):
        older = _bundle(
            suffix="older",
            valid_until_utc="2026-08-23T17:00:00+00:00",
        )
        newer = _bundle(
            suffix="newer",
            prediction_at_utc="2026-08-23T15:20:00+00:00",
            decision_at_utc="2026-08-23T15:21:00+00:00",
            publication_at_utc="2026-08-23T15:22:00+00:00",
            availability_at_utc="2026-08-23T15:23:00+00:00",
            source_evaluation_at_utc="2026-08-23T15:24:00+00:00",
            decision_bar_end_at_utc="2026-08-23T15:30:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:30:00+00:00",
            consumer_evaluation_at_utc="2026-08-23T15:35:00+00:00",
            valid_until_utc="2026-08-23T17:00:00+00:00",
        )

        boundaries = [
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
            _boundary("AAA", "2026-08-23T15:20:00+00:00"),
            _boundary("AAA", "2026-08-23T15:30:00+00:00"),
            _boundary("AAA", "2026-08-23T15:31:00+00:00"),
        ]

        first = build_external_signal_replay_evidence(
            evidence_bundles=[older, newer],
            replay_boundaries=boundaries,
        )
        second = build_external_signal_replay_evidence(
            evidence_bundles=[newer, older],
            replay_boundaries=list(reversed(boundaries)),
        )

        self.assertEqual(first, second)

        events = first["record"]["replay_events"]
        self.assertEqual(
            [event["replay_event_state"] for event in events],
            [
                APPLIED,
                ALREADY_APPLIED,
                APPLIED,
                ALREADY_APPLIED,
            ],
        )
        self.assertEqual(
            events[0]["selected_signal_id"],
            _selected_signal_id(older),
        )
        self.assertEqual(
            events[1]["selected_signal_id"],
            _selected_signal_id(older),
        )
        self.assertEqual(
            events[2]["selected_signal_id"],
            _selected_signal_id(newer),
        )
        self.assertEqual(
            events[3]["selected_signal_id"],
            _selected_signal_id(newer),
        )

    def test_multi_instrument_order_is_canonical_and_input_order_independent(self):
        aaa = _bundle(suffix="aaa", instrument="AAA")
        bbb = _bundle(
            suffix="bbb",
            instrument="BBB",
            signal="SELL",
            confidence=0.40,
        )

        boundaries = [
            _boundary("BBB", "2026-08-23T15:10:00+00:00"),
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
        ]

        first = build_external_signal_replay_evidence(
            evidence_bundles=[bbb, aaa],
            replay_boundaries=boundaries,
        )
        second = build_external_signal_replay_evidence(
            evidence_bundles=[aaa, bbb],
            replay_boundaries=list(reversed(boundaries)),
        )

        self.assertEqual(first, second)
        self.assertEqual(
            [
                item["canonical_instrument_id"]
                for item in first["record"]["replay_boundaries"]
            ],
            ["AAA", "BBB"],
        )
        self.assertEqual(
            [
                item["canonical_instrument_id"]
                for item in first["record"]["replay_events"]
            ],
            ["AAA", "BBB"],
        )

    def test_repeat_construction_serialization_and_caller_immutability(self):
        bundle = _bundle(suffix="immutable")
        bundles = [bundle]
        boundaries = [
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
        ]

        original_bundles = deepcopy(bundles)
        original_boundaries = deepcopy(boundaries)

        first = build_external_signal_replay_evidence(
            evidence_bundles=bundles,
            replay_boundaries=boundaries,
        )
        second = build_external_signal_replay_evidence(
            evidence_bundles=deepcopy(bundles),
            replay_boundaries=deepcopy(boundaries),
        )

        self.assertEqual(first, second)
        self.assertEqual(bundles, original_bundles)
        self.assertEqual(boundaries, original_boundaries)
        self.assertEqual(
            canonical_serialize_external_signal_replay_evidence(
                first,
                evidence_bundles=bundles,
                replay_boundaries=boundaries,
            ),
            canonical_serialize_external_signal_replay_evidence(
                second,
                evidence_bundles=bundles,
                replay_boundaries=boundaries,
            ),
        )

    def test_invalid_upstream_parity_evidence_fails_closed(self):
        bundle = _bundle(suffix="invalid-upstream")
        bad = deepcopy(bundle)
        bad["parity_evidence"]["parity_sha256"] = "0" * 64

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "INVALID_UPSTREAM_PARITY_EVIDENCE",
        ):
            build_external_signal_replay_evidence(
                evidence_bundles=[bad],
                replay_boundaries=[
                    _boundary("AAA", "2026-08-23T15:10:00+00:00"),
                ],
            )

    def test_duplicate_bundle_and_signal_identity_fail_closed(self):
        bundle = _bundle(suffix="duplicate-bundle")

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "DUPLICATE_INPUT_EVIDENCE",
        ):
            build_external_signal_replay_evidence(
                evidence_bundles=[bundle, deepcopy(bundle)],
                replay_boundaries=[
                    _boundary("AAA", "2026-08-23T15:10:00+00:00"),
                ],
            )

        shared_prediction_sha = _sha("shared-prediction-bytes")

        first = _bundle(
            suffix="duplicate-signal-a",
            producer_identity="producer-a",
            prediction_identity="shared-prediction",
            prediction_sha256=shared_prediction_sha,
        )
        second = _bundle(
            suffix="duplicate-signal-b",
            producer_identity="producer-b",
            prediction_identity="shared-prediction",
            prediction_sha256=shared_prediction_sha,
        )

        self.assertNotEqual(
            first["package"]["record"]["package_id"],
            second["package"]["record"]["package_id"],
        )
        self.assertEqual(
            _selected_signal_id(first),
            _selected_signal_id(second),
        )

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "DUPLICATE_INPUT_EVIDENCE",
        ):
            build_external_signal_replay_evidence(
                evidence_bundles=[first, second],
                replay_boundaries=[
                    _boundary("AAA", "2026-08-23T15:10:00+00:00"),
                ],
            )

    def test_replay_boundary_contract_is_strict_and_exact(self):
        bundle = _bundle(suffix="boundary-contract")

        bad_cases = [
            [
                {
                    "canonical_instrument_id": "AAA",
                    "replay_boundary_at_utc": "2026-08-23T15:10:00+00:00",
                    "extra": "forbidden",
                }
            ],
            [
                {
                    "canonical_instrument_id": "AAA",
                    "replay_boundary_at_utc": "2026-08-23T15:10:00",
                }
            ],
            [
                {
                    "canonical_instrument_id": "AAA",
                    "replay_boundary_at_utc": "2026-08-23T11:10:00-04:00",
                }
            ],
            [
                {
                    "canonical_instrument_id": "AAA",
                    "replay_boundary_at_utc": 1,
                }
            ],
            [
                _boundary("aaa", "2026-08-23T15:10:00+00:00"),
            ],
        ]

        for candidate in bad_cases:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ExternalSignalReplayError):
                    build_external_signal_replay_evidence(
                        evidence_bundles=[bundle],
                        replay_boundaries=candidate,
                    )

        duplicate = [
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
        ]

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "DUPLICATE_REPLAY_BOUNDARY",
        ):
            build_external_signal_replay_evidence(
                evidence_bundles=[bundle],
                replay_boundaries=duplicate,
            )

    def test_ambiguous_equal_temporal_selection_key_fails_closed(self):
        first = _bundle(
            suffix="tie-a",
            prediction_identity="prediction-tie-a",
        )
        second = _bundle(
            suffix="tie-b",
            prediction_identity="prediction-tie-b",
        )

        self.assertNotEqual(
            _selected_signal_id(first),
            _selected_signal_id(second),
        )

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "AMBIGUOUS_TEMPORAL_SELECTION",
        ):
            build_external_signal_replay_evidence(
                evidence_bundles=[first, second],
                replay_boundaries=[
                    _boundary("AAA", "2026-08-23T15:10:00+00:00"),
                ],
            )

    def test_stale_latest_signal_does_not_fall_back_to_older_signal(self):
        older = _bundle(
            suffix="stale-old",
            valid_until_utc="2026-08-23T17:00:00+00:00",
        )
        newer = _bundle(
            suffix="stale-new",
            prediction_at_utc="2026-08-23T15:20:00+00:00",
            decision_at_utc="2026-08-23T15:21:00+00:00",
            publication_at_utc="2026-08-23T15:22:00+00:00",
            availability_at_utc="2026-08-23T15:23:00+00:00",
            source_evaluation_at_utc="2026-08-23T15:24:00+00:00",
            decision_bar_end_at_utc="2026-08-23T15:30:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:30:00+00:00",
            consumer_evaluation_at_utc="2026-08-23T15:31:00+00:00",
            valid_until_utc="2026-08-23T15:35:00+00:00",
        )

        evidence = build_external_signal_replay_evidence(
            evidence_bundles=[older, newer],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:40:00+00:00"),
            ],
        )

        event = evidence["record"]["replay_events"][0]

        self.assertEqual(
            event["replay_event_state"],
            STALE_LATEST_SIGNAL,
        )
        self.assertEqual(
            event["selected_signal_id"],
            _selected_signal_id(newer),
        )
        self.assertNotEqual(
            event["selected_signal_id"],
            _selected_signal_id(older),
        )
        self.assertFalse(event["offline_application_recorded"])

    def test_future_signal_does_not_look_ahead_over_latest_eligible_signal(self):
        older = _bundle(suffix="no-lookahead-old")
        newer = _bundle(
            suffix="no-lookahead-new",
            prediction_at_utc="2026-08-23T15:20:00+00:00",
            decision_at_utc="2026-08-23T15:21:00+00:00",
            publication_at_utc="2026-08-23T15:22:00+00:00",
            availability_at_utc="2026-08-23T15:23:00+00:00",
            source_evaluation_at_utc="2026-08-23T15:24:00+00:00",
            decision_bar_end_at_utc="2026-08-23T15:30:00+00:00",
            eligible_reference_at_utc="2026-08-23T15:30:00+00:00",
            consumer_evaluation_at_utc="2026-08-23T15:35:00+00:00",
        )

        evidence = build_external_signal_replay_evidence(
            evidence_bundles=[newer, older],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:20:00+00:00"),
            ],
        )

        event = evidence["record"]["replay_events"][0]
        self.assertEqual(event["replay_event_state"], APPLIED)
        self.assertEqual(
            event["selected_signal_id"],
            _selected_signal_id(older),
        )

    def test_result_tampering_and_nested_type_coercion_fail_closed(self):
        bundle = _bundle(suffix="tamper")
        boundaries = [
            _boundary("AAA", "2026-08-23T15:10:00+00:00"),
        ]

        evidence = build_external_signal_replay_evidence(
            evidence_bundles=[bundle],
            replay_boundaries=boundaries,
        )

        changed_id = deepcopy(evidence)
        changed_id["record"]["replay_id"] = (
            "external_signal_replay:" + ("0" * 64)
        )
        _rebind_replay_checksum(changed_id)

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "REPLAY_RECORD_CROSSLINK_MISMATCH",
        ):
            validate_external_signal_replay_evidence(
                changed_id,
                evidence_bundles=[bundle],
                replay_boundaries=boundaries,
            )

        type_coerced = deepcopy(evidence)
        self.assertEqual(
            type_coerced["record"]["metrics"]["applied_event_count"],
            1,
        )
        type_coerced["record"]["metrics"]["applied_event_count"] = True
        _rebind_replay_checksum(type_coerced)

        with self.assertRaisesRegex(
            ExternalSignalReplayError,
            "REPLAY_RECORD_CROSSLINK_MISMATCH",
        ):
            validate_external_signal_replay_evidence(
                type_coerced,
                evidence_bundles=[bundle],
                replay_boundaries=boundaries,
            )

    def test_material_replay_inputs_change_identity_and_checksum(self):
        bundle = _bundle(suffix="identity")

        first = build_external_signal_replay_evidence(
            evidence_bundles=[bundle],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:10:00+00:00"),
            ],
        )
        second = build_external_signal_replay_evidence(
            evidence_bundles=[bundle],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:11:00+00:00"),
            ],
        )

        self.assertNotEqual(
            first["record"]["replay_input_id"],
            second["record"]["replay_input_id"],
        )
        self.assertNotEqual(
            first["record"]["replay_id"],
            second["record"]["replay_id"],
        )
        self.assertNotEqual(
            first["replay_sha256"],
            second["replay_sha256"],
        )

    def test_result_contains_only_non_economic_replay_evidence(self):
        bundle = _bundle(suffix="non-economic")
        evidence = build_external_signal_replay_evidence(
            evidence_bundles=[bundle],
            replay_boundaries=[
                _boundary("AAA", "2026-08-23T15:10:00+00:00"),
            ],
        )

        prohibited = {
            "pnl",
            "returns",
            "sharpe",
            "drawdown",
            "portfolio_value",
            "commission",
            "spread",
            "slippage",
            "liquidity",
            "fill_count",
            "target_weight",
            "action",
            "position",
            "quantity",
            "cash",
            "order",
            "fill",
        }

        record = evidence["record"]

        self.assertTrue(prohibited.isdisjoint(record))
        self.assertTrue(prohibited.isdisjoint(record["metrics"]))

        for event in record["replay_events"]:
            self.assertTrue(prohibited.isdisjoint(event))

    def test_static_boundary_attribution_and_public_tm021_reuse(self):
        source = SOURCE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)

        observed_roots: set[str] = set()
        parity_imports: set[str] = set()

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
                    == "quantitative_trading_research.evaluation."
                    "quantconnect_signal_parity"
                ):
                    parity_imports.update(
                        alias.name for alias in node.names
                    )

        allowed_roots = {
            "__future__",
            "copy",
            "datetime",
            "hashlib",
            "hmac",
            "json",
            "typing",
            "quantitative_trading_research",
        }

        self.assertLessEqual(observed_roots, allowed_roots)
        self.assertEqual(
            parity_imports,
            {
                "ExternalSignalParityError",
                "validate_external_signal_parity_evidence",
            },
        )
        self.assertFalse(
            any(name.startswith("_") for name in parity_imports)
        )

        self.assertIn("racoope70/ppo-trading-pipeline", source)
        self.assertIn(
            "072103f43d8b2488c3efca183f637ab0508a193a",
            source,
        )
        self.assertIn(
            "quantconnect/lean_unh_xom_dynamic_signal_backtest.py",
            source,
        )

        prohibited_tokens = (
            "AlgorithmImports",
            "QCAlgorithm",
            "self.object_store",
            "self.time",
            "set_holdings(",
            "SetHoldings(",
            "target_weight",
            "market_order(",
            "limit_order(",
            "submit_order(",
            "requests.",
            "urllib.",
            "socket.",
            "os.environ",
            "os.getenv(",
            "datetime.now(",
            "datetime.utcnow(",
            "time.time(",
            "open(",
            "read_text(",
            "write_text(",
            "model.predict(",
            ".fit(",
        )

        for token in prohibited_tokens:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
