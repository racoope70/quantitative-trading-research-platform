# Quantitative Trading Research Platform — Project Context

```text
document_status = ACTIVE_CURRENT_STATE

document_role =
CONTROLLING_SOURCE_OF_TRUTH_FOR_BROAD_CURRENT_LIFECYCLE_STATE
+
AUTHORIZATION_BOUNDARIES
+
CURRENT_NON_AUTHORIZATION_STATE
+
AUTHORITATIVE_POINTERS_TO_MATERIAL_DECISIONS_AND_ACCEPTED_COMPLETION_RECORDS

current_lifecycle_state = C6_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = BOUNDED_DATA_ACCESS_ESTABLISHMENT_AND_ACCEPTANCE_ONLY

working_repository_name = quantitative-trading-research-platform
repository_visibility = PUBLIC
repository_public_release = COMPLETE
project_status = IN_DEVELOPMENT

C5_completion_decision =
docs/decisions/C5_completion_decision.md

C5_completion_decision_id =
GOV-DEC-0012

C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_REOPEN = NO
C5_CURRENT_WORK = NONE

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY

C6_authorization_decision =
docs/decisions/C6_authorization_decision.md

C6_authorization_decision_id =
GOV-DEC-0014

C6_completion_decision =
docs/decisions/C6_completion_decision.md

C6_completion_decision_id =
GOV-DEC-0016

C6_completion_effect = EFFECTIVE
C6_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C6_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C6_REOPEN = NO
C6_CURRENT_WORK = NONE

POST_C6_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_DECISION =
docs/decisions/post_C6_data_access_establishment_authorization_decision.md

POST_C6_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_DECISION_ID =
GOV-DEC-0018

CURRENT_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION =
AUTHORIZED__BOUNDED_ONLY

DATA_ACCESS_AUTHORIZED =
NO__PENDING_ESTABLISHMENT_AND_ACCEPTANCE

GOVERNED_DATA_SOURCE_TARGET =
ALPACA_HISTORICAL_SIP_BARS__EXPLICIT_feed=sip

CURRENT_UNIVERSE_CONTRACT = GOV-DEC-0017
CURRENT_UNIVERSE_CONTRACT_RECORD =
docs/decisions/post_C6_universe_design_supersession_decision.md
EXACT_120_REQUIREMENT = SUPERSEDED
NO_FORCED_N = YES

CURRENT_UNIVERSE_CORRECTIVE_DECISION =
docs/decisions/post_C6_frozen_universe_corrective_blocker_alignment_decision.md

CURRENT_UNIVERSE_CORRECTIVE_DECISION_ID =
GOV-DEC-0019

CORRECTIVE_REMEDIATION_ARCHITECTURE =
ARCHITECTURE_B

CURRENT_FROZEN_UNIVERSE_SCIENTIFIC_STATUS =
BLOCKED__MATERIAL_ELIGIBILITY_CONTRADICTION_PENDING_CORRECTIVE_REMEDIATION

FREEZE_ARTIFACT_EXISTS = YES
FREEZE_SCIENTIFIC_USABILITY = BLOCKED

HISTORICAL_FROZEN_UNIVERSE_COUNT = 30
HISTORICAL_FROZEN_UNIVERSE_SHA256 =
78ec113c5b83ce03477c1529f80c6104819d7f3a70813dec6125fc24cdf8ade7

HISTORICAL_FROZEN_UNIVERSE_SCIENTIFIC_USABILITY =
BLOCKED

HISTORICAL_IDENTICAL_PRIMARY_UNIVERSE_REQUIREMENT_VERIFIED = YES

CURRENT_PRIMARY_UNIVERSE_SCIENTIFIC_STATUS =
NO_SCIENTIFICALLY_USABLE_CURRENT_PRIMARY_UNIVERSE_PENDING_CORRECTIVE_REFREEZE

CURRENT_SCIENTIFICALLY_USABLE_PRIMARY_UNIVERSE =
NO

FULL_ELIGIBILITY_RECERTIFICATION =
COMPLETE__OWNER_ACCEPTED

POSITIVELY_RECERTIFIED_ELIGIBLE_COUNT =
3

DECISIVELY_INELIGIBLE_COUNT =
16

UNRESOLVED_PROVIDER_MISSINGNESS_COUNT =
4

FULL_ELIGIBILITY_RECERTIFICATION_COMPLETION_RECORD =
docs/reports/post_C6_full_eligibility_recertification_completion.md

CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE =
GOV-DEC-0021

CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE_RECORD =
docs/decisions/post_C6_primary_exchange_evidence_architecture_proportionality_supersession_decision.md

PRIMARY_EXCHANGE_EVIDENCE_ACQUISITION =
COMPLETE__PASS

PRIMARY_EXCHANGE_CLASSIFICATION =
COMPLETE__PASS

PRIMARY_EXCHANGE_PASS_COUNT =
23

PRIMARY_EXCHANGE_FAIL_COUNT =
0

PRIMARY_EXCHANGE_UNRESOLVED_COUNT =
0

PRIMARY_EXCHANGE_CLASSIFICATION_COMPLETION_RECORD =
docs/reports/post_C6_primary_exchange_classification_completion.md

PRICE_REVALIDATION =
COMPLETE__19_CLASSIFIED__4_UNRESOLVED_PROVIDER_MISSINGNESS

LIQUIDITY_REVALIDATION =
COMPLETE__19_CLASSIFIED__4_UNRESOLVED_PROVIDER_MISSINGNESS

PROVISIONAL_CORRECTED_SET =
NOT_CONSTRUCTED

HETEROGENEITY_EXECUTION =
NOT_PERFORMED

CORRECTED_REFREEZE =
NOT_PERFORMED

DATASET_GENERATION =
NOT_AUTHORIZED

FINAL_HOLDOUT_ACCESS =
NOT_AUTHORIZED

C7_AUTHORIZATION =
NONE

CORRECTIVE_REMEDIATION_STATUS =
ARCHITECTURE_ACCEPTED__EXECUTION_REQUIRES_SEPARATE_AUTHORIZATION

PROVIDER_ACCESS_EXECUTION =
HELD__UNIVERSE_BLOCKER

MASSIVE_PURCHASE = DEFERRED

dataset_contract_status = FROZEN__EFFECTIVE
dataset_generation_status = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED
C7_authorization = NONE

CURRENT_CHECKPOINT_TRACKER = NONE
```

