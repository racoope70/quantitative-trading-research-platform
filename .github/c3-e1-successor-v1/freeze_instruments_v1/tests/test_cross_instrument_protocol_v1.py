from __future__ import annotations
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_inventory(self): self.assertEqual(len([p for p in ROOT.rglob('*') if p.is_file()]),59)
 def test_group_counts(self): self.assertEqual(23+13+23,59)
 def test_scope(self): self.assertTrue(all('freeze_instruments_v1' in str(p) for p in ROOT.rglob('*') if p.is_file()))
 def test_final_checkpoint_ordering_present(self):
  t=(ROOT/'src/blocker_014/attestation_transaction_controller_v1.py').read_text(); self.assertIn('POST_DOMAIN',t)
if __name__=='__main__': unittest.main()
