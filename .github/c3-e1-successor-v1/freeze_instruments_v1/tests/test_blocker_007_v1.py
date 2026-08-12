import json, os, pathlib, socket, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

import hashlib
import observation_authority_v1 as a
from nftables_delivery_barrier_v1 import StabilityError
class Blocker007Tests(unittest.TestCase):
    def test_001_exact_capability_boundary(self):
        with mock.patch.object(a,'effective_caps',return_value=1<<a.CAP_NET_ADMIN): a.assert_capability_boundary()
    def test_002_extra_capability_rejected(self):
        with mock.patch.object(a,'effective_caps',return_value=(1<<a.CAP_NET_ADMIN)|1):
            with self.assertRaises(a.AuthorityError): a.assert_capability_boundary()
    def test_003_fixed_file_identity(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x'; p.write_bytes(b'abc'); out=a.collect_fixed_files([{'role':'x','path':str(p),'sha256':hashlib.sha256(b'abc').hexdigest()}]); self.assertEqual(out[0]['byte_count'],3)
    def test_004_wrong_fixed_file_identity(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x'; p.write_bytes(b'abc')
            with self.assertRaises(Exception): a.collect_fixed_files([{'role':'x','path':str(p),'sha256':'00'*32}])
    def test_005_decode_genid(self): self.assertEqual(a.decode_genid(b'\0'*16+b'\0\0\0\x05',{'width_bits':32,'byteorder':'big','payload_offset':16}),5)
    def test_006_snapshot_identity_deterministic(self): self.assertEqual(a.snapshot_identity({'records':[b'a',b'b']}),hashlib.sha256(b'ab').hexdigest())
    def test_007_perform_stability_delegates_zero_mutation(self):
        snap=lambda _: {'valid':True,'sha256':'aa'}; vals=iter([7,7,7]); out=a.perform_firewall_stability(snap,lambda:next(vals),lambda:{'notification_count':0,'healthy':True}); self.assertEqual(out['genid_final'],7)
    def test_008_authority_does_not_import_transition_monitor(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text(); self.assertNotIn('nftables_transition_monitor_v1',src); self.assertIn('nftables_snapshot_v1',src)
