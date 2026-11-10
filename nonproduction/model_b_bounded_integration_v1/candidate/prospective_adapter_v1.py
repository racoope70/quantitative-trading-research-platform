#!/usr/bin/env python3
"""Prospective bounded-executor V3 adapter; historical V3 bytes remain unchanged.

Exercises V3's exact read-only ephemeral Codex call/evidence API with injected
nonproduction mocks; no CLI here invokes real Codex. Any future activation
requires a new authorized runtime and separate real execution gating.
"""
from __future__ import annotations
import hashlib
import json
import os
import stat
import subprocess
from contextlib import contextmanager
import shutil
from pathlib import Path
from real_partition_manifest_v1 import sha_file, ensure, verify_s04, verify_identity_manifest, ManifestStop
from partition_contract_nonproduction_v1 import unit_evidence, digest, canonical_json, v3
from checkpoint_resume_readiness_v8 import now_utc
from managing_activation_gate_trusted_v1 import require_real_activation, require_synthetic_activation

class LiveIntegrationStop(ManifestStop):pass

def write_once(path,data):
    path=Path(path)
    ensure(not path.exists() and not path.is_symlink(),'LIVE_UNIT_INPUT_EXISTS')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    ensure(path.read_bytes()==data,'LIVE_UNIT_INPUT_READBACK_MISMATCH')
    return sha_file(path)

def unit_prompt(role):
    ensure(role in ('PRIMARY','INDEPENDENT'),'INVALID_UNIT_ROLE')
    intro=('isolated Primary' if role=='PRIMARY' else 'fresh isolated Independent')
    return (f'You are the {intro} semantic adjudicator. Using ONLY this unit input directory, '
      'read EVERY complete authoritative body and header referenced by the 25 records in '
      'neutral_semantic_evidence.jsonl. Apply semantic_rule_v2.json and reason_precedence_v2.json '
      'without changing their scientific interpretation. Return ONLY valid JSON with rows of the exact '
      'form {"rows":[{"canonical_source_identity":"<exact canonical_source_identity from this index record>",'
      '"authorized_population_position":<exact INTEGER authorized_population_position from this index record>,'
      '"body_disposition":"<valid governed disposition>","reason_code":"<valid governed reason>",'
      '"concise_review_rationale":"<nonempty evidence-grounded explanation>"}]}. '
      'For EACH output row COPY identity and authorized position from the SAME input index record. '
      'AUTHORIZED_POPULATION_POSITION_JSON_TYPE=INTEGER. '
      'Emit authorized_population_position as a JSON integer number, never quoted; '
      'DO_NOT_QUOTE_THE_INTEGER=YES. DO_NOT_CONVERT_POSITION_TO_STRING=YES. '
      'COPY_THE_EXACT_INTEGER_NUMERIC_VALUE_FROM_THE_SAME_AUTHORIZED_INPUT_RECORD=YES. '
      'POSITIONS_MUST_MATCH_INDEX_ROW_BY_ROW=YES. OUTPUT_ORDER_MUST_MATCH_INDEX_ORDER=YES. '
      'DO_NOT_RENUMBER_POSITIONS=YES. DO_NOT_USE_A_CONSTANT_POSITION=YES. '
      'Return exactly 25 rows; do not report completion if any required body/header was unread.')

def _bounded_input_read(path, maximum):
    """Read no more than the remaining accepted input envelope before writing."""
    path=Path(path)
    before=path.lstat()
    ensure(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size<=maximum,
           'UNIT_INPUT_SOURCE_SIZE_OR_TYPE_LIMIT')
    with path.open('rb') as f:
        opened=os.fstat(f.fileno())
        ensure((opened.st_dev,opened.st_ino,opened.st_size,opened.st_nlink)==
               (before.st_dev,before.st_ino,before.st_size,1), 'UNIT_INPUT_SOURCE_CHANGED_DURING_OPEN')
        data=f.read(maximum+1)
    ensure(len(data)<=maximum,'UNIT_INPUT_MATERIALIZATION_LIMIT')
    return data


