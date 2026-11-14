# Batch0004 PRIMARY S05 — Historical REAL Execution Evidence Record

**Document status:** PUBLISHED — nonauthorizing historical reference (documentation-only; not an execution authority)  
**Prepared:** 2026-11-09  
**Scope:** Original October 14–15, 2026 Batch0004 creation, corrected manual launch, aggregate scientific acceptance, and later evidence-recovery findings.  
**Not a source of current authorization:** This record cannot approve REAL execution, source inspection, checkpoint access, recovery mutations, or changes to the execution architecture.

## 1. Executive finding

The recovered October 2026 MAIN/batch-creation and MANAGING conversations support a historical account in which a corrected Owner-initiated Mac Terminal workflow began REAL PRIMARY S05 processing on October 15, 2026. The subsequently reported checkpoint state froze U0001–U0011 (11 × 25 = **275 accepted records**) and stopped with U0012 unfinished. Historical MANAGING accepted the corrected release for launch and subsequently accepted preservation of the aggregate frozen state. The recovered history describes **Owner manual initiation of the terminal workflow followed by driver-controlled sequential processing across multiple 25-record units**; it does **not** establish a separate Owner manual initiation for each unit or a one-unit-bounded entrypoint.

**This does not establish a complete authenticated chain** from the exact source bytes and immutable configuration/runtime through a specific individual unit's validation, Policy B acceptance, checkpoint commit, and independent acceptance. The full manual-execution binding remains **NOT_ESTABLISHED**. No alternative independently authenticated successful REAL run was located in the other accessible historical summaries.

## 2. Historical timeline

| Date/time (UTC, where recovered) | Reported event | Evidence qualification |
|---|---|---|
| 2026-10-14 | Batch0004 partitioned as 500 records, positions 1501–2000, in 20 units of 25. | Historical construction/partition report; manifest identity recorded. |
| 2026-10-15, before corrected release | Earlier terminal release encountered a prestart failure; it was not the successful REAL execution. | Historical MAIN/MANAGING account. |
| 2026-10-15 16:41:17 | MANAGING accepted the corrected driver/release and approved the identity-bound retry with clean reserved roots. | Recovered MANAGING acceptance reference, not reverified original receipt bytes. |
| 2026-10-15 17:17:48 | Owner reported REAL prestart PASS, root reservation PASS, operator confirmation and U0001 started. | OWNER_REPORTED in historical MANAGING review. |
| 2026-10-15 17:20:32 | Execution report identified U0001–U0011 as frozen (275 accepted records), U0012 unfinished. | Historical execution summary; primary per-unit receipts not recovered. |
| 2026-10-15 17:21:31 | Further report confirmed 275 accepted records and a U0012 position-validation controlled stop. | Historical execution summary. |
| 2026-10-15 20:31:26 | MANAGING accepted controlled-stop disposition preserving frozen state. | Recovered MANAGING acceptance reference. |

The earlier reported corrected-release integrity **218/218 PASS**, targeted tests **40/40 PASS**, REAL prestart **PASS**, and U0001 process return **0** are historical results. Process exit 0 is not itself scientific acceptance.

## 3. Recovered source, run and checkpoint identities

### Batch construction

| Identity | Recorded value | Qualification |
|---|---|---|
| Population | 500 records; positions 1501–2000 | Historical report |
| Unit structure | 20 units × 25 records | Historical report |
| S04 source manifest SHA-256 | `ade0a453cc6030d27cb0f1924eb17abe15eb082f55b3fd47af53f52927c543cc` | Historical source identity |
| S04 evidence SHA-256 | `0a92b5086a07972bdeb1c8210d50ed6c9c6e43d968b993165d06724c76372dc0` | Historical evidence identity |
| Partition manifest path | `/Users/richardcooper/Downloads/batch0004_REAL_size25_identity_bound_partition_manifest_v1/real_partition_manifest.json` | Historical pointer; present inspection classification not established here |
| Partition manifest SHA-256 | `cf0196e66a646fa02812d35a85879336fb635c437b2df1686e4740f4ca66f53f` | Historical identity |
| Partition rule SHA-256 | `7cfb32b29ad4f8375287bc0d2196872588655f8d270f1cc5372dc933a8cb6a09` | Historical identity |
| Partition-construction task | `POST_C6_Q1_2027_D1_BODY_BATCH0004_SIZE25_REAL_PARTITION_MANIFEST_AND_LIVE_INTEGRATION_BUILD_V1` | Historical task ID |

### Original corrected launch

