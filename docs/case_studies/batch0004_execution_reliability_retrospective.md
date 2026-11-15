# Batch0004 U0012 — Engineering Reliability Retrospective

**Status:** Published historical engineering retrospective  
**Disposition:** Permanent retained `CONTROLLED_STOP` (terminal incomplete)  
**Project:** Quantitative Trading Research Platform (QTRP)\
**Repository location:** `docs/case_studies/batch0004_execution_reliability_retrospective.md`\
**Scope:** Batch0004 / Primary / S05 / U0012, Attempts 1–11\
**Evidence cutoff:** 2026-11-14; final retained-stop disposition incorporated from accepted nonprotected handoff\
**Document role:** Nonauthorizing engineering case study, not a recovery procedure, scientific acceptance record, or lifecycle controller.

## Executive summary

Batch0004 was designed to process deterministic 25-record units while protecting the integrity of previously accepted scientific results. Units U0001–U0011 account for **275 accepted records**. U0012 encountered **eleven unsuccessful execution attempts**. The failure history exposed difficulties across event capture, validation, command execution, timeout handling, checkpoint continuation, and terminal-state bookkeeping. The recorded failure categories are not interchangeable, and the available nonprotected materials do not establish an exact cause for every numbered attempt.

The engineering response separated execution authority, scientific acceptance, state continuity, and evidence integrity. In the later Attempt 11 sequence, a qualified prelaunch and correctly consumed single-use Owner authorization were followed by a native executor exit code of 1 and a controlled stop. **No new scientific records were accepted.** A subsequent finalization path was reported to reject with `ENGINE_ATTEMPT_ALREADY_EXISTS` after A0011 had been recorded. This is an identified post-record finalization guard defect. It is **not a demonstrated explanation for the native process failure**.

MANAGING accepted an isolated NONPRODUCTION correction of the finalization defect, supported by **33/33 focused synthetic checks PASS**. A later authorized selected-control attestation passed for checkpoint56/A0011 linkage. It did not restore the absent terminal journal event, explain native exit code 1, or authorize another REAL attempt. The original recovery workstream remains closed in permanent retained `CONTROLLED_STOP`, not completed scientific continuation.

## 1. Engineering objective

The objective was not merely to produce output for U0012. It was to resume the original scientifically accepted lineage without disturbing U0001–U0011 and to preserve deterministic 25-record processing. A new unit could be accepted only when its input, producer/event capture, validation, output, and recovery state were consistent with the accepted scientific contracts.

The safety model combined bounded runtime and source/configuration identities with checkpoint ancestry and frozen-result integrity. It included all-occurrence Policy B validation and complete execution-event capture. Single-use Model B Owner authorization, replay rejection, and fail-closed disposition on ambiguity completed the safeguards. Previously accepted data and the untouched validation/final-holdout boundary were not to be reprocessed or exposed to resolve operational failures. A successful process launch, an exit status, a successful authorization transaction, and scientific acceptance are four different outcomes.

The Owner-approved narrow recovery treatment later closed blanket historical P4/P10 reconstruction as a prerequisite for the specific original Attempt 11 continuation. Historical P4/P10 remain `UNRESOLVED__RECONSTRUCTION_CLOSED`. This decision did not authenticate missing historical producer events, waive scientific integrity, or grant reusable REAL authority.

## 2. Attempts 1–11 — chronological failures and observed symptoms

**Evidence standard:** The nonprotected consolidated M1–M12 history and research synthesis substantiate eleven attempts and an aggregate failure taxonomy. They **do not provide an authenticated one-to-one attribution** of every category to Attempts 1–10. Accordingly, an empty attribution below means *not established from material reviewed for this report*, not that the attempt lacked evidence elsewhere. The precise symptom, cause, and fix must not be reconstructed by guesswork.

