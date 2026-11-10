"""Only new typed-contract / FILE transport / lifecycle / recovery qualifications."""
import copy,dataclasses,json,os,signal,subprocess,sys,time,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap();import file_frame_support as f
import owner_authorization as owner
import owner_publication as pub
from real_candidate import executor_v1 as ex,activation_v1 as activation
from real_candidate.real_binding_v1 import FutureRealUnitBinding
from trusted_stage.staging_v1 import verify_stage
RUN=str(time.time_ns());RESULTS=[]
SOURCE_IDS={str(p.relative_to(n.ROOT)):n.sha(p.read_bytes()) for folder in ('accepted','candidate','tests') for p in (n.ROOT/folder).rglob('*') if p.is_file()}
SOURCE_IDS['composition.py']=n.sha((n.ROOT/'composition.py').read_bytes())
SOURCE_INVENTORY_SHA=n.sha(n.canonical(SOURCE_IDS))
def check(id,group,kind,expected,fn):
 try:
  detail=fn();r={'test_id':id,'group':group,'execution_classification':kind,'expected_result':expected,'observed_result':detail,'result':'PASS'}
 except Exception as exc:
  traceback.print_exc();r={'test_id':id,'group':group,'execution_classification':kind,'expected_result':expected,'observed_result':{'type':type(exc).__name__,'reason':str(exc)[:240]},'result':'FAIL'}
 r.update(source_inventory_sha256=SOURCE_INVENTORY_SHA,evidence_reference='evidence/'+NAME+'#'+id)
 RESULTS.append(r);print(json.dumps(r,sort_keys=True),flush=True)
def reject(fn):
 try:fn()
 except Exception as e:return {'rejected':True,'type':type(e).__name__,'reason':str(e)[:180]}
 raise AssertionError('EXPECTED_FAIL_CLOSED')
def fixture(label,fault='ok',max_output=16*1024*1024):
 x=f.components(c,label+'_'+RUN,fault,max_output)
 x['_fixture_id']={'path':str(x['directory']),'checkpoint_sequence':54,'checkpoint_identity':x['checkpoint'].identity,'frame_path':str(x['frame']),'frame_sha256':n.sha(x['frame'].read_bytes()),'frame_length':x['frame'].stat().st_size,'raw_neutral_input_sha256':n.sha(x['t'].raw_unit_input),'capture_configuration_sha256':x['supervisor'].config_sha256,'frame_file_identity':owner.model_b_frame_identity(x['frame'])}
 return x
def no_child(x,head):
 assert not x['supervisor']._observed and x['supervisor'].timing_receipt().get('child_pid') is None
 assert x['engine'].head.read_bytes()==head and x['engine'].state['units'][11]['attempt_count']==10
 assert not(x['engine'].workspace/'frozen_units/U0012').exists()
def no_orphan(o):
 timing=json.loads(o.timing_receipt);pid=timing['child_pid'];assert type(pid) is int and timing['cleanup_success'] is True
 try:os.kill(pid,0)
 except ProcessLookupError:pass
 else:raise AssertionError('SYNTHETIC_CHILD_NOT_REAPED')
 return {'child_pid':pid,'reaped':True,'cleanup_success':True,'timing_receipt_sha256':n.sha(o.timing_receipt)}
def capture_evidence(x,o):
 p=x['directory'];(p/'captured_stdout.jsonl').write_bytes(o.stdout);(p/'captured_stderr.txt').write_bytes(o.stderr)
 return {'actual_child_execution':True,'actual_program':'ISOLATED_PYTHON_SYNTHETIC_ONLY','exit_code':o.exit_code,'termination':o.termination,'timeout':o.timeout,'truncated':o.truncated,'capture_complete':o.capture_complete,'cleanup_complete':o.cleanup_complete,'stdout_sha256':o.stdout_sha256,'stderr_sha256':o.stderr_sha256,'input_delivery':o.input_delivery,'fixture_identity':x['_fixture_id'],'lifecycle':no_orphan(o)}
