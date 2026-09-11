#!/usr/bin/env python3
"""Build the representation regression corpus from accepted result artifacts."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re


P_FAMILY = "RAW_HYPHEN_P_CLASS_TO_CQS_LOWERCASE_P"
WS_FAMILY = "RAW_HYPHEN_WS_TO_DOT_WS"
U_FAMILY = "RAW_HYPHEN_U_TO_DOT_U"
DOT_CLASS_FAMILY = "RAW_HYPHEN_CLASS_TO_DOT_CLASS"
AUTHORIZED = {P_FAMILY, WS_FAMILY, U_FAMILY}

EXPECTED_HASHES = {
    "manual_security_identity_adaptive_tranche_001_results_2024-08-30.csv": "c5b43b73877d0e445427744f7ffba33882caae1ec716feefb7025ac38d5054f8",
    "manual_security_identity_adaptive_tranche_002_results_2024-08-30.csv": "0f6923474a3ec2e5a8b76b62502dbdbe710b4c39bc740d2da87d8e2b90b1b3a6",
    "manual_security_identity_adaptive_tranche_003_results_2024-08-30.csv": "c25075e6767bd2d92723254fa58c45db9779897cbf8d7cbcbc0a5d639b959e7f",
    "manual_security_identity_adaptive_tranche_004_results_2024-08-30.csv": "f3590718d48314a0e0005dd4c95d5136b0e172d48d291fddd8f971ab151033f9",
    "manual_security_identity_adaptive_tranche_005_results_2024-08-30.csv": "af471ef08b56ce4aa48c7503f51ef35384c10adeeb681df94ea51ac034ffe2a5",
    "manual_security_identity_adaptive_tranche_006_results_2024-08-30.csv": "2684c7f6008a30b83a987ff2e42b62ff17c48826ce62491ff3386be594c01e5e",
    "manual_security_identity_adaptive_tranche_007_results_2024-08-30.csv": "1526c0508a1458b7bf58a1a8beba9f1d883cbde25b6695114f0b65465f6457db",
    "manual_security_identity_adaptive_tranche_008_results_2024-08-30.csv": "6ded9fc62c68e308ef24058ca0e655ed0000a6b58ebb8058897125bd24953714",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _derive(raw_symbol: str, family: str) -> str:
    patterns = {
        P_FAMILY: (r"^([A-Z0-9]+)-P-([A-Z0-9]+)$", lambda m: f"{m[1]}p{m[2]}"),
        WS_FAMILY: (r"^([A-Z0-9]+)-WS$", lambda m: f"{m[1]}.WS"),
        U_FAMILY: (r"^([A-Z0-9]+)-U$", lambda m: f"{m[1]}.U"),
        DOT_CLASS_FAMILY: (r"^([A-Z0-9]+)-([A-Z0-9]+)$", lambda m: f"{m[1]}.{m[2]}"),
    }
    pattern, transform = patterns[family]
    match = re.fullmatch(pattern, raw_symbol)
    return transform(match) if match else ""


def _family(row: dict[str, str]) -> str:
    explicit = next(
        (
            row.get(name, "")
            for name in (
                "representation_family",
                "observed_representation_family",
                "representation_family_observed",
            )
            if row.get(name, "")
        ),
        "",
    )
    if explicit:
        return explicit
    raw = row.get("raw_symbol", "")
    accepted = row.get("historical_ticker", "")
    for family in (P_FAMILY, WS_FAMILY, U_FAMILY, DOT_CLASS_FAMILY):
        if _derive(raw, family) == accepted:
            return family
    return ""


def build(artifact_dir: Path) -> dict[str, object]:
    positives: list[dict[str, object]] = []
    dot_negatives: list[dict[str, object]] = []
    sources: dict[str, str] = {}

    for filename, expected_hash in EXPECTED_HASHES.items():
        path = artifact_dir / filename
        actual_hash = _sha256(path)
        if actual_hash != expected_hash:
            raise RuntimeError(f"accepted artifact hash mismatch: {filename}")
        sources[filename] = actual_hash
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        for row in rows:
            family = _family(row)
            if family not in AUTHORIZED | {DOT_CLASS_FAMILY}:
                continue
            raw_symbol = row["raw_symbol"]
            derived = _derive(raw_symbol, family)
            accepted = (
                row.get("authoritative_historical_symbol", "")
                or row.get("historical_ticker", "")
            )
            qualification = row.get("representation_qualification_status", "")
            terminal = row.get("terminal_resolution_status", "")
            resolution = row.get("resolution_class", "")
            common = {
                "case_id": row["tranche_case_id"],
                "raw_record_index": int(row["raw_record_index"]),
                "raw_symbol": raw_symbol,
                "representation_family": family,
                "derived_authoritative_symbol": derived,
                "accepted_authoritative_symbol": accepted,
                "source_artifact": filename,
                "source_artifact_sha256": actual_hash,
            }
            if family in AUTHORIZED:
                accepted_qualification = qualification in (
                    "",
                    "QUALIFIED__EXACT_CASE_ONLY",
                )
                accepted_terminal = terminal in ("VERIFIED", "RESOLVED")
                if (
                    accepted_qualification
                    and accepted_terminal
                    and resolution != "UNRESOLVED"
                    and accepted == derived
                ):
                    common["accepted_structural_exclusion_reason"] = row.get(
                        "structural_exclusion_reason", ""
                    )
                    positives.append(common)
            elif (
                qualification == "UNQUALIFIED__FAIL_CLOSED"
                or (not qualification and terminal == "UNRESOLVED")
            ):
                common["accepted_case_status"] = "UNQUALIFIED__FAIL_CLOSED"
                dot_negatives.append(common)

    positives.sort(key=lambda row: (row["source_artifact"], row["case_id"]))
    dot_negatives.sort(key=lambda row: (row["source_artifact"], row["case_id"]))
    symbols = sorted({row["accepted_authoritative_symbol"] for row in positives})
    return {
        "schema_id": "FIRST_PASS_SYMBOL_REPRESENTATION_REGRESSION_V1",
        "fixture_role": "REGRESSION_DERIVED_FROM_ACCEPTED_PRE_CUTOFF_ARTIFACTS",
        "scientific_evidence_status": "NOT_NEW_SCIENTIFIC_EVIDENCE",
        "authoritative_frame_identifier": "ACCEPTED_ADAPTIVE_TRANCHE_SYMBOLOGY_PRE_CUTOFF_2024-08-30",
        "authoritative_frame_date": "2024-08-30",
        "historical_applicability": "PRE_CUTOFF",
        "accepted_source_artifact_sha256": sources,
        "authoritative_symbols": symbols,
        "positive_cases": positives,
        "dot_class_negative_cases": dot_negatives,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = build(args.artifact_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    counts = Counter(
        row["representation_family"] for row in payload["positive_cases"]
    )
    print(
        json.dumps(
            {
                "positive_case_count": len(payload["positive_cases"]),
                "positive_by_family": dict(sorted(counts.items())),
                "dot_class_negative_case_count": len(
                    payload["dot_class_negative_cases"]
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
