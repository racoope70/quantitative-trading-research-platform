"""Deterministic, non-activating release identity construction and verification.

One release descriptor with detached SHA avoids a cyclic self-hash dependency.
Does not create/approve a REAL release; Independent review is still required.
"""
from __future__ import annotations
from pathlib import Path
import json
from trusted_stage.staging_v1 import sha,canonical,require,safe_read

MANIFEST_FILE='REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json'
PIN_FILE='REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256'

TASK='POST_C6_Q1_2027_D1_BODY_BATCH0004_PRIMARY_S05_REAL_CAPTURE_ISSUER_INTEGRATION_CORRECTION_V2'
REQUIRED_CANDIDATE=('capture_v1.py','checkpoint_v1.py','proof_issuer_v1.py',
                    'activation_v1.py','real_binding_v1.py','validation_v1.py','proof_path_v1.py','release_v1.py','executor_v1.py','engine_v1.py','policy_b_events_v1.py','policy_b_validation_v1.py','policy_b_proof_v1.py')
PINNED_ACCEPTED={
 'HISTORICAL_RECOVERY_V3_SOURCE':('accepted_recovery/recovery_two_attempt_v3.py','0376a36a82d9e18f45cdcda879c0175c2ec0dd899e32a00b8c59174082460531'),
 'ACCESSIBLE_TRUST_BASIS_ALIGNMENT':('real_trust_boundary/real_boundary_v1.py','fcdb3a5e094050d83139e0d770cceca7b562769d1e46b9d1137d13a615845955'),
 'ACCESSIBLE_TRUST_POLICY':('ACCESSIBLE_TRUST_BASIS_POLICY_ALIGNMENT_V1.json','0fc6838b48b775b684e10325204794e36577e1e69c37bd3136e46f36cc5f1993'),
 'V7_V2_POLICY':('policy_v7_prospective.json','f3747fa0712821c32a9e97a02f196133e5544fff481185517de0e3748b4eef67'),
 'V7_V2_CLASSIFIER':('availability_classifier_v7_prospective.py','8c20ea1dd8507e94606af849b7e5886a738cdff2c9d7d3aa333bfef4de42c651'),
 'VALIDATOR':('accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py','d8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42'),
 'REAL_ADAPTER':('accepted_recovery/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py','1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424'),
 'CHECKPOINT_ENGINE':('accepted_recovery/checkpoint_resume_activation_trusted_v1.py','fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1'),
 'RECOVERY_INTERFACE':('accepted_recovery/bounded_controlled_stop_recovery_real_interface_v2.py','b51c63dd499c20711d153cc9abfca0361b588ad1c4ae772b1f84f464fcfba785'),
 'MODE_PROVENANCE':('accepted_recovery/recovery_mode_binding_descriptor_v2.json','0adcb00fbe0c98243e4241388043640a3a7ca4a658d02f37c8a56167d4f6365b'),
 'STAGING_READBACK':('trusted_stage/staging_v1.py','afbae35b8a1fc9204b3e8ef9244781667315155062a4b3c54e09e156b8e38125'),
 'EXACT_BYTE_PROMOTION':('trusted_stage/promotion_v1.py','edc5e568e181297872e2658410b9604006730b71470b8eb75b677b5b4ea75ef7'),
}
# The two accepted source-slice digests are historical provenance references,
# not separate executable bytes. The controlling alignment source is pinned above.
IDENTITY_CORRECTION_REFERENCES={
    'actual_input_source_slice_sha256':'7cabe8e58c9b4f0ef8eb1aa14bbe189aede74bffff159e78054a2d5d932267f8',
    'fresh_prelaunch_source_slice_sha256':'b9d00750be4fd495a7b32da50f5e5b865e7b288191d2c5618381713fe05c0a56',
    'historical_complete_module_sha256':'65fb889c82881c25b47ec6758681b1f496b164c2c3792c48a060ced5de71bfe8',
}
# Previously owner-observed Mac identities: reference-only until freshly
# reattested after Independent review; never claim current verification.
OWNER_OBSERVED_EXECUTORS={
 'codex_native_macos_x64_sha256':'17ae582b1048415503cf9455e677fd75c5b25ced17f20b883e55946fc5eeb679',
 'codex_js_launcher_sha256':'61b0194f3bb6534439c8d26a3ed57d0805f84b884588b761795323eeb92fcf70',
 'node_sha256':'a5ebb9adc969c8fcc486823ada530a4130b0d56edf954de7b05c280170487b1a',
 'python_sha256':'d4f152f2a753c94e0e7935c8ebbe6b2609979e1df7898422b577d0076383d08b',
 'verification_status':'OWNER_OBSERVED_HISTORICALLY__FRESH_REAL_ATTESTATION_REQUIRED'
}

