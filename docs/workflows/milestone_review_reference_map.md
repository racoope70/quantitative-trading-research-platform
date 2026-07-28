# Milestone Review Reference Map

```text
document_status = DRAFT_FOR_OWNER_REVIEW
document_role = NON_AUTHORIZING_ROADMAP_AND_EVIDENCE_NAVIGATION
authorization_effect = NONE
controlling_current_state_document = PROJECT_CONTEXT.md
current_phase_status_source = PROJECT_CONTEXT.md
```

## 1. Purpose

This map identifies:

- Major C0–C15 phases.
- Phase purposes.
- Entry and exit gates.
- Material decisions, runs, reports, and audits.
- Curated 2v evidence that a fresh chat must review before beginning a major phase.

It does not control current authorization or duplicate the current authorization block.

## 2. New-chat use

A fresh project chat should:

1. Read `PROJECT_CONTEXT.md`.
2. Locate the applicable phase in this map.
3. Read that phase’s curated 2v records.
4. Read the applicable Future Map section.
5. Inspect Git history and VS Code to verify implementation state.

Git history and VS Code verify implementation and completion evidence. They do not independently authorize work.

## 3. Major phase flow

| Phase | Purpose | Entry gate | Exit gate |
|---|---|---|---|
| C0 — Canonical Governance Foundation and Legacy Migration Charter | Create the private repository and establish governance, C1 templates, minimal structure, documentation-only controls, and audit instructions | Owner accepts the proposed C0 scope | Complete package committed; audit passes; owner accepts closure |
| C1 — Legacy Evidence Classification and Architecture Migration Design | Review the bounded historical sections and material 2v evidence; recommend retained controls, canonical architecture, and migration | C0 completed and C1 authorized | Three C1 outputs accepted; risk-proportional audit passes; no executable migration occurred |
| C2 — Canonical Repository Skeleton and Migration Preparation | Refine canonical package boundaries, interfaces, migration order, and verification plans without executable legacy migration | C1 recommendations accepted and C2 authorized | Migration-ready skeleton and preparation package accepted |
| C3 — Python Environment and Dependency Reconstruction | Select the supported Python version and establish the reproducible canonical environment | C2 preparation accepted | Clean environment, lock, compatibility findings, and audit accepted |
| C4 — Selected Code Migration, Adaptation, and Verification | Migrate approved technical assets into the canonical environment using offline verification and the provider boundary below | C3 environment accepted and C4 scope authorized | Selected migration, adaptation, offline tests, provenance, and audit accepted |
| C5 — Data Source, Calendar, and Initial Universe Decision | Evaluate and accept provider strategy, licensing, permitted use, calendars, and universe criteria | C4 technical foundation accepted and C5 authorized | Data-source, calendar, and universe decision accepted and audited |
| C6 — Dataset Contract Freeze | Define raw and processed dataset requirements before generation | C5 decision accepted | Dataset contracts frozen and independently audited |
| C7 — Dataset Generation and Acceptance | Generate and validate the governed dataset | C6 contracts accepted and data access authorized | Dataset passes contract, provenance, and acceptance audit |
| C8 — PPO v2 Implementation Readiness | Complete tested PPO v2 implementation and training preflight | C7 dataset accepted | PPO implementation and training plan pass readiness audit |
| C9 — PPO v2 Training, Validation, Qualification, and Freeze | Train and validate PPO using predeclared non-final data and reach an accepted terminal disposition without opening the shared final holdout | C8 readiness accepted and training authorized | `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`; shared final holdout untouched |
| C10 — Random Forest Gate Development and Validation | Develop and validate the RF gate only when a qualified frozen PPO foundation exists | `C9_terminal_disposition = QUALIFIED_AND_FROZEN` and `focused_RF_readiness_audit = PASS` | If entered: `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`; if PPO is not qualified: `NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION`; shared final holdout untouched |
| C11 — XGBoost Gate Development and Validation | Develop and validate the XGBoost gate only when a qualified frozen PPO foundation exists and C10 has an accepted terminal disposition | `C9_terminal_disposition = QUALIFIED_AND_FROZEN`, `C10_has_accepted_terminal_disposition = YES`, and `focused_XGBoost_readiness_audit = PASS` | If entered: `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`; if PPO is not qualified: `NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION`; shared final holdout untouched |
| C12 — Eligible-Candidate Freeze, Shared Final Holdout, and Promotion Decision | Freeze all eligible candidates and the common evaluation package; open the shared final holdout once only when at least one eligible candidate exists; otherwise record the no-eligible-candidate outcome without holdout access | All applicable model-family phases have accepted terminal dispositions; all eligible candidates are frozen; common evaluation package is frozen. Final-holdout path additionally requires at least one eligible candidate and express holdout authorization | Eligible-candidate path: shared holdout report and promotion/rejection/inconclusive decision audited. No-eligible-candidate path: `C12_terminal_disposition = NO_ELIGIBLE_CANDIDATE` and `final_holdout_accessed = NO` |
| C13 — Publication Release | Produce a publication- or portfolio-ready research package, including negative or inconclusive findings where applicable | C12 disposition accepted and publication scope authorized | Claims, reproducibility, and publication audit pass |
| C14 — Controlled Paper Trading | Evaluate a promoted candidate in controlled paper operation | Candidate promoted and broker-readiness audit accepted | Operational and economic evidence independently reviewed |
| C15 — Possible Live-Capital Consideration | Decide whether limited live-capital consideration is justified | Sustained paper evidence and separate risk-review authorization | Explicit live-capital disposition; no automatic deployment |

