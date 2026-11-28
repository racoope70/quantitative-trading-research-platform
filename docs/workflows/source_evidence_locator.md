# QTRP — Source and Evidence Locator

**Role:** Nonauthorizing, public-facing index of *accepted* NONPRODUCTION source identities and engineering evidence. It is not a live custody attestation, access grant, authorization record, runtime integration decision, or substitute for the accepted evidence package. For lifecycle and authorization state, see [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md).

## A0012 five-source reference baseline — accepted 2026-11-16

**Owner acceptance:** `ACCEPT_COMPLETED_FIVE_SOURCE_BASELINE_WITHIN_EVIDENCE_SCOPE`.

**Controlling disposition:** `ACCEPT_E_SCHEMA_FIRST_RECOVERY__CLOSE_FIVE_SOURCE_BASELINE__RETAIN_COMPATIBILITY_GATES`, accepted by OWNER within the verified source/custody evidence scope. The five A–E source references were classified NONPROTECTED, authenticated to their historical identities, and staged in isolated, *reference-only* NONPRODUCTION custody. Four source references and the original 64-file donor were **not** reauthenticated during E's final schema-first task; their prior accepted receipts were retained.

| Dependency | Logical source identity (not a host location) | Accepted SHA-256 | Bytes | Reference staging |
| --- | --- | --- | ---: | --- |
| **A — Deployment binding manifest** | `REFERENCE_DEPLOY/deployed_runtime_composition_g01_g05_resumed_v1/DEPLOYED_RUNTIME_BINDING_MANIFEST.json` | `2ce533284245735e960c6e3694bf9f9abf8b8bb30fcff1b32da0970f2e79994e` | 38,376 | Accepted PASS (reference only) |
| **B — REAL S04 bridge V3** | `REFERENCE_DEPLOY/real_s04_validator_input_bridge_v1/real_s04_validator_input_bridge_v3.py` | `c3673d27f95f6d11950d2ddcc534e2768c169a8dd99d1982f92857774f8cae3b` | 10,131 | Accepted PASS (reference only) |
| **C — Transport guard** | `ROOT/transport_guard.py` | `d6bac7270b79f14edf1ab007f833dbc22276166e7077ce4610c8a74895dca179` | 4,196 | Accepted PASS (reference only) |
| **D — Original release descriptor** | `REFERENCE_DEPLOY/REAL_RUNTIME_CANDIDATE_RELEASE_MANIFEST_V2.json` | `00d35a429b23e3967478778f9c28c1265fd25dad0f0da5d7feba55d0a6fb9260` | 5,341 | Accepted PASS (reference only) |
| **E — Preparation-binding manifest** | `PREPARED/preparation_binding_manifest.json` | `dafb1ebba47545e080274b6822f2ad7de8bea5a68b16af531f6508d72f3fe76a` | 4,191 | Accepted PASS (reference only) |

**Controlling completion evidence:** `BATCH0004_A0012_E_SCHEMA_FIRST_FINAL_CLASSIFICATION_V1_EVIDENCE.zip`; SHA-256 `82707086fc70d809c9acceb8a13738a7b43358f7c34195f8ec8d54f24a501f88`; **77,116 bytes; 19/19 archive members** verified against the accepted manifest, member lengths/hashes and ZIP CRC. Evidence package and source-custody locations are indexed in a separate **Owner-private continuity record**; do not infer that a public repository contains or backs up the archive.

**E classification:** Pinned bridge V3 producer and published JSON construction supplied a closed schema of **17 required top-level fields and 31 field contracts**. The three booleans are fixed `false` nonauthorization/nonprovision declarations. Schema gate PASS preceded E's one authorized inspection; E conformed, was classified NONPROTECTED, matched its expected SHA-256, and passed exclusive source-copy integrity. The original source/configuration lineage relationships A→C, B→E, E→B, E→D, and consumer→E are supported within the recorded static evidence scope. Referenced scientific data was **not** opened or validated.

**Historical Gate 0B distinction:** The original Gate 0B review had incomplete source coverage. Later Phase A/B donor verification/transfer and the five-source source-reference baseline were completed in separate bounded operations. The later baseline PASS does not rewrite the historical Gate 0B result or imply that Gate 0C was reached.

## Other accepted NONPRODUCTION engineering evidence

