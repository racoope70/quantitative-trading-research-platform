"""Host-neutral C3 configuration boundary.

This module intentionally contains no provider, broker, dataset, model, execution,
or trading configuration. It performs no filesystem or network activity at import.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Mapping

SCHEMA_ID = "C3_HOST_NEUTRAL_CONFIGURATION_SCHEMA_V1"
SCHEMA_VERSION = 1
ALLOWED_KEYS = frozenset({"C3_EVIDENCE_DIRECTORY", "C3_OFFLINE_REQUIRED"})
PROHIBITED_PREFIXES = ("APCA_", "ALPACA_", "BROKER_", "TRADING_", "MARKET_DATA_")
PROHIBITED_HISTORICAL_KEYS = frozenset({
    "TICKERS", "BARS_FEED", "DATA_TIMEFRAME", "TRAIN_TIMEFRAME", "EQUITY_TIMEFRAME",
    "DRY_RUN", "AUTO_RUN_LIVE", "REQUIRE_PAPER", "ALLOW_SHORTS", "USE_FRACTIONALS",
    "WEIGHT_CAP", "SIZING_MODE", "CONF_FLOOR", "ENTER_CONF_MIN", "ENTER_WEIGHT_MIN",
    "EXIT_WEIGHT_MAX", "REBALANCE_MIN_NOTIONAL", "RAW_POS_MIN", "RAW_NEG_MAX",
    "TAKE_PROFIT_PCT", "STOP_LOSS_PCT", "MAX_DAILY_DRAWDOWN_PCT", "GROSS_CAP",
    "NET_CAP", "EMERGENCY_FLATTEN_ON_EXPOSURE", "FLATTEN_INTO_CLOSE", "START_FLAT",
    "EXIT_AFTER_CLOSE", "FORCE_FLATTEN_ON_EXIT", "CLOSE_FLATTEN_MINUTES",
    "CLOSE_FLATTEN_TIMEOUT_SEC", "COOLDOWN_MIN", "STALE_MAX_SEC",
    "ORDER_TIMEOUT_SECONDS", "RECONCILE_DRIFT_THRESHOLD", "SYMBOL_STEP_TIMEOUT_SEC",
    "RUN_VERSION", "CONFIG_CHANGES", "REASON_FOR_CHANGE",
})


class ConfigurationError(ValueError):
    """Fail-closed C3 configuration error."""


@dataclass(frozen=True)
class C3Settings:
    schema_id: str = SCHEMA_ID
    schema_version: int = SCHEMA_VERSION
    evidence_directory: str = ".c3-evidence"
    offline_required: bool = True

    def canonical_payload(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode("utf-8")

    def checksum_sha256(self) -> str:
        return hashlib.sha256(self.canonical_payload()).hexdigest()


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes"}:
        return True
    if normalized in {"0", "false", "no"}:
        return False
    raise ConfigurationError("C3_OFFLINE_REQUIRED must be a boolean literal")


def settings_from_mapping(values: Mapping[str, str]) -> C3Settings:
    prohibited = sorted(
        k for k in values
        if k.startswith(PROHIBITED_PREFIXES) or k in PROHIBITED_HISTORICAL_KEYS
    )
    if prohibited:
        raise ConfigurationError(f"known operational/later-phase variables are prohibited during C3: {prohibited}")
    unexpected = sorted(k for k in values if k.startswith("C3_") and k not in ALLOWED_KEYS)
    if unexpected:
        raise ConfigurationError(f"unsupported C3 settings: {unexpected}")

    evidence_directory = values.get("C3_EVIDENCE_DIRECTORY", ".c3-evidence").strip()
    if not evidence_directory or evidence_directory.startswith("/") or ".." in evidence_directory.split("/"):
        raise ConfigurationError("C3_EVIDENCE_DIRECTORY must be a nonempty relative path without '..'")

    offline_required = _parse_bool(values.get("C3_OFFLINE_REQUIRED", "true"))
    if not offline_required:
        raise ConfigurationError("offline execution is mandatory in the host-neutral C3 preparation boundary")

    return C3Settings(evidence_directory=evidence_directory, offline_required=offline_required)
