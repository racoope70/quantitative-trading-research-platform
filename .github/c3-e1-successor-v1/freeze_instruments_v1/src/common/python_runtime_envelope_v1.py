"""Fail-closed checks for the admitted isolated CPython scientific runtime."""
from __future__ import annotations
import os, sys
from pathlib import Path

class RuntimeEnvelopeError(RuntimeError): pass

def find_reachable_pyc(roots):
    bad=[]
    for root in map(Path,roots):
        rr=root.resolve(strict=True)
        for cache in rr.rglob('__pycache__'): bad.append(str(cache.resolve(strict=True)))
        for p in rr.rglob('*.pyc'):
            rp=p.resolve(strict=True)
            try: rp.relative_to(rr)
            except ValueError: raise RuntimeEnvelopeError(f"pyc escapes admitted root: {p}")
            bad.append(str(rp))
    return sorted(bad)

def verify_sys_path(expected):
    actual=[str(Path(x).resolve()) for x in sys.path if x]; exp=[str(Path(x).resolve()) for x in expected]
    if actual!=exp: raise RuntimeEnvelopeError(f"sys.path mismatch: {actual!r} != {exp!r}")

def verify_runtime(expected_sys_path=None,import_roots=None,require_flags=True):
    if require_flags:
        for k,v in {'isolated':1,'dont_write_bytecode':1,'no_site':1,'ignore_environment':1}.items():
            if getattr(sys.flags,k,None)!=v: raise RuntimeEnvelopeError(f"sys.flags.{k} mismatch")
    for key in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','PYTHONUSERBASE','PYTHONPYCACHEPREFIX'):
        if os.environ.get(key): raise RuntimeEnvelopeError(f"prohibited Python environment variable: {key}")
    if expected_sys_path is not None: verify_sys_path(expected_sys_path)
    if import_roots:
        bad=find_reachable_pyc(import_roots)
        if bad: raise RuntimeEnvelopeError(f"reachable pyc prohibited: {bad[0]}")
    return True