| Attempt | Observed symptom or disposition | Confirmed root cause | Corrective action / disposition | Evidence status |
|---|---|---|---|---|
| **A0001** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | No numbered-attempt-specific correction supportable; accepted history preserved | **Historical aggregate only** [E1, E2] |
| **A0002** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation; do not infer a fix | **Historical aggregate only** [E1, E2] |
| **A0003** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation | **Historical aggregate only** [E1, E2] |
| **A0004** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation | **Historical aggregate only** [E1, E2] |
| **A0005** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation | **Historical aggregate only** [E1, E2] |
| **A0006** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation | **Historical aggregate only** [E1, E2] |
| **A0007** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | Same evidence limitation | **Historical aggregate only** [E1, E2] |
| **A0008** | **Event/message-cardinality rejection** reported by a prior controlled-stop review | Underlying producer cause not independently established in source material used for this report | Rejection preserved; no accepted new unit. No specific production correction independently attributed | **Prior review reported; receipt not reauthenticated here** [E3] |
| **A0009** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | No numbered-attempt-specific correction supportable | **Historical aggregate only** [E1, E2] |
| **A0010** | Unsuccessful historical U0012 attempt; individual symptom not established here | Not established | No numbered-attempt-specific correction supportable | **Historical aggregate only** [E1, E2] |
| **A0011** | Actual Owner-authorized REAL attempt started; native subprocess **exit code 1**; **CONTROLLED_STOP**; zero new accepted records | **Native exit-code cause UNRESOLVED.** Separate post-record finalization guard defect identified | Preserve A0011/checkpoint56; no replay. Isolated finalization correction qualified **33/33 synthetic PASS** but remains uninstalled; selected control linkage later attested PASS, and terminal journal remains incomplete | **Owner/MANAGING accepted outcome; source-trace classification for guard; selected custody subsequently attested PASS; native cause unresolved** [E1, E4, E6–E10] |

**Reported failure categories across Attempts 1–10, without unsupported attempt assignment:** output/validation conflicts; producer/schema and event-lifecycle issues; timeouts; message-cardinality rejection; Policy B rejection; parser/internal-command faults; and executable-lookup failure. This is a **historical taxonomy**, not eleven independently verified diagnoses [E2, E5]. Specific pairs of symptom → cause → correction remain unclaimed where per-attempt nonprotected receipts are unavailable.

## 3. Root-cause investigation

### Attempt 11: native versus finalization causes

**Native execution failure:** The exact Model B Owner authorization was published and consumed, the native child started, and the child exited with status **1**. The underlying cause has **not** been independently established. The REAL attempt ended in `CONTROLLED_STOP`, with **zero** new accepted scientific records and no U0013 activity [E1].

**Post-record finalization failure:** The state subsequently reported checkpoint sequence **56** and recorded attempt **A0011**. A missing terminal journal event and `ENGINE_ATTEMPT_ALREADY_EXISTS` were reported. Source-trace evidence identified an *attempt-absence guard being reused after the attempt had already been recorded*—a defective finalization-phase predicate. MANAGING accepted a **bounded, isolated NONPRODUCTION correction** supported by **33/33 focused synthetic PASS** [E4].

**Causal boundary:** The identified finalization defect explains an observed *finalization rejection*, not the preceding native subprocess exit code 1. Neither the correction nor its synthetic tests establishes completed REAL terminal recovery. No checkpoint rollback, journal rewrite, replay, new REAL execution, or science acceptance is authorized here.

### Diagnostic findings and evidence limits

**Observability versus correctness.** A generic guard classification or outer process status is insufficient to establish why an executor failed. Failure receipts must preserve an actionable, nondisclosing reason and the exact phase that rejected the operation. The earlier prelaunch history included an unsuccessful qualification. A later authorized qualification passed, but that does not retroactively change the earlier failure.

**Complete event accounting.** A pipeline may emit plausible output while violating event cardinality, producer lifecycle, command completion, or Policy B requirements. Validation must check the complete observed sequence and its precedence rules. A partial or conveniently filtered capture is not scientific success.

**Recovery is a state machine, not a retry loop.** Checkpoint, journal, attempt registration, authorization consumption, and scientific acceptance progress independently. A0011's appearance in recovery history and checkpoint56 does not imply terminal finalization or 25 newly accepted records. Single-use authorization prevents a failed attempt from simply being rerun to obtain a different result.

**Evidence provenance matters.** A current file hash establishes a byte comparison against an accepted expectation. It does not retroactively establish an unknown historical writer. The narrow P4/P10 decision prevented indefinite repetition of unattainable historical reconstruction while retaining the controls applicable to continuation.

**Engineering qualification is scoped.** Synthetic tests demonstrate behavior on fixtures. Accepted installation and prelaunch qualifications establish specified readiness properties. Neither substitutes for a successful native executor, completed terminal journal, verified recovery custody, or independently accepted scientific results.

## 4. Engineering corrections

