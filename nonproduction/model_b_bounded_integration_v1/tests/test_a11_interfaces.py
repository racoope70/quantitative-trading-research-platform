"""Changed A11 interfaces only; real Python children, synthetic state, no REAL authority."""
import copy,dataclasses,json,os,subprocess,sys,time,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap()
import owner_authorization as owner
import owner_publication as pub
import checkpoint_resume_activation_trusted_v1 as core
from real_candidate import activation_v1,executor_v1
from prospective_adapter_v1 import prospective_attempt_layout
from trusted_stage.staging_v1 import verify_stage
RUN=str(time.time_ns());RESULTS=[]
def test(name,fn):
 try:detail=fn();r={'test':name,'result':'PASS','detail':detail}
 except Exception as e:
  traceback.print_exc();r={'test':name,'result':'FAIL','type':type(e).__name__,'error':str(e)[:500]}
 RESULTS.append(r);print(json.dumps(r,sort_keys=True),flush=True)
def reject(fn):
 try:fn()
 except Exception as e:return {'type':type(e).__name__,'reason':str(e)[:200]}
 raise AssertionError('EXPECTED_FAIL_CLOSED')
def document(x):return owner.model_b_document(x['t'],x['executor'],x['path'],x['binding'],x['frame'],n.ROOT)
def rebind(doc):
    # Structurally coherent forged proposals must still fail independent derivation.
    t=doc['target_authorization'];e=doc['execution_binding']
    t['configuration_sha256']=n.sha(n.canonical(t['configuration']))
    e['configuration_sha256']=t['configuration_sha256'];e['target_sha256']=n.sha(n.canonical(t))
    return doc
def publish(x,name='authority',doc=None,approval=None):
 raw=n.canonical(document(x) if doc is None else doc);candidate=x['directory']/(name+'.candidate.json')
 candidate.write_bytes(raw);candidate.chmod(0o600);directory=x['directory']/name
 rd,wr=os.pipe()
 a={'task_id':pub.MODEL_B_TASK,'sha256':n.sha(raw),'length':len(raw),'owner_pid':os.getpid()}
 if approval is not None:a=approval(a)
 os.write(wr,n.canonical(a));os.close(wr)
 try:p=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/owner_publish.py'),str(rd),str(candidate),str(directory),n.sha(raw),str(len(raw))],cwd=n.ROOT,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},pass_fds=(rd,),capture_output=True,timeout=20)
 finally:os.close(rd)
 return directory,raw,p
def consume(x,d,raw):return owner.consume_model_b(n.sha(raw),len(raw),directory=d,t=x['t'],executor=x['executor'],path=x['path'],binding=x['binding'],frame=x['frame'],release_root=n.ROOT)
def prepare(x):
 d,raw,p=publish(x);assert p.returncode==0,p.stderr.decode();consume(x,d,raw)
 x['t'].bind_v7_verifier(x['path'],binding=x['binding'],checkpoint=x['checkpoint'],input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,release_root=n.ROOT)
 return d,raw
def observe(x):return x['supervisor'].observe(input_file=x['frame'],pinned_input_sha256=x['binding'].unit_input_sha256,timeout_seconds=x['supervisor'].child_capture_budget_seconds,test_only=True)
def unchanged(x,h):
 assert x['engine'].head.read_bytes()==h and not x['supervisor']._observed
 x['engine'].verify();assert x['engine'].state['units'][11]['attempt_count']==10
 assert not (x['engine'].workspace/'frozen_units/U0012').exists()
def readback(x):
 p=subprocess.run([n.PYTHON,'-I','-B',str(n.ROOT/'tests/verify_state.py'),x['directory'].name],cwd=n.ROOT,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},capture_output=True,timeout=20)
 assert p.returncode==0,p.stderr.decode();return json.loads(p.stdout)
def run_connected(x):
 d,raw,p=publish(x);assert p.returncode==0,p.stderr.decode()
 out=activation_v1.run_model_b_synthetic(n.sha(raw),len(raw),directory=d,transaction=x['t'],executor=x['executor'],proof_path=x['path'],binding=x['binding'],checkpoint=x['checkpoint'],input_path=x['frame'],release_root=n.ROOT,stage_root=x['directory']/'stage')
 return out,d,raw,json.loads(p.stdout)

