# C3 Python Environment and Dependency Reconstruction — Python Policy and Dependency Evaluation Preparation

```text
record_status = HOST_NEUTRAL_PYTHON_POLICY_AND_DEPENDENCY_EVALUATION_PREPARATION
canonical_basis = b764eed6a92c39153c7f5e525a457c92445306d9
C3_terminal_disposition = NOT_REACHED
FREEZE_BLOCKER_001 = OPEN__NO_QUALIFIED_HOST_SELECTED
Stage1_scientific_admission_progression = PAUSED_AT_STAGE1A
scientific_host = NOT_SELECTED
package_acquisition_performed = NO
resolver_execution_performed = NO
requirements_lock_generated = NO
clean_environment_constructed = NO
```

## 1. Preparation boundary

This record defines the static, reviewable specification for a later separately authorized dependency-resolution and clean-environment reconstruction transaction. It does not install packages, query package indexes through a resolver, resolve compatibility, generate `requirements.lock`, construct an environment, create technical C3 CI, select a scientific host, or advance C4.

Historical requirement expressions remain evidence only. No package or version is accepted merely because it appeared in predecessor `requirements.txt` or predecessor CI.

## 2. Exact Python candidate set

```text
python_selection_method = BOUNDED_TWO_CANDIDATE_MINOR_VERSION_EVALUATION
candidate_minor_1 = 3.12
candidate_minor_2 = 3.13
candidate_count = 2
supported_minor_versions_after_successful_C3 = 1
final_selected_python_policy = UNRESOLVED_PENDING_CONTROLLED_EVALUATION
preferred_evaluation_candidate = 3.13
fallback_evaluation_candidate = 3.12
```

### Candidate 3.12

Inclusion basis:

- Exact accepted historical CI evidence used Python `3.12`.
- It minimizes migration distance from the predecessor environment.
- It provides the strongest historical compatibility anchor available in accepted C1 evidence.

Limitation:

- Historical use does not establish current compatibility.
- The 3.12 series is now in security-fixes-only maintenance, so its maintenance horizon is weaker than 3.13.

### Candidate 3.13

Inclusion basis:

- It is one minor newer than the accepted historical 3.12 anchor, keeping the evaluation bounded.
- It offers a stronger maintenance horizon than 3.12.
- Current packaging/tooling evidence supports evaluating it rather than defaulting to the newest possible Python series.

Limitation:

- No accepted project execution has yet established that the complete proposed dependency set resolves, installs, imports, and passes focused C3 tests on 3.13.

### Selection criteria

Both candidates must be evaluated under the same rules:

1. Same proposed direct-dependency specification.
2. Same exact resolver family and version.
3. Same exact package-source allowlist.
4. Same hash-generation and lock-integrity requirements.
5. Same clean reconstruction procedure.
6. Same canonical environment-level import contract.
7. Same focused C3 tests and network-denied offline phase.
8. Same local/CI equivalence rules.

Evaluation dimensions:

- `canonical_package_compatibility`
- `accepted_direct_dependency_compatibility`
- `platform_support_status`
- `reproducibility_implications`
- `test_tooling_compatibility`
- `scientific_library_compatibility`
- `migration_implications_for_C4`
- `known_historical_compatibility_evidence`
- `maintenance_horizon`

Selection rule:

- If exactly one candidate satisfies all mandatory criteria, select that minor.
- If both satisfy all mandatory criteria with equivalent reproducibility evidence, prefer 3.13 because of the stronger maintenance horizon.
- If 3.13 requires prohibited sources, unsupported artifacts, incompatible direct constraints, or weaker reproducibility, select 3.12 if 3.12 independently passes.
- If neither candidate passes, classify the outcome using the accepted C3 terminal framework; do not add a third candidate without separate authorization.

The exact CPython patch version for each candidate must be recorded at execution time and becomes evidence, not a second supported-minor policy.

## 3. Historical requirement classification

Source identity for all entries below:

