#!/usr/bin/env python3
"""Self-contained successor E1 V1 semantic rules.

Identity: C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1

Historical V3/V4 is lineage only. This generic implementation remains
fail-closed, NOT_READY, and NOT_AUTHORIZED.
"""
from __future__ import annotations

CONTRACT_FAMILY = "C3_E1_SUCCESSOR_ACCEPTANCE_CONTRACT_V1"
RULE_SET_IDENTITY = "C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1"
SCHEMA_IDENTITY = "C3_E1_SUCCESSOR_CLOSED_EVIDENCE_SCHEMA_V1"
GENERIC_IMPLEMENTATION_STATUS = "STATIC_GENERIC_FAIL_CLOSED_IMPLEMENTATION_ONLY"
GENERIC_PRE_EXECUTION_READINESS = "NOT_READY"
GENERIC_EXECUTION_AUTHORIZATION = "NOT_AUTHORIZED"

REQUIRED_GENERIC_MISSING_ADAPTERS = {
    "runtime_instantiation_attestation_adapter",
    "observation_authority_observation_adapter",
    "transition_event_evidence_adapter",
}
GATE_VALUES = {"PASS", "FAIL", "INCONCLUSIVE", "NOT_EXECUTED"}
FAIL_TERMINALS = {
    "FAIL_CONFIGURATION",
    "FAIL_ENVIRONMENT_IDENTITY_MISMATCH",
    "FAIL_OBSERVATION_INVARIANT",
    "FAIL_VALIDATION_INSTRUMENT_IDENTITY",
    "FAIL_EVIDENCE_INTEGRITY",
}
REQUIRED_RULE_IDENTITIES = (
    "C3_E1_SUCCESSOR_KERNEL_COMPLETENESS_RULE_V1",
    "C3_E1_SUCCESSOR_KERNEL_CONFIGURATION_BINDING_RULE_V1",
    "C3_E1_SUCCESSOR_FIREWALL_COMPLETENESS_RULE_V1",
    "C3_E1_SUCCESSOR_DETERMINISTIC_ABSENCE_RULE_V1",
    "C3_E1_SUCCESSOR_FIREWALL_STABILITY_RULE_V1",
    "C3_E1_SUCCESSOR_ENVIRONMENT_IDENTITY_RULE_V1",
    "C3_E1_SUCCESSOR_BUILD_PROVENANCE_RULE_V1",
    "C3_E1_SUCCESSOR_BUILD_OUTPUT_BINDING_RULE_V1",
    "C3_E1_SUCCESSOR_RUNTIME_INSTANTIATION_BINDING_RULE_V1",
    "C3_E1_SUCCESSOR_RUNTIME_SPECIFICATION_BINDING_RULE_V1",
    "C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_RULE_V1",
    "C3_E1_SUCCESSOR_NO_MUTATION_RULE_V1",
    "C3_E1_SUCCESSOR_EVIDENCE_INTEGRITY_RULE_V1",
    "C3_E1_SUCCESSOR_TRANSPORT_INTEGRITY_RULE_V1",
    "C3_E1_SUCCESSOR_QUALIFICATION_ROOT_INTEGRITY_RULE_V1",
)

class SemanticRuleError(ValueError):
    pass

def _gate(value, name):
    if value not in GATE_VALUES:
        raise SemanticRuleError(f"{name}: invalid classification {value!r}")
    return value

def _collapse(gates, fail_terminal):
    gates = list(gates)
    if "FAIL" in gates:
        return fail_terminal
    if all(g == "PASS" for g in gates):
        return "PASS"
    return "INCONCLUSIVE"

def evaluate_generic_invariants(r):
    if r["implementation_status"] != GENERIC_IMPLEMENTATION_STATUS:
        return "FAIL_VALIDATION_INSTRUMENT_IDENTITY"
    if r["successor_pre_execution_readiness"] != GENERIC_PRE_EXECUTION_READINESS:
        return "FAIL_OBSERVATION_INVARIANT"
    if r["successor_execution_authorization"] != GENERIC_EXECUTION_AUTHORIZATION:
        return "FAIL_OBSERVATION_INVARIANT"
    if not REQUIRED_GENERIC_MISSING_ADAPTERS.issubset(set(r["missing_future_adapters"])):
        return "FAIL_OBSERVATION_INVARIANT"
    return "PASS"

