"""Focused tests for the C4 TM-061 offline no-submit package evaluator."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

import pytest

from quantitative_trading_research.artifacts.execution_evidence import (
    build_checksummed_execution_evidence,
)
from quantitative_trading_research.execution.coordinator import (
    build_execution_coordinator,
)
from quantitative_trading_research.execution.no_submit_decision import (
    build_no_submit_decision,
)
from quantitative_trading_research.execution.plan import build_execution_plan
from quantitative_trading_research.execution.plan_filter import filter_execution_plan
from quantitative_trading_research.execution.pre_trade import (
    evaluate_pre_trade_eligibility,
)
from quantitative_trading_research.execution.risk_controls import (
    evaluate_risk_controls,
)
from quantitative_trading_research.execution.submission import (
    build_submission_boundary,
)
from quantitative_trading_research.evaluation.no_submit_package import (
    ECONOMIC_QUALIFICATION,
    EXECUTION_READINESS,
    FAIL_OUTCOME,
    INCONCLUSIVE_OUTCOME,
    MODEL_QUALITY,
    PASS_OUTCOME,
    NoSubmitPackageEvaluationError,
    evaluate_no_submit_package,
    validate_no_submit_package_evaluation,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    ROOT
    / "src"
    / "quantitative_trading_research"
    / "evaluation"
    / "no_submit_package.py"
)

STATE_AT = "2026-08-22T15:00:00+00:00"
PRICE_AT = "2026-08-22T15:01:00+00:00"
PLAN_AT = "2026-08-22T15:02:00+00:00"
FILTER_AT = "2026-08-22T15:03:00+00:00"
EVALUATION_AT = "2026-08-22T15:02:30+00:00"


def _rows(*, target_weight: float = 0.20) -> list[dict]:
    return [
        {
            "instrument_id": "AAA",
            "target_weight": target_weight,
            "current_weight": 0.0,
            "equity": 100_000.0,
        }
    ]


def _coordinator(*, target_weight: float = 0.20) -> dict:
    rows = _rows(target_weight=target_weight)
    risk = evaluate_risk_controls(
        plan_rows=[
            {
                "instrument_id": row["instrument_id"],
                "target_weight": row["target_weight"],
                "current_weight": row["current_weight"],
                "equity": row["equity"],
                "order_submitted": False,
                "observed_at_utc": STATE_AT,
            }
            for row in rows
        ],
        account_state={
            "open_orders_count": 0,
            "positions_count": 0,
        },
    )

    decisions = [
        build_no_submit_decision(
            decision_id="decision-1",
            instrument_id="AAA",
            target_weight=target_weight,
            current_weight=0.0,
            equity=100_000.0,
        )
    ]

    pre_trade = evaluate_pre_trade_eligibility(
        risk_result=risk,
        decisions=decisions,
    )

    plan = build_execution_plan(
        pre_trade_result=pre_trade,
        price_evidence=[
            {
                "instrument_id": "AAA",
                "price": 100.0,
                "observed_at_utc": PRICE_AT,
            }
        ],
        configuration={
            "min_notional": 25.0,
            "allow_shorts": True,
            "use_fractionals": True,
            "qty_precision": 6,
        },
        plan_at_utc=PLAN_AT,
    )

    filtered = filter_execution_plan(
        execution_plan=plan,
        selection_criteria={
            "instrument_id": "AAA",
            "side": None,
        },
        filtered_at_utc=FILTER_AT,
    )

    boundary = build_submission_boundary(
        filtered_execution_plan=filtered,
    )

    return build_execution_coordinator(
        risk_result=risk,
        pre_trade_result=pre_trade,
        execution_plan=plan,
        filtered_execution_plan=filtered,
        submission_boundary=boundary,
    )


def _package(
    *,
    coordinator: dict | None = None,
    broker_state_before: dict | None = None,
    broker_state_after: dict | None = None,
) -> dict:
    return build_checksummed_execution_evidence(
        evidence_id="tm061-package-001",
        execution_state=_coordinator() if coordinator is None else coordinator,
        broker_state_before=(
            {} if broker_state_before is None else broker_state_before
        ),
        broker_state_after=(
            {} if broker_state_after is None else broker_state_after
        ),
        metadata={"mode": "offline_test"},
    )


def _evaluate(
    package: dict | None = None,
    *,
    evaluation_at_utc: str = EVALUATION_AT,
    max_age_seconds: float = 60.0,
    require_broker_state_authority: bool = False,
) -> dict:
    return evaluate_no_submit_package(
        package=_package() if package is None else package,
        evaluation_at_utc=evaluation_at_utc,
        max_age_seconds=max_age_seconds,
        require_broker_state_authority=require_broker_state_authority,
    )


def _repackage_coordinator(coordinator: dict) -> dict:
    return build_checksummed_execution_evidence(
        evidence_id="tm061-package-001",
        execution_state=coordinator,
        broker_state_before={},
        broker_state_after={},
        metadata={"mode": "offline_test"},
    )


def test_valid_checksummed_tm033_package_with_tm030_coordinator_passes():
    result = _evaluate()

    assert result["operational_evaluation"] == PASS_OUTCOME
    assert result["reason_codes"] == ["OPERATIONAL_REQUIREMENTS_SATISFIED"]
    validate_no_submit_package_evaluation(result)


def test_evaluator_identity_is_deterministic():
    package = _package()
    first = _evaluate(package)
    second = _evaluate(package)

    assert first == second
    assert first["evaluation_id"] == second["evaluation_id"]


def test_material_policy_change_changes_evaluator_identity():
    package = _package()
    first = _evaluate(package, max_age_seconds=60.0)
    second = _evaluate(package, max_age_seconds=61.0)

    assert first["evaluation_id"] != second["evaluation_id"]


def test_reason_order_is_deterministic_when_failure_and_inconclusive_evidence_coexist():
    result = _evaluate(
        evaluation_at_utc="2026-08-22T15:04:00+00:00",
        max_age_seconds=60.0,
        require_broker_state_authority=True,
    )

    assert result["operational_evaluation"] == FAIL_OUTCOME
    assert result["reason_codes"] == [
        "STALE_EVIDENCE",
        "BROKER_STATE_AUTHORITY_NOT_ESTABLISHED",
    ]


def test_explicit_fail_outcome_for_stale_valid_evidence():
    result = _evaluate(
        evaluation_at_utc="2026-08-22T15:04:00+00:00",
        max_age_seconds=60.0,
    )

    assert result["operational_evaluation"] == FAIL_OUTCOME
    assert result["freshness"]["passed"] is False
    assert result["reason_codes"] == ["STALE_EVIDENCE"]


def test_explicit_inconclusive_outcome_for_unverifiable_broker_authority_requirement():
    result = _evaluate(require_broker_state_authority=True)

    assert result["operational_evaluation"] == INCONCLUSIVE_OUTCOME
    assert result["broker_state_authority"] == {
        "required": True,
        "established": False,
        "source_provenance": "caller_supplied_unverified",
    }
    assert result["reason_codes"] == [
        "BROKER_STATE_AUTHORITY_NOT_ESTABLISHED"
    ]


@pytest.mark.parametrize("package", [None, [], "package", 1, False])
def test_missing_or_non_mapping_package_fails_closed(package):
    with pytest.raises(NoSubmitPackageEvaluationError):
        evaluate_no_submit_package(
            package=package,
            evaluation_at_utc=EVALUATION_AT,
            max_age_seconds=60.0,
        )


def test_missing_package_field_fails_closed():
    package = _package()
    del package["checksum_sha256"]

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_unexpected_package_field_fails_closed():
    package = _package()
    package["provider"] = "forbidden"

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_tm033_checksum_tampering_fails_closed_before_coordinator_policy():
    package = _package()
    package["record"]["execution_state"]["orders_submitted"] = 1

    with pytest.raises(
        NoSubmitPackageEvaluationError,
        match="execution-evidence package is invalid",
    ):
        _evaluate(package)


def test_wrong_checksum_algorithm_fails_closed_transitively_through_tm033():
    package = _package()
    package["checksum_algorithm"] = "sha512"

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_malformed_tm030_coordinator_fails_closed_after_valid_tm033_checksum():
    coordinator = _coordinator()
    del coordinator["upstream_chain"]
    package = _repackage_coordinator(coordinator)

    with pytest.raises(
        NoSubmitPackageEvaluationError,
        match="execution_state coordinator is invalid",
    ):
        _evaluate(package)


def test_forged_tm030_coordinator_identity_fails_closed():
    coordinator = _coordinator()
    coordinator["coordinator_id"] = "execution_coordinator:forged"
    package = _repackage_coordinator(coordinator)

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_reordered_tm030_upstream_chain_fails_closed_transitively():
    coordinator = _coordinator()
    coordinator["upstream_chain"][0], coordinator["upstream_chain"][1] = (
        coordinator["upstream_chain"][1],
        coordinator["upstream_chain"][0],
    )
    package = _repackage_coordinator(coordinator)

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_cross_contract_tm030_mismatch_fails_closed_transitively():
    first = _coordinator(target_weight=0.20)
    second = _coordinator(target_weight=0.25)
    first["risk_result"] = second["risk_result"]
    package = _repackage_coordinator(first)

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_tampered_tm030_embedded_plan_fails_closed_transitively():
    coordinator = _coordinator()
    coordinator["execution_plan"]["intents"][0]["quantity"] += 1.0
    package = _repackage_coordinator(coordinator)

    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(package)


def test_source_package_identities_are_preserved_exactly():
    package = _package()
    result = _evaluate(package)

    assert result["source_execution_evidence_checksum"] == package[
        "checksum_sha256"
    ]
    assert result["source_execution_evidence_id"] == package["record"][
        "evidence_id"
    ]
    assert result["source_coordinator_id"] == package["record"][
        "execution_state"
    ]["coordinator_id"]


def test_fresh_timestamp_uses_embedded_tm062_plan_at_utc():
    result = _evaluate(
        evaluation_at_utc="2026-08-22T15:02:59+00:00",
        max_age_seconds=60.0,
    )

    assert result["freshness"]["plan_at_utc"] == PLAN_AT
    assert result["freshness"]["age_seconds"] == 59.0
    assert result["freshness"]["passed"] is True
    assert result["operational_evaluation"] == PASS_OUTCOME


def test_exact_freshness_boundary_is_accepted_deterministically():
    result = _evaluate(
        evaluation_at_utc="2026-08-22T15:03:00+00:00",
        max_age_seconds=60.0,
    )

    assert result["freshness"]["age_seconds"] == 60.0
    assert result["freshness"]["passed"] is True
    assert result["operational_evaluation"] == PASS_OUTCOME


def test_stale_timestamp_is_fail_outcome_not_inconclusive():
    result = _evaluate(
        evaluation_at_utc="2026-08-22T15:03:00.000001+00:00",
        max_age_seconds=60.0,
    )

    assert result["freshness"]["age_seconds"] > 60.0
    assert result["operational_evaluation"] == FAIL_OUTCOME


def test_future_plan_timestamp_relative_to_evaluation_fails_closed():
    with pytest.raises(
        NoSubmitPackageEvaluationError,
        match="must not precede",
    ):
        _evaluate(evaluation_at_utc="2026-08-22T15:01:59+00:00")


@pytest.mark.parametrize(
    "evaluation_at_utc",
    [
        "",
        "not-a-timestamp",
        "2026-08-22T15:02:30",
        "2026-08-22T11:02:30-04:00",
        None,
    ],
)
def test_malformed_or_non_utc_evaluation_timestamp_fails_closed(
    evaluation_at_utc,
):
    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(evaluation_at_utc=evaluation_at_utc)


@pytest.mark.parametrize(
    "max_age_seconds",
    [-1, float("nan"), float("inf"), True, "60", None],
)
def test_invalid_freshness_policy_fails_closed(max_age_seconds):
    with pytest.raises(NoSubmitPackageEvaluationError):
        _evaluate(max_age_seconds=max_age_seconds)


def test_require_broker_state_authority_policy_must_be_boolean():
    with pytest.raises(NoSubmitPackageEvaluationError):
        evaluate_no_submit_package(
            package=_package(),
            evaluation_at_utc=EVALUATION_AT,
            max_age_seconds=60.0,
            require_broker_state_authority=1,
        )


def test_no_submit_boundary_is_preserved_in_pass_result():
    result = _evaluate()

    assert result["submission_authorized"] is False
    assert result["order_submitted"] is False
    assert result["orders_submitted"] == 0


def test_attempted_no_submit_mutations_are_rejected_transitively_by_tm030():
    for field, value in (
        ("submission_authorized", True),
        ("order_submitted", True),
        ("orders_submitted", 1),
    ):
        coordinator = _coordinator()
        coordinator[field] = value
        package = _repackage_coordinator(coordinator)

        with pytest.raises(NoSubmitPackageEvaluationError):
            _evaluate(package)


def test_operational_pass_never_implies_economic_or_model_qualification():
    result = _evaluate()

    assert result["operational_evaluation"] == PASS_OUTCOME
    assert result["economic_qualification"] == ECONOMIC_QUALIFICATION
    assert result["economic_qualification"] == "NOT_EVALUATED"
    assert result["model_quality"] == MODEL_QUALITY
    assert result["model_quality"] == "NOT_EVALUATED"
    assert result["execution_readiness"] == EXECUTION_READINESS
    assert result["execution_readiness"] == "NOT_ESTABLISHED"
    assert result["promotion_authorized"] is False
    assert result["order_authorized"] is False


def test_caller_supplied_tm033_broker_state_is_not_treated_as_authoritative():
    package = _package(
        broker_state_before={
            "account": {"equity": "100000", "status": "ACTIVE"},
            "positions": [{"symbol": "AAA", "qty": "100"}],
        },
        broker_state_after={
            "account": {"equity": "100001", "status": "ACTIVE"},
            "positions": [{"symbol": "AAA", "qty": "100"}],
        },
    )

    result = _evaluate(package)

    assert result["operational_evaluation"] == PASS_OUTCOME
    assert result["broker_state_authority"]["established"] is False
    assert result["broker_state_authority"]["source_provenance"] == (
        "caller_supplied_unverified"
    )
    assert "broker_state_before" not in result
    assert "broker_state_after" not in result


def test_broker_authority_requirement_with_same_unverified_data_is_inconclusive():
    package = _package(
        broker_state_before={"account": {"status": "ACTIVE"}},
        broker_state_after={"account": {"status": "ACTIVE"}},
    )

    result = _evaluate(
        package,
        require_broker_state_authority=True,
    )

    assert result["operational_evaluation"] == INCONCLUSIVE_OUTCOME
    assert result["broker_state_authority"]["established"] is False


def test_result_validator_rejects_tampered_identity_or_reason_order():
    result = _evaluate()

    tampered_identity = deepcopy(result)
    tampered_identity["evaluation_id"] = "no_submit_package_evaluation:forged"
    with pytest.raises(NoSubmitPackageEvaluationError):
        validate_no_submit_package_evaluation(tampered_identity)

    tampered_reasons = deepcopy(result)
    tampered_reasons["reason_codes"] = ["STALE_EVIDENCE"]
    with pytest.raises(NoSubmitPackageEvaluationError):
        validate_no_submit_package_evaluation(tampered_reasons)


def test_historical_attribution_is_immutable_and_explicit():
    source = SOURCE_PATH.read_text(encoding="utf-8")

    assert "racoope70/ppo-trading-pipeline" in source
    assert "072103f43d8b2488c3efca183f637ab0508a193a" in source
    assert "src/paper_trading/evaluate_dry_run.py" in source


def test_source_import_surface_has_no_new_third_party_dependency():
    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
    imported_roots: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(
                alias.name.split(".", 1)[0] for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])

    assert imported_roots <= {
        "__future__",
        "copy",
        "datetime",
        "hashlib",
        "json",
        "math",
        "typing",
        "quantitative_trading_research",
    }
    assert "pandas" not in imported_roots
    assert "numpy" not in imported_roots
    assert "requests" not in imported_roots
    assert "alpaca" not in imported_roots


def test_source_has_no_implicit_wall_clock_filesystem_or_environment_access():
    tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))

    forbidden_names = {
        "open",
        "Path",
        "getenv",
        "environ",
        "time",
        "sleep",
    }
    called_names: set[str] = set()
    attributes: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called_names.add(node.func.id)
        if isinstance(node, ast.Attribute):
            attributes.add(node.attr)

    assert called_names.isdisjoint(forbidden_names)
    assert "now" not in attributes
    assert "utcnow" not in attributes
    assert "time" not in attributes
    assert "getenv" not in attributes


def test_module_import_is_offline_and_side_effect_free():
    source_root = ROOT / "src"
    code = r'''
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("pathlib.Path.write_text", side_effect=AssertionError("write called")), \
     patch("pathlib.Path.open", side_effect=AssertionError("file open called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.evaluation.no_submit_package
'''

    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env={
            "PATH": str(Path(sys.executable).parent),
            "PYTHONPATH": str(source_root),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, (
        f"stdout={completed.stdout}\nstderr={completed.stderr}"
    )
