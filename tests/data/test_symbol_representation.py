"""Regression tests for the bounded first-pass representation layer.

The accepted-precedent fixture is derived from hash-pinned research artifacts.
Synthetic cases below test software controls only and are not scientific
evidence. ``unittest`` runs in the recovery workspace, and pytest also collects
these tests in the canonical repository suite.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import fields
from datetime import date
import inspect
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from quantitative_trading_research.data.symbol_representation import (
    DOT_CLASS_FAMILY,
    FAIL_CLOSED,
    P_FAMILY,
    PRE_CUTOFF,
    RESOLVED,
    U_FAMILY,
    WS_FAMILY,
    AuthoritativeSymbolFrame,
    AuthoritativeSymbolRecord,
    RepresentationBridgeResult,
    resolve_symbol_representation,
)


FIXTURE_PATH = (
    ROOT
    / "tests"
    / "data"
    / "fixtures"
    / "symbol_representation_accepted_precedent_v1.json"
)
CUTOFF = date(2024, 8, 30)


def _synthetic_frame(
    *symbols: str,
    frame_date: date = CUTOFF,
    historical_applicability: str = PRE_CUTOFF,
    conflicts: tuple[str, ...] = (),
) -> AuthoritativeSymbolFrame:
    return AuthoritativeSymbolFrame.from_records(
        identifier="SYNTHETIC_SOFTWARE_CONTROL__NOT_SCIENTIFIC_EVIDENCE",
        frame_date=frame_date,
        historical_applicability=historical_applicability,
        records=(
            AuthoritativeSymbolRecord(
                symbol=symbol,
                provenance=f"SYNTHETIC_RECORD::{index}",
            )
            for index, symbol in enumerate(symbols, start=1)
        ),
        conflicting_symbols=conflicts,
    )


class TestSymbolRepresentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.precedent = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        provenance_by_symbol: dict[str, list[str]] = defaultdict(list)
        for row in cls.precedent["positive_cases"]:
            provenance_by_symbol[row["accepted_authoritative_symbol"]].append(
                f"{row['source_artifact']}::{row['case_id']}"
            )
        records = [
            AuthoritativeSymbolRecord(
                symbol=symbol,
                provenance="|".join(sorted(provenance_by_symbol[symbol])),
            )
            for symbol in cls.precedent["authoritative_symbols"]
        ]
        cls.accepted_frame = AuthoritativeSymbolFrame.from_records(
            identifier=cls.precedent["authoritative_frame_identifier"],
            frame_date=date.fromisoformat(
                cls.precedent["authoritative_frame_date"]
            ),
            historical_applicability=cls.precedent[
                "historical_applicability"
            ],
            records=records,
        )

    def test_fixture_counts_and_frozen_source_hashes(self):
        positives = self.precedent["positive_cases"]
        family_counts = Counter(
            row["representation_family"] for row in positives
        )
        self.assertEqual(len(positives), 376)
        self.assertEqual(
            family_counts,
            {P_FAMILY: 317, WS_FAMILY: 50, U_FAMILY: 9},
        )
        self.assertEqual(len(self.precedent["dot_class_negative_cases"]), 45)
        self.assertEqual(
            set(self.precedent["accepted_source_artifact_sha256"].values()),
            {
                "c5b43b73877d0e445427744f7ffba33882caae1ec716feefb7025ac38d5054f8",
                "0f6923474a3ec2e5a8b76b62502dbdbe710b4c39bc740d2da87d8e2b90b1b3a6",
                "c25075e6767bd2d92723254fa58c45db9779897cbf8d7cbcbc0a5d639b959e7f",
                "f3590718d48314a0e0005dd4c95d5136b0e172d48d291fddd8f971ab151033f9",
                "af471ef08b56ce4aa48c7503f51ef35384c10adeeb681df94ea51ac034ffe2a5",
                "2684c7f6008a30b83a987ff2e42b62ff17c48826ce62491ff3386be594c01e5e",
                "1526c0508a1458b7bf58a1a8beba9f1d883cbde25b6695114f0b65465f6457db",
                "6ded9fc62c68e308ef24058ca0e655ed0000a6b58ebb8058897125bd24953714",
            },
        )

    def test_all_accepted_authorized_family_precedents_reproduce(self):
        for family, expected_count in (
            (P_FAMILY, 317),
            (WS_FAMILY, 50),
            (U_FAMILY, 9),
        ):
            cases = [
                row
                for row in self.precedent["positive_cases"]
                if row["representation_family"] == family
            ]
            self.assertEqual(len(cases), expected_count)
            for row in cases:
                with self.subTest(family=family, case_id=row["case_id"]):
                    result = resolve_symbol_representation(
                        raw_symbol=row["raw_symbol"],
                        representation_family=family,
                        authoritative_frame=self.accepted_frame,
                        governed_cutoff=CUTOFF,
                    )
                    self.assertEqual(result.representation_bridge_status, RESOLVED)
                    self.assertEqual(
                        result.derived_authoritative_candidate,
                        row["accepted_authoritative_symbol"],
                    )
                    self.assertEqual(
                        result.authoritative_symbol,
                        row["accepted_authoritative_symbol"],
                    )
                    self.assertEqual(result.exact_match_count, 1)
                    self.assertEqual(
                        result.authoritative_candidate_match_count,
                        1,
                    )
                    self.assertTrue(
                        result.matched_authoritative_record_provenance
                    )
                    self.assertIn(
                        result.matched_authoritative_record_provenance,
                        result.representation_provenance,
                    )

    def test_all_accepted_dot_class_negatives_remain_exact_case_only(self):
        false_positives = []
        for row in self.precedent["dot_class_negative_cases"]:
            result = resolve_symbol_representation(
                raw_symbol=row["raw_symbol"],
                representation_family=DOT_CLASS_FAMILY,
                authoritative_frame=self.accepted_frame,
                governed_cutoff=CUTOFF,
            )
            if result.representation_bridge_status != FAIL_CLOSED:
                false_positives.append(row["case_id"])
            self.assertEqual(
                result.failure_reason,
                "DOT_CLASS_REQUIRES_EXACT_CASE_REPRESENTATION_QUALIFICATION",
            )
            self.assertEqual(result.authoritative_symbol, "")
            self.assertEqual(
                result.matched_authoritative_record_provenance,
                "",
            )
        self.assertEqual(len(self.precedent["dot_class_negative_cases"]), 45)
        self.assertEqual(false_positives, [])

    def test_synthetic_software_controls_fail_closed(self):
        cases = [
            ("ABC-P-", P_FAMILY, _synthetic_frame("ABCpA"), "RAW_SYMBOL_GRAMMAR_FAILURE"),
            ("ABC-WS", WS_FAMILY, _synthetic_frame("ABC.WS", "ABC.WS"), "MULTIPLE_AUTHORITATIVE_MATCHES"),
            ("ABC-U", U_FAMILY, _synthetic_frame("ABC.U", conflicts=("ABC.U",)), "CONFLICTING_REPRESENTATION_EVIDENCE"),
            ("ABC-P-A", P_FAMILY, _synthetic_frame("ABCpA", frame_date=date(2024, 8, 31)), "AUTHORITATIVE_FRAME_NOT_HISTORICALLY_APPLICABLE"),
            ("ABC-P-A", P_FAMILY, _synthetic_frame("ABCpA", historical_applicability="CURRENT_STATE_ONLY"), "AUTHORITATIVE_FRAME_NOT_HISTORICALLY_APPLICABLE"),
            ("ABC/P-A", "RAW_SLASH_P_TO_CQS_LOWERCASE_P", _synthetic_frame("ABCpA"), "UNKNOWN_OR_UNAUTHORIZED_REPRESENTATION_FAMILY"),
            ("ABC-A", DOT_CLASS_FAMILY, _synthetic_frame("ABC.A"), "DOT_CLASS_REQUIRES_EXACT_CASE_REPRESENTATION_QUALIFICATION"),
        ]
        for raw_symbol, family, frame, failure_reason in cases:
            with self.subTest(failure_reason=failure_reason):
                result = resolve_symbol_representation(
                    raw_symbol=raw_symbol,
                    representation_family=family,
                    authoritative_frame=frame,
                    governed_cutoff=CUTOFF,
                )
                self.assertEqual(result.representation_bridge_status, FAIL_CLOSED)
                self.assertEqual(result.failure_reason, failure_reason)
                self.assertEqual(result.authoritative_symbol, "")
                self.assertEqual(
                    result.matched_authoritative_record_provenance,
                    "",
                )

    def test_derived_symbol_absent_control_fails_closed(self):
        result = resolve_symbol_representation(
            raw_symbol="ABC-P-Z",
            representation_family=P_FAMILY,
            authoritative_frame=_synthetic_frame("ABCpA"),
            governed_cutoff=CUTOFF,
        )
        self.assertEqual(
            result.derived_authoritative_candidate,
            "ABCpZ",
        )
        self.assertEqual(result.representation_bridge_status, FAIL_CLOSED)
        self.assertEqual(
            result.failure_reason,
            "DERIVED_SYMBOL_ABSENT__ZERO_AUTHORITATIVE_MATCHES",
        )

    def test_zero_authoritative_matches_control_fails_closed(self):
        result = resolve_symbol_representation(
            raw_symbol="XYZ-WS",
            representation_family=WS_FAMILY,
            authoritative_frame=_synthetic_frame(),
            governed_cutoff=CUTOFF,
        )
        self.assertEqual(result.authoritative_candidate_match_count, 0)
        self.assertEqual(result.exact_match_count, 0)
        self.assertEqual(result.representation_bridge_status, FAIL_CLOSED)
        self.assertEqual(
            result.failure_reason,
            "DERIVED_SYMBOL_ABSENT__ZERO_AUTHORITATIVE_MATCHES",
        )

    def test_representation_result_surface_has_no_substantive_fields(self):
        field_names = {field.name for field in fields(RepresentationBridgeResult)}
        self.assertEqual(
            field_names,
            {
                "representation_family",
                "raw_symbol",
                "derived_authoritative_candidate",
                "authoritative_candidate_match_count",
                "exact_match_count",
                "authoritative_symbol",
                "representation_bridge_status",
                "representation_rule_id",
                "authoritative_frame_identifier",
                "authoritative_frame_date",
                "historical_applicability",
                "representation_provenance",
                "matched_authoritative_record_provenance",
                "failure_reason",
            },
        )
        self.assertEqual(
            set(inspect.signature(resolve_symbol_representation).parameters),
            {
                "raw_symbol",
                "representation_family",
                "authoritative_frame",
                "governed_cutoff",
            },
        )
        forbidden_in_result_and_inputs = {
            "security_type",
            "security_level_identity",
            "share_class_identity",
            "eligibility",
            "continuity",
            "primary_listing",
            "top_120_membership",
            "current_ticker",
            "current_exchange",
        }
        self.assertTrue(field_names.isdisjoint(forbidden_in_result_and_inputs))

    def test_p_family_bridge_is_independent_of_instrument_type(self):
        required_debt = {"MER-P-K", "NEE-P-R", "NYCB-P-U", "PBI-P-B"}
        p_cases = {
            row["raw_symbol"]: row
            for row in self.precedent["positive_cases"]
            if row["representation_family"] == P_FAMILY
        }
        self.assertTrue(required_debt <= p_cases.keys())
        self.assertEqual(
            {
                p_cases[symbol]["accepted_structural_exclusion_reason"]
                for symbol in required_debt
            },
            {"DEBT_OR_STRUCTURED_PRODUCT"},
        )
        self.assertTrue(
            any(
                row["accepted_structural_exclusion_reason"]
                == "PREFERRED_OR_DEPOSITARY_PREFERRED"
                for row in p_cases.values()
            )
        )
        for row in p_cases.values():
            result = resolve_symbol_representation(
                raw_symbol=row["raw_symbol"],
                representation_family=P_FAMILY,
                authoritative_frame=self.accepted_frame,
                governed_cutoff=CUTOFF,
            )
            self.assertEqual(result.representation_bridge_status, RESOLVED)
            self.assertFalse(hasattr(result, "structural_exclusion_reason"))
            self.assertFalse(hasattr(result, "security_type"))

    def test_success_preserves_exact_matched_record_provenance(self):
        result = resolve_symbol_representation(
            raw_symbol="ABC-P-A",
            representation_family=P_FAMILY,
            authoritative_frame=_synthetic_frame("ABCpA"),
            governed_cutoff=CUTOFF,
        )
        self.assertEqual(result.representation_bridge_status, RESOLVED)
        self.assertEqual(
            result.matched_authoritative_record_provenance,
            "SYNTHETIC_RECORD::1",
        )
        self.assertIn(
            "MATCHED_AUTHORITATIVE_RECORD=SYNTHETIC_RECORD::1",
            result.representation_provenance,
        )

    def test_exact_single_match_with_blank_record_provenance_fails_closed(self):
        frame = AuthoritativeSymbolFrame.from_records(
            identifier="SYNTHETIC_SOFTWARE_CONTROL__NOT_SCIENTIFIC_EVIDENCE",
            frame_date=CUTOFF,
            historical_applicability=PRE_CUTOFF,
            records=(
                AuthoritativeSymbolRecord(symbol="ABCpA", provenance=""),
            ),
        )
        result = resolve_symbol_representation(
            raw_symbol="ABC-P-A",
            representation_family=P_FAMILY,
            authoritative_frame=frame,
            governed_cutoff=CUTOFF,
        )
        self.assertEqual(result.exact_match_count, 1)
        self.assertEqual(result.representation_bridge_status, FAIL_CLOSED)
        self.assertEqual(result.authoritative_symbol, "")
        self.assertEqual(result.matched_authoritative_record_provenance, "")
        self.assertEqual(
            result.failure_reason,
            "MISSING_REQUIRED_REPRESENTATION_PROVENANCE",
        )

    def test_valid_exact_match_with_blank_frame_identifier_fails_closed(self):
        frame = AuthoritativeSymbolFrame.from_records(
            identifier="",
            frame_date=CUTOFF,
            historical_applicability=PRE_CUTOFF,
            records=(
                AuthoritativeSymbolRecord(
                    symbol="ABCpA",
                    provenance="SYNTHETIC_RECORD::1",
                ),
            ),
        )
        result = resolve_symbol_representation(
            raw_symbol="ABC-P-A",
            representation_family=P_FAMILY,
            authoritative_frame=frame,
            governed_cutoff=CUTOFF,
        )
        self.assertEqual(result.exact_match_count, 1)
        self.assertEqual(result.representation_bridge_status, FAIL_CLOSED)
        self.assertEqual(result.authoritative_symbol, "")
        self.assertEqual(result.authoritative_frame_identifier, "")
        self.assertEqual(
            result.failure_reason,
            "MISSING_REQUIRED_REPRESENTATION_PROVENANCE",
        )


if __name__ == "__main__":
    unittest.main()
