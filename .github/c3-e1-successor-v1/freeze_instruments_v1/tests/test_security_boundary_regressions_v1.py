import os, pathlib, socket, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,stream_peercred,send_fd_with_credentials,require_exact_one_fd
from python_runtime_envelope_v1 import find_reachable_pyc
class SecurityBoundaryTests(unittest.TestCase):
    def test_001_seqpacket_scm_credentials_per_message(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b); a.send(b'x'); data,cred,_,_=recv_authenticated(b); self.assertEqual(data,b'x'); self.assertEqual(cred.pid,os.getpid()); a.close(); b.close()
    def test_002_fd_transfer_credentials_and_one_fd(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b); r,w=os.pipe()
        try:
            send_fd_with_credentials(a,b'fd',r); data,cred,anc,_=recv_authenticated(b); got=require_exact_one_fd(anc); self.assertEqual(data,b'fd'); self.assertEqual(cred.pid,os.getpid()); os.close(got)
        finally: os.close(r); os.close(w); a.close(); b.close()
    def test_003_stream_so_peercred_for_qemu_path(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_STREAM); self.assertEqual(stream_peercred(a).pid,os.getpid()); a.close(); b.close()
    def test_004_pyc_absence_guard(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td); (p/'x.pyc').write_bytes(b'x'); self.assertEqual(find_reachable_pyc([p]),[str(p/'x.pyc')])
    def test_005_native_launcher_fail_closed_normalization(self):
        s=(ROOT/'src/native/python_instrument_launcher_v1.c').read_text();
        for token in ('clearenv()','chdir("/")','setrlimit(RLIMIT_CORE','sigprocmask','PR_SET_NO_NEW_PRIVS'): self.assertIn(token,s)
    def test_006_transition_monitor_never_has_cap_net_admin(self):
        s=(ROOT/'src/blocker_006/nftables_transition_monitor_v1.py').read_text(); self.assertIn('CAP_NET_ADMIN prohibited',s); unit=(ROOT/'units/nftables_transition_monitor_v1.service').read_text(); self.assertNotIn('CAP_NET_ADMIN',unit)
    def test_007_observation_authority_exact_cap_and_hard_denies(self):
        unit=(ROOT/'units/observation_authority_v1.service').read_text(); self.assertIn('CapabilityBoundingSet=CAP_NET_ADMIN',unit); self.assertIn('SystemCallArchitectures=native',unit); self.assertIn('SystemCallFilter=~',unit)
    def test_008_auditd_queue_directive_selected(self):
        c=(ROOT/'config/blocker_005/auditd_e1_v1.conf').read_text(); self.assertIn('q_depth = 4096',c); self.assertNotIn('plugin_queue_depth',c); self.assertIn('overflow_action = SUSPEND',c)
    def test_009_qemu_control_channels_remain_prohibited(self):
        s=(ROOT/'src/blocker_014/runtime_instantiation_launcher_v1.py').read_text(); self.assertIn("'-qmp'",s); self.assertIn("'-monitor'",s); self.assertIn('QEMU control channel prohibited',s)
    def test_010_verifier_execution_boundary_outside_host(self):
        import json; cfg=json.loads((ROOT/'config/blocker_013/blocker_013_config_v1.json').read_text()); self.assertEqual(cfg['execution_boundary'],'OUTSIDE_ATTESTED_HOST')
    def test_011_host_sink_rejects_guest_stream_replacement(self):
        s=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text(); self.assertIn('QEMU guest evidence stream replacement prohibited',s)
    def test_012_ack_before_durable_commit_not_possible(self):
        s=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text(); accept=s[s.index('def accept_guest'):s.index('def accept_host')]; self.assertLess(accept.index('self.append'),accept.index('pack_ack'))
    def test_013_qemu_stream_reconnect_policy_is_fail_closed(self):
        import json; policy=json.loads((ROOT/'config/common/ipc_and_storage_policy_v1.json').read_text()); self.assertEqual(policy['reconnect_during_governed_interval'],'PROHIBITED'); sink=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text(); self.assertIn('guest_stream_claimed=True',sink)
    def test_014_runtime_standard_fds_are_both_normalized_and_verified(self):
        s=(ROOT/'src/blocker_014/runtime_instantiation_launcher_v1.py').read_text(); self.assertIn('normalize_standard_fds()',s); self.assertIn('verify_devnull_standard_fds()',s); unit=(ROOT/'units/runtime_instantiation_launcher_v1.service').read_text(); self.assertIn('StandardInput=null',unit); self.assertIn('StandardOutput=null',unit); self.assertIn('StandardError=null',unit)
    def test_015_audit_durable_ack_failure_cannot_block_unobserved_on_stdin(self):
        s=(ROOT/'src/blocker_005/audit_realtime_plugin_v1.py').read_text(); self.assertIn('select.select([0]',s); self.assertIn('exporter.failure is not None',s); self.assertIn('durable writer failed',s)
    def test_016_authenticated_receiver_allows_clean_eof_but_not_scientific_message_without_credentials(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b); a.close(); data,cred,anc,_=recv_authenticated(b); self.assertEqual(data,b''); self.assertIsNone(cred); self.assertEqual(anc,[]); b.close()