| Identity | Recorded value | Qualification |
|---|---|---|
| Historical REAL run ID | `BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F` | Recovered historical identifier |
| Corrected terminal driver | `terminal_prestart_driver_recovery_v1.py` | Historical candidate for successful launch |
| Driver path | `/Users/richardcooper/Downloads/batch0004_primary_S05_terminal_state_recovery_v1/terminal_prestart_driver_recovery_v1.py` | Recovered exact historical path; current bytes unverified |
| Expected driver SHA-256 | `90670766b005e74908896bb7e6d46e5eae84c39174591520b040a0d83e61b85d` | Historical accepted source identity; **not** current host-verified digest |
| Superseding release SHA-256 | `e3c3b7860764f404130ac27c74052f509d065fa171c28c2beeb9b1549b7f141a` | Historical reported identity |
| Associated report path | `/Users/richardcooper/Downloads/batch0004_primary_S05_terminal_state_recovery_v1/managing_terminal_driver_recovery_return_v1.md` | Historical pointer; file bytes and classification unverified |
| Reported release ZIP name | `batch0004_PRIMARY_S05_TERMINAL_DRIVER_STATE_RECOVERY_v1.zip` | Historical filename, not verified present content |
| Final execution authorization SHA-256 | `22270e91bccd75ab451a0b36a14fa1aefef4414963071847d502ab3027858753` | Historical identity only |
| Final execution policy SHA-256 | `7236c9d0f49b568b508915b8a8f03efac2a723831e07f74fe2a5e1c995f7f34e` | Historical identity only |
| Authorization/policy binding SHA-256 | `3199ccb1ac3dc753940a38f1c5d53911633d4b68fa9474a54e83098ba846de26` | Historical identity only |
| Original trusted MANAGING approval SHA-256 | `b228cfaf437527dd9bde2a971312522a8feb1c2cb6f391da45ed5e64c07e7780` | Historical identity only |
| Original controlled-stop checkpoint SHA-256 | `bd109fe88e9c5e39ba3e0d3f1a4d75ea71c9b7ac469a4ab8721b97a44dc09fb7` | **October 15 historical checkpoint**, not present checkpoint 54 |
| Later historical checkpoint attestation SHA-256 | `5d1174955a09babd2e1fd817c0f6b76bf9dfc88dde420fbd01eabb167d639108` | Subsequent corroborating historical identity |

**Earlier, unsuccessful release — distinguish explicitly:** earlier driver `92dd25c1dc1ec3550ed39e02e22657b0e1398af91748a3d8f0715ecee5236126`; earlier release `44e98544f523fc9185adf11557c02db02270646fda12fa5048bc207583fd1e18`; earlier ZIP `c497069daa3e6617b1a058eb5e6695db7b883b2aeb2399d2a6b049a959a8fa69`. Do not attribute the successful frozen units to this predecessor.

## 4. What MANAGING accepted, and what was not independently reproduced

**Historical acceptance:** MANAGING accepted the corrected release for the original retry, and later accepted the controlled-stop state preserving U0001–U0011. The reported checkpoint contains 275 frozen records and U0012 unfinished. Owner initiation of the overall terminal workflow is distinct from the subsequent automated, sequential multi-unit processing. The history does not establish eleven independent manual starts or current `MAX_NEW_UNITS=1` compatibility.

**Evidentiary limits:** These findings are recovered from historical messages, summaries and handoffs. This historical record did **not** independently inspect the original receipt bytes, scientific records, checkpoint, runtime or executable. An accepted aggregate frozen-state report does not prove which immutable runtime/configuration produced each particular unit. Later A10 installation or preservation receipts do not close the October 15 execution binding.

## 5. November 2026 bounded Codex lookup — observed vs not established

Codex reported that two files existed as regular files with UID501/GID20, mode 0644 and one hard link:

| Exact file | Observed size | Current classification / byte verification |
|---|---:|---|
| `.../batch0004_primary_S05_terminal_state_recovery_v1/terminal_prestart_driver_recovery_v1.py` | 16,207 bytes | NONPROTECTED classification **NOT_ESTABLISHED**; current SHA-256 **not checked**. |
| `.../batch0004_primary_S05_terminal_state_recovery_v1/managing_terminal_driver_recovery_return_v1.md` | 3,830 bytes | NONPROTECTED classification **NOT_ESTABLISHED**; contents and SHA-256 **not checked**. |

The bounded lookup found no accepted NONPROTECTED inventory matching the identified driver/report identities. Codex stopped before reading or hashing them. File existence, extension, permissions, ownership, and historically named paths do not establish permitted classification. Neither path is authorized for inspection by this note.