| Area | Engineering improvement or accepted practice | Demonstrated limit |
|---|---|---|
| Deterministic units | Fixed 25-record U0012 scope, exact input/frame identities, source and partition binding | Does not guarantee successful native execution |
| Checkpoint/recovery | Pinned predecessor integrity, checkpoint-chain checks, bounded state transitions and nonacceptance on failure | Selected checkpoint56/A0011 control linkage subsequently attested PASS; terminal journal remains incomplete without a qualified cold-finalization path |
| Replay prevention | One-time Owner authorization, durable consumption, attempted-unit identity and fail-closed replay guard | Attempt 11 authority is consumed; no replay or Attempt 12 approved |
| Capture and validation | Complete event/capture contract, cardinality, schema, reason precedence and Policy B all-occurrence checks | Passing a subset of checks or receiving plausible output cannot establish acceptance |
| Installation / configuration | Accepted inert installation, 58/58 installed identities, bounded runtime/source binding and qualification | Current protected recovery outcome remains a separate evidence problem |
| Integration testing | Earlier accepted focused synthetic/nonproduction suites, 38/38 later integration PASS, and 33/33 focused finalization-correction checks PASS | Synthetic checks do not authenticate protected state or explain native exit code 1 |
| Evidence preservation | Independent hashes, receipts, explicit classes of confidence and exact stop states | Incomplete causal evidence must remain UNRESOLVED rather than be filled by inference |

The engineering objective is **reliable fail-closed behavior with an auditable route to eventual completion**, not maximizing the number of mechanisms or declaring success whenever safeguards reject unsafe progress.

## 5. Verification and regression testing

| Verification / operation | Final evidence-qualified status | What it does **not** establish |
|---|---|---|
| NONPRODUCTION prelaunch integration | 38/38 PASS (accepted historical report) [E1] | Native execution success or scientific acceptance |
| Actual protected prelaunch qualification | PASS within specified observed scope (accepted historical report) [E1] | Reusable REAL authorization |
| Owner authorization publication and consumption | PASS; authorization consumed once [E6] | Replay permission or terminal completion |
| Original native A0011 execution | Exit code **1**, `CONTROLLED_STOP`, **0** new accepted scientific records [E6] | Underlying native RC1 cause |
| Isolated post-record finalization guard correction | **33/33** synthetic NONPRODUCTION checks PASS; correction **uninstalled** [E7] | Native RC1 remedy or live terminal repair |
| Selected checkpoint56/A0011 custody/linkage | **PASS**; head/snapshot/A0011 linked, 11 attempts, original ten-entry prefix preserved [E8] | Full historical scientific chain, consumption journal, or terminal event |
| Authenticated native stderr diagnostic | **INCONCLUSIVE / UNKNOWN / NO_KNOWN_SIGNATURE**; two bodies/two reads, 14,149 bytes [E9] | Native root-cause identification |
| Terminal-only cold finalization feasibility | **NO_SAFE_PATH_ESTABLISHED** under existing accepted interfaces; terminal event **absent in prior accepted evidence** [E10] | Actual journal completion or authorization to backfill |
| Original Attempt 11 disposition | **Permanent retained CONTROLLED_STOP; workstream closed** [E10; Owner/MANAGING acceptance] | A successfully processed U0012 unit |
| Continued scientific/REAL authority | 275 prior accepted records preserved; 0 new accepted; further REAL **not authorized**, U0013 **prohibited** [E6–E10] | Permission to start another attempt |

**Evidence boundary:** MAIN reviewed and integrity-checked the supplied nonprotected handoff and selected archival receipts, not live Mac-host protected artifacts. The reported process and state facts retain their classifications as `CODEX_DIRECT_HOST_OBSERVATION` or accepted Owner/MANAGING findings. Only the precise nonprotected bytes directly inspected by MAIN were independently verified by MAIN. This retrospective does not claim independent full-state reattestation and is not a recovery procedure or authority instrument.

## 6. Final resolution — permanent retained CONTROLLED_STOP

**Accepted disposition (2026-11-14):** `ACCEPT_A11_PERMANENT_CONTROLLED_STOP__TERMINAL_INCOMPLETE_DISCLOSED__NATIVE_RC1_UNRESOLVED__CURRENT_RECOVERY_WORKSTREAM_CLOSED` [E6–E10]. The phrase “recovery workstream closed” means retaining the original stopped state without another unauthorized operation. It does **not** mean native execution was repaired, the terminal journal was finalized, or the U0012 unit was scientifically accepted.

The original one-shot Owner authorization was published and durably consumed. It is nonreusable. The native A0011 process exited with code 1. Checkpoint 56 and recorded A0011 remain. A later authorized selected-control attestation verified the checkpoint head/snapshot/A0011 linkage and **11 recorded attempts**. The attestation used three selected bodies, four reads (26,908 bytes), zero retries, and no scientific payload reads [E6, E8]. These findings establish only the selected control/custody claims, not the full historical scientific chain or the terminal event.

