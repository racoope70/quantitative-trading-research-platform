# Repository Protection Conventions

```text
document_status = DRAFT_FOR_OWNER_REVIEW
authorization_effect = NONE
repository_status = NOT_YET_CREATED
repository_operating_model = PRIMARILY_OWNER_OPERATED
```

## 1. Visibility and secrets

The repository should begin private. Secret scanning and protections against committed credentials, tokens, certificates, and credential-bearing logs should be enabled where supported.

## 2. Risk-proportional default-branch protection

Material changes require a branch/PR, passing checks, owner or delegated review, resolution of material findings, and any phase-required independent review.

Routine work within an accepted phase may use a focused PR or direct commit when permitted, required CI passes, no material boundary changes occur, no credentials/network/data/holdout/broker/order capability are introduced, and the change is reversible.

Force pushes and deletion of the protected default branch should remain disabled.

## 3. C0 checks

C0 CI is documentation-only and non-executing.

Permitted checks include required-file presence, Markdown/internal links, YAML syntax, exact CSV header, duplicate paths, governance-field consistency, and stale-path detection.

C0 checks must not install research/trading dependencies, import historical code, access a network/data/accounts, train models, or connect to a broker.

## 4. Material merge authority

Explicit owner or delegated material-risk review is required for authorization, dataset, provider, model, holdout, broker, publication, risk-limit, and live-capital changes.

## 5. Release tags

Reserve tags for accepted datasets, accepted candidates, publication releases, controlled paper-trading baselines, and major platform releases.

## 6. Historical repositories and C4 safeguard

The canonical repository must not depend on historical default branches, local paths, or submodules.

C4 protections must prevent credentials, required network-backed tests, market-data requests in CI, production endpoints, and provider approval being inferred from merged code.

## 7. Draft status

```text
authorization_effect = NONE
```
