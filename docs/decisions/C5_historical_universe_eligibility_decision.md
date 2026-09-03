# C5 Historical Universe Eligibility and PIT Evidence Decision

```text
document_status = ACCEPTED_C5_HISTORICAL_UNIVERSE_ELIGIBILITY_RECORD
document_role = SUBSTANTIVE_C5_DECISION_EVIDENCE
authorization_effect = NONE
current_state_control = NO
current_lifecycle_state = C5_ACTIVE
CURRENT_CHECKPOINT_TRACKER = NONE
provider_account_activity = NONE
market_data_acquisition = NONE
dataset_generation = NONE
actual_security_membership_constructed = NO
C6_authorization = NONE
```

## 1. Purpose

This record preserves the accepted C5 historical-universe scientific
eligibility framework and the point-in-time evidence architecture required to
support it.

The design is accepted at the capability level. This record does not purchase
or acquire NYSE data, authorize an NYSE account or entitlement, construct
actual historical security membership, generate a dataset, authorize C6, or
change current lifecycle state.

It is substantive C5 decision evidence only and is not a current-state
controller.

## 2. Security-type eligibility

```text
SECURITY_TYPE_ELIGIBILITY =
US-INCORPORATED ORDINARY COMMON SHARES ONLY
```

Primary eligible listings are:

- NYSE;
- NYSE American; and
- Nasdaq.

Exclude:

- ETFs;
- ETNs;
- closed-end funds;
- ADRs;
- foreign ordinary shares;
- preferred stock;
- OTC securities at formation;
- warrants;
- rights;
- units;
- SPAC / pre-combination securities; and
- other non-ordinary equity structures.

Separately listed ordinary-common-share classes are evaluated as separate
securities.

No issuer-level quota is imposed.

## 3. Listing and trading eligibility

At each formation cutoff, the security must be point-in-time active and
primary-listed on NYSE, NYSE American, or Nasdaq.

No delisting, acquisition, or other hard terminal event may be effective at or
before the formation open.

Current or survivor-only status must not be used to reconstruct historical
eligibility.

Provider missingness or an Alpaca-specific tradable flag does not establish
security ineligibility.

## 4. History eligibility

The security must have at least 252 completed regular sessions of continuous
eligible exchange-listed history before formation.

Ticker changes or transfers among eligible exchanges do not reset history when
stable security identity is preserved.

```text
MINIMUM_PRE_FORMATION_HISTORY =
252 COMPLETED REGULAR SESSIONS

MINIMUM_VALID_DAILY_PRICE_TRADE_OBSERVATIONS =
240_OF_252
```

Provider-attributed missingness is classified separately from genuine
security ineligibility.

## 5. Price eligibility

Use only completed regular sessions available at the formation cutoff.

```text
IMMEDIATELY_PRECEDING_VALID_CLOSE >= USD 5.00

AND

MEDIAN_PRECEDING_20_AS_TRADED_CLOSES >= USD 5.00

MINIMUM_VALID_OBSERVATIONS =
19_OF_20
```

Do not apply future corporate actions.

## 6. Liquidity eligibility

```text
LIQUIDITY_LOOKBACK =
60 COMPLETED REGULAR SESSIONS

DAILY_DOLLAR_VOLUME =
REGULAR_SESSION_CLOSE
*
REGULAR_SESSION_SHARE_VOLUME

LIQUIDITY_THRESHOLD =
MEDIAN_60_SESSION_DOLLAR_VOLUME >= USD 20,000,000

MINIMUM_VALID_OBSERVATIONS =
57_OF_60
```

Extended-hours observations are excluded.

All observations used for this eligibility criterion and for the later
liquidity ranking must use:

```text
ALPACA_HISTORICAL_STOCK_FEED = SIP
ALPACA_FEED_PARAMETER = EXPLICITLY_PIN_feed=sip
```

IEX and SIP volume must not be mixed.

If required SIP observations are unavailable, classify the condition as
provider missingness rather than substituting IEX volume or zero volume.

## 7. Missingness model

Maintain three distinct states:

```text
ELIGIBLE
INELIGIBLE
UNRESOLVED_PROVIDER_MISSINGNESS
```

Failure may be declared only when point-in-time evidence establishes failure
of an eligibility rule.

Missing provider data must not be interpreted as delisting, zero trading, or
other security ineligibility.

A security whose required fact cannot be resolved cannot be selected for that
formation, but it remains explicitly unresolved rather than failed.

## 8. Corporate-action handling

Stable security identity is the continuity key.

