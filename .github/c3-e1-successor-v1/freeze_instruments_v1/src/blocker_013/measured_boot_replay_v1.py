from __future__ import annotations
import hashlib
class ReplayError(RuntimeError): pass

def extend_sha256(pcr:bytes,digest:bytes)->bytes:
    if len(pcr)!=32 or len(digest)!=32: raise ReplayError('SHA256 PCR/digest must be 32 bytes')
    return hashlib.sha256(pcr+digest).digest()
def replay_sha256_events(digests,initial=b'\0'*32):
    p=initial
    for d in digests: p=extend_sha256(p,d)
    return p
def parse_event_log(raw:bytes): raise ReplayError('exact selected-host event-log structure not frozen')