| Artifact / purpose | Evidence identity | Recorded limit |
| --- | --- | --- |
| A0011 guard-correction donor | 64-file inventory SHA-256 `0e03a3c24970f854bf900a59937d0dea2226ec3f0e60a885ab56b0096b01401c`; release SHA-256 `dac825ef66d3255f54c8c879de0fd6977bdd3d6566a0785525544d964e8ee6db` | Phase A/B accepted donor/candidate custody; the donor is NONPRODUCTION and not a REAL-compatible installation. Historical host location is Owner-private. |
| Guard-correction provenance | `QTRP_A11_CHECKPOINT56_GUARD_CORRECTION_EVIDENCE.zip`, SHA-256 `ef2c0e08fc7a07a5a639ba9cb67f59409c26183b6f15dbcb8af71d5ec1fab35c` | Historical NONPRODUCTION provenance; no public or durable backup is established by this index. |
| Automation Reliability Engineering Implementation V1 | `AUTOMATION_RELIABILITY_ENGINEERING_IMPLEMENTATION_V1_EVIDENCE.zip`, SHA-256 `ada0e352e6a22703040252aa84382efd3f9d13ca7e733f993d7406bb97dfbde5` | Accepted bounded C1–C3 source and 27/27 selected final-source synthetic results. See [technical completion report](../reports/automation_reliability_engineering_v1_completion.md). |
| A0012 synthetic readiness | `BATCH0004_U0012_A0012_PROSPECTIVE_READINESS_V1_EVIDENCE.zip`, SHA-256 `df3ca9d91256dd398e90e050776350603dde0be252424e02219468472bcf0ea5` | MANAGING-reported 14/14 selected synthetic cases, including diagnostic qualification; REAL A0012 behavior remains unqualified. |
| A0012 source-donor discovery | Discovery evidence ZIP SHA-256 `fb972a0c3e70e3bc5bf4bd91aabec0e987fd96e256d5e60c800c885c0479d3bd` | `CONSOLIDATED_SOURCE_DONOR_DISCOVERY_REPORT.md` and its receipts record historical donor provenance and search scope; do not restart discovery solely to rebuild this index. |
| A0012 independent-case NONPRODUCTION compatibility | Accepted 67-file revision SHA-256 `7579e64784ec89610f48189c3bcd500f6655df3f27bfb3c7bc37f95f4f350f09` | 9/9 focused synthetic interface groups PASS; no installed REAL case, provider invocation or scientific acceptance. Earlier 66-file D1–D4 source qualified 11/11 within its scope. |
| A0012 targeted R/C/P compatibility | Corrected 67-file revision SHA-256 `e16d6740fc3ea7f00e57f8bced78eedd3f940ee5e1d30a4421812521caece6e2`; accepted evidence ZIP SHA-256 `5dce2858e95c4af8959c49c0907c52c6a3ca9f937974a1f8f3425b97e942ff9d` | 7/7 focused NONPRODUCTION PASS; R/C/P mapping only. Eight accepted parent source timestamps changed despite byte-identical rewrites; Owner acknowledged the bounded metadata exception. |
| A0012 accountable designation instruments | Accepted nonapplied six-member decision ZIP SHA-256 `a71f6377307ec80e2bf4d01ecf6693191c4e1ae05628a42e9fc63acb3bb3dfbe` | Designation decisions A–D are prepared, but authoritative allocation, P4/custody, state and installable REAL release remain unassigned; private evidence is not published here. |
| Final A0012 consolidated NONPRODUCTION engineering — accepted 2026-11-27 | 73-file revision `f17a0264f7fb7fb0c1b0aab969c2b68ea67be0453c94ddf59aae690aae24cfe4`; `QTRP_A0012_REAL_INTERFACE_DURABLE_COMPLETION_NP_V1_EVIDENCE.zip`, SHA-256 `e38fac284d75fd8d2f12bbbb7e7626db4bfde780979098f02bd955357b251b55` (293 members) | Accepted 59/59 interface and subsequent 32/32 durable/source/affected-regression qualifications, separately scoped with unaffected evidence reused. Actual synthetic filesystem evidence ran as UID501; modeled roles do not extend prior D3 OS evidence or establish actual REAL designation, installation, state/custody conformance, provider behavior or scientific acceptance. See [technical completion and exact limits](../reports/automation_reliability_engineering_v1_completion.md#accepted-final-consolidated-nonproduction-engineering--2026-11-27). |

## Accepted milestone boundaries and usage

- `PHASE_A = PASS`; `PHASE_B = PASS`; `FIVE_SOURCE_BASELINE = PASS__ACCEPTED`; `SOURCE_RECOVERY = CLOSED_WITHIN_ACCEPTED_EVIDENCE_SCOPE`.
- **Historical snapshot at the 2026-11-16 source-baseline acceptance (not current Phase C status):** `PHASE_C_ENGINEERING = PENDING`; `TEN_INTERFACE_COMPATIBILITY_ASSESSMENT = NOT_AUTHORIZED`; `BEHAVIORAL_COMPATIBILITY = NOT_TESTED`; `GATE_0C = NOT_REACHED`.
- **Later accepted status as of 2026-11-22:** See [current Batch0004/U0012 context](../../PROJECT_CONTEXT.md#batch0004--primary-s05--u0012-automation-continuation--accepted-state-2026-11-22) and the [bounded engineering completion record](../reports/automation_reliability_engineering_v1_completion.md); subsequent NONPRODUCTION engineering and design acceptance did not authorize Gate 0C, REAL A0012 or U0013.
- `REAL_A0012 = NOT_AUTHORIZED`; `U0013 = PROHIBITED`; A0011 recovery authority remains consumed/nonreusable.
- Source identity authentication and reference staging **are not** executable integration, behavioral compatibility, current scientific validity, live source availability, REAL authorization, or production readiness.
- Consult the accepted evidence and exact Owner authorization before any later source access, source modifications, testing, or gate progression. Do not repeat accepted source recovery absent specific contradictory evidence.
- Before opening, hashing, copying or using an artifact, establish its permitted NONPROTECTED classification and current exact access authority. Historical identities and accepted receipts do not grant new access.
- This locator does not authorize searching additional repositories, Downloads, backups or protected locations. Use accepted provenance and the current task scope before any such discovery.
- Check the exact source revision, inventory, byte lengths, hashes, release/configuration/runtime bindings and compatibility scope before reuse. Keep historical versions distinct; never splice unrelated revisions into a claimed coherent source.
- Do not publish host-specific paths, source bodies, raw preparation values, protected scientific objects, credentials, checkpoint/journal bodies, or private custody receipts in this public locator.
- Private preservation receipts carry storage and backup findings. This public index makes no live host-location, independent-backup or retention guarantee; detailed paths and preservation gaps remain Owner-private.
