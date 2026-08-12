from __future__ import annotations
from pathlib import Path
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_NFTABLES_TRANSITION_MONITOR_V1'; CAP_NET_ADMIN=12
class MonitorError(RuntimeError): pass

def effective_capabilities():
    for line in Path('/proc/self/status').read_text().splitlines():
        if line.startswith('CapEff:'): return int(line.split()[1],16)
    raise MonitorError('CapEff unavailable')
def assert_receive_only():
    if effective_capabilities() & (1<<CAP_NET_ADMIN): raise MonitorError('CAP_NET_ADMIN prohibited in transition monitor')
    return True

def main():
    assert_receive_only(); raise SystemExit('transferred notification FD and frozen multiplexer config required')
if __name__=='__main__': main()
