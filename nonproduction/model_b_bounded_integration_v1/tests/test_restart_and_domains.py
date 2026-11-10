"""Fresh consumed-authority replay and unchanged REAL-domain rejection checks."""
import copy,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap()
import owner_authorization as owner
import owner_publication as publication
import checkpoint_resume_activation_trusted_v1 as core
from real_candidate.capture_v1 import ControlledLocalCapture
from real_candidate.validation_v1 import BoundAcceptedValidator
from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBCapturedFixtureExecutor,PolicyBPredecessor
from trusted_stage.staging_v1 import UnitBinding
results=[]
def reject(label,fn):
    try:fn()
    except Exception as exc:results.append({'test':label,'result':'PASS','rejection':type(exc).__name__,'reason':str(exc)[:180]});return
    raise AssertionError(label+'_UNEXPECTEDLY_ACCEPTED')

# Use the latest actual incomplete-child fixture; no new scientific processing.
fixture=sorted((n.ROOT/'fixtures').glob('incomplete_*'))[-1]
raw=(fixture/'authority/authorization.json').read_bytes();doc=publication.validate_model_b_document(raw)
reject('MODEL_B_DOCUMENT_REJECTED_BY_EXISTING_REAL_INERT_PUBLICATION_VALIDATOR',lambda:publication.validate_owner_document(raw))
candidate=fixture/'authority.candidate.json'
rd,wr=os.pipe();os.write(wr,n.canonical({'task_id':publication.MODEL_B_TASK,
    'sha256':n.sha(raw),'length':len(raw),'owner_pid':os.getpid()}));os.close(wr)
reject('SAME_EXECUTOR_PROCESS_CANNOT_APPROVE_ITS_OWN_PUBLICATION',lambda:publication.publish_model_b(candidate,n.sha(raw),len(raw),approval_fd=rd,directory=fixture/'self_publication'))
assert not (fixture/'self_publication').exists()
engine=core.CheckpointEngine(fixture/'state','PRIMARY');engine.verify()
head=engine.head.read_bytes()
before={p.relative_to(fixture).as_posix():n.sha(p.read_bytes()) for p in fixture.rglob('*') if p.is_file()}
rows=core.unit_evidence(engine.partition,engine.evidence,'U0012');source= n.ROOT/'candidate/dependencies/synthetic_fixture'
case=c.recovery.synthetic_case(engine,b''.join(n.canonical(r) for r in rows))
t=c.recovery.ControlledStopRecovery(engine,copy.deepcopy(case),b''.join(n.canonical(r) for r in rows),expected_case=copy.deepcopy(case))
cfg=doc['fixture_binding']['capture_configuration']
supervisor=ControlledLocalCapture(executable=Path(cfg['executable']),executable_sha256=doc['target_authorization']['runtime_sha256'],
    argv=tuple(cfg['argv']),cwd=Path(cfg['cwd']),env=cfg['env'],adapter_sha256=cfg['adapter_sha256'],
    mode='NONPRODUCTION_TEST',allow_test_fixture=True,
    prelaunch_budget_seconds=cfg['timeout_policy']['prelaunch_budget_seconds'],
    child_capture_budget_seconds=cfg['timeout_policy']['post_popen_capture_budget_seconds'])
validator=BoundAcceptedValidator(accepted_root=n.ROOT/'accepted',supervisor=supervisor,
    partition_path=source/'partition.json',evidence_path=source/'evidence.json',reason_path=source/'reason_normalized.json',
    partition_sha256=n.sha((source/'partition.json').read_bytes()),evidence_sha256=n.sha((source/'evidence.json').read_bytes()),reason_sha256=n.sha((source/'reason_normalized.json').read_bytes()))
path=PolicyBProofPath(supervisor=supervisor,validator=validator,release_root=n.ROOT,synthetic_engine=engine)
binding=UnitBinding('BATCH0004','PRIMARY','U0012',case['attempt_id'],case['checkpoint_manifest_sha256'],
    n.sha((fixture/'frame.json').read_bytes()),'SYNTHETIC_NONPRODUCTION',supervisor.config_sha256,
    tuple(range(1776,1801)),tuple(r['canonical_source_identity'] for r in rows))
executor=PolicyBCapturedFixtureExecutor(path)
assert n.canonical(owner.model_b_document(t,executor,path,binding,fixture/'frame.json',n.ROOT))==raw
reject('FRESH_PROCESS_CONSUMED_AUTHORITY_REPLAY',lambda:owner.consume_model_b(n.sha(raw),len(raw),directory=fixture/'authority',
    t=t,executor=executor,path=path,binding=binding,frame=fixture/'frame.json',release_root=n.ROOT))
assert getattr(t,'_model_b_owner_context',None) is None
assert not t._prepared and not t._dispatched and not supervisor._observed
assert head==engine.head.read_bytes()
after={p.relative_to(fixture).as_posix():n.sha(p.read_bytes()) for p in fixture.rglob('*') if p.is_file()}
assert before==after
value={'classification':'CODEX_REPORTED','results':results,'passed':len(results),'total':len(results),
    'child_launches':0,'checkpoint_and_all_fixture_bytes_unchanged':True,'audit':n.AUDIT}
(n.ROOT/'evidence/FRESH_RESTART_AND_DOMAIN_REGRESSION.json').write_bytes(n.canonical(value))
print(json.dumps(value,indent=2))
