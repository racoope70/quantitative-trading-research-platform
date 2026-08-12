from __future__ import annotations
import errno,hashlib,os,selectors,socket
from evidence_protocol_v1 import pack_local_packet
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,read_runtime_binding_file
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,require_exact_one_fd
CAP_NET_ADMIN=12; SOURCE_TYPE=2
class MonitorError(RuntimeError): pass

def effective_caps():
    for line in open('/proc/self/status',encoding='utf-8'):
        if line.startswith('CapEff:'): return int(line.split()[1],16)
    raise MonitorError('CapEff unavailable')
def assert_receive_only():
    if effective_caps() & (1<<CAP_NET_ADMIN): raise MonitorError('CAP_NET_ADMIN prohibited in transition monitor')
def receive(sock):
    try: data,_,flags,_=sock.recvmsg(1048576)
    except OSError as exc:
        if exc.errno==errno.ENOBUFS: raise MonitorError('ENOBUFS') from exc
        raise
    if flags & socket.MSG_TRUNC: raise MonitorError('MSG_TRUNC')
    if not data: raise MonitorError('notification socket closed')
    return data

def transition_evidence(raw,ru,no):
    return canonical_bytes({'record_type':'NFTABLES_TRANSITION','runtime_instance_uuid':ru,'observation_nonce':no,'raw_netlink_byte_count':len(raw),'raw_netlink_sha256':hashlib.sha256(raw).hexdigest(),'raw_netlink_hex':raw.hex()})
def barrier_evidence(barrier_id,ru,no,notification_count,effective_rcvbuf):
    return canonical_bytes({'record_type':'NFTABLES_NOTIFICATION_BARRIER','runtime_instance_uuid':ru,'observation_nonce':no,'barrier_id':barrier_id,'notification_count':notification_count,'effective_so_rcvbuf':effective_rcvbuf,'enobufs_observed':False,'msg_trunc_observed':False,'receiver_continuity':True,'healthy':True})
def _send_mux(mux,seq,ru,no,raw):
    mux.send(pack_local_packet(SOURCE_TYPE,seq,ru,no,raw)); return seq+1

def main():
    assert_receive_only()
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_006/blocker_006_config_v1.json')
    cfg5=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); binding=read_runtime_binding_file(cfg5['guest_runtime_binding_path']); ru=binding['runtime_instance_uuid']; no=binding['observation_nonce']
    handoff=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); enable_seqpacket_credentials(handoff)
    try: os.unlink(cfg['monitor_handoff_socket'])
    except FileNotFoundError: pass
    handoff.bind(cfg['monitor_handoff_socket']); os.chmod(cfg['monitor_handoff_socket'],0o660); handoff.listen(1)
    conn,_=handoff.accept(); packet,_cred,anc,_=recv_authenticated(conn)
    if packet!=b'NFTABLES_NOTIFICATION_FD_V1': raise MonitorError('unexpected bootstrap handoff record')
    fd=require_exact_one_fd(anc); ns=socket.socket(fileno=fd)
    effective=ns.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
    conn.send(b'NFTABLES_NOTIFICATION_FD_ACCEPTED_V1')
    try: os.unlink(cfg['monitor_barrier_socket'])
    except FileNotFoundError: pass
    barrier=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); barrier.bind(cfg['monitor_barrier_socket']); os.chmod(cfg['monitor_barrier_socket'],0o660); barrier.listen(4)
    mux=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); mux.connect(cfg['guest_mux_socket'])
    sel=selectors.DefaultSelector(); sel.register(ns,selectors.EVENT_READ,'netlink'); sel.register(barrier,selectors.EVENT_READ,'barrier')
    seq=0; total_notifications=0
    try:
        while True:
            for key,_ in sel.select():
                if key.data=='netlink':
                    raw=receive(ns); total_notifications+=1; seq=_send_mux(mux,seq,ru,no,transition_evidence(raw,ru,no))
                else:
                    bc,_=barrier.accept()
                    try:
                        request=canonical_loads(bc.recv(65536))
                        if set(request)!={'record_type','barrier_id','runtime_instance_uuid','observation_nonce'} or request['record_type']!='NFTABLES_NOTIFICATION_BARRIER_REQUEST' or request['runtime_instance_uuid']!=ru or request['observation_nonce']!=no: raise MonitorError('invalid barrier request')
                        drained=0; ns.setblocking(False)
                        try:
                            while True:
                                try: raw=receive(ns)
                                except BlockingIOError: break
                                drained+=1; total_notifications+=1; seq=_send_mux(mux,seq,ru,no,transition_evidence(raw,ru,no))
                        finally: ns.setblocking(True)
                        ev=barrier_evidence(request['barrier_id'],ru,no,drained,effective); seq=_send_mux(mux,seq,ru,no,ev); bc.send(ev)
                    finally: bc.close()
    finally:
        sel.close(); mux.close(); barrier.close(); ns.close(); conn.close(); handoff.close()
if __name__=='__main__': main()
