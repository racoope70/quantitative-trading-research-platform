#!/usr/bin/env python3
"""Batch 0004 size-25 integrated checkpoint/resume -- REAL EXECUTION DISABLED.

No real Batch 0004 evidence, Codex backend, or repository writes. This component
reuses pinned V3 semantic checks and v1 position-only partition validation.
Actual scientific integration and partition freeze are NOT authorized.
"""
from __future__ import annotations
import copy
import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from availability_classifier_v6 import decide_availability
from managing_activation_gate_trusted_v1 import require_real_activation, require_synthetic_activation

from partition_contract_nonproduction_v1 import (
    PartitionStop, build_partition_manifest, verify_manifest, unit_evidence,
    validate_semantic_unit, validate_aggregation, digest, canonical_json, v3,
    FIRST, LAST, TOTAL,
)

SCHEMA_VERSION = 'BATCH0004_SIZE25_CHECKPOINT_MANIFEST_INTEGRATION_V2'
TASK_ID = 'POST_C6_Q1_2027_D1_BODY_BATCH0004_SIZE25_REAL_PARTITION_MANIFEST_AND_LIVE_INTEGRATION_BUILD_V1'
RULE = 'SORT_AUTHORIZED_POSITION_ASCENDING__CONTIGUOUS_FIXED_SIZE_25'
SYNTHETIC_SOURCE_SHA = '9' * 64
SIZE, COUNT = 25, 20
LIFECYCLE = ('PENDING', 'EXECUTING', 'VALIDATED', 'FROZEN')
NON_RESUMABLE = 'CONTROLLED_STOP__RETURN_TO_MANAGING'
PAUSED = 'PAUSED_EXTERNAL_AVAILABILITY'
DONE = 'COMPLETE_NONPRODUCTION__READY_FOR_MANAGING'
INPUT_FILES = ('neutral_semantic_evidence.jsonl', 'reason_precedence_v2.json', 'semantic_rule_v2.json', 'partition_manifest.json')
SCHEMA_PATH = Path(__file__).resolve().parent / 'checkpoint_manifest_schema_integrated_v2.json'
SCHEMA_DOCUMENT = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
SCHEMA_REQUIRED = set(SCHEMA_DOCUMENT['required'])
SCHEMA_UNIT_REQUIRED = set(SCHEMA_DOCUMENT['properties']['units']['items']['required'])

class CheckpointStop(PartitionStop):
    pass

def require(ok, text):
    if not ok:
        raise CheckpointStop(text)

def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha_file(path: Path) -> str:
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'MISSING_OR_SYMLINK_FILE__'+str(path))
    return hash_bytes(path.read_bytes())

def obj_bytes(obj) -> bytes:
    return (canonical_json(obj)+'\n').encode('utf-8')

def strictly_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def unique_write(path, data: bytes):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.is_symlink(), 'SYMLINK_ARTIFACT')
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    require(path.read_bytes() == data, 'SERIALIZATION_READBACK_FAILED')
    return hash_bytes(data)

