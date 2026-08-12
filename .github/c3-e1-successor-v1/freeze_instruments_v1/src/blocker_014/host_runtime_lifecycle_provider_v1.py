from __future__ import annotations
import os
from process_identity_v1 import process_identity,assert_same_process
INSTRUMENT_IDENTITY='C3_E1_SUCCESSOR_HOST_RUNTIME_LIFECYCLE_PROVIDER_V1'
class LifecycleBinding:
    def __init__(self,pid:int): self.expected=process_identity(pid); self.pidfd=os.pidfd_open(pid) if hasattr(os,'pidfd_open') else None
    def check(self): assert_same_process(self.expected,process_identity(self.expected['pid'])); return self.expected
    def close(self):
        if self.pidfd is not None: os.close(self.pidfd); self.pidfd=None
def main(): raise SystemExit('authenticated launcher pidfd/runtime binding required')
if __name__=='__main__': main()
