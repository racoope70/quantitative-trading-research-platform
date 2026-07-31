# C1 Legacy Evidence and Architecture Report

```text
document_status = DRAFT_FOR_OWNER_REVIEW
template_phase = C0
completed_output_phase = C1
completed_output_path = docs/reports/C1_legacy_evidence_and_architecture_report.md
authorization_effect = NONE
current_lifecycle_state = C1_ACTIVE
C1_phase_status = ACTIVE
C2_authorization_status = NOT_AUTHORIZED
current_model_candidate = NONE
current_deployment_candidate = NONE
```

## 1. Executive summary

C1 reviewed the complete accepted inventory of fifteen bounded historical sections across the project's exploratory, validation, modular implementation, and canonical governance repositories. The review preserved material evidence and durable controls, separated historical procedures from reusable architecture, normalized technical recommendations, and recorded limitations without converting historical work into current authorization or current model candidacy.

The three C1 outputs perform different and non-overlapping roles:

1. `docs/migration/legacy_evidence_retention_matrix.csv` preserves material historical evidence, decisions, controls, limitations, corrections, and future relevance.
2. `docs/migration/technical_migration_manifest.yaml` identifies technical assets and canonical responsibilities that may be considered in later phases, without executing migration.
3. `docs/reports/C1_legacy_evidence_and_architecture_report.md` consolidates the accepted section-level findings, architecture conclusions, functional 2v crosswalk, unresolved decisions, and phase boundaries.

The completed retention matrix contains 124 evidence rows and 20 fields and has been committed and pushed on the canonical C1 branch. The normalized technical manifest contains 82 unique exact-path items derived from 81 original eligible recommendations, 100 physical path references, nine bundled recommendations, and seventeen repeated exact paths; it has been committed and pushed, and its remote branch recording has been verified. Ten conflicting duplicate treatments were reconciled into one manifest-level disposition per unique asset. Every manifest owner disposition remains `PENDING`, every destination path remains unset, and no manifest recommendation is executable authority.

The historical standalone PPO and PPO-plus-Random-Forest work retain research, architecture, testing, and negative-result value. They are not current candidates. The accepted terminal state remains:

```text
legacy_ppo_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
legacy_ppo_random_forest_status = COMPLETED_HISTORICAL_RESEARCH_BASELINE
legacy_ppo_final_classification = INFRASTRUCTURE_FIXTURE_ONLY
current_model_candidate = NONE
current_deployment_candidate = NONE
```

The principal retained architecture is modular, testable, provenance-aware, leakage-conscious, provider-bounded, and phase-gated. The principal historical limitations are incomplete artifact-byte provenance, inconsistent environment identity, incomplete notebook-to-module parity evidence, historical holdout misuse, unresolved provider coverage, an unaccepted dataset, unresolved missing-bar causality, and operational demonstrations that do not establish economic qualification.

C1 remains documentation-only. This report does not authorize copying, adapting, executing, testing, installing, fetching, generating, training, validating, opening a holdout, accessing a provider or broker, submitting orders, promoting a model, or beginning C2.

Recommended current disposition:

```text
REMAIN_IN_C1_FOR_CORRECTION
```

Independent content audit and owner acceptance govern whether this report may be accepted as part of the final C1 package. The retention matrix and technical manifest have already passed artifact-content audit and have been committed and pushed, with the manifest’s remote branch recording verified. C2 requires separate express authorization after C1 closure.

## 2. Scope and method

### 2.1 Repositories and immutable review snapshots

| Repository | Immutable reference used | C1 use |
|---|---|---|
| `racoope70/exploratory-daytrading` | `2d6f354451515ff07ff6d022ea989ade2bc7574a` | Broad exploratory models, notebooks, data prototypes, feature design, selectors, QuantConnect experiments, and historical artifacts |
| `racoope70/quant-trading-model-validation` | `0a9c203bc322f6821c04074cb4c28498ab2ab38f` | Structured standalone PPO, PPO-plus-Random-Forest, reliability, and validation evidence |
| `racoope70/ppo-trading-pipeline` | `072103f43d8b2488c3efca183f637ab0508a193a` | Modular architecture, data reconstruction, environment, provider, holdout, paper-trading, execution-safety, and governance history |
| `racoope70/quantitative-trading-research-platform` | C1 branch last verified at `7f4c2b5ac092a3ce940b17fb1c3250476ed27a1a` | Current C1 authority, committed template, committed retention matrix, committed technical migration manifest, and canonical phase boundaries |

A later historical dataset-reconstruction correction was also represented where the accepted crosswalk explicitly cited commit:

```text
4cbb979a88176c252abcf5e1cd2f310c605573e9
```

Historical repositories remain evidence and engineering sources. They are not runtime dependencies and do not control current authorization.

### 2.2 Accepted inputs

This report uses:

- The committed C1 report template.
- The fifteen accepted bounded historical reviews.
- The accepted bounded-section-to-functional-2v crosswalk and its direct, contextual, unresolved, and no-direct mapping rules.
- The completed retention matrix:
  - SHA-256: `cf4162277ce2a7b418e340fedb2ff1e2165be20a7966e995569a1105819e357a`
  - 124 evidence rows excluding the header.
  - 20 fields.
  - All owner dispositions `PENDING`.
