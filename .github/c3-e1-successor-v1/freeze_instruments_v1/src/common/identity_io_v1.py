from __future__ import annotations
import hashlib,importlib.util,json,os,re
from pathlib import Path
class IdentityError(RuntimeError):pass
def sha256_bytes(data):return hashlib.sha256(data).hexdigest()
def file_identity(path):
 h=hashlib.sha256();n=0
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):n+=len(b);h.update(b)
 return {'byte_count':n,'sha256':h.hexdigest()}
def require_file_identity(path,expected_sha256,expected_byte_count=None):
 if not expected_sha256 or str(expected_sha256).startswith('UNRESOLVED'):raise IdentityError(f'expected file identity unresolved: {path}')
 got=file_identity(path)
 if got['sha256']!=expected_sha256 or (expected_byte_count is not None and got['byte_count']!=expected_byte_count):raise IdentityError(f'file identity mismatch: {path}')
 return got
def _canonical_module():
 p=Path(__file__).resolve().parents[3]/'canonical_json_v1.py'
 if not p.is_file():raise IdentityError(f'canonicalizer missing: {p}')
 spec=importlib.util.spec_from_file_location('c3canon',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 if getattr(mod,'CANONICALIZATION_IDENTITY',None)!='C3_E1_SUCCESSOR_CANONICAL_JSON_V1':raise IdentityError('canonicalizer identity mismatch')
 return mod
def canonical_bytes(obj):return _canonical_module().canonical_bytes(obj)
def canonical_sha256(obj):return sha256_bytes(canonical_bytes(obj))
def canonical_loads(raw):return _canonical_module().load_strict_bytes(raw if isinstance(raw,bytes) else raw.encode())
def read_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def assert_resolved(obj,label='configuration'):
 def walk(v,path):
  if isinstance(v,str) and v.startswith('UNRESOLVED'):raise IdentityError(f'{label} unresolved at {path}: {v}')
  if isinstance(v,dict):
   for k,x in v.items():walk(x,f'{path}.{k}')
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,f'{path}[{i}]')
 walk(obj,'$');return obj
def durable_write(path,data,mode=0o600):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp');fd=os.open(tmp,os.O_CREAT|os.O_TRUNC|os.O_WRONLY,mode)
 try:
  mv=memoryview(data)
  while mv:
   n=os.write(fd,mv)
   if n<=0:raise OSError('short write')
   mv=mv[n:]
  os.fsync(fd)
 finally:os.close(fd)
 os.replace(tmp,p);dfd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(dfd)
 finally:os.close(dfd)
 return file_identity(p)
_ALLOWED={'$schema','$id','$defs','$ref','oneOf','type','required','properties','additionalProperties','const','enum','pattern','minLength','minimum','maximum','items','minItems','maxItems','uniqueItems'}
def _check_schema(schema,path='$schema'):
 if not isinstance(schema,dict):raise IdentityError(f'schema object required at {path}')
 bad=set(schema)-_ALLOWED
 if bad:raise IdentityError(f'unsupported scientific-schema keyword at {path}: {sorted(bad)}')
 if schema.get('type')=='object' and schema.get('additionalProperties') is not False:raise IdentityError(f'closed object schema required at {path}')
 if 'required' in schema:
  if not isinstance(schema['required'],list) or len(schema['required'])!=len(set(schema['required'])):raise IdentityError(f'invalid required list at {path}')
  unknown=set(schema['required'])-set(schema.get('properties',{}))
  if unknown:raise IdentityError(f'required field without property at {path}: {sorted(unknown)}')
 for k,v in schema.get('$defs',{}).items():_check_schema(v,f'{path}.$defs.{k}')
 for i,v in enumerate(schema.get('oneOf',[])):_check_schema(v,f'{path}.oneOf[{i}]')
 for k,v in schema.get('properties',{}).items():_check_schema(v,f'{path}.properties.{k}')
 if isinstance(schema.get('items'),dict):_check_schema(schema['items'],f'{path}.items')
def _resolve_ref(root,ref):
 if not isinstance(ref,str) or not ref.startswith('#/$defs/') or '/' in ref[len('#/$defs/'):]:raise IdentityError(f'unsupported schema ref: {ref!r}')
 name=ref[len('#/$defs/'):]
 try:return root['$defs'][name]
 except Exception as e:raise IdentityError(f'unresolved schema ref: {ref}') from e
