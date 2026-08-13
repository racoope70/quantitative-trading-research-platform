from __future__ import annotations
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]


class DependencyIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = tomllib.loads((ROOT / "pyproject.toml").read_text())

    def test_no_canonical_direct_dependency_is_prematurely_accepted(self):
        self.assertEqual(self.data["project"]["dependencies"], [])

    def test_historical_candidates_are_explicitly_unresolved(self):
        candidates = self.data["tool"]["c3"]["historical_dependency_candidates"]
        self.assertGreater(len(candidates), 0)
        self.assertTrue(all(c["status"] == "UNRESOLVED_CANDIDATE_ONLY" for c in candidates))

    def test_lock_is_explicitly_not_generated(self):
        self.assertEqual(self.data["tool"]["c3"]["lock_status"], "NOT_GENERATED_NO_ACQUISITION_AUTHORIZED")

    def test_selected_python_policy_remains_unresolved(self):
        self.assertEqual(self.data["tool"]["c3"]["selected_python_policy"], "UNRESOLVED_BOUNDED_TWO_CANDIDATE_EVALUATION_NOT_EXECUTED")


if __name__ == "__main__":
    unittest.main()
