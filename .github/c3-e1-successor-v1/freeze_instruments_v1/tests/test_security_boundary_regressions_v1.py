import json, os, pathlib, socket, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

import array, hashlib
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,stream_peercred,send_fd_with_credentials,require_exact_one_fd
from python_runtime_envelope_v1 import find_reachable_pyc,RuntimeEnvelopeError
class SecurityBoundaryTests(unittest.TestCase):
    def test_001_seqpacket_scm_credentials_per_message(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b); a.send(b'x'); data,cred,anc,_=recv_authenticated(b); self.assertEqual(data,b'x'); self.assertEqual(cred.pid,os.getpid()); a.close(); b.close()
    def test_002_fd_transfer_has_credentials_and_one_fd(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b)
        r,w=os.pipe()
        try:
            send_fd_with_credentials(a,b'fd',r); data,cred,anc,_=recv_authenticated(b); got=require_exact_one_fd(anc); self.assertEqual(data,b'fd'); self.assertEqual(cred.pid,os.getpid()); self.assertTrue(os.fstat(got)); os.close(got)
        finally: os.close(r); os.close(w); a.close(); b.close()
    def test_003_stream_so_peercred(self):
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_STREAM); self.assertEqual(stream_peercred(a).pid,os.getpid()); a.close(); b.close()
    def test_004_pyc_and_direct_bypass_guards(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td); (p/'x.pyc').write_bytes(b'x'); self.assertEqual(find_reachable_pyc([p]),[str(p/'x.pyc')])
        launch=(ROOT/'src/native/python_instrument_launcher_v1.c').read_text(); self.assertIn('clearenv()',launch); self.assertIn('if(chdir("/")!=0)',launch); self.assertIn('setrlimit(RLIMIT_CORE',launch); self.assertIn('sigprocmask',launch)
