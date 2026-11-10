#!/usr/bin/env python3
"""Trusted Managing approval overlay for Primary S05 -- no Codex in this build.

This is not a bypass of V6 scientific checks. Existing V6 source integrity,
real S04 manifest/evidence validation, and frozen rule identities are rechecked.
The package pins exactly one Managing approval SHA256 and immutable file path.
This module does not execute Codex or reserve checkpoint roots.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REF=HERE/'reference'/'v6_accepted'
if str(REF) not in sys.path:sys.path.insert(0,str(REF))
from runtime_activation_gate_v6 import (policy,check_real_bindings,check_reference_sources,
  check_active_sources,require_synthetic_activation,ActivationStop)
ACTIVATION_READY=True
REAL_EXECUTION_AUTHORIZED=False
# Explicitly uninstalled. A later *new sealed release* may pin one hash; this
# immutable V1 release never trusts caller-controlled approval bytes.
PINNED_MANAGING_APPROVAL_SHA256='b228cfaf437527dd9bde2a971312522a8feb1c2cb6f391da45ed5e64c07e7780'
APPROVAL_FILE=HERE/'trusted_managing_approval_v1.json'
AUTH='22270e91bccd75ab451a0b36a14fa1aefef4414963071847d502ab3027858753'
POLICY='7236c9d0f49b568b508915b8a8f03efac2a723831e07f74fe2a5e1c995f7f34e'
BIND='3199ccb1ac3dc753940a38f1c5d53911633d4b68fa9474a54e83098ba846de26'
CLAIM='a6a2bc399da55a16ededd27f8d1d3795e5143328d102116d494db85d749bb830'
ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
FROZEN={
 'real_partition_manifest_sha256':'cf0196e66a646fa02812d35a85879336fb635c437b2df1686e4740f4ca66f53f',
 'partition_rule_sha256':'7cfb32b29ad4f8375287bc0d2196872588655f8d270f1cc5372dc933a8cb6a09',
 'real_s04_manifest_sha256':'ade0a453cc6030d27cb0f1924eb17abe15eb082f55b3fd47af53f52927c543cc',
 'real_s04_evidence_sha256':'0a92b5086a07972bdeb1c8210d50ed6c9c6e43d968b993165d06724c76372dc0',
 'semantic_rule_sha256':'a424085098e871e7f555b29caf3641c5317ac581c9130ba28971385f98aa4fa3',
 'reason_precedence_sha256':'57a7827a23b4c7aa47c19ad950b59871dcff7301addf84f7a2fca580a90f9445'
}
ACTIVE={
 'active_checkpoint_implementation_sha256':'083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27',
 'active_availability_classifier_sha256':'29d87996fc284400e2b5d47201b525b295aef0e1b6daf5ec77818c69c73dd24f',
 'active_live_adapter_sha256':'b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b',
 'active_runtime_activation_gate_sha256':'96726fd117813fb9ff6003cdce86d53bac7bca30483b15097bb64e6f4483ad25',
 'active_readiness_runtime_sha256':'f6f3bdf770c6d0b31696e06f059f2c67fcc89fb2c2825db62651f54ded0744da'
}
V6_POLICY='db64d55bfa38fa9a6e6ecc074f348e92191215ad549d4debff67c35e8b8635de'

def _need(ok,code):
 if not ok:raise ActivationStop(code)
def sha(path):
 p=Path(path)
 _need(p.is_file() and not p.is_symlink(),'EXPECTED_REGULAR_FILE_REQUIRED')
 return hashlib.sha256(p.read_bytes()).hexdigest()
def pinned(path,expected):
 _need(sha(path)==expected,'SEALED_IDENTITY_MISMATCH__'+Path(path).name)
 try:data=json.loads(Path(path).read_bytes())
 except Exception as exc:raise ActivationStop('INVALID_SEALED_JSON') from exc
 _need(type(data)==dict,'INVALID_SEALED_JSON_STRUCTURE')
 return data

def check_activation_inputs(*,role,attempt_identity,authorization_path,approval_path=None):
 _need(role=='PRIMARY','ONLY_PRIMARY_S05_AUTHORIZED')
 _need(attempt_identity==ATTEMPT,'WRONG_PRIMARY_ATTEMPT')
 # All accepted V6 integrity checks apply, not just raw role/hash checks.
 old=policy();check_reference_sources();check_active_sources(old)
 _need(all(old.get(k)==v for k,v in FROZEN.items()),'FROZEN_INPUT_BINDING_CHANGED')
 _need(all(old.get(k)==v for k,v in ACTIVE.items()),'FROZEN_ACTIVE_V6_CHANGED')
 _need(sha(REF/'runtime_activation_policy_v6.json')==V6_POLICY,'V6_SEALED_POLICY_DRIFT')
 prep=HERE/'reference'/'final_preparation'
 auth=pinned(prep/'final_primary_s05_authorization_v1.json',AUTH)
 core=pinned(prep/'scoped_real_execution_policy_v1.json',POLICY)
 bind=pinned(prep/'policy_authorization_binding_v1.json',BIND)
 claim=pinned(prep/'authorization_claim_v1.json',CLAIM)
 _need(core['role']=='PRIMARY' and core['attempt_identity']==ATTEMPT and
       core['independent_s09_authorized'] is False and core['batch0005_authorized'] is False and
       core['real_semantic_execution_enabled'] is True and core['real_execution_authorized_now'] is False,
       'FINAL_PRIMARY_POLICY_SCOPE_INVALID')
 _need(bind['final_authorization_sha256']==AUTH and bind['base_policy_sha256']==POLICY and
       bind['currently_approved_to_execute'] is False and bind['final_managing_release_approval_sha256'] is None,
       'FINAL_BINDING_INVALID')
 _need(auth['authorization_claim_sha256']==CLAIM and
       auth['final_runtime_policy_sha256']==POLICY and auth['role']==role and
       auth['attempt_identity']==attempt_identity and claim['role']==role and
       claim['attempt_identity']==attempt_identity,'FINAL_AUTH_BINDING_INVALID')
 for k,v in FROZEN.items():_need(claim.get(k)==v and auth.get(k)==v,'FINAL_FROZEN_INPUT_MISMATCH__'+k)
 for k,v in ACTIVE.items():_need(claim.get(k)==v and auth.get(k)==v,'FINAL_RUNTIME_INPUT_MISMATCH__'+k)
 _need(auth.get('sealed_policy_sha256')==V6_POLICY,'SEALED_RUNTIME_POLICY_MISMATCH')
 _need(authorization_path is not None and sha(authorization_path)==AUTH,
       'FINAL_AUTHORIZATION_ARTIFACT_MISSING_OR_WRONG')
 # The future approval itself must be pinned by trusted separately released code.
 _need(PINNED_MANAGING_APPROVAL_SHA256 is not None,'MANAGING_APPROVAL_TRUST_PIN_NOT_INSTALLED')
 # Trust comes solely from the immutable overlay pin and the fixed packaged file.
 # Caller-supplied approval paths may not replace this exact artifact.
 _need(approval_path is None or Path(approval_path).absolute()==APPROVAL_FILE.absolute(),
       'MANAGING_APPROVAL_PATH_OVERRIDE_FORBIDDEN')
 approval=pinned(APPROVAL_FILE,PINNED_MANAGING_APPROVAL_SHA256)
 required={
   'schema_version':'BATCH0004_PRIMARY_S05_TRUSTED_MANAGING_APPROVAL_V1',
   'approved':True,'managing_approval':'YES__EXACT_IDENTITIES_ONLY',
   'real_execution_authorized':'YES__EXACT_IDENTITIES_ONLY',
   'authorized_role':'PRIMARY','authorized_stage':'S05','authorized_batch':'BATCH0004',
   'authorized_attempt':ATTEMPT,'role':'PRIMARY',
   'stage':'S05_PRIMARY_SEMANTIC_ADJUDICATION','batch_id':'BATCH0004',
   'attempt_identity':ATTEMPT,'partition_size':25,'partition_count':20,
   'final_authorization_sha256':AUTH,'final_policy_sha256':POLICY,
   'policy_authorization_binding_sha256':BIND,'authorization_claim_sha256':CLAIM,
   'original_activation_release_descriptor_sha256':'68d8cabc2dd9d083dceed82d2b6e2da295a7d3427110fda2cadbbb91062d8ddc',
   'original_activation_bridge_sha256':'dcb0d1b169d6624b3c388a7ce8d2a4e232104a77f457a8be6c16cbf5ecc35ef2',
   'original_activation_prestart_driver_sha256':'e44d0942ba0838639fc1bde8a2c09509889badccf76a8c60028de19695297df0',
   'accepted_v6_sealed_policy_sha256':V6_POLICY,
   's09_independent_authorized':False,'batch0005_authorized':False,
   'alternate_attempts_authorized':False,
   **FROZEN,**ACTIVE
 }
 _need(set(approval)==set(required)|{'task_id'},'TRUSTED_APPROVAL_SCHEMA_FIELDS_MISMATCH')
 _need(approval.get('task_id')=='POST_C6_Q1_2027_D1_BODY_BATCH0004_PRIMARY_S05_TRUSTED_MANAGING_APPROVAL_ARTIFACT_V1',
       'TRUSTED_APPROVAL_TASK_MISMATCH')
 for k,v in required.items():
  _need(type(approval.get(k)) is type(v) and approval.get(k)==v,
        'TRUSTED_APPROVAL_SCOPE_MISMATCH__'+k)
 return old

def require_real_activation(*,source_root,manifest_path,role,attempt_identity,authorization_path=None,checkpoint_root=None):
 # Exact hash-pinned approval is mandatory; this function never reserves roots
 # or launches a Codex subprocess. Fresh prestart still belongs to a later driver.
 check_activation_inputs(role=role,attempt_identity=attempt_identity,authorization_path=authorization_path)
 info=check_real_bindings(source_root,manifest_path)
 if checkpoint_root is not None:
  root=Path(checkpoint_root)
  _need(not root.is_symlink(),'CHECKPOINT_ROOT_SYMLINK')
 return dict(real=True,role=role,attempt_identity=attempt_identity,source_info=info)
