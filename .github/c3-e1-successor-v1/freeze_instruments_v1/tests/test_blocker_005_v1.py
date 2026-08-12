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

import hashlib
from evidence_protocol_v1 import *
from audit_string_framing_v1 import LineFramer,FramingError
from durable_journal_v1 import DurableJournal
from identity_io_v1 import canonical_bytes,canonical_loads

RU='12345678-1234-1234-1234-123456789abc'; NO='11'*32; RR='22'*32
class Blocker005Tests(unittest.TestCase):
    def setUp(self): _install_canonical_fixture(self)
    def test_001_guest_frame_roundtrip(self):
        f=pack_guest_frame(2,7,b'{}',b'raw'); d=unpack_guest_frame(f); self.assertEqual((d['source_type'],d['guest_sequence'],d['raw_evidence']),(2,7,b'raw'))
    def test_002_guest_metadata_requires_raw_sha(self):
        md={'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_identity':'src','source_sequence':0,'source_native_identity':'inst','guest_boot_id':'boot','guest_monotonic_timestamp_ns':1,'raw_evidence_byte_count':3,'raw_evidence_sha256':'00'*32}
        with self.assertRaises(ProtocolError): validate_guest_metadata(md,source_type=1,raw_evidence=b'raw',expected_runtime_uuid=RU,expected_nonce=NO)
    def test_003_guest_metadata_host_runtime_binding(self):
        raw=b'x'; md={'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_identity':'src','source_sequence':0,'source_native_identity':'inst','guest_boot_id':'boot','guest_monotonic_timestamp_ns':1,'raw_evidence_byte_count':1,'raw_evidence_sha256':hashlib.sha256(raw).hexdigest()}
        with self.assertRaises(ProtocolError): validate_guest_metadata({**md,'runtime_instance_uuid':'22345678-1234-1234-1234-123456789abc'},source_type=1,raw_evidence=raw,expected_runtime_uuid=RU,expected_nonce=NO)
    def test_004_ack_bound_to_transaction(self):
        frame=b'frame'; a=unpack_ack(pack_ack(guest_sequence=0,source_sequence=0,host_sequence=4,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_sha256=hashlib.sha256(frame).digest(),record_sha256=bytes.fromhex('33'*32)))
        validate_ack(a,guest_sequence=0,source_sequence=0,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_bytes=frame)
        with self.assertRaises(ProtocolError): validate_ack(a,guest_sequence=0,source_sequence=0,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_bytes=b'other')
    def test_005_host_ack_bound_to_source_and_runtime(self):
        payload=b'p'; a=make_host_ack(runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',source_sequence=2,host_sequence=9,payload=payload,record_sha256='44'*32)
        validate_host_ack(a,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',source_sequence=2,payload=payload)
        with self.assertRaises(ProtocolError): validate_host_ack(a,runtime_instance_uuid=RU,observation_nonce='55'*32,source_instance_identity='src',source_sequence=2,payload=payload)
    def test_006_local_packet_roundtrip(self):
        p=unpack_local_packet(pack_local_packet(1,2,RU,NO,b'abc')); self.assertEqual((p['source_sequence'],p['runtime_instance_uuid'],p['raw_evidence']),(2,RU,b'abc'))
    def test_007_sequence_gap_rejected(self):
        with self.assertRaises(ProtocolError): SequenceState().consume(1)
    def test_008_audit_framer_fragmented_and_exact_lf(self):
        f=LineFramer(20); self.assertEqual(f.feed(b'ab'),[]); self.assertEqual(f.feed(b'c\ndef\n'),[b'abc\n',b'def\n']); f.finish()
    def test_009_audit_framer_partial_eof(self):
        f=LineFramer(20); f.feed(b'partial')
        with self.assertRaises(FramingError): f.finish()
    def test_010_audit_framer_limit(self):
        f=LineFramer(3)
        with self.assertRaises(FramingError): f.feed(b'abcd')
    def test_011_host_hash_binds_timestamps(self):
        kw=dict(origin=ORIGIN_HOST,host_sequence=0,previous_sha256=b'\0'*32,payload=b'x')
        self.assertNotEqual(host_record_hash(monotonic_ns=1,utc_ns=2,**kw),host_record_hash(monotonic_ns=2,utc_ns=2,**kw))
    def test_012_durable_journal_returns_only_after_commit(self):
        with tempfile.TemporaryDirectory() as td:
            j=DurableJournal(pathlib.Path(td)/'j',pathlib.Path(td)/'h',canonical_bytes)
            r=j.commit(origin=ORIGIN_HOST,host_sequence=0,monotonic_ns=1,utc_ns=2,previous_sha256=b'\0'*32,payload=b'x',runtime_instance_uuid=RU); j.close()
            self.assertTrue(r['durable']); self.assertTrue((pathlib.Path(td)/'h').is_file())
