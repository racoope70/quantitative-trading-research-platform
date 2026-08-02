# Artifacts Subsystem

## Canonical Responsibility

Own immutable manifests, checksums, serialization, atomic publication, evidence retention, and dataset, model, configuration, prediction, execution-plan, and run identity contracts.

## Permitted Future Contents

- Pure identity, checksum, manifest, and serialization utilities after later authorization.
- Controlled staging, atomic publication, readback, and append-only evidence contracts.
- Versioned provenance references to accepted historical and canonical sources.

## Prohibited Coupling

Do not decide model quality, select candidates, hide required evidence through ignore rules, access providers or brokers, or publish incomplete or identity-mismatched packages.

## Dependency Direction

Artifact contracts may be consumed across subsystems but must remain independent of provider, broker, training, evaluation-decision, and execution implementations.

## Responsible Future Phase

C4 governs selected artifact and publication implementation. Later phases bind their outputs to these contracts.

## Required Future Verification

- Verify deterministic serialization and checksums.
- Verify atomic multi-file publication and failure cleanup.
- Verify immutable provenance and rejection of collisions or mismatches.
