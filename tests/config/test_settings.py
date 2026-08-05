"""Tests for the explicit C3 settings contract."""

from __future__ import annotations

import json
import os
import unittest

from quantitative_trading_research.config.settings import (
    ACCEPTED_SCHEMA_FIELDS,
    SCHEMA_VERSION,
    EnvironmentSettings,
    SettingsValidationError,
    accepted_settings_mapping,
    build_accepted_settings,
)


class EnvironmentSettingsTests(unittest.TestCase):
    def test_accepted_mapping_constructs_exact_settings(self) -> None:
        settings = build_accepted_settings()
        self.assertEqual(settings.schema_version, SCHEMA_VERSION)
        self.assertEqual(
            settings.to_mapping(),
            accepted_settings_mapping(),
        )

    def test_exact_accepted_schema_field_set(self) -> None:
        self.assertEqual(
            tuple(accepted_settings_mapping()),
            ACCEPTED_SCHEMA_FIELDS,
        )
        self.assertEqual(len(ACCEPTED_SCHEMA_FIELDS), 26)
        self.assertNotIn("hash_enforcement_required", ACCEPTED_SCHEMA_FIELDS)

    def test_missing_field_is_rejected(self) -> None:
        values = accepted_settings_mapping()
        values.pop("lock_identity_path")

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_REQUIRED_FIELD_MISSING",
        ):
            EnvironmentSettings.from_mapping(values)

    def test_unknown_field_is_rejected(self) -> None:
        values = accepted_settings_mapping()
        values["unknown"] = "value"

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_UNKNOWN_FIELD",
        ):
            EnvironmentSettings.from_mapping(values)

    def test_non_dict_mapping_is_rejected(self) -> None:
        class MappingLike(dict[str, object]):
            pass

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_MAPPING_TYPE_INVALID",
        ):
            EnvironmentSettings.from_mapping(
                MappingLike(accepted_settings_mapping())
            )

    def test_wrong_field_type_is_rejected_without_coercion(self) -> None:
        values = accepted_settings_mapping()
        values["third_party_runtime_dependency_count"] = "0"

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_FIELD_TYPE_INVALID:third_party_runtime_dependency_count",
        ):
            EnvironmentSettings.from_mapping(values)

    def test_bool_is_not_accepted_as_int(self) -> None:
        values = accepted_settings_mapping()
        values["third_party_runtime_dependency_count"] = False

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_FIELD_TYPE_INVALID:third_party_runtime_dependency_count",
        ):
            EnvironmentSettings.from_mapping(values)

    def test_wrong_static_value_is_rejected(self) -> None:
        values = accepted_settings_mapping()
        values["supported_python_minor"] = "3.11"

        with self.assertRaisesRegex(
            SettingsValidationError,
            "SETTINGS_FIELD_VALUE_INVALID:supported_python_minor",
        ):
            EnvironmentSettings.from_mapping(values)

    def test_canonical_serialization_is_compact_sorted_ascii_json(self) -> None:
        settings = build_accepted_settings()
        raw = settings.canonical_json_bytes()

        self.assertFalse(raw.endswith(b"\n"))
        self.assertNotIn(b" ", raw)
        decoded = json.loads(raw.decode("utf-8"))
        self.assertEqual(decoded, accepted_settings_mapping())
        self.assertEqual(
            raw,
            json.dumps(
                decoded,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            ).encode("utf-8"),
        )

    def test_checksum_and_identity_are_reproducible(self) -> None:
        first = build_accepted_settings()
        second = build_accepted_settings()

        self.assertRegex(first.checksum, r"^[0-9a-f]{64}$")
        self.assertEqual(first.checksum, second.checksum)
        self.assertEqual(
            first.identity,
            f"{SCHEMA_VERSION}:sha256:{first.checksum}",
        )

    def test_construction_does_not_read_or_modify_environment(self) -> None:
        before = dict(os.environ)
        build_accepted_settings()
        after = dict(os.environ)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
