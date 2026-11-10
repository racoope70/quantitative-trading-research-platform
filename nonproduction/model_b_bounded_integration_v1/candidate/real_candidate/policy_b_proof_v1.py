"""Explicit Policy B proof/consumer; separate from Policy A and Owner authority.

REAL contexts use the existing attestor and exact Owner readback/consumption
checks. The explicit synthetic branch uses the accepted synthetic engine only.
No checkpoint writer, process launcher, publication or consumption API is added.
"""
from dataclasses import dataclass,asdict
from pathlib import Path
import copy,json
from trusted_stage import staging_v1 as s
from .capture_v1 import ControlledLocalCapture
from .validation_v1 import BoundAcceptedValidator
from .checkpoint_v1 import PersistedCheckpointAttestor
from .proof_path_v1 import BoundProofPath
from .policy_b_validation_v1 import PolicyBScientificValidator
from .release_v1 import verify_release,MANIFEST_FILE
from . import proof_issuer_v1 as policy_a
import availability_classifier_v7_prospective as v7

VERSION='BATCH0004_POLICY_B_INTEGRITY_PROOF_V1_SHA256'
FIELDS={'PROOF_VERSION','PROOF_PHASE','POLICY_SHA256','POLICY_B_RECEIPT','BINDING','CONTEXT',
        'CAPTURE_NONCE','COMMON_RESULT_SHA256','VALIDATED_PAYLOAD_SHA256','EXPECTED_STAGE_SHA256',
        'STAGED_BYTES_SHA256','READBACK_SHA256','STAGED_FILE_SIZE','PRESTAGE_PROOF_SHA256',
        'SOURCE_SHA256','EXECUTION_MODE'}

@dataclass(frozen=True,slots=True)
class PolicyBProof:
    claims: dict
    proof_sha256: str

@dataclass(frozen=True,slots=True)
class PolicyBPredecessor:
    identity: str
    sequence: int
    snapshot_sha256: str
    head_sha256: str

def source_sha():return s.sha(s.safe_read(Path(__file__)))
def proof_hash(claims):return s.sha(VERSION.encode()+b'\0'+s.canonical(claims))

