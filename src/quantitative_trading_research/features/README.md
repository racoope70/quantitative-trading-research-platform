# Features Subsystem

## Canonical Responsibility

Own deterministic feature definitions, ordering, timing, windowing, dtype, provenance, and leakage-safe transformation responsibilities.

## Permitted Future Contents

- Pure feature formulas and transformations after later authorization.
- Versioned feature manifests and deterministic output ordering.
- Offline tests using synthetic or separately accepted fixtures.

## Prohibited Coupling

Do not acquire data, select datasets, fit preprocessing on validation or holdout observations, train models, rank candidates, or submit orders.

## Dependency Direction

Features may consume validated configuration and governed data contracts. Features must not depend on models, evaluation, or execution.

## Responsible Future Phase

C4 may prepare selected feature implementation. C6 governs final feature timing, leakage, and dataset-contract acceptance.

## Required Future Verification

- Verify exact formula and timing semantics.
- Verify chronological and no-lookahead behavior.
- Verify deterministic identities and output ordering.
