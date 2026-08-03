# Quantitative Trading Research Platform

```text
document_status = ACTIVE_REPOSITORY_OVERVIEW
repository_status = CREATED_PRIVATE
current_lifecycle_state = C3_ACTIVE
authorization_effect = C3_SCOPE_ONLY
```

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting serious machine-learning research, publication-quality analysis, controlled paper trading, and possible later deployment consideration.

The research program will investigate:

1. Standalone PPO v2.
2. PPO plus Random Forest gating when a qualified PPO foundation exists.
3. PPO plus XGBoost gating when a qualified PPO foundation exists and C10 has an accepted terminal disposition.

The three-family research objective does not guarantee three eligible candidates.

Each applicable family may produce a qualified frozen candidate, be rejected, produce no candidate, or remain inconclusive. RF and XGBoost may be not applicable when PPO is not qualified.

Only `QUALIFIED_AND_FROZEN` candidates are eligible for the shared final holdout.

If at least one eligible candidate exists, the final holdout is opened once and applied consistently to every eligible frozen candidate under the common evaluation package.

If no eligible candidate exists, the final holdout is not accessed and the project records `NO_ELIGIBLE_CANDIDATE` before the owner decides whether to stop the cycle, publish a negative or inconclusive result, or authorize a redesign phase.

## Operating principles

The project prioritizes temporal causality, leakage prevention, train-only preprocessing, reproducibility, data and artifact provenance, honest costs, fair candidate comparison, shared final-holdout integrity, fail-closed trading controls, and separation of research, operational, and deployment evidence.

## Historical lineage

- `racoope70/exploratory-daytrading`: broad historical research archive.
- `racoope70/quant-trading-model-validation`: historical PPO/PPO+RF validation evidence and specialized components.
- `racoope70/ppo-trading-pipeline`: presumptive modular architecture, provenance, testing, broker-safety, and deployment-engineering source.

No historical repository or module is automatically accepted. The canonical repository will not require historical repositories as runtime dependencies.

Historical PPO and PPO+RF systems are completed research baselines, not current deployment candidates.

## Governance and orientation

Current authorization and state are controlled by `PROJECT_CONTEXT.md`.

A fresh project chat should read `PROJECT_CONTEXT.md`, the applicable Milestone Map and curated 2v records, the applicable Future Map section, and then inspect Git history and VS Code.

Files present in the repository do not independently authorize execution.

## Current repository status

```text
current_lifecycle_state = C3_ACTIVE
active_major_phase = C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
proposed_next_major_phase = C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
phase_status = ACTIVE
authorization_effect = C3_SCOPE_ONLY
C1_phase_status = COMPLETED
C1_completion_effect = EFFECTIVE
C2_phase_status = COMPLETED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_effect = EFFECTIVE
C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_activation_effect = EFFECTIVE_ONLY_AFTER_SUCCESSFUL_EXACT_POST_MERGE_VALIDATION
C3_technical_work_may_begin = YES_WITHIN_C3_SCOPE_ONLY_AFTER_SUCCESSFUL_EXACT_POST_MERGE_ACTIVATION_VALIDATION
C4_authorization_effect = NONE
current_model_candidate = NONE
current_deployment_candidate = NONE
```

C1 and C2 are completed. The accepted activation-alignment target records C3 as the active major phase. C4 is the proposed next major phase but remains unauthorized together with every later phase. The bounded C3 technical workstream may begin only after successful validation on the exact activation-alignment squash commit.

C3 authorizes only the bounded environment, dependency, configuration, and offline-diagnostics scope recorded in `GOV-DEC-0007` after effective activation. It does not authorize C4 application migration, provider or operational network activity, market-data or dataset activity, model implementation or validation, qualification, final-holdout access, broker activity, paper orders, live orders, or trading activity.
