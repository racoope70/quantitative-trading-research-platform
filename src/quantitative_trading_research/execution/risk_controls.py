"""Pure offline fail-closed risk-control evaluation.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/paper_trading/risk_controls.py``.

The historical source combined reusable deterministic risk-limit checks with
pandas dataframes, filesystem loading, CLI behavior, and paper-trading
terminology. This C4 module preserves only pure provider-neutral risk-control
evaluation from explicit caller-supplied or mocked state.

``target_weight``, ``current_weight``, and ``equity`` are authoritative input
primitives. Delta weight and intended notional are derived deterministically.
If a caller supplies either redundant derivative, it must agree exactly with
the canonical arithmetic or evaluation fails closed.

This module performs no filesystem or network operations, obtains no provider
or broker state, submits no orders, performs no training or inference, and
accesses no canonical dataset or final holdout.
"""

from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Any


SCHEMA_ID = "C4_OFFLINE_RISK_CONTROL_V1"
SCHEMA_VERSION = 1
RESULT_TYPE = "offline_risk_control_result"
STATE_PROVENANCE = "caller_supplied_unverified"

_BASE_CHECK_NAMES = (
    "equity_above_minimum",
    "plan_equity_consistent",
    "single_symbol_target_weight_within_limit",
    "gross_target_weight_within_limit",
    "net_target_weight_within_limit",
    "no_prior_orders_submitted",
    "single_intended_notional_within_limit",
    "total_intended_notional_within_limit",
)

_PLAN_REQUIRED_KEYS = {
    "instrument_id",
    "target_weight",
    "current_weight",
    "equity",
    "order_submitted",
}

_PLAN_OPTIONAL_KEYS = {
    "intended_delta_weight",
    "intended_notional",
    "observed_at_utc",
}

_EVALUATED_ROW_REQUIRED_KEYS = {
    "instrument_id",
    "target_weight",
    "current_weight",
    "equity",
    "canonical_delta_weight",
    "canonical_intended_notional",
    "order_submitted",
}

_EVALUATED_ROW_OPTIONAL_KEYS = {
    "observed_at_utc",
}

_ACCOUNT_KEYS = {
    "open_orders_count",
    "positions_count",
}

_RESULT_KEYS = {
    "schema_id",
    "schema_version",
    "result_type",
    "state_provenance",
    "passed",
    "configuration",
    "account_state",
    "evaluation_context",
    "evaluated_rows",
    "checks",
}

_CHECK_KEYS = {
    "name",
    "passed",
    "severity",
    "evidence",
}


class RiskControlError(ValueError):
    """Fail-closed error for malformed risk input or result evidence."""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RiskControlError(f"{name} must be a dict")
    return dict(value)


