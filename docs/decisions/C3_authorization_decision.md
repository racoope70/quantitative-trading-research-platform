# C3 Python Environment and Dependency Reconstruction Authorization Decision

```text
document_status = ACCEPTED_C3_AUTHORIZATION_DECISION
intended_repository_path = docs/decisions/C3_authorization_decision.md
decision_id = GOV-DEC-0007
decision_type = C3_PHASE_AUTHORIZATION
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED
owner_decision = ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT

manager_review_status = PERFORMED
manager_review_classification = PASS
material_findings = NONE
required_corrections = NONE

authorized_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

authorized_scope =
BOUNDED_C3_ENVIRONMENT_DEPENDENCY_CONFIGURATION_AND_OFFLINE_DIAGNOSTICS_ONLY

decision_basis_commit =
fc360d1e57f04fb258e11821ffd3eb2c376828f2

owner_selection_matrix_id =
C3_OWNER_SELECTION_MATRIX_V1

owner_selection_matrix_status = ACCEPTED

OSM_01_status = ACCEPTED_SELECTED_OPTION
OSM_02_status = ACCEPTED_SELECTED_OPTION
OSM_03_status = ACCEPTED_SELECTED_OPTION
OSM_04_status = ACCEPTED_SELECTED_OPTION
OSM_05_status = ACCEPTED_SELECTED_OPTION
OSM_06_status = ACCEPTED_SELECTED_OPTION
OSM_07_status = ACCEPTED_SELECTED_OPTION
OSM_08_status = ACCEPTED_SELECTED_OPTION
OSM_09_status = ACCEPTED_SELECTED_OPTION
OSM_10_status = ACCEPTED_SELECTED_OPTION
OSM_11_status = ACCEPTED_SELECTED_OPTION
OSM_12_status = ACCEPTED_SELECTED_OPTION
OSM_13_status = ACCEPTED_SELECTED_OPTION
OSM_14_status = ACCEPTED_SELECTED_OPTION
OSM_15_status = ACCEPTED_SELECTED_OPTION
OSM_16_status = ACCEPTED_SELECTED_OPTION
OSM_17_status = ACCEPTED_SELECTED_OPTION
OSM_18_status = ACCEPTED_SELECTED_OPTION
OSM_19_status = ACCEPTED_SELECTED_OPTION

remaining_material_owner_decisions = NONE

authorization_effect =
C3_SCOPE_ONLY_AFTER_EFFECTIVE_CANONICAL_ACTIVATION

C3_activation_effect =
EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN_AND_SUCCESSFUL_EXACT_POST_MERGE_VALIDATION

C4_authorization_effect = NONE
current_model_candidate = NONE
current_deployment_candidate = NONE

repository_recording_status =
RECORDED_AND_ALIGNED

C3_technical_work_may_begin =
NO_UNTIL_SUCCESSFUL_EXACT_POST_MERGE_ACTIVATION_VALIDATION
```

## 1. Purpose

This decision records the owner’s accepted bounded authorization for:

```text
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
```

C3’s purpose is to:

* Select and record one supported canonical Python minor-version policy.
* Reconstruct a clean and reproducible canonical Python environment.
* Establish exact approved dependency-source identities.
* Establish direct and fully resolved dependency identities.
* Create and verify a lock or equivalently reproducible dependency artifact.
* Define a typed, versioned, checksummed configuration boundary.
* Define the committed environment-variable and secret-reference boundary.
* Define canonical environment-level import targets.
* Selectively reimplement bounded environment diagnostics.
* Demonstrate reproducible local and CI environment construction.
* Establish the environment prerequisite required before a separately authorized C4 may be considered.

C3 is not an application-code migration phase.

C3 is not a provider, broker, market-data, dataset, feature, model, evaluation, execution, final-holdout, paper-trading, or live-trading phase.

Successful dependency acquisition does not establish application correctness.

Successful dependency installation does not establish model, provider, dataset, or trading-system readiness.

Successful canonical imports establish only the tested environment-level import result.

## 2. Exact canonical basis

```text
canonical_repository =
racoope70/quantitative-trading-research-platform

canonical_repository_visibility = PRIVATE
canonical_branch = main

exact_decision_basis_commit =
fc360d1e57f04fb258e11821ffd3eb2c376828f2

C2_completion_effect = EFFECTIVE
C3_authorization_status_before_alignment = NOT_AUTHORIZED
C3_authorization_effect_before_alignment = NONE
```

The controlling and supporting basis is:

1. `PROJECT_CONTEXT.md`.
2. `docs/decisions/C2_completion_decision.md`.
3. `docs/architecture/C2_canonical_repository_skeleton_and_boundaries.md`.
4. `docs/migration/C2_migration_disposition_plan.yaml`.
5. `docs/reports/C2_migration_preparation_and_C3_handoff.md`.
6. `docs/workflows/milestone_review_reference_map.md`.
7. `docs/workflows/future_validation_training_reference_map.md`.
8. Accepted immutable C1 evidence referenced by the C2 plan.
9. The corrected C3 authorization orientation.
10. The corrected orientation’s Manager Review classification of `PASS`.
11. The corrected proposed C3 authorization decision’s Manager Review classification of `PASS`.
12. The owner’s exact accepted command.
13. All nineteen accepted selections in `C3_OWNER_SELECTION_MATRIX_V1`.

`PROJECT_CONTEXT.md` remains the sole controlling source for:

* Current lifecycle state.
* Active phase.
* Authorization effect.
* Authorized and prohibited work.
* Environment and dependency status.
* Provider, network, dataset, model, broker, and trading access status.
* Current model and deployment candidate status.
* Current blocker and next permitted workstream.

The milestone and future maps remain non-authorizing guidance and evidence-navigation records.

Historical repositories remain read-only evidence sources. They do not become runtime dependencies or sources of current authorization.

## 3. Current state before effective activation

Until this accepted decision is recorded on canonical `main`, controlling state is aligned, and the exact canonical squash commit passes required post-merge validation:

```text
current_lifecycle_state = C2_COMPLETED
C2_completion_effect = EFFECTIVE
active_major_phase = NONE
authorization_effect = NONE

C3_authorization_status = NOT_AUTHORIZED
C3_authorization_effect = NONE
C4_authorization_effect = NONE

dependency_acquisition = NOT_AUTHORIZED
package_source_access = NOT_AUTHORIZED
environment_construction = NOT_AUTHORIZED
dependency_installation = NOT_AUTHORIZED
import_execution = NOT_AUTHORIZED
diagnostic_execution = NOT_AUTHORIZED
ordinary_test_execution = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

C3_technical_work_may_begin = NO
```

## 4. Owner-selection binding rule

### 4.1 Controlling selection matrix

```text
owner_selection_matrix_id =
C3_OWNER_SELECTION_MATRIX_V1

owner_selection_matrix_status = ACCEPTED

every_material_owner_selection_status =
ACCEPTED_SELECTED_OPTION

remaining_RECOMMENDED_material_selections = NONE
remaining_UNRESOLVED_material_selections = NONE
remaining_UNSPECIFIED_material_selections = NONE
remaining_BLANK_material_selections = NONE
remaining_material_owner_decisions = NONE
```

Every material selection required before C3 activation appears in Section 25.

No selection outside that matrix may be inferred from:

* Narrative recommendations.
* Prior chats.
* Manager Review.
* Historical repository behavior.
* A default tool configuration.
* A branch or pull request.
* Successful pull-request validation.
* Successful package installation.
* Successful import execution.

### 4.2 Accepted controlled approach

The owner accepted controlled approach A:

> The exact owner command accepts every specifically enumerated selected option in `C3_OWNER_SELECTION_MATRIX_V1`.

The command does not accept unstated alternatives or unspecified later choices.

## 5. Lifecycle-effect rules

### 5.1 Accepted decision before canonical alignment

This decision is owner accepted, but C3 is not effectively active merely because the accepted text exists in chat, a local file, a branch, a commit, a push, or a pull request.

```text
owner_acceptance_status = ACCEPTED
owner_selection_matrix_status = ACCEPTED
canonical_alignment_status = PENDING
exact_post_merge_validation_status = PENDING
C3_authorization_effect = NONE
C3_technical_work_may_begin = NO
```

### 5.2 Branch and pull-request stage

The following have no independent lifecycle effect:

```text
branch_effect = NONE
local_commit_effect = NONE
push_effect = NONE
pull_request_effect = NONE
Manager_Review_effect = NONE
pull_request_validation_effect = NONE
```

Canonical `main` remains controlling.

### 5.3 Merged but not exactly post-merge validated

After the exact authorization and activation-alignment package is squash-merged, but before successful validation on that exact canonical commit:

```text
target_C3_state_recorded = YES
C3_activation_verified = NO
C3_authorization_effect = NOT_YET_VERIFIED_EFFECTIVE
C3_technical_work_may_begin = NO
```

### 5.4 Effective activation

C3 becomes effective only when:

```text
owner_acceptance_status = ACCEPTED

owner_selection_matrix_status = ACCEPTED

every_material_owner_selection_status =
ACCEPTED_SELECTED_OPTION

authorization_decision_recorded_on_canonical_main = YES
PROJECT_CONTEXT_alignment_recorded_on_canonical_main = YES

exact_activation_changed_file_scope = PASSED
required_pull_request_validation = SUCCESS
Manager_Review_of_exact_activation_package = PASS
authorized_merge_method = SQUASH
owner_squash_merge_authorization = ISSUED
exact_post_merge_validation = SUCCESS
exact_activation_commit = RECORDED_AND_VERIFIED
```

Only then may canonical state be treated as:

```text
current_lifecycle_state = C3_ACTIVE

active_major_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

phase_status = ACTIVE
authorization_effect = C3_SCOPE_ONLY
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE

C2_completion_effect = EFFECTIVE
C4_authorization_effect = NONE

current_model_candidate = NONE
current_deployment_candidate = NONE

C3_technical_work_may_begin = YES_WITHIN_EXACT_C3_SCOPE_ONLY
```

## 6. Exact C3-selected identity inventory

The C3 inventory is limited to exactly:

```text
C1-TM-040
C1-TM-042
C1-TM-043
C1-TM-047
C1-TM-082
```

All five use:

```text
source_repository =
racoope70/ppo-trading-pipeline

source_commit =
072103f43d8b2488c3efca183f637ab0508a193a
```

### 6.1 `C1-TM-040`

```text
source_path = src/config.py
c2_disposition = SELECT_FOR_C3_ENVIRONMENT_ANALYSIS

canonical_responsibility =
Provide a typed, versioned, checksummed canonical configuration boundary.

proposed_destination_path =
src/quantitative_trading_research/config/settings.py

migration_wave =
C3-WAVE-02-ENVIRONMENT_AND_CONFIGURATION_CONTRACT
```

### 6.2 `C1-TM-042`

```text
source_path = requirements.txt
c2_disposition = SELECT_FOR_C3_ENVIRONMENT_ANALYSIS

canonical_responsibility =
Provide the starting dependency inventory for canonical C3 dependency reconstruction.

proposed_destination_path = pyproject.toml

migration_wave =
C3-WAVE-01-INTERPRETER_AND_DEPENDENCY_INVENTORY
```

### 6.3 `C1-TM-043`

```text
source_path = .env.example
c2_disposition = SELECT_FOR_C3_ENVIRONMENT_ANALYSIS

canonical_responsibility =
Provide deferred input to the canonical secret and environment-variable interface.

proposed_destination_path =
docs/configuration/environment_variables.md

migration_wave =
C3-WAVE-02-ENVIRONMENT_AND_CONFIGURATION_CONTRACT
```

### 6.4 `C1-TM-047`

```text
source_path = .github/workflows/tests.yml
c2_disposition = SELECT_FOR_C3_ENVIRONMENT_ANALYSIS

canonical_responsibility =
Provide a baseline for canonical CI while enforcing the C3-selected
Python, dependency, lock, and package-source identities.

proposed_destination_path =
.github/workflows/tests.yml

migration_wave =
C3-WAVE-03-REPRODUCIBLE-CI-AND-IMPORT-DIAGNOSTICS
```

### 6.5 `C1-TM-082`

```text
source_path =
artifacts/ppo_v2/package_preparation/v3_08_fresh_technical_diagnosis/commands/future_exact_diagnosis_command.txt

c1_classification = HISTORICAL_ARCHIVE_ONLY
c2_disposition = SELECT_FOR_C3_ENVIRONMENT_ANALYSIS

canonical_responsibility =
Serve as historical design evidence for atomic diagnostic records,
bounded probes, and fail-closed controls, not as canonical executable code.

proposed_destination_path =
src/quantitative_trading_research/config/environment_diagnostics.py

migration_wave =
C3-WAVE-03-REPRODUCIBLE-CI-AND-IMPORT-DIAGNOSTICS
```

No additional C1 identity may be silently included.

## 7. Exact C3-responsibility limitation inventory

C3 must preserve exactly:

```text
C2-LIM-C3-001
C2-LIM-C3-002
C2-LIM-C3-003
C2-LIM-C3-004
C2-LIM-C3-005
C2-LIM-C4-008
```

Every limitation enters C3 as:

```text
current_status = UNRESOLVED
current_authorization_effect = NONE
resolution_claimed_during_c2 = NO
```

### 7.1 `C2-LIM-C3-001`

No supported canonical Python interpreter or reproducible environment identity has been selected or established.

### 7.2 `C2-LIM-C3-002`

Dependency versions, package sources, resolved lock identity, and local-to-CI equivalence remain unresolved.

### 7.3 `C2-LIM-C3-003`

Historical package identities and import targets conflict or remain unavailable, so no canonical import surface is established.

### 7.4 `C2-LIM-C3-004`

Canonical configuration, environment-variable, secret, and provider-specific setting boundaries remain undefined.

### 7.5 `C2-LIM-C3-005`

The historical diagnostic command contains conflicting import targets, incorrect terminal classification logic, and workspace-specific assumptions.

### 7.6 `C2-LIM-C4-008`

C4 remains dependent on a separately accepted C3 environment, dependency identity, package-source identity, import contract, and reproducible offline test boundary.

Although this limitation has a C4-prefixed identity, its responsible future phase is C3.

Resolution of `C2-LIM-C4-008` establishes only a C4 environment entry prerequisite. It does not authorize C4.

## 8. Exact C3 entry conditions

C3 may begin only when:

```text
C2_completion_effect = EFFECTIVE

owner_C3_authorization_decision = ACCEPTED

owner_selection_matrix_id =
C3_OWNER_SELECTION_MATRIX_V1

owner_selection_matrix_status = ACCEPTED

every_material_owner_selection_status =
ACCEPTED_SELECTED_OPTION

C3_authorization_decision_repository_status =
RECORDED_ON_CANONICAL_MAIN

PROJECT_CONTEXT_alignment_status =
RECORDED_AND_VERIFIED

current_lifecycle_state = C3_ACTIVE

active_major_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

phase_status = ACTIVE
authorization_effect = C3_SCOPE_ONLY
C3_authorization_status = AUTHORIZED
C3_authorization_effect = EFFECTIVE

required_pull_request_validation = SUCCESS
Manager_Review_of_exact_activation_package = PASS
owner_squash_merge_authorization = ISSUED
required_post_merge_validation = SUCCESS
exact_C3_activation_commit = RECORDED_AND_VERIFIED
```

Additional conditions are:

1. Canonical `main` passes freshness verification.
2. The five exact C3 identities are recorded without addition or substitution.
3. The six exact limitations are recorded without omission.
4. The exact activation changed-file scope is accepted.
5. The exact technical changed-file scope is accepted.
6. The Python-selection method is accepted.
7. The two-candidate limit is accepted.
8. The permitted package-source classes are accepted.
9. The exact source allowlist is accepted.
10. The no-package-source-credential policy is accepted.
11. The dependency-constraint policy is accepted.
12. The resolver policy is accepted.
13. The lock and integrity standard is accepted.
14. The local-to-CI equivalence rule is accepted.
15. The deny-by-default network design is accepted.
16. Selective reimplementation of `C1-TM-082` is accepted.
17. The completion review and audit level is accepted.
18. The non-success lifecycle treatment is accepted.
19. The optional `PROJECT_CONTEXT.md` rename choice is accepted.
20. The exclusion of `C1-TM-039` and `.gitignore` is accepted.
21. Historical repositories remain read-only.
22. No provider, broker, market-data, account, entitlement, operational API, runtime application, dataset, model, final-holdout, order, or trading access is required.
23. Feature, label, temporal-split, leakage, embargo, calendar, and dataset-contract implementation remains prohibited.
24. The stale completion pointer correction is included in the exact alignment package.
25. No material owner selection remains unresolved.

