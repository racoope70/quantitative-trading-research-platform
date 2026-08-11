#!/usr/bin/env python3
"""Successor E1 V1 structural + semantic validator.

Identity: C3_E1_SUCCESSOR_SEMANTIC_VALIDATOR_V1

Manifest-declared component bytes are verified before the canonicalizer or
semantic rule module is imported. Schema validity alone never yields a
scientific PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
SCHEMA_PATH = HERE / "C3_E1_SUCCESSOR_CLOSED_EVIDENCE_SCHEMA_V1.json"
RULES_PATH = HERE / "C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1.py"
CANON_PATH = HERE / "canonical_json_v1.py"
COLLECTOR_PATH = HERE / "successor_e1_collector_v1.py"
VALIDATOR_PATH = HERE / "successor_e1_validator_v1.py"
MANIFEST_PATH = HERE / "contract_implementation_manifest_v1.json"
VALIDATOR_IDENTITY = "C3_E1_SUCCESSOR_SEMANTIC_VALIDATOR_V1"

EXPECTED_COMPONENT_PATHS = {
    ".github/c3-e1-successor-v1/C3_E1_SUCCESSOR_CLOSED_EVIDENCE_SCHEMA_V1.json":
        "C3_E1_SUCCESSOR_CLOSED_EVIDENCE_SCHEMA_V1",
    ".github/c3-e1-successor-v1/C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1.py":
        "C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1",
    ".github/c3-e1-successor-v1/canonical_json_v1.py":
        "C3_E1_SUCCESSOR_CANONICAL_JSON_V1",
    ".github/c3-e1-successor-v1/successor_e1_collector_v1.py":
        "C3_E1_SUCCESSOR_GENERIC_COLLECTOR_V1",
    ".github/c3-e1-successor-v1/successor_e1_validator_v1.py":
        "C3_E1_SUCCESSOR_SEMANTIC_VALIDATOR_V1",
}
SUPPORTED_SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
INT64_MAX = 9223372036854775807

SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema", "$defs", "$ref", "type", "properties", "required",
    "additionalProperties", "items", "minItems", "maxItems",
    "enum", "const", "pattern", "minimum", "maximum",
}
SUPPORTED_PATTERNS = {
    "^[0-9a-f]{64}$",
    "^[0-9a-f]{40}$",
    "^[A-Za-z0-9_]+$",
}
DEF_NAME_RE = re.compile(r"^[A-Za-z0-9_]+$", re.ASCII)
REF_RE = re.compile(r"^#/\$defs/([A-Za-z0-9_]+)$", re.ASCII)

class ValidationInstrumentFailure(RuntimeError): pass
class EvidenceValidationError(ValueError): pass

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _strict_manifest_load(raw: bytes) -> dict:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as e:
        raise ValidationInstrumentFailure(f"manifest UTF-8 failure: {e}") from e
    if text.startswith("\ufeff"):
        raise ValidationInstrumentFailure("manifest BOM prohibited")
    def hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValidationInstrumentFailure(f"duplicate manifest key: {k}")
            out[k] = v
        return out
    try:
        def parse_manifest_int(token):
            value = int(token, 10)
            if value < -9223372036854775808 or value > INT64_MAX:
                raise ValidationInstrumentFailure(f"manifest integer outside signed-int64 domain: {token}")
            return value
        obj = json.loads(
            text,
            object_pairs_hook=hook,
            parse_int=parse_manifest_int,
            parse_float=lambda s: (_ for _ in ()).throw(
                ValidationInstrumentFailure(f"manifest float prohibited: {s}")
            ),
            parse_constant=lambda s: (_ for _ in ()).throw(
                ValidationInstrumentFailure(f"manifest non-finite prohibited: {s}")
            ),
        )
    except json.JSONDecodeError as e:
        raise ValidationInstrumentFailure(f"manifest JSON failure: {e}") from e
    if not isinstance(obj, dict):
        raise ValidationInstrumentFailure("manifest root must be object")
    return obj

def verify_manifest_component_bytes() -> dict:
    manifest = _strict_manifest_load(MANIFEST_PATH.read_bytes())
    expected_top = {
        "manifest_identity", "contract_family", "implementation_scope",
        "successor_pre_execution_readiness", "successor_execution_authorization",
        "canonicalization", "files", "deferred",
    }
    if set(manifest) != expected_top:
        raise ValidationInstrumentFailure("unexpected implementation manifest top-level fields")
    if manifest.get("manifest_identity") != "C3_E1_SUCCESSOR_CONTRACT_IMPLEMENTATION_MANIFEST_V1":
        raise ValidationInstrumentFailure("manifest identity mismatch")
    if manifest.get("contract_family") != "C3_E1_SUCCESSOR_ACCEPTANCE_CONTRACT_V1":
        raise ValidationInstrumentFailure("manifest contract mismatch")
    if manifest.get("implementation_scope") != "STATIC_GENERIC_FAIL_CLOSED_IMPLEMENTATION_ONLY":
        raise ValidationInstrumentFailure("manifest scope mismatch")
    if manifest.get("successor_pre_execution_readiness") != "NOT_READY":
        raise ValidationInstrumentFailure("generic readiness drift")
    if manifest.get("successor_execution_authorization") != "NOT_AUTHORIZED":
        raise ValidationInstrumentFailure("generic authorization drift")

    canonicalization = manifest.get("canonicalization")
    if not isinstance(canonicalization, dict) or set(canonicalization) != {
        "identity", "normalization_form", "normalization_provider", "unicode_data_version"
    }:
        raise ValidationInstrumentFailure("canonicalization manifest shape mismatch")
    deferred = manifest.get("deferred")
    expected_deferred = {
        "specific_VM_platform", "specific_observation_authority_mechanism",
        "CAP_NET_ADMIN_sufficiency", "transition_event_provider",
        "runtime_instantiation_attestation_adapter",
        "observation_authority_observation_adapter",
        "transition_event_evidence_adapter",
        "platform_build_output_identity_adapter_if_required",
        "future_successor_caller",
    }
    if not isinstance(deferred, dict) or set(deferred) != expected_deferred:
        raise ValidationInstrumentFailure("deferred manifest shape mismatch")

    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ValidationInstrumentFailure("manifest files must be array")
    if any(not isinstance(e, dict) for e in entries):
        raise ValidationInstrumentFailure("manifest component entry must be object")
    paths = [e.get("path") for e in entries]
    if len(paths) != len(set(paths)):
        raise ValidationInstrumentFailure("duplicate component path")
    if set(paths) != set(EXPECTED_COMPONENT_PATHS):
        raise ValidationInstrumentFailure("exact component path set mismatch")

    for e in entries:
        if set(e) != {"path", "sha256", "byte_count"}:
            raise ValidationInstrumentFailure("unexpected component manifest fields")
        rel = e["path"]
        p = REPO_ROOT / rel
        if not p.is_file() or p.is_symlink():
            raise ValidationInstrumentFailure(f"component absent/not regular: {rel}")
        if (
            not isinstance(e["byte_count"], int)
            or isinstance(e["byte_count"], bool)
            or e["byte_count"] < 0
            or e["byte_count"] > INT64_MAX
        ):
            raise ValidationInstrumentFailure(f"invalid component byte_count: {rel}")
        if not isinstance(e["sha256"], str) or len(e["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in e["sha256"]):
            raise ValidationInstrumentFailure(f"invalid component sha256: {rel}")
        if p.stat().st_size != e["byte_count"]:
            raise ValidationInstrumentFailure(
                f"VALIDATION_INSTRUMENT_IDENTITY_FAILURE byte_count: {rel}"
            )
        if sha256_file(p) != e["sha256"]:
            raise ValidationInstrumentFailure(
                f"VALIDATION_INSTRUMENT_IDENTITY_FAILURE sha256: {rel}"
            )
        text = p.read_text(encoding="utf-8")
        if EXPECTED_COMPONENT_PATHS[rel] not in text:
            raise ValidationInstrumentFailure(
                f"VALIDATION_INSTRUMENT_IDENTITY_FAILURE declared identity: {rel}"
            )
    return manifest

def _load_verified_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValidationInstrumentFailure(f"cannot load {path}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

# CRITICAL ORDER: verify all five component bytes BEFORE importing CANON/RULES.
_BOOTSTRAP_MANIFEST = verify_manifest_component_bytes()
CANON = _load_verified_module("c3_succ_canon", CANON_PATH)
RULES = _load_verified_module("c3_succ_rules", RULES_PATH)

def verify_manifest_semantics() -> dict:
    # Reparse with the now-verified canonicalizer and ensure the same manifest
    # remains valid under frozen canonical JSON rules.
    m = CANON.load_strict_bytes(MANIFEST_PATH.read_bytes())
    if not isinstance(m, dict) or m != _BOOTSTRAP_MANIFEST:
        raise ValidationInstrumentFailure("canonical manifest parse mismatch")
    cfg = m.get("canonicalization")
    if not isinstance(cfg, dict):
        raise ValidationInstrumentFailure("canonicalization manifest missing")
    if cfg.get("identity") != "C3_E1_SUCCESSOR_CANONICAL_JSON_V1":
        raise ValidationInstrumentFailure("canonicalizer identity mismatch")
    if cfg.get("normalization_form") != "NFC":
        raise ValidationInstrumentFailure("normalization form mismatch")
    if cfg.get("normalization_provider") != "python-unicodedata":
        raise ValidationInstrumentFailure("normalization provider mismatch")
    if cfg.get("unicode_data_version") != CANON.UNICODE_DATA_VERSION:
        raise ValidationInstrumentFailure("Unicode database mismatch")
    return m

def _schema_children(node):
    out = []
    if isinstance(node.get("properties"), dict):
        out += [x for x in node["properties"].values() if isinstance(x, dict)]
    if isinstance(node.get("$defs"), dict):
        out += [x for x in node["$defs"].values() if isinstance(x, dict)]
    if isinstance(node.get("items"), dict):
        out.append(node["items"])
    return out

def prevalidate_schema(schema):
    if not isinstance(schema, dict) or not isinstance(schema.get("$defs"), dict):
        raise ValidationInstrumentFailure("invalid schema root/$defs")
    if schema.get("$schema") != SUPPORTED_SCHEMA_URI:
        raise ValidationInstrumentFailure("unsupported $schema URI")
    defs = schema["$defs"]
    for name in defs:
        if DEF_NAME_RE.fullmatch(name) is None or "/" in name or "~" in name:
            raise ValidationInstrumentFailure(f"unsupported definition name {name!r}")

    ref_edges = {name: set() for name in defs}

    def walk(node, root=False, owner=None):
        unknown = set(node) - SUPPORTED_SCHEMA_KEYWORDS
        if unknown:
            raise ValidationInstrumentFailure(f"unsupported schema keywords {sorted(unknown)}")
        if "$schema" in node and not root:
            raise ValidationInstrumentFailure("nested $schema prohibited")
        declared_type = node.get("type")
        if declared_type is not None:
            declared_types = declared_type if isinstance(declared_type, list) else [declared_type]
            if not declared_types or not all(isinstance(x, str) for x in declared_types):
                raise ValidationInstrumentFailure("schema type must be string or nonempty string array")
            if len(declared_types) != len(set(declared_types)):
                raise ValidationInstrumentFailure("duplicate schema type prohibited")
            allowed_types = {"null", "boolean", "integer", "string", "array", "object"}
            if any(x not in allowed_types for x in declared_types):
                raise ValidationInstrumentFailure("unsupported schema type")
        if "properties" in node:
            if not isinstance(node["properties"], dict) or any(not isinstance(k, str) or not isinstance(v, dict) for k,v in node["properties"].items()):
                raise ValidationInstrumentFailure("properties must map strings to schema objects")
        if "required" in node:
            req = node["required"]
            if not isinstance(req, list) or any(not isinstance(x, str) for x in req) or len(req) != len(set(req)):
                raise ValidationInstrumentFailure("required must be unique string array")
        if "additionalProperties" in node and not isinstance(node["additionalProperties"], bool):
            raise ValidationInstrumentFailure("additionalProperties must be boolean")
        if "items" in node and not isinstance(node["items"], dict):
            raise ValidationInstrumentFailure("items must be schema object")
        for item_key in ("minItems", "maxItems"):
            if item_key in node and (not isinstance(node[item_key], int) or isinstance(node[item_key], bool) or node[item_key] < 0 or node[item_key] > INT64_MAX):
                raise ValidationInstrumentFailure(f"{item_key} must be nonnegative int64")
        if "minItems" in node and "maxItems" in node and node["minItems"] > node["maxItems"]:
            raise ValidationInstrumentFailure("minItems exceeds maxItems")
        if "pattern" in node and (not isinstance(node["pattern"], str) or node["pattern"] not in SUPPORTED_PATTERNS):
            raise ValidationInstrumentFailure(f"unsupported pattern {node['pattern']!r}")
        if "$ref" in node and not root and set(node) != {"$ref"}:
            raise ValidationInstrumentFailure("$ref siblings unsupported in frozen subset")
        if "minimum" in node and (not isinstance(node["minimum"], int) or isinstance(node["minimum"], bool)):
            raise ValidationInstrumentFailure("minimum must be integer")
        if "maximum" in node and (not isinstance(node["maximum"], int) or isinstance(node["maximum"], bool)):
            raise ValidationInstrumentFailure("maximum must be integer")
        if "minimum" in node and "maximum" in node and node["minimum"] > node["maximum"]:
            raise ValidationInstrumentFailure("minimum exceeds maximum")
        declared_types = declared_type if isinstance(declared_type, list) else [declared_type]
        if "integer" in declared_types:
            if "minimum" not in node or "maximum" not in node:
                raise ValidationInstrumentFailure("integer schema requires explicit minimum and maximum")
            if node["minimum"] < -9223372036854775808 or node["maximum"] > INT64_MAX:
                raise ValidationInstrumentFailure("integer schema bounds outside signed-int64 domain")
        if "$ref" in node:
            ref = node["$ref"]
            m = REF_RE.fullmatch(ref) if isinstance(ref, str) else None
            if not m:
                raise ValidationInstrumentFailure(f"unsupported $ref {ref!r}")
            target = m.group(1)
            if target not in defs:
                raise ValidationInstrumentFailure(f"unresolved $ref {ref!r}")
            if owner is not None:
                ref_edges[owner].add(target)
        if "$defs" in node and not root:
            raise ValidationInstrumentFailure("nested $defs prohibited")
        if isinstance(node.get("properties"), dict):
            for child in node["properties"].values():
                if isinstance(child, dict): walk(child, False, owner)
        if isinstance(node.get("items"), dict):
            walk(node["items"], False, owner)

    # Root structure excluding definitions, then every definition with edge attribution.
    root_copy = {k: v for k, v in schema.items() if k != "$defs"}
    walk(root_copy, True, None)
    for name, definition in defs.items():
        if not isinstance(definition, dict):
            raise ValidationInstrumentFailure("$defs value must be object")
        walk(definition, False, name)

    visiting = set()
    visited = set()
    def dfs(name):
        if name in visiting:
            raise ValidationInstrumentFailure("cyclic local $ref graph prohibited")
        if name in visited:
            return
        visiting.add(name)
        for target in ref_edges[name]:
            dfs(target)
        visiting.remove(name)
        visited.add(name)
    for name in defs:
        dfs(name)

def _resolve_ref(ref, root):
    m = REF_RE.fullmatch(ref)
    if not m or m.group(1) not in root["$defs"]:
        raise ValidationInstrumentFailure(f"unresolved/unsupported $ref {ref!r}")
    return root["$defs"][m.group(1)]

def _pattern_match(pattern, value):
    if pattern == "^[0-9a-f]{64}$":
        return len(value) == 64 and all(c in "0123456789abcdef" for c in value)
    if pattern == "^[0-9a-f]{40}$":
        return len(value) == 40 and all(c in "0123456789abcdef" for c in value)
    if pattern == "^[A-Za-z0-9_]+$":
        return bool(value) and all(
            ("A" <= c <= "Z") or ("a" <= c <= "z")
            or ("0" <= c <= "9") or c == "_" for c in value
        )
    raise ValidationInstrumentFailure("unsupported pattern")

def _type_ok(value, expected):
    if expected == "null": return value is None
    if expected == "boolean": return isinstance(value, bool)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "string": return isinstance(value, str)
    if expected == "array": return isinstance(value, list)
    if expected == "object": return isinstance(value, dict)
    raise ValidationInstrumentFailure(f"unsupported type {expected}")

def validate_instance(value, schema, root, path="$"):
    if "$ref" in schema:
        return validate_instance(value, _resolve_ref(schema["$ref"], root), root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not all(isinstance(x, str) for x in types):
            raise ValidationInstrumentFailure("non-string schema type")
        if not any(_type_ok(value, x) for x in types):
            raise EvidenceValidationError(f"{path}: type mismatch")
        if value is None: return
    if "enum" in schema and value not in schema["enum"]:
        raise EvidenceValidationError(f"{path}: enum mismatch")
    if "const" in schema and value != schema["const"]:
        raise EvidenceValidationError(f"{path}: const mismatch")
    if isinstance(value, str) and "pattern" in schema and not _pattern_match(schema["pattern"], value):
        raise EvidenceValidationError(f"{path}: pattern mismatch")
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise EvidenceValidationError(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            raise EvidenceValidationError(f"{path}: above maximum")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise EvidenceValidationError(f"{path}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise EvidenceValidationError(f"{path}: too many items")
        if "items" in schema:
            for i, item in enumerate(value):
                validate_instance(item, schema["items"], root, f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in value: raise EvidenceValidationError(f"{path}: missing {k}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(props)
            if extra: raise EvidenceValidationError(f"{path}: extra properties {sorted(extra)}")
        for k, child in props.items():
            if k in value: validate_instance(value[k], child, root, f"{path}.{k}")

def load_schema():
    s = CANON.load_strict_bytes(SCHEMA_PATH.read_bytes())
    if not isinstance(s, dict):
        raise ValidationInstrumentFailure("schema root not object")
    prevalidate_schema(s)
    return s

def _qualification_root_expected(record, non_root_gates):
    """Compute qualification root from evidence and independently evaluated NON-ROOT gates only."""
    root_object = {
        "contract_family": record["contract_family"],
        "implementation_manifest_sha256": record["implementation_identity_binding"]["manifest_sha256"],
        "expected_build_provenance_sha256": record["build_provenance"]["expected_build_provenance_sha256"],
        "frozen_build_output_identity": record["build_provenance"]["frozen_build_output_identity"],
        "admitted_successor_environment_specification_sha256":
            record["runtime_specification_binding"]["admitted_successor_environment_specification_sha256"],
        "runtime_instantiation_evidence_sha256":
            record["governed_runtime_instantiation_binding"]["launch_or_instantiation_evidence_sha256"],
        "observed_runtime_manifest_sha256":
            record["runtime_specification_binding"]["observed_runtime_manifest_sha256"],
        "observation_authority_evidence_sha256":
            record["observation_authority_evidence"]["observed_authority_evidence_sha256"],
        "mutation_evidence_sha256": record["governed_environment_mutation_gate"]["evidence_sha256"],
        "evidence_manifest_sha256": record["evidence_integrity"]["evidence_manifest_sha256"],
        "transport_manifest_sha256": record["transport_binding"]["transport_manifest_sha256"],
        "non_root_semantic_gate_results": non_root_gates,
    }
    if "qualification_root_integrity" in non_root_gates:
        raise ValidationInstrumentFailure("qualification root cannot include its own integrity gate")
    return hashlib.sha256(CANON.canonical_bytes(root_object)).hexdigest()

def validate_record(path: Path):
    manifest = verify_manifest_semantics()
    schema = load_schema()
    record = CANON.load_strict_bytes(path.read_bytes())
    if not isinstance(record, dict):
        raise EvidenceValidationError("record root not object")
    validate_instance(record, schema, schema)

    actual_manifest_sha = sha256_file(MANIFEST_PATH)
    if record["implementation_identity_binding"]["manifest_sha256"] != actual_manifest_sha:
        raise ValidationInstrumentFailure(
            "VALIDATION_INSTRUMENT_IDENTITY_FAILURE manifest binding mismatch"
        )
    if record["implementation_identity_binding"]["component_identity_gate"] != "PASS":
        raise ValidationInstrumentFailure(
            "VALIDATION_INSTRUMENT_IDENTITY_FAILURE record does not affirm verified component gate"
        )

    non_root = RULES.evaluate_non_root(record)
    root_state = RULES.evaluate_qualification_root_state(record)

    claimed_root = record["qualification_root_binding"]["successor_environment_qualification_root_sha256"]
    if root_state == "PASS":
        expected_root = _qualification_root_expected(record, non_root)
        verified_root = claimed_root == expected_root
        if not verified_root:
            raise EvidenceValidationError("qualification root digest mismatch")
    elif root_state in ("NOT_EXECUTED", "INCONCLUSIVE"):
        verified_root = None
    else:
        verified_root = False

    semantic = RULES.evaluate_all(record, verified_qualification_root=verified_root)
    if record["terminal_result"]["classification"] != semantic["terminal"]:
        raise EvidenceValidationError(
            f"terminal mismatch: claimed {record['terminal_result']['classification']}, "
            f"derived {semantic['terminal']}"
        )
    return {
        "structural_validation": "PASS",
        "implementation_manifest_binding": "PASS",
        "semantic_gate_results": semantic["gates"],
        "terminal_classification": semantic["terminal"],
    }

def _generic_record(manifest_sha):
    h = "0" * 64
    bid = {
        "identity_type": "C3_E1_SUCCESSOR_FROZEN_BUILD_OUTPUT_MANIFEST_SHA256_V1",
        "identity_algorithm": "SHA-256",
        "identity_value": h,
    }
    ne = "NOT_EXECUTED"
    return {
        "contract_family": "C3_E1_SUCCESSOR_ACCEPTANCE_CONTRACT_V1",
        "schema_identity": "C3_E1_SUCCESSOR_CLOSED_EVIDENCE_SCHEMA_V1",
        "semantic_rule_set_identity": "C3_E1_SUCCESSOR_CROSS_FIELD_SEMANTIC_RULE_SET_V1",
        "implementation_status": "STATIC_GENERIC_FAIL_CLOSED_IMPLEMENTATION_ONLY",
        "successor_pre_execution_readiness": "NOT_READY",
        "successor_execution_authorization": "NOT_AUTHORIZED",
        "empirical_observation_started": False,
        "implementation_identity_binding": {"manifest_sha256": manifest_sha, "component_identity_gate": "PASS"},
        "build_provenance": {
            "expected_build_provenance_sha256": h,
            "environment_build_record_sha256": h,
            "reconstruction_material_manifest_sha256": h,
            "build_provenance_integrity": ne,
            "reconstructability": ne,
            "build_output_binding": ne,
            "frozen_build_output_identity": bid,
        },
        "runtime_specification_binding": {
            "admitted_successor_environment_specification_sha256": h,
            "observed_runtime_manifest_sha256": None,
            "classification": ne,
        },
        "governed_runtime_instantiation_binding": {
            "classification": ne,
            "frozen_build_output_identity": bid,
            "launch_or_instantiation_evidence_sha256": None,
            "runtime_instance_identity_sha256": None,
            "binding_method_identity": None,
        },
        "kernel_evidence": {
            "expected": {
                "kernel_release": "DEFERRED",
                "exact_running_kernel_image_sha256": h,
                "kernel_configuration_sha256": h,
                "required_config_m_module_manifest_sha256": h,
            },
            "observed": {
                "kernel_release": None,
                "exact_running_kernel_image_sha256": None,
                "kernel_configuration_sha256": None,
                "required_config_m_module_manifest_sha256": None,
            },
            "kernel_release_binding": ne,
            "running_kernel_image_binding": ne,
            "kernel_configuration_binding": ne,
            "required_config_m_module_completeness": ne,
            "kernel_completeness": ne,
        },
        "firewall_evidence": {
            "required_scope_manifest_sha256": h,
            "observed_scope_manifest_sha256": None,
            "completeness": ne, "stability": ne, "deterministic_absence": ne,
            "evidence_sha256": None,
        },
        "observation_authority_evidence": {
            "expected_authority_specification_sha256": h,
            "observed_authority_evidence_sha256": None,
            "authority_identity_binding": ne, "no_privilege_transition": ne,
        },
        "governed_environment_mutation_gate": {
            "classification": ne, "evidence_sha256": None,
            "package_acquisition_observation": ne,
            "package_installation_observation": ne,
            "package_upgrade_observation": ne,
            "kernel_change_observation": ne,
            "module_mutation_observation": ne,
            "firewall_mutation_observation": ne,
            "environment_reconfiguration_observation": ne,
            "authority_transition_observation": ne,
        },
        "evidence_integrity": {
            "evidence_manifest_sha256": None,
            "content_address_integrity": ne,
            "evidence_completeness": ne,
            "evidence_stability": ne,
        },
        "transport_binding": {"transport_manifest_sha256": None, "transport_integrity": ne},
        "qualification_root_binding": {
            "successor_environment_qualification_root_sha256": None,
            "qualification_root_integrity": ne,
        },
        "missing_future_adapters": sorted(RULES.REQUIRED_GENERIC_MISSING_ADAPTERS),
        "historical_boundary": {
            "historical_v3_v4_runtime_dependency": "NO",
            "historical_attempt_reclassification_possible": "NO",
            "attempts_1_through_5": "IMMUTABLE",
        },
        "terminal_result": {"classification": "NOT_EXECUTED", "derived_by_validator": True},
    }

def self_test():
    verify_manifest_semantics()
    schema = load_schema()
    results = {
        "implementation_manifest_component_binding_tests": "PASS",
        "schema_prevalidation_tests": "PASS",
    }
    ct = CANON.self_test()
    if any(v != "PASS" for k, v in ct.items() if k != "unicode_data_version"):
        raise AssertionError(ct)
    results["canonicalization_byte_exact_tests"] = "PASS"
    if any(v != "PASS" for v in RULES.self_test().values()):
        raise AssertionError("semantic rule self-test")
    results["self_contained_semantic_rule_tests"] = "PASS"

    r = _generic_record(sha256_file(MANIFEST_PATH))
    validate_instance(r, schema, schema)
    sem = RULES.evaluate_all(r)
    if sem["terminal"] != "NOT_EXECUTED":
        raise AssertionError("generic terminal")
    observed = r["kernel_evidence"]["observed"]
    if any(observed[name] is not None for name in (
        "kernel_release",
        "exact_running_kernel_image_sha256",
        "kernel_configuration_sha256",
        "required_config_m_module_manifest_sha256",
    )):
        raise AssertionError("NOT_EXECUTED contains synthetic observed kernel identity")
    results["not_executed_has_no_synthetic_observed_kernel_identity"] = "PASS"
    results["generic_schema_plus_semantic_validation"] = "PASS"

    mismatch = _generic_record(sha256_file(MANIFEST_PATH))
    mismatch["empirical_observation_started"] = True
    mismatch["kernel_evidence"]["observed"] = {
        "kernel_release": mismatch["kernel_evidence"]["expected"]["kernel_release"],
        "exact_running_kernel_image_sha256": "1" * 64,
        "kernel_configuration_sha256": mismatch["kernel_evidence"]["expected"]["kernel_configuration_sha256"],
        "required_config_m_module_manifest_sha256": mismatch["kernel_evidence"]["expected"]["required_config_m_module_manifest_sha256"],
    }
    mismatch["kernel_evidence"]["kernel_release_binding"] = "PASS"
    mismatch["kernel_evidence"]["running_kernel_image_binding"] = "INCONCLUSIVE"
    mismatch["kernel_evidence"]["kernel_configuration_binding"] = "PASS"
    mismatch["kernel_evidence"]["required_config_m_module_completeness"] = "PASS"
    mismatch["kernel_evidence"]["kernel_completeness"] = "INCONCLUSIVE"
    if RULES.evaluate_kernel(mismatch) != "FAIL_CONFIGURATION":
        raise AssertionError("direct kernel mismatch was downgraded")
    if RULES.evaluate_all(mismatch)["terminal"] != "FAIL_CONFIGURATION":
        raise AssertionError("kernel mismatch did not propagate to terminal")
    results["direct_kernel_identity_mismatch_is_fail"] = "PASS"

    missing_obs = _generic_record(sha256_file(MANIFEST_PATH))
    missing_obs["empirical_observation_started"] = True
    missing_obs["kernel_evidence"]["observed"] = {
        "kernel_release": None,
        "exact_running_kernel_image_sha256": None,
        "kernel_configuration_sha256": None,
        "required_config_m_module_manifest_sha256": None,
    }
    missing_obs["kernel_evidence"]["kernel_release_binding"] = "INCONCLUSIVE"
    missing_obs["kernel_evidence"]["running_kernel_image_binding"] = "INCONCLUSIVE"
    missing_obs["kernel_evidence"]["kernel_configuration_binding"] = "INCONCLUSIVE"
    missing_obs["kernel_evidence"]["required_config_m_module_completeness"] = "INCONCLUSIVE"
    missing_obs["kernel_evidence"]["kernel_completeness"] = "INCONCLUSIVE"
    if RULES.evaluate_kernel(missing_obs) != "INCONCLUSIVE":
        raise AssertionError("started-but-unobserved kernel did not remain INCONCLUSIVE")
    results["started_unobserved_kernel_identity_is_null_inconclusive"] = "PASS"

    bad = dict(r)
    bad["successor_pre_execution_readiness"] = "READY_FOR_OWNER_EXECUTION_DECISION"
    try:
        validate_instance(bad, schema, schema)
    except EvidenceValidationError:
        pass
    else:
        raise AssertionError("fabricated READY accepted")
    results["fabricated_ready_authorized_record_rejected"] = "PASS"

    # Missing-adapter empirical fixture must itself obey the corrected kernel
    # observation-state semantics: observation started + unavailable identity
    # is represented by null identity + INCONCLUSIVE gate, never NOT_EXECUTED.
    empirical = _generic_record(sha256_file(MANIFEST_PATH))
    empirical["empirical_observation_started"] = True
    empirical["runtime_specification_binding"]["classification"] = "INCONCLUSIVE"
    empirical["governed_runtime_instantiation_binding"]["classification"] = "INCONCLUSIVE"
    empirical["kernel_evidence"]["observed"] = {
        "kernel_release": None,
        "exact_running_kernel_image_sha256": None,
        "kernel_configuration_sha256": None,
        "required_config_m_module_manifest_sha256": None,
    }
    for k in ("kernel_release_binding","running_kernel_image_binding","kernel_configuration_binding","required_config_m_module_completeness","kernel_completeness"):
        empirical["kernel_evidence"][k] = "INCONCLUSIVE"
    for k in ("completeness","stability","deterministic_absence"):
        empirical["firewall_evidence"][k] = "INCONCLUSIVE"
    for k in ("authority_identity_binding","no_privilege_transition"):
        empirical["observation_authority_evidence"][k] = "INCONCLUSIVE"
    empirical["governed_environment_mutation_gate"]["classification"] = "INCONCLUSIVE"
    for k in (
        "package_acquisition_observation","package_installation_observation","package_upgrade_observation",
        "kernel_change_observation","module_mutation_observation","firewall_mutation_observation",
        "environment_reconfiguration_observation","authority_transition_observation",
    ):
        empirical["governed_environment_mutation_gate"][k] = "INCONCLUSIVE"
    for k in ("content_address_integrity","evidence_completeness","evidence_stability"):
        empirical["evidence_integrity"][k] = "INCONCLUSIVE"
    empirical["transport_binding"]["transport_integrity"] = "INCONCLUSIVE"
    empirical["qualification_root_binding"]["qualification_root_integrity"] = "INCONCLUSIVE"
    if RULES.evaluate_all(empirical)["terminal"] != "INCONCLUSIVE":
        raise AssertionError("missing adapter fail-closed fixture did not derive INCONCLUSIVE")
    results["fail_closed_missing_adapter_tests"] = "PASS"

    bad_schema = dict(schema); bad_schema["pattern"] = ".*"
    try:
        prevalidate_schema(bad_schema)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("unsupported pattern accepted")
    results["pattern_allowlist_tests"] = "PASS"

    bad_ref = {"$schema": schema["$schema"], "$ref": "other.json#/$defs/sha256", "$defs": schema["$defs"]}
    try:
        prevalidate_schema(bad_ref)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("external ref accepted")
    results["local_ref_tests"] = "PASS"

    wrong_uri = dict(schema); wrong_uri["$schema"] = "https://example.invalid/schema"
    try:
        prevalidate_schema(wrong_uri)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("unsupported $schema URI accepted")
    results["exact_schema_uri_tests"] = "PASS"

    unbounded_int = {"$schema": SUPPORTED_SCHEMA_URI, "$ref": "#/$defs/A", "$defs": {"A": {"type": "integer"}}}
    try:
        prevalidate_schema(unbounded_int)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("unbounded integer schema accepted")
    results["integer_schema_bounds_tests"] = "PASS"

    unsupported_type = {"$schema": SUPPORTED_SCHEMA_URI, "$ref": "#/$defs/A", "$defs": {"A": {"type": "number"}}}
    try:
        prevalidate_schema(unsupported_type)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("unsupported schema type accepted")
    results["schema_type_allowlist_tests"] = "PASS"

    for raw in (b'{"x":9223372036854775808}', b'{"x":1,"x":2}'):
        try:
            _strict_manifest_load(raw)
        except ValidationInstrumentFailure:
            pass
        else:
            raise AssertionError("strict manifest parser accepted invalid numeric/duplicate input")
    results["strict_manifest_parser_tests"] = "PASS"

    cyc = {"$schema": SUPPORTED_SCHEMA_URI, "$ref": "#/$defs/A", "$defs": {"A": {"$ref": "#/$defs/A"}}}
    try:
        prevalidate_schema(cyc)
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("cyclic local $ref accepted")
    results["local_ref_cycle_rejection_tests"] = "PASS"

    # Truthful observation-state regression across all represented observation domains.
    noobs = _generic_record(sha256_file(MANIFEST_PATH))
    nr = RULES.evaluate_non_root(noobs)
    for name in ("runtime_specification","runtime_instantiation","kernel","firewall","observation_authority","no_mutation","evidence_integrity","transport_integrity"):
        if nr[name] != "NOT_EXECUTED":
            raise AssertionError(f"{name} not truthful NOT_EXECUTED")
    if RULES.evaluate_qualification_root_state(noobs) != "NOT_EXECUTED":
        raise AssertionError("qualification root not truthful NOT_EXECUTED")
    results["not_started_observation_domains_are_not_executed"] = "PASS"

    started = _generic_record(sha256_file(MANIFEST_PATH))
    started["empirical_observation_started"] = True
    started["runtime_specification_binding"]["classification"] = "INCONCLUSIVE"
    started["governed_runtime_instantiation_binding"]["classification"] = "INCONCLUSIVE"
    for k in ("kernel_release_binding","running_kernel_image_binding","kernel_configuration_binding","required_config_m_module_completeness","kernel_completeness"):
        started["kernel_evidence"][k] = "INCONCLUSIVE"
    for k in ("completeness","stability","deterministic_absence"):
        started["firewall_evidence"][k] = "INCONCLUSIVE"
    for k in ("authority_identity_binding","no_privilege_transition"):
        started["observation_authority_evidence"][k] = "INCONCLUSIVE"
    started["governed_environment_mutation_gate"]["classification"] = "INCONCLUSIVE"
    for k in (
        "package_acquisition_observation","package_installation_observation","package_upgrade_observation",
        "kernel_change_observation","module_mutation_observation","firewall_mutation_observation",
        "environment_reconfiguration_observation","authority_transition_observation",
    ):
        started["governed_environment_mutation_gate"][k] = "INCONCLUSIVE"
    for k in ("content_address_integrity","evidence_completeness","evidence_stability"):
        started["evidence_integrity"][k] = "INCONCLUSIVE"
    started["transport_binding"]["transport_integrity"] = "INCONCLUSIVE"
    started["qualification_root_binding"]["qualification_root_integrity"] = "INCONCLUSIVE"
    sr = RULES.evaluate_non_root(started)
    for name in ("runtime_specification","runtime_instantiation","kernel","firewall","observation_authority","no_mutation","evidence_integrity","transport_integrity"):
        if sr[name] != "INCONCLUSIVE":
            raise AssertionError(f"{name} missing-started observation not INCONCLUSIVE: {sr[name]}")
    if RULES.evaluate_qualification_root_state(started) != "INCONCLUSIVE":
        raise AssertionError("qualification root missing-started observation not INCONCLUSIVE")
    results["started_missing_observation_domains_are_inconclusive"] = "PASS"

    # Prohibit non-null observation evidence while observation is declared not started.
    contradiction = _generic_record(sha256_file(MANIFEST_PATH))
    contradiction["runtime_specification_binding"]["observed_runtime_manifest_sha256"] = "1" * 64
    if RULES.evaluate_runtime_specification(contradiction) != "FAIL_OBSERVATION_INVARIANT":
        raise AssertionError("not-started observed runtime evidence accepted")
    results["not_started_observed_evidence_rejected"] = "PASS"

    # Qualification root cannot participate in proving itself.
    if "qualification_root_integrity" in RULES.evaluate_non_root(r):
        raise AssertionError("qualification root included in non-root gate set")
    try:
        _qualification_root_expected(r, {"qualification_root_integrity": "PASS"})
    except ValidationInstrumentFailure:
        pass
    else:
        raise AssertionError("qualification root circular input accepted")
    results["qualification_root_no_circular_pass"] = "PASS"

    return results

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--validate-record")
    a = p.parse_args()
    if a.self_test:
        print(json.dumps(self_test(), sort_keys=True)); return 0
    if a.validate_record:
        print(json.dumps(validate_record(Path(a.validate_record)), sort_keys=True)); return 0
    p.error("--self-test or --validate-record required")

if __name__ == "__main__":
    raise SystemExit(main())