def evaluate_implementation_identity(r):
    g = _gate(r["implementation_identity_binding"]["component_identity_gate"], "component_identity_gate")
    if g == "FAIL":
        return "FAIL_VALIDATION_INSTRUMENT_IDENTITY"
    return g

def evaluate_environment_identity(r):
    a = r["build_provenance"]["frozen_build_output_identity"]
    b = r["governed_runtime_instantiation_binding"]["frozen_build_output_identity"]
    return "PASS" if a == b else "FAIL_ENVIRONMENT_IDENTITY_MISMATCH"

def evaluate_build_provenance(r):
    b = r["build_provenance"]
    return _collapse(
        [_gate(b[k], k) for k in ("build_provenance_integrity","reconstructability","build_output_binding")],
        "FAIL_EVIDENCE_INTEGRITY",
    )

def _started_gate_with_optional_evidence(started, gate, evidence_present, name, fail_terminal):
    """Enforce truthful NOT_EXECUTED/INCONCLUSIVE/PASS state for one observation."""
    g = _gate(gate, name)
    if not started:
        if evidence_present or g != "NOT_EXECUTED":
            return "FAIL_OBSERVATION_INVARIANT"
        return "NOT_EXECUTED"
    if not evidence_present:
        if g != "INCONCLUSIVE":
            return "FAIL_CONFIGURATION"
        return "INCONCLUSIVE"
    if g == "NOT_EXECUTED":
        return "FAIL_CONFIGURATION"
    if g == "FAIL":
        return fail_terminal
    return g


def evaluate_runtime_specification(r):
    x = r["runtime_specification_binding"]
    return _started_gate_with_optional_evidence(
        r["empirical_observation_started"],
        x["classification"],
        x["observed_runtime_manifest_sha256"] is not None,
        "runtime_specification_binding",
        "FAIL_ENVIRONMENT_IDENTITY_MISMATCH",
    )


def evaluate_runtime_instantiation(r):
    x = r["governed_runtime_instantiation_binding"]
    present = (
        x["launch_or_instantiation_evidence_sha256"] is not None
        and x["runtime_instance_identity_sha256"] is not None
        and x["binding_method_identity"] is not None
    )
    # Partial population is contradictory rather than silently incomplete.
    parts = (
        x["launch_or_instantiation_evidence_sha256"],
        x["runtime_instance_identity_sha256"],
        x["binding_method_identity"],
    )
    if any(v is not None for v in parts) and not all(v is not None for v in parts):
        return "FAIL_CONFIGURATION"
    return _started_gate_with_optional_evidence(
        r["empirical_observation_started"],
        x["classification"],
        present,
        "runtime_instantiation_binding",
        "FAIL_ENVIRONMENT_IDENTITY_MISMATCH",
    )


def evaluate_kernel(r):
    """Derive kernel result from evidence identities before claimed gate labels."""
    k = r["kernel_evidence"]
    expected = k["expected"]
    observed = k["observed"]
    started = r["empirical_observation_started"]

    dimensions = (
        ("kernel_release", "kernel_release_binding"),
        ("exact_running_kernel_image_sha256", "running_kernel_image_binding"),
        ("kernel_configuration_sha256", "kernel_configuration_binding"),
        ("required_config_m_module_manifest_sha256", "required_config_m_module_completeness"),
    )
    derived = []
    for identity_field, gate_field in dimensions:
        exp = expected[identity_field]
        obs = observed[identity_field]
        claimed = _gate(k[gate_field], gate_field)
        if not started:
            if obs is not None or claimed != "NOT_EXECUTED":
                return "FAIL_OBSERVATION_INVARIANT"
            derived.append("NOT_EXECUTED")
            continue
        if obs is None:
            if claimed != "INCONCLUSIVE":
                return "FAIL_CONFIGURATION"
            derived.append("INCONCLUSIVE")
            continue
        if obs != exp:
            return "FAIL_CONFIGURATION"
        if claimed == "FAIL":
            return "FAIL_CONFIGURATION"
        if claimed == "PASS":
            derived.append("PASS")
        elif claimed == "INCONCLUSIVE":
            derived.append("INCONCLUSIVE")
        else:
            return "FAIL_CONFIGURATION"

    complete = _gate(k["kernel_completeness"], "kernel_completeness")
    if not started:
        return "NOT_EXECUTED" if complete == "NOT_EXECUTED" else "FAIL_CONFIGURATION"
    if "INCONCLUSIVE" in derived:
        return "INCONCLUSIVE" if complete == "INCONCLUSIVE" else "FAIL_CONFIGURATION"
    if all(x == "PASS" for x in derived):
        if complete == "PASS": return "PASS"
        if complete == "INCONCLUSIVE": return "INCONCLUSIVE"
        return "FAIL_CONFIGURATION"
    raise SemanticRuleError("unreachable kernel semantic state")


