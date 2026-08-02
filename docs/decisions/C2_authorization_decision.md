# C2 Authorization Decision

```text
document_status = ACCEPTED_C2_AUTHORIZATION_DECISION
intended_repository_path = docs/decisions/C2_authorization_decision.md
decision_id = GOV-DEC-0005
decision_type = C2_PHASE_AUTHORIZATION
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED
owner_decision = ACCEPT_GOV_DEC_0005_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_ACTIVATION_ALIGNMENT
authorized_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
authorized_scope = C2_NON_OPERATIONAL_SKELETON_AND_MIGRATION_PREPARATION_ONLY
authorization_effect = C2_SCOPE_ONLY
C2_activation_effect = EFFECTIVE_ONLY_WITH_ALIGNED_CANONICAL_MAIN
C3_authorization_effect = NONE
curated_record = 2v.GOV.06
decision_basis_commit = 8e8fe0d0fb66dddd2e73e5024add796c7004eab9
manager_review_status = PERFORMED
manager_review_classification = PASS
material_findings = NONE
required_corrections = NONE
accepted_C1_artifacts = IMMUTABLE
current_model_candidate = NONE
current_deployment_candidate = NONE
repository_recording_status = RECORDED_AND_ALIGNED
```

## 1. Purpose and authorization effect

This decision records the owner’s accepted authorization for:
C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
The owner issued:
owner_decision =
ACCEPT_GOV_DEC_0005_AND_AUTHORIZE_CONTROLLED_REPOSITORY_RECORDING_AND_C2_ACTIVATION_ALIGNMENT
C2 is limited to:
* A non-operational canonical repository skeleton.
* Package and subsystem responsibility boundaries.
* Documented interface boundaries.
* Migration preparation using accepted C1 manifest identities.
* Proposed destination paths and migration waves.
* Future verification planning.
* A bounded C3 environment-reconstruction handoff.
C2 is a preparation phase. It is not an executable migration, environment, provider, data, model, validation, final-holdout, broker, or trading phase.
This decision has no lifecycle effect merely because it exists on a branch or in a pull request.
C2 becomes effective only when this accepted decision and the aligned controlling state are merged together to canonical main and the required validation succeeds.
## 2. Canonical repository and controlling basis

repository = racoope70/quantitative-trading-research-platform
repository_visibility = PRIVATE
canonical_branch = main
exact_decision_basis_commit = 8e8fe0d0fb66dddd2e73e5024add796c7004eab9
C1_completion_effect = EFFECTIVE
C2_authorization_status_before_alignment = NOT_AUTHORIZED
PROJECT_CONTEXT.md remains the sole controlling source for:
* Lifecycle state.
* Active phase.
* Authorization effect.
* Authorized and prohibited work.
* Dataset, environment, access, model, and candidate status.
* The next permitted workstream.
The accepted supporting basis is:
1. PROJECT_CONTEXT.md.
2. docs/decisions/C1_completion_decision.md.
3. docs/migration/legacy_evidence_retention_matrix.csv.
4. docs/migration/technical_migration_manifest.yaml.
5. docs/reports/C1_legacy_evidence_and_architecture_report.md.
6. docs/audits/C1_independent_legacy_evidence_and_architecture_audit_report.md.
7. docs/workflows/milestone_review_reference_map.md.
8. docs/workflows/future_validation_training_reference_map.md.
9. The fresh Manager Review classification PASS.
10. The owner’s seven explicit C2 selections.
The milestone and future maps remain non-authorizing guidance and evidence-navigation records.
Historical repositories remain evidence and engineering sources. They do not become runtime dependencies or sources of current authorization.
## 3. Accepted owner selections

### 3.1 Skeleton implementation level

selected_option =
OPTION_A_PLUS_EMPTY_PACKAGE_MARKERS

documentation_boundary_files =
AUTHORIZED

empty_package_markers =
AUTHORIZED_AT_EXACT_LISTED_PATHS

abstract_interface_stubs =
NOT_AUTHORIZED
### 3.2 Accepted C1 artifacts

selected_option =
KEEP_ACCEPTED_C1_ARTIFACTS_IMMUTABLE_AND_CREATE_SEPARATE_C2_PLAN

accepted_C1_artifacts =
IMMUTABLE