If canonical `main` changes from the decision-basis commit before the recording branch is created, the workflow must stop for a bounded freshness review.

## 9. Minimum authorized C3 scope

Only after effective activation may C3 perform the work in this section.

### 9.1 Read-only evidence inspection

C3 may inspect:

* The canonical repository.
* The five exact selected historical identities.
* The six exact limitations.
* Accepted C1 and C2 environment-related evidence.
* Historical interpreter, dependency, configuration, CI, and diagnostic evidence.

Historical repositories must not be edited.

### 9.2 Python-policy evaluation

C3 may:

* Inventory historical Python evidence.
* Inspect required dependency compatibility information.
* Evaluate no more than two candidate Python minor versions.
* Use the same approved dependency and test policy for both candidates.
* Select one supported minor-version policy when the accepted criteria pass.
* Record exact patch identities used for evidence.
* Retain rejected and inconclusive candidate evidence.

C3 may not select a candidate using application data, features, models, evaluation, execution, providers, brokers, or trading behavior.

### 9.3 Dependency reconstruction

C3 may:

* Inventory direct dependencies.
* Resolve transitive dependencies.
* Identify conflicting, unavailable, redundant, or unsupported dependencies.
* Exclude dependencies that have no authorized C3 responsibility.
* Create `pyproject.toml`.
* Generate `requirements.lock`.
* Record resolver and package-manager identities.
* Verify the committed lock.
* Verify clean-environment repeatability.
* Compare local and CI identities.

Dependency inclusion does not authorize later application use.

### 9.4 Narrowly approved dependency acquisition

C3 may access only the exact dependency destinations in:

```text
C3_DEPENDENCY_SOURCE_ALLOWLIST_V1
```

defined in Section 10.

Network access may be used only to:

* Retrieve package-index metadata under the listed index path.
* Retrieve dependency artifacts under the listed artifact path.
* Resolve the accepted dependency set.
* Verify dependency artifact integrity.

### 9.5 Environment construction

C3 may:

* Create isolated C3 environments.
* Install dependencies only from the accepted allowlist.
* Record interpreter, platform, package-manager, resolver, package-source, dependency, and environment identities.
* Verify repeatable reconstruction.
* Verify local and CI equivalence.

### 9.6 Configuration boundary

C3 may implement only:

```text
src/quantitative_trading_research/config/settings.py
```

for:

* Typed environment-level settings.
* Versioned configuration schema.
* Deterministic configuration identity.
* Configuration checksums.
* Missing and contradictory setting rejection.
* Secret-reference boundaries without secret values.
* Deferred provider-setting classifications.
* No-import-side-effect controls.

### 9.7 Environment-variable documentation

C3 may create:

```text
docs/configuration/environment_variables.md
```

It must classify variables as:

* Required nonsecret.
* Optional nonsecret.
* Prohibited.
* Secret reference.
* Provider-specific deferred.
* Broker-specific prohibited.
* Later-phase deferred.

### 9.8 Environment diagnostics

C3 may implement only:

```text
src/quantitative_trading_research/config/environment_diagnostics.py
```

for:

* Python identity.
* Platform identity.
* Environment identity.
* Package-manager and resolver identity.
* Dependency identity.
* Package-source identity.
* Lock identity.
* Configuration identity.
* Canonical environment-level import targets.
* Structured diagnostic outcomes.
* Atomic sanitized evidence writing.

### 9.9 Focused C3 tests

C3 may create only tests for:

* Dependency identity.
* Package-source identity.
* Lock integrity.
* Configuration identity.
* Secret exclusion.
* Environment-level import targets.
* Diagnostic terminal branches.
* Atomic evidence.
* Approved-destination enforcement.
* Unapproved-network denial.
* Local-to-CI equivalence.
* Absence of application behavior.

### 9.10 C3 CI

C3 may create or modify:

```text
.github/workflows/tests.yml
```

The workflow must separate:

1. Approved dependency acquisition.
2. Network-denied canonical imports, diagnostics, configuration tests, and ordinary tests.

## 10. Exact package-source allowlist

### 10.1 Versioned allowlist identity

```text
dependency_source_allowlist_id =
C3_DEPENDENCY_SOURCE_ALLOWLIST_V1

allowlist_record_location =
docs/decisions/C3_authorization_decision.md#exact-package-source-allowlist

allowlist_version = 1
allowlist_policy = DENY_ALL_EXCEPT_EXACT_LISTED_DESTINATIONS
```

No separate allowlist file is authorized.

### 10.2 Approved package-index destination

```text
source_id = C3-PKG-SOURCE-001
source_class = PUBLIC_PACKAGE_INDEX
source_role = SIMPLE_INDEX

approved_scheme = https
approved_hostname = pypi.org
approved_port = 443
approved_path_prefix = /simple/

normalized_index_url =
https://pypi.org:443/simple/

credentials_permitted = NO
HTTP_permitted = NO
trusted_host_TLS_bypass_permitted = NO
```

### 10.3 Approved artifact destination

```text
source_id = C3-PKG-SOURCE-002
source_class = PUBLIC_ARTIFACT_HOST
source_role = PACKAGE_ARTIFACT_DOWNLOAD

approved_scheme = https
approved_hostname = files.pythonhosted.org
approved_port = 443
approved_path_prefix = /packages/

normalized_artifact_base_url =
https://files.pythonhosted.org:443/packages/

credentials_permitted = NO
HTTP_permitted = NO
trusted_host_TLS_bypass_permitted = NO
```

### 10.4 Exact allowlist enforcement

```text
alternate_index_urls_permitted = NO
extra_index_urls_permitted = NO
private_indexes_permitted = NO
mirrors_permitted = NO
prestaged_sources_permitted = NO
VCS_dependencies_permitted = NO
arbitrary_direct_URL_dependencies_permitted = NO
local_editable_dependencies_permitted = NO
redirect_to_unlisted_hostname_permitted = NO
unlisted_hostname_access_permitted = NO
```

Additional requirements:

* TLS certificate verification must remain enabled.
* Hostname, scheme, port, and path prefix form the normalized destination identity.
* Dynamic destination IP addresses are not independent approved identities.
* A redirect may proceed only when the destination remains within an exact listed scheme, hostname, port, and path prefix.
* Package-manager version checking must be disabled during acquisition to prevent unrelated destination access.
* No installer telemetry or update check may access an unlisted destination.
* The source list must be repeated exactly in the C3 environment manifest.
* Local and CI acquisition must use these same two source identities.

Any private source, mirror, prestaged source, alternate host, or additional destination requires a separate owner-authorized scope amendment.

## 11. Dependency-acquisition boundary

### 11.1 Permitted network purpose

Approved network access is limited to:

* Package-index metadata retrieval.
* Approved package-artifact retrieval.
* Dependency resolution.
* Artifact-integrity verification.

### 11.2 Mandatory restrictions

```text
network_policy = DENY_BY_DEFAULT

temporary_acquisition_allowlist =
C3_DEPENDENCY_SOURCE_ALLOWLIST_V1

provider_API_access = PROHIBITED
broker_API_access = PROHIBITED
market_data_requests = PROHIBITED
account_inspection = PROHIBITED
entitlement_inspection = PROHIBITED
authenticated_operational_API_access = PROHIBITED
runtime_application_network_activity = PROHIBITED
order_network_activity = PROHIBITED
trading_network_activity = PROHIBITED
```

### 11.3 Prohibited interpretations

Approved package acquisition is not evidence of:

* Provider acceptance.
* Broker acceptance.
* Feed acceptance.
* Entitlement acceptance.
* Market-data availability.
* Account access.
* Operational API compatibility.
* Dataset readiness.
* Model readiness.
* Deployment readiness.
* Trading readiness.

## 12. Offline execution boundary

After dependency artifacts are available:

```text
canonical_import_checks_offline = REQUIRED
configuration_tests_offline = REQUIRED
diagnostic_execution_offline = REQUIRED
ordinary_test_execution_offline = REQUIRED

network_access_during_offline_execution = DENIED

package_source_credentials_during_offline_execution = NONE
provider_credentials_during_offline_execution = NONE
broker_credentials_during_offline_execution = NONE
market_data_credentials_during_offline_execution = NONE

provider_access_during_offline_execution = NO
broker_access_during_offline_execution = NO
market_data_access_during_offline_execution = NO
account_access_during_offline_execution = NO
entitlement_access_during_offline_execution = NO
dataset_access_during_offline_execution = NO
model_execution_during_offline_execution = NO
final_holdout_access_during_offline_execution = NO
order_activity_during_offline_execution = NO
trading_activity_during_offline_execution = NO
```

The acquisition stage and offline stage must be separate workflow steps.

The offline stage must deny network access rather than relying only on code-review expectations.

## 13. Absolute C3 application-scope exclusion

Feature, label, temporal-split, leakage, embargo, calendar, and dataset-contract implementation is not authorized during C3.

C3 may create only:

* Environment-level import guards.
* Dependency-resolution tests.
* Dependency-integrity tests.
* Configuration tests.
* Offline environment diagnostics.
* Environment and dependency identity checks.

These controls must not implement or exercise:

* Application data behavior.
* Data acquisition.
* Data normalization.
* Dataset preparation.
* Dataset validation.
* Features.
* Labels.
* Temporal splits.
* Leakage controls.
* Embargo logic.
* Market calendars.
* Dataset contracts.
* Models.
* Training.
* Inference.
* Evaluation.
* Backtesting.
* Execution planning.
* Provider behavior.
* Broker behavior.
* Order behavior.
* Trading behavior.

No “strictly necessary” or similar exception is permitted.

## 14. Python-selection method

```text
python_selection_method =
BOUNDED_TWO_CANDIDATE_MINOR_VERSION_EVALUATION

candidate_minor_version_limit = 2
supported_minor_versions_after_successful_C3 = 1
```

The process must:

1. Inventory historical interpreter evidence.
2. Inventory Python compatibility requirements of authorized dependencies.
3. Identify no more than two reasonable candidate minor versions.
4. Record why each candidate was included.
5. Apply the same source allowlist to both.
6. Apply the same resolver policy to both.
7. Apply the same lock-integrity requirements to both.
8. Apply the same environment-level import contract to both.
9. Apply the same focused C3 tests to both.
10. Reject any candidate requiring prohibited application or operational activity.
11. Select one supported minor version only when the accepted criteria pass.
12. Preserve rejected and inconclusive candidate evidence.
13. Record the exact interpreter implementation and patch version used.
14. Bind the selected minor-version policy consistently into project metadata, lock evidence, local reconstruction, and CI.

## 15. Dependency-constraint and resolver policy

### 15.1 Direct dependency policy

```text
direct_dependency_record =
pyproject.toml

direct_dependency_constraint_policy =
BOUNDED_DIRECT_CONSTRAINTS_WITH_EXPLICIT_RATIONALE
```

Every direct dependency must:

* Serve an authorized C3 responsibility.
* Have an explicit constraint.
* Have recorded rationale.
* Avoid an unconstrained wildcard.
* Avoid a floating branch or mutable archive.
* Avoid a historical-repository runtime dependency.

### 15.2 Resolver policy

```text
resolver_family =
PIP_TOOLS_PIP_COMPILE

resolver_invocation_family =
python_-m_piptools_compile

resolver_version_policy =
EXACT_RESOLVER_VERSION_RECORDED_IN_C3_MANIFEST

resolver_output =
requirements.lock

resolver_hash_generation = REQUIRED
```

The resolved artifact must be generated using the accepted index allowlist and must not emit or retain an alternate index, trusted-host bypass, VCS dependency, or arbitrary direct URL.

### 15.3 Installation policy

```text
installation_invocation_family =
python_-m_pip_install

installation_input =
requirements.lock

require_hashes = YES

dependency_source_allowlist =
C3_DEPENDENCY_SOURCE_ALLOWLIST_V1
```

No dependency may be installed outside the accepted lock during canonical construction.

## 16. Lock and integrity requirements

The accepted lock must include:

* Exact package names.
* Exact resolved versions.
* Artifact hashes.
* Direct and transitive dependencies.
* Python compatibility.
* Platform markers where applicable.
* Approved source compatibility.
* Resolver identity and version.
* Generation context.
* Lock checksum.

The lock must:

* Resolve every authorized runtime and C3 test dependency.
* Reject unapproved sources.
* Prevent silent version drift.
* Be reproducible in clean local and CI environments.
* Fail closed when absent, stale, altered, unhashed, or inconsistent with `pyproject.toml`.

```text
resolved_dependency_identity_path =
requirements.lock

lock_integrity_standard =
EXACT_RESOLVED_VERSIONS_PLUS_ARTIFACT_HASHES

hash_enforcement_during_installation = REQUIRED
```

## 17. Credential and secret boundary

```text
package_source_credentials_permitted = NO
private_package_source_credentials_permitted = NO
provider_credentials_permitted = NO
broker_credentials_permitted = NO
market_data_credentials_permitted = NO
account_credentials_permitted = NO
operational_API_credentials_permitted = NO
```

No credential value may appear in:

* Git.
* `pyproject.toml`.
* `requirements.lock`.
* Documentation.
* Diagnostic evidence.
* Workflow logs.
* Test output.
* Committed environment files.

C3 may document secret-reference names and handling rules. It may not record secret values.

A future need for authenticated dependency acquisition requires a separate owner-authorized amendment and cannot be inferred from this decision.

## 18. Configuration requirements

The configuration implementation must:

* Be typed.
* Be versioned.
* Produce deterministic identity.
* Support a checksum.
* Separate nonsecret configuration from secrets.
* Reject missing required values.
* Reject unsupported values.
* Reject contradictory values.
* Reject identity mismatches.
* Avoid import-time execution.
* Avoid import-time filesystem mutation.
* Avoid import-time network activity.
* Avoid provider, broker, data, model, evaluation, execution, or trading coupling.

Provider, broker, dataset, model, holdout, execution, and trading fields may be marked only as deferred or prohibited. They must not become operational settings in C3.

## 19. `C1-TM-082` and diagnostic requirements

### 19.1 Required treatment

```text
C1_TM_082_treatment =
SELECTIVE_CLEAN_REIMPLEMENTATION_OF_DURABLE_CONTROLS_ONLY

copy_historical_command = PROHIBITED
execute_historical_command_as_canonical = PROHIBITED
automatic_historical_behavior_acceptance = NO
```

### 19.2 Required corrections

The canonical implementation must:

* Remove workspace-specific assumptions.
* Replace conflicting historical import targets.
* Correct terminal-state classification.
* Prevent an exception from producing success.
* Record Python identity.
* Record environment identity.
* Record dependency identity.
* Record package-source identity.
* Record lock identity.
* Record configuration identity.
* Record import-target identity.
* Write evidence atomically.
* Sanitize environment and path details.
* Exclude secrets.
* Run offline after acquisition.
* Fail if prohibited network activity is attempted.
* Avoid application imports or behavior.

### 19.3 Terminal outcomes