def context(x):return ex.ExecutionContext.for_nonproduction(supervisor=x['supervisor'],frame=x['frame'],work_root=x['directory']/'work',stage_root=x['directory']/'stage',durable_root=x['directory']/'durable',historical_attempt_count=10)
def typed_run(ctx):return ex.run_codex_executor(working_directory=ctx.working_directory,prompt=ctx.prompt,codex_path=ctx.codex_path,evidence_root=ctx.evidence_root,role='PRIMARY',execution_context=ctx)
def readback(x):
 p=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/verify_state.py'),x['directory'].name],cwd=n.ROOT,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},capture_output=True,timeout=20)
 assert p.returncode==0,p.stderr.decode();return json.loads(p.stdout)
def typed_tests():
 import typed_contract_fixtures as tf
 gold=tf.a11_fixture()
 def verify(doc,gold=gold):
  raw=pub.canonical(doc);return owner.verify_real_document_bindings(doc,target=gold['target_authorization'],execution_binding=gold['execution_binding'],expected_sha=n.sha(raw),expected_length=len(raw))
 check('T01_PURE_A11_SHAPE','typed','STATIC_IN_MEMORY_SYNTHETIC_CONTRACT','Schema and independent target/effects comparison pass without authority',lambda:{'validated':bool(verify(gold)),'synthetic_target_sha256':n.sha(pub.canonical(gold['target_authorization'])),'synthetic_effects_sha256':n.sha(pub.canonical(gold['execution_binding'])),'REAL_artifact_created':False})
 for name,mutate in [('target',lambda d:d['target_authorization'].update(attempt_id='SYNTHETIC_CHANGED')),('checkpoint',lambda d:d['target_authorization'].update(checkpoint_identity='f'*64)),('effect',lambda d:d['execution_binding']['effects']['runtime'].update(input_sha256='f'*64)),('source',lambda d:d['target_authorization']['base_deployment_configuration']['selected_source_sha256'].update(synthetic_component='f'*64)),('configuration',lambda d:d['target_authorization']['base_deployment_configuration'].update(detached_pin_sha256='f'*64)),('ordinal',lambda d:d['target_authorization'].update(next_attempt_sequence=12))]:
  def wrong(mutate=mutate):
   doc=copy.deepcopy(gold);mutate(doc);tf.refresh(doc);return reject(lambda:verify(doc))
  check('T02_WRONG_'+name.upper(),'typed','STATIC_IN_MEMORY_SYNTHETIC_CONTRACT','Incorrect independently expected identity rejected',wrong)
 x=fixture('typed_static');ctx=context(x)
 def static():
  facts=ex.verify_runtime_context(ctx,working_directory=ctx.working_directory,prompt=ctx.prompt,codex_path=ctx.codex_path,evidence_root=ctx.evidence_root,role='PRIMARY')
  assert facts['historical_attempt_count']==10 and facts['next_attempt_sequence']==11 and facts['frame_path']==str(x['frame']) and facts['frame_length']==x['frame'].stat().st_size
  rb=FutureRealUnitBinding('BATCH0004','PRIMARY','U0012','SYNTHETIC_TYPED_ONLY',n.sha(b'synthetic-checkpoint'),n.sha(b'synthetic-frame'),'REAL',n.sha(b'synthetic-mode'),tuple(range(1776,1801)),tuple(n.sha(str(i).encode()) for i in range(25)),1);assert rb.verify() is rb
  return {'fixture_identity':x['_fixture_id'],'ExecutionContext_STATIC':'PASS','FutureRealUnitBinding_value_validation':'PASS','context_sha256':facts['context_identity'],'no_REAL_authority':True}
 check('T03_TYPED_STATIC_CONTEXT','typed','STATIC_TYPED_SYNTHETIC_OBJECTS','Typed context seals exact file identity and A0011 destination',static)
 def alias():
  other=x['directory']/'typed_alias.json';other.write_bytes(x['frame'].read_bytes());ctx.frame=other
  try:return reject(lambda:ex.verify_runtime_context(ctx))
  finally:ctx.frame=x['frame']
 check('T04_TYPED_PATH_SEAL','typed','STATIC_TYPED_SYNTHETIC_OBJECTS','Same-byte alias path rejected by sealed typed context',alias)
 check('T05_TYPED_EXECUTING_REAL_AUTHORITY_DENIED','typed','STATIC_TYPED_SYNTHETIC_OBJECTS','NP context cannot enter REAL-authority phase',lambda:reject(lambda:ex.verify_runtime_context(ctx,phase='EXECUTING')))
 check('T06_REAL_ACTIVATION_DENIED','typed','STATIC_TYPED_SYNTHETIC_OBJECTS','NP transaction cannot activate REAL',lambda:reject(lambda:activation.production_activation(x['t'])))
 check('T07_REAL_TARGET_CURRENT_FACTS_UNQUALIFIED','typed','STATIC_IN_MEMORY_SYNTHETIC_CONTRACT','Synthetic target rejected by exact-current REAL derivation',lambda:{'rejection':reject(lambda:owner.prospective_a11_target(gold['target_authorization'],expected_configuration_sha256=gold['target_authorization']['deployment_identity'])),'qualification':'UNQUALIFIED__EXACT_CURRENT_REAL_IDENTITIES_AND_AUTHORITY_NOT_SUPPLIED'})
 def actual_typed():
  y=fixture('typed_actual');f.prepare(y);ctx=context(y);facts=ex.verify_runtime_context(ctx);result=typed_run(ctx);o=next(iter(y['supervisor']._observed.values()));diag=f.child_diagnostic(o)
  assert result['return_code']==0 and diag['stdin_bytes']==0 and ctx._used
  manifest=json.loads((ctx.evidence_root/'primary_executor_attempt_manifest.json').read_bytes())
  assert manifest['artifacts']['raw_stdout']['sha256']==o.stdout_sha256
  assert (ctx.evidence_root/'primary_executor_raw_stdout.jsonl').read_bytes()==o.stdout
  replay=reject(lambda:typed_run(ctx))
  (n.ROOT/'evidence/FILE_REPLAY_FIXTURE.json').write_bytes(n.canonical({'fixture':y['directory'].name}))
  return {**capture_evidence(y,o),'typed_executor':'ACTUAL_EXISTING_run_codex_executor_NONPRODUCTION_BRANCH','context_sha256':facts['context_identity'],'fresh_replay_fixture':y['directory'].name,'repeat_rejection':replay,'scientific_acceptance_performed':False}
 check('T08_ACTUAL_TYPED_NP_EXECUTOR','typed','ACTUAL_PYTHON_CHILD_THROUGH_TYPED_NP_EXECUTOR','Existing typed runner executes file-bound child and persists capture exactly',actual_typed)

