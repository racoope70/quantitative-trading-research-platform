from __future__ import annotations
import hashlib, struct, uuid
from dataclasses import dataclass

MAGIC=b'C3E1'; VERSION=1; ORIGIN_GUEST=1; ORIGIN_HOST=2; MAX_U64=(1<<64)-1
DOMAIN=b'C3_E1_HOST_EVIDENCE_RECORD_V1\0'
_GUEST=struct.Struct('>4sHHQIQ')
_LOCAL=struct.Struct('>4sHHQ16s32sI')
_ACK=struct.Struct('>4sQQQ16s32s32s32s32s')
_RUNTIME=struct.Struct('>4s16s32s32s')
_TOKEN=struct.Struct('>4s16s32s32s32sQ')
_LOCAL_MAGIC=b'C3P2'; _ACK_MAGIC=b'C3A2'; _RUNTIME_MAGIC=b'C3R1'; _TOKEN_MAGIC=b'C3T1'

class ProtocolError(ValueError): pass

def _u64(v,n):
    if isinstance(v,bool) or not isinstance(v,int) or not 0<=v<=MAX_U64: raise ProtocolError(f'{n}: uint64 required')
    return v

def _sha(v,n):
    if isinstance(v,str):
        if len(v)!=64 or v.lower()!=v: raise ProtocolError(f'{n}: lowercase SHA256 hex required')
        try: v=bytes.fromhex(v)
        except ValueError as e: raise ProtocolError(f'{n}: SHA256 hex required') from e
    if not isinstance(v,bytes) or len(v)!=32: raise ProtocolError(f'{n}: 32 bytes required')
    return v

def uuid_bytes(v):
    if isinstance(v,bytes):
        if len(v)!=16: raise ProtocolError('runtime UUID width')
        return v
    try: u=uuid.UUID(v)
    except Exception as e: raise ProtocolError('runtime UUID required') from e
    if str(u)!=v.lower(): raise ProtocolError('canonical runtime UUID required')
    return u.bytes

def uuid_text(b):
    if len(b)!=16: raise ProtocolError('runtime UUID width')
    return str(uuid.UUID(bytes=b))

def nonce_bytes(v):
    if isinstance(v,bytes):
        if len(v)!=32: raise ProtocolError('nonce width')
        return v
    if not isinstance(v,str) or len(v)!=64 or v.lower()!=v: raise ProtocolError('nonce lowercase hex required')
    try: b=bytes.fromhex(v)
    except ValueError as e: raise ProtocolError('nonce hex required') from e
    if len(b)!=32: raise ProtocolError('nonce width')
    return b

def sha256_hex(b): return hashlib.sha256(b).hexdigest()
def source_instance_digest(s):
    if not isinstance(s,str) or not s: raise ProtocolError('source instance required')
    return hashlib.sha256(s.encode()).digest()

def pack_guest_frame(source_type,guest_sequence,metadata_bytes,raw_evidence):
    if not isinstance(source_type,int) or not 0<=source_type<=0xffff: raise ProtocolError('source type')
    _u64(guest_sequence,'guest_sequence')
    if len(metadata_bytes)>0xffffffff: raise ProtocolError('metadata too long')
    return _GUEST.pack(MAGIC,VERSION,source_type,guest_sequence,len(metadata_bytes),len(raw_evidence))+metadata_bytes+raw_evidence

def unpack_guest_frame(frame):
    if len(frame)<_GUEST.size: raise ProtocolError('truncated guest frame')
    magic,ver,stype,gseq,mlen,rlen=_GUEST.unpack_from(frame)
    if magic!=MAGIC or ver!=VERSION: raise ProtocolError('guest frame identity/version')
    end=_GUEST.size+mlen+rlen
    if end!=len(frame): raise ProtocolError('guest frame length')
    return {'source_type':stype,'guest_sequence':gseq,'metadata_bytes':frame[_GUEST.size:_GUEST.size+mlen],'raw_evidence':frame[_GUEST.size+mlen:]}

def recv_exact(stream,n):
    out=bytearray()
    while len(out)<n:
        b=stream.recv(n-len(out))
        if not b: raise EOFError('stream closed')
        out.extend(b)
    return bytes(out)

def recv_guest_frame(stream):
    head=recv_exact(stream,_GUEST.size); magic,ver,st,g,m,r=_GUEST.unpack(head)
    if magic!=MAGIC or ver!=VERSION: raise ProtocolError('guest stream frame identity')
    return head+recv_exact(stream,m+r)

