"""Only disposable synthetic FILE_IDENTITY_FRAME fixtures, using existing capture."""
import copy,json,os,subprocess
from pathlib import Path
import np_support as n

def child_source(fault='ok'):
    source=n.child_source(fault)
    source=source.replace('import json,os,sys,time','import json,os,sys,time,hashlib,stat\nframe_path=sys.argv[1]\nexpected_sha=sys.argv[2]\nexpected_size=int(sys.argv[3])')
    source=source.replace("if event=='open' or event.startswith(('socket.','subprocess.'))", "if event=='open' and isinstance(args[0],str) and args[0]==frame_path and not (args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)):return\n    if event=='open' or event.startswith(('socket.','subprocess.'))")
    source=source.replace('rows=json.load(sys.stdin)', '''assert os.read(0,1)==b'', 'STDIN_FALLBACK_FORBIDDEN'
fd=os.open(frame_path,os.O_RDONLY|os.O_NOFOLLOW)
try:
    before=os.fstat(fd)
    assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==expected_size
    raw=b''
    while len(raw)<=expected_size:
        part=os.read(fd,min(65536,expected_size+1-len(raw)))
        if not part:break
        raw+=part
    after=os.fstat(fd)
    expected_identity=json.loads(sys.argv[4])
    assert expected_identity=={'device':before.st_dev,'inode':before.st_ino,'size':before.st_size,'mtime_ns':before.st_mtime_ns,'links':before.st_nlink}
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
finally:os.close(fd)
assert len(raw)==expected_size and hashlib.sha256(raw).hexdigest()==expected_sha
rows=json.loads(raw)
diag={'pid':os.getpid(),'cwd':os.getcwd(),'executable':sys.executable,'argv':sys.argv[1:],
    'frame_path_sha256':hashlib.sha256(frame_path.encode()).hexdigest(),'frame_sha256':hashlib.sha256(raw).hexdigest(),
    'frame_length':len(raw),'stdin_bytes':0,'file_identity':{'device':before.st_dev,'inode':before.st_ino,'size':before.st_size,'mtime_ns':before.st_mtime_ns,'links':before.st_nlink},
    'environment':dict(os.environ)}
if fault=='overflow':sys.stdout.write('x'*2048);sys.stdout.flush();time.sleep(1)
if fault=='stderr':print('SYNTHETIC_STDERR_EXACT',file=sys.stderr)
''')
    source=source.replace("events.append({'type':'item.completed','item':{'id':'item_1'", "events += [{'type':'item.started','item':{'id':'item_0','type':'command_execution','command':'SYNTHETIC_FILE_IDENTITY_FRAME_CHECK','aggregated_output':'','exit_code':None,'status':'in_progress'}},{'type':'item.completed','item':{'id':'item_0','type':'command_execution','command':'SYNTHETIC_FILE_IDENTITY_FRAME_CHECK','aggregated_output':json.dumps(diag,sort_keys=True,separators=(',',':')),'exit_code':0,'status':'completed'}}]\nif fault=='position_type':output['rows'][0]['authorized_population_position']=str(output['rows'][0]['authorized_population_position'])\nevents.append({'type':'item.completed','item':{'id':'item_1'")
    source=source.replace("events.append({'type':'turn.completed'", "if fault in ('equivalent','conflicting'):\n    message=json.loads(json.dumps(events[-1]));message['item']['id']='item_2'\n    if fault=='conflicting':message['item']['text']=message['item']['text'].replace('Fresh synthetic','Different synthetic')\n    events.append(message)\nevents.append({'type':'turn.completed'")
    return source