- The corrected completed technical migration manifest:
  - SHA-256: `c8fc766e81b06d47cbf72050d8e844006a45c9e18d4bd19df96d990ea4f18dd9`
  - 82 items.
  - 82 unique item IDs.
  - All owner dispositions `PENDING`.
- The accepted normalization decisions:
  - one exact source path per manifest item;
  - one consolidated disposition per unique exact asset;
  - complete traceability to all original recommendations;
  - no silent disappearance of accepted findings.
- The current C1 authorization boundary in `PROJECT_CONTEXT.md`.

### 2.3 Bounded inventory

The complete accepted inventory is:

1. Exploratory model development.
2. Legacy standalone PPO.
3. Legacy PPO plus Random Forest.
4. QuantConnect integration.
5. Alpaca operational reliability.
6. Modular VS Code migration.
7. Legacy artifact inventory and model-quality audit.
8. Final holdout and candidate selection.
9. Paper-trading and execution safety.
10. PPO v2 design and data contracts.
11. Dataset reconstruction.
12. Missing-bar investigation and remediation.
13. Market-data provider and SIP-access investigation.
14. Python and Alpaca environment diagnosis.
15. Governance-system development and lessons.

No additional bounded section was created during C1.

### 2.4 Review method

For each bounded section, the review:

1. Identified immutable repository sources and material records.
2. Distinguished decisive evidence from contextual or administrative evidence.
3. Identified superseding corrections and terminal decisions.
4. Separated durable controls from one-time procedures.
5. Applied one accepted retention classification:
   - `CARRY_FORWARD`
   - `SUMMARIZE_AND_REFERENCE`
   - `HISTORICAL_ARCHIVE_ONLY`
   - `OBSOLETE_OR_SUPERSEDED`
6. Recorded consolidation targets and future-phase relevance.
7. Applied the functional 2v lookup without inventing contiguous historical ranges.
8. Separated evidence-retention records from technical migration recommendations.
9. Preserved unresolved, blocked, failed, inconclusive, and no-candidate outcomes.

Materiality was assessed proportionally. The existence of another file, audit, review, run, or historical checkpoint did not create a new bounded section by itself.

### 2.5 Functional 2v interpretation

The accepted functional lookup is:

```text
2v.10  source/test implementation
2v.20  mocked unit and contract testing
2v.30  data-fetch authorization or execution
2v.40  dataset generation or dataset evidence
2v.50  dataset validation or validation-only preflight
2v.60  embargo or VecNormalize hardening
2v.70  PPO retraining authorization or execution
2v.80  final holdout or candidate selection
2v.90  paper trading, deployment, or live discussion
2v.100 future universe expansion
```

Mappings are represented as:

```text
DIRECT_FUNCTIONAL_MAPPING =
The record materially performs, authorizes, or directly evidences the named
technical function.

CONTEXTUAL_FUNCTIONAL_MAPPING =
The record governs, plans, reviews, or interprets the function without itself
performing or directly evidencing it.

UNRESOLVED_MAPPING =
The evidence or technical outcome remains incomplete, conflicting, or
inconclusive.

NO_DIRECT_FUNCTIONAL_2v_MAPPING =
The record concerns governance architecture, orientation, navigation,
correction lineage, or administrative procedure rather than a technical
function.
```

A sequence of functional references is not a contiguous historical-version range:

```text
functional_reference_sequence != contiguous_historical_version_range
```

The report therefore records exact section-level mapping status without inventing unsupported historical ranges.

### 2.6 C1 execution boundary

C1 authorized read-only inspection and documentation-only preparation of the three C1 outputs. It did not authorize:

- Historical-repository editing.
- Executable code migration or adaptation.
- Source, test, script, notebook, or command execution.
- Dependency installation or environment creation.
- Provider selection or acceptance.
- Credentials, authenticated access, network/API activity, or market-data requests.
- Dataset generation, modification, reconstruction, imputation, or acceptance.
- Model implementation, training, retraining, validation, qualification, promotion, or artifact creation.
- Final-holdout access.
- Broker access, paper orders, live orders, or trading.
- C2 or any later-phase work.

No executable migration occurred while preparing this report.

## 3. Bounded historical sections reviewed

