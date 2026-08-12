from __future__ import annotations
import subprocess,tempfile
from pathlib import Path
class QuoteError(RuntimeError): pass

def acquire_quote(tool,args_template,qualification_hex):
    if not isinstance(tool,str) or not tool.startswith('/'): raise QuoteError('absolute tpm2_quote path required')
    if not isinstance(qualification_hex,str) or len(qualification_hex)!=64: raise QuoteError('32-byte quote qualification required')
    with tempfile.TemporaryDirectory() as td:
        paths={'message':str(Path(td)/'quote.msg'),'signature':str(Path(td)/'quote.sig'),'pcr':str(Path(td)/'quote.pcr'),'qualification':qualification_hex}
        args=[]
        for item in args_template:
            if not isinstance(item,str): raise QuoteError('quote argument must be string')
            try: args.append(item.format(**paths))
            except KeyError as e: raise QuoteError(f'unknown quote placeholder: {e}') from e
        cp=subprocess.run([tool,*args],shell=False,capture_output=True)
        if cp.returncode: raise QuoteError(f'tpm2_quote failed {cp.returncode}')
        out={}
        for role,key in [('quote_message','message'),('quote_signature','signature'),('quoted_pcr_bytes','pcr')]:
            p=Path(paths[key])
            if not p.is_file() or p.stat().st_size==0: raise QuoteError(f'tpm2_quote output missing: {role}')
            out[role]=p.read_bytes()
        out['stdout']=cp.stdout; out['stderr']=cp.stderr; out['exit_code']=cp.returncode
        return out
