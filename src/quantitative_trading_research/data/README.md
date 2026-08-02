# Data Subsystem

## Canonical Responsibility

Own provider-neutral acquisition orchestration, schemas, calendars, expected slots, reconstruction, preparation, provenance, and dataset-contract responsibilities.

## Permitted Future Contents

- Provider-neutral interfaces and offline fixtures after later authorization.
- Versioned schema, calendar, coverage, provenance, and reconstruction contracts.
- Deterministic preparation from immutable dataset and split identities.

## Prohibited Coupling

Do not accept a provider, access a network, request market data, silently impute missing observations, accept a dataset, fit model preprocessing outside the training boundary, or access the final holdout without later authorization.

## Dependency Direction

Data may consume validated configuration and artifact-identity utilities. It must not depend on features, models, evaluation, or execution.

## Responsible Future Phase

C4 may prepare offline data boundaries. C5 governs provider decisions. C6 governs contract freeze. C7 governs generation and acceptance.

## Required Future Verification

- Verify immutable raw and derived identities.
- Verify schema, calendar, expected-slot, coverage, duplicate, missingness, and timestamp behavior.
- Verify no provider or dataset activity occurs outside its authorized phase.
