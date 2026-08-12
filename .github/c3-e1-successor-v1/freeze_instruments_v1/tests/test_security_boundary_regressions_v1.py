from __future__ import annotations
import json,os,socket,struct,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_007']: sys.path.insert(0,str(d))
from python_runtime_envelope_v1 import find_reachable_pyc
from ipc_peer_auth_v1 import parse_credentials,PeerAuthError,enable_seqpacket_credentials,recv_authenticated,stream_peercred
class T(unittest.TestCase):
 def test_pyc_rejected_inventory(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'__pycache__'; p.mkdir(); (p/'x.pyc').write_bytes(b'x'); self.assertTrue(find_reachable_pyc([td]))
 def test_missing_credentials(self): self.assertRaises(PeerAuthError,parse_credentials,[])
 def test_seqpacket_kernel_credentials(self):
  a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b); a.send(b'x'); data,cred,_=recv_authenticated(b); self.assertEqual(data,b'x'); self.assertEqual(cred.pid,os.getpid()); a.close(); b.close()
 def test_stream_peercred(self):
  a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_STREAM); self.assertEqual(stream_peercred(a).pid,os.getpid()); a.close(); b.close()
 def test_native_launcher_everywhere(self):
  for p in (ROOT/'units').glob('*.service'): self.assertIn('python_instrument_launcher_v1',p.read_text())
  self.assertIn('python_instrument_launcher_v1',(ROOT/'config/blocker_005/audit_plugin_v1.conf').read_text())
 def test_monitor_independent(self): self.assertNotIn('nftables_transition_monitor_v1',(ROOT/'src/blocker_007/observation_authority_v1.py').read_text())
if __name__=='__main__': unittest.main()
