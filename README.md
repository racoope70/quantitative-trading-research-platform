# Quantitative Trading Research Platform

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-lightgrey)
[![Tests](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research and
trading platform for machine-learning and reinforcement-learning research,
publication-quality analysis, controlled paper-trading progression, and
possible later deployment under separate authorization.

```text
document_role =
PROJECT_ORIENTATION
+
HIGH_LEVEL_PUBLIC_STATUS
+
NAVIGATION_ENTRY_POINT
```

## Research program

The accepted prospective research direction uses a bounded RL set:

- PPO — mandatory primary baseline;
- SAC — bounded alternative candidate; and
- RecurrentPPO — bounded recurrent candidate.

Random Forest and XGBoost are future participation-gate ablations. The research
program asks whether supervised gating adds incremental value rather than
assuming that gating improves an RL policy.

The prospective comparison preserves one shared untouched final holdout.
Final-holdout access is separately governed and is not authorized during model
development, qualification, gating, or model/gate selection.

Detailed scientific methodology and routing are recorded in GOV-DEC-0013 and
the non-authorizing Future Validation and Training Reference Map rather than
duplicated here.

## Operating principles

The project emphasizes leakage control, reproducibility, data provenance,
realistic transaction and execution costs, chronological evaluation, fair model
comparison, final-holdout integrity, and separation between research evidence
and deployment readiness.

## Historical lineage

- `racoope70/exploratory-daytrading` — broad historical exploratory ML/RL
  research.
- `racoope70/quant-trading-model-validation` — historical structured PPO and
  PPO+RF validation research.
- `racoope70/ppo-trading-pipeline` — historical source for modular
  architecture, provenance, testing, broker-safety, and
  deployment-engineering patterns.

Historical repositories are evidence and engineering lineage. They are not
runtime dependencies or sources of current authorization.

## Governance and navigation

`PROJECT_CONTEXT.md` controls broad current lifecycle state and authorization
boundaries.

Key navigation:

- [Project Context](PROJECT_CONTEXT.md) — broad current lifecycle,
  authorization, and non-authorization state.
- [GOV-DEC-0013](docs/decisions/post_C5_pre_C6_RL_research_design_decision.md)
  — accepted post-C5/pre-C6 RL research-design decision.
- [Milestone Review Reference Map](docs/workflows/milestone_review_reference_map.md)
  — non-authorizing roadmap, governance, evidence, and historical navigation.
- [Future Validation and Training Reference Map](docs/workflows/future_validation_training_reference_map.md)
  — non-authorizing future validation, training, evaluation, and holdout
  guidance.

Files and reference maps do not independently authorize execution.

## Current repository status

```text
repository_status = PUBLIC
repository_public_release = COMPLETE
project_status = IN_DEVELOPMENT

current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE

C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

C6_and_later = UNAUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

CURRENT_CHECKPOINT_TRACKER = NONE
```

C5 is completed and effective. No current C5 execution authorization remains.

GOV-DEC-0013 records prospective scientific direction only; it does not
authorize C6, dataset-contract freeze, model implementation or training, gate
training, backtesting, final-holdout access, paper trading, or live trading.

The repository is public and remains in development. Public availability does
not imply dataset acceptance, model qualification, production readiness, or
trading readiness.