```text
identity = C1-TM-042
source_repository = racoope70/ppo-trading-pipeline
source_commit = 072103f43d8b2488c3efca183f637ab0508a193a
source_path = requirements.txt
source_blob = 3dafa779f02d6bcb1b3f49689729bcb1900a63c9
historical_requirement_expressions = EVIDENCE_ONLY
automatic_historical_dependency_acceptance = NO
```

| Historical expression | Preparation classification | Canonical treatment |
|---|---|---|
| `numpy` | RETAIN_CANDIDATE | Proposed direct dependency with bounded constraint. |
| `pandas` | RETAIN_CANDIDATE | Proposed direct dependency with bounded constraint. |
| `python-dotenv` | REPLACED | Not proposed; canonical C3 settings use a typed stdlib mapping boundary rather than `.env` loading. |
| `alpaca-py` | DEFERRED | Provider-specific dependency remains deferred to the responsible provider phase. |
| `matplotlib` | EXCLUDED_FROM_BASE | Visualization is not required for the canonical base environment; reconsider only if a later authorized responsibility requires it. |
| `scikit-learn` | RETAIN_CANDIDATE | Proposed direct dependency for accepted classical-ML responsibilities. |
| `joblib` | EXCLUDED_AS_DIRECT | No independent canonical need established; allow only as resolver-selected transitive dependency unless later direct imports justify promotion. |
| `tqdm` | EXCLUDED_AS_DIRECT | Progress UI is not a canonical environment responsibility; allow transitively if required. |
| `requests` | EXCLUDED_AS_DIRECT | Generic network client is not a canonical base responsibility and must not expand the C3 network boundary. |
| `yfinance` | DEFERRED | Market-data/provider behavior is outside C3 and requires later authorization. |
| `PyWavelets` | RETAIN_CANDIDATE | Proposed direct dependency for accepted wavelet/feature research responsibilities. |
| `xgboost` | RETAIN_CANDIDATE | Proposed direct dependency for the accepted XGBoost model-gate lineage. |
| `stable-baselines3[extra]>=2.0.0` | CONSTRAINED_AND_REPLACED | Retain core `stable-baselines3` only; drop `[extra]` to avoid unrelated optional packages. |
| `gymnasium>=0.29` | CONSTRAINED | Retain with a bounded modern Gymnasium constraint. |
| `shimmy>=2.0.0` | EXCLUDED_AS_DIRECT | Legacy Gym compatibility bridge is not required unless later migration evidence proves a direct need. |
| `gym-anytrading` | EXCLUDED | Historical environment abstraction is not accepted canonical architecture. |
| `torch` | RETAIN_CANDIDATE | Proposed direct dependency as the SB3/PPO tensor backend. |
| `torchvision` | EXCLUDED | Vision package has no accepted canonical responsibility. |
| `torchaudio` | EXCLUDED | Audio package has no accepted canonical responsibility. |
| `pyarrow` | RETAIN_CANDIDATE | Proposed direct dependency for deterministic columnar data interchange/persistence responsibilities. |
| `transformers` | EXCLUDED | No accepted canonical transformer responsibility exists in the current architecture. |
| `tensorflow==2.16.2` | EXCLUDED | Current accepted PPO lineage is PyTorch/SB3; historical TensorFlow presence is not canonical need. |
| `protobuf==3.20.3` | EXCLUDED_AS_DIRECT | Historical compatibility pin is not a canonical direct responsibility; resolver may select it transitively if required. |
| `numba==0.60.0` | UNRESOLVED | Performance optimization is not yet proven necessary; do not include unless later direct code evidence establishes canonical need. |
| `exchange-calendars==4.13.2` | RETAIN_CANDIDATE | Proposed direct dependency for future accepted exchange-calendar responsibility, without executing calendar logic during C3. |

## 4. Proposed direct dependency candidate set

These are preparation proposals, not yet canonical `[project].dependencies`. Acceptance requires review plus the later controlled compatibility transaction.

### `numpy`

