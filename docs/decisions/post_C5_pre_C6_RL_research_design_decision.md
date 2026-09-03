# Post-C5 / Pre-C6 RL Research Design Decision

```text
document_status =
ACCEPTED_POST_C5_PRE_C6_RL_RESEARCH_DESIGN_DECISION

document_role =
SUBSTANTIVE_OWNER_SCIENTIFIC_DESIGN_DECISION

current_state_control =
NO

decision_id =
GOV-DEC-0013

decision_type =
POST_C5_PRE_C6_RL_RESEARCH_DESIGN_ALIGNMENT

decision_status =
ACCEPTED_WITH_REFINEMENTS

owner_decision =
ACCEPT_POST_C5_PRE_C6_RL_RESEARCH_DESIGN_ALIGNMENT_WITH_REFINEMENTS

authorization_effect =
SCIENTIFIC_DIRECTION_ONLY__NO_EXECUTION_AUTHORITY

OWNER_REDECISION_REQUIRED =
NO

C5_STATUS =
COMPLETED__COMPLETE_EFFECTIVE

CURRENT_C5_EXECUTION_AUTHORIZATION =
NONE_AFTER_COMPLETION

C5_REOPEN =
NO

C5_CURRENT_WORK =
NONE

PRIMARY_RESEARCH_QUESTION =
ARCHITECTURE_LEVEL_SUPERVISED_GATING_INCREMENTAL_VALUE

PREDECLARED_RL_CANDIDATE_SET =
PPO
+
SAC
+
RECURRENTPPO

CANDIDATE_SET_EXPANSION =
NOT_AUTHORIZED

FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO

PPO =
MANDATORY_PRIMARY_BASELINE

A2C =
HISTORICAL_REFERENCE_ONLY

OTHER_RL_MODELS =
OUT_OF_SCOPE_ABSENT_SEPARATE_OWNER_AUTHORIZED_REDESIGN

COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

SUPERVISED_GATING =
TESTABLE_ARCHITECTURAL_HYPOTHESIS

RF_XGB_ROLE =
ALTERNATIVE_PARTICIPATION_GATE_ABLATIONS

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

PERMITTED_FUTURE_TERMINAL_OUTCOMES =
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
NOT_APPLICABLE_WHERE_PREDECLARED_CONDITIONS_FAIL

C8 =
BOUNDED_RL_CANDIDATE_IMPLEMENTATION_READINESS

C9 =
BOUNDED_RL_TRAINING_VALIDATION_COMPARISON_QUALIFICATION_AND_FREEZE

C10 =
RF_PARTICIPATION_GATE_ABLATION

C11 =
XGBOOST_PARTICIPATION_GATE_ABLATION

C12 =
ELIGIBLE_CANDIDATE_FREEZE
+
ONE_SHARED_UNTOUCHED_FINAL_HOLDOUT
+
FINAL_DISPOSITION

C6_DATASET_CONTRACT =
NOT_FROZEN

C6_AUTHORIZATION =
NONE

dataset_contract_freeze =
NOT_AUTHORIZED

dataset_activity =
NONE

model_activity =
NONE

model_training =
NOT_AUTHORIZED

gate_training =
NOT_AUTHORIZED

backtesting =
NOT_AUTHORIZED

final_holdout_access =
NONE

paper_trading =
NOT_AUTHORIZED

live_trading =
NOT_AUTHORIZED

dependency_files_change_required_now =
NO

CURRENT_CHECKPOINT_TRACKER =
NONE
```

## 1. Purpose

This decision records the Owner-accepted post-C5 / pre-C6 RL research-design
alignment.

It is a substantive scientific-direction decision made after effective C5
closure and before any future C6 authorization.

This decision does not reopen C5, create current C5 work, activate C6, freeze a
dataset contract, or authorize data, model, gating, backtesting, final-holdout,
paper-trading, or live-trading activity.

`PROJECT_CONTEXT.md` remains the controlling source for broad current lifecycle
state and authorization boundaries.

## 2. Primary research question

The prospective primary research question is architecture-level:

```text
PRIMARY_RESEARCH_QUESTION =
ARCHITECTURE_LEVEL_SUPERVISED_GATING_INCREMENTAL_VALUE
```

The program will test whether supervised participation gating provides
incremental value over qualified ungated RL policies.

RF/XGBoost gating is therefore a testable architectural hypothesis, not an
assumed improvement.

## 3. Bounded RL candidate set

The predeclared RL candidate set is:

```text
PPO
SAC
RECURRENTPPO
```

PPO is the mandatory primary scientific baseline.

A2C remains historical reference evidence only.

Other RL models remain out of scope absent a separately Owner-authorized
research redesign.

