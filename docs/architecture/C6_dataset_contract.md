# C6 Dataset Contract

```text
document_status = C6_B_DRAFT__NOT_FROZEN
document_role = C6_DATASET_CONTRACT__C6_A_INPUTS_PLUS_C6_B_SCHEMA_IDENTITY_PROVENANCE
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

dataset_contract_status = AUTHORIZED__NOT_FROZEN
dataset_generation_status = NOT_AUTHORIZED

ACCEPTED_REQUIREMENT =
REQUIREMENT_ALREADY_ESTABLISHED_BY_CANONICAL_DECISION_OR_ACCEPTED_GUIDANCE

C6_B_DETAIL_DEFINED =
TECHNICAL_DETAIL_DEFINED_WITHIN_AUTHORIZED_C6_B_SCOPE__PENDING_MANAGING_REVIEW

C6_DETAIL_TO_BE_DEFINED =
TECHNICAL_CONTRACT_DETAIL_INTENTIONALLY_DEFERRED_TO_A_LATER_C6_WORK_PACKAGE

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Document role and governance status

This document contains the published C6-A dataset-contract skeleton and
accepted-input inventory plus the bounded C6-B technical definitions for raw
and processed schemas, identity, lineage, provenance, and reproducibility.

It remains a draft C6 dataset contract and is not frozen.

`PROJECT_CONTEXT.md` remains the controlling source of truth for broad current
lifecycle state and authorization boundaries.

`docs/decisions/C6_authorization_decision.md` is supporting authorization
evidence for the already-effective bounded C6 scope.

This document creates no new authorization and is not a checkpoint tracker,
execution log, dataset-acceptance record, model specification, training plan,
or final-holdout approval.

Requirements and technical specifications in this document use three states:

- `ACCEPTED_REQUIREMENT` — already established by canonical decisions or
  accepted methodological guidance.
- `C6_B_DETAIL_DEFINED` — a technical schema, identity, lineage, provenance,
  or reproducibility detail defined within the bounded C6-B authority and
  presented for Managing review.
- `C6_DETAIL_TO_BE_DEFINED` — a technical C6 contract detail assigned to a
  later work package and intentionally not resolved by C6-B.

A third notation is used only where source reconciliation is required:

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

C6-A organized accepted requirements and identified unresolved specification
work. C6-B now resolves only the raw/processed schema, identity, lineage,
provenance, reproducibility, and material-source-change details explicitly
assigned to C6-B. C6-C through C6-F details remain deferred.

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
C6_C_CHRONOLOGY_RULES = DEFERRED
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

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define the exact time-order validation
rules that operate on these identities.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define the exact calendar-version
identity, calendar fields, expected-slot representation, DST conversion
contract, early-close metadata, local-session-date fields, UTC serialization,
and conflict-validation rules.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define the exact as-of/availability
fields, event-effective-time representation, chronological integrity checks,
lookahead rejection rules, horizon-overlap treatment, and conditions under
which an embargo is required.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define field-level and row-level
missingness codes, expected-slot classifications, reconstruction states,
permitted versus prohibited reconstruction operations, unresolved-gap
representation, and exact fail-closed handling.

C6-A does not choose an imputation or reconstruction algorithm.

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

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define the exact formation-cutoff and
PIT evidence-availability encoding.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-D must define the exact common observation/state
fields, ordering, data availability at decision time, normalization interface,
history dependencies, state dimensions, and model-neutral representation.

C6-A does not choose an observation vector or model architecture.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-D must define exact sequence length, lookback,
warm-up length, reset/boundary semantics, cross-session rules, padding/masking
rules if any, and the model-neutral sequence tensor/interface contract.

No recurrent hyperparameter is selected in C6-A.

## 13. Continuous target-position/exposure action representation

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S3]: the common action formulation is
  `CONTINUOUS_TARGET_POSITION_OR_EXPOSURE`.
- `ACCEPTED_REQUIREMENT` [S3]: the common formulation applies prospectively to
  the bounded PPO/SAC/RecurrentPPO comparison and does not imply any model has
  been implemented, trained, qualified, or authorized for execution.

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-D must define the exact action domain, scaling,
position/exposure units, action-to-position transition representation,
decision timing, rebalance semantics, and any model-neutral constraints.

C6-A does not choose leverage, long/short bounds, position limits, or
rebalancing parameters.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-D must define the exact execution-price input,
turnover representation, spread input, slippage input, transaction-cost input,
position-sizing/economic fields, and the frozen interface through which later
models and evaluations consume them.

C6-A does not invent spread, slippage, fee, market-impact, latency, or other
cost-model parameter values.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-E must define exact development, walk-forward
validation, qualification, and final-holdout partition identities and date
boundaries; fold geometry; step sizes; horizon/embargo treatment; split
versioning; and deterministic partition-generation rules.

No final experiment is defined or executed in C6-A.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-E must define the exact gate-feature dataset
interface, target/outcome definition, prediction horizon, feature-availability
cutoff, RL-action/outcome alignment, paired gated/ungated dataset identity,
and leakage checks.

C6-A does not define gate features, labels, thresholds, or train a gate.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-F must define exact dataset acceptance checks,
thresholds, pass/fail/unresolved dispositions, evidence package, fail-closed
conditions, and acceptance-report requirements.

C6-A performs no dataset acceptance.

## 19. Independent C6 review requirements

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S2]: independent C6 review requirements are part of
  the authorized C6 contract-freeze scope.
- `ACCEPTED_REQUIREMENT` [S9]: the C6 exit gate requires dataset contracts to
  be frozen and independently audited.

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-F must define the exact independent-review
scope, evidence package, review checklist, material-finding treatment,
correction boundary, and PASS/FAIL disposition requirements.

C6-A does not perform the independent C6 review.

## 20. Contract-freeze requirements

### Accepted requirements

- `ACCEPTED_REQUIREMENT` [S1, S2]: C6 is authorized for specification,
  independent review, and final contract freeze only.
- `ACCEPTED_REQUIREMENT` [S1]: current dataset-contract status is
  `AUTHORIZED__NOT_FROZEN`.
- `ACCEPTED_REQUIREMENT` [S2, S9]: final C6 contract freeze is required before
  later governed dataset generation/acceptance may proceed.

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-F must define the freeze artifact identity,
version/checksum requirements, evidence of review acceptance, immutable
post-freeze representation, and exact completion-signoff package.

C6-A does not freeze this document.

## 21. Explicit exclusions / non-authorization boundary

C6 remains specification/freeze work only; C6-B is schema, identity, lineage, and provenance specification only.

The following remain prohibited:

```text
data_purchase = NOT_AUTHORIZED
provider_purchase = NOT_AUTHORIZED
provider_account_activity = NOT_AUTHORIZED
network_or_API_data_acquisition = NOT_AUTHORIZED
data_download = NOT_AUTHORIZED

