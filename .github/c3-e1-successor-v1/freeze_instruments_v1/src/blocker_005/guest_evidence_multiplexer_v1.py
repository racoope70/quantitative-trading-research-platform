from __future__ import annotations
import hashlib,os,socket,threading,time
from evidence_protocol_v1 import *
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,bind_source
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,durable_write
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_GUEST_EVIDENCE_MULTIPLEXER_V1'
class MultiplexerError(RuntimeError): pass

class FDStream:
    def __init__(self,fd): self.fd=fd; self.write_lock=threading.Lock()
    def recv(self,n): return os.read(self.fd,n)
    def sendall(self,data):
        with self.write_lock:
            mv=memoryview(data)
            while mv:
                n=os.write(self.fd,mv)
                if n<=0: raise MultiplexerError('virtio-serial short write')
                mv=mv[n:]
    def close(self):
        if self.fd is not None: os.close(self.fd); self.fd=None

def open_guest_virtio_serial(path):
    if not isinstance(path,str) or not path.startswith('/dev/virtio-ports/'): raise MultiplexerError('frozen virtio-serial device path required')
    return FDStream(os.open(path,os.O_RDWR|os.O_NOCTTY|os.O_CLOEXEC))

class GuestMultiplexer:
    def __init__(self,channel,policy,binding):
        self.channel=channel; self.policy=policy; self.ru=binding['runtime_instance_uuid']; self.no=binding['observation_nonce']; self.rr=binding['runtime_instantiation_attestation_record_sha256']
        self.guest_seq=0; self.source_seq={}; self.cv=threading.Condition(); self.acks={}; self.start_token=None; self.failure=None; self.send_lock=threading.Lock()
    def _boot(self):
        v=open('/proc/sys/kernel/random/boot_id',encoding='ascii').read().strip()
        if not v: raise MultiplexerError('guest boot ID unavailable')
        return v
    def _policy_for(self,cred,source_type):
        matches=[x for x in self.policy if x['uid']==cred.uid and x['gid']==cred.gid and x['source_type']==source_type]
        if len(matches)!=1: raise MultiplexerError('producer policy mapping mismatch')
        return matches[0]
    def authenticate_source(self,cred,source_type):
        m=self._policy_for(cred,source_type)
        ident=bind_source(cred,expected_uid=m['uid'],expected_gid=m['gid'],expected_instrument_identity=m['instrument_identity'],expected_process=m['expected_process'])
        src=f"{m['instrument_identity']}:{ident['pid']}:{ident['starttime']}:{ident['executable_sha256']}:{ident['cmdline_sha256']}:{ident['cgroup_sha256']}"
        return m,src
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
            with self.cv:self.failure=exc;self.cv.notify_all()
    def _wait_ack(self,gseq):
        with self.cv:
            while gseq not in self.acks and self.failure is None:self.cv.wait()
            if self.failure is not None:raise MultiplexerError(f'host control failure: {self.failure}')
            return self.acks.pop(gseq)
    def handle(self,packet,cred):
        p=unpack_local_packet(packet)
        if p['runtime_instance_uuid']!=self.ru or p['observation_nonce']!=self.no: raise MultiplexerError('producer runtime binding mismatch')
        m,src=self.authenticate_source(cred,p['source_type'])
        with self.send_lock:
            expected=self.source_seq.get(src,0)
            if p['source_sequence']!=expected: raise MultiplexerError('source sequence mismatch')
            raw=p['raw_evidence']
            md=canonical_bytes({'runtime_instance_uuid':self.ru,'observation_nonce':self.no,'source_instance_identity':src,'source_sequence':p['source_sequence'],'source_native_identity':m['instrument_identity'],'guest_boot_id':self._boot(),'guest_monotonic_timestamp_ns':time.monotonic_ns(),'raw_evidence_byte_count':len(raw),'raw_evidence_sha256':hashlib.sha256(raw).hexdigest()})
            gseq=self.guest_seq
            frame=pack_guest_frame(p['source_type'],gseq,md,raw)
            self.channel.sendall(frame)
            host_ack=self._wait_ack(gseq)
            validate_ack(host_ack,guest_sequence=gseq,source_sequence=p['source_sequence'],runtime_instance_uuid=self.ru,observation_nonce=self.no,source_instance_identity=src,transaction_bytes=frame)
            self.guest_seq+=1; self.source_seq[src]=expected+1
            return producer_ack_from_host(host_ack,packet)
    def wait_for_start_token(self):
        with self.cv:
            while self.start_token is None and self.failure is None:self.cv.wait()
            if self.failure is not None:raise MultiplexerError(f'host control failure: {self.failure}')
            return dict(self.start_token)

def _serve_producer_connection(mux,conn):
    try:
        enable_seqpacket_credentials(conn)
        while True:
            packet,cred,_,_=recv_authenticated(conn)
            if not packet:break
            ack=mux.handle(packet,cred)
            conn.sendall(canonical_bytes(ack))
    finally:conn.close()

def _producer_accept_loop(mux,listener):
    while True:
        conn,_=listener.accept()
        threading.Thread(target=_serve_producer_connection,args=(mux,conn),daemon=True).start()

def _serve_start_gate(mux,listener,policy,consumer_identity):
    while True:
        conn,_=listener.accept()
        try:
            enable_seqpacket_credentials(conn)
            packet,cred,_,_=recv_authenticated(conn)
            req=canonical_loads(packet)
            if req!={'record_type':'START_GATE_REQUEST','runtime_instance_uuid':mux.ru,'observation_nonce':mux.no,'runtime_instantiation_attestation_record_sha256':mux.rr}:raise MultiplexerError('start gate request binding mismatch')
            candidates=[x for x in policy if x['uid']==cred.uid and x['gid']==cred.gid and x['instrument_identity']==consumer_identity]
            if len(candidates)!=1:raise MultiplexerError('start gate consumer policy mismatch')
            p=candidates[0];bind_source(cred,expected_uid=p['uid'],expected_gid=p['gid'],expected_instrument_identity=p['instrument_identity'],expected_process=p['expected_process'])
            conn.sendall(canonical_bytes(mux.wait_for_start_token()))
        finally:conn.close()

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json')
    channel=open_guest_virtio_serial(cfg['guest_virtio_port_path'])
    binding=unpack_runtime_binding(recv_exact(channel,runtime_binding_size()))
    durable_write(cfg['guest_runtime_binding_path'],canonical_bytes(binding))
    mux=GuestMultiplexer(channel,cfg['guest_producer_policy'],binding)
    threading.Thread(target=mux.control_loop,daemon=True).start()
    listeners=[]
    try:
        for path in (cfg['guest_mux_socket'],cfg['guest_start_gate_socket']):
            try:os.unlink(path)
            except FileNotFoundError:pass
        producer=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);producer.bind(cfg['guest_mux_socket']);os.chmod(cfg['guest_mux_socket'],0o660);producer.listen(cfg['guest_mux_backlog']);listeners.append(producer)
        gate=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);gate.bind(cfg['guest_start_gate_socket']);os.chmod(cfg['guest_start_gate_socket'],0o660);gate.listen(4);listeners.append(gate)
        threading.Thread(target=_producer_accept_loop,args=(mux,producer),daemon=True).start()
        _serve_start_gate(mux,gate,cfg['guest_producer_policy'],cfg['start_gate_consumer_instrument_identity'])
    finally:
        for s in listeners:s.close()
        channel.close()
if __name__=='__main__':main()