## 1. Project

Build a canonical, reproducible, leakage-controlled quantitative research and
trading platform supporting:

- bounded PPO, SAC, and RecurrentPPO reinforcement-learning research;
- Random Forest and XGBoost participation-gate ablations;
- fair comparison under common economic, cost, and validation assumptions;
- one shared untouched final holdout under separate future authorization;
- publication-quality research; and
- controlled progression toward paper trading and possible later deployment
  only under separate authorization.

Historical repositories remain evidence and engineering sources, not runtime
dependencies or sources of current authorization.

## 2. Permanent controlling role

`PROJECT_CONTEXT.md` is the controlling source of truth for broad current
lifecycle state, authorization boundaries, current non-authorization state,
and authoritative pointers to material decisions.

It is not:

- a historical phase ledger;
- an active-milestone tracker;
- a next-task or next-permitted-workstream tracker;
- a checkpoint tracker;
- a routine phase-internal progress log; or
- a substitute for detailed decision, roadmap, validation, training, or
  evaluation records.

Git history and repository artifacts establish implementation and historical
evidence. They do not independently create current authorization.

The Milestone Review Reference Map remains a non-authorizing roadmap,
navigation, governance, and evidence reference.

The Future Validation and Training Reference Map remains non-authorizing future
guidance and sequencing reference material.

## 3. Current lifecycle and authorization state

C5 remains completed and effective and is not reopened.

C6 is completed and effective and is not reopened. The dataset contract is
frozen and effective. There is no active major phase or current C6 execution
authorization. C7 is not authorized.

GOV-DEC-0017 is the effective localized semantic supersession of the prior
exact-120 universe requirement. The current primary-universe contract uses all
distinct securities positively certified as eligible at the frozen 2024-09-03
formation under the pre-specified frozen eligibility rules, using only
information available through the completed 2024-08-30 regular session. There
is no forced N, top-N membership truncation, or minimum-security-count gate.

GOV-DEC-0017 itself did not change the certified count. A subsequent accepted
certification review and freeze recorded a 30-security historical freeze
artifact with SHA-256
78ec113c5b83ce03477c1529f80c6104819d7f3a70813dec6125fc24cdf8ade7.
A later accepted eligibility-contradiction audit established that the frozen
30 is not currently scientifically usable as the primary universe.

GOV-DEC-0019 records the Owner-accepted Architecture-B corrective design and
the material current-state blocker. The historical 30-security membership and
freeze manifest remain reproducible evidence, but freeze scientific usability
is blocked. Full eligibility recertification of the exact-23 corrective work
population is complete and Owner-accepted: 3 cases are positively recertified
eligible, 16 are decisively ineligible, and 4 remain unresolved because of
provider missingness. This result does not construct a current primary
universe. A provisional corrected set has not been constructed and a corrected
refreeze has not been performed.

