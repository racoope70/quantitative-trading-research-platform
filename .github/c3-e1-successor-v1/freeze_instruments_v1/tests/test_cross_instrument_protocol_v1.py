import json, os, pathlib, socket, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

from identity_io_v1 import validate_schema_file,IdentityError,read_json
class CrossInstrumentTests(unittest.TestCase):
    def test_001_exact_59_path_inventory(self): self.assertEqual(len([p for p in ROOT.rglob('*') if p.is_file()]),59)
    def test_002_group_arithmetic_23_13_23(self):
        tests=list((ROOT/'tests').glob('test_*_v1.py')); self.assertEqual(len(tests),7); self.assertEqual(23+13+23,59)
    def test_003_all_units_use_native_launcher(self):
        for p in (ROOT/'units').glob('*.service'): self.assertIn('python_instrument_launcher_v1',p.read_text(),p.name)
    def test_004_host_guest_source_separation(self):
        host=(ROOT/'src/blocker_014/host_runtime_lifecycle_provider_v1.py').read_text(); mux=(ROOT/'src/blocker_005/guest_evidence_multiplexer_v1.py').read_text(); self.assertIn("host_sink_socket",host); self.assertNotIn('HOST_RUNTIME_LIFECYCLE_PROVIDER',mux)
    def test_005_schema_unknown_scientific_field_fails(self):
        o={'record_type':'RUNTIME_BINDING_ESTABLISHED','runtime_instance_uuid':'12345678-1234-1234-1234-123456789abc','observation_nonce':'11'*32,'qemu_pid':1,'runtime_instantiation_attestation_record_sha256':'22'*32,'extra':1}
        with self.assertRaises(IdentityError): validate_schema_file(o,ROOT/'schemas/freeze_instrument_records_v1.schema.json')
    def test_006_qualification_root_order_is_explicit(self):
        src=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertLess(src.index('def run_post'),src.index('def main')); self.assertIn('derive_qualification_root(pre_sha,canonical_sha256(res),c[\'sha256\'])',src)
