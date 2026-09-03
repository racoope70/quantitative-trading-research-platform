# Quantitative Trading Research Platform — Project Context

```text
document_status = ACTIVE_CURRENT_STATE

document_role =
CONTROLLING_SOURCE_OF_TRUTH_FOR_BROAD_CURRENT_LIFECYCLE_STATE
+
AUTHORIZATION_BOUNDARIES
+
CURRENT_NON_AUTHORIZATION_STATE
+
AUTHORITATIVE_POINTERS_TO_MATERIAL_DECISIONS

current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE

working_repository_name = quantitative-trading-research-platform
repository_visibility = PUBLIC
repository_public_release = COMPLETE
project_status = IN_DEVELOPMENT

C5_completion_decision =
docs/decisions/C5_completion_decision.md

C5_completion_decision_id =
GOV-DEC-0012

C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_REOPEN = NO
C5_CURRENT_WORK = NONE

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

C6_AUTHORIZATION = NONE
C6_authorization_effect = NONE

current_authorized_workstream = NONE

dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Project

Build a canonical, reproducible, leakage-controlled quantitative research and
trading platform supporting:

- bounded PPO, SAC, and RecurrentPPO reinforcement-learning research;
- Random Forest and XGBoost participation-gate ablations;
- fair comparison under common economic, cost, and validation assumptions;
- one shared untouched final holdout under separate future authorization;
- publication-quality research; and
- controlled progression toward paper trading and possible later deployment
  only under separate authorization.

Historical repositories remain evidence and engineering sources, not runtime
dependencies or sources of current authorization.

## 2. Permanent controlling role

`PROJECT_CONTEXT.md` is the controlling source of truth for broad current
lifecycle state, authorization boundaries, current non-authorization state,
and authoritative pointers to material decisions.

It is not:

- a historical phase ledger;
- an active-milestone tracker;
- a next-task or next-permitted-workstream tracker;
- a checkpoint tracker;
- a routine phase-internal progress log; or
- a substitute for detailed decision, roadmap, validation, training, or
  evaluation records.

Git history and repository artifacts establish implementation and historical
evidence. They do not independently create current authorization.

The Milestone Review Reference Map remains a non-authorizing roadmap,
navigation, governance, and evidence reference.

The Future Validation and Training Reference Map remains non-authorizing future
guidance and sequencing reference material.

## 3. Current lifecycle and authorization state

C5 is completed and effective.

There is no active major phase, no current C5 execution authorization, and no
C6 authorization.

```text
current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE

C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_REOPEN = NO
C5_CURRENT_WORK = NONE

C6_AUTHORIZATION = NONE
C6_authorization_effect = NONE

current_authorized_workstream = NONE
CURRENT_CHECKPOINT_TRACKER = NONE
```

## 4. Authoritative material-decision pointers

C5 completion and closure are recorded in:

```text
C5_completion_decision =
docs/decisions/C5_completion_decision.md

C5_completion_decision_id =
GOV-DEC-0012
```

The accepted post-C5 / pre-C6 scientific direction is recorded in:

```text
POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY
```

GOV-DEC-0013 is the detailed scientific-design record. This document does not
duplicate its detailed candidate-routing, gating, readiness, phase-sequencing,
or future evaluation methodology.

## 5. High-level prospective research direction

The accepted prospective research direction is bounded RL research using PPO,
SAC, and RecurrentPPO, with PPO retained as the mandatory primary baseline.

Random Forest and XGBoost are future participation-gate ablations around
eligible RL foundations.

The final comparison architecture preserves one shared untouched final holdout.
Final-holdout access remains separately governed and is not currently
authorized.

No statement in this section means that a current model candidate exists or
that implementation, training, qualification, gating, backtesting, or final
evaluation is authorized.

## 6. Current dataset, model, and execution boundary

```text
dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
```

No dataset-contract freeze, provider activity, data acquisition, dataset
generation, model implementation, model training, gate training, backtesting,
final-holdout access, paper trading, or live trading is authorized by the
current state.

## 7. Navigation

Use:

- `PROJECT_CONTEXT.md` for broad current lifecycle and authorization state;
- `docs/decisions/C5_completion_decision.md` for C5 completion and closure;
- `docs/decisions/post_C5_pre_C6_RL_research_design_decision.md` for the
  accepted prospective RL/gating scientific design;
- `docs/workflows/milestone_review_reference_map.md` for non-authorizing
  roadmap, governance, evidence, and historical navigation;
- `docs/workflows/future_validation_training_reference_map.md` for
  non-authorizing future validation, training, evaluation, and holdout
  guidance; and
- Git history and the working tree for implementation evidence.

Files, plans, and reference maps do not independently authorize execution.