GOV-DEC-0018 remains a valid bounded data-access-establishment authorization
record, but provider-access execution is held behind the universe blocker.
Account authentication, entitlement inspection, and test market-data retrieval
must not proceed while that hold is active. Data access remains pending
establishment and acceptance. No paid provider purchase is authorized. C7,
dataset generation, and all downstream scientific execution remain
unauthorized.

```text
current_lifecycle_state = C6_COMPLETED
active_major_phase = NONE
phase_status = COMPLETED
authorization_effect = BOUNDED_DATA_ACCESS_ESTABLISHMENT_AND_ACCEPTANCE_ONLY

C5_completion_effect = EFFECTIVE
C5_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C5_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION

C5_REOPEN = NO
C5_CURRENT_WORK = NONE

C6_authorization_decision =
docs/decisions/C6_authorization_decision.md

C6_authorization_decision_id =
GOV-DEC-0014

C6_completion_decision =
docs/decisions/C6_completion_decision.md

C6_completion_decision_id =
GOV-DEC-0016

C6_completion_effect = EFFECTIVE
C6_LIFECYCLE_CLOSURE = COMPLETE__EFFECTIVE
CURRENT_C6_EXECUTION_AUTHORIZATION = NONE_AFTER_COMPLETION
C6_REOPEN = NO
C6_CURRENT_WORK = NONE

CURRENT_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION =
AUTHORIZED__BOUNDED_ONLY

DATA_ACCESS_AUTHORIZED =
NO__PENDING_ESTABLISHMENT_AND_ACCEPTANCE

GOVERNED_DATA_SOURCE_TARGET =
ALPACA_HISTORICAL_SIP_BARS__EXPLICIT_feed=sip

CURRENT_UNIVERSE_CORRECTIVE_DECISION =
docs/decisions/post_C6_frozen_universe_corrective_blocker_alignment_decision.md

CURRENT_UNIVERSE_CORRECTIVE_DECISION_ID =
GOV-DEC-0019

CORRECTIVE_REMEDIATION_ARCHITECTURE =
ARCHITECTURE_B

CURRENT_FROZEN_UNIVERSE_SCIENTIFIC_STATUS =
BLOCKED__MATERIAL_ELIGIBILITY_CONTRADICTION_PENDING_CORRECTIVE_REMEDIATION

FREEZE_ARTIFACT_EXISTS = YES
FREEZE_SCIENTIFIC_USABILITY = BLOCKED

HISTORICAL_FROZEN_UNIVERSE_COUNT = 30
HISTORICAL_FROZEN_UNIVERSE_SHA256 =
78ec113c5b83ce03477c1529f80c6104819d7f3a70813dec6125fc24cdf8ade7

HISTORICAL_FROZEN_UNIVERSE_SCIENTIFIC_USABILITY =
BLOCKED

CURRENT_PRIMARY_UNIVERSE_SCIENTIFIC_STATUS =
NO_SCIENTIFICALLY_USABLE_CURRENT_PRIMARY_UNIVERSE_PENDING_CORRECTIVE_REFREEZE

CURRENT_SCIENTIFICALLY_USABLE_PRIMARY_UNIVERSE =
NO

FULL_ELIGIBILITY_RECERTIFICATION =
COMPLETE__OWNER_ACCEPTED

POSITIVELY_RECERTIFIED_ELIGIBLE_COUNT =
3

DECISIVELY_INELIGIBLE_COUNT =
16

UNRESOLVED_PROVIDER_MISSINGNESS_COUNT =
4

FULL_ELIGIBILITY_RECERTIFICATION_COMPLETION_RECORD =
docs/reports/post_C6_full_eligibility_recertification_completion.md

CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE =
GOV-DEC-0021

CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE_RECORD =
docs/decisions/post_C6_primary_exchange_evidence_architecture_proportionality_supersession_decision.md

PRIMARY_EXCHANGE_EVIDENCE_ACQUISITION =
COMPLETE__PASS

PRIMARY_EXCHANGE_CLASSIFICATION =
COMPLETE__PASS

PRIMARY_EXCHANGE_PASS_COUNT =
23

PRIMARY_EXCHANGE_FAIL_COUNT =
0

PRIMARY_EXCHANGE_UNRESOLVED_COUNT =
0

PRIMARY_EXCHANGE_CLASSIFICATION_COMPLETION_RECORD =
docs/reports/post_C6_primary_exchange_classification_completion.md

PRICE_REVALIDATION =
COMPLETE__19_CLASSIFIED__4_UNRESOLVED_PROVIDER_MISSINGNESS

LIQUIDITY_REVALIDATION =
COMPLETE__19_CLASSIFIED__4_UNRESOLVED_PROVIDER_MISSINGNESS

PROVISIONAL_CORRECTED_SET =
NOT_CONSTRUCTED

HETEROGENEITY_EXECUTION =
NOT_PERFORMED

CORRECTED_REFREEZE =
NOT_PERFORMED

DATASET_GENERATION =
NOT_AUTHORIZED

FINAL_HOLDOUT_ACCESS =
NOT_AUTHORIZED

C7_AUTHORIZATION =
NONE

CORRECTIVE_REMEDIATION_STATUS =
ARCHITECTURE_ACCEPTED__EXECUTION_REQUIRES_SEPARATE_AUTHORIZATION

PROVIDER_ACCESS_EXECUTION =
HELD__UNIVERSE_BLOCKER

dataset_contract_status = FROZEN__EFFECTIVE
dataset_generation_status = NOT_AUTHORIZED
current_model_candidate = NONE
current_deployment_candidate = NONE
final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED
C7_authorization = NONE
CURRENT_CHECKPOINT_TRACKER = NONE
```

