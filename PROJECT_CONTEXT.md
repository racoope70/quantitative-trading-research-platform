# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C4_COMPLETED
active_major_phase = NONE
proposed_next_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
C1_phase_status = COMPLETED
C1_completion_effect = EFFECTIVE
C2_phase_status = COMPLETED
C2_authorization_status = AUTHORIZED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_effect = EFFECTIVE
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_completion_decision = docs/decisions/C3_completion_decision.md
C3_completion_decision_id = GOV-DEC-0008
C3_completion_owner_decision = ACCEPTED
C3_completion_effect = EFFECTIVE
C3_technical_work_status = COMPLETE
C4_environment_entry_prerequisite = SATISFIED
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_owner_decision = ACCEPT_C4_TECHNICAL_COMPLETION_AND_AUTHORIZE_BOUNDED_C4_COMPLETION_ALIGNMENT_RECORDING
C4_completion_status = ACCEPTED
selected_C4_subset_completion = 21_OF_21_COMPLETE
C4_technical_completion = YES
final_independent_C4_technical_closeout_audit = PASS
required_additional_C4_technical_work = NONE
C4_technical_work_status = COMPLETE
C4_completion_effect = EFFECTIVE
HISTORICAL_C4_AUTHORIZATION = PRESERVED
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C5_entry_prerequisite = SATISFIED
C5_authorization_effect = NONE
next_permitted_workstream = NONE__C5_REQUIRES_SEPARATE_OWNER_AUTHORIZATION
```

## 1. Project

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting:

- Standalone PPO v2.
- PPO plus Random Forest gate.
- PPO plus XGBoost gate.
- Fair comparison of eligible frozen candidates using common data, splits, costs, benchmarks, and one shared untouched final holdout.
- Publication-quality research, controlled paper trading, and possible later live-capital consideration under separate authorization.

Historical repositories remain evidence and engineering sources, not runtime dependencies or sources of current authorization.

## 2. Controlling role

This document is the sole controlling source for:

- Lifecycle, active phase, and phase status.
- Authorized and prohibited work.
- Current material blocker or decision.
- Dataset, model, environment, and access status.
- Latest completed phase, active milestone, and next permitted workstream.
- Required maps and latest material records.

It does not contain detailed chronology or a completed governance chain. Git history and VS Code verify implementation state; they do not establish current authorization.

## 3. Lifecycle, entry gate, and current status

```text
PRE_C0_DRAFT_REVIEW
→ C0_ACTIVE
→ C0_COMPLETED
→ C1_ACTIVE
→ C1_COMPLETED
→ C2_ACTIVE
→ C2_COMPLETED
→ C3_ACTIVE
→ C3_COMPLETED
→ C4_ACTIVE
→ C4_COMPLETED
```

The aligned target state records C0 through C4 as completed. The bounded C4 authorization recorded by `docs/decisions/C4_authorization_decision.md` remains historical accepted evidence, but no current C4 execution authorization remains after completion. C5 and every later phase remain unauthorized and require separate Owner authorization.

```text
current_material_blocker = NONE
current_lifecycle_state = C4_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE
C1_status = COMPLETED
C1_completion_effect = EFFECTIVE
C2_status = COMPLETED
C2_completion_effect = EFFECTIVE
C3_status = COMPLETED
C3_completion_effect = EFFECTIVE
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_status = ACCEPTED
selected_C4_subset_completion = 21_OF_21_COMPLETE
C4_technical_completion = YES
final_independent_C4_technical_closeout_audit = PASS
required_additional_C4_technical_work = NONE
C4_technical_work_status = COMPLETE
C4_completion_effect = EFFECTIVE
HISTORICAL_C4_AUTHORIZATION = PRESERVED
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C5_entry_prerequisite = SATISFIED
C5_authorization_effect = NONE
next_permitted_workstream = NONE__C5_REQUIRES_SEPARATE_OWNER_AUTHORIZATION
current_model_candidate = NONE
current_deployment_candidate = NONE
```

C4 completion does not reopen C3 and does not authorize C5 or any later operational, data, training, holdout, trading, scientific-host, or public-release work.

## 4. Completed C2 scope and preserved C1 evidence

C2 completed the accepted non-operational repository-skeleton and migration-preparation scope.

The completed C2 package is limited to:

- Creating the three accepted C2 output documents.
- Creating the approved `src/quantitative_trading_research/` responsibility-document skeleton.
- Creating the exact approved empty or docstring-only package markers.
- Providing high-level dispositions for all 82 accepted C1 manifest items.
- Providing full destination, wave, limitation, and verification planning only for C3/C4-relevant items.
- Maintaining the authoritative `items` and `unresolved_limitations` YAML collections.
- Preparing a bounded C3 environment-reconstruction handoff.
- Updating the existing documentation-consistency workflow with bounded document, structure, YAML, and referential-integrity validation.

The accepted C1 outputs remain immutable:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

The accepted C1 completion evidence remains:

```text
independent_C1_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
independent_C1_audit_classification = PASS
bounded_section_coverage = 15_OF_15_CONFIRMED
completion_decision = docs/decisions/C1_completion_decision.md
completion_decision_id = GOV-DEC-0004
completion_decision_owner_status = ACCEPTED
accepted_C1_artifacts = IMMUTABLE
```

Historical repositories remain read-only evidence and engineering sources. They are not runtime dependencies or sources of current authorization.

## 5. Continuing non-authorization

C2- and C3-specific execution restrictions were phase-scoped controls and are retained in their accepted decisions and Git history rather than presented here as current restrictions. The completed C4 state continues to prohibit all work that requires a later authorization.

C4 completion does not authorize:

- C5 or any later phase.
- Provider selection, acceptance, credentials, authenticated access, market-data requests, entitlement checks, or production provider operations.
- Dataset selection, acceptance, generation, reconstruction, remediation, or final universe selection.
- Model training, retraining, model selection, qualification, promotion, or new model artifact creation.
- Shared final-holdout access.
- Scientific-host qualification.
- Broker-account activity, paper orders, live orders, paper trading, or live trading.
- Public release or deployment-readiness claims.
- Change Point Analysis implementation.

Historical repository material remains evidence and engineering lineage, not current runtime dependency or authorization.

## 6. Current material decisions

```text
proposed_repository_visibility = PRIVATE
presumptive_architecture_source = racoope70/ppo-trading-pipeline
canonical_package_name = quantitative_trading_research
automatic_module_acceptance = NO
accepted_C1_artifacts = IMMUTABLE
abstract_interface_stubs_during_C2 = NOT_AUTHORIZED
provider_or_broker_specific_implementation_during_C2 = NOT_AUTHORIZED
supported_python_version = 3.13__CPYTHON_3.13.14
final_ticker_universe = NOT_SELECTED
```

## 7. Dataset status

```text
dataset_status = NO_NEW_REPOSITORY_DATASET_SELECTED_OR_ACCEPTED
provider_acceptance_status = NONE
dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED
final_ticker_universe_status = NOT_SELECTED
historical_six_symbol_group_status = CANDIDATE_ONLY
```

Historical v3.08 established only that no acceptable raw candidate existed under its old zero-missing-slot-tolerance contract.

## 8. Model status

```text
legacy_ppo_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
legacy_ppo_random_forest_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
ppo_v2_status = HISTORICAL_SCAFFOLDING_EXISTS_NOT_TRAINED_IN_NEW_REPOSITORY
random_forest_gate_status = FUTURE_PHASE
xgboost_gate_status = FUTURE_PHASE
current_model_candidate = NONE
current_deployment_candidate = NONE
```

Historical models do not become current candidates through review, classification, completion, or migration recommendation.

## 9. Environment and access status

```text
canonical_environment_status = ESTABLISHED_AND_EFFECTIVE
canonical_platform = LINUX_X86_64_AMD64
supported_python_version = 3.13__CPYTHON_3.13.14
dependency_environment_source_phase = C3_COMPLETED
network_or_api_testing = NOT_AUTHORIZED
market_data_access = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
scientific_host_qualification = NOT_AUTHORIZED
public_release = NOT_AUTHORIZED
```

The accepted C3 environment remains the controlling canonical environment foundation. C4 completion does not redesign or reopen it.

## 10. Completed governance evidence through C4

C0 through C4 have accepted lifecycle records. The current controlling target is C4 completed with no active major phase and no C5 authorization.

```text
C0_completion_decision = docs/decisions/C0_completion_decision.md
C0_completion_decision_id = GOV-DEC-0002
C1_completion_decision = docs/decisions/C1_completion_decision.md
C1_completion_decision_id = GOV-DEC-0004
C1_completion_effect = EFFECTIVE
C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_decision_id = GOV-DEC-0005
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_effect = EFFECTIVE
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_completion_decision = docs/decisions/C3_completion_decision.md
C3_completion_decision_id = GOV-DEC-0008
C3_completion_effect = EFFECTIVE
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_owner_decision = ACCEPT_C4_TECHNICAL_COMPLETION_AND_AUTHORIZE_BOUNDED_C4_COMPLETION_ALIGNMENT_RECORDING
C4_completion_status = ACCEPTED
selected_C4_subset_completion = 21_OF_21_COMPLETE
final_independent_C4_technical_closeout_audit = PASS
required_additional_C4_technical_work = NONE
C4_completion_effect = EFFECTIVE
C5_authorization_effect = NONE
```

No prohibited later-phase technical execution is authorized by these completion records.

## 11. Major milestone pointers

```text
latest_completed_major_milestone = C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
active_major_milestone = NONE
latest_authorization_decision = docs/decisions/C4_authorization_decision.md
latest_completion_record = docs/decisions/C4_completion_decision.md
next_permitted_workstream = NONE__C5_REQUIRES_SEPARATE_OWNER_AUTHORIZATION
```

## 12. Required reading and new-chat orientation

A fresh project chat must:

1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.

```text
latest_material_decision = docs/decisions/C4_completion_decision.md
latest_material_completion_record = docs/decisions/C4_completion_decision.md
latest_material_independent_audit = FINAL_C4_INDEPENDENT_TECHNICAL_CLOSEOUT_AUDIT__PASS
```

## 13. Maintenance guidance

```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
