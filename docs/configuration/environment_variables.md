# C3 Environment-Variable Contract

## Scope

This document records the C3 environment-variable boundary only. It does not
authorize provider, broker, market-data, account, order, model, dataset, or
trading behavior.

## Active C3 Variables

```text
active_required_nonsecret_variables = NONE
active_optional_nonsecret_variables = NONE
canonical_C3_settings_environment_consumption = NONE
```

Canonical C3 settings are constructed only from an explicit typed in-memory
mapping. Importing the package or either C3 configuration module must not read
the process environment, a dotenv file, a configuration file, the filesystem,
or the network.

## Secret References Retained for Later Phases

The following historical names are recorded only as deferred secret
references:

```text
APCA_API_KEY_ID
APCA_API_SECRET_KEY
```

They are not a canonical C3 secret interface. C3 code, diagnostics, tests, and
offline execution must not consume, validate, print, persist, or transmit them.

## Provider-Specific Deferred Variables

```text
APCA_API_BASE_URL
BARS_FEED
```

These remain deferred. Their presence does not authorize provider access,
broker access, entitlement inspection, market-data retrieval, or any
operational API activity.

## Later-Phase Deferred Variables

```text
RUN_VERSION
CONFIG_CHANGES
REASON_FOR_CHANGE
TICKERS
DATA_TIMEFRAME
TRAIN_TIMEFRAME
EQUITY_TIMEFRAME
```

These names remain documentary historical evidence only. C3 does not consume
them and does not migrate the historical environment contract.

## Prohibited C3 Environment Content

C3 must not accept environment variables that configure or expose:

- Credentials, tokens, secrets, cookies, authorization headers, or private
  package indexes.
- Proxies, trusted-host bypasses, alternate indexes, mirrors, find-links
  locations, or editable dependency paths.
- Provider, broker, feed, account, entitlement, market-data, dataset, feature,
  label, model, evaluation, final-holdout, order, position, risk, execution, or
  trading behavior.
- Runtime application behavior or historical Alpaca execution controls.

The network-denied child environment is constructed from an empty base and an
exact nonsecret allowlist required by the launcher. No raw parent environment
is inherited.

## Import and Side-Effect Boundary

The following imports must be deterministic and side-effect free:

```text
quantitative_trading_research
quantitative_trading_research.config
quantitative_trading_research.config.settings
quantitative_trading_research.config.environment_diagnostics
```

Importing them must not:

- Read environment variables.
- Read or write configuration files.
- Create directories or artifacts.
- Open sockets or resolve hostnames.
- Contact GitHub, PyPI, a provider, a broker, or a market-data service.
- Inspect accounts, entitlements, datasets, models, final holdouts, orders, or
  trading state.

## Evidence State

```text
environment_variable_contract_status = STATIC_IMPLEMENTATION_COMPLETE
environment_variable_runtime_verification = PASS_GATE_2_LOCAL_ENVIRONMENT_EXCLUSION
CI_environment_exclusion_verification = PENDING_GATE_3_EXECUTION
secret_exposure_result = PASS_NO_SECRET_EXPOSURE_DETECTED_DURING_GATE_2_LOCAL_EXECUTION
```
