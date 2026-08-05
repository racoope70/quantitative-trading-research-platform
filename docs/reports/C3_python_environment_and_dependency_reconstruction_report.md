# C3 Python Environment and Dependency Reconstruction Report

```text
document_status = GATE_2_LOCAL_RECONSTRUCTION_COMPLETE_PENDING_GATE_3
phase = C3
working_branch = c3-python-environment-dependency-reconstruction
working_base_commit = 748159123dbb4944e090e7d8adeac9306a7bf0a8
canonical_source_commit = UNBOUND
C3_gate_1_status = PASS_COMPLETE
C3_gate_2_status = PASS_COMPLETE
C3_gate_3_status = NOT_AUTHORIZED
C3_terminal_disposition = NOT_YET_ESTABLISHED
C3_completion_effect = NONE
C4_authorization_effect = NONE
```

## 1. Gate 2 Scope Performed

Gate 2 verified the exact twelve-file Gate 1 payload, generated the canonical
working-tree `requirements.lock`, acquired and verified the accepted tooling,
built the canonical local project wheel, constructed two clean local Python
3.12 environments, executed approved local imports, diagnostics, and tests,
and bound the resulting local evidence in the environment-variable contract,
the C3 manifest, and this report.

Repository writes were limited to:

1. `requirements.lock`
2. `docs/configuration/environment_variables.md`
3. `docs/reports/C3_environment_and_dependency_manifest.yaml`
4. `docs/reports/C3_python_environment_and_dependency_reconstruction_report.md`
5. `tests/environment/test_import_contract.py`

The test-file change is a subordinate Gate 2 consistency correction: the
original static test treated the required canonical import namespace
`quantitative_trading_research.config.settings` as prohibited merely because
the package name contains the substring `trading`. The corrected test exempts
that exact accepted internal import while preserving all prohibited-subsystem
checks for every other imported module.

All environments, downloaded wheels, build products, test workspaces, logs,
and raw diagnostic evidence were created in one external temporary transaction
root and removed before successful termination.

## 2. Verified Gate 1 Basis

```text
gate_1_applicator_sha256 = 1662552b5ae02d5d4f84dc88847d68fd7e7479d48ac3055e9f96d874a9eefd93
gate_1_payload_combined_sha256 = 211ebc4b8e41866f2191ba043241ab1bf052d140a2fa89ed41f0fc441bf450cf
gate_1_static_file_count = 12
requirements_lock_precondition = ABSENT
repository_status_precondition = EXACT_TWELVE_UNTRACKED_GATE_1_FILES
```

Every Gate 1 file matched its independently bound SHA-256 before acquisition.
No tracked or staged repository change was present.

## 3. Local Python Identity

```text
python_implementation = CPython
python_version = 3.12.7
supported_python_minor = 3.12
supported_python_constraint = >=3.12,<3.13
python_cache_tag = cpython-312
python_SOABI = cpython-312-darwin
platform_tag = macosx-13.0-x86_64
operating_system = Darwin
operating_system_version = 13.7.8
machine = x86_64
pointer_bits = 64
interpreter_file_sha256 = 930c9891d9f8ad9bcc04e245520eb77aa839e13e966f8ca8e1359d4af2cbadb0
```

The exact patch is local reconstruction evidence. Exact local-to-CI patch
equality remains unnecessary; CI must independently satisfy the accepted
CPython 3.12 policy.

## 4. Package-Source Boundary and Tooling Artifacts

```text
dependency_source_allowlist_id = C3_DEPENDENCY_SOURCE_ALLOWLIST_V1
approved_simple_index_url = https://pypi.org:443/simple/
approved_artifact_url_prefix = https://files.pythonhosted.org:443/packages/
credentials_used = NO
proxy_use = NO
alternate_index_use = NO
mirror_use = NO
artifact_inventory_count = 8
artifact_inventory_checksum = 2e3a5399d2a313661f23e8c0a1364ac6fa6f394502ba5d507c93f4102a6257ff
```

Acquisition used the Python standard-library HTTPS client with certificate and
hostname verification, proxy handling disabled, explicit PEP 691 JSON simple
requests, exact `py3-none-any` wheel selection, and SHA-256 comparison against
the index-declared digest. Redirects, queries, credentials, and destinations
outside the two accepted source classes were fail-closed.

- `pip==26.1.2`
  - filename: `pip-26.1.2-py3-none-any.whl`
  - SHA-256: `382ff9f685ee3bc25864f820aa50505825f10f5458ffff07e30a6d96e5715cab`
  - bytes: `1813144`
  - simple-index identity: `https://pypi.org:443/simple/pip/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/5d/95/6b5cb3461ea5673ba0995989746db58eb18b91b54dbf331e72f569540946/pip-26.1.2-py3-none-any.whl`
