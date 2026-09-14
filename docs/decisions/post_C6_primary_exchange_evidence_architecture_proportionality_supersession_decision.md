# Post-C6 Primary-Exchange Evidence Architecture Proportionality Supersession Decision

## Decision record

```text
document_status =
OWNER_AUTHORIZED_MATERIAL_DECISION

document_role =
MATERIAL_OWNER_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE_PROPORTIONALITY_SUPERSESSION_DECISION

current_state_control =
NO

decision_id =
GOV-DEC-0021

owner_decision =
AUTHORIZE_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE_PROPORTIONALITY_SUPERSESSION
__PRESERVE_ALL_POINT_IN_TIME_IDENTITY_CUTOFF_AND_FAIL_CLOSED_CONTROLS

decision_effect =
LOCALIZED_PRIMARY_EXCHANGE_EVIDENCE_SOURCE_ARCHITECTURE_SUPERSESSION_ONLY

canonical_effectiveness =
EFFECTIVE_ONLY_AFTER_ACCEPTED_RECORDING_ON_CANONICAL_MAIN

superseded_rule_component =
GOV_DEC_0020_SPECIFIC_SOURCE_EXCLUSIVITY_ONLY

historical_decision_mutation =
NO
```

This decision records the Owner-authorized proportionality supersession of the
project's primary-exchange evidence-source architecture.

It changes only the requirement that acceptable primary-exchange evidence be
exclusive to the two named sources established through GOV-DEC-0020:

- NYSE Daily TAQ Master / `Listed Exchange`; or
- NYSE Group Equity Security Master / `Primary Market`.

It does not weaken the governed scientific requirement to establish the
historical security-specific or share-class-specific primary listing market.

It does not itself acquire evidence, access a provider, classify or reclassify
a security, certify eligibility, mutate universe membership, execute any later
Architecture-B step, reopen C5 or C6, generate a dataset, perform model work,
open the final holdout, or authorize C7.

`PROJECT_CONTEXT.md` remains the controlling source of truth for broad current
lifecycle state, authorization boundaries, current non-authorization state,
and authoritative pointers to material decisions.

## Historical decisions preserved

```text
C5_HISTORICAL_DECISION =
UNCHANGED_HISTORICAL_DECISION_TIME_EVIDENCE

GOV_DEC_0020 =
UNCHANGED_HISTORICAL_MATERIAL_DECISION

GOV_DEC_0021_PROSPECTIVE_SUPERSESSION =
GOV_DEC_0020_SPECIFIC_SOURCE_EXCLUSIVITY_ONLY
```

The historical C5 eligibility decision remains evidence of the rule accepted
at its decision time, including its use of NYSE Daily TAQ Master / `Listed
Exchange`.

GOV-DEC-0020 remains immutable historical evidence of the later accepted
two-source architecture.

GOV-DEC-0021 does not retrospectively rewrite either historical decision.

After canonical effectiveness, GOV-DEC-0021 prospectively supersedes only the
specific-source exclusivity component of GOV-DEC-0020.

## Preserved scientific controls

The following controls remain unchanged and mandatory:

```text
FORMATION_POINT =
2024-09-03_REGULAR_SESSION_OPEN

INFORMATION_CUTOFF =
COMPLETED_2024-08-30_REGULAR_SESSION

REQUIRED_FACT =
HISTORICAL_SECURITY_SPECIFIC_OR_SHARE_CLASS_SPECIFIC_PRIMARY_LISTING_MARKET

EXACT_SECURITY_IDENTITY =
REQUIRED

EXACT_SHARE_CLASS =
REQUIRED_WHERE_APPLICABLE

CURRENT_STATE_BACKCAST =
PROHIBITED

POST_CUTOFF_INFORMATION_USED_TO_CREATE_PASS =
PROHIBITED

UNACCEPTED_PREDECESSOR_SUCCESSOR_STITCHING =
PROHIBITED

CONFLICTING_AUTHORITATIVE_EVIDENCE =
UNRESOLVED

AMBIGUOUS_IDENTITY =
UNRESOLVED

AMBIGUOUS_SHARE_CLASS =
UNRESOLVED

AMBIGUOUS_CUTOFF_ADMISSIBILITY =
UNRESOLVED

ELIGIBILITY_FAVORING_TIE_BREAK =
PROHIBITED

FAIL_CLOSED =
YES

SCIENTIFIC_RIGOR_RELAXED =
NO

SOURCE_EXCLUSIVITY_RELAXED =
YES
```

