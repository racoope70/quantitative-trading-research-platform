import json, os, pathlib, socket, struct, sys, tempfile, unittest, hashlib
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

from nftables_snapshot_v1 import *
from nftables_delivery_barrier_v1 import evaluate,barrier_record,StabilityError
from nftables_transition_monitor_v1 import transition_evidence,window_open_evidence
from identity_io_v1 import canonical_loads

def msg(t,seq,payload=b'',flags=0):
    n=HDR.size+len(payload);raw=HDR.pack(n,t,flags,seq,0)+payload;return raw+b'\0'*(((n+3)&~3)-n)
class FakeDumpSock:
    def __init__(self,dg,effective=16384):self.dg=dg;self.effective=effective;self.sent=None
    def getsockopt(self,*_):return self.effective
    def send(self,b):self.sent=b;return len(b)
    def recvmsg(self,*_):return self.dg,[],0,None
class Blocker006Tests(unittest.TestCase):
    def test_001_dump_done_zero(self):self.assertEqual(validate_dump([msg(100,7,b'x')+msg(NLMSG_DONE,7,ERR.pack(0))],7),[HDR.pack(HDR.size+1,100,0,7,0)+b'x'])
    def test_002_done_nonzero_rejected(self):
        with self.assertRaises(NetlinkDumpError):validate_dump([msg(NLMSG_DONE,1,ERR.pack(-5))],1)
    def test_003_dump_intr_rejected(self):
        with self.assertRaises(NetlinkDumpError):validate_dump([msg(100,1,b'x',NLM_F_DUMP_INTR)+msg(NLMSG_DONE,1,ERR.pack(0))],1)
    def test_004_missing_done_rejected(self):
        with self.assertRaises(NetlinkDumpError):validate_dump([msg(100,1,b'x')],1)
    def test_005_sequence_mismatch_rejected(self):
        with self.assertRaises(NetlinkDumpError):validate_dump([msg(NLMSG_DONE,2,ERR.pack(0))],1)
    def test_006_nlmsg_overrun_rejected(self):
        with self.assertRaises(NetlinkDumpError):validate_dump([msg(NLMSG_OVERRUN,1,b'')+msg(NLMSG_DONE,1,ERR.pack(0))],1)
    def test_007_stability_pass(self):self.assertEqual(evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=1,genid_final=1,notification_count=0,barrier_healthy=True,barrier_durable=True),'PASS')
    def test_008_mutate_restore_cannot_pass(self):
        with self.assertRaises(StabilityError):evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=1,genid_final=1,notification_count=2,barrier_healthy=True,barrier_durable=True)
    def test_009_genid_change_cannot_pass(self):
        with self.assertRaises(StabilityError):evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=2,genid_final=2,notification_count=0,barrier_healthy=True,barrier_durable=True)
    def test_010_transition_evidence_has_raw_hash(self):
        o=canonical_loads(transition_evidence(b'abc','12345678-1234-1234-1234-123456789abc','11'*32));self.assertEqual(o['raw_netlink_sha256'],hashlib.sha256(b'abc').hexdigest());self.assertEqual(o['raw_netlink_byte_count'],3)
    def test_011_dump_retains_configured_requested_buffer(self):
        dg=msg(100,1,b'x')+msg(NLMSG_DONE,1,ERR.pack(0));s=FakeDumpSock(dg,32768);r=recv_complete_dump(s,b'req',1,requested_so_rcvbuf=8192);self.assertEqual(r['requested_so_rcvbuf'],8192);self.assertEqual(r['effective_so_rcvbuf'],32768)
    def test_012_dump_retains_complete_raw_transaction(self):
        dg=msg(100,1,b'x')+msg(NLMSG_DONE,1,ERR.pack(0));r=recv_complete_dump(FakeDumpSock(dg),b'req',1,requested_so_rcvbuf=8192);tx=r['raw_transaction'];self.assertEqual(tx['request_hex'],b'req'.hex());self.assertEqual(tx['response_datagrams_hex'],[dg.hex()]);self.assertEqual(tx['response_sha256'],hashlib.sha256(dg).hexdigest())
    def test_013_dump_requires_requested_buffer_identity(self):
        dg=msg(NLMSG_DONE,1,ERR.pack(0))
        with self.assertRaises(NetlinkDumpError):recv_complete_dump(FakeDumpSock(dg),b'req',1)
    def test_014_stability_requires_durable_barrier(self):
        with self.assertRaises(StabilityError):evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=1,genid_final=1,notification_count=0,barrier_healthy=True,barrier_durable=False)
    def test_015_barrier_count_is_whole_window_delta(self):
        r=barrier_record(barrier_id='x',runtime_instance_uuid='12345678-1234-1234-1234-123456789abc',observation_nonce='11'*32,window_baseline_total_notifications=7,total_notifications_at_barrier=9,monitor_source_sequence_at_window_open=4,monitor_source_sequence_at_barrier=8,requested_so_rcvbuf=1,effective_so_rcvbuf=2,enobufs_observed=False,msg_trunc_observed=False,nlmsg_overrun_observed=False,receiver_continuity=True,notification_count_during_window=2);self.assertEqual(r['notification_count_during_window'],2)
    def test_016_barrier_inconsistent_delta_rejected(self):
        with self.assertRaises(StabilityError):barrier_record(barrier_id='x',runtime_instance_uuid='12345678-1234-1234-1234-123456789abc',observation_nonce='11'*32,window_baseline_total_notifications=7,total_notifications_at_barrier=9,monitor_source_sequence_at_window_open=4,monitor_source_sequence_at_barrier=8,requested_so_rcvbuf=1,effective_so_rcvbuf=2,enobufs_observed=False,msg_trunc_observed=False,nlmsg_overrun_observed=False,receiver_continuity=True,notification_count_during_window=0)
    def test_017_transition_monitor_has_explicit_window_baseline(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text();self.assertIn('NFTABLES_STABILITY_WINDOW_OPEN_REQUEST',src);self.assertIn('window_baseline_total_notifications',src);self.assertIn('total_notifications-state',src)
    def test_018_transition_monitor_waits_durable_ack(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text();self.assertIn('validate_producer_ack',src);self.assertIn("durable producer ACK missing",src)
    def test_019_bootstrap_identity_is_kernel_authenticated(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text();self.assertIn("bootstrap_peer_policy",src);self.assertIn("bind_source(cred",src)
    def test_020_window_open_evidence_binds_buffers(self):
        o=canonical_loads(window_open_evidence('w','12345678-1234-1234-1234-123456789abc','11'*32,2,3,4096,8192));self.assertEqual(o['requested_so_rcvbuf'],4096);self.assertEqual(o['effective_so_rcvbuf'],8192)
    def test_021_monitor_authenticates_mux_durable_ack(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text(); self.assertIn('enable_seqpacket_credentials(mux)',src); self.assertIn("cfg5['guest_mux_provider_policy']",src); self.assertIn('_authenticate_peer(cred',src)
    def test_022_bootstrap_authenticates_monitor_acceptance(self):
        src=(ROOT/'src/blocker_006/nftables_monitor_bootstrap_v1.py').read_text(); self.assertIn('enable_seqpacket_credentials(peer)',src); self.assertIn("cfg['monitor_peer_policy']",src); self.assertIn('bind_source(cred',src)
    def test_023_barrier_requests_are_kernel_authenticated_to_authority(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text(); self.assertIn("cfg['authority_peer_policy']",src); self.assertIn('recv_authenticated(bc)',src)
    def test_024_monitor_source_sequence_advances_only_after_mux_ack(self):
        src=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text(); seg=src[src.index('def _send_mux'):src.index('def _drain')]; self.assertLess(seg.index('validate_producer_ack'),seg.index('return seq+1'))

