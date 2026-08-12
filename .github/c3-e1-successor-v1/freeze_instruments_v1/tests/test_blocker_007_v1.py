import json, os, pathlib, socket, struct, sys, tempfile, unittest, hashlib
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

import observation_authority_v1 as a
from nftables_delivery_barrier_v1 import StabilityError
class Blocker007Tests(unittest.TestCase):
    def test_001_exact_capability_boundary(self):
        with mock.patch.object(a,'effective_caps',return_value=1<<a.CAP_NET_ADMIN):a.assert_capability_boundary()
    def test_002_extra_capability_rejected(self):
        with mock.patch.object(a,'effective_caps',return_value=(1<<a.CAP_NET_ADMIN)|1):
            with self.assertRaises(a.AuthorityError):a.assert_capability_boundary()
    def test_003_fixed_file_identity(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x';p.write_bytes(b'abc');out=a.collect_fixed_files([{'role':'x','path':str(p),'sha256':hashlib.sha256(b'abc').hexdigest()}]);self.assertEqual(out[0]['byte_count'],3)
    def test_004_wrong_fixed_file_identity(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x';p.write_bytes(b'abc')
            with self.assertRaises(Exception):a.collect_fixed_files([{'role':'x','path':str(p),'sha256':'00'*32}])
    def test_005_decode_genid(self):self.assertEqual(a.decode_genid(b'\0'*16+b'\0\0\0\x05',{'width_bits':32,'byteorder':'big','payload_offset':16}),5)
    def test_006_snapshot_identity_deterministic(self):self.assertEqual(a.snapshot_identity({'records':[b'a',b'b']}),hashlib.sha256(b'ab').hexdigest())
    def test_007_perform_stability_whole_window_zero(self):
        snap=lambda _:{'valid':True,'sha256':'aa','raw_transaction':{}}
        vals=iter([(7,{}),(7,{}),(7,{})]);opened={'window_baseline_total_notifications':4};bar=lambda _:{'notification_count_during_window':0,'healthy':True,'durable_ack_record_sha256':'11'*32}
        out=a.perform_firewall_stability(snap,lambda:next(vals),lambda:opened,bar);self.assertEqual(out['genid_final'],7)
    def test_008_authority_does_not_import_transition_monitor(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text();self.assertNotIn('nftables_transition_monitor_v1',src);self.assertIn('nftables_snapshot_v1',src)
    def test_009_authority_consumes_start_gate_before_observation(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text();main=src[src.index('def main():'):];self.assertLess(main.index('consume_start_gate'),main.index('collect_fixed_files'));self.assertLess(main.index('consume_start_gate'),main.index('run_firewall_stability'))
    def test_010_authority_validates_producer_ack(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text();self.assertIn('validate_producer_ack',src);self.assertIn('durable producer ACK missing',src)
    def test_011_authority_persists_observation_boundaries_from_ack(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text();self.assertIn("'observation_start_host_sequence':token['observation_start_host_sequence']",src);self.assertIn("'observation_end_host_sequence':ack2['host_sequence']",src)
    def test_012_authority_retains_raw_snapshot_transactions(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text();self.assertIn('snapshot_a_raw_transaction',src);self.assertIn('snapshot_b_raw_transaction',src);self.assertIn('getgen_raw_transactions',src)
    def test_013_service_enforces_native_architecture(self):
        unit=(ROOT/'units/observation_authority_v1.service').read_text();self.assertIn('SystemCallArchitectures=native',unit)
    def test_014_service_enforces_all_frozen_hard_denies(self):
        unit=(ROOT/'units/observation_authority_v1.service').read_text();manifest=json.loads((ROOT/'config/blocker_007/dac_seccomp_manifest_v1.json').read_text())
        self.assertIn('SystemCallFilter=~',unit)
        for syscall in manifest['hard_denied_syscalls']:self.assertIn(syscall,unit)
    def test_015_service_exact_cap_net_admin_only(self):
        unit=(ROOT/'units/observation_authority_v1.service').read_text();self.assertIn('CapabilityBoundingSet=CAP_NET_ADMIN',unit);self.assertIn('AmbientCapabilities=CAP_NET_ADMIN',unit)
    def test_016_final_getgen_occurs_before_closing_transition_barrier(self):
        calls=[]
        def snap(label): calls.append('snapshot_'+label); return {'valid':True,'sha256':'x'}
        vals=iter([(1,{'g':0}),(1,{'g':1}),(1,{'g':2})])
        def gen(): calls.append('getgen'); return next(vals)
        def opened(): calls.append('open'); return {'x':1}
        def barrier(_): calls.append('barrier'); return {'notification_count_during_window':0,'healthy':True,'durable_ack_record_sha256':'11'*32}
        a.perform_firewall_stability(snap,gen,opened,barrier); self.assertEqual(calls[-2:],['getgen','barrier'])
    def test_017_start_gate_response_authenticates_guest_mux(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text(); seg=src[src.index('def consume_start_gate'):src.index('def _send')]; self.assertIn('enable_seqpacket_credentials(s)',seg); self.assertIn("cfg5['guest_mux_provider_policy']",seg); self.assertIn('bind_source(cred',seg)
    def test_018_authority_scientific_ack_authenticates_guest_mux(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text(); seg=src[src.index('def _send'):src.index('def main')]; self.assertIn('recv_authenticated(mux)',seg); self.assertIn("cfg5['guest_mux_provider_policy']",seg)
    def test_019_observation_end_boundary_comes_from_durable_evidence_ack(self):
        src=(ROOT/'src/blocker_007/observation_authority_v1.py').read_text(); self.assertIn("'observation_end_host_sequence':ack2['host_sequence']",src)

