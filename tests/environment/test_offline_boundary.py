from __future__ import annotations
from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[2]


class OfflineBoundaryTests(unittest.TestCase):
    def test_diagnostics_imports_no_network_library(self):
        tree = ast.parse((ROOT / "src/quantitative_trading_research/config/environment_diagnostics.py").read_text())
        imports = {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        imports |= {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        self.assertTrue({"socket", "urllib", "http", "requests", "subprocess"}.isdisjoint(imports))

    def test_environment_contract_contains_no_secret_value(self):
        text = (ROOT / "docs/configuration/environment_variables.md").read_text()
        self.assertNotIn("APCA_API_SECRET_KEY=", text)
        self.assertNotIn("APCA_API_KEY_ID=", text)

    def test_manifest_keeps_freeze_blocker_open(self):
        text = (ROOT / "docs/reports/C3_environment_and_dependency_manifest.yaml").read_text()
        self.assertIn('"FREEZE_BLOCKER_001": "OPEN__NO_QUALIFIED_HOST_SELECTED"', text)
        self.assertIn('"Stage1_scientific_freeze_advanced": "NO"', text)


if __name__ == "__main__":
    unittest.main()