separate_C2_plan =
docs/migration/C2_migration_disposition_plan.yaml
Modification of an accepted C1 artifact requires a separately authorized material-correction process and is outside C2.
### 3.3 Manifest disposition depth

selected_option =
HIGH_LEVEL_DISPOSITION_FOR_ALL_82_ITEMS_WITH_FULL_PLANNING_ONLY_FOR_C3_C4_ITEMS

all_82_C1_manifest_items =
HIGH_LEVEL_ACCOUNTING_REQUIRED

C3_C4_relevant_items =
FULL_DESTINATION_WAVE_LIMITATION_AND_VERIFICATION_PLANNING_REQUIRED

later_phase_items =
EXPLICIT_HIGH_LEVEL_DEFERRAL_REQUIRED
### 3.4 Canonical package and subsystem boundaries

canonical_package_name =
quantitative_trading_research

canonical_package_root =
src/quantitative_trading_research

major_subsystems =
config
data
features
models
evaluation
artifacts
execution
### 3.5 C2 continuous integration

selected_option =
UPDATE_EXISTING_DOCUMENTATION_WORKFLOW_FOR_BOUNDED_DOCUMENT_STRUCTURE_AND_YAML_VALIDATION

workflow_path =
.github/workflows/c0-documentation-consistency.yml

parallel_C2_workflow =
NOT_AUTHORIZED
### 3.6 Minimum C2 output package

selected_option =
THREE_CORE_C2_DOCUMENTS_PLUS_APPROVED_SKELETON_FILES

new_template_framework =
NOT_AUTHORIZED

additional_governance_system =
NOT_AUTHORIZED
### 3.7 Provider and broker interface treatment

selected_option =
DOCUMENTATION_ONLY_UNTIL_C4

abstract_interface_stubs_during_C2 =
NOT_AUTHORIZED

provider_specific_implementation_during_C2 =
NOT_AUTHORIZED

broker_specific_implementation_during_C2 =
NOT_AUTHORIZED
## 4. Exact C2 entry conditions

C2 may begin only when:
C1_completion_effect = EFFECTIVE
owner_C2_authorization_decision = ACCEPTED
authorization_decision_repository_status = RECORDED_ON_CANONICAL_MAIN
PROJECT_CONTEXT_alignment_status = RECORDED_AND_VERIFIED
current_lifecycle_state = C2_ACTIVE
active_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
phase_status = ACTIVE
authorization_effect = C2_SCOPE_ONLY
C2_authorization_status = AUTHORIZED
C2_activation_status = ACTIVE
required_pull_request_validation = SUCCESS
required_post_merge_validation = SUCCESS
exact_C2_activation_commit = RECORDED_AND_VERIFIED
If canonical main moves from the decision-basis commit before the recording branch is created, the workflow must stop for freshness review.
No C2 implementation action may begin from:
* This decision file on a local branch.
* A local commit.
* A pushed branch.
* An open pull request.
* Successful pull-request CI alone.
## 5. Exact authorized C2 scope

### 5.1 Read-only evidence inspection

C2 may inspect read-only:
* The canonical repository.
* The accepted C1 completion evidence.
* The three accepted C1 outputs.
* Exact historical source records only when Section 10 permits them.
Historical repositories must not be edited.
### 5.2 Non-operational canonical skeleton

C2 may create only the exact skeleton files listed in Section 7.
Responsibility documents may define:
* Canonical responsibility.
* Permitted future contents.
* Prohibited coupling.
* Dependency direction.
* Provider-neutral and broker-neutral boundaries.
* Responsible future phase.
* Required future verification.
They may not implement those responsibilities.
Empty package markers may contain:
* No content; or
* One optional module docstring.
They may contain no:
* Imports.
* Initialization behavior.
* Side effects.
* Compatibility logic.
* Dependency checks.
* Version detection.
* Registration.
* Runtime behavior.
### 5.3 Authoritative YAML collections

The C2 migration-disposition plan must use exactly:
items =
THE_AUTHORITATIVE_TOP_LEVEL_C1_ITEM_COLLECTION

unresolved_limitations =
THE_AUTHORITATIVE_TOP_LEVEL_LIMITATION_COLLECTION
The exact top-level YAML structure is:
items: []
unresolved_limitations: []
No alternative, duplicate, singular, or differently capitalized collection key is permitted.
### 5.4 Item accounting and migration preparation

