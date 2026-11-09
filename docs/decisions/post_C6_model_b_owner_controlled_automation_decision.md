# Post-C6 Model B — Owner-Controlled Automation Decision

**Date:** 2026-11-09  
**Decision:** Owner adoption of Model B — Owner-Controlled Automation.  
**Decision authority:** Owner; expressly adopted under `QTRP_MODEL_B_OWNER_POLICY_DECISION_V1`. **Documentation preparation:** MAIN/Codex under `QTRP_MODEL_B_CONSOLIDATED_DOCUMENTATION_PREPARATION_V1`; ADMIN reviewed the publication strategy.

This proposed record is prepared for MAIN independent review; publication requires separate authorization.

## Adopted operating assumption

Following the completed proportionality review, the Owner adopted Model B for
cooperative, Owner-initiated operation in a noncompromised environment. The Owner
accepts reduced protection against malicious or compromised execution at the
same privilege level.

Root-executed Python and separate OS identities are no longer mandatory future
architectural requirements solely to defend against that stronger adversarial
model. This policy decision does not establish a trusted runtime, prove OS
separation, or qualify an unprivileged replacement. The observed writable-runtime
failure remains a failure for the proposed root Python bootstrap.

Existing implementation controls remain effective. This record authorizes no
engineering or security-control bypass. Replacing those controls requires
separately authorized implementation and qualification within the adopted policy.

## Preserved requirements

- Explicit Owner authority remains necessary; an executor cannot authorize
  itself. Preserve single-use authority, exact bindings and replay rejection.
- Bind the exact input, source, runtime, configuration, policy, unit and attempt
  identities. A manual command or AI-generated approval supplies no execution
  authority by itself.
- Preserve exactly 25 records per unit, bounded retry and unit limits,
  `MAX_NEW_UNITS=1`, and the U0013 prohibition. Consumed Attempt 10 authority is
  not reusable; no additional retry is granted here.
- Preserve complete event capture, Policy B and its reason precedence,
  deterministic scientific validation and acceptance. A process return code
  alone does not establish scientific acceptance.
- Protect frozen scientific data and accepted U0001–U0011 results (275 records),
  chronological independence, and training/validation/holdout isolation. This
  record grants no protected-data access.
- Preserve checkpoint 54 ancestry, U0012 pending after ten historical attempts,
  and the requirement to establish recovery compatibility. Policy adoption
  neither proves continuity nor creates a new recovery lineage.
- Preserve staging, readback, proof verification and fail-closed acceptance;
  failure, interruption, ambiguous evidence or replay must not advance accepted
  checkpoint state.

## Remaining REAL-readiness boundaries

The [bounded synthetic integration closure](../reports/QTRP_Model_B_Controlled_Stop_Closure_2026-11-09.md)
records a stop before implementation. Child invocation, 25-record processing,
capture, validation, proof, checkpoint finalization and replay qualification were
not reached. Owner policy adoption does not convert that stop into integration
or scientific acceptance.

Authoritative current recovery compatibility and provenance, the applicable
protected-access authority, complete prospective Attempt 11 configuration and
execution bindings, runtime qualification under the adopted policy, and final
pre-REAL readiness remain prerequisites. They are not established by this
documentation task. No new authorization candidate is published or consumed.

```text
MODEL_B_POLICY = OWNER_ADOPTED
C06 = CONTROLLED_STOP
CHECKPOINT = 54
U0012 = PENDING__TEN_HISTORICAL_ATTEMPTS
REAL_ACTIVATION = HARD_DISABLED
ATTEMPT11_REAL = NOT_AUTHORIZED
U0013 = PROHIBITED
```

This record grants no REAL authorization, deployment or execution.
[PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) remains controlling for broad
current lifecycle state and authorization boundaries. The
[Milestone Review Reference Map](../workflows/milestone_review_reference_map.md)
remains nonauthorizing.

## Historical context

The [November 9 consolidated research findings](../reports/QTRP_Deep_Research_Consolidated_Findings_2026-11-09.md)
and the integration closure retain their original bytes and decision-time
limitations. Their pending-review and next-decision language predates the
completed proportionality review and explicit Owner adoption recorded here.
Neither historical report grants current implementation or execution authority.
