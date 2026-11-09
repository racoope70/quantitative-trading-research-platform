# QTRP — Deep Research Consolidated Findings

**Date:** 2026-11-09  
**Document role:** Non-authorizing research reference; **not** a controlling lifecycle document or implementation approval.  
**Status:** Deep Research original report + subsequent attachment-based evidence review consolidated. Independent Codex repository review is **pending** for architectural comparison.

## Sources

1. **Original:** `deep-research-report.md` — *QTRP Automation Simplification: Independent Architecture, Scientific-Integrity, and Security Review* (152 lines in supplied text representation).
2. **Evidence-based follow-up:** `Pasted text(20261109-061043).txt` — *QTRP — Independent Evidence Review*, dated 2026-11-09.

This document summarizes the two supplied reports. It does **not** independently authenticate their external citations or examine protected QTRP artifacts, current Mac filesystem state, or repository execution state. Statements about historical acceptances are reported with their limitations.

## Executive conclusion

**Research recommendation: retain `D + E + B`, conditionally.**

- **D — Selective recovery/authorization simplification:** Preserve accepted scientific processing and validation; reduce unnecessary coupling and custom recovery/authorization mechanisms without removing security invariants.
- **E — Explicit new recovery lineage:** A possible response to unprovable historical continuity, not a way to retroactively prove old state or to establish scientific comparability by declaration.
- **B — Owner-initiated one-unit operation:** The Owner authorizes one 25-record unit while constrained software handles deterministic processing, validation, evidence and controlled acceptance.
- **C — Codex/VS Code orchestration:** Optional convenience, never the source of REAL execution authority.
- **A — Continue custom architecture unchanged** and **F — full restart:** Not favored as defaults on present evidence.

**Important:** No architectural option has been adopted for REAL use. The recommendation is conditional on source-grounded local review, a bounded synthetic integration demonstration, and separate resolution of REAL-specific authority, protected access and scientific-continuity requirements.

## Why simplification is being considered

The original report identifies **control conflation**: provenance recovery, security authorization, execution, scientific acceptance and audit requirements became tightly coupled, creating serial prerequisites that blocked one another. Significant synthetic qualification work accumulated while the crucial question of whether checkpoint 54 represents a safe current resume state remained unresolved.

The subsequent evidence review **does not** conclude that all B53 controls were excessive. Its finding is narrower: the current implementation/dependency structure grew disproportionate, but bounded protected reads, source identity, namespace stability, replay prevention and proper authorization remain legitimate safeguards.

## Evidence-grounded project position

| Area | Finding and qualification |
|---|---|
| Batch0004 | 500 records in 20 units of 25 (supplied project state). |
| U0001–U0011 | 275 frozen accepted records, **historically MANAGING-accepted**; exact per-unit execution provenance not independently reconstructed. |
| U0012 | Pending after ten historical REAL attempts; checkpoint 54 (accepted project state, not newly independently verified). |
| Attempts 1–10 | Reported producer/schema, auxiliary applicability, capture, timeout, lifecycle, parser and internal-command issues; not merely authorization bureaucracy. |
| Current integration | C06-to-A11 qualification has accepted NONPRODUCTION evidence; does not establish REAL readiness. |
| Class B/Class C | Historical expectations reported for 149 Class B and 26 Class C objects; current applicability and Class C producer/version/schema provenance unresolved. |
| B53 | Synthetic qualification passed in earlier evidence, but protected-capable authorization and real protected access remain unqualified. |
| Python trust | Current runtime reported writable by the relevant user; proposed privileged Python use blocked. Independently authenticated immutable runtime and complete dependency closure not established. |

## Essential controls to retain

- Exact 25-record input/unit identities and authorized scope; `MAX_NEW_UNITS=1` and U0013 prohibition while applicable.
- Training/validation/holdout isolation, chronological and leakage-safe processing, and no unauthorized holdout access.
- Bound processor, source, runtime, configuration, input and policy identities as demanded by the relevant trust boundary.
- Complete schema, type, semantic, producer-event lifecycle, Policy B and reason-precedence checks; outer process exit status alone is insufficient.
- Complete evidence capture and nondisclosing failure outcomes; do not accept partial or ambiguous results.
- Staged complete-unit validation, immutable or protected accepted results, duplicate/replay rejection and accepted-predecessor checking.
- Crash/restart reconciliation across staged artifacts, evidence and the authoritative acceptance record; SQLite or atomic rename alone is not proof of end-to-end durability.
- Owner authority for REAL execution and protected access, backed by enforceable controls rather than an AI prompt alone.

