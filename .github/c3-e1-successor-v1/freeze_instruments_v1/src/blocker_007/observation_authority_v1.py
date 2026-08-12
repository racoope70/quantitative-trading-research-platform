from __future__ import annotations
import hashlib,os,socket
from evidence_protocol_v1 import pack_local_packet,validate_producer_ack
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,bind_source
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,read_runtime_binding_file,require_file_identity,assert_resolved,durable_write
from nftables_delivery_barrier_v1 import evaluate
from nftables_snapshot_v1 import recv_complete_dump
from process_identity_v1 import scientific_process_instance
CAP_NET_ADMIN=12;SOURCE_TYPE=3;INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1'
class AuthorityError(RuntimeError):pass

def effective_caps():
    for line in open('/proc/self/status',encoding='utf-8'):
        if line.startswith('CapEff:'):return int(line.split()[1],16)
    raise AuthorityError('CapEff unavailable')
def assert_capability_boundary():
    if effective_caps()!=(1<<CAP_NET_ADMIN):raise AuthorityError('exact CAP_NET_ADMIN required')
def collect_fixed_files(items):
    return [{'role':x['role'],'path':x['path'],**require_file_identity(x['path'],x['sha256'],x.get('byte_count'))} for x in items]
def decode_genid(raw,descriptor):
    width=descriptor.get('width_bits');order=descriptor.get('byteorder');offset=descriptor.get('payload_offset',0)
    if width!=32 or order not in ('big','little') or not isinstance(offset,int) or offset<0 or len(raw)<offset+4:raise AuthorityError('exact GETGEN descriptor required')
    return int.from_bytes(raw[offset:offset+4],order)
def snapshot_identity(result):
    raw=b''.join(result['records']);return hashlib.sha256(raw).hexdigest()
def perform_firewall_stability(snapshot_fn,getgen_fn,window_open_fn,barrier_fn):
    opened=window_open_fn();g0,g0tx=getgen_fn();a=snapshot_fn('A');b=snapshot_fn('B');g1,g1tx=getgen_fn();g2,g2tx=getgen_fn();bar=barrier_fn(opened)
    evaluate(snapshot_a_valid=a['valid'],snapshot_b_valid=b['valid'],snapshot_a_sha256=a['sha256'],snapshot_b_sha256=b['sha256'],genid_open=g0,genid_after_b=g1,genid_final=g2,notification_count=bar['notification_count_during_window'],barrier_healthy=bar['healthy'],barrier_durable=bool(bar.get('durable_ack_record_sha256')))
    return {'window_open':opened,'snapshot_a':a,'snapshot_b':b,'genid_open':g0,'genid_after_b':g1,'genid_final':g2,'getgen_transactions':[g0tx,g1tx,g2tx],'notification_barrier':bar}
def _netlink_socket(requested_rcvbuf):
    s=socket.socket(socket.AF_NETLINK,socket.SOCK_RAW,socket.NETLINK_NETFILTER);s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,requested_rcvbuf);effective=s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF);s.bind((0,0));return s,requested_rcvbuf,effective
def _barrier_transaction(path,request,cfg6):
    b=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(b)
    try:
        b.connect(path);b.send(canonical_bytes(request));raw,cred,_,_=recv_authenticated(b)
        policy=cfg6['monitor_peer_policy'];bind_source(cred,expected_uid=policy['uid'],expected_gid=policy['gid'],expected_instrument_identity=policy['instrument_identity'],expected_process=policy['expected_process'])
    finally:b.close()
    if not raw:raise AuthorityError('nftables monitor barrier response missing')
    return canonical_loads(raw)
