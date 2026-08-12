from __future__ import annotations
import hashlib,os,struct
from pathlib import Path
from evidence_protocol_v1 import host_record_preimage,host_record_hash
class DurabilityError(RuntimeError):pass
class DurableJournal:
 def __init__(self,journal_path,head_path,canonicalizer):
  self.journal=Path(journal_path);self.head=Path(head_path);self.canonicalizer=canonicalizer;self.journal.parent.mkdir(parents=True,exist_ok=True);self.head.parent.mkdir(parents=True,exist_ok=True);self.fd=os.open(self.journal,os.O_CREAT|os.O_APPEND|os.O_WRONLY,0o600)
 def close(self):
  if self.fd is not None:os.close(self.fd);self.fd=None
 def _write_all(self,fd,data):
  mv=memoryview(data)
  while mv:
   n=os.write(fd,mv)
   if n<=0:raise OSError('short write')
   mv=mv[n:]
 def commit(self,*,origin,host_sequence,monotonic_ns,utc_ns,previous_sha256,payload,runtime_instance_uuid):
  pre=host_record_preimage(origin,host_sequence,monotonic_ns,utc_ns,previous_sha256,payload);digest=host_record_hash(origin=origin,host_sequence=host_sequence,monotonic_ns=monotonic_ns,utc_ns=utc_ns,previous_sha256=previous_sha256,payload=payload);entry=struct.pack('>Q',len(pre))+pre+digest
  try:
   self._write_all(self.fd,entry);os.fsync(self.fd);end=os.lseek(self.fd,0,os.SEEK_END);raw=self.canonicalizer({'runtime_instance_uuid':runtime_instance_uuid,'host_sequence':host_sequence,'record_sha256':digest.hex(),'journal_end_offset':end});tmp=self.head.with_name(self.head.name+'.tmp');tfd=os.open(tmp,os.O_CREAT|os.O_TRUNC|os.O_WRONLY,0o600)
   try:self._write_all(tfd,raw);os.fsync(tfd)
   finally:os.close(tfd)
   os.replace(tmp,self.head);dfd=os.open(self.head.parent,os.O_RDONLY|os.O_DIRECTORY)
   try:os.fsync(dfd)
   finally:os.close(dfd)
  except OSError as e:raise DurabilityError(str(e)) from e
  return {'durable':True,'host_sequence':host_sequence,'record_sha256':digest.hex(),'journal_end_offset':end}
 def fsync_and_identity(self):
  os.fsync(self.fd);h=hashlib.sha256();n=0
  with self.journal.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):n+=len(b);h.update(b)
  return {'byte_count':n,'sha256':h.hexdigest()}
