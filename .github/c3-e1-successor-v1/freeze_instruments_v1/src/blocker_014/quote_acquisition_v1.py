from __future__ import annotations
import subprocess
class QuoteError(RuntimeError): pass

def acquire_quote(tool:str,args:list[str]):
    if not tool.startswith('/'): raise QuoteError('absolute tpm2_quote path required')
    cp=subprocess.run([tool,*args],shell=False,capture_output=True)
    if cp.returncode!=0: raise QuoteError(f'tpm2_quote failed: {cp.returncode}')
    return {'stdout':cp.stdout,'stderr':cp.stderr}
