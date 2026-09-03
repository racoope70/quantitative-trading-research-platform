# C5 Calendar, Cost, and Regime Decision

```text
document_status = ACCEPTED_C5_CALENDAR_COST_REGIME_RECORD
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

This record preserves the accepted C5 decisions that close the bounded
calendar/session/timestamp, spreads-and-expected-costs, and regime-diversity
decision-coverage gaps identified by the C5 exit-readiness audit.

This record supplies substantive C5 decision evidence only.

It does not:

- purchase, subscribe to, authenticate to, or access provider data;
- create a provider account or entitlement;
- construct actual historical-universe membership;
- generate or accept a dataset;
- define or freeze a C6 dataset contract;
- authorize C6;
- authorize model training, validation, backtesting, or final-holdout access;
  or
- declare C5 lifecycle completion.

`PROJECT_CONTEXT.md` remains the controlling source for broad current lifecycle
state and authorization boundaries.

## 2. Calendar, session, and timestamp decision

### 2.1 Authoritative exchange-session boundaries

The canonical research calendar follows the applicable official U.S.
cash-equity exchange calendar for securities primary-listed on NYSE,
NYSE American, and Nasdaq.

```text
CANONICAL_REGULAR_SESSION =
OFFICIAL U.S. CASH-EQUITY CORE / REGULAR SESSION
FOR NYSE, NYSE AMERICAN, AND NASDAQ
WITH OFFICIAL HOLIDAY AND EARLY-CLOSE OVERRIDES

EXCHANGE_LOCAL_TIMEZONE =
America/New_York

REGULAR_SESSION_OPEN =
09:30 America/New_York

REGULAR_SESSION_CLOSE =
16:00 America/New_York ON NORMAL SESSIONS
WITH OFFICIAL EXCHANGE EARLY-CLOSE TIME OVERRIDING 16:00

HOLIDAY_RULE =
USE APPLICABLE OFFICIAL EXCHANGE TRADING CALENDAR

NON_TRADING_SESSION_RULE =
WEEKENDS, FULL-DAY EXCHANGE HOLIDAYS, AND OTHER OFFICIALLY CLOSED
SESSIONS ARE EXCLUDED;
DO NOT CREATE SYNTHETIC REGULAR-SESSION BARS

EARLY_CLOSE_RULE =
PRESERVE OFFICIAL PUBLISHED EARLY CLOSE;
DO NOT EXTEND TO 16:00

EXTENDED_HOURS =
EXCLUDED
```

Official exchange session boundaries and official holiday or early-close
designations are authoritative inputs.

Provider-specific bar boundaries or default calendars must not override those
authoritative exchange-session rules.

### 2.2 DST and internal timestamp representation

```text
DST_RULE =
CONSTRUCT SESSION IN America/New_York FIRST,
THEN CONVERT THAT DATE'S INSTANTS TO UTC;
DO NOT USE A FIXED UTC OFFSET

INTERNAL_TIMESTAMP_STANDARD =
TIMEZONE-AWARE UTC INSTANTS INTERNALLY
WHILE PRESERVING EXCHANGE-LOCAL SESSION DATE / CALENDAR IDENTITY
```

DST is therefore resolved through the exchange-local IANA timezone and
official session date before UTC conversion.

The platform must not encode regular-session times as permanently fixed UTC-5
or UTC-4 offsets.

### 2.3 Provider-neutral hourly-bar representation

The exchanges establish the authoritative session boundaries.

The following interval representation is an internal provider-neutral research
standard and is not attributed to the exchanges:

```text
HOURLY_BAR_ANCHOR =
09:30 America/New_York

HOURLY_BAR_INTERVAL_SEMANTICS =
HALF-OPEN [START, END),
NOMINAL 60-MINUTE WIDTH,
END CAPPED AT OFFICIAL SESSION CLOSE

CANONICAL_BAR_TIMESTAMP =
OPEN_TIME / INTERVAL_START,
NORMALIZED INTERNALLY TO UTC

PARTIAL_FINAL_REGULAR_SESSION_BAR_RULE =
PRESERVE FINAL TRUNCATED BAR THROUGH OFFICIAL SESSION CLOSE;
DO NOT DROP, PAD TO 60 MINUTES, OR CROSS SESSION BOUNDARY
```

For a normal 09:30-16:00 regular session:

```text
09:30-10:30
10:30-11:30
11:30-12:30
12:30-13:30
13:30-14:30
14:30-15:30
15:30-16:00
```

The final interval is intentionally shorter than 60 minutes because the
official session closes at 16:00.

For an official 13:00 early close:

```text
OFFICIAL_SESSION_CLOSE =
13:00 America/New_York

