# Execution Subsystem

## Canonical Responsibility

Own future broker-neutral decision, execution-plan, risk, submission-boundary, idempotency, reconciliation, flattening, and broker-evidence responsibilities.

## Permitted Future Contents

- Pure decision, plan, risk, and reconciliation logic using mocks and offline fixtures after later authorization.
- Explicit provider and broker adapter boundaries.
- Fail-closed state validation and immutable intent and execution evidence contracts.

## Prohibited Coupling

Do not connect to a broker, authenticate, submit orders, conduct paper or live trading, or represent a provider-specific implementation as accepted during C2 or C4.

## Dependency Direction

Execution may later consume frozen, qualified decision artifacts and validated configuration. Research, data, feature, model, and evaluation subsystems must not depend on execution.

## Responsible Future Phase

C4 may prepare pure offline contracts and mocks. C14 governs controlled paper trading. C15 governs any live-trading consideration.

## Required Future Verification

- Verify one submission authority and idempotent intent identity.
- Verify fail-closed account, position, order, clock, and session handling.
- Verify ambiguous-submit, fill, terminal-status, resulting-position, and flatten reconciliation.
