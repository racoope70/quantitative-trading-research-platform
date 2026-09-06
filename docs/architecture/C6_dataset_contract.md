# C6 Dataset Contract

```text
document_status = C6_G_REVIEW_HISTORY_RECORDED__INDEPENDENT_EVIDENCE_CONTROLS__NOT_FROZEN
document_role = C6_DATASET_CONTRACT__C6_A_THROUGH_C6_F_PUBLISHED__C6_G_REVIEW_HISTORY
current_state_control = NO
authorization_effect = NONE

controlling_current_state_document = PROJECT_CONTEXT.md
supporting_C6_authorization_decision =
docs/decisions/C6_authorization_decision.md

C6_phase = C6_ACTIVE
C6_authorization =
AUTHORIZED__SPECIFICATION_AND_CONTRACT_FREEZE_ONLY

C6_A_work_package =
CONTRACT_SKELETON_AND_ACCEPTED_INPUT_INVENTORY

C6_A_scope =
ORGANIZATION_AND_REQUIREMENTS_INVENTORY_ONLY

C6_A_status = COMPLETE__PUBLISHED__EFFECTIVE

C6_B_work_package =
RAW_PROCESSED_SCHEMA_IDENTITY_AND_PROVENANCE

C6_B_scope =
TECHNICAL_SCHEMA_IDENTITY_LINEAGE_AND_PROVENANCE_SPECIFICATION_ONLY

C6_B_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_B_REOPEN = NO

C6_C_work_package =
CHRONOLOGY_LEAKAGE_CALENDAR_AND_MISSINGNESS

C6_C_scope =
TECHNICAL_CHRONOLOGY_LEAKAGE_CALENDAR_SESSION_PIT_AND_MISSINGNESS_SPECIFICATION_ONLY

C6_C_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_C_REOPEN = NO

C6_D_work_package =
RL_STATE_RECURRENT_ACTION_AND_ECONOMIC_REPRESENTATION

C6_D_scope =
TECHNICAL_RL_STATE_RECURRENT_ACTION_AND_ECONOMIC_REPRESENTATION_SPECIFICATION_ONLY

C6_D_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_D_REOPEN = NO

C6_E_work_package =
DEVELOPMENT_VALIDATION_HOLDOUT_AND_GATE_ALIGNMENT

C6_E_scope =
TECHNICAL_DEVELOPMENT_VALIDATION_QUALIFICATION_HOLDOUT_AND_GATE_ALIGNMENT_SPECIFICATION_ONLY

C6_E_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_E_REOPEN = NO

C6_F_work_package =
DATASET_ACCEPTANCE_AND_INDEPENDENT_REVIEW_RULES

C6_F_scope =
TECHNICAL_DATASET_ACCEPTANCE_INDEPENDENT_REVIEW_AND_CONTRACT_FREEZE_REQUIREMENTS_SPECIFICATION_ONLY

C6_F_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_F_PUBLICATION_COMMIT = 5ae9557d823aa2e82ca507af72b147f1efbdad59
C6_F_PUBLICATION_CI = PASS

C6_G_INITIAL_REVIEW_DISPOSITION = PASS_WITH_BOUNDED_CORRECTION
C6_G_INITIAL_MATERIAL_FINDING_COUNT = 0
C6_G_INITIAL_BOUNDED_CORRECTABLE_FINDING_COUNT = 3
C6_G_REVERIFICATION_1_DISPOSITION = PASS_WITH_BOUNDED_CORRECTION
C6G_FIND_001_REVERIFICATION_1 = OPEN
C6G_FIND_002_REVERIFICATION_1 = OPEN
C6G_FIND_003_REVERIFICATION_1 = CLOSED
C6_G_REVERIFICATION_1_OPEN_BOUNDED_CORRECTABLE_FINDING_COUNT = 2
C6_G_REVERIFICATION_1_MATERIAL_FINDING_COUNT = 0
C6_G_FINAL_REVIEW_DISPOSITION =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS
C6_G_REVIEW_CLOSURE =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS

CORRECTION_PUBLICATION_AUTHORITY = EXTERNAL_TO_THIS_DOCUMENT
CORRECTION_PUBLICATION_STATE =
ESTABLISHED_BY_CANONICAL_GIT_HISTORY_AND_GOVERNANCE_EVIDENCE
THIS_DOCUMENT_CREATES_PUBLICATION_AUTHORIZATION = NO
C6_H_FREEZE_ELIGIBLE = NO
C6_DATASET_CONTRACT = NOT_FROZEN

dataset_contract_status = AUTHORIZED__NOT_FROZEN
dataset_generation_status = NOT_AUTHORIZED

ACCEPTED_REQUIREMENT =
REQUIREMENT_ALREADY_ESTABLISHED_BY_CANONICAL_DECISION_OR_ACCEPTED_GUIDANCE

C6_B_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_COMPLETED_PUBLISHED_C6_B_SCOPE

C6_C_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_COMPLETED_PUBLISHED_C6_C_SCOPE

C6_D_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_COMPLETED_PUBLISHED_C6_D_SCOPE

C6_E_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_COMPLETED_PUBLISHED_C6_E_SCOPE

C6_F_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_COMPLETED_PUBLISHED_EFFECTIVE_C6_F_SCOPE

C6_DETAIL_TO_BE_DEFINED =
TECHNICAL_CONTRACT_DETAIL_INTENTIONALLY_DEFERRED_TO_A_LATER_C6_WORK_PACKAGE

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Document role and governance status

This document contains the published/effective C6-A dataset-contract
skeleton and accepted-input inventory, the published/effective C6-B technical
definitions for raw and processed schemas, identity, lineage, provenance, and
reproducibility, the published/effective C6-C technical definitions for
chronology, leakage, calendar/session validation, PIT availability, and
missingness/reconstruction, the published/effective C6-D definitions for RL
state, recurrent sequences, continuous actions, and economic representation,
the published/effective C6-E definitions for development, validation,
qualification, final-holdout isolation, and gate alignment, and the
published/effective C6-F requirements for dataset acceptance, independent
review, and contract freeze. The complete initial C6-G review returned
PASS_WITH_BOUNDED_CORRECTION with zero material findings and three bounded
correctable findings. The first independent re-verification returned
PASS_WITH_BOUNDED_CORRECTION, closing C6G-FIND-003 and leaving C6G-FIND-001
and C6G-FIND-002 open at that review. These are historical review facts;
subsequent independent evidence controls closure and final disposition.
Authoring or publishing corrections does not itself establish a review result.

It remains a draft C6 dataset contract and is not frozen.

`PROJECT_CONTEXT.md` remains the controlling source of truth for broad current
lifecycle state and authorization boundaries.

`docs/decisions/C6_authorization_decision.md` is supporting authorization
evidence for the already-effective bounded C6 scope.

This document creates no new authorization and is not a checkpoint tracker,
execution log, dataset-acceptance record, model specification, training plan,
or final-holdout approval.

Requirements and technical specifications in this document use seven states:

- `ACCEPTED_REQUIREMENT` — already established by canonical decisions or
  accepted methodological guidance.
- `C6_B_DETAIL_DEFINED` — a technical schema, identity, lineage, provenance,
  or reproducibility detail defined within the completed, published, and
  effective bounded C6-B surface.
- `C6_C_DETAIL_DEFINED` — a chronology, leakage, calendar/session,
  PIT-availability, or missingness/reconstruction detail defined within the
  completed, published, and effective bounded C6-C surface.
- `C6_D_DETAIL_DEFINED` — an RL state, recurrent sequence, continuous action,
  or economic-interface detail within the completed, published, and effective
  bounded C6-D surface.
- `C6_E_DETAIL_DEFINED` — a partition, evaluation-isolation, or gate-alignment
  detail within the completed, published, and effective bounded C6-E surface.
- `C6_F_DETAIL_DEFINED` — a dataset-acceptance, independent-review, or freeze
  requirement within the completed, published, and effective C6-F scope.
- `C6_DETAIL_TO_BE_DEFINED` — a technical C6 contract detail assigned to a
  later work package; historical authoring-stage deferrals must be read with
  their fulfilled references where subsequently defined.

A separate notation is used only where source reconciliation is required:

- `SOURCE_RECONCILIATION_NOTE` — wording supplied to C6-A that is not directly
  established by the current canonical source documents reviewed. It must not
  be silently promoted to an accepted scientific rule.

## 2. Purpose and scope

C6 defines and freezes the governed dataset contract before any later dataset
generation or acceptance activity.

The contract must remain model-family neutral across the accepted bounded RL
candidate set and support:

- raw-data requirements;
- processed-data requirements;
- identity and ordering;
- calendar and timestamp semantics;
- chronology and leakage controls;
- explicit missingness representation;
- point-in-time historical-universe provenance;
- PPO, SAC, and RecurrentPPO compatibility;
- recurrent sequence requirements;
- continuous target-position/exposure actions;
- common economic, execution, spread, slippage, turnover, and cost inputs;
- chronological development, validation, qualification, and final-holdout
  isolation;
- RF/XGBoost gate-feature and target alignment;
- provider/source provenance and reproducibility identity;
- dataset acceptance rules;
- independent C6 review; and
- final contract freeze.

C6-A through C6-F are complete, published, and effective within their bounded
surfaces and are not reopened. C6-G initial review and first re-verification
are recorded as historical evidence. The latter closed C6G-FIND-003 and left
two findings open at that review. This second correction addresses only the
remaining C6G-FIND-001 and state-representation portion of C6G-FIND-002;
it does not modify C6G-FIND-003 or independently determine finding closure.
Historical statements describing what an earlier work package
did not execute retain that historical scope. Dataset acceptance, C6-H freeze,
and C7 execution remain unauthorized.

## 3. Controlling scientific and governance inputs

The accepted-input inventory uses the following canonical sources.

| ID | Canonical source | Role in this contract |
|---|---|---|
| S1 | `PROJECT_CONTEXT.md` | Controlling broad lifecycle and authorization state |
| S2 | `docs/decisions/C6_authorization_decision.md` | GOV-DEC-0014 bounded C6 scope, exclusions, and contract-freeze authority |
| S3 | `docs/decisions/post_C5_pre_C6_RL_research_design_decision.md` | GOV-DEC-0013 accepted RL/gating scientific design |
| S4 | `docs/decisions/C5_provider_strategy_decision.md` | Accepted provider-neutral architecture and provenance principles |
| S5 | `docs/decisions/C5_historical_universe_timing_decision.md` | Accepted study-window and formation chronology |
| S6 | `docs/decisions/C5_historical_universe_eligibility_decision.md` | Accepted universe eligibility and PIT evidence architecture |
| S7 | `docs/decisions/C5_calendar_cost_regime_decision.md` | Accepted calendar, hourly-bar, cost, liquidity, and regime principles |
| S8 | `docs/decisions/C5_completion_decision.md` | Evidence that the C5 scientific decision surface was accepted and closed |
| S9 | `docs/workflows/milestone_review_reference_map.md` | Non-authorizing roadmap and C6 entry/exit-gate reference |
| S10 | `docs/workflows/future_validation_training_reference_map.md` | Non-authorizing accepted methodological guidance and C6 compatibility envelope |
| S11 | `docs/architecture/C2_canonical_repository_skeleton_and_boundaries.md` | Canonical subsystem responsibility boundaries |
| S12 | `src/quantitative_trading_research/data/README.md` | Data-subsystem responsibility, provenance, reconstruction, and future verification boundaries |

S9 and S10 are reference documents and grant no authorization.

## 4. Raw-data contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S4, S11, S12]: downstream data representation must
  remain provider neutral, with provider-specific behavior isolated behind
  provider boundaries/adapters.
- `ACCEPTED_REQUIREMENT` [S4]: provider-specific provenance must preserve
  material source semantics, including provider and dataset/feed, publisher or
  venue scope, identifier namespace, timestamp and bar semantics,
  raw/adjusted lineage, corporate-action/reference snapshot, revision or
  as-of state, retrieval timestamp, checksum, and license/entitlement lineage
  where applicable.
- `ACCEPTED_REQUIREMENT` [S4]: a material canonical-source change requires a
  canonical dataset rebuild and rerun of affected later
  training/validation/backtest work.
- `ACCEPTED_REQUIREMENT` [S4, S6]: Alpaca may serve as a provisional
  historical market-bar source and later paper-feed infrastructure when
  separately authorized, but Alpaca is not an acceptable sole point-in-time
  historical reference source.
- `ACCEPTED_REQUIREMENT` [S6]: the accepted PIT capability envelope preserves
  Sharadar `TICKERS + ACTIONS`, Alpaca historical SIP bars with explicit
  `feed=sip`, dated SEC EDGAR / Inline-XBRL evidence, and historical NYSE
  Daily TAQ Master primary-listing evidence.
- `ACCEPTED_REQUIREMENT` [S6]: the PIT capability envelope is a capability
  design, not evidence that any provider has been purchased, acquired,
  entitled, or authorized for execution.

### C6-B technical definition — canonical raw layer

`C6_B_DETAIL_DEFINED` — the canonical raw layer consists of immutable source
objects plus provider-neutral normalized raw records. The logical contract is
independent of any one storage engine or provider delivery format. Original
source-object bytes and their exact SHA-256 identity remain the evidence root;
normalized raw records preserve provider semantics without turning provider
fields into downstream canonical assumptions.

#### Canonical raw record classes

| Logical class | Purpose | Natural-key basis |
|---|---|---|
| `raw_market_bar` | Provider market-bar observation used as governed market input | source object SHA-256 + source row locator |
| `raw_security_event` | Dated ticker, listing, delisting, acquisition, corporate-action, or other security event evidence | source object SHA-256 + source row locator |
| `raw_reference_evidence` | Dated reference, filing, incorporation, security-type, SPAC, or primary-listing evidence | source object SHA-256 + source row locator |

No record class implies that the source has been purchased or acquired. These
classes define only how later authorized source material must be represented.

#### Source-object manifest

Every ingested source object must have one immutable manifest record with:

| Field | Logical dtype | Required | Meaning |
|---|---|---:|---|
| `source_object_sha256` | string | YES | Lowercase 64-hex SHA-256 of the exact source-object bytes |
| `source_object_byte_count` | int64 | YES | Exact byte count of the source object |
| `provider_name` | string | YES | Provider or authoritative source identity |
| `source_dataset` | string | YES | Provider dataset/product/source name |
| `source_feed` | string | CONDITIONAL | Explicit feed when feed semantics are material; for applicable Alpaca stock bars this records `sip` |
| `publisher_or_venue` | string | CONDITIONAL | Publisher, venue, or market scope when applicable |
| `retrieved_at_utc` | timestamp[ns, UTC] | YES | Retrieval instant; provenance only, not market-event time |
| `source_asof_utc` | timestamp[ns, UTC] | CONDITIONAL | Source snapshot/as-of instant when supplied or material |
| `revision_id` | string | CONDITIONAL | Provider revision/version identifier when available |
| `media_type_or_format` | string | YES | Source delivery representation without making it canonical downstream semantics |
| `license_entitlement_ref` | string | CONDITIONAL | Non-secret reference to the applicable license/entitlement record; never credentials |
| `adapter_version` | string | YES | Human-readable provider-adapter version |
| `adapter_identity` | string | YES | SHA-256 identity of the adapter specification/code/configuration used for normalization |
| `source_field_map_version` | string | YES | Human-readable mapping version |
| `source_field_map_identity` | string | YES | SHA-256 identity of the canonical source-field mapping manifest |

#### Common raw-record envelope

Every normalized raw record must contain:

| Field | Logical dtype | Required | Meaning |
|---|---|---:|---|
| `raw_record_id` | string | YES | Immutable content/locator-derived row identity defined below |
| `raw_record_class` | string | YES | One of the canonical raw record classes above |
| `raw_schema_version` | string | YES | Human-readable schema version paired with immutable schema identity |
| `provider_name` | string | YES | Source provider identity |
| `source_dataset` | string | YES | Source dataset/product identity |
| `source_feed` | string | CONDITIONAL | Explicit material feed identity |
| `publisher_or_venue` | string | CONDITIONAL | Source publisher/venue scope |
| `source_object_sha256` | string | YES | Parent source-object identity |
| `source_row_locator` | string | YES | Deterministic locator within the immutable source object |
| `provider_record_id` | string | OPTIONAL | Provider-native record identifier when supplied |
| `provider_security_id_namespace` | string | CONDITIONAL | Namespace of any provider-native security identifier |
| `provider_security_id` | string | CONDITIONAL | Provider-native security identifier; never the universal canonical key |
| `symbol` | string | OPTIONAL | Provider symbol/ticker as an attribute, not continuity identity |
| `source_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Provider event/bar time normalized to a timezone-aware UTC instant |
| `source_asof_utc` | timestamp[ns, UTC] | CONDITIONAL | Source as-of/snapshot instant when applicable |
| `retrieved_at_utc` | timestamp[ns, UTC] | YES | Retrieval instant copied from the source-object manifest |
| `revision_id` | string | OPTIONAL | Provider revision identity when supplied |
| `raw_adjustment_state` | string | YES | `RAW_AS_TRADED`, `PROVIDER_ADJUSTED`, `NOT_APPLICABLE`, or `SOURCE_UNSPECIFIED` |
| `reference_snapshot_id` | string | OPTIONAL | Corporate-action/reference snapshot identity when applicable |
| `source_field_map_version` | string | YES | Human-readable field-mapping contract version |
| `source_field_map_identity` | string | YES | Immutable hash of the field-mapping manifest |
| `adapter_identity` | string | YES | Immutable adapter identity |
| `license_entitlement_ref` | string | OPTIONAL | Non-secret provenance reference where applicable |
| `payload_sha256` | string | YES | SHA-256 of canonical serialization of the captured source-field payload |
| `provider_extension_json` | string | OPTIONAL | Canonical JSON preserving material provider fields not represented by common columns |

Canonical financial numeric fields stored in raw normalized records use
`decimal128(38,10)` unless the source is intrinsically integral, in which case
`int64` is used. Timestamps are timezone-aware UTC instants; text is UTF-8 and
identifier text is not silently case-folded or normalized.

For every raw-schema table below, `YES` means the field is present and non-null
for every row of that class; `OPTIONAL` means the field is present in the
schema and may be null without a class-specific triggering condition; and
`CONDITIONAL` means the field is present in the schema and must be non-null
whenever the stated source-semantic condition applies, otherwise it is null.
These storage-field rules do not decide when an observation is legally
available to a historical cutoff; those chronology/availability rules remain
C6-C.

#### `raw_market_bar` class-specific fields

The common-envelope `source_time_utc` field is required for every
`raw_market_bar` and stores the provider bar/event timestamp under the
source-field mapping contract. The exact class-specific contract is:

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `source_time_utc` | timestamp[ns, UTC] | YES | Provider bar/event timestamp normalized to UTC; chronology-use validation remains C6-C |
| `open` | decimal128(38,10) | YES | Source open value under recorded source semantics |
| `high` | decimal128(38,10) | YES | Source high value under recorded source semantics |
| `low` | decimal128(38,10) | YES | Source low value under recorded source semantics |
| `close` | decimal128(38,10) | YES | Source close value under recorded source semantics |
| `volume` | int64 | YES | Source share-volume value under recorded source/feed semantics |
| `trade_count` | int64 | OPTIONAL | Source trade count when supplied |
| `vwap` | decimal128(38,10) | OPTIONAL | Source VWAP when supplied |

No class-specific `bar_end_utc` field is added to the normalized raw schema in
C6-B. Provider-native interval-end or other material timing semantics that are
not represented by `source_time_utc` remain preserved through the immutable
source object, source-field mapping, and `provider_extension_json`; the
canonical processed interval contract remains separate.

#### `raw_security_event` class-specific fields

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `event_type` | string | YES | Canonical event-category label under the source-field mapping |
| `event_payload_json` | string | YES | Canonical JSON containing the captured event-specific values |
| `event_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Dated event instant when the source supplies a distinct event timestamp |
| `effective_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Effective instant when the source explicitly supplies one |
| `source_asof_utc` | timestamp[ns, UTC] | CONDITIONAL | Common-envelope source snapshot/as-of instant when applicable |

`event_time_utc`, `effective_time_utc`, and `source_asof_utc` are storage and
provenance fields only. C6-C must still define availability, cutoff usability,
event-effective chronology, and no-lookahead validation.

#### `raw_reference_evidence` class-specific fields

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `evidence_type` | string | YES | Canonical evidence-category label |
| `document_or_record_id` | string | YES | Source document, filing, master-record, or equivalent source identifier |
| `evidence_value_json` | string | YES | Canonical JSON containing the captured evidence values |
| `evidence_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Dated evidence/document instant when the source supplies one |
| `effective_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Effective instant represented by the evidence when explicitly supplied |
| `source_asof_utc` | timestamp[ns, UTC] | CONDITIONAL | Common-envelope source snapshot/as-of instant when applicable |

These dated/as-of fields preserve source identity and reproducibility. C6-B
does not define the C6-C rule for when any evidence becomes available or may
be used at a formation cutoff.

`raw_record_id` is SHA-256 over canonical identity serialization of:
`raw_schema_version`, `raw_record_class`, `source_object_sha256`,
`source_row_locator`, and `payload_sha256`. A source-row locator must be stable
within the immutable source object and must not depend on a local absolute
path.

#### Source-field mapping contract

Each provider adapter must have a versioned source-field mapping manifest that
records source field/path, canonical field, source dtype, canonical dtype,
unit/scaling conversion, timestamp interpretation, nullability mapping, and
provider-semantic notes. Its canonical JSON SHA-256 is
`source_field_map_identity`. A semantic mapping change creates both a new
`source_field_map_version` and a new `source_field_map_identity`. Required canonical fields may not be silently
synthesized from unrelated provider fields. Material provider-only semantics
that do not fit common columns remain preserved in the source object and, when
needed, `provider_extension_json` rather than being discarded to create a
lowest-common-denominator schema.

## 5. Processed-data contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S11, S12]: processed data must be derived through
  governed provider-neutral data responsibilities rather than model-specific
  acquisition logic.
- `ACCEPTED_REQUIREMENT` [S12]: deterministic preparation must be tied to
  immutable dataset and split identities.
- `ACCEPTED_REQUIREMENT` [S7]: the canonical intraday representation must be
  capable of preserving the accepted official-session and provider-neutral
  hourly-bar semantics.
- `ACCEPTED_REQUIREMENT` [S6]: eligibility calculations using close, price,
  volume, and dollar-volume history must use only information available by
  the applicable point-in-time cutoff.
- `ACCEPTED_REQUIREMENT` [S11, S12]: silent imputation or silent dataset
  acceptance is prohibited.

### C6-B technical definition — canonical processed layer

`C6_B_DETAIL_DEFINED` — processed data is provider-neutral and contains only
non-model-specific canonical data products. Feature tensors, model observation
vectors, recurrent tensors, fitted preprocessing, and model-specific float
conversion are not processed-data responsibilities in C6-B.

The canonical processed layer contains these logical tables:

1. `processed_market_bar`;
2. `security_identifier_map`;
3. `processed_security_reference`;
4. `processed_universe_membership`; and
5. `lineage_edge`.