dataset_generation = NOT_AUTHORIZED
dataset_acceptance_execution = NOT_AUTHORIZED
feature_generation = NOT_AUTHORIZED_BY_C6_B

RL_model_implementation = NOT_AUTHORIZED

PPO_training = NOT_AUTHORIZED
SAC_training = NOT_AUTHORIZED
RecurrentPPO_training = NOT_AUTHORIZED

RF_training = NOT_AUTHORIZED
XGBoost_training = NOT_AUTHORIZED

backtest_execution = NOT_AUTHORIZED
model_qualification = NOT_AUTHORIZED

final_holdout_access = NOT_AUTHORIZED

paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED

candidate_set_expansion = NOT_AUTHORIZED
host_or_compute_authorization = NOT_AUTHORIZED
C7_or_later_execution = NOT_AUTHORIZED

C5_REOPEN = NO
CURRENT_CHECKPOINT_TRACKER = NONE
```

The explicit C6 exclusions are controlled by S1/S2. The additional
`feature_generation = NOT_AUTHORIZED_BY_C6_B` line records the narrower C6-B
schema/identity/provenance task boundary and creates no broader C6 rule.

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
This means the bounded C6-B specification surface is defined for Managing
review; it does not mean the overall C6 dataset contract is frozen or that any
data has been generated or accepted.

### C6-C — Chronology, leakage, calendar, and missingness

`C6_DETAIL_TO_BE_DEFINED`:

- exact PIT/as-of availability representation;
- event-effective-time representation;
- chronology and no-lookahead checks;
- horizon-overlap and embargo applicability;
- calendar-version and expected-slot identity;
- UTC/local-session field contract;
- DST and early-close validation;
- cross-exchange calendar divergence handling;
- missingness codes and expected-slot classifications;
- reconstruction-state representation; and
- permitted/prohibited reconstruction rules.

### C6-D — RL state, recurrent, action, and economic representation

`C6_DETAIL_TO_BE_DEFINED`:

- exact common observation/state fields;
- availability timing of state inputs;
- model-neutral normalization interface;
- recurrent sequence and lookback length;
- recurrent warm-up and reset/boundary rules;
- common continuous action domain/scaling;
- target-position/exposure units and transition representation;
- execution-price inputs;
- turnover representation;
- spread/slippage/cost inputs; and
- exact economic-interface parameters.

### C6-E — Development, validation, holdout, and gate alignment

`C6_DETAIL_TO_BE_DEFINED`:

- exact chronological development partitions;
- walk-forward fold geometry;
- validation and qualification partition identities;
- split date boundaries and version identity;
- horizon/embargo treatment;
- final-holdout partition identity and isolation controls;
- gate-feature dataset interface;
- gate-target/outcome definition;
- gate feature/target time alignment;
- paired gated/ungated dataset comparability; and
- leakage-safe gate-target construction checks.

### C6-F — Dataset acceptance and independent review rules

`C6_DETAIL_TO_BE_DEFINED`:

- exact dataset-acceptance checks and thresholds;
- PASS/FAIL/UNRESOLVED dispositions;
- acceptance evidence package;
- independent-review checklist and evidence;
- material-finding/correction rules;
- freeze artifact version/checksum;
- freeze acceptance evidence; and
- final C6 contract-freeze/completion signoff requirements.

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

C6-A is complete, published, and effective. C6-B adds bounded technical
definitions for Managing review. Neither C6-A completion nor this C6-B draft
equals C6 completion.

C6 cannot be represented as complete or frozen merely because the skeleton and
C6-B definitions exist.

`C6_DETAIL_TO_BE_DEFINED` — the exact acceptance/review/freeze evidence package
must be resolved in the later authorized C6 work before C6 completion can be
considered.

```text
C6_A_STATUS = COMPLETE__PUBLISHED__EFFECTIVE
C6_B_DOCUMENT_STATUS = DRAFT_FOR_MANAGING_REVIEW
C6_B_DETAILS_ADDED = YES
C6_DATASET_CONTRACT = NOT_FROZEN
DATASET_GENERATION = NOT_AUTHORIZED
FINAL_HOLDOUT_ACCESS = NOT_AUTHORIZED
CURRENT_CHECKPOINT_TRACKER = NONE
```
