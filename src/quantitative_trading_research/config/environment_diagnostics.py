"""Deterministic, host-neutral C3 environment diagnostics.

No networking, package installation, provider access, dataset access, or model
execution occurs here. Results are development evidence only until the later
scientific-host admission path is completed.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from typing import Iterable

from .settings import C3Settings

DIAGNOSTIC_SCHEMA_ID = "C3_HOST_NEUTRAL_ENVIRONMENT_DIAGNOSTIC_V1"
TERMINAL_OUTCOMES = {
    "PASS",
    "FAIL_MISSING_PACKAGE",
    "FAIL_INCOMPATIBLE_VERSION",
    "FAIL_INVALID_IMPORT_TARGET",
    "FAIL_CONFIGURATION",
    "FAIL_IDENTITY_MISMATCH",
    "FAIL_PROHIBITED_NETWORK_ATTEMPT",
    "FAIL_PROHIBITED_SECRET_EXPOSURE",
    "FAIL_OTHER",
    "INCONCLUSIVE",
}
CANONICAL_IMPORT_TARGETS = (
    "quantitative_trading_research",
    "quantitative_trading_research.config",
)


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_import_targets(targets: Iterable[str] = CANONICAL_IMPORT_TARGETS) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for target in targets:
        try:
            importlib.import_module(target)
        except ModuleNotFoundError:
            status = "FAIL_MISSING_PACKAGE"
        except Exception:
            status = "FAIL_INVALID_IMPORT_TARGET"
        else:
            status = "PASS"
        results.append({"target": target, "status": status})
    return results


def collect_static_diagnostic(repo_root: Path, settings: C3Settings) -> dict[str, object]:
    pyproject = repo_root / "pyproject.toml"
    lock = repo_root / "requirements.lock"
    imports = inspect_import_targets()
    terminal = "PASS" if all(item["status"] == "PASS" for item in imports) else "INCONCLUSIVE"
    return {
        "schema_id": DIAGNOSTIC_SCHEMA_ID,
        "scope": "HOST_NEUTRAL_NON_CONTROLLING_STATIC_OFFLINE_PREPARATION",
        "scientific_host_status": "UNRESOLVED_FREEZE_BLOCKER_001",
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
        },
        "dependency": {
            "pyproject_sha256": sha256_file(pyproject),
            "lock_sha256": sha256_file(lock),
            "lock_status": "PRESENT" if lock.is_file() else "UNRESOLVED_NOT_GENERATED",
            "source_allowlist_id": "C3_DEPENDENCY_SOURCE_ALLOWLIST_V1",
        },
        "configuration": {
            "schema_id": settings.schema_id,
            "checksum_sha256": settings.checksum_sha256(),
            "offline_required": settings.offline_required,
        },
        "canonical_import_targets": imports,
        "terminal_outcome": terminal,
    }


def atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
