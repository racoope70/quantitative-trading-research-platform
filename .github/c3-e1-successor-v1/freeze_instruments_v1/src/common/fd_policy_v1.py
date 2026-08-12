"""Inherited file-descriptor allowlist validation for QEMU exec."""
from __future__ import annotations
import fcntl, os
from pathlib import Path
class FDPolicyError(RuntimeError): pass

def open_fds(): return sorted(int(p.name) for p in Path('/proc/self/fd').iterdir() if p.name.isdigit())
def verify_inherited(allowed=(0,1,2,3)):
    actual=set(open_fds()); allowed=set(allowed); extras=[]
    for fd in actual-allowed:
        try: fcntl.fcntl(fd,fcntl.F_GETFD); extras.append(fd)
        except OSError: pass
    if extras: raise FDPolicyError(f"unexpected open descriptors: {extras}")
    missing=[fd for fd in allowed if fd not in actual]
    if missing: raise FDPolicyError(f"missing admitted descriptors: {missing}")
def fd_target(fd:int)->str: return os.readlink(f'/proc/self/fd/{fd}')
def ensure_inheritable(fd:int):
    flags=fcntl.fcntl(fd,fcntl.F_GETFD)
    if flags & fcntl.FD_CLOEXEC: fcntl.fcntl(fd,fcntl.F_SETFD,flags & ~fcntl.FD_CLOEXEC)