A subsequent authorized native diagnostic authenticated the selected manifest and stderr but found `INCONCLUSIVE / UNKNOWN / NO_KNOWN_SIGNATURE`. The native exit-code-1 root cause is **not established**. The diagnostic involved one wrapper and one worker invocation, zero retries, and two protected reads totaling 14,149 bytes [E9]. No raw stderr was disclosed in this case study. The identified `ENGINE_ATTEMPT_ALREADY_EXISTS` post-record guard defect is a separate issue. Its 33/33 synthetic NONPRODUCTION correction was accepted but **not installed**. No completed REAL finalization followed [E7].

The terminal journal event is absent in accepted prior evidence and was not reverified as part of the selected checkpoint attestation. Existing finalization requires original process-local transaction/authorization authority. The accepted bounded feasibility review found **no qualified safe new-caller cold-finalization path**. Fabricating an event or replaying the consumed authorization is therefore not an acceptable resolution [E10]. The scientific record remains at **275 accepted historical records and zero newly accepted records**. Attempt 11 is permanently retained in `CONTROLLED_STOP`. No Attempt 11 replay, Attempt 12, U0013, or other REAL continuation is authorized.

## 7. Lessons learned

The most transferable lesson is to separate the questions being answered. Authority determines whether an exact operation may occur. Capture and Policy B determine whether the processor produced admissible evidence. Checkpoint and journal controls establish what state was durably recorded. Scientific acceptance determines whether a new unit is accepted. A defect in one area does not prove a defect in another.

Future bounded engineering should keep a small, explicit transition table for attempt creation, child execution, exit disposition, evidence staging, scientific acceptance, and terminal recording. Guards should be phase-specific: a valid “attempt must not exist” predicate before registration must not inadvertently block finalizing that now-recorded attempt. A focused regression test should cover that transition and failure/restart paths, while protected qualification remains separately authorized.

The system also benefits from concise machine-checkable receipts with actionable nondisclosing failure codes, strict input/output identities, and explicit distinctions between verified, host-reported, and unresolved findings. Reuse accepted qualified components and existing Model B safeguards. Avoid rebuilding historical proofs, multiplying review layers, or introducing new orchestration frameworks without a demonstrated defect. **Simplification is not relaxation of scientific or security boundaries.**

## Appendix A — Source and evidence mapping

This map separates directly reviewed **nonauthorizing** documents from Owner/MANAGING-provided acceptance and historical claims. It is not permission to read protected artifacts or reopen historical producer investigation.

