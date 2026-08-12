from __future__ import annotations
import sys,unittest,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_006']: sys.path.insert(0,str(d))
from nftables_snapshot_v1 import *
from nftables_delivery_barrier_v1 import evaluate,StabilityError
class T(unittest.TestCase):
 def msg(self,typ,seq,payload=b'',flags=0):
  n=16+len(payload); raw=struct.pack('IHHII',n,typ,flags,seq,0)+payload; return raw+b'\0'*((-n)%4)
 def test_done_zero(self): self.assertEqual(len(validate_dump([self.msg(100,7,b'x')+self.msg(NLMSG_DONE,7,struct.pack('i',0))],7)),1)
 def test_done_negative(self): self.assertRaises(NetlinkDumpError,validate_dump,[self.msg(NLMSG_DONE,7,struct.pack('i',-5))],7)
 def test_dump_intr(self): self.assertRaises(NetlinkDumpError,validate_dump,[self.msg(100,7,b'x',NLM_F_DUMP_INTR)+self.msg(NLMSG_DONE,7,struct.pack('i',0))],7)
 def test_mutate_restore(self): self.assertRaises(StabilityError,evaluate,snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='x',snapshot_b_sha256='x',genid_open=1,genid_after_b=1,genid_final=1,notification_count=2,barrier_healthy=True)
if __name__=='__main__': unittest.main()
