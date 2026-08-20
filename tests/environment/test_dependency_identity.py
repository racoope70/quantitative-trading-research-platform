from __future__ import annotations
from pathlib import Path
import hashlib
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_HISTORICAL_REQUIREMENTS = [
    "numpy", "pandas", "python-dotenv", "alpaca-py", "matplotlib", "scikit-learn",
    "joblib", "tqdm", "requests", "yfinance", "PyWavelets", "xgboost",
    "stable-baselines3[extra]>=2.0.0", "gymnasium>=0.29", "shimmy>=2.0.0",
    "gym-anytrading", "torch", "torchvision", "torchaudio", "pyarrow",
    "transformers", "tensorflow==2.16.2", "protobuf==3.20.3", "numba==0.60.0",
    "exchange-calendars==4.13.2",
]

EXPECTED_CANONICAL_DEPENDENCIES = [
    "numpy>=2.2,<3",
    "pandas>=2.2,<4",
    "scikit-learn>=1.6,<2",
    "PyWavelets>=1.8,<2",
    "xgboost>=3,<4",
    "stable-baselines3>=2.7,<3",
    "gymnasium>=1.1,<2",
    "torch>=2.7,<3",
    "pyarrow>=20,<26",
    "exchange-calendars>=4.11,<5",
]

EXPECTED_CANONICAL_LOCK_SHA256 = (
    "98723d20ba3581b0026df3ec177b734d5dc038e429a26a81545d93d8baad44db"
)


class DependencyIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = tomllib.loads((ROOT / "pyproject.toml").read_text())

    def test_canonical_direct_dependencies_match_accepted_set(self):
        self.assertEqual(
            self.data["project"]["dependencies"],
            EXPECTED_CANONICAL_DEPENDENCIES,
        )

    def test_canonical_python_policy_is_bound_to_3_13(self):
        self.assertEqual(
            self.data["project"]["requires-python"],
            ">=3.13,<3.14",
        )
        self.assertEqual(
            self.data["tool"]["c3"]["selected_python_policy"],
            "3.13",
        )

    def test_historical_candidates_are_explicitly_unresolved(self):
        candidates = self.data["tool"]["c3"]["historical_dependency_candidates"]
        self.assertEqual(len(candidates), 25)
        self.assertTrue(all(c["status"] == "UNRESOLVED_CANDIDATE_ONLY" for c in candidates))

    def test_historical_requirement_expressions_are_lossless_and_ordered(self):
        candidates = self.data["tool"]["c3"]["historical_dependency_candidates"]
        self.assertEqual([c["historical_requirement"] for c in candidates], EXPECTED_HISTORICAL_REQUIREMENTS)

    def test_historical_inventory_provenance_is_bound(self):
        inventory = self.data["tool"]["c3"]["historical_dependency_inventory"]
        self.assertEqual(inventory["identity"], "C1-TM-042")
        self.assertEqual(inventory["historical_source_repository"], "racoope70/ppo-trading-pipeline")
        self.assertEqual(inventory["historical_source_commit"], "072103f43d8b2488c3efca183f637ab0508a193a")
        self.assertEqual(inventory["historical_source_path"], "requirements.txt")
        self.assertEqual(inventory["historical_source_blob_sha"], "3dafa779f02d6bcb1b3f49689729bcb1900a63c9")
        self.assertEqual(inventory["member_count"], 25)

    def test_canonical_lock_is_present_with_exact_identity(self):
        lock = ROOT / "requirements.lock"
        self.assertTrue(lock.is_file())
        digest = hashlib.sha256(lock.read_bytes()).hexdigest()
        self.assertEqual(digest, EXPECTED_CANONICAL_LOCK_SHA256)


if __name__ == "__main__":
    unittest.main()