- `pip-tools==7.6.0`
  - filename: `pip_tools-7.6.0-py3-none-any.whl`
  - SHA-256: `4bd99155b6d8de358a214b0865e1a2855a453570c1a83d40f7b564870b8657be`
  - bytes: `74337`
  - simple-index identity: `https://pypi.org:443/simple/pip-tools/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/60/2f/5f434153d2bf85ae8f85826228707e694276b9e73d6d8040433a03ceeea9/pip_tools-7.6.0-py3-none-any.whl`
- `setuptools==83.0.0`
  - filename: `setuptools-83.0.0-py3-none-any.whl`
  - SHA-256: `29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3`
  - bytes: `1008090`
  - simple-index identity: `https://pypi.org:443/simple/setuptools/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/5d/40/e1e72872c6354b306daef1703549e8e83b4d43cfea356311bf722a043752/setuptools-83.0.0-py3-none-any.whl`
- `build==1.5.0`
  - filename: `build-1.5.0-py3-none-any.whl`
  - SHA-256: `13f3eecb844759ab66efec90ca17639bbf14dc06cb2fdf37a9010322d9c50a6f`
  - bytes: `26018`
  - simple-index identity: `https://pypi.org:443/simple/build/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/0d/fe/6bea5c9162869c5beba5d9c8abbed835ec85bf1ec1fba05a3822325c45f3/build-1.5.0-py3-none-any.whl`
- `wheel==0.47.0`
  - filename: `wheel-0.47.0-py3-none-any.whl`
  - SHA-256: `212281cab4dff978f6cedd499cd893e1f620791ca6ff7107cf270781e587eced`
  - bytes: `32218`
  - simple-index identity: `https://pypi.org:443/simple/wheel/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/87/1b/9e33c09813d65e248f7f773119148a612516a4bea93e9c6f545f78455b7c/wheel-0.47.0-py3-none-any.whl`
- `click==8.4.2`
  - filename: `click-8.4.2-py3-none-any.whl`
  - SHA-256: `e6f9f66136c816745b9d65817da91d61d957fb16e02e4dcd0552553c5a197b76`
  - bytes: `119243`
  - simple-index identity: `https://pypi.org:443/simple/click/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/fb/e2/79c688af8b210d232694e31e59da9f6ec747bae31c3f5946e4e9b98860d5/click-8.4.2-py3-none-any.whl`
- `packaging==26.2`
  - filename: `packaging-26.2-py3-none-any.whl`
  - SHA-256: `5fc45236b9446107ff2415ce77c807cee2862cb6fac22b8a73826d0693b0980e`
  - bytes: `100195`
  - simple-index identity: `https://pypi.org:443/simple/packaging/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/df/b2/87e62e8c3e2f4b32e5fe99e0b86d576da1312593b39f47d8ceef365e95ed/packaging-26.2-py3-none-any.whl`
- `pyproject-hooks==1.2.0`
  - filename: `pyproject_hooks-1.2.0-py3-none-any.whl`
  - SHA-256: `9e5c6bfa8dcc30091c74b0cf803c81fdd29d94f01992a7707bc97babb1141913`
  - bytes: `10216`
  - simple-index identity: `https://pypi.org:443/simple/pyproject-hooks/`
  - artifact identity: `https://files.pythonhosted.org:443/packages/bd/24/12818598c362d7f300f18e74db45963dbcb85150324092410c8b49405e42/pyproject_hooks-1.2.0-py3-none-any.whl`

The previously observed pip wheel hash remained consistent with the accepted
`pip==26.1.2` artifact identity. The complete artifact inventory above is the
Gate 2 canonical local acquisition evidence.

## 5. Tooling Environment

```text
pip = 26.1.2
pip-tools = 7.6.0
setuptools = 83.0.0
build = 1.5.0
wheel = 0.47.0
click = 8.4.2
packaging = 26.2
pyproject-hooks = 1.2.0
tooling_environment_checksum = e788d6219f138f58121aee7199732ae23c4c2269fb13a65950066250d24d06fa
tooling_environment_identity = C3_TOOLING_ENVIRONMENT_IDENTITY_V1:sha256:e788d6219f138f58121aee7199732ae23c4c2269fb13a65950066250d24d06fa
pip_check = PASS
```

The tooling environment was newly constructed outside the repository. The
interpreter's bundled bootstrap pip was used only to install the verified
`pip==26.1.2` wheel. All remaining tooling wheels were then installed with
`--no-index --no-deps`; no tooling package is a project runtime or test
dependency.

## 6. Configuration and Dependency Metadata