| No. | Historical section | Legacy repository scope | Accepted functional 2v status | Material evidence reviewed | Main conclusion | Main limitation | Future phase relevance |
|---:|---|---|---|---|---|---|---|
| 1 | Exploratory model development | Exploratory | Direct: `2v.10, 2v.30, 2v.40, 2v.80, 2v.100`; contextual: `2v.60, 2v.70, 2v.90`; unresolved: `2v.50`; no-direct orientation records | Repository overview, early AAPL prototype, feature/RF notebook, model selector, multi-stock pipeline, alternative models | Preserves research breadth, feature ideas, negative lessons, and selector concepts as design and publication evidence | Results were provisional; randomized splitting, Colab/Drive dependence, incomplete provenance, and no accepted validation or candidate status | C2, C5, C6, C8, C12, C13 |
| 2 | Legacy standalone PPO | Exploratory, validation, PPO pipeline | Direct: `2v.10, 2v.30, 2v.40, 2v.60, 2v.70, 2v.80, 2v.90`; unresolved: `2v.50`; no-direct broad narration | Monolithic and modular training, split and normalization controls, retraining, holdout, selection, artifact audit, final decision | Retains PPO architecture, integration evidence, temporal controls, and model-quality lessons | Final classification is infrastructure fixture only; economic edge failed; artifact-byte provenance remains incomplete; not a current candidate | C4, C6, C8, C9, C12, C13 |
| 3 | Legacy PPO plus Random Forest | Exploratory, validation, PPO pipeline | Direct: `2v.10, 2v.30, 2v.40, 2v.70, 2v.80`; contextual: `2v.50, 2v.60, 2v.90`; no direct `2v.20` or `2v.100` | Hybrid source, gate configuration, representative TXN artifact family, selector evidence, terminal legacy decision | Retains hybrid gating design, representative immutable package evidence, and comparison lessons | Historical economic qualification and complete selected-symbol artifact coverage were not established; no current candidate | C4, C10, C12, C13 |
| 4 | QuantConnect integration | Exploratory, validation, PPO pipeline | Direct: `2v.10, 2v.20, 2v.30, 2v.40, 2v.80`; contextual: `2v.50, 2v.60, 2v.90`; no direct `2v.70` | Native LEAN experiments, external-signal preparation, adapter, consumer, payload exporter, local parity checks, replay algorithm | Established useful external-signal and offline integration patterns with PPO inference outside LEAN | Freshness could fail open; schema/checksum/run identity, timestamp preservation, same-bar semantics, and paper/live readiness were not established | C4, C5, C14 |
| 5 | Alpaca operational reliability | Exploratory, validation, PPO pipeline | Direct: `2v.10, 2v.20, 2v.30, 2v.90`; contextual: `2v.90`; no direct `2v.40, 2v.50, 2v.60, 2v.70, 2v.80` | Alpaca adapters and loaders, mocked tests, dry runs, paper-order and reconciliation evidence, freshness and stale-plan controls | Preserves broker-client boundaries, normalization, no-submit behavior, reconciliation, and operational controls | Connectivity, accepted orders, or stable sessions do not prove model quality, provider acceptance, or economic qualification | C4, C5, C14 |
| 6 | Modular VS Code migration | Exploratory, validation, PPO pipeline | Direct: `2v.10, 2v.20`; no direct execution mapping to later functional categories | Package structure, source modules, configuration, CLI, tests, CI, adapters, workflows, historical notebook antecedents | Provides the presumptive modular architecture source and reusable responsibility boundaries | Notebook-to-module lineage, numerical parity, clean-environment reproducibility, and automatic source acceptance remain unproven | C2, C3, C4 |
| 7 | Legacy artifact inventory and model-quality audit | Validation, PPO pipeline | Direct: `2v.10, 2v.20, 2v.80, 2v.90`; contextual: `2v.80, 2v.90` | Artifact inventory, parser, contract tests, promotion standard, model-quality audit, final decision, reliability evidence | Separates artifact completeness and infrastructure value from trading edge and candidate eligibility | Immutable model-byte provenance was incomplete; historical selection and paper evidence did not overcome the negative model-quality conclusion | C4, C8, C12, C13 |
| 8 | Final holdout and candidate selection | PPO pipeline | Direct: `2v.10, 2v.20, 2v.80, 2v.90`; contextual: `2v.80, 2v.90` | Holdout evaluator, selector, tests, v1.8.5 holdout, v1.9 selection, selected manifest, no-submit handoff | Preserves implementation and negative lessons for candidate freeze, predeclared rules, and one common final holdout | Historical final holdout was used to select among same-family windows and cannot be treated as canonical untouched-holdout evidence | C12 |
| 9 | Paper-trading and execution safety | PPO pipeline | Direct: `2v.10, 2v.20, 2v.30, 2v.90`; contextual: `2v.90` | Dry-run producer, execution plan, risk controls, checklist, loop, logging, mocked tests, submit and monitoring records | Preserves fail-closed safety, single submission authority, limits, idempotency needs, reconciliation, flattening, and evidence requirements | Several procedures were manual, mutable, account-specific, or demonstration-oriented; paper operation did not establish economic qualification | C4, C14 |
| 10 | PPO v2 design and data contracts | PPO pipeline | Direct: `2v.10, 2v.20, 2v.60`; contextual: `2v.70` | PPO v2 design, configuration, contract, preparation interfaces, handoff, training configuration, tests | Preserves a safer scaffold with split boundaries, positive embargo, fail-closed contracts, and explicit training handoff | No PPO v2 training occurred; actual train-only VecNormalize fitting, locking, propagation, and artifact identity were not established | C4, C6, C8, C9 |
| 11 | Dataset reconstruction | PPO pipeline | Direct: `2v.10, 2v.20, 2v.30, 2v.40`; contextual: `2v.30, 2v.40` | Reconstruction design, contract, calendar, writer, tests, fetch and generation records, blocked evidence review | Preserves deterministic reconstruction responsibilities, expected-slot controls, provenance writing, and fail-closed generation evidence | No dataset was selected or accepted; generation remained blocked by completeness and later provider/environment limitations | C4, C5, C6, C7 |
| 12 | Missing-bar investigation and remediation | PPO pipeline | Direct: `2v.10, 2v.30, 2v.40`; contextual: `2v.30, 2v.40`; unresolved provider cause | Calendar and expected-slot source, gap analysis, targeted refetch authorization and execution, blocked remediation decision | Preserves exact-gap detection, bounded remediation, no silent imputation, and negative evidence | The internal provider cause and complete remediation path remained unresolved; no complete accepted dataset resulted | C5, C6, C7 |
| 13 | Market-data provider and SIP-access investigation | PPO pipeline | Direct: `2v.30`; contextual: `2v.30`; no-direct public research and governance records; unresolved access outcome | SIP authorization, official public research, account inspection, minimal historical access attempt, evidence review and correction | Preserves entitlement, licensing, account-evidence, fail-closed transport, and provider-decision requirements | No successful SIP request or response was established; provider coverage and acceptance remain inconclusive | C5 |
| 14 | Python and Alpaca environment diagnosis | PPO pipeline | Direct: `2v.10`; contextual: `2v.10`; no-direct evidence-capture and authorization records; unresolved environment outcome | Requirements, CI, source imports, diagnostic command, import failures, root-cause and correction records | Preserves environment reconstruction inputs and the requirement for exact interpreter/package identity | Historical import surfaces conflicted; Python 3.11 Alpaca package identity/version and a compatible environment were not established; remediation was not executed | C3 |
| 15 | Governance-system development and lessons | PPO pipeline | Direct: `2v.10, 2v.30, 2v.40, 2v.50, 2v.80, 2v.90`; contextual: `2v.10, 2v.20, 2v.30, 2v.50, 2v.70`; no-direct governance records | Source hierarchy, authorization mechanics, evidence contracts, failed and corrected reviews, archive compression, source-of-truth alignment, proportionality | Historical governance was substantively strong but procedurally overgrown; preserve controls and simplify mechanics | Source-of-truth drift, repetitive closeouts, checkpoint proliferation, manual transcription, and disproportionate governance burden | C2, C13 |

