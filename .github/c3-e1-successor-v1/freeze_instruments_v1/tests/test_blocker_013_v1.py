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

import hashlib, struct
from ak_provenance_v1 import *
from measured_boot_replay_v1 import *
from ima_replay_v1 import *
from external_attestation_verifier_v1 import decode_objects,VerificationError,compare_host_tcb,canonical_result,make_post_challenge,validate_quote_pcrs
from identity_io_v1 import canonical_bytes,canonical_sha256,validate_schema_instance,read_json,IdentityError

def tpm2b_public():
    # TPMT_PUBLIC: type ECC (0x23), nameAlg SHA256 (0x0b), synthetic remainder
    body=b'\x00\x23\x00\x0b'+b'X'*20
    return len(body).to_bytes(2,'big')+body

def specid_event2():
    sig=b'Spec ID Event03'+b'\0'; sig=sig.ljust(16,b'\0'); data=sig+struct.pack('<I4B',0,0,2,0,2)+struct.pack('<I',1)+struct.pack('<HH',0x000B,32)+b'\0'
    legacy=struct.pack('<II',0,EV_NO_ACTION)+b'\0'*20+struct.pack('<I',len(data))+data
    d=b'\x11'*32; ev=struct.pack('<IIIH',0,1,1,0x000B)+d+struct.pack('<I',1)+b'X'
    return legacy+ev,d
class Blocker013Tests(unittest.TestCase):
    def setUp(self): _install_canonical_fixture(self)
    def test_001_ak_name_uses_tpmt_public(self):
        p=tpm2b_public(); self.assertTrue(compute_name(p).startswith('000b'))
    def test_002_ak_qualified_name(self):
        n=compute_name(tpm2b_public()); self.assertEqual(len(compute_qualified_name('000b'+'00'*32,n)),68)
    def test_003_activation_pass(self): self.assertEqual(verify_credential_activation_evidence({'method':'TPM2_ACTIVATECREDENTIAL','credential_secret_sha256':'11'*32,'activated_secret_sha256':'11'*32,'result':'PASS'}),'PASS')
    def test_004_activation_mismatch_fails(self):
        with self.assertRaises(AKProvenanceError): verify_credential_activation_evidence({'method':'TPM2_ACTIVATECREDENTIAL','credential_secret_sha256':'11'*32,'activated_secret_sha256':'22'*32,'result':'PASS'})
    def test_005_event2_direct_parse(self):
        d=b'\x22'*32; raw=struct.pack('<IIIH',1,2,1,0x000B)+d+struct.pack('<I',0); e=parse_event_log(raw,'TCG_PCR_EVENT2_LE_V1'); self.assertEqual(e[0]['digests'][0x000B],d)
    def test_006_specid_plus_event2_parse(self):
        raw,d=specid_event2(); e=parse_event_log(raw); self.assertEqual(e[-1]['digests'][0x000B],d)
    def test_007_measured_boot_replay(self):
        raw,d=specid_event2(); e=parse_event_log(raw); self.assertEqual(replay(e,[0])[0],extend(b'\0'*32,d,'sha256'))
    def test_008_measured_boot_truncation_fails(self):
        with self.assertRaises(ReplayError): parse_event_log(b'abc')
    def test_009_ima_parse_and_replay(self):
        data=b'abc'; th=hashlib.sha256(data).digest(); name=b'ima-ng\0'; raw=(10).to_bytes(4,'little')+th+len(name).to_bytes(4,'little')+name+len(data).to_bytes(4,'little')+data; desc={'format_identity':'IMA_NATIVE_BINARY_CANONICAL_V1','byteorder':'little','template_hash_algorithm':'sha256','template_hash_size':32,'allowed_templates':['ima-ng','ima-buf']}; rs=parse_native_binary_measurements(raw,desc); self.assertEqual(replay_records(rs).hex(),hashlib.sha256(b'\0'*32+th).hexdigest())
    def test_010_ima_unknown_template_fails(self):
        data=b'a'; th=hashlib.sha256(data).digest(); name=b'bad\0'; raw=(10).to_bytes(4,'little')+th+len(name).to_bytes(4,'little')+name+len(data).to_bytes(4,'little')+data; desc={'format_identity':'IMA_NATIVE_BINARY_CANONICAL_V1','byteorder':'little','template_hash_algorithm':'sha256','template_hash_size':32,'allowed_templates':['ima-ng']}
        with self.assertRaises(IMAReplayError): parse_native_binary_measurements(raw,desc)
    def test_011_decode_objects_requires_exact_hash(self):
        good={'role':'x','byte_count':1,'sha256':hashlib.sha256(b'a').hexdigest(),'data_hex':'61'}; self.assertEqual(decode_objects({'objects':{'x':good}})['x'],b'a')
        bad={**good,'sha256':'00'*32}
        with self.assertRaises(VerificationError): decode_objects({'objects':{'x':bad}})
    def test_012_host_tcb_exact_member_set(self):
        self.assertEqual(compare_host_tcb({'q':'11'*32},{'q':'11'*32}),'PASS')
        with self.assertRaises(VerificationError): compare_host_tcb({'q':'11'*32,'x':'22'*32},{'q':'11'*32})
    def test_013_canonical_result_binds_bundle(self):
        b={'runtime_instance_uuid':'12345678-1234-1234-1234-123456789abc','observation_nonce':'11'*32,'verifier_manifest_sha256':'22'*32,'runtime_instantiation_attestation_record_sha256':'33'*32}; o,h=canonical_result('PRE_E1_RESULT',b,'PASS',{'ak_provenance':'PASS'}); self.assertEqual(o['attestation_bundle_sha256'],canonical_sha256(b)); self.assertEqual(len(h),64)
    def test_014_post_challenge_is_fresh_shape(self):
        c,_=make_post_challenge('12345678-1234-1234-1234-123456789abc','11'*32,'22'*32,'33'*32); self.assertEqual(len(c['fresh_challenge']),64); self.assertEqual(c['transaction_type'],'POST_OBSERVATION_CHALLENGE')
