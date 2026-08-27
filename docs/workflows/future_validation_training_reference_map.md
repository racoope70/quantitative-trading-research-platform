# Future Validation and Training Reference Map

```text
document_status = ESTABLISHED_NON_AUTHORIZING_REFERENCE
document_role = NON_AUTHORIZING_FUTURE_GUIDANCE_AND_SEQUENCING_REFERENCE
authorization_effect = NONE
```

## 1. Purpose

This document contains permanent methodological guidance and high-level planned tasks.

It does not contain current authorization, current blockers, phase status, completed-chain history, or claims that future work is active.

Detailed phase checklists should be created only when the applicable phase becomes active.

## 2. Permanent scientific principles

All future research must preserve:

- Temporal causality.
- Train-only fitting.
- Leakage-controlled chronological evaluation.
- Explicit embargo where required.
- Predeclared qualification, rejection, and promotion criteria.
- Honest transaction-cost and slippage assumptions.
- Complete data and artifact provenance.
- Retention of adverse and inconclusive results.
- Separation of software correctness, statistical performance, economic performance, broker reliability, and deployment readiness.

## 3. Architecture, environment, and migration

Required sequence:

```text
canonical skeleton and migration preparation
→ Python environment and dependency reconstruction
→ selected code migration, adaptation, and verification
```

Migration must preserve immutable source attribution, one canonical responsibility per component, known limitations, required tests, and no runtime dependency on historical repositories.

C4 may include provider-neutral interfaces, mocks, offline fixtures, normalization utilities, and provisional provider components.

C4 does not establish provider acceptance or authorize credentials, authenticated access, network/API testing, market-data requests, entitlement conclusions, or production-source validation.

## 4. Data and universe guidance

Future data phases must define:

- Provider, feed, licensing, and permitted use.
- Calendar, session, timestamp, and corporate-action rules.
- Schema, dtypes, missing-slot policy, exclusions, and imputation policy.
- Symbols, date ranges, provenance, checksums, and immutable dataset identity.

Universe selection should consider liquidity, spreads, expected costs, coverage, corporate actions, sector and regime diversity, provider availability, compute requirements, survivorship bias, and selection bias.

Recommended progression:

```text
single-ticker engineering verification
→ small diagnostic subset
→ accepted final comparison universe
```

## 5. Validation and leakage guidance

Future validation must define training, validation, development-test or qualification data, embargo, refit rules, benchmarks, costs, and terminal disposition criteria.

Controls must prevent full-series fitting, centered rolling windows, future-aware joins, label leakage, random time-series splitting, holdout-driven changes, invalid preprocessor reuse, and future-aware missing-data treatment.

## 6. PPO terminal disposition

PPO v2 is a fresh second-generation implementation.

Its active phase record should define observation and action spaces, reward, costs, position constraints, training procedure, artifact contract, and qualification criteria.

A predeclared PPO development-test or qualification period may be used. It must remain distinct from the shared final holdout.

C9 may close with:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

## 7. Random Forest and XGBoost branching

C10 may begin only when:

```text
C9_terminal_disposition = QUALIFIED_AND_FROZEN
focused_RF_readiness_audit = PASS
```

When PPO is not qualified:

```text
C10_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

When C10 proceeds, it may close with:

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

C10 does not need to produce a qualified RF candidate. It needs only an accepted terminal disposition while PPO remains qualified.

When PPO is not qualified:

```text
C11_terminal_disposition = NOT_APPLICABLE_NO_QUALIFIED_PPO_FOUNDATION
```

When C11 proceeds, it may close with:

```text
QUALIFIED_AND_FROZEN
REJECTED
NO_CANDIDATE
INCONCLUSIVE
```

RF and XGBoost readiness reviews should address targets, feature availability, temporal alignment, train-only fitting, thresholds, interaction with PPO, costs, and terminal disposition criteria.

Feature importance and SHAP analysis must not be presented as causal evidence.

## 8. Eligible candidates and shared final holdout

The research objective is to investigate PPO, PPO plus Random Forest, and PPO plus XGBoost fairly. It does not guarantee that all three families will produce eligible candidates.

Only model families with:

```text
QUALIFIED_AND_FROZEN
```

are eligible for the shared final holdout.

The final-holdout path requires:

```text
all_applicable_model_family_phases_have_accepted_terminal_dispositions = YES
all_eligible_candidates_are_frozen = YES
at_least_one_eligible_candidate_exists = YES
common_evaluation_package_is_frozen = YES
final_holdout_access_is_expressly_authorized = YES
```

The final holdout must be opened once and applied consistently to every eligible frozen candidate.

It must not be used for tuning, feature selection, threshold selection, reward redesign, candidate replacement, or iterative debugging.

Rejected, no-candidate, inconclusive, and not-applicable outcomes must remain visible in the final research report.

When no eligible candidate exists:

```text
C12_terminal_disposition = NO_ELIGIBLE_CANDIDATE
final_holdout_accessed = NO
```

The owner must choose one:

```text
STOP_CURRENT_RESEARCH_CYCLE
PUBLISH_NEGATIVE_OR_INCONCLUSIVE_RESULT
RETURN_TO_A_SEPARATELY_AUTHORIZED_REDESIGN_PHASE
```

An unqualified model must not be forced into the final holdout.

## 9. Publication, paper trading, and deployment

Publication must accurately present methods, costs, uncertainty, limitations, rejected, no-candidate, inconclusive, and not-applicable outcomes, and reproducibility evidence.

Paper trading requires paper-only credentials and endpoints, live-endpoint rejection, no-submit defaults, explicit order enablement, position and loss limits, stale-data and duplicate-order controls, reconciliation, kill switch, flattening procedures, and complete logs.

Operational reliability and economic performance must be reported separately.

Paper trading does not authorize live deployment. Live-capital consideration requires a separate risk framework, owner authorization, and independent audit.

## 10. Monitoring, retirement, and retraining

Monitoring should cover data availability and drift, prediction behavior, costs, turnover, exposure, drawdown, broker failures, and artifact/configuration mismatches.

Retirement criteria must be defined before operational use.

Retraining must use a new accepted data cutoff and cycle identity, updated provenance, preserved interpretation of viewed holdouts, new future evaluation data where possible, incumbent comparison, and independent replacement review.

A viewed holdout cannot become untouched again.
