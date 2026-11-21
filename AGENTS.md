
# QTRP — Standing Codex Instructions

Scope: this repository only. These are persistent operating instructions, not a task authorization, scientific-access grant, or instruction to execute work. Follow the current Owner-authorized task and applicable higher-priority controls. Do not infer permission from this file.

## 1. Scientific blindness and protected-data boundary

- Treat frozen accepted scientific bodies and sealed/unseen validation, test, and holdout data as protected. Do not open, preview, sample, decode, print, summarize, or otherwise inspect their contents without explicit, exact Owner/ADMIN authorization for the data, operation, verifier, access mode, purpose, and lifecycle stage.
- Never infer protected-data access from general engineering, read-only, debugging, evidence, or testing authority. A shell command that reads payload bytes for hashing still counts as access; do not do so without applicable authorization.
- Prefer approved nonprotected metadata, source/configuration identities, manifests, prior accepted receipts, provenance, permitted filesystem size/stat information, authorized development data, and synthetic nonproduction fixtures. Do not use frozen or holdout payloads as test fixtures.
- Restrict evidence and reports to approved safe fields. Never expose protected command text, raw stdout/stderr, scientific rows/messages, or secrets through logs, tracebacks, packages, or summaries.
- Fail closed if a protected-content boundary is uncertain. Do not broaden access to resolve uncertainty casually.

## 2. Authorization continuity; avoid approval cycling

- Identify the controlling Owner/ADMIN decision and its exact scope before any sensitive operation. Scope includes the approved files/data, operation, verifier, access mode, scientific purpose, lifecycle range, and any single-use or count limits.
- Reuse an existing, unconsumed authorization when all relevant dimensions of the proposed operation remain within its approved scope. Do not ask for a fresh approval solely because the same approved check occurs at another already-authorized stage.
- Do not reuse consumed single-use authorizations, revive closed diagnostics, extend a lifecycle boundary, infer additional scientific access, or treat accepted historical examples as active permission.

### Bounded Autonomous NONPRODUCTION Engineering

For explicitly authorized NONPRODUCTION engineering tasks, follow:

**INSPECT → IDENTIFY → CORRECT → REGRESSION TEST → RERUN → CONTINUE**

- Inspect directly related interfaces and dependencies to identify reasonably discoverable in-scope defects rather than stopping at the first defect.
- Correct routine implementation and integration defects autonomously within the authorized mutation surface.
- Reuse existing code, tests, and accepted contracts. Avoid unnecessary frameworks, orchestration, or governance.
- Run focused synthetic, integration, and regression tests. Continue bounded corrections until the task passes, a substantiated blocker is established, or an authorization boundary is reached. Do not retry indefinitely.
- Preserve scientific integrity, protected data, authorization controls, runtime identities, evidence, and repository safeguards.
- Do not expand protected-data access, alter scientific/security contracts, mutate unauthorized installed runtimes, or initiate REAL execution.
- Consolidate related findings and return one coherent result through the established MAIN → MANAGING → OWNER review and decision process, with Codex reporting through its assigned coordinator when applicable.

**One Owner terminal action at a time does not mean one engineering defect at a time.**

This instruction grants no independent execution or mutation authority. All work remains limited to the current authorized task and applicable repository controls.

### Escalation boundaries

- Escalate genuine scope expansion, ambiguity, new protected-data access, scientific-independence concerns, acceptance-methodology changes, immutable-state mutation, material security changes, or REAL/production execution or publication lacking specific Owner authority.
- Avoid speculative new governance, redundant approvals, and unrelated redesign.

## 3. REAL execution, evidence, and fail-closed controls

- REAL execution, checkpoint/recovery mutation, Owner authorization publication or consumption, immutable scientific-state mutation, and production deployment require their own current, exact authorization. Neither these instructions nor a successful nonproduction test supplies it.
- Preserve applicable input/runtime/configuration identities, unit/attempt limits, exact checkpoint/resume behavior, authorization binding, replay rejection, staging/readback, deterministic scientific unit contracts, and fail-closed checks.
- Do not weaken scientific validation, success-only command-status checks, proof/recovery logic, reason precedence, or acceptance criteria to make an execution pass.
- Preserve completed units and frozen accepted evidence. Never treat a controlled stop as scientific acceptance; never retry a consumed attempt or advance to a new unit without the applicable authorization.
- Use source- and evidence-backed conclusions. Clearly separate independently verified evidence, Codex direct host observations, Owner-reported facts, and unresolved facts. Do not represent a source capability or current configuration as proof of an unobserved historical event.
- Treat Owner-accepted scientific-sufficiency decisions as binding within their exact source, unit, attempt, and lifecycle scopes. Do not impose stronger historical scientific requirements without a controlling contract, material contradictory evidence, or explicit Owner approval.
- Reuse accepted historical science and lineage. Missing current checkpoint, preparation, or authorization evidence is an unresolved operating-state issue, not automatic invalidation of historical scientific acceptance. No blanket P10 authentication, broad S04 recertification, full historical scientific reconstruction, or Option B population admission is automatically required for original-lineage U0012.
- Original Attempt 11 Option A four-object/accepted-lineage sufficiency is specific to its approved binding; do not extend it to a later attempt or changed instance without exact evidence and controlling authority.
- Retain the current P4 requirement for an independently acceptable recovery declaration and applicable custody, exact predecessor/preparation identity, Policy B validation, required persistence/checkpoint/terminal integrity, one-use authorization and restart/replay protection. Do not weaken existing integrity guards without separate authority.

