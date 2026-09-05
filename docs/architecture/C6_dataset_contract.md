# C6 Dataset Contract

```text
document_status = C6_A_DRAFT__NOT_FROZEN
document_role = C6_DATASET_CONTRACT_SKELETON_AND_ACCEPTED_INPUT_INVENTORY
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

dataset_contract_status = AUTHORIZED__NOT_FROZEN
dataset_generation_status = NOT_AUTHORIZED

ACCEPTED_REQUIREMENT =
REQUIREMENT_ALREADY_ESTABLISHED_BY_CANONICAL_DECISION_OR_ACCEPTED_GUIDANCE

C6_DETAIL_TO_BE_DEFINED =
TECHNICAL_CONTRACT_DETAIL_INTENTIONALLY_DEFERRED_TO_A_LATER_C6_WORK_PACKAGE

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Document role and governance status

This document is the initial C6 dataset-contract skeleton and accepted-input
inventory.

It is not the frozen C6 dataset contract.

`PROJECT_CONTEXT.md` remains the controlling source of truth for broad current
lifecycle state and authorization boundaries.

`docs/decisions/C6_authorization_decision.md` is supporting authorization
evidence for the already-effective bounded C6 scope.

This document creates no new authorization and is not a checkpoint tracker,
execution log, dataset-acceptance record, model specification, training plan,
or final-holdout approval.

Requirements in this document use two states:

- `ACCEPTED_REQUIREMENT` — already established by canonical decisions or
  accepted methodological guidance.
- `C6_DETAIL_TO_BE_DEFINED` — a later technical C6 contract detail that has
  not been decided in C6-A.

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

C6-A organizes accepted requirements and identifies unresolved specification
work. It does not resolve later C6-B through C6-F details merely because a
technical choice appears useful.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-B must define the exact raw-data tables/files,
field names, dtypes, requiredness, key columns, schema versions, source-field
mapping, immutable raw identity, and raw-contract validation representation.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-B must define the exact processed schema,
column names, dtypes, transformation lineage, adjustment representation,
derived-row identity, and raw-to-processed mapping.

Feature generation is not performed or specified as executable behavior in
C6-A.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-B must define canonical identifier namespaces,
composite keys, row identity, uniqueness constraints, deterministic sort keys,
version identity, and duplicate-rejection rules.

`C6_DETAIL_TO_BE_DEFINED` — C6-C must define the exact time-order validation
rules that operate on those identities.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-B must define the exact persisted membership,
eligibility-result, ranking, evidence-reference, and stable-identity fields.

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

### Deferred detail

`C6_DETAIL_TO_BE_DEFINED` — C6-B must define the exact provenance manifest,
schema version, source-version identity, checksums, retrieval/as-of fields,
adapter identity, raw/processed lineage links, and material-provider-change
recording contract.

No provider purchase, account activity, entitlement, authentication, network
access, or acquisition occurs in C6-A.

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

C6-A is specification/inventory work only.

The following remain prohibited:

```text
data_purchase = NOT_AUTHORIZED
provider_purchase = NOT_AUTHORIZED
provider_account_activity = NOT_AUTHORIZED
network_or_API_data_acquisition = NOT_AUTHORIZED
data_download = NOT_AUTHORIZED

dataset_generation = NOT_AUTHORIZED
dataset_acceptance_execution = NOT_AUTHORIZED
feature_generation = NOT_AUTHORIZED_BY_C6_A

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
`feature_generation = NOT_AUTHORIZED_BY_C6_A` line records the narrower C6-A
organization/inventory task boundary and creates no broader C6 rule.

## 22. Open C6 specification items by later work package

### C6-B — Raw/processed schema, identity, and provenance

`C6_DETAIL_TO_BE_DEFINED`:

- exact raw-data schema and dtypes;
- exact processed-data schema and dtypes;
- required/optional field semantics;
- raw-to-processed transformation lineage;
- stable security/row/time identity fields;
- identifier namespaces and composite keys;
- duplicate/uniqueness rules;
- exact ordering keys;
- schema and dataset-version identity;
- provenance manifest schema;
- source/feed/version/as-of/retrieval fields;
- checksums and lineage links; and
- material-provider-change recording and rebuild identity.

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

C6-A completion does not equal C6 completion.

C6 cannot be represented as complete or frozen merely because this skeleton
exists.

`C6_DETAIL_TO_BE_DEFINED` — the exact acceptance/review/freeze evidence package
must be resolved in the later authorized C6 work before C6 completion can be
considered.

```text
C6_A_DOCUMENT_STATUS = DRAFT_FOR_MANAGING_REVIEW
C6_DATASET_CONTRACT = NOT_FROZEN
DATASET_GENERATION = NOT_AUTHORIZED
FINAL_HOLDOUT_ACCESS = NOT_AUTHORIZED
CURRENT_CHECKPOINT_TRACKER = NONE
```
