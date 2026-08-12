"""Crash-aware durable evidence journal. ACK eligibility is returned only after durability."""
from __future__ import annotations
import os, struct
from pathlib import Path
from evidence_protocol_v1 import host_record_hash,host_record_preimage
class DurabilityError(RuntimeError): pass
class DurableJournal:
    def __init__(self,journal_path,head_path,canonicalizer):
        self.journal=Path(journal_path); self.head=Path(head_path); self.canonicalizer=canonicalizer
        self.journal.parent.mkdir(parents=True,exist_ok=True); self.head.parent.mkdir(parents=True,exist_ok=True)
        self.fd=os.open(self.journal,os.O_CREAT|os.O_APPEND|os.O_WRONLY,0o600)
    def close(self):
        if self.fd is not None: os.close(self.fd); self.fd=None
    def commit(self,*,origin,host_sequence,monotonic_ns,utc_ns,previous_sha256,payload,runtime_instance_uuid):
        pre=host_record_preimage(origin,host_sequence,monotonic_ns,utc_ns,previous_sha256,payload)
        digest=host_record_hash(origin=origin,host_sequence=host_sequence,monotonic_ns=monotonic_ns,utc_ns=utc_ns,previous_sha256=previous_sha256,payload=payload)
        entry=struct.pack('>Q',len(pre))+pre+digest
        try:
            view=memoryview(entry)
            while view:
                n=os.write(self.fd,view)
                if n<=0: raise OSError("short write")
                view=view[n:]
            os.fsync(self.fd); offset=os.lseek(self.fd,0,os.SEEK_END)
            head_obj={"runtime_instance_uuid":runtime_instance_uuid,"host_sequence":host_sequence,"record_sha256":digest.hex(),"journal_end_offset":offset}
            raw=self.canonicalizer(head_obj); tmp=self.head.with_name(self.head.name+'.tmp')
            tfd=os.open(tmp,os.O_CREAT|os.O_TRUNC|os.O_WRONLY,0o600)
            try: os.write(tfd,raw); os.fsync(tfd)
            finally: os.close(tfd)
            os.replace(tmp,self.head)
            dfd=os.open(self.head.parent,os.O_DIRECTORY|os.O_RDONLY)
            try: os.fsync(dfd)
            finally: os.close(dfd)
        except OSError as exc: raise DurabilityError(str(exc)) from exc
        return {"durable":True,"host_sequence":host_sequence,"record_sha256":digest.hex(),"journal_end_offset":offset}
