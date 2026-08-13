from __future__ import annotations
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from quantitative_trading_research.config.settings import ConfigurationError, settings_from_mapping


class SettingsTests(unittest.TestCase):
    def test_defaults_are_offline(self):
        settings = settings_from_mapping({})
        self.assertTrue(settings.offline_required)
        self.assertEqual(len(settings.checksum_sha256()), 64)

    def test_rejects_offline_false(self):
        with self.assertRaises(ConfigurationError):
            settings_from_mapping({"C3_OFFLINE_REQUIRED": "false"})

    def test_rejects_provider_secret(self):
        with self.assertRaises(ConfigurationError):
            settings_from_mapping({"APCA_API_KEY_ID": "secret"})

    def test_rejects_unknown_c3_key(self):
        with self.assertRaises(ConfigurationError):
            settings_from_mapping({"C3_UNKNOWN": "x"})

    def test_rejects_absolute_evidence_path(self):
        with self.assertRaises(ConfigurationError):
            settings_from_mapping({"C3_EVIDENCE_DIRECTORY": "/tmp/x"})

    def test_checksum_is_deterministic(self):
        a = settings_from_mapping({"C3_EVIDENCE_DIRECTORY": "evidence"})
        b = settings_from_mapping({"C3_EVIDENCE_DIRECTORY": "evidence"})
        self.assertEqual(a.checksum_sha256(), b.checksum_sha256())


if __name__ == "__main__":
    unittest.main()