For the processed tables below, `YES` means present and non-null for every
applicable row; `OPTIONAL` means present in the schema and nullable without a
table-specific triggering condition; and `CONDITIONAL` means present in the
schema and non-null whenever the stated condition applies, otherwise null.
This defines storage schema and nullability only. C6-C retains chronology,
availability, calendar-validation, and missingness/reconstruction rules.

#### `processed_market_bar`

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `processed_row_id` | string | YES | Immutable processed-row identity defined in section 6 |
| `processed_schema_version` | string | YES | Human-readable processed-schema version paired with schema identity |
| `canonical_security_id` | string | YES | Stable project-scoped security continuity key |
| `bar_start_utc` | timestamp[ns, UTC] | YES | Canonical interval-start time identity |
| `bar_end_utc` | timestamp[ns, UTC] | YES | Canonical interval end represented by the processed row |
| `session_date_local` | date32 | YES | Exchange-local session date |
| `open` | decimal128(38,10) | YES | Canonical processed open |
| `high` | decimal128(38,10) | YES | Canonical processed high |
| `low` | decimal128(38,10) | YES | Canonical processed low |
| `close` | decimal128(38,10) | YES | Canonical processed close |
| `volume` | int64 | YES | Canonical processed share volume |
| `source_lineage_id` | string | YES | Deterministic row-to-raw lineage-set identity |
| `adjustment_lineage_id` | string | YES | Row-level adjustment-lineage identity defined in section 17 |
| `transformation_identity` | string | YES | Deterministic transformation identity defined in section 17 |

`bar_start_utc` is the canonical bar time identity already required by the
accepted interval-start convention. C6-C remains responsible for exact
calendar-version mechanics, expected-slot validation, DST checks, and
cross-exchange calendar-conflict validation.

#### `security_identifier_map`

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `processed_row_id` | string | YES | Immutable processed-row identity |
| `processed_schema_version` | string | YES | Human-readable processed-schema version |
| `canonical_security_id` | string | CONDITIONAL | Required when `mapping_status = RESOLVED`; null when no single safe canonical identity is established |
| `identifier_namespace` | string | YES | Preserved identifier namespace |
| `identifier_value` | string | YES | Identifier value exactly within its namespace |
| `mapping_status` | string | YES | One of `RESOLVED`, `UNRESOLVED`, or `CONFLICT` |
| `candidate_canonical_security_ids` | array[string] | YES | Sorted unique candidate IDs; exactly the resolved ID for `RESOLVED`, empty when none is established, multiple values permitted for `CONFLICT` |
| `source_evidence_ref` | string | YES | Governed evidence reference supporting the mapping state |
| `source_lineage_id` | string | YES | Deterministic row-to-raw lineage-set identity |
| `valid_from_utc` | timestamp[ns, UTC] | CONDITIONAL | Source-supported validity start when one exists |
| `valid_to_utc` | timestamp[ns, UTC] | CONDITIONAL | Source-supported validity end when one exists |

Unresolved or conflicting mappings may not be silently coerced to a resolved
canonical security identity. Exact point-in-time evidence-availability
validation remains C6-C.

#### `processed_security_reference`

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `processed_row_id` | string | YES | Immutable processed-row identity |
| `processed_schema_version` | string | YES | Human-readable processed-schema version |
| `canonical_security_id` | string | YES | Stable project-scoped security identity |
| `attribute_name` | string | YES | Canonical reference-attribute name |
| `attribute_value_json` | string | YES | Canonical JSON representation of the attribute value |
| `source_evidence_ref` | string | YES | Governed source-evidence reference |
| `source_lineage_id` | string | YES | Deterministic row-to-raw lineage-set identity |
| `transformation_identity` | string | YES | Deterministic transformation identity |
| `effective_time_utc` | timestamp[ns, UTC] | CONDITIONAL | Source-supported effective instant when the attribute/event has one |

C6-C defines later availability/no-lookahead validation; C6-B defines only the
persisted field, dtype, nullability, and lineage contract.

#### `processed_universe_membership`

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `processed_row_id` | string | YES | Immutable processed-row identity |
| `processed_schema_version` | string | YES | Human-readable processed-schema version |
| `canonical_security_id` | string | YES | Stable project-scoped security identity |
| `formation_time_utc` | timestamp[ns, UTC] | YES | Persisted formation-event identity; cutoff usability rules remain C6-C |
| `eligibility_state` | string | YES | Exactly `ELIGIBLE`, `INELIGIBLE`, or `UNRESOLVED_PROVIDER_MISSINGNESS` |
| `selected_flag` | boolean | YES | Whether the security belongs to the formed universe |
| `evidence_bundle_id` | string | YES | Deterministic identity of supporting raw evidence |
| `source_lineage_id` | string | YES | Deterministic row-to-raw lineage-set identity |
| `transformation_identity` | string | YES | Deterministic transformation identity |
| `liquidity_rank` | int64 | CONDITIONAL | Accepted dollar-volume rank when established |
| `median_60_session_dollar_volume` | decimal128(38,10) | CONDITIONAL | Accepted liquidity statistic when established |
| `primary_listing_exchange` | string | CONDITIONAL | Governed primary-listing value when established |

The nullable/conditional fields above remain null when the governed evidence
does not establish them; absence is not silently converted into a failing
scientific value.

#### `lineage_edge`

| Field | Logical dtype | Requiredness | Stored meaning |
|---|---|---:|---|
| `lineage_edge_id` | string | YES | Immutable lineage-edge identity defined in section 6 |
| `child_table` | string | YES | Schema-defined logical child-table name |
| `child_row_id` | string | YES | Child processed-row identity |
| `parent_raw_record_id` | string | YES | Parent raw-record identity |
| `relationship_type` | string | YES | Canonical lineage relationship label |
| `transformation_identity` | string | YES | Exact transformation identity that produced the child relation |

A processed row with multiple raw parents has multiple lineage edges; lineage
is never inferred from filenames, row position, or a machine-local path.

Every logical table name used in `processed_row_id` construction is the exact
schema-defined table-name constant shown in this section. It is a
`schema_identity`-covered context value, not a mutable filename or inferred
runtime label. Every table using `processed_row_id` persists
`processed_schema_version`, so each row-ID input is either a required persisted
field or an explicit immutable schema-context constant.

All processed financial numeric values use `decimal128(38,10)` unless
intrinsically integral, in which case `int64` is used. Boolean state uses
`boolean`; timestamps use timezone-aware `timestamp[ns, UTC]`; local session
dates use `date32`; text uses UTF-8. Arrays use the element dtype shown and are
canonically ordered where their semantics are set-like. Any later
model-specific floating-point conversion belongs to later model/data-interface
work, not to this canonical processed identity.

```text
FEATURE_GENERATION = OUT_OF_SCOPE
MODEL_SPECIFIC_TENSORS = OUT_OF_SCOPE
C6_C_CHRONOLOGY_RULES =
DEFINED_IN_SECTIONS_7_THROUGH_10__C6_C_COMPLETE_PUBLISHED_EFFECTIVE
```

Feature generation remains outside C6-B and is not performed or specified as
executable behavior here.

## 6. Identity, ordering, and uniqueness

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S6]: stable security identity is the continuity key.
- `ACCEPTED_REQUIREMENT` [S6]: ticker changes do not reset eligible-history
  continuity when stable security identity is preserved.
- `ACCEPTED_REQUIREMENT` [S6]: separately listed ordinary-common-share classes
  are evaluated as separate securities.
- `ACCEPTED_REQUIREMENT` [S6]: a successor security does not inherit the
  predecessor's 252-session history merely because of economic succession.
- `ACCEPTED_REQUIREMENT` [S6]: exact liquidity-ranking ties are broken by
  stable security identifier ascending, with identifier namespace preserved.
- `ACCEPTED_REQUIREMENT` [S3, S10]: the dataset contract must preserve stable
  row, security, and time identity.

### C6-B technical definition — security, row, ordering, and uniqueness

`C6_B_DETAIL_DEFINED` — `canonical_security_id` is the project-scoped stable
security continuity key. It is an opaque UTF-8 string stored in the immutable
security-identity registry, is never reused for another security, survives
ticker changes when the same security continues, and is distinct for
separately listed ordinary-common-share classes. A successor security receives
a distinct canonical identity and cannot inherit predecessor history merely
through economic succession.

Ticker/symbol, primary-listing exchange, and every provider-native identifier
are attributes mapped through `security_identifier_map`; none is the sole
canonical continuity key. The registry preserves every identifier namespace
and source-evidence reference. Actual canonical ID values are created only
when later dataset generation is authorized; C6-B defines their required
properties and registry contract rather than inventing current securities.
Given a frozen registry version, every resolvable provider identifier maps
deterministically to the same `canonical_security_id`. Unresolved or
conflicting mappings remain explicit and are never guessed.

#### Immutable security-identity registry contract

`C6_B_DETAIL_DEFINED` — the security-identity registry is a canonical JSON
artifact with a schema header and an ordered `records` array. Its schema header
contains:

| Field | Logical dtype | Requiredness |
|---|---|---:|
| `registry_schema_version` | string | YES |
| `registry_schema_identity` | string | YES |
| `records` | array[registry_record] | YES |

Each `registry_record` has the exact contract:

| Field | Logical dtype | Requiredness | Meaning |
|---|---|---:|---|
| `canonical_security_id` | string | CONDITIONAL | Required only when one safe project identity is established |
| `identifier_namespace` | string | YES | Preserved source/canonical identifier namespace |
| `identifier_value` | string | YES | Identifier value within that namespace |
| `mapping_status` | string | YES | `RESOLVED`, `UNRESOLVED`, or `CONFLICT` |
| `candidate_canonical_security_ids` | array[string] | YES | Sorted unique candidate IDs; one equal to `canonical_security_id` for `RESOLVED`, empty when none exists, multiple permitted for `CONFLICT` |
| `source_evidence_refs` | array[string] | YES | Sorted unique governed evidence references supporting the mapping state |
| `valid_from_utc` | timestamp[ns, UTC] | CONDITIONAL | Source-supported validity start when present |
| `valid_to_utc` | timestamp[ns, UTC] | CONDITIONAL | Source-supported validity end when present |

Actual `canonical_security_id` values are not created in C6-B. The registry
schema merely defines how later authorized identity resolution must be
recorded. The exact evidence-availability/no-lookahead rules governing whether
a mapping is usable at a historical cutoff remain C6-C.

`registry_schema_identity` is SHA-256 over the canonical schema specification
for the registry header and record fields under the section-17 canonical JSON
rules. Before hashing the registry artifact, each record's set-like arrays are
sorted uniquely and the `records` array is sorted ascending by:

1. `identifier_namespace`;
2. `identifier_value`;
3. `valid_from_utc`, with null after non-null;
4. `valid_to_utc`, with null after non-null;
5. `mapping_status`;
6. `canonical_security_id`, with null after non-null;
7. canonical serialization of `candidate_canonical_security_ids`; and
8. canonical serialization of `source_evidence_refs`.

The exact canonical registry artifact hashed for identity is the UTF-8
canonical JSON object containing `registry_schema_version`,
`registry_schema_identity`, and the ordered `records` array.

```text
security_identity_registry_sha256 =
SHA256(EXACT_CANONICAL_SECURITY_REGISTRY_ARTIFACT_BYTES)
```

A human-readable `registry_version` is derived after hashing as
`security-registry-<registry_schema_version>-<first-12-hex-of-registry-sha256>`.
It is descriptive and is not an input to
`security_identity_registry_sha256`, preventing self-reference. For a
security-bearing dataset, the full registry SHA-256 is required in provenance
and dataset identity. For a dataset role to which no security registry is
semantically applicable, the exact identity input is the literal
`NOT_APPLICABLE`; null, omission, or a machine-local registry path is not an
equivalent substitute.

#### Canonical row identities

- `raw_record_id` uses the exact SHA-256 construction defined in section 4.
- `processed_row_id` is SHA-256 over canonical identity serialization of
  `processed_schema_version`, the exact schema-defined logical table-name
  constant, and that table's natural-key values. `processed_schema_version` is
  a required persisted field on every table using `processed_row_id`; the
  logical table name is an immutable `schema_identity`-covered context value.
  The row ID does not include mutable filenames, local paths, retrieval order,
  or dataset row position.
- `lineage_edge_id` is SHA-256 over child table, child row ID, parent raw
  record ID, relationship type, and transformation identity.
- `evidence_bundle_id` is SHA-256 over the sorted unique set of supporting raw
  record IDs plus the applicable evidence-bundle schema version.

#### Natural keys and uniqueness

| Table/class | Canonical natural key |
|---|---|
| normalized raw record | `source_object_sha256`, `source_row_locator`, `raw_record_class` |
| `processed_market_bar` | `canonical_security_id`, `bar_start_utc` |
| `security_identifier_map` | `canonical_security_id`, `identifier_namespace`, `identifier_value`, `valid_from_utc` |
| `processed_security_reference` | `canonical_security_id`, `attribute_name`, `effective_time_utc`, `source_evidence_ref` |
| `processed_universe_membership` | `formation_time_utc`, `canonical_security_id` |
| `lineage_edge` | `child_table`, `child_row_id`, `parent_raw_record_id`, `relationship_type` |

A duplicate processed natural key is a structural conflict and must not be
silently deduplicated or last-write-wins overwritten. A hash collision in
which equal identity hashes correspond to unequal canonical identity tuples is
a hard identity conflict. C6-B requires the conflict to remain visible; C6-F
later defines executable acceptance disposition.

#### Deterministic ordering

Canonical serialization and persisted ordering use stable ascending order with
UTF-8 binary collation for strings, chronological ascending order for
timestamps, numeric ascending order for numbers, and nulls after non-null
values. The table-specific primary ordering is:

- raw records: `raw_record_class`, `provider_name`, `source_dataset`,
  `source_object_sha256`, `source_row_locator`, `raw_record_id`;
- market bars: `canonical_security_id`, `bar_start_utc`, `processed_row_id`;
- identifier mappings: `canonical_security_id`, `identifier_namespace`,
  `valid_from_utc`, `identifier_value`, `source_evidence_ref`;
- security reference: `canonical_security_id`, `attribute_name`,
  `effective_time_utc`, `source_evidence_ref`, `processed_row_id`;
- universe membership: `formation_time_utc`, `liquidity_rank`,
  `canonical_security_id`, `processed_row_id`; and
- lineage edges: `child_table`, `child_row_id`, `parent_raw_record_id`,
  `relationship_type`.

The already accepted liquidity-ranking tie-break remains stable security
identifier ascending with namespace preserved; nothing in this ordering
contract introduces future information.

### C6-C technical definition — chronological validity and duplicate conflicts

`C6_C_DETAIL_DEFINED` — persisted deterministic ordering remains exactly the
C6-B ordering contract. Chronological validity is a separate C6-C validation
property and does not alter C6-B row identity, security identity, natural-key
construction, or deterministic persisted ordering.

For `processed_market_bar`, the canonical natural key remains:

```text
canonical_security_id
+
bar_start_utc
```

More than one processed market-bar row for the same
`canonical_security_id` and `bar_start_utc` is a chronology/uniqueness
conflict. Such a conflict must not be resolved through last-write-wins
selection, silent deduplication, averaging, retrieval order, or any equivalent
implicit preference.

Equal-looking OHLCV or other values do not erase the duplicate-lineage
conflict. Every underlying raw/source record and lineage edge remains
preserved. The conflict remains explicit and fail-closed until separately
governed source reconciliation establishes the valid canonical observation.

```text
DUPLICATE_SECURITY_TIMESTAMP_RULE =
FAIL_CLOSED_UNTIL_GOVERNED_SOURCE_RECONCILIATION

C6_B_IDENTITY_CONSTRUCTION_CHANGED = NO
```

## 7. Timestamp, time-zone, session, and calendar contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S7]: the canonical research calendar follows the
  applicable official U.S. cash-equity core/regular session for NYSE,
  NYSE American, and Nasdaq, including official holidays and early closes.
- `ACCEPTED_REQUIREMENT` [S7]: exchange-local timezone is
  `America/New_York`.
- `ACCEPTED_REQUIREMENT` [S7]: normal regular session is 09:30–16:00 local
  time, with an official early close overriding 16:00.
- `ACCEPTED_REQUIREMENT` [S7]: weekends, full-day exchange holidays, and other
  officially closed sessions are excluded; synthetic regular-session bars
  must not be created.
- `ACCEPTED_REQUIREMENT` [S7]: extended hours are excluded.
- `ACCEPTED_REQUIREMENT` [S7]: construct the local session under
  `America/New_York` first and then convert that date's instants to UTC; a
  fixed UTC offset is prohibited.
- `ACCEPTED_REQUIREMENT` [S7]: internal timestamps are timezone-aware UTC
  instants while retaining exchange-local session date/calendar identity.
- `ACCEPTED_REQUIREMENT` [S7]: hourly bars are anchored at 09:30 local time.
- `ACCEPTED_REQUIREMENT` [S7]: hourly intervals are half-open `[START, END)`,
  nominally 60 minutes, with the end capped at official session close.
- `ACCEPTED_REQUIREMENT` [S7]: canonical bar timestamp is interval start/open
  time.
- `ACCEPTED_REQUIREMENT` [S7]: the final truncated regular-session interval is
  preserved rather than dropped, padded to 60 minutes, or extended across a
  session boundary.
- `ACCEPTED_REQUIREMENT` [S7]: official exchange-specific calendars remain
  authoritative; if a material authoritative divergence exists, the
  security's primary-listing exchange controls.

### C6-C technical definition — calendar, session, and expected-slot validation

`C6_C_DETAIL_DEFINED` — calendar/session chronology is represented through
governed validation metadata and artifacts operating on the existing C6-B
schema. C6-C adds no canonical raw or processed table and no new C6-B persisted
schema field.

For each applicable security/session validation context, the governed
representation must establish:

| Validation item | Required representation |
|---|---|
| `eligible_primary_listing_exchange` | Governed eligible primary-listing exchange identity |
| `authoritative_calendar_source_identity` | Identity of the authoritative exchange-calendar source |
| `calendar_version_or_snapshot_identity` | Immutable version or snapshot identity of the governed calendar representation |
| `calendar_identity_ref` | Deterministic calendar identity defined below |
| `exchange_timezone` | Exactly `America/New_York` |
| `session_date_local` | Exchange-local regular-session date |
| `official_session_open_local` | Published official regular-session open local time |
| `official_session_close_local` | Published official regular-session close local time |
| `session_open_utc` | UTC instant derived from the official local open |
| `session_close_utc` | UTC instant derived from the official local close |
| `official_early_close_flag` | Boolean indicator that the published official close is earlier than the normal close |
| `expected_bar_slot_ordinal` | Zero-based deterministic slot ordinal within the applicable regular session |
| `expected_bar_start_local` | Expected slot start in exchange-local time |
| `expected_bar_end_local` | Expected slot end in exchange-local time |
| `expected_bar_start_utc` | UTC conversion of the expected local slot start |
| `expected_bar_end_utc` | UTC conversion of the expected local slot end |
| `final_partial_slot_flag` | Boolean indicator that the final slot is truncated by the official session close |

`calendar_identity_ref` is the lowercase-hex SHA-256 of canonical JSON
containing the governed authoritative calendar-source identity,
calendar-version/snapshot identity, eligible primary-listing exchange,
`America/New_York` timezone interpretation, and the deterministically ordered
official session representation required for the applicable calendar scope.
A machine-local path, mutable filename, provider default, or unrecorded
timezone assumption is not a calendar identity.

Expected hourly slots are derived from the applicable official session. The
grid is anchored at 09:30 local time, uses half-open `[START, END)` intervals,
uses nominal 60-minute intervals, caps each interval end at the official
session close, preserves the resulting final truncated interval, and never
crosses a session boundary.

```text
EXPECTED_SLOT =
DERIVED_FROM_THE_APPLICABLE_OFFICIAL_SESSION

CLOSED_SESSION =
NO_EXPECTED_REGULAR_SESSION_SLOTS

EXTENDED_HOURS =
OUT_OF_SCOPE
```

DST handling is deterministic: construct the official session in
`America/New_York` first, resolve that local date under the applicable IANA
timezone rules, and only then convert the resulting instants to UTC. Fixed
UTC-5, fixed UTC-4, or any other hard-coded offset assumption is prohibited.

For an official early close, the published official close controls. The
expected slot grid is regenerated for that shortened session; the truncated
last interval is preserved, the session is not extended to 16:00, and the
short final interval is not padded to 60 minutes.

Official exchange-specific calendar identity is preserved. If material
authoritative calendars diverge, the security's governed primary-listing
exchange controls. Unresolved or conflicting primary-exchange evidence must
not silently fall back to a different exchange calendar, and unresolved
calendar identity is fail-closed for affected chronology validation.

No calendar data is acquired by this specification work package.

## 8. Point-in-time and chronology/leakage contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S5]: historical study window is
  2024-09-03 through 2026-08-31 inclusive.
- `ACCEPTED_REQUIREMENT` [S5]: first formation is the
  2024-09-03 regular-session open using only information available through the
  completed 2024-08-30 regular session.
- `ACCEPTED_REQUIREMENT` [S5, S7]: scheduled universe reformation occurs
  monthly at the open of the first regular session of each calendar month
  using only information available through the immediately preceding
  completed regular session.
- `ACCEPTED_REQUIREMENT` [S5]: the 252-session eligibility-history lookback
  may extend before the accepted study window without changing the study
  window.
- `ACCEPTED_REQUIREMENT` [S6]: future corporate actions must not be applied to
  earlier formation cutoffs.
- `ACCEPTED_REQUIREMENT` [S6]: current/survivor-only status must not be used
  to reconstruct historical eligibility.
- `ACCEPTED_REQUIREMENT` [S6]: security-type, incorporation, SPAC status, and
  primary-listing evidence must be dated and available by the applicable
  formation cutoff.
- `ACCEPTED_REQUIREMENT` [S3, S10]: C6 must preserve deterministic
  chronological folds and leakage-safe time ordering.
- `ACCEPTED_REQUIREMENT` [S10]: preprocessing/fitting must respect training
  boundaries, with explicit embargo where required.

### C6-C technical definition — PIT availability and leakage control

`C6_C_DETAIL_DEFINED` — the controlling chronology principle is:

```text
INFORMATION_USABLE_AT_DECISION_TIME_T =
ONLY_INFORMATION_ESTABLISHED_AS_AVAILABLE_BY_T
AND
ONLY_STATE_OR_EVENT_EFFECTS_APPLICABLE_BY_T
```

Retrieval time is provenance and is not historical availability evidence by
itself. C6-C distinguishes:

- source/event observation time — the source observation, event, evidence, or
  bar time represented by existing fields such as `source_time_utc`,
  `event_time_utc`, or `evidence_time_utc`;
- effective time — `effective_time_utc`, when the represented state or event
  takes effect;
- source as-of time — `source_asof_utc`, when the source explicitly represents
  a snapshot or as-of semantic;
- retrieval time — `retrieved_at_utc`, when the source object was obtained for
  project provenance; and
- decision/formation cutoff time — the governed instant at which historical
  usability is evaluated.

