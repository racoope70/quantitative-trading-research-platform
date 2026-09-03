# Quantitative Trading Research Platform — Project Context

```text
document_status = ACTIVE_CURRENT_STATE
current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
proposed_next_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE
working_repository_name = quantitative-trading-research-platform
repository_creation_status = CREATED_PRIVATE
repository_visibility = PUBLIC
repository_public_release = COMPLETE
PUBLIC_RELEASE_HYGIENE_CHECK_PENDING = NO
PUBLIC_RELEASE_HYGIENE_CHECK_RESULT = PASS
public_release_action = COMPLETE
repository_visibility_changed = YES
license_policy = NO_LICENSE__ALL_RIGHTS_RESERVED_BY_DEFAULT
license_file_present = NO

C1_phase_status = COMPLETED
C1_completion_effect = EFFECTIVE

C2_phase_status = COMPLETED
C2_authorization_status = AUTHORIZED
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_effect = EFFECTIVE

C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE
C3_completion_decision = docs/decisions/C3_completion_decision.md
C3_completion_decision_id = GOV-DEC-0008
C3_completion_owner_decision = ACCEPTED
C3_completion_effect = EFFECTIVE
C3_technical_work_status = COMPLETE

C4_environment_entry_prerequisite = SATISFIED
C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
selected_C4_surface = OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_status = ACCEPTED
selected_C4_subset_completion = 21_OF_21_COMPLETE
C4_technical_completion = YES
final_independent_C4_technical_closeout_audit = PASS
required_additional_C4_technical_work = NONE
C4_technical_work_status = COMPLETE
C4_completion_effect = EFFECTIVE
C4_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
HISTORICAL_C4_AUTHORIZATION = PRESERVED
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_entry_prerequisite = SATISFIED
C5_authorization_decision = docs/decisions/C5_authorization_decision.md
C5_authorization_decision_id = GOV-DEC-0011
C5_authorization_status = AUTHORIZED
C5_owner_decision_status = ACCEPTED
C5_completion_decision = docs/decisions/C5_completion_decision.md
C5_completion_decision_id = GOV-DEC-0012
C5_completion_status = ACCEPTED
C5_scientific_decision_work = COMPLETE
C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
HISTORICAL_C5_AUTHORIZATION = PRESERVED
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

current_authorized_workstream = NONE
next_permitted_workstream = NONE_UNTIL_SEPARATE_OWNER_ADMIN_DECISION

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

PRIMARY_RESEARCH_QUESTION =
ARCHITECTURE_LEVEL_SUPERVISED_GATING_INCREMENTAL_VALUE

PREDECLARED_RL_CANDIDATE_SET =
PPO_SAC_RECURRENTPPO

COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

CANDIDATE_SET_EXPANSION =
NOT_AUTHORIZED

FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO

C5_REOPEN =
NO

C5_CURRENT_WORK =
NONE

C6_AUTHORIZATION =
SEPARATE_OWNER_ADMIN_DECISION

C6_authorization_effect = NONE

dataset_status = NO_NEW_REPOSITORY_DATASET_SELECTED_OR_ACCEPTED
provider_acceptance_status = NONE
dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED
final_ticker_universe_status = NOT_SELECTED

current_model_candidate = NONE
current_deployment_candidate = NONE

CURRENT_CHECKPOINT_TRACKER = NONE
```

The repository was initially created as private; `repository_visibility = PUBLIC`
records its current visibility.

## 1. Project

Build a canonical, reproducible, leakage-controlled quantitative research and trading platform supporting:

- Standalone PPO v2.
- PPO plus Random Forest gate.
- PPO plus XGBoost gate.
- Fair comparison of eligible frozen candidates using common data, splits, costs, benchmarks, and one shared untouched final holdout.
- Publication-quality research, controlled paper trading, and possible later live-capital consideration under separate authorization.

Historical repositories remain evidence and engineering sources, not runtime dependencies or sources of current authorization.

