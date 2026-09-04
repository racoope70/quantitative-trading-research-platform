# Future Validation and Training Reference Map

```text
document_status = ESTABLISHED_NON_AUTHORIZING_REFERENCE
document_role = NON_AUTHORIZING_FUTURE_GUIDANCE_AND_SEQUENCING_REFERENCE
authorization_effect = NONE
current_state_control = NO
```

## 1. Purpose

This document contains permanent methodological guidance and high-level planned tasks.

It does not contain current authorization, current blockers, phase status, completed-chain history, or claims that future work is active.

Detailed phase checklists should be created only when the applicable phase becomes active.

## 2. Permanent scientific principles

All future research must preserve:

- Temporal causality.
- Train-only fitting.
- Leakage-controlled chronological evaluation.
- Explicit embargo where required.
- Predeclared qualification, rejection, and promotion criteria.
- Honest transaction-cost and slippage assumptions.
- Complete data and artifact provenance.
- Retention of adverse and inconclusive results.
- Separation of software correctness, statistical performance, economic performance, broker reliability, and deployment readiness.

## 3. Architecture, environment, and migration

Required sequence:

```text
canonical skeleton and migration preparation
→ Python environment and dependency reconstruction
→ selected code migration, adaptation, and verification
```

Migration must preserve immutable source attribution, one canonical responsibility per component, known limitations, required tests, and no runtime dependency on historical repositories.

C4 may include provider-neutral interfaces, mocks, offline fixtures, normalization utilities, and provisional provider components.

C4 does not establish provider acceptance or authorize credentials, authenticated access, network/API testing, market-data requests, entitlement conclusions, or production-source validation.

## 4. Data and universe guidance

Future data phases must define:

- Provider, feed, licensing, and permitted use.
- Calendar, session, timestamp, and corporate-action rules.
- Schema, dtypes, missing-slot policy, exclusions, and imputation policy.
- Symbols, date ranges, provenance, checksums, and immutable dataset identity.

Universe selection should consider liquidity, spreads, expected costs,
coverage, corporate actions, sector and regime diversity, provider
availability, compute requirements, survivorship bias, and selection bias.

Recommended progression:

```text
single-ticker engineering verification
→ small diagnostic subset
→ accepted final comparison universe
```

### Future C6 model-family-neutral compatibility envelope

GOV-DEC-0013 establishes prospective scientific direction only.

Current C6 authorization and lifecycle status are controlled by
`PROJECT_CONTEXT.md`; this reference map grants no authorization.

Any C6 dataset contract must remain model-family neutral
while supporting:

```text
COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

PPO_COMPATIBILITY =
REQUIRED

SAC_COMPATIBILITY =
REQUIRED

RECURRENTPPO_COMPATIBILITY =
REQUIRED

C6_DATASET_CONTRACT =
NOT_FROZEN
```

The future contract must be capable of preserving:

- chronological sequence construction;
- recurrent lookback and warm-up requirements;
- recurrent episode and session boundaries;
- common economic, cost, and execution inputs;
- deterministic chronological folds;
- gate-feature and outcome alignment;
- leakage-safe gate-target construction;
- provenance;
- stable row, security, and time identity; and
- untouched final-holdout isolation.

This guidance does not authorize provider activity, data acquisition, dataset
generation, dataset acceptance, or dataset-contract freeze.

## 5. Validation and leakage guidance

Future validation must define training, validation, development-test or qualification data, embargo, refit rules, benchmarks, costs, and terminal disposition criteria.

Controls must prevent full-series fitting, centered rolling windows, future-aware joins, label leakage, random time-series splitting, holdout-driven changes, invalid preprocessor reuse, and future-aware missing-data treatment.

## 6. Bounded RL candidate readiness, training, qualification, and freeze

The accepted prospective scientific direction is:

```text
POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

PREDECLARED_RL_CANDIDATES =
PPO
SAC
RECURRENTPPO

PPO =
MANDATORY_PRIMARY_BASELINE

A2C =
HISTORICAL_REFERENCE_ONLY

OTHER_RL_MODELS =
OUT_OF_SCOPE

CANDIDATE_SET_EXPANSION =
NOT_AUTHORIZED

FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO

COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

C8 =
BOUNDED_RL_CANDIDATE_IMPLEMENTATION_READINESS

C9 =
BOUNDED_RL_TRAINING_VALIDATION_COMPARISON_QUALIFICATION_AND_FREEZE
```

PPO, SAC, and RecurrentPPO are predeclared candidate families.

Predeclaration does not require every family to be implemented or trained.