```text
RETRIEVED_AT_UTC =
PROVENANCE_ONLY__NOT_PROOF_OF_HISTORICAL_AVAILABILITY

SOURCE_ASOF_UTC =
SOURCE_SNAPSHOT_OR_AS_OF_SEMANTIC_WHEN_APPLICABLE

EFFECTIVE_TIME_UTC =
WHEN_THE_REPRESENTED_STATE_OR_EVENT_TAKES_EFFECT
```

Historical use requires sufficient governed dated evidence and lineage
showing that the information was available no later than the applicable
decision cutoff. A later retrieval does not by itself prove or disprove
historical availability; the historical source/as-of/event evidence must
establish it.

For a state or event change, knowledge and effectiveness are separate
conditions. Information becoming known does not make a future effective state
apply before `effective_time_utc`. Conversely, an event whose effective time
has arrived cannot be used in historical reconstruction before its historical
availability is established. Applicable historical state therefore requires
both the availability condition and the effective-time condition to be
satisfied.

For completed market bars, `bar_start_utc` remains the canonical interval-start
identity. OHLC, volume, VWAP, trade count, and other completed-bar contents are
not available at that interval start. Such contents become eligible for
downstream feature use only after `bar_end_utc` and after any stricter governed
source-availability condition has been satisfied. A decision at a bar open
cannot use that bar's eventual close, high, low, volume, VWAP, or trade count.

Although feature-generation execution remains unauthorized, any later feature
or transformation governed by this contract must satisfy all of the following:

- every value depends only on inputs available by its decision cutoff;
- rolling windows are trailing-only;
- centered rolling windows are prohibited;
- negative shifts or future leads are prohibited;
- future-normalized statistics are prohibited;
- full-sample fitted transformations are prohibited;
- future-informed imputation is prohibited;
- fitted preprocessing uses training information only;
- transformation availability cannot precede the latest required input
  availability; and
- cross-sectional calculations at a decision time use only securities and
  values valid under that same cutoff.

Formation chronology remains:

```text
FIRST_FORMATION =
2024-09-03_REGULAR_SESSION_OPEN

FIRST_FORMATION_INFORMATION_CUTOFF =
THROUGH_THE_COMPLETED_2024-08-30_REGULAR_SESSION

MONTHLY_REFORMATION =
FIRST_REGULAR_SESSION_OPEN_OF_EACH_CALENDAR_MONTH

REFORMATION_INFORMATION_CUTOFF =
THROUGH_THE_IMMEDIATELY_PRECEDING_COMPLETED_REGULAR_SESSION
```

Formation-morning information arising after the immediately preceding
completed regular session is not usable for the formation decision.

C6-C also establishes a no-overlap invariant for forward targets and labels. A
training example whose target/label depends on future information extending
into a later validation, qualification, or other governed decision region
cannot remain in the earlier training information set. Such observations must
be excluded from the earlier information set under the later partition
implementation.

Embargo applicability is required whenever forward target/label information
would otherwise cross a governed partition boundary. C6-C establishes that
invariant but does not choose partition dates or fold geometry.

```text
HORIZON_OVERLAP_ACROSS_GOVERNED_PARTITION_BOUNDARY =
PROHIBITED

EMBARGO_APPLICABILITY =
REQUIRED_WHEN_FORWARD_TARGET_OR_LABEL_INFORMATION_WOULD_CROSS_A_GOVERNED_PARTITION_BOUNDARY

EXACT_FOLD_GEOMETRY =
DEFINED_IN_SECTION_15__C6_E_COMPLETE_PUBLISHED_EFFECTIVE

EXACT_PARTITION_BOUNDARIES =
DEFINED_IN_SECTION_15__C6_E_COMPLETE_PUBLISHED_EFFECTIVE
```

Published/effective C6-E instantiates the exact chronological partition
geometry and embargo rules in section 15.

## 9. Missingness and reconstruction representation

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S4, S6]: provider coverage/missingness is distinct
  from genuine historical security ineligibility.
- `ACCEPTED_REQUIREMENT` [S6]: universe eligibility preserves three states:
  `ELIGIBLE`, `INELIGIBLE`, and
  `UNRESOLVED_PROVIDER_MISSINGNESS`.
- `ACCEPTED_REQUIREMENT` [S6]: absent required SIP observations must be
  classified as provider missingness rather than replaced with IEX volume or
  zero volume.
- `ACCEPTED_REQUIREMENT` [S6]: missing provider data must not be interpreted
  as delisting, zero trading, or another eligibility failure.
- `ACCEPTED_REQUIREMENT` [S7]: closed-session bars must not be synthesized.
- `ACCEPTED_REQUIREMENT` [S11, S12]: reconstruction/missingness handling must
  be explicit and silent imputation is prohibited.

### C6-C technical definition — expected-slot missingness and reconstruction

`C6_C_DETAIL_DEFINED` — absence is interpreted only after the applicable
calendar/session expected-slot validation has been established. The minimum
row/slot chronology classification is:

```text
OBSERVED_UNIQUE
EXPECTED_SLOT_MISSING
NOT_EXPECTED_CLOSED_SESSION
DUPLICATE_SLOT_CONFLICT
UNRESOLVED_CALENDAR
```

`OBSERVED_UNIQUE` requires exactly one valid governed observation for the
expected security × slot. `EXPECTED_SLOT_MISSING` means the official calendar
requires a slot but no valid unique governed observation resolves it.
`NOT_EXPECTED_CLOSED_SESSION` means the applicable official calendar defines
no regular-session slot. `DUPLICATE_SLOT_CONFLICT` preserves the section-6
duplicate conflict. `UNRESOLVED_CALENDAR` means expected-slot status itself
cannot be established fail-closed.

Field-level validation must distinguish at least:

```text
VALUE_PRESENT
SOURCE_NULL_OR_MISSING
OPTIONAL_SOURCE_FIELD_NOT_SUPPLIED
INVALID_OR_UNUSABLE_VALUE
STRUCTURALLY_NOT_APPLICABLE
```

None of those non-present states may be silently converted into a valid
numerical observation.

For market bars:

```text
MISSING_EXPECTED_BAR =
EXPLICIT_UNRESOLVED_MISSINGNESS
```

A missing expected bar is not zero volume, unchanged price, delisting,
ineligibility, market closure, or a valid flat bar.

The following reconstruction operations are prohibited:

```text
FORWARD_FILL =
PROHIBITED_FOR_MISSING_MARKET_BAR_OHLCV

BACKWARD_FILL_FROM_FUTURE =
PROHIBITED

LINEAR_OR_OTHER_PRICE_INTERPOLATION =
PROHIBITED

SYNTHETIC_OHLC_TO_HIDE_GAP =
PROHIBITED

SYNTHETIC_ZERO_VOLUME_BAR =
PROHIBITED

CROSS_SESSION_CARRY =
PROHIBITED

PADDING_A_TRUNCATED_FINAL_BAR =
PROHIBITED

CREATING_A_BAR_FOR_A_CLOSED_SESSION =
PROHIBITED
```

Automatic alternate-provider substitution is not authorized. A gap may be
resolved only through separately governed source evidence that preserves
source/provenance identity and satisfies the applicable semantic and PIT
requirements. Until then, the gap remains explicit.

The minimum reconstruction-state representation is:

```text
ORIGINAL_OBSERVATION
GOVERNED_SOURCE_RESOLUTION
UNRESOLVED_MISSINGNESS
```

No reconstruction state may conceal synthetic financial values. C6-C defines
representation and fail-closed chronology validation only; it does not execute
reconstruction or dataset acceptance.

```text
MISSINGNESS_ACCEPTANCE_RULES =
DEFINED_IN_SECTION_18__C6_F_COMPLETE_PUBLISHED_EFFECTIVE

ARBITRARY_MINIMUM_OBSERVED_BAR_PERCENTAGE = NONE
```

Acceptance uses explicit missingness classification and complete expected-slot
accounting, not an arbitrary observed-bar threshold. C6-A did not choose an
imputation or reconstruction algorithm.

## 10. Universe-membership and eligibility provenance

### Accepted requirements — security and listing

- `ACCEPTED_REQUIREMENT` [S6]: eligible security type is U.S.-incorporated
  ordinary common shares only.
- `ACCEPTED_REQUIREMENT` [S6]: eligible primary listings are NYSE,
  NYSE American, and Nasdaq.
- `ACCEPTED_REQUIREMENT` [S6]: exclude ETFs, ETNs, closed-end funds, ADRs,
  foreign ordinary shares, preferred stock, OTC securities at formation,
  warrants, rights, units, SPAC/pre-combination securities, and other
  non-ordinary equity structures.
- `ACCEPTED_REQUIREMENT` [S6]: separately listed ordinary-common-share classes
  remain separate securities.
- `ACCEPTED_REQUIREMENT` [S6]: at formation, each security must be PIT active
  and primary-listed on an eligible exchange, with no effective hard terminal
  event at or before the formation open.

### Accepted requirements — history and coverage

- `ACCEPTED_REQUIREMENT` [S6]: minimum pre-formation history is
  252 completed regular sessions.
- `ACCEPTED_REQUIREMENT` [S6]: minimum valid daily price/trade observations are
  240 of 252.
- `ACCEPTED_REQUIREMENT` [S6]: immediately preceding valid close must be at
  least USD 5.00.
- `ACCEPTED_REQUIREMENT` [S6]: median preceding 20 as-traded closes must be at
  least USD 5.00 with at least 19 valid observations of 20.
- `ACCEPTED_REQUIREMENT` [S6]: liquidity lookback is 60 completed regular
  sessions.
- `ACCEPTED_REQUIREMENT` [S6]: daily dollar volume is regular-session close
  multiplied by regular-session share volume.
- `ACCEPTED_REQUIREMENT` [S6]: median 60-session dollar volume must be at least
  USD 20,000,000 with at least 57 valid observations of 60.
- `ACCEPTED_REQUIREMENT` [S6]: required liquidity observations and ranking use
  Alpaca historical stock feed SIP with explicit `feed=sip` when that source
  is applicable; IEX and SIP volume must not be mixed.

### Accepted requirements — formation and turnover of membership

- `ACCEPTED_REQUIREMENT` [S5]: scheduled reformation is monthly at the first
  regular-session open using the preceding completed regular session as the
  information cutoff.
- `ACCEPTED_REQUIREMENT` [S5, S6]: a security is removed when a hard terminal
  event becomes effective.
- `ACCEPTED_REQUIREMENT` [S5, S6]: `MID_CYCLE_BACKFILL = NONE`.
- `ACCEPTED_REQUIREMENT` [S5]: a vacated slot remains vacant until the next
  scheduled monthly reformation.

### Accepted requirements — ranking and underfill

- `ACCEPTED_REQUIREMENT` [S6]: eligible securities are ranked by trailing
  60-completed-session median daily dollar volume descending.
- `ACCEPTED_REQUIREMENT` [S6]: if 60 or more securities are eligible, select
  exactly 60.
- `ACCEPTED_REQUIREMENT` [S6]: if 50–59 securities are eligible, use all
  eligible securities without relaxing thresholds.
- `ACCEPTED_REQUIREMENT` [S6]: below 50 is
  `UNDERFILLED_BELOW_ACCEPTED_RANGE` and requires review before universe
  construction proceeds.
- `ACCEPTED_REQUIREMENT` [S6]: exact ties use stable security identifier
  ascending with namespace preserved.
- `ACCEPTED_REQUIREMENT` [S6, S7]: no sector, industry, market-cap, market
  regime, or other diversity quota is used as a security-level selection
  quota.

### Source reconciliation note

`SOURCE_RECONCILIATION_NOTE` — the C6-A task brief describes an
"acceptable range = 50 to 75." The current canonical C5 eligibility decision
reviewed directly establishes the target/underfill rules above but does not
establish 75 as a separate upper-bound rule. Because 60-or-more eligible
securities are reduced to exactly 60, C6-A does not manufacture a
`MAXIMUM_ACCEPTABLE_UNIVERSE = 75` requirement.

If an independent 75-security upper bound is intended, Managing must identify
or establish its canonical source before contract freeze.

### C6-B persisted representation

`C6_B_DETAIL_DEFINED` — persisted universe membership uses the
`processed_universe_membership` table defined in section 5. Its security
continuity field is `canonical_security_id`; symbol is not a membership key.
`formation_time_utc` identifies the formation event, `eligibility_state`
preserves the three already accepted eligibility states, `selected_flag`
records whether the security is in the formed universe, and `liquidity_rank`
records the accepted dollar-volume ranking when defined.

`evidence_bundle_id` must resolve to the exact sorted set of raw evidence
records supporting the security's eligibility/ranking result, including the
applicable provider/feed and PIT reference evidence. `source_lineage_id` and
`transformation_identity` connect the membership row to its raw parents and
deterministic transformation specification. `primary_listing_exchange` and
`median_60_session_dollar_volume` are stored when established by the governed
source material; absence is never silently converted into a failing value.

### C6-C technical definition — formation cutoff and PIT evidence availability

`C6_C_DETAIL_DEFINED` — formation chronology validation is derived from the
existing `formation_time_utc`, the applicable official exchange calendar, the
immediately preceding completed official regular session, governed PIT
evidence, and the existing source/effective/as-of fields and lineage.

C6-C defines the validation-level value:

```text
FORMATION_INFORMATION_CUTOFF_UTC =
OFFICIAL_CLOSE_INSTANT_OF_THE_IMMEDIATELY_PRECEDING_COMPLETED_REGULAR_SESSION
```

`FORMATION_INFORMATION_CUTOFF_UTC` is a derived chronology-validation value
and is not a new C6-B persisted schema field.

For the first formation at the 2024-09-03 regular-session open, this cutoff is
the official close instant of the completed 2024-08-30 regular session. For
each scheduled monthly reformation, it is derived from the immediately
preceding completed official regular session.

Eligibility and ranking evidence is usable only when governed historical
availability is established no later than the applicable
`FORMATION_INFORMATION_CUTOFF_UTC`. Lookback calculations use only completed
regular sessions permitted by that cutoff. Formation-morning information after
the preceding completed session is excluded.

Future corporate actions must not alter earlier eligibility. For a hard
terminal event, a security is not removed before the event becomes effective,
and the event is not used before its historical availability is established.
Historical-universe state therefore respects both effective-time and
availability conditions.

The accepted membership mechanics remain unchanged:

```text
MID_CYCLE_BACKFILL =
NONE
```

Nothing in this C6-C definition changes the accepted ranking rule, 60-security
selection rule, 50-to-59 underfill handling, below-50 review state, tie-break
rule, or the separate 75-security source-reconciliation note.

### C6G-FIND-002 correction — universe rule specification identity

`universe_definition_identity` is the upstream RULE_SPECIFICATION_IDENTITY of
the accepted universe definition, not REALIZED_MEMBERSHIP_IDENTITY and not a
dataset identity. The complete versioned canonical payload has these fields
and values, transcribing the accepted rules above:

| Field | Canonical value |
|---|---|
| `universe_definition_spec_version` | `"1"` |
| `eligible_security_type_rule` | `"US_INCORPORATED_ORDINARY_COMMON_SHARES_ONLY__SEPARATELY_LISTED_CLASSES_ARE_SEPARATE_SECURITIES"` |
| `eligible_primary_listing_exchange_set` | `["NYSE", "NYSE American", "Nasdaq"]` |
| `excluded_security_structure_rules` | `["ADRs", "ETFs", "ETNs", "OTC securities at formation", "SPAC/pre-combination securities", "closed-end funds", "foreign ordinary shares", "other non-ordinary equity structures", "preferred stock", "rights", "units", "warrants"]` |
| `formation_PIT_active_listing_rule` | `"PIT_ACTIVE_AND_PRIMARY_LISTED_ON_ELIGIBLE_EXCHANGE_AT_FORMATION"` |
| `hard_terminal_event_rule` | `"NO_EFFECTIVE_HARD_TERMINAL_EVENT_AT_OR_BEFORE_FORMATION_OPEN"` |
| `minimum_completed_history_sessions` | `252` |
| `minimum_valid_history_observations` | `240` |
| `immediately_preceding_valid_close_minimum_usd` | `5` |
| `median_close_lookback_sessions` | `20` |
| `minimum_valid_median_close_observations` | `19` |
| `median_close_minimum_usd` | `5` |
| `liquidity_lookback_sessions` | `60` |
| `minimum_valid_liquidity_observations` | `57` |
| `median_daily_dollar_volume_minimum_usd` | `20000000` |
| `daily_dollar_volume_definition` | `"REGULAR_SESSION_CLOSE_TIMES_REGULAR_SESSION_SHARE_VOLUME"` |
| `applicable_liquidity_feed_rule` | `"ALPACA_HISTORICAL_STOCK_SIP__EXPLICIT_feed=sip_WHEN_APPLICABLE__NO_IEX_SIP_VOLUME_MIXING"` |
| `first_formation_rule` | `"2024-09-03_REGULAR_SESSION_OPEN"` |
| `scheduled_reformation_rule` | `"MONTHLY_FIRST_REGULAR_SESSION_OPEN"` |
| `formation_information_cutoff_rule` | `"OFFICIAL_CLOSE_OF_IMMEDIATELY_PRECEDING_COMPLETED_REGULAR_SESSION__FIRST_CUTOFF_2024-08-30__AVAILABLE_BY_CUTOFF_ONLY"` |
| `hard_terminal_removal_rule` | `"REMOVE_WHEN_EFFECTIVE_AND_HISTORICALLY_AVAILABLE__NEVER_BEFORE_EITHER"` |
| `mid_cycle_backfill_rule` | `"NONE__VACATED_SLOT_REMAINS_VACANT_UNTIL_NEXT_SCHEDULED_MONTHLY_REFORMATION"` |
| `liquidity_ranking_rule` | `"TRAILING_60_COMPLETED_SESSION_MEDIAN_DAILY_DOLLAR_VOLUME_DESCENDING"` |
| `ranking_tie_break_rule` | `"STABLE_SECURITY_IDENTIFIER_ASCENDING_WITH_NAMESPACE_PRESERVED"` |
| `selection_rule_when_eligible_count_ge_60` | `"SELECT_EXACTLY_60"` |
| `selection_rule_when_eligible_count_50_through_59` | `"USE_ALL_ELIGIBLE_WITHOUT_RELAXING_THRESHOLDS"` |
| `underfilled_below_50_rule` | `"UNDERFILLED_BELOW_ACCEPTED_RANGE__REVIEW_REQUIRED_BEFORE_UNIVERSE_CONSTRUCTION"` |
| `security_level_diversity_quota_rule` | `"NONE__NO_SECTOR_INDUSTRY_MARKET_CAP_MARKET_REGIME_OR_OTHER_DIVERSITY_QUOTA"` |

Numeric thresholds retain the accepted at-least comparison and completed
pre-formation regular-session lookbacks; median closes remain as-traded.
These semantics are part of the version-1 field definitions, not new rules.
Set-like arrays are lexicographically sorted and unique; all payload values
use the exact JSON representations above under section-17 serialization.

```text
universe_definition_identity =
SHA256(CANONICAL_JSON_OF_UNIVERSE_DEFINITION_SPECIFICATION)
```

Exclude the identity itself, realized monthly membership rows,
`processed_universe_membership` artifact hashes, evidence bundle IDs,
source-lineage IDs, `dataset_instance_id`, `provenance_manifest_identity`,
downstream model/gate identities, local paths, and observational timestamps.
The specification is upstream of membership and dataset artifacts. A material
accepted-rule change creates a new identity; ordinary monthly membership
changes under unchanged rules do not. The 75-security note is not a rule or
payload input. No actual universe identity is generated in this correction.

## 11. Common PPO/SAC/RecurrentPPO observation/state contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3]: predeclared RL candidate set is PPO, SAC, and
  RecurrentPPO.
- `ACCEPTED_REQUIREMENT` [S3]: PPO is the mandatory primary baseline.
- `ACCEPTED_REQUIREMENT` [S3]: candidate-set expansion is not authorized.
- `ACCEPTED_REQUIREMENT` [S3, S10]: the C6 dataset contract must remain
  model-family neutral and support PPO, SAC, and RecurrentPPO compatibility.
- `ACCEPTED_REQUIREMENT` [S3, S10]: the common dataset contract must support
  chronological sequence construction, recurrent requirements, common
  economic inputs, and stable row/security/time identity without encoding one
  RL family's implementation assumptions as the common data contract.

### C6-D technical definition — common logical decision state

`C6_D_DETAIL_DEFINED` — PPO, SAC, and RecurrentPPO consume the same
model-family-neutral logical decision observation. This is an interface over
the accepted C6-B identities and C6-C timing rules, not another canonical
table, a chosen model architecture, or generated features or tensors.

The logical field order is the following; per-slot fields use ascending slot
index, and per-feature fields use the immutable ordered feature schema:

1. `decision_time_utc` — decision instant T in UTC.
2. `exchange_local_session_identity_by_slot` — official exchange calendar,
   exchange-local session date, and time-zone identity under section 7.
3. `security_slot_id` and `slot_to_canonical_security_id` — deterministic slot
   indices and explicit stable security identity mapping, with identifier
   namespace preserved; an unassigned slot has an explicit absent mapping.
4. `active_security_mask` — whether each slot is active for this decision.
5. `ordered_market_feature_schema_identity` and
   `ordered_market_feature_values_by_slot` — immutable ordered feature
   definitions and their values when later generated.
6. `feature_input_validity_mask` and `feature_input_availability_mask` —
   explicit validity and availability for each corresponding input, including
   required economic inputs; masks are aligned with the ordered fields.
7. Current portfolio/position state and previous target-exposure state —
   the pre-decision fields in section 14, in that section's listed order.
8. `session_start_flag`, `formation_boundary_flag`, and `episode_start_flag`
   — explicit session, formation/reformation, and episode-start/reset
   indicators; affected slots are identified when a boundary is slot-specific.

```text
MAX_UNIVERSE_SLOTS = 60
USABLE_INPUT_AT_T = AVAILABLE_BY_T AND APPLICABLE_BY_T
```

For N selected securities, N <= 60, initial slot order follows the accepted
liquidity rank descending by trailing median dollar volume and the accepted
stable security identifier ascending tie-break with namespace preserved
(section 10). Assign slots 0 through N-1 in that order; remaining slots are
inactive. This does not relax accepted underfill/review requirements.
Hard-terminal removal deactivates the affected slot at the governed effective
and available time; there is no mid-cycle replacement or compaction. A vacated
slot remains vacant until scheduled reformation. Slot position alone is never
security identity: the explicit mapping and formation identity must accompany
each observation and remain traceable across remapping.

All inputs must satisfy section 8 availability and applicability at T.
Future information and current-bar information not yet available at T are
excluded. Unresolved required active-slot state remains explicitly unresolved
and fail-closed: no policy action may be emitted. A mask documents missingness;
it does not authorize silently replacing financial values with zero or
bypassing required-input checks. Inactive-slot placeholders are masked
non-observations, distinct from valid financial zeros and from unresolved
active-slot inputs.

### C6-D technical definition — normalization and state dimension

`C6_D_DETAIL_DEFINED` — the normalization interface requires immutable ordered
feature identity, preprocessing/transformation identity, fitted-parameter
identity when fitting applies, and the later governed training-partition
identity. Fitting uses only that training partition; the same transformation,
feature order, and fitted parameters apply identically to later governed
evaluation data. Full-sample fitting, future-aware normalization, and silent
candidate-specific reordering are prohibited. No normalization algorithm or
future market-feature set is selected here.

