from __future__ import annotations
from pathlib import Path
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_OBSERVATION_AUTHORITY_V1'; CAP_NET_ADMIN=12
class AuthorityError(RuntimeError): pass

def capeff():
    for line in Path('/proc/self/status').read_text().splitlines():
        if line.startswith('CapEff:'): return int(line.split()[1],16)
    raise AuthorityError('CapEff unavailable')
def verify_caps():
    eff=capeff(); expected=1<<CAP_NET_ADMIN
    if eff!=expected: raise AuthorityError(f'exact CAP_NET_ADMIN-only effective set required: {eff:#x}')
    return True

def main():
    verify_caps(); raise SystemExit('exact Stage-1 observation configuration required')
if __name__=='__main__': main()