| ID | Source / evidence basis | Directly examined for this report? | Supports / does not support |
|---|---|---|---|
| **E1** | Prepared consolidated M1–M12 report: `docs/reports/batch0004_u0012_attempt11_recovery_closure_and_milestones.md` (MANAGING accepted substantive content; available on this working branch) | **Yes**, local prepared Markdown copy | Accepted milestones, ten prior attempts, Attempt 11 controlled stop, checkpoint56, zero new records, evidence limitations. **Does not** provide per-attempt A0001–A0010 diagnoses or authenticated original Mac receipts. |
| **E2** | `QTRP_Deep_Research_Consolidated_Findings_2026-11-09(1).md`, nonauthorizing research synthesis | **Yes**, supplied local Markdown | Aggregate Attempts 1–10 taxonomy, essential invariants and architecture lessons. **Does not** independently establish a numbered-attempt cause or constitute an adopted recovery architecture. |
| **E3** | Earlier reported independent Attempt 8 controlled-stop review (`BATCH0004_PRIMARY_S05_U0012_ATTEMPT8_CONTROLLED_STOP_EVIDENCE_REVIEW`) | **No** original review receipt reauthenticated for this report | Historically reported event-cardinality rejection; attribution and producer cause require the accepted original nonprotected review if promoted beyond reported status. No search or protected read undertaken. |
| **E4** | Current MANAGING retrospective directive and accepted post-A0011 NONPRODUCTION correction outcome | **Yes**, as Owner/MANAGING-supplied instruction, **not** as local source/receipt authentication | Finalization guard classification, MANAGING-accepted 33/33 synthetic PASS, checkpoint56/A0011 and unresolved native exit code. **Does not** prove protected recovery or scientific PASS. |
| **E5** | Current MANAGING preliminary classification of eleven historical failures | **Yes**, as supplied instruction | Broad output/validation, timeout, cardinality, Policy B and executable-lookup taxonomy. **Does not** assign these categories to individual earlier attempt numbers. |
| **E6** | Handoff `evidence/01_A11_REAL_ATTEMPT11_CONTROLLED_STOP_EVIDENCE.zip` (original execution, consumed authority, checkpoint56 reported state) | **Yes**, selected nonprotected canonical receipts; archive integrity in handoff manifest | Exact observed native exit 1, A0011 controlled stop, 0 new records, terminal incomplete; source host observations remain attributed. |
| **E7** | Handoff `evidence/02_FINALIZATION_GUARD_CORRECTION_EVIDENCE.zip` (accepted isolated correction) | **Yes**, consolidated nonprotected qualification report; no source execution | Accepted 7 bootstrap + 26 focused synthetic PASS (33/33), uninstalled guard correction; does not establish native cause or REAL completion. |
| **E8** | Handoff `evidence/03_CHECKPOINT56_AUTHORIZED_CONTROL_ATTESTATION_EVIDENCE.zip` and `evidence/06_AUTHORIZED_ATTESTATION_CONSOLIDATED_REPORT.md` | **Yes**, nonprotected attestation result and review summary; **not** underlying protected objects | Selected checkpoint56/head/A0011 linkage PASS; 11 attempts; bounded control reads; no terminal-journal or full scientific-chain attestation. |
| **E9** | Handoff `evidence/04_AUTHORIZED_NATIVE_RC1_DIAGNOSTIC_EVIDENCE.zip` and `evidence/07_AUTHORIZED_DIAGNOSTIC_MANAGING_REPORT.md` | **Yes**, nonprotected diagnostic result and review summary; **not** raw stderr | Authenticated manifest/stderr identity, INCONCLUSIVE/UNKNOWN/NO_KNOWN_SIGNATURE; native RC1 cause remains unknown. |
| **E10** | Handoff `evidence/05_A11_TERMINAL_DISPOSITION_NONPRODUCTION_FEASIBILITY_REPORT.md` and accepted final Owner/MANAGING disposition | **Yes**, nonprotected feasibility report and accepted disposition; no live journal read | Original process-local finalizer cannot be treated as an authorized cold terminal-only writer; retained permanent CONTROLLED_STOP and terminal incompleteness. |

### Attempt-level evidence index

| Attempt(s) | Cited basis | Evidence-confidence ceiling in this report | What would be needed for a stronger claim |
|---|---|---|---|
| **A0001–A0007** | E1, E2, E5 | Historical unsuccessful-attempt status and **aggregate** failure taxonomy only | Already-accepted, classified NONPROTECTED attempt-level disposition/receipt for the exact number |
| **A0008** | E1, E3 | Reported prior review of cardinality rejection; primary report not directly checked | Original accepted nonprotected controlled-stop review for exact assertion and severity |
| **A0009–A0010** | E1, E2, E5 | Historical unsuccessful-attempt status and **aggregate** failure taxonomy only | Already-accepted, classified NONPROTECTED attempt-level disposition/receipt |
| **A0011** | E1, E4, E6–E10 | Original controlled stop and selected checkpoint56/A0011 linkage PASS; native diagnostic inconclusive; cold finalization unsupported | Retain native cause UNRESOLVED and terminal event ABSENT; no further protected inspection or reconstruction authorized by this report |

**Explicitly unresolved claims:** Individual failure-category assignments and root causes for most Attempts 1–10; original Attempt 8 review reauthentication; exact native exit-code-1 cause; native RC1 cause; full historical-chain custody outside the selected attestation; absent terminal-journal completion; success of any future separately authorized REAL continuation. These are **evidence gaps**, not new demands for broad historical reconstruction.

**Public-content boundary:** No credentials, local private paths, protected record bodies, raw executor streams, or sensitive authorization contents are included in this report. Preserve these restrictions in future edits.

---

**Document status:** Published historical engineering retrospective; nonauthorizing.
**Final accepted scientific disposition:** `ACCEPT_A11_PERMANENT_CONTROLLED_STOP__TERMINAL_INCOMPLETE_DISCLOSED__NATIVE_RC1_UNRESOLVED__CURRENT_RECOVERY_WORKSTREAM_CLOSED`\
**Current controls:** `C06=CONTROLLED_STOP`; `HISTORICAL_P4/P10=UNRESOLVED__RECONSTRUCTION_CLOSED`; `FURTHER_REAL_AUTHORIZED=NO`; `U0013=PROHIBITED`.\
**Future editorial action:** Replace `[E3]` and aggregate-only attempt entries only if already accepted, classified nonprotected evidence becomes available. Sections 5–6 now record the accepted permanent stopped disposition; do not recast it as a repaired native execution or restart P4/P10 reconstruction.
