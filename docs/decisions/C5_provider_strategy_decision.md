# C5 Provider Strategy Decision

```text
document_status = ACCEPTED_C5_PROVIDER_STRATEGY_RECORD
document_role = SUBSTANTIVE_C5_DECISION_EVIDENCE
authorization_effect = NONE
current_state_control = NO
provider_purchase_authorization_effect = NONE
provider_account_authorization_effect = NONE
market_data_acquisition_authorization_effect = NONE
dataset_generation_authorization_effect = NONE
scientific_host_authorization_effect = NONE
C6_authorization_effect = NONE
CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Purpose

This record preserves the settled C5 provider strategy so future work does
not repeat the completed provider research.

It records decision-quality conclusions within the already-authorized C5
Data Source, Calendar, and Initial Universe Decision scope.

It does not authorize provider purchases, provider accounts, authentication,
market-data acquisition, dataset generation, scientific-host qualification
or purchase, C6, model work, final-holdout access, paper trading, or live
trading.

`PROJECT_CONTEXT.md` remains the controlling source for broad current
lifecycle state and authorization boundaries.

## 2. Provider-neutral architecture

```text
PROVIDER_NEUTRAL_INTERNAL_SCHEMA = ACCEPTED
PROVIDER_SPECIFIC_ADAPTER_BOUNDARY = ACCEPTED
PROVIDER_SPECIFIC_PROVENANCE_REQUIRED = YES
LOWEST_COMMON_DENOMINATOR_SCHEMA = NOT_ACCEPTABLE
```

Provider-neutral means downstream software reuse. It does not mean
observations from different providers are scientifically interchangeable.

Material source semantics must be preserved where applicable, including:

- provider and dataset/feed;
- publisher or venue scope;
- identifier namespace;
- timestamp and bar semantics;
- raw/adjusted lineage;
- corporate-action and reference snapshot;
- revision or as-of state;
- retrieval timestamp;
- checksum; and
- license or entitlement lineage.

If the canonical source changes materially later:

```text
CANONICAL_DATASET_REBUILD = YES
AFFECTED_TRAINING_VALIDATION_BACKTEST_RERUN = YES
```

The platform must not be hard-coded around Alpaca, Sharadar, Databento,
CRSP, or another provider.

## 3. Alpaca provisional market-bar role

```text
CURRENT_WORKING_MARKET_BAR_SOURCE = ALPACA_PROVISIONAL
ALPACA_HISTORICAL_MARKET_DATA_ROLE =
LOW_COST_PROVISIONAL_MARKET_BAR_SOURCE

ALPACA_CURRENT_ELIGIBLE_HISTORICAL_COST =
APPROXIMATELY_0_USD
```

Alpaca remains potentially useful for historical bars, later paper-trading
feed work when separately authorized, and provider-specific adapter work.

Alpaca is rejected as the sole point-in-time historical reference source:

```text
ALPACA_SOLE_PIT_REFERENCE_SOURCE = REJECTED
ALPACA_POINT_IN_TIME_UNIVERSE_RECONSTRUCTION = FAIL
ALPACA_SURVIVORSHIP_BIAS_CONTROL = FAIL
ALPACA_REPRODUCIBILITY_FIT_FOR_PIT = FAIL
```

Provider coverage or missingness must remain separate from historical
security eligibility.

## 4. Sharadar low-cost PIT path

```text
CURRENT_WORKING_PIT_REFERENCE_PATH =
SHARADAR_PRICES_5_YEAR_WHEN_NEEDED

SHARADAR_POINT_IN_TIME_FIT =
PASS_WITH_BOUNDARIES

SHARADAR_PIT_CORE =
TICKERS
+
ACTIONS
```

The reviewed core provides the relevant point-in-time reference capabilities
for the contemplated study, including:

- active and delisted securities;
- dated listing events;
- dated delisting events;
- historical ticker changes;
- stable permaticker identity;
- acquisitions; and
- terminal events.

The reviewed depth is sufficient for the contemplated approximately 720-day
study.

Decision-time reviewed pricing:

```text
SHARADAR_PRICES_5_YEAR_COST =
9_USD_PER_MONTH
OR
99_USD_PER_YEAR

SHARADAR_MONTHLY_MINIMUM_TERM =
ONE_MONTH
```

The current cheapest credible working path is:

```text
ALPACA_HISTORICAL_BARS
+
SHARADAR_PRICES_5_YEAR_PIT_REFERENCE
```

The current incremental cost when actually needed is approximately USD 9
per month.

## 5. Sharadar enhanced path

The enhanced path is:

```text
ALPACA_HISTORICAL_BARS
+
SHARADAR_FUNDAMENTALS_5_YEAR
```

Decision-time reviewed pricing:

```text
SHARADAR_FUNDAMENTALS_5_YEAR_COST =
19_USD_PER_MONTH
OR
199_USD_PER_YEAR
```

The enhanced tier adds relevant fundamentals/SF1, daily, and events
capabilities.

It must not be selected merely because it exists.

The accepted trigger is:

```text
ENHANCED_PATH_TRIGGER =
ONLY_IF_APPROVED_UNIVERSE_OR_SCIENTIFIC_REQUIREMENTS_REQUIRE
FUNDAMENTALS_SF1_OR_EVENTS_UNAVAILABLE_IN_THE_9_USD_PIT_CORE
```

Whether that trigger is met remains a later C5 determination when the
applicable universe and scientific requirements are concrete.

## 6. Sharadar licensing and retention boundary

Under the currently reviewed terms:

```text
SHARADAR_USE_BOUNDARY =
PERSONAL_NONPROFESSIONAL_USE_UNDER_CURRENTLY_REVIEWED_TERMS