The exact historical version range remains intentionally unassigned where the evidence spans noncontiguous functional categories. The accepted crosswalk records direct, contextual, unresolved, and no-direct statuses instead of inventing a range.

## 4. Material evidence, controls, and limitations

### 4.1 Historical evidence versus current authorization

Historical records establish what was designed, implemented, executed, observed, reviewed, corrected, or rejected in the historical repositories. They do not control the current canonical repository.

Current authorization comes only from the active canonical `PROJECT_CONTEXT.md` and the accepted C1 authorization decision read together. Therefore:

- A historical training authorization does not authorize current training.
- A historical provider or broker session does not authorize current access.
- A historical selected or paper-tested model does not become a current candidate.
- A historical final holdout does not become the canonical shared final holdout.
- A migration recommendation does not authorize copying or adapting code.
- A future map or roadmap entry is guidance, not permission.

### 4.2 Durable controls retained

| Control area | Durable control retained |
|---|---|
| Source of truth | One controlling current-state document; roadmap and future map remain non-authorizing |
| Evidence identity | Immutable repository commits, checksums, source paths, artifact identity, raw-versus-corrected evidence separation |
| Data | Provider decision before governed acquisition; explicit contract; versioned schema; expected-slot and calendar logic; no silent imputation |
| Leakage and time | Chronological splits, positive embargo where required, train-only preprocessing, explicit feature timing, no same-observation train/evaluate |
| Models | Predeclared qualification, benchmark and stability evidence, explicit rejected/no-candidate/inconclusive outcomes |
| Holdout | Candidate and evaluation-package freeze before one shared untouched final holdout; no post-access tuning |
| Artifacts | Exact dataset, feature, preprocessing, model, configuration, environment, and run identity |
| Execution | Paper-only credential and endpoint boundary, fail-closed broker state, limits, single authority, idempotency, reconciliation, flattening, kill state |
| Provider boundary | Offline interfaces and mocks may precede provider acceptance; authenticated access and production validation require later authorization |
| Governance | Risk-proportional review, owner acceptance for authority changes, independent review for material risk, concise completion records |

### 4.3 One-time procedures retained only as history

The following historical procedures do not become canonical defaults:

- Colab installation cells and Google Drive path handling.
- Direct notebook downloads and account-specific credential workflows.
- Mutable local artifact folders or wildcard model selection.
- Manual result inspection as a substitute for machine-readable evidence.
- Best-window-only selection or final-holdout maximization.
- Repeated final, terminal, finalization, and closeout loops.
- One document for every administrative micro-transition.
- Hard-coded freshness anchors that become stale immediately.
- Command-specific governance chains where ordinary automated tests suffice.
- Manually copied broker values, inferred fills, or unchecksummed execution plans.
- Treating successful API calls, backtests, or paper orders as evidence of trading edge.
- Carrying historical authorization forward by implication.

### 4.4 Accepted findings versus unresolved limitations

Accepted findings include:

- The project has valuable exploratory, modular, data, model, and execution-safety lineage.
- The standalone PPO legacy result is an infrastructure fixture, not a qualified model.
- PPO-plus-Random-Forest retains design value but lacks accepted economic qualification.
- The historical holdout and selection process does not meet the canonical future standard.
- The modular PPO pipeline is the presumptive architecture source, but no module is automatically accepted.
- Operational Alpaca and QuantConnect work provides interface and safety lessons, not provider or deployment acceptance.
- PPO v2 source scaffolds and data contracts exist, but no canonical PPO v2 training occurred.
- Dataset reconstruction and remediation evidence is useful, but no dataset is accepted.
- Governance controls protected material boundaries but became procedurally overgrown.