## 4. Project reference-document boundaries and navigation (J2)

These repository-relative links point to the established documents. Consult the relevant document when the task requires it; do not automatically read all three for routine engineering work.

- [Project Context](PROJECT_CONTEXT.md) — Controlling source of truth for broad current lifecycle state, authorization boundaries, explicit nonauthorization, and pointers to material decisions. Consult for state-dependent or authorization-sensitive work. It is not a per-action task tracker or checkpoint ledger, and reading it grants no new authority.
- [Milestone Review Reference Map](docs/workflows/milestone_review_reference_map.md) — Non-authorizing roadmap, governance/evidence/decision history, and curated 2V navigation. Consult for phase history, milestone evidence, and decision lookup.
- [Future Validation and Training Reference Map](docs/workflows/future_validation_training_reference_map.md) — Non-authorizing prospective scientific sequencing, training, evaluation, and holdout guidance. Consult for future scientific planning, without treating future guidance as currently authorized activity.

### Source and evidence discovery

Before searching for or reconstructing project source/evidence,
consult `docs/workflows/source_evidence_locator.md` and its
accepted provenance references.

Verify current identity and access authorization before use.
Do not infer permission to inspect protected artifacts or
search additional locations from the locator alone.

Use local repository files and accepted current task evidence; do not assume a remote main version overrides uncommitted, accepted local state. If references appear inconsistent with a newer controlling Owner/ADMIN decision, flag the discrepancy rather than silently updating state or inventing authorization.

Do not promote a reference map, old report, prior task, or this `AGENTS.md` to an authorization source. Do not change any governance/reference document unless the current task explicitly authorizes that change.

Use the current MAIN → MANAGING → OWNER routing for review and material decisions; ADMIN receives escalated governance or scientific decisions. Preserve the established separation of roles.

## 5. Working style

- Execute forward from accepted state. Prefer the smallest directly relevant source/configuration trace, bounded correction, and focused regression tests. Do not reopen settled work without material contrary evidence.
- For Owner Mac terminal or GUI interactions: give exactly one safe action at a time, explain it briefly, await its complete result, classify PASS / FAIL / NEEDS_CORRECTION / UNRESOLVED, then proceed.
- No deletion or alteration of protected/frozen data. For storage checks, inspect only permitted filesystem size/metadata and clearly unrelated ordinary cache locations; do not list, view, move, or delete protected dataset contents.
- Avoid unnecessary new launchers, signers, controllers, tracing layers, dependency changes, documentation workstreams, or broad repository scans. Keep production and NONPRODUCTION scopes distinct.
- When a Codex reasoning-effort recommendation is requested for this project, use Extra High for substantial cross-file or security-boundary work, High for bounded straightforward work, and Ultra only for exceptional security/architecture analysis.

## 6. Engineering and Git safeguards

- Inspect the directly relevant repository surface before editing. Avoid broad repository scans unless necessary to resolve the active task.
- Make a short implementation plan before material multi-file edits. For small bounded changes, proceed directly.
- Use the exact interpreter required by the accepted contract for QTRP-owned Python components and applicable tests. Do not create, replace, or switch Python environments unless the active task authorizes it. Do not automatically extend QTRP's host Python 3.12 interpreter requirement to autonomous Codex inner commands unless an applicable accepted contract explicitly requires it.
- Edit only files required for the active task. Do not make opportunistic cleanup, formatting, documentation, dependency, or refactoring changes outside scope.
- Run focused tests when appropriate for the files and behavior changed. If tests are not applicable, state why rather than running unrelated suites.
- Before any authorized commit, inspect the intended diff and verify the staged set with `git status --short` and `git diff --cached --name-only`. If an intended file is unexpectedly ignored or unstaged, stop and report the condition rather than forcing it with git add -f.
- Do not push, tag, or publish repository changes unless the active Owner-authorized task explicitly permits it.

## 7. Per-task authority

The active task prompt and controlling Owner/ADMIN decisions supply task-specific authorizations, protected-access fields, attempt/unit limits, and stop conditions. If those are absent or unclear, perform only plainly safe work already authorized and report the exact missing boundary.

This file grants no new access, repository mutation, REAL dispatch, scientific acceptance, publication, commit, push, or repeat of any completed one-shot diagnostic.
