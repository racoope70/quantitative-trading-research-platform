from __future__ import annotations
import time
from evidence_protocol_v1 import ORIGIN_GUEST,ORIGIN_HOST,recv_guest_frame,unpack_guest_frame,pack_ack
from identity_io_v1 import read_json,assert_resolved
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_HOST_EVIDENCE_SINK_V1'
class SinkState:
    def __init__(self,journal): self.journal=journal; self.seq=0; self.prev=b'\0'*32; self.sealed=False
    def append(self,origin,payload,runtime_uuid):
        if self.sealed: raise RuntimeError('observation chain sealed')
        r=self.journal.commit(origin=origin,host_sequence=self.seq,monotonic_ns=time.monotonic_ns(),utc_ns=time.time_ns(),previous_sha256=self.prev,payload=payload,runtime_instance_uuid=runtime_uuid)
        self.prev=bytes.fromhex(r['record_sha256']); self.seq+=1; return r
    def accept_guest_frame(self,stream,runtime_uuid):
        frame=recv_guest_frame(stream); decoded=unpack_guest_frame(frame); r=self.append(ORIGIN_GUEST,frame,runtime_uuid)
        stream.sendall(pack_ack(decoded['guest_sequence'],r['host_sequence'],bytes.fromhex(r['record_sha256']))); return r
    def accept_host_payload(self,payload,runtime_uuid): return self.append(ORIGIN_HOST,payload,runtime_uuid)
    def seal(self): self.sealed=True

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); assert_resolved(cfg,'blocker_005_config')
    raise SystemExit('governed evidence storage/socket identities required')
if __name__=='__main__': main()
