from __future__ import annotations
import os,socket,struct
from dataclasses import dataclass
from process_identity_v1 import process_identity,assert_frozen_instrument_identity
_UCRED=struct.Struct('3i');_INT=struct.Struct('i')
class PeerAuthError(RuntimeError):pass
@dataclass(frozen=True)
class KernelCred:pid:int;uid:int;gid:int
def enable_seqpacket_credentials(sock):
 sock.setsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED,1)
 if sock.getsockopt(socket.SOL_SOCKET,socket.SO_PASSCRED)!=1:raise PeerAuthError('SO_PASSCRED unavailable')
def parse_credentials(anc):
 vals=[]
 for level,typ,data in anc:
  if level==socket.SOL_SOCKET and typ==socket.SCM_CREDENTIALS:
   if len(data)<_UCRED.size:raise PeerAuthError('truncated SCM_CREDENTIALS')
   vals.append(KernelCred(*_UCRED.unpack_from(data)))
 if len(vals)!=1:raise PeerAuthError(f'exactly one SCM_CREDENTIALS required; got {len(vals)}')
 return vals[0]
def recv_authenticated(sock,max_bytes=4*1024*1024):
 data,anc,flags,address=sock.recvmsg(max_bytes,socket.CMSG_SPACE(_UCRED.size)+socket.CMSG_SPACE(_INT.size*16))
 if flags&getattr(socket,'MSG_TRUNC',0):raise PeerAuthError('truncated scientific packet')
 return data,parse_credentials(anc),anc,address
def stream_peercred(sock):return KernelCred(*_UCRED.unpack(sock.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,_UCRED.size)))
def bind_source(cred,*,expected_uid,expected_gid,expected_instrument_identity,expected_process):
 if cred.uid!=expected_uid or cred.gid!=expected_gid:raise PeerAuthError('UID/GID mismatch')
 observed=process_identity(cred.pid)
 try:assert_frozen_instrument_identity(observed,expected_process)
 except Exception as e:raise PeerAuthError(f'frozen producer identity failed: {e}') from e
 return {'instrument_identity':expected_instrument_identity,'pid':cred.pid,'uid':cred.uid,'gid':cred.gid,**{k:v for k,v in observed.items() if k!='pid'}}
def extract_fds(anc):
 out=[]
 for level,typ,data in anc:
  if level==socket.SOL_SOCKET and typ==socket.SCM_RIGHTS:
   usable=len(data)-(len(data)%_INT.size)
   if usable:out.extend(struct.unpack(f'{usable//_INT.size}i',data[:usable]))
 return out
def send_fd_with_credentials(sock,payload,fd):
 if sock.sendmsg([payload],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,_INT.pack(fd))])!=len(payload):raise PeerAuthError('short SCM_RIGHTS handoff')
def require_exact_one_fd(anc):
 fds=extract_fds(anc)
 if len(fds)!=1:
  for fd in fds:
   try:os.close(fd)
   except OSError:pass
  raise PeerAuthError(f'exactly one FD required; got {len(fds)}')
 return fds[0]