def evaluate_firewall(r):
    f = r["firewall_evidence"]
    started = r["empirical_observation_started"]
    evidence_present = f["observed_scope_manifest_sha256"] is not None and f["evidence_sha256"] is not None
    if (f["observed_scope_manifest_sha256"] is None) != (f["evidence_sha256"] is None):
        return "FAIL_CONFIGURATION"
    gates = [_gate(f[k], f"firewall.{k}") for k in ("completeness","stability","deterministic_absence")]
    if not started:
        if evidence_present or any(g != "NOT_EXECUTED" for g in gates):
            return "FAIL_OBSERVATION_INVARIANT"
        return "NOT_EXECUTED"
    if not evidence_present:
        return "INCONCLUSIVE" if all(g == "INCONCLUSIVE" for g in gates) else "FAIL_CONFIGURATION"
    if any(g == "NOT_EXECUTED" for g in gates): return "FAIL_CONFIGURATION"
    if "FAIL" in gates: return "FAIL_CONFIGURATION"
    return "PASS" if all(g == "PASS" for g in gates) else "INCONCLUSIVE"


def evaluate_authority(r):
    a = r["observation_authority_evidence"]
    started = r["empirical_observation_started"]
    gates = [_gate(a[k], k) for k in ("authority_identity_binding","no_privilege_transition")]
    present = a["observed_authority_evidence_sha256"] is not None
    if not started:
        if present or any(g != "NOT_EXECUTED" for g in gates): return "FAIL_OBSERVATION_INVARIANT"
        return "NOT_EXECUTED"
    if not present:
        return "INCONCLUSIVE" if all(g == "INCONCLUSIVE" for g in gates) else "FAIL_CONFIGURATION"
    if any(g == "NOT_EXECUTED" for g in gates): return "FAIL_CONFIGURATION"
    if "FAIL" in gates: return "FAIL_OBSERVATION_INVARIANT"
    return "PASS" if all(g == "PASS" for g in gates) else "INCONCLUSIVE"


def evaluate_no_mutation(r):
    m = r["governed_environment_mutation_gate"]
    started = r["empirical_observation_started"]
    names = (
        "package_acquisition_observation","package_installation_observation",
        "package_upgrade_observation","kernel_change_observation",
        "module_mutation_observation","firewall_mutation_observation",
        "environment_reconfiguration_observation","authority_transition_observation",
    )
    sub = [_gate(m[n], n) for n in names]
    claimed = _gate(m["classification"], "mutation.classification")
    present = m["evidence_sha256"] is not None
    if not started:
        if present or claimed != "NOT_EXECUTED" or any(g != "NOT_EXECUTED" for g in sub):
            return "FAIL_OBSERVATION_INVARIANT"
        return "NOT_EXECUTED"
    if not present:
        if claimed == "INCONCLUSIVE" and all(g == "INCONCLUSIVE" for g in sub): return "INCONCLUSIVE"
        return "FAIL_CONFIGURATION"
    if claimed == "NOT_EXECUTED" or any(g == "NOT_EXECUTED" for g in sub): return "FAIL_CONFIGURATION"
    if claimed == "FAIL" or "FAIL" in sub: return "FAIL_OBSERVATION_INVARIANT"
    return "PASS" if claimed == "PASS" and all(g == "PASS" for g in sub) else "INCONCLUSIVE"


def evaluate_evidence_integrity(r):
    e = r["evidence_integrity"]
    started = r["empirical_observation_started"]
    gates = [_gate(e[k], k) for k in ("content_address_integrity","evidence_completeness","evidence_stability")]
    present = e["evidence_manifest_sha256"] is not None
    if not started:
        if present or any(g != "NOT_EXECUTED" for g in gates): return "FAIL_OBSERVATION_INVARIANT"
        return "NOT_EXECUTED"
    if not present:
        return "INCONCLUSIVE" if all(g == "INCONCLUSIVE" for g in gates) else "FAIL_CONFIGURATION"
    if any(g == "NOT_EXECUTED" for g in gates): return "FAIL_CONFIGURATION"
    if "FAIL" in gates: return "FAIL_EVIDENCE_INTEGRITY"
    return "PASS" if all(g == "PASS" for g in gates) else "INCONCLUSIVE"


