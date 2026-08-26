# Contribution Conventions

```text
document_status = DRAFT_FOR_OWNER_REVIEW
authorization_effect = NONE
repository_operating_model = PRIMARILY_OWNER_OPERATED
```

## 1. Governing state

Before work begins, read `PROJECT_CONTEXT.md`, the applicable Milestone Map and curated records, and the applicable Future Map section, then inspect Git history and the working tree for implementation state.

## 2. Risk-proportional workflow

Material changes require a branch, pull request, explicit review, passing CI, and any phase-required independent review.

Material changes include governance, data, provider, model, holdout, broker, publication, safety, and live-capital boundaries.

Routine work within an accepted phase may use a focused PR or a direct commit when the owner-operated workflow permits it, required CI passes, no material boundary changes occur, and the change is reviewable and reversible.

## 3. Scope discipline

Contributions must not introduce unauthorized data/provider/account/broker access, network/API testing, holdout access, model-family expansion, order capability, credentials, scientific-contract changes, or weakened safety controls.

## 4. Commit and PR content

Material PRs should state purpose, active phase, responsibilities changed, checks performed, limitations, external systems accessed, and whether authorization/scientific/safety boundaries changed.

Routine direct commits should remain focused, descriptive, and traceable.

## 5. Technical migration and provider boundary

Migrated assets must record immutable source attribution, classification, canonical responsibility, required changes, limitations, tests, destination, and owner disposition.

During C4, the authorized migration scope included provider-neutral interfaces, mocks, offline fixtures, normalization/schema utilities, and provisional provider code. C4 did not authorize provider acceptance, credentials, authenticated access, network/API testing, market-data requests, entitlement conclusions, or production validation.

## 6. Testing and documentation

Testing should be proportional to risk.

Create separate records only for material decisions, dataset builds, training campaigns, holdout access, promotions, publication releases, broker-connected campaigns, incidents, and required audits.

Git history, focused PRs, issues, and CI are sufficient for ordinary work.

## 7. Draft status

These conventions become operational only after C0 activation and repository creation.

```text
authorization_effect = NONE
```
