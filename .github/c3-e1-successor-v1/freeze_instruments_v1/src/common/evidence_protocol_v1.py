"""C3 E1 successor freeze-instrument evidence framing and hash-chain primitives.

Pure protocol code only: no system observation, privilege changes, or mutation.
"""
from __future__ import annotations
import hashlib, struct
from dataclasses import dataclass

MAGIC=b"C3E1"; VERSION=1
_HEADER=struct.Struct(">4sHHQIQ")
ORIGIN_GUEST=1; ORIGIN_HOST=2
DOMAIN=b"C3_E1_HOST_EVIDENCE_RECORD_V1\0"
MAX_U64=(1<<64)-1

class ProtocolError(ValueError): pass

def _u64(v:int,name:str)->int:
    if not isinstance(v,int) or isinstance(v,bool) or not 0<=v<=MAX_U64:
        raise ProtocolError(f"{name}: uint64 required")
    return v

def sha256_hex(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def pack_guest_frame(source_type:int, guest_sequence:int, metadata_bytes:bytes, raw_evidence:bytes)->bytes:
    if not 0<=source_type<=0xffff: raise ProtocolError("source_type out of range")
    _u64(guest_sequence,"guest_sequence")
    if len(metadata_bytes)>0xffffffff: raise ProtocolError("metadata too long")
    return _HEADER.pack(MAGIC,VERSION,source_type,guest_sequence,len(metadata_bytes),len(raw_evidence))+metadata_bytes+raw_evidence

def unpack_guest_frame(frame:bytes):
    if len(frame)<_HEADER.size: raise ProtocolError("truncated frame header")
    magic,version,source_type,seq,mlen,rlen=_HEADER.unpack_from(frame)
    if magic!=MAGIC or version!=VERSION: raise ProtocolError("frame identity/version mismatch")
    end=_HEADER.size+mlen+rlen
    if end!=len(frame): raise ProtocolError("frame length mismatch")
    return {"source_type":source_type,"guest_sequence":seq,"metadata_bytes":frame[_HEADER.size:_HEADER.size+mlen],"raw_evidence":frame[_HEADER.size+mlen:end]}

def host_record_preimage(origin:int, host_sequence:int, monotonic_ns:int, utc_ns:int, previous_sha256:bytes, payload:bytes)->bytes:
    if origin not in (ORIGIN_GUEST,ORIGIN_HOST): raise ProtocolError("invalid origin")
    for n,v in (("host_sequence",host_sequence),("monotonic_ns",monotonic_ns),("utc_ns",utc_ns)): _u64(v,n)
    if len(previous_sha256)!=32: raise ProtocolError("previous SHA256 must be 32 bytes")
    return DOMAIN+bytes([origin])+struct.pack(">QQQ",host_sequence,monotonic_ns,utc_ns)+previous_sha256+struct.pack(">Q",len(payload))+payload

def host_record_hash(**kwargs)->bytes: return hashlib.sha256(host_record_preimage(**kwargs)).digest()

@dataclass(frozen=True)
class SequenceState:
    next_value:int=0
    def consume(self,value:int)->"SequenceState":
        _u64(value,"sequence")
        if value!=self.next_value: raise ProtocolError(f"sequence mismatch: expected {self.next_value}, got {value}")
        if value==MAX_U64: raise ProtocolError("sequence exhausted")
        return SequenceState(value+1)

_LOCAL_MAGIC=b"C3P1"; _LOCAL=struct.Struct(">4sHQI")
_ACK_MAGIC=b"C3A1"; _ACK=struct.Struct(">4sQQ32s")

def pack_local_packet(source_type:int, source_sequence:int, raw_evidence:bytes)->bytes:
    if not 0<=source_type<=0xffff: raise ProtocolError("source_type out of range")
    _u64(source_sequence,"source_sequence")
    if len(raw_evidence)>0xffffffff: raise ProtocolError("local evidence too long")
    return _LOCAL.pack(_LOCAL_MAGIC,source_type,source_sequence,len(raw_evidence))+raw_evidence

def unpack_local_packet(packet:bytes):
    if len(packet)<_LOCAL.size: raise ProtocolError("truncated local packet")
    magic,stype,seq,n=_LOCAL.unpack_from(packet)
    if magic!=_LOCAL_MAGIC or len(packet)!=_LOCAL.size+n: raise ProtocolError("local packet mismatch")
    return {"source_type":stype,"source_sequence":seq,"raw_evidence":packet[_LOCAL.size:]}

def pack_ack(guest_sequence:int,host_sequence:int,record_sha256:bytes)->bytes:
    _u64(guest_sequence,"guest_sequence"); _u64(host_sequence,"host_sequence")
    if len(record_sha256)!=32: raise ProtocolError("record SHA256 width")
    return _ACK.pack(_ACK_MAGIC,guest_sequence,host_sequence,record_sha256)

def unpack_ack(data:bytes):
    if len(data)!=_ACK.size: raise ProtocolError("ACK length")
    magic,g,h,d=_ACK.unpack(data)
    if magic!=_ACK_MAGIC: raise ProtocolError("ACK magic")
    return {"guest_sequence":g,"host_sequence":h,"record_sha256":d}

def recv_exact(stream, n:int)->bytes:
    out=bytearray()
    while len(out)<n:
        chunk=stream.recv(n-len(out))
        if not chunk: raise EOFError("stream closed")
        out.extend(chunk)
    return bytes(out)

def recv_guest_frame(stream)->bytes:
    head=recv_exact(stream,_HEADER.size)
    magic,version,stype,seq,mlen,rlen=_HEADER.unpack(head)
    if magic!=MAGIC or version!=VERSION: raise ProtocolError("frame identity/version mismatch")
    return head+recv_exact(stream,mlen+rlen)
