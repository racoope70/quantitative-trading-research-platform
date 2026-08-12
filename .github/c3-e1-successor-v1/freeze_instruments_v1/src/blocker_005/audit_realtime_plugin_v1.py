from __future__ import annotations
import os,queue,select,signal,socket,threading
from audit_string_framing_v1 import LineFramer
from evidence_protocol_v1 import pack_local_packet,validate_producer_ack
from identity_io_v1 import canonical_loads,read_json,read_runtime_binding_file
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,bind_source
from process_identity_v1 import scientific_process_instance
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_AUDIT_REALTIME_PLUGIN_V1'; SOURCE_TYPE=1
class AuditPluginError(RuntimeError): pass
_stop=False
def _term(*_):
    global _stop; _stop=True
def _hup(*_): raise AuditPluginError('SIGHUP prohibited during governed interval')

def _authenticate_mux_ack(sock,cfg,packet,seq,ru,no):
    raw,cred,_,_=recv_authenticated(sock)
    if not raw: raise AuditPluginError('durable producer ACK missing')
    policy=cfg['guest_mux_provider_policy']
    bind_source(cred,expected_uid=policy['uid'],expected_gid=policy['gid'],expected_instrument_identity=policy['instrument_identity'],expected_process=policy['expected_process'])
    ack=canonical_loads(raw);source=scientific_process_instance(INSTRUMENT_IDENTITY)
    return validate_producer_ack(ack,source_sequence=seq,runtime_instance_uuid=ru,observation_nonce=no,source_instance_identity=source,producer_transaction_bytes=packet)

class DurableExporter:
    def __init__(self,sock,ru,no,cfg):
        self.sock=sock; self.ru=ru; self.no=no; self.cfg=cfg; self.seq=0; self.failure=None
        self.sock.settimeout(cfg['producer_ack_timeout_seconds'])
    def send_record(self,record):
        packet=pack_local_packet(SOURCE_TYPE,self.seq,self.ru,self.no,record)
        self.sock.send(packet);ack=_authenticate_mux_ack(self.sock,self.cfg,packet,self.seq,self.ru,self.no);self.seq+=1;return ack

def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json')
    binding=read_runtime_binding_file(cfg['guest_runtime_binding_path']);ru=binding['runtime_instance_uuid'];no=binding['observation_nonce']
    signal.signal(signal.SIGTERM,_term);signal.signal(signal.SIGHUP,_hup)
    sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(sock);sock.connect(cfg['guest_mux_socket'])
    exporter=DurableExporter(sock,ru,no,cfg);work=queue.Queue(maxsize=cfg['audit_queue_records']);sentinel=object()
    def writer():
        try:
            while True:
                item=work.get()
                try:
                    if item is sentinel:return
                    exporter.send_record(item)
                finally:work.task_done()
        except BaseException as exc:
            exporter.failure=exc
            try:sock.shutdown(socket.SHUT_RDWR)
            except OSError:pass
    t=threading.Thread(target=writer,name='c3-e1-audit-durable-writer',daemon=True);t.start();fr=LineFramer(cfg['audit_max_record_bytes'])
    try:
        while not _stop:
            if exporter.failure is not None:raise AuditPluginError(f'durable writer failed: {exporter.failure}')
            readable,_,_=select.select([0],[],[],0.1)
            if not readable:continue
            b=os.read(0,65536)
            if not b:break
            for rec in fr.feed(b):
                try:work.put_nowait(rec)
                except queue.Full as exc:raise AuditPluginError('bounded audit export queue overflow') from exc
        fr.finish()
        try:work.put_nowait(sentinel)
        except queue.Full as exc:raise AuditPluginError('bounded audit queue cannot terminate cleanly') from exc
        work.join();t.join(timeout=cfg['producer_ack_timeout_seconds'])
        if t.is_alive():raise AuditPluginError('durable writer did not terminate')
        if exporter.failure is not None:raise AuditPluginError(f'durable writer failed: {exporter.failure}')
    finally:sock.close()
if __name__=='__main__':main()