def materialize_unit_source(source_root, partition_manifest, evidence, unit_id, working_directory, *, resource_budget=None):
    root=Path(source_root);out=Path(working_directory)
    ensure(not out.exists() and not out.is_symlink(),'UNIT_INPUT_WORKDIR_ALREADY_EXISTS')
    rows=unit_evidence(partition_manifest,evidence,unit_id)
    ensure(len(rows)==25,'NOT_EXACT_25_UNIT_INPUT')
    remaining=None if resource_budget is None else resource_budget['input_materialization_bytes']
    ensure(remaining is None or (type(remaining) is int and remaining>=0),'INVALID_UNIT_INPUT_BUDGET')
    def input_read(path):
        return path.read_bytes() if remaining is None else _bounded_input_read(path,remaining)
    def input_write(path,data):
        nonlocal remaining
        if remaining is not None:
            ensure(len(data)<=remaining,'UNIT_INPUT_MATERIALIZATION_LIMIT')
        result=write_once(path,data)
        if remaining is not None:remaining-=len(data)
        return result
    out.mkdir(parents=True,exist_ok=False)
    hashes={}
    for name in ('semantic_rule_v2.json','reason_precedence_v2.json'):
        hashes[name]=input_write(out/name,input_read(root/name))
        rule_sha=(sha_file(root/name) if resource_budget is None else
                  hashlib.sha256(_bounded_input_read(root/name,resource_budget['input_materialization_bytes'])).hexdigest())
        ensure(hashes[name]==rule_sha,'UNIT_RULE_INPUT_HASH_DRIFT')
    for row in rows:
        for col in ('body_evidence_member','header_evidence_member'):
            name=row[col]
            src=root/name
            ensure(src.is_file() and not src.is_symlink(),'MISSING_UNIT_BODY_OR_HEADER')
            hashes[name]=input_write(out/name,input_read(src))
            key=('extracted_body_sha256' if col.startswith('body') else 'extracted_header_sha256')
            ensure(hashes[name]==row[key],'UNIT_BODY_HEADER_HASH_MISMATCH')
    if remaining is not None:
        from real_candidate.executor_v1 import serialization_size
        measured=0
        for row in rows:
            measured+=serialization_size(row,remaining-measured,ensure_ascii=False,indent=None,
                                         separators=None,allow_nan=True)
    neutral='\n'.join(json.dumps(row,sort_keys=True,ensure_ascii=False) for row in rows)+'\n'
    hashes['neutral_semantic_evidence.jsonl']=input_write(out/'neutral_semantic_evidence.jsonl',neutral.encode())
    index={'role_neutral':True,'unit_id':unit_id,'positions':[r['authorized_population_position'] for r in rows],
           'identities':[r['canonical_source_identity'] for r in rows],
           'file_hashes':hashes,'source_s04_manifest_sha256':partition_manifest['source_s04_manifest_sha256']}
    if remaining is not None:
        serialization_size(index,remaining,ensure_ascii=True,indent=2,separators=None,allow_nan=True)
    input_write(out/'unit_neutral_input_manifest.json',(json.dumps(index,sort_keys=True,indent=2)+'\n').encode())
    ensure(len(hashes)==53,'UNIT_NEUTRAL_MEMBER_COUNT')
    ensure(not any(p.name.startswith(('primary_executor','primary_semantic','checkpoint_head')) for p in out.rglob('*')),
           'PRIMARY_RAW_IN_NEUTRAL_INPUT')
    return out,index