class PolicyBProofPath:
    def __init__(self,*,supervisor,validator,release_root,checkpoint_attestor=None,synthetic_engine=None):
        s.require(type(supervisor) is ControlledLocalCapture and type(validator) is BoundAcceptedValidator and
                  validator.supervisor is supervisor,'POLICY_B_EXACT_COMPONENTS_REQUIRED')
        self.supervisor,self.validator=supervisor,validator
        self.release_root=Path(release_root);self.release_identity=verify_release(self.release_root)
        self.checkpoint_attestor=checkpoint_attestor;self.synthetic_engine=synthetic_engine
        if supervisor.mode=='REAL':
            s.require(type(checkpoint_attestor) is PersistedCheckpointAttestor and synthetic_engine is None,
                      'POLICY_B_REAL_OWNER_ATTESTOR_REQUIRED')
            descriptor=json.loads(s.safe_read(self.release_root/MANIFEST_FILE))
            s.require(supervisor.adapter_sha256==descriptor['prospective_components']['EXECUTOR_INTERFACE']['sha256'],
                      'POLICY_B_REAL_ADAPTER_IDENTITY')
        else:
            import checkpoint_resume_activation_trusted_v1 as core
            s.require(supervisor.mode=='NONPRODUCTION_TEST' and supervisor._allow_test and
                      type(synthetic_engine) is core.CheckpointEngine and not hasattr(synthetic_engine,'real_source') and
                      checkpoint_attestor is None and
                      synthetic_engine.verify().state['attempt_identity'].startswith('SYNTHETIC_POLICY_B_') and
                      (synthetic_engine.input_hashes['neutral_semantic_evidence.jsonl']==
                        '61d687a415611aa75db955485db36e90e70b0fae2b2cdd10518c6a3659c1f496' or
                       (Path(__file__).resolve()==Path('/private/tmp/QTRP_MODEL_B_A11_REAL_CONTRACT_NONPRODUCTION_QUALIFICATION_V1/candidate/real_candidate/policy_b_proof_v1.py')
                        and synthetic_engine.state['attempt_identity'].startswith('SYNTHETIC_POLICY_B_MODEL_B_')
                        and synthetic_engine.evidence==validator._read_sources()[1])),
                      'POLICY_B_EXACT_SYNTHETIC_CONTEXT_REQUIRED')
        self.issuer=self;self.issuer_source_sha256=source_sha()
        self.transaction=None;self.binding=None;self.predecessor=None;self.frame=None
        self._adapter=None;self._candidate=None;self._consumed=False;self.consume_count=0

    def _fresh_sources(self):
        s.require(source_sha()==self.issuer_source_sha256,'POLICY_B_PROOF_SOURCE_DRIFT')
        return BoundProofPath._fresh_sources(self)

    def bind_recovery(self,t,binding,checkpoint,frame,input_sha):
        import recovery_two_attempt_v3 as r
        s.require(type(t) is r.ControlledStopRecovery and self.transaction is None and
                  type(binding) is (s.UnitBinding if self.synthetic_engine is not None else
                    __import__('real_candidate.real_binding_v1',fromlist=['FutureRealUnitBinding']).FutureRealUnitBinding),
                  'POLICY_B_EXACT_RECOVERY_BINDING_REQUIRED')
        s.require(binding.unit_input_sha256==input_sha and binding.attempt_id==t.case['attempt_id'] and
                  binding.checkpoint_identity==checkpoint.identity==t.case['checkpoint_manifest_sha256'],
                  'POLICY_B_EXACT_PREDECESSOR_REQUIRED')
        self.transaction,self.binding,self.predecessor,self.frame=t,binding,checkpoint,Path(frame)
        if self.synthetic_engine is not None:
            s.require(t.engine is self.synthetic_engine and type(checkpoint) is PolicyBPredecessor and
                      binding.execution_mode=='SYNTHETIC_NONPRODUCTION' and t._real_owner_context is None and
                      t.case['real_execution_authorized'] is False,'POLICY_B_NP_CANNOT_GRANT_REAL_AUTHORITY')
            self._head=s.safe_read(t.engine.head)
            self._snapshot=s.safe_read(t._original_stopped_checkpoint_path)
        self.configuration_bytes()

    def configuration_bytes(self):
        s.require(self.binding is not None and self.transaction is not None,'POLICY_B_NOT_BOUND')
        self.binding.verify();self.supervisor._fresh();sources=self._fresh_sources()
        rows=self.validator.module.unit_evidence(*self.validator._read_sources()[:2],'U0012')
        s.require(s.safe_read(self.frame)==s.canonical(rows) and s.sha(s.safe_read(self.frame))==self.binding.unit_input_sha256 and
                  self.binding.mode_binding_sha256==self.supervisor.config_sha256 and
                  self.binding.expected_identities==tuple(r['canonical_source_identity'] for r in rows),
                  'POLICY_B_INPUT_RUNTIME_CONFIGURATION_DRIFT')
        return s.canonical({'proof_domain':VERSION,'release':self.release_identity,'sources':sources,
            'binding':asdict(self.binding),'frame':str(self.frame),'supervisor':self.supervisor.config_sha256,
            'predecessor':self.predecessor.identity,'checkpoint_root':str(self.transaction.engine.root)})

    def snapshot_for_recovery(self,t,binding,checkpoint,frame,input_sha):
        s.require(self.transaction is t and self.binding==binding and self.predecessor is checkpoint and
                  self.frame==Path(frame) and binding.unit_input_sha256==input_sha,'POLICY_B_COMPONENT_SUBSTITUTION')
        if self.synthetic_engine is not None:
            s.require(type(checkpoint) is PolicyBPredecessor and t.engine is self.synthetic_engine and
                      s.safe_read(t._original_stopped_checkpoint_path)==self._snapshot and
                      s.sha(self._snapshot)==checkpoint.snapshot_sha256 and s.sha(self._head)==checkpoint.head_sha256 and
                      json.loads(self._snapshot)['checkpoint_manifest_sha256']==checkpoint.identity and
                      json.loads(self._snapshot)['checkpoint_sequence']==checkpoint.sequence and
                      json.loads(self._head)['snapshot_file_sha256']==checkpoint.snapshot_sha256,
                      'POLICY_B_CHECKPOINT_PREDECESSOR_CONFLICT')
        return s.canonical({'configuration':json.loads(self.configuration_bytes()),'case':t.case,
            'journal':str(t.journal),'journal_sha256':t._authorized_event_sha256,
            'mode_binding_sha256':t._bound_mode_sha256})

    def _check_checkpoint(self,checkpoint):
        s.require(checkpoint is self.predecessor,'POLICY_B_CHECKPOINT_SUBSTITUTED')
        t=self.transaction
        if self.synthetic_engine is not None:
            self.snapshot_for_recovery(t,self.binding,checkpoint,self.frame,self.binding.unit_input_sha256)
            if t._dispatched:t._fresh_pre_dispatch_guard()
            else:t._fresh_pre_mutation_guard()
        else:
            s.require(self.checkpoint_attestor.verify_receipt(checkpoint),'POLICY_B_CHECKPOINT_STALE')
            t._fresh_pre_dispatch_guard()

    def _context(self,capture):
        self._check_checkpoint(self.predecessor)
        b=self.binding;t=self.transaction
        context={'batch':b.batch_id,'role':b.role,'unit':b.unit_id,'attempt':b.attempt_id,
            'checkpoint':b.checkpoint_identity,'mode':b.execution_mode,'max_new_units':1,'u0013_prohibited':True,
            'input_sha256':b.unit_input_sha256,'runtime_sha256':capture.executable_sha256,
            'configuration_sha256':self.supervisor.config_sha256,'invocation_id':capture.invocation_id,
            'recovery_binding_sha256':t.binding_hash,'recovery_journal_sha256':t._authorized_event_sha256,
            'checkpoint_root':str(t.engine.root),'release_sha256':self.release_identity}
        if self.synthetic_engine is not None:
            s.require(t._real_owner_context is None and self.supervisor.mode=='NONPRODUCTION_TEST',
                      'POLICY_B_UNAUTHORIZED_REAL_AUTHORITY')
            context.update(authorization_domain='SYNTHETIC_ONLY_NO_OWNER_AUTHORITY',
                           attempt_ordinal=len(t._historical_attempts)+1)
            if getattr(t,'_model_b_owner_context',None) is not None:
                import owner_authorization as owner
                context.update(owner.verify_model_b_authority(self.supervisor))
        else:
            # Existing exact consumed Owner publication and phase checks, before stage.
            transaction,consumed,doc,owner_pin,consumption_pin=BoundProofPath._trusted_policy_b_authority(
                self,capture,b,self.predecessor,self.frame)
            import owner_authorization as owner
            context.update(authorization={'sha256':owner_pin,'consumption_sha256':consumption_pin,
                'length':consumed['authorization_length'],'consumer_uid':doc['consumer_uid'],'scope':doc['scope']},
                recovery=transaction,runtime=owner.execution_facts(doc)['runtime'],
                attempt_ordinal=transaction['attempt_ordinal'])
        return context

    def common_text(self,capture):
        from . import policy_b_events_v1 as events
        self.supervisor.verify(capture,input_file=self.frame,pinned_input_sha256=self.binding.unit_input_sha256)
        # No authority is inferred from this extraction; scientific receipt/proof
        # independently re-derive the same complete occurrence set.
        b=self.binding
        context={'batch':b.batch_id,'role':b.role,'unit':b.unit_id,'attempt':b.attempt_id,'checkpoint':b.checkpoint_identity,
            'mode':b.execution_mode,'max_new_units':1,'u0013_prohibited':True,'input_sha256':b.unit_input_sha256,
            'runtime_sha256':capture.executable_sha256,'configuration_sha256':capture.config_sha256}
        return events.inspect_envelope(capture.stdout,expected_context=context,
            frozen_extract=self.validator.module.v3.parse_codex_json_events).common_result.decode('utf8')

    def _expected(self,receipt,phase,stage=None):
        s.require(phase in ('PRESTAGE','STAGED') and self._adapter is not None,'POLICY_B_PROOF_PHASE')
        s.require(type(self._adapter) is PolicyBScientificValidator and
                  self._adapter.validator is self.validator and self._adapter.supervisor is self.supervisor and
                  self._adapter.binding is self.binding and self._adapter.frame==self.frame and
                  self._adapter.capture is receipt.capture,'POLICY_B_SCIENTIFIC_ADAPTER_SUBSTITUTED')
        claims,payload=self._adapter.verify(receipt)
        # Consumer expectations come from its own bound recovery/Owner context,
        # independently of even an origin-sealed submitted receipt.
        s.require(s.canonical(claims['execution'])==s.canonical(self._context(receipt.capture)) and
                  s.canonical(claims['source_identities'])==s.canonical(self._fresh_sources()),
                  'POLICY_B_RECEIPT_CONTEXT_OR_SOURCE_SUBSTITUTION')
        derived,checked,common=self._adapter.reconstruct()
        s.require(s.canonical(claims)==s.canonical(derived) and s.canonical(payload)==s.canonical(checked),
                  'POLICY_B_SCIENTIFIC_RECONSTRUCTION_MISMATCH')
        raw=s.canonical(payload);expected=s.sha(raw);o=receipt.capture
        result=self.result(o)
        if phase=='PRESTAGE':
            s.require(stage is None,'POLICY_B_PRESTAGE_READBACK_FORBIDDEN');observed=None
        else:
            s.require(type(stage) is s.StagedArtifact and stage.binding==self.binding and
                      stage.file==self._stage_root/'staging/U0012'/(self.binding.attempt_id+'.json'),
                      'POLICY_B_STAGE_IDENTITY_MISMATCH')
            observed=s.verify_stage(stage)
            s.require(observed==raw and stage.staged_bytes_sha256==stage.readback_sha256==expected,
                      'POLICY_B_STAGE_READBACK_MISMATCH')
            policy_a._expected_auxiliary_source(result,observed_rows=25)
        trusted=claims['execution']
        value={'PROOF_VERSION':VERSION,'PROOF_PHASE':phase,'POLICY_SHA256':self._fresh_sources()['POLICY_B_POLICY'],
            'POLICY_B_RECEIPT':{'identity':receipt.identity,'claims':claims},'BINDING':asdict(self.binding),
            'CONTEXT':trusted,'CAPTURE_NONCE':o.invocation_id,'COMMON_RESULT_SHA256':s.sha(common),
            'VALIDATED_PAYLOAD_SHA256':receipt.validated_output_sha256,'EXPECTED_STAGE_SHA256':expected,
            'STAGED_BYTES_SHA256':s.sha(observed) if observed is not None else None,
            'READBACK_SHA256':s.sha(observed) if observed is not None else None,
            'STAGED_FILE_SIZE':len(observed) if observed is not None else None,'PRESTAGE_PROOF_SHA256':None,
            'SOURCE_SHA256':source_sha(),'EXECUTION_MODE':self.binding.execution_mode}
        if phase=='STAGED':value['PRESTAGE_PROOF_SHA256']=proof_hash(self._expected(receipt,'PRESTAGE'))
        s.require(set(value)==FIELDS,'POLICY_B_INTERNAL_FIELD_SET');return value

    def verify_proof(self,proof,receipt,*,phase,stage=None):
        s.require(type(proof) is PolicyBProof and type(proof.claims) is dict and set(proof.claims)==FIELDS and
                  proof.claims['PROOF_VERSION']==VERSION,'POLICY_B_PROOF_TYPE_DOMAIN_FIELDS')
        s.require(proof.proof_sha256==proof_hash(proof.claims),'POLICY_B_PROOF_HASH')
        s.require(s.canonical(proof.claims)==s.canonical(self._expected(receipt,phase,stage)),
                  'POLICY_B_PROOF_INDEPENDENT_RECONSTRUCTION_MISMATCH');return True

    def issue(self,*,capture,input_path,input_sha256,stage_root,binding,checkpoint):
        s.require(not self._consumed and self._candidate is None and binding is self.binding and
                  Path(input_path)==self.frame and input_sha256==binding.unit_input_sha256,
                  'POLICY_B_STALE_OR_UNBOUND_ISSUANCE')
        self._check_checkpoint(checkpoint);self._fresh_sources()
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=input_sha256)
        s.require(len([x for x in capture.stderr.decode('utf8').splitlines() if x.strip()])<=1,
                  'UNKNOWN_OR_CONFLICTING_STDERR')
        # _context REAL uses the unchanged scientific receipt interface checks;
        # scientific receipt issuance itself must finish before authority evidence.
        self._active_receipt=None
        self._adapter=PolicyBScientificValidator(validator=self.validator,capture=capture,binding=binding,
            frame=self.frame,context_provider=lambda:self._context(capture),source_provider=self._fresh_sources)
        receipt=self._adapter.issue();self._active_receipt=receipt
        if self.supervisor.mode=='REAL':
            from .executor_v1 import serialization_size
            maximum=self.transaction._bound_adapter.execution_context.storage_contract()['artifact_bytes']
            serialization_size(receipt.payload,maximum,ensure_ascii=False,indent=None,separators=(',',':'))
        self._stage_root=Path(stage_root)
        preliminary=PolicyBProof(self._expected(receipt,'PRESTAGE'),'')
        preliminary=PolicyBProof(preliminary.claims,proof_hash(preliminary.claims))
        self.verify_proof(preliminary,receipt,phase='PRESTAGE')
        stage=s.stage_validated_payload(stage_root,binding,receipt.payload)
        proof=PolicyBProof(self._expected(receipt,'STAGED',stage),'')
        proof=PolicyBProof(proof.claims,proof_hash(proof.claims))
        self.verify_proof(proof,receipt,phase='STAGED',stage=stage)
        self._candidate=(capture,stage,proof,receipt);self.preliminary=preliminary
        return stage,proof,receipt

    def verify_prepared(self):
        s.require(not self._consumed and type(self._candidate) is tuple,'POLICY_B_MISSING_OR_CONSUMED_PROOF')
        o,stage,proof,receipt=self._candidate
        self._check_checkpoint(self.predecessor)
        s.require(o is receipt.capture and self._adapter.capture is o,'POLICY_B_CAPTURE_SUBSTITUTED')
        self.verify_proof(proof,receipt,phase='STAGED',stage=stage);return True

    def result(self,o):
        return {'process_started':True,'return_code':o.exit_code,'termination_state':o.termination,'timeout_status':o.timeout,
            'context_id':o.invocation_id,'agent_message':self.common_text(o),'raw_stdout':o.stdout.decode('utf8'),
            'raw_stderr':o.stderr.decode('utf8'),'stdout_sha256':o.stdout_sha256,'stderr_sha256':o.stderr_sha256,
            'raw_output_sha256':o.raw_output_sha256,'executor_sha256':o.executable_sha256,
            'config_sha256':o.config_sha256,'capture_source_sha256':o.capture_source_sha256}

    def qualify_prospective_only(self,*,capture,input_path,input_sha256,stage,proof,receipt,binding,checkpoint):
        s.require(not self._consumed and binding is self.binding and checkpoint is self.predecessor and
                  (capture,stage,proof,receipt)==self._candidate and Path(input_path)==self.frame and
                  input_sha256==binding.unit_input_sha256,'POLICY_B_RECOVERY_REPLAY_OR_SUBSTITUTION')
        self.verify_prepared()
        result=self.result(capture)
        integrity=v7.VerifiedOperationalIntegrity(25,25,True,True,True,True,True,capture.timeout,
            capture.execution_exception,capture.truncated,capture.local_transport_interruption,False,True)
        verdict=v7.decide_availability(result,integrity=integrity)
        s.require(verdict['decision']=='NO_EXTERNAL_SIGNAL' and not verdict['hard_stop_classes'] and
                  not verdict['conflict_evidence'] and
                  (verdict['operational_classification']=='NORMAL_SUCCESS' or verdict['auxiliary_diagnostic_nonblocking']),
                  'POLICY_B_OPERATIONAL_QUALIFICATION_REJECTED')
        self._check_checkpoint(checkpoint);self._consumed=True;self.consume_count+=1;return verdict

