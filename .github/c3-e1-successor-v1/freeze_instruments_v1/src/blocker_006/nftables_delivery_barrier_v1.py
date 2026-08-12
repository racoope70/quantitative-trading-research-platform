from __future__ import annotations
class StabilityError(RuntimeError): pass

def evaluate(*,snapshot_a_valid,snapshot_b_valid,snapshot_a_sha256,snapshot_b_sha256,genid_open,genid_after_b,genid_final,notification_count,barrier_healthy):
    if not snapshot_a_valid or not snapshot_b_valid: raise StabilityError('invalid snapshot')
    if snapshot_a_sha256!=snapshot_b_sha256: raise StabilityError('snapshot identity changed')
    if not (genid_open==genid_after_b==genid_final): raise StabilityError('generation changed')
    if notification_count!=0: raise StabilityError('mutation event observed')
    if not barrier_healthy: raise StabilityError('notification barrier incomplete')
    return 'PASS'