## 4. Model-family branching and shared final holdout

### C9 — PPO v2 terminal dispositions

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

### C10 — Random Forest gate

C10 may begin only when:

```text
C9_terminal_disposition = QUALIFIED_AND_FROZEN
focused_RF_readiness_audit = PASS
```

When PPO is not qualified:

```text
C10_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

When C10 proceeds, valid terminal dispositions are:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

### C11 — XGBoost gate

C11 may begin only when:

```text
C9_terminal_disposition = QUALIFIED_AND_FROZEN
C10_has_accepted_terminal_disposition = YES
focused_XGBoost_readiness_audit = PASS
```

C10 does not need to produce a qualified RF candidate. Any accepted C10 terminal disposition is sufficient when PPO remains qualified.

When PPO is not qualified:

```text
C11_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

When C11 proceeds, valid terminal dispositions are:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

### C12 — Eligible-candidate path

Only model families with:

```text
QUALIFIED_AND_FROZEN
```

are eligible for the shared final holdout.

The final-holdout path requires:

```text
all_applicable_model_family_phases_have_accepted_terminal_dispositions = YES
all_eligible_candidates_are_frozen = YES
at_least_one_eligible_candidate_exists = YES
common_evaluation_package_is_frozen = YES
final_holdout_access_is_expressly_authorized = YES
```

The final holdout must be opened once and applied consistently to every eligible frozen candidate.

Rejected, no-candidate, inconclusive, and not-applicable outcomes remain visible in the final research report.

### C12 — No-eligible-candidate path

When no eligible candidate exists:

```text
C12_terminal_disposition = NO_ELIGIBLE_CANDIDATE
final_holdout_accessed = NO
```

The owner must select one next disposition:

```text
STOP_CURRENT_RESEARCH_CYCLE
PUBLISH_NEGATIVE_OR_INCONCLUSIVE_RESULT
RETURN_TO_A_SEPARATELY_AUTHORIZED_REDESIGN_PHASE
```

An unqualified model must not be forced into the final holdout merely to produce a three-model comparison.

## 5. C4 provider boundary

C4 may migrate and test offline:

- Provider-neutral interfaces.
- Abstract data-source contracts.
- Mocked adapters and fixtures.
- Parsing, normalization, and schema-validation utilities.
- Provisionally selected provider components that do not require network or authenticated access.

C4 does not authorize:

- Provider acceptance.
- Credentials or authenticated access.
- Network or API testing.
- Market-data requests.
- Entitlement verification.
- Provider account inspection.
- Production data-source validation.
- Final provider, feed, adjustment, calendar, or permitted-use decisions.

Those decisions and activities remain in C5 or a later separately authorized data phase.

## 6. C1 bounded historical section inventory

```text
C1_BOUNDED_HISTORICAL_SECTION_INVENTORY

1. Exploratory model development
2. Legacy standalone PPO
3. Legacy PPO plus Random Forest
4. QuantConnect integration
5. Alpaca operational reliability
6. Modular VS Code migration
7. Legacy artifact inventory and model-quality audit
8. Final holdout and candidate selection
9. Paper-trading and execution safety
10. PPO v2 design and data contracts
11. Dataset reconstruction
12. Missing-bar investigation and remediation
13. Market-data provider and SIP-access investigation
14. Python and Alpaca environment diagnosis
15. Governance-system development and lessons
```

