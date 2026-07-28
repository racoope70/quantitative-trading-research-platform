# Independent C0 Governance-Foundation Audit Instructions

```text
document_status = DRAFT_FOR_OWNER_REVIEW
audit_status = NOT_STARTED
authorization_effect = NONE
```

## 1. Purpose

Independently determine whether the completed C0 package establishes a clear, proportionate, non-duplicative governance and migration foundation.

Audit the package as one integrated system.

## 2. Required evidence

Review all eleven C0 files, repository structure, documentation-only CI, protections, C0 Git history, and evidence that no prohibited technical execution occurred.

## 3. Core audit questions

### Lifecycle and document boundaries

Confirm owner acceptance activates C0; repository creation, commits, audit, remediation, and closure are completion conditions; draft review has no authorization effect; `PROJECT_CONTEXT.md` is concise; the Milestone Map does not duplicate authorization; and the Future Map remains guidance-only.

### C1 bounded historical scope

Confirm that:

- The Milestone Map contains `C1_BOUNDED_HISTORICAL_SECTION_INVENTORY` with all fifteen provisional sections.
- C1 must identify the exact historical 2v entry or range for each section.
- A new section may be added only when materially distinct.
- Another file, audit, review, commit, run record, or 2v entry is not sufficient by itself.
- An added section requires a material-distinction rationale, applicable repository, applicable 2v range, owner acceptance, and inclusion in the C1 report.
- The package does not require exhaustive classification of every minor file within a section.
- Material-record and proportional-review rules remain intact.

### C1 artifact structure

Confirm C0 templates are separate from future C1 outputs, there are exactly three primary C1 outputs, duplicate evidence tracking is avoided, and technical assets are separated from governance evidence.

### Architecture and provider sequencing

Confirm environment reconstruction precedes executable migration and C4 prohibits provider acceptance, credentials, authenticated access, network/API testing, market-data requests, entitlement verification, account inspection, and production validation.

### PPO, RF, and XGBoost branching

Confirm:

- C9 may close with `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`.
- C10 may begin only when `C9_terminal_disposition = QUALIFIED_AND_FROZEN` and the focused RF readiness audit passes.
- When PPO is not qualified, C10 is `NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION`.
- When C10 proceeds, its valid terminal dispositions are `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`.
- C11 may begin only when PPO is qualified, C10 has any accepted terminal disposition, and the focused XGBoost readiness audit passes.
- C10 does not need to produce a qualified RF candidate for C11 to proceed.
- When PPO is not qualified, C11 is `NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION`.
- When C11 proceeds, its valid terminal dispositions are `QUALIFIED_AND_FROZEN`, `REJECTED`, `NO_CANDIDATE`, or `INCONCLUSIVE`.

### C12 eligible candidates and final holdout

Confirm that the phase is named:

```text
C12 — Eligible-Candidate Freeze, Shared Final Holdout, and Promotion Decision
```

Confirm that:

- All applicable model-family phases have accepted terminal dispositions.
- Only `QUALIFIED_AND_FROZEN` families are eligible.
- All eligible candidates are frozen.
- At least one eligible candidate exists before final-holdout access.
- The common evaluation package is frozen.
- Final-holdout access is expressly authorized.
- The final holdout is opened once and applied consistently to every eligible frozen candidate.
- Rejected, no-candidate, inconclusive, and not-applicable outcomes remain visible in the final report.

When no eligible candidate exists, confirm:

```text
C12_terminal_disposition = NO_ELIGIBLE_CANDIDATE
final_holdout_accessed = NO
```

Confirm the owner may choose:

```text
STOP_CURRENT_RESEARCH_CYCLE
PUBLISH_NEGATIVE_OR_INCONCLUSIVE_RESULT
RETURN_TO_A_SEPARATELY_AUTHORIZED_REDESIGN_PHASE
```

Confirm no unqualified model is forced into the final holdout.

### Risk-proportional workflow

Confirm material governance, data, model, provider, broker, holdout, publication, and live-capital changes require branch/PR review and applicable independent review, while routine work may use a focused PR or permitted direct commit when CI passes and no material boundary changes.

## 4. Out-of-scope activity

The auditor must not execute code, install research/trading dependencies, access networks/providers/brokers/data/holdout/accounts, train models, generate datasets, or submit orders.

## 5. Audit decision

Use:

```text
PASS
NEEDS_CORRECTION
FAIL
```

A correction finding should identify the defect, location, risk, required change, and whether remediation remains inside C0.

## 6. Report and reaudit

The report should contain scope, evidence, independence, conclusion, findings, required corrections, observations, prohibited-activity confirmation, decision, and permitted next step.

Use one corrected audit or concise addendum after remediation. Avoid recursive review chains unless a material evidence, scope, independence, or reasoning problem requires them.

## 7. C0 closure recommendation

Recommend closure only when the complete package is committed, protections exist, documentation-only CI passes, material findings are resolved, no prohibited execution occurred, C1 is next, and the owner still accepts closure.

## 8. Draft status

```text
audit_status = NOT_STARTED
owner_acceptance_status = PENDING
authorization_effect = NONE
```
