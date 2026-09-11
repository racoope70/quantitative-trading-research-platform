"""Fail-closed first-pass symbol-representation bridges.

This module implements only the three reusable representation families that
the Owner authorized.  It translates a raw symbol into a candidate symbol and
checks that candidate against an explicit, historically applicable frame.  It
does not determine security identity, type, eligibility, continuity, listing,
or membership.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Final, Iterable


P_FAMILY: Final = "RAW_HYPHEN_P_CLASS_TO_CQS_LOWERCASE_P"
WS_FAMILY: Final = "RAW_HYPHEN_WS_TO_DOT_WS"
U_FAMILY: Final = "RAW_HYPHEN_U_TO_DOT_U"
DOT_CLASS_FAMILY: Final = "RAW_HYPHEN_CLASS_TO_DOT_CLASS"

RESOLVED: Final = (
    "RESOLVED_BY_OWNER_AUTHORIZED_REUSABLE_REPRESENTATION_RULE"
)
FAIL_CLOSED: Final = "FAIL_CLOSED"
PRE_CUTOFF: Final = "PRE_CUTOFF"

_RULES: Final = {
    P_FAMILY: (
        re.compile(r"^(?P<base>[A-Z0-9]+)-P-(?P<class>[A-Z0-9]+)$"),
        "OWNER_AUTHORIZED_FIRST_PASS_P_CLASS_REPRESENTATION_V1",
        lambda match: f"{match.group('base')}p{match.group('class')}",
    ),
    WS_FAMILY: (
        re.compile(r"^(?P<base>[A-Z0-9]+)-WS$"),
        "OWNER_AUTHORIZED_FIRST_PASS_WS_REPRESENTATION_V1",
        lambda match: f"{match.group('base')}.WS",
    ),
    U_FAMILY: (
        re.compile(r"^(?P<base>[A-Z0-9]+)-U$"),
        "OWNER_AUTHORIZED_FIRST_PASS_U_REPRESENTATION_V1",
        lambda match: f"{match.group('base')}.U",
    ),
}


@dataclass(frozen=True)
class AuthoritativeSymbolRecord:
    """One exact symbol occurrence in an accepted authoritative frame."""

    symbol: str
    provenance: str


@dataclass(frozen=True)
class AuthoritativeSymbolFrame:
    """Explicit historically governed symbology frame supplied by a caller."""

    identifier: str
    frame_date: date
    historical_applicability: str
    records: tuple[AuthoritativeSymbolRecord, ...]
    conflicting_symbols: frozenset[str] = frozenset()

    @classmethod
    def from_records(
        cls,
        *,
        identifier: str,
        frame_date: date,
        historical_applicability: str,
        records: Iterable[AuthoritativeSymbolRecord],
        conflicting_symbols: Iterable[str] = (),
    ) -> "AuthoritativeSymbolFrame":
        return cls(
            identifier=identifier,
            frame_date=frame_date,
            historical_applicability=historical_applicability,
            records=tuple(records),
            conflicting_symbols=frozenset(conflicting_symbols),
        )


@dataclass(frozen=True)
class RepresentationBridgeResult:
    """Representation-only result; substantive adjudication is excluded."""

    representation_family: str
    raw_symbol: str
    derived_authoritative_candidate: str
    authoritative_candidate_match_count: int
    exact_match_count: int
    authoritative_symbol: str
    representation_bridge_status: str
    representation_rule_id: str
    authoritative_frame_identifier: str
    authoritative_frame_date: str
    historical_applicability: str
    representation_provenance: str
    matched_authoritative_record_provenance: str
    failure_reason: str


def _result(
    *,
    family: str,
    raw_symbol: str,
    candidate: str,
    match_count: int,
    authoritative_symbol: str,
    status: str,
    rule_id: str,
    frame: AuthoritativeSymbolFrame,
    failure_reason: str,
    matched_record_provenance: str = "",
) -> RepresentationBridgeResult:
    provenance = (
        f"RULE={rule_id or 'NONE'};FRAME={frame.identifier};"
        f"FRAME_DATE={frame.frame_date.isoformat()};"
        f"HISTORICAL_APPLICABILITY={frame.historical_applicability};"
        f"EXACT_MATCH_COUNT={match_count}"
    )
    if matched_record_provenance:
        provenance = (
            f"{provenance};MATCHED_AUTHORITATIVE_RECORD="
            f"{matched_record_provenance}"
        )
    return RepresentationBridgeResult(
        representation_family=family,
        raw_symbol=raw_symbol,
        derived_authoritative_candidate=candidate,
        authoritative_candidate_match_count=match_count,
        exact_match_count=match_count,
        authoritative_symbol=authoritative_symbol,
        representation_bridge_status=status,
        representation_rule_id=rule_id,
        authoritative_frame_identifier=frame.identifier,
        authoritative_frame_date=frame.frame_date.isoformat(),
        historical_applicability=frame.historical_applicability,
        representation_provenance=provenance,
        matched_authoritative_record_provenance=matched_record_provenance,
        failure_reason=failure_reason,
    )


def resolve_symbol_representation(
    *,
    raw_symbol: str,
    representation_family: str,
    authoritative_frame: AuthoritativeSymbolFrame,
    governed_cutoff: date,
) -> RepresentationBridgeResult:
    """Resolve one authorized raw-symbol formatting bridge or fail closed."""

    if representation_family == DOT_CLASS_FAMILY:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate="",
            match_count=0,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id="",
            frame=authoritative_frame,
            failure_reason="DOT_CLASS_REQUIRES_EXACT_CASE_REPRESENTATION_QUALIFICATION",
        )

    rule = _RULES.get(representation_family)
    if rule is None:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate="",
            match_count=0,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id="",
            frame=authoritative_frame,
            failure_reason="UNKNOWN_OR_UNAUTHORIZED_REPRESENTATION_FAMILY",
        )

    grammar, rule_id, derive = rule
    match = grammar.fullmatch(raw_symbol)
    if match is None:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate="",
            match_count=0,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="RAW_SYMBOL_GRAMMAR_FAILURE",
        )

    candidate = derive(match)
    matches = [
        record
        for record in authoritative_frame.records
        if record.symbol == candidate
    ]
    match_count = len(matches)

    if (
        authoritative_frame.historical_applicability != PRE_CUTOFF
        or authoritative_frame.frame_date > governed_cutoff
    ):
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate=candidate,
            match_count=match_count,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="AUTHORITATIVE_FRAME_NOT_HISTORICALLY_APPLICABLE",
        )

    if match_count == 0:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate=candidate,
            match_count=0,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="DERIVED_SYMBOL_ABSENT__ZERO_AUTHORITATIVE_MATCHES",
        )

    if match_count != 1:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate=candidate,
            match_count=match_count,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="MULTIPLE_AUTHORITATIVE_MATCHES",
        )

    if candidate in authoritative_frame.conflicting_symbols:
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate=candidate,
            match_count=1,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="CONFLICTING_REPRESENTATION_EVIDENCE",
        )

    if (
        not authoritative_frame.identifier.strip()
        or not matches[0].provenance.strip()
    ):
        return _result(
            family=representation_family,
            raw_symbol=raw_symbol,
            candidate=candidate,
            match_count=1,
            authoritative_symbol="",
            status=FAIL_CLOSED,
            rule_id=rule_id,
            frame=authoritative_frame,
            failure_reason="MISSING_REQUIRED_REPRESENTATION_PROVENANCE",
        )

    return _result(
        family=representation_family,
        raw_symbol=raw_symbol,
        candidate=candidate,
        match_count=1,
        authoritative_symbol=candidate,
        status=RESOLVED,
        rule_id=rule_id,
        frame=authoritative_frame,
        matched_record_provenance=matches[0].provenance,
        failure_reason="",
    )