```text
STATE_DIMENSION = DETERMINISTIC_LAYOUT(
    FROZEN_ORDERED_FEATURE_SCHEMA,
    FIXED_REQUIRED_ECONOMIC_STATE_FIELDS,
    FIXED_MASK_BOUNDARY_FIELDS,
    MAX_UNIVERSE_SLOTS
)
```

The later frozen schema must declare each field's shape, encoding, and order,
including mask/boundary shapes and any history dependencies. Slot-indexed
fields always reserve 60 slots; global fields occur once. Feature dimensions
are derived from that schema, not from the observed active count or candidate
family. Identity metadata stays attached to the layout even if not numerically
encoded as policy features. The dimension is deterministic once these inputs
are frozen; this draft does not invent a numeric feature dimension or tensor.

### C6G-FIND-002 correction — structural state interface identity

`state_interface_identity` is the immutable structural identity of the common
PPO/SAC/RecurrentPPO logical state interface. The canonical specification
contains exactly the following 16 identity-bearing fields and no others in V1:

```text
state_interface_spec_version
MAX_UNIVERSE_SLOTS
ordered_logical_state_field_descriptors
global_vs_slot_indexed_shape_rules
slot_ordering_and_mapping_semantics
ordered_market_feature_schema_identity
ordered_required_economic_state_field_schema
feature_input_validity_mask_schema
feature_input_availability_mask_schema
session_start_flag_schema
formation_boundary_flag_schema
episode_start_flag_schema
inactive_slot_representation_semantics
required_active_slot_fail_closed_semantics
field_dtype_and_encoding_rules
required_identity_reference_field_definitions

state_interface_identity =
SHA256(CANONICAL_JSON_OF_STATE_INTERFACE_SPECIFICATION)
```

Use section-17 canonical JSON/SHA-256 rules. The specification version is
exactly the JSON string "1"; `MAX_UNIVERSE_SLOTS` is the JSON integer 60.
Ordered descriptors expand the existing
eight logical field groups above in their declared order, with each field's
name, logical dtype, encoding, shape, units where applicable, and requiredness.
Global fields occur once; slot-indexed fields reserve 60 entries. Feature axes
follow the frozen ordered market-feature schema. Mapping, inactive-slot,
required-input fail-closed, and mask/boundary semantics are those already
specified in this section; their exact layout and encodings must be recorded.
Required identity-reference definitions describe reference names and meanings,
not sample-specific referenced values.

The economic schema preserves section-14 pre-decision order:
`portfolio_equity_usd`, `cash_usd`, `position_quantity_by_slot`,
`position_market_value_usd_by_slot`, `current_exposure_fraction_by_slot`,
`previous_target_exposure_fraction_by_slot`, `gross_exposure_fraction`, then
`net_exposure_fraction`. USD, signed quantities, and exposure-fraction units
and denominators remain as defined there. This definition selects no feature
set, numeric recurrent L/W, exposure bounds, or model architecture.

Exclude decision timestamp values, current active security IDs, actual slot
assignments, feature values, mask values, current portfolio values, policy
actions, `dataset_instance_id`, policy/model identity, gate identity, and the
computed `state_interface_identity` itself. Normalization transformation,
fitted-parameter, and training-partition identities remain required separate
provenance. Their fitted/run-specific values do not redefine this structural
identity; the interface still defines the required external reference fields.

```text
STATE_INTERFACE_IDENTITY_MATERIALIZATION_PRECONDITION =
ORDERED_MARKET_FEATURE_SCHEMA_IDENTITY_IS_FROZEN
AND ALL_IDENTITY_BEARING_STATE_LAYOUT_AND_ENCODING_CONFIGURATION_IS_FROZEN
```

Before that condition, `state_interface_identity = NOT_YET_MATERIALIZED` is a
specification state, not an error. The exact interface must be frozen before
applicable model training. A material change in ordered feature schema, field
order, shape, encoding, mask/boundary layout, required economic-state layout,
or max-slot envelope creates a different identity; affected later work must
use it under then-applicable governance. No actual state identity is generated
by this correction.

### C6G-FIND-002 second correction — exact V1 representation

A materialized `STATE_INTERFACE_SPECIFICATION_V1` has exactly the 16 keys
listed above, `state_interface_spec_version = "1"`, and `MAX_UNIVERSE_SLOTS = 60`.
No optional top-level extension is permitted. Adding, removing, or renaming
a key requires a new specification version. The rules below define how the
later frozen configuration is represented, without selecting that scientific
configuration or generating an identity now.

#### V1 representation — exact ordered logical field expansion

`ordered_logical_state_field_descriptors` must contain EXACTLY 20 descriptor
objects in this order:

```text
1  decision_time_utc
2  exchange_local_session_identity_by_slot
3  security_slot_id
4  slot_to_canonical_security_id
5  active_security_mask
6  ordered_market_feature_schema_identity
7  ordered_market_feature_values_by_slot
8  feature_input_validity_mask
9  feature_input_availability_mask
10 portfolio_equity_usd
11 cash_usd
12 position_quantity_by_slot
13 position_market_value_usd_by_slot
14 current_exposure_fraction_by_slot
15 previous_target_exposure_fraction_by_slot
16 gross_exposure_fraction
17 net_exposure_fraction
18 session_start_flag
19 formation_boundary_flag
20 episode_start_flag
```

This is only the exact expansion of the already accepted eight logical groups.

Do not add another policy input.

Do not remove one.

#### V1 representation — exact field-descriptor object schema

Every entry in `ordered_logical_state_field_descriptors` must be a JSON object
with EXACTLY these seven keys:

```text
field_name
scope
logical_dtype
encoding
shape
units
requiredness
```

No additional key is permitted in V1.

Represent:

##### `field_name`

exact UTF-8 string from the required ordered field-name list.

##### `scope`

one exact frozen token from:

```text
GLOBAL
SLOT_INDEXED
SLOT_FEATURE_INDEXED
REFERENCE_METADATA
ALIGNED_MASK
```

The materialized layout must select one concrete permitted scope.

##### `logical_dtype`

nonempty exact UTF-8 token frozen by the governed layout.

##### `encoding`

nonempty exact UTF-8 token frozen by the governed layout.

Do not case-fold, trim, alias, or otherwise normalize these token values before
hashing.

##### `shape`

the exact shape representation defined below.

##### `units`

either:

* an exact nonempty UTF-8 unit token; or
* JSON `null` when units are not applicable.

Do not omit `units`.

##### `requiredness`

exactly one:

```text
REQUIRED
CONDITIONAL
```

No other requiredness token is valid in V1.

Any required descriptor value that is not yet frozen means the structural
identity remains:

```text
NOT_YET_MATERIALIZED
```

It is not replaced with a placeholder inside a materialized payload.

#### V1 representation — exact shape representation

Every `shape` value is a JSON array.

A scalar/global scalar shape is:

```json
[]
```

Every non-scalar dimension is represented by an object with EXACTLY:

```text
kind
value
```

Allowed dimension forms are:

Fixed:

```json
{"kind":"FIXED","value":60}
```

or another positive JSON integer only when that exact fixed extent has been
separately frozen as part of the accepted state layout.

Reference-derived:

```json
{"kind":"REFERENCE","value":"ORDERED_MARKET_FEATURE_COUNT"}
```

For V1, `REFERENCE` dimensions may use only the exact reference token:

```text
ORDERED_MARKET_FEATURE_COUNT
```

unless a later separately governed new state-interface version adds another
reference dimension.

Canonical examples:

global:

```json
[]
```

slot indexed:

```json
[{"kind":"FIXED","value":60}]
```

slot x market feature:

```json
[
  {"kind":"FIXED","value":60},
  {"kind":"REFERENCE","value":"ORDERED_MARKET_FEATURE_COUNT"}
]
```

No shorthand such as `"60xF"`, tuples, omitted scalar shape, or implementation
language shape object is permitted.

#### V1 representation — exact global / slot shape-rule object

`global_vs_slot_indexed_shape_rules` is a JSON object with EXACTLY:

```text
global_shape
slot_indexed_shape
slot_feature_shape
```

Its V1 values are the exact canonical shape arrays defined above.

No additional key is permitted.

#### V1 representation — exact slot-mapping semantics object

`slot_ordering_and_mapping_semantics` is a JSON object with EXACTLY:

```text
slot_index_base
max_slots
formation_order_rule
identity_tie_break_rule
unassigned_slot_rule
hard_terminal_vacancy_rule
mid_cycle_compaction_rule
security_identity_mapping_rule
```

Require:

```text
slot_index_base = 0
max_slots = 60
```

The remaining string values must be exact UTF-8 canonical tokens transcribing
ONLY the already accepted section-10/11 rules:

* liquidity ranking descending;
* stable security identifier ascending tie-break with namespace;
* unassigned slots inactive;
* hard-terminal vacancy retained until scheduled reformation;
* no mid-cycle compaction/replacement;
* explicit slot-to-canonical-security identity mapping.

Do not change any scientific rule.

The exact token values are fixed by the V1 object below.

No additional object key is permitted.

The exact V1 slot semantics object is:

```json
{
  "slot_index_base": 0,
  "max_slots": 60,
  "formation_order_rule": "LIQUIDITY_RANK_DESCENDING",
  "identity_tie_break_rule": "STABLE_SECURITY_IDENTIFIER_ASCENDING_WITH_NAMESPACE_PRESERVED",
  "unassigned_slot_rule": "INACTIVE",
  "hard_terminal_vacancy_rule": "VACANT_UNTIL_SCHEDULED_REFORMATION",
  "mid_cycle_compaction_rule": "NO_COMPACTION_OR_REPLACEMENT",
  "security_identity_mapping_rule": "EXPLICIT_SLOT_TO_CANONICAL_SECURITY_ID"
}
```

#### V1 representation — exact market-feature-schema identity value

Within a MATERIALIZED state-interface payload:

`ordered_market_feature_schema_identity`

must be the exact frozen identity value of that schema using its governed
identity format.

It cannot equal:

```text
NOT_YET_MATERIALIZED
UNKNOWN
TBD
null
```

If that upstream identity is not frozen:

```text
state_interface_identity =
NOT_YET_MATERIALIZED
```

and no materialized state-interface payload/hash exists yet.

#### V1 representation — exact economic-schema representation

`ordered_required_economic_state_field_schema` is represented as an ordered
JSON array of EXACTLY these eight field-name strings:

```json
[
  "portfolio_equity_usd",
  "cash_usd",
  "position_quantity_by_slot",
  "position_market_value_usd_by_slot",
  "current_exposure_fraction_by_slot",
  "previous_target_exposure_fraction_by_slot",
  "gross_exposure_fraction",
  "net_exposure_fraction"
]
```

The complete shape/dtype/encoding/unit/requiredness definitions are the
corresponding entries in `ordered_logical_state_field_descriptors`.

Do NOT duplicate independent descriptor objects here.

This prevents inconsistent duplicated schemas.

The underlying economic meanings and units remain exactly those already defined
in section 14.

#### V1 representation — exact mask-schema objects

Both:

`feature_input_validity_mask_schema`

and:

`feature_input_availability_mask_schema`

must be JSON objects with EXACTLY:

```text
field_name
masked_field_names
logical_dtype
encoding
alignment_rule
true_semantics
false_semantics
```

##### `field_name`

the exact corresponding mask field name.

##### `masked_field_names`

an ordered JSON array of exact field-name strings from the 20-field descriptor
list.

The exact applicable list is part of the frozen identity-bearing layout.

Its order is identity-bearing.

`logical_dtype`
and
`encoding`

exact frozen UTF-8 tokens.

`alignment_rule`
must be the exact canonical rule equivalent to:

```text
MASKED_FIELD_NAMES_IN_ORDER__MASK_LAYOUT_EXACTLY_ALIGNS_WITH_REFERENCED_INPUT_LAYOUT
```

The exact validity and availability semantic tokens are fixed below,
consistent with the existing section-11 rules.

Do not invent an imputation permission.

A mask still does not authorize financial-zero replacement.

No additional mask-schema key is permitted.

V1 mask semantic values are exact strings:

| Schema | `true_semantics` | `false_semantics` |
|---|---|---|
| `feature_input_validity_mask_schema` | `INPUT_VALID_UNDER_GOVERNED_RULES` | `INPUT_NOT_ESTABLISHED_VALID__NO_SILENT_FINANCIAL_ZERO_REPLACEMENT` |
| `feature_input_availability_mask_schema` | `INPUT_AVAILABLE_BY_DECISION_TIME_T` | `INPUT_NOT_ESTABLISHED_AVAILABLE_BY_DECISION_TIME_T` |

Both mask schemas use the exact `alignment_rule` string
`MASKED_FIELD_NAMES_IN_ORDER__MASK_LAYOUT_EXACTLY_ALIGNS_WITH_REFERENCED_INPUT_LAYOUT`.
Their dtype and encoding values must equal the corresponding descriptor's
values. The frozen masked-field list must satisfy existing section-11 coverage,
including required economic inputs; this does not permit omitting required
inputs or weakening applicability/fail-closed rules.

#### V1 representation — exact boundary-flag object schema

Each of:

`session_start_flag_schema`
`formation_boundary_flag_schema`
`episode_start_flag_schema`

is a JSON object with EXACTLY:

```text
field_name
scope
logical_dtype
encoding
shape
slot_specific_affected_slot_representation
```

`field_name`
must equal the corresponding exact field name.

`scope`
must be one concrete frozen permitted scope:

```text
GLOBAL
SLOT_INDEXED
```

`shape` uses the V1 shape representation above and must agree with `scope`.

`logical_dtype`
and
`encoding`
are exact frozen UTF-8 tokens.

`slot_specific_affected_slot_representation`
must be exactly one frozen canonical token describing the already accepted
behavior that affected slots are explicitly identified when slot-specific.

No additional key is permitted.

For V1, `slot_specific_affected_slot_representation` is the exact string
`GLOBAL_BOUNDARY_APPLIES_TO_ALL_SLOTS` for GLOBAL scope, or
`SLOT_INDEXED_FLAGS_EXPLICITLY_IDENTIFY_AFFECTED_SLOTS` for SLOT_INDEXED scope.
The scope, shape, dtype, and encoding must match the corresponding logical
field descriptor; these schema objects cannot create contradictory duplicate
layouts. GLOBAL shape is `[]`; SLOT_INDEXED shape is
`[{"kind":"FIXED","value":60}]`.

#### V1 representation — exact semantic token fields

These top-level values are exact UTF-8 canonical tokens, not free-form nested
objects:

```text
inactive_slot_representation_semantics
required_active_slot_fail_closed_semantics
```

Their exact V1 values below transcribe the already accepted section-11 rules:

* inactive placeholders are masked non-observations distinct from valid
  financial zeros and unresolved active input;
* unresolved required active-slot state fails closed and no policy action may
  be emitted.

Do not alter those semantics.

Exact V1 values:

```text
inactive_slot_representation_semantics =
MASKED_NON_OBSERVATIONS_DISTINCT_FROM_VALID_FINANCIAL_ZEROS_AND_UNRESOLVED_ACTIVE_INPUT
required_active_slot_fail_closed_semantics =
UNRESOLVED_REQUIRED_ACTIVE_SLOT_STATE_FAILS_CLOSED__NO_POLICY_ACTION
```

These values are JSON strings in the materialized payload.

#### V1 representation — exact dtype / encoding rule object

`field_dtype_and_encoding_rules` is a JSON object containing EXACTLY:

```text
logical_dtype_value_representation
encoding_value_representation
string_normalization
units_not_applicable_representation
unfrozen_required_value_effect
```

Use exactly these V1 string values:

```text
logical_dtype_value_representation = EXACT_UTF8_TOKEN
encoding_value_representation = EXACT_UTF8_TOKEN
string_normalization = NONE
units_not_applicable_representation = JSON_NULL
unfrozen_required_value_effect = STATE_INTERFACE_IDENTITY_NOT_YET_MATERIALIZED
```

No additional key is permitted.

#### V1 representation — exact identity-reference definition objects

`required_identity_reference_field_definitions` is an ordered JSON array.

Every entry is an object with EXACTLY:

```text
field_name
reference_kind
reference_semantics
requiredness
runtime_referenced_value_in_structural_hash
```

##### `field_name`

exact governed reference-field name.

`reference_kind`
and
`reference_semantics`

exact frozen UTF-8 tokens.

##### `requiredness`

`REQUIRED` or `CONDITIONAL`.

##### `runtime_referenced_value_in_structural_hash`

JSON Boolean.

For reference fields whose runtime/sample referenced value is explicitly
excluded from the structural identity, require:

```json
false
```

Array order follows first occurrence in the governed logical interface; do not
sort lexicographically unless the contract explicitly defines that order as
the interface order.

The exact reference list is part of the frozen layout/configuration and must be
complete before identity materialization.

#### V1 representation — extension / optional-field rules

For `STATE_INTERFACE_SPECIFICATION_V1`:

```text
UNDECLARED_TOP_LEVEL_KEYS = PROHIBITED
UNDECLARED_NESTED_KEYS = PROHIBITED
OMITTED_REQUIRED_KEYS = PROHIBITED
```

Only `units` may use JSON `null`, and only where units are not applicable.

No other missing value is represented by omission or null.

All arrays preserve the explicit contract-defined order.

No array is automatically sorted unless explicitly defined as set-like.

No object/value string is trimmed, case-folded, alias-normalized, or rewritten
before hashing.

Any representational extension requiring:

* another top-level key;
* another descriptor key;
* another dimension kind;
* another symbolic dimension reference;
* another nested schema member

requires a new:

```text
state_interface_spec_version
```

and therefore a different state-interface identity once materialized.

#### V1 representation — canonical serialization / hash

Preserve section-17 canonical JSON rules.

After all required values are frozen and the materialization precondition is
satisfied:

```text
state_interface_identity =
SHA256(CANONICAL_JSON_OF_STATE_INTERFACE_SPECIFICATION_V1)
```

The payload excludes:

* `state_interface_identity` itself;
* runtime/sample values already excluded by the existing contract;
* observational timestamps;
* local filesystem paths.

Before all required payload values are frozen:

```text
state_interface_identity =
NOT_YET_MATERIALIZED
```

No placeholder payload is hashed.

## 12. Recurrent sequence, lookback, warm-up, and boundary contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3, S10]: the dataset contract must support recurrent
  chronological sequence construction.
- `ACCEPTED_REQUIREMENT` [S3, S10]: recurrent lookback and warm-up
  requirements must be representable.
- `ACCEPTED_REQUIREMENT` [S3, S10]: recurrent episode and session boundaries
  must be representable.
- `ACCEPTED_REQUIREMENT` [S7]: recurrent sequences must remain compatible with
  official session boundaries, early closes, and truncated final bars.

### C6-D technical definition — chronological recurrent interface

`C6_D_DETAIL_DEFINED` — recurrent sequences contain ordered section-11
decision observations, with an additional chronological sequence axis. This
does not change ordinary PPO/SAC observation semantics.

```text
recurrent_lookback_steps = L
recurrent_warmup_steps = W
L >= 1
0 <= W <= L
recurrent_session_boundary_policy =
RESET_AT_SESSION_START | CARRY_WITH_EXPLICIT_SESSION_BOUNDARY
```

L is the required number of valid decision observations in an applicable
recurrent window; W is the leading subset used to initialize/advance hidden
state before scored/learning steps. Warm-up observations are not scored or
used as learning targets. W = L permits a warm-up-only window, not a scored
sample. Numeric L and W and the chosen session-boundary policy must be
recorded as configuration identity and frozen before applicable recurrent
training; none is selected here.

Sequences ascend strictly by decision time, ending no later than the decision
being evaluated. No future rows, random ordering, duplicate decision steps,
or synthetic financial observations to fill history are permitted. Sequences,
warm-up, and carried hidden state may not cross later governed partition
boundaries; this requirement does not define those partitions or start C6-E.

The sequence interface carries `sequence_valid_length`,
`sequence_valid_mask`, `episode_start_flag`, `session_start_flag`, and
`formation_boundary_flag`, with per-step and affected-slot alignment.
`sequence_valid_length` counts real valid decision observations, and
`sequence_valid_mask` distinguishes them from non-observation padding.
Episode/partition starts reset hidden state. Formation/reformation remapping
resets affected hidden state before the remapped security is consumed;
hard-terminal removal resets and deactivates the affected state. Shared hidden
state must reset wherever needed to prevent affected-security history from
surviving through a coupled representation.

`RESET_AT_SESSION_START` resets at each official session start and history
requirements must be satisfied after that reset.
`CARRY_WITH_EXPLICIT_SESSION_BOUNDARY` permits chronological carry between
real sessions while retaining explicit session-start flags and respecting all
other reset and partition rules. Neither policy creates a synthetic overnight
timestep; official early closes and truncated final bars retain section-7
semantics.

`INSUFFICIENT_RECURRENT_HISTORY` is explicit when L valid observations or W
valid warm-up steps cannot be provided under these timing, validity, and reset
rules. Such a window cannot produce a recurrent action or scored sample;
future backfill is prohibited. Any later fixed-shape padding is masked
`NON-OBSERVATION` padding, excluded from valid length, warm-up, hidden-state
updates, and scoring. It must not represent zero OHLCV, zero volume, or flat
price and cannot satisfy a history requirement.

## 13. Continuous target-position/exposure action representation

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3]: the common action formulation is
  `CONTINUOUS_TARGET_POSITION_OR_EXPOSURE`.
- `ACCEPTED_REQUIREMENT` [S3]: the common formulation applies prospectively to
  the bounded PPO/SAC/RecurrentPPO comparison and does not imply any model has
  been implemented, trained, qualified, or authorized for execution.

### C6-D technical definition — continuous target exposure

`C6_D_DETAIL_DEFINED`:

```text
COMMON_ACTION_FORMULATION = CONTINUOUS_TARGET_POSITION_OR_EXPOSURE
normalized_policy_action ∈ [-1, 1] per active security slot
PHYSICAL_EXPOSURE_UNITS =
SIGNED_NOTIONAL_EXPOSURE_AS_FRACTION_OF_PRE_TRADE_PORTFOLIO_EQUITY

target_exposure = target_exposure_min
    + ((normalized_policy_action + 1) / 2)
    * (target_exposure_max - target_exposure_min)

required_rebalance = target_exposure - current_realized_exposure
```

`target_exposure_min` and `target_exposure_max` are configured finite bounds
with min <= max, resolved for each active slot. The affine mapping is
deterministic and monotone nondecreasing, maps the endpoints to the configured
bounds, and is constant if the bounds coincide. Invalid/nonfinite actions or
configuration fail closed, without silent clipping. Inactive slots are masked
and have physical target exposure zero; their policy values are ignored.

Exposure bounds, their slot/security applicability, and later gross, net,
leverage, and concentration constraints and their enforcement rule are
identity-bearing configuration common to the governed comparison. This draft
selects no numerical limits, leverage, long-only, or short-selling policy.
Later constraint handling must preserve the requested target distinctly from
any feasible or executed outcome.

