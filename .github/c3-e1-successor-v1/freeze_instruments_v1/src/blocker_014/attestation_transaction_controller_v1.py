from __future__ import annotations
import hashlib,os,socket,ssl,time,struct
from pathlib import Path
from identity_io_v1 import canonical_bytes,canonical_loads,canonical_sha256,read_json,validate_schema_file,require_file_identity
from quote_acquisition_v1 import acquire_quote
from evidence_protocol_v1 import validate_host_ack
from ipc_peer_auth_v1 import enable_seqpacket_credentials,recv_authenticated,bind_source
from process_identity_v1 import process_identity
PRE=b'C3_E1_QUOTE_QUALIFICATION_V1\0';POST=b'C3_E1_POST_OBSERVATION_CHECKPOINT_ATTESTATION_V1\0'
class AttestationError(RuntimeError):pass
_LEN=struct.Struct('>Q')
def _recv_exact(sock,n):
    out=bytearray()
    while len(out)<n:
        b=sock.recv(n-len(out))
        if not b:raise AttestationError('TLS transaction truncated')
        out.extend(b)
    return bytes(out)
def pre_qualification(ru,no,rr,v):
    if [len(x) for x in (ru,no,rr,v)]!=[16,32,32,32]:raise AttestationError('pre binding width')
    return hashlib.sha256(PRE+ru+no+rr+v).digest()
def post_qualification(ru,no,ch,final_seq,final_hash,checkpoint,start_seq,end_seq,rr,v):
    if len(ru)!=16 or any(len(x)!=32 for x in (no,ch,final_hash,checkpoint,rr,v)):raise AttestationError('post binding width')
    return hashlib.sha256(POST+ru+no+ch+final_seq.to_bytes(8,'big')+final_hash+checkpoint+start_seq.to_bytes(8,'big')+end_seq.to_bytes(8,'big')+rr+v).digest()
def require_pass(result,expected):
    if result.get('classification')!='PASS':raise AttestationError('verifier PASS required')
    for k,v in expected.items():
        if result.get(k)!=v:raise AttestationError(f'verifier binding {k}')
def tls_transaction(cfg,obj):
    for k in ('verifier_endpoint_host','client_cert','client_key','server_ca','verifier_server_name'):
        if str(cfg.get(k,'')).startswith('UNRESOLVED'):raise AttestationError(f'transport unresolved {k}')
    ctx=ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile=cfg['server_ca']);ctx.minimum_version=ssl.TLSVersion.TLSv1_3;ctx.maximum_version=ssl.TLSVersion.TLSv1_3;ctx.load_cert_chain(cfg['client_cert'],cfg['client_key'])
    with socket.create_connection((cfg['verifier_endpoint_host'],cfg['verifier_endpoint_port']),timeout=cfg['transaction_timeout_seconds']) as s:
        with ctx.wrap_socket(s,server_hostname=cfg['verifier_server_name']) as t:
            raw=canonical_bytes(obj);t.sendall(_LEN.pack(len(raw))+raw);n=_LEN.unpack(_recv_exact(t,_LEN.size))[0]
            if n<=0 or n>cfg['max_transaction_bytes']:raise AttestationError('verifier response size invalid')
            response=canonical_loads(_recv_exact(t,n));validate_schema_file(response,cfg['attestation_schema_path']);return response
def _source_instance():
    i=process_identity(os.getpid());return f"C3_E1_SUCCESSOR_ATTESTATION_TRANSACTION_CONTROLLER_V1:{i['pid']}:{i['starttime']}:{i['executable_sha256']}:{i['cmdline_sha256']}:{i['cgroup_sha256']}"
class SinkClient:
    def __init__(self,cfg,ru,no):
        self.cfg=cfg;self.ru=ru;self.no=no;self.seq=0;self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);enable_seqpacket_credentials(self.sock);self.sock.settimeout(cfg['transaction_timeout_seconds']);self.sock.connect(cfg['host_sink_socket'])
    def event(self,obj):
        payload=canonical_bytes(obj);self.sock.send(canonical_bytes({'_transport_source_sequence':self.seq,**obj}));raw,cred,_,_=recv_authenticated(self.sock)
        if not raw:raise AttestationError('host sink durable ACK missing')
        hp=self.cfg['host_sink_peer_policy'];bind_source(cred,expected_uid=hp['uid'],expected_gid=hp['gid'],expected_instrument_identity=hp['instrument_identity'],expected_process=hp['expected_process'])
        ack=canonical_loads(raw);validate_host_ack(ack,runtime_instance_uuid=self.ru,observation_nonce=self.no,source_instance_identity=_source_instance(),source_sequence=self.seq,payload=payload);self.seq+=1;return ack
    def close(self):self.sock.close()