def recv_host_control(stream):
    magic=recv_exact(stream,4)
    if magic==_ACK_MAGIC: return 'ACK',unpack_ack(magic+recv_exact(stream,_ACK.size-4))
    if magic==_TOKEN_MAGIC: return 'START_TOKEN',unpack_start_token(magic+recv_exact(stream,_TOKEN.size-4))
    raise ProtocolError(f'unknown host-control magic: {magic!r}')

def pack_local_packet(source_type,source_sequence,runtime_instance_uuid,observation_nonce,raw_evidence):
    if not isinstance(source_type,int) or not 0<=source_type<=0xffff: raise ProtocolError('source type')
    _u64(source_sequence,'source_sequence')
    if len(raw_evidence)>0xffffffff: raise ProtocolError('local evidence too long')
    return _LOCAL.pack(_LOCAL_MAGIC,VERSION,source_type,source_sequence,uuid_bytes(runtime_instance_uuid),nonce_bytes(observation_nonce),len(raw_evidence))+raw_evidence

def unpack_local_packet(packet):
    if len(packet)<_LOCAL.size: raise ProtocolError('truncated local packet')
    magic,ver,st,seq,ru,no,n=_LOCAL.unpack_from(packet)
    if magic!=_LOCAL_MAGIC or ver!=VERSION or len(packet)!=_LOCAL.size+n: raise ProtocolError('local packet mismatch')
    return {'source_type':st,'source_sequence':seq,'runtime_instance_uuid':uuid_text(ru),'observation_nonce':no.hex(),'raw_evidence':packet[_LOCAL.size:]}

def pack_ack(*,guest_sequence,source_sequence,host_sequence,runtime_instance_uuid,observation_nonce,source_instance_identity,transaction_sha256,record_sha256):
    for n,v in [('guest_sequence',guest_sequence),('source_sequence',source_sequence),('host_sequence',host_sequence)]: _u64(v,n)
    return _ACK.pack(_ACK_MAGIC,guest_sequence,source_sequence,host_sequence,uuid_bytes(runtime_instance_uuid),nonce_bytes(observation_nonce),source_instance_digest(source_instance_identity),_sha(transaction_sha256,'transaction'),_sha(record_sha256,'record'))

def unpack_ack(data):
    if len(data)!=_ACK.size: raise ProtocolError('ACK length')
    m,g,s,h,ru,no,src,tx,rec=_ACK.unpack(data)
    if m!=_ACK_MAGIC: raise ProtocolError('ACK magic')
    return {'guest_sequence':g,'source_sequence':s,'host_sequence':h,'runtime_instance_uuid':uuid_text(ru),'observation_nonce':no.hex(),'source_instance_sha256':src.hex(),'transaction_sha256':tx.hex(),'record_sha256':rec.hex()}

def ack_size(): return _ACK.size

def pack_runtime_binding(runtime_instance_uuid,observation_nonce,runtime_record_sha256):
    return _RUNTIME.pack(_RUNTIME_MAGIC,uuid_bytes(runtime_instance_uuid),nonce_bytes(observation_nonce),_sha(runtime_record_sha256,'runtime_record'))

def unpack_runtime_binding(data):
    if len(data)!=_RUNTIME.size: raise ProtocolError('runtime binding length')
    m,ru,no,sha=_RUNTIME.unpack(data)
    if m!=_RUNTIME_MAGIC: raise ProtocolError('runtime binding magic')
    return {'runtime_instance_uuid':uuid_text(ru),'observation_nonce':no.hex(),'runtime_instantiation_attestation_record_sha256':sha.hex()}

def runtime_binding_size(): return _RUNTIME.size

def pack_start_token(runtime_instance_uuid,observation_nonce,verifier_result_sha256,runtime_record_sha256,host_sequence):
    _u64(host_sequence,'host_sequence')
    return _TOKEN.pack(_TOKEN_MAGIC,uuid_bytes(runtime_instance_uuid),nonce_bytes(observation_nonce),_sha(verifier_result_sha256,'verifier_result'),_sha(runtime_record_sha256,'runtime_record'),host_sequence)

def unpack_start_token(data):
    if len(data)!=_TOKEN.size: raise ProtocolError('start token length')
    m,ru,no,vr,rr,hs=_TOKEN.unpack(data)
    if m!=_TOKEN_MAGIC: raise ProtocolError('start token magic')
    return {'runtime_instance_uuid':uuid_text(ru),'observation_nonce':no.hex(),'verifier_result_sha256':vr.hex(),'runtime_instantiation_attestation_record_sha256':rr.hex(),'host_sequence_of_durable_verifier_result':hs}