```text
PASS
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

## 20. Exact changed-file scopes

### 20.1 Authorization recording and activation alignment

May create or modify exactly:

```text
docs/decisions/C3_authorization_decision.md
PROJECT_CONTEXT.md
README.md
docs/workflows/milestone_review_reference_map.md
.github/workflows/c0-documentation-consistency.yml
```

#### `docs/decisions/C3_authorization_decision.md`

Must record:

* This accepted decision.
* `C3_OWNER_SELECTION_MATRIX_V1`.
* `C3_DEPENDENCY_SOURCE_ALLOWLIST_V1`.
* All nineteen accepted selected options.
* Exact identities, limitations, scopes, lifecycle rules, and prohibitions.

#### `PROJECT_CONTEXT.md`

May:

* Record the intended C3 active target state.
* Preserve C2 completion as effective.
* Preserve C4 and later non-authorization.
* Preserve both candidate statuses as `NONE`.
* Correct the stale pointer:

```text
latest_material_completion_record =
docs/decisions/C2_completion_decision.md
```

The correction:

* Corrects a preexisting stale pointer.
* Requires no standalone pull request.
* Does not imply C3 completion.
* Does not independently authorize technical work.

The optional field rename is not selected:

```text
latest_material_decision =
PRESERVE_EXISTING_FIELD_NAME_DURING_C3_ACTIVATION
```

#### `README.md`

May align only the high-level active-phase and non-authorization wording.

#### `docs/workflows/milestone_review_reference_map.md`

May record the accepted C3 authorization pointer while preserving the map’s non-authorizing role.

#### `.github/workflows/c0-documentation-consistency.yml`

May add only bounded decision, matrix, allowlist, lifecycle, pointer, and exact-scope validation.

It may not:

* Install project dependencies.
* Access package sources.
* Import project source.
* Execute project tests.
* Conduct technical C3 work.

### 20.2 C3 technical package

Only after effective C3 activation may create or modify exactly:

```text
pyproject.toml
requirements.lock
docs/configuration/environment_variables.md
docs/reports/C3_environment_and_dependency_manifest.yaml
docs/reports/C3_python_environment_and_dependency_reconstruction_report.md
src/quantitative_trading_research/config/settings.py
src/quantitative_trading_research/config/environment_diagnostics.py
.github/workflows/tests.yml
tests/config/test_settings.py
tests/config/test_environment_diagnostics.py
tests/environment/test_dependency_identity.py
tests/environment/test_import_contract.py
tests/environment/test_offline_boundary.py
```

No file outside the exact accepted scope may be changed without a separate owner-authorized amendment.

### 20.3 Explicit exclusions

```text
C1-TM-039 = EXCLUDED_FROM_C3
.gitignore = NO_CHANGE_AUTHORIZED
```

The scope also excludes all application data, feature, model, evaluation, artifact-runtime, execution, provider, broker, dataset, final-holdout, and trading files.

## 21. Required evidence

### 21.1 Environment and dependency manifest

```text
docs/reports/C3_environment_and_dependency_manifest.yaml
```

Must record:

```text
canonical_repository
canonical_source_commit
C3_cycle_identity
owner_selection_matrix_id
owner_selection_matrix_status
dependency_source_allowlist_id
selected_python_policy
interpreter_implementation
interpreter_version
platform_identity
environment_tool_identity
package_manager_identity
resolver_identity
resolver_version
approved_package_sources
package_source_credential_policy
dependency_metadata_checksum
lock_checksum
direct_dependency_count
resolved_dependency_count
canonical_import_targets
configuration_schema_identity
configuration_checksum
local_environment_identity
CI_environment_identity
local_CI_equivalence_result
dependency_acquisition_boundary
offline_execution_boundary
related_C3_identity_ids
related_limitation_ids
prohibited_activity_confirmation
```

### 21.2 C3 reconstruction report

```text
docs/reports/C3_python_environment_and_dependency_reconstruction_report.md
```

Must report:

* Scope performed.
* Python candidates evaluated.
* Selection or failure to select.
* Dependency inventory.
* Exact package-source destinations.
* Acquisition evidence.
* Lock and integrity evidence.
* Local reconstruction.
* CI reconstruction.
* Local-to-CI comparison.
* Offline import results.
* Configuration results.
* Diagnostic results.
* Limitation-by-limitation disposition.
* Prohibited-activity assessment.
* Terminal disposition.
* Exact commits.
* Exact workflow runs and conclusions.

### 21.3 Network-boundary evidence

Required evidence includes:

* Allowlist identity.
* Approved hostnames, protocols, ports, and path prefixes.
* Denial of every unapproved destination.
* Acquisition-step logs with secrets absent.
* Proof that imports and tests occurred in network-denied steps.
* Proof that no provider, broker, market-data, account, entitlement, order, or trading destination was accessed.

### 21.4 Integrity evidence

Required evidence includes:

* Resolver identity and version.
* Lock-generation command identity.
* Lock checksum.
* Artifact hashes.
* Hash-enforced installation result.
* Clean local reconstruction.
* Clean CI reconstruction.
* Local and CI source comparison.
* Local and CI lock comparison.

### 21.5 Evidence limitations

C3 repository and CI evidence cannot prove the absence of unrecorded external activity.

C3 evidence must not claim:

* Provider acceptance.
* Broker acceptance.
* Dataset acceptance.
* Feature correctness.
* Model readiness.
* Candidate status.
* Economic qualification.
* Deployment readiness.
* Trading readiness.

## 22. Validation, review, and audit requirements

### 22.1 Activation-alignment validation

Must verify:

* Exact five-file scope.
* Exact canonical basis.
* Exact decision identity.
* Accepted `C3_OWNER_SELECTION_MATRIX_V1`.
* All nineteen matrix entries have `ACCEPTED_SELECTED_OPTION`.
* No unresolved material selection remains.
* Exact five C3 identities.
* Exact six limitations.
* Exact allowlist destinations.
* Current C2 completion remains effective.
* C4 and later remain unauthorized.
* Both candidate statuses remain `NONE`.
* Pointer correction is exact.
* No C3 completion claim exists.
* No technical file exists in the alignment package.
* No dependency or network activity occurs.

### 22.2 Technical C3 validation

Must verify:

* Exact technical changed-file scope.
* `pyproject.toml` validity.
* Lock completeness and hashes.
* Exact source allowlist.
* No alternate package source.
* Denial of unapproved destinations.
* Local and CI source identity.
* Network denial after acquisition.
* Configuration contract.
* Diagnostic terminal branches.
* Atomic evidence.
* Secret exclusion.
* Absence of application behavior.
* Absence of provider, broker, data, model, holdout, order, and trading activity.

### 22.3 Manager Review

Manager Review is required for:

1. The proposed authorization decision before owner acceptance.
2. The exact activation-alignment package before merge.
3. The exact technical outcome package.
4. Any later C3 completion decision.

The proposed authorization decision received:

```text
manager_review_status = PERFORMED
manager_review_classification = PASS
material_findings = NONE
required_corrections = NONE
```

Manager Review has no independent authorization effect.

### 22.4 Focused independent review

A focused independent C3 review is required for every proposed terminal outcome.

#### Successful outcome

For:

```text
C3_terminal_disposition =
ACCEPTED_REPRODUCIBLE_ENVIRONMENT
```

the required field is:

```text
focused_independent_C3_completion_audit_classification = PASS
```

No other audit classification may support successful C3 completion.

#### Non-success outcomes

For:

```text
REJECTED_NO_ACCEPTABLE_ENVIRONMENT
BLOCKED_EXTERNAL_OR_OWNER_DEPENDENCY
INCONCLUSIVE
```

an independent review may validate the accuracy and evidentiary support of the non-success outcome through:

```text
focused_independent_C3_non_success_outcome_review =
REQUIRED

focused_independent_C3_non_success_outcome_review_classification =
PASS_OR_NEEDS_CORRECTION
```

A passing non-success outcome review means only that the rejection, blocker, or inconclusive conclusion is accurately supported.

It does not count as:

```text
focused_independent_C3_completion_audit_classification = PASS
```

and cannot support:

```text
current_lifecycle_state = C3_COMPLETED
C3_completion_effect = EFFECTIVE
C4_environment_entry_prerequisite = SATISFIED
```

### 22.5 Merge method

```text
authorized_recording_branch =
c3-authorization-activation-alignment

