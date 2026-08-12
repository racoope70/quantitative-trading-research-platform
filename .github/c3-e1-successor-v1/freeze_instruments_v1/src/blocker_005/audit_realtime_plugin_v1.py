from __future__ import annotations
import os, signal, socket
from audit_string_framing_v1 import LineFramer, FramingError
from evidence_protocol_v1 import pack_local_packet
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_AUDIT_REALTIME_PLUGIN_V1'; SOURCE_TYPE=1

def run(stdin_fd:int,mux_path:str):
    s=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); s.connect(mux_path)
    unexpected={'value':False}
    def bad_signal(*_): unexpected['value']=True
    signal.signal(signal.SIGHUP,bad_signal); signal.signal(signal.SIGTERM,bad_signal)
    fr=LineFramer(); seq=0
    try:
        while not unexpected['value']:
            chunk=os.read(stdin_fd,65536)
            if not chunk:
                fr.finish(); return 0
            for rec in fr.feed(chunk):
                s.sendall(pack_local_packet(SOURCE_TYPE,seq,rec)); seq+=1
        raise FramingError('unexpected signal during governed interval')
    finally: s.close()

def main(): return run(0,'/run/c3-e1/guest-mux.sock')
if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,FramingError): raise SystemExit(2)