At decision time T, establish the section-11/14 pre-decision state before
choosing action T. The action is a target exposure, not buy/sell/hold and not
executed trade quantity. `current_realized_exposure` is the corresponding
pre-decision exposure on the same pre-trade-equity denominator;
`required_rebalance` is the required exposure change, not an execution promise.
Crossing zero needs no special discrete action. Preserve pre-decision exposure,
requested target exposure, required exposure change, and later execution
outcome separately. An inactive target of zero does not assert that a residual
holding has already been liquidated; holdings and any later execution remain
explicit economic state. No action may be emitted from unresolved fail-closed
state. Decision scheduling and later execution timing/latency must have
explicit governed configuration consistent with sections 7–8.

## 14. Economic, execution-price, turnover, spread, slippage, and cost inputs

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S7]: C5 uses no separate hard bid-ask-spread
  threshold and no separate expected-execution-cost threshold for universe
  eligibility.
- `ACCEPTED_REQUIREMENT` [S7]: the accepted median-dollar-volume screen remains
  the coarse ex-ante tradability/liquidity eligibility mechanism.
- `ACCEPTED_REQUIREMENT` [S7]: spread and expected costs remain scientifically
  relevant diagnostics rather than additional C5 security-selection quotas.
- `ACCEPTED_REQUIREMENT` [S7]: a realistic execution-cost model is required
  when applicable later backtest/validation work is separately authorized.
- `ACCEPTED_REQUIREMENT` [S3, S10]: C6 must support common economic, cost, and
  execution inputs across the accepted RL candidate set.

### C6-D technical definition — pre-decision economic state

`C6_D_DETAIL_DEFINED` — the ordered required pre-decision economic fields are:

```text
portfolio_equity_usd
cash_usd
position_quantity_by_slot
position_market_value_usd_by_slot
current_exposure_fraction_by_slot
previous_target_exposure_fraction_by_slot
gross_exposure_fraction
net_exposure_fraction
```

All policy-visible state at T must be established and usable by T. Quantities
and market values are signed; current exposure is signed position market value
divided by applicable pre-trade portfolio equity. Gross exposure is the sum of
absolute current slot exposures and net exposure their signed sum. Prior
requested targets remain distinct from current realized positions. Valuation
price source, timing, currency treatment, and portfolio accounting conventions
must be explicit configuration/provenance. Required values must be finite and
the equity denominator strictly positive; unresolved or invalid required
state fails closed, without silent financial-zero replacement. Residual
holdings remain accounted for even if their policy slot is inactive.

### C6-D technical definition — later transition and cost interface

`C6_D_DETAIL_DEFINED` — a later transition preserves decision time, slot/security
mapping, action/configuration identity, execution/outcome timing, and at least
the following ordered fields:

```text
requested_target_exposure_fraction_by_slot
required_exposure_change_by_slot
trade_quantity_by_slot
trade_notional_usd_by_slot
execution_reference_price_usd_by_slot
executed_price_usd_by_slot
turnover_fraction
spread_cost_usd
slippage_cost_usd
fees_usd
other_transaction_cost_usd
total_transaction_cost_usd
post_trade_cash_usd
post_trade_equity_usd
post_trade_exposure_fraction_by_slot
```

Trade quantity is signed executed quantity; trade notional is signed executed
quantity times executed price in USD. Execution reference and executed prices
remain separate, with explicit source, timestamp, aggregation, and no-fill
applicability/validity. Multiple fills retain the detail needed to reconcile
slot aggregates and costs. Post-trade exposure uses post-trade equity and
therefore need not equal the requested pre-trade-equity-based target.

```text
turnover_fraction =
SUM_OVER_EXECUTED_FILLS(ABS(trade_notional_usd))
/ applicable_pre_trade_portfolio_equity_usd

total_transaction_cost_usd = spread_cost_usd + slippage_cost_usd
    + fees_usd + other_transaction_cost_usd
```

Turnover is dimensionless; each executed fill is counted once. Do not add both
a fill and its slot aggregate, net opposing fills before taking absolute
notional, or add requested rebalances to executed turnover. No additional
two-sided multiplier applies. The denominator is the same strictly positive
pre-trade equity for the represented transition.

Execution-price conventions, spread, slippage, fees, latency, market impact,
and related assumptions must later be explicit configuration/provenance
inputs, including units, timing, source, version, and aggregation conventions.
Cost attribution must make components mutually exclusive: distinguish spread
from residual slippage and allocate market impact once. Specify which costs
are already embedded in executed prices and which are cash charges so later
cash/equity accounting does not deduct embedded costs twice. Preserve cost
component validity and reconciliation with the execution outcome; missing
costs are not silently zero. No numerical cost assumption is selected here.

Realized action-T execution, slippage, and cost outcomes belong to the later
transition and cannot enter the state used to choose action T. Prior outcomes
may enter later state only when available and applicable. Spread/cost
diagnostics remain diagnostics, not new security eligibility quotas. These
are interface definitions only; no economic values, execution outcomes,
features, datasets, or model implementation are generated.

## 15. Development, validation, qualification, and final-holdout partition contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3, S10]: development and evaluation must remain
  chronological and leakage controlled.
- `ACCEPTED_REQUIREMENT` [S3, S10]: deterministic chronological folds must be
  supported.
- `ACCEPTED_REQUIREMENT` [S4, S11]: walk-forward mechanics are preserved as a
  governed research-platform responsibility rather than replaced with random
  splitting.
- `ACCEPTED_REQUIREMENT` [S3]: candidate development, qualification, gating,
  routing, threshold decisions, and model/gate selection occur before
  final-holdout access.
- `ACCEPTED_REQUIREMENT` [S3]: only eligible frozen candidates may reach the
  separately governed final evaluation.
- `ACCEPTED_REQUIREMENT` [S3, S9]: there is one shared untouched final holdout,
  opened once only under a common frozen evaluation package and separate
  authorization.
- `ACCEPTED_REQUIREMENT` [S1, S2]: final-holdout access is not authorized
  during C6.

### C6-E technical definition — chronological regions and walk-forward folds

`C6_E_DETAIL_DEFINED` — all dates below are inclusive and refer to official
accepted regular sessions under the C6-C calendar contract. Region assignment
uses the decision observation's accepted exchange-local session identity;
calendar-derived UTC instants govern dependency checks. No observations are
manufactured for holidays, weekends, or closed sessions.

```text
STUDY_WINDOW = 2024-09-03 THROUGH 2026-08-31 INCLUSIVE
DEVELOPMENT_REGION = 2024-09-03 THROUGH 2026-03-31 INCLUSIVE
QUALIFICATION_REGION = 2026-04-01 THROUGH 2026-05-29 INCLUSIVE
FINAL_HOLDOUT_REGION = 2026-06-01 THROUGH 2026-08-31 INCLUSIVE
REGION_OVERLAP = NONE
REGION_ORDER = DEVELOPMENT THEN QUALIFICATION THEN FINAL_HOLDOUT

WALK_FORWARD_TRAIN_START = 2024-09-03
TRAIN_WINDOW_STYLE = EXPANDING
VALIDATION_WINDOW_STYLE = ONE_CALENDAR_MONTH_OF_ACCEPTED_REGULAR_SESSIONS
WALK_FORWARD_STEP = ONE_CALENDAR_MONTH
VALIDATION_FOLD_COUNT = 7
```

No observation may belong to more than one top-level region in the same
governed research cycle. Development contains exactly these seven validation
folds, in the listed order:

| Fold | Train start | Train end | Validation start | Validation end |
|---|---|---|---|---|
| FOLD_1 | 2024-09-03 | 2025-08-29 | 2025-09-02 | 2025-09-30 |
| FOLD_2 | 2024-09-03 | 2025-09-30 | 2025-10-01 | 2025-10-31 |
| FOLD_3 | 2024-09-03 | 2025-10-31 | 2025-11-03 | 2025-11-28 |
| FOLD_4 | 2024-09-03 | 2025-11-28 | 2025-12-01 | 2025-12-31 |
| FOLD_5 | 2024-09-03 | 2025-12-31 | 2026-01-02 | 2026-01-30 |
| FOLD_6 | 2024-09-03 | 2026-01-30 | 2026-02-02 | 2026-02-27 |
| FOLD_7 | 2024-09-03 | 2026-02-27 | 2026-03-02 | 2026-03-31 |

A completed validation region may enter the next fold's expanding training
history. No validation observation enters its own fold's training set. No
random split is permitted. These date ranges are nominal membership bounds;
the dependency and validity exclusions below still apply.

### C6-E technical definition — forward dependencies, purge, and embargo

`C6_E_DETAIL_DEFINED` — every example preserves:

```text
example_information_cutoff_utc
target_or_outcome_start_utc
target_or_outcome_end_utc

BOUNDARY_PURGE_RULE =
IF target_or_outcome_end_utc >= next_governed_partition_start_utc
THEN EXCLUDE_EXAMPLE_FROM_EARLIER_PARTITION

EMBARGO_DURATION =
DERIVED_FROM_THE_MAXIMUM_FORWARD_INFORMATION_DEPENDENCY_OF_THE_APPLICABLE_TARGET_OR_OUTCOME
FIXED_ARBITRARY_CALENDAR_DAY_EMBARGO = NONE
```

The information cutoff is the latest permitted input instant for the example;
all features must satisfy C6-C availability/applicability at that cutoff.
Target/outcome start and end describe the complete forward dependency, not
merely the stored label timestamp. Unknown or invalid dependency bounds remain
explicit and fail closed for partition eligibility.

An example is eligible only when its complete target/outcome dependency stays
inside its permitted temporal boundary. The next partition's start is the
calendar-derived UTC start instant of its first accepted regular session.
An inclusive end date permits dependencies only through that date's applicable
official session close, not through later closed-session time.

- Fold training purges every example whose forward target/outcome reaches
  that fold's validation start, including equality.
- Fold validation excludes every example whose target/outcome extends beyond
  that validation fold's official end, even if the next fold starts later.
- Qualification excludes every example whose target/outcome reaches the
  final-holdout start; it also requires the full outcome within the
  qualification region's own inclusive end.
- Final holdout requires the complete target/outcome inside the holdout region
  under the later frozen final evaluation package.

The same rule applies to development refitting at the qualification boundary.
Embargo/purge is derived from the maximum forward information dependency of
the applicable target/outcome identities and the actual example intervals;
no arbitrary calendar-day duration is selected. A row timestamp before a
boundary never excuses a label/outcome dependency across it. Gate horizons
in section 16 participate in these checks. Sequence and warm-up partition
resets and non-crossing requirements in section 12 remain unchanged.

### C6-E technical definition — preprocessing and split identity

`C6_E_DETAIL_DEFINED`:

```text
PREPROCESSOR_FIT_REGION = THAT_FOLD_TRAIN_REGION_ONLY
```

For each fold, fit preprocessing only on its eligible training information,
then apply the fitted transformation unchanged to that fold's validation
region. Fitting on train plus validation, qualification, final holdout, or the
full study is prohibited. Future-aware normalization and re-estimation using
the validation period being evaluated are prohibited. Preserve section-11
ordered feature, transformation, fitted-parameter, and training-partition
identities; candidate-specific feature reordering is not allowed.

After development choices are frozen, any later authorized final
pre-qualification training refit may use only the complete DEVELOPMENT_REGION,
subject to forward-dependency purge at the qualification boundary.
Qualification and final-holdout observations never contribute to fitted
preprocessing parameters.

The immutable partition specification's complete canonical identity payload
contains at least:

```text
split_spec_version
study_window_start
study_window_end
calendar_identity_ref
development_region
walk_forward_fold_definitions
qualification_region
final_holdout_region
boundary_purge_rule
embargo_rule
applicable_target_horizon_identities
preprocessing_fit_policy
ordering_rules

split_identity = SHA256(CANONICAL_JSON_OF_COMPLETE_SPLIT_SPECIFICATION)
```

Use section-17 canonical JSON and lowercase-hex SHA-256 rules. Include exact
bounds, inclusive-end/session-to-UTC semantics, the ordered seven fold
records, and the complete dependency/fit rules; material specification or
horizon changes produce a different identity. `split_identity` itself is not
part of its hash payload. Ordering is chronological decision time ascending,
then the accepted deterministic security/slot ordering where a tie applies;
folds are ordered FOLD_1 through FOLD_7. Duplicate decision examples are not
introduced by ordering or assignment.

`split_identity` is the authoritative value referenced by the already-reserved
`split_identity_ref` in later applicable dataset provenance. A partition's
identity is resolved by that split identity plus its region role and, where
applicable, fold identifier and train/validation role. This defines no new
C6-B canonical table and does not change dataset-instance hash membership.
No actual split identity value, dataset instance, partition artifact, or
physical split is generated in C6-E.

### C6-E technical definition — qualification and candidate comparability

`C6_E_DETAIL_DEFINED` — qualification is a separate pre-holdout evaluation
region, usable later only after applicable candidate/gate development choices
are frozen and evaluation is separately authorized. It determines only
predeclared dispositions such as:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
NOT_APPLICABLE_WHERE_PREDECLARED_CONDITIONS_FAIL
```

Qualification is not used for architecture redesign, hyperparameter tuning,
feature selection, normalization refitting, gate-target redesign,
gate-threshold tuning, Option B+ foundation rerouting, or reward redesign.
If an artifact/configuration changes because qualification results were
observed, the prior result no longer qualifies the changed artifact. Viewed
qualification observations cannot be represented as untouched evidence for
that modified artifact. Redesign/requalification disposition requires later
governance and is not authorized by C6-E.

PPO, SAC, and RecurrentPPO use the same study-window identity, split identity,
development/validation/qualification date geometry, canonical dataset identity,
calendar identity, universe-formation history, economic/cost interface,
decision-time chronology, and comparable evaluation definitions.
Candidate-specific recurrent warm-up or compatibility exclusions may produce
explicitly reported unusable examples, but never candidate-specific partition
dates. Candidate-specific availability counts and reasons remain visible; no
model family receives a more favorable temporal partition.

### C6-E technical definition — one shared untouched final holdout

`C6_E_DETAIL_DEFINED`:

```text
FINAL_HOLDOUT = ONE_SHARED_UNTOUCHED_FINAL_HOLDOUT
FINAL_HOLDOUT_REGION = 2026-06-01 THROUGH 2026-08-31 INCLUSIVE
```

Specifying this date identity is not final-holdout data access. Row-level data,
metrics, outcome summaries, diagnostics, model outputs, and performance
results remain inaccessible until separately authorized. Before any future
opening, all of the following must hold:

```text
ALL_APPLICABLE_CANDIDATE_AND_GATE_PHASES_HAVE_ACCEPTED_TERMINAL_DISPOSITIONS = YES
ALL_ELIGIBLE_CANDIDATES_ARE_FROZEN = YES
AT_LEAST_ONE_ELIGIBLE_CANDIDATE_EXISTS = YES
COMMON_EVALUATION_PACKAGE_IS_FROZEN = YES
FINAL_HOLDOUT_ACCESS_IS_EXPRESSLY_AUTHORIZED = YES
```

The holdout is opened once under that common frozen package. It cannot be
used for PPO/SAC/RecurrentPPO selection, candidate replacement, feature or
preprocessing selection, hyperparameter tuning, reward redesign, gate-feature
or gate-target redesign, gate-threshold selection, Option B+ routing,
debugging, or repeated evaluation. If no eligible frozen candidate exists,
`FINAL_HOLDOUT_ACCESSED = NO`. Accidental/viewed holdout information must be
recorded as viewed and cannot become untouched again. C6-E accesses no
final-holdout data and authorizes no evaluation.

## 16. RF/XGBoost gate-feature and target-alignment contract

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3]: supervised gating is a
  `TESTABLE_ARCHITECTURAL_HYPOTHESIS`, not an assumed improvement.
- `ACCEPTED_REQUIREMENT` [S3]: Random Forest and XGBoost are alternative
  participation-gate ablations.
- `ACCEPTED_REQUIREMENT` [S3]: every gated experiment must preserve its paired
  ungated control.
- `ACCEPTED_REQUIREMENT` [S3, S10]: C6 must support gate-feature/outcome
  alignment and leakage-safe gate-target construction.
- `ACCEPTED_REQUIREMENT` [S3]: primary gating-foundation routing uses the
  predeclared PPO → SAC → RecurrentPPO priority rather than post-hoc best
  development score.
- `ACCEPTED_REQUIREMENT` [S3]: candidate-set expansion is not authorized.

### C6-E technical definition — gate decision and feature interface

`C6_E_DETAIL_DEFINED`:

```text
SUPERVISED_GATING = TESTABLE_ARCHITECTURAL_HYPOTHESIS
RF_XGB_ROLE = ALTERNATIVE_PARTICIPATION_GATE_ABLATIONS
RL_POLICY_DECISION_TIME = T
GATE_DECISION_ORDER =
FROZEN_RL_STATE_AT_T
→ FROZEN_RL_POLICY_PROPOSAL_AT_T
→ GATE_DECISION
→ LATER_EXECUTION_TRANSITION
```

The participation gate acts after a frozen RL foundation policy produces its
requested target exposure for T and before the requested rebalance is
executed. It decides only whether that rebalance participates; it does not
replace the continuous target-exposure action formulation in section 13.

Each logical gate example preserves at least the following fields, in this
order, with feature values and masks aligned to the immutable gate schema:

```text
split_identity
dataset_instance_id
foundation_policy_identity
foundation_policy_configuration_identity
decision_time_utc
gate_decision_time_utc
canonical_security_id
security_slot_id
state_interface_identity
gate_feature_schema_identity
gate_feature_values
gate_feature_validity_mask
gate_feature_availability_mask
current_realized_exposure_fraction
ungated_requested_target_exposure_fraction
required_exposure_change
outcome_start_utc
outcome_end_utc
gate_target_state
portfolio_action_context_identity
paired_control_identity
```

The gate example's `state_interface_identity` references the exact frozen
structural interface identity defined in section 11.

This is a model-neutral gate dataset interface, not a generated dataset or
additional C6-B canonical table. Identity and future target/outcome fields
remain provenance/label metadata, not implicitly policy-visible gate features.
Required unresolved inputs fail closed; masks never silently turn unavailable
financial information into zero. Slot identity must resolve to the same
canonical security and formation mapping as the RL observation.

Permissible features include information already valid in RL state at T,
current economic state available at T, and the frozen policy's requested
target/action magnitude/direction, generated before the gate decision.
Future price movement, action-T realized execution price, slippage or cost,
later reward or P&L, future labels, qualification results, and final-holdout
information are prohibited gate features.

```text
GATE_FEATURE_AVAILABILITY_CUTOFF = GATE_DECISION_TIME_UTC
```

`GATE_DECISION_TIME_UTC` is the example's `gate_decision_time_utc`. All
market/economic information must already satisfy C6-C availability and
applicability at the original RL decision time T; a later gate timestamp does
not allow newer market inputs. The policy proposal is permissible because it
was produced from that already-valid state before the gate acts, and is not
future market information. Feature transformations obey section-15 fit
boundaries and preserve their schema and fitted-parameter identities.

### C6-E technical definition — incremental participation target

`C6_E_DETAIL_DEFINED` — the gate learns whether executing the frozen policy's
proposed rebalance adds positive incremental economic value relative to
suppressing that rebalance. Eligibility requires:

```text
ungated_requested_target_exposure_fraction != current_realized_exposure_fraction
```

Exact no-rebalance proposals receive
`gate_target_state = NO_REBALANCE_NOT_GATE_ELIGIBLE` and create no artificial
participation label. For each actionable example, later authorized target
construction compares two outcomes from the same pre-decision state and
same governed market path:

```text
UNGATED_OUTCOME = EXECUTE_THE_FROZEN_RL_REQUESTED_REBALANCE
SUPPRESSED_OUTCOME =
DO_NOT_EXECUTE_THAT_REQUESTED_REBALANCE
AND MAINTAIN_THE_PRE_DECISION_REALIZED_EXPOSURE
SUBJECT_TO_THE_SAME_MANDATORY_EXOGENOUS_RULES

incremental_net_value_usd = UNGATED_END_VALUE_USD - SUPPRESSED_END_VALUE_USD

GATE_TARGET_PARTICIPATE = 1 IF incremental_net_value_usd > 0
GATE_TARGET_SUPPRESS = 0 IF incremental_net_value_usd <= 0
```

The pair shares starting state, market path, calendar, execution/cost
configuration, mandatory terminal/event treatment, and evaluation horizon.
End values include all incremental transaction/execution costs attributable
to participation, using section-14 accounting without double-counting.
Suppression means retaining the pre-decision position rather than requesting
the proposed rebalance; market valuation can subsequently change its exposure
fraction. It does not introduce extra trades to hold a numerical fraction
constant. Mandatory exogenous rules apply identically to both branches.

A zero incremental difference does not claim participation adds value.
Unresolved paired outcomes remain explicit and cannot be converted into a
binary target. The valid binary target is separate from `gate_target_state`,
which records target eligibility/availability. C6-E generates no target value,
paired outcome, reward, or P&L.

### C6-E technical definition — single-slot counterfactual attribution

`C6_E_DETAIL_DEFINED`:

```text
GATE_COUNTERFACTUAL_SCOPE = SINGLE_SLOT_PARTICIPATION_DECISION_AT_T
```

For the gate example's target slot s, `UNGATED_OUTCOME` executes the frozen
RL requested rebalance for s, while `SUPPRESSED_OUTCOME` suppresses only that
rebalance. The only intended experimental difference is participation for s.
Both branches share the pre-decision portfolio state, market path, outcome
horizon, transaction/execution-cost assumptions, mandatory exogenous rules,
and non-target-slot decision context.

For every other slot j != s, both branches preserve identically the frozen RL
proposal at T, non-target-slot gate participation decision/status,
active/inactive slot mapping, mandatory exogenous actions, portfolio constraint
configuration, execution/cost configuration, execution ordering or simultaneity
convention, applicable market path, and evaluation horizon. Neither branch may
silently re-optimize another slot, change its gate decision, substitute another
security, change execution priority, change portfolio constraints or cost
assumptions, or rebalance another slot merely because s was suppressed.

`portfolio_action_context_identity` identifies the immutable contemporaneous
portfolio-action context held fixed for target slot s. Its canonical payload
contains at least:

```text
decision_time_utc
foundation_policy_identity
foundation_policy_configuration_identity
ordered_simultaneous_RL_requested_target_exposures
ordered_non_target_slot_participation_statuses
non_target_slot_reference_policy_identity
active_inactive_slot_mapping
portfolio_constraint_configuration_identity
execution_ordering_or_simultaneity_convention_identity
execution_cost_configuration_identity
mandatory_exogenous_action_context