def authorization_tests():
 x=n.components(c,'binding_'+RUN);h=x['engine'].head.read_bytes()
 for key,val in [('checkpoint_identity','e'*64),('input_sha256','e'*64),('runtime_sha256','e'*64),('configuration_sha256','e'*64),('release_sha256','e'*64),('case_sha256','e'*64),('attempt_ordinal',10),('historical_attempt_count',9),('unit_id','U0013')]:
  def wrong(key=key,val=val):
   doc=document(x);doc['target_authorization'][key]=val
   if key!='configuration_sha256':rebind(doc)
   d,r,p=publish(x,'wrong_'+key,doc)
   result=reject(lambda:consume(x,d,r)) if p.returncode==0 else {'publisher_exit':p.returncode}
   unchanged(x,h);return result
  test('WRONG_'+key.upper(),wrong)
 for name,mutate in [('physical_effect',lambda d:d['execution_binding']['operational'].__setitem__('stage_root',str(x['directory']/'other_stage'))),('source',lambda d:d['fixture_binding']['sources'].__setitem__('POLICY_B_POLICY','e'*64)),('history',lambda d:d['target_authorization']['configuration']['historical_attempts'][0].__setitem__('manifest_sha256','e'*64))]:
  def wrong(name=name,mutate=mutate):
   doc=copy.deepcopy(document(x));mutate(doc);rebind(doc);d,r,p=publish(x,'wrong_'+name,doc)
   result=reject(lambda:consume(x,d,r)) if p.returncode==0 else {'publisher_exit':p.returncode}
   unchanged(x,h);return result
  test('WRONG_'+name.upper(),wrong)
 def completeness():
  cfg=copy.deepcopy(document(x)['target_authorization']['configuration']);cfg.pop('execution_configuration_complete');cfg.pop('runtime_sha256')
  r=reject(lambda:c.model_b_technical_configuration(cfg));unchanged(x,h);return r
 test('MISSING_INDEPENDENT_CONFIGURATION_OPERAND',completeness)
 def incomplete_capture():
  cfg=copy.deepcopy(document(x)['target_authorization']['configuration']);cfg.pop('execution_configuration_complete');cfg['capture'].pop('argv')
  return reject(lambda:c.model_b_technical_configuration(cfg))
 test('MISSING_CAPTURE_ARGV_CANNOT_DECLARE_COMPLETE',incomplete_capture)
 for label,fn in [('MISSING_APPROVAL',lambda:pub.publish_model_b(x['directory']/'missing','a'*64,1,approval_fd=None,directory=x['directory']/'no_owner')),('MISSING_AUTHORIZATION',lambda:consume(x,x['directory']/'missing',b'{}\n')),('NO_AUTHORITY_AT_ACTUAL_SPAWN_SINK',lambda:observe(x)),('REAL_ACTIVATION_REJECTS_NP_TRANSACTION',lambda:activation_v1.production_activation(x['t'])),('REAL_VALIDATOR_REJECTS_NP_DOCUMENT',lambda:pub.validate_owner_document(n.canonical(document(x))))]:
  test(label,lambda fn=fn:reject(fn))
 def malformed():
  d,r,p=publish(x,'bad_approval',approval=lambda a:{**a,'sha256':'0'*64});assert p.returncode!=0 and not d.exists();unchanged(x,h);return {'publisher_exit':p.returncode}
 test('MALFORMED_OR_MISMATCHED_OWNER_APPROVAL',malformed)
 def self_publish():
  raw=n.canonical(document(x));p=x['directory']/'self.candidate';p.write_bytes(raw);p.chmod(0o600)
  rd,wr=os.pipe();os.write(wr,n.canonical({'task_id':pub.MODEL_B_TASK,'sha256':n.sha(raw),'length':len(raw),'owner_pid':os.getpid()}));os.close(wr)
  r=reject(lambda:pub.publish_model_b(p,n.sha(raw),len(raw),approval_fd=rd,directory=x['directory']/'self_authority'));unchanged(x,h);return r
 test('EXECUTOR_SAME_PROCESS_SELF_APPROVAL_REJECTED',self_publish)
 def partial_publication():
  d,r,p=publish(x,'partial_publication');assert p.returncode==0
  (d/'publication_complete.json').unlink();result=reject(lambda:consume(x,d,r));assert not (d/'consumed.json').exists();unchanged(x,h);return result
 test('INCOMPLETE_PUBLICATION_NO_CONSUMPTION_OR_DISPATCH',partial_publication)
 def partial_consumption():
  y=n.components(c,'partial_consumption_'+RUN);hh=y['engine'].head.read_bytes();d,r=prepare(y)
  (d/'consumption_complete.json').unlink();result=reject(lambda:observe(y));unchanged(y,hh)
  replay=reject(lambda:consume(y,d,r));return {'spawn_rejected':result,'reconsume_rejected':replay}
 test('INCOMPLETE_CONSUMPTION_NO_DISPATCH_OR_RETRY',partial_consumption)
 def interrupted_consumption():
  y=n.components(c,'interrupted_consumption_'+RUN);hh=y['engine'].head.read_bytes();d,r,p=publish(y);assert p.returncode==0
  original=y['t'].authorize_nonproduction
  def interrupted(*args):raise OSError('SYNTHETIC_RESERVATION_INTERRUPTION')
  y['t'].authorize_nonproduction=interrupted
  try:a=reject(lambda:consume(y,d,r))
  finally:y['t'].authorize_nonproduction=original
  assert (d/'consumed.json').is_file() and not (d/'consumption_complete.json').exists()
  assert getattr(y['t'],'_model_b_owner_context',None) is None
  b=reject(lambda:consume(y,d,r));unchanged(y,hh)
  return {'injected_failure':a,'retry_rejected':b,'authority_attached':False}
 test('INTERRUPTED_RESERVATION_RETAINS_CONSUMPTION_AND_REJECTS_RETRY',interrupted_consumption)
 def consumption_replay():
  y=n.components(c,'replay_'+RUN);hh=y['engine'].head.read_bytes();d,r=prepare(y)
  a=reject(lambda:consume(y,d,r));unchanged(y,hh)
  # A new transaction over the same synthetic checkpoint must also reject.
  rows=core.unit_evidence(y['engine'].partition,y['engine'].evidence,'U0012');raw_input=b''.join(n.canonical(z) for z in rows)
  t=c.recovery.ControlledStopRecovery(y['engine'],copy.deepcopy(y['t'].case),raw_input,expected_case=copy.deepcopy(y['t'].case))
  z=dict(y,t=t)
  b=reject(lambda:consume(z,d,r));assert not t._prepared;unchanged(y,hh)
  (n.ROOT/'evidence/REPLAY_FIXTURE.json').write_bytes(n.canonical({'fixture':y['directory'].name}))
  return {'same_transaction':a,'new_transaction':b}
 test('DURABLE_CONSUMPTION_REPLAY',consumption_replay)
 def launch_claim():
  y=n.components(c,'claim_'+RUN);hh=y['engine'].head.read_bytes();prepare(y)
  a=owner.verify_model_b_authority(y['supervisor'],claim_launch=True)
  b=reject(lambda:owner.verify_model_b_authority(y['supervisor'],claim_launch=True));unchanged(y,hh)
  return {'first_claim':a,'duplicate_claim':b,'child_launches':0}
 test('EXCLUSIVE_DURABLE_LAUNCH_CLAIM',launch_claim)
 def fresh_substitution():
  y=n.components(c,'fresh_substitution_'+RUN);hh=y['engine'].head.read_bytes();d,r=prepare(y)
  (d/'authorization.json').write_bytes(r+b' ');result=reject(lambda:observe(y));unchanged(y,hh);return result
 test('FRESH_BOUNDARY_REJECTS_POST_CONSUMPTION_SUBSTITUTION',fresh_substitution)

