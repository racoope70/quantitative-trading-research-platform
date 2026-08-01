# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C1_COMPLETED
active_major_phase = NONE
proposed_next_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
phase_status = C1_COMPLETED_AWAITING_C2_AUTHORIZATION
authorization_effect = NONE
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
C1_phase_status = COMPLETED
C2_authorization_status = NOT_AUTHORIZED
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
```

C0 and C1 are completed. No major phase is active. C2 is the proposed next phase, remains unauthorized, and may begin only through a separate future owner authorization decision.

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
C2_authorization_status = NOT_AUTHORIZED
```

C1 completion becomes effective only through the accepted controlling-state alignment merge that introduces this completed-state package to canonical `main`. The earlier C1 completion-decision merge alone did not make C1 completion effective.

## 4. Completed C1 scope and evidence

C1 completed the accepted bounded read-only and documentation-only scope covering the fifteen sections in `C1_BOUNDED_HISTORICAL_SECTION_INVENTORY`.

The three accepted C1 outputs are:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

The accepted completion evidence includes:

```text
independent_C1_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
independent_C1_audit_classification = PASS
bounded_section_coverage = 15_OF_15_CONFIRMED
completion_decision = docs/decisions/C1_completion_decision.md
completion_decision_id = GOV-DEC-0004
completion_decision_owner_status = ACCEPTED
```

Historical repositories remain evidence and engineering sources. The completed review did not migrate executable code, select a provider or dataset, create a current model candidate, or authorize later-phase work.

## 5. Continuing non-authorization

C1 completion does not authorize:

- Editing any historical repository.
- Executable legacy-code migration or adaptation.
- Executing historical or canonical source code, tests, notebooks, or scripts.
- Training, validation, backtest execution, qualification, promotion, or artifact creation.
- Dependency installation or Python-environment creation.
- Provider selection or acceptance.
- Credentials, authenticated access, network/API activity, entitlement checks, or market-data requests.
- Dataset generation, reconstruction, download, modification, imputation, or acceptance.
- Final ticker-universe selection.
- Model implementation, training, retraining, validation, or final-holdout access.
- Broker-account access, paper orders, live orders, or trading activity.
- Profitability, deployment-readiness, publication, paper-trading, or live-capital claims.
- C2 or any later-phase technical work.
- Automatic acceptance of any historical asset or conclusion.

Only a separate future owner authorization decision may authorize C2. No technical work is presently authorized.

## 6. Current material decisions

```text
proposed_repository_visibility = PRIVATE
presumptive_architecture_source = racoope70/ppo-trading-pipeline
automatic_module_acceptance = NO
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

## 10. Completed governance evidence

C0 and C1 are completed major milestones.

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
```

No prohibited technical execution was identified in the reviewed repository and GitHub evidence. That conclusion remains limited to reviewed repository and GitHub evidence; such evidence cannot independently prove the absence of unrecorded activity outside the repository.

## 11. Major milestone pointers

```text
latest_completed_major_milestone = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
active_major_milestone = NONE
latest_authorization_decision = docs/decisions/C1_authorization_decision.md
latest_completion_record = docs/decisions/C1_completion_decision.md
next_permitted_workstream = C2_AUTHORIZATION_DECISION_ONLY
```

## 12. Required reading and new-chat orientation

A fresh project chat must:

1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.

```text
latest_material_decision = docs/decisions/C1_completion_decision.md
latest_material_completion_record = docs/decisions/C1_completion_decision.md
latest_material_independent_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
```

## 13. Maintenance guidance

```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