def run_firewall_stability(cfg6,ru,no):
    assert_resolved({'snapshot_request_hex':cfg6['snapshot_request_hex'],'getgen_request_hex':cfg6['getgen_request_hex']},'exact nftables UAPI requests')
    snapshot_request=bytes.fromhex(cfg6['snapshot_request_hex']);getgen_request=bytes.fromhex(cfg6['getgen_request_hex']);seq=cfg6['request_sequence_start'];descriptor=cfg6['getgen_descriptor'];sock,requested,effective=_netlink_socket(cfg6['requested_so_rcvbuf']);barrier_id=os.urandom(16).hex()
    try:
        def snapshot(_label):
            nonlocal seq
            result=recv_complete_dump(sock,snapshot_request,seq,requested_so_rcvbuf=requested);seq+=1
            if result['effective_so_rcvbuf']!=effective:raise AuthorityError('snapshot socket receive-buffer drift')
            return {'valid':True,'sha256':snapshot_identity(result),'requested_so_rcvbuf':requested,'effective_so_rcvbuf':effective,'raw_transaction':result['raw_transaction']}
        def getgen():
            nonlocal seq
            result=recv_complete_dump(sock,getgen_request,seq,requested_so_rcvbuf=requested);seq+=1
            if len(result['records'])!=1:raise AuthorityError('GETGEN must return one scientific record')
            return decode_genid(result['records'][0],descriptor),result['raw_transaction']
        def window_open():
            req={'record_type':'NFTABLES_STABILITY_WINDOW_OPEN_REQUEST','barrier_id':barrier_id,'runtime_instance_uuid':ru,'observation_nonce':no};response=_barrier_transaction(cfg6['monitor_barrier_socket'],req,cfg6)
            required={'record_type','barrier_id','runtime_instance_uuid','observation_nonce','window_baseline_total_notifications','monitor_source_sequence_at_window_open','requested_so_rcvbuf','effective_so_rcvbuf','durable_ack_host_sequence','durable_ack_record_sha256','healthy'}
            if set(response)!=required or response['record_type']!='NFTABLES_STABILITY_WINDOW_OPEN_ACK' or response['barrier_id']!=barrier_id or response['runtime_instance_uuid']!=ru or response['observation_nonce']!=no or not response['healthy']:raise AuthorityError('window-open barrier binding mismatch')
            return response
        def barrier(opened):
            req={'record_type':'NFTABLES_NOTIFICATION_BARRIER_REQUEST','barrier_id':barrier_id,'runtime_instance_uuid':ru,'observation_nonce':no,'window_baseline_total_notifications':opened['window_baseline_total_notifications'],'monitor_source_sequence_at_window_open':opened['monitor_source_sequence_at_window_open']};response=_barrier_transaction(cfg6['monitor_barrier_socket'],req,cfg6)
            expected={'record_type','barrier_id','runtime_instance_uuid','observation_nonce','window_baseline_total_notifications','total_notifications_at_barrier','monitor_source_sequence_at_window_open','monitor_source_sequence_at_barrier','requested_so_rcvbuf','effective_so_rcvbuf','enobufs_observed','msg_trunc_observed','nlmsg_overrun_observed','receiver_continuity','notification_count_during_window','durable_ack_host_sequence','durable_ack_record_sha256','healthy'}
            if set(response)!=expected or response['record_type']!='NFTABLES_NOTIFICATION_BARRIER' or response['barrier_id']!=barrier_id or response['runtime_instance_uuid']!=ru or response['observation_nonce']!=no:raise AuthorityError('notification barrier binding mismatch')
            if response['enobufs_observed'] or response['msg_trunc_observed'] or response['nlmsg_overrun_observed'] or not response['receiver_continuity'] or not response['healthy']:raise AuthorityError('notification barrier unhealthy')
            return response
        return perform_firewall_stability(snapshot,getgen,window_open,barrier)
    finally:sock.close()