## 6. Explicitly unresolved links

1. Independently authenticated current file bytes for the corrected driver and associated Managing report.
2. Accepted NONPROTECTED classification for those two exact artifacts (and any original receipt subsequently identified).
3. The exact immutable launch configuration path/SHA-256 binding driver, authorization/policy, run, input, checkpoint and interpreter.
4. The actual historical interpreter absolute path, version and hash used in the successful run. A later interpreter inventory does not prove the October 15 runtime.
5. Original U0001 scientific validation/Policy B PASS receipt and 25-record checkpoint-commit receipt with exact paths/hashes.
6. Per-unit authenticated execution-to-acceptance binding through U0011.
7. Whether the original multi-unit driver meets any present one-unit, single-use, Owner/executor separation or runtime controls; **not established and not assumed**.
8. Any alternative successful REAL workflow with a stronger authenticated transaction-specific receipt. The accessible conceptual/ADMIN-adjacent historical summary found none, but did not prove none existed.

**Overall classification:** `HISTORICAL_EXECUTION_CONTEXT = PARTIAL` (significant corroborating history); `HISTORICAL_AGGREGATE_275_RECORD_ACCEPTANCE = HISTORICALLY_MANAGING_ACCEPTED`; `EXACT_MANUAL_ENTRYPOINT_TO_ACCEPTED_UNIT_BINDING = NOT_ESTABLISHED`.

## 7. Controlling current boundary (recorded at preparation, not superseded by this note)

```text
C06 = CONTROLLED_STOP
CHECKPOINT = 54
U0012 = PENDING__TEN_HISTORICAL_ATTEMPTS
ATTEMPT11_REAL = NOT_AUTHORIZED
U0013 = PROHIBITED
REAL_ACTIVATION = HARD_DISABLED
```

This is a historical snapshot only. Consult the controlling current `PROJECT_CONTEXT.md` and actual approved decisions for later lifecycle/current authority. Historical approval hashes, launch success, or this record cannot authorize REAL activity, protected data inspection, B53 engineering, checkpoint changes, or reuse of the old driver.

## 8. Evidence provenance and confidence

This note consolidates user-supplied historical conversation handoffs and bounded Codex host observations; **it is not a newly conducted independent forensic verification**.

| Source / recovered handoff | Contribution | Reliance limit |
|---|---|---|
| `Pasted text(20261109-044244).txt` — original creation-chat handoff | Original 20×25 partition, corrected driver path/hash, early launch sequence, aggregate checkpoint identities | Historical reconstruction; explicit missing per-unit receipts and full config/runtime binding. |
| `Pasted text(20261109-050736).txt` — October 15 MANAGING evidence recovery | Historical MANAGING decisions and dated UTC references, corrected release and 275-row acceptance | Historical conversation review; primary acceptance receipts and classification not recovered. First 62 lines were unrelated GUI-smoke context. |
| `Pasted text(20261109-050148).txt` — historical MANAGING continuity handoff | Governance boundary and missing-evidence summary | Continuity instructions, **not** an additional verification result. |
| `Pasted text(20261109-051621).txt` — broader historical discovery from conceptual-learning chat | No better independently established alternative REAL success in accessible history | **Not an independent ADMIN forensic review**; visibility incomplete. |
| Owner-provided bounded Codex V2 and focused exact-file lookup returns | Later A10 receipts did not bind original success; current exact-file existence/metadata; stopped at classification | `CODEX_REPORTED`, not MAIN-independent host verification; no protected access. |

## 9. Publication and change-control boundary

**Published repository path:** `docs/history/batch0004_s05_2026_10_15_historical_real_execution_evidence.md`

- The **Milestone Review Reference Map** links once to this nonauthorizing history from its existing Batch0004/S05 evidence-navigation area. This record is not a checkpoint tracker or an authorization artifact.
- `PROJECT_CONTEXT.md` remains the sole controlling broad current lifecycle reference and is unchanged by this historical publication.
- Source handoffs and relevant receipts remain unchanged. This publication does not access, bundle, open or copy protected checkpoint, unit workspace, frozen scientific/validation/holdout payloads, or Class C body data.
- This documentation-only publication does not change code, tests, runtime, recovery, checkpoint, REAL activation or authorization.

**Closing archival disposition:** `DOCUMENT_HISTORICAL_FINDINGS__PRESERVE_EVIDENCE_LIMITS__CLOSE_BROAD_CHAT_SEARCH__NO_EXECUTION_AUTHORITY`.
