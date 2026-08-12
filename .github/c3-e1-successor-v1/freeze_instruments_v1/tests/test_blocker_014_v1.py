from __future__ import annotations
import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_014']: sys.path.insert(0,str(d))
from attestation_transaction_controller_v1 import pre_qualification,post_qualification,PRE_DOMAIN
class T(unittest.TestCase):
 def test_pre(self):
  a=b'a'*16;b=b'b'*32;c=b'c'*32;d=b'd'*32; self.assertEqual(pre_qualification(a,b,c,d),hashlib.sha256(PRE_DOMAIN+a+b+c+d).digest())
 def test_post_head_bound(self):
  args=[b'a'*16,b'b'*32,b'c'*32,3,b'd'*32,b'e'*32,1,2,b'f'*32,b'g'*32]; x=post_qualification(*args); args[4]=b'z'*32; self.assertNotEqual(x,post_qualification(*args))
 def test_fd_manifest(self):
  m=json.loads((ROOT/'config/blocker_014/qemu_inherited_fd_manifest_v1.json').read_text()); self.assertEqual(set(m['fds']),{'0','1','2','3'})
if __name__=='__main__': unittest.main()
