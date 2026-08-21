"""Offline tests for canonical TM-053 diagnostic evidence."""

from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.evaluation.diagnostics import (
    DIAGNOSTIC_SCHEMA_ID,
    DIAGNOSTIC_SCHEMA_VERSION,
    DIAGNOSTIC_SCOPE,
    FAIL_REQUIRED_OBSERVATION_OUTCOME,
    PASS_OUTCOME,
    DiagnosticEvidenceError,
    build_diagnostic_evidence,
    normalize_diagnostic_value,
    validate_diagnostic_evidence,
)


def _passing_inputs():
    return {
        "diagnostic_id": "tm053-offline-check",
        "required_observations": {
            "configuration_present": True,
            "evidence_identity_present": True,
        },
        "optional_observations": {
            "supplemental_note_present": False,
        },
        "metadata": {
            "source": "synthetic",
            "nested": {"z": 2, "a": 1},
        },
    }


def test_builds_versioned_structured_passing_evidence():
    evidence = build_diagnostic_evidence(**_passing_inputs())

    assert evidence["schema_id"] == DIAGNOSTIC_SCHEMA_ID
    assert evidence["schema_version"] == DIAGNOSTIC_SCHEMA_VERSION
    assert evidence["scope"] == DIAGNOSTIC_SCOPE
    assert evidence["terminal_outcome"] == PASS_OUTCOME
    assert evidence["failed_required_observations"] == []

    validate_diagnostic_evidence(evidence)


def test_failed_required_observations_are_sorted_and_control_outcome():
    evidence = build_diagnostic_evidence(
        diagnostic_id="required-failure",
        required_observations={
            "z_check": False,
            "a_check": False,
            "middle_check": True,
        },
    )

    assert list(evidence["required_observations"]) == [
        "a_check",
        "middle_check",
        "z_check",
    ]
    assert evidence["failed_required_observations"] == [
        "a_check",
        "z_check",
    ]
    assert (
        evidence["terminal_outcome"]
        == FAIL_REQUIRED_OBSERVATION_OUTCOME
    )


def test_optional_observations_do_not_control_terminal_outcome():
    evidence = build_diagnostic_evidence(
        diagnostic_id="optional-only-failure",
        required_observations={"required_check": True},
        optional_observations={"optional_check": False},
    )

    assert evidence["optional_observations"]["optional_check"] is False
    assert evidence["terminal_outcome"] == PASS_OUTCOME


def test_output_is_deterministically_normalized():
    first = build_diagnostic_evidence(
        diagnostic_id="deterministic",
        required_observations={"z": True, "a": True},
        optional_observations={"y": False, "b": True},
        metadata={
            "z": {"two": 2, "one": 1},
            "a": [3, {"d": 4, "c": 3}],
        },
    )

    second = build_diagnostic_evidence(
        diagnostic_id="deterministic",
        required_observations={"a": True, "z": True},
        optional_observations={"b": True, "y": False},
        metadata={
            "a": [3, {"c": 3, "d": 4}],
            "z": {"one": 1, "two": 2},
        },
    )

    assert first == second
    assert list(first["required_observations"]) == ["a", "z"]
    assert list(first["optional_observations"]) == ["b", "y"]
    assert list(first["metadata"]) == ["a", "z"]
    assert list(first["metadata"]["z"]) == ["one", "two"]


@pytest.mark.parametrize(
    "bad_id",
    ["", "   ", " padded", "padded ", None, 123],
)
def test_invalid_diagnostic_id_fails_closed(bad_id):
    with pytest.raises(DiagnosticEvidenceError, match="diagnostic_id"):
        build_diagnostic_evidence(
            diagnostic_id=bad_id,
            required_observations={"check": True},
        )


@pytest.mark.parametrize(
    "bad_required",
    [
        {},
        [],
        "",
        {"check": 1},
        {"check": "true"},
        {"": True},
        {" ": True},
        {" padded": True},
        {"padded ": True},
        {"valid": True, 1: False},
    ],
)
def test_malformed_required_observations_fail_closed(bad_required):
    with pytest.raises(DiagnosticEvidenceError):
        build_diagnostic_evidence(
            diagnostic_id="bad-required",
            required_observations=bad_required,
        )


