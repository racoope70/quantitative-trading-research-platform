# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C4_ACTIVE
active_major_phase = C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
proposed_next_major_phase = NONE
phase_status = ACTIVE
authorization_effect = C4_SCOPE_ONLY
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
C3_owner_decision = ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT
C3_owner_selection_matrix_id = C3_OWNER_SELECTION_MATRIX_V1
C3_owner_selection_matrix_status = ACCEPTED
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_activation_effect = EFFECTIVE
C3_completion_decision = docs/decisions/C3_completion_decision.md
C3_completion_decision_id = GOV-DEC-0008
C3_completion_owner_decision = ACCEPTED
C3_completion_alignment_status = RECORDED_AND_ALIGNED
pre_merge_lifecycle_effect = NONE
post_merge_pre_validation_completion_effect = NOT_YET_VERIFIED_EFFECTIVE
C3_completion_effect = EFFECTIVE
C4_environment_entry_prerequisite = SATISFIED
C3_technical_work_status = COMPLETE
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
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
```

C0, C1, C2, and C3 are completed. C4 is the active major phase under the already-issued bounded Owner authorization recorded by `docs/decisions/C4_authorization_decision.md`. C5 and every later phase remain unauthorized. C3 completion remains effective and is not reopened by C4 activation.

```text
current_material_blocker = NONE
C0_status = COMPLETED
C1_status = COMPLETED
C1_completion_decision = docs/decisions/C1_completion_decision.md
C1_completion_decision_id = GOV-DEC-0004
C1_completion_owner_decision = ACCEPT_C1_COMPLETION_DECISION
C1_completion_pull_request = 8
C1_completion_owner_disposition_record = PR_8_COMMENT_5149557106
C1_completion_owner_disposition_head_commit = f8a75447ad6819efa5fbef10fe0ff36f115f8185
C1_completion_authorized_merge_method = SQUASH
C1_completion_decision_merge_commit = 7a5ed69620a773a0a0941239bc568678be41fa9a
C1_completion_pr_validation_run = 16
C1_completion_pr_validation_conclusion = SUCCESS
C1_completion_post_merge_manual_validation_run = 17
C1_completion_post_merge_manual_validation_event = WORKFLOW_DISPATCH
C1_completion_post_merge_manual_validation_commit = 7a5ed69620a773a0a0941239bc568678be41fa9a
C1_completion_post_merge_manual_validation_conclusion = SUCCESS
C1_completion_effect = EFFECTIVE
C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_decision_id = GOV-DEC-0005
C2_owner_decision = ACCEPT_GOV_DEC_0005_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_ACTIVATION_ALIGNMENT
C2_authorization_Manager_Review_classification = PASS
C2_authorization_status = AUTHORIZED
C2_package_pull_request = 11
C2_package_reviewed_head_commit = c7f5f39c54eaa40788ba3fcd4a36abc724304d3c
C2_package_merge_commit = 87b3460f0b112314ec1dd2cb1faa847fa5572b6f
C2_package_post_merge_validation_run = 24
C2_package_post_merge_validation_conclusion = SUCCESS
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_owner_decision = ACCEPT_GOV_DEC_0006_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_COMPLETION_ALIGNMENT
C2_completion_Manager_Review_classification = PASS
C2_completion_effect = EFFECTIVE
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_owner_decision = ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT
C3_owner_selection_matrix_id = C3_OWNER_SELECTION_MATRIX_V1
C3_owner_selection_matrix_status = ACCEPTED
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_technical_work_status = COMPLETE
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
```

C1, C2, and C3 completion remain effective. C4 is active only within the bounded selected-code migration, adaptation, and verification authorization recorded by `docs/decisions/C4_authorization_decision.md`. This C4 alignment does not reopen C3 or authorize C5 or any later phase.

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

C2 does not authorize:

- Editing any historical repository.
- Modifying accepted C1 artifacts.
- Executable legacy-code migration, copying, adaptation, or reimplementation.
- Creating abstract interface stubs.
- Creating provider-specific or broker-specific implementation.
- Importing or executing historical or canonical project source.
- Running project tests, notebooks, scripts, CLIs, training, validation, evaluation, or backtests.
- Selecting Python, installing dependencies, creating an environment, resolving imports, or creating a dependency lock.
- Provider or feed selection or acceptance.
- Credentials, authenticated access, network/API activity, entitlement checks, or market-data requests.
- Dataset selection, generation, reconstruction, modification, imputation, remediation, or acceptance.
- Final ticker-universe selection.
- Model implementation, training, validation, qualification, freezing, rejection, promotion, or artifact creation.
- Final-holdout access.
- Broker-account access, paper orders, live orders, paper trading, or live trading.
- Profitability, deployment-readiness, publication, or live-capital claims.
- C3 or any later-phase work.
- Automatic acceptance of any historical asset, result, model, dataset, or conclusion.

C2 workflow validation may execute only bounded workflow-contained standard-runner logic. It may not import or execute canonical or historical project source.

C3 received separate owner authorization through `GOV-DEC-0007`; C4 and every later phase require separate owner authorization. The bounded C3 technical workstream may not begin until successful validation of the exact activation-alignment squash commit.

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
dependency_installation = C3_SCOPE_ONLY_AFTER_SUCCESSFUL_EXACT_POST_MERGE_ACTIVATION_VALIDATION
environment_construction = C3_SCOPE_ONLY_AFTER_SUCCESSFUL_EXACT_POST_MERGE_ACTIVATION_VALIDATION
package_source_access = EXACT_C3_ALLOWLIST_ONLY_DURING_DEPENDENCY_ACQUISITION_AFTER_SUCCESSFUL_EXACT_POST_MERGE_ACTIVATION_VALIDATION
network_or_api_testing = NOT_AUTHORIZED
market_data_access = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
public_release = NOT_AUTHORIZED
```

