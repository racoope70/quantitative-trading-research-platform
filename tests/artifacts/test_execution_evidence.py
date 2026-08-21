"""Offline tests for canonical TM-033 execution-evidence construction."""

from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.artifacts.execution_evidence import (
    BROKER_STATE_PROVENANCE,
    CHECKSUM_ALGORITHM,
    EVIDENCE_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    ExecutionEvidenceError,
    build_checksummed_execution_evidence,
    build_execution_evidence_record,
    canonical_json_bytes,
    checksum_sha256,
    normalize_evidence_value,
    validate_checksummed_execution_evidence,
    validate_execution_evidence_record,
)


def _example_inputs():
    return {
        "evidence_id": "tm033-example",
        "metadata": {
            "run_id": "synthetic-run-001",
            "mode": "offline_test",
        },
        "execution_state": {
            "orders_required": 1,
            "orders_submitted": 0,
            "risk_passed": True,
        },
        "broker_state_before": {
            "account": {"equity": "100000"},
            "positions": [{"symbol": "AMD", "qty": "10"}],
        },
        "broker_state_after": {
            "account": {"equity": "100100"},
            "positions": [{"symbol": "AMD", "qty": "10"}],
        },
    }


def test_record_is_versioned_and_marks_broker_state_unverified():
    record = build_execution_evidence_record(**_example_inputs())

    assert record["schema_id"] == SCHEMA_ID
    assert record["schema_version"] == SCHEMA_VERSION
    assert record["evidence_type"] == EVIDENCE_TYPE
    assert record["broker_state_provenance"] == BROKER_STATE_PROVENANCE
    validate_execution_evidence_record(record)


def test_serialization_and_checksum_are_deterministic():
    first = build_execution_evidence_record(**_example_inputs())

    reordered = build_execution_evidence_record(
        evidence_id="tm033-example",
        metadata={"mode": "offline_test", "run_id": "synthetic-run-001"},
        execution_state={
            "risk_passed": True,
            "orders_submitted": 0,
            "orders_required": 1,
        },
        broker_state_before={
            "positions": [{"qty": "10", "symbol": "AMD"}],
            "account": {"equity": "100000"},
        },
        broker_state_after={
            "positions": [{"qty": "10", "symbol": "AMD"}],
            "account": {"equity": "100100"},
        },
    )

    assert canonical_json_bytes(first) == canonical_json_bytes(reordered)
    assert checksum_sha256(first) == checksum_sha256(reordered)
    assert len(checksum_sha256(first)) == 64


def test_checksummed_package_validates_and_detects_tampering():
    package = build_checksummed_execution_evidence(**_example_inputs())

    assert package["checksum_algorithm"] == CHECKSUM_ALGORITHM
    validate_checksummed_execution_evidence(package)

    tampered = deepcopy(package)
    tampered["record"]["execution_state"]["orders_submitted"] = 1

    with pytest.raises(ExecutionEvidenceError, match="checksum mismatch"):
        validate_checksummed_execution_evidence(tampered)


@pytest.mark.parametrize(
    ("field_name", "malformed_value"),
    [
        ("metadata", []),
        ("metadata", ""),
        ("broker_state_before", []),
        ("broker_state_before", 0),
        ("broker_state_after", ""),
        ("broker_state_after", False),
    ],
)
def test_falsey_and_non_mapping_optional_state_fails_closed(
    field_name,
    malformed_value,
):
    arguments = _example_inputs()
    arguments[field_name] = malformed_value

    with pytest.raises(ExecutionEvidenceError, match="must be a dict"):
        build_execution_evidence_record(**arguments)


def test_none_optional_state_is_explicitly_normalized_to_empty_mapping():
    arguments = _example_inputs()
    arguments["metadata"] = None
    arguments["broker_state_before"] = None
    arguments["broker_state_after"] = None

    record = build_execution_evidence_record(**arguments)

    assert record["metadata"] == {}
    assert record["broker_state_before"] == {}
    assert record["broker_state_after"] == {}


@pytest.mark.parametrize(
    "value",
    [
        {"bad": {1, 2}},
        {"bad": float("nan")},
        {"bad": float("inf")},
        {1: "non-string-key"},
        object(),
    ],
)
def test_ambiguous_or_unsupported_values_fail_closed(value):
    with pytest.raises(ExecutionEvidenceError):
        normalize_evidence_value(value)


@pytest.mark.parametrize(
    "bad_id",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_invalid_evidence_id_fails_closed(bad_id):
    arguments = _example_inputs()
    arguments["evidence_id"] = bad_id

    with pytest.raises(ExecutionEvidenceError, match="evidence_id"):
        build_execution_evidence_record(**arguments)


def test_record_schema_rejects_missing_or_unexpected_fields():
    record = build_execution_evidence_record(**_example_inputs())

    missing = deepcopy(record)
    del missing["execution_state"]

    with pytest.raises(ExecutionEvidenceError, match="keys mismatch"):
        validate_execution_evidence_record(missing)

    unexpected = deepcopy(record)
    unexpected["provider"] = "forbidden"

    with pytest.raises(ExecutionEvidenceError, match="keys mismatch"):
        validate_execution_evidence_record(unexpected)


def test_broker_state_is_preserved_as_opaque_caller_supplied_data():
    arguments = _example_inputs()
    record = build_execution_evidence_record(**arguments)

    assert record["broker_state_before"] == arguments["broker_state_before"]
    assert record["broker_state_after"] == arguments["broker_state_after"]
    assert record["broker_state_provenance"] == "caller_supplied_unverified"


def test_module_import_is_offline_and_side_effect_free():
    source_root = ROOT / "src"

    code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("pathlib.Path.write_text", side_effect=AssertionError("write called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.artifacts.execution_evidence
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