SHARADAR_SOURCE_DATA_RETENTION_AFTER_TERMINATION =
DELETE_WITHIN_30_DAYS

SHARADAR_RECONSTRUCTIVE_EXTRACT_RETENTION_AFTER_TERMINATION =
DELETE_WITHIN_30_DAYS

SHARADAR_NONRECONSTRUCTIVE_DERIVED_OUTPUTS =
MAY_BE_RETAINED_UNDER_CURRENTLY_REVIEWED_TERMS

SHARADAR_RAW_DATA_REDISTRIBUTION =
PROHIBITED
```

Public use and publication must remain within applicable current licensing,
attribution, and redistribution boundaries.

Because commercial and license terms can change, then-current pricing,
licensing, retention, permitted-use, and attribution terms must be rechecked
immediately before any separately authorized purchase, acquisition, or
public use.

## 7. Just-in-time purchase rule

```text
SHARADAR_PURCHASE_NOW = NO

SHARADAR_PURCHASE_TRIGGER =
C5_HISTORICAL_UNIVERSE_CONSTRUCTION_IS_SEPARATELY_AUTHORIZED
AND
READY_TO_EXECUTE
```

The project should not begin a paid entitlement or its retention/deletion
clock before the data has immediate scientific use.

Account creation, subscription, authentication, and acquisition remain
separately bounded actions.

## 8. Deferred stronger provider options

```text
DATABENTO =
SCIENTIFIC_PIT_BENCHMARK_AND_DEFERRED_FUTURE_CANDIDATE

CRSP =
SCIENTIFICALLY_STRONG_FUTURE_OPTION_IF_ACCESS_OR_BUDGET_BECOMES_AVAILABLE
```

Broad provider research should not be reopened absent:

```text
NEW_MATERIAL_SCIENTIFIC_DECISION_VALUE
OR
MATERIAL_BUDGET_CHANGE
OR
NEW_INSTITUTIONAL_ACCESS
```

## 9. Budget principle

```text
CURRENT_BUDGET_CONSTRAINT =
MATERIAL_NEAR_TERM_DECISION_VARIABLE

LONG_TERM_PROVIDER_ARCHITECTURE_CONSTRAINED_BY_CURRENT_BUDGET =
NO
```

The near-term objective is to minimize current cash cost without weakening
point-in-time scientific requirements or creating provider lock-in.

Long-term provider decisions may be reconsidered if scientific decision value,
budget, or institutional access materially changes.

## 10. Scientific-host boundary

Scientific-host purchase remains deferred.

The current workstation remains the development workstation and controlled
Linux VM host.

The lack of a new scientific host does not invalidate provider-neutral
architecture, point-in-time eligibility logic, universe-definition logic,
data contracts, feature definitions, tests, walk-forward mechanics, backtest
mechanics, or current research-platform development.

The accepted revisit trigger is:

```text
SCIENTIFIC_HOST_REVISIT_TRIGGER =
PIPELINE_MATURE
+
LATER_AUTHORIZED_PHASE_REQUIRES_QUALIFIED_CANONICAL_SCIENTIFIC_EXECUTION
+
BUDGET_REVIEW
```

At that future point the then-current CPU/GPU workload, RAM, storage, Linux
compatibility, reproducibility, performance, and local-versus-cloud economics
must be reassessed.

Current hardware assumptions must not be frozen into that future decision.

## 11. Material evidence basis

This record summarizes the already-completed C5 provider research rather than
storing the full research transcript.

Material evidence reviewed for the settled conclusions included applicable
official provider documentation and terms concerning:

- Alpaca historical US-equity market data and feed characteristics;
- Nasdaq Data Link / Sharadar product coverage and decision-time pricing;
- Sharadar TICKERS and ACTIONS point-in-time reference capabilities;
- Sharadar Fundamentals/SF1, daily, and events capabilities;
- Sharadar licensing, permitted use, retention, and redistribution terms;
- Databento historical and reference-data capabilities; and
- CRSP US stock and reference-data capabilities.

## 12. Deferred C5 decisions

This record does not determine:

- the exact historical study window;
- the exact first formation date;
- the exact universe rebalance or reformation cadence;
- the exact provider-neutral dataset contract;
- the exact provenance schema for dataset construction;
- actual security membership; or
- whether the USD 9 Sharadar core ultimately suffices or the USD 19
  enhanced-tier trigger is met.

Those remain bounded C5 items to resolve when their decision value becomes
concrete.

This record does not authorize C6 or any later lifecycle phase.