FINAL_BAR =
12:30-13:00
```

Do not synthesize a `13:00-13:30` interval, extend the final bar beyond the
official close, or cross a session boundary.

### 2.4 Formation alignment

The accepted historical-universe timing decision remains unchanged.

```text
FORMATION_OPEN_ALIGNMENT =
MONTHLY FORMATION AT THE OPEN OF THE FIRST ACCEPTED REGULAR SESSION

FORMATION_INFORMATION_CUTOFF =
ONLY INFORMATION AVAILABLE THROUGH
THE IMMEDIATELY PRECEDING COMPLETED REGULAR SESSION
```

Formation therefore occurs at the accepted regular-session open and does not
use formation-morning information that became available after the immediately
preceding completed regular session.

### 2.5 Exchange-calendar divergence rule

```text
NYSE_NYSE_AMERICAN_NASDAQ_CALENDAR_CONFLICT =
NO MATERIAL SCHEDULED CONFLICT IDENTIFIED
FOR THE ACCEPTED STUDY WINDOW

SEPARATE_EXCHANGE_CALENDAR_POLICY =
PRESERVE OFFICIAL EXCHANGE-SPECIFIC CALENDARS AS AUTHORITATIVE INPUTS;
IF A MATERIAL AUTHORITATIVE DIVERGENCE EXISTS,
THE SECURITY'S PRIMARY-LISTING EXCHANGE CONTROLS
```

The accepted study does not require different normal hourly-bar grids merely
because securities are primary-listed on different eligible exchanges.

Official exchange-specific calendars must nevertheless remain available as
authoritative inputs so a material divergence is not silently discarded.

## 3. Spreads and expected costs

C5 explicitly evaluates spreads and expected costs without creating an
unsupported bid-ask-spread threshold.

```text
UNIVERSE_ELIGIBILITY =
NO SEPARATE HARD BID-ASK-SPREAD THRESHOLD
AND
NO SEPARATE EXPECTED-EXECUTION-COST THRESHOLD

ACCEPTED_C5_LIQUIDITY_SCREEN =
MEDIAN_60_SESSION_DOLLAR_VOLUME >= USD 20,000,000

ROLE_OF_LIQUIDITY_SCREEN =
COARSE EX-ANTE TRADABILITY / LIQUIDITY FILTER,
NOT A COMPLETE MEASURE OF BID-ASK SPREAD OR EXECUTION COST

SPREADS_AND_EXPECTED_COSTS =
OBSERVED / REPORTED DIAGNOSTICS WHEN SUITABLE DATA ARE AVAILABLE,
NOT C5 SECURITY-ELIGIBILITY QUOTAS

SPREAD_THRESHOLD_REQUIRED =
NO

EXPECTED_COST_THRESHOLD_REQUIRED =
NO

NEW_PAID_DATA_DEPENDENCY_REQUIRED_FOR_C5 =
NO
```

Higher trading activity can support liquidity, while bid-ask spread is another
material liquidity and transaction-cost dimension.

The accepted USD 20 million median-dollar-volume threshold must therefore not
be interpreted as proving that bid-ask-spread or execution-cost risk has been
fully controlled.

At the same time, C5 has no scientific basis for inventing an arbitrary
security-level spread threshold without the order-size, quote, depth,
volatility, market-condition, and execution-context assumptions required to
interpret it.

The C5 hard eligibility rule remains the accepted liquidity screen.

Spreads and expected costs remain scientifically relevant diagnostics rather
than additional C5 universe quotas.

The later execution boundary is:

```text
FUTURE_EXECUTION_COST_MODEL =
SCIENTIFICALLY_REQUIRED WHEN THE APPLICABLE LATER
BACKTEST / VALIDATION WORK IS SEPARATELY AUTHORIZED

CURRENT_EXECUTION_AUTHORIZATION_EFFECT =
NONE
```

This future scientific requirement is not current authorization to design,
fit, execute, or validate a backtest cost model.

## 4. Regime diversity

C5 distinguishes cross-sectional security selection from market conditions
that vary through time.

```text
CROSS_SECTIONAL_UNIVERSE_DIVERSITY =
DO NOT USE MARKET REGIME AS A SECURITY-LEVEL ELIGIBILITY FILTER OR QUOTA