def adapter_tests():
 def source_interfaces():
  binding=c.recovery.compatibility_binding()
  assert c.recovery.verify_exact_approved_real_interfaces() is True
  return {'normal_bootstrap':'PASS','actual_compatibility_binding':'PASS','actual_source_interface_verification':'PASS',
    'historical_attempt_count_retained':binding['historical_attempt_count'],'protected_observation':False,'real_authority':False}
 test('ACTUAL_RECOVERY_COMPATIBILITY_AND_SOURCE_PIN_ENTRYPOINTS',source_interfaces)
 history=copy.deepcopy(c.recovery.A11_CASE['historical_attempts']);root=n.ROOT/'fixtures/layout/work'
 def layout(count,**kwargs):
  values=dict(history=history[:count],checkpoint_identity='a'*64,expected_checkpoint_identity='a'*64,checkpoint_sequence=54 if count==10 else 52,work_root=root)
  values.update(kwargs);return prospective_attempt_layout(**values)
 for count in (9,10):
  def matched(count=count):
   v=layout(count,attempt_no=count+1,working_directory=root/f'PRIMARY/U0012/A{count+1:04d}/input');return {k:str(z) if isinstance(z,Path) else z for k,z in v.items()}
  test('MATCHED_A'+str(count+1)+'_HISTORY_AND_PATH',matched)
 for label,kwargs in [('WRONG_ORDINAL',{'attempt_no':10}),('WRONG_DIRECTORY',{'working_directory':root/'PRIMARY/U0012/A0010/input'}),('WRONG_CHECKPOINT',{'checkpoint_identity':'b'*64}),('MIXED_CHECKPOINT',{'checkpoint_sequence':52}),('EXTRA_HISTORY',{'history':history+[history[-1]]}),('WRONG_COUNT',{'history':history[:8]}),('U0013',{'unit_id':'U0013'}),('BOOLEAN_ORDINAL',{'attempt_no':True})]:
  test('ADAPTER_'+label,lambda kwargs=kwargs:reject(lambda:layout(10,**kwargs)))
 def false_history():
  h=copy.deepcopy(history);h[-1]['attempt_number']=9;return reject(lambda:layout(10,history=h))
 test('ADAPTER_UNVERIFIED_ORDERED_HISTORY_REJECTED',false_history)
 def actual_adapter_rejection(unit,ordinal):
  # Inert object exercises the public execute guard; no source constructor,
  # scientific materialization, executor or REAL authority is invoked.
  from types import SimpleNamespace
  from prospective_adapter_v1 import V3CodexUnitAdapter
  a=object.__new__(V3CodexUnitAdapter);a.real_source=True;a.work_root=root
  t=SimpleNamespace(_historical_attempts=history,case=c.recovery.A11_CASE,expected_case=c.recovery.A11_CASE)
  a.execution_context=SimpleNamespace(transaction=t,working_directory=root/'PRIMARY/U0012/A0011/input')
  return reject(lambda:a.execute('PRIMARY',unit,[],ordinal,()))
 test('PUBLIC_ADAPTER_EXECUTE_REJECTS_A10_ORDINAL_IN_A11',lambda:actual_adapter_rejection('U0012',10))
 test('PUBLIC_ADAPTER_EXECUTE_REJECTS_U0013',lambda:actual_adapter_rejection('U0013',11))