Candidate-specific readiness and compatibility conditions must be satisfied
before a family proceeds under separate future authorization.

Permitted future terminal outcomes include, as applicable:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
NOT_APPLICABLE_WHERE_PREDECLARED_CONDITIONS_FAIL
```

No fourth RL family may be substituted merely because a predeclared candidate
fails readiness, compatibility, qualification, or applicability requirements.

The shared final holdout remains distinct from all C8/C9 readiness,
development, comparison, qualification, and freeze activity.

## 7. RF and XGBoost participation-gate ablations

Supervised participation gating is an architectural hypothesis to be tested
against qualified ungated RL controls.

```text
SUPERVISED_GATING =
TESTABLE_ARCHITECTURAL_HYPOTHESIS

RF_XGB_ROLE =
ALTERNATIVE_PARTICIPATION_GATE_ABLATIONS

C10 =
RF_PARTICIPATION_GATE_ABLATION

C11 =
XGBOOST_PARTICIPATION_GATE_ABLATION

QUALIFICATION_ROUTING =
OPTION_B_PLUS

PRIMARY_GATING_FOUNDATION_COUNT =
1

OPTIONAL_ROBUSTNESS_GATING_FOUNDATION_COUNT =
AT_MOST_1

PRIMARY_FOUNDATION_PRIORITY =
PPO
THEN_SAC
THEN_RECURRENTPPO

POST_HOC_BEST_SCORE_ROUTING =
NOT_AUTHORIZED
```

The primary gating foundation must be selected from qualified and frozen RL
policies using the fixed priority rather than observed best development score.

At most one additional qualified and frozen RL policy may be used for
robustness.

If used, it must be selected from the remaining eligible candidates using the
same fixed priority.

No candidate is forced through implementation, training, qualification, or
freeze merely to populate either gating foundation.

Each RF or XGBoost gate experiment must preserve a paired ungated control under
the same comparable evaluation framework.

Gate features, gate targets, thresholds, and outcomes must remain
chronologically aligned and leakage controlled.

Feature importance and SHAP analysis must not be presented as causal evidence.

## 8. Eligible candidates and one shared untouched final holdout

Prospective C12 interpretation:

```text
C12 =
ELIGIBLE_CANDIDATE_FREEZE
+
ONE_SHARED_UNTOUCHED_FINAL_HOLDOUT
+
FINAL_DISPOSITION
```

Only eligible `QUALIFIED_AND_FROZEN` candidates may enter the final-holdout
path.

The final-holdout path requires:

```text
all_applicable_candidate_and_gate_phases_have_accepted_terminal_dispositions = YES
all_eligible_candidates_are_frozen = YES
at_least_one_eligible_candidate_exists = YES
common_evaluation_package_is_frozen = YES
final_holdout_access_is_expressly_authorized = YES
```

The final holdout must be opened once and applied consistently under one common
frozen evaluation package.

It must not be used for:

- RL model selection;
- reward redesign;
- candidate replacement;
- feature selection;
- gate-target redesign;
- gate-threshold selection;
- Option B+ foundation routing; or
- iterative debugging.

Rejected, no-candidate, inconclusive, and not-applicable outcomes remain
visible in the final research report.

When no eligible candidate exists:

```text
C12_terminal_disposition =
NO_ELIGIBLE_CANDIDATE

final_holdout_accessed =
NO
```

The Owner must separately decide whether to stop the research cycle, publish a
negative or inconclusive result, or authorize a redesign.

A viewed holdout cannot become untouched again.

## 9. Publication, paper trading, and deployment

Publication must accurately present methods, costs, uncertainty, limitations, rejected, no-candidate, inconclusive, and not-applicable outcomes, and reproducibility evidence.

Paper trading requires paper-only credentials and endpoints, live-endpoint rejection, no-submit defaults, explicit order enablement, position and loss limits, stale-data and duplicate-order controls, reconciliation, kill switch, flattening procedures, and complete logs.

Operational reliability and economic performance must be reported separately.

Paper trading does not authorize live deployment. Live-capital consideration requires a separate risk framework, owner authorization, and independent audit.

## 10. Monitoring, retirement, and retraining

Monitoring should cover data availability and drift, prediction behavior, costs, turnover, exposure, drawdown, broker failures, and artifact/configuration mismatches.

Retirement criteria must be defined before operational use.

Retraining must use a new accepted data cutoff and cycle identity, updated provenance, preserved interpretation of viewed holdouts, new future evaluation data where possible, incumbent comparison, and independent replacement review.

A viewed holdout cannot become untouched again.