def start_token_size(): return _TOKEN.size

def host_record_preimage(origin,host_sequence,monotonic_ns,utc_ns,previous_sha256,payload):
    if origin not in (ORIGIN_GUEST,ORIGIN_HOST): raise ProtocolError('origin')
    for n,v in [('host_sequence',host_sequence),('monotonic_ns',monotonic_ns),('utc_ns',utc_ns)]: _u64(v,n)
    return DOMAIN+bytes([origin])+struct.pack('>QQQ',host_sequence,monotonic_ns,utc_ns)+_sha(previous_sha256,'previous_sha256')+struct.pack('>Q',len(payload))+payload

def host_record_hash(**kw): return hashlib.sha256(host_record_preimage(**kw)).digest()

@dataclass(frozen=True)
class SequenceState:
    next_value:int=0
    def consume(self,value):
        _u64(value,'sequence')
        if value!=self.next_value: raise ProtocolError(f'sequence mismatch expected {self.next_value} got {value}')
        if value==MAX_U64: raise ProtocolError('sequence exhausted')
        return SequenceState(value+1)

def validate_guest_metadata(md,*,source_type,raw_evidence,expected_runtime_uuid,expected_nonce):
    required={'runtime_instance_uuid','observation_nonce','source_instance_identity','source_sequence','source_native_identity','guest_boot_id','guest_monotonic_timestamp_ns','raw_evidence_byte_count','raw_evidence_sha256'}
    if set(md)!=required: raise ProtocolError(f'guest metadata fields mismatch: {sorted(set(md)^required)}')
    if md['runtime_instance_uuid']!=expected_runtime_uuid or md['observation_nonce']!=expected_nonce: raise ProtocolError('host-bound runtime UUID/nonce mismatch')
    if md['raw_evidence_byte_count']!=len(raw_evidence) or md['raw_evidence_sha256']!=sha256_hex(raw_evidence): raise ProtocolError('raw evidence identity mismatch')
    _u64(md['source_sequence'],'source_sequence'); _u64(md['guest_monotonic_timestamp_ns'],'guest timestamp')
    for k in ['source_instance_identity','source_native_identity','guest_boot_id']:
        if not isinstance(md[k],str) or not md[k] or md[k].startswith('UNRESOLVED'): raise ProtocolError(f'{k} must be observed/resolved')
    return md

def validate_ack(ack,*,guest_sequence,source_sequence,runtime_instance_uuid,observation_nonce,source_instance_identity,transaction_bytes):
    expected={'guest_sequence':guest_sequence,'source_sequence':source_sequence,'runtime_instance_uuid':runtime_instance_uuid,'observation_nonce':observation_nonce,'source_instance_sha256':source_instance_digest(source_instance_identity).hex(),'transaction_sha256':sha256_hex(transaction_bytes)}
    for k,v in expected.items():
        if ack.get(k)!=v: raise ProtocolError(f'ACK binding mismatch: {k}')
    if not isinstance(ack.get('host_sequence'),int) or not isinstance(ack.get('record_sha256'),str) or len(ack['record_sha256'])!=64: raise ProtocolError('ACK durable record identity missing')
    return ack

def make_host_ack(*,runtime_instance_uuid,observation_nonce,source_instance_identity,source_sequence,host_sequence,payload,record_sha256):
    _u64(source_sequence,'source_sequence'); _u64(host_sequence,'host_sequence'); _sha(record_sha256,'record_sha256')
    return {'durable':True,'runtime_instance_uuid':runtime_instance_uuid,'observation_nonce':observation_nonce,'source_instance_sha256':source_instance_digest(source_instance_identity).hex(),'source_sequence':source_sequence,'host_sequence':host_sequence,'transaction_sha256':sha256_hex(payload),'record_sha256':record_sha256 if isinstance(record_sha256,str) else record_sha256.hex()}

def validate_host_ack(ack,*,runtime_instance_uuid,observation_nonce,source_instance_identity,source_sequence,payload):
    expected={'durable':True,'runtime_instance_uuid':runtime_instance_uuid,'observation_nonce':observation_nonce,'source_instance_sha256':source_instance_digest(source_instance_identity).hex(),'source_sequence':source_sequence,'transaction_sha256':sha256_hex(payload)}
    for k,v in expected.items():
        if ack.get(k)!=v: raise ProtocolError(f'host ACK binding mismatch: {k}')
    _u64(ack.get('host_sequence'),'host_sequence'); _sha(ack.get('record_sha256'),'record_sha256')
    return ack