```text
configuration_schema = C3_ENVIRONMENT_SETTINGS_V1
configuration_field_count = 26
configuration_checksum = fc157ea345d1d14f3868ffb822e92199d5bacd88f9df457ada04018a71938bc1
configuration_identity = C3_ENVIRONMENT_SETTINGS_V1:sha256:fc157ea345d1d14f3868ffb822e92199d5bacd88f9df457ada04018a71938bc1
dependency_metadata_schema = C3_DEPENDENCY_METADATA_V1
dependency_metadata_checksum = 7acce244378b75e677c38feac945996845a441c34ebb3382d328426b70c5e489
dependency_metadata_identity = C3_DEPENDENCY_METADATA_V1:sha256:7acce244378b75e677c38feac945996845a441c34ebb3382d328426b70c5e489
direct_project_dependency_count = 0
resolved_project_dependency_count = 0
hash_enforcement_required_dependency_metadata_fact = true
```

The configuration checksum was independently calculated from the accepted
26-field mapping and reproduced by both installed local environments. The
`hash_enforcement_required` fact remains dependency metadata and is not a
field in `C3_ENVIRONMENT_SETTINGS_V1`.

## 7. Canonical Requirements Lock

The canonical lock was generated twice from the exact canonical repository
root using relative `pyproject.toml` and `requirements.lock` paths and the
accepted command:

```text
python -m piptools compile
--no-config
--resolver=backtracking
--generate-hashes
--strip-extras
--header
--newline=lf
--no-emit-index-url
--no-emit-trusted-host
--no-emit-find-links
--no-emit-options
--output-file=requirements.lock
pyproject.toml
```

```text
repeated_local_generation = PASS_EXACT_BYTE_IDENTITY
canonical_lock_sha256 = 37f9e4eb0a6fe13ebf484cd0005d5913994514194a58bd79d19aa47895d36c08
canonical_lock_byte_count = 287
project_requirement_entry_count = 0
artifact_hash_entry_count = 0
hash_enforced_installation = PASS_ZERO_ENTRY_LOCK
canonical_checksum_matches_prior_experimental_value = YES
```

The checksum was bound from newly generated canonical bytes. Any numerical
equality with the prior experiment is independently reproduced evidence and
is not reuse or promotion of the experimental checksum. The prior checksum
remains classified as `NONCANONICAL_EXPERIMENTAL_EVIDENCE_ONLY`.

Linux regeneration and cross-platform byte comparison remain
`PENDING_GATE_3_EXECUTION`.

## 8. Project Wheel

```text
project_wheel_filename = quantitative_trading_research_platform-0.0.0-py3-none-any.whl
project_wheel_sha256 = 1a720bdd51a99ee130b84f8f01c90c95368e081e611572b28df77086d72c3a46
normalized_wheel_metadata_checksum = 48bff38c314840e2c9a9310298b6b3b8c92e59ac0753ea7b86e942bb494fa035
wheel_member_count = 14
accepted_source_requires_python = >=3.12,<3.13
wheel_metadata_requires_python = <3.13,>=3.12
requires_python_semantic_equivalence = PASS
requires_python_normalized_identity = PASS_EXACT_NORMALIZED_MATCH
wheel_tag = py3-none-any
Requires-Dist_count = 0
entry_point_count = 0
build_result = PASS
```

The wheel was built outside the repository with `python -m build --wheel
--no-isolation` using `build==1.5.0` and `setuptools==83.0.0`. No build output
was retained in the repository.

## 9. Two Clean Local Constructions

```text
construction_1_status = PASS
construction_1_environment_identity = C3_CANONICAL_ENVIRONMENT_IDENTITY_V1:sha256:69b8a888eeed955dd63c3bc8d9607a20481afe3bd4a3397ee546edf3f1f12e99
construction_2_status = PASS
construction_2_environment_identity = C3_CANONICAL_ENVIRONMENT_IDENTITY_V1:sha256:69b8a888eeed955dd63c3bc8d9607a20481afe3bd4a3397ee546edf3f1f12e99
repeated_environment_identity_result = PASS_EXACT_IDENTITY_MATCH
repeated_environment_identity = C3_CANONICAL_ENVIRONMENT_IDENTITY_V1:sha256:69b8a888eeed955dd63c3bc8d9607a20481afe3bd4a3397ee546edf3f1f12e99
```

Each environment was separately created from CPython 3.12, received the same
verified tooling wheels, applied `requirements.lock` with `--require-hashes
--no-index`, installed the project wheel with `--no-deps`, and passed
`pip check`.

## 10. Imports, Diagnostics, Configuration, and Tests

```text
canonical_import_target_count = 4
canonical_import_result = PASS
diagnostic_overall_result = PASS
local_diagnostic_evidence_identity = C3_ENVIRONMENT_DIAGNOSTIC_EVIDENCE_V1:sha256:23d77f462d8a8c86826d49baf96772eb77977f174b3e61bc5e02d9c938c6244d
local_environment_identity = C3_CANONICAL_ENVIRONMENT_IDENTITY_V1:sha256:69b8a888eeed955dd63c3bc8d9607a20481afe3bd4a3397ee546edf3f1f12e99
configuration_test_result = PASS
diagnostic_test_result = PASS
ordinary_unittest_result = PASS
configuration_test_count = 11
diagnostic_test_count = 18
ordinary_test_count = 47
atomic_write_result = PASS
```