## 10. Completed governance evidence and current C3 authorization

C0, C1, and C2 are completed major milestones. The accepted activation-alignment target records C3 as active. The bounded C3 technical workstream may begin only after successful validation of the exact canonical activation-alignment squash commit.

```text
C0_completion_conditions_status = SATISFIED
C0_owner_closure_acceptance = ACCEPTED
C0_completion_decision = docs/decisions/C0_completion_decision.md
C0_completion_decision_id = GOV-DEC-0002
C1_completion_conditions_status = SATISFIED
C1_owner_completion_acceptance = ACCEPTED
C1_completion_decision = docs/decisions/C1_completion_decision.md
C1_completion_decision_id = GOV-DEC-0004
C1_independent_audit_status = PASS
C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_decision_id = GOV-DEC-0005
C2_authorization_Manager_Review = PASS
C2_owner_authorization_status = ACCEPTED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_owner_completion_acceptance = ACCEPTED
C2_completion_effect = EFFECTIVE
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_owner_decision = ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT
C3_owner_selection_matrix_id = C3_OWNER_SELECTION_MATRIX_V1
C3_owner_selection_matrix_status = ACCEPTED
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_technical_work_status = COMPLETE
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
```

No prohibited technical execution was identified in the reviewed repository and GitHub evidence. That conclusion remains limited to reviewed repository and GitHub evidence; it cannot prove the absence of unrecorded external activity.

## 11. Major milestone pointers

```text
latest_completed_major_milestone = C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
active_major_milestone = C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
latest_authorization_decision = docs/decisions/C4_authorization_decision.md
latest_completion_record = docs/decisions/C3_completion_decision.md
next_permitted_workstream = BOUNDED_C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION_ONLY
```

## 12. Required reading and new-chat orientation

A fresh project chat must:

1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.

```text
latest_material_decision = docs/decisions/C4_authorization_decision.md
latest_material_completion_record = docs/decisions/C3_completion_decision.md
latest_material_independent_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
```

## 13. Maintenance guidance

```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