```text
package_name = numpy
proposed_inclusion = YES
proposed_constraint = >=2.2,<3
source_evidence = C1-TM-042
canonical_need = numerical array foundation used across accepted quantitative responsibilities
compatibility_question = both Python candidates; pandas/scikit-learn/PyWavelets/xgboost/SB3 compatibility
rationale = retain a modern bounded major line while the lock records the exact resolved version
known_limitation = exact compatible resolution not executed
```

### `pandas`

```text
package_name = pandas
proposed_inclusion = YES
proposed_constraint = >=2.2,<4
source_evidence = C1-TM-042
canonical_need = tabular and time-series representation used by accepted research responsibilities
compatibility_question = both Python candidates; NumPy/PyArrow compatibility and 2.x-versus-3.x migration behavior
rationale = bounded supported 2.x/3.x release families while exact compatibility and final pin remain lock-resolved
known_limitation = exact compatible resolution and later API-migration testing not executed
```

### `scikit-learn`

```text
package_name = scikit-learn
proposed_inclusion = YES
proposed_constraint = >=1.6,<2
source_evidence = C1-TM-042 plus accepted classical-ML lineage
canonical_need = Random Forest and common classical-ML interfaces required by accepted future responsibilities
compatibility_question = both Python candidates; NumPy/SciPy/joblib transitive resolution
rationale = bounded pre-2.0 API family while avoiding historical unconstrained drift
known_limitation = transitive scientific stack not yet resolved
```

### `PyWavelets`

```text
package_name = PyWavelets
proposed_inclusion = YES
proposed_constraint = >=1.8,<2
source_evidence = C1-TM-042 plus accepted feature-research lineage
canonical_need = wavelet transforms where retained by later authorized feature migration
compatibility_question = both Python candidates; NumPy ABI/wheel compatibility
rationale = bounded stable 1.x family; exact version remains lock-resolved
known_limitation = later feature migration must still prove direct use
```

### `xgboost`

```text
package_name = xgboost
proposed_inclusion = YES
proposed_constraint = >=3,<4
source_evidence = C1-TM-042 plus accepted XGBoost-gate lineage
canonical_need = XGBoost candidate gate in the accepted research roadmap
compatibility_question = both Python candidates; platform wheel and NumPy/scikit-learn interoperability
rationale = bounded current 3.x major family with exact lock pin deferred
known_limitation = no C3 model execution is permitted
```

### `stable-baselines3`

```text
package_name = stable-baselines3
proposed_inclusion = YES
proposed_constraint = >=2.7,<3
source_evidence = historical stable-baselines3[extra]>=2.0.0 plus accepted PPO lineage
canonical_need = canonical PPO/RL library family
compatibility_question = both Python candidates; Gymnasium/Torch constraints and optional-extra exclusion
rationale = use core package only and bound to current 2.x family; do not inherit historical [extra]
known_limitation = PPO execution remains outside this preparation and current C3 tests
```

### `gymnasium`

```text
package_name = gymnasium
proposed_inclusion = YES
proposed_constraint = >=1.1,<2
source_evidence = historical gymnasium>=0.29 plus accepted PPO environment lineage
canonical_need = canonical RL environment interface paired with SB3
compatibility_question = both Python candidates; SB3-supported Gymnasium range
rationale = replace historical minimum-only expression with bounded 1.x family
known_limitation = exact SB3/Gymnasium pairing must be resolved
```

### `torch`

```text
package_name = torch
proposed_inclusion = YES
proposed_constraint = >=2.7,<3
source_evidence = C1-TM-042 plus SB3 backend requirement
canonical_need = tensor backend for accepted PPO/SB3 responsibilities
compatibility_question = both Python candidates; target-platform wheels and SB3 compatibility
rationale = bounded 2.x family with exact platform-specific artifact identity deferred to lock/reconstruction
known_limitation = platform wheel availability must be proven for every controlled construction
```

### `pyarrow`

