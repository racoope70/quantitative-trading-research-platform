"""Linux process identity helpers used to defeat PID-reuse/self-assertion ambiguity."""
from __future__ import annotations
import hashlib, os
from pathlib import Path
class ProcessIdentityError(RuntimeError): pass

def proc_starttime(pid:int)->int:
    text=Path(f"/proc/{pid}/stat").read_text(); r=text.rfind(')')
    if r<0: raise ProcessIdentityError("malformed /proc stat")
    fields=text[r+2:].split(); return int(fields[19])
def executable_path(pid:int)->str: return os.readlink(f"/proc/{pid}/exe")
def _file_bytes(path): return Path(path).read_bytes()
def process_identity(pid:int)->dict:
    cmd=_file_bytes(f'/proc/{pid}/cmdline'); cg=_file_bytes(f'/proc/{pid}/cgroup')
    return {"pid":pid,"starttime":proc_starttime(pid),"executable":executable_path(pid),"cmdline_sha256":hashlib.sha256(cmd).hexdigest(),"cgroup_sha256":hashlib.sha256(cg).hexdigest()}
def assert_same_process(expected:dict,observed:dict):
    for k in ('pid','starttime','executable','cmdline_sha256','cgroup_sha256'):
        if k in expected and expected.get(k)!=observed.get(k): raise ProcessIdentityError(f"process identity mismatch: {k}")
