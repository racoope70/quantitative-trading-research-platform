"""Bounded real child / accepted validator / Policy B / recovery integration."""
import copy,dataclasses,hashlib,json,os,subprocess,sys,time,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap()
import owner_authorization as owner
import owner_publication as publication
import checkpoint_resume_activation_trusted_v1 as core
from real_candidate import activation_v1
from trusted_stage.staging_v1 import verify_stage
RUN=str(time.time_ns())
RESULTS=[]
def check(label,fn):
    try: detail=fn();record={'test':label,'result':'PASS','detail':detail}
    except Exception as exc:
        record={'test':label,'result':'FAIL','type':type(exc).__name__,'error':str(exc)[:500]}
        traceback.print_exc()
    RESULTS.append(record);print(json.dumps(record,sort_keys=True),flush=True)
    return record['result']=='PASS'
def rejected(fn):
    try: fn()
    except Exception as exc:return {'rejected':True,'type':type(exc).__name__,'reason':str(exc)[:180]}
    raise AssertionError('EXPECTED_REJECTION')
def document(x):
    return owner.model_b_document(x['t'],x['executor'],x['path'],x['binding'],x['frame'],n.ROOT)
def publish(x,name='authority',doc=None):
    raw=n.canonical(document(x) if doc is None else doc)
    candidate=x['directory']/(name+'.candidate.json');candidate.write_bytes(raw);candidate.chmod(0o600)
    directory=x['directory']/name
    rd,wr=os.pipe()
    os.write(wr,n.canonical({'task_id':publication.MODEL_B_TASK,
        'sha256':n.sha(raw),'length':len(raw),'owner_pid':os.getpid()}));os.close(wr)
    try:
        result=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/owner_publish.py'),str(rd),str(candidate),str(directory),n.sha(raw),str(len(raw))],
            cwd=n.ROOT,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},pass_fds=(rd,),capture_output=True,timeout=20)
    finally:os.close(rd)
    return directory,raw,result
def consume(x,directory,raw):
    return owner.consume_model_b(n.sha(raw),len(raw),directory=directory,t=x['t'],executor=x['executor'],
        path=x['path'],binding=x['binding'],frame=x['frame'],release_root=n.ROOT)
def prepare(x):
    directory,raw,p=publish(x)
    assert p.returncode==0,p.stderr.decode()
    consume(x,directory,raw)
    x['t'].bind_v7_verifier(x['path'],binding=x['binding'],checkpoint=x['checkpoint'],
        input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,release_root=n.ROOT)
    return directory,raw
def unchanged(x,head):
    assert x['engine'].head.read_bytes()==head
    assert not (x['engine'].workspace/'frozen_units/U0012').exists()
    x['engine'].verify();assert x['engine'].state['units'][11]['attempt_count']==10
    assert x['engine'].state['units'][12]['attempt_count']==0
def issue(x,o):
    return x['path'].issue(capture=o,input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,
        stage_root=x['directory']/'stage',binding=x['binding'],checkpoint=x['checkpoint'])
def observe(x):
    return x['supervisor'].observe(input_file=x['frame'],pinned_input_sha256=x['binding'].unit_input_sha256,
        timeout_seconds=x['supervisor'].child_capture_budget_seconds,test_only=True)
def fresh_readback(x):
    p=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/verify_state.py'),x['directory'].name],cwd=n.ROOT,
        env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},capture_output=True,timeout=20)
    assert p.returncode==0,p.stderr.decode()
    return json.loads(p.stdout)