Unresolved limitations include:

- Immutable artifact-byte provenance for `TECH-PPO-02-07`.
- Complete model and preprocessing lineage for historical selected artifacts.
- Clean-environment and dependency reproducibility.
- Notebook-to-module numerical parity.
- Final provider, feed, entitlement, licensing, calendar, and permitted-use decisions.
- The root cause and acceptable resolution of historical missing bars.
- A selected and accepted canonical dataset.
- Actual PPO v2 train-only normalization and training evidence.
- A qualified frozen PPO, RF gate, or XGBoost gate.
- A valid shared final holdout outcome.
- Economically meaningful controlled paper evidence.

## 5. Consolidation decisions

| Historical evidence group | Overlap | Consolidation decision | Proposed retained artifact | Curated 2v treatment |
|---|---|---|---|---|
| Exploratory notebooks and overview records | Models, features, data, validation, selector, and deployment ideas overlap later sections | Retain a concise model/data catalog, durable feature and leakage lessons, and negative findings; archive notebook-specific procedure | Retention-matrix evidence plus selected manifest recommendations | Direct/contextual functional mappings remain section-specific; broad orientation receives no-direct mapping |
| Standalone PPO lineage | Training, data, holdout, artifact audit, and paper overlap sections 6–9 | Preserve architecture and corrections; exclude the historical monolith; retain final negative disposition | Matrix section 2 plus normalized manifest items `C1-TM-005`–`C1-TM-010` and shared assets | Functional mappings remain noncontiguous; unresolved `2v.50` is explicit |
| PPO-plus-Random-Forest | Hybrid design overlaps exploratory, model selection, and future C10 | Preserve representative immutable package and design; do not treat it as qualified or complete | Matrix section 3 and manifest `C1-TM-011`–`C1-TM-018` | Direct model/data/training/selection mappings; validation, hardening, and deployment remain contextual |
| QuantConnect and Alpaca integration | Adapters overlap modular architecture, provider decision, and execution safety | Consolidate by responsibility; retain offline-adaptable boundaries; defer provider acceptance and broker execution | Manifest adapter, consumer, test, and safety items; matrix sections 4, 5, and 9 | `2v.90` direct only for actual paper/broker evidence; narrative and planning are contextual |
| Modular migration | The same exact paths appeared in multiple bounded sections | Normalize one exact path per item and one disposition per unique asset; preserve each section-specific finding in rationale and limitations | 82-item normalized manifest | One unique technical identity; multiple section references remain traceable |
| Artifact inventory, holdout, and candidate selection | Artifact completeness, selection, promotion, and paper handoff overlapped | Separate artifact validity, model quality, selection integrity, and execution relevance; later terminal decisions supersede promotion language | Matrix sections 7 and 8; shared manifest assets | `2v.80` and `2v.90` direct only when actual selection or paper handoff occurred |
| Dataset reconstruction, missing bars, provider, and environment | One blocked chain spanned code, data, provider, and environment | Preserve each failure and correction under its own bounded section; do not collapse them into a successful dataset or provider conclusion | Matrix sections 11–14; manifest sections 11 and 14 | Direct, contextual, and unresolved outcomes remain separately visible |
| Governance records | Authorization, reviews, alignment, navigation, and technical checkpoints were interleaved | Preserve material controls and correction lineage; archive repetitive mechanics; avoid functional mappings for governance-only records | Matrix section 15 and this report | Use `NO_DIRECT_FUNCTIONAL_2v_MAPPING` unless the record materially performs or evidences a technical function |
| Repeated technical paths | 17 exact paths repeated across 100 physical references; 10 had conflicting treatments | Resolve to one consolidated item per exact path using the safer or more specific accepted disposition; preserve all original findings in the crosswalk | Manifest items `C1-TM-001`–`C1-TM-082` | Technical identity is unique; historical section mappings remain many-to-one |
| Legacy PPO model-artifact directory | Inventory records described local model artifacts without immutable bytes or checksum package | Exclude `TECH-PPO-02-07` from manifest pending immutable provenance | Matrix evidence and separate exclusion record | No technical manifest item until provenance is established |

## 6. Technical migration recommendations

### 6.1 Manifest normalization

The completed manifest reconciles:

```text
original_eligible_recommendation_IDs = 81
physical_path_references = 100
bundled_recommendations = 9
duplicated_exact_paths = 17
conflicting_duplicate_treatments = 10
unique_exact_paths = 82
normalized_manifest_items = 82
```

The normalized count is 82 because splitting nine bundled recommendations produced 100 physical path references, and consolidation removed eighteen repeated occurrences across seventeen repeated exact paths.

Every normalized item contains one exact committed source path. Every repeated source path has one consolidated manifest-level disposition. All original recommendation findings remain traceable through historical purpose, required changes, limitations, tests, and canonical responsibility.

### 6.2 Item distribution

#### Asset type