```text
package_name = pyarrow
proposed_inclusion = YES
proposed_constraint = >=20,<26
source_evidence = C1-TM-042 plus accepted deterministic data-artifact responsibilities
canonical_need = columnar data interchange/persistence support
compatibility_question = both Python candidates; NumPy/Pandas compatibility and target-platform wheels
rationale = bounded recent release window while the lock supplies exact artifact hashes
known_limitation = no dataset activity is authorized during C3
```

### `exchange-calendars`

```text
package_name = exchange-calendars
proposed_inclusion = YES
proposed_constraint = >=4.11,<5
source_evidence = historical exchange-calendars==4.13.2 plus accepted future calendar responsibility
canonical_need = explicit exchange-calendar dependency for later authorized dataset/calendar work
compatibility_question = both Python candidates; Pandas/NumPy compatibility
rationale = replace historical exact application-era pin with bounded 4.x intent and defer exact pin to lock resolution
known_limitation = calendar behavior remains prohibited during C3
```

Proposed direct candidate count: `10`.

## 5. Excluded and unresolved direct dependencies

Excluded/deferred from the proposed base direct set:

```text
python-dotenv
alpaca-py
matplotlib
joblib
tqdm
requests
yfinance
shimmy
gym-anytrading
torchvision
torchaudio
transformers
tensorflow
protobuf
```

Unresolved direct question:

```text
numba = UNRESOLVED_OPTIONAL_PERFORMANCE_DEPENDENCY
```

`numba` must remain excluded from canonical direct dependencies unless later accepted code evidence proves a direct performance responsibility that cannot be met without it.

## 6. Resolver preparation

```text
resolver_family = PIP_TOOLS_PIP_COMPILE
resolver_invocation_family = python_-m_piptools_compile
proposed_resolver_exact_version = 7.6.1
resolver_status = PREPARATION_PROPOSAL_NOT_INSTALLED_OR_EXECUTED
resolver_hash_generation = REQUIRED
resolver_output = requirements.lock
```

Reason for proposing `pip-tools==7.6.1`:

- It is the current release in the already accepted resolver family at preparation time.
- It supports both bounded Python candidates.
- It preserves `pip-compile --generate-hashes` behavior required by the C3 lock policy.

The future execution must record both `pip-tools` and `pip` exact versions because `pip-tools` delegates resolution/install mechanics to pip internals.

## 7. Future package-source boundary

Exactly and only:

```text
index = https://pypi.org:443/simple/
artifact_host = https://files.pythonhosted.org:443/packages/
credentials = NONE
alternate_index = PROHIBITED
extra_index = PROHIBITED
mirror = PROHIBITED
VCS_dependency = PROHIBITED
arbitrary_direct_URL = PROHIBITED
trusted_host_TLS_bypass = PROHIBITED
redirect_to_unlisted_destination = PROHIBITED
package_manager_version_check = DISABLED_DURING_ACQUISITION
```

The preparation workstream performs no access to these destinations through pip, pip-tools, or another resolver.

## 8. Exact future resolution/reconstruction transaction

A later separately authorized execution transaction should perform the following, fail-closed and in order:

