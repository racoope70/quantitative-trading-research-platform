# C3 Python Environment and Dependency Reconstruction — Host-Neutral Preparation Record

```text
record_status = HOST_NEUTRAL_STATIC_PREPARATION_ONLY
C3_terminal_disposition = NOT_REACHED
FREEZE_BLOCKER_001 = OPEN__NO_QUALIFIED_HOST_SELECTED
Stage1_scientific_admission_progression = PAUSED_AT_STAGE1A
scientific_host = NOT_SELECTED
```

## Scope performed

This bounded package prepares only the host-neutral portions of the accepted C3 technical scope: historical dependency inventory, direct-dependency candidate recording, configuration and environment-variable contracts, canonical environment-level import targets, deterministic offline diagnostics, and focused standard-library tests.

It does not select a scientific host, select a final Python policy, resolve dependencies, acquire package metadata or artifacts, generate a lock, install packages, construct an environment, create CI infrastructure, or advance Stage1B–Stage1E scientific freeze/admission.

## Python candidates

The accepted method remains `BOUNDED_TWO_CANDIDATE_MINOR_VERSION_EVALUATION`. No candidate evaluation was executed in this workstream, and no supported Python minor version is selected by this record.

## Dependency inventory

The historical `requirements.txt` identity `C1-TM-042` was inspected at its accepted source commit. Candidate names are recorded in `pyproject.toml` only as unresolved historical candidates. `project.dependencies` remains empty so that no package is prematurely accepted as a canonical direct dependency.

The accepted source allowlist remains:

- `https://pypi.org:443/simple/`
- `https://files.pythonhosted.org:443/packages/`

No network access or acquisition was performed.

## Configuration and secret boundary

`settings.py` provides a typed, versioned, deterministic host-neutral configuration identity with no import-time network/filesystem mutation. Operational/provider/broker variables are rejected. `docs/configuration/environment_variables.md` defines the corresponding nonsecret, secret-reference, prohibited, and deferred classes.

## Diagnostics and import contract

`environment_diagnostics.py` implements only environment-level Python/platform/dependency/configuration/import evidence. Canonical import targets are limited to the package root and config package. It performs no provider, data, model, evaluation, execution, or trading behavior.

## Scientific-host and Stage1 boundary

All final host-dependent identities remain unresolved. In particular, this package does not introduce kernel, firmware, TPM/EK, QEMU/OVMF, CPython-byte, native-library, or scientific-host hashes. `FREEZE_BLOCKER_001` remains open.

## Validation boundary

Only syntax/static validation and deterministic standard-library offline tests are valid for this package. Any Mac-side result is non-controlling development evidence and is not scientific-host qualification.

## Remaining C3 work

Still unresolved: Python two-candidate evaluation, exact direct dependency acceptance/constraints, resolver version identity, dependency resolution, hashed `requirements.lock`, clean environment reconstruction, technical CI, local-to-CI equivalence, and final C3 outcome evidence. Host-dependent successor Stage1 identities remain paused until a qualified physical host is selected.