def transport_tests():
 def positive():
  x=fixture('frame_positive');f.prepare(x);o=f.observe(x);d=f.child_diagnostic(o)
  assert o.exit_code==0 and o.input_delivery=='FILE_IDENTITY_FRAME' and d['stdin_bytes']==0
  assert d['frame_sha256']==x['_fixture_id']['frame_sha256'] and d['frame_length']==x['_fixture_id']['frame_length']
  assert d['file_identity']==x['_fixture_id']['frame_file_identity'] and d['frame_path_sha256']==n.sha(str(x['frame']).encode())
  assert d['cwd']==str(x['supervisor'].cwd) and d['executable']==str(x['supervisor'].executable)
  (x['directory']/'child_frame_diagnostic.json').write_bytes(n.canonical(d))
  assert d['argv']==list(x['supervisor'].argv[3:]), {'actual_argv':d['argv'],'expected_argv':list(x['supervisor'].argv[3:])}
  assert d['environment']==x['supervisor'].env, {'actual_environment':d['environment'],'expected_environment':x['supervisor'].env}
  assert x['_fixture_id']['raw_neutral_input_sha256']!=d['frame_sha256']
  return {**capture_evidence(x,o),'child_frame_diagnostic':d,'raw_input_distinct':True}
 check('F01_ACTUAL_FILE_DELIVERY','file','ACTUAL_PYTHON_CHILD','Exact file path/identity/length/bytes, argv/cwd/env, empty STDIN and distinct raw input',positive)
 for fault in ('alias','content','replace_same_bytes','prelaunch_replace','stdin_fallback','argv','cwd','environment','runtime'):
  def negative(fault=fault):
   x=fixture('frame_'+fault);h=x['engine'].head.read_bytes();f.prepare(x);path=None;hook=None
   if fault=='alias':path=x['directory']/'alias.json';path.write_bytes(x['frame'].read_bytes())
   elif fault=='content':x['frame'].write_bytes(x['frame'].read_bytes()+b' ')
   elif fault in ('replace_same_bytes','prelaunch_replace'):
    def replace():
     other=x['directory']/'new_inode.json';other.write_bytes(x['frame'].read_bytes());os.replace(other,x['frame'])
    if fault=='replace_same_bytes':replace()
    else:hook=replace
   elif fault=='stdin_fallback':x['supervisor'].input_delivery='STDIN'
   elif fault=='argv':x['supervisor'].argv=(*x['supervisor'].argv,'UNAPPROVED')
   elif fault=='cwd':x['supervisor'].cwd=x['directory']
   elif fault=='environment':x['supervisor'].env['PATH']='/synthetic/wrong'
   elif fault=='runtime':x['supervisor']._original_executable_sha='f'*64
   r=reject(lambda:f.observe(x,path,hook));no_child(x,h);return {'rejection':r,'actual_child_execution':False,'fixture_identity':x['_fixture_id']}
  check('F02_REJECT_'+fault.upper(),'file','PRELAUNCH_REJECTION_NO_CHILD','Reject before subprocess without checkpoint or attempt advance',negative)

