# Configuration Subsystem

## Canonical Responsibility

Own versioned configuration, environment-variable, path, authorization-boundary, and configuration-identity responsibilities.

## Permitted Future Contents

- Typed and versioned configuration schemas after C3/C4 authorization.
- Platform-neutral path resolution.
- Deterministic configuration validation, checksums, and redacted identity records.

## Prohibited Coupling

Do not store secrets, select providers, request data, train models, access brokers, submit orders, or perform work at import time.

## Dependency Direction

Configuration may depend on standard validation and identity utilities. Other subsystems may consume validated configuration; configuration must not depend on data, features, models, evaluation, or execution.

## Responsible Future Phase

C3 owns environment and dependency reconstruction. C4 may later implement selected configuration assets. Provider-specific acceptance remains C5 or later.

## Required Future Verification

- Verify deterministic configuration identity.
- Verify missing, contradictory, unsupported, and secret-bearing values fail closed.
- Verify configuration imports remain offline and side-effect-free.