authorized_merge_method = SQUASH
direct_push_to_main = NOT_AUTHORIZED
force_push = NOT_AUTHORIZED
```

Activation and later successful completion each require exact post-merge validation on their applicable canonical commit.

## 23. Successful C3 completion conditions

C3 may reach:

```text
C3_terminal_disposition =
ACCEPTED_REPRODUCIBLE_ENVIRONMENT
```

only when all conditions below are satisfied:

1. One supported Python minor-version policy is selected.
2. Exact interpreter implementation and patch identity are recorded.
3. The accepted two-candidate method was followed.
4. The exact public source allowlist was used.
5. No unapproved source was accessed.
6. No package-source credential was used.
7. Direct dependencies are recorded.
8. Transitive dependencies are resolved.
9. Constraints are recorded.
10. The accepted resolver was used.
11. The exact resolver version is recorded.
12. A complete hashed lock exists.
13. Lock integrity passes.
14. Installation enforces hashes.
15. At least two clean constructions reproduce the accepted identity.
16. One accepted construction occurs in canonical CI.
17. Local and CI Python identities satisfy the accepted rule.
18. Local and CI dependency identities satisfy the accepted rule.
19. Local and CI package-source identities are exact matches.
20. Canonical environment-level import targets are defined.
21. Every import receives an explicit terminal result.
22. Imports run offline.
23. Configuration tests run offline.
24. Diagnostics run offline.
25. Ordinary tests run offline.
26. Network access is denied during offline execution.
27. Offline execution has no credentials.
28. Offline execution accesses no provider.
29. Offline execution accesses no broker.
30. Offline execution requests no market data.
31. Offline execution inspects no account.
32. Offline execution inspects no entitlement.
33. Offline execution accesses no dataset.
34. Offline execution executes no model.
35. Offline execution accesses no final holdout.
36. Offline execution creates or submits no order.
37. Offline execution performs no trading.
38. The typed configuration boundary passes.
39. Configuration identity and checksum pass.
40. Secret-exclusion controls pass.
41. Provider-specific operational settings remain deferred.
42. `C1-TM-082` was selectively reimplemented rather than copied.
43. Every diagnostic terminal branch is tested.
44. Exceptions cannot produce success.
45. Diagnostic evidence is atomic and sanitized.
46. No feature implementation exists.
47. No label implementation exists.
48. No temporal-split implementation exists.
49. No leakage implementation exists.
50. No embargo implementation exists.
51. No calendar implementation exists.
52. No dataset-contract implementation exists.
53. No application-data behavior is implemented or exercised.
54. No model behavior is implemented or exercised.
55. No evaluation behavior is implemented or exercised.
56. No execution behavior is implemented or exercised.
57. No provider or broker behavior is implemented or exercised.
58. No trading behavior is implemented or exercised.
59. Exact technical changed-file scope is satisfied.
60. The C3 manifest is complete.
61. The C3 report is complete.
62. All six limitations are mapped to evidence.
63. Every limitation required for successful completion is resolved by accepted evidence.
64. Pull-request validation succeeds.
65. Manager Review passes the exact outcome package.
66. The focused independent audit returns exactly:

```text
focused_independent_C3_completion_audit_classification = PASS
```

67. The owner accepts a separate successful C3 completion decision.
68. A separate completion-alignment package is squash-merged.
69. Exact post-merge completion validation succeeds.
70. C4 remains separately unauthorized.

Only after all successful conditions may canonical state record:

```text
current_lifecycle_state = C3_COMPLETED
C3_completion_effect = EFFECTIVE
active_major_phase = NONE

C4_environment_entry_prerequisite = SATISFIED
C4_authorization_effect = NONE

current_model_candidate = NONE
current_deployment_candidate = NONE
```

A green workflow, successful installation, successful import, or passing Manager Review without an independent completion-audit `PASS` is insufficient.

## 24. Terminal outcomes and lifecycle effects

The permitted terminal outcomes are:

```text
ACCEPTED_REPRODUCIBLE_ENVIRONMENT
REJECTED_NO_ACCEPTABLE_ENVIRONMENT
BLOCKED_EXTERNAL_OR_OWNER_DEPENDENCY
INCONCLUSIVE
```

### 24.1 `ACCEPTED_REPRODUCIBLE_ENVIRONMENT`

Required:

```text
C3_successful_completion = YES

focused_independent_C3_completion_audit_classification = PASS

C3_completion_effect =
EFFECTIVE_ONLY_AFTER_ACCEPTED_COMPLETION_ALIGNMENT_AND_EXACT_POST_MERGE_VALIDATION

C4_environment_entry_prerequisite =
SATISFIED_ONLY_AFTER_EFFECTIVE_C3_COMPLETION

C4_authorization_effect = NONE
current_model_candidate = NONE
current_deployment_candidate = NONE
```

This outcome establishes an environment prerequisite only. It does not authorize C4.

### 24.2 `REJECTED_NO_ACCEPTABLE_ENVIRONMENT`

Use when no authorized candidate environment satisfies the accepted requirements.

```text
C3_successful_completion = NO
C3_completion_effect = NONE

current_lifecycle_state = C3_ACTIVE

active_major_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

phase_status =
C3_REJECTED_PENDING_SEPARATE_OWNER_DISPOSITION

further_C3_technical_work =
NOT_AUTHORIZED_WITHOUT_SEPARATE_OWNER_DISPOSITION

C4_environment_entry_prerequisite = NOT_SATISFIED
C4_may_begin = NO
C4_authorization_effect = NONE

current_model_candidate = NONE
current_deployment_candidate = NONE

separate_owner_disposition_required = YES
```

Canonical state must not be aligned to `C3_COMPLETED`.

A focused independent review may confirm that the rejection is accurate, but it is not a successful completion audit.

### 24.3 `BLOCKED_EXTERNAL_OR_OWNER_DEPENDENCY`

Use when an approved source, artifact, owner decision, compatibility prerequisite, or external dependency prevents further bounded work.

```text
C3_successful_completion = NO
C3_completion_effect = NONE

current_lifecycle_state = C3_ACTIVE

active_major_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

phase_status =
C3_BLOCKED_PENDING_SEPARATE_OWNER_DISPOSITION

further_C3_technical_work =
NOT_AUTHORIZED_WITHOUT_SEPARATE_OWNER_DISPOSITION

C4_environment_entry_prerequisite = NOT_SATISFIED
C4_may_begin = NO
C4_authorization_effect = NONE

current_model_candidate = NONE
current_deployment_candidate = NONE

separate_owner_disposition_required = YES
```

Canonical state must not be aligned to `C3_COMPLETED`.

### 24.4 `INCONCLUSIVE`

Use when evidence is insufficient to accept or reject a reproducible canonical environment.

```text
C3_successful_completion = NO
C3_completion_effect = NONE

current_lifecycle_state = C3_ACTIVE

active_major_phase =
C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION

phase_status =
C3_INCONCLUSIVE_PENDING_SEPARATE_OWNER_DISPOSITION

further_C3_technical_work =
NOT_AUTHORIZED_WITHOUT_SEPARATE_OWNER_DISPOSITION

C4_environment_entry_prerequisite = NOT_SATISFIED
C4_may_begin = NO
C4_authorization_effect = NONE

current_model_candidate = NONE
current_deployment_candidate = NONE

separate_owner_disposition_required = YES
```

Canonical state must not be aligned to `C3_COMPLETED`.

### 24.5 Later owner disposition after non-success

After a rejected, blocked, or inconclusive outcome, the owner may separately choose an appropriately bounded action such as:

```text
PRESERVE_C3_AS_BLOCKED_PENDING_A_PREREQUISITE
STOP_CURRENT_RESEARCH_CYCLE
AUTHORIZE_A_SEPARATE_BOUNDED_REDESIGN
REQUEST_ADDITIONAL_EVIDENCE_UNDER_SEPARATE_AUTHORIZATION
```

No non-success outcome automatically authorizes:

* Additional dependency sources.
* Additional credentials.
* More Python candidates.
* A redesign.
* Additional technical execution.
* C4.
* Any later phase.

## 25. C3 owner-selection matrix

```text
owner_selection_matrix_id =
C3_OWNER_SELECTION_MATRIX_V1

matrix_status = ACCEPTED
```

### OSM-01 — C3 authorization

```text
owner_decision_required = YES

selected_option =
ACCEPT_BOUNDED_C3_AUTHORIZATION_DEFINED_BY_GOV_DEC_0007

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
REJECT_C3_AUTHORIZATION;
DEFER_C3_AUTHORIZATION;
RETURN_DRAFT_FOR_CORRECTION

technical_rationale =
C2 is effectively completed and the accepted handoff identifies a reproducible
Python environment as the required prerequisite before any future C4 work.

authorization_consequence =
Acceptance permits only the controlled activation-alignment workflow initially.
Technical work remains prohibited until activation is effective.
```

### OSM-02 — Python-selection method

```text
owner_decision_required = YES

selected_option =
BOUNDED_TWO_CANDIDATE_MINOR_VERSION_EVALUATION

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
OWNER_PRESELECTS_ONE_MINOR_VERSION;
ONE_CANDIDATE_ONLY;
THREE_CANDIDATE_LIMIT

technical_rationale =
Two candidates provide bounded compatibility comparison without creating an
open-ended multi-version support project.