## 2. Controlling role

This document is the sole controlling source for:

- Lifecycle, active phase, and phase status.
- Authorized and prohibited work.
- Current material blocker or decision.
- Dataset, model, environment, and access status.
- Latest completed phase, active milestone, and next permitted workstream.
- Required maps and latest material records.

It does not contain detailed chronology or a completed governance chain. Git history and the working tree verify implementation state; they do not establish current authorization.

## 3. Lifecycle, entry gate, and current status

```text
PRE_C0_DRAFT_REVIEW
→ C0_ACTIVE
→ C0_COMPLETED
→ C1_ACTIVE
→ C1_COMPLETED
→ C2_ACTIVE
→ C2_COMPLETED
→ C3_ACTIVE
→ C3_COMPLETED
→ C4_ACTIVE
→ C4_COMPLETED
→ C5_ACTIVE
→ C5_COMPLETED
```

C0 through C4 remain completed and effective.

The Owner has accepted C5 completion and closure after the complete C5
data-source, calendar, historical-timing, PIT-eligibility, cost, and regime
decision surface passed final exit-readiness review.

The aligned completed target has no active major phase and no current C5
execution authorization. Effective lifecycle closure requires canonical
recording of this aligned target followed by successful required exact
validation of that canonical commit.

C5 completion does not authorize C6 or any provider, data, model, holdout,
broker, paper-trading, or live-trading execution.

```text
current_material_blocker = NONE
current_lifecycle_state = C5_COMPLETED
active_major_phase = NONE
proposed_next_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE

C4_completion_effect = EFFECTIVE
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_authorization_decision = docs/decisions/C5_authorization_decision.md
C5_authorization_decision_id = GOV-DEC-0011
C5_authorization_status = AUTHORIZED
C5_owner_decision_status = ACCEPTED

C5_completion_decision = docs/decisions/C5_completion_decision.md
C5_completion_decision_id = GOV-DEC-0012
C5_completion_status = ACCEPTED
C5_scientific_decision_work = COMPLETE
C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
HISTORICAL_C5_AUTHORIZATION = PRESERVED
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

current_authorized_workstream = NONE
next_permitted_workstream = NONE_UNTIL_SEPARATE_OWNER_ADMIN_DECISION

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

PRIMARY_RESEARCH_QUESTION =
ARCHITECTURE_LEVEL_SUPERVISED_GATING_INCREMENTAL_VALUE

PREDECLARED_RL_CANDIDATE_SET =
PPO_SAC_RECURRENTPPO

COMMON_ACTION_FORMULATION =
CONTINUOUS_TARGET_POSITION_OR_EXPOSURE

CANDIDATE_SET_EXPANSION =
NOT_AUTHORIZED

FORCED_TRAINING_OF_UNREADY_CANDIDATE =
NO

C5_REOPEN =
NO

C5_CURRENT_WORK =
NONE

C6_AUTHORIZATION =
SEPARATE_OWNER_ADMIN_DECISION

C6_authorization_effect = NONE

dataset_status = NO_NEW_REPOSITORY_DATASET_SELECTED_OR_ACCEPTED
provider_acceptance_status = NONE
dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED
final_ticker_universe_status = NOT_SELECTED

current_model_candidate = NONE
current_deployment_candidate = NONE

CURRENT_CHECKPOINT_TRACKER = NONE
```

The post-C5/pre-C6 RL-design alignment requirement does not reopen C5, does not
block C5 closure, and does not itself authorize the alignment work or C6.

## 4. Completed C2 scope and preserved C1 evidence

C2 completed the accepted non-operational repository-skeleton and migration-preparation scope.

The completed C2 package is limited to:

