# Quantitative Trading Research Platform

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting machine-learning research, publication-quality analysis, controlled paper trading, and potential later deployment.

## Research Program

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

The project emphasizes leakage control, reproducibility, data provenance, realistic evaluation costs, fair model comparison, final-holdout integrity, and clear separation between research and deployment evidence.

## Historical lineage

- `racoope70/exploratory-daytrading`: broad historical research archive.
- `racoope70/quant-trading-model-validation`: historical PPO/PPO+RF validation evidence and specialized components.
- `racoope70/ppo-trading-pipeline`: historical source for modular architecture, provenance, testing, broker-safety, and deployment-engineering patterns.

No historical repository or module is automatically accepted. The canonical repository will not require historical repositories as runtime dependencies.

Historical PPO and PPO+RF systems are completed research baselines, not current deployment candidates.

## Governance and orientation

Current authorization and state are controlled by `PROJECT_CONTEXT.md`.

Project governance and roadmap references:

- [Project Context](PROJECT_CONTEXT.md) — controlling broad current lifecycle and authorization state.
- [Milestone Review Reference Map](docs/workflows/milestone_review_reference_map.md) — roadmap, big-section navigation, governance and evidence reference, and completed/future milestone navigation; non-authorizing.
- [Future Validation and Training Reference Map](docs/workflows/future_validation_training_reference_map.md) — non-authorizing future validation, training, evaluation, and holdout guidance.

For project orientation, read `PROJECT_CONTEXT.md`, the applicable Milestone Map and curated 2v records, and the applicable Future Map section, then inspect Git history and the working tree.

Files present in the repository do not independently authorize execution.

## Current repository status

```text
repository_status = PUBLIC
repository_public_release = COMPLETE
license_policy = NO_LICENSE__ALL_RIGHTS_RESERVED_BY_DEFAULT
license_file_present = NO

current_lifecycle_state = C5_ACTIVE
active_major_phase = C5_DATA_SOURCE_CALENDAR_AND_INITIAL_UNIVERSE_DECISION
proposed_next_major_phase = NONE
phase_status = ACTIVE
authorization_effect = C5_SCOPE_ONLY

C1_phase_status = COMPLETED
C1_completion_effect = EFFECTIVE

C2_phase_status = COMPLETED
C2_completion_effect = EFFECTIVE

C3_phase_status = COMPLETED
C3_completion_effect = EFFECTIVE

C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_status = ACCEPTED
C4_completion_effect = EFFECTIVE
selected_C4_subset_completion = 21_OF_21_COMPLETE
C4_technical_completion = YES
final_independent_C4_technical_closeout_audit = PASS
required_additional_C4_technical_work = NONE
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C4 = COMPLETED__EFFECTIVE

C5_owner_authorization = ACCEPTED
C5_authorization_decision = docs/decisions/C5_authorization_decision.md
C5_authorization_decision_id = GOV-DEC-0011
C5_authorization_status = AUTHORIZED
C5_activation_status = EFFECTIVE
C5_activation_precondition = SATISFIED
C5_current_execution_effect = EFFECTIVE

C6_and_later = UNAUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE
```

C1 through C4 are complete. C5 is the active lifecycle phase under the accepted bounded Data Source, Calendar, and Initial Universe Decision authorization.

Operational provider access, credentials, market-data acquisition, dataset generation or acceptance, C6 and later phases, model training, final-holdout access, paper/live trading, and broker activity remain unauthorized.

The repository is public and remains in development. Public release does not imply production readiness, dataset acceptance, model qualification, or trading readiness.