authorization_consequence =
No more than two candidate minor versions may be evaluated.
```

### OSM-03 — Candidate-version limit and successful policy

```text
owner_decision_required = YES

selected_option =
MAXIMUM_TWO_CANDIDATE_MINOR_VERSIONS_AND_ONE_SUPPORTED_MINOR_VERSION_AFTER_SUCCESS

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
ONE_CANDIDATE_AND_ONE_SUPPORTED_MINOR;
MULTIPLE_SUPPORTED_MINOR_VERSIONS;
EXACT_PATCH_ONLY_POLICY

technical_rationale =
One supported minor version minimizes environment drift while exact patch identities
remain recorded in evidence.

authorization_consequence =
C3 cannot evaluate an additional candidate without separate authorization.
```

### OSM-04 — Permitted source classes

```text
owner_decision_required = YES

selected_option =
PUBLIC_OFFICIAL_PYPI_SOURCE_CLASS_ONLY

selection_status = ACCEPTED_SELECTED_OPTION

public_sources = PERMITTED_AT_EXACT_ALLOWLIST
private_sources = NOT_PERMITTED
mirrors = NOT_PERMITTED
prestaged_sources = NOT_PERMITTED

reasonable_alternatives =
PRESTAGED_ONLY;
APPROVED_PRIVATE_INDEX;
APPROVED_MIRROR;
MIXED_EXACTLY_LISTED_SOURCES

technical_rationale =
One exact public source class provides the smallest initial provenance and credential boundary.

authorization_consequence =
No private, mirrored, prestaged, alternate, or supplemental source may be used.
```

### OSM-05 — Exact source destinations

```text
owner_decision_required = YES

selected_option =
C3_DEPENDENCY_SOURCE_ALLOWLIST_V1

selection_status = ACCEPTED_SELECTED_OPTION

accepted_destinations =
https://pypi.org:443/simple/
https://files.pythonhosted.org:443/packages/

reasonable_alternatives =
A_DIFFERENT_EXACT_VERSIONED_ALLOWLIST;
PRESTAGED_NO_NETWORK_ALLOWLIST;
PRIVATE_SOURCE_ALLOWLIST

technical_rationale =
Exact scheme, hostname, port, and path-prefix identities are enforceable and avoid
the ambiguity of referring generally to official artifact hosts.

authorization_consequence =
Every unlisted network destination remains denied.
```

### OSM-06 — Package-source credentials

```text
owner_decision_required = YES

selected_option =
NO_PACKAGE_SOURCE_CREDENTIALS

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
NARROW_READ_ONLY_PRIVATE_INDEX_TOKEN;
SHORT_LIVED_CI_IDENTITY;
OWNER_PRESTAGED_AUTHENTICATED_ARTIFACTS

technical_rationale =
The selected public allowlist requires no credential and avoids unnecessary secret risk.

authorization_consequence =
C3 may not access any authenticated dependency source.
```

### OSM-07 — Direct dependency constraints

```text
owner_decision_required = YES

selected_option =
BOUNDED_DIRECT_CONSTRAINTS_WITH_EXPLICIT_RATIONALE_IN_PYPROJECT

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
EXACT_DIRECT_PINS;
MINIMUM_ONLY_CONSTRAINTS_WITH_LOCK;
OWNER_SELECTED_COMPATIBLE_RELEASE_POLICY

technical_rationale =
Bounded direct constraints preserve declared intent while the lock records the exact resolution.

authorization_consequence =
Every direct dependency must have an accepted bounded constraint and rationale.
```

### OSM-08 — Resolver policy

```text
owner_decision_required = YES

selected_option =
PIP_TOOLS_PIP_COMPILE_WITH_EXACT_TOOL_VERSION_RECORDED

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
OWNER_SELECTED_EQUIVALENT_HASH_CAPABLE_RESOLVER;
UV_LOCK;
POETRY_LOCK;
EXACT_MANUAL_RESOLUTION

technical_rationale =
A declared resolver family with exact tool identity supports deterministic lock generation
and reviewable hash output.

authorization_consequence =
Only this resolver family may generate the canonical C3 lock.
```

### OSM-09 — Lock and integrity standard

```text
owner_decision_required = YES

selected_option =
REQUIREMENTS_LOCK_WITH_EXACT_RESOLVED_VERSIONS_AND_ARTIFACT_HASHES

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
EQUIVALENT_TOOL_SPECIFIC_HASHED_LOCK;
SIGNED_INTERNAL_ARTIFACT_MANIFEST;
CHECKSUMMED_PRESTAGED_WHEELHOUSE_MANIFEST

technical_rationale =
Exact versions and artifact hashes prevent silent transitive or artifact drift.

authorization_consequence =
An unhashed, incomplete, stale, or nonreproducible lock cannot satisfy C3 completion.
```

### OSM-10 — Local-to-CI equivalence

```text
owner_decision_required = YES

selected_option =
EXACT_MATCH_OF_PYTHON_MINOR_POLICY_LOCK_CHECKSUM_AND_PACKAGE_SOURCE_IDENTITIES

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
ARTIFACT_HASH_EQUIVALENCE_ACROSS_APPROVED_MIRRORS;
PLATFORM_SPECIFIC_LOCKS_WITH_EXPLICIT_EQUIVALENCE;
CI_PRESTAGED_AND_LOCAL_PUBLIC_HASH_EQUIVALENCE

technical_rationale =
Exact source and lock matching provides the strongest simple reproducibility rule.

authorization_consequence =
A build using a different source identity or lock checksum fails equivalence.
```

### OSM-11 — Network enforcement

```text
owner_decision_required = YES

selected_option =
DENY_BY_DEFAULT_EGRESS_WITH_TEMPORARY_ACQUISITION_ALLOWLIST_AND_NETWORK_DENIED_OFFLINE_STEPS

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
PRESTAGED_DEPENDENCIES_WITH_NO_NETWORK;
SEPARATE_ACQUISITION_AND_OFFLINE_CI_JOBS;
OWNER_SELECTED_EQUIVALENT_DENY_BY_DEFAULT_CONTROL

technical_rationale =
Enforcement distinguishes legitimate package retrieval from prohibited application
or operational network behavior.

authorization_consequence =
C3 evidence is unacceptable without approved-destination enforcement and offline-step denial.
```

### OSM-12 — `C1-TM-082` treatment

```text
owner_decision_required = YES

selected_option =
SELECTIVE_CLEAN_REIMPLEMENTATION_OF_DURABLE_CONTROLS_ONLY

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
HISTORICAL_REFERENCE_ONLY_WITH_NO_REIMPLEMENTATION;
NARROWER_DIAGNOSTIC_SUBSET;
DEFER_DIAGNOSTICS

technical_rationale =
The historical command has accepted defects and workspace assumptions.

authorization_consequence =
The historical command may not be copied or executed as canonical implementation.
```

### OSM-13 — Activation changed-file scope

```text
owner_decision_required = YES

selected_option =
EXACT_FIVE_FILE_ACTIVATION_SCOPE_IN_SECTION_20_1

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
RETURN_FOR_NARROWER_ALIGNMENT_SCOPE;
REMOVE_OPTIONAL_README_ALIGNMENT;
SEPARATE_FUTURE_MAP_UPDATE

technical_rationale =
The five files are sufficient to record the decision, controlling state, roadmap pointer,
high-level status, and bounded validation.

authorization_consequence =
No file outside Section 20.1 may change during activation alignment.
```

### OSM-14 — Technical changed-file scope

```text
owner_decision_required = YES

selected_option =
EXACT_THIRTEEN_FILE_TECHNICAL_SCOPE_IN_SECTION_20_2

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
REMOVE_NONESSENTIAL_TEST_PATHS;
USE_AN_EQUIVALENT_OWNER_SELECTED_LOCK_PATH;
RETURN_FOR_A_NARROWER_SCOPE

technical_rationale =
The scope contains only dependency, configuration, diagnostics, evidence, CI, and focused tests.

authorization_consequence =
No application or unlisted file may change during C3.
```

### OSM-15 — Completion review and audit

```text
owner_decision_required = YES

selected_option =
MANAGER_REVIEW_PLUS_FOCUSED_INDEPENDENT_C3_REVIEW_WITH_AUDIT_PASS_REQUIRED_FOR_SUCCESS

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
MANAGER_REVIEW_ONLY;
FULL_REPOSITORY_WIDE_AUDIT;
INDEPENDENT_REVIEW_ONLY

