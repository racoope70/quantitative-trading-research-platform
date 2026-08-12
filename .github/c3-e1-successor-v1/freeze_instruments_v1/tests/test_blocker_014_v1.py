import hashlib, json, os, pathlib, stat, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))
import fd_policy_v1 as fd
import runtime_instantiation_launcher_v1 as l
import host_runtime_lifecycle_provider_v1 as h
import attestation_transaction_controller_v1 as c
from identity_io_v1 import canonical_bytes,canonical_sha256
RU='12345678-1234-1234-1234-123456789abc'; NO='11'*32; RR='22'*32
class Blocker014Tests(unittest.TestCase):
    def test_001_qemu_transport_exact_chain_bound_in_config(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); t=cfg['qemu_evidence_transport']; self.assertEqual(t['host_socket'],'/run/c3-e1/qemu-evidence.sock'); self.assertEqual(t['guest_device_path'],'/dev/virtio-ports/org.c3e1.evidence'); self.assertIn('-chardev',cfg['qemu_argv']); self.assertIn('-device',cfg['qemu_argv'])
    def test_002_validate_qemu_transport_requires_chardev_and_virtserial(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); self.assertEqual(len(l.validate_qemu_evidence_transport(cfg)),64)
        bad={**cfg,'qemu_argv':[x for x in cfg['qemu_argv'] if not x.startswith('socket,id=')]}
        with self.assertRaises(l.LaunchError): l.validate_qemu_evidence_transport(bad)
    def test_003_qemu_configuration_identity_binds_transport(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); cfg['qemu_machine_configuration_sha256']='UNRESOLVED_STAGE1_QEMU_CONFIG_SHA256'; a=l.qemu_configuration_identity(cfg); cfg2=json.loads(json.dumps(cfg)); cfg2['qemu_evidence_transport']['virtio_port_name']='org.c3e1.other'; b=l.qemu_configuration_identity(cfg2); self.assertNotEqual(a,b);
        with self.assertRaises(l.LaunchError): l.validate_qemu_evidence_transport(cfg2)
    def test_004_fd_manifest_is_exact_0_1_2_3(self):
        m=json.loads((ROOT/'config/blocker_014/qemu_inherited_fd_manifest_v1.json').read_text()); self.assertEqual(set(m['fds']),{'0','1','2','3'}); self.assertEqual(m['fds']['3'],'EXACT_VERIFIED_DM_VERITY_OBJECT')
    def test_005_standard_fd_enforcement_checks_devnull_and_modes(self):
        src=(ROOT/'src/common/fd_policy_v1.py').read_text(); self.assertIn('normalize_standard_fds',src); self.assertIn('verify_devnull_standard_fds',src); self.assertIn("'/dev/null'",src); self.assertIn('O_RDONLY',src); self.assertIn('O_WRONLY',src)
    def test_006_runtime_launcher_normalizes_before_exact_allowlist(self):
        src=(ROOT/'src/blocker_014/runtime_instantiation_launcher_v1.py').read_text(); self.assertLess(src.index('normalize_standard_fds()'),src.index('verify_inherited((0,1,2,3))')); self.assertLess(src.index('verify_devnull_standard_fds()'),src.index('verify_inherited((0,1,2,3))'))
    def test_007_runtime_unit_sets_standard_streams_null(self):
        s=(ROOT/'units/runtime_instantiation_launcher_v1.service').read_text(); self.assertIn('StandardInput=null',s); self.assertIn('StandardOutput=null',s); self.assertIn('StandardError=null',s)
    def test_008_launcher_handoff_auth_policy_is_frozen(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); p=cfg['launcher_peer_policy']; self.assertEqual(p['instrument_identity'],'C3_E1_SUCCESSOR_RUNTIME_INSTANTIATION_LAUNCHER_V1'); self.assertIn('expected_process',p)
    def test_009_lifecycle_authenticates_launcher_before_pidfd_use(self):
        src=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); self.assertIn('bind_source(cred',src); self.assertIn("launcher_peer_policy",src); self.assertLess(src.index('bind_source(cred'),src.index("open(f'/proc/self/fdinfo/{pidfd}')"))
    def test_010_attestation_input_has_single_trusted_producer(self):
        src=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); self.assertIn('def produce_attestation_input',src); self.assertIn("RUNTIME_ATTESTATION_INPUT",src); self.assertIn('durable_write',src)
    def test_011_attestation_input_reference_is_content_addressed(self):
        src=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); self.assertIn("RUNTIME_ATTESTATION_INPUT_REFERENCE",src); self.assertIn("'byte_count'",src); self.assertIn("'sha256'",src)
    def test_012_controller_requires_input_and_reference_identity(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertIn('runtime_transaction_input_reference_path',src); self.assertIn('require_file_identity',src); self.assertIn('runtime attestation input reference binding',src)
    def test_013_controller_does_not_accept_host_verification_context(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertIn('host-supplied verification context prohibited',src); self.assertNotIn("r['attestation_objects']",src)
    def test_014_pre_qualification_binds_runtime_and_verifier(self):
        q=c.pre_qualification(bytes.fromhex('12'*16),bytes.fromhex(NO),bytes.fromhex(RR),bytes.fromhex('33'*32)); self.assertEqual(len(q),32); self.assertNotEqual(q,c.pre_qualification(bytes.fromhex('12'*16),bytes.fromhex(NO),bytes.fromhex(RR),bytes.fromhex('44'*32)))
    def test_015_post_qualification_binds_checkpoint(self):
        args=(bytes.fromhex('12'*16),bytes.fromhex(NO),bytes.fromhex('33'*32),9,bytes.fromhex('44'*32),bytes.fromhex('55'*32),2,8,bytes.fromhex(RR),bytes.fromhex('66'*32)); q=c.post_qualification(*args); a=list(args); a[4]=bytes.fromhex('77'*32); self.assertNotEqual(q,c.post_qualification(*a))
    def test_016_controller_uses_one_persistent_sink_client_for_pre_and_checkpoint(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); main=src[src.index('def main():'):]; self.assertEqual(main.count('SinkClient('),1); self.assertIn('run_pre_e1(cfg,r,sink)',main); self.assertIn('request_final_checkpoint(cfg,r,read_json',main)
    def test_017_start_token_release_is_after_verifier_pass(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); seg=src[src.index('def run_pre_e1'):src.index('def request_final_checkpoint')]; self.assertLess(seg.index("'PRE_E1_VERIFIER_RESULT'"),seg.index("'START_TOKEN_RELEASE_REQUEST'"))
    def test_018_runtime_input_schema_is_closed_and_bound(self):
        schema=json.loads((ROOT/'schemas/freeze_instrument_records_v1.schema.json').read_text()); d=schema['$defs']['att_input']; self.assertFalse(d['additionalProperties']); self.assertIn('runtime_record_sha256',d['required']); self.assertIn('evidence_inputs',d['required'])
    def test_019_runtime_input_roles_exclude_verification_context(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); self.assertNotIn('verification_context',cfg['pre_attestation_roles']); self.assertNotIn('verification_context',cfg['post_attestation_roles']); self.assertNotIn('verification_context',cfg['attestation_evidence_inputs'])
    def test_020_launch_record_binds_qemu_transport_identity(self):
        src=(ROOT/'src/blocker_014/runtime_instantiation_launcher_v1.py').read_text(); self.assertIn("'qemu_evidence_transport_configuration_sha256'",src); schema=json.loads((ROOT/'schemas/freeze_instrument_records_v1.schema.json').read_text()); self.assertIn('qemu_evidence_transport_configuration_sha256',schema['$defs']['runtime_instantiation']['required'])
    def test_021_runtime_attestation_input_evidence_refs_are_content_addressed(self):
        schema=json.loads((ROOT/'schemas/freeze_instrument_records_v1.schema.json').read_text()); ref=schema['$defs']['att_evidence_ref']; self.assertEqual(set(ref['required']),{'path','byte_count','sha256'}); self.assertFalse(ref['additionalProperties'])
    def test_022_lifecycle_builds_content_addressed_runtime_input(self):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td); roles=('ak_enrollment_record','ak_tpmt_public','ek_certificate','measured_boot_event_log','ima_binary_measurements','host_tcb_observation'); paths={}
            for role in roles: p=td/role; p.write_bytes(role.encode()); paths[role]=str(p)
            record={'record_type':'RUNTIME_INSTANTIATION_ATTESTATION_RECORD','admitted_environment_specification_sha256':'01'*32,'frozen_build_output_manifest_sha256':'02'*32,'raw_disk_sha256':'03'*32,'dm_verity_configuration_sha256':'04'*32,'dm_verity_root_hash':'root','dm_verity_hash_tree_sha256':'05'*32,'verified_block_object_identity':{'st_dev':1,'st_ino':2,'st_mode':3,'st_rdev':4,'target':'/dev/x'},'qemu_binary_sha256':'06'*32,'qemu_machine_configuration_sha256':'07'*32,'qemu_evidence_transport_configuration_sha256':'08'*32,'preopened_fd_binding_identity':'09'*32,'qemu_process_identity':'qemu','runtime_instance_uuid':RU,'observation_nonce':NO,'guest_firmware_identity':'0a'*32,'host_evidence_channel_configuration_sha256':'0b'*32,'host_attestation_state_reference':'host','launch_timestamp_monotonic':1,'launch_timestamp_utc':2}
            rr=canonical_sha256(record); cfg={'attestation_evidence_inputs':paths,'pre_attestation_roles':list(roles),'post_attestation_roles':['ak_enrollment_record','ak_tpmt_public'],'verifier_manifest_sha256':'0c'*32,'runtime_transaction_input_path':str(td/'input.json'),'runtime_transaction_input_reference_path':str(td/'ref.json'),'record_schema_path':str(ROOT/'schemas/freeze_instrument_records_v1.schema.json')}; obj,ref=h.produce_attestation_input(cfg,{'runtime_instance_uuid':RU,'observation_nonce':NO,'runtime_instantiation_attestation_record_sha256':rr,'runtime_instantiation_attestation_record':record}); self.assertEqual(obj['runtime_instantiation_record'],record); self.assertTrue(all(set(x)=={'path','byte_count','sha256'} for x in obj['evidence_inputs'].values())); self.assertEqual(len(ref['sha256']),64)
    def test_023_controller_rechecks_bound_evidence_identity_before_read(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'e'; p.write_bytes(b'good'); spec={'path':str(p),'byte_count':4,'sha256':hashlib.sha256(b'good').hexdigest()}; r={'evidence_inputs':{'x':spec}}; p.write_bytes(b'evil')
            with self.assertRaises(Exception): c._objects_from_input(r,['x'])
    def test_024_qemu_transport_does_not_allow_reconnect_during_governed_interval(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); self.assertFalse(any('reconnect' in x for x in cfg['qemu_argv'])); policy=json.loads((ROOT/'config/common/ipc_and_storage_policy_v1.json').read_text()); self.assertEqual(policy['reconnect_during_governed_interval'],'PROHIBITED')
    def test_025_lifecycle_and_controller_authenticate_host_sink_acks(self):
        for rel in ('src/blocker_014/host_runtime_lifecycle_provider_v1.py','src/blocker_014/attestation_transaction_controller_v1.py'):
            src=(ROOT/rel).read_text(); self.assertIn('host_sink_peer_policy',src); self.assertIn('recv_authenticated',src); self.assertIn('bind_source(',src)
    def test_026_runtime_input_embeds_exact_runtime_record_and_controller_rechecks_hash(self):
        life=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); ctrl=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertIn("'runtime_instantiation_record':rec",life); self.assertIn("canonical_sha256(r['runtime_instantiation_record'])!=r['runtime_record_sha256']",ctrl)

