from __future__ import annotations
import hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_013']: sys.path.insert(0,str(d))
from measured_boot_replay_v1 import replay_sha256_events
from ima_replay_v1 import replay_template_digests
from ak_provenance_v1 import verify_binding
class T(unittest.TestCase):
 def test_replay(self):
  ds=[b'a'*32,b'b'*32]; p=b'\0'*32
  for d in ds: p=hashlib.sha256(p+d).digest()
  self.assertEqual(replay_sha256_events(ds),p); self.assertEqual(replay_template_digests(ds),p)
 def test_ak(self):
  r={'attestation_key_public_identity':'a','endorsement_key_public_identity':'e','physical_host_identity':'h'}; self.assertEqual(verify_binding(r,r),'PASS')
if __name__=='__main__': unittest.main()