Every accepted C1 technical migration manifest identity must appear once in items.
Each item must:
* Use its accepted c1_item_id.
* Preserve its exact source repository.
* Preserve its full immutable source commit.
* Preserve its exact source path.
* Preserve its C1 classification.
* Preserve or define its canonical responsibility.
* Receive a high-level C2 disposition.
* Link applicable limitations through related_limitation_ids.
* Record future_verification_requirements.
* Identify its responsible future phase.
* Receive detailed destination and wave planning only when C3/C4 relevant.
Permitted high-level dispositions are:
SELECT_FOR_C3_ENVIRONMENT_ANALYSIS
SELECT_FOR_C4_MIGRATION_PREPARATION
DEFER_TO_C5_PROVIDER_DECISION
DEFER_TO_C6_DATASET_CONTRACT
DEFER_TO_C7_DATASET_GENERATION
DEFER_TO_C8_MODEL_READINESS
DEFER_TO_C9_PPO_QUALIFICATION
DEFER_TO_C10_RF_GATE
DEFER_TO_C11_XGBOOST_GATE
DEFER_TO_C12_FINAL_HOLDOUT
DEFER_TO_C13_PUBLICATION
DEFER_TO_C14_PAPER_TRADING
DEFER_TO_C15_LIVE_CONSIDERATION
RETAIN_HISTORICAL_ONLY
REJECT_FROM_CANONICAL_MIGRATION
DEFER_PENDING_OWNER_DECISION
DEFER_PENDING_IMMUTABLE_PROVENANCE
A disposition prepares future work. It does not authorize the assigned future phase.
### 5.5 Unresolved-limitation register

The unresolved_limitations collection must use:
unresolved_limitations:
  - limitation_id:
    related_c1_item_ids: []
    source_c1_evidence: []
    limitation_statement:
    current_status: UNRESOLVED
    responsible_future_phase:
    future_verification_requirements: []
    current_authorization_effect: NONE
    resolution_claimed_during_c2: NO
    notes:
Each material limitation must appear once.
One limitation may link to several C1 items.
Repeated copies of the same full limitation record are not required under every item.
Required fixed values are:
current_status = UNRESOLVED
current_authorization_effect = NONE
resolution_claimed_during_c2 = NO
### 5.6 Referential integrity

Every value in:
items[*].related_limitation_ids
must resolve to a valid:
unresolved_limitations[*].limitation_id
Every value in:
unresolved_limitations[*].related_c1_item_ids
must resolve to a valid:
items[*].c1_item_id
Validation must use the exact normalized, case-sensitive keys.
No unresolved reference is permitted.
### 5.7 Destination paths and migration waves

C2 may propose destination paths and migration waves for C3/C4-relevant items.
A proposed destination path or migration wave:
* Is not migration.
* Is not asset acceptance.
* Is not proof of correctness.
* Is not proof of parity.
* Does not resolve provenance.
* Does not resolve a limitation.
* Does not create a candidate.
* Does not authorize later implementation.
### 5.8 Future verification planning

C2 may document future requirements for:
* Static structure checks.
* Import and responsibility boundaries.
* Interface contracts.
* Synthetic and mocked testing.
* Fail-closed behavior.
* Chronological ordering, leakage, and embargo controls.
* Schema and dtype checks.
* Artifact, dataset, environment, configuration, and run identity.
* Notebook-to-module lineage.
* Numerical and behavioral parity.
* Provider-neutral and broker-neutral offline verification.
C2 may not execute those future project tests.
### 5.9 Bounded C3 handoff

C2 may prepare a C3 handoff identifying:
* Candidate Python versions for later evaluation.
* Historical interpreter evidence.
* Historical dependency sources.
* Dependency conflicts.
* Conflicting or unavailable import surfaces.
* Clean-environment requirements.
* Dependency-lock requirements.
* Import-smoke-test requirements.
* C3 limitation IDs.
* Applicable source_c1_evidence.
* Applicable future_verification_requirements.
C2 may not select Python, install dependencies, create an environment, resolve imports, create a lock, or execute compatibility checks.
### 5.10 Bounded workflow-contained validation

