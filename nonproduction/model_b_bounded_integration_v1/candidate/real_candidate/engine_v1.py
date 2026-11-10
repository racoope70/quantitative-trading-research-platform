"""Prospective Owner-compatible view of the unchanged checkpoint engine.

The historical parent remains pinned and unchanged. REAL construction and
identity verification are read-only and never confer Owner authority. REAL
writes require fresh verification of the existing consumed Owner recovery
transaction. Generic run/initialization/aggregation remain denied. No private
locator is included in configuration.
"""
from pathlib import Path
import copy
import json
import checkpoint_resume_activation_trusted_v1 as historical

HISTORICAL_SOURCE_SHA256='fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1'
ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'


def _legacy_readonly_requirements():
    """Retain independent source/policy requirements, without legacy grants."""
    import managing_activation_gate_trusted_v1 as gate
    old=gate.policy()
    gate.check_reference_sources()
    gate.check_active_sources(old)
    historical.require(all(old.get(k)==v for k,v in gate.FROZEN.items()),'FROZEN_INPUT_BINDING_CHANGED')
    historical.require(all(old.get(k)==v for k,v in gate.ACTIVE.items()),'FROZEN_ACTIVE_V6_CHANGED')
    historical.require(gate.sha(gate.REF/'runtime_activation_policy_v6.json')==gate.V6_POLICY,'V6_SEALED_POLICY_DRIFT')


def _bytes(obj, maximum, *, ascii=False):
    from real_candidate.executor_v1 import serialization_size
    serialization_size(obj,maximum,ensure_ascii=ascii,indent=None,separators=(',',':'),allow_nan=True)
    raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=ascii)+'\n').encode('utf-8')
    historical.require(len(raw)<=maximum,'CHECKPOINT_SERIALIZATION_LIMIT')
    return raw


def _utf8(value, maximum):
    historical.require(type(value) is str,'INVALID_EXECUTOR_EVIDENCE_TYPES')
    size=0
    for offset in range(0,len(value),8192):
        size+=len(value[offset:offset+8192].encode('utf-8'))
        historical.require(size<=maximum,'CHECKPOINT_STREAM_LIMIT')
    return value.encode('utf-8')