def authority_tests():
 x=fixture('owner_identity');h=x['engine'].head.read_bytes()
 def approval():
  d,raw,p=f.publish(x);assert p.returncode==0
  receipt=json.loads(p.stdout);assert receipt['owner_pid']==os.getpid() and receipt['publisher_pid']!=os.getpid()
  assert (d/'publication_complete.json').read_bytes()==pub.model_b_completion(n.sha(raw),len(raw))
  f.consume(x,d,raw);assert (d/'consumed.json').read_bytes()==(d/'consumption_complete.json').read_bytes()
  return {'fixture_identity':x['_fixture_id'],'independent_process_approval':receipt,'consumption_sha256':n.sha((d/'consumed.json').read_bytes()),'REAL_authority':False}
 check('A01_OWNER_APPROVAL_PUBLICATION_CONSUMPTION','authority','ACTUAL_NP_OWNER_PUBLISHER_PROCESS','Exact independent-process approval, durable completion, exclusive consumption',approval)
 check('A02_DUPLICATE_CONSUMPTION','authority','NO_CHILD_AUTHORIZATION_REJECTION','Consumed publication cannot be consumed twice',lambda:reject(lambda:f.consume(x,x['directory']/'authority',(x['directory']/'authority/authorization.json').read_bytes())))
 def partial_pub():
  y=fixture('partial_pub');d,raw,p=f.publish(y);assert p.returncode==0;(d/'publication_complete.json').unlink()
  r=reject(lambda:f.consume(y,d,raw));assert not(d/'consumed.json').exists();return {'fixture_identity':y['_fixture_id'],'rejection':r}
 check('A03_PARTIAL_PUBLICATION','authority','NO_CHILD_AUTHORIZATION_REJECTION','Incomplete publication cannot consume',partial_pub)
 def partial_cons():
  y=fixture('partial_cons');h=y['engine'].head.read_bytes();d,raw=f.prepare(y);(d/'consumption_complete.json').unlink()
  r=reject(lambda:f.observe(y));no_child(y,h);return {'fixture_identity':y['_fixture_id'],'rejection':r}
 check('A04_PARTIAL_CONSUMPTION','authority','PRELAUNCH_REJECTION_NO_CHILD','Incomplete consumption cannot launch',partial_cons)
 def missing():
  y=fixture('missing_owner');return {'fixture_identity':y['_fixture_id'],'rejection':reject(lambda:pub.publish_model_b(y['directory']/'missing','f'*64,1,approval_fd=None,directory=y['directory']/'self'))}
 check('A05_MISSING_OWNER_APPROVAL','authority','NO_CHILD_AUTHORIZATION_REJECTION','Executor cannot publish without independent Owner channel',missing)
 def malformed():
  y=fixture('malformed_owner');d,raw,p=f.publish(y,approval=lambda a:{**a,'sha256':'0'*64});assert p.returncode!=0 and not d.exists();return {'fixture_identity':y['_fixture_id'],'publisher_exit':p.returncode}
 check('A06_MALFORMED_OWNER_APPROVAL','authority','ACTUAL_REJECTED_NP_PUBLISHER_PROCESS','Mismatched approval rejected before publication',malformed)
 def self_approve():
  y=fixture('self_owner');raw=n.canonical(f.document(y));candidate=y['directory']/'candidate.json';candidate.write_bytes(raw);candidate.chmod(0o600)
  rd,wr=os.pipe();os.write(wr,n.canonical({'task_id':pub.MODEL_B_TASK,'owner_pid':os.getpid(),'sha256':n.sha(raw),'length':len(raw)}));os.close(wr)
  return {'fixture_identity':y['_fixture_id'],'rejection':reject(lambda:pub.publish_model_b(candidate,n.sha(raw),len(raw),approval_fd=rd,directory=y['directory']/'self'))}
 check('A07_EXECUTOR_SELF_APPROVAL','authority','NO_CHILD_AUTHORIZATION_REJECTION','Same process cannot assert its own independent approval',self_approve)
 for fault in ('target','effects','source','stale'):
  def mismatch(fault=fault):
   y=fixture('authority_'+fault);h=y['engine'].head.read_bytes();doc=f.document(y)
   if fault=='target':doc['target_authorization']['case_sha256']='f'*64;doc['execution_binding']['target_sha256']=n.sha(n.canonical(doc['target_authorization']))
   elif fault=='effects':
    doc['execution_binding']['operational']=copy.deepcopy(doc['execution_binding']['operational'])
    doc['execution_binding']['operational']['stage_root']=str(y['directory']/'wrong_stage')
   elif fault=='source':doc['fixture_binding']['sources']['POLICY_B_POLICY']='f'*64
   d,raw,p=f.publish(y,doc=doc);assert p.returncode==0,p.stderr.decode()
   if fault=='stale':(d/'authorization.json').write_bytes(raw+b' ')
   r=reject(lambda:f.consume(y,d,raw));no_child(y,h);return {'fixture_identity':y['_fixture_id'],'rejection':r}
  check('A08_REJECT_'+fault.upper(),'authority','NO_CHILD_AUTHORIZATION_REJECTION','Independent expected identities or current bytes reject malformed authority',mismatch)
 def claim():
  y=fixture('duplicate_claim');f.prepare(y);owner.verify_model_b_authority(y['supervisor'],claim_launch=True)
  return {'fixture_identity':y['_fixture_id'],'rejection':reject(lambda:owner.verify_model_b_authority(y['supervisor'],claim_launch=True)),'child_launches':0}
 check('A09_DUPLICATE_LAUNCH_CLAIM','authority','NO_CHILD_AUTHORIZATION_REJECTION','Exclusive durable launch claim cannot repeat',claim)

