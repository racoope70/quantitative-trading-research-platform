# C6 Dataset Contract Freeze Authorization Decision

```text
document_status = ACCEPTED_C6_AUTHORIZATION_DECISION
document_role = SUPPORTING_MATERIAL_AUTHORIZATION_EVIDENCE
authorization_effect = SUPPORTS_CONTROLLING_PROJECT_CONTEXT_STATE
intended_repository_path = docs/decisions/C6_authorization_decision.md

decision_id = GOV-DEC-0014
decision_type = C6_PHASE_AUTHORIZATION_CANONICAL_RECORDING
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED

OWNER_DECISION_ALREADY_MADE = YES
NEW_SUBSTANTIVE_AUTHORIZATION_CREATED_BY_THIS_RECORD = NO

authorized_phase = C6_DATASET_CONTRACT_FREEZE
C6_AUTHORIZATION = AUTHORIZED__SPECIFICATION_AND_CONTRACT_FREEZE_ONLY
C6_authorization_scope = C6_SCOPE_ONLY

C5_completion_effect = EFFECTIVE
C5_REOPEN = NO
POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT = ACCEPTED

PREDECLARED_RL_CANDIDATES =
PPO
+
SAC
+
RECURRENTPPO

PPO = MANDATORY_PRIMARY_BASELINE
COMMON_ACTION_FORMULATION = CONTINUOUS_TARGET_POSITION_OR_EXPOSURE
SUPERVISED_GATING = TESTABLE_ARCHITECTURAL_HYPOTHESIS
RL_CANDIDATE_EXPANSION = NOT_AUTHORIZED

C6_EXECUTION_BOUNDARY =
NO_DATA_GENERATION
+
NO_MODEL_TRAINING
+
NO_FINAL_HOLDOUT_ACCESS

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Purpose

This record canonically records an Owner C6 authorization that has already
been made and accepted.

It does not create, expand, reinterpret, or re-decide the Owner authorization.

The authorized C6 scope is limited to dataset-contract specification,
independent review, and final contract freeze.

It does not authorize dataset generation, model implementation or training,
final-holdout access, trading, deployment, or any C7-or-later execution.

## 2. Owner-authorized C6 scope

The bounded C6 specification, review, and contract-freeze scope covers:

1. Raw data contract.

2. Processed data contract.

3. Chronology and leakage controls.

4. Common PPO/SAC/RecurrentPPO observation and state contract.

5. Recurrent sequence, lookback, warm-up, and session requirements.

6. Continuous target-position/exposure and economic representation.

7. Development, validation, and final-holdout partition contract.

8. RF/XGBoost gating alignment and leakage-safe targets.

9. Provenance and provider-neutral contract.

10. Dataset acceptance rules.

11. Independent C6 review requirements.

12. Final C6 contract freeze.

The scope is specification and governance work only. Dataset acceptance rules
may be defined, but dataset-acceptance execution is not authorized.

## 3. Explicit exclusions

```text
data_purchase = NOT_AUTHORIZED
provider_purchase = NOT_AUTHORIZED
provider_account_activity = NOT_AUTHORIZED
data_download = NOT_AUTHORIZED
network_or_API_data_acquisition = NOT_AUTHORIZED
dataset_generation = NOT_AUTHORIZED
dataset_acceptance_execution = NOT_AUTHORIZED
RL_model_implementation = NOT_AUTHORIZED
PPO_training = NOT_AUTHORIZED
SAC_training = NOT_AUTHORIZED
RecurrentPPO_training = NOT_AUTHORIZED
RF_training = NOT_AUTHORIZED
XGBoost_training = NOT_AUTHORIZED
backtest_execution = NOT_AUTHORIZED
model_qualification = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED
candidate_set_expansion = NOT_AUTHORIZED
host_or_compute_authorization = NOT_AUTHORIZED
C7_or_later_execution = NOT_AUTHORIZED
```

No provider purchase, account activity, authenticated acquisition, download,
dataset generation, model execution, qualification, holdout access, trading,
or deployment is authorized by this C6 decision.

## 4. Governance role

This decision record is supporting material authorization evidence.

`PROJECT_CONTEXT.md` remains the controlling source of truth for broad current
lifecycle state and authorization boundaries.

The Milestone Review Reference Map and Future Validation and Training Reference
Map remain non-authorizing reference documents.

This record is not a checkpoint tracker and does not create another approval
layer.

```text
CURRENT_CHECKPOINT_TRACKER = NONE
```
