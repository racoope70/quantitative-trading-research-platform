"""Canonical import-target and import-side-effect tests."""

from __future__ import annotations

import ast
import importlib
import os
from pathlib import Path
import socket
import sys
import unittest
from unittest import mock
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "src" / "quantitative_trading_research"

TARGETS = (
    "quantitative_trading_research",
    "quantitative_trading_research.config",
    "quantitative_trading_research.config.settings",
    "quantitative_trading_research.config.environment_diagnostics",
)

PROHIBITED_SUBSYSTEM_TERMS = (
    "alpaca",
    "broker",
    "market_data",
    "marketdata",
    "provider",
    "dataset",
    "features",
    "models",
    "evaluation",
    "execution",
    "holdout",
    "orders",
    "trading",
)


class ImportContractTests(unittest.TestCase):
    def tearDown(self) -> None:
        for target in reversed(TARGETS):
            sys.modules.pop(target, None)

    def test_exact_canonical_targets_import(self) -> None:
        imported = tuple(importlib.import_module(target) for target in TARGETS)
        self.assertEqual(
            tuple(module.__name__ for module in imported),
            TARGETS,
        )

    def test_fresh_import_has_no_filesystem_or_network_side_effect(self) -> None:
        for target in reversed(TARGETS):
            sys.modules.pop(target, None)

        with (
            mock.patch.object(
                os,
                "mkdir",
                side_effect=AssertionError("unexpected mkdir"),
            ),
            mock.patch.object(
                os,
                "makedirs",
                side_effect=AssertionError("unexpected makedirs"),
            ),
            mock.patch.object(
                socket,
                "socket",
                side_effect=AssertionError("unexpected socket"),
            ),
            mock.patch.object(
                socket,
                "getaddrinfo",
                side_effect=AssertionError("unexpected DNS"),
            ),
            mock.patch.object(
                urllib.request,
                "urlopen",
                side_effect=AssertionError("unexpected HTTP"),
            ),
        ):
            for target in TARGETS:
                module = importlib.import_module(target)
                self.assertEqual(module.__name__, target)

    def test_fresh_import_does_not_read_environment(self) -> None:
        for target in reversed(TARGETS):
            sys.modules.pop(target, None)

        original_getenv = os.getenv

        def rejected_getenv(*args: object, **kwargs: object) -> str:
            raise AssertionError("unexpected environment lookup")

        with mock.patch.object(os, "getenv", side_effect=rejected_getenv):
            for target in TARGETS:
                module = importlib.import_module(target)
                self.assertEqual(module.__name__, target)

        self.assertIs(os.getenv, original_getenv)

    def test_only_accepted_C3_modules_are_implemented(self) -> None:
        allowed = set(SOURCE_ROOT.rglob("__init__.py"))
        allowed.update(
            {
                SOURCE_ROOT / "config" / "settings.py",
                SOURCE_ROOT / "config" / "environment_diagnostics.py",
            }
        )

        implemented = {
            path
            for path in SOURCE_ROOT.rglob("*.py")
            if path.read_text(encoding="utf-8").strip()
        }

        unexpected = sorted(
            path.relative_to(ROOT).as_posix()
            for path in implemented
            if path not in allowed
        )
        self.assertEqual(unexpected, [])

    def test_C3_modules_do_not_import_prohibited_subsystems(self) -> None:
        for path in (
            SOURCE_ROOT / "config" / "settings.py",
            SOURCE_ROOT / "config" / "environment_diagnostics.py",
        ):
            tree = ast.parse(
                path.read_text(encoding="utf-8"),
                filename=path.as_posix(),
            )
            imported_names: list[str] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_names.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imported_names.append(node.module or "")

            accepted_internal_imports = {
                "quantitative_trading_research.config.settings",
            }
            inspected_names = [
                name.lower()
                for name in imported_names
                if name not in accepted_internal_imports
            ]
            lowered = "\n".join(inspected_names)
            for term in PROHIBITED_SUBSYSTEM_TERMS:
                with self.subTest(path=path.name, term=term):
                    self.assertNotIn(term, lowered)

    def test_imports_do_not_create_repository_files(self) -> None:
        before = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
        }

        for target in TARGETS:
            importlib.import_module(target)

        after = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
        }

        # Bytecode caches are disabled by the canonical launcher. This test
        # ignores existing or newly observed cache files and verifies that no
        # durable non-cache file is created.
        before = {
            item for item in before if "__pycache__/" not in item
        }
        after = {
            item for item in after if "__pycache__/" not in item
        }
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
