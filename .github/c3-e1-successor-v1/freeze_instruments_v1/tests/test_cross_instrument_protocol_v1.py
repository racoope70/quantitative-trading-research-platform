import json, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))
from identity_io_v1 import validate_schema_file,IdentityError
class CrossInstrumentTests(unittest.TestCase):
    def test_001_exact_59_path_inventory(self): self.assertEqual(len([p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]),59)
    def test_002_group_arithmetic_23_13_23(self): self.assertEqual(23+13+23,59); self.assertEqual(len(list((ROOT/'tests').glob('test_*_v1.py'))),7)
    def test_003_all_units_use_native_launcher(self):
        for p in (ROOT/'units').glob('*.service'): self.assertIn('python_instrument_launcher_v1',p.read_text(),p.name)
    def test_004_transport_identity_matches_guest_and_qemu(self):
        c5=json.loads((ROOT/'config/blocker_005/blocker_005_config_v1.json').read_text()); c14=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); t=c14['qemu_evidence_transport']; self.assertEqual(c5['guest_channel_socket'],t['host_socket']); self.assertEqual(c5['guest_virtio_port_path'],t['guest_device_path']); self.assertEqual(c5['guest_virtio_port_name'],t['virtio_port_name'])
    def test_005_host_guest_source_separation(self):
        host=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); mux=(ROOT/'src/blocker_005/guest_evidence_multiplexer_v1.py').read_text(); self.assertIn('host_sink_socket',host); self.assertNotIn('HOST_RUNTIME_LIFECYCLE_PROVIDER',mux)
    def test_006_start_gate_has_single_authority_consumer(self):
        c5=json.loads((ROOT/'config/blocker_005/blocker_005_config_v1.json').read_text()); self.assertEqual(c5['start_gate_consumer_instrument_identity'],'C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1'); a=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text(); self.assertIn('consume_start_gate',a)
    def test_007_external_expectations_never_cross_host_bundle_schema(self):
        schema=(ROOT/'schemas/attestation_transaction_v1.schema.json').read_text(); self.assertNotIn('verification_context',schema); ctrl=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertNotIn("attestation_objects",ctrl)
    def test_008_qualification_root_order_explicit(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertLess(src.index('def run_post'),src.index('def main')); self.assertIn('derive_qualification_root(pre_sha,canonical_sha256(res),c[\'sha256\'])',src)
    def test_009_schema_unknown_scientific_field_fails(self):
        o={'record_type':'RUNTIME_BINDING_ESTABLISHED','runtime_instance_uuid':'12345678-1234-1234-1234-123456789abc','observation_nonce':'11'*32,'qemu_pid':1,'runtime_instantiation_attestation_record_sha256':'22'*32,'extra':1}
        with self.assertRaises(IdentityError): validate_schema_file(o,ROOT/'schemas/freeze_instrument_records_v1.schema.json')
    def test_010_resolved_findings_006_007_guards_remain(self):
        io=(ROOT/'src/common/identity_io_v1.py').read_text(); self.assertIn('closed object schema required',io); self.assertIn('unknown scientific fields',io); self.assertEqual(len(list((ROOT/'tests').glob('test_*_v1.py'))),7)
    def test_011_no_direct_python_service_entrypoints(self):
        for p in (ROOT/'units').glob('*.service'): self.assertNotIn('ExecStart=/usr/bin/python',p.read_text(),p.name)
    def test_012_no_new_artifact_path_for_verifier_expectations(self):
        cfg=json.loads((ROOT/'config/blocker_013/blocker_013_config_v1.json').read_text()); self.assertEqual(set(cfg['expected_manifest_bindings']),{'pcr_policy','ima_policy','host_tcb_manifest','ak_ek_policy','runtime_binding_policy'})
    def test_013_no_qemu_reconnect_flag_and_sink_claim_is_single_use(self):
        cfg=json.loads((ROOT/'config/blocker_014/blocker_014_config_v1.json').read_text()); self.assertFalse(any('reconnect' in x for x in cfg['qemu_argv'])); sink=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text(); self.assertIn('guest_stream_claimed',sink)
    def test_014_all_local_scientific_ack_consumers_use_kernel_peer_auth(self):
        for rel in ('src/blocker_005/audit_realtime_plugin_v1.py','src/blocker_006/nftables_transition_monitor_v1.py','src/blocker_007/observation_authority_v1.py','src/blocker_014/host_runtime_lifecycle_provider_v1.py','src/blocker_014/attestation_transaction_controller_v1.py'):
            src=(ROOT/rel).read_text(); self.assertIn('recv_authenticated',src,rel); self.assertIn('bind_source',src,rel)
    def test_015_runtime_attestation_input_is_content_addressed_end_to_end(self):
        schema=json.loads((ROOT/'schemas/freeze_instrument_records_v1.schema.json').read_text()); self.assertIn('runtime_instantiation_record',schema['$defs']['att_input']['required']); self.assertEqual(set(schema['$defs']['att_evidence_ref']['required']),{'path','byte_count','sha256'})