def _type_ok(v,t):return {'object':lambda:isinstance(v,dict),'array':lambda:isinstance(v,list),'string':lambda:isinstance(v,str),'integer':lambda:isinstance(v,int) and not isinstance(v,bool),'boolean':lambda:isinstance(v,bool),'null':lambda:v is None}[t]()
def validate_schema_instance(instance,schema,root_schema=None,path='$'):
 root=schema if root_schema is None else root_schema
 if root_schema is None:_check_schema(root)
 if '$ref' in schema:
  if set(schema)!={'$ref'}:raise IdentityError(f'$ref siblings prohibited at {path}')
  return validate_schema_instance(instance,_resolve_ref(root,schema['$ref']),root,path)
 if 'oneOf' in schema:
  matches=0
  for sub in schema['oneOf']:
   try:validate_schema_instance(instance,sub,root,path);matches+=1
   except IdentityError:pass
  if matches!=1:raise IdentityError(f'oneOf exactly-one required at {path}; matches={matches}')
  return instance
 if 'type' in schema:
  if schema['type'] not in {'object','array','string','integer','boolean','null'} or not _type_ok(instance,schema['type']):raise IdentityError(f'type mismatch at {path}')
 if 'const' in schema and instance!=schema['const']:raise IdentityError(f'const mismatch at {path}')
 if 'enum' in schema and instance not in schema['enum']:raise IdentityError(f'enum mismatch at {path}')
 if isinstance(instance,str):
  if 'minLength' in schema and len(instance)<schema['minLength']:raise IdentityError(f'minLength mismatch at {path}')
  if 'pattern' in schema and re.fullmatch(schema['pattern'],instance) is None:raise IdentityError(f'pattern mismatch at {path}')
 if isinstance(instance,int) and not isinstance(instance,bool):
  if 'minimum' in schema and instance<schema['minimum']:raise IdentityError(f'minimum at {path}')
  if 'maximum' in schema and instance>schema['maximum']:raise IdentityError(f'maximum at {path}')
 if isinstance(instance,list):
  if 'minItems' in schema and len(instance)<schema['minItems']:raise IdentityError(f'minItems at {path}')
  if 'maxItems' in schema and len(instance)>schema['maxItems']:raise IdentityError(f'maxItems at {path}')
  if schema.get('uniqueItems') and len({json.dumps(x,sort_keys=True) for x in instance})!=len(instance):raise IdentityError(f'uniqueItems at {path}')
  if 'items' in schema:
   for i,x in enumerate(instance):validate_schema_instance(x,schema['items'],root,f'{path}[{i}]')
 if isinstance(instance,dict):
  req=schema.get('required',[]);miss=set(req)-set(instance)
  if miss:raise IdentityError(f'missing required fields at {path}: {sorted(miss)}')
  props=schema.get('properties',{})
  if schema.get('additionalProperties') is False:
   extra=set(instance)-set(props)
   if extra:raise IdentityError(f'unknown scientific fields at {path}: {sorted(extra)}')
  for k,v in instance.items():
   if k in props:validate_schema_instance(v,props[k],root,f'{path}.{k}')
 return instance
def validate_schema_file(instance,schema_path):
 s=read_json(schema_path);return validate_schema_instance(instance,s,s)

def read_runtime_binding_file(path):
 obj=read_json(path);req={'runtime_instance_uuid','observation_nonce','runtime_instantiation_attestation_record_sha256'}
 if set(obj)!=req:raise IdentityError('runtime binding fields mismatch')
 from evidence_protocol_v1 import uuid_bytes,nonce_bytes
 uuid_bytes(obj['runtime_instance_uuid']);nonce_bytes(obj['observation_nonce'])
 sha=obj['runtime_instantiation_attestation_record_sha256']
 if not isinstance(sha,str) or len(sha)!=64 or sha.lower()!=sha:
  raise IdentityError('runtime record SHA256')
 try: bytes.fromhex(sha)
 except ValueError as e: raise IdentityError('runtime record SHA256') from e
 return obj
