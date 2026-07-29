# Repository Protection Conventions

```text
document_status = ACTIVE_C0_POLICY
authorization_effect = NONE
repository_status = CREATED_PRIVATE
repository_operating_model = PRIMARILY_OWNER_OPERATED
```

`PROJECT_CONTEXT.md` remains the sole source of current authorization. This document defines non-authorizing repository-protection policy and evidence.

## 1. Visibility and protection basis

The repository remains private. Public visibility must not be used merely to obtain free protection features.

No unenforced ruleset or classic branch-protection rule was created. The limitations below are platform or account-plan limitations rather than repository defects.

## 2. Verified GitHub limitations

```text
private_branch_protection_capability = UNAVAILABLE_UNDER_CURRENT_PLAN
classic_branch_protection_enforcement = UNAVAILABLE_UNDER_CURRENT_PLAN
ruleset_enforcement = UNAVAILABLE_UNDER_CURRENT_PLAN
secret_scanning_capability = UNAVAILABLE_UNDER_CURRENT_PLAN_OR_ACCOUNT_CONFIGURATION
push_protection_capability = UNAVAILABLE_UNDER_CURRENT_PLAN_OR_ACCOUNT_CONFIGURATION
```

No GitHub-enforced branch protection, ruleset enforcement, secret scanning, or push protection is represented as active.

## 3. Temporary C0 owner-operated compensating controls

```text
temporary_compensating_controls_scope = C0_ONLY
owner_acceptance_status = ACCEPTED
```

For the remainder of C0:

- Force pushes to `main` are prohibited by owner policy.
- Deletion of `main` is prohibited by owner policy.
- Material changes require a branch and pull request.
- Documentation-consistency CI must pass before a material merge.
- Routine direct commits must be authorized, reversible, focused, and reviewed after writing.
- Commit SHA and changed paths must be verified after every write.
- Credentials, tokens, private certificates, sensitive values, account data, and credential-bearing logs must not be committed.
- No executable code, provider access, data, model, holdout, broker, or order capability may be introduced during C0.
- The independent C0 auditor must review the plan limitations and these compensating controls.

## 4. Risk-proportional default-branch workflow

Material changes require a branch and pull request, passing checks, owner or delegated review, resolution of material findings, and any phase-required independent review.

Routine work within an accepted phase may use a focused pull request or direct commit when expressly permitted, required CI passes, no material boundary changes occur, no credentials, network, data, holdout, broker, or order capability are introduced, and the change is reversible.

Because GitHub enforcement is unavailable under the current plan, force pushes to `main` and deletion of `main` remain prohibited through the accepted owner-operated controls.

## 5. C0 checks

C0 CI is documentation-only and non-executing.

Permitted checks include required-file presence, Markdown and internal links, YAML syntax, exact CSV header, duplicate paths, governance-field consistency, and stale-path detection.

C0 checks must not install research or trading dependencies, import historical code, access a network, data, accounts, providers, or brokers, train models, access holdout data, or submit orders.

## 6. Material merge authority

Explicit owner or delegated material-risk review is required for authorization, dataset, provider, model, holdout, broker, publication, risk-limit, and live-capital changes.

## 7. Protection reassessment

```text
protection_reassessment_required_before = C4_SELECTED_CODE_MIGRATION_ADAPTATION_AND_VERIFICATION
```

Reassessment is required earlier if a separately authorized activity materially increases repository, credential, data, provider, broker, or execution risk.

The later applicable phase must decide whether a plan upgrade or another protection approach is necessary. No GitHub plan upgrade is accepted or required by this document alone.

## 8. Release tags

Reserve tags for accepted datasets, accepted candidates, publication releases, controlled paper-trading baselines, and major platform releases.

## 9. Historical repositories and C4 safeguard

The canonical repository must not depend on historical default branches, local paths, or submodules.

C4 protections must prevent credentials, required network-backed tests, market-data requests in CI, production endpoints, and provider approval from being inferred from merged code.

## 10. Non-authorizing effect

```text
authorization_effect = NONE
```
