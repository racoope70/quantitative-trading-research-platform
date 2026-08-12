"""Linux kernel-bound local IPC credentials for scientific evidence sources."""
from __future__ import annotations
import os, socket, struct
from dataclasses import dataclass
from process_identity_v1 import process_identity

_UCRED=struct.Struct('3i')
class PeerAuthError(RuntimeError): pass

@dataclass(frozen=True)
class KernelCred:
    pid:int; uid:int; gid:int

def enable_seqpacket_credentials(sock:socket.socket): sock.setsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED,1)
def parse_credentials(ancdata):
    found=[]
    for level,typ,data in ancdata:
        if level==socket.SOL_SOCKET and typ==socket.SCM_CREDENTIALS:
            if len(data)<_UCRED.size: raise PeerAuthError("truncated SCM_CREDENTIALS")
            found.append(KernelCred(*_UCRED.unpack_from(data)))
    if len(found)!=1: raise PeerAuthError(f"exactly one SCM_CREDENTIALS required; got {len(found)}")
    return found[0]

def recv_authenticated(sock:socket.socket,max_bytes:int=1024*1024):
    data,anc,flags,addr=sock.recvmsg(max_bytes,socket.CMSG_SPACE(_UCRED.size)+socket.CMSG_SPACE(struct.calcsize('i')*8))
    if flags & getattr(socket,'MSG_TRUNC',0): raise PeerAuthError("truncated packet")
    return data,parse_credentials(anc),anc

def stream_peercred(sock:socket.socket)->KernelCred:
    raw=sock.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,_UCRED.size)
    return KernelCred(*_UCRED.unpack(raw))

def bind_source(cred:KernelCred,expected_uid:int,expected_gid:int,expected_pid:int|None=None,expected_process:dict|None=None):
    if cred.uid!=expected_uid or cred.gid!=expected_gid: raise PeerAuthError("UID/GID mismatch")
    if expected_pid is not None and cred.pid!=expected_pid: raise PeerAuthError("PID mismatch")
    pi=process_identity(cred.pid)
    if expected_process:
        for k,v in expected_process.items():
            if v is not None and v != "UNRESOLVED_GOVERNED_BUILD" and pi.get(k)!=v: raise PeerAuthError(f"process identity mismatch: {k}")
    return {"pid":cred.pid,"uid":cred.uid,"gid":cred.gid,**{k:v for k,v in pi.items() if k!='pid'}}

def extract_fds(ancdata):
    out=[]; item=struct.calcsize('i')
    for level,typ,data in ancdata:
        if level==socket.SOL_SOCKET and typ==socket.SCM_RIGHTS:
            usable=len(data)-(len(data)%item); out.extend(struct.unpack(f'{usable//item}i',data[:usable]))
    return out
