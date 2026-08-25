# C5 Data Source, Calendar, and Initial Universe Decision Authorization Decision

```text
document_status = ACCEPTED_C5_AUTHORIZATION_DECISION
intended_repository_path = docs/decisions/C5_authorization_decision.md
decision_id = GOV-DEC-0011
decision_type = C5_PHASE_AUTHORIZATION_CANONICAL_RECORDING
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED

OWNER_DECISION_ALREADY_MADE = YES
NEW_SUBSTANTIVE_AUTHORIZATION_CREATED_BY_THIS_ALIGNMENT = NO

authorized_phase =
C5_DATA_SOURCE_CALENDAR_AND_INITIAL_UNIVERSE_DECISION

C5_scope =
BOUNDED_DATA_SOURCE_CALENDAR_AND_INITIAL_UNIVERSE_DECISION

C5_entry_prerequisite = SATISFIED
C4_completion_effect = EFFECTIVE
C4_reopen = NO

C5_authorization_status = AUTHORIZED
C5_owner_decision_status = ACCEPTED
authorization_scope = C5_SCOPE_ONLY

pre_merge_lifecycle_effect = NONE
post_merge_pre_validation_C5_activation_effect = NOT_YET_VERIFIED_EFFECTIVE
Stage_A_exact_post_merge_validation_effect =
SATISFIES_C5_ACTIVATION_PRECONDITION_ONLY

subsequent_current_state_recording_required = YES
C6_authorization_effect = NONE
remaining_material_owner_decisions = NONE
```

## 1. Purpose

This record canonically records an Owner C5 authorization that has already
been made and accepted.

It does not create a new substantive Owner decision, does not expand C5, and
does not itself make C5 the current active lifecycle phase.

During this Stage A recording, `PROJECT_CONTEXT.md` remains truthfully aligned
to:

```text
current_lifecycle_state = C4_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = NONE
```

Successful exact post-merge validation of the Stage A canonical alignment
establishes the C5 activation precondition only.

A subsequent bounded current-state recording transaction is still required
before `PROJECT_CONTEXT.md` may record `C5_ACTIVE` and
`authorization_effect = C5_SCOPE_ONLY`.

No new Owner decision is required for that later bounded state-recording
transaction.

## 2. Owner-authorized C5 scope

The Owner-authorized C5 scope is limited to:

1. Evaluate provider candidates and provider strategy.

2. Evaluate provider and feed characteristics relevant to the canonical
   research program.

3. Review licensing, permitted-use, and relevant entitlement requirements at
   the research and decision level.

4. Define canonical market-calendar, session, timestamp, and related
   source-selection requirements necessary for the C5 decision.

5. Define and evaluate initial universe-selection criteria, including
   liquidity, spreads and expected costs, coverage, corporate actions,
   sector and regime diversity, provider availability, compute requirements,
   survivorship bias, and selection bias.

6. Produce bounded C5 data-source, calendar, and initial-universe decision
   evidence and perform the review or audit necessary for the C5 exit
   decision.

After canonical C5 activation becomes effective, research-level review of
public provider documentation, licensing terms, calendar specifications,
feed descriptions, and historical evidence belongs to this bounded scope.

## 3. Preserved exclusions

```text
credentials = NOT_AUTHORIZED
authenticated_provider_access = NOT_AUTHORIZED
network_or_API_data_acquisition = NOT_AUTHORIZED
provider_account_activity = NOT_AUTHORIZED
production_market_data_requests = NOT_AUTHORIZED
dataset_generation = NOT_AUTHORIZED
dataset_acceptance = NOT_AUTHORIZED
C6_dataset_contract_freeze = NOT_AUTHORIZED
model_training = NOT_AUTHORIZED
model_retraining_or_selection = NOT_AUTHORIZED
model_qualification = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
scientific_host_qualification = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
broker_account_activity = NOT_AUTHORIZED
public_release = NOT_AUTHORIZED
Change_Point_Analysis_execution = NOT_AUTHORIZED
C6_or_any_later_phase = NOT_AUTHORIZED
```

C4 remains completed and effective and is not reopened.

## 4. Governance role

`PROJECT_CONTEXT.md` remains the controlling broad current lifecycle and
authorization-state document.

The Milestone Review Reference Map remains a non-authorizing roadmap,
navigation, governance, 2v, and evidence reference.

The Future Validation and Training Reference Map remains a non-authorizing
future-guidance and sequencing reference.

This decision record is supporting authorization evidence only. It is not a
current checkpoint tracker and does not create another approval layer.

```text
CURRENT_CHECKPOINT_TRACKER = NONE
```
