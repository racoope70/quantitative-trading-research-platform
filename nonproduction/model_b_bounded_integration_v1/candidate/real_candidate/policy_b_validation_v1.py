"""Policy B sealed scientific receipt from the original registered capture.

The accepted scientific functions and Policy A validator are unchanged. This
adapter derives complete-message equivalence; it does not grant Owner authority.
"""
from dataclasses import dataclass
from pathlib import Path
import copy,json
from trusted_stage import staging_v1 as s
from . import capture_v1 as cap, validation_v1 as accepted
from . import policy_b_events_v1 as events

DOMAIN='BATCH0004_POLICY_B_SCIENTIFIC_RECEIPT_V1'

@dataclass(frozen=True,slots=True)
class PolicyBScientificReceipt:
    capture: object
    claims: dict
    payload: dict
    actual_input_bytes: bytes
    actual_input_sha256: str
    validator_sha256: str
    validated_output_sha256: str
    identity: str
    _seal: object

class PolicyBScientificValidator:
    def __init__(self,*,validator,capture,binding,frame,context_provider,source_provider):
        s.require(type(validator) is accepted.BoundAcceptedValidator and
                  type(validator.supervisor) is cap.ControlledLocalCapture and
                  type(capture) is cap.LocalObservation,'POLICY_B_TRUSTED_SCIENTIFIC_INTERFACE_REQUIRED')
        self.validator,self.supervisor,self.capture=validator,validator.supervisor,capture
        self.binding=binding.verify();self.frame=Path(frame)
        self.context_provider,self.source_provider=context_provider,source_provider
        self._source= s.sha(s.safe_read(Path(__file__)))
        self._context=s.canonical(context_provider())
        self._seal=object();self._receipt=None

    def reconstruct(self):
        s.require(s.sha(s.safe_read(Path(__file__)))==self._source,'POLICY_B_VALIDATOR_SOURCE_DRIFT')
        sources=self.source_provider();context=self.context_provider()
        s.require(s.canonical(context)==self._context,'POLICY_B_EXECUTION_CONTEXT_STALE')
        b=self.binding.verify();o=self.capture
        self.supervisor.verify(o,input_file=self.frame,pinned_input_sha256=b.unit_input_sha256)
        s.require(o.exit_code==0 and o.termination=='NORMAL_SUCCESS' and o.capture_complete and o.cleanup_complete and
                  not(o.timeout or o.truncated or o.execution_exception or o.local_transport_interruption),
                  'POLICY_B_CAPTURE_INCOMPLETE_OR_FAILED')
        expected_mode='REAL' if b.execution_mode=='REAL' else 'NONPRODUCTION_TEST'
        s.require(o.mode==self.supervisor.mode==expected_mode and
                  o.actual_input_sha256==b.unit_input_sha256 and o.config_sha256==b.mode_binding_sha256 and
                  context['input_sha256']==o.actual_input_sha256 and context['runtime_sha256']==o.executable_sha256 and
                  context['configuration_sha256']==o.config_sha256 and context['invocation_id']==o.invocation_id,
                  'POLICY_B_EXECUTION_IDENTITY_MISMATCH')
        a=events.inspect_envelope(o.stdout,expected_context=context,
                                 frozen_extract=self.validator.module.v3.parse_codex_json_events)
        partition,evidence,reason=self.validator._read_sources()
        rows=self.validator.module.unit_evidence(partition,evidence,'U0012')
        raw=s.canonical(rows)
        s.require(raw==s.safe_read(self.frame) and s.sha(raw)==b.unit_input_sha256 and
                  tuple(r['canonical_source_identity'] for r in rows)==b.expected_identities,
                  'POLICY_B_EXACT_SCIENTIFIC_INPUT_REQUIRED')
        result={'process_started':True,'return_code':o.exit_code,'termination_state':o.termination,
            'timeout_status':o.timeout,'context_id':o.invocation_id,'agent_message':a.common_result.decode('utf8')}
        checked=self.validator.module.validate_semantic_unit(partition,evidence,reason,'U0012',result,'PRIMARY')
        checked['row_count']=25
        s.require(len(checked['raw_rows'])==len(checked['validated_rows'])==25,'POLICY_B_EXACT_25_ROWS_REQUIRED')
        s.check_payload(checked,b)
        payload_sha=accepted._validated_output_hash(checked)
        claims={'domain':DOMAIN,'full_capture_sha256':s.sha(o.stdout),'full_capture_length':len(o.stdout),
            'complete_occurrence_set':a.witness['all_qualifying_occurrences'],
            'ordered_message_text_sha256':a.witness['ordered_message_text_hashes'],
            'common_result_sha256':s.sha(a.common_result),'common_result_length':len(a.common_result),
            'message_count':a.witness['message_count'],'completed_turn_count':a.witness['completed_turn_count'],
            'cli_thread_id':a.witness['cli_thread_id'],'provider_message_identity':'NOT_ESTABLISHED',
            'validated_scientific_payload_sha256':payload_sha,'batch_unit_attempt':{
                'batch':b.batch_id,'role':b.role,'unit':b.unit_id,'attempt':b.attempt_id,'checkpoint':b.checkpoint_identity},
            'execution':context,'source_identities':sources,'validator_sha256':accepted.VALIDATOR_SHA,
            'source_input_sha256':[pin for _,pin in self.validator._sources],
            'scientific_semantics_and_reason_precedence':'UNCHANGED_ACCEPTED_FUNCTIONS'}
        return claims,checked,a.common_result

    def issue(self):
        s.require(self._receipt is None,'POLICY_B_RECEIPT_ALREADY_ISSUED')
        claims,payload,_=self.reconstruct()
        identity=s.sha(DOMAIN.encode()+b'\0'+s.canonical(claims))
        r=PolicyBScientificReceipt(self.capture,copy.deepcopy(claims),copy.deepcopy(payload),
            s.safe_read(self.frame),self.binding.unit_input_sha256,accepted.VALIDATOR_SHA,
            accepted._validated_output_hash(payload),identity,self._seal)
        self._receipt=(r,s.canonical(claims),s.canonical(payload));return r

    def verify(self,r):
        s.require(type(r) is PolicyBScientificReceipt and self._receipt is not None and
                  r is self._receipt[0] and r._seal is self._seal and r.capture is self.capture,
                  'POLICY_B_RECEIPT_ORIGIN_REJECTED')
        claims,payload,_=self.reconstruct()
        s.require(s.canonical(r.claims)==s.canonical(claims)==self._receipt[1] and
                  s.canonical(r.payload)==s.canonical(payload)==self._receipt[2] and
                  r.identity==s.sha(DOMAIN.encode()+b'\0'+s.canonical(claims)) and
                  r.actual_input_bytes==s.safe_read(self.frame) and r.actual_input_sha256==self.binding.unit_input_sha256 and
                  r.validator_sha256==accepted.VALIDATOR_SHA and
                  r.validated_output_sha256==accepted._validated_output_hash(payload),
                  'POLICY_B_RECEIPT_RECONSTRUCTION_MISMATCH')
        return claims,payload
