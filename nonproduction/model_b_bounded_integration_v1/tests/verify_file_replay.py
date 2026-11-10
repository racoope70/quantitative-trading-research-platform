"""Fresh interpreter: existing consumed NP publication never re-arms recovery."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap()
import owner_authorization as owner
import owner_publication as pub
import checkpoint_resume_activation_trusted_v1 as core
from real_candidate.capture_v1 import ControlledLocalCapture
from real_candidate.validation_v1 import BoundAcceptedValidator
from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBCapturedFixtureExecutor
from trusted_stage.staging_v1 import UnitBinding
fixture=n.ROOT/'fixtures'/json.loads((n.ROOT/'evidence/FILE_REPLAY_FIXTURE.json').read_bytes())['fixture']
before={str(p):n.sha(p.read_bytes()) for p in fixture.rglob('*') if p.is_file()}
raw=(fixture/'authority/authorization.json').read_bytes();doc=pub.validate_model_b_document(raw)
engine=core.CheckpointEngine(fixture/'state','PRIMARY');engine.verify()
rows=core.unit_evidence(engine.partition,engine.evidence,'U0012');unit_raw=b''.join(n.canonical(r) for r in rows)
case=c.recovery.synthetic_case(engine,unit_raw)
t=c.recovery.ControlledStopRecovery(engine,copy.deepcopy(case),unit_raw,expected_case=copy.deepcopy(case))
cfg=doc['fixture_binding']['capture_configuration'];source=n.ROOT/'candidate/dependencies/synthetic_fixture'
supervisor=ControlledLocalCapture(executable=Path(cfg['executable']),executable_sha256=doc['target_authorization']['runtime_sha256'],argv=tuple(cfg['argv']),cwd=Path(cfg['cwd']),env=cfg['env'],adapter_sha256=cfg['adapter_sha256'],mode='NONPRODUCTION_TEST',allow_test_fixture=True,input_delivery=cfg['input_delivery'],max_output_bytes=cfg['max_output_bytes'],prelaunch_budget_seconds=cfg['timeout_policy']['prelaunch_budget_seconds'],child_capture_budget_seconds=cfg['timeout_policy']['post_popen_capture_budget_seconds'])
validator=BoundAcceptedValidator(accepted_root=n.ROOT/'accepted',supervisor=supervisor,partition_path=source/'partition.json',evidence_path=source/'evidence.json',reason_path=source/'reason_normalized.json',partition_sha256=n.sha((source/'partition.json').read_bytes()),evidence_sha256=n.sha((source/'evidence.json').read_bytes()),reason_sha256=n.sha((source/'reason_normalized.json').read_bytes()))
path=PolicyBProofPath(supervisor=supervisor,validator=validator,release_root=n.ROOT,synthetic_engine=engine)
binding=UnitBinding('BATCH0004','PRIMARY','U0012',case['attempt_id'],case['checkpoint_manifest_sha256'],n.sha((fixture/'frame.json').read_bytes()),'SYNTHETIC_NONPRODUCTION',supervisor.config_sha256,tuple(range(1776,1801)),tuple(r['canonical_source_identity'] for r in rows),1)
executor=PolicyBCapturedFixtureExecutor(path)
assert n.canonical(owner.model_b_document(t,executor,path,binding,fixture/'frame.json',n.ROOT))==raw
try:owner.consume_model_b(n.sha(raw),len(raw),directory=fixture/'authority',t=t,executor=executor,path=path,binding=binding,frame=fixture/'frame.json',release_root=n.ROOT)
except FileExistsError as e:reason=type(e).__name__
else:raise AssertionError('FRESH_REPLAY_NOT_REJECTED')
assert getattr(t,'_model_b_owner_context',None) is None and not t._prepared and not t._dispatched and not supervisor._observed
assert before=={str(p):n.sha(p.read_bytes()) for p in fixture.rglob('*') if p.is_file()}
result={'classification':'CODEX_REPORTED','test':'FRESH_PROCESS_FILE_CONSUMED_REPLAY','result':'PASS','rejection':reason,'child_launches':0,'input_delivery':supervisor.input_delivery,'fixture_identity':{'path':str(fixture),'authorization_sha256':n.sha(raw),'frame_sha256':n.sha((fixture/'frame.json').read_bytes())},'all_fixture_bytes_preserved':True,'audit':n.AUDIT,
 'source_binding':{'composition_sha256':n.sha((n.ROOT/'composition.py').read_bytes()),'release_sha256':n.sha((n.ROOT/'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json').read_bytes()),'closure':c._NONPRODUCTION_SOURCE_CLOSURE}}
(n.ROOT/'evidence/FILE_FRESH_PROCESS_REPLAY.json').write_bytes(n.canonical(result));print(json.dumps(result))