def make_descriptor(root:Path):
    root=Path(root)
    acc={}
    for name,(path,pin) in PINNED_ACCEPTED.items():
        b=safe_read(root/'accepted'/path)
        require(sha(b)==pin,'ACCEPTED_COMPONENT_IDENTITY_DRIFT__'+name)
        acc[name]={'path':'accepted/'+path,'sha256':pin}
    created={}
    for f in REQUIRED_CANDIDATE:
        p=root/'candidate/real_candidate'/f
        created[f.removesuffix('.py').upper()]={'path':'candidate/real_candidate/'+f,'sha256':sha(safe_read(p))}
    created['POLICY_B_POLICY']={'path':'candidate/real_candidate/policy_b_policy_v1.json',
        'sha256':sha(safe_read(root/'candidate/real_candidate/policy_b_policy_v1.json'))}
    prospective={name:{'path':path,'sha256':sha(safe_read(root/path))} for name,path in {
        'EXECUTOR_INTERFACE':'candidate/prospective_adapter_v1.py',
        'RECOVERY':'candidate/recovery_bounded_v4.py',
        'RECOVERY_MEMBERSHIP':'candidate/membership_readonly.py',
        'B53_READ_ONLY_AUTHORITY_CONTRACT':'candidate/b53_owner_readonly_v1.py',
        'RECOVERY_COMPATIBILITY':'candidate/recovery_compatibility_bounded_v4.json'}.items()}
    # Demonstrate the historical actual-input/prelaunch slice references have
    # been copied only as separately-accepted provenance, not freshly measured.
    history=json.loads(safe_read(root/'accepted/IDENTITY_CORRECTION_SOURCE_SLICE_HASHES.json'))
    require(history['actual_input_binding']['sha256']==IDENTITY_CORRECTION_REFERENCES['actual_input_source_slice_sha256'] and
            history['fresh_prelaunch_identity']['sha256']==IDENTITY_CORRECTION_REFERENCES['fresh_prelaunch_source_slice_sha256'],
            'ACCEPTED_IDENTITY_CORRECTION_PROVENANCE_INVALID')
    return {
      'project':'QUANTITATIVE_TRADING_RESEARCH_PLATFORM','batch_id':'BATCH_0004','role':'PRIMARY',
      'task_id':TASK,'release_version':'BOUNDED_EXECUTOR_RECOVERY_CANDIDATE_V4',
      'release_purpose':'REAL_S05_RUNTIME_CANDIDATE',
      'release_status':'NONPRODUCTION_VALIDATED_NOT_ACTIVATED',
      'release_is_approved_for_real_use':False,'production_activation_gate':'HARD_DISABLED',
      'operational_proof_signer_required':False,'real_authorization_prepared':False,
      'max_new_units':1,'authorized_unit_contract':'U0012_ONLY','u0013_prohibited':True,
      'accepted_components':acc,'new_integration_components':created,'prospective_components':prospective,
      'historical_release_reference_sha256':'1b1f9e867cb921910031fa7fba6296c31808df4da627f6eefed1fd0b26f79a93',
      'accepted_historical_identity_correction_references':IDENTITY_CORRECTION_REFERENCES,
      'owner_observed_executors_reference_only':OWNER_OBSERVED_EXECUTORS,
      'operational_proof_mechanism':'CANONICAL_SHA256_PLUS_INDEPENDENT_EXPECTED_CLAIMS',
      'proof_schema':'BATCH0004_POLICY_B_INTEGRITY_PROOF_V1_SHA256',
      'policy_a_proof_schema':'BATCH0004_OPERATIONAL_INTEGRITY_PROOF_V2_SHA256',
      'scientific_acceptance_contract':'POLICY_B_EXACT_COMPLETE_MESSAGE_VALUE_V1',
      'capture_mode':'LOCAL_OBSERVATIONS_ONLY__NEVER_PRIVILEGED_TELEMETRY',
      'checkpoint_mode':'READ_ONLY_ATTESTATION__SCIENTIFIC_ENGINE_SEPARATELY_REQUIRED',
      'real_activation_eligible':False,
      'owner_authorized_execution_contract':'EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION',
      'rejected_predecessor_candidate_identity':'3d3d1f06981bedc39cac7003ed5d0e2e91b192f30807b749352f099119f14b27',
      'correction_scope':'EXECUTION_SINK_AUTHORIZATION__EXACT_VALIDATED_OUTPUT_RECEIPT_BINDING',
    }

def verify_release(root:Path, *, descriptor_file=MANIFEST_FILE,
                   pin_file=PIN_FILE):
    root=Path(root)
    manifest_bytes=safe_read(root/descriptor_file)
    digest=sha(manifest_bytes)
    require(safe_read(root/pin_file).decode('ascii').strip()==digest,'RELEASE_MANIFEST_TAMPERED')
    descriptor=json.loads(manifest_bytes)
    require(manifest_bytes==canonical(descriptor),'RELEASE_MANIFEST_NONCANONICAL')
    require(descriptor==make_descriptor(root),'RELEASE_COMPONENT_SUBSTITUTION_OR_CONFIGURATION_DRIFT')
    require(descriptor['release_status']=='NONPRODUCTION_VALIDATED_NOT_ACTIVATED' and
            descriptor['production_activation_gate']=='HARD_DISABLED' and
            descriptor['operational_proof_signer_required'] is False and
            descriptor['real_activation_eligible'] is False and
            descriptor['owner_authorized_execution_contract']==
                'EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION','RELEASE_ACTIVATION_TAMPERING')
    return digest