C2 may update:
.github/workflows/c0-documentation-consistency.yml
The workflow may use bounded inline Python, Ruby, shell, or equivalent standard-runner logic only for:
* Markdown paths and required sections.
* YAML parsing.
* Exact items and unresolved_limitations collection checks.
* Required normalized-field checks.
* Unique c1_item_id checks.
* Unique limitation_id checks.
* Required fixed-value checks.
* source_c1_evidence checks.
* Responsible-future-phase checks.
* future_verification_requirements checks.
* Bidirectional referential-integrity checks.
* Duplicate C1 identity detection.
* Full commit-format checks.
* Path-format checks.
* Repository-structure checks.
* Prohibited-content checks.
* Internal lifecycle-field consistency checks.
Workflow validation must:
* Treat YAML keys as case-sensitive.
* Reject inconsistent singular, plural, prefix, or capitalization variants.
* Use only runner-provided or already available standard tooling.
* Install no dependency.
* Create no project environment.
* Import no canonical project module.
* Import no historical project module.
* Execute no canonical project source.
* Execute no historical project source.
* Run no project test, notebook, CLI, model, adapter, or data pipeline.
* Access no network, provider, broker, credential, market data, or dataset.
## 6. Exact prohibited scope

C2 does not authorize:
* Editing a historical repository.
* Modifying an accepted C1 artifact.
* Reclassifying accepted C1 evidence without separate material-correction authorization.
* Copying or adapting executable legacy code.
* Reimplementing technical behavior.
* Creating abstract interface stubs.
* Creating provider-specific or broker-specific implementation.
* Importing or executing canonical or historical project source.
* Running project tests, scripts, notebooks, CLIs, training, validation, evaluation, or backtests.
* Selecting Python.
* Installing dependencies.
* Creating an environment.
* Resolving dependency or import conflicts.
* Selecting or accepting a provider or feed.
* Credentials, network access, API access, entitlement checks, or market-data requests.
* Selecting or accepting a dataset.
* Dataset generation, reconstruction, modification, imputation, remediation, or completeness execution.
* Selecting the final ticker universe.
* Implementing PPO, Random Forest, XGBoost, or a hybrid gate.
* Creating features, labels, trained artifacts, or current candidates.
* Training, validation, qualification, freezing, rejection, promotion, or final-holdout access.
* Broker-account access.
* Paper orders, live orders, paper trading, or live trading.
* Activating C3 or a later phase.
* Publication, deployment-readiness, profitability, or live-capital claims.
## 7. Exact C2 changed-file scope

### 7.1 Principal C2 outputs

C2 may create exactly:
docs/architecture/C2_canonical_repository_skeleton_and_boundaries.md
docs/migration/C2_migration_disposition_plan.yaml
docs/reports/C2_migration_preparation_and_C3_handoff.md
### 7.2 Skeleton responsibility documents

C2 may create exactly:
src/quantitative_trading_research/README.md
src/quantitative_trading_research/config/README.md
src/quantitative_trading_research/data/README.md
src/quantitative_trading_research/features/README.md
src/quantitative_trading_research/models/README.md
src/quantitative_trading_research/evaluation/README.md
src/quantitative_trading_research/artifacts/README.md
src/quantitative_trading_research/execution/README.md
tests/README.md
### 7.3 Empty package markers

C2 may create exactly:
src/quantitative_trading_research/__init__.py
src/quantitative_trading_research/config/__init__.py
src/quantitative_trading_research/data/__init__.py
src/quantitative_trading_research/features/__init__.py
src/quantitative_trading_research/models/__init__.py
src/quantitative_trading_research/evaluation/__init__.py
src/quantitative_trading_research/artifacts/__init__.py
src/quantitative_trading_research/execution/__init__.py
### 7.4 Existing workflow

C2 may modify exactly:
.github/workflows/c0-documentation-consistency.yml
Only the bounded validation in Section 5.10 is authorized.
### 7.5 Scope exclusion

No abstract interface-stub path is authorized.
No unspecified .py file is authorized.
No file outside Sections 7.1 through 7.4 may be created, modified, moved, renamed, or deleted during C2.
## 8. Minimum required C2 outputs

### 8.1 Architecture and boundary record

docs/architecture/C2_canonical_repository_skeleton_and_boundaries.md
It must record:
* The canonical package and subsystem paths.
* One canonical responsibility per subsystem.
* Dependency direction.
* Provider and broker boundaries.
* Prohibited coupling.
* Future phase assignments.
* Future verification requirements.
* No executable implementation.
### 8.2 Machine-readable disposition plan