1. Reverify canonical `main`, accepted preparation record, exact 10-package proposed direct set, candidate minors, resolver version, and allowlist.
2. Freeze one exact CPython patch build for candidate 3.12 and one exact CPython patch build for candidate 3.13 for evaluation evidence.
3. Create isolated candidate-resolution environments; they are evaluation environments, not canonical acceptance.
4. Acquire exactly `pip-tools==7.6.1` and its required bootstrap dependencies only through `C3_DEPENDENCY_SOURCE_ALLOWLIST_V1`; record exact pip/pip-tools versions and hashes.
5. Materialize the reviewed bounded direct constraints into `pyproject.toml`; keep rationale metadata adjacent in `[tool.c3]` or the reconstruction report.
6. For each candidate minor, execute `python -m piptools compile` with hash generation, exact PyPI index identity, no extra index, no trusted-host bypass, and output to a candidate lock artifact.
7. Reject any resolution that requires an unapproved source, VCS/direct URL, incompatible Python marker, unavailable required artifact, or dependency outside the accepted policy.
8. Compare candidate lock graphs, direct constraints, transitive versions, artifact availability, and source identities.
9. Run a clean hash-enforced installation from the candidate lock using `python -m pip install --require-hashes -r <candidate-lock>` with only the accepted source boundary.
10. Disable network and credentials after acquisition.
11. Run canonical environment-level imports, configuration tests, diagnostics, dependency/lock identity tests, and ordinary focused C3 tests offline.
12. Select the single Python minor only after the accepted candidate-selection rule is satisfied.
13. Generate the canonical `requirements.lock` for the selected minor with exact versions and artifact hashes; compute and record lock checksum plus dependency-metadata checksum.
14. Reconstruct the selected environment cleanly at least twice and verify identity reproducibility.
15. Create/update `.github/workflows/tests.yml` with separate acquisition and network-denied validation stages; reconstruct from the same canonical lock and source identities in CI.
16. Verify exact local/CI match for selected Python-minor policy, lock checksum, and package-source identities.
17. Update the C3 manifest/report with exact interpreter, resolver, dependency, lock, environment, CI, and equivalence evidence.
18. Route the exact technical outcome package through required Manager Review and focused independent review before any C3 terminal decision.

## 9. Future execution changed-file scope

No new path is required beyond the already authorized C3 technical scope. The future execution is expected to create or modify only as needed:

```text
pyproject.toml
requirements.lock
docs/reports/C3_environment_and_dependency_manifest.yaml
docs/reports/C3_python_environment_and_dependency_reconstruction_report.md
.github/workflows/tests.yml
tests/environment/test_dependency_identity.py
tests/environment/test_import_contract.py
tests/environment/test_offline_boundary.py
src/quantitative_trading_research/config/environment_diagnostics.py
```

`settings.py` and its tests need change only if the future accepted environment identity requires a bounded correction; no change is implied by this preparation.

## 10. Evidence and terminal classification for the future transaction

Per candidate, record at minimum:

```text
candidate_minor
exact_interpreter_implementation_and_patch
resolver_identity_and_version
pip_identity_and_version
source_allowlist_identity
resolution_result
resolved_dependency_graph
artifact_hash_coverage
lock_checksum
clean_install_result
canonical_import_results
offline_test_result
network_denial_result
secret_exclusion_result
platform_artifact_availability
```

Candidate classification:

```text
PASS_CANDIDATE
FAIL_MISSING_PACKAGE
FAIL_INCOMPATIBLE_VERSION
FAIL_INVALID_IMPORT_TARGET
FAIL_CONFIGURATION
FAIL_IDENTITY_MISMATCH
FAIL_PROHIBITED_NETWORK_ATTEMPT
FAIL_PROHIBITED_SECRET_EXPOSURE
FAIL_OTHER
INCONCLUSIVE
```

Overall C3 remains governed by the accepted terminal outcomes:

```text
ACCEPTED_REPRODUCIBLE_ENVIRONMENT
REJECTED_NO_ACCEPTABLE_ENVIRONMENT
BLOCKED_EXTERNAL_OR_OWNER_DEPENDENCY
INCONCLUSIVE
```

A resolver success alone is insufficient. A candidate cannot pass without hash-complete lock evidence, clean reconstruction, offline import/test success, source-boundary enforcement, and required identity/equivalence evidence.

## 11. Scientific-host preservation

```text
dedicated_scientific_host_purchase = ALREADY_DEFERRED_BY_OWNER
current_Mac_role = DEVELOPMENT_AND_NON_CONTROLLING_RESEARCH_WORKSTATION
Stage1_scientific_host_track = PAUSED_AT_FREEZE_BLOCKER_001
proceed_with_host_neutral_project_work_now = YES
purchase_qualified_scientific_host_now = NO
scientific_host_track_changed = NO
```

This preparation does not reopen or alter the hardware decision.