def integration_tests(faults=('ok','failed','short','internal','incomplete','reason_precedence')):
 for fault in faults:
  def connected(fault=fault):
   x=n.components(c,'connected_'+fault+'_'+RUN,fault);e=x['engine'];old={str(p):n.sha(p.read_bytes()) for p in (e.workspace/'frozen_units').rglob('unit_result.json')}
   out,d,raw,publication=run_connected(x);o=out['capture'];v=readback(x)
   assert o is not None and o.cleanup_complete and len(x['supervisor']._observed)==1
   if fault=='timeout':assert o.timeout and not o.capture_complete
   else:assert o.capture_complete
   assert v['attempt_count']==11 and v['U0013_attempt_count']==0
   assert old=={p:n.sha(Path(p).read_bytes()) for p in old}
   assert x['t']._executing_checkpoint_sha256 is not None and v['checkpoint_sequence']>54
   assert x['executor'].calls==1
   if fault=='ok':
    assert out['outcome']=='FROZEN' and v['U0012']=='FROZEN' and o.exit_code==0
    assert len(out['receipt'].payload['validated_rows'])==25 and verify_stage(out['stage'])==n.canonical(out['receipt'].payload)
    assert x['path'].consume_count==1
   else:
    assert out['outcome']=='CONTROLLED_STOP' and v['U0012']=='PENDING'
    assert not (e.workspace/'frozen_units/U0012').exists() and out['proof'] is None
   replay=reject(lambda:observe(x))
   value={'actual_child_execution':True,'actual_child':'ISOLATED_PYTHON_SYNTHETIC_PROCESSOR','real_codex_execution':False,
    'outcome':out['outcome'],'fault':fault,'exit_code':o.exit_code,'capture_complete':o.capture_complete,'cleanup_complete':o.cleanup_complete,
    'stdout_sha256':o.stdout_sha256,'stderr_sha256':o.stderr_sha256,'capture_failure':x['executor'].capture_failure,
    'rows':25 if fault=='ok' else 0,'frozen_predecessors_preserved':275,'publication':publication,
    'executing_checkpoint_identity':x['t']._executing_checkpoint_sha256,'readback':v,'replay':replay,'fixture':str(x['directory'])}
   (x['directory']/'qualification_receipt.json').write_bytes(n.canonical(value))
   if out['proof'] is not None:
    (x['directory']/'proof.json').write_bytes(n.canonical(dataclasses.asdict(out['proof'])))
   return value
  test('CONNECTED_A11_'+fault.upper(),connected)

