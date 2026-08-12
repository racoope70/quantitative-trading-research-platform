from __future__ import annotations
import hashlib, os
from pathlib import Path
class ProcessIdentityError(RuntimeError): pass

def proc_starttime(pid):
    t=Path(f'/proc/{pid}/stat').read_text(); r=t.rfind(')'); f=t[r+2:].split()
    if r<0 or len(f)<=19: raise ProcessIdentityError('malformed proc stat')
    return int(f[19])
def executable_path(pid): return os.readlink(f'/proc/{pid}/exe')
def _hash_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def process_identity(pid):
    exe=executable_path(pid); cmd=Path(f'/proc/{pid}/cmdline').read_bytes(); cg=Path(f'/proc/{pid}/cgroup').read_bytes()
    return {'pid':pid,'starttime':proc_starttime(pid),'executable':exe,'executable_sha256':_hash_file(exe),'cmdline_sha256':hashlib.sha256(cmd).hexdigest(),'cgroup_sha256':hashlib.sha256(cg).hexdigest()}
def assert_same_process(expected,observed):
    for k in ('pid','starttime','executable','executable_sha256','cmdline_sha256','cgroup_sha256'):
        if k in expected and expected[k]!=observed.get(k): raise ProcessIdentityError(f'process identity mismatch: {k}')
    return observed
def assert_frozen_instrument_identity(observed,expected):
    for k in ('executable_sha256','cmdline_sha256','cgroup_sha256','instrument_source_path','instrument_source_sha256'):
        v=expected.get(k)
        if not v or str(v).startswith('UNRESOLVED'): raise ProcessIdentityError(f'frozen expected identity unavailable: {k}')
    if observed.get('executable_sha256')!=expected['executable_sha256']: raise ProcessIdentityError('frozen process identity mismatch: executable_sha256')
    if observed.get('cmdline_sha256')!=expected['cmdline_sha256']: raise ProcessIdentityError('frozen process identity mismatch: cmdline_sha256')
    if observed.get('cgroup_sha256')!=expected['cgroup_sha256']: raise ProcessIdentityError('frozen process identity mismatch: cgroup_sha256')
    if expected.get('executable') and not str(expected['executable']).startswith('UNRESOLVED') and observed.get('executable')!=expected['executable']: raise ProcessIdentityError('executable path mismatch')
    src=Path(expected['instrument_source_path'])
    if not src.is_file() or _hash_file(src)!=expected['instrument_source_sha256']: raise ProcessIdentityError('frozen instrument source identity mismatch')
    return observed
def scientific_process_instance(instrument_identity,pid=None):
    i=process_identity(os.getpid() if pid is None else pid)
    return f"{instrument_identity}:{i['pid']}:{i['starttime']}:{i['executable_sha256']}:{i['cmdline_sha256']}:{i['cgroup_sha256']}"