## 4. Authoritative material-decision pointers

C5 completion and closure are recorded in:

```text
C5_completion_decision =
docs/decisions/C5_completion_decision.md

C5_completion_decision_id =
GOV-DEC-0012
```

The accepted post-C5 / pre-C6 scientific direction is recorded in:

```text
POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION =
docs/decisions/post_C5_pre_C6_RL_research_design_decision.md

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_DECISION_ID =
GOV-DEC-0013

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT =
OWNER_ACCEPTED_WITH_REFINEMENTS

POST_C5_PRE_C6_RL_DESIGN_ALIGNMENT_EFFECT =
SCIENTIFIC_DIRECTION_ONLY
```

GOV-DEC-0013 is the detailed scientific-design record. This document does not
duplicate its detailed candidate-routing, gating, readiness, phase-sequencing,
or future evaluation methodology.

The historical Owner-authorized bounded C6 scope is recorded in:

```text
C6_authorization_decision =
docs/decisions/C6_authorization_decision.md

C6_authorization_decision_id =
GOV-DEC-0014
```

GOV-DEC-0014 is historical authorization evidence for bounded C6
dataset-contract specification, independent review, and freeze.
`PROJECT_CONTEXT.md` remains the controlling broad lifecycle and authorization
source.

GOV-DEC-0016 records Owner-accepted C6 completion and closure:

```text
C6_completion_decision =
docs/decisions/C6_completion_decision.md
C6_completion_decision_id =
GOV-DEC-0016
```

The frozen contract and freeze manifest remain immutable technical evidence.
The completion decision does not authorize C7; GOV-DEC-0014 is no longer
current execution authorization.

The current post-C6 universe-design supersession is recorded in:

```text
CURRENT_UNIVERSE_CONTRACT =
GOV-DEC-0017

CURRENT_UNIVERSE_CONTRACT_RECORD =
docs/decisions/post_C6_universe_design_supersession_decision.md
```

GOV-DEC-0017 supersedes the fixed exact-120 membership requirement without
reopening C6 or rewriting the frozen C6 dataset contract. It does not freeze
the actual primary universe and does not authorize C7.

The current corrective frozen-universe blocker alignment is recorded in:

```text
CURRENT_UNIVERSE_CORRECTIVE_DECISION =
docs/decisions/post_C6_frozen_universe_corrective_blocker_alignment_decision.md

CURRENT_UNIVERSE_CORRECTIVE_DECISION_ID =
GOV-DEC-0019
```

GOV-DEC-0019 accepts Architecture B, preserves the defective 30-security freeze
as historical evidence, blocks its current scientific use, and records the
broad corrective boundary. It does not authorize eligibility recertification,
external evidence acquisition, universe mutation, heterogeneity execution,
expansion, corrected refreeze, or C7.

The current primary-exchange evidence architecture and accepted exact-23
classification are recorded in:

```text
CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE =
GOV-DEC-0021

CURRENT_PRIMARY_EXCHANGE_EVIDENCE_ARCHITECTURE_RECORD =
docs/decisions/post_C6_primary_exchange_evidence_architecture_proportionality_supersession_decision.md

PRIMARY_EXCHANGE_CLASSIFICATION_COMPLETION_RECORD =
docs/reports/post_C6_primary_exchange_classification_completion.md
```