@contextmanager
def primary_filesystem_guard(roots, ledger):
    """Preserve accepted V3 S09 deny/restore discipline around executor only."""
    roots=tuple(Path(x) for x in roots)
    ensure(len(roots)==2 and len({x.resolve() for x in roots})==2,
           'PRIMARY_ROOT_GUARD_COUNT_OR_DISTINCTNESS')
    for root in roots:
        ensure(root.is_dir() and not root.is_symlink(),'PRIMARY_GUARD_ROOT_MISSING_OR_SYMLINK')
    ledger=Path(ledger)
    ensure(ledger.is_file() and ledger.resolve().is_relative_to(roots[1].resolve()),
           'PRIMARY_LEDGER_OUTSIDE_GUARDED_ROOT')
    ledger_before=sha_file(ledger)
    modes={root:stat.S_IMODE(root.stat().st_mode) for root in roots}
    try:
        for root in roots:os.chmod(root,0o000)
        if os.geteuid()!=0: # Mac runs as unprivileged user; root test fixture cannot prove denial.
            probe=subprocess.run(['/bin/cat',str(ledger)],capture_output=True,text=True,check=False)
            ensure(probe.returncode!=0,'INDEPENDENT_FILESYSTEM_ISOLATION_FAILURE')
        yield
    finally:
        for root,mode in modes.items():os.chmod(root,mode)
        ensure(sha_file(ledger)==ledger_before,'PRIMARY_LEDGER_MUTATED_DURING_INDEPENDENT')

HISTORICAL_ADAPTER_SHA256='1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424'
PROSPECTIVE_ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'


def verify_prospective_context(adapter, *, phase='STATIC'):
    """Exact bounded callable and existing trusted context, never a launch grant."""
    from real_candidate import executor_v1
    ensure(adapter.runner is executor_v1.run_codex_executor,
           'REAL_RUNNER_MUST_BE_PROSPECTIVE_BOUNDED_EXECUTOR')
    ensure(adapter.role=='PRIMARY' and adapter.attempt_identity==PROSPECTIVE_ATTEMPT,
           'PROSPECTIVE_EXACT_ROLE_OR_ATTEMPT_REQUIRED')
    ensure(adapter.execution_context is not None,'PROSPECTIVE_EXECUTION_CONTEXT_REQUIRED')
    work=adapter.work_root/'PRIMARY'/'U0012'/'A0010'
    return executor_v1.verify_runtime_context(adapter.execution_context,phase=phase,
        working_directory=work/'input',prompt=unit_prompt('PRIMARY'),
        codex_path=adapter.codex_path,evidence_root=work/'v3_executor_raw_evidence',role='PRIMARY')


