# Quantitative Trading Research Platform

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-lightgrey)
[![Tests](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

> **Status: In development**
>
> No model is currently qualified for deployment. Final evaluation and trading
> stages remain separately governed. See
> [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) for authoritative lifecycle and
> authorization state.

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research
platform for machine learning and reinforcement learning applications. The
platform supports controlled progression to paper trading and possible later
deployment under separate authorization.

## Research program

The accepted prospective research direction uses a bounded RL set:

- PPO — mandatory primary baseline
- SAC — bounded alternative candidate
- RecurrentPPO — bounded recurrent candidate

Random Forest and XGBoost are future participation-gate ablations. The research
program asks whether supervised gating adds incremental value rather than
assuming that gating improves an RL policy.

The prospective comparison preserves one shared untouched final holdout.
Final-holdout access is separately governed and is not authorized during model
development, qualification, gating, or model/gate selection.

Detailed scientific methodology and routing remain in the accepted decision
records and the non-authorizing Future Validation and Training Reference Map
rather than being duplicated in this project-orientation document.

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

`PROJECT_CONTEXT.md` is the authoritative source for broad current lifecycle
and authorization state.

Key navigation:

- [Project Context](PROJECT_CONTEXT.md) — authoritative broad lifecycle and authorization state.
- [Milestone Review Reference Map](docs/workflows/milestone_review_reference_map.md) — non-authorizing roadmap, governance, evidence, and historical navigation.
- [Future Validation and Training Reference Map](docs/workflows/future_validation_training_reference_map.md) — non-authorizing future validation, training, evaluation, and holdout guidance.

Files and reference maps do not independently authorize execution.
