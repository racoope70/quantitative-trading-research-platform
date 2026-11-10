#!/usr/bin/env python3
"""Case-bound, append-only, ONE-unit recovery transaction -- prospective bounded-executor compatible V4 (REAL hard disabled) -- immutable mode bound authorization.

Built against unchanged accepted V6 checkpoint, validator, parser, and classifier.
Nonproduction integration only; no CLI start, root mutation, or Codex call in release tests.
Existing checkpoint schema does NOT allow a new global_state literal; therefore
RECOVERY_AUTHORIZED__FIRST_UNFINISHED_ONLY lives in an immutable, linked sidecar
journal. Checkpoint snapshots and original stop event are never overwritten.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
DEPS=Path(__file__).resolve().parent/'dependencies'
sys.path.insert(0,str(DEPS))
REF=DEPS/'reference'/'v6_accepted'
if str(REF) not in sys.path:sys.path.insert(0,str(REF))

from checkpoint_resume_activation_trusted_v1 import (
    CheckpointEngine, SyntheticMockExecutor, NON_RESUMABLE, PAUSED, CheckpointStop,
    require, obj_bytes, sha_file, unique_write, strictly_json, digest,
    unit_evidence, validate_semantic_unit, canonical_json, decide_availability,
    looks_complete, now_utc, SIZE,
)
from prospective_adapter_v1 import V3CodexUnitAdapter, v3 as frozen_v3, verify_prospective_context
from real_candidate.engine_v1 import BoundCheckpointEngine
from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBPredecessor,PolicyBCapturedFixtureExecutor

# Hash identities of the accepted exact interface implementations. No duck typing.
REAL_CHECKPOINT_INTERFACE_SHA256 = "fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1"
REAL_EXECUTOR_INTERFACE_SHA256 = '2315601c2f83fa18107257025ec94ef85d65b12c7a38e4a2c44066d77d3723ac'
HISTORICAL_EXECUTOR_INTERFACE_SHA256 = "1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424"
ACTIVE_V6_CHECKPOINT_SHA256 = "083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27"
ACTIVE_V6_EXECUTOR_SHA256 = "b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b"

def verify_exact_approved_real_interfaces():
    base=DEPS
    need(sha_file(base/"checkpoint_resume_activation_trusted_v1.py")==REAL_CHECKPOINT_INTERFACE_SHA256,
         "REAL_CHECKPOINT_ENGINE_IMPLEMENTATION_SHA_DRIFT")
    need(sha_file(base/"corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py")==HISTORICAL_EXECUTOR_INTERFACE_SHA256,
         "HISTORICAL_REAL_EXECUTOR_IMPLEMENTATION_SHA_DRIFT")
    pins=compatibility_binding()['prospective_source_sha256']
    need(set(pins)=={'prospective_adapter_v1.py','real_candidate/executor_v1.py','real_candidate/capture_v1.py','real_candidate/engine_v1.py'},
         'PROSPECTIVE_SOURCE_PIN_SET_DRIFT')
    need(pins['prospective_adapter_v1.py']==REAL_EXECUTOR_INTERFACE_SHA256,'PROSPECTIVE_ADAPTER_BINDING_DRIFT')
    import prospective_adapter_v1 as prospective_adapter
    from real_candidate import executor_v1,capture_v1,engine_v1
    modules={'prospective_adapter_v1.py':prospective_adapter,
             'real_candidate/executor_v1.py':executor_v1,'real_candidate/capture_v1.py':capture_v1,
             'real_candidate/engine_v1.py':engine_v1}
    need(prospective_adapter.V3CodexUnitAdapter is V3CodexUnitAdapter,'PROSPECTIVE_ADAPTER_CLASS_SUBSTITUTED')
    for name,pin in pins.items():
        expected=Path(__file__).resolve().parent/name
        need(Path(modules[name].__file__).resolve()==expected.resolve(),'PROSPECTIVE_LOADED_SOURCE_PATH_DRIFT__'+name)
        need(sha_file(expected)==pin,'PROSPECTIVE_SOURCE_IDENTITY_DRIFT__'+name)
    need(sha_file(base/"reference/v6_accepted/checkpoint_resume_readiness_v8.py")==ACTIVE_V6_CHECKPOINT_SHA256,
         "ACCEPTED_V6_CHECKPOINT_IMPLEMENTATION_SHA_DRIFT")
    need(sha_file(base/"reference/v6_accepted/v3_partition_live_adapter_readiness_v7.py")==ACTIVE_V6_EXECUTOR_SHA256,
         "ACCEPTED_V6_EXECUTOR_IMPLEMENTATION_SHA_DRIFT")
    return True


RECOVERY_STATE='RECOVERY_AUTHORIZED__FIRST_UNFINISHED_ONLY'
CASE_TASK='POST_C6_Q1_2027_D1_BODY_BATCH0004_PRIMARY_S05_BOUNDED_CONTROLLED_STOP_RECOVERY_IMPLEMENTATION_V1'
ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
REAL_CHECKPOINT_MANIFEST = '379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe'
REAL_UNIT_INPUT_SHA256='d01c11ab77b36eda886dccbf6288887e063583cbe016fb8a033f16a6b8360221'
# Identified from the read-only U0012 diagnostic: raw bytes of the executor's
# neutral_semantic_evidence.jsonl, not a coerced/re-serialized Python object.
REAL_CASE={
    'schema_version':'BATCH0004_U0012_EXACT_CONTROLLED_STOP_RECOVERY_BINDING_V1',
    'task_id':CASE_TASK,
    'batch_id':'BATCH0004','state_id':'S05_PRIMARY_SEMANTIC_ADJUDICATION',
    'role':'PRIMARY','attempt_id':ATTEMPT,
    'checkpoint_manifest_sha256':REAL_CHECKPOINT_MANIFEST,
    'first_unfinished_unit':'U0012',
    'partition_manifest_sha256':'cf0196e66a646fa02812d35a85879336fb635c437b2df1686e4740f4ca66f53f',
    'semantic_rule_sha256':'a424085098e871e7f555b29caf3641c5317ac581c9130ba28971385f98aa4fa3',
    'reason_precedence_sha256':'57a7827a23b4c7aa47c19ad950b59871dcff7301addf84f7a2fca580a90f9445',
    'corrected_prompt_sha256':'55ad5330b9c2bcb4f68de0fec996adf93914d55e728456c247fbb16407757780',
    'corrected_adapter_sha256':'1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424',
    'superseding_runtime_wiring_sha256':'5d504e90fe11097d2bba13d98d62ea547853b75468cf2a913ac1e4f70c88f951',
    'superseding_execution_release_descriptor_sha256':'50ba1290bbcfcca373410ca2c0b3fcbbea94440110a964248e3acff460dd5fe1',
    'unit_input_sha256':REAL_UNIT_INPUT_SHA256,
    'unit_input_sha256_kind':'SHA256_OF_RAW_U0012_EXECUTOR_NEUTRAL_JSONL_BYTES',
    'authorized_recovery_unit':'U0012',
    'max_new_units':1,
    'expected_position_start':1776,'expected_position_end':1800,
    'frozen_prefix_count':11,'frozen_primary_row_count':275,
    'original_stop_reason':'EXACT_U0012_RECOVERY_CONTROLLED_STOP__RecoveryReject__CONFLICTING_OR_UNKNOWN_EXECUTOR_FAILURE',
    'real_execution_authorized':False,
    'historical_attempts':[{'attempt_number': 1, 'context_id': '01a1408b-4b6d-7560-992c-02ee2e864c52', 'manifest_sha256': 'a6b1d031cde7f4c6ff2a03a50c80cbfa9a8127f045b2eb4c59421d8c4e936c9c', 'status': 'EXECUTOR_NORMAL_RETURN'}, {'attempt_number': 2, 'context_id': '01a141b1-721e-7302-8d69-0db2a5f70f8f', 'manifest_sha256': 'dfd4c500eddeb96d8485be9c120572addb267a32ac730149569567d7acc5e05d', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 3, 'context_id': 'dacfa152ac032a5e243961f9497feff5e6469a249738d32a', 'manifest_sha256': '2fd04836b5b58e3f73646c1202862cf3b2f8c76f8e96a0e504e4ef40d978994f', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 4, 'context_id': None, 'manifest_sha256': '2cce58285b4513c8df75b52fab31074b27e63ebf3271817cdeea31b6b198b8a5', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 5, 'context_id': 'f2fcab4fa761e62aa119b658ca0b15f01a16a48252c97ffc', 'manifest_sha256': '9d1e852ea055579b7f7140f6eacb483088be5ecadee32a9e0deea7a46b45f57e', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 6, 'context_id': '7c08204d30d49fdf2931447ff4fb690dc7219f8fcb1b0e5d', 'manifest_sha256': 'e4317f1bb10faad84842cda80a46a042ee6e6099927bf98ad0936b7c5bdca3e8', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 7, 'context_id': 'f020029dae795dc52e6ffd13227f19580f1789e5be742c22', 'manifest_sha256': 'a027cecbae36ad083a8b20cf30fd4413a17c4a873d5c599e79f0ebdd2d9e5382', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 8, 'context_id': 'a55b03d089163149f2eb5efc4587ee2e665bf21338cd3bc3', 'manifest_sha256': '9d195f4c2d54d09f3348d770542c70101c2f1c649c09ffef8ffe241cc9809edb', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}, {'attempt_number': 9, 'context_id': 'eeb02ed8884bb8da6cb219b0588524d708406bb2f77f0621', 'manifest_sha256': 'f34d8ae44d5a5bb32e1bcc149dfca85b2c1412f15668df8500f2f36f164253a8', 'status': 'EXTERNAL_CONFLICT__CONTROLLED_STOP'}],
}

class RecoveryReject(RuntimeError): pass

class FreshCheckpointIntegrityError(RecoveryReject):
    """No recovery mutation or executor dispatch allowed on persisted drift."""


def need(condition,code):
    if not condition:raise RecoveryReject(code)

def sha_bytes(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def json_bytes(obj)->bytes:return (json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('utf-8')

def case_binding_sha(case):return sha_bytes(json_bytes(case))

def exact_case(case,expected):
    need(type(case) is dict and case == expected and set(case)==set(expected),'RECOVERY_BINDING_TAMPERED_OR_WRONG_CASE')
    need(type(case['max_new_units']) is int and case['max_new_units']==1,'MAX_NEW_UNITS_NOT_ONE')
    need(case['authorized_recovery_unit']=='U0012' and case['first_unfinished_unit']=='U0012','NOT_EXACT_U0012')
    need(case['role']=='PRIMARY' and case['batch_id']=='BATCH0004','RECOVERY_ROLE_OR_BATCH_MISMATCH')
    return True

def check_real_case_constants():
    exact_case(REAL_CASE,REAL_CASE)
    need(REAL_CASE['checkpoint_manifest_sha256']==REAL_CHECKPOINT_MANIFEST,'ACCEPTED_STOP_CHECKPOINT_CHANGED')
    need(REAL_CASE['unit_input_sha256']==REAL_UNIT_INPUT_SHA256,'REAL_U0012_INPUT_PIN_CHANGED')
    return True

# Test-only case construction changes ONLY the checkpoint/source hashes to match
# the accepted V6 synthetic fixture. It is never an authorization for real roots.
def synthetic_case(engine,raw_executor_unit_input:bytes):
    engine.verify()
    case=copy.deepcopy(REAL_CASE)
    case.update({
      'attempt_id':engine.state['attempt_identity'],
      'checkpoint_manifest_sha256':engine.state['checkpoint_manifest_sha256'],
      'partition_manifest_sha256':engine.identity_manifest_hash if hasattr(engine,'identity_manifest_hash') else engine.state['partition_manifest_sha256'],
      'semantic_rule_sha256':engine.state['semantic_rule_identity_sha256'],
      'reason_precedence_sha256':engine.state['reason_precedence_identity_sha256'],
      'unit_input_sha256':sha_bytes(raw_executor_unit_input),
      'unit_input_sha256_kind':'SHA256_OF_RAW_SYNTHETIC_U0012_NEUTRAL_INPUT_BYTES',
      'original_stop_reason':engine.state['stop_reason'],
      'real_execution_authorized':False,
      'historical_attempts':copy.deepcopy(engine.state['units'][11]['attempts']),
    })
    return case

# Frozen structural mode contract. The immutable payload is serialized, SHA256
# pinned into a NEW case+mode recovery journal identity, and reverified at each
# mutation/dispatch boundary. No authority comes from a mutable real_source flag.
MODE_SCHEMA='BATCH0004_U0012_EXACT_RECOVERY_EXECUTION_MODE_BINDING_V2'


def mode_schema_identity():
    return sha_bytes(json_bytes({'schema_version':MODE_SCHEMA,
      'required_fields':['execution_mode','engine_mode','adapter_mode',
                         'authorization_mode','expected_provenance_mode',
                         'engine_class','adapter_class','engine_configuration_sha256',
                         'adapter_configuration_sha256']}))


def engine_mode_snapshot(engine):
    need(type(engine) in (CheckpointEngine,BoundCheckpointEngine),
         'UNAPPROVED_CHECKPOINT_ENGINE_INTERFACE')
    if type(engine) is CheckpointEngine:
        need(not hasattr(engine,'real_source'),'SYNTHETIC_ENGINE_HAS_REAL_SOURCE_FLAG')
        return 'SYNTHETIC',{'engine_class':'CheckpointEngine','role':engine.role,
                  'checkpoint_root':str(engine.root)}
    need(type(engine.real_source) is bool,'ENGINE_EXECUTION_MODE_MALFORMED')
    return ('REAL' if engine.real_source else 'SYNTHETIC'),{
        'engine_class':'BoundCheckpointEngine','real_source':engine.real_source,
        'role':engine.role,'checkpoint_root':str(engine.root),
        'source_root':str(engine.source_root),
        'identity_manifest_path':str(engine.identity_manifest_path),
        'authorization_path':str(engine.authorization_path),
        'attempt_identity':engine.attempt_identity,
    }


def adapter_mode_snapshot(adapter):
    if type(adapter) is PolicyBCapturedFixtureExecutor:
        need(type(adapter.path) is PolicyBProofPath and adapter.path.synthetic_engine is not None, 'POLICY_B_NP_EXECUTOR_ONLY')
        return 'SYNTHETIC',{'adapter_class':'PolicyBCapturedFixtureExecutor','configuration_sha256':sha_bytes(adapter.configuration_bytes())}
    need(type(adapter) in (SyntheticMockExecutor,V3CodexUnitAdapter),'UNAPPROVED_EXECUTOR_INTERFACE')
    if type(adapter) is SyntheticMockExecutor:
        need(not hasattr(adapter,'real_source'),'SYNTHETIC_MOCK_HAS_REAL_MODE_FLAG')
        return 'SYNTHETIC', {'adapter_class':'SyntheticMockExecutor',
                'run_nonce':adapter.run_nonce}
    verify_exact_approved_real_interfaces()
    need(hasattr(adapter,'real_source') and type(adapter.real_source) is bool,
         'EXECUTOR_REAL_SOURCE_UNCONFIGURED_OR_MALFORMED')
    need(adapter.role=='PRIMARY' and adapter.attempt_identity in (None,ATTEMPT),
         'EXECUTOR_ROLE_OR_ATTEMPT_MISMATCH')
    need(adapter.independent_package_root is None,'INDEPENDENT_EXECUTOR_FORBIDDEN')
    info={'adapter_class':'V3CodexUnitAdapter',
          'real_source':adapter.real_source,'role':adapter.role,
          'attempt_identity':adapter.attempt_identity,
          'authorization_path':str(adapter.authorization_path),
          'source_root':str(adapter.source_root),
          'manifest_path':str(adapter.manifest_path),
          'work_root':str(adapter.work_root),
          'codex_path':str(adapter.codex_path),
          'runner_module':getattr(adapter.runner,'__module__',None),
          'runner_name':getattr(adapter.runner,'__qualname__',None),
         }
    if adapter.real_source:
        facts=verify_prospective_context(adapter,phase='STATIC')
        need(type(facts) is dict and type(facts.get('context_identity')) is str and len(facts['context_identity'])==64,
             'PROSPECTIVE_CONTEXT_IDENTITY_REQUIRED')
        info['execution_context_identity']=facts['context_identity']
    return ('REAL' if adapter.real_source else 'SYNTHETIC'),info


def immutable_mode_contract(engine,adapter):
    engine_mode,engine_config=engine_mode_snapshot(engine)
    adapter_mode,adapter_config=adapter_mode_snapshot(adapter)
    need(engine_mode==adapter_mode,'ENGINE_ADAPTER_EXECUTION_MODE_MISMATCH')
    need((engine_mode=='REAL' and type(engine) is BoundCheckpointEngine
          and type(adapter) is V3CodexUnitAdapter) or engine_mode=='SYNTHETIC',
         'REAL_EXECUTION_COMPONENT_PAIRING_INVALID')
    if engine_mode=='REAL':
        # Constructor-time V3 checks are not enough: a previously synthetic
        # adapter can be mutated into real mode after initialization.
        from real_candidate.executor_v1 import run_codex_executor
        need(adapter.runner is run_codex_executor,'REAL_ADAPTER_MUST_USE_PROSPECTIVE_BOUNDED_EXECUTOR')
        verify_prospective_context(adapter,phase='STATIC')
        need(adapter.source_root==engine.source_root and
             adapter.manifest_path==engine.identity_manifest_path and
             str(adapter.authorization_path)==str(engine.authorization_path) and
             adapter.attempt_identity==engine.attempt_identity==ATTEMPT,
             'REAL_ENGINE_ADAPTER_SOURCE_OR_AUTHORIZATION_MISMATCH')
    return {'schema_version':MODE_SCHEMA,'execution_mode':engine_mode,
            'engine_mode':engine_mode,'adapter_mode':adapter_mode,
            'authorization_mode':engine_mode,'expected_provenance_mode':engine_mode,
            'engine_class':type(engine).__name__,'adapter_class':type(adapter).__name__,
            'engine_configuration_sha256':sha_bytes(json_bytes(engine_config)),
            'adapter_configuration_sha256':sha_bytes(json_bytes(adapter_config))}


def case_and_mode_sha(case,mode_contract):
    return sha_bytes(json_bytes({'case_sha256':case_binding_sha(case),
                                 'mode_contract_sha256':sha_bytes(json_bytes(mode_contract))}))


# Compatibility evidence is not execution authorization. All REAL mutation and
# dispatch entry points below remain hard disabled in this correction release.
COMPATIBILITY_BINDING_SHA256 = 'a0fb4907a1cdada02c4cc500cfdc5c840363fb08bd4794510d0404c49b75545e'
REAL_ACTIVATION_GATE_STATE = 'HARD_DISABLED'

def compatibility_binding():
    base=Path(__file__).resolve().parent
    raw=(base/'recovery_compatibility_bounded_v4.json').read_bytes()
    need(sha_bytes(raw)==COMPATIBILITY_BINDING_SHA256,'COMPATIBILITY_BINDING_DRIFT')
    bound=json.loads(raw)
    need(bound.get('finalized') is True,'PROSPECTIVE_BINDING_NOT_FINALIZED')
    historical=(base/'recovery_compatibility_binding.json').read_bytes()
    need(sha_bytes(historical)==bound['historical_compatibility_binding_sha256']==
         '63460e14a99e9e02be8b8a758a2b5c37f0946b81e18e090f751d8bfbad3fdcaa',
         'HISTORICAL_COMPATIBILITY_BINDING_DRIFT')
    prior=json.loads(historical)
    need(all(bound.get(k)==v for k,v in prior.items() if k not in ('schema','checkpoint_files_sha256','checkpoint_logical_identity','historical_attempt_count','historical_attempts')),'HISTORICAL_RECOVERY_CONTRACT_DRIFT')
    need(bound['historical_attempts'][:2]==prior['historical_attempts'] and bound['historical_attempt_count']==9 and len(bound['historical_attempts'])==9,'HISTORICAL_ATTEMPT_PREFIX_DRIFT')
    need(all(bound['checkpoint_files_sha256'].get(k)==v for k,v in prior['checkpoint_files_sha256'].items() if k!='PRIMARY/checkpoint_head.json'),'HISTORICAL_CHECKPOINT_PREFIX_DRIFT')
    # Historical bytes remain mandatory provenance, never an executable module.
    # The existing release verifier enforces their accepted-component custody;
    # the separately pinned Owner source supplies the expected release identity.
    custody=base.parent/'accepted/accepted_recovery/recovery_two_attempt_v3.py'
    need(all(not folder.is_symlink() and folder.is_dir()
             for folder in (custody.parent.parent,custody.parent)) and
         not custody.is_symlink(),'HISTORICAL_RECOVERY_SOURCE_DRIFT')
    need(sha_file(custody)==bound['historical_recovery_source_sha256']==
         '0376a36a82d9e18f45cdcda879c0175c2ec0dd899e32a00b8c59174082460531',
         'HISTORICAL_RECOVERY_SOURCE_DRIFT')
    from real_candidate import release_v1
    import owner_authorization as owner
    need(Path(release_v1.__file__).resolve()==base/'real_candidate/release_v1.py' and
         Path(owner.__file__).resolve()==base/'owner_authorization.py',
         'HISTORICAL_RECOVERY_CUSTODY_MODULE_ORIGIN_DRIFT')
    need(release_v1.verify_release(base.parent)==owner.COMPATIBILITY_RELEASE_SHA,
         'HISTORICAL_RECOVERY_CUSTODY_RELEASE_DRIFT')
    descriptor=strictly_json(base.parent/release_v1.MANIFEST_FILE)
    need(descriptor['accepted_components'].get('HISTORICAL_RECOVERY_V3_SOURCE')=={
             'path':'accepted/accepted_recovery/recovery_two_attempt_v3.py',
             'sha256':bound['historical_recovery_source_sha256']},
         'HISTORICAL_RECOVERY_SOURCE_DRIFT')
    return bound

def verify_attempt_lineage(unit, historical, *, allow_appended=False):
    need(type(historical) is list and len(historical) in (1,2,3,4,5,6,7,8,9,10),'HISTORICAL_LINEAGE_MISSING')
    for i,a in enumerate(historical,1):
        need(type(a) is dict and type(a.get('attempt_number')) is int and
             a['attempt_number']==i,'HISTORICAL_ATTEMPT_ORDER')
    need(len({a['manifest_sha256'] for a in historical})==len(historical) and
         len({a['context_id'] for a in historical if a['context_id'] is not None})==
         sum(a['context_id'] is not None for a in historical), 'DUPLICATE_HISTORICAL_ATTEMPT')
    attempts=unit['attempts'];count=unit['attempt_count']
    need(type(count) is int and type(attempts) is list and count==len(attempts),'ATTEMPT_COUNTER_RESET_OR_DRIFT')
    need(json_bytes(attempts[:len(historical)])==json_bytes(historical),'HISTORICAL_ATTEMPT_LINEAGE_CHANGED')
    need(count==len(historical) or (allow_appended and count==len(historical)+1),'UNAUTHORIZED_ATTEMPT_COUNT')
    need(len({a['manifest_sha256'] for a in attempts})==count and
         len({a['context_id'] for a in attempts if a['context_id'] is not None})==
         sum(a['context_id'] is not None for a in attempts),'DUPLICATE_ATTEMPT_IDENTITY')
    if allow_appended and count>len(historical):
        need(type(attempts[-1]['attempt_number']) is int and
             attempts[-1]['attempt_number']==len(historical)+1,'UNAUTHORIZED_NEXT_ATTEMPT_SEQUENCE')
    return True

CURRENT_CHECKPOINT_MANIFEST = 'c9184a5b8cc0b57499ae0cace5e1a676cd0ca278411334fdaec17f56b1a5572c'
CURRENT_TENTH_ATTEMPT = {'attempt_number':10,
    'context_id':'3ca6a3b385be87481402ae4df0ec064453427e93a53e91c7',
    'manifest_sha256':'66b5d6bb032c3a397c8b10b5ceadd1899456974525849f51e39bc34901fbe996',
    'status':'EXTERNAL_CONFLICT__CONTROLLED_STOP'}
A11_CASE = copy.deepcopy(REAL_CASE)
A11_CASE.update(checkpoint_manifest_sha256=CURRENT_CHECKPOINT_MANIFEST,
                historical_attempts=REAL_CASE['historical_attempts']+[CURRENT_TENTH_ATTEMPT])


def prospective_attempt_context(case, state=None, *, synthetic=False):
    """Exact case-derived ordinal; this returns facts, never execution authority."""
    exact_case(case,case)
    need(type(synthetic) is bool,'INVALID_EXECUTION_MODE')
    history=case.get('historical_attempts')
    need(type(history) is list and len(history) in range(1,11),'INVALID_HISTORICAL_ATTEMPT_COUNT')
    verify_attempt_lineage({'attempts':history,'attempt_count':len(history)},history)
    if len(history)==10:
        if not synthetic:
            need(case==A11_CASE,'A11_CASE_OR_HISTORY_DRIFT')
        else:
            need(type(case['attempt_id']) is str and
                 (case['attempt_id']==ATTEMPT or case['attempt_id'].startswith('SYNTHETIC_'))
                 and case['real_execution_authorized'] is False and
                 case['unit_input_sha256_kind']=='SHA256_OF_RAW_SYNTHETIC_U0012_NEUTRAL_INPUT_BYTES',
                 'A11_CASE_OR_HISTORY_DRIFT')
        if state is not None:
            need(state['checkpoint_sequence']==54 and
                 state['checkpoint_manifest_sha256']==case['checkpoint_manifest_sha256'] and
                 state['units'][11]['state']=='PENDING','A11_CHECKPOINT_CONTEXT_DRIFT')
            verify_attempt_lineage(state['units'][11],history)
    return {'historical_attempt_count':len(history),'next_attempt_sequence':len(history)+1,
            'checkpoint_sequence':54 if len(history)==10 else None}
MEMBERSHIP_SOURCE_SHA256 = '4afebb18b53fa0985dabcf10b56d08427334096c3223fc5b1a7a9698aa79884c'


def _current_declaration(raw, expected_sha256, historical, nonproduction):
    # A caller-supplied digest is an identity input, never Owner authorization.
    # Its authority, current applicability and freshness remain independent gates.
    need(type(raw) is bytes and type(expected_sha256) is str and
         len(expected_sha256)==64 and all(c in '0123456789abcdef' for c in expected_sha256),
         'CURRENT_MEMBERSHIP_DECLARATION_REQUIRED')
    need(sha_bytes(raw)==expected_sha256,'CURRENT_MEMBERSHIP_DECLARATION_DRIFT')
    bound=json.loads(raw)
    need(raw==json_bytes(bound) and set(bound)==set(historical),'CURRENT_DECLARATION_SCHEMA_DRIFT')
    changed={'checkpoint_files_sha256','checkpoint_logical_identity','historical_attempt_count','historical_attempts'}
    need(all(bound[k]==v for k,v in historical.items() if k not in changed),
         'CURRENT_DECLARATION_CONTRACT_DRIFT')
    need(type(bound['historical_attempt_count']) is int and bound['historical_attempt_count']==10 and
         type(bound['historical_attempts']) is list and len(bound['historical_attempts'])==10,
         'CURRENT_HISTORY_COUNT_DRIFT')
    history=bound['historical_attempts']
    need(all(type(a) is dict and set(a)=={'attempt_number','context_id','manifest_sha256','status'}
             for a in history),'CURRENT_HISTORY_SCHEMA_DRIFT')
    verify_attempt_lineage({'attempts':history,'attempt_count':10},history)
    for a in history:
        need(type(a['manifest_sha256']) is str and len(a['manifest_sha256'])==64 and
             all(c in '0123456789abcdef' for c in a['manifest_sha256']) and
             (a['context_id'] is None or type(a['context_id']) is str) and
             a['status'] in ('EXECUTOR_NORMAL_RETURN','EXTERNAL_CONFLICT__CONTROLLED_STOP'),
             'CURRENT_HISTORY_SCHEMA_DRIFT')
    if not nonproduction:
        need(history==historical['historical_attempts']+[CURRENT_TENTH_ATTEMPT],
             'EXACT_CURRENT_HISTORY_DRIFT')
        need(bound['checkpoint_logical_identity']==CURRENT_CHECKPOINT_MANIFEST,'STALE_OR_CHANGED_CHECKPOINT')
        need(all(bound['checkpoint_files_sha256'].get(k)==v
                 for k,v in historical['checkpoint_files_sha256'].items()
                 if k!='PRIMARY/checkpoint_head.json'), 'HISTORICAL_CHECKPOINT_PREFIX_DRIFT')
    pins=bound['checkpoint_files_sha256']
    need(type(pins) is dict and pins and all(type(v) is str and len(v)==64 and
         all(c in '0123456789abcdef' for c in v) for v in pins.values()),'CURRENT_MEMBER_PINS_INVALID')
    logical=bound['checkpoint_logical_identity']
    need(type(logical) is str and len(logical)==64 and all(c in '0123456789abcdef' for c in logical),
         'CURRENT_CHECKPOINT_IDENTITY_INVALID')
    return bound


_SELECTIVE_TASK = 'BATCH0004_C06_MINIMUM_SELECTIVE_CONTENT_VERIFICATION_ENGINEERING_V1'
_B53_ENGINEERING_ROOT = Path('/private/tmp/QTRP_BATCH0004_C06_B53_OS_SEPARATION_HANDOFF_NP_V1')
_B53_OS_RUNTIME = Path('/private/tmp/QTRP_B53_OWNER_EXECUTOR_OS_FIXTURE_NP_V1/runtime')
_SELECTIVE_ROOT = (_B53_OS_RUNTIME if Path(__file__).absolute() ==
                   _B53_OS_RUNTIME/'candidate/recovery_bounded_v4.py' else _B53_ENGINEERING_ROOT)
# Engineering-only declarations authored from literal synthetic specifications,
# independently of observed objects. These are NOT current V4/Owner REAL authority.
_SELECTIVE_EXPECTATION_PINS = frozenset((
    '088bb28f69ef620054c6a38abd09dacea92ef8917731359f0ea9640302c37e70',
    '439f88dd98664796882d1d96b3b83481080670fe8623bd2177ff13bc7a7072dd',
))

_CLASS_B53_CONTRACT = 'CLASS_B53_HASH_ONLY_NONPRODUCTION'
_CLASS_B53_TASK = 'BATCH0004_C06_CLASS_B53_PROTECTED_USE_NONPRODUCTION_QUALIFICATION_V1'
_CLASS_B53_EXPECTATION_PIN = '2effafb7618c54fd8ae0b77a0e121abc27df0902e01e1ac7290c955ebeab00fc'
_CLASS_B53_KEY = 'PRIMARY/checkpoints/checkpoint_000053.json'
_CLASS_B53_BYTES = 13118
# Historical reference only. This is not a protected-access authority or a
# current-content declaration; every callable comparison remains synthetic-only.
_CLASS_B53_HISTORICAL_SHA256 = 'd3183e29c012380ed9b4b17039a8cab4e568acc2f33ee5c03bd5f7bc4bc5c05a'


def verify_selective_content(root=None, *, expectation=None, expectation_sha256=None,
                             authority=None, mode=None, source_context=None, contract=None):
    """Synthetic-only selective comparison using the existing Membership reader.

    Load through the qualified existing composition and supply that module as
    source_context. The Owner's present engineering scope plus source-bound
    synthetic declaration pins is the authority; a caller digest alone is not.
    No live V4 declaration, protected read permission or REAL authority is issued.
    """
    class_b53=type(contract) is str and contract==_CLASS_B53_CONTRACT
    result={'schema':'C06_SELECTIVE_CONTENT_RESULT_V1','mode':'SYNTHETIC_NONPRODUCTION',
        'expectation_identity':None,'selected_count':0,'verified_count':0,
        'classification':'REJECT__SELECTIVE_VERIFICATION_FAILED','read_bytes':0,
        'namespace_stability':'NOT_ESTABLISHED','nonselected_body_reads':0,
        'scientific_parsing_count':0,'real_authority':False}
    if contract is not None:
        result={'schema':'C06_CLASS_B53_HASH_RESULT_V1','expectation_identity':None,
            'result':'REJECT','selected_count':0,'verified_count':0,'read_bytes':0,
            'namespace_stability':'NOT_ESTABLISHED','nonselected_body_reads':0,
            'scientific_parsing_count':0,'real_authority':False,
            'observation_started_utc':datetime.now(timezone.utc).isoformat(),
            'observation_finished_utc':None}
    scope=None
    def check(ok,code):
        if not ok:raise RecoveryReject(code)
    def keys(value):
        check(type(value) is list and len(value)<=256,'SELECTIVE_KEYS')
        check(all(type(k) is str and 0<len(k)<=240 and '\x00' not in k and
              not k.startswith('/') and all(p not in ('','.','..') for p in k.split('/'))
              for k in value),'SELECTIVE_KEYS')
        check(value==sorted(set(value)),'SELECTIVE_KEYS')
        return set(value)
    def pin(value):
        return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)
    try:
        # All mode/root/expectation/class/authority checks precede filesystem access.
        check(contract is None or class_b53,'SELECTIVE_MODE')
        check(type(mode) is str and mode=='SYNTHETIC_NONPRODUCTION','SELECTIVE_MODE')
        check(type(root) in (str,type(Path('/'))),'SELECTIVE_ROOT')
        root=Path(root)
        area=_SELECTIVE_ROOT/('fixtures/class_b53' if class_b53 else 'fixtures/selective_content')
        check(root.is_absolute() and '..' not in root.parts and root!=area and
              root.is_relative_to(area),'SELECTIVE_ROOT')
        check(type(expectation) is bytes and 0<len(expectation)<=32768 and
              pin(expectation_sha256),'SELECTIVE_EXPECTATION')
        d=json.loads(expectation)
        check(type(d) is dict and set(d)=={'schema','scope','expected_regular_files',
              'expected_descendant_directories','namespace_sha256','selected','total_read_budget'}
              and d['schema']==('C06_CLASS_B53_SYNTHETIC_EXPECTATIONS_V1' if class_b53
                                else 'C06_SELECTIVE_EXPECTATIONS_V1') and
              expectation==json_bytes(d),'SELECTIVE_EXPECTATION')
        check(d['scope']=='SYNTHETIC_NONPROTECTED','SELECTIVE_CLASS')
        files=keys(d['expected_regular_files']);directories=keys(d['expected_descendant_directories'])
        check(files and not(files&directories),'SELECTIVE_KEYS')
        for name in files|directories:
            check(all(str(parent) in directories for parent in Path(name).parents
                      if str(parent)!='.'),'SELECTIVE_KEYS')
        namespace={'schema':'C06_EXPECTED_NAMESPACE_V1','regular_files':d['expected_regular_files'],
                   'descendant_directories':d['expected_descendant_directories']}
        check(pin(d['namespace_sha256']) and sha_bytes(json_bytes(namespace))==d['namespace_sha256'],
              'SELECTIVE_NAMESPACE_IDENTITY')
        selected=d['selected']
        check(type(selected) is list and 1<=len(selected)<=16 and
              all(type(v) is dict and set(v)=={'key','sha256','min_bytes','max_bytes','class'}
                  for v in selected),'SELECTIVE_SELECTION')
        chosen=keys([v['key'] for v in selected])
        check(chosen<=files,'SELECTIVE_SELECTION')
        selected_class='B' if class_b53 else 'SYNTHETIC_NONPROTECTED'
        check(all(v['class']==selected_class for v in selected),'SELECTIVE_CLASS')
        check(all(pin(v['sha256']) for v in selected),'SELECTIVE_EXPECTATION')
        check(all(type(v['min_bytes']) is int and type(v['max_bytes']) is int and
                  0<=v['min_bytes']<=v['max_bytes']<=65536 for v in selected),
              'SELECTIVE_BUDGET')
        budget=d['total_read_budget']
        check(type(budget) is int and 0<=budget<=1048576 and
              sum(v['max_bytes'] for v in selected)<=budget,'SELECTIVE_BUDGET')
        if class_b53:
            check(len(selected)==1 and chosen=={_CLASS_B53_KEY},'SELECTIVE_SELECTION')
            check(selected[0]['min_bytes']==selected[0]['max_bytes']==budget==_CLASS_B53_BYTES,
                  'SELECTIVE_BUDGET')
        check(type(authority) is dict and all(type(k) is str and type(v) is str
              for k,v in authority.items()) and authority=={
            'task_id':_CLASS_B53_TASK if class_b53 else _SELECTIVE_TASK,
            'scope':'SOURCE_BOUND_CLASS_B53_SYNTHETIC_FIXTURES_ONLY' if class_b53
                    else 'SOURCE_BOUND_SYNTHETIC_FIXTURES_ONLY',
            'expectation_sha256':expectation_sha256} and
            sha_bytes(expectation)==expectation_sha256 and
            (expectation_sha256==_CLASS_B53_EXPECTATION_PIN if class_b53
             else expectation_sha256 in _SELECTIVE_EXPECTATION_PINS),'SELECTIVE_AUTHORITY')
        result.update(expectation_identity=expectation_sha256,selected_count=len(selected))

        # Reuse the existing qualified composition's exact source-closure checks.
        check(type(source_context) is type(sys) and
              getattr(source_context,'recovery',None) is sys.modules.get(__name__) and
              Path(getattr(source_context,'__file__','')).absolute()==_SELECTIVE_ROOT/'composition.py'
              and Path(__file__).absolute()==_SELECTIVE_ROOT/'candidate/recovery_bounded_v4.py',
              'SELECTIVE_SOURCE_CONTEXT')
        verifier=getattr(source_context,'_verify_nonproduction_sources',None)
        check(callable(verifier) and getattr(verifier,'__globals__',None) is source_context.__dict__
              and verifier.__code__.co_filename==str(_SELECTIVE_ROOT/'composition.py'),
              'SELECTIVE_SOURCE_CONTEXT')
        try:
            verifier()
            check(sha_file(_SELECTIVE_ROOT/'composition.py')==
                  source_context._LOADED_COMPOSITION_SOURCE_SHA256,'SELECTIVE_SOURCE_CONTEXT')
            check(source_context.verify_release(_SELECTIVE_ROOT)==source_context.RELEASE_SHA,
                  'SELECTIVE_SOURCE_CONTEXT')
        except Exception:
            raise RecoveryReject('SELECTIVE_SOURCE_CONTEXT') from None
        base=_SELECTIVE_ROOT/'candidate'
        loaded=sys.modules.get('membership_readonly')
        check(loaded is None or Path(getattr(loaded,'__file__','')).absolute()==base/'membership_readonly.py',
              'SELECTIVE_SOURCE_CONTEXT')
        import membership_readonly
        check(Path(membership_readonly.__file__).absolute()==base/'membership_readonly.py' and
              sha_file(base/'membership_readonly.py')==MEMBERSHIP_SOURCE_SHA256,
              'SELECTIVE_SOURCE_CONTEXT')
        bounded_scope=({'expected_directories':d['expected_descendant_directories'],
                        'selected_body_keys':chosen,'body_read_budget':budget}
                       if class_b53 else {})
        comparison_matches=True
        with membership_readonly.Membership(root,d['expected_regular_files'],**bounded_scope) as scope:
            check(set(scope.directories)-{''}==directories,'SELECTIVE_DIRECTORY_SET')
            # Budget the whole selected operation before opening any member body.
            sizes={v['key']:scope.files[v['key']][2][6] for v in selected}
            check(all(v['min_bytes']<=sizes[v['key']]<=v['max_bytes'] for v in selected),
                  'SELECTIVE_OBJECT_SIZE')
            check(sum(sizes.values())<=budget,'SELECTIVE_BUDGET')
            for v in selected:
                name=v['key']
                check(name in chosen and v['class']==selected_class,
                      'SELECTIVE_SELECTION')
                raw=scope.read(root/name,max_bytes=min(v['max_bytes'],budget-scope.body_read_bytes))
                result['read_bytes']=scope.body_read_bytes
                matches=sha_bytes(raw)==v['sha256']
                if class_b53:
                    # Retain disagreement until normal __exit__ verifies the
                    # complete final namespace and identity interval.
                    comparison_matches=comparison_matches and matches
                    result['verified_count']+=int(matches)
                else:
                    check(matches,'SELECTIVE_CONTENT_MISMATCH')
                    result['verified_count']+=1
            check(set(scope.body_read_paths)<=chosen and len(scope.body_read_paths)==len(selected),
                  'SELECTIVE_READ_SCOPE')
            check(scope.body_read_bytes<=budget,'SELECTIVE_BUDGET')
        # Existing __exit__ completed ancestor and namespace stability checks.
        if class_b53:
            result.update(result='MATCH' if comparison_matches else 'MISMATCH',
                          namespace_stability='STABLE_DURING_VERIFICATION')
        else:
            result.update(classification='MATCH',namespace_stability='STABLE_DURING_VERIFICATION')
    except Exception as exc:
        if scope is not None:
            result['read_bytes']=scope.body_read_bytes
        safe={'SELECTIVE_MODE','SELECTIVE_ROOT','SELECTIVE_EXPECTATION','SELECTIVE_CLASS',
              'SELECTIVE_KEYS','SELECTIVE_NAMESPACE_IDENTITY','SELECTIVE_SELECTION',
              'SELECTIVE_BUDGET','SELECTIVE_AUTHORITY','SELECTIVE_SOURCE_CONTEXT',
              'SELECTIVE_DIRECTORY_SET','SELECTIVE_OBJECT_SIZE','SELECTIVE_CONTENT_MISMATCH',
              'SELECTIVE_READ_SCOPE','MEMBER_READ_BUDGET','MEMBER_SET_MISMATCH','UNEXPECTED_MEMBER',
              'SYMLINK_MEMBER','MULTILINK_MEMBER','INVALID_OBJECT_TYPE','UNSAFE_ROOT',
              'PATH_SUBSTITUTION','DIRECTORY_ALIAS','DIRECTORY_CHANGED','ROOT_OR_ANCESTOR_CHANGED',
              'MEMBER_IDENTITY_CHANGED','MEMBER_CHANGED_DURING_READ','NONCANONICAL_MEMBER_KEY'}
        code=exc.args[0] if len(exc.args)==1 and type(exc.args[0]) is str else None
        if contract is not None:
            result['result']='REJECT'
        else:
            result['classification']='REJECT__'+(code if code in safe else 'SELECTIVE_VERIFICATION_FAILED')
    if contract is not None:
        result['observation_finished_utc']=datetime.now(timezone.utc).isoformat()
    return result


def verify_authoritative_compatibility(root, *, current_binding=None,
                                       expected_binding_sha256=None, nonproduction=False):
    """Existing read-only verifier; never authorizes or arms recovery.

    A new current V4 declaration and independently accepted digest are mandatory.
    Historical inventories cannot supply current membership. Synthetic mode is
    confined to this engineering candidate's explicit fixture namespace.
    """
    try:
        need(type(nonproduction) is bool,'CURRENT_VERIFICATION_MODE_INVALID')
        need(current_binding is not None and expected_binding_sha256 is not None,
             'CURRENT_MEMBERSHIP_DECLARATION_REQUIRED')  # before checkpoint metadata
        historical=compatibility_binding()  # original provenance/custody remains mandatory
        bound=_current_declaration(current_binding,expected_binding_sha256,historical,nonproduction)
        root=Path(root).absolute()
        if nonproduction:
            fixtures=Path(__file__).absolute().parent.parent/'fixtures'
            need(root!=fixtures and root.is_relative_to(fixtures),'SYNTHETIC_ROOT_REQUIRED')
        base=Path(__file__).absolute().parent
        # Check loaded origins before importing a possibly preloaded substitute.
        for name,path in [('membership_readonly',base/'membership_readonly.py'),
                          ('real_candidate.checkpoint_v1',base/'real_candidate/checkpoint_v1.py')]:
            loaded=sys.modules.get(name)
            need(loaded is None or Path(getattr(loaded,'__file__','')).absolute()==path,
                 'CURRENT_RECOVERY_MODULE_ORIGIN_DRIFT')
        import membership_readonly
        from real_candidate import checkpoint_v1
        need(Path(membership_readonly.__file__).absolute()==base/'membership_readonly.py' and
             sha_file(base/'membership_readonly.py')==MEMBERSHIP_SOURCE_SHA256,
             'MEMBERSHIP_SOURCE_DRIFT')
        import owner_authorization as owner
        need(Path(checkpoint_v1.__file__).absolute()==base/'real_candidate/checkpoint_v1.py' and
             sha_file(base/'real_candidate/checkpoint_v1.py')==
             owner.COMPATIBILITY_SOURCE_PINS['real_candidate/checkpoint_v1.py'],
             'ATTESTOR_SOURCE_DRIFT')
        with membership_readonly.Membership(root,bound['checkpoint_files_sha256']) as scope:
            paths=scope.paths
            for name,pin in bound['checkpoint_files_sha256'].items():
                need(sha_bytes(scope.read(paths[name]))==pin,'CHECKPOINT_EVIDENCE_BYTES_CHANGED')
            head=json.loads(scope.read(root/'PRIMARY/checkpoint_head.json'))
            need(head['checkpoint_manifest_sha256']==bound['checkpoint_logical_identity'],
                 'STALE_OR_CHANGED_CHECKPOINT')
            snapshots=[p for n,p in paths.items() if n.startswith('PRIMARY/checkpoints/') and
                       Path(n).name.startswith('checkpoint_') and n.endswith('.json')]
            def exists(path):
                try:name=str(Path(path).relative_to(root))
                except ValueError:raise RecoveryReject('UNDECLARED_METADATA_REQUEST') from None
                return name in paths or name in scope.directories
            a=checkpoint_v1.PersistedCheckpointAttestor(root,
                pinned_checkpoint_sha256=bound['checkpoint_logical_identity'],
                expected_history=bound['historical_attempts'],read_bytes=scope.read,
                snapshot_paths=snapshots,path_exists=exists)
            receipt=a.verify();a.verify_receipt(receipt)
            s=json.loads(scope.read(root/'PRIMARY/checkpoints'/head['snapshot_file']))
            verify_attempt_lineage(s['units'][11],bound['historical_attempts'])
            need(s['units'][11]['state']=='PENDING' and
                 s['units'][11]['frozen_output_sha256'] is None and
                 s['units'][11]['frozen_context_id'] is None and
                 s['units'][11]['executor_attempt_manifest_sha256'] is None,'ATTEMPT2_RETROACTIVE_ACCEPTANCE')
            for attempt in s['units'][11]['attempts']:
                folder=root/'PRIMARY/executor_attempts/U0012'/f"A{attempt['attempt_number']:04d}"
                manifest=scope.read(folder/'executor_attempt_manifest.json')
                m=json.loads(manifest)
                need(sha_bytes(manifest)==attempt['manifest_sha256'] and
                     m['attempt_number']==attempt['attempt_number'] and
                     m['context_id']==attempt['context_id'] and m['status']==attempt['status'],
                     'ATTEMPT_EVIDENCE_BINDING_DRIFT')
                need(type(m['artifacts']) is dict,'ATTEMPT_EVIDENCE_BINDING_DRIFT')
                for name,pin in m['artifacts'].items():
                    artifact=scope.declared_artifact(folder,name)
                    need(sha_bytes(scope.read(artifact))==pin,'ATTEMPT_RAW_EVIDENCE_CHANGED')
            result={'verification_scope':'SYNTHETIC_NONPRODUCTION' if nonproduction else 'READ_ONLY_CURRENT_IDENTITY',
                'checkpoint_identity':receipt.identity,'checkpoint_sequence':receipt.sequence,
                'historical_attempt_count':10,'exact_historical_attempts_verified':True,
                'membership_sha256':expected_binding_sha256,'member_count':len(paths),
                'confined_body_reads':len(scope.body_read_paths),'frozen_rows':receipt.frozen_rows,
                'attempt2_accepted':False,'u0013_attempts':receipt.u0013_attempts,
                'real_activation':'HARD_DISABLED','next_retry_authorized':False}
        return result  # only after the existing before/after namespace checks
    except Exception as exc:
        # Never embed parsed data, member names, paths, OS messages or tracebacks.
        safe_codes={'CURRENT_MEMBERSHIP_DECLARATION_REQUIRED','CURRENT_MEMBERSHIP_DECLARATION_DRIFT',
            'CURRENT_DECLARATION_SCHEMA_DRIFT','CURRENT_DECLARATION_CONTRACT_DRIFT',
            'CURRENT_HISTORY_COUNT_DRIFT','CURRENT_HISTORY_SCHEMA_DRIFT','CURRENT_MEMBER_PINS_INVALID',
            'CURRENT_CHECKPOINT_IDENTITY_INVALID','CURRENT_VERIFICATION_MODE_INVALID','SYNTHETIC_ROOT_REQUIRED',
            'EXACT_CURRENT_HISTORY_DRIFT','STALE_OR_CHANGED_CHECKPOINT','HISTORICAL_CHECKPOINT_PREFIX_DRIFT',
            'CURRENT_RECOVERY_MODULE_ORIGIN_DRIFT','MEMBERSHIP_SOURCE_DRIFT','ATTESTOR_SOURCE_DRIFT',
            'CHECKPOINT_EVIDENCE_BYTES_CHANGED','ATTEMPT_EVIDENCE_BINDING_DRIFT','ATTEMPT_RAW_EVIDENCE_CHANGED',
            'ATTEMPT2_RETROACTIVE_ACCEPTANCE','MEMBER_SET_MISMATCH','UNEXPECTED_MEMBER','SYMLINK_MEMBER',
            'UNSAFE_ROOT','PATH_SUBSTITUTION','DIRECTORY_CHANGED','ROOT_OR_ANCESTOR_CHANGED',
            'MEMBER_IDENTITY_CHANGED','INVALID_OBJECT_TYPE','MULTILINK_MEMBER','NONCANONICAL_MEMBER_KEY',
            'UNDECLARED_BODY_READ','UNDECLARED_DYNAMIC_ARTIFACT','UNSAFE_DYNAMIC_ARTIFACT',
            'MEMBER_CHANGED_DURING_READ','DIRECTORY_ALIAS','DUPLICATE_MEMBER_KEY',
            'HISTORICAL_ATTEMPT_ORDER','DUPLICATE_HISTORICAL_ATTEMPT','HISTORICAL_ATTEMPT_LINEAGE_CHANGED',
            'HISTORICAL_RECOVERY_SOURCE_DRIFT','HISTORICAL_RECOVERY_CUSTODY_RELEASE_DRIFT',
            'HISTORICAL_RECOVERY_CUSTODY_MODULE_ORIGIN_DRIFT','CHECKPOINT_SEQUENCE_INVALID',
            'CHECKPOINT_HEAD_OR_EXTERNAL_ANCHOR_MISMATCH','CHECKPOINT_LINKAGE_MISMATCH',
            'CHECKPOINT_SELF_HASH_MISMATCH','FROZEN_OUTPUT_BINDING_DRIFT','FROZEN_ROW_DIGEST_DRIFT',
            'FROZEN_POSITION_DRIFT','U0012_OR_U0013_ATTEMPT_DRIFT'}
        code=exc.args[0] if len(exc.args)==1 and type(exc.args[0]) is str else None
        raise RecoveryReject(code if code in safe_codes else 'CURRENT_RECOVERY_VERIFICATION_REJECTED') from None

class ExactOneUnitExecutor:
    """Defense in depth: this wrapper can never dispatch any unit except U0012 once."""
    def __init__(self,executor,*,pre_dispatch_check=None,bound_mode_contract=None,mode_check=None,historical_attempt_count=1):
        need(type(executor) in (SyntheticMockExecutor,V3CodexUnitAdapter,PolicyBCapturedFixtureExecutor),
             'UNAPPROVED_EXECUTOR_INTERFACE')
        if type(executor) is V3CodexUnitAdapter:
            verify_exact_approved_real_interfaces()
            need(executor.role=='PRIMARY' and type(executor.real_source) is bool and
                 ((executor.real_source and executor.attempt_identity==ATTEMPT) or
                  (not executor.real_source and type(executor.attempt_identity) is str and
                   executor.attempt_identity.startswith('SYNTHETIC_READINESS_'))),
                 'REAL_EXECUTOR_ROLE_OR_ATTEMPT_MISMATCH')
            need(executor.independent_package_root is None, 'INDEPENDENT_EXECUTOR_FORBIDDEN')
        need(type(historical_attempt_count) is int and historical_attempt_count in range(1,11),'INVALID_HISTORICAL_ATTEMPT_COUNT')
        if historical_attempt_count==10:
            need(callable(pre_dispatch_check) and callable(mode_check) and
                 type(bound_mode_contract) is dict,'A11_FRESH_DISPATCH_BINDING_REQUIRED')
        self._historical_attempt_count=historical_attempt_count
        self._executor=executor;self.calls=0
        self._pre_dispatch_check=pre_dispatch_check
        self._mode_check=mode_check
        self._bound_mode_contract=copy.deepcopy(bound_mode_contract)
    def execute(self,role,unit_id,input_rows,attempt_no,prior_contexts):
        need(role=='PRIMARY' and unit_id=='U0012','U0013_OR_ALTERNATE_UNIT_DISPATCH_FORBIDDEN')
        need(self.calls==0,'DUPLICATE_UNIT_DISPATCH_FORBIDDEN')
        need(type(attempt_no) is int and attempt_no==self._historical_attempt_count+1,'UNAUTHORIZED_NEXT_U0012_ATTEMPT_SEQUENCE')
        need(len(input_rows)==25,'UNIT_INPUT_WRONG_ROW_COUNT')
        need([r['authorized_population_position'] for r in input_rows]==list(range(1776,1801)),
             'EXACT_U0012_POSITIONS_CHANGED')
        # Last executable boundary: re-read the actual persisted checkpoint chain,
        # never accept cached engine.state as proof. No mock/Codex call on failure.
        if self._pre_dispatch_check is not None:
            self._pre_dispatch_check()
        if self._mode_check is not None:
            self._mode_check()  # final executable boundary; cached flags cannot promote authority
        if type(self._executor) is V3CodexUnitAdapter and self._executor.real_source:
            from real_candidate.activation_v1 import production_activation
            production_activation(self._executor.execution_context.transaction,phase='EXECUTING')
        self.calls+=1
        return self._executor.execute(role,unit_id,input_rows,attempt_no,prior_contexts)

class ControlledStopRecovery:
    """Separate append-only recovery journal + sealed single-unit dispatcher.

    Accepts ONLY exact reviewed synthetic and real-checkpoint interfaces.
    Real activation remains a separate existing trusted Managing gate; this
    module never introduces an alternate scientific executor or new authority.
    """
    def __init__(self,engine:CheckpointEngine,case:dict,raw_executor_unit_input:bytes,*,expected_case:dict):
        need(type(engine) in (CheckpointEngine,BoundCheckpointEngine),
             'UNAPPROVED_CHECKPOINT_ENGINE_INTERFACE')
        if type(engine) is BoundCheckpointEngine:
            verify_exact_approved_real_interfaces()
            need(engine.role=='PRIMARY','REAL_ENGINE_ROLE_MISMATCH')
            need(engine.identity_manifest_hash==sha_file(engine.identity_manifest_path),
                 'REAL_IDENTITY_MANIFEST_HASH_DRIFT')
        need(engine.role=='PRIMARY','INDEPENDENT_RECOVERY_FORBIDDEN')
        need(type(raw_executor_unit_input) is bytes,'INPUT_MUST_BE_UNCHANGED_BYTES')
        self._historical_attempts=copy.deepcopy(case.get('historical_attempts',[]))
        need(len(self._historical_attempts) in range(1,11),'MISSING_BOUND_HISTORICAL_ATTEMPTS')
        if len(self._historical_attempts)==10:
            prospective_attempt_context(case,synthetic=not (type(engine) is BoundCheckpointEngine and engine.real_source))
            exact_case(case,expected_case)
        self.engine=engine;self.case=case;self.expected_case=copy.deepcopy(expected_case)
        self.raw_unit_input=raw_executor_unit_input
        self.binding_hash=case_binding_sha(case)
        self.journal=engine.workspace/'recovery_transactions'/self.binding_hash
        self.entry=self.journal/'event_000001_authorized.json'
        self.outcome=self.journal/'event_000002_outcome.json'
        self._prepared=False
        self._dispatched=False
        self._authorized_event_sha256=None
        self._executing_checkpoint_sha256=None
        self._original_stopped_checkpoint_path=None
        self._frozen_bindings=None
        self._bound_adapter=None
        self._bound_mode_contract=None
        self._bound_mode_json=None
        self._bound_mode_sha256=None
        self._bound_auth_class=None
        self._bound_runner=None
        self._bound_execution_context=None
        self._v7_consumer=None
        self._v7_candidate=None
        self._v7_used=False
        self._v7_verification_failure=None
        self._first_rejection=None
        self._v7_verified=None
        self._real_owner_context=None
        self._real_consumption_durable=None

    def bind_v7_verifier(self, path, *, binding, checkpoint, input_path,
                         input_sha256, release_root):
        """Bind the existing proof verifier before execution, not executor claims.

        Trusted runtime wiring supplies the existing BoundProofPath instance.
        Forwarded evidence is untrusted until recovery invokes its verifier.
        This is inert-only integration; no REAL activation/authority is added.
        """
        if type(path) is PolicyBProofPath and type(self.engine) is CheckpointEngine:
            from trusted_stage.staging_v1 import UnitBinding
            need(path.synthetic_engine is self.engine and not hasattr(self.engine,'real_source') and
                 self.case['attempt_id'].startswith('SYNTHETIC_POLICY_B_') and
                 type(binding) is UnitBinding and type(checkpoint) is PolicyBPredecessor and
                 self._real_owner_context is None and not self._dispatched and self._v7_consumer is None,
                 'POLICY_B_EXACT_NP_RECOVERY_REQUIRED')
            self.verify_authorization()
            path.bind_recovery(self,binding,checkpoint,input_path,input_sha256)
            consumer=(path,binding,checkpoint,Path(input_path),input_sha256,Path(release_root),
                      (path.supervisor,path.validator,path.checkpoint_attestor,path.issuer),frozenset(path.supervisor._observed))
            self._v7_consumer=(consumer,self._v7_consumer_snapshot(consumer))
            return self._v7_consumer[1]
        from real_candidate.proof_path_v1 import BoundProofPath
        from trusted_stage.staging_v1 import UnitBinding
        from real_candidate.real_binding_v1 import FutureRealUnitBinding
        need(type(self.engine) is BoundCheckpointEngine,
             'V7_EXACT_BOUND_ENGINE_REQUIRED')
        expected_binding=(FutureRealUnitBinding if self.engine.real_source is True else UnitBinding)
        need(type(path) in (BoundProofPath,PolicyBProofPath) and type(binding) is expected_binding,
             'UNTRUSTED_V7_VERIFIER_INTERFACE')
        need(self._v7_consumer is None and not self._dispatched,
             'V7_VERIFIER_ALREADY_BOUND_OR_DISPATCHED')
        need(type(self.engine) is BoundCheckpointEngine,'V7_EXACT_BOUND_ENGINE_REQUIRED')
        if self._real_owner_context is not None:
            from real_candidate.activation_v1 import verify_owner_real_activation
            verify_owner_real_activation(self)
        else:need(self.engine.real_source is False,'V7_REAL_OWNER_CONTRACT_REQUIRED')
        self.verify_authorization()
        if type(path) is PolicyBProofPath:path.bind_recovery(self,binding,checkpoint,input_path,input_sha256)
        objects=(path.supervisor,path.validator,path.checkpoint_attestor,path.issuer)
        frame=Path(input_path);release=Path(release_root)
        consumer=(path,binding,checkpoint,frame,input_sha256,release,objects,
                  frozenset(path.supervisor._observed))
        snapshot=self._v7_consumer_snapshot(consumer)
        self._v7_consumer=(consumer,snapshot)
        return snapshot

    def _v7_consumer_snapshot(self, consumer):
        from real_candidate.release_v1 import verify_release
        from real_candidate import proof_issuer_v1
        from trusted_stage.staging_v1 import canonical
        import dataclasses
        path,binding,checkpoint,frame,input_sha,release,objects,_=consumer
        if type(path) is PolicyBProofPath and type(self.engine) is CheckpointEngine:
            need(path.synthetic_engine is self.engine and
                 (path.supervisor,path.validator,path.checkpoint_attestor,path.issuer)==objects,
                 'POLICY_B_NP_COMPONENT_DRIFT')
            return path.snapshot_for_recovery(self,binding,checkpoint,frame,input_sha)
        need((path.supervisor,path.validator,path.checkpoint_attestor,path.issuer)==objects,
             'V7_VERIFIER_COMPONENT_SUBSTITUTION')
        need(verify_release(release)==path.release_identity,'V7_RELEASE_IDENTITY_DRIFT')
        binding.verify()
        need(path.supervisor.mode==('REAL' if self.engine.real_source else 'NONPRODUCTION_TEST')
             and path.validator.supervisor is path.supervisor, 'V7_TRUSTED_COMPONENT_MODE_DRIFT')
        path.supervisor._fresh()
        need(path.validator._read_sources()==(self.engine.partition,self.engine.evidence,self.engine.reason),
             'V7_SCIENTIFIC_SOURCE_BINDING_DRIFT')
        rows=unit_evidence(self.engine.partition,self.engine.evidence,'U0012')
        need(frame.resolve().is_relative_to(self.engine.root.parent.resolve()) and
             not frame.is_symlink() and frame.read_bytes()==canonical(rows) and
             sha_bytes(frame.read_bytes())==input_sha==binding.unit_input_sha256,
             'V7_EXACT_INPUT_BINDING_DRIFT')
        need(binding.batch_id=='BATCH0004' and binding.role=='PRIMARY' and binding.unit_id=='U0012' and
             binding.attempt_id==self.case['attempt_id']==ATTEMPT and
             binding.checkpoint_identity==checkpoint.identity==self.case['checkpoint_manifest_sha256'] and
             binding.mode_binding_sha256==path.supervisor.config_sha256 and
             binding.expected_identities==tuple(row['canonical_source_identity'] for row in rows),
             'V7_EXACT_TRANSACTION_BINDING_DRIFT')
        attestor=path.checkpoint_attestor
        need(attestor.root==self.engine.root and attestor._last is checkpoint and
             attestor._recovery_phase is not None and attestor._recovery_phase[0] is self and
             checkpoint._phase is not None, 'V7_CHECKPOINT_PHASE_TRANSACTION_DRIFT')
        issuer=(__import__('real_candidate.policy_b_proof_v1',fromlist=['source_sha']) if type(path) is PolicyBProofPath else proof_issuer_v1)
        need(issuer.source_sha()==path.issuer.issuer_source_sha256,'V7_PROOF_IMPLEMENTATION_DRIFT')
        return json_bytes({'binding':dataclasses.asdict(binding),'frame':str(frame),
            'release':str(release),'release_sha256':path.release_identity,
            'checkpoint_phase_sha256':sha_bytes(checkpoint._phase),
            'case_sha256':case_binding_sha(self.case),'journal':str(self.journal),
            'journal_sha256':self._authorized_event_sha256,'mode_sha256':self._bound_mode_sha256,
            'proof_implementation_sha256':path.issuer.issuer_source_sha256,
            'proof_schema':issuer.VERSION})

    def submit_v7_evidence(self, capture, stage, proof, receipt):
        """Forward existing objects only; this function grants no trust."""
        need(self._v7_consumer is not None and self._dispatched and
             self._executing_checkpoint_sha256 is not None and
             self._v7_candidate is None and not self._v7_used,
             'V7_EVIDENCE_MISSING_PHASE_OR_REPLAY')
        self._v7_candidate=(capture,stage,proof,receipt)

    def _classify_with_v7_evidence(self, result, *, semantic_validator):
        baseline=decide_availability(result,semantic_validator=semantic_validator)
        if self._v7_consumer is None:
            return baseline  # historical consumers and all REAL guards unchanged
        from real_candidate.proof_path_v1 import BoundProofPath
        import availability_classifier_v7_prospective as v7
        active=result.get('raw_stderr')
        active=[line for line in active.splitlines() if line.strip()] if type(active) is str else []
        stops=baseline['conflict_evidence']
        eligible=(len(active)==1 and v7.positive_auxiliary_source(active[0]) and
                  len(stops)==1 and stops[0]['failure_class']=='UNCLASSIFIED_NONEXTERNAL_FAILURE' and
                  stops[0]['source_field'].startswith('raw_stderr[') and
                  not baseline['external_signal_detected'] and
                  not baseline['fields_present_minus_fields_inspected'] and
                  not baseline['malformed_control_fields'])
        if baseline['decision']=='CONTROLLED_STOP' and not eligible:
            self._v7_used=True
            return baseline  # preserve every independent V6 stop and its ledger
        try:
            need(not self._v7_used,'V7_EVIDENCE_REPLAY')
            self._v7_used=True  # failed verification is also single use
            consumer,snapshot=self._v7_consumer
            need(self._v7_consumer_snapshot(consumer)==snapshot,'V7_CONSUMER_IDENTITY_DRIFT')
            self._fresh_pre_dispatch_guard()
            need(type(self._v7_candidate) is tuple and len(self._v7_candidate)==4,
                 'V7_TRUSTED_EVIDENCE_MISSING')
            capture,stage,proof,receipt=self._v7_candidate
            path,binding,checkpoint,frame,input_sha,_,_,old_invocations=consumer
            # Verify before reading observation attributes: a dictionary/success
            # flag is never an observation or an integrity attestation.
            path.supervisor.verify(capture,input_file=frame,pinned_input_sha256=input_sha)
            checked=validate_semantic_unit(self.engine.partition,self.engine.evidence,
                self.engine.reason,'U0012',result,'PRIMARY')
            need(capture.invocation_id not in old_invocations and
                 capture.invocation_id==result.get('context_id') and
                 result.get('process_started') is True and type(result.get('return_code')) is int and
                 result['return_code']==capture.exit_code and
                 result.get('termination_state')==capture.termination and
                 type(result.get('timeout_status')) is bool and result['timeout_status']==capture.timeout and
                 result.get('raw_stdout')==capture.stdout.decode('utf-8') and
                 result.get('raw_stderr')==capture.stderr.decode('utf-8') and
                 result.get('agent_message')==(path.common_text(capture) if type(path) is PolicyBProofPath else path.validator._agent_message(capture)),
                 'V7_EXECUTOR_OBSERVATION_SUBSTITUTION')
            need({**checked,'row_count':25}==receipt.payload,'V7_VALIDATED_PAYLOAD_SUBSTITUTION')
            # Consumer invokes the unchanged accepted verifier itself. Neither
            # the executor nor the forwarder supplies the accepted verdict.
            qualifier=(PolicyBProofPath if type(path) is PolicyBProofPath else BoundProofPath)
            verdict=qualifier.qualify_prospective_only(path,capture=capture,input_path=frame,
                input_sha256=input_sha,stage=stage,proof=proof,receipt=receipt,
                binding=binding,checkpoint=checkpoint)
            need(verdict['historical_v6_verdict']==baseline,'V7_BASELINE_SUBSTITUTION')
            if eligible:
                need(verdict['auxiliary_diagnostic_nonblocking'] is True,
                     'V7_NOT_EXACT_V6_EXCEPTION')
            else:
                need(baseline['decision']=='NO_EXTERNAL_SIGNAL' and
                     verdict['auxiliary_diagnostic_nonblocking'] is False and
                     verdict['classification']==baseline['classification']=='NONE' and
                     verdict['operational_classification']=='NORMAL_SUCCESS',
                     'V7_ORDINARY_SUCCESS_NOT_VERIFIED')
            need(self._v7_consumer_snapshot(consumer)==snapshot,'V7_CONSUMER_CHANGED_DURING_VERIFICATION')
            self._fresh_pre_dispatch_guard()
            self._v7_verified={'invocation_id':capture.invocation_id,'proof_sha256':proof.proof_sha256,
                'checkpoint_before':checkpoint.identity,'executing_checkpoint':self._executing_checkpoint_sha256,
                'recovery_binding_sha256':self.binding_hash,'journal_sha256':self._authorized_event_sha256,
                'owner_authorization_sha256':(path.checkpoint_attestor._recovery_phase[4] if path.checkpoint_attestor is not None else None),
                'owner_consumption_sha256':(path.checkpoint_attestor._recovery_phase[5] if path.checkpoint_attestor is not None else None),
                'proof_domain':(proof.claims.get('PROOF_VERSION')),'policy_b_consumed':type(path) is PolicyBProofPath}
            return verdict
        except Exception as exc:
            from real_candidate.executor_v1 import remember_first_rejection
            remember_first_rejection(self,exc)
            self._v7_verification_failure=str(exc)
            # Existing V6 taxonomy and precedence; add a verifier-observed
            # VALIDATION_FAILURE without editing/hiding the captured stderr.
            return decide_availability({**result,'validation_failure':True},semantic_validator=semantic_validator)

    def _mode_guard(self):
        need(self._bound_mode_contract is not None and self._bound_adapter is not None,
             'EXECUTION_MODE_NOT_BOUND_AT_AUTHORIZATION')
        current=immutable_mode_contract(self.engine,self._bound_adapter)
        need(current==self._bound_mode_contract and
             sha_bytes(json_bytes(current))==self._bound_mode_sha256 and
             json_bytes(current)==self._bound_mode_json,
             'IMMUTABLE_EXECUTION_MODE_DRIFT')
        need(self._bound_auth_class==current['authorization_mode'],
             'AUTHORIZATION_EXECUTION_MODE_DRIFT')
        need(self._real_input_authorization_ok(),
             'TRUSTED_EXECUTION_MODE_AUTHORIZATION_REVOKED')
        if type(self._bound_adapter) is V3CodexUnitAdapter:
            need(self._bound_adapter.runner is self._bound_runner,
                 'REAL_EXECUTOR_RUNNER_CHANGED_AFTER_AUTHORIZATION')
            if self._bound_adapter.real_source:
                need(self._bound_adapter.execution_context is self._bound_execution_context,
                     'PROSPECTIVE_CONTEXT_CHANGED_AFTER_AUTHORIZATION')
        if current['execution_mode']=='REAL':
            need(type(self.engine) is BoundCheckpointEngine and self.engine.real_source is True
                 and type(self._bound_adapter) is V3CodexUnitAdapter and
                 self._bound_adapter.real_source is True,
                 'REAL_DISPATCH_REQUIRES_REAL_ENGINE_REAL_ADAPTER')
        return True

    def _bind_mode_at_authorization(self,adapter):
        need(self._bound_mode_contract is None and not self._prepared,
             'EXECUTION_MODE_ALREADY_BOUND')
        contract=immutable_mode_contract(self.engine,adapter)
        need(self._real_input_authorization_ok(),
             'EXECUTION_AUTHORIZATION_MODE_REJECTED')
        self._bound_adapter=adapter
        self._bound_mode_contract=copy.deepcopy(contract)
        self._bound_mode_json=json_bytes(contract)
        self._bound_mode_sha256=sha_bytes(self._bound_mode_json)
        self._bound_auth_class=contract['authorization_mode']
        self._bound_runner=(adapter.runner if type(adapter) is V3CodexUnitAdapter else None)
        self._bound_execution_context=(adapter.execution_context if type(adapter) is V3CodexUnitAdapter else None)
        if type(self.engine) is BoundCheckpointEngine and not self.engine.real_source:
            self.engine._owner_transaction=self  # NP budget locator, never REAL authority
        self.binding_hash=case_and_mode_sha(self.case,contract)
        self.journal=self.engine.workspace/'recovery_transactions'/self.binding_hash
        self.entry=self.journal/'event_000001_authorized.json'
        self.outcome=self.journal/'event_000002_outcome.json'
        self._mode_guard()
        return contract

    def _partition_binding_ok(self, persisted):
        # BoundCheckpointEngine records DERIVED contract bytes in checkpoint;
        # REAL_CASE pins the separately immutable IDENTITY-BOUND manifest.
        if type(self.engine) is BoundCheckpointEngine:
            return (self.case['partition_manifest_sha256']==self.engine.identity_manifest_hash
                    and sha_file(self.engine.identity_manifest_path)==self.engine.identity_manifest_hash
                    and persisted['partition_manifest_sha256']==self.engine.input_hashes['partition_manifest.json'])
        return persisted['partition_manifest_sha256']==self.case['partition_manifest_sha256']

    def _real_input_authorization_ok(self):
        if self._real_owner_context is not None:
            import owner_authorization as owner
            try:owner.verify_real_recovery_context(self)
            except Exception as exc:raise RecoveryReject(str(exc)) from exc
            return self.case['real_execution_authorized'] is False and (not self.engine.real_source or
                self.case==(A11_CASE if len(self._historical_attempts)==10 else REAL_CASE))
        # Readonly configuration/provenance is not execution authority.
        if type(self.engine) is BoundCheckpointEngine and self.engine.real_source:return False
        return self.case['real_execution_authorized'] is False

    def _fresh_persisted_checkpoint(self, *, expected_checkpoint_sha256, expected_u0012_state):
        """Re-read and verify complete persisted chain, frozen bytes and case binding.

        Not an in-memory state comparison. Accepted V6 .verify() rereads the head,
        ALL checkpoint snapshots, clean inputs, 11 frozen outputs, executor evidence,
        and strict validator. The original stop history must remain in the chain.
        This function performs no checkpoint or journal write.
        """
        try:
            # Explicit fresh filesystem read, independent of cached engine.state.
            persisted=self.engine._read_snapshot_chain()
            need(persisted['checkpoint_manifest_sha256']==expected_checkpoint_sha256,
                 'PERSISTED_CHECKPOINT_IDENTITY_DRIFT')
            verified=self.engine.verify(expected_attempt_id=self.case['attempt_id'])
            s=verified.state
            need(s['checkpoint_manifest_sha256']==expected_checkpoint_sha256 and
                 s['checkpoint_manifest_sha256']==persisted['checkpoint_manifest_sha256'],
                 'PERSISTED_CHECKPOINT_CHANGED_DURING_FULL_VERIFICATION')
            need(s['global_state']==NON_RESUMABLE and s['role']=='PRIMARY',
                 'PERSISTED_STOP_STATE_CHANGED')
            need(s['first_unfinished_unit']=='U0012' and len(s['units'])==20,
                 'PERSISTED_FIRST_UNFINISHED_UNIT_CHANGED')
            need([u['state'] for u in s['units'][:11]]==['FROZEN']*11 and
                 all(u['state']=='PENDING' for u in s['units'][12:]),
                 'PERSISTED_FROZEN_PREFIX_OR_SUFFIX_CHANGED')
            u=s['units'][11]
            need(u['unit_id']=='U0012' and u['state']==expected_u0012_state and
                 verify_attempt_lineage(u,self._historical_attempts) and
                 u['attempts'][0]['status']=='EXECUTOR_NORMAL_RETURN' and
                 u['frozen_output_sha256'] is None,
                 'PERSISTED_U0012_STATE_OR_HISTORICAL_ATTEMPT_CHANGED')
            need([u['frozen_output_sha256'] for u in s['units'][:11]]==self._frozen_bindings,
                 'PERSISTED_FROZEN_UNIT_BINDINGS_CHANGED')
            need(self._partition_binding_ok(s) and
                 s['semantic_rule_identity_sha256']==self.case['semantic_rule_sha256'] and
                 s['reason_precedence_identity_sha256']==self.case['reason_precedence_sha256'],
                 'PERSISTED_SCIENTIFIC_IDENTITIES_CHANGED')
            need(s['attempt_identity']==self.case['attempt_id'],
                 'PERSISTED_ATTEMPT_CHANGED')
            # The original stopped checkpoint must remain an unmodified element
            # in the immutable persisted chain, including the original failure.
            original=self._original_stopped_checkpoint_path
            need(original.is_file() and not original.is_symlink(),
                 'ORIGINAL_CONTROLLED_STOP_SNAPSHOT_MISSING')
            stop=strictly_json(original)
            need(stop['checkpoint_manifest_sha256']==self.case['checkpoint_manifest_sha256'] and
                 stop['global_state']==NON_RESUMABLE and
                 stop['stop_reason']==self.case['original_stop_reason'],
                 'ORIGINAL_CONTROLLED_STOP_SNAPSHOT_CHANGED')
            # Check current head again to catch intervening checkpoint updates.
            reread=self.engine._read_snapshot_chain()
            need(reread['checkpoint_manifest_sha256']==expected_checkpoint_sha256,
                 'PERSISTED_CHAIN_TOCTOU_CHANGED')
            return s
        except Exception as exc:
            if len(self._historical_attempts)==10:
                raise FreshCheckpointIntegrityError('PERSISTED_CHECKPOINT_VERIFICATION_FAILED') from None
            raise FreshCheckpointIntegrityError('PERSISTED_CHECKPOINT_VERIFICATION_FAILED__'+str(exc)) from exc

    def _fresh_pre_mutation_guard(self):
        self._fresh_persisted_checkpoint(
            expected_checkpoint_sha256=self.case['checkpoint_manifest_sha256'],
            expected_u0012_state='PENDING')
        self.verify_authorization_event_only()
        self._mode_guard()
        return True

    def _fresh_pre_dispatch_guard(self):
        need(self._executing_checkpoint_sha256 is not None,
             'NO_VERIFIED_EXECUTING_CHECKPOINT')
        self._fresh_persisted_checkpoint(
            expected_checkpoint_sha256=self._executing_checkpoint_sha256,
            expected_u0012_state='EXECUTING')
        self.verify_authorization_event_only(allow_dispatched=True)
        self._mode_guard()
        return True

    def verify_authorization_event_only(self, *, allow_dispatched=False):
        """Verify immutable sidecar journal; NEVER substitutes for disk checkpoint."""
        need(self._prepared and (allow_dispatched or not self._dispatched),'RECOVERY_NOT_ARMED_OR_ALREADY_DISPATCHED')
        need(self.entry.is_file() and not self.entry.is_symlink() and not self.outcome.exists(),
             'RECOVERY_EVENT_MISSING_OR_ALREADY_TERMINAL')
        data=strictly_json(self.entry)
        need(self._authorized_event_sha256 is not None and sha_file(self.entry)==self._authorized_event_sha256
             and self.entry.read_bytes()==json_bytes(data),'RECOVERY_EVENT_ANY_BYTE_MODIFICATION')
        need(data['transition_to']==RECOVERY_STATE and data['recovery_binding_sha256']==self.binding_hash and
             data['unit_id']=='U0012' and data['max_new_units']==1,'RECOVERY_EVENT_TAMPERED')
        need(self.case==self.expected_case,'RECOVERY_CASE_DRIFT')
        need(json_bytes(data['historical_attempts'])==json_bytes(self._historical_attempts) and
             data['historical_attempt_count']==len(self._historical_attempts),'RECOVERY_EVENT_HISTORY_DRIFT')
        need(data.get('execution_mode_binding_sha256')==self._bound_mode_sha256
             and data.get('execution_mode_contract')==self._bound_mode_contract
             and self.binding_hash==case_and_mode_sha(self.case,self._bound_mode_contract),
             'RECOVERY_EVENT_EXECUTION_MODE_BINDING_MISMATCH')
        need(data['checkpoint_before_sha256']==self.case['checkpoint_manifest_sha256'],
             'RECOVERY_EVENT_ORIGINAL_CHECKPOINT_MISMATCH')
        return True

    def proof_checkpoint_binding(self, *, owner_authorization_sha256,
                                 owner_consumption_sha256, executing):
        """Read-only phase binding for the already authorized transaction.

        The publication identity is a trusted input from prior independent
        publication readback, NOT authority created by this method. Its exact
        durable consumption must already exist. No authorization, consumption,
        mutation, retry or REAL activation is performed here.
        """
        need(type(executing) is bool, 'PROOF_PHASE_INVALID')
        for pin in (owner_authorization_sha256, owner_consumption_sha256):
            need(type(pin) is str and len(pin)==64 and
                 set(pin)<=set('0123456789abcdef'), 'PROOF_OWNER_PIN_INVALID')
        need(self._dispatched is executing, 'PROOF_RECOVERY_PHASE_MISMATCH')
        if executing:
            self._fresh_pre_dispatch_guard()
        else:
            self._fresh_pre_mutation_guard()
        count=len(self._historical_attempts)
        need(count in (9,10) and (count==10 or self.case['attempt_id']==ATTEMPT),
             'PROOF_REQUIRES_EXACT_ATTEMPT_TEN_OR_ELEVEN')
        if count==10:
            prospective_attempt_context(self.case,synthetic=not (type(self.engine) is BoundCheckpointEngine and self.engine.real_source))
        need(sha_bytes(self.raw_unit_input)==self.case['unit_input_sha256'],
             'PROOF_INPUT_BINDING_DRIFT')
        consumed=self.journal/'owner_authorization_consumed.json'
        need(consumed.is_file() and not consumed.is_symlink(), 'PROOF_CONSUMPTION_MISSING')
        raw=consumed.read_bytes()
        data=json.loads(raw)
        need(raw==json_bytes(data) and sha_bytes(raw)==owner_consumption_sha256,
             'PROOF_CONSUMPTION_BYTES_DRIFT')
        need(data.get('authorization_identity')==owner_authorization_sha256 and
             data.get('checkpoint_before')==self.case['checkpoint_manifest_sha256'] and
             data.get('unit_id')=='U0012' and type(data.get('max_new_units')) is int and
             data['max_new_units']==1 and data.get('real_execution_authorized') is False,
             'PROOF_OWNER_BINDING_DRIFT')
        if data.get('schema')=='OWNER_REAL_AUTHORIZATION_CONSUMPTION_V1':
            import owner_authorization as owner
            owner.verify_real_consumption_context(self)
            need(self._real_owner_context[0]==owner_authorization_sha256 and
                 data['scope']==owner.publication.real_publication_contract(
                     owner.derive_target(checkpoint_phase='FACTS',prospective_a11=count==10))[1],
                 'PROOF_REAL_OWNER_SCOPE_DRIFT')
        elif data.get('schema')=='OWNER_AUTHORIZATION_CONSUMPTION_V1':
            need(data.get('scope')=='INERT_U0012_ATTEMPT3_ONLY__REAL_EXECUTION_FORBIDDEN'
                 and type(data.get('next_attempt_sequence')) is int and
                 data['next_attempt_sequence']==3, 'PROOF_OWNER_SCOPE_DRIFT')
        else:
            need(data.get('schema')=='NONPRODUCTION_TEST_ONLY_CONSUMPTION_V1' and
                 data.get('authority')=='MOCKED_NOT_OWNER_PUBLICATION' and
                 data.get('attempt')==(self.case['attempt_id'] if count==10 else ATTEMPT)
                 and type(data.get('ordinal')) is int and
                 data['ordinal']==count+1, 'PROOF_OWNER_SCOPE_DRIFT')
        return json_bytes({'checkpoint_before':self.case['checkpoint_manifest_sha256'],
            'checkpoint_root':str(self.engine.root), 'attempt_id':self.case['attempt_id'],
            'attempt_ordinal':count+1, 'unit_id':'U0012', 'max_new_units':1,
            'case_sha256':case_binding_sha(self.case),
            'input_sha256':sha_bytes(self.raw_unit_input),
            'recovery_binding_sha256':self.binding_hash,
            'journal':str(self.journal), 'journal_sha256':self._authorized_event_sha256,
            'mode_contract':self._bound_mode_contract,
            'mode_contract_sha256':self._bound_mode_sha256,
            'owner_authorization_sha256':owner_authorization_sha256,
            'owner_consumption_sha256':owner_consumption_sha256})

    def check_preconditions(self):
        exact_case(self.case,self.expected_case)
        if type(self.engine) is BoundCheckpointEngine and self.engine.real_source and self._real_owner_context is None:
            need(self.case==(A11_CASE if len(self._historical_attempts)==10 else REAL_CASE)
                 and self.case['real_execution_authorized'] is False and
                 self.engine.verify_readonly_configuration(),'REAL_INPUT_PROVENANCE_BINDING_INVALID')
        else:need(self._real_input_authorization_ok(),'REAL_INPUT_AUTHORIZATION_BINDING_INVALID')
        need(sha_bytes(self.raw_unit_input)==self.case['unit_input_sha256'],'UNIT_INPUT_SHA256_MISMATCH')
        try:
            rows=[json.loads(line) for line in self.raw_unit_input.decode('utf-8').splitlines() if line.strip()]
        except (ValueError,UnicodeError) as exc:
            raise RecoveryReject('UNIT_INPUT_NOT_VALID_JSONL') from exc
        need(len(rows)==25 and rows==unit_evidence(self.engine.partition,self.engine.evidence,'U0012'),
             'UNIT_INPUT_CONTENT_NOT_IDENTICAL_TO_FROZEN_ASSIGNMENT')
        need([r['authorized_population_position'] for r in rows]==list(range(1776,1801)) and
             all(type(r['authorized_population_position']) is int for r in rows),
             'UNIT_INPUT_POSITION_TYPE_OR_ORDER_CHANGED')
        needed_kind=('SHA256_OF_RAW_U0012_EXECUTOR_NEUTRAL_JSONL_BYTES'
                     if type(self.engine) is BoundCheckpointEngine and self.engine.real_source
                     else 'SHA256_OF_RAW_SYNTHETIC_U0012_NEUTRAL_INPUT_BYTES')
        need(self.case['unit_input_sha256_kind']==needed_kind, 'UNIT_INPUT_AUTHORIZATION_KIND_INVALID')
        self.engine.verify(expected_attempt_id=self.case['attempt_id'])
        s=self.engine.state
        if len(self._historical_attempts)==10:
            prospective_attempt_context(self.case,s,synthetic=not (type(self.engine) is BoundCheckpointEngine and self.engine.real_source))
        need(s['global_state']==NON_RESUMABLE,'CHECKPOINT_NOT_CONTROLLED_STOP')
        need(s['checkpoint_manifest_sha256']==self.case['checkpoint_manifest_sha256'],'WRONG_CHECKPOINT_OR_REPLAY')
        need(s['stop_reason']==self.case['original_stop_reason'],'ORIGINAL_CONTROLLED_STOP_NOT_PINNED')
        need(s['first_unfinished_unit']=='U0012'==self.case['first_unfinished_unit'], 'FIRST_UNFINISHED_NOT_U0012')
        need(s['role']=='PRIMARY' and s['attempt_identity']==self.case['attempt_id'],'ROLE_ATTEMPT_MISMATCH')
        need(self._partition_binding_ok(s),'PARTITION_HASH_MISMATCH')
        need(s['semantic_rule_identity_sha256']==self.case['semantic_rule_sha256'],'SEMANTIC_RULE_HASH_MISMATCH')
        need(s['reason_precedence_identity_sha256']==self.case['reason_precedence_sha256'],'REASON_PRECEDENCE_HASH_MISMATCH')
        units=s['units']
        need(len(units)==20 and [u['state'] for u in units[:11]]==['FROZEN']*11,'FROZEN_PREFIX_CHANGED')
        need(all(u['state']=='PENDING' for u in units[11:]),'PENDING_SUFFIX_CHANGED')
        need(s['first_unfinished_unit']=='U0012' and verify_attempt_lineage(units[11],self._historical_attempts) and
             units[11]['frozen_output_sha256'] is None,'FAILED_U0012_NOT_PRESERVED_AS_UNACCEPTED')
        need(units[11]['attempts'][0]['status']=='EXECUTOR_NORMAL_RETURN','FAILED_U0012_ATTEMPT_MISSING')
        need(units[11]['position_start']==1776 and units[11]['position_end']==1800,'U0012_ASSIGNMENT_CHANGED')
        need(len([u for u in units if u['state']=='FROZEN'])*25==275,'FROZEN_ROW_COUNT_NOT_275')
        need(not self.journal.exists() and not self.journal.is_symlink(),'RECOVERY_BINDING_REPLAY_FORBIDDEN')
        self._frozen_bindings=[u['frozen_output_sha256'] for u in units[:11]]
        self._original_stopped_checkpoint_path=self.engine.workspace/'checkpoints'/f"checkpoint_{s['checkpoint_sequence']:06d}.json"
        # Do NOT trust cached state, including in an authorization after a previous
        # engine.verify(). This guard rereads disk before even creating a sidecar.
        self._fresh_persisted_checkpoint(expected_checkpoint_sha256=self.case['checkpoint_manifest_sha256'],
                                         expected_u0012_state='PENDING')
        return True

    def authorize_nonproduction(self,executor):
        need(self._real_owner_context is None,'REAL_DOMAIN_REQUIRES_OWNER_RECOVERY_ENTRYPOINT')
        need(not (type(self.engine) is BoundCheckpointEngine and self.engine.real_source),
             'REAL_ACTIVATION_HARD_DISABLED__NO_NEW_AUTHORIZATION')
        return self._reserve_exact_recovery(executor)

    def authorize_real_domain(self,executor):
        import owner_authorization as owner
        owner.verify_real_recovery_context(self)
        need(self._real_owner_context[2] is executor,'OWNER_BOUND_EXECUTOR_SUBSTITUTED')
        return self._reserve_exact_recovery(executor)

    def _serialization_context(self):
        adapter=self._bound_adapter
        context=getattr(adapter,'execution_context',None) if adapter is not None else None
        if type(self.engine) is BoundCheckpointEngine and self.engine.real_source:
            need(context is not None,'REAL_RECOVERY_EXECUTION_CONTEXT_REQUIRED')
        return context

    def _bounded_json(self,data,*,ascii=True):
        context=self._serialization_context()
        if context is None:return json_bytes(data) if ascii else obj_bytes(data)
        from real_candidate.executor_v1 import serialization_size
        maximum=context.storage_contract()['artifact_bytes']
        serialization_size(data,maximum,ensure_ascii=ascii,indent=None,separators=(',',':'),allow_nan=True)
        raw=(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=ascii)+'\n').encode('utf-8')
        need(len(raw)<=maximum,'RECOVERY_SERIALIZATION_LIMIT')
        return raw

    def _capacity_before_reservation(self):
        context=self._serialization_context()
        if context is not None:
            from real_candidate.executor_v1 import _ensure_capacity
            _ensure_capacity(context.evidence_root,context.storage_contract()['peak_storage_bytes'])

    def _reserve_exact_recovery(self,executor):
        if len(self._historical_attempts)==10:
            prospective_attempt_context(self.case,self.engine.verify().state,
                synthetic=not (type(self.engine) is BoundCheckpointEngine and self.engine.real_source))
        if self._real_owner_context is not None or (type(self.engine) is BoundCheckpointEngine and self.engine.real_source):
            import owner_authorization as owner
            owner.verify_real_recovery_context(self)
        self._bind_mode_at_authorization(executor)
        self.check_preconditions()
        # Last possible fresh check before the FIRST recovery journal mutation.
        self._fresh_persisted_checkpoint(expected_checkpoint_sha256=self.case['checkpoint_manifest_sha256'],
                                         expected_u0012_state='PENDING')
        self._mode_guard()  # no sidecar write before a fresh trusted-mode check
        prior=self.engine.state
        self._capacity_before_reservation()
        self.journal.mkdir(parents=True,exist_ok=False)
        data={'schema_version':'BATCH0004_APPEND_ONLY_RECOVERY_EVENT_V1',
            'transition_from':NON_RESUMABLE,'transition_to':RECOVERY_STATE,
            'checkpoint_before_sha256':prior['checkpoint_manifest_sha256'],
            'original_stop_reason':prior['stop_reason'],
            'original_u0012_failed_attempt_sha256':prior['units'][11]['attempts'][0]['manifest_sha256'],
            'historical_attempts':copy.deepcopy(self._historical_attempts),
            'historical_attempt_count':len(self._historical_attempts),
            'frozen_prefix_sha256':digest([u['frozen_output_sha256'] for u in prior['units'][:11]]),
            'recovery_binding_sha256':self.binding_hash,'role':'PRIMARY','unit_id':'U0012',
            'max_new_units':1,'original_snapshots_immutable':True,
            'execution_mode_contract':self._bound_mode_contract,
            'execution_mode_binding_sha256':self._bound_mode_sha256}
        data_raw=self._bounded_json(data)
        unique_write(self.entry,data_raw)
        need(strictly_json(self.entry)==data and sha_file(self.entry)==sha_bytes(data_raw),
             'RECOVERY_TRANSITION_READBACK_FAILED')
        need(self.engine.verify().state['checkpoint_manifest_sha256']==prior['checkpoint_manifest_sha256'],
             'PREEXISTING_CHECKPOINT_CHANGED_DURING_RECOVERY_AUTHORIZATION')
        self._authorized_event_sha256=sha_file(self.entry)
        self._prepared=True
        return data

    def verify_authorization(self):
        self.verify_authorization_event_only()
        self._mode_guard()
        # Always refresh from persisted checkpoint; cached state cannot authorize.
        self._fresh_persisted_checkpoint(expected_checkpoint_sha256=self.case['checkpoint_manifest_sha256'],
                                         expected_u0012_state='PENDING')
        self._mode_guard()
        return True

    def run_exact_unit_nonproduction(self,executor):
        if type(executor) is PolicyBCapturedFixtureExecutor:
            try:
                need(type(self.engine) is CheckpointEngine and not hasattr(self.engine,'real_source') and
                     self._real_owner_context is None and not self._dispatched and not self._v7_used and
                     self._bound_adapter is executor and self._v7_consumer is not None,
                     'POLICY_B_NP_WRONG_STATE_OR_REPLAY')
                self.verify_authorization()
                consumer,snapshot=self._v7_consumer
                need(type(consumer[0]) is PolicyBProofPath and self._v7_consumer_snapshot(consumer)==snapshot,
                     'POLICY_B_NP_CONSUMER_DRIFT')
                if executor._capture_request is not None:
                    executor.verify_capture_request()
                else:
                    consumer[0].verify_prepared()
                    need(consumer[0]._candidate[0].invocation_id not in consumer[7],'POLICY_B_NP_STALE_CAPTURE')
                self._fresh_pre_mutation_guard()
            except Exception as exc:
                self._dispatched=True;self._v7_used=True
                raise RecoveryReject('POLICY_B_NP_PREMUTATION_REJECTION__'+str(exc)) from exc
        need(self._real_owner_context is None,'REAL_DOMAIN_REQUIRES_OWNER_RECOVERY_ENTRYPOINT')
        return self._run_exact_recovery(executor)

    def run_exact_unit_owner_authorized(self,executor):
        need(self._real_owner_context is not None,'REAL_OWNER_CONTEXT_REQUIRED')
        return self._run_exact_recovery(executor)

    def _run_exact_recovery(self,executor):
        # Exact consumed Owner authority and the unchanged PENDING checkpoint
        # are independently verified before the first REAL checkpoint mutation.
        try:
            if type(self.engine) is BoundCheckpointEngine and self.engine.real_source:
                from real_candidate.activation_v1 import production_activation
                production_activation(self,phase='RESERVED')
            else:
                need(self._real_owner_context is None,'REAL_OWNER_AUTHORITY_REQUIRES_REAL_ENGINE')
            need(executor is self._bound_adapter,'EXECUTOR_CHANGED_AFTER_AUTHORIZATION')
            self._mode_guard()
            self.verify_authorization()
            # Independent final guard before any EXECUTING snapshot is written.
            self._fresh_pre_mutation_guard()
        except (FreshCheckpointIntegrityError,RecoveryReject):
            self._dispatched=True  # fail-closed: no bypass or retry on same transaction
            return 'CONTROLLED_STOP'
        self._dispatched=True  # permanent even on exception/crash
        engine=self.engine
        u=engine.state['units'][11]
        need(u['unit_id']=='U0012' and u['state']=='PENDING','UNIT_NOT_PENDING')
        if len(self._historical_attempts)==10:
            prospective_attempt_context(self.case,engine.state,
                synthetic=not (type(engine) is BoundCheckpointEngine and engine.real_source))
        self._mode_guard()
        executor=ExactOneUnitExecutor(executor,pre_dispatch_check=self._fresh_pre_dispatch_guard,
                                      bound_mode_contract=self._bound_mode_contract,
                                      mode_check=self._mode_guard,historical_attempt_count=len(self._historical_attempts))
        need(immutable_mode_contract(engine,self._bound_adapter)==self._bound_mode_contract,
             'ENGINE_EXECUTOR_PAIRING_INVALID')
        prior_contexts={a['context_id'] for item in engine.state['units'] for a in item['attempts'] if a['context_id']}
        old_frozen=[sha_file(engine.workspace/'frozen_units'/f'U{i:04d}'/'unit_result.json') for i in range(1,12)]
        initial_attempt=u['attempts'][0]['manifest_sha256']
        input_rows=unit_evidence(engine.partition,engine.evidence,'U0012')
        before_input=digest(input_rows)
        u['state']='EXECUTING';engine._snapshot()
        self._executing_checkpoint_sha256=engine.state['checkpoint_manifest_sha256']
        u=engine.state['units'][11]
        try:
            result=executor.execute('PRIMARY','U0012',input_rows,u['attempt_count']+1,tuple(prior_contexts))
        except (FreshCheckpointIntegrityError,RecoveryReject):
            # Do not mutate a checkpoint or dispatch after mode/checkpoint drift.
            # The sidecar has been authorized and an EXECUTING snapshot may have
            # been appended before an adversarial change, but no executor is called.
            return 'CONTROLLED_STOP'
        except Exception as exc:
            from real_candidate.executor_v1 import remember_first_rejection
            remember_first_rejection(self,exc)
            u['state']='PENDING';engine.state['global_state']=NON_RESUMABLE
            engine.state['stop_reason']='EXACT_U0012_RECOVERY_EXECUTOR_FAILURE__'+type(exc).__name__
            engine._snapshot(); outcome='CONTROLLED_STOP'
            return self._finish(outcome,old_frozen,initial_attempt,executor.calls)

        # Fresh disk verification replaces the cached engine.state object. Rebind
        # the local unit before recording the new executor result.
        u=engine.state['units'][11]
        try:
            self._mode_guard()
            # Synthetic mocks simulate process_started=True. This cannot prove
            # a real Codex launch and must not be used for mode/provenance.
            if self._bound_mode_contract['execution_mode']=='SYNTHETIC':
                need(result.get('codex_subprocess_started') in (None,False) and
                     result.get('real_codex_subprocess_started') in (None,False) and
                     result.get('provenance_mode') in (None,'SYNTHETIC') and
                     result.get('synthetic_only') in (None,True),
                     'SYNTHETIC_EXECUTOR_CLAIMS_REAL_PROVENANCE')
            else:
                need(result.get('provenance_mode') in (None,'REAL') and
                     result.get('synthetic_only') in (None,False),
                     'REAL_EXECUTOR_CLAIMS_SYNTHETIC_PROVENANCE')
        except RecoveryReject as exc:
            u['state']='PENDING';engine.state['global_state']=NON_RESUMABLE
            engine.state['stop_reason']='EXECUTION_MODE_OR_PROVENANCE_FAILURE__'+str(exc)
            engine._snapshot()
            return self._finish('CONTROLLED_STOP',old_frozen,initial_attempt,executor.calls)

        def validate_for_availability(payload):
            checked=validate_semantic_unit(engine.partition,engine.evidence,engine.reason,'U0012',
                {**result,'agent_message':canonical_json(payload)},'PRIMARY')
            assigned=engine.partition['units'][11]
            need([r['authorized_population_position'] for r in checked['raw_rows']]==assigned['positions'],
                 'U0012_RAW_POSITION_SEQUENCE_CHANGED')
            need([r['canonical_source_identity'] for r in checked['raw_rows']]==assigned['canonical_source_identities'],
                 'U0012_RAW_IDENTITIES_CHANGED')
        decision=self._classify_with_v7_evidence(result,semantic_validator=validate_for_availability)
        # Independent evidence verification refreshes persisted engine.state.
        # Record/finalize against that verified unit, never the prior object.
        u=engine.state['units'][11]
        if self._v7_verified is not None:
            decision={**decision,'verified_operational_proof':copy.deepcopy(self._v7_verified)}
        result['availability_evidence']=decision
        if decision['decision']=='CONTROLLED_STOP':
            from real_candidate.executor_v1 import remember_first_rejection,first_rejection_fields
            remember_first_rejection(self)
            # Observability only: append AFTER classification; never feed these
            # fields to the scientific/availability decision or proof verifier.
            result['availability_evidence']={**decision,**first_rejection_fields(self)}
        external=decision['classification'] if decision['decision']=='PAUSED_EXTERNAL_AVAILABILITY' else None
        status=('EXTERNAL_CONFLICT__CONTROLLED_STOP' if decision['decision']=='CONTROLLED_STOP' else
                ('EXTERNALLY_INTERRUPTED' if external else
                 ('EXECUTOR_NORMAL_RETURN' if looks_complete(result) else 'EXECUTOR_ABNORMAL')))
        attempt_sha=engine._record_attempt(u,result,status)
        try:
            need(digest(input_rows)==before_input and digest(engine.evidence)==engine._memory_neutral_sha256,
                 'NEUTRAL_INPUT_MUTATION')
            if decision['decision']=='CONTROLLED_STOP':raise RecoveryReject('CONFLICTING_OR_UNKNOWN_EXECUTOR_FAILURE')
            if external:
                u['state']='PENDING';engine.state['global_state']=NON_RESUMABLE
                engine.state['pause_reason']=external
                engine.state['stop_reason']='EXACT_U0012_RECOVERY_EXTERNAL_PAUSE__U0013_BLOCKED'
                engine._snapshot();outcome='WAITING_FOR_EXTERNAL_AVAILABILITY'
            else:
                need(result.get('context_id') not in prior_contexts,'REUSED_EXECUTOR_CONTEXT')
                checked=validate_semantic_unit(engine.partition,engine.evidence,engine.reason,
                                               'U0012',result,'PRIMARY')
                assigned=engine.partition['units'][11]
                need([r['authorized_population_position'] for r in checked['raw_rows']]==assigned['positions'],
                     'U0012_RAW_POSITION_SEQUENCE_CHANGED')
                need([r['canonical_source_identity'] for r in checked['raw_rows']]==assigned['canonical_source_identities'],
                     'U0012_RAW_IDENTITY_SEQUENCE_CHANGED')
                u['state']='VALIDATED';engine._snapshot();u=engine.state['units'][11]
                path=engine.workspace/'frozen_units'/'U0012'/'unit_result.json'
                outsha=unique_write(path,self._bounded_json(checked,ascii=False))
                need(strictly_json(path)==checked,'FROZEN_UNIT_READBACK_FAILED')
                u['frozen_output_sha256']=outsha
                u['executor_attempt_manifest_sha256']=attempt_sha
                u['frozen_context_id']=result['context_id'];u['state']='FROZEN'
                engine.state['global_state']=NON_RESUMABLE
                engine.state['stop_reason']='EXACT_U0012_RECOVERY_FROZEN__U0013_UNAUTHORIZED'
                engine._snapshot()
                engine.verify();outcome='FROZEN'
        except Exception as exc:
            from real_candidate.executor_v1 import remember_first_rejection
            remember_first_rejection(self,exc)
            u=engine.state['units'][11]
            u['state']='PENDING';u['frozen_output_sha256']=None
            u['executor_attempt_manifest_sha256']=None;u['frozen_context_id']=None
            engine.state['global_state']=NON_RESUMABLE
            engine.state['stop_reason']='EXACT_U0012_RECOVERY_CONTROLLED_STOP__'+type(exc).__name__+'__'+str(exc)
            engine._snapshot();outcome='CONTROLLED_STOP'
        return self._finish(outcome,old_frozen,initial_attempt,executor.calls,process_started=result.get('process_started'))

    def _finish(self,outcome,old_frozen,original_attempt,call_count,*,process_started=None):
        engine=self.engine
        engine.verify(expected_attempt_id=self.case['attempt_id'])
        need(call_count<=1,'EXACT_ONCE_UNIT_DISPATCH_VIOLATION')
        if len(self._historical_attempts)==10:
            prospective_attempt_context(self.case,synthetic=not (type(engine) is BoundCheckpointEngine and engine.real_source))
            need(engine.state['units'][11]['attempt_count'] in (10,11),'A11_ATTEMPT_COUNT_DRIFT')
        need(verify_attempt_lineage(engine.state['units'][11],self._historical_attempts,allow_appended=True) and
             engine.state['units'][11]['attempts'][0]['manifest_sha256']==original_attempt,
             'ORIGINAL_FAILED_U0012_ATTEMPT_REWRITTEN')
        need([sha_file(engine.workspace/'frozen_units'/f'U{i:04d}'/'unit_result.json') for i in range(1,12)]==old_frozen,
             'PREVIOUS_FROZEN_UNIT_MODIFIED')
        need(all(u['state']=='PENDING' for u in engine.state['units'][12:]),'U0013_OR_FUTURE_UNIT_ACCESSED')
        need(engine.state['global_state']==NON_RESUMABLE,'UNAUTHORIZED_GENERIC_RESUME')
        self._mode_guard()
        bound_mode=self._bound_mode_contract['execution_mode']
        event={'schema_version':'BATCH0004_EXACT_RECOVERY_TERMINAL_EVENT_V2',
               'execution_mode_contract':self._bound_mode_contract,
               'execution_mode_binding_sha256':self._bound_mode_sha256,
               'previous_recovery_event_sha256':sha_file(self.entry),
               'initial_checkpoint_sha256':self.case['checkpoint_manifest_sha256'],
               'terminal_checkpoint_sha256':engine.state['checkpoint_manifest_sha256'],
               'outcome':outcome,'authorized_unit':'U0012',
               'max_new_units':1,
               'codex_subprocess_started':(bool(process_started) if bound_mode=='REAL'
                                            and type(process_started) is bool else False),
               'synthetic_only':bound_mode=='SYNTHETIC',
               'recorded_provenance_mode':bound_mode,
               'first_unfinished_unit':engine.state['first_unfinished_unit'],
               'frozen_unit_count':sum(u['state']=='FROZEN' for u in engine.state['units'])}
        if self._v7_verified is not None:
            event['verified_operational_proof']=copy.deepcopy(self._v7_verified)
            event['finalization_readback']={
                'state':engine.state['units'][11]['state'],
                'frozen_output_sha256':engine.state['units'][11]['frozen_output_sha256'],
                'attempt_manifest_sha256':engine.state['units'][11]['executor_attempt_manifest_sha256']}
        if outcome=='CONTROLLED_STOP':
            from real_candidate.executor_v1 import remember_first_rejection,first_rejection_fields
            remember_first_rejection(self)
            event.update(first_rejection_fields(self))
        unique_write(self.outcome,self._bounded_json(event))
        need(strictly_json(self.outcome)==event,'RECOVERY_TERMINAL_EVENT_READBACK_FAILURE')
        return outcome

    def run(self,*args,**kwargs):raise RecoveryReject('ORDINARY_RUN_FORBIDDEN_IN_RECOVERY_TRANSACTION')
    def resume(self,*args,**kwargs):raise RecoveryReject('ORDINARY_AVAILABILITY_RESUME_FORBIDDEN')

if __name__=='__main__':
    print('PROSPECTIVE_BOUNDED_RECOVERY_V4_ONLY__NO_REAL_START')
    print('REAL_RECOVERY_BINDING_SHA256 =',case_binding_sha(REAL_CASE))
