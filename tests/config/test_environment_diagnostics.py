"""Tests for deterministic C3 diagnostics and atomic evidence writes."""

from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
from typing import NamedTuple
import unittest
from unittest import mock

from quantitative_trading_research.config.environment_diagnostics import (
    CANONICAL_IMPORT_TARGETS,
    DIAGNOSTIC_SCHEMA_VERSION,
    FAIL_CONFIGURATION,
    FAIL_IDENTITY_MISMATCH,
    FAIL_INCOMPATIBLE_VERSION,
    FAIL_MISSING_PACKAGE,
    FAIL_PROHIBITED_NETWORK_ATTEMPT,
    FAIL_PROHIBITED_SECRET_EXPOSURE,
    IMPORT_INVALID_TARGET,
    INCONCLUSIVE,
    OVERALL_PASS,
    DiagnosticContractError,
    DiagnosticEvidence,
    ImportResult,
    build_dependency_metadata,
    build_environment_identity,
    run_diagnostics,
    write_evidence_atomic,
)
from quantitative_trading_research.config.settings import (
    build_accepted_settings,
)


class _VersionInfoStub(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


EXPECTED_VERSIONS = {
    "pip": "26.1.2",
    "pip-tools": "7.6.0",
    "build": "1.5.0",
    "setuptools": "83.0.0",
    "wheel": "0.47.0",
    "quantitative-trading-research-platform": "0.0.0",
}


def _version_lookup(name: str) -> str:
    return EXPECTED_VERSIONS[name]


class DiagnosticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = build_accepted_settings()
        _, self.dependency_checksum, _ = build_dependency_metadata(
            self.settings
        )
        self.lock_checksum = "a" * 64

    def _run(self, **overrides: object) -> DiagnosticEvidence:
        kwargs: dict[str, object] = {
            "dependency_metadata_checksum": self.dependency_checksum,
            "lock_checksum": self.lock_checksum,
            "network_boundary_result": OVERALL_PASS,
            "secret_exclusion_result": OVERALL_PASS,
        }
        kwargs.update(overrides)

        with (
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.metadata.version",
                side_effect=_version_lookup,
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.platform.python_implementation",
                return_value="CPython",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.platform.python_version",
                return_value="3.12.9",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.version_info",
                _VersionInfoStub(3, 12, 0, "final", 0),
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.prefix",
                "/temporary/venv",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.base_prefix",
                "/temporary/base",
                create=True,
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.importlib.import_module",
                return_value=object(),
            ),
        ):
            return run_diagnostics(self.settings, **kwargs)

    def test_dependency_metadata_is_empty_and_deterministic(self) -> None:
        first, first_checksum, first_identity = build_dependency_metadata(
            self.settings
        )
        second, second_checksum, second_identity = build_dependency_metadata(
            self.settings
        )

        self.assertEqual(first["direct_runtime_dependencies"], [])
        self.assertEqual(first["direct_test_dependencies"], [])
        self.assertEqual(first["resolved_project_dependencies"], [])
        self.assertEqual(first["direct_project_dependency_count"], 0)
        self.assertEqual(first["resolved_project_dependency_count"], 0)
        self.assertEqual(first, second)
        self.assertEqual(first_checksum, second_checksum)
        self.assertEqual(first_identity, second_identity)
        self.assertRegex(first_checksum, r"^[0-9a-f]{64}$")

    def test_successful_diagnostic_is_deterministic(self) -> None:
        first = self._run()
        second = self._run()

        self.assertEqual(first.overall_result, OVERALL_PASS)
        self.assertEqual(first, second)
        self.assertEqual(first.schema_version, DIAGNOSTIC_SCHEMA_VERSION)
        self.assertRegex(first.evidence_checksum, r"^[0-9a-f]{64}$")
        self.assertEqual(
            first.evidence_identity,
            f"{DIAGNOSTIC_SCHEMA_VERSION}:sha256:"
            f"{first.evidence_checksum}",
        )
        self.assertTrue(
            all(
                result.status == OVERALL_PASS
                for result in first.import_results
            )
        )
        self.assertTrue(
            all(
                value is False
                for value in first.prohibited_activity_confirmation.values()
            )
        )

    def test_environment_identity_is_deterministic(self) -> None:
        evidence = self._run()
        first = build_environment_identity(self.settings, evidence)
        second = build_environment_identity(self.settings, evidence)

        self.assertEqual(first, second)
        self.assertRegex(first[1], r"^[0-9a-f]{64}$")
        self.assertTrue(first[2].endswith(first[1]))

    def test_secret_failure_has_highest_precedence(self) -> None:
        evidence = self._run(
            network_boundary_result=FAIL_PROHIBITED_NETWORK_ATTEMPT,
            secret_exclusion_result=FAIL_PROHIBITED_SECRET_EXPOSURE,
        )
        self.assertEqual(
            evidence.overall_result,
            FAIL_PROHIBITED_SECRET_EXPOSURE,
        )

    def test_network_failure_precedes_other_failures(self) -> None:
        evidence = self._run(
            network_boundary_result=FAIL_PROHIBITED_NETWORK_ATTEMPT
        )
        self.assertEqual(
            evidence.overall_result,
            FAIL_PROHIBITED_NETWORK_ATTEMPT,
        )

    def test_wrong_python_minor_fails_identity(self) -> None:
        with (
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.metadata.version",
                side_effect=_version_lookup,
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.platform.python_implementation",
                return_value="CPython",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.platform.python_version",
                return_value="3.11.15",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.version_info",
                _VersionInfoStub(3, 11, 0, "final", 0),
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.prefix",
                "/temporary/venv",
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.sys.base_prefix",
                "/temporary/base",
                create=True,
            ),
            mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.importlib.import_module",
                return_value=object(),
            ),
        ):
            evidence = run_diagnostics(
                self.settings,
                dependency_metadata_checksum=self.dependency_checksum,
                lock_checksum=self.lock_checksum,
                network_boundary_result=OVERALL_PASS,
                secret_exclusion_result=OVERALL_PASS,
            )

        self.assertEqual(evidence.overall_result, FAIL_IDENTITY_MISMATCH)

    def test_missing_tooling_fails_missing_package(self) -> None:
        def missing_pip(name: str) -> str:
            if name == "pip-tools":
                from importlib import metadata

                raise metadata.PackageNotFoundError(name)
            return EXPECTED_VERSIONS[name]

        with mock.patch(
            "quantitative_trading_research.config."
            "environment_diagnostics.metadata.version",
            side_effect=missing_pip,
        ):
            with (
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.platform.python_implementation",
                    return_value="CPython",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.platform.python_version",
                    return_value="3.12.9",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.version_info",
                    _VersionInfoStub(3, 12, 0, "final", 0),
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.prefix",
                    "/temporary/venv",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.base_prefix",
                    "/temporary/base",
                    create=True,
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.importlib.import_module",
                    return_value=object(),
                ),
            ):
                evidence = run_diagnostics(
                    self.settings,
                    dependency_metadata_checksum=self.dependency_checksum,
                    lock_checksum=self.lock_checksum,
                    network_boundary_result=OVERALL_PASS,
                    secret_exclusion_result=OVERALL_PASS,
                )

        self.assertEqual(evidence.overall_result, FAIL_MISSING_PACKAGE)

    def test_incompatible_tooling_version_fails(self) -> None:
        versions = dict(EXPECTED_VERSIONS)
        versions["pip"] = "26.2"

        with mock.patch(
            "quantitative_trading_research.config."
            "environment_diagnostics.metadata.version",
            side_effect=lambda name: versions[name],
        ):
            with (
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.platform.python_implementation",
                    return_value="CPython",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.platform.python_version",
                    return_value="3.12.9",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.version_info",
                    _VersionInfoStub(3, 12, 0, "final", 0),
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.prefix",
                    "/temporary/venv",
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.sys.base_prefix",
                    "/temporary/base",
                    create=True,
                ),
                mock.patch(
                    "quantitative_trading_research.config."
                    "environment_diagnostics.importlib.import_module",
                    return_value=object(),
                ),
            ):
                evidence = run_diagnostics(
                    self.settings,
                    dependency_metadata_checksum=self.dependency_checksum,
                    lock_checksum=self.lock_checksum,
                    network_boundary_result=OVERALL_PASS,
                    secret_exclusion_result=OVERALL_PASS,
                )

        self.assertEqual(
            evidence.overall_result,
            FAIL_INCOMPATIBLE_VERSION,
        )

    def test_invalid_import_target_set_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            DiagnosticContractError,
            "IMPORT_TARGET_SET_INVALID",
        ):
            self._run(import_targets=("quantitative_trading_research",))

    def test_invalid_checksum_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            DiagnosticContractError,
            "LOCK_CHECKSUM_INVALID",
        ):
            self._run(lock_checksum="not-a-checksum")

    def test_inconclusive_network_result_cannot_pass(self) -> None:
        evidence = self._run(network_boundary_result=INCONCLUSIVE)
        self.assertEqual(evidence.overall_result, INCONCLUSIVE)

    def test_atomic_write_succeeds_outside_repository(self) -> None:
        evidence = self._run()

        with tempfile.TemporaryDirectory() as base:
            base_path = Path(base).resolve()
            repository = base_path / "repository"
            approved = base_path / "evidence"
            repository.mkdir()
            approved.mkdir()

            basename = write_evidence_atomic(
                evidence,
                approved_root=approved,
                basename="diagnostic.json",
                repository_root=repository,
            )

            self.assertEqual(basename, "diagnostic.json")
            final_path = approved / basename
            self.assertTrue(final_path.is_file())
            raw = final_path.read_bytes()
            self.assertTrue(raw.endswith(b"\n"))
            self.assertEqual(
                json.loads(raw.decode("utf-8")),
                json.loads(evidence.canonical_json_bytes()),
            )
            self.assertFalse((approved / ".diagnostic.json.tmp").exists())

    def test_atomic_write_rejects_repository_destination(self) -> None:
        evidence = self._run()

        with tempfile.TemporaryDirectory() as base:
            repository = Path(base).resolve()
            approved = repository / "evidence"
            approved.mkdir()

            with self.assertRaisesRegex(
                DiagnosticContractError,
                "APPROVED_ROOT_INSIDE_REPOSITORY",
            ):
                write_evidence_atomic(
                    evidence,
                    approved_root=approved,
                    basename="diagnostic.json",
                    repository_root=repository,
                )

    def test_atomic_write_rejects_collision(self) -> None:
        evidence = self._run()

        with tempfile.TemporaryDirectory() as base:
            base_path = Path(base).resolve()
            repository = base_path / "repository"
            approved = base_path / "evidence"
            repository.mkdir()
            approved.mkdir()
            (approved / "diagnostic.json").write_text(
                "{}",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                DiagnosticContractError,
                "EVIDENCE_DESTINATION_COLLISION",
            ):
                write_evidence_atomic(
                    evidence,
                    approved_root=approved,
                    basename="diagnostic.json",
                    repository_root=repository,
                )

    def test_atomic_write_rejects_unsafe_basename(self) -> None:
        evidence = self._run()

        with tempfile.TemporaryDirectory() as base:
            base_path = Path(base).resolve()
            repository = base_path / "repository"
            approved = base_path / "evidence"
            repository.mkdir()
            approved.mkdir()

            for basename in (
                "../diagnostic.json",
                "/diagnostic.json",
                "diagnostic.txt",
                "nested/diagnostic.json",
                "nested\\diagnostic.json",
                "\x00.json",
            ):
                with self.subTest(basename=repr(basename)):
                    with self.assertRaisesRegex(
                        DiagnosticContractError,
                        "EVIDENCE_BASENAME_INVALID",
                    ):
                        write_evidence_atomic(
                            evidence,
                            approved_root=approved,
                            basename=basename,
                            repository_root=repository,
                        )

    def test_atomic_write_failure_cleans_partial_files(self) -> None:
        evidence = self._run()

        with tempfile.TemporaryDirectory() as base:
            base_path = Path(base).resolve()
            repository = base_path / "repository"
            approved = base_path / "evidence"
            repository.mkdir()
            approved.mkdir()

            with mock.patch(
                "quantitative_trading_research.config."
                "environment_diagnostics.os.replace",
                side_effect=OSError("suppressed"),
            ):
                with self.assertRaisesRegex(
                    DiagnosticContractError,
                    "EVIDENCE_ATOMIC_WRITE_FAILED",
                ):
                    write_evidence_atomic(
                        evidence,
                        approved_root=approved,
                        basename="diagnostic.json",
                        repository_root=repository,
                    )

            self.assertFalse((approved / "diagnostic.json").exists())
            self.assertFalse((approved / ".diagnostic.json.tmp").exists())

    def test_evidence_serialization_contains_no_raw_exception(self) -> None:
        evidence = self._run()
        raw = evidence.canonical_json_bytes().decode("utf-8")
        self.assertNotIn("Traceback", raw)
        self.assertNotIn("Exception", raw)
        self.assertNotIn("suppressed", raw.lower())


class ImportResultContractTests(unittest.TestCase):
    def test_invalid_target_status_is_fixed(self) -> None:
        result = ImportResult(
            "not valid",
            IMPORT_INVALID_TARGET,
            "INVALID_TARGET",
        )
        self.assertEqual(result.status, IMPORT_INVALID_TARGET)


if __name__ == "__main__":
    unittest.main()
