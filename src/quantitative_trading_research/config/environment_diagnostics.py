"""Deterministic, fail-closed C3 environment diagnostics.

The module is inert on import. Diagnostics and evidence writes occur only
through explicit function calls.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
import hashlib
import importlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import re
import stat
import sys
import sysconfig
from typing import Final

from quantitative_trading_research.config.settings import EnvironmentSettings


DIAGNOSTIC_SCHEMA_VERSION: Final[str] = (
    "C3_ENVIRONMENT_DIAGNOSTIC_EVIDENCE_V1"
)
ENVIRONMENT_IDENTITY_SCHEMA_VERSION: Final[str] = (
    "C3_CANONICAL_ENVIRONMENT_IDENTITY_V1"
)
DEPENDENCY_METADATA_SCHEMA_VERSION: Final[str] = "C3_DEPENDENCY_METADATA_V1"

CANONICAL_IMPORT_TARGETS: Final[tuple[str, ...]] = (
    "quantitative_trading_research",
    "quantitative_trading_research.config",
    "quantitative_trading_research.config.settings",
    "quantitative_trading_research.config.environment_diagnostics",
)

IMPORT_PASS: Final[str] = "PASS"
IMPORT_MISSING_PACKAGE: Final[str] = "MISSING_PACKAGE"
IMPORT_INCOMPATIBLE_VERSION: Final[str] = "INCOMPATIBLE_VERSION"
IMPORT_INVALID_TARGET: Final[str] = "INVALID_TARGET"
IMPORT_OTHER: Final[str] = "OTHER"
IMPORT_INCONCLUSIVE: Final[str] = "INCONCLUSIVE"

OVERALL_PASS: Final[str] = "PASS"
FAIL_MISSING_PACKAGE: Final[str] = "FAIL_MISSING_PACKAGE"
FAIL_INCOMPATIBLE_VERSION: Final[str] = "FAIL_INCOMPATIBLE_VERSION"
FAIL_INVALID_IMPORT_TARGET: Final[str] = "FAIL_INVALID_IMPORT_TARGET"
FAIL_CONFIGURATION: Final[str] = "FAIL_CONFIGURATION"
FAIL_IDENTITY_MISMATCH: Final[str] = "FAIL_IDENTITY_MISMATCH"
FAIL_PROHIBITED_NETWORK_ATTEMPT: Final[str] = (
    "FAIL_PROHIBITED_NETWORK_ATTEMPT"
)
FAIL_PROHIBITED_SECRET_EXPOSURE: Final[str] = (
    "FAIL_PROHIBITED_SECRET_EXPOSURE"
)
FAIL_OTHER: Final[str] = "FAIL_OTHER"
INCONCLUSIVE: Final[str] = "INCONCLUSIVE"

_SHA256_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_IMPORT_TARGET_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$"
)

_ACCEPTED_LIMITATIONS: Final[tuple[str, ...]] = (
    "C2-LIM-C3-001",
    "C2-LIM-C3-002",
    "C2-LIM-C3-003",
    "C2-LIM-C3-004",
    "C2-LIM-C3-005",
    "C2-LIM-C4-008",
)

_PROHIBITED_ACTIVITY_FIELDS: Final[tuple[str, ...]] = (
    "provider_access",
    "broker_access",
    "market_data_request",
    "account_inspection",
    "entitlement_inspection",
    "dataset_access",
    "model_execution",
    "final_holdout_access",
    "order_activity",
    "trading_activity",
)


class DiagnosticContractError(ValueError):
    """Raised for invalid diagnostic inputs or unsafe evidence requests."""


@dataclass(frozen=True, slots=True)
class ImportResult:
    """Sanitized terminal result for one canonical import target."""

    target: str
    status: str
    detail_code: str


@dataclass(frozen=True, slots=True)
class DiagnosticEvidence:
    """Complete deterministic C3 diagnostic evidence."""

    schema_version: str
    configuration_identity: str
    configuration_checksum: str
    python_implementation: str
    python_version: str
    python_minor_policy_result: str
    python_cache_tag: str
    python_soabi: str
    platform_tag: str
    virtual_environment_result: str
    package_manager_identity: str
    resolver_identity: str
    build_frontend_identity: str
    build_backend_provider_identity: str
    wheel_identity: str
    project_distribution_identity: str
    dependency_metadata_checksum: str
    lock_checksum: str
    package_source_allowlist_id: str
    approved_simple_index_url: str
    approved_artifact_url_prefix: str
    import_results: tuple[ImportResult, ...]
    network_boundary_result: str
    secret_exclusion_result: str
    prohibited_activity_confirmation: Mapping[str, bool]
    related_limitation_ids: tuple[str, ...]
    overall_result: str
    evidence_checksum: str
    evidence_identity: str

    def payload_without_evidence_identity(self) -> dict[str, object]:
        payload = asdict(self)
        payload.pop("evidence_checksum")
        payload.pop("evidence_identity")
        return payload

    def canonical_json_bytes(self) -> bytes:
        return _canonical_json_bytes(asdict(self))


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _is_lowercase_sha256(value: str) -> bool:
    return bool(_SHA256_RE.fullmatch(value))


def _is_virtual_environment() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def _metadata_version(distribution: str) -> tuple[str, str]:
    try:
        return metadata.version(distribution), "PASS"
    except metadata.PackageNotFoundError:
        return "UNAVAILABLE", "MISSING"
    except Exception:
        return "UNAVAILABLE", "INCONCLUSIVE"


def _tool_identity(
    distribution: str,
    expected_version: str,
) -> tuple[str, str]:
    actual_version, terminal = _metadata_version(distribution)
    identity = f"{distribution}=={actual_version}"

    if terminal == "MISSING":
        return identity, FAIL_MISSING_PACKAGE
    if terminal == "INCONCLUSIVE":
        return identity, INCONCLUSIVE
    if actual_version != expected_version:
        return identity, FAIL_INCOMPATIBLE_VERSION
    return identity, OVERALL_PASS


def _validate_import_targets(targets: Sequence[str]) -> None:
    if type(targets) not in (tuple, list):
        raise DiagnosticContractError("IMPORT_TARGET_COLLECTION_INVALID")
    if tuple(targets) != CANONICAL_IMPORT_TARGETS:
        raise DiagnosticContractError("IMPORT_TARGET_SET_INVALID")
    for target in targets:
        if type(target) is not str or not _IMPORT_TARGET_RE.fullmatch(target):
            raise DiagnosticContractError("IMPORT_TARGET_SYNTAX_INVALID")


def _run_import(target: str) -> ImportResult:
    if not _IMPORT_TARGET_RE.fullmatch(target):
        return ImportResult(target, IMPORT_INVALID_TARGET, "INVALID_TARGET")

    try:
        importlib.import_module(target)
    except ModuleNotFoundError as exc:
        if exc.name == target or (
            exc.name is not None and target.startswith(f"{exc.name}.")
        ):
            return ImportResult(
                target,
                IMPORT_MISSING_PACKAGE,
                "TARGET_MODULE_NOT_FOUND",
            )
        return ImportResult(
            target,
            IMPORT_OTHER,
            "DEPENDENCY_MODULE_NOT_FOUND",
        )
    except ImportError:
        return ImportResult(
            target,
            IMPORT_INCOMPATIBLE_VERSION,
            "IMPORT_ERROR",
        )
    except Exception:
        return ImportResult(
            target,
            IMPORT_OTHER,
            "UNSANITIZED_EXCEPTION_SUPPRESSED",
        )

    return ImportResult(target, IMPORT_PASS, "IMPORT_COMPLETED")


def _overall_result(
    *,
    configuration_valid: bool,
    identity_mismatch: bool,
    tool_results: Sequence[str],
    import_results: Sequence[ImportResult],
    network_boundary_result: str,
    secret_exclusion_result: str,
) -> str:
    if secret_exclusion_result == FAIL_PROHIBITED_SECRET_EXPOSURE:
        return FAIL_PROHIBITED_SECRET_EXPOSURE
    if network_boundary_result == FAIL_PROHIBITED_NETWORK_ATTEMPT:
        return FAIL_PROHIBITED_NETWORK_ATTEMPT
    if not configuration_valid:
        return FAIL_CONFIGURATION
    if identity_mismatch:
        return FAIL_IDENTITY_MISMATCH
    if any(item.status == IMPORT_INVALID_TARGET for item in import_results):
        return FAIL_INVALID_IMPORT_TARGET
    if (
        FAIL_MISSING_PACKAGE in tool_results
        or any(item.status == IMPORT_MISSING_PACKAGE for item in import_results)
    ):
        return FAIL_MISSING_PACKAGE
    if (
        FAIL_INCOMPATIBLE_VERSION in tool_results
        or any(
            item.status == IMPORT_INCOMPATIBLE_VERSION
            for item in import_results
        )
    ):
        return FAIL_INCOMPATIBLE_VERSION
    if (
        FAIL_OTHER in tool_results
        or any(item.status == IMPORT_OTHER for item in import_results)
    ):
        return FAIL_OTHER
    if (
        INCONCLUSIVE in tool_results
        or network_boundary_result == INCONCLUSIVE
        or secret_exclusion_result == INCONCLUSIVE
        or any(item.status == IMPORT_INCONCLUSIVE for item in import_results)
    ):
        return INCONCLUSIVE
    return OVERALL_PASS


def build_dependency_metadata(
    settings: EnvironmentSettings,
) -> tuple[dict[str, object], str, str]:
    """Build the accepted zero-project-dependency metadata identity."""

    payload: dict[str, object] = {
        "schema_version": DEPENDENCY_METADATA_SCHEMA_VERSION,
        "python_implementation": settings.python_implementation,
        "supported_python_minor": settings.supported_python_minor,
        "supported_python_constraint": settings.supported_python_constraint,
        "runtime_dependency_policy": settings.runtime_dependency_policy,
        "test_framework": settings.test_framework,
        "direct_runtime_dependencies": [],
        "direct_test_dependencies": [],
        "resolved_project_dependencies": [],
        "direct_project_dependency_count": 0,
        "resolved_project_dependency_count": 0,
        "build_system_requirements": [
            (
                f"{settings.build_backend_provider}=="
                f"{settings.build_backend_provider_version}"
            )
        ],
        "package_manager_identity": (
            f"{settings.package_manager_identity}=="
            f"{settings.package_manager_version}"
        ),
        "resolver_identity": (
            f"{settings.resolver_identity}=={settings.resolver_version}"
        ),
        "build_frontend_identity": (
            f"{settings.build_frontend}=="
            f"{settings.build_frontend_version}"
        ),
        "build_backend": settings.build_backend,
        "dependency_source_allowlist_id": (
            settings.dependency_source_allowlist_id
        ),
        "approved_simple_index_url": settings.approved_simple_index_url,
        "approved_artifact_url_prefix": settings.approved_artifact_url_prefix,
        "lock_identity_path": settings.lock_identity_path,
        "hash_enforcement_required": True,
    }
    checksum = hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()
    identity = (
        f"{DEPENDENCY_METADATA_SCHEMA_VERSION}:sha256:{checksum}"
    )
    return payload, checksum, identity


def run_diagnostics(
    settings: EnvironmentSettings,
    *,
    dependency_metadata_checksum: str,
    lock_checksum: str,
    network_boundary_result: str,
    secret_exclusion_result: str,
    import_targets: Sequence[str] = CANONICAL_IMPORT_TARGETS,
    related_limitation_ids: Sequence[str] = _ACCEPTED_LIMITATIONS,
) -> DiagnosticEvidence:
    """Run the explicit, sanitized C3 environment diagnostic."""

    _validate_import_targets(import_targets)

    if not _is_lowercase_sha256(dependency_metadata_checksum):
        raise DiagnosticContractError("DEPENDENCY_METADATA_CHECKSUM_INVALID")
    if not _is_lowercase_sha256(lock_checksum):
        raise DiagnosticContractError("LOCK_CHECKSUM_INVALID")
    if network_boundary_result not in {
        OVERALL_PASS,
        FAIL_PROHIBITED_NETWORK_ATTEMPT,
        INCONCLUSIVE,
    }:
        raise DiagnosticContractError("NETWORK_BOUNDARY_RESULT_INVALID")
    if secret_exclusion_result not in {
        OVERALL_PASS,
        FAIL_PROHIBITED_SECRET_EXPOSURE,
        INCONCLUSIVE,
    }:
        raise DiagnosticContractError("SECRET_EXCLUSION_RESULT_INVALID")
    if tuple(related_limitation_ids) != _ACCEPTED_LIMITATIONS:
        raise DiagnosticContractError("LIMITATION_SET_INVALID")

    python_implementation = platform.python_implementation()
    python_version = platform.python_version()
    python_minor = f"{sys.version_info.major}.{sys.version_info.minor}"
    python_minor_policy_result = (
        OVERALL_PASS
        if (
            python_implementation == settings.python_implementation
            and python_minor == settings.supported_python_minor
        )
        else FAIL_IDENTITY_MISMATCH
    )

    expected_tools = (
        (
            settings.package_manager_identity,
            settings.package_manager_version,
        ),
        (settings.resolver_identity, settings.resolver_version),
        (
            settings.build_frontend,
            settings.build_frontend_version,
        ),
        (
            settings.build_backend_provider,
            settings.build_backend_provider_version,
        ),
        ("wheel", "0.47.0"),
        (
            settings.canonical_distribution_name,
            settings.canonical_project_version,
        ),
    )

    identities: list[str] = []
    tool_results: list[str] = []
    for distribution, expected_version in expected_tools:
        identity, result = _tool_identity(distribution, expected_version)
        identities.append(identity)
        tool_results.append(result)

    imports = tuple(_run_import(target) for target in import_targets)
    prohibited = {field: False for field in _PROHIBITED_ACTIVITY_FIELDS}

    identity_mismatch = (
        python_minor_policy_result != OVERALL_PASS
        or not _is_virtual_environment()
    )

    overall = _overall_result(
        configuration_valid=True,
        identity_mismatch=identity_mismatch,
        tool_results=tool_results,
        import_results=imports,
        network_boundary_result=network_boundary_result,
        secret_exclusion_result=secret_exclusion_result,
    )

    base_payload: dict[str, object] = {
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "configuration_identity": settings.identity,
        "configuration_checksum": settings.checksum,
        "python_implementation": python_implementation,
        "python_version": python_version,
        "python_minor_policy_result": python_minor_policy_result,
        "python_cache_tag": sys.implementation.cache_tag or "UNAVAILABLE",
        "python_soabi": (
            str(sysconfig.get_config_var("SOABI") or "UNAVAILABLE")
        ),
        "platform_tag": sysconfig.get_platform(),
        "virtual_environment_result": (
            OVERALL_PASS if _is_virtual_environment() else FAIL_IDENTITY_MISMATCH
        ),
        "package_manager_identity": identities[0],
        "resolver_identity": identities[1],
        "build_frontend_identity": identities[2],
        "build_backend_provider_identity": identities[3],
        "wheel_identity": identities[4],
        "project_distribution_identity": identities[5],
        "dependency_metadata_checksum": dependency_metadata_checksum,
        "lock_checksum": lock_checksum,
        "package_source_allowlist_id": (
            settings.dependency_source_allowlist_id
        ),
        "approved_simple_index_url": settings.approved_simple_index_url,
        "approved_artifact_url_prefix": settings.approved_artifact_url_prefix,
        "import_results": tuple(asdict(item) for item in imports),
        "network_boundary_result": network_boundary_result,
        "secret_exclusion_result": secret_exclusion_result,
        "prohibited_activity_confirmation": prohibited,
        "related_limitation_ids": tuple(related_limitation_ids),
        "overall_result": overall,
    }

    evidence_checksum = hashlib.sha256(
        _canonical_json_bytes(base_payload)
    ).hexdigest()
    evidence_identity = (
        f"{DIAGNOSTIC_SCHEMA_VERSION}:sha256:{evidence_checksum}"
    )

    return DiagnosticEvidence(
        schema_version=DIAGNOSTIC_SCHEMA_VERSION,
        configuration_identity=settings.identity,
        configuration_checksum=settings.checksum,
        python_implementation=python_implementation,
        python_version=python_version,
        python_minor_policy_result=python_minor_policy_result,
        python_cache_tag=sys.implementation.cache_tag or "UNAVAILABLE",
        python_soabi=str(sysconfig.get_config_var("SOABI") or "UNAVAILABLE"),
        platform_tag=sysconfig.get_platform(),
        virtual_environment_result=(
            OVERALL_PASS if _is_virtual_environment() else FAIL_IDENTITY_MISMATCH
        ),
        package_manager_identity=identities[0],
        resolver_identity=identities[1],
        build_frontend_identity=identities[2],
        build_backend_provider_identity=identities[3],
        wheel_identity=identities[4],
        project_distribution_identity=identities[5],
        dependency_metadata_checksum=dependency_metadata_checksum,
        lock_checksum=lock_checksum,
        package_source_allowlist_id=settings.dependency_source_allowlist_id,
        approved_simple_index_url=settings.approved_simple_index_url,
        approved_artifact_url_prefix=settings.approved_artifact_url_prefix,
        import_results=imports,
        network_boundary_result=network_boundary_result,
        secret_exclusion_result=secret_exclusion_result,
        prohibited_activity_confirmation=prohibited,
        related_limitation_ids=tuple(related_limitation_ids),
        overall_result=overall,
        evidence_checksum=evidence_checksum,
        evidence_identity=evidence_identity,
    )


def build_environment_identity(
    settings: EnvironmentSettings,
    evidence: DiagnosticEvidence,
) -> tuple[dict[str, object], str, str]:
    """Build the versioned environment identity from explicit evidence."""

    payload: dict[str, object] = {
        "schema_version": ENVIRONMENT_IDENTITY_SCHEMA_VERSION,
        "python_implementation": evidence.python_implementation,
        "python_version": evidence.python_version,
        "supported_python_minor": settings.supported_python_minor,
        "supported_python_constraint": settings.supported_python_constraint,
        "python_cache_tag": evidence.python_cache_tag,
        "python_soabi": evidence.python_soabi,
        "platform_tag": evidence.platform_tag,
        "virtual_environment_result": evidence.virtual_environment_result,
        "package_manager_identity": evidence.package_manager_identity,
        "resolver_identity": evidence.resolver_identity,
        "build_frontend_identity": evidence.build_frontend_identity,
        "build_backend_provider_identity": (
            evidence.build_backend_provider_identity
        ),
        "wheel_identity": evidence.wheel_identity,
        "project_distribution_identity": (
            evidence.project_distribution_identity
        ),
        "dependency_source_allowlist_id": (
            evidence.package_source_allowlist_id
        ),
        "approved_simple_index_url": evidence.approved_simple_index_url,
        "approved_artifact_url_prefix": evidence.approved_artifact_url_prefix,
        "dependency_metadata_checksum": (
            evidence.dependency_metadata_checksum
        ),
        "lock_checksum": evidence.lock_checksum,
        "configuration_identity": evidence.configuration_identity,
    }
    checksum = hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()
    identity = f"{ENVIRONMENT_IDENTITY_SCHEMA_VERSION}:sha256:{checksum}"
    return payload, checksum, identity


def _reject_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)

    for part in absolute.parts[1:]:
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError as exc:
            raise DiagnosticContractError(
                "APPROVED_ROOT_COMPONENT_MISSING"
            ) from exc
        if stat.S_ISLNK(mode):
            raise DiagnosticContractError(
                "APPROVED_ROOT_SYMLINK_COMPONENT"
            )


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def write_evidence_atomic(
    evidence: DiagnosticEvidence,
    *,
    approved_root: Path,
    basename: str,
    repository_root: Path,
) -> str:
    """Write deterministic evidence only to an approved external temp root."""

    if type(basename) is not str:
        raise DiagnosticContractError("EVIDENCE_BASENAME_TYPE_INVALID")
    if (
        not basename
        or basename in {".", ".."}
        or "\x00" in basename
        or "/" in basename
        or "\\" in basename
        or Path(basename).is_absolute()
        or Path(basename).name != basename
        or not basename.endswith(".json")
    ):
        raise DiagnosticContractError("EVIDENCE_BASENAME_INVALID")

    if not approved_root.exists() or not approved_root.is_dir():
        raise DiagnosticContractError("APPROVED_ROOT_INVALID")
    if not repository_root.exists() or not repository_root.is_dir():
        raise DiagnosticContractError("REPOSITORY_ROOT_INVALID")

    _reject_symlink_components(approved_root)
    _reject_symlink_components(repository_root)

    approved_real = approved_root.resolve(strict=True)
    repository_real = repository_root.resolve(strict=True)

    if (
        approved_real == repository_real
        or _is_relative_to(approved_real, repository_real)
    ):
        raise DiagnosticContractError("APPROVED_ROOT_INSIDE_REPOSITORY")

    final_path = approved_real / basename
    temp_path = approved_real / f".{basename}.tmp"

    if os.path.lexists(final_path) or os.path.lexists(temp_path):
        raise DiagnosticContractError("EVIDENCE_DESTINATION_COLLISION")

    raw = evidence.canonical_json_bytes() + b"\n"
    descriptor = -1

    try:
        descriptor = os.open(
            temp_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = -1
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(temp_path, final_path)

        directory_descriptor = os.open(approved_real, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except Exception as exc:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        try:
            final_path.unlink(missing_ok=True)
        except OSError:
            pass
        if isinstance(exc, DiagnosticContractError):
            raise
        raise DiagnosticContractError("EVIDENCE_ATOMIC_WRITE_FAILED") from exc

    return basename
