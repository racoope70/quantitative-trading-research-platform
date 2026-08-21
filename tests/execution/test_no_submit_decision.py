"""Offline deterministic tests for canonical TM-028 no-submit decisions."""

from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.execution.no_submit_decision import (
    DECISION_ACTION,
    DECISION_TYPE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    STATE_PROVENANCE,
    NoSubmitDecisionError,
    build_no_submit_decision,
    validate_no_submit_decision,
)


def _example_inputs():
    return {
        "decision_id": "tm028-example",
        "instrument_id": "SYNTHETIC_X",
        "target_weight": 0.25,
        "current_weight": 0.10,
        "equity": 100_000.0,
        "metadata": {
            "run_id": "synthetic-run-001",
            "mode": "offline_test",
        },
    }


def test_decision_is_versioned_provider_neutral_and_no_submit():
    decision = build_no_submit_decision(**_example_inputs())

    assert decision["schema_id"] == SCHEMA_ID
    assert decision["schema_version"] == SCHEMA_VERSION
    assert decision["decision_type"] == DECISION_TYPE
    assert decision["state_provenance"] == STATE_PROVENANCE
    assert decision["decision_action"] == DECISION_ACTION
    assert decision["submission_authorized"] is False
    assert decision["order_submitted"] is False

    validate_no_submit_decision(decision)


def test_historical_reusable_decision_arithmetic_is_preserved():
    decision = build_no_submit_decision(**_example_inputs())

    assert decision["target_weight"] == 0.25
    assert decision["current_weight"] == 0.10
    assert decision["intended_delta_weight"] == pytest.approx(0.15)
    assert decision["equity"] == 100_000.0
    assert decision["intended_notional"] == pytest.approx(15_000.0)


def test_negative_delta_is_deterministic_and_still_no_submit():
    arguments = _example_inputs()
    arguments["target_weight"] = 0.05
    arguments["current_weight"] = 0.20

    decision = build_no_submit_decision(**arguments)

    assert decision["intended_delta_weight"] == pytest.approx(-0.15)
    assert decision["intended_notional"] == pytest.approx(-15_000.0)
    assert decision["decision_action"] == "NO_SUBMIT"
    assert decision["submission_authorized"] is False
    assert decision["order_submitted"] is False


def test_identical_inputs_produce_identical_decision_package():
    first = build_no_submit_decision(**_example_inputs())
    second = build_no_submit_decision(**_example_inputs())

    assert first == second


def test_metadata_key_order_does_not_change_semantic_package():
    first = build_no_submit_decision(**_example_inputs())

    arguments = _example_inputs()
    arguments["metadata"] = {
        "mode": "offline_test",
        "run_id": "synthetic-run-001",
    }

    second = build_no_submit_decision(**arguments)

    assert first == second


def test_none_metadata_normalizes_to_empty_mapping():
    arguments = _example_inputs()
    arguments["metadata"] = None

    decision = build_no_submit_decision(**arguments)

    assert decision["metadata"] == {}


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("decision_id", ""),
        ("decision_id", "   "),
        ("decision_id", None),
        ("decision_id", 123),
        ("instrument_id", ""),
        ("instrument_id", "   "),
        ("instrument_id", None),
        ("instrument_id", 123),
    ],
)
def test_invalid_identity_fields_fail_closed(field_name, bad_value):
    arguments = _example_inputs()
    arguments[field_name] = bad_value

    with pytest.raises(NoSubmitDecisionError, match=field_name):
        build_no_submit_decision(**arguments)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("target_weight", True),
        ("target_weight", float("nan")),
        ("target_weight", float("inf")),
        ("target_weight", "0.25"),
        ("current_weight", False),
        ("current_weight", float("-inf")),
        ("current_weight", None),
        ("equity", True),
        ("equity", float("nan")),
        ("equity", "100000"),
    ],
)
def test_malformed_numeric_inputs_fail_closed(field_name, bad_value):
    arguments = _example_inputs()
    arguments[field_name] = bad_value

    with pytest.raises(NoSubmitDecisionError, match=field_name):
        build_no_submit_decision(**arguments)


@pytest.mark.parametrize(
    "metadata",
    [
        [],
        "",
        0,
        False,
        {"bad": {1, 2}},
        {"bad": float("nan")},
        {1: "non-string-key"},
        {"bad": object()},
    ],
)
def test_malformed_or_ambiguous_metadata_fails_closed(metadata):
    arguments = _example_inputs()
    arguments["metadata"] = metadata

    with pytest.raises(NoSubmitDecisionError):
        build_no_submit_decision(**arguments)


def test_schema_rejects_missing_and_unexpected_fields():
    decision = build_no_submit_decision(**_example_inputs())

    missing = deepcopy(decision)
    del missing["order_submitted"]

    with pytest.raises(NoSubmitDecisionError, match="keys mismatch"):
        validate_no_submit_decision(missing)

    unexpected = deepcopy(decision)
    unexpected["provider"] = "forbidden"

    with pytest.raises(NoSubmitDecisionError, match="keys mismatch"):
        validate_no_submit_decision(unexpected)


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        ("schema_id", "OTHER", "schema_id"),
        ("schema_version", 2, "schema_version"),
        ("schema_version", True, "schema_version"),
        ("decision_type", "operational_order", "type"),
        ("state_provenance", "live_broker", "provenance"),
        ("decision_action", "SUBMIT", "NO_SUBMIT"),
        ("submission_authorized", True, "submission_authorized"),
        ("submission_authorized", 0, "submission_authorized"),
        ("order_submitted", True, "order_submitted"),
        ("order_submitted", 0, "order_submitted"),
    ],
)
def test_operational_or_unsupported_contract_mutations_fail_closed(
    field_name,
    bad_value,
    message,
):
    decision = build_no_submit_decision(**_example_inputs())
    decision[field_name] = bad_value

    with pytest.raises(NoSubmitDecisionError, match=message):
        validate_no_submit_decision(decision)


def test_tampered_delta_weight_fails_closed():
    decision = build_no_submit_decision(**_example_inputs())
    decision["intended_delta_weight"] = 0.99

    with pytest.raises(
        NoSubmitDecisionError,
        match="intended_delta_weight",
    ):
        validate_no_submit_decision(decision)


def test_tampered_intended_notional_fails_closed():
    decision = build_no_submit_decision(**_example_inputs())
    decision["intended_notional"] = 1.0

    with pytest.raises(
        NoSubmitDecisionError,
        match="intended_notional",
    ):
        validate_no_submit_decision(decision)


def test_module_import_is_offline_and_side_effect_free():
    source_root = ROOT / "src"

    code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("pathlib.Path.write_text", side_effect=AssertionError("write called")), \
     patch("pathlib.Path.open", side_effect=AssertionError("file open called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.execution.no_submit_decision
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


def test_module_source_has_no_operational_imports():
    source = (
        ROOT
        / "src"
        / "quantitative_trading_research"
        / "execution"
        / "no_submit_decision.py"
    ).read_text(encoding="utf-8")

    prohibited_imports = (
        "import alpaca",
        "from alpaca",
        "import requests",
        "from requests",
        "import pandas",
        "from pandas",
        "import numpy",
        "from numpy",
        "import torch",
        "from torch",
        "import stable_baselines3",
        "from stable_baselines3",
        "import pyarrow",
        "from pyarrow",
    )

    for prohibited in prohibited_imports:
        assert prohibited not in source
