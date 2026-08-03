# Milestone Review Reference Map

```text
document_status = ACTIVE_NON_AUTHORIZING_REFERENCE
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
| C0 — Canonical Governance Foundation and Legacy Migration Charter | Create the private repository and establish governance, C1 templates, minimal structure, documentation-only controls, and audit instructions | Owner accepts the proposed C0 scope | Complete package committed; audit passes; owner accepts closure; aligned controlling state records `C0_COMPLETED` |
| C1 — Legacy Evidence Classification and Architecture Migration Design | Review the bounded historical sections and material 2v evidence; recommend retained controls, canonical architecture, and migration | C0 completed and C1 authorized | Three C1 outputs accepted; risk-proportional audit passes; owner accepts completion; no executable migration occurred; aligned controlling state records `C1_COMPLETED` |
| C2 — Canonical Repository Skeleton and Migration Preparation | Refine canonical package boundaries, interfaces, migration order, and verification plans without executable legacy migration | C1 completed and C2 separately authorized | Migration-ready skeleton and preparation package accepted |
| C3 — Python Environment and Dependency Reconstruction | Select the supported Python version and establish the reproducible canonical environment | C2 preparation accepted and C3 separately authorized | Clean environment, lock, compatibility findings, and audit accepted |
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

C1 phase-exit status:

```text
C1_phase_exit_status = ACCEPTED_AND_EFFECTIVE_THROUGH_ALIGNED_CONTROLLING_STATE
C1_completion_effect = EFFECTIVE
C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_status = AUTHORIZED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_phase_exit_status = ACCEPTED_AND_EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_STATE_AND_SUCCESSFUL_POST_MERGE_VALIDATION
C2_completion_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_POST_MERGE_VALIDATION
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_activation_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_EXACT_POST_MERGE_VALIDATION
C4_authorization_effect = NONE
```

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

The completed C1 review covered all fifteen bounded historical sections.

C1 did not require exhaustive classification of every minor file within a section. The material-record and proportional-review rules remained controlling.

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

## 8. Canonical C0, C1, C2, and C3 curated lookup

```text
2v.GOV.01 — Accepted C0 governance-foundation decision and package
2v.GOV.02 — Independent C0 governance-foundation audit
2v.GOV.03 — C0 completion decision
2v.GOV.04 — C1 phase authorization decision
2v.GOV.05 — C1 completion and closure decision
2v.GOV.06 — C2 phase authorization decision
2v.GOV.07 — C2 completion and closure decision
2v.GOV.08 — C3 phase authorization decision
2v.LEGACY.01 — C1 bounded historical inventory and functional crosswalk
2v.LEGACY.02 — C1 legacy evidence retention matrix
2v.ARCH.01 — C1 technical migration manifest
2v.ARCH.02 — C1 legacy evidence and architecture report
```

### 2v.GOV.02 — Canonical independent-audit evidence

```text
2v_record = 2v.GOV.02
record_type = INDEPENDENT_C0_GOVERNANCE_FOUNDATION_AUDIT
record_path = docs/audits/C0_independent_governance_foundation_audit_report.md
exact_commit_audited = 4f7ab457beb0cf75bcba446009a07f81b47847a0
audit_conclusion = PASS
correction_findings = NONE
remediation_required = NO
reaudit_required = NO
authorization_effect = NONE
C0_completion_effect = NONE
C1_authorization_effect = NONE
```

### 2v.GOV.03 — Canonical C0 completion evidence

```text
2v_record = 2v.GOV.03
record_type = C0_COMPLETION_AND_CLOSURE_DECISION
record_path = docs/decisions/C0_completion_decision.md
decision_id = GOV-DEC-0002
owner_decision = ACCEPT_C0_CLOSURE
owner_acceptance_status = ACCEPTED
owner_disposition_record = PR_4_COMMENT_5117264967
owner_disposition_head_commit = 061243b92df2bf9351a50618dc0f894be34570eb
completion_decision_merge_commit = c4235e466e3a8248fb0a61b342265e3a50dde76a
completion_decision_merge_push_workflow_run = 9
completion_decision_merge_push_workflow_conclusion = SUCCESS
C0_completion_effect = EFFECTIVE
C1_authorization_effect = NONE
```

This record closes C0 when read with the aligned controlling state in `PROJECT_CONTEXT.md`. It does not authorize or activate C1.

### 2v.GOV.04 — Canonical C1 authorization evidence

```text
2v_record = 2v.GOV.04
record_type = C1_PHASE_AUTHORIZATION_DECISION
record_path = docs/decisions/C1_authorization_decision.md
decision_id = GOV-DEC-0003
owner_decision = AUTHORIZE_C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
owner_acceptance_status = ACCEPTED
owner_disposition_record = PR_6_COMMENT_5120803290
owner_disposition_head_commit = 18351d71fa0eedfb8ebdaa2ed9b33d051fd9829a
authorization_decision_merge_commit = 593f8b79246688dc9e17ee961a726f641b4d433e
authorization_decision_pr_validation_run = 12
authorization_decision_pr_validation_conclusion = SUCCESS
authorization_decision_merge_push_workflow_run = 13
authorization_decision_merge_push_workflow_conclusion = SUCCESS
C1_authorization_effect = EFFECTIVE
C1_activation_effect = EFFECTIVE_WHEN_READ_WITH_ALIGNED_PROJECT_CONTEXT
C2_authorization_effect = NONE
```

This map does not independently authorize or activate C1. `2v.GOV.04` records the historical accepted C1 authorization evidence.

### 2v.GOV.05 — Canonical C1 completion evidence

```text
2v_record = 2v.GOV.05
record_type = C1_COMPLETION_AND_CLOSURE_DECISION
record_path = docs/decisions/C1_completion_decision.md
decision_id = GOV-DEC-0004
owner_decision = ACCEPT_C1_COMPLETION_DECISION
owner_acceptance_status = ACCEPTED
owner_disposition_record = PR_8_COMMENT_5149557106
owner_disposition_head_commit = f8a75447ad6819efa5fbef10fe0ff36f115f8185
authorized_merge_method = SQUASH
completion_decision_merge_commit = 7a5ed69620a773a0a0941239bc568678be41fa9a
completion_decision_pr_validation_run = 16
completion_decision_pr_validation_conclusion = SUCCESS
completion_decision_post_merge_manual_validation_run = 17
completion_decision_post_merge_manual_validation_event = WORKFLOW_DISPATCH
completion_decision_post_merge_manual_validation_commit = 7a5ed69620a773a0a0941239bc568678be41fa9a
completion_decision_post_merge_manual_validation_conclusion = SUCCESS
independent_C1_audit_record = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
independent_C1_audit_classification = PASS
bounded_section_coverage = 15_OF_15_CONFIRMED
C1_completion_effect = EFFECTIVE
C2_authorization_effect = NONE
```

This record closes C1 only when read with the accepted aligned controlling state in `PROJECT_CONTEXT.md`. It does not independently authorize or activate C2.

### 2v.GOV.06 — Canonical C2 authorization evidence

```text
2v_record = 2v.GOV.06
record_type = C2_PHASE_AUTHORIZATION_DECISION
record_path = docs/decisions/C2_authorization_decision.md
decision_id = GOV-DEC-0005
owner_decision = ACCEPT_GOV_DEC_0005_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_ACTIVATION_ALIGNMENT
owner_acceptance_status = ACCEPTED
decision_basis_commit = 8e8fe0d0fb66dddd2e73e5024add796c7004eab9
manager_review_classification = PASS
authorized_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
authorized_scope = C2_NON_OPERATIONAL_SKELETON_AND_MIGRATION_PREPARATION_ONLY
accepted_C1_artifacts = IMMUTABLE
authorized_recording_branch = c2-authorization-decision
authorized_merge_method = SQUASH
C2_activation_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN
C3_authorization_effect = NONE
```

This map does not independently authorize or activate C2. `2v.GOV.06` becomes effective only when read with the accepted decision and aligned controlling state on canonical `main`. It does not authorize C3 or any later phase.

### 2v.GOV.07 — Canonical C2 completion evidence

```text
2v_record = 2v.GOV.07
record_type = C2_COMPLETION_AND_CLOSURE_DECISION
record_path = docs/decisions/C2_completion_decision.md
decision_id = GOV-DEC-0006
owner_decision = ACCEPT_GOV_DEC_0006_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_COMPLETION_ALIGNMENT
owner_completion_decision_status = ACCEPTED
manager_review_status = PERFORMED
manager_review_classification = PASS
material_findings = NONE
required_corrections = NONE
independent_C2_audit_required = NO_CONDITIONAL_TRIGGER_IDENTIFIED
C2_package_pull_request = 11
C2_package_reviewed_head_commit = c7f5f39c54eaa40788ba3fcd4a36abc724304d3c
C2_package_merge_commit = 87b3460f0b112314ec1dd2cb1faa847fa5572b6f
C2_package_post_merge_validation_run = 24
C2_package_post_merge_validation_conclusion = SUCCESS
authorized_recording_branch = c2-completion-alignment
authorized_merge_method = SQUASH
C2_completion_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_POST_MERGE_VALIDATION
C3_authorization_status = NOT_AUTHORIZED
C3_authorization_effect = NONE
```

This map does not independently close C2. `2v.GOV.07` records the accepted
completion decision and becomes effective only when read with the aligned
controlling state on canonical `main` after successful validation of the exact
completion-alignment squash commit.

It does not authorize C3 or any later phase.

### 2v.GOV.08 — Canonical C3 authorization evidence

```text
2v_record = 2v.GOV.08
record_type = C3_PHASE_AUTHORIZATION_DECISION
record_path = docs/decisions/C3_authorization_decision.md
decision_id = GOV-DEC-0007
owner_decision = ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT
owner_acceptance_status = ACCEPTED
decision_basis_commit = fc360d1e57f04fb258e11821ffd3eb2c376828f2
manager_review_status = PERFORMED
manager_review_classification = PASS
material_findings = NONE
required_corrections = NONE
owner_selection_matrix_id = C3_OWNER_SELECTION_MATRIX_V1
owner_selection_matrix_status = ACCEPTED
remaining_material_owner_decisions = NONE
authorized_phase = C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
authorized_scope = BOUNDED_C3_ENVIRONMENT_DEPENDENCY_CONFIGURATION_AND_OFFLINE_DIAGNOSTICS_ONLY
authorized_recording_branch = c3-authorization-activation-alignment
authorized_merge_method = SQUASH
C3_activation_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_EXACT_POST_MERGE_VALIDATION
C4_authorization_effect = NONE
```

This map does not independently authorize or activate C3. `2v.GOV.08`
becomes effective only when read with the accepted decision and aligned
controlling state on canonical `main` after successful validation of the exact
activation-alignment squash commit.

It does not authorize C4 or any later phase.

### 2v.LEGACY.01 — C1 bounded historical inventory and functional crosswalk

```text
2v_record = 2v.LEGACY.01
record_type = C1_BOUNDED_HISTORICAL_INVENTORY_AND_FUNCTIONAL_CROSSWALK
record_path = docs/reports/C1_legacy_evidence_and_architecture_report.md
authorization_effect = NONE
```

### 2v.LEGACY.02 — C1 legacy evidence retention matrix

```text
2v_record = 2v.LEGACY.02
record_type = C1_LEGACY_EVIDENCE_RETENTION_MATRIX
record_path = docs/migration/legacy_evidence_retention_matrix.csv
authorization_effect = NONE
```

### 2v.ARCH.01 — C1 technical migration manifest

```text
2v_record = 2v.ARCH.01
record_type = C1_TECHNICAL_MIGRATION_MANIFEST
record_path = docs/migration/technical_migration_manifest.yaml
authorization_effect = NONE
```

### 2v.ARCH.02 — C1 legacy evidence and architecture report

```text
2v_record = 2v.ARCH.02
record_type = C1_LEGACY_EVIDENCE_AND_ARCHITECTURE_REPORT
record_path = docs/reports/C1_legacy_evidence_and_architecture_report.md
authorization_effect = NONE
```

No curated record independently authorizes work.

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

For each bounded historical section, C1:

1. Identified applicable exact legacy 2v entries where defensible and otherwise
   recorded direct, contextual, unresolved, or no-direct functional mappings
   with the associated records.
2. Determined materiality.
3. Reviewed decisive and materially supporting evidence.
4. Identified superseding corrections.
5. Separated durable controls from one-time procedures.
6. Classified retained evidence.
7. Determined consolidation targets and future-phase relevance.
8. Proposed curated new 2v references.
9. Recorded technical migration recommendations separately.

Required classifications were:

```text
CARRY_FORWARD
SUMMARIZE_AND_REFERENCE
HISTORICAL_ARCHIVE_ONLY
OBSOLETE_OR_SUPERSEDED
```

## 10. C1 templates and outputs

C0 templates:

```text
docs/templates/C1_legacy_evidence_retention_matrix_template.csv
docs/templates/C1_technical_migration_manifest_template.yaml
docs/templates/C1_legacy_evidence_and_architecture_report_template.md
```

Completed C1 outputs:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

## 11. C1 completion standard

C1 closed after:

1. Every section in the accepted bounded inventory was reviewed.
2. Applicable legacy 2v entries or functional mappings were identified.
3. Material evidence was recorded in the completed retention matrix.
4. Durable controls, limitations, and consolidation decisions were captured.
5. Material technical assets were recorded in the completed manifest.
6. The curated 2v structure was accepted.
7. The C1 summary report was completed and accepted.
8. The owner accepted the recommendations and completion decision.
9. One risk-proportional independent C1 audit passed.
10. No executable technical migration occurred in the reviewed repository and GitHub evidence.
11. The accepted decision was validated and merged through pull request #8.
12. The aligned controlling state recorded `C1_COMPLETED`.

```text
C1_phase_exit_status = ACCEPTED_AND_EFFECTIVE_THROUGH_ALIGNED_CONTROLLING_STATE
C1_completion_effect = EFFECTIVE
C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_status = AUTHORIZED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_phase_exit_status = ACCEPTED_AND_EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_STATE_AND_SUCCESSFUL_POST_MERGE_VALIDATION
C2_completion_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_POST_MERGE_VALIDATION
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_activation_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_EXACT_POST_MERGE_VALIDATION
C4_authorization_effect = NONE
```

## 12. Chronology and verification

Exact chronology should be verified through Git history, accepted decisions, material reports, audits, release tags where applicable, and immutable historical links.

Git history and VS Code confirm technical implementation state. They do not control authorization.
