# C1 Authorization Decision

```text
document_status = OWNER_ACCEPTED_PENDING_REPOSITORY_ALIGNMENT
decision_id = GOV-DEC-0003
decision_type = C1_PHASE_AUTHORIZATION
decision_status = ACCEPTED_IN_CHAT_PENDING_REPOSITORY_ALIGNMENT
owner_acceptance_status = ACCEPTED_IN_CHAT
owner_decision = AUTHORIZE_C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
authorized_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
authorized_scope = C1_DOCUMENTATION_AND_READ_ONLY_REPOSITORY_INSPECTION_ONLY
authorization_effect = NONE_PENDING_CONTROLLING_STATE_ALIGNMENT
C1_activation_effect = NONE_PENDING_CONTROLLING_STATE_ALIGNMENT
C2_authorization_effect = NONE
proposed_curated_record = 2v.GOV.04
```

## 1. Purpose

This decision records the owner’s explicit authorization in chat for the
C1 Legacy Evidence Classification and Architecture Migration Design phase.

The owner selected:

```text
AUTHORIZE_C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
```

This record does not become effective repository authorization until it is
reviewed, merged, and followed by a separate controlling-state alignment in
`PROJECT_CONTEXT.md`.

## 2. Entry-gate evidence

```text
repository = racoope70/quantitative-trading-research-platform
repository_visibility = PRIVATE
C0_status = COMPLETED
C0_completion_record = docs/decisions/C0_completion_decision.md
C0_completion_decision_id = GOV-DEC-0002
C0_curated_completion_record = 2v.GOV.03
C0_completion_alignment_merge_commit = 7fb85b8446cfecd7d26361e9ea9f6a98daaafc58
C0_completion_alignment_push_workflow_run = 11
C0_completion_alignment_push_workflow_conclusion = SUCCESS
C1_entry_gate_C0_completed = SATISFIED
C1_entry_gate_owner_authorization = ACCEPTED_IN_CHAT
repository_recording_status = PENDING
```

The C0 completion and workflow evidence establishes that C0 is closed. The
owner’s explicit chat decision establishes the intended C1 authorization,
subject to repository recording and controlling-state alignment.

## 3. Authorized C1 purpose

C1 may review the bounded historical sections and material legacy evidence
to recommend:

- Evidence that should be carried forward, summarized, archived, or treated
  as obsolete or superseded.
- Durable controls and lessons that should govern the canonical platform.
- Canonical architecture and responsibility boundaries.
- Technical assets that may later be copied, reimplemented, adapted,
  referenced, retained historically, excluded, or deferred.
- The appropriate future phase for each accepted recommendation.

C1 is an evidence-classification and architecture-design phase. It is not an
implementation, migration, environment, data, model, or trading phase.

## 4. Authorized repositories and inspection mode

C1 authorizes read-only inspection of:

```text
racoope70/exploratory-daytrading
racoope70/quant-trading-model-validation
racoope70/ppo-trading-pipeline
racoope70/quantitative-trading-research-platform
```

Permitted inspection includes read-only review of material:

- Files and repository structure.
- Commits and immutable commit references.
- Pull requests and review records.
- Decisions, audits, runs, reports, and workflow evidence.
- Historical 2v entries and ranges.
- Source and test assets only to understand historical purpose, limitations,
  architecture, and potential future migration treatment.

Historical repositories remain evidence and engineering sources. They do
not become runtime dependencies or sources of current authorization.

## 5. Bounded review scope

C1 must cover all fifteen sections in:

```text
C1_BOUNDED_HISTORICAL_SECTION_INVENTORY
```

as defined in:

```text
docs/workflows/milestone_review_reference_map.md
```

For each bounded section, C1 must:

1. Identify the exact historical 2v entry or range.
2. Determine materiality.
3. Review decisive and materially supporting evidence.
4. Identify superseding corrections.
5. Separate durable controls from one-time procedures.
6. Classify retained evidence.
7. Determine consolidation targets and future-phase relevance.
8. Propose curated canonical 2v references.
9. Record technical migration recommendations separately.

