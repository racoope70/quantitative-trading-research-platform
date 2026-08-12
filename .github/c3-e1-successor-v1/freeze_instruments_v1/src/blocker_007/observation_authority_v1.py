from __future__ import annotations
import hashlib,os,socket
from evidence_protocol_v1 import pack_local_packet
from identity_io_v1 import canonical_bytes,canonical_loads,read_json,read_runtime_binding_file,require_file_identity,assert_resolved
from nftables_delivery_barrier_v1 import evaluate
from nftables_snapshot_v1 import recv_complete_dump
CAP_NET_ADMIN=12; SOURCE_TYPE=3
class AuthorityError(RuntimeError): pass

def effective_caps():
    for line in open('/proc/self/status',encoding='utf-8'):
        if line.startswith('CapEff:'): return int(line.split()[1],16)
    raise AuthorityError('CapEff unavailable')
def assert_capability_boundary():
    if effective_caps() != (1<<CAP_NET_ADMIN): raise AuthorityError('exact CAP_NET_ADMIN required')
def collect_fixed_files(items):
    return [{'role':x['role'],'path':x['path'],**require_file_identity(x['path'],x['sha256'],x.get('byte_count'))} for x in items]
def decode_genid(raw,descriptor):
    width=descriptor.get('width_bits'); order=descriptor.get('byteorder'); offset=descriptor.get('payload_offset',0)
    if width!=32 or order not in ('big','little') or not isinstance(offset,int) or offset<0 or len(raw)<offset+4: raise AuthorityError('exact GETGEN descriptor required')
    return int.from_bytes(raw[offset:offset+4],order)
def snapshot_identity(result):
    raw=b''.join(result['records']); return hashlib.sha256(raw).hexdigest()
def perform_firewall_stability(snapshot_fn,getgen_fn,barrier_fn):
    g0=getgen_fn(); a=snapshot_fn('A'); b=snapshot_fn('B'); g1=getgen_fn(); bar=barrier_fn(); g2=getgen_fn()
    evaluate(snapshot_a_valid=a['valid'],snapshot_b_valid=b['valid'],snapshot_a_sha256=a['sha256'],snapshot_b_sha256=b['sha256'],genid_open=g0,genid_after_b=g1,genid_final=g2,notification_count=bar['notification_count'],barrier_healthy=bar['healthy'])
    return {'snapshot_a':a,'snapshot_b':b,'genid_open':g0,'genid_after_b':g1,'genid_final':g2,'notification_barrier':bar}
def _netlink_socket(requested_rcvbuf):
    s=socket.socket(socket.AF_NETLINK,socket.SOCK_RAW,socket.NETLINK_NETFILTER); s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,requested_rcvbuf); s.bind((0,0)); return s
def run_firewall_stability(cfg6,ru,no):
    assert_resolved({'snapshot_request_hex':cfg6['snapshot_request_hex'],'getgen_request_hex':cfg6['getgen_request_hex']},'exact nftables UAPI requests')
    snapshot_request=bytes.fromhex(cfg6['snapshot_request_hex']); getgen_request=bytes.fromhex(cfg6['getgen_request_hex']); seq=cfg6['request_sequence_start']; descriptor=cfg6['getgen_descriptor']; sock=_netlink_socket(cfg6['requested_so_rcvbuf'])
    try:
        def snapshot(_label):
            nonlocal seq
            result=recv_complete_dump(sock,snapshot_request,seq); seq+=1
            return {'valid':True,'sha256':snapshot_identity(result),'requested_so_rcvbuf':result['requested_so_rcvbuf'],'effective_so_rcvbuf':result['effective_so_rcvbuf']}
        def getgen():
            nonlocal seq
            result=recv_complete_dump(sock,getgen_request,seq); seq+=1
            if len(result['records'])!=1: raise AuthorityError('GETGEN must return one scientific record')
            return decode_genid(result['records'][0],descriptor)
        def barrier():
            b=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
            try:
                b.connect(cfg6['monitor_barrier_socket']); barrier_id=os.urandom(16).hex(); req={'record_type':'NFTABLES_NOTIFICATION_BARRIER_REQUEST','barrier_id':barrier_id,'runtime_instance_uuid':ru,'observation_nonce':no}; b.send(canonical_bytes(req)); response=canonical_loads(b.recv(65536))
            finally: b.close()
            expected={'record_type','runtime_instance_uuid','observation_nonce','barrier_id','notification_count','effective_so_rcvbuf','enobufs_observed','msg_trunc_observed','receiver_continuity','healthy'}
            if set(response)!=expected or response['barrier_id']!=barrier_id or response['runtime_instance_uuid']!=ru or response['observation_nonce']!=no: raise AuthorityError('notification barrier binding mismatch')
            if response['enobufs_observed'] or response['msg_trunc_observed'] or not response['receiver_continuity']: raise AuthorityError('notification barrier unhealthy')
            return response
        return perform_firewall_stability(snapshot,getgen,barrier)
    finally: sock.close()
def _send(mux,seq,ru,no,obj):
    mux.send(pack_local_packet(SOURCE_TYPE,seq,ru,no,canonical_bytes(obj))); return seq+1
def main():
    assert_capability_boundary(); cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_007/blocker_007_config_v1.json'); cfg6=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_006/blocker_006_config_v1.json'); cfg5=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_005/blocker_005_config_v1.json'); binding=read_runtime_binding_file(cfg5['guest_runtime_binding_path']); ru=binding['runtime_instance_uuid']; no=binding['observation_nonce']
    files=collect_fixed_files(cfg['fixed_file_observations']); stability=run_firewall_stability(cfg6,ru,no)
    mux=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET); mux.connect(cfg['guest_mux_socket']); seq=0
    try:
        seq=_send(mux,seq,ru,no,{'record_type':'OBSERVATION_AUTHORITY_STATE','runtime_instance_uuid':ru,'observation_nonce':no,'instrument_identity':'C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1','cap_eff':effective_caps(),'monitor_process_independent':True,'fixed_file_observations':files})
        _send(mux,seq,ru,no,{'record_type':'NFTABLES_STABILITY_RESULT','runtime_instance_uuid':ru,'observation_nonce':no,'classification':'PASS','snapshot_a_sha256':stability['snapshot_a']['sha256'],'snapshot_b_sha256':stability['snapshot_b']['sha256'],'genid_open':stability['genid_open'],'genid_after_b':stability['genid_after_b'],'genid_final':stability['genid_final'],'notification_count':stability['notification_barrier']['notification_count']})
    finally: mux.close()
if __name__=='__main__': main()
