# Quantitative Trading Research Platform

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-lightgrey)
[![Tests](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/racoope70/quantitative-trading-research-platform/actions/workflows/tests.yml)

## Mission

Build a canonical, reproducible, leakage-controlled quantitative research
platform for machine learning and reinforcement learning applications. The
platform supports controlled progression to paper trading and possible later
deployment under separate authorization.

## Platform milestones

The platform has achieved the following scientific and engineering milestones, 
supported by documented validation:

- **Research data contract:** The C6 model-family-neutral dataset specification
  was reviewed and frozen for future separately authorized research.
- **Experimental universe:** A 42-security primary universe was selected,
  characterized, and frozen under a predeclared protocol. The available
  formation-population limitations remain recorded.
- **Reliability engineering:** The Batch0004 workflow implements deterministic 25-record
  processing units, checkpoint and provenance controls, replay safeguards, and fail-closed execution behavior.
- **Verification and transparency:** Focused NONPRODUCTION qualification and
  accepted engineering reviews document both demonstrated controls and
  unresolved execution limitations, without treating a stopped attempt as
  scientific success.

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

- Leakage control
- Reproducibility
- Data provenance
- Realistic transaction and execution costs
- Chronological evaluation
- Fair model comparison
- Final-holdout integrity
- Clear separation between research evidence and deployment readiness

## Research progression

QTRP grew out of successive research iterations rather than a single implementation.
Early ML/RL experiments evolved into structured chronological validation, followed by 
modular PPO and execution research. These iterations reinforced the importance of rigorous 
model qualification and operational safeguards.
The current platform brings those lessons together in a reproducible,
evidence-driven research architecture.

1. **Exploration — [`exploratory-daytrading`](https://github.com/racoope70/exploratory-daytrading)**  
   Historical exploratory ML/RL research, feature engineering, model experimentation, and early evaluation work.

2. **Structured model validation — [`quant-trading-model-validation`](https://github.com/racoope70/quant-trading-model-validation)**  
   Historical PPO and PPO + Random Forest research with chronological / walk-forward validation, backtesting, signal evaluation, and preserved model artifacts.

3. **Modular PPO implementation and execution research — [`ppo-trading-pipeline`](https://github.com/racoope70/ppo-trading-pipeline)**  
   Historical modular PPO research covering implementation structure, provenance, testing, execution realism, broker integration, and stricter model-quality review.

4. **Current canonical research platform — this repository**  
   Current research platform focused on reproducibility, leakage control, data provenance, chronological evaluation, fair RL model comparison, supervised-gating research, and final-holdout integrity.

The three earlier repositories document historical research and are not runtime dependencies of the current platform. Their historical results do not establish qualification under the current evaluation standards.

## Governance and navigation

`PROJECT_CONTEXT.md` is the authoritative source for broad current lifecycle
and authorization state.

Key navigation:

- [Project Context](PROJECT_CONTEXT.md) — authoritative broad lifecycle and authorization state.
- [Milestone Review Reference Map](docs/workflows/milestone_review_reference_map.md) — non-authorizing roadmap, governance, evidence, and historical navigation.
- [Future Validation and Training Reference Map](docs/workflows/future_validation_training_reference_map.md) — non-authorizing future validation, training, evaluation, and holdout guidance.
- [Engineering Reliability Retrospective](docs/case_studies/batch0004_execution_reliability_retrospective.md) — execution integrity, failure investigation, regression verification, and engineering lessons learned.
- [Automation Reliability Engineering Reference](docs/workflows/automation_reliability_engineering_reference.md) — prospective engineering philosophy, reliability assessment, integration testing, and simplification guidance.

Files and reference maps do not independently authorize execution.

## Research status and limitations

Completed data-contract, universe, and engineering milestones establish the research foundation. 
However, these accomplishments do not yet demonstrate a qualified trading model.

Model training, final-holdout evaluation, paper trading, and deployment remain separately
governed. The latest Batch0004 U0012 attempt remains in a documented controlled
stop, with no new scientifically accepted records.

![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

> **Status: Current canonical research platform — in development**
>
> No model is currently qualified for deployment.