class BoundCheckpointEngine(historical.BoundCheckpointEngine):
    def __init__(self,root,role,source_root,identity_manifest_path,*,real_source=False,
                 authorization_path=None,attempt_identity=None,prospective_a11=False):
        historical.require(type(real_source) is bool,'ENGINE_EXECUTION_MODE_MALFORMED')
        historical.require(type(prospective_a11) is bool,'ENGINE_ATTEMPT_CONTEXT_INVALID')
        self._prospective_a11=prospective_a11
        self._owner_transaction=None
        if not real_source:
            super().__init__(root,role,source_root,identity_manifest_path,real_source=False,
                authorization_path=authorization_path,attempt_identity=attempt_identity)
            return
        historical.require(role=='PRIMARY' and attempt_identity==ATTEMPT and authorization_path is None,
                           'PROSPECTIVE_ENGINE_SCOPE_DRIFT')
        historical.require(historical.sha_file(Path(historical.__file__))==HISTORICAL_SOURCE_SHA256,
                           'HISTORICAL_CHECKPOINT_SOURCE_DRIFT')
        _legacy_readonly_requirements()
        import owner_authorization as owner
        owner.verify_real_engine_configuration(root,role,source_root,identity_manifest_path,attempt_identity,
                                              prospective_a11=prospective_a11)
        # Original readonly hydration body. Only the obsolete grant representation
        # is replaced above; S04, identity, rules and partition checks stay intact.
        from real_partition_manifest_v1 import verify_s04,verify_identity_manifest
        self.root=Path(root)
        self.role=role
        historical.require(role in ('PRIMARY','INDEPENDENT'),'INVALID_ROLE')
        self.workspace=self.root/role
        self.head=self.workspace/'checkpoint_head.json'
        self.source_root=Path(source_root)
        self.real_source=real_source
        self.identity_manifest_path=Path(identity_manifest_path)
        self.authorization_path=authorization_path
        self.attempt_identity=attempt_identity
        self.source_info=verify_s04(self.source_root,real=real_source)
        self.identity_manifest=historical.strictly_json(self.identity_manifest_path)
        verify_identity_manifest(self.identity_manifest,self.source_info)
        self.identity_manifest_hash=historical.sha_file(self.identity_manifest_path)
        self.evidence=self.source_info['rows']
        self.reason=historical.v3.load_reason_contract(self.source_root/'reason_precedence_v2.json')
        self.partition=historical.build_partition_manifest(self.evidence,historical.SIZE,self.source_info['manifest_sha256'])
        contents={'neutral_semantic_evidence.jsonl':(self.source_root/'neutral_semantic_evidence.jsonl').read_bytes(),
                  'reason_precedence_v2.json':(self.source_root/'reason_precedence_v2.json').read_bytes(),
                  'semantic_rule_v2.json':(self.source_root/'semantic_rule_v2.json').read_bytes(),
                  'partition_manifest.json':historical.obj_bytes(self.partition)}
        self.inputs=contents
        self.input_hashes={k:historical.hash_bytes(v) for k,v in contents.items()}
        self._memory_neutral_sha256=historical.digest(self.evidence)
        self.schema_id=historical.schema_sha()
        self.state=None

    def verify_readonly_configuration(self):
        historical.require(type(self.real_source) is bool,'ENGINE_EXECUTION_MODE_MALFORMED')
        if self.real_source:
            import owner_authorization as owner
            historical.require(historical.sha_file(Path(historical.__file__))==HISTORICAL_SOURCE_SHA256,
                               'HISTORICAL_CHECKPOINT_SOURCE_DRIFT')
            _legacy_readonly_requirements()
            owner.verify_real_engine_configuration(self.root,self.role,self.source_root,
                self.identity_manifest_path,self.attempt_identity,
                prospective_a11=self._prospective_a11)
        return True

    def _write_context(self):
        tx=self._owner_transaction
        if tx is not None and len(tx.case.get('historical_attempts',[]))==10:
            import recovery_two_attempt_v3 as recovery
            historical.require(type(tx) is recovery.ControlledStopRecovery and
                               tx.engine is self,'A11_ENGINE_TRANSACTION_DRIFT')
            recovery.prospective_attempt_context(tx.case,synthetic=not self.real_source)
        if self.real_source:
            from real_candidate.activation_v1 import production_activation
            production_activation(tx,phase='MUTATION')
            historical.require(tx is not None and tx.engine is self,'OWNER_ENGINE_TRANSACTION_REQUIRED')
            import owner_authorization as owner
            owner.verify_real_consumption_context(tx)  # locator is never authority
            historical.require(tx.case['authorized_recovery_unit']=='U0012' and tx.case['max_new_units']==1
                and tx.case['attempt_id']==ATTEMPT,'OWNER_ENGINE_SCOPE_DRIFT')
            historical.require(all(u['state']=='PENDING' and u['attempt_count']==0 for u in self.state['units'][12:]),
                               'U0013_OR_FUTURE_UNIT_ACCESSED')
        adapter=getattr(tx,'_bound_adapter',None) if tx is not None else None
        context=getattr(adapter,'execution_context',None)
        if self.real_source:historical.require(context is not None,'OWNER_ENGINE_CONTEXT_REQUIRED')
        return context

    def _write_budget(self):
        context=self._write_context()
        return (context,context.storage_contract()) if context is not None else (None,None)

    def initialize(self,*args,**kwargs):
        historical.require(not self.real_source,'REAL_ENGINE_INITIALIZATION_FORBIDDEN')
        return super().initialize(*args,**kwargs)

    def run(self,*args,**kwargs):
        historical.require(not self.real_source,'REAL_ENGINE_REQUIRES_EXACT_OWNER_RECOVERY')
        return super().run(*args,**kwargs)

    def _aggregate(self,*args,**kwargs):
        historical.require(not self.real_source,'U0013_AND_AGGREGATION_FORBIDDEN')
        return super()._aggregate(*args,**kwargs)

    def _snapshot(self):
        context,budget=self._write_budget()
        if budget is None:return super()._snapshot()
        from real_candidate.executor_v1 import _ensure_capacity,serialization_size
        maximum=budget['artifact_bytes']
        historical.require(self.state is not None,'NO_CHECKPOINT_STATE')
        serialization_size(self.state,maximum,ensure_ascii=False,indent=None,separators=(',',':'),allow_nan=True)
        snapshot=copy.deepcopy(self.state)
        snapshot['checkpoint_sequence']+=1
        snapshot['checkpoint_timestamp']=historical.now_utc()
        snapshot['previous_checkpoint_sha256']=self.state.get('checkpoint_manifest_sha256')
        snapshot['first_unfinished_unit']=next((u['unit_id'] for u in snapshot['units'] if u['state']!='FROZEN'),None)
        serialization_size(snapshot,maximum,ensure_ascii=False,indent=None,separators=(',',':'),allow_nan=True)
        snapshot['checkpoint_manifest_sha256']=historical.digest({k:v for k,v in snapshot.items() if k!='checkpoint_manifest_sha256'})
        historical.validate_schema(snapshot)
        raw=_bytes(snapshot,maximum)
        head={'sequence':snapshot['checkpoint_sequence'],
              'snapshot_file':f"checkpoint_{snapshot['checkpoint_sequence']:06d}.json",
              'snapshot_file_sha256':historical.hash_bytes(raw),
              'checkpoint_manifest_sha256':snapshot['checkpoint_manifest_sha256']}
        _bytes(head,maximum)
        _ensure_capacity(self.workspace,len(raw)+len(historical.obj_bytes(head))+budget['failure_reserve_bytes'])
        snapshot_sha=historical.unique_write(self.workspace/'checkpoints'/head['snapshot_file'],raw)
        historical.require(snapshot_sha==head['snapshot_file_sha256'],'SNAPSHOT_WRITE_HASH_DRIFT')
        historical.replace_head(self.head,head)
        self.state=snapshot

    def _record_attempt(self,u,result,classification):
        context,budget=self._write_budget()
        if budget is None:return super()._record_attempt(u,result,classification)
        from real_candidate.executor_v1 import _ensure_capacity
        limit=budget['capture_bytes']
        n=u['attempt_count']+1
        tx=self._owner_transaction
        count=len(tx.case['historical_attempts']) if tx is not None else 9
        historical.require(count in (9,10) and u['unit_id']=='U0012' and
                           n==count+1,'PROSPECTIVE_ATTEMPT_SCOPE_DRIFT')
        if count==10:
            import recovery_two_attempt_v3 as recovery
            recovery.prospective_attempt_context(tx.case,synthetic=not self.real_source)
            recovery.verify_attempt_lineage(u,tx.case['historical_attempts'])
        raw={name:_utf8(text,limit) for name,text in (
            ('raw_stdout.jsonl',result.get('raw_stdout','')),('raw_stderr.txt',result.get('raw_stderr','')),
            ('attempt_final_message.txt',result.get('agent_message','')))}
        historical.require(len(raw['raw_stdout.jsonl'])+len(raw['raw_stderr.txt'])<=limit,'CHECKPOINT_AGGREGATE_STREAM_LIMIT')
        arts={name:historical.hash_bytes(value) for name,value in raw.items()}
        manifest={'schema_version':'SYNTHETIC_EXECUTOR_ATTEMPT_V1','role':self.role,'unit_id':u['unit_id'],
            'attempt_number':n,'attempt_identity':self.state['attempt_identity'],
            'partition_manifest_sha256':self.state['partition_manifest_sha256'],
            'input_manifest_sha256':historical.digest({'unit_id':u['unit_id'],'position_start':u['position_start'],
                'position_end':u['position_end'],'identity_list_sha256':u['identity_list_sha256']}),
            'context_id':result.get('context_id'),'process_started':result.get('process_started'),
            'process_return_code':result.get('return_code'),'process_termination_state':result.get('termination_state'),
            'timeout_status':result.get('timeout_status'),'started_utc':result.get('started_utc'),
            'ended_utc':result.get('ended_utc'),'status':classification,'artifacts':arts,
            'availability_evidence':result.get('availability_evidence')}
        manifest_raw=_bytes(manifest,budget['artifact_bytes'])
        directory=self.workspace/'executor_attempts'/u['unit_id']/f'A{n:04d}'
        _ensure_capacity(self.workspace,sum(map(len,raw.values()))+len(manifest_raw)+budget['failure_reserve_bytes'])
        directory.mkdir(parents=True,exist_ok=False)
        written={name:historical.unique_write(directory/name,value) for name,value in raw.items()}
        historical.require(written==arts,'ATTEMPT_RAW_WRITE_HASH_DRIFT')
        manifest_sha=historical.unique_write(directory/'executor_attempt_manifest.json',manifest_raw)
        u['attempts'].append({'attempt_number':n,'context_id':result.get('context_id'),
            'status':classification,'manifest_sha256':manifest_sha})
        u['attempt_count']=n
        return manifest_sha