docs/migration/C2_migration_disposition_plan.yaml
Its authoritative schema is:
items:
  - c1_item_id:
    source_repository:
    source_commit:
    source_path:
    c1_classification:
    canonical_responsibility:
    c2_disposition:
    proposed_destination_path:
    migration_wave:
    required_prerequisites: []
    required_attribution:
    related_limitation_ids: []
    future_verification_requirements: []
    responsible_future_phase:
    owner_selection_status:
    notes:

unresolved_limitations:
  - limitation_id:
    related_c1_item_ids: []
    source_c1_evidence: []
    limitation_statement:
    current_status: UNRESOLVED
    responsible_future_phase:
    future_verification_requirements: []
    current_authorization_effect: NONE
    resolution_claimed_during_c2: NO
    notes:
All 82 accepted C1 manifest items must receive a high-level disposition.
Only C3/C4-relevant items require complete destination, migration-wave, limitation, and verification planning.
### 8.3 C2 report and C3 handoff

docs/reports/C2_migration_preparation_and_C3_handoff.md
It must include:
* C2 scope performed.
* Skeleton summary.
* All-82-item disposition summary.
* C3/C4 planning summary.
* Migration-wave summary.
* Unresolved-limitation summary.
* C3 handoff.
* Deferred later-phase responsibilities.
* Evidence limitations.
* Checks performed.
* Prohibited activity that did not occur.
* Completion-condition assessment.
* Explicit confirmation that C3 remains unauthorized.
## 9. Evidence, attribution, and traceability

Every item must preserve:
c1_item_id
source_repository
source_commit
source_path
c1_classification
canonical_responsibility
related_limitation_ids
future_verification_requirements
responsible_future_phase
owner_selection_status
Every unresolved limitation must preserve:
limitation_id
related_c1_item_ids
source_c1_evidence
limitation_statement
current_status
responsible_future_phase
future_verification_requirements
current_authorization_effect
resolution_claimed_during_c2
C2 must not:
* Shorten full source commits.
* Replace immutable commits with branch names.
* Infer missing source paths.
* Invent artifact, dataset, environment, configuration, or run identity.
* Treat file presence as byte-level provenance.
* Silently merge conflicting identities.
* Silently omit a material limitation or negative finding.
* Treat a proposed destination as migration.
* Treat a future-phase assignment as authorization.
* Mark a limitation resolved without later-phase evidence and authorization.
## 10. Historical-evidence proportionality rule

The accepted C1 retention matrix, technical migration manifest, architecture report, independent audit, and completion decision are the primary historical filter.
C2 does not require a file-by-file rereview of historical:
docs/reviews/
docs/workflows/
An exact historical record may be opened only when:
* A material C2 question cannot be resolved from accepted C1 evidence.
* Two retained conclusions conflict.
* Exact historical evidence is required to verify a material claim.
* A specific possible omission has been identified.
* A provider, data, model, holdout, safety, or publication decision materially depends on the record.
* The owner explicitly requests exact lineage.
Additional historical documents do not automatically prove incomplete C1 coverage.
C2 must carry forward:
* Durable controls.
* Technical responsibilities.
* Material limitations.
* Negative findings.
* Failed outcomes.
* Blocked outcomes.
* Inconclusive outcomes.
* Safety boundaries.
* Provenance requirements.
* Leakage controls.
* Holdout-integrity lessons.
C2 must leave redundant, administrative, superseded, and one-time procedures in historical repositories.
No limitation is resolved merely because it was summarized, consolidated, assigned a phase, or linked to a destination path.
## 11. Future-phase assignment of unresolved limitations

### C3

C3 owns:
* Python interpreter selection.
* Dependency reconstruction.
* Environment reproducibility.
* Import-surface reconstruction.
* Package compatibility.
* Clean-environment and import-smoke evidence.
* Environment identity.
### C4

C4 owns:
* Selected source migration and adaptation.
* Notebook-to-module lineage.
* Interface verification.
* Offline contract and synthetic tests.
* Numerical and behavioral parity.
* Configuration, artifact, provenance, and run identity.
### C5

C5 owns:
* Provider and feed selection.
* Coverage, entitlement, and licensing.
* Calendar and timestamp policy.
* Initial-universe decisions.
### C6

C6 owns:
* Dataset fields.
* Schemas and dtypes.
* Timing and expected-slot rules.
* Missing-data and acceptance requirements.
* Dataset provenance and identity requirements.
### C7

