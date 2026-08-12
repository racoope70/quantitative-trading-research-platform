from __future__ import annotations
import hashlib,subprocess
class AKProvenanceError(RuntimeError): pass
ALG_SHA256=0x000B

def _tpmt_public(tpm2b_public):
    if len(tpm2b_public)<4: raise AKProvenanceError('TPM2B_PUBLIC truncated')
    n=int.from_bytes(tpm2b_public[:2],'big')
    if n!=len(tpm2b_public)-2: raise AKProvenanceError('TPM2B_PUBLIC size mismatch')
    return tpm2b_public[2:]
def compute_name(tpm2b_public):
    public=_tpmt_public(tpm2b_public)
    if len(public)<4: raise AKProvenanceError('TPMT_PUBLIC truncated')
    name_alg=int.from_bytes(public[2:4],'big')
    if name_alg!=ALG_SHA256: raise AKProvenanceError('AK nameAlg must be SHA256')
    return (name_alg.to_bytes(2,'big')+hashlib.sha256(public).digest()).hex()
def compute_qualified_name(parent_qn_hex,name_hex):
    try: parent=bytes.fromhex(parent_qn_hex); name=bytes.fromhex(name_hex)
    except ValueError as e: raise AKProvenanceError('QualifiedName hex') from e
    if len(name)<2 or int.from_bytes(name[:2],'big')!=ALG_SHA256: raise AKProvenanceError('AK Name algorithm')
    return (ALG_SHA256.to_bytes(2,'big')+hashlib.sha256(parent+name).digest()).hex()
def verify_credential_activation_evidence(proof):
    req={'method','credential_secret_sha256','activated_secret_sha256','result'}
    if not isinstance(proof,dict) or set(proof)!=req or proof['method']!='TPM2_ACTIVATECREDENTIAL' or proof['result']!='PASS': raise AKProvenanceError('credential activation evidence structure/result')
    for k in ('credential_secret_sha256','activated_secret_sha256'):
        v=proof[k]
        if not isinstance(v,str) or len(v)!=64 or v.lower()!=v:
            raise AKProvenanceError('credential activation digest')
        try: bytes.fromhex(v)
        except ValueError as e: raise AKProvenanceError('credential activation digest') from e
    if proof['credential_secret_sha256']!=proof['activated_secret_sha256']: raise AKProvenanceError('credential activation secret mismatch')
    return 'PASS'
def verify_ek_certificate(openssl_path,cert,ca,expected_pubkey_sha256):
    if not all(isinstance(x,str) and x.startswith('/') for x in (openssl_path,cert,ca)): raise AKProvenanceError('absolute EK trust paths required')
    v=subprocess.run([openssl_path,'verify','-CAfile',ca,cert],shell=False,capture_output=True)
    if v.returncode: raise AKProvenanceError('EK trust chain failed')
    p=subprocess.run([openssl_path,'x509','-in',cert,'-pubkey','-noout'],shell=False,capture_output=True)
    if p.returncode or hashlib.sha256(p.stdout).hexdigest()!=expected_pubkey_sha256: raise AKProvenanceError('EK public identity mismatch')
    return 'PASS'
def verify_binding(record,expected,tpmt_public_bytes=None,parent_qualified_name_hex=None):
    req={'physical_host_identity','TPM_identity','endorsement_key_public_identity','endorsement_key_trust_or_enrollment_evidence','attestation_key_public_identity','attestation_key_name_or_equivalent_TPM_object_identity','proof_that_attestation_key_is_controlled_by_the_intended_TPM','enrollment_context','applicable_PCR_policy','provenance_evidence_reference'}
    if set(record)!=req: raise AKProvenanceError('enrollment fields mismatch')
    for k,v in expected.items():
        if record.get(k)!=v: raise AKProvenanceError(f'expected provenance mismatch {k}')
    verify_credential_activation_evidence(record['proof_that_attestation_key_is_controlled_by_the_intended_TPM'])
    if tpmt_public_bytes is not None:
        if hashlib.sha256(tpmt_public_bytes).hexdigest()!=record['attestation_key_public_identity']['TPM2B_PUBLIC_sha256']: raise AKProvenanceError('AK public hash mismatch')
        name=compute_name(tpmt_public_bytes)
        if name!=record['attestation_key_name_or_equivalent_TPM_object_identity']['name_hex']: raise AKProvenanceError('AK Name mismatch')
        if parent_qualified_name_hex and compute_qualified_name(parent_qualified_name_hex,name)!=record['attestation_key_name_or_equivalent_TPM_object_identity']['qualified_name_hex']: raise AKProvenanceError('AK QualifiedName mismatch')
    return 'PASS'