def negative_suite():
    x=n.components(c,'auth_'+RUN);head=x['engine'].head.read_bytes()
    for key,value in [('unit_id','U0013'),('attempt_ordinal',12),('checkpoint_identity','f'*64),
                      ('input_sha256','f'*64),('runtime_sha256','f'*64),('configuration_sha256','f'*64),
                      ('policy_sha256','f'*64),('real_execution_authorized',True),('environment','REAL')]:
        def case(key=key,value=value):
            doc=document(x);doc['target_authorization'][key]=value
            directory,raw,p=publish(x,'wrong_'+key,doc)
            if p.returncode==0: verdict=rejected(lambda:consume(x,directory,raw))
            else: verdict={'rejected':True,'stage':'OWNER_PUBLICATION','publisher_exit':p.returncode}
            unchanged(x,head);assert not x['supervisor']._observed
            return verdict
        check('AUTH_'+key,case)
    def source_mismatch():
        doc=document(x);doc['fixture_binding']['sources']['POLICY_B_POLICY']='e'*64
        directory,raw,p=publish(x,'wrong_source',doc);assert p.returncode==0
        result=rejected(lambda:consume(x,directory,raw));unchanged(x,head);return result
    check('AUTH_source_identity',source_mismatch)
    def no_authority():
        result=rejected(lambda:observe(x));unchanged(x,head);assert not x['supervisor']._observed;return result
    check('NO_AUTHORITY_AT_ACTUAL_CHILD_SINK',no_authority)
    def missing():
        result=rejected(lambda:consume(x,x['directory']/'missing',b'{}\n'));unchanged(x,head);return result
    check('MISSING_AUTHORIZATION',missing)
    def malformed():
        result=rejected(lambda:publication.validate_model_b_document(b'{"schema":true}\n'));unchanged(x,head);return result
    check('MALFORMED_AUTHORIZATION',malformed)
    check('EXECUTOR_SELF_PUBLICATION_NO_OWNER_CHANNEL',lambda:rejected(lambda:publication.publish_model_b(
        x['directory']/'unapproved',n.sha(b''),0,approval_fd=None,directory=x['directory']/'self_authorized')))
    check('REAL_ACTIVATION_WITHOUT_REAL_OWNER_TRANSACTION',lambda:rejected(lambda:activation_v1.production_activation(x['t'])))
    check('REAL_DOCUMENT_VALIDATOR_REJECTS_SYNTHETIC_AUTHORIZATION',lambda:rejected(lambda:publication.validate_owner_document(n.canonical(document(x)))))
    check('INPUT_PATH_OUTSIDE_SYNTHETIC_SCOPE_REJECTED_BEFORE_IO',lambda:rejected(lambda:owner.model_b_document(
        x['t'],x['executor'],x['path'],x['binding'],Path('/QTRP_SYNTHETIC_OUTSIDE_SCOPE/frame.json'),n.ROOT)))
    check('STAGE_PATH_OUTSIDE_SYNTHETIC_SCOPE_REJECTED_BEFORE_IO',lambda:rejected(lambda:activation_v1.run_model_b_synthetic(
        'f'*64,1,directory=x['directory']/'missing',transaction=x['t'],executor=x['executor'],proof_path=x['path'],
        binding=x['binding'],checkpoint=x['checkpoint'],input_path=x['frame'],release_root=n.ROOT,
        stage_root=Path('/QTRP_SYNTHETIC_OUTSIDE_SCOPE/stage'))))
    for fault in ['failed','timeout','malformed','short','internal','duplicate','incomplete','types','reason_precedence','boundary']:
        def case(fault=fault):
            y=n.components(c,fault+'_'+RUN,fault);h=y['engine'].head.read_bytes()
            directory,raw=prepare(y);o=observe(y)
            result=rejected(lambda:issue(y,o));unchanged(y,h)
            replay=rejected(lambda:observe(y));unchanged(y,h)
            verification=fresh_readback(y)
            assert verification['U0012']=='PENDING' and verification['attempt_count']==10
            detail={'rejection':result,'actual_child_exit':o.exit_code,'actual_timeout':o.timeout,
                'capture_complete':o.capture_complete,'cleanup_complete':o.cleanup_complete,
                'launch_count':len(y['supervisor']._observed),'no_checkpoint_advance':True,
                'replay':replay,'fresh_process':verification}
            (y['directory']/'actual_stdout.jsonl').write_bytes(o.stdout)
            (y['directory']/'actual_stderr.txt').write_bytes(o.stderr)
            return detail
        check('CHILD_'+fault,case)
    def proof_tamper():
        y=n.components(c,'proof_'+RUN);h=y['engine'].head.read_bytes();prepare(y);o=observe(y)
        stage,proof,receipt=issue(y,o)
        bad=copy.deepcopy(proof.claims);bad['CONTEXT']['input_sha256']='f'*64
        p=type(proof)(bad,__import__('real_candidate.policy_b_proof_v1',fromlist=['proof_hash']).proof_hash(bad))
        a=rejected(lambda:y['path'].verify_proof(p,receipt,phase='STAGED',stage=stage))
        raw=stage.file.read_bytes();stage.file.chmod(0o600);stage.file.write_bytes(raw+b' ')
        b=rejected(lambda:y['path'].verify_prepared())
        unchanged(y,h);return {'forged_proof':a,'stage_readback_mismatch':b,'no_checkpoint_advance':True}
    check('FORGED_PROOF_AND_STAGE_READBACK_REJECTION',proof_tamper)

