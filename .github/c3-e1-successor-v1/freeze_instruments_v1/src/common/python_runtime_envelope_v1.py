from __future__ import annotations
import hashlib, os, sys
from pathlib import Path
class RuntimeEnvelopeError(RuntimeError): pass

def _file_sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def find_reachable_pyc(roots):
    out=[]
    for root in roots:
        p=Path(root).resolve()
        if not p.exists(): raise RuntimeEnvelopeError(f'import root missing: {p}')
        for x in p.rglob('*'):
            if x.is_symlink():
                r=x.resolve(strict=True)
                if p not in r.parents and r!=p: raise RuntimeEnvelopeError(f'import symlink escapes root: {x}')
            if x.is_file() and x.suffix=='.pyc': out.append(str(x))
    return sorted(out)
def verify_manifest_files(entries,label):
    if not isinstance(entries,list): raise RuntimeEnvelopeError(f'{label} manifest not frozen')
    for e in entries:
        if set(e)!={'path','byte_count','sha256'}: raise RuntimeEnvelopeError(f'{label} entry fields')
        p=Path(e['path'])
        if not p.is_file(): raise RuntimeEnvelopeError(f'{label} file missing: {p}')
        if p.stat().st_size!=e['byte_count'] or _file_sha(p)!=e['sha256']: raise RuntimeEnvelopeError(f'{label} identity mismatch: {p}')
    return True
def verify_runtime(*,expected_sys_path,import_roots,require_flags=True,manifest=None):
    if require_flags:
        f=sys.flags; checks={'isolated':f.isolated,'dont_write_bytecode':f.dont_write_bytecode,'no_site':f.no_site,'ignore_environment':f.ignore_environment,'utf8_mode':f.utf8_mode}; bad=[k for k,v in checks.items() if v!=1]
        if bad: raise RuntimeEnvelopeError(f'CPython isolation flags missing: {bad}')
    if list(sys.path)!=list(expected_sys_path): raise RuntimeEnvelopeError('sys.path drift')
    if [k for k in os.environ if k.startswith('PYTHON')]: raise RuntimeEnvelopeError('PYTHON environment influence present')
    pyc=find_reachable_pyc(import_roots)
    if pyc: raise RuntimeEnvelopeError(f'pyc inputs prohibited: {pyc[:3]}')
    if manifest is not None:
        if manifest.get('pyc_policy')!='PYC_PROHIBITED_AND_VERIFIED_ABSENT': raise RuntimeEnvelopeError('pyc policy drift')
        verify_manifest_files(manifest.get('project_python_files'),'project Python')
        verify_manifest_files(manifest.get('stdlib_files'),'stdlib')
        verify_manifest_files(manifest.get('extension_modules'),'extension module')
    return True
