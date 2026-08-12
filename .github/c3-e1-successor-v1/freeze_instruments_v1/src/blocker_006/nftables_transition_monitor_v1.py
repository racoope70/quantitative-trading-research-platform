from __future__ import annotations
import errno,hashlib,os,selectors,socket
from evidence_protocol_v1 import pack_local_packet,validate_producer_ack
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,read_runtime_binding_file
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,require_exact_one_fd,bind_source
from nftables_snapshot_v1 import iter_msgs,NLMSG_OVERRUN
from nftables_delivery_barrier_v1 import barrier_record
from process_identity_v1 import scientific_process_instance
CAP_NET_ADMIN=12;SOURCE_TYPE=2;INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_NFTABLES_TRANSITION_MONITOR_V1'
class MonitorError(RuntimeError):pass

def effective_caps():
    for line in open('/proc/self/status',encoding='utf-8'):
        if line.startswith('CapEff:'):return int(line.split()[1],16)
    raise MonitorError('CapEff unavailable')
def assert_receive_only():
    if effective_caps()&(1<<CAP_NET_ADMIN):raise MonitorError('CAP_NET_ADMIN prohibited in transition monitor')
def receive(sock):
    try:data,_,flags,_=sock.recvmsg(1048576)
    except OSError as exc:
        if exc.errno==errno.ENOBUFS:raise MonitorError('ENOBUFS') from exc
        raise
    if flags&socket.MSG_TRUNC:raise MonitorError('MSG_TRUNC')
    if not data:raise MonitorError('notification socket closed')
    for m in iter_msgs(data):
        if m['type']==NLMSG_OVERRUN:raise MonitorError('NLMSG_OVERRUN')
    return data
def transition_evidence(raw,ru,no):
    return canonical_bytes({'record_type':'NFTABLES_TRANSITION','runtime_instance_uuid':ru,'observation_nonce':no,'raw_netlink_byte_count':len(raw),'raw_netlink_sha256':hashlib.sha256(raw).hexdigest(),'raw_netlink_hex':raw.hex()})
def window_open_evidence(window_id,ru,no,total,source_seq,requested,effective):
    return canonical_bytes({'record_type':'NFTABLES_STABILITY_WINDOW_OPEN','runtime_instance_uuid':ru,'observation_nonce':no,'barrier_id':window_id,'window_baseline_total_notifications':total,'monitor_source_sequence_at_window_open':source_seq,'requested_so_rcvbuf':requested,'effective_so_rcvbuf':effective,'receiver_continuity':True})
def _authenticate_peer(cred,policy):
    return bind_source(cred,expected_uid=policy['uid'],expected_gid=policy['gid'],expected_instrument_identity=policy['instrument_identity'],expected_process=policy['expected_process'])
def _send_mux(mux,seq,ru,no,raw,cfg5):
    source=scientific_process_instance(INSTRUMENT_IDENTITY);packet=pack_local_packet(SOURCE_TYPE,seq,ru,no,raw);mux.send(packet)
    ackraw,cred,_,_=recv_authenticated(mux)
    if not ackraw:raise MonitorError('durable producer ACK missing')
    _authenticate_peer(cred,cfg5['guest_mux_provider_policy'])
    ack=canonical_loads(ackraw);validate_producer_ack(ack,source_sequence=seq,runtime_instance_uuid=ru,observation_nonce=no,source_instance_identity=source,producer_transaction_bytes=packet)
    return seq+1,ack
def _drain(ns,mux,seq,ru,no,cfg5):
    count=0;ns.setblocking(False)
    try:
        while True:
            try:raw=receive(ns)
            except BlockingIOError:break
            count+=1;seq,_=_send_mux(mux,seq,ru,no,transition_evidence(raw,ru,no),cfg5)
    finally:ns.setblocking(True)
    return count,seq
