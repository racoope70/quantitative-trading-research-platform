"""Trusted composition: captured facts -> accepted validation -> staging -> proof.

The versioned canonical record is independently reconstructed from trusted
observations. Its content SHA-256 never establishes Owner authority.
This component is not a REAL dispatcher and never mutates checkpoints.
"""
from __future__ import annotations
from pathlib import Path
from trusted_stage.staging_v1 import require,StageStop,sha,stage_validated_payload,verify_stage,UnitBinding
from real_candidate.capture_v1 import ControlledLocalCapture,LocalObservation
from real_candidate.validation_v1 import BoundAcceptedValidator
from real_candidate import proof_issuer_v1 as trusted_issuer
from real_candidate.checkpoint_v1 import PersistedCheckpointAttestor,CheckpointAttestation
import availability_classifier_v7_prospective as v7
from real_candidate.release_v1 import verify_release,PINNED_ACCEPTED,MANIFEST_FILE

class BoundProofPath:
    def __init__(self, *, supervisor:ControlledLocalCapture, validator:BoundAcceptedValidator,
                 checkpoint_attestor:PersistedCheckpointAttestor,
                 release_root:Path):
        require(type(supervisor) is ControlledLocalCapture and type(validator) is BoundAcceptedValidator and
                validator.supervisor is supervisor and
                type(checkpoint_attestor) is PersistedCheckpointAttestor, 'UNTRUSTED_INTEGRATION_INTERFACE')
        self.release_identity=verify_release(release_root)
        if supervisor.mode=='REAL':
            require(supervisor.adapter_sha256==__import__('json').loads((Path(release_root)/MANIFEST_FILE).read_bytes())['prospective_components']['EXECUTOR_INTERFACE']['sha256'],
                    'UNAPPROVED_REAL_ADAPTER_IDENTITY')
        self.supervisor=supervisor;self.validator=validator
        self.release_root=Path(release_root)
        self.checkpoint_attestor=checkpoint_attestor
        self.issuer=trusted_issuer.TrustedIssuer(pinned_issuer_source_sha256=trusted_issuer.source_sha())

    def issue(self, *, capture:LocalObservation,input_path:Path,input_sha256:str,stage_root:Path,
              binding:UnitBinding,checkpoint:CheckpointAttestation):
        require(self.checkpoint_attestor.verify_receipt(checkpoint),'CHECKPOINT_DRIFT')
        require(binding.checkpoint_identity==checkpoint.identity and binding.unit_id=='U0012' and
                binding.max_new_units==1, 'ISSUER_WRONG_CHECKPOINT_OR_UNIT')
        require((binding.execution_mode=='REAL' and capture.mode=='REAL') or
                (binding.execution_mode=='SYNTHETIC_NONPRODUCTION' and capture.mode=='NONPRODUCTION_TEST'),
                'PROOF_EXECUTION_MODE_MISMATCH')
        self._fresh_sources()
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=input_sha256)
        require(capture.exit_code==0 and capture.termination=='NORMAL_SUCCESS' and
                not (capture.timeout or capture.truncated or capture.execution_exception or capture.local_transport_interruption),
                'OPERATIONAL_FAILURE')
        try:
            lines=[line for line in capture.stderr.decode('utf8',errors='strict').splitlines()
                   if line.strip()]
        except UnicodeDecodeError as ex:
            raise StageStop('UNDECODABLE_STDERR') from ex
        # Ordinary success need not emit the exceptional diagnostic. Keep the
        # one-nonblank-diagnostic bound; accepted V7 classification below binds
        # any auxiliary claim after scientific validation and exact readback.
        require(len(lines)<=1,'UNKNOWN_OR_CONFLICTING_STDERR')
        receipt=self.validator.validate(capture,input_path=input_path,input_sha256=input_sha256)
        self.validator.verify_receipt(receipt,capture)
        require(binding.unit_input_sha256==receipt.actual_input_sha256 and
                binding.expected_identities==tuple(row['canonical_source_identity'] for row in
                                                   self.validator.module.unit_evidence(*self.validator._read_sources()[:2],'U0012')),
                'BOUND_ACTUAL_S04_INPUT_MISMATCH')
        if self.supervisor.mode=='REAL':
            from real_candidate.executor_v1 import serialization_size
            transaction=self.checkpoint_attestor._recovery_phase[0]
            maximum=transaction._bound_adapter.execution_context.storage_contract()['artifact_bytes']
            serialization_size(receipt.payload,maximum,ensure_ascii=False,indent=None,separators=(',',':'))
        stage=stage_validated_payload(stage_root,binding,receipt.payload)
        require(verify_stage(stage)==stage.file.read_bytes(),'NONACCEPTING_STAGE_VERIFICATION_FAILED')
        self.validator.verify_receipt(receipt,capture)  # reject post-validation mutation before recording
        result={'process_started':True,'return_code':capture.exit_code,
                'termination_state':capture.termination,'timeout_status':capture.timeout,
                'context_id':capture.invocation_id,'raw_stdout':capture.stdout.decode('utf8'),
                'raw_stderr':capture.stderr.decode('utf8'),
                'agent_message':self.validator._agent_message(capture),
                'stdout_sha256':capture.stdout_sha256,'stderr_sha256':capture.stderr_sha256,
                'raw_output_sha256':capture.raw_output_sha256,
                'executor_sha256':capture.executable_sha256,'config_sha256':capture.config_sha256,
                'capture_source_sha256':capture.capture_source_sha256}
        evidence=self._trusted_evidence(capture,receipt,stage,binding,checkpoint,input_path)
        proof=self.issuer.issue(stage,binding=binding,result=result,capture_nonce=capture.invocation_id,
                trusted_evidence=evidence)
        require(self.checkpoint_attestor.verify_receipt(checkpoint),'CHECKPOINT_DRIFT_AFTER_RECORDING')
        require(trusted_issuer.verify_proof(proof,pinned_issuer_sha256=trusted_issuer.source_sha(),
                binding=binding,stage=stage,result=result,capture_nonce=capture.invocation_id,
                trusted_evidence=self._trusted_evidence(capture,receipt,stage,binding,checkpoint,input_path)),
                'PROOF_CHECK_FAILED')
        return stage,proof,receipt

    def qualify_prospective_only(self, *, capture:LocalObservation, input_path:Path, input_sha256:str,
                                stage,proof,receipt,binding:UnitBinding,checkpoint:CheckpointAttestation):
        """Existing V7 V2 prospective verdict AFTER proof verification; never freezes."""
        require((binding.execution_mode=='REAL' and capture.mode=='REAL') or
                (binding.execution_mode=='SYNTHETIC_NONPRODUCTION' and capture.mode=='NONPRODUCTION_TEST'),
                'PROOF_EXECUTION_MODE_MISMATCH')
        self._fresh_sources()
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=input_sha256)
        require(self.checkpoint_attestor.verify_receipt(checkpoint),'CHECKPOINT_CHANGED_PRE_V7')
        self.validator.verify_receipt(receipt,capture)
        require(binding.unit_input_sha256==receipt.actual_input_sha256 and
                stage.binding==binding and verify_stage(stage)==stage.file.read_bytes(),
                'UNTRUSTED_STAGING_PRE_V7')
        result={'process_started':True,'return_code':capture.exit_code,
                'termination_state':capture.termination,'timeout_status':capture.timeout,
                'context_id':capture.invocation_id,'raw_stdout':capture.stdout.decode('utf8'),
                'raw_stderr':capture.stderr.decode('utf8'),
                'agent_message':self.validator._agent_message(capture),
                'stdout_sha256':capture.stdout_sha256,'stderr_sha256':capture.stderr_sha256,
                'raw_output_sha256':capture.raw_output_sha256,
                'executor_sha256':capture.executable_sha256,'config_sha256':capture.config_sha256,
                'capture_source_sha256':capture.capture_source_sha256}
        require(trusted_issuer.verify_proof(proof,pinned_issuer_sha256=trusted_issuer.source_sha(),
                binding=binding,stage=stage,result=result,capture_nonce=capture.invocation_id,
                trusted_evidence=self._trusted_evidence(capture,receipt,stage,binding,checkpoint,input_path)),
                'HASH_BOUND_PROOF_NOT_VERIFIED')
        integ=v7.VerifiedOperationalIntegrity(expected_rows=25,observed_rows=len(receipt.payload['validated_rows']),
                complete_output=True,output_schema_valid=True,identities_valid=True,positions_valid=True,
                serialization_readback_pass=True,semantic_subprocess_timeout=capture.timeout,
                semantic_execution_exception=capture.execution_exception,output_truncation=capture.truncated,
                transport_interruption=capture.local_transport_interruption,external_availability_present=False,
                # LOCAL diagnostic attestation only; never provider-internal provenance.
                source_attested=True)
        verdict=v7.decide_availability(result,integrity=integ)
        require(verdict['decision']=='NO_EXTERNAL_SIGNAL' and
                verdict['conflict_evidence']==[] and verdict['hard_stop_classes']==[] and
                ((verdict['classification']=='NONBLOCKING_AUXILIARY_EXECUTOR_DIAGNOSTIC' and
                  verdict['auxiliary_diagnostic_nonblocking'] is True) or
                 (verdict['classification']=='NONE' and
                  verdict['operational_classification']=='NORMAL_SUCCESS' and
                  verdict['auxiliary_diagnostic_nonblocking'] is False)),
                'V7_V2_PROSPECTIVE_FAILURE')
        return verdict

    def _fresh_sources(self):
        import json
        from real_candidate import (capture_v1,checkpoint_v1,proof_issuer_v1,activation_v1,
            real_binding_v1,validation_v1,release_v1,proof_path_v1,executor_v1,engine_v1)
        require(verify_release(self.release_root)==self.release_identity,'PROOF_RELEASE_IDENTITY_DRIFT')
        descriptor=json.loads((self.release_root/MANIFEST_FILE).read_bytes())
        sources={}
        for name,module in (('CAPTURE_V1',capture_v1),('CHECKPOINT_V1',checkpoint_v1),
                ('PROOF_ISSUER_V1',proof_issuer_v1),('ACTIVATION_V1',activation_v1),
                ('REAL_BINDING_V1',real_binding_v1),('VALIDATION_V1',validation_v1),
                ('RELEASE_V1',release_v1),('PROOF_PATH_V1',proof_path_v1),
                ('EXECUTOR_V1',executor_v1),('ENGINE_V1',engine_v1),
                *[(n,__import__('real_candidate.'+f,fromlist=[f])) for n,f in
                  [('POLICY_B_EVENTS_V1','policy_b_events_v1'),('POLICY_B_VALIDATION_V1','policy_b_validation_v1'),
                   ('POLICY_B_PROOF_V1','policy_b_proof_v1')]]):
            item=descriptor['new_integration_components'][name];pin=item['sha256']
            require(Path(module.__file__).resolve()==(self.release_root/item['path']).resolve()
                    and sha(Path(module.__file__).read_bytes())==pin,'LOADED_PROOF_SOURCE_IDENTITY_DRIFT__'+name)
            sources[name]=pin
        import prospective_adapter_v1
        import recovery_two_attempt_v3 as recovery
        for key,module in [('EXECUTOR_INTERFACE',prospective_adapter_v1),('RECOVERY',recovery)]:
            item=descriptor['prospective_components'][key]
            require(Path(module.__file__).resolve()==(self.release_root/item['path']).resolve() and
                    sha(Path(module.__file__).read_bytes())==item['sha256'],'LOADED_PROSPECTIVE_SOURCE_DRIFT__'+key)
            sources[key]=item['sha256']
        item=descriptor['prospective_components']['RECOVERY_COMPATIBILITY']
        require(sha((self.release_root/item['path']).read_bytes())==item['sha256'],'PROSPECTIVE_COMPATIBILITY_DRIFT')
        sources['RECOVERY_COMPATIBILITY']=item['sha256']
        import trusted_stage.staging_v1 as staging
        import availability_classifier_v7_prospective as classifier
        for name,module in [('STAGING_READBACK',staging),('V7_V2_CLASSIFIER',classifier)]:
            pin=PINNED_ACCEPTED[name][1]
            require(sha(Path(module.__file__).read_bytes())==pin,'LOADED_ACCEPTED_SOURCE_IDENTITY_DRIFT__'+name)
            sources[name]=pin
        item=descriptor['new_integration_components']['POLICY_B_POLICY']
        require(sha((self.release_root/item['path']).read_bytes())==item['sha256'],'POLICY_B_POLICY_DRIFT')
        sources['POLICY_B_POLICY']=item['sha256']
        return sources

    def _trusted_evidence(self,capture,receipt,stage,binding,checkpoint,input_path):
        """Reconstruct on every verification; no executor-supplied trust flags."""
        import json
        import owner_authorization as owner
        from trusted_stage.staging_v1 import canonical
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=binding.unit_input_sha256)
        self.validator.verify_receipt(receipt,capture)
        require(self.checkpoint_attestor.verify_receipt(checkpoint),'CHECKPOINT_CHANGED_PRE_PROOF')
        require(self.checkpoint_attestor._recovery_phase is not None,'PROOF_RECOVERY_PHASE_REQUIRED')
        t,_,_,_,owner_pin,consumption_pin=self.checkpoint_attestor._recovery_phase
        transaction=json.loads(t.proof_checkpoint_binding(owner_authorization_sha256=owner_pin,
            owner_consumption_sha256=consumption_pin,executing=True))
        consumed=json.loads((t.journal/'owner_authorization_consumed.json').read_bytes())
        doc=owner.verify_transaction_publication(owner_pin,consumed['authorization_length'],t,t._bound_adapter,
            self,binding,input_path,self.release_root,phase='EXECUTING')
        require(verify_stage(stage)==canonical(receipt.payload),'PROOF_STAGE_VALIDATED_BYTES_MISMATCH')
        positions=[row['authorized_population_position'] for row in receipt.payload['validated_rows']]
        raw_positions=[row['authorized_population_position'] for row in receipt.payload['raw_rows']]
        require(all(type(x) is int for x in positions+raw_positions) and
                positions==raw_positions==list(range(1776,1801)),
                'PROOF_EXACT_POSITIONS_REQUIRED')
        return {
            'contract':{'batch':'BATCH0004','role':'PRIMARY','phase':'S05','unit':'U0012',
                'attempt_id':binding.attempt_id,'attempt_ordinal':10,'max_new_units':1,'u0013_prohibited':True},
            'authorization':{'sha256':owner_pin,'consumption_sha256':consumption_pin,
                'length':consumed['authorization_length'],'consumer_uid':doc['consumer_uid'],'scope':doc['scope'],
                'REAL_target_attempt_id':owner.publication.REAL_ATTEMPT,
                'REAL_target_checkpoint':doc['target_authorization']['checkpoint_identity']},
            'checkpoint':{'predecessor':checkpoint.identity,'executing_successor':t._executing_checkpoint_sha256,
                'predecessor_sequence':checkpoint.sequence,'successor_sequence':checkpoint.sequence+1,
                'phase_sha256':sha(checkpoint._phase)},
            'recovery':transaction,
            'sources':self._fresh_sources(),
            'runtime':owner.execution_facts(doc)['runtime'],
            'process':{'invocation_id':capture.invocation_id,'started_ns':capture.started_ns,'exited_ns':capture.exited_ns,
                'process_started':True,'return_code':capture.exit_code,'termination':capture.termination,
                'timeout':capture.timeout,'truncated':capture.truncated,'execution_exception':capture.execution_exception,
                'transport_interruption':capture.local_transport_interruption,'mode':capture.mode,
                'stdout_sha256':capture.stdout_sha256,'stderr_sha256':capture.stderr_sha256,
                'raw_output_sha256':capture.raw_output_sha256,'executable_sha256':capture.executable_sha256,
                'adapter_sha256':capture.adapter_sha256,'config_sha256':capture.config_sha256,
                'capture_source_sha256':capture.capture_source_sha256,'actual_input_sha256':capture.actual_input_sha256},
            'validation':{'validator_sha256':receipt.validator_sha256,
                'validated_output_sha256':receipt.validated_output_sha256,'positions':positions,
                'expected_identities_sha256':sha(canonical(list(binding.expected_identities))),
                'source_sha256':[pin for _,pin in self.validator._sources],
                'scientific_and_reason_precedence':'ACCEPTED_VALIDATOR_VERIFIED'},
            'staging':{'sha256':stage.staged_bytes_sha256,'readback_sha256':stage.readback_sha256,
                'bytes':stage.file_size,'row_count':stage.row_count},
            'ordering':{'finalization':'NOT_YET_PERFORMED','v7_qualification':'REQUIRES_INDEPENDENT_RECOVERY_VERIFICATION'},
        }

    def _trusted_policy_b_authority(self,capture,binding,checkpoint,input_path):
        import json
        import owner_authorization as owner
        from trusted_stage.staging_v1 import canonical
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=binding.unit_input_sha256)
        require(self.checkpoint_attestor.verify_receipt(checkpoint),'CHECKPOINT_CHANGED_PRE_PROOF')
        require(self.checkpoint_attestor._recovery_phase is not None,'PROOF_RECOVERY_PHASE_REQUIRED')
        t,_,_,_,owner_pin,consumption_pin=self.checkpoint_attestor._recovery_phase
        transaction=json.loads(t.proof_checkpoint_binding(owner_authorization_sha256=owner_pin,
            owner_consumption_sha256=consumption_pin,executing=True))
        consumed=json.loads((t.journal/'owner_authorization_consumed.json').read_bytes())
        doc=owner.verify_transaction_publication(owner_pin,consumed['authorization_length'],t,t._bound_adapter,
            self,binding,input_path,self.release_root,phase='EXECUTING')
        return transaction,consumed,doc,owner_pin,consumption_pin
