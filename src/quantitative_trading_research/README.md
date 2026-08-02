# Quantitative Trading Research Package

## Canonical Responsibility

Define the canonical top-level namespace and the ownership boundaries among configuration, data, features, models, evaluation, artifacts, and execution.

## Permitted Future Contents

- Package-level documentation and, after later authorization, minimal namespace metadata.
- Explicit subsystem exports that introduce no import-time execution or hidden side effects.
- Version and identity references governed by canonical artifact and environment contracts.

## Prohibited Coupling

Do not place data acquisition, feature calculation, model execution, evaluation, broker access, order submission, or environment setup in the package root.

## Dependency Direction

The package root may expose stable subsystem boundaries but must not create reverse dependencies or import provider, broker, training, or execution implementations at import time.

## Responsible Future Phase

C2 defines this boundary. C3 governs environment and packaging identity. C4 governs any later executable namespace implementation.

## Required Future Verification

- Verify imports remain side-effect-free and offline.
- Verify only approved subsystem boundaries are exposed.
- Verify no executable responsibility is duplicated at the package root.
