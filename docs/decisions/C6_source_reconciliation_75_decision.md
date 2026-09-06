# C6 75-Security Source-Reconciliation Decision

```text
document_status = ACCEPTED_C6_SOURCE_RECONCILIATION_75_DECISION
document_role = SUPPORTING_MATERIAL_OWNER_DISPOSITION_EVIDENCE
authorization_effect = NONE
intended_repository_path = docs/decisions/C6_source_reconciliation_75_decision.md
decision_id = GOV-DEC-0015
decision_type = C6_SOURCE_RECONCILIATION_75_CANONICAL_RECORDING
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED
OWNER_DECISION_ALREADY_MADE = YES
NEW_SUBSTANTIVE_OWNER_DECISION_CREATED_BY_THIS_RECORD = NO
NEW_SCIENTIFIC_RULE_CREATED_BY_THIS_RECORD = NO
CURRENT_CHECKPOINT_TRACKER = NONE
```

## Owner/Admin disposition

This record canonically records the Owner/Admin decision already made. It
creates no new substantive decision or scientific rule.

```text
OWNER_DECISION = RESOLVE_C6_SOURCE_RECONCILIATION_75_AS_NONCONTROLLING__RETIRED
SOURCE_RECONCILIATION_75_STATUS = RESOLVED_AS_NONCONTROLLING__RETIRED
CONTROLLING_75_SECURITY_RULE = NONE
ACCEPTED_UNIVERSE_RULES_CHANGED = NO
C6_G_REOPEN_REQUIRED = NO
SOURCE_RECONCILIATION_75_FREEZE_BLOCKER = CLEARED_BY_OWNER_ADMIN_DISPOSITION
MAXIMUM_ACCEPTABLE_UNIVERSE_75 = NOT_A_CONTROLLING_RULE
```

Historical `50 to 75` wording is non-authoritative and retired. It creates no
upper-bound requirement or scientific requirement and does not modify the
accepted universe rules. The accepted rules remain:

```text
60_OR_MORE = SELECT_EXACTLY_60
50_TO_59 = SELECT_ALL_ELIGIBLE_WITHOUT_RELAXING_THRESHOLDS
BELOW_50 = UNDERFILLED_BELOW_ACCEPTED_RANGE__RETURN_FOR_REVIEW_BEFORE_UNIVERSE_CONSTRUCTION_PROCEEDS
```

## Binding to final C6-G evidence

The established final independent-review evidence supplied for this canonical
recording is:

```text
C6_G = COMPLETE__INDEPENDENT_REVIEW_PASS
C6_G_FINAL_REVIEW_DISPOSITION = PASS
C6_G_REVIEW_CLOSED = YES
C6_G_REOPEN_REQUIRED = NO
C6_G_REVIEWED_CONTRACT_SHA256 = bc452466d4a1db129568e23657351bfab8a51e6248eea3954b2a729f7cb87dc6
C6_G_REVIEWED_CONTRACT_GIT_BLOB_SHA = 6aa1d7887c1ef701ca66c9d354396dbc5a204004
c6_independent_review_identity = 5a69af6f2eca2b87ceb937beb71eccbd67d5fb51e15fc4a4e695d3adbbf15576
```

The reviewed contract at `docs/architecture/C6_dataset_contract.md` remains
byte-identical: 191289 bytes. This separate disposition records retirement of
the source note without editing that independently reviewed artifact or
reopening C6-G.

## Source-reconciliation disposition identity

```text
source_reconciliation_disposition_spec_version = C6_SOURCE_RECONCILIATION_DISPOSITION_V1
source_reconciliation_disposition_identity = 50c5e643692a9eeb326b622c0f8056d49e50c6672f686c69d9545680853c0488
```

The identity is lowercase SHA-256 over the UTF-8 bytes of the exact canonical
JSON below, with lexicographically sorted object keys and no insignificant
whitespace or trailing newline in the hashed payload. Boolean values are JSON
booleans. The payload contains exactly the twelve prescribed fields and no
observational timestamps, local paths, or self-identity field, following the
C6 section-17 canonical serialization rules.

CANONICAL_SOURCE_RECONCILIATION_DISPOSITION_PAYLOAD:

```json
{"accepted_universe_rules_changed":false,"c6_g_reopen_required":false,"c6_g_reviewed_contract_sha256":"bc452466d4a1db129568e23657351bfab8a51e6248eea3954b2a729f7cb87dc6","c6_independent_review_identity":"5a69af6f2eca2b87ceb937beb71eccbd67d5fb51e15fc4a4e695d3adbbf15576","controlling_75_security_rule":"NONE","decision_id":"GOV-DEC-0015","owner_decision":"RESOLVE_C6_SOURCE_RECONCILIATION_75_AS_NONCONTROLLING__RETIRED","rule_50_to_59":"SELECT_ALL_ELIGIBLE_WITHOUT_RELAXING_THRESHOLDS","rule_60_or_more":"SELECT_EXACTLY_60","rule_below_50":"UNDERFILLED_BELOW_ACCEPTED_RANGE__RETURN_FOR_REVIEW_BEFORE_UNIVERSE_CONSTRUCTION_PROCEEDS","source_reconciliation_75_status":"RESOLVED_AS_NONCONTROLLING__RETIRED","source_reconciliation_disposition_spec_version":"C6_SOURCE_RECONCILIATION_DISPOSITION_V1"}
```

## Non-authorization boundary

This record clears the specific source-reconciliation blocker only. It does
not itself authorize or execute C6-H, freeze the contract, or authorize C7.

```text
C6_H_AUTHORIZATION = NONE
C6_H_FREEZE_EXECUTED = NO
C6_DATASET_CONTRACT = NOT_FROZEN
DATASET_ACCEPTANCE_EXECUTED = NO
DATA_GENERATED = NO
FEATURES_GENERATED = NO
MODEL_IMPLEMENTED = NO
MODEL_TRAINED = NO
QUALIFICATION_EXECUTED = NO
FINAL_HOLDOUT_ACCESSED = NO
C7_STARTED = NO
CURRENT_CHECKPOINT_TRACKER = NONE
```
