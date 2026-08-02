# Quantitative Trading Research Platform

```text
document_status = ACTIVE_REPOSITORY_OVERVIEW
repository_status = CREATED_PRIVATE
current_lifecycle_state = C2_ACTIVE
authorization_effect = C2_SCOPE_ONLY
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
current_lifecycle_state = C2_ACTIVE
active_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
proposed_next_major_phase = C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
C1_phase_status = COMPLETED
C2_authorization_status = AUTHORIZED
C2_activation_status = ACTIVE
C3_authorization_effect = NONE
authorization_effect = C2_SCOPE_ONLY
current_model_candidate = NONE
current_deployment_candidate = NONE
```

C1 is completed. C2 is active only within the accepted non-operational repository-skeleton and migration-preparation scope in `docs/decisions/C2_authorization_decision.md`. C3 and every later phase remain unauthorized.

C2 does not authorize executable migration, environment or dependency work, provider or network activity, market-data or dataset activity, model implementation or validation, qualification, final-holdout access, broker activity, paper orders, live orders, or trading activity.