The supersession concerns proportionality of the evidence-source architecture,
not the rigor of the underlying historical eligibility fact.

## Bounded primary-exchange evidence architecture

### Tier 1 — official historical exchange evidence

```text
TIER_1 =
OFFICIAL_HISTORICAL_EXCHANGE_RECORD
OR
OFFICIAL_EXCHANGE_LISTING_DELISTING_TRANSFER_NOTICE
```

Tier-1 evidence is admissible only where it establishes:

- exact security or applicable share class sufficiently;
- direct listing-market semantics;
- the relevant effective state or date;
- cutoff admissibility; and
- sufficient event-chain closure through the governed cutoff.

### Tier 2 — contemporaneous SEC EDGAR evidence

```text
TIER_2 =
CONTEMPORANEOUS_SEC_EDGAR_RECORD
```

Tier-2 evidence is admissible only where it contains:

- exact security or applicable share class;
- explicit listing, primary listing, principal listing, delisting, or transfer
  language;
- named relevant market or markets;
- effective timing sufficient to establish the governed historical state; and
- filing or publication information admissible under the existing cutoff.

```text
GENERIC_SECTION_12B_EXCHANGE_REGISTRATION_ONLY =
INSUFFICIENT
```

A generic Securities Exchange Act Section 12(b) registration table or exchange
registration reference must not automatically be normalized to the security's
primary listing market.

### Tier 3 — other authoritative effective-dated reference evidence

```text
TIER_3 =
OTHER_AUTHORITATIVE_EFFECTIVE_DATED_REFERENCE_SOURCE
```

Tier-3 evidence requires:

- explicit primary-listing-market semantics;
- historical point-in-time or effective-dated capability;
- exact security identity;
- exact share-class control where applicable;
- cutoff compatibility; and
- reproducible auditable provenance.

```text
NEW_TIER_3_PROVIDER_FIRST_USE =
REQUIRES_SEPARATE_SCIENTIFIC_VALIDATION_AND_ACCEPTANCE
```

The existence of Tier 3 does not automatically accept any commercial,
reference-data, or other provider.

## Currently accepted high-quality sources

The following currently accepted sources remain scientifically admissible:

```text
NYSE_DAILY_TAQ_MASTER
FIELD =
Listed Exchange

NYSE_GROUP_EQUITY_SECURITY_MASTER
FIELD =
Primary Market

PRIOR_NAMED_SOURCE_STATUS =
EXCLUSIVE_ACCEPTED_ARCHITECTURE

CURRENT_NAMED_SOURCE_STATUS =
ACCEPTED_HIGH_QUALITY_EVIDENCE_SOURCES_WITHIN_THE_BROADER_ARCHITECTURE
```

They are not deprecated, invalidated, or scientifically weakened by this
decision.

## Cross-tier decision rules

```text
USE_HIGHEST_AVAILABLE_TIER_FIRST =
YES

SINGLE_UNAMBIGUOUS_AUTHORITATIVE_RECORD_CAN_ESTABLISH_FACT =
YES__CONDITIONAL
```

A single authoritative record may establish the required fact only when all of
the following are satisfied:

```text
DIRECT_PRIMARY_OR_PRINCIPAL_LISTING_SEMANTICS =
YES

EXACT_SECURITY_OR_SHARE_CLASS_IDENTITY =
YES

CUTOFF_ADMISSIBILITY =
YES

EVENT_CHAIN_CLOSURE_SUFFICIENT =
YES

CONFLICTING_ADMISSIBLE_AUTHORITATIVE_EVIDENCE =
NO
```

```text
MULTIPLE_SOURCES_REQUIRED =
CONDITIONAL
```

Additional evidence is required where:

- a record predates the cutoff sufficiently that an intervening listing event
  could change state;
- source semantics are indirect;
- identity requires a crosswalk;
- share-class identity is uncertain; or
- historical state is otherwise incompletely established.

Fail-closed cross-tier rules are:

```text
IF_AUTHORITATIVE_SOURCES_CONFLICT =
UNRESOLVED

IF_IDENTITY_AMBIGUOUS =
UNRESOLVED

IF_SHARE_CLASS_AMBIGUOUS =
UNRESOLVED

IF_CUTOFF_ADMISSIBILITY_AMBIGUOUS =
UNRESOLVED

IF_EVENT_CHAIN_CANNOT_BE_CLOSED =
UNRESOLVED

IF_ONLY_CURRENT_METADATA_EXISTS =
UNRESOLVED

IF_ONLY_EXCHANGE_REGISTRATION_EXISTS =
UNRESOLVED

NO_ELIGIBILITY_FAVORING_TIE_BREAK =
YES
```

