# QTRP Automation Reliability Engineering Approach

**Document status:** Nonauthorizing engineering guidance. The Engineering Gap Assessment is complete, and Implementation V1 is Owner-accepted within bounded NONPRODUCTION scope. Installed REAL-runtime compatibility, scientific acceptance, source integration, deployment readiness, protected access, and REAL execution authorization are not established by these results or this reference.

## 1. Purpose and boundaries

This reference preserves the **QTRP Automation Reliability Engineering Approach**: a project-specific application of lightweight Systems Engineering and Site Reliability Engineering (SRE) practices. Its focus is evidence-based failure analysis, observability, durable execution-state management, and targeted NONPRODUCTION fault-injection testing. It guides evidence-based engineering judgment, rather than establishing a new formal industry framework. It is not an implementation specification, current-work tracker, lifecycle controller, authorization instrument, or substitute for code and evidence inspection.

The philosophy remains established guidance. The separately authorized Engineering Gap Assessment and bounded NONPRODUCTION Implementation V1 have been completed and accepted within their demonstrated scope. This document grants no authority to install those corrections, alter the canonical source or REAL runtime, consume authorization, access protected data, or begin readiness work.

## 2. Engineering philosophy

The objective is to replace repeated reactive debugging with a holistic, evidence-based review of the existing automation lifecycle. Understand how the implemented components work together before selecting corrections. Prioritize reliable execution, actionable diagnostics, safe terminal outcomes, maintainability, and genuine simplification.

1. **Reuse accepted controls.** Preserve proven authorization, scientific validation, provenance, checkpoint, replay, and fail-closed mechanisms. Inspect existing interfaces before proposing replacements.
2. **Diagnose before designing.** Review the complete relevant automation architecture and its integration boundaries using permitted source and evidence. Identify demonstrated implementation or test-coverage gaps before recommending changes. Do not infer a correction from an unexplained return code.
3. **Make failure progress observable.** Where permitted and technically feasible, distinguish the last confirmed execution stage, an evidence-supported error reason, and whether computation, evidence staging, and scientific acceptance occurred. Preserve `UNKNOWN` when the cause is not established.
4. **Make lifecycle outcomes dependable.** Distinguish attempt registration, native execution, checkpoint/journal updates, scientific validation, acceptance, and terminal disposition. Unexpected termination must not silently imply success or erase the last trustworthy state. If safe finalization is unavailable, explicitly report terminal incompleteness and fail closed.
5. **Test realistic paths and failures.** Prefer decisive NONPRODUCTION integration using permissible synthetic fixtures, the intended native execution path where feasible, and targeted fault injection over expanding unrelated unit-test counts.
6. **Prefer proportional corrections.** Simplify, consolidate, or remove mechanisms only when supported by a real requirement, defect, or maintenance burden. Avoid unnecessary orchestration, telemetry infrastructure, dependencies, controllers, signers, and review processes.
7. **Separate kinds of success.** A successful synthetic run is engineering evidence, not scientific acceptance, REAL authorization, provider readiness, paper-trading approval, or deployment qualification.
8. **Preserve protected boundaries.** Maintain scientific blindness, frozen-result and final-holdout protections, safe evidence handling, exact single-use authorization, replay rejection, and existing fail-closed conditions.

These principles continue to guide future permitted evaluation; they do **not** require a particular logging framework, state-machine redesign, test harness, or additional code correction.

## 3. Completed Engineering Gap Assessment — reusable method

The separately authorized Engineering Gap Assessment is **complete and accepted**. Its six bounded questions are preserved below as a reusable description of the method applied, not as a pending assignment, a new formal industry framework, or six additional governance gates.

| Assessment | Senior engineering question |
|---|---|
| Existing architecture | What do we already have, and how does it work together? |
| Failure coverage | What did our previous tests fail to demonstrate? |
| Required corrections | What actually needs to change? |
| Test strategy | How will we prove the proposed corrections work? |
| Complexity assessment | What can we reuse, simplify, consolidate, or eliminate? |
| Readiness conditions | What must be true before another REAL attempt is even considered? |

**A. Existing architecture.** Map the directly relevant execution, event-capture, diagnostic, authorization, checkpoint, scientific-validation, and finalization interfaces. Distinguish *implemented*, *directly verified*, *historically reported*, *incomplete*, and *reusable* capabilities. Do not equate source-code presence with successful runtime behavior.