def lifecycle_tests():
 for fault in ('failed','timeout','overflow','stderr','incomplete'):
  def run(fault=fault):
   x=fixture('lifecycle_'+fault,fault,512 if fault=='overflow' else 16*1024*1024);f.prepare(x);ctx=context(x)
   outcome=reject(lambda:typed_run(ctx)) if fault not in ('stderr','incomplete') else typed_run(ctx)
   o=next(iter(x['supervisor']._observed.values()))
   if fault=='failed':assert o.exit_code==7 and o.stdout==b'' and o.stderr==b''
   if fault=='timeout':assert o.timeout and not o.capture_complete
   if fault=='overflow':assert o.limit_exceeded and len(o.stdout)+len(o.stderr)<=512 and not o.capture_complete
   if fault=='stderr':assert o.stderr==b'SYNTHETIC_STDERR_EXACT\n' and o.exit_code==0
   if fault=='incomplete':assert o.exit_code==0
   assert (ctx.evidence_root/'primary_executor_raw_stdout.jsonl').read_bytes()==o.stdout
   assert (ctx.evidence_root/'primary_executor_raw_stderr.txt').read_bytes()==o.stderr
   assert x['engine'].state['units'][11]['attempt_count']==10 and not(x['engine'].workspace/'frozen_units/U0012').exists()
   return {**capture_evidence(x,o),'typed_executor_outcome':{'return_code':outcome['return_code']} if fault in ('stderr','incomplete') else outcome,'scientific_acceptance':False,'acceptance_requires_separate_Policy_B_validation':True}
  check('L01_'+fault.upper(),'lifecycle','ACTUAL_PYTHON_CHILD_THROUGH_TYPED_NP_EXECUTOR','Capture bounded output/status/timing; reap child; preserve raw bytes; no acceptance',run)

