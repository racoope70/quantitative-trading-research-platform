from __future__ import annotations
import os,signal,socket
from audit_string_framing_v1 import LineFramer
from evidence_protocol_v1 import pack_local_packet
from identity_io_v1 import read_json,read_runtime_binding_file
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_AUDIT_REALTIME_PLUGIN_V1'; SOURCE_TYPE=1
class AuditPluginError(RuntimeError): pass
_stop=False
def _term(*_):
    global _stop; _stop=True
def _hup(*_): raise AuditPluginError('SIGHUP prohibited during governed interval')
def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); binding=read_runtime_binding_file(cfg['guest_runtime_binding_path']); ru=binding['runtime_instance_uuid']; no=binding['observation_nonce']
    signal.signal(signal.SIGTERM,_term); signal.signal(signal.SIGHUP,_hup); sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); sock.connect(cfg['guest_mux_socket']); fr=LineFramer(cfg['audit_max_record_bytes']); seq=0
    try:
        while not _stop:
            b=os.read(0,65536)
            if not b: break
            for rec in fr.feed(b): sock.send(pack_local_packet(SOURCE_TYPE,seq,ru,no,rec)); seq+=1
        fr.finish()
    finally: sock.close()
if __name__=='__main__': main()