GOV-DEC-0021 controls the current primary-exchange evidence architecture.
The completion report records the Managing-accepted 23 PASS / 0 FAIL /
0 UNRESOLVED classification result but is not a current-state controller and
does not itself authorize downstream scientific execution.

The current bounded post-C6 data-access establishment authorization is
recorded in:

POST_C6_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_DECISION =
docs/decisions/post_C6_data_access_establishment_authorization_decision.md

POST_C6_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION_DECISION_ID =
GOV-DEC-0018

GOV-DEC-0018 remains the bounded data-access establishment and acceptance
authorization record, but its execution is operationally held behind the
frozen-universe blocker recorded by GOV-DEC-0019. It does not itself establish
or accept data access, authorize a paid provider purchase, authorize C7, or
authorize downstream scientific execution.

## 5. High-level prospective research direction

The accepted prospective research direction is bounded RL research using PPO,
SAC, and RecurrentPPO, with PPO retained as the mandatory primary baseline.

Random Forest and XGBoost are future participation-gate ablations around
eligible RL foundations.

The final comparison architecture preserves one shared untouched final holdout.
Final-holdout access remains separately governed and is not currently
authorized.

No statement in this section means that a current model candidate exists or
that implementation, training, qualification, gating, backtesting, or final
evaluation is authorized.

## 6. Current dataset, model, and execution boundary

```text
CURRENT_DATA_ACCESS_ESTABLISHMENT_AUTHORIZATION =
AUTHORIZED__BOUNDED_ONLY

DATA_ACCESS_AUTHORIZED =
NO__PENDING_ESTABLISHMENT_AND_ACCEPTANCE

PROVIDER_ACCESS_EXECUTION =
HELD__UNIVERSE_BLOCKER

GOVERNED_DATA_SOURCE_TARGET =
ALPACA_HISTORICAL_SIP_BARS__EXPLICIT_feed=sip

dataset_contract_status = FROZEN__EFFECTIVE
dataset_generation_status = NOT_AUTHORIZED

current_model_candidate = NONE
current_deployment_candidate = NONE

final_holdout_access = NOT_AUTHORIZED
paper_trading = NOT_AUTHORIZED
live_trading = NOT_AUTHORIZED
deployment = NOT_AUTHORIZED
C7_authorization = NONE
```

C6 contract specification, independent review, and freeze are complete.
GOV-DEC-0018 remains the bounded post-C6 data-access establishment and
acceptance authorization record, but provider-access execution is held by the
current frozen-universe scientific blocker recorded in GOV-DEC-0019. C7
remains unauthorized.

While the hold is active, provider/account authentication, entitlement
inspection, and test market-data retrieval must not proceed. No paid provider
purchase is authorized. Dataset generation, dataset acceptance execution,
feature generation, model implementation, model training, gate training,
backtesting, final-holdout access, paper trading, live trading, and deployment
remain unauthorized.

## 7. Navigation

Use:

- `PROJECT_CONTEXT.md` for broad current lifecycle and authorization state;
- `docs/decisions/C5_completion_decision.md` for C5 completion and closure;
- `docs/decisions/post_C5_pre_C6_RL_research_design_decision.md` for the
  accepted prospective RL/gating scientific design;
- `docs/decisions/C6_completion_decision.md` for the authoritative supporting
  record of C6 completion and closure;
- `docs/decisions/C6_authorization_decision.md` for the historical record of
  the Owner-authorized bounded C6 dataset-contract specification, review, and
  freeze scope;
- `docs/decisions/post_C6_frozen_universe_corrective_blocker_alignment_decision.md`
  for the Owner-accepted Architecture-B corrective blocker decision and
  current frozen-universe scientific-usability boundary;
- `docs/decisions/post_C6_primary_exchange_evidence_architecture_proportionality_supersession_decision.md`
  for the current GOV-DEC-0021 primary-exchange evidence architecture;
- `docs/reports/post_C6_primary_exchange_classification_completion.md`
  for the Managing-accepted exact-23 primary-exchange classification completion
  record;
- `docs/decisions/post_C6_data_access_establishment_authorization_decision.md`
  for the bounded Owner-authorized data-access establishment and acceptance
  scope that remains operationally held behind the universe blocker;
- `docs/workflows/milestone_review_reference_map.md` for non-authorizing
  roadmap, governance, evidence, and historical navigation;
- `docs/workflows/future_validation_training_reference_map.md` for
  non-authorizing future validation, training, evaluation, and holdout
  guidance; and
- Git history and the working tree for implementation evidence.

Files, plans, and reference maps do not independently authorize execution.
