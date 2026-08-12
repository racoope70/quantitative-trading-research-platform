from __future__ import annotations
import sys,tempfile,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005']: sys.path.insert(0,str(d))
from evidence_protocol_v1 import *
from audit_string_framing_v1 import LineFramer,FramingError
from durable_journal_v1 import DurableJournal
class T(unittest.TestCase):
 def test_frame(self):
  f=pack_guest_frame(1,0,b'{}',b'x\n'); self.assertEqual(unpack_guest_frame(f)['raw_evidence'],b'x\n')
 def test_chain(self):
  p=host_record_preimage(ORIGIN_GUEST,0,1,2,b'\0'*32,b'x'); self.assertEqual(host_record_hash(origin=ORIGIN_GUEST,host_sequence=0,monotonic_ns=1,utc_ns=2,previous_sha256=b'\0'*32,payload=b'x'),hashlib.sha256(p).digest())
 def test_framing(self):
  f=LineFramer(); self.assertEqual(f.feed(b'a\nb\n'),[b'a\n',b'b\n']); f.finish()
 def test_durable(self):
  with tempfile.TemporaryDirectory() as td:
   j=DurableJournal(Path(td)/'j',Path(td)/'h',lambda o:(str(sorted(o.items()))+'\n').encode()); r=j.commit(origin=ORIGIN_HOST,host_sequence=0,monotonic_ns=1,utc_ns=2,previous_sha256=b'\0'*32,payload=b'data',runtime_instance_uuid='u'); self.assertTrue(r['durable']); j.close()
if __name__=='__main__': unittest.main()