## Event-chain closure

Event-chain closure remains a mandatory scientific control.

An earlier historical listing record does not automatically establish the
security's state as of the completed 2024-08-30 regular session.

Where a source record predates the cutoff and an intervening event could
reasonably change listing state, later separately authorized evidence
acquisition must search through the governed cutoff for relevant:

- listing transfers;
- delistings;
- Form 25 activity where applicable;
- SEC Item 3.01 events where applicable;
- official exchange listing, delisting, or transfer notices; and
- other admissible listing-state changes.

If the event chain cannot be closed adequately:

```text
PRIMARY_EXCHANGE_STATUS =
UNRESOLVED
```

No post-cutoff fact may be used to manufacture a formation-point pass.

## Minimum provenance requirements

Any later separately authorized evidence acquisition and classification must
preserve, as applicable:

```text
SOURCE_TIER
SOURCE_TYPE
SOURCE_NAME
CANONICAL_URL_OR_ACCESSION
PUBLICATION_OR_EDGAR_ACCEPTANCE_TIMESTAMP
RELEVANT_EFFECTIVE_DATE
CIK_OR_EXCHANGE_SECURITY_IDENTIFIER
CUSIP_OR_OTHER_STABLE_IDENTIFIER_WHERE_AVAILABLE
EXACT_SECURITY_TITLE
EXACT_SHARE_CLASS
FORMATION_TICKER_OR_SYMBOL
RAW_LISTING_STATEMENT_OR_FIELD_VALUE
NORMALIZED_PRIMARY_MARKET
EVENT_CHAIN_SEARCH_START
EVENT_CHAIN_SEARCH_END
INTERVENING_LISTING_EVENT_RESULT
CONFLICT_CHECK_RESULT
SOURCE_ARTIFACT_HASH_OR_EQUIVALENT_IMMUTABLE_PROVENANCE
```

Reproducibility remains mandatory.

If evidence sufficient to reproduce the classification cannot be preserved,
the required fact remains unresolved.

## Massive status

```text
MASSIVE_STOCKS_REFERENCE_DATA =
CANDIDATE_ONLY

MASSIVE_SOURCE_USE_AUTHORIZED =
NO

MASSIVE_PURCHASE_AUTHORIZED =
NO

MASSIVE_PAYMENT_AUTHORIZED =
NO

MASSIVE_FIRST_USE_REQUIRES =
SEPARATE_SCIENTIFIC_VALIDATION_AND_ACCEPTANCE
```

The broader Tier-3 architecture does not silently elevate Massive Stocks
reference data into an accepted Tier-3 source.

No Massive account, purchase, payment, access, evidence acquisition, or
scientific use is authorized by this decision.

## Current 23-security state

This decision does not classify or reclassify any security.

```text
PRIMARY_EXCHANGE_PASS_COUNT =
0

PRIMARY_EXCHANGE_FAIL_COUNT =
0

PRIMARY_EXCHANGE_UNRESOLVED_COUNT =
23

PRIMARY_EXCHANGE_EVIDENCE_CLASSIFICATION_PERFORMED_BY_THIS_DECISION =
NO

FULL_ELIGIBILITY_RECERTIFICATION_PERFORMED =
NO
```

The 23 potentially retainable securities are not declared fully eligible by
this decision.

Their primary-exchange fact remains unresolved pending separately authorized
evidence acquisition, classification, review, and acceptance.

The accepted 252-session-history and security-continuity findings are not
re-adjudicated here.

## Architecture-B relationship

The accepted Architecture-B corrective design remains unchanged.

```text
ARCHITECTURE_B_STATUS =
PRESERVED

HISTORICAL_30_SECURITY_FREEZE =
PRESERVED_AS_HISTORICAL_EVIDENCE

HISTORICAL_30_SECURITY_FREEZE_SCIENTIFIC_USE =
BLOCKED

CORRECTIVE_EXECUTION_AUTHORIZED_BY_GOV_DEC_0021 =
NO
```

GOV-DEC-0021 supplies a prospective scientific evidence architecture for a
later separately authorized primary-exchange evidence task.