portfolio_action_context_identity =
SHA256(CANONICAL_JSON_OF_PORTFOLIO_ACTION_CONTEXT_SPECIFICATION)
```

Use section-17 canonical JSON and SHA-256 rules, excluding the computed
identity itself from its payload. Ordered entries retain explicit slot and
canonical security mapping in the accepted slot order; non-target participation
statuses explicitly identify j != s. The target remains separately identified
by `canonical_security_id` plus `security_slot_id`. Including this context
identity in both the logical gate example and the paired-control payload makes
the pair uniquely encode the target-slot decision plus its fixed contemporaneous
portfolio context. Missing or ambiguous required context cannot yield a
supervised binary target.

```text
GATE_TARGET_STATE = COUNTERFACTUAL_NOT_IDENTIFIABLE
```

Use this state whenever shared portfolio feasibility or execution coupling
prevents the branches from differing only in target-slot participation. This
includes binding cash, gross exposure, net exposure, leverage, concentration,
shared execution-allocation, or other portfolio-wide feasibility constraints
that necessarily change another slot when s executes or is suppressed. Do not
silently reallocate other slots, invent a binary target, label PARTICIPATE, or
label SUPPRESS; exclude the example from supervised gate-target use. A later
separately frozen deterministic attribution rule could govern such cases, but
C6-E neither chooses nor authorizes one.

The existing `incremental_net_value_usd = UNGATED_END_VALUE_USD -
SUPPRESSED_END_VALUE_USD` and positive-value PARTICIPATE / nonpositive-value
SUPPRESS rules remain unchanged. Their binary values are valid only under
`SINGLE_SLOT_PARTICIPATION_DECISION_AT_T` with uniquely reproducible fixed
contemporaneous portfolio context and an identifiable comparison, in addition
to the existing eligibility, availability, and horizon requirements.

### C6-E technical definition — supervised label reference context

`C6_E_DETAIL_DEFINED`:

```text
GATE_LABEL_COUNTERFACTUAL_REFERENCE = FROZEN_UNGATED_RL_REFERENCE
RF_XGB_GATE_OUTPUTS_IN_TARGET_CONSTRUCTION = PROHIBITED
non_target_slot_reference_policy_identity = FROZEN_UNGATED_RL_REFERENCE
GATE_TARGET_CONSTRUCTION_CIRCULARITY = PROHIBITED
```

For supervised label construction for target slot s, the branch difference
remains EXECUTE versus SUPPRESS the frozen RL proposal for s. Every non-target
slot j != s uses a deterministic reference status derived only from the frozen
ungated RL foundation policy and already-governed pre-decision state:

| Non-target slot condition | NON_TARGET_REFERENCE_STATUS |
|---|---|
| j is inactive | `INACTIVE_NO_ACTION` |
| j is active and `ungated_requested_target_exposure_fraction == current_realized_exposure_fraction` | `NO_REBALANCE_REFERENCE` |
| j is active and `ungated_requested_target_exposure_fraction != current_realized_exposure_fraction` | `PARTICIPATE_UNGATED_REFERENCE` |

The active-slot comparisons require valid, resolved inputs under the existing
fail-closed rules. These statuses measure s's marginal participation value
relative to the frozen ungated RL portfolio context. Mandatory exogenous
actions remain separately governed and identical in both branches; existing
shared-constraint and `COUNTERFACTUAL_NOT_IDENTIFIABLE` rules remain fully
effective, including the prohibition on silent other-slot reallocation.

For supervised target construction,
`ordered_non_target_slot_participation_statuses` in the existing
`portfolio_action_context_identity` payload means precisely these deterministic
reference statuses in the accepted slot order. The added
`non_target_slot_reference_policy_identity` field identifies the
`FROZEN_UNGATED_RL_REFERENCE` rule. No RF/XGBoost gate identity, prediction, or
learned threshold is used inside this label-reference identity. No RF
prediction, XGBoost prediction, learned gate threshold, qualification result,
or later gate output may determine a non-target reference status for a label.

A supervised target must be fully constructible before its RF or XGBoost gate
model or threshold is trained. RF labels cannot depend on RF predictions, and
XGBoost labels cannot depend on XGBoost predictions; neither may depend on the
other gate's predictions. Target construction is independent of which gate
later consumes the label. RF and XGBoost can consume the same frozen target
definition/reference context and remain alternative ablations of the same
gating hypothesis, subject to the existing shared-schema/target requirement.
Neither model may redefine its own target through model-dependent context.

This frozen ungated reference applies specifically to supervised label
construction. It does not require every non-target slot to execute in a later
gated portfolio evaluation. Later separately authorized evaluation may apply
trained gates to multiple slots under frozen inference rules. Interactions
among simultaneous gate decisions are measured in the actual paired
gated-versus-ungated experiment; they must not feed backward into label
construction through model-dependent non-target statuses. The existing
single-slot counterfactual, incremental net value, binary target, market-path,
horizon, cost, portfolio-constraint, and mandatory-exogenous-action rules are
unchanged.

### C6-E technical definition — outcome horizon and leakage controls

`C6_E_DETAIL_DEFINED`:

```text
GATE_OUTCOME_START = THE_GOVERNED_EXECUTION_TRANSITION_FOR_ACTION_T
GATE_OUTCOME_END =
THE_NEXT_GOVERNED_DECISION_TIME_FOR_THE_SAME_SLOT_WITHIN_THE_SAME_PARTITION_AND_EPISODE

GATE_TARGET_STATE = OUTCOME_HORIZON_NOT_AVAILABLE
IF NO_VALID_NEXT_GOVERNED_DECISION_EXISTS_INSIDE_THE_SAME_PARTITION_AND_EPISODE
```

`outcome_start_utc` and `outcome_end_utc` resolve these governed instants.
The end is evaluated before the next decision's action/transition, so that
next action does not contaminate action-T participation value. A remapped slot
is not continuity of the prior security; section-12 resets and identity
requirements apply. An unavailable horizon produces no supervised gate target.
The horizon must never cross a walk-forward validation boundary, the
development/qualification boundary, the qualification/final-holdout boundary,
or an episode-reset boundary that invalidates comparison identity.

Gate examples preserve the section-15 information cutoff and complete
forward-dependency bounds; this outcome horizon is an applicable target-horizon
identity for split hashing and purge/embargo. No target may survive because
its feature timestamp precedes a boundary if its outcome crosses that
boundary. Outcome/label computation, when later authorized, is separate from
feature assembly and cannot feed future outcomes into the gate's decision.

### C6-E technical definition — paired control identity and development boundary

`C6_E_DETAIL_DEFINED` — an immutable paired-control specification includes at
least:

```text
dataset_instance_id
split_identity
foundation_policy_identity
foundation_policy_configuration_identity
decision_time_utc
canonical_security_id
security_slot_id
pre_decision_state_identity
ungated_policy_action_identity
execution_cost_configuration_identity
gate_feature_schema_identity
gate_target_definition_identity
outcome_horizon_identity
portfolio_action_context_identity

paired_control_identity = SHA256(CANONICAL_JSON_OF_PAIRED_CONTROL_SPECIFICATION)
```

Use section-17 canonical JSON/SHA-256 rules, excluding the computed identity
itself from its payload. These are references to the governed source dataset
and immutable policy/state/configuration identities; do not create a circular
source dataset identity by including an identity-bearing gate artifact in its
own referenced source dataset hash inputs.

For RF or XGBoost gated experiments, the paired ungated control differs only
in the participation decision mechanism. No hidden differences in data,
temporal partitions, foundation policy, initial state, transaction-cost
assumptions, outcome horizon, or evaluation metrics are permitted. Downstream
state divergence caused by participation is an outcome, not permission to
change the common experiment configuration. RF and XGBoost ablations for the
same foundation use the same gate-feature schema and target definition unless
a separately authorized prospective redesign changes the experiment family.

C6-E selects no RF or XGBoost threshold. Later authorized gate threshold
selection uses DEVELOPMENT_REGION only; the threshold is frozen before
applicable qualification. Qualification and final-holdout results cannot tune
a threshold, select RF versus XGBoost, change gate features, target, or horizon,
or alter the foundation policy. Gate development remains subject to section-15
chronological folds, train-only fitting, and dependency purge rules.

### C6-E technical definition — Option B+ foundation routing

`C6_E_DETAIL_DEFINED`:

```text
QUALIFICATION_ROUTING = OPTION_B_PLUS
PRIMARY_GATING_FOUNDATION_COUNT = 1
OPTIONAL_ROBUSTNESS_GATING_FOUNDATION_COUNT = AT_MOST_1
PRIMARY_FOUNDATION_PRIORITY =
PPO
THEN_SAC
THEN_RECURRENTPPO
POST_HOC_BEST_SCORE_ROUTING = NOT_AUTHORIZED
```

Primary routing is only among later candidates with accepted eligible frozen
dispositions. Use this priority, never the observed best development or
qualification score: PPO if eligible/frozen; otherwise SAC; otherwise
RecurrentPPO. At most one additional eligible/frozen candidate is an optional
robustness foundation, chosen from the remaining candidates by the same
priority. No candidate is forced through implementation/training to populate
a foundation, and no fourth RL model may be substituted. If none is eligible,
there is no foundation; the count does not override eligibility or authorize
work. These interfaces do not implement, train, qualify, or route a live
candidate or gate.

## 17. Provider/source provenance and reproducibility identity

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S4]: provider-neutral schema and provider-specific
  adapter boundaries are preserved.
- `ACCEPTED_REQUIREMENT` [S4]: material provider semantics must remain explicit
  rather than being flattened into a lowest-common-denominator schema.
- `ACCEPTED_REQUIREMENT` [S4]: provenance includes source/feed identity,
  identifier namespace, timestamp/bar semantics, raw/adjusted lineage,
  corporate-action/reference state, as-of/revision state, retrieval timestamp,
  checksum, and license/entitlement lineage where applicable.
- `ACCEPTED_REQUIREMENT` [S4]: a material source change requires dataset
  rebuild and affected later research rerun.
- `ACCEPTED_REQUIREMENT` [S6]: the accepted PIT capability path remains
  multi-source and explicitly separates historical eligibility evidence from
  provider market-bar coverage.
- `ACCEPTED_REQUIREMENT` [S11, S12]: data responsibilities include immutable
  raw/derived identity and provenance verification.

### C6-B technical definition — provenance and reproducibility identity

`C6_B_DETAIL_DEFINED` — all identity hashes use SHA-256 and lowercase hex.
Canonical hash serialization is UTF-8 canonical JSON with lexicographically
sorted object keys, explicit nulls, no insignificant whitespace, UTC RFC3339
`Z` timestamps, decimal values serialized as normalized decimal strings, and
arrays placed in their contractually defined deterministic order. Machine-local
absolute paths, notebook execution order, unstored environment state, and
unrecorded provider defaults are excluded from scientific identity.

Human-readable `*_schema_version` labels support review, but the authoritative
schema identity is:

`schema_identity = SHA256(canonical schema specification)`

where the canonical schema specification includes logical table/class names,
field names, dtypes, requiredness/nullability, natural keys, ordering rules,
and field semantics.

#### Dataset provenance manifest

Every raw or processed dataset instance must have one immutable provenance
manifest containing:

| Field | Required | Identity role |
|---|---:|---|
| `manifest_schema_version` | YES | Manifest schema label |
| `dataset_role` | YES | Raw or processed logical dataset role |
| `schema_identity` | YES | Immutable schema hash |
| `dataset_instance_id` | YES | Authoritative dataset-instance identity |
| `source_provenance_identity` | YES | Hash of governed source identities and semantics |
| `transformation_identity` | YES | Processed transformation hash; `NOT_APPLICABLE` for purely raw capture |
| `provenance_manifest_identity` | YES | Hash of identity-bearing manifest payload excluding itself |
| `security_identity_registry_sha256` | CONDITIONAL | Required for security-bearing datasets |
| `universe_definition_identity` | CONDITIONAL | Required when accepted universe rules/membership apply |
| `calendar_identity_ref` | CONDITIONAL | Required when session/calendar semantics apply; C6-C defines its final mechanics |
| `adjustment_lineage_identity` | CONDITIONAL | Explicit price/reference adjustment lineage |
| `parent_dataset_ids` | YES | Ordered array; empty only where no parent dataset exists |
| `source_object_sha256s` | YES | Ordered unique source-object hashes |
| `data_artifact_sha256s` | YES | Ordered hashes of canonical pre-manifest data artifacts whose bytes are independent of dataset/manifest identity |
| `source_field_map_versions` | YES | Ordered unique human-readable adapter mapping versions |
| `source_field_map_identities` | YES | Ordered unique immutable mapping-manifest hashes |
| `adapter_identities` | YES | Ordered unique immutable adapter identities |
| `code_repository` | CONDITIONAL | Required for processed transformations |
| `code_commit_sha` | CONDITIONAL | Required immutable code version for processed transformations |
| `transformation_spec_version` | CONDITIONAL | Required for processed transformations |
| `transformation_configuration_sha256` | CONDITIONAL | Required for processed transformations |
| `license_entitlement_refs` | YES | Non-secret provenance references; may be empty when not applicable |
| `created_at_utc` | YES | Observational manifest creation time; excluded from dataset scientific identity |
| `split_identity_ref` | OPTIONAL | Reserved reference for later C6-E partition identity; C6-B defines no split policy |

#### Canonical data-artifact hash membership

`data_artifact_sha256s` is the lexicographically sorted unique set of SHA-256
hashes for immutable canonical data artifacts whose bytes are finalized before
`dataset_instance_id` is computed. Depending on dataset role, these are the
canonical raw-record and/or processed-table/partition content artifacts
covered by `schema_identity`.

The identity input explicitly excludes:

- the provenance manifest containing `dataset_instance_id`;
- `provenance_manifest_identity`;
- any final manifest artifact or sidecar whose bytes contain
  `dataset_instance_id`;
- any report, display metadata, mutable index, filename-only locator, or other
  artifact whose bytes are created or rewritten after `dataset_instance_id`;
  and
- any artifact whose bytes depend directly or indirectly on
  `dataset_instance_id` or `provenance_manifest_identity`.

If an implementation later embeds `dataset_instance_id` into an otherwise
canonical data file, that file cannot be a member of the pre-manifest
`data_artifact_sha256s` identity input; its scientific content root must be
hashed in an identity-independent canonical representation instead.

Each source entry represented by `source_provenance_identity` must preserve,
when applicable: provider, dataset/product, explicit feed, publisher/venue
scope, identifier namespace, timestamp/bar semantic identifier,
raw-versus-adjusted state, corporate-action/reference snapshot identity,
source as-of/revision state, retrieval timestamp, source-object SHA-256,
license/entitlement reference, adapter version/identity, and source-field-map version/identity.
Provider defaults that are material to scientific interpretation must be
recorded explicitly. In particular, applicable Alpaca historical stock bars
record `source_feed = sip`; Alpaca remains provisional market-bar/later
paper-feed infrastructure and is not promoted to the sole PIT reference source.

#### Binding of universe and state interface identity references

The existing provenance-manifest and dataset-instance
`universe_definition_identity` references mean the exact upstream rule
specification identity in section 10. They never identify realized membership
or include membership artifact hashes that later feed the same dataset
identity. Rule specification precedes realized membership, canonical artifact
hashes, dataset identity, and provenance manifest identity in the existing
acyclic dependency order.

`state_interface_identity` is the section-11 structural identity, not a new
`dataset_instance_id` input. No input is added to the existing hash payload;
any separately governed dataset-role requirement must preserve that explicit
payload and its identity boundaries. `DATASET_IDENTITY_CIRCULARITY = NONE`
and `PROVENANCE_MANIFEST_SELF_REFERENCE = NONE` remain unchanged.

#### Identity envelopes

`source_provenance_identity` is SHA-256 over the canonically ordered source
entries, immutable source-object hashes, adapter identities, field-map identities, and material
provider semantics.

For processed datasets, `transformation_identity` is SHA-256 over canonical
JSON containing code commit, transformation-spec version,
transformation-configuration SHA-256, parent schema identities, and the
already-computed `adjustment_lineage_identity`. Adjustment-lineage records do
not contain `transformation_identity`, so this dependency is one-way. An
observational execution timestamp is not part of this deterministic
transformation identity.

`dataset_instance_id` is SHA-256 over canonical JSON containing exactly:
`dataset_role`, `schema_identity`, `source_provenance_identity`,
`transformation_identity`, `security_identity_registry_sha256`,
`universe_definition_identity`, `calendar_identity_ref`,
`adjustment_lineage_identity`, and the lexicographically ordered
`data_artifact_sha256s`. Each conditional identity field uses its contractually
defined literal `NOT_APPLICABLE` when that concept does not apply; silent
omission is not equivalent. No current dataset ID is generated by C6-B because
no dataset exists.

Only after `dataset_instance_id` exists is the provenance-manifest payload
assembled. `provenance_manifest_identity` is SHA-256 over the canonical
identity-bearing manifest payload including `dataset_instance_id`, but with
the `provenance_manifest_identity` field itself omitted. `created_at_utc`,
descriptive local paths, and non-scientific display metadata are also excluded
from that hash input. The final serialized manifest may then store the computed
`provenance_manifest_identity`; the final manifest bytes are never a member of
`data_artifact_sha256s`.

The deterministic dependency order is:

```text
SOURCE_OBJECT_IDENTITIES
→ SCHEMA_SOURCE_REGISTRY_AND_ADJUSTMENT_LINEAGE_IDENTITIES
→ TRANSFORMATION_IDENTITY
→ CANONICAL_DATA_ARTIFACT_HASHES
→ DATASET_INSTANCE_ID
→ PROVENANCE_MANIFEST_PAYLOAD
→ PROVENANCE_MANIFEST_IDENTITY

DATASET_IDENTITY_CIRCULARITY = NONE
PROVENANCE_MANIFEST_SELF_REFERENCE = NONE
ARTIFACT_HASH_MEMBERSHIP = EXPLICIT
IDENTITY_DEPENDENCY_ORDER = DEFINED
```

A human-readable dataset version label may be derived from schema version and a
short prefix of `dataset_instance_id`, but it is never authoritative in place
of the full dataset identity.

#### Raw-to-processed lineage

Every processed dataset manifest references its raw parent dataset identity or
identities. Every processed row has `source_lineage_id`, defined as SHA-256
over the sorted unique set of that row's `lineage_edge_id` values. Each lineage
edge names the child row, parent raw record, relationship type, and exact
`transformation_identity`. Many-to-one and many-to-many transformations are
therefore explicit rather than inferred from row order or filenames.

#### Adjustment-lineage identity contract

`raw_adjustment_state` remains the raw-record source-state field and preserves
exactly `RAW_AS_TRADED`, `PROVIDER_ADJUSTED`, `NOT_APPLICABLE`, or
`SOURCE_UNSPECIFIED`.

Each processed market-bar row references exactly one
`adjustment_lineage_id`. That value identifies one canonical
`adjustment_lineage_record` with this exact identity-bearing schema:

| Field | Logical dtype | Requiredness | Identity meaning |
|---|---|---:|---|
| `adjustment_lineage_schema_version` | string | YES | Human-readable lineage-schema version |
| `source_adjustment_state` | string | YES | One of the four `raw_adjustment_state` values |
| `parent_raw_record_ids` | array[string] | YES | Sorted unique raw-record parents contributing to the row |
| `reference_snapshot_ids` | array[string] | YES | Sorted unique source/reference snapshot IDs; empty when none apply |
| `corporate_action_raw_record_ids` | array[string] | YES | Sorted unique raw corporate-action/event records used by the adjustment specification; empty when none apply |
| `adjustment_spec_identity` | string | YES | SHA-256 identity of the adjustment specification, or literal `NOT_APPLICABLE` when no adjustment specification applies |
| `adjustment_configuration_identity` | string | YES | SHA-256 identity of adjustment configuration, or literal `NOT_APPLICABLE` when none applies |

`adjustment_lineage_id` is the lowercase-hex SHA-256 of the UTF-8 canonical
JSON serialization of the complete record above. The ID field itself is not
inside the hashed record. The record contains no `transformation_identity`,
`dataset_instance_id`, or processed-row ID, so it introduces no circular
dependency.

`adjustment_lineage_identity` is a distinct dataset-scope value, not an alias
for a row's `adjustment_lineage_id`. For a processed dataset to which
adjustment semantics apply, it is SHA-256 over canonical JSON containing the
adjustment-lineage schema identity and the lexicographically sorted unique set
of all `adjustment_lineage_id` values referenced by that dataset. The processed
dataset manifest stores this full `adjustment_lineage_identity`, and it is an
input to `transformation_identity` and `dataset_instance_id` as defined above.

When a processed market-bar row is intentionally preserved as raw/as-traded or
provider-adjusted, `source_adjustment_state` records `RAW_AS_TRADED` or
`PROVIDER_ADJUSTED` and the source/reference inputs remain explicit. When the
source does not establish its adjustment state,
`source_adjustment_state = SOURCE_UNSPECIFIED`; that state is not silently
treated as raw/as-traded. When adjustment semantics are structurally irrelevant
to a row or dataset role, `source_adjustment_state = NOT_APPLICABLE`,
reference/corporate-action arrays are empty, and both adjustment spec/config
fields use the exact literal `NOT_APPLICABLE`.

For a processed dataset role with no adjustment-bearing rows at all, the
manifest field `adjustment_lineage_identity` uses the exact literal
`NOT_APPLICABLE`. For a processed market-bar dataset, each row still has a
deterministic `adjustment_lineage_id`, including rows whose lineage record
states `NOT_APPLICABLE`; the dataset-level identity is therefore computed from
the sorted unique row-level IDs rather than replaced by null.

Source/reference snapshot IDs and corporate-action raw-record IDs are identity
references only. C6-C later governs when such evidence is point-in-time
available, whether it may be applied at a historical cutoff, chronology
validation, and no-lookahead enforcement. C6-B does not apply future actions or
execute adjustments.

#### Provider-neutral boundary

Canonical downstream field semantics, natural keys, and dataset identities do
not change merely because a provider adapter changes. Provider-specific field
names and behavior remain inside versioned adapters and source-field maps,
while material provider semantics remain explicit in provenance. A provider
switch cannot silently masquerade as the same dataset instance: any material
source/feed/semantic difference changes `source_provenance_identity` and,
therefore, `dataset_instance_id`.

The accepted PIT capability envelope remains multi-source: Sharadar
`TICKERS + ACTIONS`, Alpaca historical SIP bars with explicit `feed=sip`, dated
SEC EDGAR / Inline-XBRL evidence, and historical NYSE Daily TAQ Master
primary-listing evidence. This is a capability contract only and performs no
provider activity.

#### Material-change classification

| Change class | C6-B definition | Required identity/consequence |
|---|---|---|
| `MATERIAL_SOURCE_CHANGE` | Provider, dataset/feed, publisher/venue scope, identifier namespace, timestamp/bar semantics, raw/adjusted semantics, reference/corporate-action snapshot basis, or other material source semantics change | New source provenance identity and dataset instance identity; affected canonical datasets require rebuild; affected later training/validation/backtest research requires rerun when separately authorized |
| `NON_MATERIAL_METADATA_CHANGE` | Descriptive label, display note, or non-identity local storage metadata changes while source bytes and material semantics remain identical | No scientific dataset identity change; must not be used to hide a material change |
| `SCHEMA_CHANGE` | Canonical field, dtype, requiredness, key, ordering, or field-semantic contract changes | New schema version and schema identity; affected dataset instances are distinct and require rebuild |
| `TRANSFORMATION_CHANGE` | Transformation code, specification, configuration, or adjustment-lineage logic changes | New transformation identity and processed dataset instance identity; affected processed datasets require rebuild |
| `DATA_REVISION` | Source publishes revised bytes, revision/as-of state, or corrected records for the same logical source scope | New source-object hash/source provenance identity and affected dataset instance identity; affected datasets require rebuild |

A license/entitlement or permitted-use change is never silently overwritten in
provenance. If it changes what source material may be retained, reproduced,
published, or used, it is a material governance/provenance change requiring
review under then-current terms; C6-B performs no provider transaction.

No provider purchase, account activity, entitlement, authentication, network
access, acquisition, dataset rebuild, or research rerun occurs in C6-B.

## 18. Dataset acceptance rules

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S2]: C6 may define dataset acceptance rules.
- `ACCEPTED_REQUIREMENT` [S2]: dataset-acceptance execution is not authorized
  during C6.
- `ACCEPTED_REQUIREMENT` [S9]: C7 generation/acceptance follows an accepted C6
  contract and later data-access authorization.
- `ACCEPTED_REQUIREMENT` [S11, S12]: later acceptance must verify schema,
  calendar, expected-slot, coverage, duplicate, missingness, timestamp,
  provenance, and immutable identity behavior.
- `ACCEPTED_REQUIREMENT` [S6]: provider missingness must not be silently
  converted into scientific eligibility failure.
- `ACCEPTED_REQUIREMENT` [S11, S12]: silent imputation and silent dataset
  acceptance are prohibited.

### C6-F technical definition — acceptance execution precondition

`C6_F_DETAIL_DEFINED` — future actual acceptance execution requires:

```text
DATASET_ACCEPTANCE_EXECUTION_PRECONDITION =
C6_DATASET_CONTRACT == FROZEN
AND dataset_contract_status == FROZEN__EFFECTIVE
AND C6_H_STATUS == COMPLETE__FROZEN__EFFECTIVE
AND SEPARATE_DATASET_ACCEPTANCE_EXECUTION_AUTHORIZATION == YES