C7 owns:
* Dataset generation.
* Completeness verification.
* Missing-bar causality and remediation evidence.
* Dataset acceptance, rejection, or inconclusive disposition.
### C8 through C11

C8 through C11 own:
* Model implementation readiness.
* PPO, Random Forest, and XGBoost work.
* Training and chronological validation.
* Qualification.
* Freeze, rejection, no-candidate, or inconclusive disposition.
C2 must preserve:
current_model_candidate = NONE
current_deployment_candidate = NONE
### C12

C12 owns:
* Eligible-candidate confirmation.
* Common evaluation-package freeze.
* One shared untouched final holdout.
* Final evaluation and promotion disposition.
C2 does not authorize access to the final holdout.
## 12. C2 completion conditions

C2 may close only when:
1. The authorized non-operational skeleton is complete.
2. Package markers are empty or contain only one optional module docstring.
3. No abstract interface stub exists.
4. Package responsibilities are complete and non-duplicative.
5. Dependency direction is documented.
6. Provider and broker boundaries remain documentation-only.
7. All 82 C1 manifest items have high-level dispositions.
8. C3/C4-relevant items have complete destination, wave, limitation, and verification planning.
9. Later-phase items have explicit high-level deferrals.
10. items and unresolved_limitations are the only authoritative top-level collections.
11. Every c1_item_id and limitation_id is unique.
12. Bidirectional referential integrity succeeds.
13. Every limitation cites source_c1_evidence.
14. Every limitation has a responsible future phase.
15. Every limitation has future_verification_requirements.
16. Every resolution_claimed_during_c2 value is NO.
17. The C3 handoff is complete.
18. Accepted C1 artifacts remain unchanged.
19. No executable migration occurred.
20. No environment or dependency activity occurred.
21. No provider, network, market-data, or dataset activity occurred.
22. No model, validation, qualification, or holdout activity occurred.
23. No broker, order, or trading activity occurred.
24. Bounded workflow validation succeeds.
25. The completed C2 package receives Manager Review PASS.
26. The owner accepts the C2 completion decision.
27. Controlling state is aligned to C2_COMPLETED.
28. C3_authorization_effect = NONE.
C2_completion_Manager_Review = REQUIRED
C2_completion_Manager_Review_classification = PASS
owner_C2_completion_acceptance = REQUIRED
independent_C2_audit = CONDITIONAL_RISK_PROPORTIONAL
A focused independent C2 audit becomes required only if C2:
* Exceeds the authorized file scope.
* Introduces abstract or executable source.
* Alters provider, data, model, holdout, broker, or trading boundaries.
* Materially redesigns the accepted architecture.
* Alters accepted C1 evidence.
* Introduces unresolved conflicting migration dispositions.
* Makes an acceptance claim unsupported by accepted evidence.
## 13. Effective aligned state and non-effects

The target aligned state is:
current_lifecycle_state = C2_ACTIVE
active_major_phase = C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
phase_status = ACTIVE
authorization_effect = C2_SCOPE_ONLY
C1_completion_effect = EFFECTIVE
C2_authorization_status = AUTHORIZED
C2_activation_status = ACTIVE
current_model_candidate = NONE
current_deployment_candidate = NONE
C3_authorization_effect = NONE
C2 authorization does not authorize:
* C3 environment reconstruction.
* C4 source migration.
* C5 provider decisions.
* C6 dataset-contract acceptance.
* C7 dataset generation or acceptance.
* C8 through C11 model work.
* C12 final-holdout access.
* Publication.
* Paper trading.
* Live trading.
## 14. Repository recording and activation boundary

The authorization-recording and activation-alignment package is limited to:
docs/decisions/C2_authorization_decision.md
PROJECT_CONTEXT.md
README.md
docs/workflows/milestone_review_reference_map.md
.github/workflows/c0-documentation-consistency.yml
The Future Validation and Training Reference Map remains unchanged unless a specific material inconsistency is separately identified.
authorized_recording_branch = c2-authorization-decision
authorized_merge_method = SQUASH
direct_push_to_main = NOT_AUTHORIZED
force_push = NOT_AUTHORIZED
The decision-record branch, commit, push, pull request, or pull-request CI does not independently activate C2.
C2 becomes effective only through the aligned canonical merge and successful required validation.
This decision registers the accepted authorization as:
2v.GOV.06
