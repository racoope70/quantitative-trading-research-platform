from __future__ import annotations
import hashlib, os, socket, threading, time
from evidence_protocol_v1 import *
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,bind_source
from identity_io_v1 import canonical_bytes,read_json,durable_write
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_GUEST_EVIDENCE_MULTIPLEXER_V1'
class MultiplexerError(RuntimeError): pass
class GuestMultiplexer:
    def __init__(self,channel,policy,binding):
        self.channel=channel; self.policy=policy; self.ru=binding['runtime_instance_uuid']; self.no=binding['observation_nonce']; self.rr=binding['runtime_instantiation_attestation_record_sha256']; self.guest_seq=0; self.source_seq={}; self.cv=threading.Condition(); self.acks={}; self.start_token=None; self.failure=None; self.send_lock=threading.Lock()
    def _boot(self):
        v=open('/proc/sys/kernel/random/boot_id',encoding='ascii').read().strip()
        if not v: raise MultiplexerError('guest boot ID unavailable')
        return v
    def control_loop(self):
        try:
            while True:
                kind,obj=recv_host_control(self.channel)
                with self.cv:
                    if kind=='ACK': self.acks[obj['guest_sequence']]=obj
                    else:
                        if obj['runtime_instance_uuid']!=self.ru or obj['observation_nonce']!=self.no or obj['runtime_instantiation_attestation_record_sha256']!=self.rr: raise MultiplexerError('start token binding mismatch')
                        self.start_token=obj
                    self.cv.notify_all()
        except BaseException as exc:
            with self.cv: self.failure=exc; self.cv.notify_all()
    def _wait_ack(self,gseq):
        with self.cv:
            while gseq not in self.acks and self.failure is None: self.cv.wait()
            if self.failure is not None: raise MultiplexerError(f'host control failure: {self.failure}')
            return self.acks.pop(gseq)
    def handle(self,packet,cred):
        p=unpack_local_packet(packet)
        if p['runtime_instance_uuid']!=self.ru or p['observation_nonce']!=self.no: raise MultiplexerError('producer runtime binding mismatch')
        matches=[x for x in self.policy if x['uid']==cred.uid and x['gid']==cred.gid and x['source_type']==p['source_type']]
        if len(matches)!=1: raise MultiplexerError('producer policy mapping mismatch')
        m=matches[0]; ident=bind_source(cred,expected_uid=m['uid'],expected_gid=m['gid'],expected_instrument_identity=m['instrument_identity'],expected_process=m['expected_process'])
        src=f"{m['instrument_identity']}:{ident['pid']}:{ident['starttime']}:{ident['executable_sha256']}:{ident['cmdline_sha256']}:{ident['cgroup_sha256']}"
        expected=self.source_seq.get(src,0)
        if p['source_sequence']!=expected: raise MultiplexerError('source sequence mismatch')
        raw=p['raw_evidence']; md=canonical_bytes({'runtime_instance_uuid':self.ru,'observation_nonce':self.no,'source_instance_identity':src,'source_sequence':p['source_sequence'],'source_native_identity':m['instrument_identity'],'guest_boot_id':self._boot(),'guest_monotonic_timestamp_ns':time.monotonic_ns(),'raw_evidence_byte_count':len(raw),'raw_evidence_sha256':hashlib.sha256(raw).hexdigest()})
        with self.send_lock:
            gseq=self.guest_seq; frame=pack_guest_frame(p['source_type'],gseq,md,raw); self.channel.sendall(frame); ack=self._wait_ack(gseq); validate_ack(ack,guest_sequence=gseq,source_sequence=p['source_sequence'],runtime_instance_uuid=self.ru,observation_nonce=self.no,source_instance_identity=src,transaction_bytes=frame); self.guest_seq+=1
        self.source_seq[src]=expected+1
        return ack
    def wait_for_start_token(self):
        with self.cv:
            while self.start_token is None and self.failure is None: self.cv.wait()
            if self.failure is not None: raise MultiplexerError(f'host control failure: {self.failure}')
            return dict(self.start_token)
def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); channel=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); channel.connect(cfg['guest_channel_socket']); binding=unpack_runtime_binding(recv_exact(channel,runtime_binding_size())); durable_write(cfg['guest_runtime_binding_path'],canonical_bytes(binding)); mux=GuestMultiplexer(channel,cfg['guest_producer_policy'],binding); threading.Thread(target=mux.control_loop,daemon=True).start()
    try: os.unlink(cfg['guest_mux_socket'])
    except FileNotFoundError: pass
    ls=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); ls.bind(cfg['guest_mux_socket']); os.chmod(cfg['guest_mux_socket'],0o660); ls.listen(16)
    try:
        while True:
            conn,_=ls.accept(); enable_seqpacket_credentials(conn)
            try:
                while True:
                    packet,cred,_,_=recv_authenticated(conn)
                    if not packet: break
                    ack=mux.handle(packet,cred); conn.sendall(canonical_bytes(ack))
            finally: conn.close()
    finally: ls.close(); channel.close()
if __name__=='__main__': main()