UNFROZEN_CONTRACT_DATASET_ACCEPTANCE = PROHIBITED
DATASET_ACCEPTANCE_PASS_AGAINST_UNFROZEN_CONTRACT = PROHIBITED
NOT_EXECUTABLE = PRECONDITION_STATE_BEFORE_ACCEPTANCE_CHECK_EXECUTION
```

C6-F defines this precondition only and does not satisfy it. C6-H freeze alone
does not authorize acceptance; separate later acceptance-execution
authorization is required. Before execution, the frozen/effective lifecycle
state, accepted C6-H freeze evidence, and applicable authorization identity
must be established. If the contract is not frozen/effective, authorization is
absent, or required freeze identity evidence cannot be established, the
procedure is `NOT_EXECUTABLE`: acceptance checks must not run against an
unfrozen or unverified contract.

`NOT_EXECUTABLE` is exclusively a pre-execution state, not a fourth
`DATASET_ACCEPTANCE_DISPOSITION` result and not an executed acceptance report's
`final_disposition`. Once execution is validly authorized against the frozen
contract, actual evaluation uses exactly PASS, FAIL, and UNRESOLVED with the
existing FAIL, then UNRESOLVED, then PASS precedence. An observed mismatch
between the acceptance execution's contract identity and accepted freeze
evidence is FAIL; it cannot yield PASS or justify proceeding on a different
contract. If detected before execution, the mismatch blocks execution rather
than authorizing acceptance checks.

### C6-F technical definition — dataset acceptance disposition model

`C6_F_DETAIL_DEFINED`

The acceptance unit is one declared governed dataset instance and role.

Define final dispositions only:

```text
DATASET_ACCEPTANCE_DISPOSITION =
PASS
|
FAIL
|
UNRESOLVED
```

Define deterministic precedence:

```text
ACCEPTANCE_PRECEDENCE =
FAIL
THEN
UNRESOLVED
THEN
PASS
```

Meaning:

PASS =
every applicable required check passes and no required check is unresolved.

FAIL =
at least one observed contract violation or hard-fail condition exists.

UNRESOLVED =
no observed hard failure exists, but required evidence is unavailable,
ambiguous, incomplete, or insufficient to establish compliance.

If both FAIL and UNRESOLVED conditions exist:

FINAL_DISPOSITION =
FAIL

Define:

```text
SILENT_DATASET_ACCEPTANCE = PROHIBITED
UNRESOLVED_AS_PASS = PROHIBITED
FAIL_CLOSED_ACCEPTANCE = REQUIRED
```

A dataset with FAIL or UNRESOLVED disposition is not an accepted governed
dataset for downstream scientific use.

C6-F defines these rules only.

No acceptance evaluation is executed in C6-F.

### C6-F technical definition — exact acceptance checks and thresholds

`C6_F_DETAIL_DEFINED`

Define deterministic checks with zero tolerance for contract violations.

Do not introduce arbitrary statistical tolerances where the earlier contract
defines exact invariants.

Applicability is determined from the declared role and claimed interfaces before
results are aggregated. Each check records its scope and applicability with
supporting evidence. A demonstrably inapplicable check is excluded from the
required-check denominator, not counted as a passed check or a fourth final
disposition. Unknown applicability is UNRESOLVED. An observed violation is
FAIL even when other required evidence is unavailable. Missing required fields
or references in an inspected artifact are observed violations; inability to
obtain the evidence needed to inspect or verify them is UNRESOLVED absent an
observed contradiction. Counts cover the complete applicable scope, not a
sample, and unavailable counts are never silently recorded as zero.

#### A. Schema conformity

Require:

* declared dataset role is explicit;
* schema version is explicit;
* recomputed schema identity equals declared schema identity exactly;
* 100% of required fields are present;
* 100% of field logical dtypes match the governed schema;
* requiredness and nullable behavior match exactly;
* canonical key fields match the applicable contract;
* canonical ordering fields match the applicable contract.

Hard thresholds:

```text
SCHEMA_IDENTITY_MISMATCH_COUNT = 0
MISSING_REQUIRED_FIELD_COUNT = 0
DTYPE_CONTRACT_VIOLATION_COUNT = 0
REQUIREDNESS_VIOLATION_COUNT = 0
```

Any nonzero count above =
FAIL.

#### B. Identity, provenance, hashes, and lineage

Where applicable require exact recomputation/verification of:

* source object SHA-256 values;
* source provenance identity;
* schema identity;
* transformation identity;
* adjustment lineage identity;
* security identity registry identity;
* universe definition identity;
* calendar identity reference;
* canonical data-artifact SHA-256 values;
* dataset instance identity;
* provenance manifest identity;
* raw-to-processed lineage;
* row-level source lineage;
* adjustment lineage records.

Hard thresholds:

```text
HASH_MISMATCH_COUNT = 0
DANGLING_LINEAGE_REFERENCE_COUNT = 0
MISSING_REQUIRED_PROVENANCE_REFERENCE_COUNT = 0
IDENTITY_RECOMPUTATION_MISMATCH_COUNT = 0
```

Require:

```text
REQUIRED_ARTIFACT_HASH_VERIFICATION_RATE = 100_PERCENT
REQUIRED_PROVENANCE_REFERENCE_COVERAGE = 100_PERCENT
```

Any required mismatch or dangling reference =
FAIL.

Required source/provenance evidence that cannot be established but has no
observed contradiction =
UNRESOLVED.

For exact acceptance recomputation, `universe_definition_identity` uses the
section-10 canonical payload; `state_interface_identity` uses the section-11
canonical payload when the artifact claims that interface. A required identity
whose required upstream frozen inputs cannot be established is UNRESOLVED
unless a direct observed contract violation exists. A declared identity that
recomputes differently is FAIL. This does not bypass the separate frozen-C6
acceptance execution precondition.

#### C. Uniqueness and deterministic ordering

Require exact contract keys and ordering.

Hard thresholds:

```text
DUPLICATE_CANONICAL_KEY_COUNT = 0
ORDERING_INVERSION_COUNT = 0
AMBIGUOUS_SECURITY_IDENTITY_COUNT = 0
```

Any nonzero value =
FAIL.

The ambiguous-identity counter has this exact population:

```text
AMBIGUOUS_SECURITY_IDENTITY_COUNT =
COUNT_OF_APPLICABLE_RECORDS_OR_USES_WHERE
AN_UNRESOLVED_OR_CONFLICTING_SECURITY_IDENTITY
IS_ASSERTED_OR_CONSUMED_AS_A_SINGLE_VALID_RESOLVED_CANONICAL_SECURITY_ID

REQUIRED_SECURITY_IDENTITY_UNRESOLVED_COUNT =
COUNT_OF_REQUIRED_USABLE_SCOPE_IDENTITIES
THAT_CANNOT_BE_ESTABLISHED_AS_RESOLVED
WITHOUT_AN_OBSERVED_FALSE_RESOLUTION_VIOLATION
```

The zero threshold above remains mandatory. False-resolution violations
include an UNRESOLVED mapping consumed as an established security, a CONFLICT
mapping with one candidate silently selected, multiple conflicting candidates
consumed as one without governed resolution, or a required usable row claiming
resolved identity contrary to evidence. Any nonzero hard-fail counter is FAIL.

Correctly retained unresolved/conflicting evidence does not itself increment
that counter when it is not consumed as resolved. For the role's required
usable scope, `REQUIRED_SECURITY_IDENTITY_UNRESOLVED_COUNT > 0` yields
UNRESOLVED unless another observed hard failure yields FAIL under the existing
precedence. Evidence outside that claimed scope remains preserved and must
not be silently deleted; it does not itself force UNRESOLVED unless the role
claims dependency on it. Every applicable scope decision is explicit in the
acceptance report. Ambiguity is not converted into PASS; FAIL, then UNRESOLVED,
then PASS precedence and provider-missingness/PIT protections remain intact.

#### D. Calendar and session conformity

Require applicable rows and expected-slot representations to agree with the
accepted C6-C calendar/session contract.

Hard thresholds:

```text
UNEXPECTED_REGULAR_SESSION_ROW_COUNT = 0
INVALID_SESSION_MAPPING_COUNT = 0
DUPLICATE_SECURITY_TIMESTAMP_COUNT = 0
DST_RULE_VIOLATION_COUNT = 0
EARLY_CLOSE_RULE_VIOLATION_COUNT = 0
BAR_INTERVAL_SEMANTIC_VIOLATION_COUNT = 0
```

Require:

```text
EXPECTED_SLOT_ACCOUNTING_RATE = 100_PERCENT
UNCLASSIFIED_EXPECTED_SLOT_COUNT = 0
```

`EXPECTED_SLOT_ACCOUNTING_RATE = 100_PERCENT` means every expected slot is
represented either by a valid observed record or by the explicit governed
missingness/reconstruction state required by section 9.

It does NOT mean 100% of expected market bars must be observed.

Do not invent a minimum observed-bar percentage.

#### E. Missingness and reconstruction

Require every missing/affected expected slot to have an explicit permitted
state.

Hard thresholds:

```text
UNCLASSIFIED_MISSINGNESS_COUNT = 0
PROHIBITED_RECONSTRUCTION_COUNT = 0
SILENT_FORWARD_FILL_COUNT = 0
SYNTHETIC_FINANCIAL_OBSERVATION_COUNT = 0
RECONSTRUCTION_WITHOUT_REQUIRED_LINEAGE_COUNT = 0
```

Any nonzero count =
FAIL.

Provider missingness, by itself, is NOT scientific eligibility failure when it
is correctly classified and handled under the existing contract.

If missing provider/source evidence prevents a required scientific identity or
PIT determination from being established:

DISPOSITION =
UNRESOLVED

unless a direct contract violation is also observed.

#### F. Chronology, PIT, and leakage

Require all historically applied information to satisfy the accepted C6-C
availability/applicability rules.

Hard thresholds:

```text
FUTURE_INFORMATION_VIOLATION_COUNT = 0
AVAILABLE_BY_T_VIOLATION_COUNT = 0
APPLICABLE_BY_T_VIOLATION_COUNT = 0
FORMATION_CUTOFF_VIOLATION_COUNT = 0
FUTURE_AWARE_TRANSFORMATION_COUNT = 0
```

Any nonzero value =
FAIL.

#### G. Historical-universe conformity

Require deterministic reproduction of applicable accepted formation and
reformation rules from the declared PIT evidence.

Hard thresholds:

```text
UNAUTHORIZED_MID_CYCLE_REPLACEMENT_COUNT = 0
HARD_TERMINAL_REMOVAL_RULE_VIOLATION_COUNT = 0
SECURITY_SLOT_MAPPING_VIOLATION_COUNT = 0
```

Membership evidence that cannot be established because required PIT evidence
is unavailable or ambiguous =
UNRESOLVED.

Do not convert provider missingness into an eligibility failure.

#### H. Split / partition conformity

For any artifact or dataset role that claims governed split/partition
membership, require exact C6-E split identity and geometry.

Hard thresholds:

```text
PARTITION_OVERLAP_COUNT = 0
OUTCOME_BOUNDARY_CROSSING_COUNT = 0
TRAIN_VALIDATION_LEAKAGE_COUNT = 0
QUALIFICATION_LEAKAGE_COUNT = 0
FINAL_HOLDOUT_LEAKAGE_COUNT = 0
PREPROCESSOR_FIT_BOUNDARY_VIOLATION_COUNT = 0
```

Any nonzero count =
FAIL.

The recomputed `split_identity` must equal the declared value exactly.

#### I. RL state / recurrent interface compatibility

For any later artifact claiming to instantiate the applicable C6-D RL
state/recurrent interface, require:

* exact state-interface identity;
* maximum 60-slot envelope semantics;
* explicit slot-to-security identity;
* correct active/inactive masks;
* no unresolved required active-slot state treated as valid;
* recurrent validity masks/lengths;
* no forbidden sequence partition crossing;
* required episode/session/formation boundary behavior;
* no silent candidate-specific feature reordering.

Hard thresholds:

```text
STATE_INTERFACE_IDENTITY_MISMATCH_COUNT = 0
ACTIVE_SLOT_IDENTITY_VIOLATION_COUNT = 0
UNMASKED_INVALID_STATE_COUNT = 0
RECURRENT_BOUNDARY_VIOLATION_COUNT = 0
```

Any nonzero count =
FAIL.

This check is applicable only when the accepted dataset/artifact role actually
claims to instantiate those interfaces.

#### J. Gate dataset / target compatibility

For any later artifact claiming to instantiate the C6-E supervised gate
interface, require:

* gate feature cutoff compliance;
* exact foundation-policy identity;
* single-slot counterfactual scope;
* frozen ungated RL label-reference context;
* no RF/XGBoost output used in target construction;
* valid portfolio-action context identity;
* valid paired-control identity;
* correct outcome horizon;
* no binary label when counterfactual is not identifiable;
* no binary label when outcome horizon is unavailable.

Hard thresholds:

```text
GATE_FEATURE_LOOKAHEAD_COUNT = 0
MODEL_DEPENDENT_TARGET_CONSTRUCTION_COUNT = 0
COUNTERFACTUAL_CONTEXT_MISMATCH_COUNT = 0
INVALID_BINARY_GATE_TARGET_COUNT = 0
```

Any nonzero count =
FAIL.

#### K. Coverage accounting

Require explicit coverage metrics by applicable:

* dataset role;
* security;
* formation/reformation interval;
* regular session;
* expected-slot status;
* source/provenance state.

Define:

```text
COVERAGE_ACCOUNTING_COMPLETENESS = 100_PERCENT
ARBITRARY_MINIMUM_OBSERVED_BAR_PERCENTAGE = NONE
```

Every expected observation position must be accounted for, but an explicit
governed missing observation is not silently converted into a failure merely
because it is absent.

### C6-F technical definition — acceptance evidence package

`C6_F_DETAIL_DEFINED`

Define a deterministic acceptance report containing at least:

```text
acceptance_spec_version
dataset_role
dataset_instance_id
schema_identity
source_provenance_identity
transformation_identity
calendar_identity_ref
universe_definition_identity
split_identity_or_NOT_APPLICABLE
evaluated_frozen_contract_sha256
evaluated_frozen_contract_git_blob_sha
evaluated_c6_contract_version_identity
evaluated_c6_freeze_manifest_identity
acceptance_execution_authorization_identity
evaluation_code_commit_identity
evaluation_environment_identity
check_results
hard_fail_count
unresolved_count
final_disposition
evidence_references
material_change_state
source_reconciliation_state
```

Each `check_results` entry must contain at least:

```text
check_id
check_scope
observed_value_or_count
required_threshold_or_invariant
check_disposition
evidence_reference
```

`evaluated_frozen_contract_sha256` is the authoritative exact frozen-contract
byte hash; no unfrozen placeholder or duplicate generic contract hash is used.
All four frozen-contract identities must agree exactly with accepted C6-H
freeze evidence. `acceptance_execution_authorization_identity` identifies the
separate authorization under which this acceptance was actually executed.
Required freeze evidence must be established before execution; inability to
establish it makes the procedure NOT_EXECUTABLE. An observed identity mismatch
in actual acceptance execution is FAIL.

The identity-bearing report payload includes these frozen-contract identities
and the acceptance-execution authorization identity, cryptographically binding
the report to the exact frozen C6 contract, contract version, freeze manifest,
and execution authorization. Mutable local paths and observational timestamps
are excluded from this payload under the existing section-17 canonical JSON
and SHA-256 rules.

The acceptance-report identity is:

```text
dataset_acceptance_report_identity =
SHA256(CANONICAL_JSON_OF_IDENTITY_BEARING_ACCEPTANCE_REPORT_PAYLOAD)
```

Use section-17 canonical JSON/SHA-256 rules.

Exclude the report identity itself and observational generation timestamp from
its own identity payload.

The final serialized report may include observational timestamps and local
paths as non-identity metadata.

Identity-bearing check results are ordered by `check_id` and `check_scope`;
evidence references identify immutable evidence content rather than mutable
local paths. `hard_fail_count` and `unresolved_count` count check entries with
those dispositions; observed row-level violation counts remain in each entry.
The final disposition follows the stated precedence over all required checks.
No acceptance report is generated in C6-F.

### C6-F technical definition — material change / reacceptance

`C6_F_DETAIL_DEFINED`

Preserve section-17 material-change classifications.

Define:

* a material source change;
* schema change;
* transformation change;
* data revision;
* material universe-definition change;
* material calendar change;
* material split change

as requiring the affected later dataset to have the appropriate new identity
and a new acceptance evaluation when separately authorized.

A prior PASS must not silently transfer to a different dataset instance.
A material split change requires a new split identity and acceptance of the
affected role/membership claim; it changes the dataset instance identity only
when section-17 dataset identity inputs change. This does not add split
identity to the earlier dataset-instance hash payload.

Non-material descriptive metadata changes do not create a new scientific
dataset identity when section-17 identity inputs are unchanged.

### C6-F technical definition — 75-security source note

`C6_F_DETAIL_DEFINED`

Preserve the existing 75-security reconciliation note as:

```text
SOURCE_RECONCILIATION_75_STATUS =
UNRESOLVED_NONCONTROLLING_NOTE
```

It is NOT an acceptance criterion.

Do not:

* require 75 securities;
* treat 75 as a maximum;
* reject a dataset for not satisfying the unverified `50 to 75` wording;
* promote that wording into an accepted scientific rule.

Dataset acceptance uses only controlling accepted universe requirements.

C6-F does not resolve this source note.

## 19. Independent C6 review requirements

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S2]: independent C6 review requirements are part of
  the authorized C6 contract-freeze scope.
- `ACCEPTED_REQUIREMENT` [S9]: the C6 exit gate requires dataset contracts to
  be frozen and independently audited.

### C6-F technical definition — C6-G review unit and independence

`C6_F_DETAIL_DEFINED`

Define:

```text
C6_G_INITIAL_MODE =
INDEPENDENT_READ_ONLY_COMPLETE_CONTRACT_REVIEW
```

The reviewer must:

* operate from a review context distinct from the authoring/execution context
  that produced the C6-F draft;
* not mutate repository content during the initial review;
* inspect the actual published contract rather than relying on Managing
  summaries;
* inspect the actual canonical scientific/governance sources cited by the
  contract;
* review C6-A through C6-F as one integrated contract;
* remain independent of any later bounded correction execution until the full
  initial audit has been returned.

C6-F does NOT execute this review.

### C6-F technical definition — C6-G evidence package

`C6_F_DETAIL_DEFINED`

Require the later independent reviewer to receive/establish at least:

```text
canonical_main_sha
contract_path
contract_byte_count
contract_sha256
contract_git_blob_sha
C6_A_publication_identity
C6_B_publication_identity
C6_C_publication_identity
C6_D_publication_identity
C6_E_publication_identity
C6_F_publication_identity
controlling_source_file_identities
supporting_decision_identities
research_design_decision_identity
current_source_reconciliation_notes
CURRENT_CHECKPOINT_TRACKER
```

The reviewer must verify the contract against actual source content and current
canonical repository state.

### C6-F technical definition — complete independent review checklist

`C6_F_DETAIL_DEFINED`

Require review of at least:

1. governance/lifecycle consistency;
2. C6 authorization boundaries;
3. accepted-source traceability;
4. schema/dtype/requiredness consistency;
5. stable identity/key/ordering rules;
6. provenance/hash/lineage non-circularity;
7. calendar/session/DST/early-close semantics;
8. chronology/PIT/as-of/effective-time controls;
9. missingness/reconstruction behavior;
10. historical-universe formation/reformation behavior;
11. PPO/SAC/RecurrentPPO model-family neutrality;
12. RL state and 60-slot semantics;
13. recurrent sequence/reset rules;
14. continuous target-exposure action semantics;
15. economic/cost interface;
16. seven-fold walk-forward geometry;
17. development/qualification/final-holdout isolation;
18. purge/embargo rules;
19. final-holdout untouched-use controls;
20. RF/XGBoost gate-feature availability;
21. single-slot counterfactual attribution;
22. frozen ungated RL gate-label reference;
23. gate-target non-circularity;
24. paired gated/ungated identity;
25. Option B+ routing;
26. dataset acceptance rules;
27. acceptance disposition determinism;
28. freeze requirements;
29. source-reconciliation treatment;
30. internal consistency and absence of identity circularity;
31. absence of authorization leakage into data/model/holdout execution.

### C6-F technical definition — finding classification

`C6_F_DETAIL_DEFINED`

Define:

```text
C6_G_FINDING_CLASS =
MATERIAL_FINDING
|
BOUNDED_CORRECTABLE_FINDING
|
NON_MATERIAL_FINDING
```

`MATERIAL_FINDING` includes a contradiction or defect that would require
changing accepted scientific/lifecycle design, such as:

* candidate-set change;
* material universe-rule change;
* chronology/PIT weakening;
* partition/final-holdout redesign;
* action/reward research redesign;
* gate research-question redesign;
* material provider/scientific requirement change;
* authorization-boundary change;
* unresolved identity/leakage defect with scientific consequences.

Material findings return to Managing/Owner/Admin.

Do not silently repair them.

`BOUNDED_CORRECTABLE_FINDING` means a deterministic ambiguity, internal
inconsistency, missing identity detail, or other correction that:

* remains within accepted C6-A through C6-F science;
* does not alter the Owner-authorized research design;
* has an exact bounded correction surface.

`NON_MATERIAL_FINDING` means editorial or descriptive presentation noise with
no scientific, identity, lifecycle, or authorization effect.

### C6-F technical definition — review dispositions

`C6_F_DETAIL_DEFINED`

Define exactly:

```text
C6_G_REVIEW_DISPOSITION =
PASS
|
PASS_WITH_BOUNDED_CORRECTION
|
FAIL
```

PASS requires:

* no MATERIAL_FINDING;
* no open BOUNDED_CORRECTABLE_FINDING;
* sufficient evidence to complete the full review.

Explicitly represented external pre-freeze blockers may coexist with PASS when
they are not defects in the contract itself.

PASS therefore does NOT automatically mean:

```text
C6_H_FREEZE_ELIGIBLE = YES
```

PASS_WITH_BOUNDED_CORRECTION requires:

* no material finding;
* at least one bounded correctable finding;
* exact bounded correction surface identified.

It does NOT close C6-G.

After Managing separately authorizes and the correction is applied, the
independent reviewer must verify the corrected surface and all affected
invariants before C6-G can receive final PASS.

FAIL applies when:

* any material finding exists; or
* evidence is insufficient to complete a scientifically valid independent
  review.

Initial review remains read-only.

No correction is automatically authorized by a review disposition.

### C6-F technical definition — independent review evidence identity

`C6_F_DETAIL_DEFINED`

Define the later review report to contain at least:

```text
review_spec_version
reviewed_contract_sha256
reviewed_contract_git_blob_sha
reviewed_canonical_main_sha
reviewed_source_identities
review_check_results
finding_inventory
external_freeze_blockers
final_review_disposition
bounded_correction_references
```

Define:

```text
c6_independent_review_identity =
SHA256(CANONICAL_JSON_OF_IDENTITY_BEARING_C6_G_REVIEW_PAYLOAD)
```

Use section-17 canonical JSON/SHA-256 rules.

Exclude its own identity and observational review timestamp from the identity
payload.

C6-G closes only with a final PASS and an immutable review identity.

### C6-F technical definition — 75-security note during review

`C6_F_DETAIL_DEFINED`

Require C6-G to verify that the separate `50 to 75` source note:

* remains explicitly identified;
* remains noncontrolling while unresolved;
* has not silently altered the accepted universe contract;
* is represented as a pre-freeze source-reconciliation item.

An unresolved but correctly represented source note may be listed as:

```text
EXTERNAL_FREEZE_BLOCKER =
SOURCE_RECONCILIATION_75_UNRESOLVED
```

without making the technical C6-G review itself fail.

However C6-H freeze remains prohibited until it is dispositioned.

## 20. Contract-freeze requirements

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S1, S2]: C6 is authorized for specification,
  independent review, and final contract freeze only.
- `ACCEPTED_REQUIREMENT` [S1]: current dataset-contract status is
  `AUTHORIZED__NOT_FROZEN`.
- `ACCEPTED_REQUIREMENT` [S2, S9]: final C6 contract freeze is required before
  later governed dataset generation/acceptance may proceed.

### C6-F technical definition — freeze eligibility

`C6_F_DETAIL_DEFINED`

C6-F does NOT execute the freeze. All eligibility and post-freeze status
values in this section are conditional future requirements, not declarations
of current eligibility or completion. Separate C6-H authorization is required
in addition to meeting eligibility; unestablished conditions cannot establish
eligibility.

Define:

```text
C6_H_FREEZE_ELIGIBLE =
YES
```

only when ALL of the following are true:

```text
C6_A_COMPLETE_PUBLISHED_EFFECTIVE = YES
C6_B_COMPLETE_PUBLISHED_EFFECTIVE = YES
C6_C_COMPLETE_PUBLISHED_EFFECTIVE = YES
C6_D_COMPLETE_PUBLISHED_EFFECTIVE = YES
C6_E_COMPLETE_PUBLISHED_EFFECTIVE = YES
C6_F_COMPLETE_PUBLISHED_EFFECTIVE = YES