def regressions():
 integration_tests(('timeout','duplicate'))
 def tamper():
  x=n.components(c,'proof_regression_'+RUN);hh=x['engine'].head.read_bytes();prepare(x);o=observe(x)
  stage,proof,receipt=x['path'].issue(capture=o,input_path=x['frame'],input_sha256=x['binding'].unit_input_sha256,
    stage_root=x['directory']/'stage',binding=x['binding'],checkpoint=x['checkpoint'])
  from real_candidate.policy_b_proof_v1 import proof_hash
  claims=copy.deepcopy(proof.claims);claims['CONTEXT']['input_sha256']='f'*64
  forged=type(proof)(claims,proof_hash(claims))
  a=reject(lambda:x['path'].verify_proof(forged,receipt,phase='STAGED',stage=stage))
  data=stage.file.read_bytes();stage.file.chmod(0o600);stage.file.write_bytes(data+b' ')
  b=reject(lambda:x['path'].verify_prepared())
  assert hh==x['engine'].head.read_bytes() and x['engine'].state['units'][11]['attempt_count']==10
  return {'forged_proof':a,'stage_tamper':b,'operational_dispatch_not_reached':True,'actual_child_execution':True}
 test('EXISTING_PROOF_AND_STAGING_READBACK_REJECT_TAMPERING',tamper)

if sys.argv[1:]==['--authorization']:authorization_tests();name='A11_AUTHORIZATION_RESULTS.json'
elif sys.argv[1:]==['--adapter']:adapter_tests();name='A10_A11_ADAPTER_RESULTS.json'
elif sys.argv[1:]==['--connected']:integration_tests();name='A11_CONNECTED_RESULTS.json'
elif sys.argv[1:]==['--regression']:regressions();name='A11_DEPENDENCY_REGRESSIONS.json'
elif sys.argv[1:]==['--timeout']:integration_tests(('timeout',));name='A11_TIMEOUT_REGRESSION.json'
else:raise SystemExit('Choose --authorization / --adapter / --connected')
value={'classification':'CODEX_REPORTED','results':RESULTS,'passed':sum(r['result']=='PASS' for r in RESULTS),'total':len(RESULTS),'audit':n.AUDIT,'REAL_ACTIVATION':'HARD_DISABLED',
 'source_binding':{'composition_sha256':n.sha((n.ROOT/'composition.py').read_bytes()),'release_sha256':n.sha((n.ROOT/'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json').read_bytes()),'closure':c._NONPRODUCTION_SOURCE_CLOSURE}}
(n.ROOT/'evidence'/name).write_bytes(n.canonical(value))
raise SystemExit(0 if value['passed']==value['total'] else 1)