Ticker changes do not reset history.

Non-terminal actions such as stock splits do not create a new security
identity and are applied only when effective.

Acquired, merged-out, delisted, or otherwise terminated securities are removed
when the terminal event becomes effective.

```text
MID_CYCLE_BACKFILL = NONE
```

A successor security does not inherit a predecessor's 252-session history
merely because of economic succession.

## 9. Selection rule

After all eligibility rules are applied:

1. rank eligible securities by trailing-60-completed-session median daily
   dollar volume in descending order;
2. select the first 60; and
3. break exact ties by stable security identifier ascending, with identifier
   namespace preserved.

Do not use:

- future returns;
- current survivor status;
- sector quotas;
- market-cap ranking; or
- random resampling.

## 10. Underfilled-universe rule

```text
60_OR_MORE =
SELECT_EXACTLY_60

50_TO_59 =
SELECT_ALL_ELIGIBLE
WITHOUT_RELAXING_THRESHOLDS

BELOW_50 =
UNDERFILLED_BELOW_ACCEPTED_RANGE
AND
RETURN_FOR_REVIEW_BEFORE_UNIVERSE_CONSTRUCTION_PROCEEDS
```

Mid-cycle terminal-event removals remain subject to the accepted no-backfill
rule even if active membership temporarily falls below 50.

## 11. Sector and other diversity

```text
SECTOR_OR_OTHER_DIVERSITY_RULE =
NO EXPLICIT SECTOR, INDUSTRY, MARKET-CAP, OR OTHER DIVERSITY QUOTA
```

Diversity and concentration remain observed properties rather than selection
quotas.

Do not assign historical sector or industry using current Sharadar snapshot
classification as though it were point-in-time evidence.

If a dated PIT sector source is unavailable:

```text
SECTOR_INDUSTRY_CONCENTRATION =
UNESTABLISHED
```

Do not create a paid dependency solely for sector reporting.

## 12. Sharadar PIT evidence role

```text
SHARADAR_9_USD_CORE_SUFFICIENT_FOR_FULL_SCIENTIFIC_RULESET =
NO

SHARADAR_19_USD_TIER_TRIGGERED =
NO

SHARADAR_19_USD_TIER_SOLVES_ALL_MISSING_REQUIREMENTS =
UNESTABLISHED
```

Preserve:

```text
SHARADAR USD 9 TICKERS + ACTIONS
```

for the accepted identity, listing-event, delisting, ticker-change,
acquisition, and terminal-event role.

Current `TICKERS` snapshot metadata must not be backcast as historical truth.

## 13. Security-type PIT evidence

Use dated SEC EDGAR filing / Inline-XBRL security-level evidence available by
the formation cutoff as necessary.

Preserve security-specific filing contexts.

Do not assume Company Facts alone preserves all security-level class/exchange
relationships.

## 14. U.S.-incorporation PIT evidence

Use dated SEC evidence available by the formation cutoff, including
`EntityIncorporationStateCountryCode` where appropriate.

Any reincorporation applies only when effective.

## 15. SPAC / pre-combination PIT evidence

Use dated SEC SPAC/de-SPAC filing evidence available by the formation cutoff.

`EntityShellCompany` may support the classification but is not independently
synonymous with SPAC status.

Preserve pre-combination status until the business combination becomes
effective.

## 16. Historical primary-exchange PIT evidence

```text
PRIMARY_EXCHANGE_SCIENTIFIC_REQUIREMENT_STATUS =
PRESERVE

SEC_SECURITY_EXCHANGE_NAME_ESTABLISHES_PRIMARY_EXCHANGE =
NO

PRIMARY_EXCHANGE_PIT_SOURCE =
NYSE DAILY TAQ MASTER

PRIMARY_EXCHANGE_FIELD =
Listed Exchange

PRIMARY_EXCHANGE_FIELD_SEMANTICS =
LISTING EXCHANGE / PRIMARY LISTING MARKET

PRIMARY_EXCHANGE_MARKET_COVERAGE =
CONSOLIDATED CTA + UTP

PRIMARY_EXCHANGE_HISTORY =
1993_TO_PRESENT
```

At each formation, use qualifying dated historical NYSE Daily TAQ Master
evidence available at the cutoff to establish the security's primary listing
market.

If the required security record or primary-listing field cannot be
established:

```text
PRIMARY_EXCHANGE_REQUIREMENT =
UNRESOLVED_PROVIDER_MISSINGNESS
```

Do not infer primary listing from:

- current Sharadar exchange metadata;
- trading venue;
- SEC exchange registration alone; or
- where most trading volume occurred.

## 17. Known valid capability path

```text
LOWEST_COST_KNOWN_VALID_COMBINED_PATH =

SHARADAR USD 9 TICKERS + ACTIONS
+
ALPACA HISTORICAL SIP BARS WITH EXPLICIT feed=sip
+
DATED SEC EDGAR / INLINE-XBRL PIT EVIDENCE
+
HISTORICAL NYSE DAILY TAQ MASTER PRIMARY-LISTING EVIDENCE

KNOWN_VALID =
CAPABILITY_DESIGN_LEVEL
```

`KNOWN_VALID = CAPABILITY_DESIGN_LEVEL` does not mean:

```text
PURCHASED
ACQUIRED
AFFORDABILITY_ACCEPTED
AUTHORIZED_FOR_EXECUTION
```

## 18. NYSE cost and authorization boundary

The currently reviewed published commercial Daily TAQ back-history schedule
is:

```text
FIRST_12_DATA_CONTENT_MONTHS =
USD 3,800 PER DATA-CONTENT MONTH

ADDITIONAL_BACK_HISTORY =
USD 500 PER ADDITIONAL DATA-CONTENT MONTH
```

The accepted study window remains 2024-09-03 through 2026-08-31
inclusive. Because each scheduled formation uses information through the
immediately preceding completed regular session, the historical NYSE Master
content months required to support the 24 scheduled formations are
approximately:

```text
REQUIRED_NYSE_HISTORICAL_CONTENT_MONTH_RANGE =
AUGUST_2024_THROUGH_JULY_2026

REQUIRED_NYSE_HISTORICAL_CONTENT_MONTH_COUNT =
24
```

This required content-month range is distinct from the study-window month
labels.

Under the reviewed published commercial back-history schedule, 24 required
content months imply approximately:

```text
APPROXIMATE_24_MONTH_PUBLISHED_COMMERCIAL_BACK_HISTORY_COST =
USD 51,600

CALCULATION =
12 * USD 3,800
+
12 * USD 500
=
USD 51,600
```

This is not a current quote and is not an approved budget or committed project
expenditure.

```text
THIS_IS_NOT_A_CURRENT_QUOTE =
YES

ACADEMIC_OR_OTHER_APPLICABLE_PRICING =
UNESTABLISHED_PENDING_THEN_CURRENT_NYSE_QUOTE

NYSE_PURCHASE_AUTHORIZATION =
NONE

NYSE_ACCOUNT_OR_ACCESS_AUTHORIZATION =
NONE

NYSE_DATA_ACQUISITION_AUTHORIZATION =
NONE

THEN_CURRENT_PRICE_AND_LICENSE_RECHECK_REQUIRED_BEFORE_ANY_PURCHASE =
YES

FUTURE_OWNER_DECISION_REQUIRED_BEFORE_PURCHASE_OR_ACCOUNT_ACTIVITY =
YES
```

## 19. Authorization boundaries

```text
current_lifecycle_state =
C5_ACTIVE

CURRENT_CHECKPOINT_TRACKER =
NONE

provider_account_activity =
NONE

market_data_acquisition =
NONE

dataset_generation =
NONE

actual_security_membership_constructed =
NO

C6_authorization =
NONE
```

This decision record does not authorize provider-account activity,
authentication, subscription or purchase activity, market or reference data
acquisition, historical-universe construction, dataset generation, C6,
training, or final-holdout access.

`PROJECT_CONTEXT.md` remains the controlling source for broad current lifecycle
state and authorization boundaries.

## 20. Material evidence basis

The accepted conclusions in this record summarize already-completed C5
capability research using authoritative documentation, as applicable,
including:

- the current NYSE Daily TAQ product/client specification establishing the
  Master file and `Listed Exchange` / Primary Listing Market semantics;
- NYSE Daily TAQ product documentation establishing consolidated CTA/UTP
  coverage, historical depth, and historical access;
- the reviewed NYSE historical market-data pricing documentation;
- Alpaca historical U.S.-equity stock-data/feed documentation establishing SIP
  versus IEX feed semantics;
- SEC EDGAR / Inline-XBRL documentation supporting dated security-level and
  incorporation evidence; and
- Sharadar / Nasdaq Data Link documentation supporting the previously accepted
  `TICKERS + ACTIONS` PIT role.

Commercial and provider terms can change. Pricing, licensing, entitlement,
permitted-use, and access terms must therefore be checked again before any
separately authorized provider transaction.
