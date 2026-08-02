# C2 Canonical Repository Skeleton and Boundaries

## Scope

C2 establishes a documentation-only canonical Python package skeleton and an evidence-grounded migration-preparation plan. It does not migrate executable historical source, select an environment or provider, create a dataset, train or validate a model, access the final holdout, connect to a broker, or authorize trading.

`PROJECT_CONTEXT.md` remains the sole controlling source of current lifecycle state and authorization. This document defines technical responsibility boundaries only and grants no independent authority.

## Canonical Package and Subsystems

The canonical package root is `src/quantitative_trading_research`.

| Subsystem | Canonical purpose |
|---|---|
| `config` | Versioned configuration, environment, path, and identity boundaries |
| `data` | Provider-neutral acquisition, schema, calendar, reconstruction, preparation, and dataset-contract responsibilities |
| `features` | Deterministic, leakage-aware feature definitions and transformations |
| `models` | Model-family implementation, training, and inference responsibilities after later authorization |
| `evaluation` | Chronological evaluation, diagnostics, candidate evidence, and comparison responsibilities |
| `artifacts` | Immutable manifests, checksums, serialization, publication, and run identity |
| `execution` | Broker-neutral decisions, execution plans, risk controls, reconciliation, and later adapter boundaries |
| `tests` | Offline, deterministic, credential-free verification of canonical contracts |

Only subsystem responsibility documents and empty package markers are created during C2.

## Responsibility Boundaries

`config` owns configuration and identity definitions but does not acquire data, train models, evaluate candidates, or submit orders.

`data` owns provider-neutral data contracts and transformations but does not select providers, accept datasets, define model behavior, or access the final holdout without later authorization.

`features` owns feature definitions, ordering, timing, and deterministic transformation requirements but does not fit on validation or holdout data.

`models` owns future model-family implementation boundaries but does not select datasets, perform candidate promotion, or control execution.

`evaluation` owns future evaluation and comparison evidence but does not mutate training inputs, select providers, or submit orders.

`artifacts` owns immutable identity, serialization, manifest, checksum, and publication responsibilities but does not decide model quality or trading authorization.

`execution` owns future broker-neutral decision and safety contracts. It does not authorize connectivity, submission, paper trading, or live trading.

`tests` owns offline verification and may not become an alternate runtime or integration pathway.

## Dependency Direction

The intended dependency direction is:

1. `config` supplies validated configuration and identity inputs.
2. `data` consumes configuration and produces governed data-contract outputs.
3. `features` consumes governed data outputs and produces versioned feature outputs.
4. `models` consumes configuration, data, and feature contracts.
5. `evaluation` consumes frozen model outputs and immutable evidence packages.
6. `artifacts` supplies cross-cutting identity and publication contracts without owning research or execution decisions.
7. `execution` may consume separately qualified and frozen decision artifacts but must not be imported by research, training, or evaluation code.
8. `tests` mirror these boundaries using offline fixtures and mocks.

Reverse dependencies that allow configuration, data, features, models, or evaluation to depend on broker implementations are prohibited.

## Provider and Broker Boundaries

No market-data provider, feed, entitlement, brokerage platform, execution venue, account, credential, or authenticated access path is accepted during C2.

Future C4 work may consider provider-neutral contracts, mocked adapters, offline fixtures, and provisionally identified provider-specific assets only under separate authorization. Provider selection, entitlement verification, network access, market-data requests, and operational acceptance remain C5 or later.

Broker connectivity, order submission, paper trading, and live trading remain prohibited. Future execution components must preserve one submission authority, idempotent intent identity, fail-closed state checks, reconciliation, and confirmed flattening.

## Prohibited Coupling

The canonical design prohibits:

- import-time execution or network activity;
- hidden provider, broker, credential, or filesystem assumptions;
- model code that acquires data or submits orders;
- execution code embedded in feature, model, or evaluation modules;
- validation or selection logic that accesses the shared final holdout early;
- preprocessing fitted outside the training boundary;
- silent imputation, calendar substitution, or dataset acceptance;
- mutable or unchecksummed artifact and run identity;
- provider-specific behavior presented as provider-neutral;
- operational success presented as economic qualification;
- historical implementation presented as canonical without later verification.

## Future Phase Assignments

- C3: Python, dependency, environment, import, lock, and reproducible CI reconstruction.
- C4: selected-code migration, adaptation, reimplementation, and offline verification.
- C5: provider, feed, entitlement, calendar, and initial-universe decisions.
- C6: dataset, feature, split, leakage, and reconstruction contract freeze.
- C7: dataset generation and acceptance.
- C8: PPO v2 implementation readiness.
- C9: PPO qualification and freeze.
- C10: Random Forest gate development and validation.
- C11: XGBoost gate development and validation.
- C12: shared untouched final holdout and promotion decision.
- C13: publication release.
- C14: controlled paper trading.
- C15: live-trading consideration.

Every phase requires separate authorization. A proposed destination, migration wave, or future responsibility is not authorization.

## Future Verification Requirements

Future implementation must verify immutable source attribution, deterministic behavior, exact input and output contracts, chronological and leakage-safe processing, environment reproducibility, artifact and run identity, offline isolation, provider and broker boundaries, fail-closed behavior, and explicit rejected, inconclusive, or no-candidate outcomes.

C3 and C4 planning details and unresolved evidence limitations are maintained in `docs/migration/C2_migration_disposition_plan.yaml`.

## Non-Execution Confirmation

C2 created no executable subsystem implementation. Package markers are empty. No canonical or historical project module was imported or executed. No environment, dependency, provider, network, market-data, dataset, model, holdout, broker, order, paper-trading, or live-trading activity occurred.