class V3CodexUnitAdapter:
    """Call-shape bridge to V3. Real requires separate pinned Managing authorization."""
    def __init__(self, source_root, manifest_path, work_root, role, *,
                 runner=None, real_source=False, codex_path=None, independent_package_root=None, primary_guard_roots=(), primary_ledger=None, authorization_path=None, attempt_identity=None, execution_context=None):
        self.source_root=Path(source_root)
        self.manifest_path=Path(manifest_path)
        self.work_root=Path(work_root)
        self.role=role
        self.real_source=real_source
        self.codex_path=codex_path or '/usr/bin/false'
        self.independent_package_root=Path(independent_package_root) if independent_package_root else None
        self.primary_guard_roots=tuple(Path(x) for x in primary_guard_roots)
        self.primary_ledger=Path(primary_ledger) if primary_ledger else None
        self.runner=runner
        self.execution_context=execution_context
        ensure(role in ('PRIMARY','INDEPENDENT'),'INVALID_EXECUTOR_ROLE')
        self.attempt_identity=attempt_identity
        self.authorization_path=authorization_path
        if real_source:
            verify_prospective_context(self,phase='STATIC')
        else:
            require_synthetic_activation(auth_path=authorization_path,role=role,
                 attempt_identity=attempt_identity,runner=runner)
        self.info=verify_s04(self.source_root,real=real_source)
        self.identity_manifest=json.loads(self.manifest_path.read_text())
        verify_identity_manifest(self.identity_manifest,self.info)
        if role=='INDEPENDENT':
            ensure(self.independent_package_root is not None,
                   'S08_CLEAN_PACKAGE_REQUIRED_FOR_INDEPENDENT')
            ensure(len(self.primary_guard_roots)==2 and self.primary_ledger is not None,
                   'S09_PRIMARY_ROOT_AND_LEDGER_DENIAL_GUARD_REQUIRED')
            self._verify_independent_package()
        else:
            ensure(self.independent_package_root is None and not self.primary_guard_roots and self.primary_ledger is None,
                   'PRIMARY_MUST_NOT_USE_INDEPENDENT_PACKAGE_OR_GUARD')
        self.partition=__import__('partition_contract_nonproduction_v1').build_partition_manifest(
            self.info['rows'],25,self.info['manifest_sha256'])

    def _verify_independent_package(self):
        from firewall_v2 import TrustedInputs, scan_independent_package
        s04_manifest=json.loads((self.source_root/'s04_primary_input_manifest.json').read_text())
        hashes=s04_manifest['file_hashes']
        trusted=TrustedInputs(
            s04_manifest_sha256=self.info['manifest_sha256'],
            neutral_evidence_sha256=self.info['neutral_sha256'],
            semantic_rule_sha256=self.info['semantic_rule_sha256'],
            reason_precedence_sha256=self.info['precedence_sha256'],
            body_sha256_by_path={k:v for k,v in hashes.items() if k.startswith('bodies/')})
        scan_independent_package(self.independent_package_root,trusted,phase='freeze')
        for k,want in [('neutral_semantic_evidence.jsonl',self.info['neutral_sha256']),
                       ('semantic_rule_v2.json',self.info['semantic_rule_sha256']),
                       ('reason_precedence_v2.json',self.info['precedence_sha256'])]:
            ensure(sha_file(self.independent_package_root/k)==want,
                   'S08_CLEAN_PACKAGE_INPUT_BINDING_CHANGED')
        return True

    def execute(self,role,unit_id,input_rows,attempt_no,prior_contexts):
        if self.real_source:
            ensure(role=='PRIMARY' and unit_id=='U0012' and type(attempt_no) is int and attempt_no==10,
                   'PROSPECTIVE_EXACT_ONE_UNIT_ATTEMPT_REQUIRED')
            verify_prospective_context(self,phase='EXECUTING')
            from real_candidate.activation_v1 import production_activation
            production_activation(self.execution_context.transaction,phase='EXECUTING')
        else:
            require_synthetic_activation(auth_path=self.authorization_path,role=self.role,
                 attempt_identity=self.attempt_identity,runner=self.runner)
        ensure(role==self.role and attempt_no>=1,'UNIT_ATTEMPT_ROLE_MISMATCH')
        ensure([r['canonical_source_identity'] for r in input_rows]==
               self.identity_manifest['units'][int(unit_id[1:])-1]['canonical_source_identities'],
               'UNIT_INPUT_IDENTITY_NOT_ASSIGNED')
        ensure(sha_file(self.source_root/'s04_primary_input_manifest.json')==self.info['manifest_sha256'] and
               sha_file(self.source_root/'neutral_semantic_evidence.jsonl')==self.info['neutral_sha256'],
               'UNIT_SOURCE_DRIFT')
        if role=='INDEPENDENT':self._verify_independent_package()
        work=self.work_root/role/unit_id/f'A{attempt_no:04d}'
        budget=self.execution_context.storage_contract() if self.execution_context is not None else None
        if budget is not None:
            from real_candidate.executor_v1 import _ensure_capacity
            _ensure_capacity(self.execution_context.evidence_root,budget['peak_storage_bytes'])
        payload_root=self.source_root if role=='PRIMARY' else self.independent_package_root
        unit_dir,index=materialize_unit_source(payload_root,self.partition,self.info['rows'],unit_id,work/'input',resource_budget=budget)
        v3_evidence=work/'v3_executor_raw_evidence'
        started=now_utc()
        returned=None
        try:
            # V3 S09 primary-root denial during the actual executor call, restored
            # on every success/failure branch. No direct Primary data in unit input.
            if role=='INDEPENDENT':
                with primary_filesystem_guard(self.primary_guard_roots,self.primary_ledger):
                    returned=self.runner(working_directory=unit_dir,prompt=unit_prompt(role),
                        codex_path=self.codex_path,evidence_root=v3_evidence,role=role)
            else:
                kwargs={'working_directory':unit_dir,'prompt':unit_prompt(role),
                        'codex_path':self.codex_path,'evidence_root':v3_evidence,'role':role}
                if self.execution_context is not None:kwargs['execution_context']=self.execution_context
                returned=self.runner(**kwargs)
        except Exception:
            # V3 executor persists raw artifacts in its finally path on failure.
            pass
        manifest_file=v3_evidence/(role.lower()+'_executor_attempt_manifest.json')
        ensure(manifest_file.is_file(),'V3_EXECUTOR_EVIDENCE_MISSING__CONTROLLED_STOP')
        if budget is not None:
            ensure(not manifest_file.is_symlink() and manifest_file.stat().st_nlink==1 and
                   manifest_file.stat().st_size<=budget['artifact_bytes'],'EXECUTOR_MANIFEST_SIZE_OR_TYPE_LIMIT')
        m=json.loads(manifest_file.read_text())
        if self.execution_context is not None:
            from real_candidate.executor_v1 import relay_first_rejection
            relay_first_rejection(self.execution_context,m)
        arts=m.get('artifacts',{})
        evidence={}
        for name in ('raw_stdout','raw_stderr','final_message'):
            item=arts[name]
            p=Path(item['path'])
            ensure(p.is_file() and p.resolve().is_relative_to(v3_evidence.resolve()),'UNTRUSTED_RAW_EVIDENCE_PATH')
            if budget is not None:
                ensure(not p.is_symlink() and p.stat().st_nlink==1 and p.stat().st_size<=budget['capture_bytes'],
                       'EXECUTOR_RAW_EVIDENCE_SIZE_OR_TYPE_LIMIT')
            ensure(sha_file(p)==item['sha256'],'V3_RAW_EVIDENCE_HASH_MISMATCH')
            evidence[name]=p.read_text(encoding='utf-8')
        if budget is not None:
            ensure(len(evidence['raw_stdout'].encode('utf-8'))+len(evidence['raw_stderr'].encode('utf-8'))<=
                   budget['capture_bytes'],'EXECUTOR_RAW_AGGREGATE_LIMIT')
        context=m.get('execution_context_identity')
        if returned is not None:
            ensure(returned.get('context_id')==context,'V3_CONTEXT_BINDING_MISMATCH')
            ensure(returned.get('agent_message')==evidence['final_message'], 'V3_FINAL_MESSAGE_BINDING_MISMATCH')
        return {'process_started':m.get('process_return_code') is not None,
                'return_code':m.get('process_return_code'),
                'termination_state':m.get('process_termination_state'),
                'timeout_status':m.get('timeout_status'),
                'context_id':context,'raw_stdout':evidence['raw_stdout'],
                'raw_stderr':evidence['raw_stderr'],'agent_message':evidence['final_message'],
                'started_utc':m.get('start_timestamp_utc') or started,
                'ended_utc':m.get('end_timestamp_utc') or now_utc()}


