#!/usr/bin/env python3
"""Case-bound, append-only, ONE-unit recovery transaction -- real-interface compatible V2 -- immutable mode bound authorization.

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
REF=Path(__file__).resolve().parent/'reference'/'v6_accepted'
if str(REF) not in sys.path:sys.path.insert(0,str(REF))

from checkpoint_resume_activation_trusted_v1 import (
    CheckpointEngine, SyntheticMockExecutor, NON_RESUMABLE, PAUSED, CheckpointStop,
    require, obj_bytes, sha_file, unique_write, strictly_json, digest,
    unit_evidence, validate_semantic_unit, canonical_json, decide_availability,
    looks_complete, now_utc, SIZE, BoundCheckpointEngine,
)
from corrected_prompt_reference.v3_partition_live_adapter_position_prompt_v1 import V3CodexUnitAdapter, v3 as frozen_v3

# Hash identities of the accepted exact interface implementations. No duck typing.
REAL_CHECKPOINT_INTERFACE_SHA256 = "fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1"
REAL_EXECUTOR_INTERFACE_SHA256 = "1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424"
ACTIVE_V6_CHECKPOINT_SHA256 = "083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27"
ACTIVE_V6_EXECUTOR_SHA256 = "b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b"

def verify_exact_approved_real_interfaces():
    base=Path(__file__).resolve().parent
    need(sha_file(base/"checkpoint_resume_activation_trusted_v1.py")==REAL_CHECKPOINT_INTERFACE_SHA256,
         "REAL_CHECKPOINT_ENGINE_IMPLEMENTATION_SHA_DRIFT")
    need(sha_file(base/"corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py")==REAL_EXECUTOR_INTERFACE_SHA256,
         "CORRECTED_REAL_EXECUTOR_IMPLEMENTATION_SHA_DRIFT")
    need(sha_file(base/"reference/v6_accepted/checkpoint_resume_readiness_v8.py")==ACTIVE_V6_CHECKPOINT_SHA256,
         "ACCEPTED_V6_CHECKPOINT_IMPLEMENTATION_SHA_DRIFT")
    need(sha_file(base/"reference/v6_accepted/v3_partition_live_adapter_readiness_v7.py")==ACTIVE_V6_EXECUTOR_SHA256,
         "ACCEPTED_V6_EXECUTOR_IMPLEMENTATION_SHA_DRIFT")
    return True


RECOVERY_STATE='RECOVERY_AUTHORIZED__FIRST_UNFINISHED_ONLY'
CASE_TASK='POST_C6_Q1_2027_D1_BODY_BATCH0004_PRIMARY_S05_BOUNDED_CONTROLLED_STOP_RECOVERY_IMPLEMENTATION_V1'
ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
REAL_CHECKPOINT_MANIFEST='bd109fe88e9c5e39ba3e0d3f1a4d75ea71c9b7ac469a4ab8721b97a44dc09fb7'
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
    'original_stop_reason':'PartitionStop__V3_SEMANTIC_UNIT_VALIDATION_FAILURE__ControlledStop__SEMANTIC_POSITION_MISMATCH',
    'real_execution_authorized':False,
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
        need(adapter.runner is frozen_v3.run_codex_executor,
             'REAL_ADAPTER_MUST_USE_FROZEN_CODEX_EXECUTOR')
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

class ExactOneUnitExecutor:
    """Defense in depth: this wrapper can never dispatch any unit except U0012 once."""
    def __init__(self,executor,*,pre_dispatch_check=None,bound_mode_contract=None,mode_check=None):
        need(type(executor) in (SyntheticMockExecutor,V3CodexUnitAdapter),
             'UNAPPROVED_EXECUTOR_INTERFACE')
        if type(executor) is V3CodexUnitAdapter:
            verify_exact_approved_real_interfaces()
            need(executor.role=='PRIMARY' and executor.attempt_identity in (None,ATTEMPT),
                 'REAL_EXECUTOR_ROLE_OR_ATTEMPT_MISMATCH')
            need(executor.independent_package_root is None, 'INDEPENDENT_EXECUTOR_FORBIDDEN')
        self._executor=executor;self.calls=0
        self._pre_dispatch_check=pre_dispatch_check
        self._mode_check=mode_check
        self._bound_mode_contract=copy.deepcopy(bound_mode_contract)
    def execute(self,role,unit_id,input_rows,attempt_no,prior_contexts):
        need(role=='PRIMARY' and unit_id=='U0012','U0013_OR_ALTERNATE_UNIT_DISPATCH_FORBIDDEN')
        need(self.calls==0,'DUPLICATE_UNIT_DISPATCH_FORBIDDEN')
        need(type(attempt_no) is int and attempt_no==2,'NOT_FRESH_SECOND_U0012_ATTEMPT')
        need(len(input_rows)==25,'UNIT_INPUT_WRONG_ROW_COUNT')
        need([r['authorized_population_position'] for r in input_rows]==list(range(1776,1801)),
             'EXACT_U0012_POSITIONS_CHANGED')
        # Last executable boundary: re-read the actual persisted checkpoint chain,
        # never accept cached engine.state as proof. No mock/Codex call on failure.
        if self._pre_dispatch_check is not None:
            self._pre_dispatch_check()
        if self._mode_check is not None:
            self._mode_check()  # final executable boundary; cached flags cannot promote authority
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
        # False means the CASE artifact itself is nonactivating. Actual real
        # authority comes only from the accepted trusted runtime activation gate.
        if type(self.engine) is BoundCheckpointEngine:
            if self.engine.real_source:
                from managing_activation_gate_trusted_v1 import require_real_activation
                require_real_activation(source_root=self.engine.source_root,
                    manifest_path=self.engine.identity_manifest_path,
                    role='PRIMARY',attempt_identity=self.case['attempt_id'],
                    authorization_path=self.engine.authorization_path,
                    checkpoint_root=self.engine.root)
                return self.case == REAL_CASE and self.case['real_execution_authorized'] is False
            return self.case['real_execution_authorized'] is False
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
                 u['attempt_count']==1 and len(u['attempts'])==1 and
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
        need(data.get('execution_mode_binding_sha256')==self._bound_mode_sha256
             and data.get('execution_mode_contract')==self._bound_mode_contract
             and self.binding_hash==case_and_mode_sha(self.case,self._bound_mode_contract),
             'RECOVERY_EVENT_EXECUTION_MODE_BINDING_MISMATCH')
        need(data['checkpoint_before_sha256']==self.case['checkpoint_manifest_sha256'],
             'RECOVERY_EVENT_ORIGINAL_CHECKPOINT_MISMATCH')
        return True

    def check_preconditions(self):
        exact_case(self.case,self.expected_case)
        need(self._real_input_authorization_ok(),'REAL_INPUT_AUTHORIZATION_BINDING_INVALID')
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
        need(s['first_unfinished_unit']=='U0012' and units[11]['attempt_count']==1 and
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
        """Explicitly bind engine, adapter and trusted authorization mode BEFORE sidecar write.

        REVIEW ONLY: invoke with temporary/copied fixtures; never live Mac inputs.
        """
        self._bind_mode_at_authorization(executor)
        self.check_preconditions()
        # Last possible fresh check before the FIRST recovery journal mutation.
        self._fresh_persisted_checkpoint(expected_checkpoint_sha256=self.case['checkpoint_manifest_sha256'],
                                         expected_u0012_state='PENDING')
        self._mode_guard()  # no sidecar write before a fresh trusted-mode check
        prior=self.engine.state
        self.journal.mkdir(parents=True,exist_ok=False)
        data={'schema_version':'BATCH0004_APPEND_ONLY_RECOVERY_EVENT_V1',
            'transition_from':NON_RESUMABLE,'transition_to':RECOVERY_STATE,
            'checkpoint_before_sha256':prior['checkpoint_manifest_sha256'],
            'original_stop_reason':prior['stop_reason'],
            'original_u0012_failed_attempt_sha256':prior['units'][11]['attempts'][0]['manifest_sha256'],
            'frozen_prefix_sha256':digest([u['frozen_output_sha256'] for u in prior['units'][:11]]),
            'recovery_binding_sha256':self.binding_hash,'role':'PRIMARY','unit_id':'U0012',
            'max_new_units':1,'original_snapshots_immutable':True,
            'execution_mode_contract':self._bound_mode_contract,
            'execution_mode_binding_sha256':self._bound_mode_sha256}
        unique_write(self.entry,json_bytes(data))
        need(strictly_json(self.entry)==data and sha_file(self.entry)==sha_bytes(json_bytes(data)),
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
        """Exactly one U0012; executor MUST be the one bound before authorization."""
        try:
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
        self._mode_guard()
        executor=ExactOneUnitExecutor(executor,pre_dispatch_check=self._fresh_pre_dispatch_guard,
                                      bound_mode_contract=self._bound_mode_contract,
                                      mode_check=self._mode_guard)
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
        decision=decide_availability(result,semantic_validator=validate_for_availability)
        result['availability_evidence']=decision
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
                outsha=unique_write(path,obj_bytes(checked))
                need(strictly_json(path)==checked,'FROZEN_UNIT_READBACK_FAILED')
                u['frozen_output_sha256']=outsha
                u['executor_attempt_manifest_sha256']=attempt_sha
                u['frozen_context_id']=result['context_id'];u['state']='FROZEN'
                engine.state['global_state']=NON_RESUMABLE
                engine.state['stop_reason']='EXACT_U0012_RECOVERY_FROZEN__U0013_UNAUTHORIZED'
                engine._snapshot()
                engine.verify();outcome='FROZEN'
        except Exception as exc:
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
        need(engine.state['units'][11]['attempts'][0]['manifest_sha256']==original_attempt,
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
        unique_write(self.outcome,json_bytes(event))
        need(strictly_json(self.outcome)==event,'RECOVERY_TERMINAL_EVENT_READBACK_FAILURE')
        return outcome

    def run(self,*args,**kwargs):raise RecoveryReject('ORDINARY_RUN_FORBIDDEN_IN_RECOVERY_TRANSACTION')
    def resume(self,*args,**kwargs):raise RecoveryReject('ORDINARY_AVAILABILITY_RESUME_FORBIDDEN')

if __name__=='__main__':
    print('NONPRODUCTION_RECOVERY_IMPLEMENTATION_V2_ONLY__NO_REAL_START')
    print('REAL_RECOVERY_BINDING_SHA256 =',case_binding_sha(REAL_CASE))
