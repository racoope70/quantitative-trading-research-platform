from __future__ import annotations
import subprocess
from measured_boot_replay_v1 import replay_sha256_events
from ima_replay_v1 import replay_template_digests
from ak_provenance_v1 import verify_binding
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_EXTERNAL_ATTESTATION_VERIFIER_V1'
class VerificationError(RuntimeError): pass

def run_checkquote(tool,args):
    if not tool.startswith('/'): raise VerificationError('absolute checkquote path required')
    cp=subprocess.run([tool,*args],shell=False,capture_output=True)
    if cp.returncode!=0: raise VerificationError(f'tpm2_checkquote failed: {cp.returncode}')
    return {'stdout':cp.stdout,'stderr':cp.stderr}
def bind_fields(bundle,expected):
    for k,v in expected.items():
        if bundle.get(k)!=v: raise VerificationError(f'bundle binding mismatch: {k}')
    return True
def classify(results):
    vals=list(results.values())
    if any(v=='FAIL' for v in vals): return 'FAIL'
    if all(v=='PASS' for v in vals): return 'PASS'
    return 'INCONCLUSIVE'
def main(): raise SystemExit('external verifier exact dependencies/trust material unresolved before Stage-1 freeze')
if __name__=='__main__': main()
