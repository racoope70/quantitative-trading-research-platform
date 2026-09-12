# Post-C6 Data-Access Establishment Authorization Decision

## Decision record

```text
document_status = OWNER_AUTHORIZED_MATERIAL_DECISION
document_role = MATERIAL_OWNER_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_DECISION

decision_id =
GOV-DEC-0018

title =
POST-C6 BOUNDED DATA-ACCESS ESTABLISHMENT AND ACCEPTANCE AUTHORIZATION

decision_status =
AUTHORIZED

owner_decision =
AUTHORIZE_BOUNDED_DATA_ACCESS_ESTABLISHMENT_AND_ACCEPTANCE

managing_disposition =
PASS__OWNER_BOUNDED_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_ACCEPTED
__REQUIRE_CANONICAL_AUTHORIZATION_RECORDING_BEFORE_PROVIDER_ACCESS

purpose =
ESTABLISH_AND_VERIFY_EXACT_GOVERNED_MARKET_DATA_ACCESS_PATH_REQUIRED_FOR_C7

current_state_control =
NO
```

This decision records the Owner-authorized bounded post-C6 data-access
establishment and acceptance workstream. It does not itself establish or
accept provider access and does not authorize C7.

## Authorized bounded scope

```text
authorized_scope =

IDENTIFY_CURRENTLY_INTENDED_GOVERNED_MARKET_BAR_SOURCE
VERIFY_ACCOUNT_ACCESS
VERIFY_REQUIRED_ENTITLEMENT
VERIFY_REQUIRED_HISTORICAL_DATE_COVERAGE
VERIFY_APPLICABILITY_TO_FROZEN_30_SECURITY_UNIVERSE
VERIFY_REQUIRED_MARKET_BAR_FIELDS
DOCUMENT_AUTHORITATIVE_ACCESS_EVIDENCE
RETURN_DATA_ACCESS_ACCEPTANCE_DISPOSITION

GOVERNED_DATA_SOURCE_TARGET =
ALPACA_HISTORICAL_SIP_BARS

ALPACA_FEED_REQUIREMENT =
EXPLICIT_feed=sip

DATA_ACCESS_ESTABLISHMENT_AUTHORIZED =
YES__BOUNDED_ONLY

DATA_ACCESS_AUTHORIZED =
NO__PENDING_ESTABLISHMENT_AND_ACCEPTANCE
```

The Alpaca SIP source is the bounded governed target to verify. This decision
does not predeclare that access has passed.

## Non-authorization boundary

```text
C7_AUTHORIZATION =
NONE

DATASET_GENERATION =
NOT_AUTHORIZED

FEATURE_GENERATION =
NOT_AUTHORIZED

MODEL_IMPLEMENTATION =
NOT_AUTHORIZED

MODEL_TRAINING =
NOT_AUTHORIZED

MODEL_QUALIFICATION =
NOT_AUTHORIZED

FINAL_HOLDOUT_ACCESS =
NOT_AUTHORIZED

PAPER_TRADING =
NOT_AUTHORIZED

LIVE_TRADING =
NOT_AUTHORIZED

DEPLOYMENT =
NOT_AUTHORIZED

NEW_PAID_PROVIDER_PURCHASE =
NOT_AUTHORIZED

MASSIVE_PURCHASE =
NOT_AUTHORIZED
```

DATA_ACCESS_AUTHORIZED must not be inferred merely from:

```text
PROVIDER_STRATEGY_DOCUMENTS
PROVISIONAL_PROVIDER_SELECTION
EXISTING_CREDENTIALS
HISTORICAL_TEST_FILES
PRIOR_TRIAL_VERIFICATION
PROVIDER_RESEARCH
ACCOUNT_EXISTENCE
```

## Governed access requirements

```text
MARKET_BAR_PROVIDER =
ALPACA

MARKET_BAR_FEED =
SIP

FEED_PARAMETER =
EXPLICIT_feed=sip

GOVERNED_STUDY_WINDOW =
2024-09-03 THROUGH 2026-08-31 INCLUSIVE

FROZEN_PRIMARY_UNIVERSE_COUNT =
30

FROZEN_PRIMARY_UNIVERSE_SHA256 =
78ec113c5b83ce03477c1529f80c6104819d7f3a70813dec6125fc24cdf8ade7

REQUIRED_RAW_MARKET_BAR_FIELDS =
SOURCE_TIME
OPEN
HIGH
LOW
CLOSE
VOLUME

OPTIONAL_WHEN_PROVIDER_SUPPLIES =
TRADE_COUNT
VWAP

CANONICAL_HOURLY_GRID =
09:30_AMERICA_NEW_YORK_ANCHORED
HALF_OPEN_INTERVALS
FINAL_INTERVAL_CAPPED_AT_OFFICIAL_SESSION_CLOSE
```

Native provider 1Hour bars are not predeclared to satisfy the accepted
canonical hourly grid. Later verification must establish access to source
granularity sufficient to construct the accepted canonical representation.

## Frozen-universe identity safety

```text
CERTIFICATE_RAW_SYMBOL_IS_AUTOMATIC_FORMATION_TICKER =
NO

PROVIDER_QUERY_IDENTITY_SOURCE =
ALREADY_ACCEPTED_CERTIFICATION_OR_PROVENANCE_EVIDENCE_ONLY

NEW_UNIVERSE_RESEARCH =
PROHIBITED

CASE_RECLASSIFICATION =
PROHIBITED

SECURITY_REPLACEMENT =
PROHIBITED

BACKFILL =
PROHIBITED

CURRENT_STATE_BACKCASTING =
PROHIBITED

FAIL_CLOSED =
YES

REQUIRED_UNIVERSE_COVERAGE_VERIFIED =
NO

RETURN_TO_MANAGING =
YES
```

Certificate raw symbols must not be blindly submitted as provider ticker
identifiers. Provider query symbols and share-class notation must be resolved
only from already accepted certification or provenance evidence.

If provider-query identity cannot be established for a frozen security, access
verification must fail closed and return to Managing.

## Recording-transaction boundary

```text
PROVIDER_ACCESS_PERFORMED =
NO

ACCOUNT_AUTHENTICATION_PERFORMED =
NO

MARKET_DATA_RETRIEVED =
NO

PAID_PURCHASE_PERFORMED =
NO

DATA_ACCESS_AUTHORIZED =
NO__PENDING_ESTABLISHMENT_AND_ACCEPTANCE

C7_AUTHORIZED =
NO

DATASET_GENERATION_STARTED =
NO

FEATURE_GENERATION_STARTED =
NO

MODEL_WORK_STARTED =
NO

FINAL_HOLDOUT_ACCESSED =
NO
```

This authorization-recording transaction creates no provider-access evidence.
Provider/account authentication, entitlement inspection, and minimal test
retrieval necessary to establish access may occur only after this authorization
is canonically recorded.

## Permanent J2 document-role boundary

PROJECT_CONTEXT.md remains the controlling source of truth for broad current
lifecycle state, authorization boundaries, current non-authorization state,
and authoritative pointers to material decisions.

This material decision record is authoritative authorization evidence but is
not a second current-state controller.

The Milestone Review Reference Map and Future Validation and Training Reference
Map remain non-authorizing references. README remains non-authorizing project
orientation.

```text
PROJECT_CONTEXT_CURRENT_STATE_CONTROL =
YES

DECISION_RECORD_CURRENT_STATE_CONTROL =
NO

CURRENT_CHECKPOINT_TRACKER =
NONE

FOURTH_GOVERNANCE_CONTROLLER_CREATED =
NO
```
