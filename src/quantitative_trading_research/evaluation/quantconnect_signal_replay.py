"""Pure deterministic offline external-signal replay and temporal-guard harness.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``quantconnect/lean_unh_xom_dynamic_signal_backtest.py``.

The historical source depended on QuantConnect/LEAN runtime state, Object Store,
platform clocks, holdings mutation, and trading-policy sizing. None of that
operational behavior is carried forward. This C4 component accepts complete
caller-supplied TM-019/TM-020/TM-021 evidence bundles plus explicit replay
boundaries and emits only deterministic offline replay evidence.

A PASS result means only that the supplied validated offline signal evidence
was replayed according to the explicit temporal contract. It does not establish
an actual market next bar, exchange-calendar correctness, order execution,
fills, portfolio performance, broker readiness, model quality, profitability,
promotion, or paper/live trading readiness.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import hmac
import json
from typing import Any

from quantitative_trading_research.evaluation.quantconnect_signal_parity import (
    ExternalSignalParityError,
    validate_external_signal_parity_evidence,
)


SCHEMA_ID = "C4_OFFLINE_EXTERNAL_SIGNAL_REPLAY_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_external_signal_replay_evidence"
REPLAY_STATE = "PASS"
REPLAY_SCOPE = "OFFLINE_EXPLICIT_REFERENCE_BOUNDARY_ONLY"
REPLAY_CLAIM = (
    "THE_SUPPLIED_VALIDATED_OFFLINE_SIGNAL_EVIDENCE_WAS_REPLAYED_"
    "ACCORDING_TO_THE_EXPLICIT_TEMPORAL_CONTRACT"
)
CHECKSUM_ALGORITHM = "sha256"

APPLIED = "APPLIED"
NOT_YET_ELIGIBLE = "NOT_YET_ELIGIBLE"
STALE_LATEST_SIGNAL = "STALE_LATEST_SIGNAL"
ALREADY_APPLIED = "ALREADY_APPLIED"
REPLAY_EVENT_STATES = (
    APPLIED,
    NOT_YET_ELIGIBLE,
    STALE_LATEST_SIGNAL,
    ALREADY_APPLIED,
)

_RESULT_KEYS = {
    "record",
    "checksum_algorithm",
    "replay_sha256",
}

_RECORD_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "replay_state",
    "replay_scope",
    "replay_claim",
    "replay_id",
    "replay_input_id",
    "source_evidence_bundles",
    "signal_ids",
    "replay_boundaries",
    "replay_events",
    "metrics",
}

_BUNDLE_INPUT_KEYS = {
    "package",
    "consumer_evidence",
    "parity_evidence",
}

_BUNDLE_RECORD_KEYS = {
    "bundle_id",
    "source_package_id",
    "source_package_sha256",
    "consumer_id",
    "consumer_sha256",
    "parity_id",
    "parity_sha256",
    "signal_ids",
}

_BOUNDARY_INPUT_KEYS = {
    "canonical_instrument_id",
    "replay_boundary_at_utc",
}

_BOUNDARY_RECORD_KEYS = {
    "boundary_id",
    "canonical_instrument_id",
    "replay_boundary_at_utc",
}

_EVENT_KEYS = {
    "boundary_id",
    "canonical_instrument_id",
    "replay_boundary_at_utc",
    "selected_signal_id",
    "selected_source_decision_at_utc",
    "selected_eligible_reference_at_utc",
    "selected_valid_until_utc",
    "replay_event_state",
    "offline_application_recorded",
}

_METRIC_KEYS = {
    "input_bundle_count",
    "source_signal_count",
    "replay_boundary_count",
    "applied_event_count",
    "not_yet_eligible_count",
    "stale_latest_count",
    "already_applied_count",
    "first_replay_boundary_at_utc",
    "last_replay_boundary_at_utc",
}


class ExternalSignalReplayError(ValueError):
    """Fail-closed error for malformed or contradictory TM-023 replay evidence."""


def _fail(code: str, detail: str = "") -> None:
    message = code if not detail else f"{code}: {detail}"
    raise ExternalSignalReplayError(message)


def _mapping(name: str, value: Any) -> dict[str, Any]:
    if type(value) is not dict:
        _fail("WRONG_TYPE", f"{name} must be a dict")
    return deepcopy(value)


def _keys(
    name: str,
    value: dict[str, Any],
    expected: set[str],
) -> None:
    if set(value) != expected:
        _fail(
            "UNEXPECTED_FIELD",
            f"{name} keys mismatch: "
            f"missing={sorted(expected - set(value))}; "
            f"unexpected={sorted(set(value) - expected)}",
        )


def _text(name: str, value: Any) -> str:
    if (
        type(value) is not str
        or not value
        or value != value.strip()
    ):
        _fail(
            "WRONG_TYPE",
            f"{name} must be a non-empty string without surrounding whitespace",
        )
    return value


def _sha(name: str, value: Any) -> str:
    text = _text(name, value)

    if len(text) != 64 or any(
        character not in "0123456789abcdef"
        for character in text
    ):
        _fail(
            "WRONG_TYPE",
            f"{name} must be lowercase 64-character SHA-256 hex",
        )

    return text


def _utc(name: str, value: Any) -> datetime:
    text = _text(name, value)

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ExternalSignalReplayError(
            f"INVALID_TIMESTAMP: "
            f"{name} must be canonical ISO-8601 UTC"
        ) from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail(
            "INVALID_TIMESTAMP",
            f"{name} must be timezone-aware UTC",
        )

    if parsed.utcoffset().total_seconds() != 0:
        _fail(
            "INVALID_TIMESTAMP",
            f"{name} must be expressed in UTC",
        )

    canonical = parsed.astimezone(timezone.utc).isoformat()

    if canonical != text:
        _fail(
            "NONCANONICAL_TIMESTAMP",
            f"{name} must use canonical UTC representation",
        )

    return parsed.astimezone(timezone.utc)


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
        raise ExternalSignalReplayError(
            "NONCANONICAL_EVIDENCE: "
            "replay evidence is not canonically serializable"
        ) from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _identity(prefix: str, value: Any) -> str:
    return f"{prefix}:{_digest(value)}"


def _exact_equal(actual: Any, expected: Any) -> bool:
    """Compare replay-owned evidence with exact recursive Python types."""

    if type(actual) is not type(expected):
        return False

    if type(expected) is dict:
        if set(actual) != set(expected):
            return False
        return all(
            _exact_equal(actual[key], expected[key])
            for key in expected
        )

    if type(expected) is list:
        if len(actual) != len(expected):
            return False
        return all(
            _exact_equal(actual_item, expected_item)
            for actual_item, expected_item in zip(actual, expected)
        )

    return actual == expected


def _validated_bundle_inputs(
    evidence_bundles: Any,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    if (
        type(evidence_bundles) is not list
        or not evidence_bundles
    ):
        _fail(
            "INVALID_BUNDLE_COLLECTION",
            "evidence_bundles must be a non-empty list",
        )

    bundle_records: list[dict[str, Any]] = []
    replay_signals: list[dict[str, Any]] = []

    seen_package_ids: set[str] = set()
    seen_consumer_ids: set[str] = set()
    seen_parity_ids: set[str] = set()
    seen_bundle_ids: set[str] = set()
    seen_signal_ids: set[str] = set()

    for index, raw in enumerate(
        deepcopy(evidence_bundles)
    ):
        bundle = _mapping(
            f"evidence_bundles[{index}]",
            raw,
        )
        _keys(
            f"evidence_bundles[{index}]",
            bundle,
            _BUNDLE_INPUT_KEYS,
        )

        package = _mapping(
            f"evidence_bundles[{index}].package",
            bundle["package"],
        )
        consumer = _mapping(
            f"evidence_bundles[{index}].consumer_evidence",
            bundle["consumer_evidence"],
        )
        parity = _mapping(
            f"evidence_bundles[{index}].parity_evidence",
            bundle["parity_evidence"],
        )

        try:
            validate_external_signal_parity_evidence(
                parity,
                package=package,
                consumer_evidence=consumer,
            )
        except ExternalSignalParityError as exc:
            raise ExternalSignalReplayError(
                "INVALID_UPSTREAM_PARITY_EVIDENCE: "
                f"bundle[{index}]: {exc}"
            ) from exc

        source_record = package["record"]
        consumer_record = consumer["record"]
        parity_record = parity["record"]

        source_package_id = source_record["package_id"]
        consumer_id = consumer_record["consumer_id"]
        parity_id = parity_record["parity_id"]

        if source_package_id in seen_package_ids:
            _fail(
                "DUPLICATE_INPUT_EVIDENCE",
                f"duplicate source_package_id: "
                f"{source_package_id}",
            )

        if consumer_id in seen_consumer_ids:
            _fail(
                "DUPLICATE_INPUT_EVIDENCE",
                f"duplicate consumer_id: "
                f"{consumer_id}",
            )

        if parity_id in seen_parity_ids:
            _fail(
                "DUPLICATE_INPUT_EVIDENCE",
                f"duplicate parity_id: "
                f"{parity_id}",
            )

        seen_package_ids.add(source_package_id)
        seen_consumer_ids.add(consumer_id)
        seen_parity_ids.add(parity_id)

        signal_ids = list(
            parity_record["signal_ids"]
        )

        bundle_payload = {
            "source_package_id":
                source_package_id,
            "source_package_sha256":
                package["package_sha256"],
            "consumer_id":
                consumer_id,
            "consumer_sha256":
                consumer["consumer_sha256"],
            "parity_id":
                parity_id,
            "parity_sha256":
                parity["parity_sha256"],
            "signal_ids":
                signal_ids,
        }

        bundle_id = _identity(
            "external_signal_replay_bundle",
            bundle_payload,
        )

        if bundle_id in seen_bundle_ids:
            _fail(
                "DUPLICATE_INPUT_EVIDENCE",
                f"duplicate bundle_id: "
                f"{bundle_id}",
            )

        seen_bundle_ids.add(bundle_id)

        bundle_record = {
            "bundle_id": bundle_id,
            **bundle_payload,
        }

        _keys(
            f"source_evidence_bundles[{index}]",
            bundle_record,
            _BUNDLE_RECORD_KEYS,
        )

        bundle_records.append(
            bundle_record
        )

        for signal_index, signal in enumerate(
            consumer_record["signals"]
        ):
            signal_id = signal["signal_id"]

            if signal_id in seen_signal_ids:
                _fail(
                    "DUPLICATE_INPUT_EVIDENCE",
                    "duplicate immutable signal_id: "
                    f"{signal_id}",
                )

            seen_signal_ids.add(
                signal_id
            )

            replay_signal = {
                "signal_id":
                    signal_id,
                "instrument_id":
                    signal["instrument_id"],
                "canonical_instrument_id":
                    signal[
                        "canonical_instrument_id"
                    ],
                "signal":
                    signal["signal"],
                "confidence":
                    signal["confidence"],
                "source_decision_at_utc":
                    signal[
                        "source_decision_at_utc"
                    ],
                "source_valid_until_utc":
                    signal[
                        "source_valid_until_utc"
                    ],
                "decision_bar_end_at_utc":
                    signal[
                        "decision_bar_end_at_utc"
                    ],
                "eligible_reference_at_utc":
                    signal[
                        "eligible_reference_at_utc"
                    ],
            }

            for field in (
                "source_decision_at_utc",
                "source_valid_until_utc",
                "decision_bar_end_at_utc",
                "eligible_reference_at_utc",
            ):
                _utc(
                    "evidence_bundles"
                    f"[{index}].signals"
                    f"[{signal_index}].{field}",
                    replay_signal[field],
                )

            replay_signals.append(
                replay_signal
            )

    bundle_records.sort(
        key=lambda item: item["bundle_id"]
    )

    replay_signals.sort(
        key=lambda item: (
            item["canonical_instrument_id"],
            _utc(
                "signal."
                "eligible_reference_at_utc",
                item[
                    "eligible_reference_at_utc"
                ],
            ),
            _utc(
                "signal."
                "source_decision_at_utc",
                item[
                    "source_decision_at_utc"
                ],
            ),
            item["signal_id"],
        )
    )

    selection_keys: dict[
        tuple[str, str, str],
        str,
    ] = {}

    for signal in replay_signals:
        selection_key = (
            signal[
                "canonical_instrument_id"
            ],
            signal[
                "eligible_reference_at_utc"
            ],
            signal[
                "source_decision_at_utc"
            ],
        )

        prior_signal_id = (
            selection_keys.get(
                selection_key
            )
        )

        if (
            prior_signal_id is not None
            and prior_signal_id
            != signal["signal_id"]
        ):
            _fail(
                "AMBIGUOUS_TEMPORAL_SELECTION",
                "distinct source signals share "
                "canonical instrument, "
                "eligible reference, and "
                "source decision time",
            )

        selection_keys[
            selection_key
        ] = signal["signal_id"]

    return (
        bundle_records,
        replay_signals,
    )


def _validated_boundaries(
    replay_boundaries: Any,
    *,
    known_instruments: set[str],
) -> list[dict[str, str]]:
    if (
        type(replay_boundaries) is not list
        or not replay_boundaries
    ):
        _fail(
            "INVALID_REPLAY_BOUNDARIES",
            "replay_boundaries must be "
            "a non-empty list",
        )

    result: list[
        dict[str, str]
    ] = []

    seen_boundary_ids: set[
        str
    ] = set()

    for index, raw in enumerate(
        deepcopy(replay_boundaries)
    ):
        boundary = _mapping(
            f"replay_boundaries[{index}]",
            raw,
        )

        _keys(
            f"replay_boundaries[{index}]",
            boundary,
            _BOUNDARY_INPUT_KEYS,
        )

        instrument = _text(
            "replay_boundaries"
            f"[{index}]."
            "canonical_instrument_id",
            boundary[
                "canonical_instrument_id"
            ],
        )

        if (
            instrument
            not in known_instruments
        ):
            _fail(
                "CANONICAL_INSTRUMENT_MISMATCH",
                "unknown replay canonical "
                f"instrument: {instrument}",
            )

        boundary_text = _text(
            "replay_boundaries"
            f"[{index}]."
            "replay_boundary_at_utc",
            boundary[
                "replay_boundary_at_utc"
            ],
        )

        _utc(
            "replay_boundaries"
            f"[{index}]."
            "replay_boundary_at_utc",
            boundary_text,
        )

        boundary_payload = {
            "canonical_instrument_id":
                instrument,
            "replay_boundary_at_utc":
                boundary_text,
        }

        boundary_id = _identity(
            "external_signal_replay_boundary",
            boundary_payload,
        )

        if (
            boundary_id
            in seen_boundary_ids
        ):
            _fail(
                "DUPLICATE_REPLAY_BOUNDARY",
                "duplicate replay boundary: "
                f"{instrument} @ "
                f"{boundary_text}",
            )

        seen_boundary_ids.add(
            boundary_id
        )

        result.append(
            {
                "boundary_id":
                    boundary_id,
                **boundary_payload,
            }
        )

    result.sort(
        key=lambda item: (
            _utc(
                "replay_boundary_at_utc",
                item[
                    "replay_boundary_at_utc"
                ],
            ),
            item[
                "canonical_instrument_id"
            ],
        )
    )

    return result


def _selected_event(
    *,
    boundary: dict[str, str],
    selected: dict[str, Any] | None,
    event_state: str,
    application_recorded: bool,
) -> dict[str, Any]:
    event = {
        "boundary_id":
            boundary["boundary_id"],
        "canonical_instrument_id":
            boundary[
                "canonical_instrument_id"
            ],
        "replay_boundary_at_utc":
            boundary[
                "replay_boundary_at_utc"
            ],
        "selected_signal_id":
            (
                None
                if selected is None
                else selected["signal_id"]
            ),
        "selected_source_decision_at_utc":
            (
                None
                if selected is None
                else selected[
                    "source_decision_at_utc"
                ]
            ),
        "selected_eligible_reference_at_utc":
            (
                None
                if selected is None
                else selected[
                    "eligible_reference_at_utc"
                ]
            ),
        "selected_valid_until_utc":
            (
                None
                if selected is None
                else selected[
                    "source_valid_until_utc"
                ]
            ),
        "replay_event_state":
            event_state,
        "offline_application_recorded":
            application_recorded,
    }

    _keys(
        "replay_event",
        event,
        _EVENT_KEYS,
    )

    return event


def _replay_events(
    replay_signals: list[
        dict[str, Any]
    ],
    replay_boundaries: list[
        dict[str, str]
    ],
) -> list[dict[str, Any]]:
    by_instrument: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for signal in replay_signals:
        by_instrument.setdefault(
            signal[
                "canonical_instrument_id"
            ],
            [],
        ).append(
            signal
        )

    applied_signal_ids: set[
        str
    ] = set()

    events: list[
        dict[str, Any]
    ] = []

    for boundary in replay_boundaries:
        instrument = boundary[
            "canonical_instrument_id"
        ]

        boundary_time = _utc(
            "replay_boundary_at_utc",
            boundary[
                "replay_boundary_at_utc"
            ],
        )

        instrument_signals = (
            by_instrument[instrument]
        )

        eligible = [
            signal
            for signal
            in instrument_signals
            if _utc(
                "signal."
                "eligible_reference_at_utc",
                signal[
                    "eligible_reference_at_utc"
                ],
            )
            <= boundary_time
        ]

        if not eligible:
            events.append(
                _selected_event(
                    boundary=boundary,
                    selected=None,
                    event_state=(
                        NOT_YET_ELIGIBLE
                    ),
                    application_recorded=(
                        False
                    ),
                )
            )
            continue

        selected = max(
            eligible,
            key=lambda signal: (
                _utc(
                    "signal."
                    "eligible_reference_at_utc",
                    signal[
                        "eligible_reference_at_utc"
                    ],
                ),
                _utc(
                    "signal."
                    "source_decision_at_utc",
                    signal[
                        "source_decision_at_utc"
                    ],
                ),
            ),
        )

        valid_until = _utc(
            "signal."
            "source_valid_until_utc",
            selected[
                "source_valid_until_utc"
            ],
        )

        if (
            boundary_time
            > valid_until
        ):
            events.append(
                _selected_event(
                    boundary=boundary,
                    selected=selected,
                    event_state=(
                        STALE_LATEST_SIGNAL
                    ),
                    application_recorded=(
                        False
                    ),
                )
            )
            continue

        if (
            selected["signal_id"]
            in applied_signal_ids
        ):
            events.append(
                _selected_event(
                    boundary=boundary,
                    selected=selected,
                    event_state=(
                        ALREADY_APPLIED
                    ),
                    application_recorded=(
                        False
                    ),
                )
            )
            continue

        applied_signal_ids.add(
            selected["signal_id"]
        )

        events.append(
            _selected_event(
                boundary=boundary,
                selected=selected,
                event_state=APPLIED,
                application_recorded=True,
            )
        )

    return events


def _metrics(
    *,
    input_bundle_count: int,
    source_signal_count: int,
    replay_boundaries: list[
        dict[str, str]
    ],
    replay_events: list[
        dict[str, Any]
    ],
) -> dict[str, Any]:
    metrics = {
        "input_bundle_count":
            input_bundle_count,
        "source_signal_count":
            source_signal_count,
        "replay_boundary_count":
            len(replay_boundaries),
        "applied_event_count":
            sum(
                event[
                    "replay_event_state"
                ] == APPLIED
                for event
                in replay_events
            ),
        "not_yet_eligible_count":
            sum(
                event[
                    "replay_event_state"
                ] == NOT_YET_ELIGIBLE
                for event
                in replay_events
            ),
        "stale_latest_count":
            sum(
                event[
                    "replay_event_state"
                ] == STALE_LATEST_SIGNAL
                for event
                in replay_events
            ),
        "already_applied_count":
            sum(
                event[
                    "replay_event_state"
                ] == ALREADY_APPLIED
                for event
                in replay_events
            ),
        "first_replay_boundary_at_utc":
            replay_boundaries[0][
                "replay_boundary_at_utc"
            ],
        "last_replay_boundary_at_utc":
            replay_boundaries[-1][
                "replay_boundary_at_utc"
            ],
    }

    _keys(
        "metrics",
        metrics,
        _METRIC_KEYS,
    )

    return metrics


def _replay_identity_payload(
    record: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: record[key]
        for key in sorted(record)
        if key != "replay_id"
    }


def _build_replay_result(
    *,
    evidence_bundles: Any,
    replay_boundaries: Any,
) -> dict[str, Any]:
    (
        source_bundles,
        replay_signals,
    ) = _validated_bundle_inputs(
        evidence_bundles
    )

    known_instruments = {
        signal[
            "canonical_instrument_id"
        ]
        for signal
        in replay_signals
    }

    boundaries = (
        _validated_boundaries(
            replay_boundaries,
            known_instruments=(
                known_instruments
            ),
        )
    )

    events = _replay_events(
        replay_signals,
        boundaries,
    )

    replay_input_id = _identity(
        "external_signal_replay_input",
        {
            "source_evidence_bundles":
                source_bundles,
            "replay_boundaries":
                boundaries,
        },
    )

    record: dict[str, Any] = {
        "schema_id":
            SCHEMA_ID,
        "schema_version":
            SCHEMA_VERSION,
        "result_type":
            RESULT_TYPE,
        "replay_state":
            REPLAY_STATE,
        "replay_scope":
            REPLAY_SCOPE,
        "replay_claim":
            REPLAY_CLAIM,
        "replay_id":
            "",
        "replay_input_id":
            replay_input_id,
        "source_evidence_bundles":
            source_bundles,
        "signal_ids":
            sorted(
                signal["signal_id"]
                for signal
                in replay_signals
            ),
        "replay_boundaries":
            boundaries,
        "replay_events":
            events,
        "metrics":
            _metrics(
                input_bundle_count=(
                    len(source_bundles)
                ),
                source_signal_count=(
                    len(replay_signals)
                ),
                replay_boundaries=(
                    boundaries
                ),
                replay_events=events,
            ),
    }

    record["replay_id"] = (
        _identity(
            "external_signal_replay",
            _replay_identity_payload(
                record
            ),
        )
    )

    return {
        "record": record,
        "checksum_algorithm":
            CHECKSUM_ALGORITHM,
        "replay_sha256":
            _digest(record),
    }


def build_external_signal_replay_evidence(
    *,
    evidence_bundles: list[
        dict[str, Any]
    ],
    replay_boundaries: list[
        dict[str, Any]
    ],
) -> dict[str, Any]:
    """Build deterministic offline replay evidence from validated upstream bundles."""

    result = _build_replay_result(
        evidence_bundles=(
            evidence_bundles
        ),
        replay_boundaries=(
            replay_boundaries
        ),
    )

    validate_external_signal_replay_evidence(
        result,
        evidence_bundles=(
            evidence_bundles
        ),
        replay_boundaries=(
            replay_boundaries
        ),
    )

    return result


def validate_external_signal_replay_evidence(
    evidence: Any,
    *,
    evidence_bundles: list[
        dict[str, Any]
    ],
    replay_boundaries: list[
        dict[str, Any]
    ],
) -> None:
    """Fail closed unless replay evidence exactly matches supplied controlled inputs."""

    expected = _build_replay_result(
        evidence_bundles=(
            evidence_bundles
        ),
        replay_boundaries=(
            replay_boundaries
        ),
    )

    value = _mapping(
        "replay evidence",
        evidence,
    )

    _keys(
        "replay evidence",
        value,
        _RESULT_KEYS,
    )

    if (
        _text(
            "checksum_algorithm",
            value["checksum_algorithm"],
        )
        != CHECKSUM_ALGORITHM
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported checksum_algorithm",
        )

    replay_sha256 = _sha(
        "replay_sha256",
        value["replay_sha256"],
    )

    record = _mapping(
        "replay evidence.record",
        value["record"],
    )

    _keys(
        "replay evidence.record",
        record,
        _RECORD_KEYS,
    )

    if (
        record["schema_id"]
        != SCHEMA_ID
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported schema_id",
        )

    if (
        type(record["schema_version"])
        is not int
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "schema_version must be an int",
        )

    if (
        record["schema_version"]
        != SCHEMA_VERSION
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported schema_version",
        )

    if (
        record["result_type"]
        != RESULT_TYPE
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported result_type",
        )

    if (
        record["replay_state"]
        != REPLAY_STATE
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "replay_state must be PASS",
        )

    if (
        record["replay_scope"]
        != REPLAY_SCOPE
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported replay_scope",
        )

    if (
        record["replay_claim"]
        != REPLAY_CLAIM
    ):
        _fail(
            "REPLAY_RECORD_SCHEMA_MISMATCH",
            "unsupported replay claim boundary",
        )

    expected_record = (
        expected["record"]
    )

    for field in sorted(
        _RECORD_KEYS
    ):
        if not _exact_equal(
            record[field],
            expected_record[field],
        ):
            _fail(
                "REPLAY_RECORD_CROSSLINK_MISMATCH",
                f"record.{field} does not "
                "match supplied validated "
                "replay inputs",
            )

    if not hmac.compare_digest(
        _digest(record),
        replay_sha256,
    ):
        _fail(
            "REPLAY_CHECKSUM_MISMATCH",
            "replay SHA-256 does not "
            "match canonical record",
        )


def canonical_serialize_external_signal_replay_evidence(
    evidence: dict[str, Any],
    *,
    evidence_bundles: list[
        dict[str, Any]
    ],
    replay_boundaries: list[
        dict[str, Any]
    ],
) -> str:
    """Return canonical JSON after complete fail-closed TM-023 validation."""

    validate_external_signal_replay_evidence(
        evidence,
        evidence_bundles=(
            evidence_bundles
        ),
        replay_boundaries=(
            replay_boundaries
        ),
    )

    return _canonical_json(
        evidence
    )
