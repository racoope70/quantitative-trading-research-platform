import json, os, pathlib, socket, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

import identity_io_v1 as _identity_io
class _LocalCanonicalStub:
    CANONICALIZATION_IDENTITY='C3_E1_SUCCESSOR_CANONICAL_JSON_V1'
    @staticmethod
    def canonical_bytes(obj):
        return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    @staticmethod
    def load_strict_bytes(raw):
        if isinstance(raw,bytes): raw=raw.decode('utf-8')
        return json.loads(raw)

def _install_canonical_fixture(case):
    patch=mock.patch.object(_identity_io,'_canonical_module',return_value=_LocalCanonicalStub)
    patch.start(); case.addCleanup(patch.stop)

from nftables_snapshot_v1 import *
from nftables_delivery_barrier_v1 import evaluate,barrier_record,StabilityError
from nftables_transition_monitor_v1 import transition_evidence,barrier_evidence
from identity_io_v1 import canonical_loads

def msg(t,seq,payload=b'',flags=0):
    n=HDR.size+len(payload); raw=HDR.pack(n,t,flags,seq,0)+payload; return raw+b'\0'*(((n+3)&~3)-n)
class Blocker006Tests(unittest.TestCase):
    def setUp(self): _install_canonical_fixture(self)
    def test_001_dump_done_zero(self): self.assertEqual(validate_dump([msg(100,7,b'x')+msg(NLMSG_DONE,7,ERR.pack(0))],7),[HDR.pack(HDR.size+1,100,0,7,0)+b'x'])
    def test_002_done_nonzero_rejected(self):
        with self.assertRaises(NetlinkDumpError): validate_dump([msg(NLMSG_DONE,1,ERR.pack(-5))],1)
    def test_003_dump_intr_rejected(self):
        with self.assertRaises(NetlinkDumpError): validate_dump([msg(100,1,b'x',NLM_F_DUMP_INTR)+msg(NLMSG_DONE,1,ERR.pack(0))],1)
    def test_004_missing_done_rejected(self):
        with self.assertRaises(NetlinkDumpError): validate_dump([msg(100,1,b'x')],1)
    def test_005_sequence_mismatch_rejected(self):
        with self.assertRaises(NetlinkDumpError): validate_dump([msg(NLMSG_DONE,2,ERR.pack(0))],1)
    def test_006_nlmsg_overrun_rejected(self):
        with self.assertRaises(NetlinkDumpError): validate_dump([msg(NLMSG_OVERRUN,1,b'')+msg(NLMSG_DONE,1,ERR.pack(0))],1)
    def test_007_stability_pass(self): self.assertEqual(evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=1,genid_final=1,notification_count=0,barrier_healthy=True),'PASS')
    def test_008_mutate_restore_cannot_pass(self):
        with self.assertRaises(StabilityError): evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=1,genid_final=1,notification_count=2,barrier_healthy=True)
    def test_009_genid_change_cannot_pass(self):
        with self.assertRaises(StabilityError): evaluate(snapshot_a_valid=True,snapshot_b_valid=True,snapshot_a_sha256='a',snapshot_b_sha256='a',genid_open=1,genid_after_b=2,genid_final=2,notification_count=0,barrier_healthy=True)
    def test_010_transition_evidence_has_raw_hash(self):
        o=canonical_loads(transition_evidence(b'abc','12345678-1234-1234-1234-123456789abc','11'*32)); self.assertEqual(o['raw_netlink_sha256'],__import__('hashlib').sha256(b'abc').hexdigest()); self.assertEqual(o['raw_netlink_byte_count'],3)