def _require_bool(name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise RiskControlError(f"{name} must be a bool")
    return value


def _require_nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RiskControlError(f"{name} must be a non-empty string")
    return value


def _require_finite_number(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RiskControlError(f"{name} must be a finite number")

    numeric = float(value)
    if not math.isfinite(numeric):
        raise RiskControlError(f"{name} must be a finite number")

    return numeric


def _require_nonnegative_integer(name: str, value: Any) -> int:
    if type(value) is not int or value < 0:
        raise RiskControlError(f"{name} must be a non-negative integer")
    return value


def _parse_utc_timestamp(name: str, value: Any) -> datetime:
    text = _require_nonempty_string(name, value)

    try:
        normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise RiskControlError(
            f"{name} must be an ISO-8601 timestamp"
        ) from exc

    if parsed.tzinfo is None:
        raise RiskControlError(f"{name} must include timezone information")

    return parsed.astimezone(timezone.utc)


def _canonical_timestamp(name: str, value: Any) -> str:
    return _parse_utc_timestamp(name, value).isoformat()


def _check(
    name: str,
    passed: bool,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "severity": "ERROR",
        "evidence": evidence,
    }


def _validated_config(config: dict[str, Any] | None) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "max_abs_symbol_weight": 0.40,
        "max_gross_target_weight": 1.00,
        "max_net_target_weight": 0.80,
        "max_single_intended_notional_pct": 0.40,
        "max_total_intended_notional_pct": 1.00,
        "min_equity": 1.0,
        "require_no_open_orders": True,
        "require_flat_start": False,
        "flat_weight_tolerance": 1e-6,
        "max_state_age_minutes": None,
    }

    supplied = {} if config is None else _require_mapping("config", config)
    unexpected = sorted(set(supplied) - set(defaults))
    if unexpected:
        raise RiskControlError(
            "unexpected risk-control config keys: " + ",".join(unexpected)
        )

    merged = defaults | supplied

    for field in (
        "max_abs_symbol_weight",
        "max_gross_target_weight",
        "max_net_target_weight",
        "max_single_intended_notional_pct",
        "max_total_intended_notional_pct",
        "min_equity",
        "flat_weight_tolerance",
    ):
        merged[field] = _require_finite_number(field, merged[field])
        if merged[field] < 0:
            raise RiskControlError(f"{field} must be non-negative")

    for field in (
        "require_no_open_orders",
        "require_flat_start",
    ):
        merged[field] = _require_bool(field, merged[field])

    max_age = merged["max_state_age_minutes"]
    if max_age is not None:
        max_age = _require_finite_number(
            "max_state_age_minutes",
            max_age,
        )
        if max_age < 0:
            raise RiskControlError(
                "max_state_age_minutes must be non-negative"
            )
        merged["max_state_age_minutes"] = max_age

    return merged


def _validated_account_state(
    account_state: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if account_state is None:
        return None

    account = _require_mapping("account_state", account_state)
    unexpected = sorted(set(account) - _ACCOUNT_KEYS)
    if unexpected:
        raise RiskControlError(
            "unexpected account_state keys: " + ",".join(unexpected)
        )

    normalized: dict[str, Any] = {}

    if "open_orders_count" in account:
        normalized["open_orders_count"] = _require_nonnegative_integer(
            "account_state.open_orders_count",
            account["open_orders_count"],
        )

    if "positions_count" in account:
        normalized["positions_count"] = _require_nonnegative_integer(
            "account_state.positions_count",
            account["positions_count"],
        )

    return normalized


def _validated_plan_rows(plan_rows: Any) -> list[dict[str, Any]]:
    if not isinstance(plan_rows, list):
        raise RiskControlError("plan_rows must be a list")

    if not plan_rows:
        raise RiskControlError("plan_rows must not be empty")

    validated: list[dict[str, Any]] = []
    seen_instruments: set[str] = set()

    allowed_keys = _PLAN_REQUIRED_KEYS | _PLAN_OPTIONAL_KEYS

    for index, raw_row in enumerate(plan_rows):
        row = _require_mapping(f"plan_rows[{index}]", raw_row)

        missing = sorted(_PLAN_REQUIRED_KEYS - set(row))
        if missing:
            raise RiskControlError(
                f"plan_rows[{index}] missing required keys: "
                + ",".join(missing)
            )

        unexpected = sorted(set(row) - allowed_keys)
        if unexpected:
            raise RiskControlError(
                f"plan_rows[{index}] has unexpected keys: "
                + ",".join(unexpected)
            )

        instrument_id = _require_nonempty_string(
            f"plan_rows[{index}].instrument_id",
            row["instrument_id"],
        )
        if instrument_id in seen_instruments:
            raise RiskControlError(
                f"duplicate instrument_id: {instrument_id}"
            )
        seen_instruments.add(instrument_id)

        target_weight = _require_finite_number(
            f"plan_rows[{index}].target_weight",
            row["target_weight"],
        )
        current_weight = _require_finite_number(
            f"plan_rows[{index}].current_weight",
            row["current_weight"],
        )
        equity = _require_finite_number(
            f"plan_rows[{index}].equity",
            row["equity"],
        )
        order_submitted = _require_bool(
            f"plan_rows[{index}].order_submitted",
            row["order_submitted"],
        )

        canonical_delta_weight = target_weight - current_weight
        canonical_intended_notional = canonical_delta_weight * equity

        if not math.isfinite(canonical_delta_weight):
            raise RiskControlError(
                f"plan_rows[{index}] derived delta weight is non-finite"
            )

        if not math.isfinite(canonical_intended_notional):
            raise RiskControlError(
                f"plan_rows[{index}] derived intended notional is non-finite"
            )

        if "intended_delta_weight" in row:
            supplied_delta = _require_finite_number(
                f"plan_rows[{index}].intended_delta_weight",
                row["intended_delta_weight"],
            )
            if supplied_delta != canonical_delta_weight:
                raise RiskControlError(
                    f"plan_rows[{index}].intended_delta_weight "
                    "contradicts canonical arithmetic"
                )

        if "intended_notional" in row:
            supplied_notional = _require_finite_number(
                f"plan_rows[{index}].intended_notional",
                row["intended_notional"],
            )
            if supplied_notional != canonical_intended_notional:
                raise RiskControlError(
                    f"plan_rows[{index}].intended_notional "
                    "contradicts canonical arithmetic"
                )

        normalized: dict[str, Any] = {
            "instrument_id": instrument_id,
            "target_weight": target_weight,
            "current_weight": current_weight,
            "equity": equity,
            "canonical_delta_weight": canonical_delta_weight,
            "canonical_intended_notional": canonical_intended_notional,
            "order_submitted": order_submitted,
        }

        if "observed_at_utc" in row:
            normalized["observed_at_utc"] = _canonical_timestamp(
                f"plan_rows[{index}].observed_at_utc",
                row["observed_at_utc"],
            )

        validated.append(normalized)

    return validated


def _validated_evaluated_rows(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or not rows:
        raise RiskControlError(
            "risk result evaluated_rows must be a non-empty list"
        )

    validated: list[dict[str, Any]] = []
    seen_instruments: set[str] = set()
    allowed = (
        _EVALUATED_ROW_REQUIRED_KEYS
        | _EVALUATED_ROW_OPTIONAL_KEYS
    )

    for index, raw_row in enumerate(rows):
        row = _require_mapping(
            f"risk result evaluated_rows[{index}]",
            raw_row,
        )

        if set(row) - allowed:
            raise RiskControlError(
                f"risk result evaluated_rows[{index}] has unexpected keys"
            )

        missing = _EVALUATED_ROW_REQUIRED_KEYS - set(row)
        if missing:
            raise RiskControlError(
                f"risk result evaluated_rows[{index}] missing required keys"
            )

        instrument_id = _require_nonempty_string(
            f"risk result evaluated_rows[{index}].instrument_id",
            row["instrument_id"],
        )
        if instrument_id in seen_instruments:
            raise RiskControlError(
                "risk result evaluated_rows contains duplicate instruments"
            )
        seen_instruments.add(instrument_id)

        target_weight = _require_finite_number(
            f"risk result evaluated_rows[{index}].target_weight",
            row["target_weight"],
        )
        current_weight = _require_finite_number(
            f"risk result evaluated_rows[{index}].current_weight",
            row["current_weight"],
        )
        equity = _require_finite_number(
            f"risk result evaluated_rows[{index}].equity",
            row["equity"],
        )
        canonical_delta_weight = _require_finite_number(
            (
                f"risk result evaluated_rows[{index}]"
                ".canonical_delta_weight"
            ),
            row["canonical_delta_weight"],
        )
        canonical_intended_notional = _require_finite_number(
            (
                f"risk result evaluated_rows[{index}]"
                ".canonical_intended_notional"
            ),
            row["canonical_intended_notional"],
        )
        order_submitted = _require_bool(
            f"risk result evaluated_rows[{index}].order_submitted",
            row["order_submitted"],
        )

        expected_delta = target_weight - current_weight
        if canonical_delta_weight != expected_delta:
            raise RiskControlError(
                "risk result canonical_delta_weight is inconsistent"
            )

        expected_notional = expected_delta * equity
        if canonical_intended_notional != expected_notional:
            raise RiskControlError(
                "risk result canonical_intended_notional is inconsistent"
            )

        normalized: dict[str, Any] = {
            "instrument_id": instrument_id,
            "target_weight": target_weight,
            "current_weight": current_weight,
            "equity": equity,
            "canonical_delta_weight": canonical_delta_weight,
            "canonical_intended_notional": canonical_intended_notional,
            "order_submitted": order_submitted,
        }

        if "observed_at_utc" in row:
            normalized["observed_at_utc"] = _canonical_timestamp(
                (
                    f"risk result evaluated_rows[{index}]"
                    ".observed_at_utc"
                ),
                row["observed_at_utc"],
            )

        validated.append(normalized)

    return validated


def _expected_check_names(config: dict[str, Any]) -> tuple[str, ...]:
    names = list(_BASE_CHECK_NAMES)

    if config["require_no_open_orders"]:
        names.append("no_open_orders")

    if config["require_flat_start"]:
        names.extend(
            (
                "account_positions_flat",
                "plan_current_weights_flat",
            )
        )

    if config["max_state_age_minutes"] is not None:
        names.append("state_not_stale")

    return tuple(names)


def _build_checks(
    *,
    rows: list[dict[str, Any]],
    account_state: dict[str, Any] | None,
    config: dict[str, Any],
    now_utc: str | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    equities = [row["equity"] for row in rows]
    reference_equity = equities[0]
    minimum_equity = min(equities)

    checks.append(
        _check(
            "equity_above_minimum",
            all(
                equity >= config["min_equity"]
                for equity in equities
            ),
            {
                "minimum_observed_equity": minimum_equity,
                "required_minimum_equity": config["min_equity"],
            },
        )
    )

    checks.append(
        _check(
            "plan_equity_consistent",
            all(equity == reference_equity for equity in equities),
            {
                "reference_equity": reference_equity,
                "observed_equities": list(equities),
            },
        )
    )

    target_weights = [row["target_weight"] for row in rows]
    max_abs_target_weight = max(abs(value) for value in target_weights)

    checks.append(
        _check(
            "single_symbol_target_weight_within_limit",
            (
                max_abs_target_weight
                <= config["max_abs_symbol_weight"]
            ),
            {
                "maximum_absolute_target_weight": max_abs_target_weight,
                "configured_limit": config["max_abs_symbol_weight"],
            },
        )
    )

    gross_target_weight = sum(abs(value) for value in target_weights)
    checks.append(
        _check(
            "gross_target_weight_within_limit",
            (
                gross_target_weight
                <= config["max_gross_target_weight"]
            ),
            {
                "gross_target_weight": gross_target_weight,
                "configured_limit": config["max_gross_target_weight"],
            },
        )
    )

    net_target_weight = abs(sum(target_weights))
    checks.append(
        _check(
            "net_target_weight_within_limit",
            net_target_weight <= config["max_net_target_weight"],
            {
                "absolute_net_target_weight": net_target_weight,
                "configured_limit": config["max_net_target_weight"],
            },
        )
    )

    submitted_count = sum(
        1 for row in rows if row["order_submitted"]
    )
    checks.append(
        _check(
            "no_prior_orders_submitted",
            submitted_count == 0,
            {
                "submitted_row_count": submitted_count,
            },
        )
    )

    intended_notionals = [
        abs(row["canonical_intended_notional"])
        for row in rows
    ]

    if reference_equity > 0:
        max_single_notional_pct = (
            max(intended_notionals) / reference_equity
        )
        total_notional_pct = (
            sum(intended_notionals) / reference_equity
        )
    else:
        max_single_notional_pct = math.inf
        total_notional_pct = math.inf

    checks.append(
        _check(
            "single_intended_notional_within_limit",
            (
                math.isfinite(max_single_notional_pct)
                and max_single_notional_pct
                <= config["max_single_intended_notional_pct"]
            ),
            {
                "maximum_intended_notional_pct": max_single_notional_pct,
                "configured_limit": (
                    config["max_single_intended_notional_pct"]
                ),
            },
        )
    )

    checks.append(
        _check(
            "total_intended_notional_within_limit",
            (
                math.isfinite(total_notional_pct)
                and total_notional_pct
                <= config["max_total_intended_notional_pct"]
            ),
            {
                "total_intended_notional_pct": total_notional_pct,
                "configured_limit": (
                    config["max_total_intended_notional_pct"]
                ),
            },
        )
    )

    if config["require_no_open_orders"]:
        if (
            account_state is None
            or "open_orders_count" not in account_state
        ):
            checks.append(
                _check(
                    "no_open_orders",
                    False,
                    {
                        "required_state_missing": True,
                        "open_orders_count": None,
                    },
                )
            )
        else:
            open_orders_count = account_state["open_orders_count"]
            checks.append(
                _check(
                    "no_open_orders",
                    open_orders_count == 0,
                    {
                        "required_state_missing": False,
                        "open_orders_count": open_orders_count,
                    },
                )
            )

    if config["require_flat_start"]:
        if (
            account_state is None
            or "positions_count" not in account_state
        ):
            checks.append(
                _check(
                    "account_positions_flat",
                    False,
                    {
                        "required_state_missing": True,
                        "positions_count": None,
                    },
                )
            )
        else:
            positions_count = account_state["positions_count"]
            checks.append(
                _check(
                    "account_positions_flat",
                    positions_count == 0,
                    {
                        "required_state_missing": False,
                        "positions_count": positions_count,
                    },
                )
            )

        max_abs_current_weight = max(
            abs(row["current_weight"])
            for row in rows
        )
        tolerance = config["flat_weight_tolerance"]

        checks.append(
            _check(
                "plan_current_weights_flat",
                max_abs_current_weight <= tolerance,
                {
                    "maximum_absolute_current_weight": (
                        max_abs_current_weight
                    ),
                    "configured_tolerance": tolerance,
                },
            )
        )

    max_age = config["max_state_age_minutes"]
    if max_age is not None:
        missing_timestamp_count = sum(
            1 for row in rows if "observed_at_utc" not in row
        )

        if now_utc is None or missing_timestamp_count:
            checks.append(
                _check(
                    "state_not_stale",
                    False,
                    {
                        "missing_now_utc": now_utc is None,
                        "missing_timestamp_count": (
                            missing_timestamp_count
                        ),
                        "minimum_age_minutes": None,
                        "maximum_age_minutes": None,
                        "configured_limit_minutes": max_age,
                        "future_timestamp_present": None,
                        "stale_timestamp_present": None,
                    },
                )
            )
        else:
            now = _parse_utc_timestamp("now_utc", now_utc)
            timestamps = [
                _parse_utc_timestamp(
                    "observed_at_utc",
                    row["observed_at_utc"],
                )
                for row in rows
            ]

            ages_minutes = [
                (now - timestamp).total_seconds() / 60.0
                for timestamp in timestamps
            ]

            minimum_age = min(ages_minutes)
            maximum_age = max(ages_minutes)
            future_present = any(age < 0.0 for age in ages_minutes)
            stale_present = any(age > max_age for age in ages_minutes)

            checks.append(
                _check(
                    "state_not_stale",
                    not future_present and not stale_present,
                    {
                        "missing_now_utc": False,
                        "missing_timestamp_count": 0,
                        "minimum_age_minutes": minimum_age,
                        "maximum_age_minutes": maximum_age,
                        "configured_limit_minutes": max_age,
                        "future_timestamp_present": future_present,
                        "stale_timestamp_present": stale_present,
                    },
                )
            )

    return checks


def evaluate_risk_controls(
    *,
    plan_rows: list[dict[str, Any]],
    account_state: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    """Evaluate deterministic risk limits from explicit provider-neutral state."""
    rows = _validated_plan_rows(plan_rows)
    cfg = _validated_config(config)
    account = _validated_account_state(account_state)

    normalized_now: str | None = None
    if now_utc is not None:
        normalized_now = _canonical_timestamp("now_utc", now_utc)

    checks = _build_checks(
        rows=rows,
        account_state=account,
        config=cfg,
        now_utc=normalized_now,
    )

    result = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "result_type": RESULT_TYPE,
        "state_provenance": STATE_PROVENANCE,
        "passed": all(check["passed"] for check in checks),
        "configuration": cfg,
        "account_state": account,
        "evaluation_context": {
            "now_utc": normalized_now,
        },
        "evaluated_rows": rows,
        "checks": checks,
    }

    validate_risk_result(result)
    return result


def validate_risk_result(result: Any) -> None:
    """Fail closed on malformed, incomplete, or forged result evidence."""
    if not isinstance(result, dict):
        raise RiskControlError("risk result must be a dict")

    if set(result) != _RESULT_KEYS:
        missing = sorted(_RESULT_KEYS - set(result))
        unexpected = sorted(set(result) - _RESULT_KEYS)
        raise RiskControlError(
            "risk result keys mismatch: "
            f"missing={missing}; unexpected={unexpected}"
        )

    if result["schema_id"] != SCHEMA_ID:
        raise RiskControlError("unsupported risk result schema_id")

    if type(result["schema_version"]) is not int:
        raise RiskControlError(
            "risk result schema_version must be an int"
        )

    if result["schema_version"] != SCHEMA_VERSION:
        raise RiskControlError(
            "unsupported risk result schema_version"
        )

    if result["result_type"] != RESULT_TYPE:
        raise RiskControlError("unsupported risk result type")

    if result["state_provenance"] != STATE_PROVENANCE:
        raise RiskControlError(
            "risk result state provenance must remain caller-supplied "
            "and unverified"
        )

    passed = _require_bool(
        "risk result passed",
        result["passed"],
    )

    config = _validated_config(
        _require_mapping(
            "risk result configuration",
            result["configuration"],
        )
    )

    account = _validated_account_state(result["account_state"])

    context = _require_mapping(
        "risk result evaluation_context",
        result["evaluation_context"],
    )
    if set(context) != {"now_utc"}:
        raise RiskControlError(
            "risk result evaluation_context keys mismatch"
        )

    now_utc = context["now_utc"]
    if now_utc is not None:
        now_utc = _canonical_timestamp(
            "risk result evaluation_context.now_utc",
            now_utc,
        )

    rows = _validated_evaluated_rows(result["evaluated_rows"])

    checks = result["checks"]
    if not isinstance(checks, list) or not checks:
        raise RiskControlError(
            "risk result checks must be a non-empty list"
        )

    supplied_names: list[str] = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise RiskControlError(
                f"risk result checks[{index}] must be a dict"
            )

        if set(check) != _CHECK_KEYS:
            raise RiskControlError(
                f"risk result checks[{index}] keys mismatch"
            )

        name = _require_nonempty_string(
            f"risk result checks[{index}].name",
            check["name"],
        )
        supplied_names.append(name)

        _require_bool(
            f"risk result checks[{index}].passed",
            check["passed"],
        )

        if check["severity"] != "ERROR":
            raise RiskControlError(
                f"risk result checks[{index}].severity must be ERROR"
            )

        if not isinstance(check["evidence"], dict):
            raise RiskControlError(
                f"risk result checks[{index}].evidence must be a dict"
            )

    if len(supplied_names) != len(set(supplied_names)):
        raise RiskControlError(
            "risk result contains duplicate check identifiers"
        )

    expected_names = _expected_check_names(config)
    if tuple(supplied_names) != expected_names:
        unknown = sorted(set(supplied_names) - set(expected_names))
        missing = sorted(set(expected_names) - set(supplied_names))
        raise RiskControlError(
            "risk result check-set mismatch: "
            f"unknown={unknown}; missing={missing}"
        )

    expected_checks = _build_checks(
        rows=rows,
        account_state=account,
        config=config,
        now_utc=now_utc,
    )

    if checks != expected_checks:
        raise RiskControlError(
            "risk result check evidence does not match canonical evaluation"
        )

    expected_passed = all(
        check["passed"]
        for check in expected_checks
    )
    if passed is not expected_passed:
        raise RiskControlError(
            "risk result passed does not match canonical check aggregation"
        )
