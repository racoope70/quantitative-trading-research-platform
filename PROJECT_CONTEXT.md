# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C2_ACTIVE
active_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
proposed_next_major_phase = C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
phase_status = ACTIVE
authorization_effect = C2_SCOPE_ONLY
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
C1_phase_status = COMPLETED
C2_authorization_status = AUTHORIZED
C2_activation_status = ACTIVE
C3_authorization_effect = NONE
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
```

C0 and C1 are completed. C2 is active only within the accepted non-operational repository-skeleton and migration-preparation scope. C3 and every later phase remain unauthorized.

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
C2_Manager_Review_classification = PASS
C2_authorization_status = AUTHORIZED
C2_activation_status = ACTIVE
C2_authorization_effect = EFFECTIVE
C3_authorization_effect = NONE
```

C1 completion remains effective. C2 authorization becomes effective only through the controlling-state alignment merge that records the accepted decision and this aligned state on canonical `main`. A branch, commit, push, pull request, or pull-request validation alone does not activate C2.

## 4. Active C2 scope and preserved C1 evidence

C2 is active only for the accepted non-operational repository-skeleton and migration-preparation scope.

Authorized C2 work is limited to:

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

C3 and every later phase require separate owner authorization.

## 6. Current material decisions

```text
proposed_repository_visibility = PRIVATE
presumptive_architecture_source = racoope70/ppo-trading-pipeline
canonical_package_name = quantitative_trading_research
automatic_module_acceptance = NO
accepted_C1_artifacts = IMMUTABLE
abstract_interface_stubs_during_C2 = NOT_AUTHORIZED
provider_or_broker_specific_implementation_during_C2 = NOT_AUTHORIZED
supported_python_version = TO_BE_SELECTED_DURING_C3
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
dependency_installation = NOT_AUTHORIZED
network_or_api_testing = NOT_AUTHORIZED
market_data_access = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
public_release = NOT_AUTHORIZED
```

## 10. Completed governance evidence and active authorization

C0 and C1 are completed major milestones. C2 is the active authorized phase.

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
C2_authorization_effect = EFFECTIVE
C3_authorization_effect = NONE
```

No prohibited technical execution was identified in the reviewed repository and GitHub evidence. That conclusion remains limited to reviewed repository and GitHub evidence; it cannot prove the absence of unrecorded external activity.

## 11. Major milestone pointers

```text
latest_completed_major_milestone = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
active_major_milestone = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
latest_authorization_decision = docs/decisions/C2_authorization_decision.md
latest_completion_record = docs/decisions/C1_completion_decision.md
next_permitted_workstream = C2_AUTHORIZED_NON_OPERATIONAL_SKELETON_AND_MIGRATION_PREPARATION_ONLY
```

## 12. Required reading and new-chat orientation

A fresh project chat must:

1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.

```text
latest_material_decision = docs/decisions/C2_authorization_decision.md
latest_material_completion_record = docs/decisions/C1_completion_decision.md
latest_material_independent_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
```

## 13. Maintenance guidance

```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
