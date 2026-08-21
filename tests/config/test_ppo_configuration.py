"""Offline tests for the canonical fail-closed PPO configuration boundary.

Adapted from ``racoope70/ppo-trading-pipeline`` at immutable source commit
``072103f43d8b2488c3efca183f637ab0508a193a``, historical path
``tests/test_ppo_v2_retraining_config.py``.
"""

from __future__ import annotations

from dataclasses import fields, replace
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.config.ppo import (
    PPOAuthorizationBoundary,
    PPOConfiguration,
    PPOConfigurationError,
    SCHEMA_ID,
    SCHEMA_VERSION,
    build_default_ppo_configuration,
)


def test_default_configuration_is_fail_closed():
    configuration = build_default_ppo_configuration()

    assert configuration.authorization.as_dict() == {
        "training_enabled": False,
        "dataset_generation_enabled": False,
        "model_artifact_creation_enabled": False,
        "final_holdout_access_enabled": False,
        "provider_operations_enabled": False,
        "paper_order_submission_enabled": False,
        "live_order_submission_enabled": False,
    }
    configuration.validate()


@pytest.mark.parametrize(
    "authorization_field",
    [
        "training_enabled",
        "dataset_generation_enabled",
        "model_artifact_creation_enabled",
        "final_holdout_access_enabled",
        "provider_operations_enabled",
        "paper_order_submission_enabled",
        "live_order_submission_enabled",
    ],
)
def test_each_operational_authorization_fails_closed(authorization_field):
    configuration = build_default_ppo_configuration()
    authorization = replace(
        configuration.authorization,
        **{authorization_field: True},
    )
    unsafe_configuration = replace(
        configuration,
        authorization=authorization,
    )

    with pytest.raises(PPOConfigurationError, match=authorization_field):
        unsafe_configuration.validate()


@pytest.mark.parametrize(
    "malformed_value",
    [
        0,
        1,
        None,
        "",
        object(),
    ],
)
def test_non_bool_authorization_capability_fails_closed(malformed_value):
    configuration = build_default_ppo_configuration()
    authorization = replace(
        configuration.authorization,
        training_enabled=malformed_value,
    )
    malformed_configuration = replace(
        configuration,
        authorization=authorization,
    )

    with pytest.raises(PPOConfigurationError, match="must be bool"):
        malformed_configuration.validate()


def test_wrong_authorization_object_type_fails_closed():
    configuration = replace(
        build_default_ppo_configuration(),
        authorization=None,
    )

    with pytest.raises(PPOConfigurationError, match="PPOAuthorizationBoundary"):
        configuration.validate()


def test_configuration_identity_is_versioned_and_deterministic():
    first = build_default_ppo_configuration()
    second = build_default_ppo_configuration()

    assert first.schema_id == SCHEMA_ID
    assert first.schema_version == SCHEMA_VERSION
    assert first.canonical_payload() == second.canonical_payload()
    assert first.checksum_sha256() == second.checksum_sha256()
    assert len(first.checksum_sha256()) == 64


def test_matching_expected_checksum_is_accepted():
    configuration = build_default_ppo_configuration()

    configuration.validate(expected_checksum=configuration.checksum_sha256())


def test_checksum_mismatch_fails_closed():
    configuration = build_default_ppo_configuration()
    mismatched = "0" * 64

    if mismatched == configuration.checksum_sha256():
        mismatched = "1" * 64

    with pytest.raises(PPOConfigurationError, match="checksum mismatch"):
        configuration.validate(expected_checksum=mismatched)


@pytest.mark.parametrize(
    "invalid_checksum",
    [
        "",
        "abc",
        "g" * 64,
        "0" * 63,
        "0" * 65,
    ],
)
def test_invalid_expected_checksum_identity_fails_closed(invalid_checksum):
    configuration = build_default_ppo_configuration()

    with pytest.raises(PPOConfigurationError, match="SHA-256 hex"):
        configuration.validate(expected_checksum=invalid_checksum)


def test_non_string_expected_checksum_fails_closed():
    configuration = build_default_ppo_configuration()

    with pytest.raises(PPOConfigurationError, match="must be a string"):
        configuration.validate(expected_checksum=123)


def test_schema_id_mismatch_fails_closed():
    configuration = replace(
        build_default_ppo_configuration(),
        schema_id="UNSUPPORTED",
    )

    with pytest.raises(PPOConfigurationError, match="schema_id"):
        configuration.validate()


def test_schema_version_bool_fails_closed():
    configuration = replace(
        build_default_ppo_configuration(),
        schema_version=True,
    )

    with pytest.raises(PPOConfigurationError, match="schema_version"):
        configuration.validate()


def test_schema_version_wrong_runtime_type_fails_closed():
    configuration = replace(
        build_default_ppo_configuration(),
        schema_version="1",
    )

    with pytest.raises(PPOConfigurationError, match="schema_version"):
        configuration.validate()


def test_schema_version_unsupported_integer_fails_closed():
    configuration = replace(
        build_default_ppo_configuration(),
        schema_version=SCHEMA_VERSION + 1,
    )

    with pytest.raises(PPOConfigurationError, match="schema_version"):
        configuration.validate()


def test_configuration_has_no_execution_command_fields():
    names = {field.name for field in fields(PPOConfiguration)}

    assert not {
        "training_command",
        "dataset_generation_command",
        "model_artifact_command",
        "paper_order_command",
        "live_order_command",
    }.intersection(names)


def test_configuration_does_not_encode_later_phase_semantics():
    names = {field.name for field in fields(PPOConfiguration)}

    prohibited_fields = {
        "provider",
        "data_source",
        "symbols",
        "universe",
        "features",
        "train_split_name",
        "eval_split_name",
        "holdout_split_name",
        "holdout_usage",
        "model_artifact_root",
        "report_root",
        "model_quality",
        "deployment_candidate",
    }

    assert prohibited_fields.isdisjoint(names)


def test_authorization_boundary_contains_only_explicit_closed_capabilities():
    names = {field.name for field in fields(PPOAuthorizationBoundary)}

    assert names == {
        "training_enabled",
        "dataset_generation_enabled",
        "model_artifact_creation_enabled",
        "final_holdout_access_enabled",
        "provider_operations_enabled",
        "paper_order_submission_enabled",
        "live_order_submission_enabled",
    }


def test_module_import_is_offline_and_side_effect_free():
    source_root = ROOT / "src"

    code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("pathlib.Path.write_text", side_effect=AssertionError("write called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.config.ppo
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