def evaluate_transport(r):
    t = r["transport_binding"]
    return _started_gate_with_optional_evidence(
        r["empirical_observation_started"],
        t["transport_integrity"],
        t["transport_manifest_sha256"] is not None,
        "transport_integrity",
        "FAIL_EVIDENCE_INTEGRITY",
    )


def evaluate_qualification_root_state(r):
    """Validate observation-state truthfulness only; cryptographic root is validator-derived."""
    q = r["qualification_root_binding"]
    return _started_gate_with_optional_evidence(
        r["empirical_observation_started"],
        q["qualification_root_integrity"],
        q["successor_environment_qualification_root_sha256"] is not None,
        "qualification_root_integrity",
        "FAIL_EVIDENCE_INTEGRITY",
    )


def evaluate_non_root(r):
    return {
        "generic_invariants": evaluate_generic_invariants(r),
        "implementation_identity": evaluate_implementation_identity(r),
        "environment_identity": evaluate_environment_identity(r),
        "build_provenance": evaluate_build_provenance(r),
        "runtime_specification": evaluate_runtime_specification(r),
        "runtime_instantiation": evaluate_runtime_instantiation(r),
        "kernel": evaluate_kernel(r),
        "firewall": evaluate_firewall(r),
        "observation_authority": evaluate_authority(r),
        "no_mutation": evaluate_no_mutation(r),
        "evidence_integrity": evaluate_evidence_integrity(r),
        "transport_integrity": evaluate_transport(r),
    }


def derive_terminal(r, gates):
    terminal = None
    for v in gates.values():
        if v in FAIL_TERMINALS:
            terminal = v; break
        if v == "FAIL":
            terminal = "FAIL_OBSERVATION_INVARIANT"; break
    if terminal is None:
        if not r["empirical_observation_started"]:
            terminal = "NOT_EXECUTED"
        elif REQUIRED_GENERIC_MISSING_ADAPTERS.issubset(set(r["missing_future_adapters"])):
            terminal = "INCONCLUSIVE"
        elif any(v in ("INCONCLUSIVE","NOT_EXECUTED") for v in gates.values()):
            terminal = "INCONCLUSIVE"
        elif all(v == "PASS" for v in gates.values()):
            terminal = "PASS"
        else:
            terminal = "FAIL_OBSERVATION_INVARIANT"
    if terminal == "PASS" and (
        r["successor_pre_execution_readiness"] != "READY_FOR_OWNER_EXECUTION_DECISION"
        or r["successor_execution_authorization"] != "EXPLICIT_SINGLE_EXECUTION_AUTHORIZED"
    ):
        raise SemanticRuleError("PASS prohibited by readiness/authorization state")
    return terminal


def evaluate_all(r, verified_qualification_root=None):
    gates = evaluate_non_root(r)
    root_state = evaluate_qualification_root_state(r)
    if root_state in FAIL_TERMINALS:
        root_result = root_state
    elif root_state in ("NOT_EXECUTED", "INCONCLUSIVE"):
        root_result = root_state
    elif root_state == "PASS":
        if verified_qualification_root is True:
            root_result = "PASS"
        elif verified_qualification_root is False:
            root_result = "FAIL_EVIDENCE_INTEGRITY"
        else:
            # Claimed PASS cannot prove itself; without independent digest verification it stays unresolved.
            root_result = "INCONCLUSIVE"
    else:
        root_result = "FAIL_OBSERVATION_INVARIANT"
    gates["qualification_root_integrity"] = root_result
    return {"gates": gates, "terminal": derive_terminal(r, gates)}

def self_test():
    assert len(REQUIRED_RULE_IDENTITIES) == 15
    assert GENERIC_PRE_EXECUTION_READINESS == "NOT_READY"
    assert GENERIC_EXECUTION_AUTHORIZATION == "NOT_AUTHORIZED"
    return {
        "self_contained_rule_inventory": "PASS",
        "generic_fail_closed_constants": "PASS",
    }

if __name__ == "__main__":
    import json
    print(json.dumps(self_test(), sort_keys=True))