TIME_SERIES_MARKET_REGIME_COVERAGE =
OBSERVED PROPERTY OF THE HISTORICAL STUDY PERIOD
AND A LATER CHRONOLOGICAL VALIDATION CONSIDERATION

REGIME_QUOTA =
NONE

REGIME_ELIGIBILITY_FILTER =
NONE

REGIME_DIVERSITY_OBSERVED_PROPERTY =
YES
```

`REGIME_DIVERSITY_OBSERVED_PROPERTY = YES` means regime diversity is
designated for observation or reporting when the applicable later work is
authorized.

It does not claim that regime composition has already been empirically
measured.

A market regime is a condition across time, such as:

- volatility state;
- trend state;
- market stress; or
- liquidity state.

It is not an intrinsic security attribute equivalent to security type,
primary-listing exchange, price eligibility, or stable security identity.

The research design must therefore not mix:

```text
WHICH SECURITIES ARE IN THE CROSS-SECTION
```

with:

```text
WHICH MARKET CONDITIONS OCCUR THROUGH TIME
```

The existing universe-diversity decision remains:

```text
SECTOR_OR_OTHER_DIVERSITY_RULE =
NO EXPLICIT SECTOR, INDUSTRY, MARKET-CAP, OR OTHER DIVERSITY QUOTA
```

No future validation folds, regime labels, dataset splits, qualification
criteria, or model rules are defined by this C5 decision.

Those remain later-phase scientific decisions only when separately authorized.

## 5. Material evidence basis

This record summarizes already-completed bounded C5 research and preserves the
material authoritative evidence basis without reopening broad provider or
market-structure research.

Authoritative calendar and session evidence includes:

- NYSE Trading Information:
  <https://www.nyse.com/trade/trading-information>
- NYSE 2024 Trading Calendar:
  <https://www.nyse.com/publicdocs/ICE_NYSE_2024_Yearly_Trading_Calendar.pdf>
- NYSE 2025 Trading Calendar:
  <https://www.nyse.com/publicdocs/ICE_NYSE_2025_Yearly_Trading_Calendar.pdf>
- NYSE 2026 Trading Calendar:
  <https://www.nyse.com/publicdocs/nyse/ICE_NYSE_2026_Yearly_Trading_Calendar.pdf>
- Nasdaq Stock Market trading-hours and holiday information:
  <https://www.nasdaq.com/market-activity/stock-market-holiday-schedule>
- NasdaqTrader U.S. Equity and Options Markets Holiday Schedule:
  <https://www.nasdaqtrader.com/trader.aspx?id=Calendar>

Material spreads, liquidity, and execution-cost evidence includes:

- U.S. Securities and Exchange Commission,
  Report on the Comparison of Order Executions Across Equity Market
  Structures:
  <https://www.sec.gov/news/studies/ordrxmkt.htm>
- FINRA material discussing trading volume, liquidity, bid-ask spreads, and
  transaction-cost implications:
  <https://syndication.finra.org/content/understanding-disclosure-documents>
- FINRA, Answers to 6 Common Questions About Online Trading:
  <https://www.finra.org/investors/insights/questions-about-online-trading>

The exchange materials establish authoritative market-session and
holiday/early-close boundaries.

The half-open hourly interval representation, UTC-normalized internal
timestamp standard, and truncated-final-bar convention are provider-neutral
platform design decisions built on those authoritative boundaries.

The SEC and FINRA materials support the distinction between trading liquidity,
quoted spreads, effective or realized execution costs, and broader transaction
costs.

They do not establish or imply a project-specific spread or expected-cost
eligibility threshold.

## 6. C5 decision-coverage and authorization boundary

```text
CALENDAR_GAP_STATUS =
RESOLVED

SPREADS_EXPECTED_COSTS_GAP_STATUS =
RESOLVED

REGIME_DIVERSITY_GAP_STATUS =
RESOLVED

MATERIAL_UNRESOLVED_C5_ITEMS =
NONE_AT_CURRENT_DECISION_COVERAGE_LEVEL
```

These findings close the bounded decision-coverage gaps identified by the C5
exit-readiness audit.

They do not independently declare the C5 lifecycle complete.

This record supplies substantive evidence for a subsequent C5 exit-readiness
audit or review only.

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

dataset_contract_freeze =
NONE

model_or_backtest_execution_authorization =
NONE

C6_authorization =
NONE
```

No provider purchase, account activity, authentication, market/reference-data
acquisition, actual universe construction, dataset generation, C6 contract
freeze, model work, backtesting, validation execution, final-holdout access,
paper trading, or live trading is authorized by this decision.