def components(c,label,fault='ok',max_output=16*1024*1024):
    from real_candidate.capture_v1 import ControlledLocalCapture
    from real_candidate.validation_v1 import BoundAcceptedValidator
    from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBCapturedFixtureExecutor
    from trusted_stage.staging_v1 import UnitBinding
    directory,engine,t,frame,checkpoint=n.make_engine(c,label)
    cwd=directory/'work/PRIMARY/U0012/A0011/input';cwd.mkdir(parents=True)
    import owner_authorization as owner
    supervisor=ControlledLocalCapture(executable=Path(n.PYTHON),executable_sha256=n.sha(Path(n.PYTHON).read_bytes()),
        argv=('-I','-c',child_source(fault),str(frame),n.sha(frame.read_bytes()),str(frame.stat().st_size),n.canonical(owner.model_b_frame_identity(frame)).decode().strip()),cwd=cwd,
        # macOS Python initializes this key. Bind it explicitly in the fixture
        # so the child's observed environment equals its reviewed configuration.
        env={'PATH':'/usr/bin:/bin','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'},
        adapter_sha256=n.sha((n.ROOT/'candidate/real_candidate/policy_b_proof_v1.py').read_bytes()),mode='NONPRODUCTION_TEST',allow_test_fixture=True,
        input_delivery='FILE_IDENTITY_FRAME',max_output_bytes=max_output,child_capture_budget_seconds=0.05 if fault=='timeout' else 5)
    source=n.ROOT/'candidate/dependencies/synthetic_fixture'
    validator=BoundAcceptedValidator(accepted_root=n.ROOT/'accepted',supervisor=supervisor,
        partition_path=source/'partition.json',evidence_path=source/'evidence.json',reason_path=source/'reason_normalized.json',
        partition_sha256=n.sha((source/'partition.json').read_bytes()),evidence_sha256=n.sha((source/'evidence.json').read_bytes()),reason_sha256=n.sha((source/'reason_normalized.json').read_bytes()))
    path=PolicyBProofPath(supervisor=supervisor,validator=validator,release_root=n.ROOT,synthetic_engine=engine)
    binding=UnitBinding('BATCH0004','PRIMARY','U0012',t.case['attempt_id'],checkpoint.identity,n.sha(frame.read_bytes()),'SYNTHETIC_NONPRODUCTION',supervisor.config_sha256,tuple(range(1776,1801)),tuple(r['canonical_source_identity'] for r in engine.evidence[275:300]),1)
    executor=PolicyBCapturedFixtureExecutor(path)
    return dict(directory=directory,engine=engine,t=t,frame=frame,checkpoint=checkpoint,supervisor=supervisor,path=path,binding=binding,executor=executor)

def document(x):
    import owner_authorization as o
    return o.model_b_document(x['t'],x['executor'],x['path'],x['binding'],x['frame'],n.ROOT)

def publish(x,name='authority',doc=None,approval=None):
    import owner_publication as pub
    raw=n.canonical(document(x) if doc is None else doc);candidate=x['directory']/(name+'.candidate.json');candidate.write_bytes(raw);candidate.chmod(0o600);directory=x['directory']/name
    rd,wr=os.pipe();a={'task_id':pub.MODEL_B_TASK,'sha256':n.sha(raw),'length':len(raw),'owner_pid':os.getpid()}
    if approval is not None:a=approval(a)
    os.write(wr,n.canonical(a));os.close(wr)
    try:p=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/owner_publish.py'),str(rd),str(candidate),str(directory),n.sha(raw),str(len(raw))],cwd=n.ROOT,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},pass_fds=(rd,),capture_output=True,timeout=20)
    finally:os.close(rd)
    return directory,raw,p

def consume(x,d,raw):
    import owner_authorization as o
    return o.consume_model_b(n.sha(raw),len(raw),directory=d,t=x['t'],executor=x['executor'],path=x['path'],binding=x['binding'],frame=x['frame'],release_root=n.ROOT)

def prepare(x):
    d,raw,p=publish(x);assert p.returncode==0,p.stderr.decode();consume(x,d,raw)
    x['t'].bind_v7_verifier(x['path'],binding=x['binding'],checkpoint=x['checkpoint'],input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,release_root=n.ROOT)
    return d,raw

def observe(x,path=None,hook=None):
    return x['supervisor'].observe(input_file=x['frame'] if path is None else path,pinned_input_sha256=x['binding'].unit_input_sha256,timeout_seconds=x['supervisor'].child_capture_budget_seconds,test_only=True,prelaunch_hook=hook)

def child_diagnostic(observation):
    events=[json.loads(line) for line in observation.stdout.splitlines()]
    completed=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('command')=='SYNTHETIC_FILE_IDENTITY_FRAME_CHECK']
    assert len(completed)==1 and completed[0]['exit_code']==0
    return json.loads(completed[0]['aggregated_output'])
