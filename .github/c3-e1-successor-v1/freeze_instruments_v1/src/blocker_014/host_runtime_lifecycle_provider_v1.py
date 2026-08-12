from __future__ import annotations
import os,socket,time
from identity_io_v1 import canonical_bytes,canonical_loads,canonical_sha256,read_json,durable_write,validate_schema_file
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,require_exact_one_fd
from process_identity_v1 import process_identity
from evidence_protocol_v1 import validate_host_ack
class LifecycleError(RuntimeError): pass
class Provider:
    def __init__(self,pidfd,pid,handoff,sink,cfg): self.pidfd=pidfd; self.pid=pid; self.handoff=handoff; self.record=handoff['runtime_instantiation_attestation_record']; self.ru=handoff['runtime_instance_uuid']; self.no=handoff['observation_nonce']; self.rr=handoff['runtime_instantiation_attestation_record_sha256']; self.sink=sink; self.cfg=cfg; self.seq=1; self.expected_qemu=None; self.fds=None; self.source_instance='C3_E1_SUCCESSOR_HOST_RUNTIME_LIFECYCLE_PROVIDER_V1'
    def emit(self,event,evidence):
        obj={'record_type':'HOST_LIFECYCLE_EVENT','runtime_instance_uuid':self.ru,'observation_nonce':self.no,'source_instance_identity':self.source_instance,'source_sequence':self.seq,'lifecycle_event_type':event,'qemu_process_identity':self.expected_qemu or process_identity(self.pid),'qemu_binary_sha256':self.cfg['qemu_sha256'],'qemu_machine_configuration_sha256':self.cfg['qemu_machine_configuration_sha256'],'verified_block_object_identity':self.record['verified_block_object_identity'],'preopened_fd_binding_identity':self.record['preopened_fd_binding_identity'],'device_identity_if_applicable':'NONE' if not evidence.get('device_identity') else evidence['device_identity'],'host_native_monotonic_timestamp_ns':time.monotonic_ns(),'host_native_UTC_timestamp_ns':time.time_ns(),'event_specific_evidence':canonical_sha256(evidence)}; payload=canonical_bytes(obj); wire=canonical_bytes({'_transport_source_sequence':self.seq,**obj}); self.sink.send(wire); ack=canonical_loads(self.sink.recv(65536)); validate_host_ack(ack,runtime_instance_uuid=self.ru,observation_nonce=self.no,source_instance_identity=self._sink_source_identity(),source_sequence=self.seq,payload=payload); self.seq+=1
    def _sink_source_identity(self):
        i=process_identity(os.getpid()); return f"C3_E1_SUCCESSOR_HOST_RUNTIME_LIFECYCLE_PROVIDER_V1:{i['pid']}:{i['starttime']}:{i['executable_sha256']}:{i['cmdline_sha256']}:{i['cgroup_sha256']}"
    def await_qemu_exec(self):
        deadline=time.monotonic()+self.cfg['qemu_exec_timeout_seconds']; initial=process_identity(self.pid); start=initial['starttime']
        while time.monotonic()<deadline:
            now=process_identity(self.pid)
            if now['starttime']!=start: raise LifecycleError('PID reuse/replacement')
            if now['executable_sha256']==self.cfg['qemu_sha256']:
                self.expected_qemu=now; return now
            time.sleep(.02)
        raise LifecycleError('QEMU in-place exec timeout')
    def check(self):
        now=process_identity(self.pid)
        if self.expected_qemu is None or now!=self.expected_qemu: raise LifecycleError('QEMU process identity changed')
        fdroot=f'/proc/{self.pid}/fd'; current={x:os.readlink(f'{fdroot}/{x}') for x in os.listdir(fdroot) if x.isdigit()}
        if self.fds is not None and current!=self.fds: self.emit('FD_TABLE_CHANGED',{'previous':self.fds,'current':current})
        self.fds=current
def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_014/blocker_014_config_v1.json')
    try: os.unlink(cfg['lifecycle_handoff_socket'])
    except FileNotFoundError: pass
    ls=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); ls.bind(cfg['lifecycle_handoff_socket']); os.chmod(cfg['lifecycle_handoff_socket'],0o660); ls.listen(1); c,_=ls.accept(); enable_seqpacket_credentials(c); packet,cred,anc,_=recv_authenticated(c); pidfd=require_exact_one_fd(anc); info=open(f'/proc/self/fdinfo/{pidfd}').read()
    if f'Pid:\t{cred.pid}' not in info: raise LifecycleError('pidfd/credential PID mismatch')
    handoff=canonical_loads(packet); required={'record_type','runtime_instance_uuid','observation_nonce','runtime_instantiation_attestation_record','runtime_instantiation_attestation_record_sha256'}
    if set(handoff)!=required or handoff['record_type']!='LAUNCHER_PIDFD_HANDOFF': raise LifecycleError('launcher handoff fields')
    rec=handoff['runtime_instantiation_attestation_record']; validate_schema_file(rec,cfg['record_schema_path'])
    if canonical_sha256(rec)!=handoff['runtime_instantiation_attestation_record_sha256'] or rec['runtime_instance_uuid']!=handoff['runtime_instance_uuid'] or rec['observation_nonce']!=handoff['observation_nonce']: raise LifecycleError('runtime record handoff binding')
    sink=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); sink.connect(cfg['host_sink_socket']); p=Provider(pidfd,cred.pid,handoff,sink,cfg); qemu=p.await_qemu_exec(); bind={'record_type':'RUNTIME_BINDING_ESTABLISHED','runtime_instance_uuid':p.ru,'observation_nonce':p.no,'qemu_pid':cred.pid,'runtime_instantiation_attestation_record_sha256':p.rr}; payload=canonical_bytes(bind); sink.send(canonical_bytes({'_transport_source_sequence':0,**bind})); ack=canonical_loads(sink.recv(65536)); validate_host_ack(ack,runtime_instance_uuid=p.ru,observation_nonce=p.no,source_instance_identity=p._sink_source_identity(),source_sequence=0,payload=payload); p.emit('QEMU_PROCESS_STARTED',{'qemu_process_identity':qemu})
    try:
        while True: p.check(); time.sleep(cfg['lifecycle_poll_seconds'])
    except (FileNotFoundError,ProcessLookupError):
        durable_write(cfg['lifecycle_final_marker_path'],canonical_bytes({'runtime_instance_uuid':p.ru,'observation_nonce':p.no,'terminal_event':'QEMU_PROCESS_EXITED'}))
    finally: os.close(pidfd); sink.close(); c.close(); ls.close()
if __name__=='__main__': main()