- Creating the three accepted C2 output documents.
- Creating the approved `src/quantitative_trading_research/` responsibility-document skeleton.
- Creating the exact approved empty or docstring-only package markers.
- Providing high-level dispositions for all 82 accepted C1 manifest items.
- Providing full destination, wave, limitation, and verification planning only for C3/C4-relevant items.
- Maintaining the authoritative `items` and `unresolved_limitations` YAML collections.
- Preparing a bounded C3 environment-reconstruction handoff.
- Updating the existing documentation-consistency workflow with bounded document, structure, YAML, and referential-integrity validation.

The accepted C1 outputs remain immutable:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

The accepted C1 completion evidence remains:

```text
independent_C1_audit = docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md
independent_C1_audit_classification = PASS
bounded_section_coverage = 15_OF_15_CONFIRMED
completion_decision = docs/decisions/C1_completion_decision.md
completion_decision_id = GOV-DEC-0004
completion_decision_owner_status = ACCEPTED
accepted_C1_artifacts = IMMUTABLE
```

Historical repositories remain read-only evidence and engineering sources. They are not runtime dependencies or sources of current authorization.

## 5. Continuing non-authorization

C5 scientific decision work is complete. No current C5 execution authorization
remains after effective closure.

The accepted historical C5 authorization and substantive decision evidence
remain preserved as research lineage; they do not create a current executable
workstream.

```text
C6_authorization_effect = NONE
dataset_contract_freeze = NOT_AUTHORIZED
provider_purchase_or_account_activity = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
market_or_reference_data_acquisition = NOT_AUTHORIZED
historical_universe_construction = NOT_AUTHORIZED
dataset_generation = NOT_AUTHORIZED
dataset_acceptance = NOT_AUTHORIZED
model_training = NOT_AUTHORIZED
model_selection_or_retraining = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
scientific_host_qualification = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
broker_account_activity = NOT_AUTHORIZED
```

The separate post-C5/pre-C6 RL-design alignment must be resolved before any C6
dataset contract may be frozen. That requirement is a scientific-design
boundary only and is not authorization to perform the alignment or to begin
C6.

Repository public release remains complete under its separate historical
authorization and does not authorize additional operational, model, holdout,
trading, or later-phase work.

Historical repository material remains evidence and engineering lineage, not
current runtime dependency or authorization.

## 6. Current material decisions

```text
presumptive_architecture_source = racoope70/ppo-trading-pipeline
canonical_package_name = quantitative_trading_research
automatic_module_acceptance = NO
accepted_C1_artifacts = IMMUTABLE
abstract_interface_stubs_during_C2 = NOT_AUTHORIZED
provider_or_broker_specific_implementation_during_C2 = NOT_AUTHORIZED
supported_python_version = 3.13__CPYTHON_3.13.14
final_ticker_universe = NOT_SELECTED
```

## 7. Dataset status

```text
dataset_status = NO_NEW_REPOSITORY_DATASET_SELECTED_OR_ACCEPTED
provider_acceptance_status = NONE
dataset_contract_status = NOT_STARTED
dataset_generation_status = NOT_AUTHORIZED
final_ticker_universe_status = NOT_SELECTED
historical_six_symbol_group_status = CANDIDATE_ONLY
```

Historical v3.08 established only that no acceptable raw candidate existed under its old zero-missing-slot-tolerance contract.

## 8. Model status

```text
legacy_ppo_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
legacy_ppo_random_forest_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
ppo_v2_status = HISTORICAL_SCAFFOLDING_EXISTS_NOT_TRAINED_IN_NEW_REPOSITORY
random_forest_gate_status = FUTURE_PHASE
xgboost_gate_status = FUTURE_PHASE
current_model_candidate = NONE
current_deployment_candidate = NONE
```

Historical models do not become current candidates through review, classification, completion, or migration recommendation.

## 9. Environment and access status

```text
canonical_environment_status = ESTABLISHED_AND_EFFECTIVE
canonical_platform = LINUX_X86_64_AMD64
supported_python_version = 3.13__CPYTHON_3.13.14
dependency_environment_source_phase = C3_COMPLETED
network_or_api_testing = NOT_AUTHORIZED
market_data_access = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
scientific_host_qualification = NOT_AUTHORIZED
```