| Asset type | Count |
|---|---:|
| `SOURCE_MODULE` | 28 |
| `SCRIPT` | 13 |
| `TEST_MODULE` | 13 |
| `CONFIGURATION` | 11 |
| `NOTEBOOK` | 7 |
| `BROKER_SAFETY_COMPONENT` | 4 |
| `MODEL_ARTIFACT` | 3 |
| `PROVENANCE_UTILITY` | 2 |
| `BUILD_OR_CI_COMPONENT` | 1 |
| **Total** | **82** |

#### Classification

| Classification | Count |
|---|---:|
| `CARRY_FORWARD` | 57 |
| `OBSOLETE_OR_SUPERSEDED` | 9 |
| `SUMMARIZE_AND_REFERENCE` | 8 |
| `HISTORICAL_ARCHIVE_ONLY` | 8 |
| **Total** | **82** |

#### Migration action

| Migration action | Count |
|---|---:|
| `ADAPT_AND_TEST` | 40 |
| `REIMPLEMENT_WITH_ATTRIBUTION` | 22 |
| `RETAIN_IN_HISTORICAL_REPOSITORY` | 11 |
| `SUMMARIZE_AND_REFERENCE` | 4 |
| `COPY_WITH_ATTRIBUTION` | 2 |
| `DEFER_DECISION` | 2 |
| `EXCLUDE_FROM_NEW_REPOSITORY` | 1 |
| **Total** | **82** |

All 82 destination paths are unset. This is intentional: C1 identifies responsibilities and future phases but does not choose final canonical paths or execute migration.

### 6.3 Canonical architecture recommendations

The future canonical platform should preserve these responsibility boundaries:

- Configuration and deterministic path management.
- Provider-neutral data-source contracts.
- Provider-specific adapters behind explicit interfaces.
- Data acquisition separated from normalization, feature generation, labels, and persistence.
- Versioned feature and dataset manifests.
- Chronological splits, embargo, and train-only preprocessing.
- Training separated from evaluation, selection, artifact management, and deployment.
- Exact artifact and run identity.
- Offline contract, interface, synthetic-data, and fail-closed tests.
- Candidate qualification and freeze before shared final holdout access.
- Broker execution separated from decision generation.
- One submission authority with limits, idempotency, reconciliation, flattening, and incident controls.
- Documentation and evidence outputs that are machine-readable where practical.

The manifest is a recommendation inventory, not an acceptance list. `CARRY_FORWARD` means the responsibility or design remains valuable; it does not mean the historical implementation is correct, compatible, safe, or ready to copy.

### 6.4 TECH-PPO-02-07 provenance limitation

```text
original_item_id = TECH-PPO-02-07
reported_asset = models/alpaca_ppo_models_master
asset_type = MODEL_ARTIFACT
accepted_classification = HISTORICAL_ARCHIVE_ONLY
manifest_inclusion = EXCLUDED_PENDING_IMMUTABLE_PROVENANCE
current_candidate_effect = NONE
```

The committed evidence preserves inventories, summaries, a selected-prefix manifest, and a final legacy decision. It does not establish the referenced PPO ZIP, VecNormalize PKL, feature-manifest, probability-configuration, and model-information bytes as committed Git objects or as one checksummed immutable external package.

The limitation is preserved by:

- `docs/audits/v1.62_ppo_baseline_artifact_inventory.csv`
- `docs/audits/v1.62_ppo_baseline_artifact_inventory_summary.md`
- `docs/audits/v1.63_ppo_baseline_model_quality_audit_summary.md`
- `config/paper_trading_six_ticker_manifest.json`
- `docs/decisions/v1.65_legacy_ppo_final_audit_decision.md`

Disposition remains:

```text
DEFERRED_PENDING_IMMUTABLE_ARTIFACT_SOURCE_OR_CHECKSUM_PACKAGE
```

No manifest item may be created for the asset directory unless immutable artifact provenance is later established and separately accepted.

## 7. C4 provider-boundary recommendations

C4 may consider only offline migration and verification of owner-accepted technical assets after C2 and C3 have completed and C4 is separately authorized.

### 7.1 Provider-neutral assets

Examples include:

- Data contracts and schema definitions.
- Feature manifests and deterministic feature logic.
- Split and embargo controls.
- Artifact identity and provenance interfaces.
- Calendar abstractions.
- Dataset reconstruction interfaces.
- Parquet/provenance writers.
- Training-input handoff interfaces.
- Broker-neutral execution plans, limits, and reconciliation contracts.

### 7.2 Mock-only and offline-verification assets

Examples include:

- Synthetic-data contract tests.
- Temporary-artifact tests.
- Mocked adapter and endpoint tests.
- No-submit and fail-closed tests.
- Risk, checklist, stale-plan, filtering, and reconciliation tests.
- CI and test-configuration components after environment reconstruction.

### 7.3 Normalization and schema utilities

Examples include:

- Bar sorting, timezone normalization, duplicate rejection, and freshness checks.
- Feature-schema validation.
- Expected-slot and market-calendar logic.
- VecNormalize identity and train-only fitting controls.
- Payload schema, expiration, checksum, and source-timestamp validation.
- Dataset provenance and deterministic writer utilities.

### 7.4 Provisionally provider-specific assets

Examples include:

- Alpaca adapter and historical-data loader.
- QuantConnect adapter, external-signal consumer, and replay logic.
- Provider-specific request construction and response parsing.
- Paper-trading broker integration components.

These may be inspected, adapted, and tested offline only after C4 authorization. Their presence in the manifest does not accept Alpaca, QuantConnect, SIP, IEX, or another provider.

C4 does not authorize:

- Provider selection or acceptance.
- Credentials or authenticated access.
- Network or API testing.
- Market-data requests.
- Entitlement verification.
- Account inspection.
- Production data-source validation.
- Broker connectivity or orders.
- Final feed, adjustment, calendar, universe, licensing, or permitted-use decisions.

Those remain C5 or later work under separate authorization.

## 8. Proposed curated 2v structure

### 8.1 Accepted bounded-section functional crosswalk

| Section | Direct functional entries | Contextual entries | Unresolved status | No-direct status |
|---:|---|---|---|---|
| 1 | `2v.10, 2v.30, 2v.40, 2v.80, 2v.100` | `2v.60, 2v.70, 2v.90` | `2v.50` remains unresolved for broad exploratory validation wording | Orientation and broad research summaries |
| 2 | `2v.10, 2v.30, 2v.40, 2v.60, 2v.70, 2v.80, 2v.90` | None | `2v.50` remains unresolved between model evaluation and defined dataset validation | Broad audit narration |
| 3 | `2v.10, 2v.30, 2v.40, 2v.70, 2v.80` | `2v.50, 2v.60, 2v.90` | Historical economic qualification remains unestablished | No material item-owned `2v.20`; broad symbol lists do not create `2v.100` |
| 4 | `2v.10, 2v.20, 2v.30, 2v.40, 2v.80` | `2v.50, 2v.60, 2v.90` | Freshness, parity, and execution semantics remain limited | PPO reference does not establish `2v.70` retraining |
| 5 | `2v.10, 2v.20, 2v.30, 2v.90` | `2v.90` | None in functional classification | Generic reports, preflight, timestamps, PPO loading, and selected models do not create `2v.40`–`2v.80` |
| 6 | `2v.10, 2v.20` | None | Architecture parity and environment reproducibility remain unresolved, not functional-category mappings | File presence does not establish later execution categories |
| 7 | `2v.10, 2v.20, 2v.80, 2v.90` | `2v.80, 2v.90` | Immutable historical model-byte provenance remains incomplete | Inventory and audit narration do not automatically create data, validation, hardening, or retraining mappings |
| 8 | `2v.10, 2v.20, 2v.80, 2v.90` | `2v.80, 2v.90` | Canonical holdout validity is not established | Dataset, embargo, retraining, and paper-default mentions do not create mappings |
| 9 | `2v.10, 2v.20, 2v.30, 2v.90` | `2v.90` | Historical paper economics do not establish qualification | Reports, checklists, timestamps, and model signals do not create `2v.40`–`2v.80` |
| 10 | `2v.10, 2v.20, 2v.60` | `2v.70` | Actual train-only normalization and PPO v2 retraining remain unestablished | Alpaca, contract, future holdout, and trading prohibitions do not create later mappings |
| 11 | `2v.10, 2v.20, 2v.30, 2v.40` | `2v.30, 2v.40` | No accepted dataset reached `2v.50` | Temporal and future-model references do not create hardening, retraining, or holdout mappings |
| 12 | `2v.10, 2v.30, 2v.40` | `2v.30, 2v.40` | Internal provider cause remains unresolved | Temporary scripts and incomplete data do not create test, validation, hardening, training, or holdout mappings |
| 13 | `2v.30` | `2v.30` | Provider coverage and successful transport remain inconclusive | Public research, licensing analysis, and governance records |
| 14 | `2v.10` | `2v.10` | Environment compatibility and package identity remain unresolved | Authorization, evidence-capture, and remediation-planning records |
| 15 | `2v.10, 2v.30, 2v.40, 2v.50, 2v.80, 2v.90` | `2v.10, 2v.20, 2v.30, 2v.50, 2v.70` | No functional-category conflict; historical checkpoint range is not converted into a contiguous range | Source hierarchy, navigation, correction lineage, archive compression, and proportionality records |

This crosswalk is non-authorizing. It is a navigation and evidence-classification structure only.

### 8.2 Proposed material curated entries

The following concise canonical references are proposed for later owner acceptance and milestone-map inclusion:

```text
2v.LEGACY.01 =
Accepted fifteen-section bounded historical inventory and functional crosswalk

2v.LEGACY.02 =
Completed legacy evidence retention matrix, including corrections,
limitations, terminal model dispositions, and no-direct mappings

2v.ARCH.01 =
Normalized technical migration manifest, exact-path identity,
duplicate reconciliation, and TECH-PPO-02-07 exclusion

2v.ARCH.02 =
C1 legacy evidence and architecture report, retained architecture,
provider boundary, and future-phase handoff
```

Existing governance authority remains under `2v.GOV.*`. The proposed `2v.LEGACY.*` and `2v.ARCH.*` entries do not create authorization.

## 9. Unresolved owner decisions

The retention matrix and normalized technical migration manifest are no longer unresolved repository-recording items: both have been committed and pushed, and the manifest's remote branch recording has been verified.

The following decisions remain materially unresolved:

1. Accept or correct this C1 report after independent audit.
2. Decide whether the three outputs collectively satisfy C1 after all material corrections.
3. Accept the final curated `2v.LEGACY.*` and `2v.ARCH.*` entries and any concise milestone-map update.
4. Preserve `TECH-PPO-02-07` as deferred unless immutable artifact bytes or a checksum-bound immutable package are established.
5. Decide whether to close C1 after the required independent audit passes.
6. Decide separately whether to authorize C2. C1 completion would make C2 eligible for consideration; it would not activate C2.

Later technical decisions remain assigned to their proper phases:

| Phase | Decision reserved for that phase |
|---|---|
| C2 | Canonical skeleton, package boundaries, migration order, and verification plan |
| C3 | Supported Python version, dependency reconstruction, lock, and clean-environment evidence |
| C4 | Owner-selected code migration, adaptation, attribution, and offline verification |
| C5 | Provider, feed, licensing, permitted use, calendar, and initial universe |
| C6 | Dataset contract freeze |
| C7 | Governed dataset generation and acceptance |
| C8 | PPO v2 implementation readiness |
| C9 | PPO v2 training, validation, qualification, and freeze |
| C10 | Random Forest gate development only with a qualified frozen PPO foundation |
| C11 | XGBoost gate development under its accepted entry gate |
| C12 | Eligible-candidate freeze, one shared untouched final holdout, and promotion decision |
| C13 | Publication or portfolio release |
| C14 | Controlled paper trading of a promoted frozen candidate |
| C15 | Possible limited live-capital consideration |

No recommendation in this report executes or authorizes any of these phases.

## 10. Recommended next disposition

```text
REMAIN_IN_C1_FOR_CORRECTION
```

Rationale:

- All fifteen bounded sections have been reviewed.
- The retention matrix has been completed, committed, and pushed.
- The technical manifest has been normalized, completed, committed, and pushed, and its remote branch recording has been verified.
- This report completes the third required C1 output as a read-only artifact.
- The three outputs reconcile at the evidence, technical-asset, and summary levels.
- Material limitations and negative findings remain visible.
- No executable migration occurred.

C1 is not yet complete because:

- Owner acceptance of this independently audited report and the final three-output package has not yet occurred.
- The committed retention matrix and technical manifest do not by themselves complete C1.
- The owner has not accepted the final three-output package.
- The required risk-proportional independent C1 audit has not yet passed.
- No owner-controlled C1 completion decision has been recorded.
- C2 remains unauthorized.

After audit and any correction, the owner may consider C1 closure. A later decision to authorize C2 must be separate and explicit.

## 11. C1 completion assessment

```text
[x] Every section in the accepted bounded historical inventory was reviewed.

[x] Exact section-level functional mapping status was recorded for every
    section using direct, contextual, unresolved, and no-direct states.
    Unsupported contiguous historical ranges were not invented.

[x] No added section required a material-distinction or owner-acceptance record.

[x] Material evidence was entered in the completed retention matrix.

[x] Durable controls and limitations were captured.

[x] Overlapping evidence received consolidation decisions.

[x] Material technical assets were entered in the normalized completed manifest.

[x] A concise curated new 2v structure was proposed.

[x] This C1 summary report was completed for read-only content audit.

[ ] The owner accepted the final recommendations and three-output package.

[ ] One risk-proportional independent C1 audit passed.

[x] No executable technical migration occurred.
```

### Three-output reconciliation

```text
retention_matrix =
docs/migration/legacy_evidence_retention_matrix.csv

retention_matrix_role =
124 material evidence records preserving historical findings,
controls, limitations, corrections, classifications, future relevance,
and owner dispositions

technical_manifest =
docs/migration/technical_migration_manifest.yaml

technical_manifest_role =
82 unique exact-path technical recommendations preserving canonical
responsibilities, required adaptations, limitations, tests, and future phases

summary_report =
docs/reports/C1_legacy_evidence_and_architecture_report.md

summary_report_role =
fifteen-section synthesis, consolidation decisions, accepted functional
crosswalk, provider boundary, unresolved decisions, and C1-to-C15 phase handoff
```

Reconciliation checks:

- The report covers all fifteen bounded sections represented in the retention matrix.
- The report's technical counts and dispositions match the corrected 82-item manifest.
- The report preserves the manifest's one-path-per-item and one-disposition-per-unique-asset normalization.
- The report preserves `TECH-PPO-02-07` as a separate provenance exclusion.
- The report preserves historical model and artifact findings without promoting any current candidate.
- The report preserves the current C1-only authorization boundary.
- The report does not assign destination paths or execute migration.
- The report does not authorize C2 or any later phase.

```text
repository_file_created = NO
repository_file_edited = NO
repository_file_staged = NO
repository_commit_created = NO
repository_push_performed = NO
repository_merge_performed = NO

retention_matrix_modified = NO
technical_manifest_modified = NO
PROJECT_CONTEXT_edited = NO
milestone_review_reference_map_edited = NO
future_validation_training_reference_map_edited = NO

technical_execution = NO
dependency_installation = NO
provider_or_network_activity = NO
market_data_activity = NO
dataset_activity = NO
model_or_holdout_activity = NO
broker_or_order_activity = NO

C2_authorization_status = NOT_AUTHORIZED
```
