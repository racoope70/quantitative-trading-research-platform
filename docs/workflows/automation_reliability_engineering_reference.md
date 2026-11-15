# QTRP Automation Reliability Engineering Approach

```text
document_role = NONAUTHORIZING_PROSPECTIVE_ENGINEERING_REFERENCE
engineering_philosophy = ESTABLISHED_GUIDANCE
engineering_gap_assessment = REQUIRED__NOT_YET_COMPLETED
technical_implementation_plan = PROVISIONAL__PENDING_ASSESSMENT
specific_code_corrections = NOT_YET_SELECTED
engineering_readiness = NOT_ESTABLISHED
authorization_effect = NONE
```

## 1. Purpose and boundaries

This reference preserves the **QTRP Automation Reliability Engineering Approach**: a project-specific application of lightweight Systems Engineering and Site Reliability Engineering (SRE) practices. Its focus is evidence-based failure analysis, observability, durable execution-state management, and targeted NONPRODUCTION fault-injection testing. It guides engineering judgment before corrections are selected, rather than establishing a new formal industry framework. It is not an implementation specification, current-work tracker, lifecycle controller, authorization instrument, or substitute for code and evidence inspection.

The philosophy is established guidance; the implementation plan is **provisional pending assessment**. No specific code corrections, installed changes, or readiness finding are approved by this document. An assessment must produce a concrete, bounded engineering recommendation rather than another open-ended research or governance program.

## 2. Supporting references

[Project Context](../../PROJECT_CONTEXT.md) controls current lifecycle and authorization state, while [AGENTS.md](../../AGENTS.md) provides standing Codex instructions. Historical engineering findings and recovery evidence remain in the [Engineering Reliability Retrospective](../case_studies/batch0004_execution_reliability_retrospective.md) and [Attempt 11 Recovery and Milestones Report](../reports/batch0004_u0012_attempt11_recovery_closure_and_milestones.md). Scientific guidance and evidence navigation remain in the [Future Validation and Training Reference Map](future_validation_training_reference_map.md) and [Milestone Review Reference Map](milestone_review_reference_map.md).

## 3. Engineering philosophy

The objective is to replace repeated reactive debugging with a holistic, evidence-based review of the existing automation lifecycle. Understand how the implemented components work together before selecting corrections. Prioritize reliable execution, actionable diagnostics, safe terminal outcomes, maintainability, and genuine simplification.

1. **Reuse accepted controls.** Preserve proven authorization, scientific validation, provenance, checkpoint, replay, and fail-closed mechanisms. Inspect existing interfaces before proposing replacements.
2. **Diagnose before designing.** Review the complete relevant automation architecture and its integration boundaries using permitted source and evidence. Identify demonstrated implementation or test-coverage gaps before recommending changes. Do not infer a correction from an unexplained return code.
3. **Make failure progress observable.** Where permitted and technically feasible, distinguish the last confirmed execution stage, an evidence-supported error reason, and whether computation, evidence staging, and scientific acceptance occurred. Preserve `UNKNOWN` when the cause is not established.
4. **Make lifecycle outcomes dependable.** Distinguish attempt registration, native execution, checkpoint/journal updates, scientific validation, acceptance, and terminal disposition. Unexpected termination must not silently imply success or erase the last trustworthy state. If safe finalization is unavailable, explicitly report terminal incompleteness and fail closed.
5. **Test realistic paths and failures.** Prefer decisive NONPRODUCTION integration using permissible synthetic fixtures, the intended native execution path where feasible, and targeted fault injection over expanding unrelated unit-test counts.
6. **Prefer proportional corrections.** Simplify, consolidate, or remove mechanisms only when supported by a real requirement, defect, or maintenance burden. Avoid unnecessary orchestration, telemetry infrastructure, dependencies, controllers, signers, and review processes.
7. **Separate kinds of success.** A successful synthetic run is engineering evidence, not scientific acceptance, REAL authorization, provider readiness, paper-trading approval, or deployment qualification.
8. **Preserve protected boundaries.** Maintain scientific blindness, frozen-result and final-holdout protections, safe evidence handling, exact single-use authorization, replay rejection, and existing fail-closed conditions.

These principles guide evaluation; they do **not** dictate a particular logging framework, state-machine redesign, test harness, or code correction before the assessment.

## 4. Required Engineering Gap Assessment

The next substantive engineering assignment, **only when separately authorized**, must inspect the existing implementation and permitted evidence and return six bounded deliverables. The six questions form a QTRP-specific assessment structure applying established engineering practices—not a new formal industry framework or six additional governance gates.

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

The assessment output should be **one evidence-backed implementation recommendation** with bounded scope, focused acceptance tests, remaining uncertainties, and genuine Owner decisions. It must not begin technical corrections merely because this reference exists.

## 5. Prospective path and completion discipline

**Established philosophy → authorized focused Engineering Gap Assessment → evidence-based technical plan → separately authorized bounded NONPRODUCTION corrections → decisive integration and fault-injection tests → independent engineering review → separate Owner decision on any REAL continuation.**

Use existing MAIN → MANAGING → OWNER routing, with ADMIN for escalated architectural, governance, or scientific review. The assessment and later implementation require their own applicable authorizations; this document supplies none. Future engineering acceptance must establish only what its direct tests and permitted evidence support, with unresolved failures and terminal incompleteness disclosed rather than relabeled as success.

Do not create additional standing documents, task trackers, approval procedures, or broad review layers to implement this reference. Keep work execution-forward and proportionate to demonstrated gaps.
