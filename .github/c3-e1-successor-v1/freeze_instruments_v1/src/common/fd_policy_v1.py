from __future__ import annotations
import fcntl,os
from pathlib import Path
class FDPolicyError(RuntimeError):pass
def open_fds():
 out=[]
 for p in Path('/proc/self/fd').iterdir():
  if p.name.isdigit():
   try:fcntl.fcntl(int(p.name),fcntl.F_GETFD);out.append(int(p.name))
   except OSError:pass
 return sorted(out)
def verify_inherited(allowed=(0,1,2,3)):
 actual=set(open_fds());want=set(allowed);extras=sorted(actual-want);missing=sorted(want-actual)
 if extras or missing:raise FDPolicyError(f'FD allowlist mismatch extras={extras} missing={missing}')
 return True
def ensure_read_only(fd):
 if (fcntl.fcntl(fd,fcntl.F_GETFL)&os.O_ACCMODE)!=os.O_RDONLY:raise FDPolicyError('verified block FD must be read-only')
def ensure_inheritable(fd):
 flags=fcntl.fcntl(fd,fcntl.F_GETFD)
 if flags&fcntl.FD_CLOEXEC:fcntl.fcntl(fd,fcntl.F_SETFD,flags&~fcntl.FD_CLOEXEC)
def normalize_fd(fd,target=3):
 if fd!=target:os.dup2(fd,target,inheritable=True);os.close(fd)
 ensure_inheritable(target);ensure_read_only(target);return target
def object_identity(fd):
 st=os.fstat(fd);return {'st_dev':st.st_dev,'st_ino':st.st_ino,'st_mode':st.st_mode,'st_rdev':st.st_rdev,'target':os.readlink(f'/proc/self/fd/{fd}')}
