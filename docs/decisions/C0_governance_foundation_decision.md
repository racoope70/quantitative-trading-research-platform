# C0 Governance-Foundation Decision

```text
document_status = DRAFT_FOR_OWNER_REVIEW
decision_id = GOV-DEC-0001
decision_status = PROPOSED
authorization_effect = NONE
```

## 1. Decision

Adopt:

- A simplified three-document governance structure.
- Phase-level, risk-proportional authorization.
- The `PRE_C0_DRAFT_REVIEW → C0_ACTIVE → C0_COMPLETED` lifecycle.
- Separate C0 templates and future C1 completed outputs.
- A provisional bounded C1 historical-section inventory.
- Environment reconstruction before executable migration.
- The C4 provider boundary.
- Qualified-PPO branching for RF and XGBoost.
- One shared final holdout for all eligible frozen candidates only.

## 2. Complete proposed C0 package

1. `PROJECT_CONTEXT.md`
2. `docs/workflows/milestone_review_reference_map.md`
3. `docs/workflows/future_validation_training_reference_map.md`
4. `docs/decisions/C0_governance_foundation_decision.md`
5. `docs/templates/C1_legacy_evidence_retention_matrix_template.csv`
6. `docs/templates/C1_technical_migration_manifest_template.yaml`
7. `docs/templates/C1_legacy_evidence_and_architecture_report_template.md`
8. `README.md`
9. `CONTRIBUTING.md`
10. `docs/governance/repository_protection_conventions.md`
11. `docs/audits/C0_independent_governance_foundation_audit_instructions.md`

All remain `DRAFT_FOR_OWNER_REVIEW` while the lifecycle is `PRE_C0_DRAFT_REVIEW`.

## 3. C0 lifecycle

Owner acceptance of the proposed C0 scope activates C0.

C0 then authorizes private-repository creation, minimal nontechnical structure, package commits, documentation-only CI, repository protections, one independent C0 audit, and correction of material findings.

Repository creation, committed deliverables, audit passage, remediation, and owner closure acceptance are completion conditions.

While under review:

```text
authorization_effect = NONE
```

## 4. Governance-document roles

- `PROJECT_CONTEXT.md`: concise current snapshot and authorization.
- Milestone Map: roadmap, gates, curated evidence, bounded C1 inventory, and material-record navigation.
- Future Map: permanent methodology and high-level future tasks.

Git history and VS Code verify implementation state but do not control authorization.

## 5. C1 templates and future outputs

C0 templates:

```text
docs/templates/C1_legacy_evidence_retention_matrix_template.csv
docs/templates/C1_technical_migration_manifest_template.yaml
docs/templates/C1_legacy_evidence_and_architecture_report_template.md
```

Future C1 outputs:

```text
docs/migration/legacy_evidence_retention_matrix.csv
docs/migration/technical_migration_manifest.yaml
docs/reports/C1_legacy_evidence_and_architecture_report.md
```

C1 has no duplicate evidence map, duplicate retention matrix, or mandatory report per minor section.

## 6. C1 bounded historical review scope

C1 begins with the provisional inventory defined in the Milestone Review Reference Map under:

```text
C1_BOUNDED_HISTORICAL_SECTION_INVENTORY
```

The inventory contains fifteen sections covering exploratory research, legacy PPO and hybrid work, platform integrations, operational and paper-trading evidence, modular migration, artifact and holdout audits, PPO v2 and data contracts, dataset reconstruction, missing-bar and provider investigations, environment diagnosis, and governance lessons.

C1 must identify the exact historical 2v entry or range for every bounded section.

A section may be added only when materially distinct. Another file, audit, review, commit, run record, or 2v entry is not sufficient by itself.

Any added section requires:

- A material-distinction rationale.
- Applicable historical repository.
- Applicable legacy 2v range.
- Owner acceptance of the scope amendment.
- Inclusion in the C1 summary report.

C1 does not require exhaustive classification of every minor file within a section. Material-record and proportional-review rules remain controlling.

## 7. Architecture, environment, and provider sequence

```text
C2_CANONICAL_REPOSITORY_SKELETON_AND_MIGRATION_PREPARATION
→ C3_PYTHON_ENVIRONMENT_AND_DEPENDENCY_RECONSTRUCTION
→ C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
```

C4 may migrate provider-neutral interfaces, mocks, fixtures, normalization/schema utilities, and provisional provider components using offline verification.

C4 does not authorize provider acceptance, credentials, authenticated access, network/API testing, market-data requests, entitlement verification, account inspection, production validation, or final provider/feed decisions.

## 8. PPO, RF, and XGBoost branching

C9 may close with:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

C10 may begin only when:

```text
C9_terminal_disposition = QUALIFIED_AND_FROZEN
focused_RF_readiness_audit = PASS
```

If PPO is not qualified:

```text
C10_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

If C10 proceeds, its terminal dispositions are:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

C11 may begin only when:

```text
C9_terminal_disposition = QUALIFIED_AND_FROZEN
C10_has_accepted_terminal_disposition = YES
focused_XGBoost_readiness_audit = PASS
```

C10 does not need to produce a qualified RF candidate. Any accepted C10 terminal disposition is sufficient while PPO remains qualified.

If PPO is not qualified:

```text
C11_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

If C11 proceeds, its terminal dispositions are:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

## 9. C12 eligible-candidate and final-holdout decision

The phase name is:

```text
C12 — Eligible-Candidate Freeze, Shared Final Holdout, and Promotion Decision
```

Only `QUALIFIED_AND_FROZEN` model families are eligible.

The final-holdout path requires:

```text
all_applicable_model_family_phases_have_accepted_terminal_dispositions = YES
all_eligible_candidates_are_frozen = YES
at_least_one_eligible_candidate_exists = YES
common_evaluation_package_is_frozen = YES
final_holdout_access_is_expressly_authorized = YES
```

The final holdout is opened once and applied consistently to every eligible frozen candidate.

Rejected, no-candidate, inconclusive, and not-applicable outcomes remain visible in the final report.

If no eligible candidate exists:

```text
C12_terminal_disposition = NO_ELIGIBLE_CANDIDATE
final_holdout_accessed = NO
```

The owner must select:

```text
STOP_CURRENT_RESEARCH_CYCLE
PUBLISH_NEGATIVE_OR_INCONCLUSIVE_RESULT
RETURN_TO_A_SEPARATELY_AUTHORIZED_REDESIGN_PHASE
```

The project must not force an unqualified model into the final holdout.

## 10. C1 next disposition

The C1 report must recommend one:

```text
PROCEED_TO_C2
REMAIN_IN_C1_FOR_CORRECTION
HOLD_FOR_OWNER_DECISION
STOP_OR_REDESIGN_MIGRATION
```

## 11. Risk-proportional contribution and protection model

Material governance, data, model, provider, broker, holdout, publication, or live-capital changes require branch/PR review and the applicable independent review.

Routine work inside an accepted phase may use a focused PR or direct commit when permitted, required CI passes, and no material boundary changes.

## 12. Draft effect

This decision becomes effective only when the owner accepts the proposed C0 scope.

Until then:

```text
decision_status = PROPOSED
authorization_effect = NONE
```
