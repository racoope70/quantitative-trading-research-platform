from __future__ import annotations
import os
from fd_policy_v1 import ensure_inheritable
from identity_io_v1 import file_identity
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_RUNTIME_INSTANTIATION_LAUNCHER_V1'
class LaunchError(RuntimeError): pass

def verify_identity(path,expected_sha256):
    got=file_identity(path)['sha256']
    if got!=expected_sha256: raise LaunchError(f'identity mismatch: {path}')
def normalize_disk_fd(fd:int,target=3):
    if fd!=target: os.dup2(fd,target,inheritable=True); os.close(fd)
    ensure_inheritable(target); return target
def exec_qemu(qemu_path,argv,env=None): os.execve(qemu_path,[qemu_path,*argv],{} if env is None else env)
def main(): raise SystemExit('governed build output/dm-verity/QEMU identities required before launch')
if __name__=='__main__': main()