**B. Failure coverage.** Compare previous component and integration tests against critical execution paths and potential failure modes. Identify what was demonstrated, what remains untested, and which gaps materially affect reliability. Do not assign root causes without supporting evidence.

**C. Required corrections.** Identify the smallest engineering changes supported by implementation and test evidence. Reuse existing mechanisms where possible, preserve established controls, and justify corrections based on reliability, simplicity, and maintainability.

**D. Test strategy.** Define successful and unsuccessful NONPRODUCTION tests covering the complete synthetic 25-record lifecycle where feasible, native-process failures, execution-stage diagnostics, scientific rejection, replay protection, checkpoint integrity, registration and finalization, and crash recovery. Specify what each test establishes and its limitations. Use only synthetic representations of protected recovery state.

**E. Complexity assessment.** Classify existing mechanisms as *retain*, *simplify*, *consolidate*, *remove*, or *needs evidence*. Justify any new component against a demonstrated need that existing mechanisms cannot satisfy. Avoid speculative redesign and duplicated governance.

**F. Readiness conditions.** Define objective evidence for engineering acceptance, including actual exercised code/runtime identities, positive and negative lifecycle outcomes, protected-boundary compliance, and trustworthy terminal/unknown-state reporting. Identify residual uncertainties and requirements for independent engineering review. Explicitly separate engineering correctness, scientific acceptance, authorization, and deployment readiness; any future REAL-readiness decision remains the Owner's separately governed decision.

The completed assessment informed one bounded, evidence-backed NONPRODUCTION implementation recommendation. Future work still requires its own applicable authorization; this reference cannot initiate corrections.

## 4. Completed engineering evidence and continuing boundaries

The Engineering Gap Assessment identified a post-registration attempt-absence guard conflict, incomplete prior full native-lifecycle and terminal-failure evidence, and an unresolved original A0011 native exit-code-1 cause. Following independent review, the Owner accepted bounded NONPRODUCTION Implementation V1; **27/27 selected final-source synthetic cases PASS**, including an actual trusted synthetic Python subprocess, a complete synthetic 25-record success path, rejected invalid synthetic output, competing admission/replay protection, checkpoint/journal consistency, handled failure and interruption/restart behavior.

The accepted NONPRODUCTION corrections are **C1**: place the attempt-absence guard at initial construction so read-only post-registration verification remains valid; **C2**: reject an existing attempt before irreversible admission/authorization consumption or native dispatch; and **C3**: classify OS process-creation rejection versus successful child creation from validated capture timing evidence. The earlier isolated C1 guard qualification also passed 33/33 synthetic checks; it is distinct from Implementation V1's 27/27 final-source suite.

**Failure distinction:** A handled native failure with valid process-local finalization authority can record a durable controlled stop. An unexpected interruption or loss of such authority preserves the last trustworthy state and may leave terminal finalization **incomplete**; neither situation permits an invented success or reconstructed consumed authority.

Source-promotion preparation is closed under Owner-selected `OPTION_A__RETAIN_ACCEPTED_NONPRODUCTION_CAPSULE` (`CLOSED_WITH_ACCEPTED_PARTIAL_TARGET_RECONCILIATION`). The accepted capsule remains a qualified prospective **NONPRODUCTION reference** with C1–C3 already present. No separate canonical integration target, source promotion, installed REAL compatibility, publication, or deployment readiness was established. The original A0011 native return-code-1 cause remains unresolved.

See [Automation Reliability Engineering V1 completion](../reports/automation_reliability_engineering_v1_completion.md) for the bounded technical record and evidence identities. Engineering acceptance is distinct from scientific acceptance, source integration, deployment readiness, protected-data access and REAL authorization. Future Batch0004 U0012 A0012 readiness engineering remains **deferred/not authorized**; no work begins automatically from this reference.

Use existing MAIN → MANAGING → OWNER routing, with ADMIN for escalated architectural, governance, or scientific review. The assessment and later implementation require their own applicable authorizations; this reference supplies none. Report unresolved failures and terminal incompleteness rather than relabeling them as success.

Keep work execution-forward and proportionate to demonstrated gaps. Do not create additional standing documents, trackers, approval procedures, or broad review layers.