def sink_event(cfg,obj,seq):
    # compatibility helper for bounded unit tests; production uses one persistent SinkClient.
    c=SinkClient(cfg,obj['runtime_instance_uuid'],obj['observation_nonce']);c.seq=seq
    try:return c.event(obj)
    finally:c.close()
def derive_qualification_root(pre_sha,post_sha,checkpoint_sha):
    try:parts=[bytes.fromhex(x) for x in (pre_sha,post_sha,checkpoint_sha)]
    except Exception as e:raise AttestationError('qualification identities') from e
    if any(len(x)!=32 for x in parts):raise AttestationError('qualification widths')
    return hashlib.sha256(b'C3_E1_SUCCESSOR_ENVIRONMENT_QUALIFICATION_ROOT_V1\0'+b''.join(parts)).hexdigest()
def _meta(role,raw):return {'role':role,'byte_count':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'data_hex':raw.hex()}
def _load_runtime_input(cfg):
    deadline=time.monotonic()+cfg['runtime_transaction_input_timeout_seconds']
    while time.monotonic()<deadline:
        if Path(cfg['runtime_transaction_input_path']).is_file() and Path(cfg['runtime_transaction_input_reference_path']).is_file():break
        time.sleep(.05)
    else:raise AttestationError('runtime attestation input not produced')
    ref=read_json(cfg['runtime_transaction_input_reference_path']);required={'record_type','runtime_instance_uuid','observation_nonce','runtime_record_sha256','path','byte_count','sha256'}
    if set(ref)!=required or ref['record_type']!='RUNTIME_ATTESTATION_INPUT_REFERENCE' or ref['path']!=cfg['runtime_transaction_input_path']:raise AttestationError('runtime attestation input reference fields')
    require_file_identity(ref['path'],ref['sha256'],ref['byte_count']);r=read_json(ref['path']);validate_schema_file(r,cfg['record_schema_path'])
    if r['runtime_instance_uuid']!=ref['runtime_instance_uuid'] or r['observation_nonce']!=ref['observation_nonce'] or r['runtime_record_sha256']!=ref['runtime_record_sha256']:raise AttestationError('runtime attestation input reference binding')
    if canonical_sha256(r['runtime_instantiation_record'])!=r['runtime_record_sha256'] or r['runtime_instantiation_record']['runtime_instance_uuid']!=r['runtime_instance_uuid'] or r['runtime_instantiation_record']['observation_nonce']!=r['observation_nonce']:raise AttestationError('runtime attestation record object binding')
    if r['verifier_manifest_sha256']!=cfg['verifier_manifest_sha256']:raise AttestationError('runtime attestation input verifier-manifest binding')
    return r
def _objects_from_input(r,roles):
    allowed=r['evidence_inputs'];out={}
    for role in roles:
        if role not in allowed:raise AttestationError(f'attestation evidence role not bound: {role}')
        spec=allowed[role]
        if set(spec)!={'path','byte_count','sha256'}:raise AttestationError(f'attestation evidence identity fields: {role}')
        path=Path(spec['path'])
        if not path.is_absolute() or not path.is_file():raise AttestationError(f'attestation evidence unavailable: {role}')
        require_file_identity(path,spec['sha256'],spec['byte_count']);out[role]=_meta(role,path.read_bytes())
    if 'verification_context' in out:raise AttestationError('host-supplied verification context prohibited')
    return out
def _runtime_record_object(r):
    raw=canonical_bytes(r['runtime_instantiation_record'])
    if hashlib.sha256(raw).hexdigest()!=r['runtime_record_sha256']:raise AttestationError('runtime record object identity mismatch')
    return _meta('runtime_instantiation_record',raw)

def _bind_quote_objects(objects,quote):
    for role in ('quote_message','quote_signature','quoted_pcr_bytes'):objects[role]=_meta(role,quote[role])
    return objects
