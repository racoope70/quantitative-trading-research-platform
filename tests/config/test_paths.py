from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.config.paths import (
    PathConfigurationError,
    ProjectPaths,
)


class ProjectPathsTests(unittest.TestCase):
    def test_explicit_base_path_is_resolved_and_normalized(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)

            paths = ProjectPaths(base)

            self.assertEqual(paths.base_path, base.resolve())
            self.assertTrue(paths.base_path.is_absolute())

    def test_relative_components_use_platform_native_path_semantics(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            paths = ProjectPaths(base)

            resolved = paths.resolve("alpha", "beta", "artifact.txt")

            self.assertEqual(
                resolved,
                base.resolve() / "alpha" / "beta" / "artifact.txt",
            )

    def test_pathlike_relative_component_is_supported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            paths = ProjectPaths(base)

            resolved = paths.resolve(Path("nested") / "leaf")

            self.assertEqual(resolved, base.resolve() / "nested" / "leaf")

    def test_repeated_resolution_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = ProjectPaths(temporary_directory)

            first = paths.resolve("reports", "result.json")
            second = paths.resolve("reports", "result.json")

            self.assertEqual(first, second)

    def test_resolve_without_components_returns_base_path(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = ProjectPaths(temporary_directory)

            self.assertEqual(paths.resolve(), paths.base_path)

    def test_missing_base_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing = Path(temporary_directory) / "does-not-exist"

            with self.assertRaises(PathConfigurationError):
                ProjectPaths(missing)

    def test_file_base_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = Path(temporary_directory) / "not-a-directory"
            file_path.write_text("x", encoding="utf-8")

            with self.assertRaises(PathConfigurationError):
                ProjectPaths(file_path)

    def test_empty_base_path_fails_closed(self):
        with self.assertRaises(PathConfigurationError):
            ProjectPaths("")

    def test_absolute_child_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = ProjectPaths(temporary_directory)
            absolute_child = Path(temporary_directory).resolve() / "outside"

            with self.assertRaises(PathConfigurationError):
                paths.resolve(absolute_child)

    def test_parent_traversal_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = ProjectPaths(temporary_directory)

            with self.assertRaises(PathConfigurationError):
                paths.resolve("alpha", "..", "outside")

    def test_module_import_does_not_mutate_working_directory_or_require_network(self):
        source_root = ROOT / "src"

        with tempfile.TemporaryDirectory() as temporary_directory:
            working_directory = Path(temporary_directory)
            before = sorted(working_directory.rglob("*"))

            code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.config.paths
"""

            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(source_root)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"

            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=working_directory,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            after = sorted(working_directory.rglob("*"))

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"stdout={completed.stdout}\nstderr={completed.stderr}",
            )
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
