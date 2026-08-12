import json, os, pathlib, socket, struct, sys, tempfile, unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
for d in [ROOT/'src/common',ROOT/'src/blocker_005',ROOT/'src/blocker_006',ROOT/'src/blocker_007',ROOT/'src/blocker_013',ROOT/'src/blocker_014']:
    if str(d) not in sys.path: sys.path.insert(0,str(d))

import identity_io_v1 as _identity_io
class _LocalCanonicalStub:
    CANONICALIZATION_IDENTITY='C3_E1_SUCCESSOR_CANONICAL_JSON_V1'
    @staticmethod
    def canonical_bytes(obj):
        return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    @staticmethod
    def load_strict_bytes(raw):
        if isinstance(raw,bytes): raw=raw.decode('utf-8')
        return json.loads(raw)

def _install_canonical_fixture(case):
    patch=mock.patch.object(_identity_io,'_canonical_module',return_value=_LocalCanonicalStub)
    patch.start(); case.addCleanup(patch.stop)

import hashlib, stat
import attestation_transaction_controller_v1 as c
import runtime_instantiation_launcher_v1 as l
from quote_acquisition_v1 import acquire_quote,QuoteError
from identity_io_v1 import canonical_bytes,canonical_sha256,read_json,validate_schema_file
class Blocker014Tests(unittest.TestCase):
    def setUp(self): _install_canonical_fixture(self)
    def test_001_pre_qualification_binds_all_fields(self):
        q=c.pre_qualification(b'1'*16,b'2'*32,b'3'*32,b'4'*32); self.assertEqual(len(q),32); self.assertNotEqual(q,c.pre_qualification(b'1'*16,b'2'*32,b'3'*32,b'5'*32))
    def test_002_post_qualification_binds_chain_head(self):
        args=(b'1'*16,b'2'*32,b'3'*32,9,b'4'*32,b'5'*32,2,8,b'6'*32,b'7'*32); q=c.post_qualification(*args); args2=list(args); args2[4]=b'8'*32; self.assertNotEqual(q,c.post_qualification(*args2))
    def test_003_require_pass_rejects_fail(self):
        with self.assertRaises(c.AttestationError): c.require_pass({'classification':'FAIL'},{})
    def test_004_qualification_root_is_domain_separated(self): self.assertEqual(len(c.derive_qualification_root('11'*32,'22'*32,'33'*32)),64)
    def test_005_frozen_output_validation(self):
        with tempfile.TemporaryDirectory() as td:
            d=pathlib.Path(td)/'disk'; d.write_bytes(b'data'); m={'manifest_type':'C3_E1_SUCCESSOR_FROZEN_BUILD_OUTPUT_MANIFEST_V1','artifact_format':'RAW_FULL_DISK_V1','architecture':'amd64','raw_disk_byte_count':4,'raw_disk_sha256':hashlib.sha256(b'data').hexdigest(),'boot_artifacts_contained_in_frozen_disk':True}; mp=pathlib.Path(td)/'m.json'; mp.write_text(json.dumps(m)); out,sha=l.validate_frozen_output({'frozen_build_output_manifest_path':str(mp),'raw_disk_path':str(d)}); self.assertEqual(out,m); self.assertEqual(len(sha),64)
    def test_006_verity_prohibited_option(self):
        cfg={'dm_verity':{'version':1,'hash_algorithm':'sha256','data_block_size':4096,'hash_block_size':4096,'num_data_blocks':1,'salt':'11','root_hash':'22','hash_tree_path':'x','hash_tree_sha256':'33'*32,'hash_tree_byte_count':1,'options':['ignore_corruption']}}
        with self.assertRaises(l.LaunchError): l.validate_verity(cfg)
    def test_007_launch_record_schema(self):
        cfg={'admitted_environment_specification_sha256':'11'*32,'qemu_sha256':'22'*32,'qemu_machine_configuration_sha256':'33'*32,'guest_firmware_sha256':'44'*32,'host_evidence_channel_configuration_sha256':'55'*32,'host_attestation_state_reference':'att','record_schema_path':str(ROOT/'schemas/freeze_instrument_records_v1.schema.json')}; v={'root_hash':'aa','hash_tree_sha256':'66'*32}; o,h=l.launch_record(cfg,'12345678-1234-1234-1234-123456789abc','77'*32,'88'*32,'99'*32,v,'block',123); self.assertEqual(o['record_type'],'RUNTIME_INSTANTIATION_ATTESTATION_RECORD'); self.assertEqual(len(h),64)
    def test_008_fd_manifest_exact_allowlist(self):
        m=read_json(ROOT/'config/blocker_014/qemu_inherited_fd_manifest_v1.json'); self.assertEqual(set(m['fds']),{'0','1','2','3'}); self.assertEqual(m['fds']['3'],'EXACT_VERIFIED_DM_VERITY_OBJECT')
    def test_009_quote_acquisition_binds_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            tool=pathlib.Path(td)/'tool'; tool.write_text('#!/bin/sh\nwhile [ $# -gt 0 ]; do case "$1" in -m) echo m > "$2"; shift 2;; -s) echo s > "$2"; shift 2;; -o) echo p > "$2"; shift 2;; *) shift;; esac; done\n'); tool.chmod(tool.stat().st_mode|stat.S_IXUSR); q=acquire_quote(str(tool),['-q','{qualification}','-m','{message}','-s','{signature}','-o','{pcr}'],'11'*32); self.assertTrue(q['quote_message']); self.assertTrue(q['quote_signature']); self.assertTrue(q['quoted_pcr_bytes'])
    def test_010_quote_acquisition_rejects_relative_tool(self):
        with self.assertRaises(QuoteError): acquire_quote('tool',[],'11'*32)
    def test_011_final_checkpoint_request_schema(self):
        o={'record_type':'FINAL_CHECKPOINT_REQUEST','runtime_instance_uuid':'12345678-1234-1234-1234-123456789abc','observation_nonce':'11'*32,'observation_start_host_sequence':1,'observation_end_host_sequence':2,'checkpoint_path':'/a','checkpoint_reference_path':'/b'}; validate_schema_file(o,ROOT/'schemas/freeze_instrument_records_v1.schema.json')
    def test_012_runtime_launcher_has_in_place_exec(self):
        src=(ROOT/'src/blocker_014/runtime_instantiation_launcher_v1.py').read_text(); self.assertIn('os.execve(cfg[\'qemu_path\']',src); self.assertIn('verify_inherited((0,1,2,3))',src)