def run_pre_e1(cfg,r,sink=None):
    q=pre_qualification(bytes.fromhex(r['runtime_uuid_hex']),bytes.fromhex(r['observation_nonce']),bytes.fromhex(r['runtime_record_sha256']),bytes.fromhex(cfg['verifier_manifest_sha256']))
    quote=acquire_quote(cfg['tpm2_quote_path'],cfg['quote_args_template'],q.hex());objects=_objects_from_input(r,r['pre_attestation_roles']);objects['runtime_instantiation_record']=_runtime_record_object(r);objects=_bind_quote_objects(objects,quote)
    b={'transaction_type':'PRE_E1_ATTESTATION','transaction_id':os.urandom(16).hex(),'runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'runtime_instantiation_attestation_record_sha256':r['runtime_record_sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256'],'quote_qualification':q.hex(),'objects':objects}
    validate_schema_file(b,cfg['attestation_schema_path']);res=tls_transaction(cfg,b);require_pass(res,{'runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'runtime_instantiation_attestation_record_sha256':r['runtime_record_sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256']});sha=canonical_sha256(res)
    own=False
    if sink is None:sink=SinkClient(cfg,r['runtime_instance_uuid'],r['observation_nonce']);own=True
    try:
        sink.event({'record_type':'PRE_E1_VERIFIER_RESULT','runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'runtime_instantiation_attestation_record_sha256':r['runtime_record_sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256'],'verifier_result_sha256':sha,'classification':'PASS'})
        sink.event({'record_type':'START_TOKEN_RELEASE_REQUEST','runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce']})
    finally:
        if own:sink.close()
    return sha
def request_final_checkpoint(cfg,r,bounds,sink=None):
    req={'record_type':'FINAL_CHECKPOINT_REQUEST','runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'observation_start_host_sequence':bounds['observation_start_host_sequence'],'observation_end_host_sequence':bounds['observation_end_host_sequence'],'checkpoint_path':cfg['final_checkpoint_path'],'checkpoint_reference_path':cfg['final_checkpoint_reference_path']}
    own=False
    if sink is None:sink=SinkClient(cfg,r['runtime_instance_uuid'],r['observation_nonce']);own=True
    try:return sink.event(req)
    finally:
        if own:sink.close()
def run_post(cfg,r,c,pre_sha):
    req={'transaction_type':'POST_OBSERVATION_CHALLENGE_REQUEST','runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'final_checkpoint_sha256':c['sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256']};ch=tls_transaction(cfg,req)
    q=post_qualification(bytes.fromhex(r['runtime_uuid_hex']),bytes.fromhex(r['observation_nonce']),bytes.fromhex(ch['fresh_challenge']),c['final_host_sequence'],bytes.fromhex(c['final_record_sha256']),bytes.fromhex(c['sha256']),c['observation_start_host_sequence'],c['observation_end_host_sequence'],bytes.fromhex(r['runtime_record_sha256']),bytes.fromhex(cfg['verifier_manifest_sha256']))
    quote=acquire_quote(cfg['tpm2_quote_path'],cfg['quote_args_template'],q.hex());objects=_objects_from_input(r,r['post_attestation_roles']);objects['runtime_instantiation_record']=_runtime_record_object(r);objects=_bind_quote_objects(objects,quote);objects['final_checkpoint']=_meta('final_checkpoint',canonical_bytes({k:v for k,v in c.items() if k!='sha256'}))
    b={'transaction_type':'POST_OBSERVATION_ATTESTATION','transaction_id':ch['transaction_id'],'runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'runtime_instantiation_attestation_record_sha256':r['runtime_record_sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256'],'final_checkpoint_sha256':c['sha256'],'fresh_challenge':ch['fresh_challenge'],'quote_qualification':q.hex(),'objects':objects}
    validate_schema_file(b,cfg['attestation_schema_path']);res=tls_transaction(cfg,b);require_pass(res,{'runtime_instance_uuid':r['runtime_instance_uuid'],'observation_nonce':r['observation_nonce'],'final_checkpoint_sha256':c['sha256'],'verifier_manifest_sha256':cfg['verifier_manifest_sha256']});return derive_qualification_root(pre_sha,canonical_sha256(res),c['sha256'])
def main():
    cfg=read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_014/blocker_014_config_v1.json');r=_load_runtime_input(cfg);sink=SinkClient(cfg,r['runtime_instance_uuid'],r['observation_nonce'])
    try:
        pre=run_pre_e1(cfg,r,sink)
        while not os.path.exists(cfg['observation_boundaries_path']):time.sleep(.5)
        request_final_checkpoint(cfg,r,read_json(cfg['observation_boundaries_path']),sink)
    finally:sink.close()
    while not(os.path.exists(cfg['final_checkpoint_reference_path']) and os.path.exists(cfg['lifecycle_final_marker_path'])):time.sleep(.5)
    c=read_json(cfg['final_checkpoint_reference_path']);print(run_post(cfg,r,c,pre))
if __name__=='__main__':main()
