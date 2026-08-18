from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from quantitative_trading_research.config.environment_diagnostics import atomic_write_json, collect_static_diagnostic, inspect_import_targets
from quantitative_trading_research.config.settings import settings_from_mapping


class DiagnosticTests(unittest.TestCase):
    def test_import_contract_passes_for_package_root(self):
        results = inspect_import_targets()
        self.assertTrue(all(item["status"] == "PASS" for item in results))

    def test_missing_import_is_classified(self):
        result = inspect_import_targets(["definitely_missing_c3_package"])[0]
        self.assertEqual(result["status"], "FAIL_MISSING_PACKAGE")

    def test_missing_import_never_produces_terminal_pass(self):
        payload = collect_static_diagnostic(ROOT, settings_from_mapping({}), targets=["definitely_missing_c3_package"])
        self.assertNotEqual(payload["terminal_outcome"], "PASS")

    def test_all_controlling_identities_lock_and_imports_produce_terminal_pass(self):
        payload = collect_static_diagnostic(ROOT, settings_from_mapping({}))
        self.assertEqual(payload["dependency"]["lock_status"], "PRESENT")
        self.assertTrue(all(item["status"] == "PASS" for item in payload["canonical_import_targets"]))
        self.assertEqual(payload["controlling_identity"]["status"], "RESOLVED")
        self.assertEqual(
            payload["controlling_identity"]["reason"],
            "ALL_REQUIRED_CONTROLLING_IDENTITIES_RESOLVED",
        )
        self.assertEqual(payload["terminal_outcome"], "PASS")

    def test_missing_lock_remains_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "pyproject.toml").write_bytes((ROOT / "pyproject.toml").read_bytes())

            payload = collect_static_diagnostic(root, settings_from_mapping({}))

            self.assertEqual(payload["dependency"]["lock_status"], "UNRESOLVED_NOT_GENERATED")
            self.assertEqual(payload["controlling_identity"]["status"], "UNRESOLVED")
            self.assertNotEqual(payload["terminal_outcome"], "PASS")

    def test_unresolved_controlling_identity_remains_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
            old = 'local_ci_equivalence_status = "PASS_EXACT_REQUIRED_IDENTITIES"'
            new = 'local_ci_equivalence_status = "UNRESOLVED_TEST_SENTINEL"'

            self.assertEqual(text.count(old), 1)

            (root / "pyproject.toml").write_text(
                text.replace(old, new, 1),
                encoding="utf-8",
            )
            (root / "requirements.lock").write_bytes(
                (ROOT / "requirements.lock").read_bytes()
            )

            payload = collect_static_diagnostic(root, settings_from_mapping({}))

            self.assertEqual(payload["dependency"]["lock_status"], "PRESENT")
            self.assertEqual(payload["controlling_identity"]["status"], "UNRESOLVED")
            self.assertNotEqual(payload["terminal_outcome"], "PASS")

    def test_atomic_json_write(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "result.json"
            atomic_write_json(path, {"x": 1})
            self.assertEqual(json.loads(path.read_text()), {"x": 1})


if __name__ == "__main__":
    unittest.main()