def recovery_tests(faults=('ok','equivalent','conflicting','types','position_type','reason_precedence','timeout','incomplete')):
 for fault in faults:
  def run(fault=fault):
   x=fixture('recovery_'+fault,fault);e=x['engine'];old={str(p):n.sha(p.read_bytes()) for p in (e.workspace/'frozen_units').rglob('unit_result.json')}
   d,raw,p=f.publish(x);assert p.returncode==0,p.stderr.decode()
   result=activation.run_model_b_synthetic(n.sha(raw),len(raw),directory=d,transaction=x['t'],executor=x['executor'],proof_path=x['path'],binding=x['binding'],checkpoint=x['checkpoint'],input_path=x['frame'],release_root=n.ROOT,stage_root=x['directory']/'stage')
   o=result['capture'];v=readback(x);assert o is not None and x['executor'].calls==1 and v['attempt_count']==11
   assert old=={p:n.sha(Path(p).read_bytes()) for p in old} and v['U0013_attempt_count']==0
   assert x['t']._executing_checkpoint_sha256 is not None
   if fault in ('ok','equivalent'):
    assert result['outcome']=='FROZEN' and v['checkpoint_sequence']==57 and v['U0012']=='FROZEN'
    assert len(result['receipt'].payload['validated_rows'])==25 and verify_stage(result['stage'])==n.canonical(result['receipt'].payload)
    assert x['path'].consume_count==1
    (x['directory']/'proof.json').write_bytes(n.canonical(dataclasses.asdict(result['proof'])))
   else:
    assert result['outcome']=='CONTROLLED_STOP' and v['U0012']=='PENDING' and v['checkpoint_sequence']==56 and not(e.workspace/'frozen_units/U0012').exists()
    expected={'conflicting':'QUALIFYING_MESSAGE_BYTES_DIFFER','types':'SUCCESS_TERMINAL_SCHEMA','timeout':'CAPTURE_FAIL_CLOSED','incomplete':'MISSING_SUCCESS_OR_RESULT'}
    if fault in expected:assert expected[fault] in x['executor'].capture_failure, x['executor'].capture_failure
    assert 'CLI_LOCAL_ITEM_ID_REQUIRED' not in x['executor'].capture_failure
   replay=reject(lambda:f.observe(x))
   return {**capture_evidence(x,o),'outcome':result['outcome'],'readback':v,'proof_stage_readback':'PASS' if result['proof'] is not None else 'NO_ACCEPTANCE','capture_failure':x['executor'].capture_failure,'frozen_predecessors_preserved':275,'retry_rejected':replay,'receipt_identity':None if result['receipt'] is None else result['receipt'].identity,'policy_b_message_count':None if result['receipt'] is None else result['receipt'].claims['message_count']}
  check('R01_'+fault.upper(),'recovery','ACTUAL_FILE_CHILD_AND_EXISTING_RECOVERY','Existing Policy B/schema/semantic/proof rules enforce success-only freeze and failed-attempt accounting',run)

