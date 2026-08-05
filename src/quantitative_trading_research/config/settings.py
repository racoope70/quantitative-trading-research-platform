"""Typed, deterministic C3 environment settings.

This module performs no environment lookup, filesystem access, network access,
or import-time construction of a settings instance.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Final


SCHEMA_VERSION: Final[str] = "C3_ENVIRONMENT_SETTINGS_V1"

ACCEPTED_SCHEMA_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "canonical_distribution_name",
    "canonical_import_package_name",
    "canonical_project_version",
    "python_implementation",
    "supported_python_minor",
    "supported_python_constraint",
    "runtime_dependency_policy",
    "third_party_runtime_dependency_count",
    "test_framework",
    "third_party_test_dependency_count",
    "package_manager_identity",
    "package_manager_version",
    "resolver_identity",
    "resolver_version",
    "build_backend",
    "build_backend_provider",
    "build_backend_provider_version",
    "build_frontend",
    "build_frontend_version",
    "dependency_source_allowlist_id",
    "approved_simple_index_url",
    "approved_artifact_url_prefix",
    "package_source_credentials_permitted",
    "lock_identity_path",
    "lock_integrity_standard",
)


class SettingsValidationError(ValueError):
    """Raised when an explicit settings mapping violates the C3 contract."""


@dataclass(frozen=True, slots=True)
class EnvironmentSettings:
    """Exact static C3 environment contract."""

    schema_version: str
    canonical_distribution_name: str
    canonical_import_package_name: str
    canonical_project_version: str
    python_implementation: str
    supported_python_minor: str
    supported_python_constraint: str
    runtime_dependency_policy: str
    third_party_runtime_dependency_count: int
    test_framework: str
    third_party_test_dependency_count: int
    package_manager_identity: str
    package_manager_version: str
    resolver_identity: str
    resolver_version: str
    build_backend: str
    build_backend_provider: str
    build_backend_provider_version: str
    build_frontend: str
    build_frontend_version: str
    dependency_source_allowlist_id: str
    approved_simple_index_url: str
    approved_artifact_url_prefix: str
    package_source_credentials_permitted: bool
    lock_identity_path: str
    lock_integrity_standard: str

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "EnvironmentSettings":
        """Build settings only from one explicit, exact mapping."""

        if type(values) is not dict:
            raise SettingsValidationError("SETTINGS_MAPPING_TYPE_INVALID")

        expected_types: dict[str, type[object]] = {
            "schema_version": str,
            "canonical_distribution_name": str,
            "canonical_import_package_name": str,
            "canonical_project_version": str,
            "python_implementation": str,
            "supported_python_minor": str,
            "supported_python_constraint": str,
            "runtime_dependency_policy": str,
            "third_party_runtime_dependency_count": int,
            "test_framework": str,
            "third_party_test_dependency_count": int,
            "package_manager_identity": str,
            "package_manager_version": str,
            "resolver_identity": str,
            "resolver_version": str,
            "build_backend": str,
            "build_backend_provider": str,
            "build_backend_provider_version": str,
            "build_frontend": str,
            "build_frontend_version": str,
            "dependency_source_allowlist_id": str,
            "approved_simple_index_url": str,
            "approved_artifact_url_prefix": str,
            "package_source_credentials_permitted": bool,
            "lock_identity_path": str,
            "lock_integrity_standard": str,
        }

        supplied = set(values)
        expected = set(expected_types)
        missing = sorted(expected - supplied)
        unknown = sorted(supplied - expected)

        if missing:
            raise SettingsValidationError("SETTINGS_REQUIRED_FIELD_MISSING")
        if unknown:
            raise SettingsValidationError("SETTINGS_UNKNOWN_FIELD")

        for field_name, expected_type in expected_types.items():
            if type(values[field_name]) is not expected_type:
                raise SettingsValidationError(
                    f"SETTINGS_FIELD_TYPE_INVALID:{field_name}"
                )

        expected_values = accepted_settings_mapping()
        for field_name, expected_value in expected_values.items():
            if values[field_name] != expected_value:
                raise SettingsValidationError(
                    f"SETTINGS_FIELD_VALUE_INVALID:{field_name}"
                )

        return cls(**values)  # type: ignore[arg-type]

    def to_mapping(self) -> dict[str, object]:
        """Return a new plain mapping in schema field form."""

        return dict(asdict(self))

    def canonical_json_bytes(self) -> bytes:
        """Serialize deterministically with no trailing newline."""

        return json.dumps(
            self.to_mapping(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")

    @property
    def checksum(self) -> str:
        """Return the lowercase SHA-256 of canonical settings bytes."""

        return hashlib.sha256(self.canonical_json_bytes()).hexdigest()

    @property
    def identity(self) -> str:
        """Return the versioned C3 settings identity."""

        return f"{SCHEMA_VERSION}:sha256:{self.checksum}"


def accepted_settings_mapping() -> dict[str, object]:
    """Return the accepted values without reading external state."""

    return {
        "schema_version": SCHEMA_VERSION,
        "canonical_distribution_name": "quantitative-trading-research-platform",
        "canonical_import_package_name": "quantitative_trading_research",
        "canonical_project_version": "0.0.0",
        "python_implementation": "CPython",
        "supported_python_minor": "3.12",
        "supported_python_constraint": ">=3.12,<3.13",
        "runtime_dependency_policy": "STANDARD_LIBRARY_ONLY",
        "third_party_runtime_dependency_count": 0,
        "test_framework": "unittest",
        "third_party_test_dependency_count": 0,
        "package_manager_identity": "pip",
        "package_manager_version": "26.1.2",
        "resolver_identity": "pip-tools",
        "resolver_version": "7.6.0",
        "build_backend": "setuptools.build_meta",
        "build_backend_provider": "setuptools",
        "build_backend_provider_version": "83.0.0",
        "build_frontend": "build",
        "build_frontend_version": "1.5.0",
        "dependency_source_allowlist_id": "C3_DEPENDENCY_SOURCE_ALLOWLIST_V1",
        "approved_simple_index_url": "https://pypi.org:443/simple/",
        "approved_artifact_url_prefix": (
            "https://files.pythonhosted.org:443/packages/"
        ),
        "package_source_credentials_permitted": False,
        "lock_identity_path": "requirements.lock",
        "lock_integrity_standard": (
            "EXACT_RESOLVED_VERSIONS_PLUS_ARTIFACT_HASHES"
        ),
    }


def build_accepted_settings() -> EnvironmentSettings:
    """Construct the accepted settings through the same explicit validator."""

    return EnvironmentSettings.from_mapping(accepted_settings_mapping())
