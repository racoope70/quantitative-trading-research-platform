# Quantitative Trading Research Platform — Project Context
```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C0_ACTIVE
active_major_phase = C0_CANONICAL_GOVERNANCE_FOUNDATION_AND_LEGACY_MIGRATION_CHARTER
proposed_next_major_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
phase_status = ACTIVE
authorization_effect = C0_SCOPE_ONLY
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
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
This document controls only:
- Lifecycle, active phase, and phase status.
- Authorized and prohibited work.
- Current material blocker or decision.
- Dataset, model, environment, and access status.
- Latest completed phase and next permitted phase.
- Required maps and latest material records.
It does not contain detailed chronology or a completed governance chain.
Git history and VS Code verify implementation state. They do not establish current authorization.
## 3. Lifecycle and current blocker
```text
PRE_C0_DRAFT_REVIEW
→ C0_ACTIVE
→ C0_COMPLETED
```
Owner acceptance of the proposed C0 scope activates C0.
```text
current_material_blocker = NONE
current_C0_status = C0_CONTROLS_COMPLETE_INDEPENDENT_AUDIT_PENDING
independent_C0_audit_status = NOT_STARTED
authorization_effect = C0_SCOPE_ONLY
```
Repository creation and committed C0 deliverables are C0 activities, not activation preconditions.
## 4. Work authorized after C0 activation
C0 may include:
- Final repository-name review and private repository creation.
- Minimal nontechnical package and documentation structure.
- Creation, revision, and commit of the complete C0 package.
- README, contribution, and repository-protection conventions.
- Documentation-only repository-consistency CI.
- Read-only historical inspection needed to finalize the C1 method.
- One independent C0 audit and correction of material findings.
- Preparation of the C0 completion decision.
## 5. Work prohibited during C0
C0 does not authorize:
- Executable legacy-code migration or execution.
- Dependency installation or environment reconstruction.
- Provider acceptance, credentials, authenticated access, network/API testing, or market-data requests.
- Dataset generation or modification.
- Model training, validation, qualification, artifacts, or holdout access.
- Broker access or paper/live orders.
- Final ticker-universe selection.
- Profitability, promotion, deployment-readiness, or public-release claims.
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
Historical models do not become current candidates through migration.
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
## 10. C0 completion conditions
C0 closes when:
1. The private repository and complete package are committed.
2. Minimal structure and documentation-only CI are operational.
3. Protections and contribution conventions exist.
4. One independent audit passes after correction of material findings.
5. The owner accepts closure.
6. No prohibited technical execution occurred.
## 11. Major milestone pointers
```text
latest_completed_major_milestone = NONE_IN_NEW_REPOSITORY
latest_completion_record = NONE
latest_independent_audit = NONE
next_permitted_major_milestone = C0_CANONICAL_GOVERNANCE_FOUNDATION_AND_LEGACY_MIGRATION_CHARTER
```
After C0 completion, the proposed next phase is `C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN`.
## 12. Required reading and new-chat orientation
A fresh project chat must:
1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and VS Code to verify accepted implementation and completed work.
```text
latest_material_decision = docs/decisions/C0_governance_foundation_decision.md
latest_material_completion_record = NONE
latest_material_independent_audit = NONE
```
## 13. Maintenance guidance
```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