The same test and diagnostic outcome was reproduced in both clean local
environments. Raw diagnostic evidence was written only to an approved external
temporary directory for atomic-write verification, read back, verified, and
deleted before transaction completion.

## 11. Local Offline and Secret-Exclusion Boundary

Each canonical local Python command received an empty-base allowlisted
environment with no GitHub, Actions, proxy, package-index, provider, broker,
market-data, account, token, credential, or secret variable. Standard input
was `/dev/null`, `close_fds=True` was used, and the child verified that no file
descriptor above two was inherited.

A standard-library CPython audit hook was installed before canonical package
imports. A nonnetwork custom audit event verified that the hook was active.
During canonical imports, diagnostics, and tests the primary interpreter
recorded zero unexpected DNS, network, process-creation, or ctypes audit
events.

```text
credential_exclusion_result = PASS
proxy_exclusion_result = PASS
package_index_variable_exclusion_result = PASS
inherited_file_descriptor_result = PASS_ZERO_ABOVE_TWO_AT_CHILD_ENTRY
primary_python_audit_guard_selftest = PASS
unexpected_primary_python_DNS_events = 0
unexpected_primary_python_network_events = 0
unexpected_primary_python_process_events = 0
unexpected_primary_python_ctypes_events = 0
environment_variable_runtime_verification = PASS_GATE_2_LOCAL_ENVIRONMENT_EXCLUSION
secret_exposure_result = PASS_NO_SECRET_EXPOSURE_DETECTED_DURING_GATE_2_LOCAL_EXECUTION
CI_environment_exclusion_verification = PENDING_GATE_3_EXECUTION
```

The environment-variable evidence document was updated from the completed
Gate 2 local transaction results. It contains no remaining Gate 2 pending or
not-executed state; CI exclusion evidence remains pending Gate 3.

Gate 2 did not execute DNS, HTTPS, IPv4, or IPv6 negative-control destinations.
Those controls, the Linux kernel namespace, privilege drop, and native or
descendant enforcement remain Gate 3 work.

macOS does not provide the accepted Linux namespace mechanism. Local evidence
therefore establishes primary-interpreter blocking and observation, not
universal kernel-level egress isolation. Universal native, descendant, DNS,
and network-syscall attempt counts remain `NOT_ESTABLISHED`.

## 12. Gate 3 and Later Evidence Preserved as Pending

The following remain unbound, pending, not executed, or unauthorized:

- GitHub-hosted runner command identities and image evidence.
- `sudo`, `unshare`, `setpriv`, and `ip` feasibility.
- Network-namespace and privilege-drop evidence.
- Exact kernel negative controls.
- Setup-python hit, miss, or inconclusive classification.
- Setup-python manifest and Python-artifact provenance.
- Linux tooling acquisition and construction.
- Linux repeated lock generation.
- Local-to-Linux lock-byte comparison.
- Canonical CI environment identity.
- Local-to-CI equivalence.
- Pull-request and post-merge workflow runs.
- Manager Review and focused independent audit.
- Owner technical-outcome decision.
- C3 completion decision and alignment.

No CI, runner, namespace, cross-platform, review, audit, or completion result
is claimed by Gate 2.

## 13. Prohibited-Activity Confirmation

Gate 2 performed no provider or broker access, market-data request, account or
entitlement inspection, dataset access, model execution, final-holdout access,
order activity, or trading activity. It used no sudo, network namespace,
GitHub Actions run, staging, commit, push, pull request, merge, or C4 action.

## 14. Evidence Limitations

C3 repository and local execution evidence cannot prove the absence of
unrecorded external activity. The evidence does not establish provider,
broker, dataset, model, candidate, deployment, publication, economic, paper-
trading, live-trading, or final-holdout readiness.

## 15. Current Terminal Disposition

```text
C3_terminal_disposition = NOT_YET_ESTABLISHED
successful_C3_completion_eligibility = NOT_YET_ESTABLISHED
C3_completion_effect = NONE
C4_authorization_effect = NONE
```

## 16. Next Material Gate

```text
recommended_next_gate =
GATE_3_AUTHORIZE_THE_EXACT_PRIVILEGED_OR_NETWORKED_GITHUB_ACTIONS_RUN
```

Gate 3 must be based on the exact reviewed workflow bytes and later Gate 4
repository-action authorization. The first remote branch push would itself
trigger the single-use capability probe, so those effects must be jointly
controlled.
