# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C1_ACTIVE
active_major_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
proposed_next_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
phase_status = ACTIVE
authorization_effect = C1_SCOPE_ONLY
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
C1_authorization_status = AUTHORIZED
C1_phase_status = ACTIVE
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
```
C0 is completed. C1 is active only within the accepted bounded read-only and documentation-only scope. C2 remains proposed and unauthorized. No technical execution follows from C1 activation.
```text
current_material_blocker = NONE
C0_status = COMPLETED
C1_authorization_decision = docs/decisions/C1_authorization_decision.md
C1_authorization_decision_id = GOV-DEC-0003
owner_disposition_record = PR_6_COMMENT_5120803290
owner_disposition_head_commit = 18351d71fa0eedfb8ebdaa2ed9b33d051fd9829a
authorized_merge_method = SQUASH
C1_authorization_decision_merge_commit = 593f8b79246688dc9e17ee961a726f641b4d433e
C1_authorization_pr_validation_run = 12
C1_authorization_pr_validation_conclusion = SUCCESS
C1_authorization_merge_push_validation_run = 13
C1_authorization_merge_push_validation_conclusion = SUCCESS
C1_activation_status = ACTIVE
```
## 4. Active C1 authorized scope
C1 authorizes read-only inspection of:
```text
racoope70/exploratory-daytrading
racoope70/quant-trading-model-validation
racoope70/ppo-trading-pipeline
racoope70/quantitative-trading-research-platform
```
Authorized C1 work is limited to:
- Proportional review of the fifteen sections in `C1_BOUNDED_HISTORICAL_SECTION_INVENTORY`.
- Documentation-only evidence classification and architecture design.
- Preparation and revision of the three accepted C1 outputs.
- Documentation-only consistency checks.
- Owner review and correction of material C1 documentation findings.
- One risk-proportional independent C1 audit.
- C1 completion-decision preparation and owner-controlled completion governance.
The three accepted C1 outputs are:
```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```
## 5. C1 prohibited scope
C1 does not authorize:
- Editing any historical repository.
- Executable legacy-code migration or adaptation.
- Executing historical or canonical source code, tests, notebooks, or scripts.
- Training, validation, or backtest execution.
- Dependency installation or Python-environment creation.
- Provider selection or acceptance.
- Credentials, authenticated access, network/API activity, or market-data requests.
- Dataset generation, reconstruction, download, modification, imputation, or acceptance.
- Model implementation, training, retraining, validation, qualification, promotion, artifact creation, or final-holdout access.
- Broker-account access, paper orders, live orders, or trading activity.
- C2 or any later-phase work.
- Automatic acceptance of any historical asset or conclusion.
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
Historical models do not become current candidates through review or migration recommendation.
## 9. Environment and access status
```text
dependency_installation = NOT_AUTHORIZED
network_or_api_testing = NOT_AUTHORIZED
market_data_access = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED
public_release = NOT_AUTHORIZED
```
## 10. Completed C0 evidence
C0 remains the latest completed major milestone. Its accepted completion decision and independent audit remain controlling historical evidence.
```text
C0_completion_conditions_status = SATISFIED
owner_closure_acceptance = ACCEPTED
completion_decision = docs/decisions/C0_completion_decision.md
completion_decision_id = GOV-DEC-0002
completion_owner_disposition_record = PR_4_COMMENT_5117264967
completion_decision_merge_commit = c4235e466e3a8248fb0a61b342265e3a50dde76a
independent_C0_audit = docs/audits/C0_independent_governance_foundation_audit_report.md
independent_C0_audit_status = PASS
```
No prohibited technical execution was detected in the reviewed repository and GitHub evidence. That conclusion remains limited to reviewed repository and GitHub evidence; such evidence cannot independently prove the absence of unrecorded activity outside the repository.
## 11. Major milestone pointers
```text
latest_completed_major_milestone = C0_CANONICAL_GOVERNANCE_FOUNDATION_AND_LEGACY_MIGRATION_CHARTER
active_major_milestone = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
latest_authorization_decision = docs/decisions/C1_authorization_decision.md
next_permitted_workstream = C1_BOUNDED_READ_ONLY_REVIEW_AND_DOCUMENTATION_OUTPUT_PREPARATION
```
## 12. Required reading and new-chat orientation
A fresh project chat must:
1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.
```text
latest_material_decision = docs/decisions/C1_authorization_decision.md
latest_material_completion_record = docs/decisions/C0_completion_decision.md
latest_material_independent_audit = docs/audits/C0_independent_governance_foundation_audit_report.md
```
## 13. Maintenance guidance
```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