## Complexity to challenge, not preemptively remove

- Custom privileged Python and immutable-runtime machinery for operations that may be safely unprivileged.
- Repeated approvals for unchanged low-risk internal engineering steps.
- Repeated large evidence narratives where a smaller authenticated machine-readable manifest suffices.
- Custom orchestration that duplicates trustworthy existing OS, job-runner or transaction capabilities.
- Multiple AI review layers without genuine independent observations.

Each proposed removal still requires a concrete threat/risk argument. Manual launch or Codex sandboxing does **not** automatically replace enforceable authorization or protected-data isolation.

## Proposed minimal operational concept — not approved

1. Owner selects and authorizes **exactly one** unit under an externally enforced scope.
2. A constrained, preferably unprivileged runner consumes an exact frozen manifest and writes into disposable staging.
3. Existing scientific processor and full validation/event-policy contracts run unchanged unless a separately justified correction is accepted.
4. Validation produces a compact evidence/identity manifest; failure or interruption does not advance accepted state.
5. A separate acceptance action atomically records one unit and rejects duplicates, with explicitly tested restart reconciliation.
6. Historical checkpoint 54 and 275 accepted records remain preserved. If a new lineage is selected, its actual continuity and comparability claims must be scientifically justified rather than inferred.

The original report floated SQLite as a small ledger example; the follow-up warns that a ledger and output publication are not inherently one crash-consistent transaction. **No decision to introduce SQLite has been made.** Reuse of a suitable existing acceptance mechanism may be preferable.

## Material corrections from the attachment-based follow-up

1. **Unprivileged execution is a hypothesis, not a proven protected-use solution.** The actual OS permission and Owner/executor boundary must be demonstrated.
2. **New lineage does not prove scientific equivalence.** Historical processor, inputs, dependencies, configuration, cross-unit state, checkpoint ancestry, schema and Policy B semantics remain relevant.
3. **One 25-record transaction is not enough by itself.** Event cardinality/lifecycle, command failures, timeouts and reason precedence must be handled.
4. **Transactional durability needs end-to-end proof.** Crash gaps between output publication, evidence and ledger changes require an authoritative commit/reconciliation rule.
5. **B53 security invariants remain material.** The implementation's complexity does not automatically invalidate its protective objectives.

## Single proposed NONPRODUCTION demonstration

**Research proposal only — not authorized for execution.** Use one synthetic 25-record fixture and disposable state, with no protected/holdout/REAL access:

1. Bind frozen synthetic manifest, exact processor/configuration and nonprotected runtime identity.
2. Exercise the existing processor, complete capture, producer schema, command-event lifecycle and Policy B validation.
3. Include an interrupted attempt and invalid completion; neither may advance a disposable acceptance record.
4. Rerun and verify scientifically appropriate equivalence, complete evidence, exactly-once acceptance, and replay rejection.
5. Demonstrate runner confinement against protected inputs, authoritative checkpoints and self-authorization; disclose any unproven OS separation.

**Stop if:** no isolated fixture can exercise the scientific pipeline without protected dependencies, reproducibility fails under justified criteria, interrupted work can become ambiguously accepted, or historical scientific state required for equivalence is unavailable. Do not add a new recovery framework merely to force PASS.

**What PASS would not prove:** Current Class B/Class C identities, Class C producer provenance, checkpoint-54 recovery compatibility, exact historical execution equivalence, protected B53 authorization, or permission for REAL Attempt 11.

## Pending independent decision input

Await independent Codex Astra/local-repository architecture review before deciding whether D + E + B is implementable and proportionate. In that synthesis, specifically compare:

- Reuse of existing checkpoint/acceptance mechanisms versus a new ledger.
- Whether one-unit unprivileged execution preserves all scientific and protected-state constraints.
- Whether a new lineage can be scientifically comparable to the frozen 275 records.
- Whether one synthetic integration could genuinely falsify the proposed simplification.

If Astra differs materially, research only the exact disagreement rather than repeating full Deep Research.

## Governing boundaries at report time

```text
C06 = CONTROLLED_STOP
CHECKPOINT = 54
U0012 = PENDING__TEN_HISTORICAL_ATTEMPTS
FROZEN_ACCEPTED_RECORDS = 275
ATTEMPT11_REAL_AUTHORIZED = NO
U0013 = PROHIBITED
```

No protected metadata/body reads, new recovery lineage, repository mutation, privileged operation, authorization publication or REAL processing is authorized by this historical research summary. `PROJECT_CONTEXT.md` remains controlling for broad current lifecycle state; the existing reference maps remain nonauthorizing.
