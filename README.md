# Quantitative Trading Research Platform

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-lightgrey)
[![Tests](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting machine-learning research, publication-quality analysis, controlled paper trading, and potential later deployment.

## Research Program

The research program will investigate:

1. Standalone PPO v2.
2. PPO plus Random Forest gating when a qualified PPO foundation exists.
3. PPO plus XGBoost gating when a qualified PPO foundation exists and C10 has an accepted terminal disposition.

The three-family research objective does not guarantee three eligible candidates.

Each applicable family may produce a qualified frozen candidate, be rejected, produce no candidate, or remain inconclusive. RF and XGBoost are only evaluated if PPO qualifies.

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

current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
proposed_next_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE

C1_phase_status = COMPLETED
C1_completion_effect = EFFECTIVE

C2_phase_status = COMPLETED
C2_completion_effect = EFFECTIVE

C3_phase_status = COMPLETED
C3_completion_effect = EFFECTIVE

C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_status = ACCEPTED
C4_completion_effect = EFFECTIVE
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C4 = COMPLETED__EFFECTIVE

C5_owner_authorization = ACCEPTED
C5_authorization_decision = docs/decisions/C5_authorization_decision.md
C5_authorization_decision_id = GOV-DEC-0011
C5_authorization_status = AUTHORIZED

C5_completion_decision = docs/decisions/C5_completion_decision.md
C5_completion_decision_id = GOV-DEC-0012
C5_completion_status = ACCEPTED
C5_completion_effect = EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
REQUIRED_BEFORE_C6_DATASET_CONTRACT_FREEZE

C6_and_later = UNAUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE
```

C1 through C5 are complete in the aligned target. C5 completion is
Owner-accepted and becomes effective through canonical recording plus the
required exact validation; no current C5 execution authorization remains
afterward.

A separate post-C5/pre-C6 RL-design alignment is required before any C6
dataset-contract freeze. That requirement is not C6 authorization and does not
authorize model development or training.

Operational provider access, credentials, market/reference-data acquisition,
historical-universe construction, dataset-contract freeze, dataset generation
or acceptance, C6 and later phases, model training, final-holdout access,
paper/live trading, and broker activity remain unauthorized.

The repository is public and remains in development. Public release does not
imply production readiness, dataset acceptance, model qualification, or
trading readiness.