def positive():
    x=n.components(c,'positive_'+RUN);engine=x['engine']
    frozen={p.as_posix():n.sha(p.read_bytes()) for p in (engine.workspace/'frozen_units').rglob('unit_result.json')}
    directory,raw,p=publish(x);assert p.returncode==0,p.stderr.decode()
    outcome=activation_v1.run_model_b_synthetic(n.sha(raw),len(raw),directory=directory,transaction=x['t'],
        executor=x['executor'],proof_path=x['path'],binding=x['binding'],checkpoint=x['checkpoint'],
        input_path=x['frame'],release_root=n.ROOT,stage_root=x['directory']/'stage')
    assert outcome['outcome']=='FROZEN',outcome['outcome']
    o=outcome['capture'];stage=outcome['stage'];proof=outcome['proof'];receipt=outcome['receipt']
    assert o.exit_code==0 and o.capture_complete and o.cleanup_complete and not o.timeout
    assert len(receipt.payload['validated_rows'])==25
    assert verify_stage(stage)==n.canonical(receipt.payload)
    assert x['executor'].calls==1 and len(x['supervisor']._observed)==1
    assert x['path'].consume_count==1
    assert frozen=={p:n.sha(Path(p).read_bytes()) for p in frozen}
    engine.verify();u=engine.state['units'][11]
    assert u['state']=='FROZEN' and u['attempt_count']==11
    assert engine.state['units'][12]['state']=='PENDING' and engine.state['units'][12]['attempt_count']==0
    replay=rejected(lambda:consume(x,directory,raw))
    retry=rejected(lambda:observe(x))
    readback=fresh_readback(x)
    assert readback['frozen_units']==12 and readback['U0012']=='FROZEN' and readback['attempt_count']==11
    assert readback['U0013_attempt_count']==0
    for name,data in [('actual_stdout.jsonl',o.stdout),('actual_stderr.txt',o.stderr),
        ('proof.json',n.canonical(dataclasses.asdict(proof))),('scientific_receipt_claims.json',n.canonical(receipt.claims))]:
        (x['directory']/name).write_bytes(data)
    detail={'actual_child_execution':True,'rows':25,'child_exit_code':o.exit_code,
        'capture_complete':o.capture_complete,'cleanup_complete':o.cleanup_complete,'stdout_sha256':o.stdout_sha256,
        'stderr_sha256':o.stderr_sha256,'capture_nonce':o.invocation_id,'Policy_B':'PASS',
        'staging_readback_proof':'PASS','proof_sha256':proof.proof_sha256,'stage_sha256':stage.staged_bytes_sha256,
        'predecessor_checkpoint_sequence':54,'final_checkpoint_sequence':readback['checkpoint_sequence'],
        'frozen_prefix_preserved':275,'new_accepted_units':1,'U0013_attempts':0,'Owner_publication':json.loads(p.stdout),
        'replay':replay,'retry':retry,'fresh_process_verification':readback,'fixture':str(x['directory'])}
    (n.ROOT/'evidence/SYNTHETIC_END_TO_END.json').write_bytes(n.canonical(detail))
    return detail

if sys.argv[1:]==['--negative']:
    negative_suite();name='FOCUSED_NEGATIVE_RESULTS.json'
elif sys.argv[1:]==['--positive']:
    prior=json.loads((n.ROOT/'evidence/FOCUSED_NEGATIVE_RESULTS.json').read_bytes())
    assert all(x['result']=='PASS' for x in prior['results']), 'NEGATIVE_GATES_NOT_PASS'
    check('COMPLETE_MODEL_B_SYNTHETIC_25_RECORD_INTEGRATION',positive);name='POSITIVE_INTEGRATION_RESULTS.json'
else:raise SystemExit('Use --negative or --positive')
value={'classification':'CODEX_REPORTED','results':RESULTS,'passed':sum(x['result']=='PASS' for x in RESULTS),
    'total':len(RESULTS),'audit':n.AUDIT,'REAL_activation':'HARD_DISABLED'}
(n.ROOT/'evidence'/name).write_bytes(n.canonical(value))
raise SystemExit(0 if value['passed']==value['total'] else 1)
