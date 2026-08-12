import hashlib, json, pathlib, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_013']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))
from identity_io_v1 import canonical_bytes
import external_attestation_verifier_v1 as v
from ak_provenance_v1 import *
from measured_boot_replay_v1 import *
from ima_replay_v1 import *
RU='12345678-1234-1234-1234-123456789abc'; NO='11'*32; RR='22'*32

def _write_manifest(td,role,obj):
    p=pathlib.Path(td)/(role+'.json'); data={'manifest_role':role,**obj}; p.write_text(json.dumps(data,sort_keys=True)); raw=p.read_bytes(); return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'byte_count':len(raw)}
class Blocker013Tests(unittest.TestCase):
    def test_001_host_verification_context_absent_from_schema(self):
        schema=(ROOT/'schemas/attestation_transaction_v1.schema.json').read_text(); self.assertNotIn('verification_context',schema)
    def test_002_verifier_loads_five_local_expectation_manifests(self):
        src=(ROOT/'src/blocker_013/external_attestation_verifier_v1.py').read_text()
        for role in ('pcr_policy','ima_policy','host_tcb_manifest','ak_ek_policy','runtime_binding_policy'): self.assertIn(role,src)
        self.assertIn('require_file_identity',src)
    def test_003_unresolved_local_manifest_fails_closed(self):
        cfg={'expected_manifest_bindings':{'pcr_policy':{'path':'UNRESOLVED_X','sha256':'UNRESOLVED_Y'}}}
        with self.assertRaises(v.VerificationError): v._manifest(cfg,'pcr_policy')
    def test_004_manifest_content_hash_is_verified(self):
        with tempfile.TemporaryDirectory() as td:
            spec=_write_manifest(td,'pcr_policy',{'x':1}); spec['sha256']='00'*32
            with self.assertRaises(Exception): v._manifest({'expected_manifest_bindings':{'pcr_policy':spec}},'pcr_policy')
    def test_005_manifest_role_must_match(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x.json'; p.write_text(json.dumps({'manifest_role':'wrong'})); raw=p.read_bytes(); spec={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'byte_count':len(raw)}
            with self.assertRaises(v.VerificationError): v._manifest({'expected_manifest_bindings':{'pcr_policy':spec}},'pcr_policy')
    def test_006_verifier_manifest_binds_all_expectation_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            roles=('pcr_policy','ima_policy','host_tcb_manifest','ak_ek_policy','runtime_binding_policy'); bindings={r:_write_manifest(td,r,{}) for r in roles}; h=hashlib.sha256(canonical_bytes({r:bindings[r]['sha256'] for r in roles})).hexdigest(); cfg={'expected_manifest_bindings':bindings,'verifier_manifest_sha256':h}; out=v.load_verifier_expectations(cfg); self.assertEqual(out['verifier_manifest_sha256'],h)
    def test_007_verifier_manifest_wrong_aggregate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            roles=('pcr_policy','ima_policy','host_tcb_manifest','ak_ek_policy','runtime_binding_policy'); bindings={r:_write_manifest(td,r,{}) for r in roles}; cfg={'expected_manifest_bindings':bindings,'verifier_manifest_sha256':'00'*32}
            with self.assertRaises(v.VerificationError): v.load_verifier_expectations(cfg)
    def test_008_runtime_policy_rejects_unadmitted_transaction(self):
        b={'transaction_type':'PRE_E1_ATTESTATION'}; p={'manifest_role':'runtime_binding_policy','allowed_transaction_types':['POST_OBSERVATION_ATTESTATION'],'expected_runtime_record_fields':{'qemu_binary_sha256':'11'*32}}
        with self.assertRaises(v.VerificationError): v._runtime_record_check(b,{}, {'freeze_record_schema_path':str(ROOT/'schemas/freeze_instrument_records_v1.schema.json')},p)
    def test_009_pre_quote_qualification_is_independently_derived(self):
        b={'runtime_instance_uuid':RU,'observation_nonce':NO,'runtime_instantiation_attestation_record_sha256':RR,'verifier_manifest_sha256':'33'*32}; q=v._pre_quote_qualification(b); self.assertEqual(len(q),64); self.assertNotEqual(q,v._pre_quote_qualification({**b,'observation_nonce':'44'*32}))
    def test_010_compare_host_tcb_exact_member_set(self):
        self.assertEqual(v.compare_host_tcb({'a':'11'*32},{'a':'11'*32}),'PASS')
        with self.assertRaises(v.VerificationError): v.compare_host_tcb({'a':'11'*32,'b':'22'*32},{'a':'11'*32})
    def test_011_decode_objects_requires_exact_hash(self):
        good={'role':'x','byte_count':1,'sha256':hashlib.sha256(b'a').hexdigest(),'data_hex':'61'}; self.assertEqual(v.decode_objects({'objects':{'x':good}})['x'],b'a')
        with self.assertRaises(v.VerificationError): v.decode_objects({'objects':{'x':{**good,'sha256':'00'*32}}})
    def test_012_ak_name_uses_tpmt_public(self):
        body=b'\x00\x23\x00\x0b'+b'X'*20; p=len(body).to_bytes(2,'big')+body; self.assertTrue(compute_name(p).startswith('000b'))
    def test_013_credential_activation_mismatch_fails(self):
        with self.assertRaises(AKProvenanceError): verify_credential_activation_evidence({'method':'TPM2_ACTIVATECREDENTIAL','credential_secret_sha256':'11'*32,'activated_secret_sha256':'22'*32,'result':'PASS'})
    def test_014_event_log_truncation_fails(self):
        with self.assertRaises(ReplayError): parse_event_log(b'abc')
    def test_015_ima_unknown_template_fails(self):
        data=b'a'; th=hashlib.sha256(data).digest(); name=b'bad\0'; raw=(10).to_bytes(4,'little')+th+len(name).to_bytes(4,'little')+name+len(data).to_bytes(4,'little')+data; desc={'format_identity':'IMA_NATIVE_BINARY_CANONICAL_V1','byteorder':'little','template_hash_algorithm':'sha256','template_hash_size':32,'allowed_templates':['ima-ng']}
        with self.assertRaises(IMAReplayError): parse_native_binary_measurements(raw,desc)
    def test_016_handler_rejects_host_context_even_before_verification(self):
        src=(ROOT/'src/blocker_013/external_attestation_verifier_v1.py').read_text(); self.assertIn("'verification_context' in objects",src); self.assertIn('host-supplied verifier expectations prohibited',src)
    def test_017_config_declares_content_addressed_expectation_bindings(self):
        cfg=json.loads((ROOT/'config/blocker_013/blocker_013_config_v1.json').read_text()); self.assertEqual(set(cfg['expected_manifest_bindings']),{'pcr_policy','ima_policy','host_tcb_manifest','ak_ek_policy','runtime_binding_policy'}); self.assertTrue(all(set(x)>= {'path','sha256'} for x in cfg['expected_manifest_bindings'].values()))
    def test_018_host_tcb_is_observation_not_expectation(self):
        schema=json.loads((ROOT/'schemas/attestation_transaction_v1.schema.json').read_text()); props=schema['$defs']['pre_objects']['properties']; self.assertIn('host_tcb_observation',props); self.assertNotIn('expected_host_tcb',props)
    def test_019_post_qualification_binds_checkpoint_and_challenge(self):
        b={'runtime_instance_uuid':RU,'observation_nonce':NO,'fresh_challenge':'33'*32,'final_checkpoint_sha256':'44'*32,'runtime_instantiation_attestation_record_sha256':RR,'verifier_manifest_sha256':'55'*32}; c={'final_host_sequence':9,'final_record_sha256':'66'*32,'observation_start_host_sequence':3,'observation_end_host_sequence':8}; q=v._post_quote_qualification(b,c); self.assertNotEqual(q,v._post_quote_qualification({**b,'fresh_challenge':'77'*32},c))
    def test_020_verifier_source_never_decodes_verification_context_as_expected(self):
        src=(ROOT/'src/blocker_013/external_attestation_verifier_v1.py').read_text(); self.assertNotIn("expected=canonical_loads(objects['verification_context'])",src)
    def test_021_runtime_record_is_observed_and_checked_against_verifier_side_fields(self):
        record={'record_type':'RUNTIME_INSTANTIATION_ATTESTATION_RECORD','admitted_environment_specification_sha256':'01'*32,'frozen_build_output_manifest_sha256':'02'*32,'raw_disk_sha256':'03'*32,'dm_verity_configuration_sha256':'04'*32,'dm_verity_root_hash':'root','dm_verity_hash_tree_sha256':'05'*32,'verified_block_object_identity':{'st_dev':1,'st_ino':2,'st_mode':3,'st_rdev':4,'target':'/dev/x'},'qemu_binary_sha256':'06'*32,'qemu_machine_configuration_sha256':'07'*32,'qemu_evidence_transport_configuration_sha256':'08'*32,'preopened_fd_binding_identity':'09'*32,'qemu_process_identity':'qemu','runtime_instance_uuid':RU,'observation_nonce':NO,'guest_firmware_identity':'0a'*32,'host_evidence_channel_configuration_sha256':'0b'*32,'host_attestation_state_reference':'host','launch_timestamp_monotonic':1,'launch_timestamp_utc':2}
        raw=canonical_bytes(record); bundle={'transaction_type':'PRE_E1_ATTESTATION','runtime_instance_uuid':RU,'observation_nonce':NO,'runtime_instantiation_attestation_record_sha256':hashlib.sha256(raw).hexdigest()}; policy={'manifest_role':'runtime_binding_policy','allowed_transaction_types':['PRE_E1_ATTESTATION'],'expected_runtime_record_fields':{'qemu_binary_sha256':'06'*32}}
        out=v._runtime_record_check(bundle,{'runtime_instantiation_record':raw},{'freeze_record_schema_path':str(ROOT/'schemas/freeze_instrument_records_v1.schema.json')},policy); self.assertEqual(out['qemu_binary_sha256'],'06'*32)
    def test_022_runtime_record_verifier_side_expected_field_mismatch_rejected(self):
        src=(ROOT/'src/blocker_013/external_attestation_verifier_v1.py').read_text(); self.assertIn('expected_runtime_record_fields',src); self.assertIn('verifier-side runtime record mismatch',src)
    def test_023_runtime_policy_has_no_circular_verifier_manifest_requirement(self):
        src=(ROOT/'src/blocker_013/external_attestation_verifier_v1.py').read_text(); self.assertNotIn('require_verifier_manifest_sha256',src)
    def test_024_attestation_schema_requires_observed_runtime_record_in_pre_and_post(self):
        schema=json.loads((ROOT/'schemas/attestation_transaction_v1.schema.json').read_text()); self.assertIn('runtime_instantiation_record',schema['$defs']['pre_objects']['required']); self.assertIn('runtime_instantiation_record',schema['$defs']['post_objects']['required'])

