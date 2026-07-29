# C1 Authorization Decision

```text
document_status = ACCEPTED_C1_AUTHORIZATION_DECISION
decision_id = GOV-DEC-0003
decision_type = C1_PHASE_AUTHORIZATION
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED
owner_decision = AUTHORIZE_C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
authorized_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
authorized_scope = C1_DOCUMENTATION_AND_READ_ONLY_REPOSITORY_INSPECTION_ONLY
authorization_effect = C1_SCOPE_ONLY
C1_activation_effect = EFFECTIVE
C2_authorization_effect = NONE
curated_record = 2v.GOV.04
repository_recording_status = RECORDED_AND_ALIGNED
```

## 1. Purpose

This decision records the owner’s accepted authorization for the C1 Legacy Evidence Classification and Architecture Migration Design phase.

The owner selected:

```text
AUTHORIZE_C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
```

The decision is recorded and effective through the aligned controlling state in `PROJECT_CONTEXT.md`.

## 2. Entry-gate and immutable authorization evidence

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
C1_entry_gate_owner_authorization = ACCEPTED
authorization_decision_pull_request = 6
owner_disposition_record = PR_6_COMMENT_5120803290
owner_disposition_head_commit = 18351d71fa0eedfb8ebdaa2ed9b33d051fd9829a
authorized_merge_method = SQUASH
authorization_decision_merge_commit = 593f8b79246688dc9e17ee961a726f641b4d433e
authorization_decision_pr_validation_run = 12
authorization_decision_pr_validation_conclusion = SUCCESS
authorization_decision_merge_push_validation_run = 13
authorization_decision_merge_push_validation_conclusion = SUCCESS
authorization_decision_merge_push_verification_source = GITHUB_ACTIONS_UI_OWNER_PROVIDED_SUCCESS_EVIDENCE
repository_recording_status = RECORDED_AND_ALIGNED
```

The C0 completion and workflow evidence establishes that C0 is closed. The owner’s explicit decision and immutable pull-request, merge, and workflow evidence establish the accepted C1 authorization when read with the aligned controlling state in `PROJECT_CONTEXT.md`.

## 3. Authorized C1 purpose

C1 may review the bounded historical sections and material legacy evidence to recommend:

- Evidence that should be carried forward, summarized, archived, or treated as obsolete or superseded.
- Durable controls and lessons that should govern the canonical platform.
- Canonical architecture and responsibility boundaries.
- Technical assets that may later be copied, reimplemented, adapted, referenced, retained historically, excluded, or deferred.
- The appropriate future phase for each accepted recommendation.

C1 is an evidence-classification and architecture-design phase. It is not an implementation, migration, environment, data, model, or trading phase.

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
- Source and test assets only to understand historical purpose, limitations, architecture, and potential future migration treatment.

Historical repositories remain evidence and engineering sources. They do not become runtime dependencies or sources of current authorization.

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

The existence of an additional file, audit, review, commit, run, or 2v entry does not independently expand the bounded section inventory.

Any proposed new historical section requires a documented material distinction and separate owner acceptance of the scope amendment.

## 6. Required evidence classifications

Material historical evidence must receive one of:

```text
CARRY_FORWARD
SUMMARIZE_AND_REFERENCE
HISTORICAL_ARCHIVE_ONLY
OBSOLETE_OR_SUPERSEDED
```

Review depth must be proportional to materiality. C1 does not require exhaustive classification of every minor or duplicative administrative file.

No historical result, model, dataset, module, audit conclusion, provider decision, or deployment claim is automatically accepted.

## 7. Required C1 outputs

C1 is limited to the following three principal completed outputs:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

The accepted C1 templates control their required schemas and content.

The retention matrix records evidence classification and future relevance.

The technical migration manifest records recommendations only. It does not execute migration.

The C1 report consolidates the material historical conclusions, architecture recommendation, retained controls, unresolved risks, and recommended disposition for C2.

Supporting governance records may include focused authorization, review, audit, correction, and completion records required to govern C1 itself. They must not create a parallel documentation system.

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
- Credentials, authenticated access, network/API testing, or market-data requests.
- Dataset generation, reconstruction, download, modification, imputation, or acceptance.
- Model implementation, training, retraining, validation, qualification, promotion, artifact creation, or final-holdout access.
- Broker-account access, paper orders, live orders, or trading activity.
- Final ticker-universe selection.
- Profitability, deployment-readiness, publication, or live-capital claims.
- C2 or any later-phase work.
- Automatic acceptance of any historical asset or conclusion.

## 10. Current aligned effect

```text
decision_status = ACCEPTED
owner_acceptance_status = ACCEPTED
authorization_effect = C1_SCOPE_ONLY
C1_activation_effect = EFFECTIVE
C2_authorization_effect = NONE
repository_recording_status = RECORDED_AND_ALIGNED
current_lifecycle_state = C1_ACTIVE
active_major_phase = C1_LEGACY_EVIDENCE_CLASSIFICATION_AND_ARCHITECTURE_MIGRATION_DESIGN
C1_authorization_status = AUTHORIZED
C1_phase_status = ACTIVE
C2_authorization_status = NOT_AUTHORIZED
```

The decision-record merge alone did not activate C1. C1 became effective only when this accepted decision was read with the separately reviewed and merged controlling-state alignment in `PROJECT_CONTEXT.md`.

## 11. Effective C1 boundary

C1 is active only within `C1_SCOPE_ONLY`:

- The four authorized repositories remain read-only evidence and engineering sources.
- The fifteen-section inventory and proportional-review method remain controlling.
- The three C1 outputs remain documentation outputs.
- No executable migration, adaptation, code execution, environment work, provider or network activity, data work, model work, holdout access, broker activity, or trading is authorized.

This alignment registers the decision as `2v.GOV.04`.

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
8. A risk-proportional independent C1 audit passes after correction of any material findings.
9. The owner accepts the C1 completion decision.

## 13. Permitted next step

The next permitted workstream is the bounded C1 read-only historical and canonical repository review and documentation-only preparation of the three accepted C1 outputs. All work remains subject to `PROJECT_CONTEXT.md`, the accepted inventory, proportional materiality review, and the prohibited boundaries in this decision. C2 remains unauthorized.
