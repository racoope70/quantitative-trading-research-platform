from __future__ import annotations
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src/blocker_007'))
from observation_authority_v1 import CAP_NET_ADMIN
class T(unittest.TestCase):
 def test_only_cap_bit(self): self.assertEqual(1<<CAP_NET_ADMIN,0x1000)
 def test_config_no_shell(self):
  c=json.loads((ROOT/'config/blocker_007/blocker_007_config_v1.json').read_text()); self.assertFalse(c['interactive_shell']); self.assertEqual(c['capabilities'],['CAP_NET_ADMIN']); self.assertTrue(c['monitor_process_independent'])
if __name__=='__main__': unittest.main()