def consume_start_gate(cfg5,binding):
    s=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(s);s.settimeout(cfg5['producer_ack_timeout_seconds'])
    try:
        s.connect(cfg5['guest_start_gate_socket']);req={'record_type':'START_GATE_REQUEST','runtime_instance_uuid':binding['runtime_instance_uuid'],'observation_nonce':binding['observation_nonce'],'runtime_instantiation_attestation_record_sha256':binding['runtime_instantiation_attestation_record_sha256']};s.send(canonical_bytes(req));raw,cred,_,_=recv_authenticated(s)
        policy=cfg5['guest_mux_provider_policy'];bind_source(cred,expected_uid=policy['uid'],expected_gid=policy['gid'],expected_instrument_identity=policy['instrument_identity'],expected_process=policy['expected_process'])
    finally:s.close()
    if not raw:raise AuthorityError('pre-E1 start token missing')
    token=canonical_loads(raw)
    required={'runtime_instance_uuid','observation_nonce','verifier_result_sha256','runtime_instantiation_attestation_record_sha256','host_sequence_of_durable_verifier_result','observation_start_host_sequence'}
    if set(token)!=required or token['runtime_instance_uuid']!=binding['runtime_instance_uuid'] or token['observation_nonce']!=binding['observation_nonce'] or token['runtime_instantiation_attestation_record_sha256']!=binding['runtime_instantiation_attestation_record_sha256']:raise AuthorityError('pre-E1 start token binding mismatch')
    if len(token['verifier_result_sha256'])!=64 or token['observation_start_host_sequence']<=token['host_sequence_of_durable_verifier_result']:raise AuthorityError('pre-E1 start token durability/order invalid')
    return token
def _send(mux,seq,ru,no,obj,cfg5):
    source=scientific_process_instance(INSTRUMENT_IDENTITY);packet=pack_local_packet(SOURCE_TYPE,seq,ru,no,canonical_bytes(obj));mux.send(packet);raw,cred,_,_=recv_authenticated(mux)
    if not raw:raise AuthorityError('durable producer ACK missing')
    policy=cfg5['guest_mux_provider_policy'];bind_source(cred,expected_uid=policy['uid'],expected_gid=policy['gid'],expected_instrument_identity=policy['instrument_identity'],expected_process=policy['expected_process'])
    ack=canonical_loads(raw);validate_producer_ack(ack,source_sequence=seq,runtime_instance_uuid=ru,observation_nonce=no,source_instance_identity=source,producer_transaction_bytes=packet);return seq+1,ack
def main():
    assert_capability_boundary();cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_007/blocker_007_config_v1.json');cfg6=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_006/blocker_006_config_v1.json');cfg5=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json');binding=read_runtime_binding_file(cfg5['guest_runtime_binding_path']);ru=binding['runtime_instance_uuid'];no=binding['observation_nonce']
    token=consume_start_gate(cfg5,binding)
    files=collect_fixed_files(cfg['fixed_file_observations']);stability=run_firewall_stability(cfg6,ru,no)
    mux=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(mux);mux.settimeout(cfg['producer_ack_timeout_seconds']);mux.connect(cfg['guest_mux_socket']);seq=0
    try:
        seq,ack1=_send(mux,seq,ru,no,{'record_type':'OBSERVATION_AUTHORITY_STATE','runtime_instance_uuid':ru,'observation_nonce':no,'instrument_identity':INSTRUMENT_IDENTITY,'cap_eff':effective_caps(),'monitor_process_independent':True,'fixed_file_observations':files,'pre_e1_verifier_result_sha256':token['verifier_result_sha256'],'observation_start_host_sequence':token['observation_start_host_sequence']},cfg5)
        result={'record_type':'NFTABLES_STABILITY_RESULT','runtime_instance_uuid':ru,'observation_nonce':no,'classification':'PASS','snapshot_a_sha256':stability['snapshot_a']['sha256'],'snapshot_b_sha256':stability['snapshot_b']['sha256'],'genid_open':stability['genid_open'],'genid_after_b':stability['genid_after_b'],'genid_final':stability['genid_final'],'notification_count':stability['notification_barrier']['notification_count_during_window'],'snapshot_a_raw_transaction':stability['snapshot_a']['raw_transaction'],'snapshot_b_raw_transaction':stability['snapshot_b']['raw_transaction'],'getgen_raw_transactions':stability['getgen_transactions'],'window_open_durable_record_sha256':stability['window_open']['durable_ack_record_sha256'],'barrier_durable_record_sha256':stability['notification_barrier']['durable_ack_record_sha256']}
        seq,ack2=_send(mux,seq,ru,no,result,cfg5)
        durable_write(cfg['observation_boundaries_path'],canonical_bytes({'runtime_instance_uuid':ru,'observation_nonce':no,'observation_start_host_sequence':token['observation_start_host_sequence'],'observation_end_host_sequence':ack2['host_sequence']}))
    finally:mux.close()
if __name__=='__main__':main()
