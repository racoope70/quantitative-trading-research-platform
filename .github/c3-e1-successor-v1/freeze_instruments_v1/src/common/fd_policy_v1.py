from __future__ import annotations
import fcntl,os,stat
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
def _access_mode(fd): return fcntl.fcntl(fd,fcntl.F_GETFL)&os.O_ACCMODE
def ensure_read_only(fd):
 if _access_mode(fd)!=os.O_RDONLY:raise FDPolicyError('verified block FD must be read-only')
def ensure_inheritable(fd):
 flags=fcntl.fcntl(fd,fcntl.F_GETFD)
 if flags&fcntl.FD_CLOEXEC:fcntl.fcntl(fd,fcntl.F_SETFD,flags&~fcntl.FD_CLOEXEC)
def normalize_fd(fd,target=3):
 if fd!=target:os.dup2(fd,target,inheritable=True);os.close(fd)
 ensure_inheritable(target);ensure_read_only(target);return target
def _open_devnull(flags): return os.open('/dev/null',flags|os.O_CLOEXEC)
def normalize_standard_fds():
 specs=((0,os.O_RDONLY),(1,os.O_WRONLY),(2,os.O_WRONLY))
 for target,flags in specs:
  fd=_open_devnull(flags)
  try:
   if fd!=target:os.dup2(fd,target,inheritable=True)
   else:ensure_inheritable(target)
  finally:
   if fd!=target:os.close(fd)
 return verify_devnull_standard_fds()
def verify_devnull_standard_fds():
 expected={0:os.O_RDONLY,1:os.O_WRONLY,2:os.O_WRONLY}
 for fd,mode in expected.items():
  try: target=os.readlink(f'/proc/self/fd/{fd}')
  except OSError as e: raise FDPolicyError(f'standard FD {fd} unavailable') from e
  if target!='/dev/null':raise FDPolicyError(f'FD{fd} must resolve to /dev/null, got {target}')
  if _access_mode(fd)!=mode:raise FDPolicyError(f'FD{fd} access mode mismatch')
 return True
def object_identity(fd):
 st=os.fstat(fd);return {'st_dev':st.st_dev,'st_ino':st.st_ino,'st_mode':st.st_mode,'st_rdev':st.st_rdev,'target':os.readlink(f'/proc/self/fd/{fd}')}
