"""Canonical hash-bound operational record; no authentication or signing API.

A content hash is integrity metadata only. BoundProofPath independently rebuilds
claims from trusted observations and OS-controlled Owner readback. This module's
pure record helpers do not establish Owner authority or validate caller evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from trusted_stage.staging_v1 import require,sha,canonical,verify_stage

VERSION='BATCH0004_OPERATIONAL_INTEGRITY_PROOF_V2_SHA256'
POLICY_SHA='f3747fa0712821c32a9e97a02f196133e5544fff481185517de0e3748b4eef67'
CLASSIFIER_SHA='8c20ea1dd8507e94606af849b7e5886a738cdff2c9d7d3aa333bfef4de42c651'
FIELDS=(
 'PROOF_VERSION','BATCH_ID','ROLE','UNIT_ID','ATTEMPT_ID','CHECKPOINT_IDENTITY',
 'UNIT_INPUT_SHA256','RAW_EXECUTOR_OUTPUT_SHA256','STAGED_BYTES_SHA256','READBACK_SHA256',
 'STAGED_FILE_SIZE','EXPECTED_ROW_COUNT','OBSERVED_ROW_COUNT','SCHEMA_VALIDATION',
 'IDENTITY_VALIDATION','POSITION_VALIDATION','SERIALIZATION_READBACK',
 'PROCESS_RETURN_CODE','PROCESS_TERMINATION','SEMANTIC_SUBPROCESS_TIMEOUT',
 'SEMANTIC_EXECUTION_EXCEPTION','OUTPUT_TRUNCATION','TRANSPORT_INTERRUPTION',
 'EXTERNAL_AVAILABILITY_SIGNAL','AUXILIARY_REFRESH_TIMEOUT_SOURCE','SOURCE_ATTESTED',
 'EXECUTION_MODE','MODE_BINDING_SHA256','V7_V2_POLICY_SHA256','V7_V2_CLASSIFIER_SOURCE_SHA256',
 'ISSUER_IMPLEMENTATION_SHA256','CAPTURE_NONCE','TRUSTED_EVIDENCE',
)

def source_sha():return sha(Path(__file__).read_bytes())
def raw_executor_hash(result):
    require(type(result) is dict,'UNTRUSTED_EXECUTOR_RESULT')
    return sha(canonical(result))

@dataclass(frozen=True,slots=True)
class OperationalProof:
    claims: dict
    proof_sha256: str

def _expected_auxiliary_source(result, *, observed_rows):
    """Derive this claim from accepted V7, never from submitted proof claims.

    BoundProofPath supplies the independently observed result and validated,
    read-back stage. This pure record helper still confers no Owner authority.
    """
    import availability_classifier_v7_prospective as v7
    require(type(result.get('raw_stderr')) is str,'PROOF_STDERR_TYPE_INVALID')
    active=[line for line in result['raw_stderr'].splitlines() if line.strip()]
    require(len(active)<=1,'UNKNOWN_OR_CONFLICTING_STDERR')
    integrity=v7.VerifiedOperationalIntegrity(expected_rows=25,observed_rows=observed_rows,
        complete_output=True,output_schema_valid=True,identities_valid=True,
        positions_valid=True,serialization_readback_pass=True,
        semantic_subprocess_timeout=result['timeout_status'],semantic_execution_exception=False,
        output_truncation=False,transport_interruption=False,
        external_availability_present=False,source_attested=True)
    verdict=v7.decide_availability(result,integrity=integrity)
    require(verdict['decision']=='NO_EXTERNAL_SIGNAL' and
            verdict['conflict_evidence']==[] and verdict['hard_stop_classes']==[] and
            not verdict['external_signal_detected'] and
            not verdict['fields_present_minus_fields_inspected'] and
            not verdict['malformed_control_fields'],'PROOF_OPERATIONAL_CLASSIFICATION_REJECTED')
    if verdict['auxiliary_diagnostic_nonblocking'] is True:
        require(verdict['classification']=='NONBLOCKING_AUXILIARY_EXECUTOR_DIAGNOSTIC' and
                len(active)==1 and v7.positive_auxiliary_source(active[0]),
                'PROOF_AUXILIARY_SOURCE_NOT_VERIFIED')
        return 'CODEX_MODELS_MANAGER_REFRESH_TIMEOUT'
    require(verdict['auxiliary_diagnostic_nonblocking'] is False and
            verdict['classification']=='NONE' and
            verdict['operational_classification']=='NORMAL_SUCCESS' and
            not verdict['positive_auxiliary_source_identified'],
            'PROOF_ORDINARY_SUCCESS_NOT_VERIFIED')
    return None

def expected_claims(*,binding,stage,result,capture_nonce,trusted_evidence,pinned_issuer_sha256):
    """Rebuild all expected fields; never derive an expectation from proof claims.

    trusted_evidence is supplied by BoundProofPath's independent observations,
    not by the executor or forwarder. These pure helpers confer no authority.
    """
    require(pinned_issuer_sha256==source_sha(),'UNTRUSTED_ISSUER_SOURCE')
    binding.verify();require(stage.binding==binding,'STAGE_BINDING_MISMATCH');verify_stage(stage)
    require(type(result.get('process_started')) is bool and result['process_started'] and
            type(result.get('return_code')) is int and result['return_code']==0 and
            result.get('termination_state')=='NORMAL_SUCCESS' and
            type(result.get('timeout_status')) is bool and not result['timeout_status'],'PROCESS_INTEGRITY_FAILURE')
    require(type(capture_nonce) is str and capture_nonce==result['context_id'],'BAD_CAPTURE_NONCE')
    require(type(trusted_evidence) is dict and set(trusted_evidence)=={
        'contract','authorization','checkpoint','recovery','sources','runtime','process','validation','staging','ordering'},
        'TRUSTED_EVIDENCE_SCHEMA_INVALID')
    require(trusted_evidence['contract']=={'batch':'BATCH0004','role':'PRIMARY','phase':'S05','unit':'U0012',
        'attempt_id':binding.attempt_id,'attempt_ordinal':10,'max_new_units':1,'u0013_prohibited':True},
        'PROOF_EXACT_CONTRACT_REQUIRED')
    require(trusted_evidence['ordering']=={'finalization':'NOT_YET_PERFORMED',
        'v7_qualification':'REQUIRES_INDEPENDENT_RECOVERY_VERIFICATION'},'PROOF_PHASE_ORDERING_INVALID')
    require(stage.row_count==len(binding.expected_positions)==25,'ROW_COUNT_MISMATCH')
    auxiliary_source=_expected_auxiliary_source(result,observed_rows=stage.row_count)
    return {
        'PROOF_VERSION':VERSION,'BATCH_ID':binding.batch_id,'ROLE':binding.role,
        'UNIT_ID':binding.unit_id,'ATTEMPT_ID':binding.attempt_id,
        'CHECKPOINT_IDENTITY':binding.checkpoint_identity,'UNIT_INPUT_SHA256':binding.unit_input_sha256,
        'RAW_EXECUTOR_OUTPUT_SHA256':raw_executor_hash(result),
        'STAGED_BYTES_SHA256':stage.staged_bytes_sha256,'READBACK_SHA256':stage.readback_sha256,
        'STAGED_FILE_SIZE':stage.file_size,'EXPECTED_ROW_COUNT':25,'OBSERVED_ROW_COUNT':stage.row_count,
        'SCHEMA_VALIDATION':True,'IDENTITY_VALIDATION':True,'POSITION_VALIDATION':True,'SERIALIZATION_READBACK':True,
        'PROCESS_RETURN_CODE':0,'PROCESS_TERMINATION':'NORMAL_SUCCESS','SEMANTIC_SUBPROCESS_TIMEOUT':False,
        'SEMANTIC_EXECUTION_EXCEPTION':False,'OUTPUT_TRUNCATION':False,'TRANSPORT_INTERRUPTION':False,
        'EXTERNAL_AVAILABILITY_SIGNAL':False,'AUXILIARY_REFRESH_TIMEOUT_SOURCE':auxiliary_source,
        'SOURCE_ATTESTED':True,'EXECUTION_MODE':binding.execution_mode,'MODE_BINDING_SHA256':binding.mode_binding_sha256,
        'V7_V2_POLICY_SHA256':POLICY_SHA,'V7_V2_CLASSIFIER_SOURCE_SHA256':CLASSIFIER_SHA,
        'ISSUER_IMPLEMENTATION_SHA256':pinned_issuer_sha256,'CAPTURE_NONCE':capture_nonce,
        'TRUSTED_EVIDENCE':trusted_evidence,
    }

class TrustedIssuer:
    def __init__(self,*,pinned_issuer_source_sha256):
        require(pinned_issuer_source_sha256==source_sha(),'ISSUER_SOURCE_CHANGED')
        self.issuer_source_sha256=pinned_issuer_source_sha256
    def issue(self,stage,*,binding,result,capture_nonce,trusted_evidence):
        claims=expected_claims(binding=binding,stage=stage,result=result,capture_nonce=capture_nonce,
            trusted_evidence=trusted_evidence,pinned_issuer_sha256=self.issuer_source_sha256)
        return OperationalProof(claims,sha(canonical(claims)))

def verify_proof(proof,*,pinned_issuer_sha256,binding,stage,result,capture_nonce,trusted_evidence):
    require(type(proof) is OperationalProof,'ARBITRARY_CALLER_PROOF_REJECTED')
    require(type(proof.claims) is dict and set(proof.claims)==set(FIELDS),'PROOF_FIELD_SET_INVALID')
    require(type(proof.proof_sha256) is str and len(proof.proof_sha256)==64 and
            set(proof.proof_sha256)<=set('0123456789abcdef'),'BAD_PROOF_ENVELOPE')
    require(sha(canonical(proof.claims))==proof.proof_sha256,'PROOF_HASH_INVALID')
    expected=expected_claims(binding=binding,stage=stage,result=result,capture_nonce=capture_nonce,
        trusted_evidence=trusted_evidence,pinned_issuer_sha256=pinned_issuer_sha256)
    # Canonical exact-byte comparison includes all nested fields and JSON types;
    # changing claims and recomputing the hash still fails this independent check.
    require(canonical(proof.claims)==canonical(expected),'PROOF_IDENTITY_OR_INTEGRITY_BINDING_MISMATCH')
    return True
