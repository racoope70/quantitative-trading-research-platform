"""Synthetic fixture construction and bounded host-access guard; no REAL inputs."""
import copy,hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PYTHON='/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12'
sha=lambda b:hashlib.sha256(b).hexdigest()
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n').encode()
AUDIT={'denied_outside_operations':0,'protected_operations':0,'subprocesses':0}
_original_stat=os.stat;_original_lstat=os.lstat
def guard():
    library=str(Path(sys.base_prefix)/'lib')
    def checked(p,write=False,metadata=False):
        if isinstance(p,int):return
        p=os.path.abspath(os.fsdecode(p))
        allowed=p==str(ROOT) or p.startswith(str(ROOT)+'/') or p==library or p.startswith(library+'/') or p in (PYTHON,'/dev/null')
        if metadata and any(q.startswith(p.rstrip('/')+'/') for q in (str(ROOT),library,PYTHON)):allowed=True
        if not allowed or (write and not(p.startswith(str(ROOT)+'/') or p=='/dev/null')):
            AUDIT['denied_outside_operations']+=1
            raise PermissionError('OUTSIDE_SYNTHETIC_SCOPE')
    def stat_guard(p,*a,**kw):
        checked(p,metadata=True);return _original_stat(p,*a,**kw)
    def lstat_guard(p,*a,**kw):
        checked(p,metadata=True);return _original_lstat(p,*a,**kw)
    os.stat=stat_guard;os.lstat=lstat_guard
    def audit(event,args):
        if event=='open':
            p,mode,flags=args
            checked(p,write=bool(flags and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
        elif event in ('os.listdir','os.scandir'):checked(args[0])
        elif event.startswith('socket.') or event in ('os.system','os.exec','os.posix_spawn','os.fork'):
            raise PermissionError('NETWORK_OR_UNAPPROVED_PROCESS_FORBIDDEN')
        elif event=='subprocess.Popen':
            exe,argv,cwd,env=args
            if exe!=PYTHON or not ('-I' in argv) or (cwd and not str(cwd).startswith(str(ROOT))):
                raise PermissionError('ONLY_ISOLATED_SYNTHETIC_PYTHON_CHILD')
            AUDIT['subprocesses']+=1
        elif event in ('os.mkdir','os.remove','os.rmdir','os.chmod','os.chown','os.truncate','os.utime'):
            checked(args[0],write=True)
        elif event in ('os.rename','os.link'):
            checked(args[0],write=True);checked(args[1],write=True)
    sys.addaudithook(audit)

def bootstrap():
    guard()
    spec=importlib.util.spec_from_file_location('model_b_composition',ROOT/'composition.py')
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    return mod

def make_engine(c,label):
    core=__import__('checkpoint_resume_activation_trusted_v1')
    from real_candidate.policy_b_proof_v1 import PolicyBPredecessor
    directory=ROOT/'fixtures'/label;directory.mkdir(mode=0o700)
    engine=core.CheckpointEngine(directory/'state','PRIMARY')
    attempt='SYNTHETIC_POLICY_B_MODEL_B_'+label
    engine.initialize(attempt)
    final=[{'canonical_source_identity':r['canonical_source_identity'],
        'authorized_population_position':r['authorized_population_position'],
        'body_disposition':'BODY_INACCESSIBLE_OR_UNRESOLVED','reason_code':'U1_AUTHORITATIVE_BODY_NOT_AVAILABLE',
        'concise_review_rationale':'Fresh synthetic unavailable-body case.'} for r in engine.evidence]
    predecessor=core.SyntheticMockExecutor(final,run_nonce=label)
    for u in engine.state['units'][:11]:
        rows=core.unit_evidence(engine.partition,engine.evidence,u['unit_id'])
        result=predecessor.execute('PRIMARY',u['unit_id'],rows,1,())
        checked=core.validate_semantic_unit(engine.partition,engine.evidence,engine.reason,u['unit_id'],result,'PRIMARY')
        manifest=engine._record_attempt(u,result,'EXECUTOR_NORMAL_RETURN')
        digest=core.unique_write(engine.workspace/'frozen_units'/u['unit_id']/'unit_result.json',core.obj_bytes(checked))
        u.update(state='FROZEN',frozen_output_sha256=digest,executor_attempt_manifest_sha256=manifest,frozen_context_id=result['context_id'])
    u=engine.state['units'][11];rows=core.unit_evidence(engine.partition,engine.evidence,'U0012')
    for n in range(1,11):
        result=predecessor.execute('PRIMARY','U0012',rows,n,())
        engine._record_attempt(u,result,'EXECUTOR_NORMAL_RETURN' if n==1 else 'EXTERNAL_CONFLICT__CONTROLLED_STOP')
    engine.state.update(global_state=core.NON_RESUMABLE,stop_reason='SYNTHETIC_ORIGINAL_CONTROLLED_STOP')
    while engine.state['checkpoint_sequence']<54:engine._snapshot()
    engine.verify(expected_attempt_id=attempt)
    raw=b''.join(canonical(row) for row in rows)
    case=c.recovery.synthetic_case(engine,raw)
    transaction=c.recovery.ControlledStopRecovery(engine,copy.deepcopy(case),raw,expected_case=copy.deepcopy(case))
    frame=directory/'frame.json';frame.write_bytes(canonical(rows))
    head=core.strictly_json(engine.head);snapshot=engine.workspace/'checkpoints'/head['snapshot_file']
    checkpoint=PolicyBPredecessor(case['checkpoint_manifest_sha256'],54,sha(snapshot.read_bytes()),sha(engine.head.read_bytes()))
    return directory,engine,transaction,frame,checkpoint

def child_source(fault='ok'):
    # This fixed synthetic processor receives stdin only. No provider, source
    # loader, authority channel, file/metadata access, network or child launch.
    return '''import json,os,sys,time
fault='''+repr(fault)+'''
def denied(*a,**kw):raise PermissionError('SYNTHETIC_CHILD_FILESYSTEM_OR_PROCESS_DENIED')
def hook(event,args):
    if event=='open' or event.startswith(('socket.','subprocess.')) or event in ('os.listdir','os.scandir','os.system','os.exec','os.fork','os.posix_spawn','os.mkdir','os.remove','os.rename'):denied()
sys.addaudithook(hook)
os.stat=denied;os.lstat=denied;os.scandir=denied;os.listdir=denied;os.pipe=denied
rows=json.load(sys.stdin)
assert len(rows)==25
if fault=='timeout':time.sleep(1)
if fault=='failed':sys.exit(7)
if fault=='boundary':
    try:open('/QTRP_SYNTHETIC_FORBIDDEN_CANARY','rb')
    except PermissionError:print('BOUNDARY_REJECTED',file=sys.stderr);sys.exit(9)
output={'rows':[{'canonical_source_identity':r['canonical_source_identity'],'authorized_population_position':r['authorized_population_position'],'body_disposition':'BODY_INACCESSIBLE_OR_UNRESOLVED','reason_code':'U1_AUTHORITATIVE_BODY_NOT_AVAILABLE','concise_review_rationale':'Fresh synthetic unavailable-body case.'} for r in rows]}
if fault=='malformed':output['rows'][0]['reason_code']='INVALID'
if fault=='short':output['rows'].pop()
if fault=='reason_precedence':output['rows'][0]['body_disposition']='BODY_CONFIRMED_NONCALENDAR'
events=[{'type':'thread.started','thread_id':'synthetic-thread-'+str(os.getpid())},{'type':'turn.started'}]
if fault=='internal':events += [{'type':'item.started','item':{'id':'item_0','type':'command_execution','command':'synthetic command','aggregated_output':'','exit_code':None,'status':'in_progress'}},{'type':'item.completed','item':{'id':'item_0','type':'command_execution','command':'synthetic command','aggregated_output':'synthetic failed','exit_code':1,'status':'completed'}}]
events.append({'type':'item.completed','item':{'id':'item_1','type':'agent_message','text':json.dumps(output,sort_keys=True,separators=(',',':'))}})
events.append({'type':'turn.completed','usage':{'input_tokens':0,'cached_input_tokens':0,'output_tokens':0}})
if fault=='duplicate':events.append(events[-1])
if fault=='incomplete':events.pop()
if fault=='types':events[-1]['usage']['input_tokens']=True
for event in events:print(json.dumps(event,sort_keys=True,separators=(',',':')),flush=True)
'''

def components(c,label,fault='ok'):
    from real_candidate.capture_v1 import ControlledLocalCapture
    from real_candidate.validation_v1 import BoundAcceptedValidator
    from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBCapturedFixtureExecutor
    from trusted_stage.staging_v1 import UnitBinding
    directory,engine,t,frame,checkpoint=make_engine(c,label)
    cwd=directory/'work/PRIMARY/U0012/A0011/input';cwd.mkdir(parents=True)
    supervisor=ControlledLocalCapture(executable=Path(PYTHON),executable_sha256=sha(Path(PYTHON).read_bytes()),
        argv=('-I','-c',child_source(fault)),cwd=cwd,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1'},
        adapter_sha256=sha((ROOT/'candidate/real_candidate/policy_b_proof_v1.py').read_bytes()),
        mode='NONPRODUCTION_TEST',allow_test_fixture=True,child_capture_budget_seconds=0.05 if fault=='timeout' else 5)
    source=ROOT/'candidate/dependencies/synthetic_fixture'
    validator=BoundAcceptedValidator(accepted_root=ROOT/'accepted',supervisor=supervisor,
        partition_path=source/'partition.json',evidence_path=source/'evidence.json',reason_path=source/'reason_normalized.json',
        partition_sha256=sha((source/'partition.json').read_bytes()),evidence_sha256=sha((source/'evidence.json').read_bytes()),reason_sha256=sha((source/'reason_normalized.json').read_bytes()))
    path=PolicyBProofPath(supervisor=supervisor,validator=validator,release_root=ROOT,synthetic_engine=engine)
    rows=engine.evidence[275:300]
    binding=UnitBinding('BATCH0004','PRIMARY','U0012',t.case['attempt_id'],checkpoint.identity,sha(frame.read_bytes()),
        'SYNTHETIC_NONPRODUCTION',supervisor.config_sha256,tuple(range(1776,1801)),tuple(r['canonical_source_identity'] for r in rows),1)
    executor=PolicyBCapturedFixtureExecutor(path)
    return {'directory':directory,'engine':engine,'t':t,'frame':frame,'checkpoint':checkpoint,'supervisor':supervisor,'path':path,'binding':binding,'executor':executor}