def main():
    assert_receive_only();cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_006/blocker_006_config_v1.json');cfg5=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json')
    binding=read_runtime_binding_file(cfg5['guest_runtime_binding_path']);ru=binding['runtime_instance_uuid'];no=binding['observation_nonce']
    handoff=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(handoff)
    try:os.unlink(cfg['monitor_handoff_socket'])
    except FileNotFoundError:pass
    handoff.bind(cfg['monitor_handoff_socket']);os.chmod(cfg['monitor_handoff_socket'],0o660);handoff.listen(1)
    conn,_=handoff.accept();enable_seqpacket_credentials(conn);packet,cred,anc,_=recv_authenticated(conn)
    if packet!=b'NFTABLES_NOTIFICATION_FD_V1':raise MonitorError('unexpected bootstrap handoff record')
    p=cfg['bootstrap_peer_policy'];bind_source(cred,expected_uid=p['uid'],expected_gid=p['gid'],expected_instrument_identity=p['instrument_identity'],expected_process=p['expected_process'])
    fd=require_exact_one_fd(anc);ns=socket.socket(fileno=fd);requested=cfg['requested_so_rcvbuf'];effective=ns.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
    conn.send(b'NFTABLES_NOTIFICATION_FD_ACCEPTED_V1')
    try:os.unlink(cfg['monitor_barrier_socket'])
    except FileNotFoundError:pass
    barrier=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);barrier.bind(cfg['monitor_barrier_socket']);os.chmod(cfg['monitor_barrier_socket'],0o660);barrier.listen(4)
    mux=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(mux);mux.settimeout(cfg['producer_ack_timeout_seconds']);mux.connect(cfg['guest_mux_socket'])
    sel=selectors.DefaultSelector();sel.register(ns,selectors.EVENT_READ,'netlink');sel.register(barrier,selectors.EVENT_READ,'barrier')
    seq=0;total_notifications=0;windows={}
    try:
        while True:
            for key,_ in sel.select():
                if key.data=='netlink':
                    raw=receive(ns);total_notifications+=1;seq,_=_send_mux(mux,seq,ru,no,transition_evidence(raw,ru,no),cfg5)
                else:
                    bc,_=barrier.accept()
                    try:
                        enable_seqpacket_credentials(bc);request_raw,request_cred,_,_=recv_authenticated(bc);_authenticate_peer(request_cred,cfg['authority_peer_policy']);request=canonical_loads(request_raw)
                        if request.get('runtime_instance_uuid')!=ru or request.get('observation_nonce')!=no:raise MonitorError('barrier runtime binding mismatch')
                        kind=request.get('record_type');window_id=request.get('barrier_id')
                        if not isinstance(window_id,str) or not window_id:raise MonitorError('barrier id required')
                        drained,seq=_drain(ns,mux,seq,ru,no,cfg5);total_notifications+=drained
                        if kind=='NFTABLES_STABILITY_WINDOW_OPEN_REQUEST':
                            if set(request)!={'record_type','barrier_id','runtime_instance_uuid','observation_nonce'}:raise MonitorError('window-open fields')
                            baseline=total_notifications;source_at_open=seq
                            ev=window_open_evidence(window_id,ru,no,baseline,source_at_open,requested,effective);seq,ack=_send_mux(mux,seq,ru,no,ev,cfg5)
                            windows[window_id]={'baseline':baseline,'source_at_open':source_at_open}
                            bc.send(canonical_bytes({'record_type':'NFTABLES_STABILITY_WINDOW_OPEN_ACK','barrier_id':window_id,'runtime_instance_uuid':ru,'observation_nonce':no,'window_baseline_total_notifications':baseline,'monitor_source_sequence_at_window_open':source_at_open,'requested_so_rcvbuf':requested,'effective_so_rcvbuf':effective,'durable_ack_host_sequence':ack['host_sequence'],'durable_ack_record_sha256':ack['record_sha256'],'healthy':True}))
                        elif kind=='NFTABLES_NOTIFICATION_BARRIER_REQUEST':
                            if set(request)!={'record_type','barrier_id','runtime_instance_uuid','observation_nonce','window_baseline_total_notifications','monitor_source_sequence_at_window_open'}:raise MonitorError('barrier request fields')
                            state=windows.pop(window_id,None)
                            if state is None or state['baseline']!=request['window_baseline_total_notifications'] or state['source_at_open']!=request['monitor_source_sequence_at_window_open']:raise MonitorError('window baseline mismatch')
                            count=total_notifications-state['baseline']
                            evobj=barrier_record(barrier_id=window_id,runtime_instance_uuid=ru,observation_nonce=no,window_baseline_total_notifications=state['baseline'],total_notifications_at_barrier=total_notifications,monitor_source_sequence_at_window_open=state['source_at_open'],monitor_source_sequence_at_barrier=seq,requested_so_rcvbuf=requested,effective_so_rcvbuf=effective,enobufs_observed=False,msg_trunc_observed=False,nlmsg_overrun_observed=False,receiver_continuity=True,notification_count_during_window=count)
                            seq,ack=_send_mux(mux,seq,ru,no,canonical_bytes(evobj),cfg5)
                            bc.send(canonical_bytes({**evobj,'durable_ack_host_sequence':ack['host_sequence'],'durable_ack_record_sha256':ack['record_sha256'],'healthy':True}))
                        else:raise MonitorError('unsupported barrier request')
                    finally:bc.close()
    finally:sel.close();mux.close();barrier.close();ns.close();conn.close();handoff.close()
if __name__=='__main__':main()