def regression_tests():
 def file_tamper():
  x=fixture('file_proof_regression');head=x['engine'].head.read_bytes();f.prepare(x);o=f.observe(x)
  stage,proof,receipt=x['path'].issue(capture=o,input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,stage_root=x['directory']/'stage',binding=x['binding'],checkpoint=x['checkpoint'])
  from real_candidate.policy_b_proof_v1 import proof_hash
  claims=copy.deepcopy(proof.claims);claims['CONTEXT']['input_sha256']='f'*64
  forged=type(proof)(claims,proof_hash(claims))
  a=reject(lambda:x['path'].verify_proof(forged,receipt,phase='STAGED',stage=stage))
  data=stage.file.read_bytes();stage.file.chmod(0o600);stage.file.write_bytes(data+b' ')
  b=reject(lambda:x['path'].verify_prepared())
  assert head==x['engine'].head.read_bytes() and x['engine'].state['units'][11]['attempt_count']==10
  return {**capture_evidence(x,o),'forged_proof_rejection':a,'stage_tamper_rejection':b,'operational_dispatch_not_reached':True}
 check('G01_FILE_PROOF_AND_READBACK_TAMPER','regression','ACTUAL_FILE_CHILD_EXISTING_SCIENTIFIC_PROOF','Existing proof reconstruction and staging reject tampering under FILE transport',file_tamper)
 def stdin_smoke():
  x=n.components(c,'stdin_compatibility_'+RUN);head=x['engine'].head.read_bytes();f.prepare(x);o=f.observe(x)
  assert o.exit_code==0 and o.input_delivery=='STDIN' and x['engine'].head.read_bytes()==head
  return {'actual_child_execution':True,'input_delivery':'STDIN','frame_sha256':n.sha(x['frame'].read_bytes()),'capture_configuration_sha256':x['supervisor'].config_sha256,'fixture_path':str(x['directory']),'lifecycle':no_orphan(o),'scientific_acceptance':False}
 check('G02_STDIN_CONDITIONAL_FIELD_REGRESSION','regression','ACTUAL_STDIN_CHILD','Conditional FILE identity fields preserve original NP STDIN capture contract',stdin_smoke)

mode=sys.argv[1] if len(sys.argv)>1 else ''
NAMES={'--typed':'TYPED_CONTRACT_RESULTS.json','--file':'FILE_TRANSPORT_RESULTS.json','--authority':'AUTHORITY_RESULTS.json','--lifecycle':'LIFECYCLE_RESULTS.json','--recovery':'RECOVERY_RESULTS.json','--recovery-timeout':'RECOVERY_TIMEOUT_REGRESSION.json','--regression':'FOCUSED_REGRESSION_RESULTS.json'}
NAME=NAMES.get(mode)
if NAME is None:raise SystemExit('Choose a bounded suite')
{'--typed':typed_tests,'--file':transport_tests,'--authority':authority_tests,'--lifecycle':lifecycle_tests,'--recovery':recovery_tests,'--recovery-timeout':lambda:recovery_tests(('timeout',)),'--regression':regression_tests}[mode]()
value={'classification':'CODEX_REPORTED','passed':sum(r['result']=='PASS' for r in RESULTS),'total':len(RESULTS),'results':RESULTS,'source_identities':SOURCE_IDS,'source_inventory_sha256':SOURCE_INVENTORY_SHA,'audit':n.AUDIT,'REAL_activation':'HARD_DISABLED'}
(n.ROOT/'evidence'/NAME).write_bytes(n.canonical(value))
raise SystemExit(0 if value['passed']==value['total'] else 1)
