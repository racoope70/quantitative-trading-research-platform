# Canonical Test Responsibilities

## Canonical Responsibility

Own deterministic, offline, credential-free verification of canonical contracts without becoming an alternate runtime, integration, provider, model-training, or trading pathway.

## Permitted Future Contents

- Unit, contract, schema, property, parity, failure-injection, and import-smoke tests after the responsible phase is authorized.
- Synthetic fixtures, mocks, and separately accepted immutable test packages.
- Checks for prohibited side effects, identity mismatches, leakage, and boundary violations.

## Prohibited Coupling

Do not access networks, credentials, providers, brokers, market data, accepted datasets, the final holdout, model training, order submission, paper trading, or live trading unless a later phase explicitly authorizes the exact activity.

## Dependency Direction

Tests may mirror authorized subsystem dependencies using mocks and fixtures. Test helpers must not introduce hidden production behavior or bypass canonical boundaries.

## Responsible Future Phase

C3 governs environment, import, and reproducible CI checks. C4 governs selected offline subsystem tests. Later tests follow their responsible phase.

## Required Future Verification

- Verify tests are deterministic and offline.
- Verify fixtures have explicit identity and scope.
- Verify prohibited activity fails closed rather than being silently skipped or performed.
