# C4 Selected Code Migration, Adaptation, and Verification Authorization Decision

```text
document_status = ACCEPTED_C4_AUTHORIZATION_DECISION
intended_repository_path = docs/decisions/C4_authorization_decision.md
decision_id = GOV-DEC-0009
decision_type = C4_PHASE_AUTHORIZATION_CANONICAL_RECORDING
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED

OWNER_DECISION_ALREADY_MADE = YES
CANONICAL_RECORDING_PREVIOUSLY_MISSING = YES
NEW_SUBSTANTIVE_AUTHORIZATION_CREATED_BY_THIS_ALIGNMENT = NO

C4_authorization_status = AUTHORIZED
C4_authorization_effect = EFFECTIVE
authorization_effect = C4_SCOPE_ONLY

authorized_phase =
C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION

C4_scope =
BOUNDED_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION

selected_C4_surface =
OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET

selected_item_count = 21
excluded_item_count = 2
deferred_item_count = 18

C3_completion_effect = EFFECTIVE
C4_environment_entry_prerequisite = SATISFIED

remaining_material_owner_decisions = NONE
```

## 1. Purpose

This decision record canonically records an Owner C4 authorization that was
already made before this repository-recording alignment.

This document does not create a new substantive Owner decision and does not
expand the previously accepted C4 scope.

The authorized C4 phase is:

```text
C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
```

The authorized work is bounded to selected-code migration, required adaptation,
item-level verification, focused offline tests, C4-scoped evidence, and other
strictly necessary work that remains within the Owner-selected C4 surface.

Historical source is evidence and implementation input. Historical behavior is
not automatically accepted and historical code need not be copied unchanged.

## 2. Selected C4 surface

The controlling selected surface is:

```text
selected_C4_surface =
OWNER_ACCEPTED_21_ITEM_BOUNDED_OFFLINE_C4_SUBSET

selected_item_count = 21
excluded_item_count = 2
deferred_item_count = 18
```

Automatic promotion of all historical migration-preparation candidates is not
authorized.

An included item may be inspected, migrated or reimplemented, adapted as
required, and verified offline only within its selected responsibility.

If an included responsibility cannot be implemented without crossing a
preserved later-phase or dependency-policy boundary, that item must stop and be
routed through the established authorization process rather than silently
expanding C4.

## 3. Preserved boundaries

This C4 authorization does not authorize:

```text
C5_OR_LATER = NOT_AUTHORIZED
provider_operations = NOT_AUTHORIZED
network_provider_operations = NOT_AUTHORIZED
model_training = NOT_AUTHORIZED
model_retraining = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED
paper_order_submission = NOT_AUTHORIZED
live_order_submission = NOT_AUTHORIZED
scientific_host_qualification = DEFERRED
dependency_policy_redesign = NOT_AUTHORIZED
canonical_Python_redesign = NOT_AUTHORIZED
canonical_lock_redesign = NOT_AUTHORIZED
CPA_implementation = NOT_AUTHORIZED
```

C3 remains completed and is not reopened by this authorization record.

The C3 dependency environment remains controlling unless separately changed
through an authorized later decision.

## 4. Governance effect

`PROJECT_CONTEXT.md` remains the broad current lifecycle and authorization
source of truth.

This decision record is supporting authorization evidence. It is not a current
checkpoint tracker and does not authorize work beyond the bounded C4 scope
recorded above.

The Milestone Review Reference Map remains non-authorizing roadmap,
navigation, governance, and evidence reference material.

The Future Validation and Training Reference Map remains non-authorizing future
guidance and sequencing material.

```text
CURRENT_CHECKPOINT_TRACKER = NONE
```
