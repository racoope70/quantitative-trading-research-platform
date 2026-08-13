from __future__ import annotations
from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ImportContractTests(unittest.TestCase):
    def test_settings_imports_only_standard_library(self):
        tree = ast.parse((ROOT / "src/quantitative_trading_research/config/settings.py").read_text())
        imports = {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        imports |= {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        self.assertTrue(imports <= {"__future__", "dataclasses", "hashlib", "json", "typing"})

    def test_diagnostics_has_no_application_subsystem_import(self):
        text = (ROOT / "src/quantitative_trading_research/config/environment_diagnostics.py").read_text()
        for prohibited in (".data", ".features", ".models", ".evaluation", ".execution"):
            self.assertNotIn(prohibited, text)


if __name__ == "__main__":
    unittest.main()
