from __future__ import annotations
import hashlib,os,socket,threading,time
from durable_journal_v1 import DurableJournal
from evidence_protocol_v1 import *
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,durable_write,validate_schema_file
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,stream_peercred,bind_source
class SinkError(RuntimeError):pass

class SinkState:
    def __init__(self,journal,schema):
        self.journal=journal;self.schema=schema;self.seq=0;self.prev=b'\0'*32;self.sealed=False
        self.ru=None;self.no=None;self.qemu_pid=None;self.rr=None
        self.guest_seq=SequenceState();self.source_seq={};self.host_seq={};self.prepass=None
        self.guest_stream=None;self.guest_stream_claimed=False;self.lock=threading.RLock();self.start_host_sequence=None;self.end_host_sequence=None
        self.runtime_bound=threading.Event()
    def bind_runtime(self,runtime_uuid,nonce,qemu_pid,runtime_record_sha256):
        uuid_bytes(runtime_uuid);nonce_bytes(nonce);_sha(runtime_record_sha256,'runtime record')
        new=(runtime_uuid,nonce,qemu_pid,runtime_record_sha256);old=(self.ru,self.no,self.qemu_pid,self.rr)
        if self.ru is not None and old!=new:raise SinkError('runtime replacement prohibited')
        self.ru,self.no,self.qemu_pid,self.rr=new;self.runtime_bound.set()
    def append(self,origin,payload):
        with self.lock:
            if self.sealed:raise SinkError('observation chain sealed')
            if self.ru is None:raise SinkError('runtime not bound')
            r=self.journal.commit(origin=origin,host_sequence=self.seq,monotonic_ns=time.monotonic_ns(),utc_ns=time.time_ns(),previous_sha256=self.prev,payload=payload,runtime_instance_uuid=self.ru)
            self.prev=bytes.fromhex(r['record_sha256']);self.seq+=1;return r
    def accept_guest(self,frame):
        d=unpack_guest_frame(frame);md=canonical_loads(d['metadata_bytes'])
        validate_guest_metadata(md,source_type=d['source_type'],raw_evidence=d['raw_evidence'],expected_runtime_uuid=self.ru,expected_nonce=self.no)
        self.guest_seq=self.guest_seq.consume(d['guest_sequence']);src=md['source_instance_identity'];expected=self.source_seq.get(src,0)
        if md['source_sequence']!=expected:raise SinkError('source sequence mismatch')
        self.source_seq[src]=expected+1;r=self.append(ORIGIN_GUEST,frame)
        return pack_ack(guest_sequence=d['guest_sequence'],source_sequence=md['source_sequence'],host_sequence=r['host_sequence'],runtime_instance_uuid=self.ru,observation_nonce=self.no,source_instance_identity=src,transaction_sha256=hashlib.sha256(frame).digest(),record_sha256=bytes.fromhex(r['record_sha256']))
    def accept_host(self,payload,identity,instrument,source_sequence):
        obj=canonical_loads(payload);validate_schema_file(obj,self.schema)
        if obj['record_type']=='RUNTIME_BINDING_ESTABLISHED':
            self.bind_runtime(obj['runtime_instance_uuid'],obj['observation_nonce'],obj['qemu_pid'],obj['runtime_instantiation_attestation_record_sha256'])
        elif obj.get('runtime_instance_uuid')!=self.ru or obj.get('observation_nonce')!=self.no:raise SinkError('host event runtime mismatch')
        src=f"{instrument}:{identity['pid']}:{identity['starttime']}:{identity['executable_sha256']}:{identity['cmdline_sha256']}:{identity['cgroup_sha256']}"
        expected=self.host_seq.get(src,0)
        if source_sequence!=expected:raise SinkError('host source sequence mismatch')
        self.host_seq[src]=expected+1
        env={'record_type':'HOST_ORIGIN_EVIDENCE_ENVELOPE','runtime_instance_uuid':self.ru,'observation_nonce':self.no,'source_native_identity':instrument,'source_instance_identity':src,'source_sequence':source_sequence,'raw_evidence_byte_count':len(payload),'raw_evidence_sha256':hashlib.sha256(payload).hexdigest(),'raw_evidence_hex':payload.hex()}
        validate_schema_file(env,self.schema);r=self.append(ORIGIN_HOST,canonical_bytes(env))
        if obj['record_type']=='PRE_E1_VERIFIER_RESULT':
            if obj['classification']!='PASS' or obj['runtime_instantiation_attestation_record_sha256']!=self.rr:raise SinkError('durable verifier PASS runtime mismatch')
            self.prepass={**obj,'host_sequence':r['host_sequence']}
        return r,src,obj
    def release_start_token(self):
        if self.guest_stream is None or self.prepass is None:raise SinkError('durable PASS and guest stream required')
        x=self.prepass
        marker=canonical_bytes({'record_type':'OBSERVATION_START_AUTHORIZED','runtime_instance_uuid':self.ru,'observation_nonce':self.no,'verifier_result_sha256':x['verifier_result_sha256'],'runtime_instantiation_attestation_record_sha256':self.rr})
        r=self.append(ORIGIN_HOST,marker);self.start_host_sequence=r['host_sequence']
        t=pack_start_token(self.ru,self.no,x['verifier_result_sha256'],self.rr,x['host_sequence'],r['host_sequence'])
        self.guest_stream.sendall(t);return t
    def final_checkpoint(self,start_seq,end_seq,path):
        if self.sealed:raise SinkError('already sealed')
        if start_seq is None or end_seq is None or start_seq>end_seq or end_seq>=self.seq:raise SinkError('invalid observation boundaries')
        ident=self.journal.fsync_and_identity()
        cp={'record_type':'FINAL_OBSERVATION_CHECKPOINT','runtime_instance_uuid':self.ru,'observation_nonce':self.no,'final_host_sequence':self.seq-1,'final_record_sha256':self.prev.hex(),'observation_start_host_sequence':start_seq,'observation_end_host_sequence':end_seq,'total_record_count':self.seq,'journal_byte_count':ident['byte_count'],'journal_sha256':ident['sha256']}
        validate_schema_file(cp,self.schema);raw=canonical_bytes(cp);durable_write(path,raw);self.sealed=True
        return cp,hashlib.sha256(raw).hexdigest()

