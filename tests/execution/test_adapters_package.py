from __future__ import annotations

import ast
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
ADAPTERS_INIT = (
    ROOT
    / "src"
    / "quantitative_trading_research"
    / "execution"
    / "adapters"
    / "__init__.py"
)


class AdaptersPackageTests(unittest.TestCase):
    def test_marker_contains_only_provenance_docstring(self):
        tree = ast.parse(ADAPTERS_INIT.read_text(encoding="utf-8"))

        self.assertEqual(1, len(tree.body))
        statement = tree.body[0]
        self.assertIsInstance(statement, ast.Expr)
        self.assertIsInstance(statement.value, ast.Constant)
        self.assertIsInstance(statement.value.value, str)

    def test_package_import_is_offline_and_side_effect_free(self):
        source_root = ROOT / "src"

        with tempfile.TemporaryDirectory() as temporary_directory:
            working_directory = Path(temporary_directory)
            before = sorted(working_directory.rglob("*"))

            code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \
     patch("socket.socket.connect", side_effect=AssertionError("network connect called")), \
     patch("socket.create_connection", side_effect=AssertionError("network connection called")):
    import quantitative_trading_research.execution.adapters
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
            0,
            completed.returncode,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