C6_G_FINAL_REVIEW_DISPOSITION = PASS

OPEN_MATERIAL_FINDING_COUNT = 0
OPEN_BOUNDED_CORRECTABLE_FINDING_COUNT = 0

SOURCE_RECONCILIATION_BLOCKER_COUNT = 0

UNRESOLVED_FREEZE_BLOCKER_COUNT = 0

UNAUTHORIZED_EXECUTION_BREACH_REQUIRING_OWNER_DISPOSITION = NO

CURRENT_CHECKPOINT_TRACKER = NONE
```

Any false condition above:

```text
C6_H_FREEZE_ELIGIBLE =
NO
```

### C6-F technical definition — 75-security freeze blocker

`C6_F_DETAIL_DEFINED`

Preserve:

```text
SOURCE_RECONCILIATION_75_STATUS =
UNRESOLVED_NONCONTROLLING_NOTE
```

while unresolved.

Before freeze it must receive one explicit authoritative disposition such as:

```text
RESOLVED_AS_NONCONTROLLING__RETIRED
```

or:

```text
RESOLVED_AS_CONTROLLING_WITH_CANONICAL_AUTHORITY
```

C6-F does not choose that disposition.

If an Owner/Admin decision or newly established canonical source makes the
75-security wording controlling and it materially conflicts with accepted
C6-A through C6-E requirements:

```text
STOP
+
OWNER_AUTHORIZED_REDESIGN_OR_REOPEN_REQUIRED
+
NEW_C6_G_REVIEW_REQUIRED_AFTER_CORRECTION
```

C6-H may not freeze while the reconciliation remains unresolved.

### C6-F technical definition — reviewed contract vs final freeze status transition

`C6_F_DETAIL_DEFINED`

Define:

```text
C6_G_REVIEWED_CONTRACT_SHA256 =
THE_EXACT_CONTRACT_SHA256_ACCEPTED_BY_FINAL_C6_G_PASS
```

C6-H may perform only a predeclared lifecycle/status freeze transition after
that PASS.

Allowed H status-transition surface:

* document status/governance block;
* section 1;
* section 2;
* section 21;
* section 22;
* section 23.

No substantive C6-H modification to sections 3–20 is permitted without
invalidating the prior review.

Define:

```text
POST_C6_G_SUBSTANTIVE_CHANGE_TO_SECTIONS_3_THROUGH_20 =
REQUIRES_NEW_INDEPENDENT_REVIEW
```

The C6-H actual diff from the reviewed contract to the frozen contract must be
captured and mechanically verified.

### C6-F technical definition — freeze artifact identities

`C6_F_DETAIL_DEFINED`

At future C6-H, after the permitted status transition, compute:

```text
frozen_contract_sha256 =
SHA256(EXACT_UTF8_BYTES_OF_FROZEN_C6_DATASET_CONTRACT)

frozen_contract_git_blob_sha =
GIT_BLOB_ID_OF_FROZEN_C6_DATASET_CONTRACT
```

Define a deterministic contract version identity over canonical JSON containing
at least:

```text
freeze_spec_version
contract_path
frozen_contract_sha256
C6_G_reviewed_contract_sha256
c6_independent_review_identity
source_reconciliation_disposition_identity
C6_A_publication_identity
C6_B_publication_identity
C6_C_publication_identity
C6_D_publication_identity
C6_E_publication_identity
C6_F_publication_identity
C6_H_status_transition_diff_sha256
```

Then:

```text
c6_contract_version_identity =
SHA256(CANONICAL_JSON_OF_C6_CONTRACT_VERSION_PAYLOAD)
```

Use section-17 canonical JSON/SHA-256 rules.

The computed identity itself is excluded from its own payload.

Do not require the future C6-H commit SHA inside this identity payload, avoiding
commit/self-reference circularity.

The eventual published freeze commit SHA is recorded as non-circular
publication evidence after publication. The exact frozen contract bytes are
finalized first. Computed contract-byte hashes, the contract version identity,
and manifests that depend on them are stored in separate evidence artifacts,
not inserted back into those hashed contract bytes. The reviewed-to-frozen
diff hash is SHA-256 of the exact captured diff bytes; the capture convention
and both endpoint identities are retained for reproducibility.

### C6-F technical definition — freeze acceptance evidence package

`C6_F_DETAIL_DEFINED`

Require future C6-H evidence to contain at least:

```text
freeze_spec_version
C6_G_reviewed_contract_sha256
c6_independent_review_identity
C6_G_final_disposition
resolved_finding_inventory
source_reconciliation_dispositions
C6_H_status_transition_diff_sha256
frozen_contract_sha256
frozen_contract_git_blob_sha
c6_contract_version_identity
freeze_publication_commit_sha
freeze_publication_parent_sha
published_changed_file_surface
post_publication_remote_main_sha
CI_results
CURRENT_CHECKPOINT_TRACKER
```

Define a deterministic freeze-manifest identity from the identity-bearing
portion of this package while excluding:

* the freeze manifest identity itself;
* observational timestamps;
* local paths;
* the future publication commit SHA if inclusion would create circularity.

The published commit SHA remains evidence, not an input that creates
self-reference. Define:

```text
c6_freeze_manifest_identity =
SHA256(CANONICAL_JSON_OF_IDENTITY_BEARING_FREEZE_MANIFEST_PAYLOAD)
```

Use section-17 canonical JSON/SHA-256 rules. The deterministic payload contains
`freeze_spec_version`, `C6_G_reviewed_contract_sha256`,
`c6_independent_review_identity`, `C6_G_final_disposition`,
`resolved_finding_inventory`, `source_reconciliation_dispositions`,
`C6_H_status_transition_diff_sha256`, `frozen_contract_sha256`,
`frozen_contract_git_blob_sha`, `c6_contract_version_identity`, and
`CURRENT_CHECKPOINT_TRACKER`. Finding and disposition inventories use stable
identity order. Publication commit/parent, published changed-file surface,
remote reconciliation, and CI results are retained as subsequent publication
evidence outside this payload. This keeps later publication observations from
creating a manifest/commit dependency cycle.

### C6-F technical definition — immutable post-freeze behavior

`C6_F_DETAIL_DEFINED`

After valid C6-H freeze:

```text
C6_DATASET_CONTRACT =
FROZEN
```

The frozen contract is immutable for the accepted C6 lifecycle.

Any later substantive contract change requires explicit new governance and may
require reopening/requalification of affected downstream work.

No silent edit may retain the prior frozen contract identity.

The final H status semantics must represent at least:

```text
C6_F_status = COMPLETE__PUBLISHED__EFFECTIVE
C6_G_status = COMPLETE__INDEPENDENT_REVIEW_PASS
C6_H_status = COMPLETE__FROZEN__EFFECTIVE

C6_DATASET_CONTRACT = FROZEN
dataset_contract_status = FROZEN__EFFECTIVE

CURRENT_CHECKPOINT_TRACKER = NONE
```

C6-H completion/freeze does NOT itself authorize:

* data purchase;
* data download;
* dataset generation;
* dataset-acceptance execution;
* model work;
* final-holdout access;
* C7 execution.

C7 still requires separate authorization.

## 21. Explicit exclusions / non-authorization boundary

C6-A through C6-F are complete, published, and effective; none is reopened.
C6-G initial review and first re-verification history are recorded above.
Authoring or publishing a correction does not independently close a finding;
independent review evidence controls closure and final PASS. Publication
authority is external to this document and publication state is established
by canonical Git history and governance evidence. This contract creates no
correction, publication, review, or freeze authorization. C6-H and C7 execution
remain unauthorized.

The authorization boundary remains:

```text
data_purchase = NOT_AUTHORIZED
provider_purchase = NOT_AUTHORIZED
provider_account_activity = NOT_AUTHORIZED
network_or_API_data_acquisition = NOT_AUTHORIZED
data_download = NOT_AUTHORIZED

dataset_generation = NOT_AUTHORIZED
dataset_acceptance_execution = NOT_AUTHORIZED
physical_partition_generation = NOT_AUTHORIZED
feature_generation = NOT_AUTHORIZED

RL_model_implementation = NOT_AUTHORIZED

PPO_training = NOT_AUTHORIZED
SAC_training = NOT_AUTHORIZED
RecurrentPPO_training = NOT_AUTHORIZED

RF_training = NOT_AUTHORIZED
XGBoost_training = NOT_AUTHORIZED

backtest_execution = NOT_AUTHORIZED
model_qualification = NOT_AUTHORIZED
model_qualification_execution = NOT_AUTHORIZED

final_holdout_access = NOT_AUTHORIZED

C6_G_INITIAL_REVIEW_EXECUTED = YES
C6_G_INITIAL_REVIEW_DISPOSITION = PASS_WITH_BOUNDED_CORRECTION
C6_G_FINAL_REVIEW_DISPOSITION =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS
C6_G_REVIEW_CLOSURE =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS
C6_H_contract_freeze_execution = NOT_AUTHORIZED

paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED

candidate_set_expansion = NOT_AUTHORIZED
host_or_compute_authorization = NOT_AUTHORIZED
C6_F_SPECIFICATION = COMPLETE__PUBLISHED__EFFECTIVE
C6_H_OR_LATER_EXECUTION = NOT_AUTHORIZED
C7_or_later_execution = NOT_AUTHORIZED

C5_REOPEN = NO
CURRENT_CHECKPOINT_TRACKER = NONE
```

The explicit C6 exclusions are controlled by S1/S2. C6-C timing, C6-D state,
C6-E partition/gate definitions, and C6-F acceptance/review/freeze requirements
authorize no downstream execution. This non-controlling document creates no
authorization.

## 22. Open C6 specification items by later work package

### C6-B — Raw/processed schema, identity, and provenance

`C6_B_DETAIL_DEFINED` — the thirteen C6-B items identified by C6-A are defined
in this draft and routed as follows:

- exact raw-data schema and dtypes — section 4;
- exact processed-data schema and dtypes — section 5;
- required/optional field semantics — sections 4 and 5;
- raw-to-processed transformation lineage — sections 5 and 17;
- stable security/row/time identity fields — sections 5, 6, and 10;
- identifier namespaces and composite keys — section 6;
- duplicate/uniqueness rules — section 6;
- exact ordering keys — section 6;
- schema and dataset-version identity — section 17;
- provenance manifest schema — section 17;
- source/feed/version/as-of/retrieval fields — sections 4 and 17;
- checksums and lineage links — sections 4, 5, 6, and 17; and
- material-provider-change recording and rebuild identity — section 17.

`C6_B_OPEN_ITEMS = NONE_AT_THIS_DRAFT_SPECIFICATION_LEVEL`.
The bounded C6-B specification surface is complete, published, and effective;
it does not mean the overall C6 dataset contract is frozen or that any data has
been generated or accepted.

### C6-C — Chronology, leakage, calendar, and missingness

`C6_C_DETAIL_DEFINED` — the bounded C6-C specification items are defined and
routed as follows:

- PIT/as-of availability representation — sections 8 and 10;
- event-effective-time representation — section 8;
- chronology/no-lookahead checks — sections 6 and 8;
- horizon-overlap/embargo applicability — section 8;
- calendar-version/expected-slot identity — section 7;
- UTC/local-session representation — section 7;
- DST/early-close validation — section 7;
- cross-exchange calendar divergence — section 7;
- missingness/expected-slot classifications — section 9;
- reconstruction-state representation — section 9;
- permitted/prohibited reconstruction — section 9;
- duplicate security × timestamp handling — sections 6 and 9; and
- formation-cutoff/PIT enforcement — sections 8 and 10.

`C6_C_OPEN_ITEMS = NONE_AT_THIS_DRAFT_SPECIFICATION_LEVEL`.

The bounded C6-C chronology, leakage, calendar/session, PIT-availability,
and missingness/reconstruction specification surface is complete, published,
and effective, and is not reopened. This does not mean the full C6 dataset
contract is frozen, a dataset exists, dataset acceptance has occurred, or any
model work is authorized.

### C6-D — RL state, recurrent, action, and economic representation

`C6_D_DETAIL_DEFINED` — the bounded definitions are routed as follows:

- common state fields/order — section 11;
- availability/PIT timing — section 11;
- normalization — section 11;
- slot/state dimension — section 11;
- recurrent sequence/lookback/warm-up — section 12;
- recurrent reset/session/formation boundary — section 12;
- insufficient-history/masking — section 12;
- continuous action domain/scaling — section 13;
- target exposure/transition — section 13;
- decision/rebalance — section 13;
- economic state — section 14;
- execution-price interface — section 14;
- turnover — section 14; and
- spread/slippage/fees/cost — section 14.

`C6_D_OPEN_ITEMS = NONE_AT_THIS_DRAFT_SPECIFICATION_LEVEL`.

The bounded C6-D specification is complete, published, effective, and not
reopened. Required later configuration values and feature-schema identities
remain to be recorded/frozen before applicable use; the interfaces do not
select them. This does not mean C6 is frozen, a dataset or features have been
generated, or a model has been implemented or trained.

### C6-E — Development, validation, holdout, and gate alignment

`C6_E_DETAIL_DEFINED` — bounded definitions are routed as follows:

- top-level chronological regions — section 15;
- walk-forward fold geometry — section 15;
- validation/qualification partition identities — section 15;
- exact split boundaries — section 15;
- step/window geometry — section 15;
- horizon-overlap/purge/embargo — section 15;
- preprocessing fit boundaries — section 15;
- split/version identity — section 15;
- candidate partition comparability — section 15;
- qualification isolation — section 15;
- final-holdout identity/isolation — section 15;
- gate decision interface — section 16;
- gate-feature dataset interface — section 16;
- gate target/outcome — section 16;
- gate horizon — section 16;
- gate feature-availability cutoff — section 16;
- RL action/outcome alignment — section 16;
- paired gated/ungated identity — section 16;
- leakage-safe gate-target construction — sections 15–16; and
- Option B+ routing — section 16.

`C6_E_OPEN_ITEMS = NONE_AT_THIS_DRAFT_SPECIFICATION_LEVEL`.

The bounded C6-E specification is complete, published, effective, and not
reopened. This does not mean C6 is frozen, a dataset exists, partitions or
features have been generated, a model has been implemented or trained,
qualification has been executed, a gate has been trained, or final holdout
has been accessed.

### C6-F — Dataset acceptance and independent review rules

`C6_F_DETAIL_DEFINED` — bounded definitions are routed as follows:

- acceptance disposition model — section 18;
- schema checks — section 18;
- identity/provenance/hash/lineage checks — section 18;
- calendar/session/expected-slot checks — section 18;
- missingness/reconstruction checks — section 18;
- chronology/PIT/leakage checks — section 18;
- historical-universe checks — section 18;
- split/partition checks — section 18;
- RL state/recurrent compatibility checks — section 18;
- gate-interface/target checks — section 18;
- coverage-accounting requirements — section 18;
- acceptance evidence/report identity — section 18;
- material-change/reacceptance rules — section 18;
- C6-G independence — section 19;
- C6-G evidence package — section 19;
- complete review checklist — section 19;
- finding classifications — section 19;
- PASS / PASS_WITH_BOUNDED_CORRECTION / FAIL rules — section 19;
- review evidence identity — section 19;
- freeze eligibility — section 20;
- source-reconciliation freeze treatment — section 20;
- reviewed-to-frozen status transition — section 20;
- freeze identities — section 20;
- freeze evidence package — section 20;
- immutable post-freeze behavior — section 20.

`C6_F_OPEN_ITEMS = NONE_AT_THIS_DRAFT_SPECIFICATION_LEVEL`.

The bounded C6-F specification is COMPLETE__PUBLISHED__EFFECTIVE. The initial
C6-G audit recorded zero material findings and three bounded findings. The
first independent re-verification returned PASS_WITH_BOUNDED_CORRECTION,
closed C6G-FIND-003, and left C6G-FIND-001 and C6G-FIND-002 open at that review.
These immutable historical dispositions do not predict subsequent review
results. Later authoring corrections do not themselves close findings; only
subsequent independent evidence establishes closure and final disposition.
No independent-review result or `c6_independent_review_identity` is created
by this execution actor.
Dataset acceptance has not executed, the source note remains unresolved,
C6-H has not occurred, C6 is not complete, and C7 is not authorized.

### Source reconciliation before freeze

The C6-A brief's separate `50 to 75` acceptable-range wording is not directly
established by the current canonical C5 eligibility decision reviewed.

This is not silently resolved as C6-B through C6-F technical design. Managing
must identify or establish a canonical source before freeze if a separate
75-security upper bound is intended.

## 23. C6 completion criteria

### Accepted completion principles

- `ACCEPTED_REQUIREMENT` [S9]: C6 exists to define raw and processed dataset
  requirements before generation.
- `ACCEPTED_REQUIREMENT` [S9]: the C6 exit gate is frozen dataset contracts
  plus independent audit.
- `ACCEPTED_REQUIREMENT` [S2]: C6 scope includes dataset acceptance-rule
  definition, independent review requirements, and final C6 contract freeze.
- `ACCEPTED_REQUIREMENT` [S1, S2]: dataset generation, dataset-acceptance
  execution, model implementation/training, and final-holdout access remain
  unauthorized during this specification/freeze scope.

C6-A through C6-F are complete, published, and effective and are not reopened.
C6-G initial review recorded three bounded findings and zero material findings.
The first re-verification closed Finding 003 and left Findings 001 and 002 open.
Final review disposition and closure are not asserted by this document;
independent review evidence controls them.
C6-H freeze remains unexecuted and unauthorized. C6 is not complete.

C6 cannot be represented as complete or frozen merely because the earlier
work packages are published/effective and the three bounded corrections
exist.

`C6_F_DETAIL_DEFINED` — sections 18–20 define acceptance/review/freeze evidence
requirements. Actual review, source-reconciliation dispositions, and freeze
evidence must be established in separately authorized later work before C6
completion can be considered.

```text
C6_A_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_B_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_B_REOPEN = NO
C6_B_DETAILS_ADDED = YES
C6_C_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_C_REOPEN = NO
C6_D_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_D_REOPEN = NO
C6_E_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_E_REOPEN = NO
C6_F_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_G_REVIEW_HISTORY = INITIAL_REVIEW_AND_REVERIFICATION_1_RECORDED
C6_G_INITIAL_REVIEW_DISPOSITION = PASS_WITH_BOUNDED_CORRECTION
C6_G_FINAL_REVIEW_DISPOSITION =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS
C6_G_REVIEW_CLOSURE =
NOT_ASSERTED_BY_THIS_DOCUMENT__INDEPENDENT_REVIEW_EVIDENCE_CONTROLS
C6_H_FREEZE_ELIGIBLE = NO
C6_DATASET_CONTRACT = NOT_FROZEN
DATASET_GENERATION = NOT_AUTHORIZED
DATASET_ACCEPTANCE_EXECUTION = NOT_AUTHORIZED
FEATURE_GENERATION = NOT_AUTHORIZED
MODEL_IMPLEMENTATION = NOT_AUTHORIZED
MODEL_TRAINING = NOT_AUTHORIZED
QUALIFICATION_EXECUTION = NOT_AUTHORIZED
FINAL_HOLDOUT_ACCESS = NOT_AUTHORIZED
C6_G_INITIAL_REVIEW_EXECUTED = YES
C6_H_FREEZE_EXECUTED = NO
CURRENT_CHECKPOINT_TRACKER = NONE
```