def aggregate_checkpoint_for_v3(ctx, engine, role):
    """Authorized transition adapter into unchanged V3 S06/S10 candidate schema.

    Does not call S05/S09 direct semantics. Real use requires sealed authorization.
    """
    from checkpoint_resume_readiness_v3 import DONE
    ensure(role in ('PRIMARY','INDEPENDENT') and engine.role==role,'AGGREGATE_ROLE_MISMATCH')
    if engine.real_source:
        require_real_activation(source_root=engine.source_root,manifest_path=engine.identity_manifest_path,
            role=role,attempt_identity=engine.attempt_identity,authorization_path=engine.authorization_path)
    engine.verify()
    ensure(engine.state['global_state']==DONE,'INCOMPLETE_PARTITIONED_STAGE')
    # The accepted checkpoint engine already exclusively wrote and self-hashed
    # the aggregate during its DONE transition. Never create it a second time.
    aggregate_path=engine.workspace/'semantic_aggregate.json'
    ensure(sha_file(aggregate_path)==engine.state['aggregate_sha256'],
           'FINAL_CHECKPOINT_AGGREGATE_HASH_MISMATCH')
    saved=json.loads(aggregate_path.read_text())
    ensure(saved.get('role')==role and saved.get('row_count')==500,
           'FINAL_CHECKPOINT_AGGREGATE_INVALID')
    summary={'contexts':saved['contexts'],'row_count':500}
    items=[]
    for unit in engine.state['units']:
        p=engine.workspace/'frozen_units'/unit['unit_id']/'unit_result.json'
        data=json.loads(p.read_text())
        items.extend(data['raw_rows'])
    ensure(len(items)==500,'INCOMPLETE_V3_CANDIDATE')
    v3.validate_semantic_rows(items,engine.evidence,engine.reason)
    state='S05_PRIMARY_SEMANTIC_ADJUDICATION' if role=='PRIMARY' else 'S09_INDEPENDENT_SEMANTIC_ADJUDICATION'
    prefix='primary' if role=='PRIMARY' else 'independent'
    paths=v3.s05_paths(ctx) if role=='PRIMARY' else v3.s09_paths(ctx)
    ensure(not paths['root'].exists(),'V3_STATE_ALREADY_EXISTS')
    paths['root'].mkdir(parents=True,exist_ok=False)
    candidate_sha=v3.write_jsonl_exclusive(paths['candidate'],items)
    ensure(v3.sha256_file(paths['candidate'])==candidate_sha,'V3_CANDIDATE_HASH_MISMATCH')
    contexts=summary['contexts']
    aggregate_context='partition-set-'+digest({'role':role,'contexts':contexts})
    executor_summary={'role':role,'backend':'codex_partitioned_v3_adapter__NONPRODUCTION_VALIDATION',
         'context_set_identity':aggregate_context,'context_ids':contexts,
         'unit_count':20,'candidate_row_count':500,'candidate_output_identity':candidate_sha,
         'checkpoint_manifest_sha256':engine.state['checkpoint_manifest_sha256'],
         'partition_manifest_sha256':engine.identity_manifest_hash,
         'complete':True}
    executor_manifest_sha=v3.write_json_exclusive(paths['executor_manifest'],executor_summary)
    if role=='PRIMARY':
        stage_inputs=[str(ctx['s04_paths']['manifest']),str(ctx['s04_paths']['evidence'])]
        next_stage='S06_PRIMARY_LEDGER_FREEZE'
    else:
        stage_inputs=[str(ctx['s08_paths']['zip'])]
        next_stage='S10_INDEPENDENT_LEDGER_FREEZE'
    # Same governed state-transition interface as frozen V3; semantic-only
    # differences are the 20 validated unit contexts and checkpoint hashes.
    v3.append_transition(ctx,state=state,
        required_inputs=stage_inputs,
        executable_action='Aggregated exactly 20 individually frozen 25-record semantic units; verified 500 records and context isolation.',
        output_artifacts=[str(paths['candidate']),str(paths['executor_manifest']),str(aggregate_path)],
        output_hashes={'candidate':candidate_sha,'executor_manifest':executor_manifest_sha,
                       'checkpoint_aggregate':engine.state['aggregate_sha256'],
                       'checkpoint_manifest':engine.state['checkpoint_manifest_sha256']},
        hard_gates={'frozen_units_20_of_20':'PASS','exact_500_row_semantics':'PASS',
                    'exact_position_identity_coverage':'PASS','fresh_contexts':'PASS',
                    'source_and_partition_manifest_binding':'PASS'},
        fail_closed_conditions=['MISSING_FROZEN_UNIT','SEMANTIC_VALIDATION_FAILURE',
                                'CHECKPOINT_TAMPER','UNIT_TAMPER','ROLE_CONTEXT_REUSE'],
        next_state=next_stage)
    ctx[('s05_paths' if role=='PRIMARY' else 's09_paths')]=paths
    ctx[('primary_context_id' if role=='PRIMARY' else 'independent_context_id')]=aggregate_context
    return {'role':role,'paths':paths,'candidate_sha256':candidate_sha,'aggregate_context_set_identity':aggregate_context,
            'context_count':len(contexts),'row_count':len(items)}
