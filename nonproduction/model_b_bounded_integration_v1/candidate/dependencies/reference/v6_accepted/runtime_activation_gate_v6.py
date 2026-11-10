#!/usr/bin/env python3
"""Sealed real activation gate and separately pinned synthetic authorization.

Real execution is deliberately disabled in this nonproduction release. Future
Managing approval requires a new versioned policy identity; an unpinned user
artifact cannot enable execution. No code here invokes Codex.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from policy_seal_v6 import PIN_POLICY_SHA256

HERE=Path(__file__).resolve().parent
PIN_POLICY=PIN_POLICY_SHA256
PIN_SYNTHETIC='c78c37817180f19443633f48627883adf102f91ec565ba0b424442e330ffa446'
PIN_PARTITION_MANIFEST='cf0196e66a646fa02812d35a85879336fb635c437b2df1686e4740f4ca66f53f'
PIN_RULE='7cfb32b29ad4f8375287bc0d2196872588655f8d270f1cc5372dc933a8cb6a09'
PIN_S04='ade0a453cc6030d27cb0f1924eb17abe15eb082f55b3fd47af53f52927c543cc'
PIN_EVIDENCE='0a92b5086a07972bdeb1c8210d50ed6c9c6e43d968b993165d06724c76372dc0'
PIN_SEMANTIC='a424085098e871e7f555b29caf3641c5317ac581c9130ba28971385f98aa4fa3'
PIN_PRECEDENCE='57a7827a23b4c7aa47c19ad950b59871dcff7301addf84f7a2fca580a90f9445'
PIN_CHECKPOINT='63500740e08ed2bda817f062a83e8c12b256674f18cf81a771f376281efd574d'
PIN_CHECKPOINT_SCHEMA='b67b0baff0efe3fa67acbb60d14f7654cbe1410fae92795c7cab608f00336268'
PIN_V3='fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0'
PIN_FIREWALL='09cf139fc69b43d43e734f966c549ddb13efd113a57bafd0e982f675785371b4'
PIN_HISTORICAL_RELEASE_INVENTORY='6d76ef2eddebdf8b2156f1492dd3bc95ac5857aff01386175fc99ce11b475fc9'
PIN_PRESERVED_V3_RELEASE_INVENTORY='1e7ad3475c24cb32ae16d6bbe715099d6e5a9e73745490b9adedd651f693651d'
PIN_PRESERVED_V4_RELEASE_INVENTORY='35db69a34a102c589a384bf7d1403c9e07ae226d6aecb22813f42df8ef6994a7'
PIN_PRESERVED_V5_RELEASE_INVENTORY='451d23b2618bbe96c2855dd3fa6a1461fc37054ece08f230ce339257a3f831ef'
PIN_PRESERVED_V2_RELEASE_INVENTORY='b2d0632bd7e7389e29f5efe2c68f3c1295c860ae15b91ae88e1759ac45d5835d'

class ActivationStop(RuntimeError):pass

def require(cond, reason):
    if not cond:raise ActivationStop(reason)

def sha_file(path):
    path=Path(path)
    require(path.is_file() and not path.is_symlink(),'AUTH_FILE_MISSING_OR_SYMLINK')
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_pinned_json(path,expected_sha):
    require(sha_file(path)==expected_sha,'ACTIVATION_POLICY_IDENTITY_MISMATCH')
    return json.loads(Path(path).read_bytes())

def policy():
    p=read_pinned_json(HERE/'runtime_activation_policy_v6.json',PIN_POLICY)
    pins={'partition_rule_sha256':PIN_RULE,'real_partition_manifest_sha256':PIN_PARTITION_MANIFEST,
          'real_s04_manifest_sha256':PIN_S04,'real_s04_evidence_sha256':PIN_EVIDENCE,
          'semantic_rule_sha256':PIN_SEMANTIC,'reason_precedence_sha256':PIN_PRECEDENCE,
          'historical_checkpoint_implementation_sha256':PIN_CHECKPOINT,
          'frozen_checkpoint_schema_sha256':PIN_CHECKPOINT_SCHEMA,
          'frozen_v3_orchestrator_sha256':PIN_V3,'frozen_firewall_sha256':PIN_FIREWALL}
    for k,v in pins.items():require(p.get(k)==v,'AUTH_POLICY_BINDING_CHANGED__'+k)
    require(p.get('expected_partition_size')==25 and p.get('expected_partition_count')==20
            and p.get('expected_position_domain')==[1501,2000],'AUTH_POLICY_PARTITIONS_CHANGED')
    require(p['schema_version']=='BATCH0004_RUNTIME_ACTIVATION_POLICY_V6','AUTH_POLICY_SCHEMA_CHANGED')
    require(p.get('real_semantic_execution_enabled') is False and
            p.get('approved_real_execution_authorization_sha256') is None and
            p.get('authorized_real_attempt_identity') is None,'V6_SEALED_REAL_AUTHORIZATION_STATE_CHANGED')
    check_active_sources(p)
    check_preserved_release_inventory()
    check_preserved_v2_release_inventory()
    check_preserved_v3_release_inventory()
    check_preserved_v4_release_inventory()
    check_preserved_v5_release_inventory()
    return p

ACTIVE_MODULES={
  'active_checkpoint_implementation_sha256':'checkpoint_resume_readiness_v8.py',
  'active_availability_classifier_sha256':'availability_classifier_v6.py',
  'active_live_adapter_sha256':'v3_partition_live_adapter_readiness_v7.py',
  'active_runtime_activation_gate_sha256':'runtime_activation_gate_v6.py',
  'active_readiness_runtime_sha256':'readiness_runtime_v6.py',
}

def check_active_sources(p=None):
    """Measure live Python modules, including THIS gate, before any authorization.

    Historical checkpoint V1 PIN_CHECKPOINT is checked as retained evidence
    only. It must never substitute for active checkpoint readiness V4.
    """
    if p is None:p=policy()
    require(set(ACTIVE_MODULES).issubset(p),'ACTIVE_RUNTIME_IDENTITY_FIELDS_MISSING')
    for key,relative in ACTIVE_MODULES.items():
        want=p.get(key)
        require(isinstance(want,str) and len(want)==64 and
                sha_file(HERE/relative)==want,
                'ACTIVE_IMPLEMENTATION_IDENTITY_MISMATCH__'+key)
    require(p.get('historical_checkpoint_implementation_sha256')==PIN_CHECKPOINT,
            'HISTORICAL_CHECKPOINT_REFERENCE_CHANGED')
    require(p['active_checkpoint_implementation_sha256']!=PIN_CHECKPOINT,
            'HISTORICAL_CHECKPOINT_USED_AS_ACTIVE_IMPLEMENTATION')
    return True

def check_preserved_release_inventory():
    """Bind historical V1 dependencies including old classifier helper functions.

    A superseding component imports V1 helper definitions and V3 validators;
    prior release inventory must remain byte-identical (39 files).
    """
    path=HERE/'readiness_release_integrity_v1.json'
    require(sha_file(path)==PIN_HISTORICAL_RELEASE_INVENTORY,
            'PRESERVED_V1_RELEASE_INVENTORY_TAMPERED')
    release=json.loads(path.read_bytes())
    hashes=release['artifact_sha256']
    require(len(hashes)==39,'PRESERVED_RELEASE_MEMBER_COUNT_CHANGED')
    for name,want in hashes.items():
        relative=Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts,
                'PRESERVED_RELEASE_PATH_TRAVERSAL')
        require(sha_file(HERE/relative)==want,'PRESERVED_V1_RELEASE_MEMBER_CHANGED__'+name)
    return True

def check_preserved_v2_release_inventory():
    """Full V2 release is immutable under superseding V3 correction."""
    path=HERE/'readiness_release_integrity_v2.json'
    require(sha_file(path)==PIN_PRESERVED_V2_RELEASE_INVENTORY,
            'PRESERVED_V2_RELEASE_INVENTORY_TAMPERED')
    inv=json.loads(path.read_bytes())
    require(inv.get('schema_version')=='BATCH0004_READINESS_RECOVERY_V2_INVENTORY',
            'PRESERVED_V2_INVENTORY_SCHEMA_CHANGED')
    hashes=inv['artifact_sha256']
    require(len(hashes)==66,'PRESERVED_V2_MEMBER_COUNT_CHANGED')
    for name,want in hashes.items():
        rel=Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts,
                'PRESERVED_V2_MEMBER_PATH_TRAVERSAL')
        require(sha_file(HERE/rel)==want,'PRESERVED_V2_MEMBER_CHANGED__'+name)
    return True

def check_preserved_v3_release_inventory():
    """Preserve the full 84-member V3 release, including its classifier."""
    path=HERE/'readiness_release_integrity_v3.json'
    require(sha_file(path)==PIN_PRESERVED_V3_RELEASE_INVENTORY,
            'PRESERVED_V3_RELEASE_INVENTORY_TAMPERED')
    inv=json.loads(path.read_bytes())
    require(inv.get('schema_version')=='BATCH0004_READINESS_RECOVERY_V3_INVENTORY',
            'PRESERVED_V3_INVENTORY_SCHEMA_CHANGED')
    hashes=inv['artifact_sha256']
    require(len(hashes)==84,'PRESERVED_V3_MEMBER_COUNT_CHANGED')
    for name,want in hashes.items():
        rel=Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts,
                'PRESERVED_V3_MEMBER_PATH_TRAVERSAL')
        require(sha_file(HERE/rel)==want,'PRESERVED_V3_MEMBER_CHANGED__'+name)
    return True

def check_preserved_v4_release_inventory():
    """Full V4 evidence and source inventory remains byte-identical."""
    path=HERE/'readiness_release_integrity_v4.json'
    require(sha_file(path)==PIN_PRESERVED_V4_RELEASE_INVENTORY,
            'PRESERVED_V4_RELEASE_INVENTORY_TAMPERED')
    inv=json.loads(path.read_bytes())
    require(inv['schema_version']=='BATCH0004_READINESS_RECOVERY_V4_INVENTORY',
            'PRESERVED_V4_INVENTORY_SCHEMA_CHANGED')
    hashes=inv['artifact_sha256']
    require(len(hashes)==103,'PRESERVED_V4_MEMBER_COUNT_CHANGED')
    for name,want in hashes.items():
        rel=Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts,
                'PRESERVED_V4_MEMBER_PATH_TRAVERSAL')
        require(sha_file(HERE/rel)==want,'PRESERVED_V4_MEMBER_CHANGED__'+name)
    return True

def check_preserved_v5_release_inventory():
    """Superseding V6 cannot mutate any preserved V5 release member."""
    path=HERE/'readiness_release_integrity_v5.json'
    require(sha_file(path)==PIN_PRESERVED_V5_RELEASE_INVENTORY,
            'PRESERVED_V5_RELEASE_INVENTORY_TAMPERED')
    inv=json.loads(path.read_bytes())
    require(inv.get('schema_version')=='BATCH0004_READINESS_RECOVERY_V5_INVENTORY',
            'PRESERVED_V5_INVENTORY_SCHEMA_CHANGED')
    hashes=inv['artifact_sha256']
    require(len(hashes)==124,'PRESERVED_V5_MEMBER_COUNT_CHANGED')
    for name,want in hashes.items():
        rel=Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts,
                'PRESERVED_V5_MEMBER_PATH_TRAVERSAL')
        require(sha_file(HERE/rel)==want,'PRESERVED_V5_MEMBER_CHANGED__'+name)
    return True

def check_reference_sources():
    # Exact accepted scientific, firewall, checkpoint source bytes. Corrected
    # readiness modules are additional, never replace source identities.
    pins={'frozen_v3_orchestrator_reference.py':PIN_V3,'firewall_v2.py':PIN_FIREWALL,
          'checkpoint_resume_nonproduction_v1.py':PIN_CHECKPOINT,
          'checkpoint_manifest_schema_v1.json':PIN_CHECKPOINT_SCHEMA}
    for rel,pin in pins.items():require(sha_file(HERE/rel)==pin,'FROZEN_REFERENCE_DRIFT__'+rel)
    return True

def check_real_bindings(source_root, manifest_path):
    """Full accepted real S04 and manifest rehash. No execution/filesystem writes."""
    from real_partition_manifest_v1 import verify_s04, verify_identity_manifest
    p=policy();check_reference_sources()
    require(sha_file(manifest_path)==p['real_partition_manifest_sha256'],
            'FROZEN_REAL_PARTITION_MANIFEST_IDENTITY_MISMATCH')
    info=verify_s04(source_root,real=True)
    require(info['manifest_sha256']==p['real_s04_manifest_sha256'] and
            info['neutral_sha256']==p['real_s04_evidence_sha256'] and
            info['semantic_rule_sha256']==p['semantic_rule_sha256'] and
            info['precedence_sha256']==p['reason_precedence_sha256'],
            'REAL_S04_BINDING_FAILURE')
    verify_identity_manifest(json.loads(Path(manifest_path).read_text()),info)
    return info

def require_real_activation(*, source_root, manifest_path, role, attempt_identity,
                            authorization_path=None, checkpoint_root=None):
    """No synthetic authorization can activate real execution.

    A future managing-authorized release must supply a new pinned policy with an
    approved artifact identity; this shipped release hard-stops *before Codex*.
    """
    p=policy()
    require(role in ('PRIMARY','INDEPENDENT'),'INVALID_ROLE_FOR_AUTH')
    require(isinstance(attempt_identity,str) and attempt_identity.strip(),
            'MISSING_REAL_ATTEMPT_IDENTITY')
    # First block missing/mismatched future Managing authorization even if real
    # S04 data is absent (safe on synthetic CI and on the current Mac release).
    require(authorization_path is not None,'MISSING_EXPLICIT_REAL_EXECUTION_AUTHORIZATION')
    require(p['real_semantic_execution_enabled'] is True and
            isinstance(p.get('approved_real_execution_authorization_sha256'),str) and
            len(p['approved_real_execution_authorization_sha256'])==64,
            'REAL_EXECUTION_DISABLED_BY_SEALED_POLICY')
    require(sha_file(authorization_path)==p['approved_real_execution_authorization_sha256'],
            'REAL_EXECUTION_AUTHORIZATION_SHA256_MISMATCH')
    auth=json.loads(Path(authorization_path).read_text())
    for key,want in (
      ('mode','REAL_PARTITIONED_SCIENTIFIC_EXECUTION'),('task_id',p['release_task_id']),
      ('role',role),('attempt_identity',attempt_identity),
      ('partition_rule_sha256',PIN_RULE),('real_partition_manifest_sha256',PIN_PARTITION_MANIFEST),
      ('real_s04_manifest_sha256',PIN_S04),('real_s04_evidence_sha256',PIN_EVIDENCE),
      ('semantic_rule_sha256',PIN_SEMANTIC),('reason_precedence_sha256',PIN_PRECEDENCE),
      ('checkpoint_implementation_sha256',p['active_checkpoint_implementation_sha256']),
      ('active_checkpoint_implementation_sha256',p['active_checkpoint_implementation_sha256']),
      ('active_availability_classifier_sha256',p['active_availability_classifier_sha256']),
      ('active_live_adapter_sha256',p['active_live_adapter_sha256']),
      ('active_runtime_activation_gate_sha256',p['active_runtime_activation_gate_sha256']),
      ('active_readiness_runtime_sha256',p['active_readiness_runtime_sha256']),
      ('sealed_policy_sha256',PIN_POLICY)):
        require(auth.get(key)==want,'EXECUTION_AUTHORIZATION_BINDING_MISMATCH__'+key)
    require(attempt_identity==p['authorized_real_attempt_identity'],
            'RUNTIME_ATTEMPT_IDENTITY_NOT_PREAPPROVED')
    info=check_real_bindings(source_root,manifest_path)
    if checkpoint_root is not None:
        root=Path(checkpoint_root)
        # Root and future independent store must have distinct role-namespaced
        # paths; never read or pass Primary outputs into Independent payloads.
        require(not root.is_symlink(),'CHECKPOINT_ROOT_SYMLINK')
    return {'authorization_sha256':sha_file(authorization_path),'role':role,
            'attempt_identity':attempt_identity,'source_info':info,'real':True}

def require_synthetic_activation(*, auth_path, role, attempt_identity, runner):
    require(role in ('PRIMARY','INDEPENDENT'),'INVALID_SYNTHETIC_ROLE')
    require(isinstance(attempt_identity,str) and attempt_identity.startswith('SYNTHETIC_READINESS_'),
            'SYNTHETIC_ATTEMPT_IDENTITY_INVALID')
    a=read_pinned_json(auth_path,PIN_SYNTHETIC)
    require(a.get('execution_mode')=='SYNTHETIC_NONPRODUCTION' and
            a.get('authorization_scope')=='INJECTED_MOCK_EXECUTOR_ONLY' and
            a.get('real_execution_permitted') is False and role in a.get('authorized_roles',[]) and
            a.get('expected_partition_size')==25 and a.get('expected_partition_count')==20,
            'SYNTHETIC_AUTHORIZATION_INVALID')
    from partition_contract_nonproduction_v1 import v3
    require(callable(runner) and runner is not v3.run_codex_executor,
            'REAL_EXECUTOR_FORBIDDEN_IN_SYNTHETIC_PATH')
    policy();check_reference_sources()
    return {'role':role,'attempt_identity':attempt_identity,'real':False,
            'authorization_sha256':PIN_SYNTHETIC}

# Explicit distinction: engineering complete != activation authorized.
ACTIVATION_READY=True
REAL_EXECUTION_AUTHORIZED=False