Candidate-set expansion is not authorized.

Predeclaration does not require every candidate to proceed through
implementation or training.

```text
FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO
```

A candidate may stop at the applicable future readiness or compatibility gate.

Permitted future terminal outcomes include, as appropriate:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
NOT_APPLICABLE_WHERE_PREDECLARED_CONDITIONS_FAIL
```

No fourth candidate may be substituted merely because a predeclared candidate
is unsuitable, unready, rejected, or not applicable.

## 4. Common action formulation

The common action formulation for the bounded RL comparison is:

```text
COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE
```

This common formulation is prospective scientific direction only.

It does not imply that PPO, SAC, or RecurrentPPO is presently implemented,
trained, qualified, or authorized for execution.

## 5. Option B+ supervised-gating routing

RF and XGBoost are alternative supervised participation-gate ablations.

The primary gating foundation is exactly one qualified and frozen RL policy
selected using the predeclared priority:

```text
PPO
THEN_SAC
THEN_RECURRENTPPO
```

The primary foundation must not be selected post hoc by observed best
development score.

```text
POST_HOC_BEST_SCORE_ROUTING =
NOT_AUTHORIZED
```

At most one additional qualified and frozen RL policy may be used as an
optional robustness gating foundation.

If used, that additional foundation is selected from the remaining eligible
candidates using the same predeclared priority.

No candidate is forced through implementation, training, qualification, or
freeze merely to populate either gating foundation.

Each gated experiment must preserve a paired ungated control so incremental
gating value can be evaluated.

## 6. Prospective phase interpretation

The accepted prospective interpretation is:

```text
C8 =
BOUNDED_RL_CANDIDATE_IMPLEMENTATION_READINESS

C9 =
BOUNDED_RL_TRAINING_VALIDATION_COMPARISON_QUALIFICATION_AND_FREEZE

C10 =
RF_PARTICIPATION_GATE_ABLATION

C11 =
XGBOOST_PARTICIPATION_GATE_ABLATION

C12 =
ELIGIBLE_CANDIDATE_FREEZE
+
ONE_SHARED_UNTOUCHED_FINAL_HOLDOUT
+
FINAL_DISPOSITION
```

C8 and C9 must preserve candidate-specific readiness and compatibility gates.

Failure of a predeclared condition may produce:

```text
NOT_APPLICABLE_WHERE_PREDECLARED_CONDITIONS_FAIL
```

without forcing implementation or training.

## 7. Future C6 dataset-compatibility envelope

Future C6, if separately authorized, must remain model-family neutral while
supporting:

- PPO compatibility;
- SAC compatibility;
- RecurrentPPO compatibility;
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

```text
C6_DATASET_CONTRACT =
NOT_FROZEN

C6_AUTHORIZATION =
NONE
```

This decision does not freeze or authorize the C6 dataset contract.

## 8. Shared untouched final holdout

RL development, qualification, gating, and candidate selection must occur
before final-holdout access.

Only eligible frozen candidates may reach the separately governed final
evaluation.

The shared final holdout must remain untouched during:

- candidate readiness and training;
- reward or configuration decisions;
- candidate qualification;
- gate-feature development;
- gate-target construction;
- threshold selection;
- Option B+ routing; and
- model or gate selection.

When separately authorized, the final holdout is opened once and evaluated
under one common frozen evaluation package.

Repeated final-holdout querying for model or gate selection is not permitted.

## 9. Historical continuity

Accepted historical decisions remain unchanged.

Earlier PPO-specific future planning remains valid historical evidence of what
was accepted at that time.

GOV-DEC-0013 prospectively supersedes that future scientific direction without
rewriting C5 or any earlier historical decision, audit, report, migration
record, or implementation evidence.

## 10. Non-authorization

```text
C5_REOPEN =
NO

C5_CURRENT_WORK =
NONE

C6_AUTHORIZATION =
NONE

C6_DATASET_CONTRACT =
NOT_FROZEN

dataset_contract_freeze =
NOT_AUTHORIZED

dataset_activity =
NONE

model_activity =
NONE

model_training =
NOT_AUTHORIZED

gate_training =
NOT_AUTHORIZED

backtesting =
NOT_AUTHORIZED

final_holdout_access =
NONE

paper_trading =
NOT_AUTHORIZED

live_trading =
NOT_AUTHORIZED

dependency_files_change_required_now =
NO

CURRENT_CHECKPOINT_TRACKER =
NONE
```

No dependency change, `sb3-contrib` addition, model implementation, gate
implementation, provider activity, data acquisition, dataset generation,
training, backtesting, final-holdout access, or trading activity is authorized
by this decision.
