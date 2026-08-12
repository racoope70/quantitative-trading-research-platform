from __future__ import annotations
import hashlib
class IMAReplayError(RuntimeError): pass

def extend_sha256(pcr:bytes,template_digest:bytes)->bytes:
    if len(pcr)!=32 or len(template_digest)!=32: raise IMAReplayError('SHA256 inputs required')
    return hashlib.sha256(pcr+template_digest).digest()
def replay_template_digests(digests,initial=b'\0'*32):
    p=initial
    for d in digests: p=extend_sha256(p,d)
    return p
def parse_native_binary_measurements(raw:bytes,format_identity:str):
    if format_identity!='IMA_NATIVE_BINARY_CANONICAL_V1': raise IMAReplayError('exact native binary format not frozen')
    raise IMAReplayError('selected-kernel native IMA parser requires Stage-1 kernel-format binding')