@pytest.mark.parametrize(
    "bad_optional",
    [
        [],
        "",
        0,
        False,
        {"check": 1},
        {"valid": True, 1: False},
    ],
)
def test_malformed_optional_observations_fail_closed(bad_optional):
    with pytest.raises(DiagnosticEvidenceError):
        build_diagnostic_evidence(
            diagnostic_id="bad-optional",
            required_observations={"required": True},
            optional_observations=bad_optional,
        )


def test_none_optional_inputs_become_empty_structures():
    evidence = build_diagnostic_evidence(
        diagnostic_id="none-optionals",
        required_observations={"required": True},
        optional_observations=None,
        metadata=None,
    )

    assert evidence["optional_observations"] == {}
    assert evidence["metadata"] == {}


def test_required_and_optional_observations_must_not_overlap():
    with pytest.raises(DiagnosticEvidenceError, match="must not overlap"):
        build_diagnostic_evidence(
            diagnostic_id="overlap",
            required_observations={"same": True},
            optional_observations={"same": False},
        )


@pytest.mark.parametrize(
    "bad_metadata",
    [
        [],
        "",
        False,
        {"bad": {1, 2}},
        {"bad": float("nan")},
        {"bad": float("inf")},
        {"valid": True, 1: False},
        object(),
    ],
)
def test_malformed_or_unsupported_metadata_fails_closed(bad_metadata):
    with pytest.raises(DiagnosticEvidenceError):
        build_diagnostic_evidence(
            diagnostic_id="bad-metadata",
            required_observations={"required": True},
            metadata=bad_metadata,
        )


def test_tuple_metadata_is_normalized_to_list():
    normalized = normalize_diagnostic_value(
        {"values": (1, 2, 3)}
    )

    assert normalized == {"values": [1, 2, 3]}


def test_validation_rejects_missing_and_unexpected_fields():
    evidence = build_diagnostic_evidence(**_passing_inputs())

    missing = deepcopy(evidence)
    del missing["terminal_outcome"]

    with pytest.raises(DiagnosticEvidenceError, match="keys mismatch"):
        validate_diagnostic_evidence(missing)

    unexpected = deepcopy(evidence)
    unexpected["provider_state"] = True

    with pytest.raises(DiagnosticEvidenceError, match="keys mismatch"):
        validate_diagnostic_evidence(unexpected)


def test_validation_rejects_inconsistent_failed_observations():
    evidence = build_diagnostic_evidence(
        diagnostic_id="tampered-failures",
        required_observations={"a": False, "b": True},
    )
    evidence["failed_required_observations"] = []

    with pytest.raises(
        DiagnosticEvidenceError,
        match="failed_required_observations is inconsistent",
    ):
        validate_diagnostic_evidence(evidence)


def test_validation_rejects_inconsistent_terminal_outcome():
    evidence = build_diagnostic_evidence(
        diagnostic_id="tampered-outcome",
        required_observations={"required": False},
    )
    evidence["terminal_outcome"] = PASS_OUTCOME

    with pytest.raises(
        DiagnosticEvidenceError,
        match="terminal_outcome is inconsistent",
    ):
        validate_diagnostic_evidence(evidence)


def test_builder_does_not_mutate_caller_inputs():
    inputs = _passing_inputs()
    original = deepcopy(inputs)

    build_diagnostic_evidence(**inputs)

    assert inputs == original


def test_module_import_is_offline_and_side_effect_free():
    source_root = ROOT / "src"

    code = """
from unittest.mock import patch

with patch(
    "pathlib.Path.mkdir",
    side_effect=AssertionError("mkdir called"),
), patch(
    "pathlib.Path.open",
    side_effect=AssertionError("file open called"),
), patch(
    "pathlib.Path.read_text",
    side_effect=AssertionError("file read called"),
), patch(
    "pathlib.Path.write_text",
    side_effect=AssertionError("file write called"),
), patch(
    "socket.socket.connect",
    side_effect=AssertionError("network connect called"),
), patch(
    "socket.create_connection",
    side_effect=AssertionError("network connection called"),
):
    import quantitative_trading_research.evaluation.diagnostics
"""

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(source_root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, (
        f"stdout={completed.stdout}\nstderr={completed.stderr}"
    )