It does not itself execute any Architecture-B step.

## Hard non-authorizations

```text
PRIMARY_EXCHANGE_EVIDENCE_ACQUISITION_AUTHORIZED =
NO__NOT_BY_THIS_RECORDING_TRANSACTION

PRIMARY_EXCHANGE_RECLASSIFICATION_AUTHORIZED =
NO

FULL_ELIGIBILITY_RECERTIFICATION_AUTHORIZED =
NO

PRICE_REVALIDATION_AUTHORIZED =
NO

LIQUIDITY_REVALIDATION_AUTHORIZED =
NO

UNIVERSE_MUTATION_AUTHORIZED =
NO

PROVISIONAL_SET_CONSTRUCTION_AUTHORIZED =
NO

HETEROGENEITY_EXECUTION_AUTHORIZED =
NO

REPRESENTATIVENESS_EXECUTION_AUTHORIZED =
NO

EXPANSION_AUTHORIZED =
NO

REFREEZE_AUTHORIZED =
NO

DATASET_GENERATION_AUTHORIZED =
NO

FEATURE_GENERATION_AUTHORIZED =
NO

MODEL_WORK_AUTHORIZED =
NO

FINAL_HOLDOUT_ACCESS_AUTHORIZED =
NO

PAPER_TRADING_AUTHORIZED =
NO

LIVE_TRADING_AUTHORIZED =
NO

DEPLOYMENT_AUTHORIZED =
NO

C7_AUTHORIZED =
NO

PURCHASE_AUTHORIZED =
NO

PAYMENT_AUTHORIZED =
NO

EXTERNAL_OUTREACH_AUTHORIZED =
NO
```

No security removal, addition, backfill, provisional universe, heterogeneity
analysis, representativeness analysis, expansion, corrected refreeze, dataset
generation, model work, final-holdout access, paper trading, live trading, or
deployment is implied.

## Document-role boundary

```text
PROJECT_CONTEXT_UPDATE_REQUIRED =
NO

PROJECT_CONTEXT.md =
BROAD_CURRENT_STATE_AND_AUTHORIZATION_CONTROLLER

GOV-DEC-0021 =
MATERIAL_SCIENTIFIC_EVIDENCE_ARCHITECTURE_SUPERSESSION_RECORD
+
NOT_CURRENT_STATE_CONTROLLER

GOV-DEC-0020 =
UNCHANGED_HISTORICAL_MATERIAL_DECISION

C5_HISTORICAL_DECISION =
UNCHANGED_HISTORICAL_DECISION_TIME_EVIDENCE

C6_DATASET_CONTRACT =
PRESERVED_AS_FROZEN_HISTORICAL_TECHNICAL_EVIDENCE

MILESTONE_REVIEW_REFERENCE_MAP =
NON_AUTHORIZING_REFERENCE_MAP

FUTURE_VALIDATION_AND_TRAINING_REFERENCE_MAP =
NON_AUTHORIZING_FUTURE_GUIDANCE

FOURTH_GOVERNANCE_CONTROLLER_CREATED =
NO

CURRENT_CHECKPOINT_TRACKER =
NONE
```

This transaction does not require mutation of `PROJECT_CONTEXT.md`, README,
either reference map, GOV-DEC-0020, the historical C5 decisions, the frozen C6
dataset contract, or the documentation-consistency validator.

## Canonical-effect boundary

```text
GOV_DEC_0021_STATUS_BEFORE_CANONICAL_ACCEPTANCE =
OWNER_AUTHORIZED__NOT_YET_CANONICALLY_EFFECTIVE

GOV_DEC_0020_REMAINS_CONTROLLING_UNTIL =
GOV_DEC_0021_ACCEPTED_RECORDING_REACHES_CANONICAL_MAIN

CANONICAL_EFFECTIVENESS =
EFFECTIVE_ONLY_AFTER_ACCEPTED_RECORDING_ON_CANONICAL_MAIN

COMMIT_BY_THIS_RECORDING_STEP =
NO

PUSH_BY_THIS_RECORDING_STEP =
NO

PR_BY_THIS_RECORDING_STEP =
NO
```

The broadened evidence architecture must not be used for primary-exchange
evidence acquisition or case classification before GOV-DEC-0021 becomes
canonically effective through an accepted recording on canonical `main`.

This draft transaction stops for Managing review before staging, commit, push,
pull-request creation, or merge.
