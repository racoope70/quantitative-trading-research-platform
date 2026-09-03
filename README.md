# Quantitative Trading Research Platform

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-lightgrey)
[![Tests](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting machine-learning research, publication-quality analysis, controlled paper trading, and potential later deployment.

## Research Program

The accepted prospective research design uses a bounded, predeclared RL set:

1. PPO — mandatory primary scientific baseline.
2. SAC — bounded alternative candidate.
3. RecurrentPPO — bounded recurrent candidate.

The common action formulation is:

```text
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE
```

Predeclaration does not force an unready or incompatible candidate through
implementation or training.

Random Forest and XGBoost are treated as alternative supervised participation-
gate ablations. Supervised gating is a testable architectural hypothesis, not
an assumed improvement.

The primary gating foundation is selected prospectively from qualified/frozen
RL policies using the fixed priority:

```text
PPO
THEN SAC
THEN RECURRENTPPO
```

Observed best development score must not be used post hoc to choose that
primary foundation.

At most one additional qualified/frozen RL policy may be used as an optional
robustness foundation.

Candidate-set expansion is not authorized.

A2C remains historical reference evidence only.

SAC and RecurrentPPO are prospective candidates; this repository does not
claim that either has been implemented, trained, or qualified.

Only eligible frozen candidates may eventually enter the separately governed
shared final evaluation. The final holdout remains untouched during candidate
development, qualification, gating, and model/gate selection and requires
separate authorization before access.

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

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

PREDECLARED_RL_CANDIDATE_SET =
PPO_SAC_RECURRENTPPO

COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

CANDIDATE_SET_EXPANSION =
NOT_AUTHORIZED

FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO

C6_and_later = UNAUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE
```

C1 through C5 are complete in the aligned target. C5 completion is
Owner-accepted and becomes effective through canonical recording plus the
required exact validation; no current C5 execution authorization remains
afterward.

The post-C5/pre-C6 RL-design alignment is Owner-accepted with refinements under
GOV-DEC-0013. It establishes prospective scientific direction only and does
not authorize C6, dataset-contract freeze, model implementation or training,
gate training, backtesting, or final-holdout access.

Operational provider access, credentials, market/reference-data acquisition,
historical-universe construction, dataset-contract freeze, dataset generation
or acceptance, C6 and later phases, model training, final-holdout access,
paper/live trading, and broker activity remain unauthorized.

The repository is public and remains in development. Public release does not
imply production readiness, dataset acceptance, model qualification, or
trading readiness.