The existence of an additional file, audit, review, commit, run, or 2v
entry does not independently expand the bounded section inventory.

Any proposed new historical section requires a documented material
distinction and separate owner acceptance of the scope amendment.

## 6. Required evidence classifications

Material historical evidence must receive one of:

```text
CARRY_FORWARD
SUMMARIZE_AND_REFERENCE
HISTORICAL_ARCHIVE_ONLY
OBSOLETE_OR_SUPERSEDED
```

Review depth must be proportional to materiality. C1 does not require
exhaustive classification of every minor or duplicative administrative file.

No historical result, model, dataset, module, audit conclusion, provider
decision, or deployment claim is automatically accepted.

## 7. Required C1 outputs

C1 is limited to the following three principal completed outputs:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

The accepted C1 templates control their required schemas and content.

The retention matrix records evidence classification and future relevance.

The technical migration manifest records recommendations only. It does not
execute migration.

The C1 report consolidates the material historical conclusions,
architecture recommendation, retained controls, unresolved risks, and
recommended disposition for C2.

Supporting governance records may include focused authorization, review,
audit, correction, and completion records required to govern C1 itself.
They must not create a parallel documentation system.

## 8. Permitted C1 activities

C1 may include:

- Read-only historical and canonical repository inspection.
- Documentation-only evidence analysis.
- Preparation and revision of the three C1 outputs.
- Documentation-only consistency checks for the C1 outputs.
- Owner review and correction of material C1 documentation findings.
- One risk-proportional independent C1 audit.
- Preparation of the C1 completion decision.
- Recording the accepted C1 disposition and proposed next phase.

## 9. Prohibited scope

C1 does not authorize:

- Editing any historical repository.
- Executable legacy-code migration or adaptation.
- Executing historical or canonical source code.
- Running tests, notebooks, scripts, training, validation, or backtests.
- Dependency installation or Python-environment creation.
- Provider selection or acceptance.
- Credentials, authenticated access, network/API testing, or market-data
  requests.
- Dataset generation, reconstruction, download, modification, imputation,
  or acceptance.
- Model implementation, training, retraining, validation, qualification,
  promotion, artifact creation, or final-holdout access.
- Broker-account access, paper orders, live orders, or trading activity.
- Final ticker-universe selection.
- Profitability, deployment-readiness, publication, or live-capital claims.
- C2 or any later-phase work.
- Automatic acceptance of any historical asset or conclusion.

## 10. Current effect before controlling-state alignment

```text
current_lifecycle_state_remains = C0_COMPLETED
active_major_phase_remains = NONE
C1_authorization_status_remains = NOT_AUTHORIZED
C1_phase_status_remains = NOT_STARTED
authorization_effect = NONE_PENDING_CONTROLLING_STATE_ALIGNMENT
```

Merging this decision record alone does not activate C1.

A separate reviewed controlling-state alignment must update
`PROJECT_CONTEXT.md` before C1 work begins.

## 11. Intended effect after later accepted alignment

The later controlling-state alignment may record:

```text
current_lifecycle_state = C1_ACTIVE
active_major_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
phase_status = ACTIVE
authorization_effect = C1_SCOPE_ONLY
C1_authorization_status = AUTHORIZED
C1_phase_status = ACTIVE
```

That alignment may register this decision as `2v.GOV.04`.

No C2 authorization follows from C1 activation.

## 12. C1 completion conditions

C1 may close only when:

1. Every bounded historical section has been reviewed proportionally.
2. Exact applicable legacy 2v entries or ranges have been identified.
3. The evidence-retention matrix is complete and accepted.
4. Durable controls, limitations, and superseding corrections are recorded.
5. The technical migration manifest is complete and accepted.
6. The C1 evidence and architecture report is complete and accepted.
7. No executable migration or other prohibited technical activity occurred.
8. A risk-proportional independent C1 audit passes after correction of any
   material findings.
9. The owner accepts the C1 completion decision.

## 13. Permitted next step

The next permitted step after this file is committed is a focused pull
request to review and record this C1 authorization decision.

Until that pull request and the later controlling-state alignment are
merged, C1 remains unauthorized and must not begin.
