"""Content identity I/O bound to the pre-existing successor canonical JSON implementation."""
from __future__ import annotations
import hashlib, importlib.util, json
from pathlib import Path

class IdentityError(RuntimeError): pass

def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def file_identity(path):
    p=Path(path); h=hashlib.sha256(); n=0
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            n+=len(chunk); h.update(chunk)
    return {"byte_count":n,"sha256":h.hexdigest()}

def _canonical_module():
    p=Path(__file__).resolve().parents[3]/'canonical_json_v1.py'
    if not p.is_file(): raise IdentityError(f"canonicalizer missing: {p}")
    spec=importlib.util.spec_from_file_location('c3_successor_canonical_json_v1',p)
    if spec is None or spec.loader is None: raise IdentityError("cannot load canonicalizer")
    mod=importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as exc: raise IdentityError(f"canonicalizer unavailable: {exc}") from exc
    if getattr(mod,'CANONICALIZATION_IDENTITY',None)!='C3_E1_SUCCESSOR_CANONICAL_JSON_V1': raise IdentityError("canonicalizer identity mismatch")
    return mod

def canonical_bytes(obj)->bytes: return _canonical_module().canonical_bytes(obj)
def canonical_sha256(obj)->str: return sha256_bytes(canonical_bytes(obj))

def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def assert_resolved(obj,label="configuration"):
    def walk(v,path):
        if isinstance(v,str) and v.startswith("UNRESOLVED"): raise IdentityError(f"{label} unresolved at {path}: {v}")
        if isinstance(v,dict):
            for k,x in v.items(): walk(x,f"{path}.{k}")
        elif isinstance(v,list):
            for i,x in enumerate(v): walk(x,f"{path}[{i}]")
    walk(obj,"$"); return obj
