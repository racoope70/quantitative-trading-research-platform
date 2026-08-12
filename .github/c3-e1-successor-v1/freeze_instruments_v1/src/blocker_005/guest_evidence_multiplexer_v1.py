from __future__ import annotations
import socket,time
from evidence_protocol_v1 import pack_guest_frame,unpack_local_packet,unpack_ack,recv_exact
from ipc_peer_auth_v1 import bind_source
from identity_io_v1 import canonical_bytes,read_json,assert_resolved
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_GUEST_EVIDENCE_MULTIPLEXER_V1'
class MultiplexerError(RuntimeError): pass
class Sequencer:
    def __init__(self): self.guest=0; self.sources={}
    def accept(self,source_instance,source_sequence):
        exp=self.sources.get(source_instance,0)
        if source_sequence!=exp: raise MultiplexerError('source sequence mismatch')
        self.sources[source_instance]=exp+1; g=self.guest; self.guest+=1; return g
class GuestMultiplexer:
    def __init__(self,channel,producer_policy,runtime_uuid,nonce): self.channel=channel; self.policy=producer_policy; self.runtime_uuid=runtime_uuid; self.nonce=nonce; self.seq=Sequencer()
    def handle_packet(self,packet,cred):
        item=unpack_local_packet(packet)
        matches=[x for x in self.policy if x['uid']==cred.uid and x['gid']==cred.gid and x['source_type']==item['source_type']]
        if len(matches)!=1: raise MultiplexerError('producer mapping not unique')
        src=matches[0]; bound=bind_source(cred,src['uid'],src['gid']); source_instance=f"{src['instrument_identity']}:{bound['pid']}:{bound['starttime']}"
        g=self.seq.accept(source_instance,item['source_sequence'])
        md=canonical_bytes({'runtime_instance_uuid':self.runtime_uuid,'observation_nonce':self.nonce,'source_instance_identity':source_instance,'source_sequence':item['source_sequence'],'source_native_identity':src['instrument_identity'],'guest_boot_id':src.get('guest_boot_id','UNRESOLVED_RUNTIME'),'guest_monotonic_timestamp_ns':time.monotonic_ns(),'raw_evidence_byte_count':len(item['raw_evidence'])})
        self.channel.sendall(pack_guest_frame(item['source_type'],g,md,item['raw_evidence']))
        ack=unpack_ack(recv_exact(self.channel,52))
        if ack['guest_sequence']!=g: raise MultiplexerError('ACK mismatch')
        return ack

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); assert_resolved(cfg,'blocker_005_config')
    raise SystemExit('runtime channel and producer policy require governed binding')
if __name__=='__main__': main()