technical_rationale =
Environment, dependency-source, lock, credential, and CI defects could contaminate every
later phase, but a full governance-system audit is disproportionate.

authorization_consequence =
ACCEPTED_REPRODUCIBLE_ENVIRONMENT requires
focused_independent_C3_completion_audit_classification = PASS.
```

### OSM-16 — Non-success outcome treatment

```text
owner_decision_required = YES

selected_option =
PRESERVE_REJECTED_BLOCKED_AND_INCONCLUSIVE_OUTCOMES_WITH_NO_COMPLETION_EFFECT_AND_SEPARATE_OWNER_DISPOSITION

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
ACCEPT_OR_REJECT_ONLY;
BLOCKED_REMAINS_NONTERMINAL_WITH_SEPARATE_DECISION;
STOP_AUTOMATICALLY_AFTER_ANY_NON_SUCCESS

technical_rationale =
Explicit evidence-preserving outcomes prevent forced acceptance and unauthorized continuation.

authorization_consequence =
No non-success outcome permits C3_COMPLETED, C4 entry, redesign, additional sources,
or further technical work without a separate owner decision.
```

### OSM-17 — Optional `PROJECT_CONTEXT.md` rename

```text
owner_decision_required = YES

selected_option =
DO_NOT_RENAME_LATEST_MATERIAL_DECISION_DURING_C3_ACTIVATION

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
RENAME_TO_LATEST_MATERIAL_AUTHORIZATION_DECISION;
DEFER_RENAME_TO_LATER_MAINTENANCE

technical_rationale =
The completion-pointer correction is material; the rename is clarity-only.

authorization_consequence =
Only the stale completion pointer is corrected during activation alignment.
```

### OSM-18 — `C1-TM-039` and `.gitignore`

```text
owner_decision_required = YES

selected_option =
EXCLUDE_C1_TM_039_FROM_C3_AND_AUTHORIZE_NO_GITIGNORE_CHANGE

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
SEPARATE_FUTURE_GITIGNORE_DISPOSITION;
LATER_REPOSITORY_HYGIENE_SCOPE;
RETAIN_HISTORICAL_ONLY

technical_rationale =
C1-TM-039 is not one of the accepted five C3-selected identities.

authorization_consequence =
No .gitignore creation or modification is authorized by GOV-DEC-0007.
```

### OSM-19 — Merge method and main-branch protection

```text
owner_decision_required = YES

selected_option =
SQUASH_MERGE_ONLY_WITH_NO_DIRECT_PUSH_AND_NO_FORCE_PUSH

selection_status = ACCEPTED_SELECTED_OPTION

reasonable_alternatives =
MERGE_COMMIT_AFTER_SEPARATE_APPROVAL;
REBASE_MERGE_AFTER_SEPARATE_APPROVAL

technical_rationale =
Squash merging preserves one exact canonical transition identity consistent with prior phases.

authorization_consequence =
A different merge method or direct main update requires separate owner authorization.
```

## 26. Exact prohibited scope

C3 does not authorize:

* Editing historical repositories.
* Modifying accepted C1 evidence.
* Reclassifying accepted evidence.
* Copying historical executable source wholesale.
* Treating historical dependencies as accepted.
* Treating historical environment success as canonical.
* Copying or executing `C1-TM-082` as canonical source.
* Adding `C1-TM-039`.
* Creating or modifying `.gitignore`.
* Migrating C4 application code.
* Data acquisition.
* Data normalization.
* Dataset preparation.
* Dataset validation.
* Feature implementation.
* Label implementation.
* Temporal-split implementation.
* Leakage implementation.
* Embargo implementation.
* Calendar implementation.
* Dataset-contract implementation.
* Application-data execution.
* Provider selection or acceptance.
* Broker selection or acceptance.
* Feed or entitlement acceptance.
* Provider API access.
* Broker API access.
* Market-data requests.
* Account inspection.
* Entitlement inspection.
* Authenticated operational API testing.
* Runtime application network activity.
* Provider connectivity.
* Broker connectivity.
* Dataset selection, generation, reconstruction, modification, remediation, imputation, or acceptance.
* PPO, Random Forest, XGBoost, or hybrid-gate implementation.
* Training or retraining.
* Inference.
* Validation.
* Evaluation.
* Backtesting.
* Candidate qualification, freezing, rejection, or promotion.
* Model-artifact creation.
* Final-holdout access.
* Current model-candidate creation.
* Current deployment-candidate creation.
* Execution-plan implementation.
* Order construction or submission.
* Paper orders.
* Live orders.
* Paper trading.
* Live trading.
* Publication-readiness claims.
* Deployment-readiness claims.
* Profitability or economic-qualification claims.
* Live-capital claims.
* C4 or later-phase activation.
* Any network destination outside `C3_DEPENDENCY_SOURCE_ALLOWLIST_V1`.
* Network access during imports, diagnostics, configuration tests, or ordinary tests.
* Credential reuse for any operational purpose.
* Committing any credential or secret.
* Treating the pointer correction as C3 completion.
* Treating the pointer correction as technical authorization.

During the authorization-recording and activation-alignment workflow specifically, no package-source access, dependency installation, environment creation, source import, source execution, or technical C3 test is authorized.

## 27. Continuing C4-and-later non-authorization

Even after effective C3 activation:

```text
C4_authorization_status = NOT_AUTHORIZED
C4_authorization_effect = NONE

provider_acceptance_status = NONE
market_data_access = NOT_AUTHORIZED
dataset_generation_status = NOT_AUTHORIZED

model_implementation = NOT_AUTHORIZED
model_training = NOT_AUTHORIZED
model_validation = NOT_AUTHORIZED
final_holdout_access = NOT_AUTHORIZED

broker_account_access = NOT_AUTHORIZED
paper_order_activity = NOT_AUTHORIZED
live_order_activity = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE
```

Successful C3 completion may satisfy only:

```text
C4_environment_entry_prerequisite = SATISFIED
```

It does not authorize C4 itself.

## 28. Repository recording and activation boundary

The authorization-recording and activation-alignment package is limited to exactly:

```text
docs/decisions/C3_authorization_decision.md
PROJECT_CONTEXT.md
README.md
docs/workflows/milestone_review_reference_map.md
.github/workflows/c0-documentation-consistency.yml
```

```text
authorized_recording_branch =
c3-authorization-activation-alignment

authorized_merge_method = SQUASH
direct_push_to_main = NOT_AUTHORIZED
force_push = NOT_AUTHORIZED
```

The Future Validation and Training Reference Map remains unchanged unless a separate material inconsistency is identified and separately authorized.

The decision-record branch, local commit, push, pull request, Manager Review result, or pull-request validation does not independently activate C3.

A merged but not exactly post-merge validated canonical commit does not independently make C3 effective.

C3 becomes effective only through the exact aligned canonical squash merge and successful required post-merge validation on that exact commit.

## 29. Accepted owner command and non-effects

The owner issued:

```text
ACCEPT_GOV_DEC_0007_WITH_ALL_PROPOSED_SELECTED_OPTIONS_IN_C3_OWNER_SELECTION_MATRIX_V1_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C3_ACTIVATION_ALIGNMENT
```

This command accepts:

* `GOV-DEC-0007`.
* `C3_OWNER_SELECTION_MATRIX_V1`.
* All nineteen selected options.
* The exact five-file authorization-recording and activation-alignment workflow.
* Required pull-request validation.
* Manager Review of the exact activation package.
* A later separately owner-authorized squash merge.
* Exact post-merge activation validation.

The command does not independently:

* Create a branch.
* Commit or push files.
* Open or merge a pull request.
* Activate C3 before exact post-merge validation.
* Install dependencies.
* Access package sources.
* Create an environment.
* Run imports, diagnostics, or tests.
* Begin technical C3 work.
* Authorize C4 or any later phase.

```text
current_lifecycle_state_before_effective_activation = C2_COMPLETED
C2_completion_effect = EFFECTIVE
active_major_phase_before_effective_activation = NONE
authorization_effect_before_effective_activation = NONE
C3_authorization_effect_before_effective_activation = NONE
C4_authorization_effect = NONE
current_model_candidate = NONE
current_deployment_candidate = NONE
```
