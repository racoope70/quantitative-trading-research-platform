import json, os, pathlib, socket, struct, sys, tempfile, unittest, threading, hashlib
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

from evidence_protocol_v1 import *
from audit_string_framing_v1 import LineFramer,FramingError
from durable_journal_v1 import DurableJournal
from ipc_peer_auth_v1 import enable_seqpacket_credentials
from identity_io_v1 import canonical_bytes,canonical_loads
import host_evidence_sink_v1 as hs
import guest_evidence_multiplexer_v1 as gm
RU='12345678-1234-1234-1234-123456789abc'; NO='11'*32; RR='22'*32
class Blocker005Tests(unittest.TestCase):
    def test_001_guest_frame_roundtrip(self):
        f=pack_guest_frame(2,7,b'{}',b'raw');d=unpack_guest_frame(f);self.assertEqual((d['source_type'],d['guest_sequence'],d['raw_evidence']),(2,7,b'raw'))
    def test_002_guest_metadata_requires_raw_sha(self):
        md={'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_identity':'src','source_sequence':0,'source_native_identity':'inst','guest_boot_id':'boot','guest_monotonic_timestamp_ns':1,'raw_evidence_byte_count':3,'raw_evidence_sha256':'00'*32}
        with self.assertRaises(ProtocolError):validate_guest_metadata(md,source_type=1,raw_evidence=b'raw',expected_runtime_uuid=RU,expected_nonce=NO)
    def test_003_guest_metadata_host_runtime_binding(self):
        raw=b'x';md={'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_identity':'src','source_sequence':0,'source_native_identity':'inst','guest_boot_id':'boot','guest_monotonic_timestamp_ns':1,'raw_evidence_byte_count':1,'raw_evidence_sha256':hashlib.sha256(raw).hexdigest()}
        with self.assertRaises(ProtocolError):validate_guest_metadata({**md,'runtime_instance_uuid':'22345678-1234-1234-1234-123456789abc'},source_type=1,raw_evidence=raw,expected_runtime_uuid=RU,expected_nonce=NO)
    def test_004_ack_bound_to_transaction(self):
        frame=b'frame';a=unpack_ack(pack_ack(guest_sequence=0,source_sequence=0,host_sequence=4,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_sha256=hashlib.sha256(frame).digest(),record_sha256=bytes.fromhex('33'*32)))
        validate_ack(a,guest_sequence=0,source_sequence=0,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_bytes=frame)
        with self.assertRaises(ProtocolError):validate_ack(a,guest_sequence=0,source_sequence=0,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',transaction_bytes=b'other')
    def test_005_host_ack_bound_to_source_and_runtime(self):
        payload=b'p';a=make_host_ack(runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',source_sequence=2,host_sequence=9,payload=payload,record_sha256='44'*32)
        validate_host_ack(a,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',source_sequence=2,payload=payload)
        with self.assertRaises(ProtocolError):validate_host_ack(a,runtime_instance_uuid=RU,observation_nonce='55'*32,source_instance_identity='src',source_sequence=2,payload=payload)
    def test_006_local_packet_roundtrip(self):
        p=unpack_local_packet(pack_local_packet(1,2,RU,NO,b'abc'));self.assertEqual((p['source_sequence'],p['runtime_instance_uuid'],p['raw_evidence']),(2,RU,b'abc'))
    def test_007_sequence_gap_rejected(self):
        with self.assertRaises(ProtocolError):SequenceState().consume(1)
    def test_008_audit_framer_fragmented_and_exact_lf(self):
        f=LineFramer(20);self.assertEqual(f.feed(b'ab'),[]);self.assertEqual(f.feed(b'c\ndef\n'),[b'abc\n',b'def\n']);f.finish()
    def test_009_audit_framer_partial_eof(self):
        f=LineFramer(20);f.feed(b'partial')
        with self.assertRaises(FramingError):f.finish()
    def test_010_audit_framer_limit(self):
        f=LineFramer(3)
        with self.assertRaises(FramingError):f.feed(b'abcd')
    def test_011_host_hash_binds_timestamps(self):
        kw=dict(origin=ORIGIN_HOST,host_sequence=0,previous_sha256=b'\0'*32,payload=b'x')
        self.assertNotEqual(host_record_hash(monotonic_ns=1,utc_ns=2,**kw),host_record_hash(monotonic_ns=2,utc_ns=2,**kw))
    def test_012_durable_journal_returns_only_after_commit(self):
        with tempfile.TemporaryDirectory() as td:
            j=DurableJournal(pathlib.Path(td)/'j',pathlib.Path(td)/'h',canonical_bytes);r=j.commit(origin=ORIGIN_HOST,host_sequence=0,monotonic_ns=1,utc_ns=2,previous_sha256=b'\0'*32,payload=b'x',runtime_instance_uuid=RU);j.close()
            self.assertTrue(r['durable']);self.assertTrue((pathlib.Path(td)/'h').is_file())
    def test_013_producer_ack_roundtrip_binding(self):
        host={'guest_sequence':3,'source_sequence':2,'host_sequence':9,'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_sha256':source_instance_digest('src').hex(),'transaction_sha256':'44'*32,'record_sha256':'55'*32}
        packet=b'local-packet';ack=producer_ack_from_host(host,packet);validate_producer_ack(ack,source_sequence=2,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',producer_transaction_bytes=packet)
    def test_014_producer_ack_wrong_source_rejected(self):
        host={'guest_sequence':3,'source_sequence':2,'host_sequence':9,'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_sha256':source_instance_digest('src').hex(),'transaction_sha256':'44'*32,'record_sha256':'55'*32}
        with self.assertRaises(ProtocolError):validate_producer_ack(producer_ack_from_host(host,b'packet'),source_sequence=2,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='other',producer_transaction_bytes=b'packet')
    def test_015_start_token_binds_observation_start_sequence(self):
        token=unpack_start_token(pack_start_token(RU,NO,'11'*32,RR,4,5));self.assertEqual(token['observation_start_host_sequence'],5);self.assertEqual(token['host_sequence_of_durable_verifier_result'],4)
    def test_016_guest_transport_uses_frozen_virtio_device(self):
        src=(ROOT/'src/blocker_005/guest_evidence_multiplexer_v1.py').read_text();self.assertIn('open_guest_virtio_serial',src);self.assertIn("'/dev/virtio-ports/'",src);self.assertNotIn("channel=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)",src)
    def test_017_guest_mux_accepts_concurrent_producers(self):
        src=(ROOT/'src/blocker_005/guest_evidence_multiplexer_v1.py').read_text();self.assertIn('threading.Thread(target=_serve_producer_connection',src);self.assertIn('self.send_lock',src)
    def test_018_guest_mux_serializes_global_guest_sequence(self):
        src=(ROOT/'src/blocker_005/guest_evidence_multiplexer_v1.py').read_text();self.assertLess(src.index('with self.send_lock:'),src.index('gseq=self.guest_seq'));self.assertIn('self.guest_seq+=1',src)
    def test_019_audit_has_bounded_queue_writer(self):
        src=(ROOT/'src/blocker_005/audit_realtime_plugin_v1.py').read_text();self.assertIn('queue.Queue(maxsize=',src);self.assertIn('queue.Full',src);self.assertIn('c3-e1-audit-durable-writer',src)
    def test_020_audit_advances_only_after_durable_ack(self):
        src=(ROOT/'src/blocker_005/audit_realtime_plugin_v1.py').read_text();self.assertLess(src.index('validate_producer_ack'),src.index('self.seq+=1'))
    def test_021_host_sink_persistent_host_connection(self):
        src=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text();start=src.index('def _handle_host_connection');segment=src[start:src.index('def main',start)];self.assertIn('while True:',segment);self.assertIn('recv_authenticated(conn)',segment)
    def test_022_host_sink_reauthenticates_each_message(self):
        src=(ROOT/'src/blocker_005/host_evidence_sink_v1.py').read_text();self.assertIn("host connection source identity changed",src);self.assertIn('bind_source(cred',src)
    def test_023_producer_ack_wrong_local_transaction_rejected(self):
        host={'guest_sequence':3,'source_sequence':2,'host_sequence':9,'runtime_instance_uuid':RU,'observation_nonce':NO,'source_instance_sha256':source_instance_digest('src').hex(),'transaction_sha256':'44'*32,'record_sha256':'55'*32}
        ack=producer_ack_from_host(host,b'packet')
        with self.assertRaises(ProtocolError): validate_producer_ack(ack,source_sequence=2,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity='src',producer_transaction_bytes=b'other')
    def test_024_mux_handle_concurrent_sources_serializes_global_sequence(self):
        class Channel:
            def __init__(self): self.frames=[]
            def sendall(self,b): self.frames.append(bytes(b))
        ch=Channel(); mux=gm.GuestMultiplexer(ch,[],{'runtime_instance_uuid':RU,'observation_nonce':NO,'runtime_instantiation_attestation_record_sha256':RR}); mux._boot=lambda:'boot'
        mux.authenticate_source=lambda cred,stype: ({'instrument_identity':f'INST{stype}'},f'src{stype}')
        def wait(gseq):
            d=unpack_guest_frame(ch.frames[gseq]); md=canonical_loads(d['metadata_bytes'])
            return unpack_ack(pack_ack(guest_sequence=gseq,source_sequence=md['source_sequence'],host_sequence=gseq,runtime_instance_uuid=RU,observation_nonce=NO,source_instance_identity=md['source_instance_identity'],transaction_sha256=hashlib.sha256(ch.frames[gseq]).digest(),record_sha256=bytes.fromhex('55'*32)))
        mux._wait_ack=wait; out=[]
        threads=[threading.Thread(target=lambda st=st: out.append(mux.handle(pack_local_packet(st,0,RU,NO,b'x'),object()))) for st in (1,2)]
        [t.start() for t in threads]; [t.join() for t in threads]
        self.assertEqual(mux.guest_seq,2); self.assertEqual(sorted(unpack_guest_frame(f)['guest_sequence'] for f in ch.frames),[0,1]); self.assertEqual(len(out),2)
    def test_025_host_sink_processes_multiple_packets_on_one_connection(self):
        class State:
            ru=RU; no=NO
            def accept_host(self,payload,identity,instrument,seq):
                obj=canonical_loads(payload); src=f"{instrument}:1:2:{'11'*32}:{'22'*32}:{'33'*32}"; return {'host_sequence':seq,'record_sha256':'44'*32},src,obj
        a,b=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(b)
        policy={'uid':os.getuid(),'gid':os.getgid(),'instrument_identity':'TEST','expected_process':{}}
        ident={'pid':1,'starttime':2,'executable_sha256':'11'*32,'cmdline_sha256':'22'*32,'cgroup_sha256':'33'*32}
        with mock.patch.object(hs,'_match_policy',return_value=policy), mock.patch.object(hs,'bind_source',return_value=ident):
            t=threading.Thread(target=hs._handle_host_connection,args=(State(),{},b),daemon=True); t.start()
            for seq in (0,1):
                obj={'record_type':'X','runtime_instance_uuid':RU,'observation_nonce':NO}; a.send(canonical_bytes({'_transport_source_sequence':seq,**obj})); raw=a.recv(65536); self.assertTrue(canonical_loads(raw)['durable'])
            a.close(); t.join(timeout=1); self.assertFalse(t.is_alive())
    def test_026_audit_ack_path_authenticates_mux_and_polls_writer_health(self):
        src=(ROOT/'src/blocker_005/audit_realtime_plugin_v1.py').read_text(); self.assertIn('enable_seqpacket_credentials(sock)',src); self.assertIn('guest_mux_provider_policy',src); self.assertIn('bind_source(cred',src); self.assertIn('select.select([0]',src)