C1 must identify the exact historical 2v entry or range for each section during the review.

A historical section may be added during C1 only when it is materially distinct from the existing bounded sections.

The existence of another file, audit, review, commit, run record, or 2v entry is not sufficient by itself to create another historical section.

Any added section must include:

- The reason it is materially distinct.
- The applicable historical repository.
- The applicable legacy 2v range.
- Owner acceptance of the scope amendment.
- Inclusion in the C1 summary report.

C1 does not require exhaustive classification of every minor file within a section. The material-record and proportional-review rules remain controlling.

## 7. Curated 2v purpose and namespaces

The curated 2v lookup points to the minimum material evidence required for a phase. The historical lookup must not be copied wholesale.

```text
2v.GOV.*       = Governance foundation
2v.LEGACY.*    = Legacy evidence classification
2v.ARCH.*      = Architecture and migration
2v.ENV.*       = Python environment
2v.DATA.*      = Data source, calendar, universe, and datasets
2v.PPO.*       = PPO v2
2v.RF.*        = Random Forest gate
2v.XGB.*       = XGBoost gate
2v.HOLDOUT.*   = Shared final holdout and promotion
2v.PUB.*       = Publication
2v.PAPER.*     = Controlled paper trading
2v.LIVE.*      = Live-capital consideration
```

## 8. Initial C0 curated lookup

```text
2v.GOV.01 — Accepted C0 governance-foundation decision and package
2v.GOV.02 — Independent C0 governance-foundation audit
2v.GOV.03 — C0 completion decision
```

`2v.GOV.01` should link:

- `PROJECT_CONTEXT.md`
- `docs/workflows/milestone_review_reference_map.md`
- `docs/workflows/future_validation_training_reference_map.md`
- `docs/decisions/C0_governance_foundation_decision.md`
- `docs/templates/C1_legacy_evidence_retention_matrix_template.csv`
- `docs/templates/C1_technical_migration_manifest_template.yaml`
- `docs/templates/C1_legacy_evidence_and_architecture_report_template.md`
- `README.md`
- `CONTRIBUTING.md`
- `docs/governance/repository_protection_conventions.md`
- `docs/audits/C0_independent_governance_foundation_audit_instructions.md`

## 9. C1 review method

For each bounded historical section, C1 must:

1. Identify the exact legacy 2v entry or range and associated records.
2. Determine materiality.
3. Review decisive and materially supporting evidence.
4. Identify superseding corrections.
5. Separate durable controls from one-time procedures.
6. Classify retained evidence.
7. Determine consolidation targets and future-phase relevance.
8. Propose curated new 2v references.
9. Record technical migration recommendations separately.

Required classifications:

```text
CARRY_FORWARD
SUMMARIZE_AND_REFERENCE
HISTORICAL_ARCHIVE_ONLY
OBSOLETE_OR_SUPERSEDED
```

Administrative records may receive lower-depth inspection after their function, successor, and lack of unique durable conclusions are confirmed.

## 10. C1 templates and outputs

C0 templates:

```text
docs/templates/C1_legacy_evidence_retention_matrix_template.csv
docs/templates/C1_technical_migration_manifest_template.yaml
docs/templates/C1_legacy_evidence_and_architecture_report_template.md
```

Future C1 completed outputs:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

## 11. C1 completion standard

C1 closes when:

1. Every section in the accepted bounded inventory, including any accepted additions, has been reviewed.
2. Exact legacy 2v ranges have been identified.
3. Material evidence is recorded in the completed retention matrix.
4. Durable controls, limitations, and consolidation decisions are captured.
5. Material technical assets are recorded in the completed manifest.
6. The curated 2v structure is proposed.
7. One C1 summary report is completed.
8. The owner accepts the recommendations.
9. One risk-proportional independent C1 audit passes.
10. No executable technical migration occurred.

## 12. Chronology and verification

Exact chronology should be verified through Git history, accepted decisions, material reports, audits, release tags where applicable, and immutable historical links.

Git history and VS Code confirm technical implementation state. They do not control authorization.
