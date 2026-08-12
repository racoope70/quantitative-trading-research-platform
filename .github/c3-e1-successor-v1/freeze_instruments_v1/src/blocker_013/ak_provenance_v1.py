from __future__ import annotations
class AKProvenanceError(RuntimeError): pass

def verify_binding(record,expected):
    required=('attestation_key_public_identity','endorsement_key_public_identity','physical_host_identity')
    for k in required:
        if k not in record: raise AKProvenanceError(f'missing {k}')
        if k in expected and record[k]!=expected[k]: raise AKProvenanceError(f'{k} mismatch')
    return 'PASS'