The accepted C3 environment remains the controlling canonical environment foundation. C4 completion does not redesign or reopen it.

## 10. Completed governance evidence through C5

C0 through C4 remain completed and effective.

The Owner C5 authorization remains preserved as historical evidence. The Owner
has now accepted C5 completion and closure after the final C5 exit-readiness
audit found no material unresolved C5 items.

The completion/current-state alignment target becomes effective only after
canonical recording and successful required exact validation.

```text
C0_completion_decision = docs/decisions/C0_completion_decision.md
C0_completion_decision_id = GOV-DEC-0002

C1_completion_decision = docs/decisions/C1_completion_decision.md
C1_completion_decision_id = GOV-DEC-0004
C1_completion_effect = EFFECTIVE

C2_authorization_decision = docs/decisions/C2_authorization_decision.md
C2_authorization_decision_id = GOV-DEC-0005
C2_completion_decision = docs/decisions/C2_completion_decision.md
C2_completion_decision_id = GOV-DEC-0006
C2_completion_effect = EFFECTIVE

C3_authorization_decision = docs/decisions/C3_authorization_decision.md
C3_authorization_decision_id = GOV-DEC-0007
C3_completion_decision = docs/decisions/C3_completion_decision.md
C3_completion_decision_id = GOV-DEC-0008
C3_completion_effect = EFFECTIVE

C4_authorization_decision = docs/decisions/C4_authorization_decision.md
C4_authorization_decision_id = GOV-DEC-0009
C4_completion_decision = docs/decisions/C4_completion_decision.md
C4_completion_decision_id = GOV-DEC-0010
C4_completion_status = ACCEPTED
C4_completion_effect = EFFECTIVE
CURRENT_C4_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_authorization_decision = docs/decisions/C5_authorization_decision.md
C5_authorization_decision_id = GOV-DEC-0011
C5_authorization_status = AUTHORIZED
C5_owner_decision_status = ACCEPTED

C5_completion_decision = docs/decisions/C5_completion_decision.md
C5_completion_decision_id = GOV-DEC-0012
C5_completion_status = ACCEPTED
C5_scientific_decision_work = COMPLETE
C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
HISTORICAL_C5_AUTHORIZATION = PRESERVED
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

C5_REOPEN =
NO

C5_CURRENT_WORK =
NONE

C6_AUTHORIZATION =
SEPARATE_OWNER_ADMIN_DECISION

C6_authorization_effect = NONE
```

These records do not authorize provider operations, dataset-contract freeze,
dataset generation or acceptance, model work, final-holdout access, trading,
or C6.

## 11. Major milestone pointers

```text
latest_completed_major_milestone = C5_DATA_SOURCE_CALENDAR_AND_INITIAL_UNIVERSE_DECISION
active_major_milestone = NONE
latest_authorization_decision = docs/decisions/C5_authorization_decision.md
latest_completion_record = docs/decisions/C5_completion_decision.md
next_permitted_workstream = NONE_UNTIL_SEPARATE_OWNER_ADMIN_DECISION
```

## 12. Required reading and project orientation

For project orientation, the following reading and verification are required:

1. Read `PROJECT_CONTEXT.md`.
2. Read the applicable Milestone Map section and curated 2v records.
3. Read the applicable Future Map section.
4. Inspect Git history and the working tree to verify accepted implementation
   and completed work.

```text
latest_material_decision = docs/decisions/post_C5_pre_C6_RL_research_design_decision.md
latest_material_completion_record = docs/decisions/C5_completion_decision.md
latest_material_independent_audit = FINAL_C5_EXIT_READINESS_AUDIT__PASS
```

## 13. Maintenance guidance

```text
target_length = APPROXIMATELY_75_TO_150_LINES
numeric_hard_failure_rule = NONE
```