def _match_policy(cfg,cred):
    candidates=[x for x in cfg['host_producer_policy'] if x['uid']==cred.uid and x['gid']==cred.gid]
    if len(candidates)!=1:raise SinkError('host producer policy mismatch')
    return candidates[0]

def _handle_host_connection(state,cfg,conn):
    enable_seqpacket_credentials(conn);bound_source=None;bound_policy=None
    try:
        while True:
            packet,cred,_,_=recv_authenticated(conn)
            if not packet:break
            p=_match_policy(cfg,cred)
            ident=bind_source(cred,expected_uid=p['uid'],expected_gid=p['gid'],expected_instrument_identity=p['instrument_identity'],expected_process=p['expected_process'])
            src=f"{p['instrument_identity']}:{ident['pid']}:{ident['starttime']}:{ident['executable_sha256']}:{ident['cmdline_sha256']}:{ident['cgroup_sha256']}"
            if bound_source is None:bound_source=src;bound_policy=p['instrument_identity']
            elif src!=bound_source or p['instrument_identity']!=bound_policy:raise SinkError('host connection source identity changed')
            wire=canonical_loads(packet)
            if '_transport_source_sequence' not in wire:raise SinkError('host transport source sequence missing')
            seq=wire.pop('_transport_source_sequence');raw=canonical_bytes(wire)
            r,src,obj=state.accept_host(raw,ident,p['instrument_identity'],seq)
            ack=make_host_ack(runtime_instance_uuid=state.ru,observation_nonce=state.no,source_instance_identity=src,source_sequence=seq,host_sequence=r['host_sequence'],payload=raw,record_sha256=r['record_sha256'])
            conn.sendall(canonical_bytes(ack))
            if obj['record_type']=='START_TOKEN_RELEASE_REQUEST':state.release_start_token()
            elif obj['record_type']=='FINAL_CHECKPOINT_REQUEST':
                cp,sha=state.final_checkpoint(obj['observation_start_host_sequence'],obj['observation_end_host_sequence'],obj['checkpoint_path'])
                durable_write(obj['checkpoint_reference_path'],canonical_bytes({'sha256':sha,**cp}))
    finally:conn.close()

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json');journal=DurableJournal(cfg['journal_path'],cfg['chain_head_path'],canonical_bytes);state=SinkState(journal,cfg['schema_path'])
    for path in (cfg['host_local_socket'],cfg['guest_channel_socket']):
        try:os.unlink(path)
        except FileNotFoundError:pass
    hls=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);hls.bind(cfg['host_local_socket']);os.chmod(cfg['host_local_socket'],0o660);hls.listen(16)
    def host_accept_loop():
        while True:
            conn,_=hls.accept();threading.Thread(target=_handle_host_connection,args=(state,cfg,conn),daemon=True).start()
    threading.Thread(target=host_accept_loop,daemon=True).start()
    gls=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);gls.bind(cfg['guest_channel_socket']);os.chmod(cfg['guest_channel_socket'],0o660);gls.listen(1)
    try:
        while True:
            conn,_=gls.accept();cred=stream_peercred(conn)
            if not state.runtime_bound.wait(cfg['qemu_peer_bind_timeout_seconds']):conn.close();continue
            if cred.pid!=state.qemu_pid or cred.uid!=cfg['qemu_uid'] or cred.gid!=cfg['qemu_gid']:conn.close();continue
            if state.guest_stream_claimed:conn.close();raise SinkError('QEMU guest evidence stream replacement prohibited')
            state.guest_stream_claimed=True;state.guest_stream=conn;conn.sendall(pack_runtime_binding(state.ru,state.no,state.rr))
            try:
                while True:conn.sendall(state.accept_guest(recv_guest_frame(conn)))
            finally:state.guest_stream=None;conn.close()
    finally:
        gls.close();hls.close();journal.close()
if __name__=='__main__':main()
