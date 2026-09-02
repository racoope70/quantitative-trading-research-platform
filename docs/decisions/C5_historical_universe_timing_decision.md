# C5 Historical Universe Timing Decision

```text
document_status = ACCEPTED_C5_HISTORICAL_UNIVERSE_TIMING_RECORD
document_role = SUBSTANTIVE_C5_DECISION_EVIDENCE
authorization_effect = NONE
current_state_control = NO
current_lifecycle_state = C5_ACTIVE
CURRENT_CHECKPOINT_TRACKER = NONE
provider_account_activity = NONE
market_data_acquisition = NONE
dataset_generation = NONE
C6_authorization = NONE
```

## 1. Purpose

This record preserves the accepted C5 historical-universe timing decisions.

It does not change the controlling `C5_ACTIVE` lifecycle state, alter the
settled provider strategy, create a checkpoint tracker, construct historical
security membership, authorize data acquisition or dataset generation, or
authorize C6.

## 2. Accepted timing decisions

```text
HISTORICAL_STUDY_WINDOW =
2024-09-03 THROUGH 2026-08-31 INCLUSIVE

FIRST_FORMATION =
2024-09-03 REGULAR-SESSION OPEN
USING ONLY INFORMATION AVAILABLE THROUGH
2024-08-30 COMPLETED REGULAR SESSION

SCHEDULED_UNIVERSE_REFORMATION =
MONTHLY
AT THE OPEN OF THE FIRST REGULAR SESSION OF EACH CALENDAR MONTH
USING ONLY INFORMATION AVAILABLE THROUGH
THE IMMEDIATELY PRECEDING COMPLETED REGULAR SESSION

TERMINAL_EVENT_REMOVAL_RULE =
REMOVE THE SECURITY FROM THE ACTIVE UNIVERSE
WHEN THE HARD TERMINAL EVENT BECOMES EFFECTIVE

MID_CYCLE_BACKFILL_RULE =
NO MID-CYCLE BACKFILL;
THE VACATED SLOT REMAINS VACANT UNTIL
THE NEXT SCHEDULED MONTHLY REFORMATION
```

## 3. Eligibility-history relationship

The settled 252-completed-regular-session eligibility history precedes
formation as needed.

For the first formation, the required eligibility-history lookback may
therefore extend before the historical study window. That pre-formation
history supports eligibility determination and does not change the accepted
study window.

## 4. Scope and authorization boundary

This timing decision does not construct or select actual security membership.

It does not authorize provider-account activity, market-data acquisition,
dataset generation, or any provider purchase or subscription activity.

The settled C5 provider strategy remains unchanged.

This record has no C6 authorization effect.
