#!/usr/bin/env python3
"""Generic read-only successor E1 V1 collection primitives.

Identity: C3_E1_SUCCESSOR_GENERIC_COLLECTOR_V1

This generic package is intentionally not execution-ready. Provider-specific
runtime-instantiation, observation-authority, transition-event, and optional
build-output adapters remain absent and therefore can never produce PASS.

The helpers below preserve the accepted kernel and logical-command semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

COLLECTOR_IDENTITY = "C3_E1_SUCCESSOR_GENERIC_COLLECTOR_V1"
IMPLEMENTATION_STATUS = "STATIC_GENERIC_FAIL_CLOSED_IMPLEMENTATION_ONLY"
PRE_EXECUTION_READINESS = "NOT_READY"
EXECUTION_AUTHORIZATION = "NOT_AUTHORIZED"

DEFERRED_ADAPTERS = (
    "runtime_instantiation_attestation_adapter",
    "observation_authority_observation_adapter",
    "transition_event_evidence_adapter",
)


class CollectorError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def path_identity(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "absolute_path": str(path),
        "exists": path.exists(),
        "regular_file": False,
        "readable": False,
        "uid": None,
        "gid": None,
        "mode_octal": None,
        "byte_count": None,
        "sha256": None,
    }
    try:
        st = path.stat()
    except OSError:
        return result
    result.update(
        regular_file=stat.S_ISREG(st.st_mode),
        readable=os.access(path, os.R_OK),
        uid=st.st_uid,
        gid=st.st_gid,
        mode_octal=f"{stat.S_IMODE(st.st_mode):04o}",
        byte_count=st.st_size,
    )
    if result["regular_file"] and result["readable"]:
        try:
            result["sha256"] = sha256_file(path)
        except OSError:
            pass
    return result


def run_exact(argv: list[str]) -> dict[str, Any]:
    if not argv or not os.path.isabs(argv[0]):
        raise CollectorError("argv[0] must be an absolute logical invocation path")
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "LC_ALL": "C", "LANG": "C"},
    )
    return {
        "argv": argv,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
        "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
    }


def resolved_implementation_identity(logical_path: str) -> dict[str, Any]:
    logical = Path(logical_path)
    try:
        resolved = logical.resolve(strict=True)
    except OSError:
        return {
            "logical_absolute_path": logical_path,
            "resolved_absolute_path": None,
            "identity": None,
        }
    return {
        "logical_absolute_path": logical_path,
        "resolved_absolute_path": str(resolved),
        "identity": path_identity(resolved),
    }


def collect_modinfo(module_name: str, logical_modinfo_path: str = "/usr/sbin/modinfo") -> dict:
    """Execute the logical modinfo entrypoint; never execute resolved kmod instead."""
    if "/" in module_name or not module_name:
        raise CollectorError("invalid module name")
    logical = Path(logical_modinfo_path)
    return {
        "module_name": module_name,
        "module_query_logical_invocation_identity": {
            "absolute_path": logical_modinfo_path,
            "argv": [logical_modinfo_path, module_name],
            "path_lstat_exists": logical.exists() or logical.is_symlink(),
        },
        "module_query_resolved_implementation_identity":
            resolved_implementation_identity(logical_modinfo_path),
        "module_query_execution":
            run_exact([logical_modinfo_path, module_name]),
    }


def _release_matches(path: str, release: str) -> bool:
    name = os.path.basename(path)
    return name == f"vmlinuz-{release}" or (
        release in path and ("vmlinuz" in name or name == "vmlinuz")
    )


def discover_running_kernel_image(kernel_release: str) -> dict[str, Any]:
    """Retain dpkg-query rc/stdout/stderr plus every candidate disposition."""
    package = f"linux-image-{kernel_release}"
    query = run_exact(["/usr/bin/dpkg-query", "-L", package])

    raw_paths: list[str] = []
    if query["exit_code"] == 0:
        raw_paths.extend(
            line.strip() for line in query["stdout"].splitlines() if line.strip()
        )
    raw_paths.extend(
        [
            f"/boot/vmlinuz-{kernel_release}",
            f"/usr/lib/modules/{kernel_release}/vmlinuz",
        ]
    )

    matched = sorted(
        {p for p in raw_paths if os.path.isabs(p) and _release_matches(p, kernel_release)}
    )
    candidates: list[dict[str, Any]] = []
    qualifying: list[dict[str, Any]] = []
    for candidate_path in matched:
        ident = path_identity(Path(candidate_path))
        record = {
            "path": candidate_path,
            "exists": ident["exists"],
            "regular_file": ident["regular_file"],
            "readable": ident["readable"],
            "identity": ident if ident["regular_file"] and ident["readable"] else None,
        }
        candidates.append(record)
        if record["exists"] and record["regular_file"] and record["readable"]:
            qualifying.append(record)

    if query["exit_code"] != 0:
        selection = "QUERY_FAILED"
    elif len(qualifying) == 1:
        selection = "EXACTLY_ONE"
    elif len(qualifying) == 0:
        selection = "ZERO"
    else:
        selection = "MULTIPLE"

    return {
        "kernel_release": kernel_release,
        "package": package,
        "dpkg_query": query,
        "all_release_matched_candidates": candidates,
        "candidate_count": len(candidates),
        "qualifying_candidate_count": len(qualifying),
        "selection_result": selection,
        "selected_file": qualifying[0] if selection == "EXACTLY_ONE" else None,
    }


def collect_logical_command(
    logical_name: str,
    logical_path: str,
    argv_suffix: list[str],
) -> dict[str, Any]:
    """Preserve logical invocation while separately binding resolved implementation."""
    argv = [logical_path, *argv_suffix]
    return {
        "logical_name": logical_name,
        "logical_invocation_identity": {
            "absolute_path": logical_path,
            "argv": argv,
            "path_lstat_exists": Path(logical_path).exists()
                or Path(logical_path).is_symlink(),
        },
        "resolved_implementation_identity":
            resolved_implementation_identity(logical_path),
        "execution": run_exact(argv),
    }


def generic_status() -> dict[str, Any]:
    return {
        "collector_identity": COLLECTOR_IDENTITY,
        "implementation_status": IMPLEMENTATION_STATUS,
        "successor_pre_execution_readiness": PRE_EXECUTION_READINESS,
        "successor_execution_authorization": EXECUTION_AUTHORIZATION,
        "missing_future_adapters": list(DEFERRED_ADAPTERS),
        "missing_future_adapter_semantics":
            "INCONCLUSIVE_OR_NOT_EXECUTED_NEVER_PASS",
        "specific_VM_platform": "DEFERRED",
        "specific_observation_authority_mechanism": "DEFERRED",
        "CAP_NET_ADMIN_sufficiency": "NOT_ESTABLISHED",
        "transition_event_provider": "DEFERRED",
    }


def self_test() -> dict[str, str]:
    # Verify command-construction semantics without executing system commands.
    logical_modinfo = "/usr/sbin/modinfo"
    modinfo_argv = [logical_modinfo, "eb_tables"]
    if modinfo_argv[0] != logical_modinfo:
        raise AssertionError("modinfo logical invocation lost")

    xtables = "/usr/sbin/iptables-nft-save"
    argv = [xtables]
    if argv[0] != xtables:
        raise AssertionError("xtables logical invocation lost")

    status = generic_status()
    if status["successor_pre_execution_readiness"] != "NOT_READY":
        raise AssertionError("generic collector became ready")
    if status["successor_execution_authorization"] != "NOT_AUTHORIZED":
        raise AssertionError("generic collector became authorized")
    return {
        "logical_modinfo_invocation": "PASS",
        "logical_xtables_invocation": "PASS",
        "generic_fail_closed_status": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--generic-status", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return 0
    if args.generic_status:
        print(json.dumps(generic_status(), sort_keys=True))
        return 0
    raise SystemExit(
        "generic successor V1 collector is not execution-ready; "
        "required environment/adapters remain deferred"
    )


if __name__ == "__main__":
    raise SystemExit(main())