class PolicyBCapturedFixtureExecutor:
    """Explicit NONPRODUCTION capture-forwarder; cannot pair with a REAL engine."""
    def __init__(self,path):
        s.require(type(path) is PolicyBProofPath and path.synthetic_engine is not None,
                  'POLICY_B_FIXTURE_REQUIRES_SYNTHETIC_ENGINE')
        self.path=path;self.calls=0;self._capture_request=None;self.capture_failure=None
    def configure_capture(self,*,binding,checkpoint,input_path,stage_root):
        import owner_publication as publication
        publication.model_b_root(input_path);publication.model_b_root(stage_root)
        request=(binding,checkpoint,Path(input_path),Path(stage_root))
        s.require(self.calls==0 and (self._capture_request is None or self._capture_request==request),
                  'MODEL_B_CAPTURE_REQUEST_SUBSTITUTION')
        self._capture_request=request
    def verify_capture_request(self):
        s.require(type(self._capture_request) is tuple and self.path._candidate is None
                  and self.calls==0 and not self.path.supervisor._observed,
                  'MODEL_B_CAPTURE_ALREADY_USED_OR_UNCONFIGURED')
        b,cp,frame,stage=self._capture_request
        s.require(b is self.path.binding and cp is self.path.predecessor and frame==self.path.frame
                  and stage==self.path.transaction.engine.root.parent/'stage',
                  'MODEL_B_CAPTURE_REQUEST_DRIFT')
        self.path._check_checkpoint(cp);self.path.configuration_bytes()
        return True
    def configuration_bytes(self):
        self.path.supervisor._fresh();sources=self.path._fresh_sources()
        return s.canonical({'domain':'SYNTHETIC_POLICY_B_CAPTURE_FORWARDING_ONLY',
            'supervisor':self.path.supervisor.config_sha256,'engine_root':str(self.path.synthetic_engine.root),
            'release':self.path.release_identity,'sources':sources})
    def execute(self,role,unit_id,input_rows,attempt_no,prior_contexts):
        t=self.path.transaction
        s.require(self.calls==0 and role=='PRIMARY' and unit_id=='U0012' and
                  attempt_no==len(t._historical_attempts)+1 and s.canonical(input_rows)==s.safe_read(self.path.frame),
                  'POLICY_B_FIXTURE_EXACT_ONE_UNIT_ONLY')
        if self._capture_request is not None:
            self.verify_capture_request()
            b,cp,frame,stage_root=self._capture_request
            from prospective_adapter_v1 import prospective_attempt_layout
            prospective_attempt_layout(history=t._historical_attempts,
                checkpoint_identity=cp.identity,expected_checkpoint_identity=t.case['checkpoint_manifest_sha256'],
                checkpoint_sequence=cp.sequence,work_root=self.path.supervisor.cwd.parents[3],
                unit_id=unit_id,attempt_no=attempt_no,working_directory=self.path.supervisor.cwd)
            o=self.path.supervisor.observe(input_file=frame,pinned_input_sha256=b.unit_input_sha256,
                timeout_seconds=self.path.supervisor.child_capture_budget_seconds,test_only=True)
            self.calls+=1
            try:
                self.path.issue(capture=o,input_path=frame,input_sha256=b.unit_input_sha256,
                    stage_root=stage_root,binding=b,checkpoint=cp)
            except Exception as exc:
                # Forward failed operational facts for existing attempt accounting.
                # A missing proof can never accept or freeze a scientific result.
                self.capture_failure=type(exc).__name__+':'+str(exc)
                return {'process_started':True,'return_code':o.exit_code,'termination_state':o.termination,
                    'timeout_status':o.timeout,'context_id':o.invocation_id,'agent_message':'',
                    'raw_stdout':o.stdout.decode('utf8',errors='replace'),
                    'raw_stderr':o.stderr.decode('utf8',errors='replace'),
                    'stdout_sha256':o.stdout_sha256,'stderr_sha256':o.stderr_sha256,
                    'raw_output_sha256':o.raw_output_sha256,'executor_sha256':o.executable_sha256,
                    'config_sha256':o.config_sha256,'capture_source_sha256':o.capture_source_sha256,
                    'validation_failure':True,'synthetic_only':True,'provenance_mode':'SYNTHETIC',
                    'codex_subprocess_started':False,'real_codex_subprocess_started':False}
        self.path.verify_prepared();o,stage,proof,receipt=self.path._candidate
        s.require(o.invocation_id not in prior_contexts,'POLICY_B_FIXTURE_STALE_CONTEXT')
        t._fresh_pre_dispatch_guard()
        if self._capture_request is None:self.calls+=1
        t.submit_v7_evidence(o,stage,proof,receipt)
        return {**self.path.result(o),'synthetic_only':True,'provenance_mode':'SYNTHETIC',
                'codex_subprocess_started':False,'real_codex_subprocess_started':False}