def replace_head(path: Path, obj):
    # The head is the sole replaceable pointer; snapshots/artifacts are exclusive.
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, scratch = tempfile.mkstemp(prefix='.head_pending_', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(obj_bytes(obj))
            f.flush()
            os.fsync(f.fileno())
        os.replace(scratch, path)
    finally:
        if os.path.exists(scratch): os.unlink(scratch)
    require(strictly_json(path)==obj,'HEAD_WRITE_READBACK_FAILED')

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def schema_sha():
    return sha_file(SCHEMA_PATH)

def validate_schema(data):
    """Check schema exactly, in addition to publishing a versioned JSON schema file."""
    require(data.get('schema_version')==SCHEMA_VERSION,'CHECKPOINT_SCHEMA_VERSION_MISMATCH')
    keys=SCHEMA_REQUIRED
    require(set(data)==keys, 'CHECKPOINT_SCHEMA_FIELDS_MISMATCH')
    require(data['partition_size']==SIZE and data['partition_count']==COUNT,'CHECKPOINT_SIZE_CHANGED')
    require(data['partition_rule']==RULE, 'CHECKPOINT_RULE_CHANGED')
    require(data['batch_id']=='BATCH_0004' and data['task_id']==TASK_ID,'CHECKPOINT_TASK_CHANGED')
    require(data['role'] in ('PRIMARY','INDEPENDENT'), 'INVALID_CHECKPOINT_ROLE')
    require(len(data['units'])==COUNT and len({u['unit_id'] for u in data['units']})==COUNT,'CHECKPOINT_UNIT_COUNT')
    require(type(data['checkpoint_sequence']) is int and data['checkpoint_sequence']>=1,'CHECKPOINT_SEQUENCE_INVALID')
    for u in data['units']:
        require(set(u)==SCHEMA_UNIT_REQUIRED,'UNIT_SCHEMA_FIELDS_MISMATCH')
        require(u['state'] in LIFECYCLE,'INVALID_UNIT_STATE')
        require(type(u['attempt_count']) is int and u['attempt_count'] == len(u['attempts']), 'UNIT_ATTEMPT_COUNT_MISMATCH')
        for a in u['attempts']:
            require(set(a)=={'attempt_number','context_id','status','manifest_sha256'},'ATTEMPT_SCHEMA_FIELDS_MISMATCH')
        if u['state']=='FROZEN':
            require(isinstance(u['frozen_output_sha256'],str) and len(u['frozen_output_sha256'])==64,'FROZEN_UNIT_HASH_MISSING')
            require(isinstance(u['executor_attempt_manifest_sha256'],str) and len(u['executor_attempt_manifest_sha256'])==64,'FROZEN_EXECUTOR_MANIFEST_HASH_MISSING')
            require(isinstance(u['frozen_context_id'],str) and u['frozen_context_id'],'FROZEN_CONTEXT_MISSING')
        else:
            require(u['frozen_output_sha256'] is None and u['executor_attempt_manifest_sha256'] is None and u['frozen_context_id'] is None,'UNFROZEN_UNIT_HAS_FROZEN_FIELDS')
    require(data['checkpoint_manifest_sha256']==digest({k:v for k,v in data.items() if k!='checkpoint_manifest_sha256'}), 'CHECKPOINT_SELF_HASH_MISMATCH')
    return True

def synthetic_inputs(base: Path):
    """Read ONLY archived synthetic fixture; never search filesystem for real evidence."""
    here=Path(__file__).resolve().parent/'synthetic_fixture'
    evidence_path=here/'neutral_semantic_evidence.jsonl'
    precedence_path=here/'reason_precedence_v2.json'
    rule_path=here/'full_s04_fixture'/'semantic_rule_v2.json'
    require(all(x.is_file() for x in (evidence_path,precedence_path,rule_path)),'SYNTHETIC_FIXTURE_MISSING')
    evidence=[json.loads(line) for line in evidence_path.read_text().splitlines() if line.strip()]
    reason=v3.load_reason_contract(precedence_path)
    manifest=build_partition_manifest(evidence,SIZE,SYNTHETIC_SOURCE_SHA)
    require(manifest['partition_count']==COUNT,'INCORRECT_PARTITION_COUNT')
    contents={'neutral_semantic_evidence.jsonl':evidence_path.read_bytes(),
              'reason_precedence_v2.json':precedence_path.read_bytes(),
              'semantic_rule_v2.json':rule_path.read_bytes(),
              'partition_manifest.json':obj_bytes(manifest)}
    hashes={k:hash_bytes(v) for k,v in contents.items()}
    return evidence,reason,manifest,contents,hashes

class CheckpointEngine:
    def __init__(self, root: Path, role: str):
        self.root=Path(root)
        self.role=role
        require(role in ('PRIMARY','INDEPENDENT'),'INVALID_ROLE')
        self.workspace=self.root/role
        self.head=self.workspace/'checkpoint_head.json'
        self.evidence,self.reason,self.partition,self.inputs,self.input_hashes=synthetic_inputs(self.root)
        self._memory_neutral_sha256=digest(self.evidence)
        self.schema_id=schema_sha()
        self.state=None

    def initialize(self, attempt_id: str):
        require(isinstance(attempt_id,str) and re.fullmatch('[A-Za-z0-9_-]{8,90}',attempt_id),'INVALID_ATTEMPT_ID')
        require(not self.workspace.exists(),'CHECKPOINT_WORKSPACE_ALREADY_EXISTS')
        self.workspace.mkdir(parents=True,exist_ok=False)
        inputs=self.workspace/'clean_inputs'
        inputs.mkdir()
        for k,v in self.inputs.items(): unique_write(inputs/k,v)
        units=[]
        for unit in self.partition['units']:
            units.append({'unit_id':unit['unit_id'],'position_start':unit['position_start'],
                          'position_end':unit['position_end'],'identity_list_sha256':digest(unit['canonical_source_identities']),
                          'state':'PENDING','attempt_count':0,'attempts':[],
                          'frozen_output_sha256':None,'executor_attempt_manifest_sha256':None,
                          'frozen_context_id':None})
        self.state={'schema_version':SCHEMA_VERSION,'schema_sha256':self.schema_id,
            'batch_id':'BATCH_0004','task_id':TASK_ID,'role':self.role,
            'partition_size':SIZE,'partition_count':COUNT,'partition_rule':RULE,
            'partition_rule_identity_sha256':digest({'rule':RULE,'size':SIZE,'domain':[FIRST,LAST]}),
            'partition_manifest_sha256':self.input_hashes['partition_manifest.json'],
            'semantic_rule_identity_sha256':self.input_hashes['semantic_rule_v2.json'],
            'reason_precedence_identity_sha256':self.input_hashes['reason_precedence_v2.json'],
            'neutral_input_sha256':self.input_hashes['neutral_semantic_evidence.jsonl'],
            'attempt_identity':attempt_id,'units':units,
            'checkpoint_sequence':0,'checkpoint_timestamp':None,
            'first_unfinished_unit':'U0001','global_state':'RUNNING',
            'pause_reason':None,'stop_reason':None,'aggregate_sha256':None,
            'previous_checkpoint_sha256':None,'checkpoint_manifest_sha256':None}
        self._snapshot()
        return self

    def _snapshot(self):
        require(self.state is not None,'NO_CHECKPOINT_STATE')
        snapshot=copy.deepcopy(self.state)
        snapshot['checkpoint_sequence']+=1
        snapshot['checkpoint_timestamp']=now_utc()
        snapshot['previous_checkpoint_sha256']=self.state.get('checkpoint_manifest_sha256')
        snapshot['first_unfinished_unit']=next((u['unit_id'] for u in snapshot['units'] if u['state']!='FROZEN'),None)
        snapshot['checkpoint_manifest_sha256']=digest({k:v for k,v in snapshot.items() if k!='checkpoint_manifest_sha256'})
        validate_schema(snapshot)
        filename=f"checkpoint_{snapshot['checkpoint_sequence']:06d}.json"
        snapshot_sha=unique_write(self.workspace/'checkpoints'/filename,obj_bytes(snapshot))
        replace_head(self.head,{'sequence':snapshot['checkpoint_sequence'],'snapshot_file':filename,
                                'snapshot_file_sha256':snapshot_sha,
                                'checkpoint_manifest_sha256':snapshot['checkpoint_manifest_sha256']})
        self.state=snapshot

    def _verify_clean_inputs(self, *, check_memory=False):
        root=self.workspace/'clean_inputs'
        require(root.is_dir() and not root.is_symlink(),'CLEAN_INPUT_DIR_MISSING')
        files={p.name for p in root.iterdir() if p.is_file() and not p.is_symlink()}
        require(files==set(INPUT_FILES) and len(list(root.iterdir()))==len(INPUT_FILES),'INDEPENDENT_INPUT_FIREWALL_FILE_SET')
        for k in INPUT_FILES:
            require((root/k).read_bytes()==self.inputs[k] and sha_file(root/k)==self.input_hashes[k], 'CLEAN_INPUT_HASH_OR_CONTENT_MISMATCH__'+k)
        if check_memory:
            reread_evidence=[json.loads(line) for line in (root/'neutral_semantic_evidence.jsonl').read_text().splitlines() if line.strip()]
            require(reread_evidence==self.evidence, 'IN_MEMORY_NEUTRAL_INPUT_MUTATED')
        require(verify_manifest(strictly_json(root/'partition_manifest.json'), self.evidence),'INVALID_PARTITION_INPUT')
        for row in self.evidence:
            require(set(row)==set(__import__('firewall_v2').EVIDENCE_KEYS),'INDEPENDENT_NEUTRAL_EVIDENCE_SCHEMA')
        return True

    def _read_snapshot_chain(self):
        require(self.head.is_file() and not self.head.is_symlink(),'CHECKPOINT_HEAD_MISSING')
        head=strictly_json(self.head)
        require(set(head)=={'sequence','snapshot_file','snapshot_file_sha256','checkpoint_manifest_sha256'},'CHECKPOINT_HEAD_FIELDS')
        require(type(head['sequence']) is int and head['sequence']>0, 'CHECKPOINT_HEAD_SEQUENCE')
        require(head['snapshot_file']==f"checkpoint_{head['sequence']:06d}.json",'INVALID_CHECKPOINT_HEAD_FILENAME')
        folder=self.workspace/'checkpoints'
        require(sha_file(folder/head['snapshot_file'])==head['snapshot_file_sha256'], 'CHECKPOINT_HEAD_FILE_HASH_MISMATCH')
        files=sorted(folder.glob('checkpoint_*.json'))
        require(len(files)==head['sequence'],'CHECKPOINT_GAP_OR_EXTRANEOUS_SNAPSHOT')
        previous=None; last=None
        for seq, p in enumerate(files,1):
            require(p.name==f'checkpoint_{seq:06d}.json' and not p.is_symlink(),'CHECKPOINT_ORDER_INVALID')
            state=strictly_json(p)
            require(p.read_bytes()==obj_bytes(state),'CHECKPOINT_HISTORY_BYTES_TAMPERED')
            validate_schema(state)
            require(state['checkpoint_sequence']==seq,'CHECKPOINT_SEQUENCE_CHANGED')
            require(state['previous_checkpoint_sha256']==previous, 'CHECKPOINT_CHAIN_BROKEN')
            require(state['schema_sha256']==self.schema_id,'CHECKPOINT_SCHEMA_SHA_MISMATCH')
            require(state['role']==self.role,'CHECKPOINT_ROLE_SWAPPED')
            previous=state['checkpoint_manifest_sha256'];last=state
        require(head['snapshot_file']==files[-1].name,'CHECKPOINT_HEAD_LATEST_MISMATCH')
        require(head['snapshot_file_sha256']==sha_file(files[-1]),'CHECKPOINT_HEAD_FILE_HASH_MISMATCH')
        require(head['checkpoint_manifest_sha256']==last['checkpoint_manifest_sha256'],'CHECKPOINT_HEAD_SELF_HASH_MISMATCH')
        return last

    def _verify_attempt(self, u, a):
        # All paths constructed from exact unit IDs + positive integer attempts.
        unit=u['unit_id'];n=a['attempt_number']
        require(n>0 and isinstance(n,int),'INVALID_ATTEMPT_ORDINAL')
        attempt=self.workspace/'executor_attempts'/unit/f'A{n:04d}'
        require(attempt.is_dir() and not attempt.is_symlink(),'MISSING_ATTEMPT_DIRECTORY')
        manifest_path=attempt/'executor_attempt_manifest.json'
        require(sha_file(manifest_path)==a['manifest_sha256'],'ATTEMPT_MANIFEST_TAMPERED')
        m=strictly_json(manifest_path)
        require(m['role']==self.role and m['unit_id']==unit and m['attempt_number']==n, 'ATTEMPT_BINDING_MISMATCH')
        require(m['attempt_identity']==self.state['attempt_identity'],'ATTEMPT_IDENTITY_MISMATCH')
        require(m['partition_manifest_sha256']==self.state['partition_manifest_sha256'], 'ATTEMPT_PARTITION_BINDING_MISMATCH')
        require(m['input_manifest_sha256']==digest({'unit_id':unit,'position_start':u['position_start'], 'position_end':u['position_end'],'identity_list_sha256':u['identity_list_sha256']}),'ATTEMPT_UNIT_INPUT_BINDING_MISMATCH')
        for k in ('raw_stdout.jsonl','raw_stderr.txt','attempt_final_message.txt'):
            require(sha_file(attempt/k)==m['artifacts'][k],'EXECUTOR_RAW_EVIDENCE_TAMPERED__'+k)
        require(a['context_id']==m['context_id'] and a['status']==m['status'], 'ATTEMPT_STATE_MISMATCH')
        return m

    def verify(self, expected_attempt_id=None, expected_partition_rule_sha=None, expected_semantic_rule_sha=None):
        require(self.workspace.is_dir() and not self.workspace.is_symlink(),'CHECKPOINT_WORKSPACE_SYMLINK_OR_MISSING')
        require(schema_sha()==self.schema_id, 'CHECKPOINT_SCHEMA_SOURCE_TAMPERED')
        self.state=self._read_snapshot_chain()
        require(self.state['schema_version']==SCHEMA_VERSION,'CHECKPOINT_SCHEMA_CHANGED')
        if expected_attempt_id is not None:
            require(self.state['attempt_identity']==expected_attempt_id,'WRONG_ATTEMPT_IDENTITY')
        if expected_partition_rule_sha is not None:
            require(self.state['partition_rule_identity_sha256']==expected_partition_rule_sha,'WRONG_PARTITION_RULE_IDENTITY')
        if expected_semantic_rule_sha is not None:
            require(self.state['semantic_rule_identity_sha256']==expected_semantic_rule_sha,'WRONG_SEMANTIC_RULE_IDENTITY')
        for name, sha in (('partition_rule_identity_sha256',digest({'rule':RULE,'size':SIZE,'domain':[FIRST,LAST]})),
            ('partition_manifest_sha256',self.input_hashes['partition_manifest.json']),
            ('semantic_rule_identity_sha256',self.input_hashes['semantic_rule_v2.json']),
            ('reason_precedence_identity_sha256',self.input_hashes['reason_precedence_v2.json']),
            ('neutral_input_sha256',self.input_hashes['neutral_semantic_evidence.jsonl'])):
            require(self.state[name]==sha,'FROZEN_SOURCE_IDENTITY_MISMATCH__'+name)
        self._verify_clean_inputs()
        units=self.state['units'];contexts=[];unfinished=False
        for i,u in enumerate(units):
            expected=self.partition['units'][i]
            require(u['unit_id']==expected['unit_id'] and u['position_start']==expected['position_start'] and
                u['position_end']==expected['position_end'] and u['identity_list_sha256']==digest(expected['canonical_source_identities']),
                'CHECKPOINT_UNIT_ASSIGNMENT_CHANGED')
            if u['state']!='FROZEN': unfinished=True
            if u['state']=='FROZEN':
                require(not unfinished,'GAPPED_FROZEN_PREFIX')
                result_file=self.workspace/'frozen_units'/u['unit_id']/'unit_result.json'
                require(sha_file(result_file)==u['frozen_output_sha256'],'FROZEN_UNIT_ARTIFACT_TAMPERED')
                data=strictly_json(result_file)
                require(data.get('role')==self.role and data.get('unit_id')==u['unit_id'] and
                        data.get('context_id')==u['frozen_context_id'],'FROZEN_RESULT_BINDING_MISMATCH')
                require(data.get('source_s04_manifest_sha256')==self.partition['source_s04_manifest_sha256'], 'FROZEN_SOURCE_BINDING_MISMATCH')
                require(digest(data['validated_rows'])==data['unit_output_sha256'], 'FROZEN_UNIT_OUTPUT_HASH_TAMPERED')
                require(digest(data['raw_rows'])==data['raw_rows_sha256'], 'FROZEN_RAW_ROW_HASH_TAMPERED')
                verified=v3.validate_semantic_rows(data['raw_rows'], unit_evidence(self.partition,self.evidence,u['unit_id']), self.reason)
                require(verified==data['validated_rows'],'FROZEN_SEMANTIC_READBACK_FAILED')
                require([r['authorized_population_position'] for r in data['raw_rows']]==expected['positions'],'FROZEN_POSITION_SEQUENCE_INVALID')
                contexts.append(u['frozen_context_id'])
                require(u['attempts'][-1]['manifest_sha256']==u['executor_attempt_manifest_sha256'] and u['attempts'][-1]['status']=='EXECUTOR_NORMAL_RETURN','FROZEN_EXECUTOR_BINDING_MISMATCH')
                executor_manifest=self._verify_attempt(u,u['attempts'][-1])
                require(executor_manifest['process_started'] is True and
                        executor_manifest['process_return_code']==0 and
                        executor_manifest['process_termination_state']=='NORMAL_SUCCESS' and
                        executor_manifest['timeout_status'] is False and
                        executor_manifest['context_id']==u['frozen_context_id'],
                        'FROZEN_EXECUTOR_SUCCESS_NOT_ESTABLISHED')
                saved_message=strictly_json(self.workspace/'executor_attempts'/u['unit_id']/
                        f"A{u['attempt_count']:04d}"/'attempt_final_message.txt')
                require(isinstance(saved_message,dict) and saved_message.get('rows')==data['raw_rows'] and
                        not v3.executor_error_indicated(saved_message),
                        'FROZEN_AGENT_MESSAGE_MISMATCH')
            require(len(u['attempts'])==u['attempt_count'],'ATTEMPT_COUNT_CHANGED')
            for no,a in enumerate(u['attempts'],1):
                require(a['attempt_number']==no,'ATTEMPT_SEQUENCE_CHANGED')
                manifest=self._verify_attempt(u,a)
                ctx=manifest.get('context_id')
                if ctx: contexts.append(ctx)
        # A frozen unit's last attempt context repeats intentionally in the above check.
        attempted=[a['context_id'] for u in units for a in u['attempts'] if a['context_id']]
        require(len(attempted)==len(set(attempted)),'DUPLICATE_OR_REUSED_CONTEXT')
        frozen_count=sum(u['state']=='FROZEN' for u in units)
        require(self.state['first_unfinished_unit']==(units[frozen_count]['unit_id'] if frozen_count<COUNT else None),'FIRST_UNFINISHED_CHANGED')
        if self.state['global_state']==DONE:
            require(frozen_count==COUNT,'PREMATURE_COMPLETE_STATE')
            require(sha_file(self.workspace/'semantic_aggregate.json')==self.state['aggregate_sha256'],'FINAL_AGGREGATE_TAMPERED')
        if self.state['global_state']==PAUSED:require(frozen_count<COUNT and self.state['pause_reason'] is not None, 'INVALID_PAUSE_STATE')
        require(self.state['global_state'] in ('RUNNING',PAUSED,NON_RESUMABLE,DONE), 'INVALID_GLOBAL_STATE')
        return self

    def _record_attempt(self, u, result, classification):
        # Persist complete attempt evidence before scientific acceptance decisions.
        n=u['attempt_count']+1
        directory=self.workspace/'executor_attempts'/u['unit_id']/f'A{n:04d}'
        directory.mkdir(parents=True,exist_ok=False)
        raw_stdout=result.get('raw_stdout','')
        raw_stderr=result.get('raw_stderr','')
        msg=result.get('agent_message','')
        require(all(isinstance(x,str) for x in (raw_stdout,raw_stderr,msg)),'INVALID_EXECUTOR_EVIDENCE_TYPES')
        arts={name:unique_write(directory/name,text.encode('utf-8')) for name,text in (
              ('raw_stdout.jsonl',raw_stdout),('raw_stderr.txt',raw_stderr),('attempt_final_message.txt',msg))}
        manifest={'schema_version':'SYNTHETIC_EXECUTOR_ATTEMPT_V1','role':self.role,'unit_id':u['unit_id'],
                  'attempt_number':n,'attempt_identity':self.state['attempt_identity'],
                  'partition_manifest_sha256':self.state['partition_manifest_sha256'],
                  'input_manifest_sha256':digest({'unit_id':u['unit_id'],'position_start':u['position_start'],
                      'position_end':u['position_end'],'identity_list_sha256':u['identity_list_sha256']}),
                  'context_id':result.get('context_id'), 'process_started':result.get('process_started'),
                  'process_return_code':result.get('return_code'),
                  'process_termination_state':result.get('termination_state'),
                  'timeout_status':result.get('timeout_status'),
                  'started_utc':result.get('started_utc'), 'ended_utc':result.get('ended_utc'),
                  'status':classification,'artifacts':arts,
                  'availability_evidence':result.get('availability_evidence')}
        manifest_sha=unique_write(directory/'executor_attempt_manifest.json',obj_bytes(manifest))
        entry={'attempt_number':n,'context_id':result.get('context_id'),
               'status':classification,'manifest_sha256':manifest_sha}
        u['attempts'].append(entry)
        u['attempt_count']=n
        return manifest_sha

    def _aggregate(self, *, disallowed_contexts=()):
        require(all(u['state']=='FROZEN' for u in self.state['units']),'AGGREGATE_UNFROZEN_UNIT')
        self.verify()
        items=[]
        for u in self.state['units']:
            items.append(strictly_json(self.workspace/'frozen_units'/u['unit_id']/'unit_result.json'))
        output=validate_aggregation(self.partition,self.evidence,self.reason,items,self.role,
                                   disallowed_contexts=disallowed_contexts)
        require(output['row_count']==500 and len(set(r['canonical_source_identity'] for r in output['rows']))==500,'AGGREGATE_DOMAIN_WRONG')
        require([r['authorized_population_position'] for r in output['rows']]==list(range(1501,2001)),'AGGREGATE_POSITIONS_WRONG')
        aggpath=self.workspace/'semantic_aggregate.json'
        aggregate_sha=unique_write(aggpath,obj_bytes(output))
        require(sha_file(aggpath)==aggregate_sha and strictly_json(aggpath)==output,'AGGREGATE_READBACK_FAILED')
        return {'row_count':500,'sha256':aggregate_sha,'contexts':output['contexts']}

    def run(self, executor, *, resume=False, availability_confirmed=False, disallowed_contexts=()):
        self.verify()
        if resume:
            require(availability_confirmed is True,'AVAILABILITY_NOT_CONFIRMED_FOR_RESUME')
            require(self.state['global_state']==PAUSED,'RESUME_REQUIRES_EXTERNAL_PAUSE')
            self.state['global_state']='RUNNING';self.state['pause_reason']=None
            self._snapshot()
        else:
            require(self.state['global_state']=='RUNNING' and
                    all(u['state'] in ('PENDING','FROZEN') for u in self.state['units']),
                    'NEW_RUN_REQUIRES_CLEAN_INITIAL_STATE')
        attempted_contexts={a['context_id'] for u in self.state['units'] for a in u['attempts'] if a['context_id']}
        require(not set(disallowed_contexts)&attempted_contexts,'ROLE_CONTEXT_ISOLATION')
        for unit_id in [item['unit_id'] for item in self.state['units']]:
            u=next(item for item in self.state['units'] if item['unit_id']==unit_id)
            if u['state']=='FROZEN': continue
            require(u['state']=='PENDING','UNIT_LEFT_IN_INCOMPLETE_STATE')
            u['state']='EXECUTING';self._snapshot()
            u=next(item for item in self.state['units'] if item['unit_id']==unit_id)
            input_rows=unit_evidence(self.partition,self.evidence,unit_id)
            before_input_hash=digest(input_rows)
            try:
                result=executor.execute(self.role,unit_id,input_rows,u['attempt_count']+1,
                                        tuple(attempted_contexts))
            except Exception as exc:
                # Executor adapter crash: cannot classify as externally resumable.
                self.state['global_state']=NON_RESUMABLE
                self.state['stop_reason']='UNHANDLED_EXECUTOR_ADAPTER_ERROR__'+type(exc).__name__
                u['state']='PENDING';self._snapshot()
                return NON_RESUMABLE
            def _output_verification(payload):
                checked=validate_semantic_unit(self.partition,self.evidence,self.reason,unit_id,
                    {**result, 'agent_message':canonical_json(payload)},self.role)
                assigned=self.partition['units'][int(unit_id[1:])-1]
                require([r['authorized_population_position'] for r in checked['raw_rows']]==assigned['positions'],
                        'CONFLICT_INVALID_POSITIONS')
                require([r['canonical_source_identity'] for r in checked['raw_rows']]==assigned['canonical_source_identities'],
                        'CONFLICT_INVALID_IDENTITIES')
            decision=decide_availability(result,semantic_validator=_output_verification)
            result['availability_evidence']=decision
            external=(decision['classification'] if decision['decision']=='PAUSED_EXTERNAL_AVAILABILITY' else None)
            status=('EXTERNAL_CONFLICT__CONTROLLED_STOP' if decision['decision']=='CONTROLLED_STOP' else
                    ('EXTERNALLY_INTERRUPTED' if external else
                     ('EXECUTOR_NORMAL_RETURN' if looks_complete(result) else 'EXECUTOR_ABNORMAL')))
            manifest_sha=self._record_attempt(u,result,status)
            try:
                require(digest(input_rows)==before_input_hash,'EXECUTOR_MUTATED_UNIT_INPUT')
                require(digest(self.evidence)==self._memory_neutral_sha256,'IN_MEMORY_NEUTRAL_INPUT_MUTATED')
            except Exception as exc:
                self.state['global_state']=NON_RESUMABLE
                self.state['stop_reason']='INPUT_BINDING_FAILURE__'+type(exc).__name__+'__'+str(exc)
                u['state']='PENDING';self._snapshot()
                return NON_RESUMABLE
            if decision['decision']=='CONTROLLED_STOP':
                u['state']='PENDING';self.state['global_state']=NON_RESUMABLE
                self.state['stop_reason']='EXTERNAL_SIGNAL_CONFLICT_OR_UNKNOWN_FAILURE'
                self._snapshot()
                return NON_RESUMABLE
            if external:
                u['state']='PENDING';self.state['global_state']=PAUSED
                self.state['pause_reason']=external;self._snapshot()
                return PAUSED
            try:
                require(result.get('context_id') not in attempted_contexts,'REUSED_EXECUTOR_CONTEXT')
                require(result.get('context_id') not in set(disallowed_contexts),'ROLE_CONTEXT_ISOLATION')
                checked=validate_semantic_unit(self.partition,self.evidence,self.reason,unit_id,result,self.role)
                # The frozen V3 validator sorts; require exact index order independently.
                expected_positions=self.partition['units'][int(unit_id[1:])-1]['positions']
                require([r.get('authorized_population_position') for r in checked['raw_rows']]==expected_positions,'UNIT_RAW_POSITION_ORDER_CHANGED')
                require([r.get('canonical_source_identity') for r in checked['raw_rows']]==self.partition['units'][int(unit_id[1:])-1]['canonical_source_identities'],'UNIT_RAW_IDENTITY_ORDER_CHANGED')
                u['state']='VALIDATED';self._snapshot()
                u=next(item for item in self.state['units'] if item['unit_id']==unit_id)
                outputpath=self.workspace/'frozen_units'/unit_id/'unit_result.json'
                output_sha=unique_write(outputpath,obj_bytes(checked))
                require(strictly_json(outputpath)==checked,'FROZEN_RESULT_READBACK_FAILURE')
                u['frozen_output_sha256']=output_sha
                u['executor_attempt_manifest_sha256']=manifest_sha
                u['frozen_context_id']=result['context_id'];u['state']='FROZEN'
                attempted_contexts.add(result['context_id'])
                self._snapshot()
                self.verify()
                u=next(item for item in self.state['units'] if item['unit_id']==unit_id)
            except Exception as exc:
                self.state['global_state']=NON_RESUMABLE
                self.state['stop_reason']=type(exc).__name__+'__'+str(exc)
                # No unsuccessful/partial output can remain frozen, even after validation.
                u['state']='PENDING';u['frozen_output_sha256']=None
                u['executor_attempt_manifest_sha256']=None;u['frozen_context_id']=None
                self._snapshot()
                return NON_RESUMABLE
        try:
            aggregate_result=self._aggregate(disallowed_contexts=disallowed_contexts)
            self.verify()
            self.state['aggregate_sha256']=aggregate_result['sha256']
            self.state['global_state']=DONE;self._snapshot()
            return DONE
        except Exception as exc:
            self.state['global_state']=NON_RESUMABLE
            self.state['stop_reason']='AGGREGATION_FAILURE__'+type(exc).__name__+'__'+str(exc)
            self._snapshot()
            return NON_RESUMABLE


def looks_complete(result):
    return result.get('process_started') is True and result.get('return_code')==0 and result.get('termination_state')=='NORMAL_SUCCESS' and result.get('timeout_status') is False

def classify_explicit_external(result):
    """Compatibility interface: never pause on unknown/conflicting evidence."""
    d=decide_availability(result)
    if d['decision']=='PAUSED_EXTERNAL_AVAILABILITY':return d['classification']
    return None


class SyntheticMockExecutor:
    """Mock only: each attempt is a distinct synthetic context, never calls Codex."""
    def __init__(self, final_rows, *, pauses=None, failures=None, run_nonce='mock-checkpoint-v1'):
        self.by_id={r['canonical_source_identity']:r for r in final_rows}
        self.pauses=pauses or {};self.failures=failures or {}
        self.run_nonce=run_nonce;self.calls=[]
    def execute(self, role, unit_id, input_rows, attempt_no, prior_contexts):
        event_key=(role,unit_id,attempt_no)
        ctx='synthetic-context-'+hashlib.sha256((self.run_nonce+str(event_key)).encode()).hexdigest()[:26]
        if ctx in prior_contexts:raise CheckpointStop('MOCK_CONTEXT_REUSED')
        self.calls.append(event_key)
        start=now_utc()
        rows=[copy.deepcopy(self.by_id[r['canonical_source_identity']]) for r in input_rows]
        out={'rows':rows};code=0;termination='NORMAL_SUCCESS'
        events=[{'type':'thread.started','thread_id':ctx},{'type':'turn.started'}]
        if event_key in self.pauses:
            code=1;termination='ERROR';out=None
            kind=self.pauses[event_key]
            text={'usage':"You've hit your usage limit. Try again later.",
                  'service':'Service unavailable 503 upstream unavailable',
                  'quota':'Your Codex quota exhausted; credits exhausted.'}[kind]
            events.extend([{'type':'error','message':text},{'type':'turn.failed','error':{'message':text}}])
        elif event_key in self.failures:
            kind=self.failures[event_key]
            if kind=='short':out={'rows':rows[:24]}
            elif kind=='wrong_identity':out['rows'][0]['canonical_source_identity']='f'*64
            elif kind=='wrong_position':out['rows'][0]['authorized_population_position']=1501
            elif kind=='wrong_reason':out['rows'][0]['reason_code']='INVALID'
            elif kind=='empty_rationale':out['rows'][0]['concise_review_rationale']=''
            elif kind=='noncompletion':out={'rows':[], 'error':'Review incomplete'}
            elif kind=='unknown':code=1;termination='ERROR';out=None;events.append({'type':'error','message':'UNKNOWN EXECUTOR ERROR'})
            elif kind=='reused_context':ctx='synthetic-context-'+hashlib.sha256((self.run_nonce+str((role,'U0001',1))).encode()).hexdigest()[:26]
            else:raise ValueError('UNKNOWN_MOCK_FAILURE')
        if code==0:events.append({'type':'turn.completed'})
        return {'process_started':True,'return_code':code,'termination_state':termination,
                'timeout_status':False,'context_id':ctx,
                'raw_stdout':'\n'.join(canonical_json(e) for e in events)+'\n',
                'raw_stderr':'','agent_message':canonical_json(out) if out is not None else '',
                'started_utc':start,'ended_utc':now_utc()}


class BoundCheckpointEngine(CheckpointEngine):
    """Accepted checkpoint state machine with provenance-bound neutral inputs.

    No real semantic run is allowed in this release. Future activation needs
    separate Managing authorization and a versioned runtime authorization.
    """
    def __init__(self, root, role, source_root, identity_manifest_path, *, real_source=False, authorization_path=None, attempt_identity=None):
        from real_partition_manifest_v1 import verify_s04, verify_identity_manifest
        self.root=Path(root)
        self.role=role
        require(role in ('PRIMARY','INDEPENDENT'),'INVALID_ROLE')
        self.workspace=self.root/role
        self.head=self.workspace/'checkpoint_head.json'
        self.source_root=Path(source_root)
        self.real_source=real_source
        self.identity_manifest_path=Path(identity_manifest_path)
        self.authorization_path=authorization_path
        self.attempt_identity=attempt_identity
        if real_source:
            require_real_activation(source_root=self.source_root,manifest_path=self.identity_manifest_path,
                                    role=role,attempt_identity=attempt_identity,authorization_path=authorization_path)
        self.source_info=verify_s04(self.source_root,real=real_source)
        self.identity_manifest=strictly_json(self.identity_manifest_path)
        verify_identity_manifest(self.identity_manifest,self.source_info)
        self.identity_manifest_hash=sha_file(self.identity_manifest_path)
        self.evidence=self.source_info['rows']
        self.reason=v3.load_reason_contract(self.source_root/'reason_precedence_v2.json')
        self.partition=build_partition_manifest(self.evidence,SIZE,self.source_info['manifest_sha256'])
        contents={'neutral_semantic_evidence.jsonl':(self.source_root/'neutral_semantic_evidence.jsonl').read_bytes(),
                  'reason_precedence_v2.json':(self.source_root/'reason_precedence_v2.json').read_bytes(),
                  'semantic_rule_v2.json':(self.source_root/'semantic_rule_v2.json').read_bytes(),
                  'partition_manifest.json':obj_bytes(self.partition)}
        self.inputs=contents
        self.input_hashes={k:hash_bytes(v) for k,v in contents.items()}
        self._memory_neutral_sha256=digest(self.evidence)
        self.schema_id=schema_sha()
        self.state=None

    def verify(self,*args,**kwargs):
        from real_partition_manifest_v1 import verify_s04,verify_identity_manifest
        # Full 1,000-file S04 audit ran in __init__ (also on every new-process
        # resume). Within one checkpoint sequence, pin neutral/rule/precedence
        # and source-manifest hashes on every verify; the live unit adapter
        # separately rehashes each exact unit body/header prior to executor.
        required={'s04_primary_input_manifest.json':'manifest_sha256',
                  'neutral_semantic_evidence.jsonl':'neutral_sha256',
                  'semantic_rule_v2.json':'semantic_rule_sha256',
                  'reason_precedence_v2.json':'precedence_sha256'}
        for name,key in required.items():
            require(sha_file(self.source_root/name)==self.source_info[key],
                    'BOUND_S04_SOURCE_IDENTITY_CHANGED__'+name)
        require(sha_file(self.identity_manifest_path)==self.identity_manifest_hash,
                'FROZEN_REAL_PARTITION_MANIFEST_TAMPERED')
        verify_identity_manifest(strictly_json(self.identity_manifest_path),self.source_info)
        return super().verify(*args,**kwargs)

    def run(self,*args,**kwargs):
        if self.real_source:
            require_real_activation(source_root=self.source_root,manifest_path=self.identity_manifest_path,
                                    role=self.role,attempt_identity=self.attempt_identity,
                                    authorization_path=self.authorization_path,checkpoint_root=self.root)
            require(self.state is not None and self.state['attempt_identity']==self.attempt_identity,
                    'REAL_CHECKPOINT_ATTEMPT_IDENTITY_CHANGED')
        return super().run(*args,**kwargs)
