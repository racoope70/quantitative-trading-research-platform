"""Fixed-purpose B53 contract; actual protected entrypoint remains disabled.

Root-only publication/claim primitives are prospective, not deployed services.
Synthetic storage exercises cannot establish Owner/executor OS separation.
No existing REAL schema, journal, checkpoint or scientific rule is reused.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from datetime import datetime, timezone
import owner_publication as publication

TASK = 'BATCH0004_C06_B53_READ_ONLY_OWNER_AUTHORITY_CONTRACT_NP_V1'
ENGINEERING_ROOT = Path('/private/tmp/QTRP_BATCH0004_C06_B53_OS_SEPARATION_HANDOFF_NP_V1')
OS_FIXTURE = Path('/private/tmp/QTRP_B53_OWNER_EXECUTOR_OS_FIXTURE_NP_V1')
OS_RUNTIME = OS_FIXTURE / 'runtime'
ROOT = Path(__file__).absolute().parent.parent
if ROOT not in (ENGINEERING_ROOT, OS_RUNTIME):
    raise RuntimeError('B53_FIXED_NONPRODUCTION_SOURCE_LOCATION_REQUIRED')
PROTECTED_ROOT = '/Users/richardcooper/Downloads/batch0004_REAL_S05_BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F_PRIMARY_checkpoint'
KEY = 'PRIMARY/checkpoints/checkpoint_000053.json'
HISTORICAL_SHA = 'd3183e29c012380ed9b4b17039a8cab4e568acc2f33ee5c03bd5f7bc4bc5c05a'
SYNTHETIC_SHA = '7eef2c798ae1eeb7226f3870e1eac287c38a0d1699c82d5dd399285a55e5f64d'
KEYSET_SHA = '9d301e623659cbccc101ac2e7c03756019f698d11d115742e7b8d9823c691c96'
SCHEMA = 'QTRP_OWNER_B53_READ_ONLY_V1'
SCOPE = 'BATCH0004_CLASS_B53_HISTORICAL_HASH_COMPARISON_ONLY'
NP_SCHEMA = 'QTRP_B53_SYNTHETIC_STORAGE_EXERCISE_V1'
NP_SCOPE = 'NONPROTECTED_SYNTHETIC_ONLY__NO_OWNER_AUTHORITY'
# Proposed distinct root-controlled locations. Importing never accesses them.
PUBLICATION_ROOT = Path('/private/var/db/qtrp-owner-b53-read-only-v1/publications')
CLAIM_ROOT = Path('/private/var/db/qtrp-owner-b53-read-only-v1/claims')
SYNTHETIC_AREA = ROOT / 'fixtures/b53_authority'
PYTHON = '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12'
PYTHON_SHA = 'd4f152f2a753c94e0e7935c8ebbe6b2609979e1df7898422b577d0076383d08b'
MAX_AGE_SECONDS = 300
ACTUAL_PROTECTED_ACCESS_ENABLED = False
METADATA_OPERATIONS = [
    'ROOT_AND_ANCESTORS_NOFOLLOW_DIRECTORY_DESCRIPTORS',
    'INITIAL_CLOSED_NAMESPACE_ENUMERATION_STAT_FSTAT_INCLUDING_UNSELECTED_B_C',
    'SELECTED_BODY_EXACT_LENGTH_HASH_ONLY',
    'FINAL_ANCESTOR_AND_FULL_CLOSED_NAMESPACE_STABILITY',
    'REJECT_UNKNOWN_ENTRY_BEFORE_STAT_OPEN_DESCENT',
]
# Literal accepted NONPROTECTED namespace expectations are inserted below.
EXPECTED_FILES = ('PRIMARY/checkpoint_head.json', 'PRIMARY/checkpoints/checkpoint_000001.json', 'PRIMARY/checkpoints/checkpoint_000002.json', 'PRIMARY/checkpoints/checkpoint_000003.json', 'PRIMARY/checkpoints/checkpoint_000004.json', 'PRIMARY/checkpoints/checkpoint_000005.json', 'PRIMARY/checkpoints/checkpoint_000006.json', 'PRIMARY/checkpoints/checkpoint_000007.json', 'PRIMARY/checkpoints/checkpoint_000008.json', 'PRIMARY/checkpoints/checkpoint_000009.json', 'PRIMARY/checkpoints/checkpoint_000010.json', 'PRIMARY/checkpoints/checkpoint_000011.json', 'PRIMARY/checkpoints/checkpoint_000012.json', 'PRIMARY/checkpoints/checkpoint_000013.json', 'PRIMARY/checkpoints/checkpoint_000014.json', 'PRIMARY/checkpoints/checkpoint_000015.json', 'PRIMARY/checkpoints/checkpoint_000016.json', 'PRIMARY/checkpoints/checkpoint_000017.json', 'PRIMARY/checkpoints/checkpoint_000018.json', 'PRIMARY/checkpoints/checkpoint_000019.json', 'PRIMARY/checkpoints/checkpoint_000020.json', 'PRIMARY/checkpoints/checkpoint_000021.json', 'PRIMARY/checkpoints/checkpoint_000022.json', 'PRIMARY/checkpoints/checkpoint_000023.json', 'PRIMARY/checkpoints/checkpoint_000024.json', 'PRIMARY/checkpoints/checkpoint_000025.json', 'PRIMARY/checkpoints/checkpoint_000026.json', 'PRIMARY/checkpoints/checkpoint_000027.json', 'PRIMARY/checkpoints/checkpoint_000028.json', 'PRIMARY/checkpoints/checkpoint_000029.json', 'PRIMARY/checkpoints/checkpoint_000030.json', 'PRIMARY/checkpoints/checkpoint_000031.json', 'PRIMARY/checkpoints/checkpoint_000032.json', 'PRIMARY/checkpoints/checkpoint_000033.json', 'PRIMARY/checkpoints/checkpoint_000034.json', 'PRIMARY/checkpoints/checkpoint_000035.json', 'PRIMARY/checkpoints/checkpoint_000036.json', 'PRIMARY/checkpoints/checkpoint_000037.json', 'PRIMARY/checkpoints/checkpoint_000038.json', 'PRIMARY/checkpoints/checkpoint_000039.json', 'PRIMARY/checkpoints/checkpoint_000040.json', 'PRIMARY/checkpoints/checkpoint_000041.json', 'PRIMARY/checkpoints/checkpoint_000042.json', 'PRIMARY/checkpoints/checkpoint_000043.json', 'PRIMARY/checkpoints/checkpoint_000044.json', 'PRIMARY/checkpoints/checkpoint_000045.json', 'PRIMARY/checkpoints/checkpoint_000046.json', 'PRIMARY/checkpoints/checkpoint_000047.json', 'PRIMARY/checkpoints/checkpoint_000048.json', 'PRIMARY/checkpoints/checkpoint_000049.json', 'PRIMARY/checkpoints/checkpoint_000050.json', 'PRIMARY/checkpoints/checkpoint_000051.json', 'PRIMARY/checkpoints/checkpoint_000052.json', 'PRIMARY/checkpoints/checkpoint_000053.json', 'PRIMARY/checkpoints/checkpoint_000054.json', 'PRIMARY/clean_inputs/neutral_semantic_evidence.jsonl', 'PRIMARY/clean_inputs/partition_manifest.json', 'PRIMARY/clean_inputs/reason_precedence_v2.json', 'PRIMARY/clean_inputs/semantic_rule_v2.json', 'PRIMARY/executor_attempts/U0001/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0001/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0001/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0001/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0002/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0002/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0002/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0002/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0003/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0003/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0003/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0003/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0004/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0004/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0004/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0004/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0005/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0005/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0005/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0005/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0006/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0006/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0006/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0006/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0007/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0007/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0007/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0007/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0008/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0008/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0008/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0008/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0009/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0009/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0009/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0009/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0010/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0010/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0010/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0010/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0011/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0011/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0011/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0011/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0001/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0001/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0001/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0001/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0002/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0002/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0002/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0002/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0003/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0003/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0003/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0003/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0004/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0004/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0004/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0004/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0005/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0005/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0005/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0005/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0006/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0006/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0006/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0006/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0007/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0007/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0007/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0007/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0008/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0008/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0008/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0008/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0009/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0009/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0009/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0009/raw_stdout.jsonl', 'PRIMARY/executor_attempts/U0012/A0010/attempt_final_message.txt', 'PRIMARY/executor_attempts/U0012/A0010/executor_attempt_manifest.json', 'PRIMARY/executor_attempts/U0012/A0010/raw_stderr.txt', 'PRIMARY/executor_attempts/U0012/A0010/raw_stdout.jsonl', 'PRIMARY/frozen_units/U0001/unit_result.json', 'PRIMARY/frozen_units/U0002/unit_result.json', 'PRIMARY/frozen_units/U0003/unit_result.json', 'PRIMARY/frozen_units/U0004/unit_result.json', 'PRIMARY/frozen_units/U0005/unit_result.json', 'PRIMARY/frozen_units/U0006/unit_result.json', 'PRIMARY/frozen_units/U0007/unit_result.json', 'PRIMARY/frozen_units/U0008/unit_result.json', 'PRIMARY/frozen_units/U0009/unit_result.json', 'PRIMARY/frozen_units/U0010/unit_result.json', 'PRIMARY/frozen_units/U0011/unit_result.json', 'PRIMARY/recovery_transactions/261237324857876022fa46fe4907013280c38ca7a0907e60132ae96229dd1a3d/event_000001_authorized.json', 'PRIMARY/recovery_transactions/261237324857876022fa46fe4907013280c38ca7a0907e60132ae96229dd1a3d/event_000002_outcome.json', 'PRIMARY/recovery_transactions/261237324857876022fa46fe4907013280c38ca7a0907e60132ae96229dd1a3d/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/31dadce00f4c432e294ba21f51cebbf2b88c23c7c7ce001bef63836323f724d2/event_000001_authorized.json', 'PRIMARY/recovery_transactions/31dadce00f4c432e294ba21f51cebbf2b88c23c7c7ce001bef63836323f724d2/event_000002_outcome.json', 'PRIMARY/recovery_transactions/488ff4fe209468bad7b02521bc196b72fa9ab84a5137468fea18812ff4acddb9/event_000001_authorized.json', 'PRIMARY/recovery_transactions/488ff4fe209468bad7b02521bc196b72fa9ab84a5137468fea18812ff4acddb9/event_000002_outcome.json', 'PRIMARY/recovery_transactions/488ff4fe209468bad7b02521bc196b72fa9ab84a5137468fea18812ff4acddb9/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/4e10bf4da877dc4437f47e84afb4f94af525cf99b0d56a7442bda82c31d3e833/event_000001_authorized.json', 'PRIMARY/recovery_transactions/4e10bf4da877dc4437f47e84afb4f94af525cf99b0d56a7442bda82c31d3e833/event_000002_outcome.json', 'PRIMARY/recovery_transactions/4e10bf4da877dc4437f47e84afb4f94af525cf99b0d56a7442bda82c31d3e833/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/5819846a2784be1626911ed2fca40f8367b5bef14103dd705abd5b23379bde52/event_000001_authorized.json', 'PRIMARY/recovery_transactions/5819846a2784be1626911ed2fca40f8367b5bef14103dd705abd5b23379bde52/event_000002_outcome.json', 'PRIMARY/recovery_transactions/5819846a2784be1626911ed2fca40f8367b5bef14103dd705abd5b23379bde52/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/6140057b18ae3855612d4bd7df770f90f0a8ed68e68db9af53a7b97be5670456/event_000001_authorized.json', 'PRIMARY/recovery_transactions/6140057b18ae3855612d4bd7df770f90f0a8ed68e68db9af53a7b97be5670456/event_000002_outcome.json', 'PRIMARY/recovery_transactions/6140057b18ae3855612d4bd7df770f90f0a8ed68e68db9af53a7b97be5670456/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/9e31bdaf3a3ffc31a758e40f108ada8dd6a2c9c606be6340ecef0315cc8da58e/event_000001_authorized.json', 'PRIMARY/recovery_transactions/9e31bdaf3a3ffc31a758e40f108ada8dd6a2c9c606be6340ecef0315cc8da58e/event_000002_outcome.json', 'PRIMARY/recovery_transactions/9e31bdaf3a3ffc31a758e40f108ada8dd6a2c9c606be6340ecef0315cc8da58e/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/cffd8e148998a98e7f62b53572735941e43405bd37ef257f8799ddae70955b8f/event_000001_authorized.json', 'PRIMARY/recovery_transactions/cffd8e148998a98e7f62b53572735941e43405bd37ef257f8799ddae70955b8f/event_000002_outcome.json', 'PRIMARY/recovery_transactions/cffd8e148998a98e7f62b53572735941e43405bd37ef257f8799ddae70955b8f/owner_authorization_consumed.json', 'PRIMARY/recovery_transactions/ee110c8f05288285134bfec046acc381be3ff32327736dd4b60e57b7b77b44db/event_000001_authorized.json', 'PRIMARY/recovery_transactions/ee110c8f05288285134bfec046acc381be3ff32327736dd4b60e57b7b77b44db/event_000002_outcome.json', 'PRIMARY/recovery_transactions/ee110c8f05288285134bfec046acc381be3ff32327736dd4b60e57b7b77b44db/owner_authorization_consumed.json')
EXPECTED_DIRECTORIES = ('PRIMARY', 'PRIMARY/checkpoints', 'PRIMARY/clean_inputs', 'PRIMARY/executor_attempts', 'PRIMARY/executor_attempts/U0001', 'PRIMARY/executor_attempts/U0001/A0001', 'PRIMARY/executor_attempts/U0002', 'PRIMARY/executor_attempts/U0002/A0001', 'PRIMARY/executor_attempts/U0003', 'PRIMARY/executor_attempts/U0003/A0001', 'PRIMARY/executor_attempts/U0004', 'PRIMARY/executor_attempts/U0004/A0001', 'PRIMARY/executor_attempts/U0005', 'PRIMARY/executor_attempts/U0005/A0001', 'PRIMARY/executor_attempts/U0006', 'PRIMARY/executor_attempts/U0006/A0001', 'PRIMARY/executor_attempts/U0007', 'PRIMARY/executor_attempts/U0007/A0001', 'PRIMARY/executor_attempts/U0008', 'PRIMARY/executor_attempts/U0008/A0001', 'PRIMARY/executor_attempts/U0009', 'PRIMARY/executor_attempts/U0009/A0001', 'PRIMARY/executor_attempts/U0010', 'PRIMARY/executor_attempts/U0010/A0001', 'PRIMARY/executor_attempts/U0011', 'PRIMARY/executor_attempts/U0011/A0001', 'PRIMARY/executor_attempts/U0012', 'PRIMARY/executor_attempts/U0012/A0001', 'PRIMARY/executor_attempts/U0012/A0002', 'PRIMARY/executor_attempts/U0012/A0003', 'PRIMARY/executor_attempts/U0012/A0004', 'PRIMARY/executor_attempts/U0012/A0005', 'PRIMARY/executor_attempts/U0012/A0006', 'PRIMARY/executor_attempts/U0012/A0007', 'PRIMARY/executor_attempts/U0012/A0008', 'PRIMARY/executor_attempts/U0012/A0009', 'PRIMARY/executor_attempts/U0012/A0010', 'PRIMARY/frozen_units', 'PRIMARY/frozen_units/U0001', 'PRIMARY/frozen_units/U0002', 'PRIMARY/frozen_units/U0003', 'PRIMARY/frozen_units/U0004', 'PRIMARY/frozen_units/U0005', 'PRIMARY/frozen_units/U0006', 'PRIMARY/frozen_units/U0007', 'PRIMARY/frozen_units/U0008', 'PRIMARY/frozen_units/U0009', 'PRIMARY/frozen_units/U0010', 'PRIMARY/frozen_units/U0011', 'PRIMARY/recovery_transactions', 'PRIMARY/recovery_transactions/261237324857876022fa46fe4907013280c38ca7a0907e60132ae96229dd1a3d', 'PRIMARY/recovery_transactions/31dadce00f4c432e294ba21f51cebbf2b88c23c7c7ce001bef63836323f724d2', 'PRIMARY/recovery_transactions/488ff4fe209468bad7b02521bc196b72fa9ab84a5137468fea18812ff4acddb9', 'PRIMARY/recovery_transactions/4e10bf4da877dc4437f47e84afb4f94af525cf99b0d56a7442bda82c31d3e833', 'PRIMARY/recovery_transactions/5819846a2784be1626911ed2fca40f8367b5bef14103dd705abd5b23379bde52', 'PRIMARY/recovery_transactions/6140057b18ae3855612d4bd7df770f90f0a8ed68e68db9af53a7b97be5670456', 'PRIMARY/recovery_transactions/9e31bdaf3a3ffc31a758e40f108ada8dd6a2c9c606be6340ecef0315cc8da58e', 'PRIMARY/recovery_transactions/cffd8e148998a98e7f62b53572735941e43405bd37ef257f8799ddae70955b8f', 'PRIMARY/recovery_transactions/ee110c8f05288285134bfec046acc381be3ff32327736dd4b60e57b7b77b44db')

class B53Stop(RuntimeError):
    pass

def need(value, code):
    if not value:
        raise B53Stop(code)

canonical = publication.canonical
digest = publication.digest

def _utc():
    return datetime.now(timezone.utc)

def _same(a, b):
    # Canonical equality preserves bool/int distinctions throughout nested data.
    return canonical(a) == canonical(b)

def _parse(raw):
    need(type(raw) is bytes and 0 < len(raw) <= 65536, 'B53_DOCUMENT_SIZE_OR_TYPE')
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'B53_DUPLICATE_FIELD')
            out[key] = value
        return out
    try:
        doc = json.loads(raw, object_pairs_hook=pairs)
        need(type(doc) is dict and raw == canonical(doc), 'B53_NONCANONICAL_DOCUMENT')
        return doc
    except (ValueError, TypeError, UnicodeError):
        raise B53Stop('B53_MALFORMED_DOCUMENT') from None

def source_binding(context):
    """Derive current nonprotected identities; never trust submitted hashes."""
    need(getattr(context, '__file__', None) == str(ROOT / 'composition.py'), 'B53_SOURCE_ORIGIN')
    verifier = getattr(context, '_verify_nonproduction_sources', None)
    need(callable(verifier) and verifier.__globals__ is vars(context)
         and verifier.__code__.co_filename == str(ROOT / 'composition.py'), 'B53_SOURCE_CONTEXT')
    verifier()
    need(context.verify_release(ROOT) == context.RELEASE_SHA, 'B53_RELEASE_IDENTITY')
    comp = digest((ROOT / 'composition.py').read_bytes())
    need(comp == context._LOADED_COMPOSITION_SOURCE_SHA256, 'B53_COMPOSITION_IDENTITY')
    closure = context._NONPRODUCTION_SOURCE_CLOSURE
    relative = 'candidate/b53_owner_readonly_v1.py'
    need(Path(__file__) == ROOT / relative and relative in closure
         and digest(Path(__file__).read_bytes()) == closure[relative], 'B53_AUTHORITY_SOURCE_IDENTITY')
    need(sys.version_info[:2] == (3, 12) and sys.executable == PYTHON
         and digest(Path(PYTHON).read_bytes()) == PYTHON_SHA, 'B53_INTERPRETER_IDENTITY')
    return {'source_closure': dict(closure), 'composition_sha256': comp,
            'release_sha256': context.RELEASE_SHA, 'verifier': 'recovery_bounded_v4.verify_selective_content',
            'authority_module_sha256': closure[relative], 'python': PYTHON,
            'python_sha256': PYTHON_SHA, 'python_version': list(sys.version_info[:3]),
            'platform': sys.platform}

def _scope(root, *, synthetic):
    need(type(root) is str, 'B53_ROOT_TYPE')
    if synthetic:
        p = Path(root)
        area = ROOT / 'fixtures/class_b53'
        need(p.is_absolute() and '..' not in p.parts and p != area
             and p.is_relative_to(area), 'B53_SYNTHETIC_ROOT_REQUIRED')
    else:
        need(root == PROTECTED_ROOT, 'B53_EXACT_PROTECTED_ROOT_REQUIRED')
    return {'root': root, 'key': KEY, 'class': 'B',
            'expected_sha256': SYNTHETIC_SHA if synthetic else HISTORICAL_SHA,
            'length': 13118, 'selected_count': 1, 'max_body_bytes': 13118,
            'max_aggregate_body_bytes': 13118, 'other_body_reads': 0,
            'expected_regular_files': list(EXPECTED_FILES),
            'expected_descendant_directories': list(EXPECTED_DIRECTORIES),
            'namespace_keyset_sha256': KEYSET_SHA,
            'metadata_operations': list(METADATA_OPERATIONS)}

def document(context, *, root, synthetic, issued_utc, expires_utc):
    """Build a proposal/storage exercise. This is never approval by itself."""
    need(type(synthetic) is bool, 'B53_MODE_TYPE')
    return {'schema': NP_SCHEMA if synthetic else SCHEMA,
            'scope': NP_SCOPE if synthetic else SCOPE, 'task_id': TASK,
            'purpose': 'ONE_B53_OPAQUE_HISTORICAL_HASH_COMPARISON',
            'mode': 'SYNTHETIC_NONPRODUCTION' if synthetic else 'PROTECTED_READ_ONLY',
            'consumer_uid': 501, 'binding': _scope(root, synthetic=synthetic),
            'implementation': source_binding(context),
            'issued_utc': issued_utc, 'expires_utc': expires_utc,
            'max_age_seconds': MAX_AGE_SECONDS, 'max_invocations': 1, 'automatic_retry': False,
            'output_contract': 'FIXED12_B53_MATCH_MISMATCH_REJECT__NO_PAYLOAD',
            'checkpoint_mutation': False, 'recovery_mutation': False,
            'scientific_mutation': False, 'REAL_execution': False,
            'publication_root': str(OS_FIXTURE/'publications') if synthetic and ROOT==OS_RUNTIME else str(PUBLICATION_ROOT),
            'claim_root': str(OS_FIXTURE/'claims') if synthetic and ROOT==OS_RUNTIME else str(CLAIM_ROOT)}

def validate(raw, context, *, synthetic, root, now=None):
    """Pure envelope/source checks do not confer protected-read authority."""
    doc = _parse(raw)
    try:
        expected = document(context, root=root, synthetic=synthetic,
                            issued_utc=doc['issued_utc'], expires_utc=doc['expires_utc'])
        need(_same(doc, expected), 'B53_EXACT_BINDING_REQUIRED')
        need(type(doc['issued_utc']) is str and type(doc['expires_utc']) is str, 'B53_FRESHNESS_TYPE')
        issued = datetime.fromisoformat(doc['issued_utc'])
        expires = datetime.fromisoformat(doc['expires_utc'])
        now = _utc() if now is None else now
        need(issued.tzinfo is not None and expires.tzinfo is not None and now.tzinfo is not None,
             'B53_FRESHNESS_TIMEZONE')
        need(0 < (expires-issued).total_seconds() <= MAX_AGE_SECONDS
             and issued <= now <= expires and (now-issued).total_seconds() <= MAX_AGE_SECONDS,
             'B53_STALE_EXPIRED_OR_FUTURE')
    except (KeyError, TypeError, ValueError, OverflowError):
        raise B53Stop('B53_REQUIRED_FIELD_OR_FRESHNESS_INVALID') from None
    return doc

def _check_directory(fd, uid):
    st = os.fstat(fd)
    need(stat.S_ISDIR(st.st_mode) and st.st_uid == uid
         and (uid != 0 or st.st_gid == 0)
         and stat.S_IMODE(st.st_mode) == 0o755, 'B53_DIRECTORY_OWNER_OR_MODE')

def _read_file(fd, name, expected, uid):
    handle = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
    try:
        value = publication.read_snapshot(handle, len(expected), uid, 0o444)
        need(value == expected, 'B53_FILE_READBACK_MISMATCH')
        return value
    finally:
        os.close(handle)

def _write_file(fd, name, raw, uid):
    handle = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400, dir_fd=fd)
    try:
        # Default restrictive umask cannot relax these final permissions.
        publication.write_all(handle, raw)
        os.fchmod(handle, 0o444)
        os.fsync(handle)
    finally:
        os.close(handle)
    os.fsync(fd)
    _read_file(fd, name, raw, uid)

def _completion(raw):
    return canonical({'schema': 'QTRP_B53_PUBLICATION_COMPLETE_V1',
                      'authorization_sha256': digest(raw), 'length': len(raw),
                      'scope': _parse(raw)['scope'], 'REAL_execution': False})

def _store_publication(parent_fd, raw, uid):
    """Descriptor primitive, not an authority API. Retains partial slots forever."""
    _check_directory(parent_fd, uid)
    name = digest(raw)
    os.mkdir(name, 0o755, dir_fd=parent_fd)  # EEXIST is a permanent stop, never repair.
    os.fsync(parent_fd)
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
    try:
        os.fchmod(fd, 0o755)
        _check_directory(fd, uid)
        _write_file(fd, 'authorization.json', raw, uid)
        _write_file(fd, 'complete.json', _completion(raw), uid)
        os.fsync(fd)
        return digest(_read_file(fd, 'authorization.json', raw, uid))
    finally:
        os.close(fd)

def _publication_readback(parent_fd, raw, uid):
    _check_directory(parent_fd, uid)
    fd = os.open(digest(raw), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
    try:
        _check_directory(fd, uid)
        _read_file(fd, 'complete.json', _completion(raw), uid)
        _read_file(fd, 'authorization.json', raw, uid)
    finally:
        os.close(fd)

def _claim_bytes(raw):
    return canonical({'schema': 'QTRP_B53_PERMANENT_CLAIM_V1',
                      'authorization_sha256': digest(raw),
                      'implementation_sha256': digest(canonical(_parse(raw)['implementation'])),
                      'consumer_uid': 501, 'max_invocations': 1,
                      'state': 'CONSUMED_BEFORE_COMPARISON__NO_RETRY'})

def _claim(parent_fd, raw, uid):
    """Permanent exclusive reservation BEFORE writing; no cleanup/reset API.

    fsync of the parent makes even a crash before claim completion consume the
    slot. Incomplete/ambiguous slots reject all subsequent claim attempts.
    Genuine irreversibility additionally requires uid0-controlled ancestors.
    """
    _check_directory(parent_fd, uid)
    name = digest(raw)
    os.mkdir(name, 0o755, dir_fd=parent_fd)
    os.fsync(parent_fd)
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
    try:
        os.fchmod(fd, 0o755)
        _check_directory(fd, uid)
        claim = _claim_bytes(raw)
        _write_file(fd, 'claimed.json', claim, uid)
        os.fsync(fd)
        os.fsync(parent_fd)
        _read_file(fd, 'claimed.json', claim, uid)
        return {'schema': 'B53_CLAIM_STORAGE_READBACK_V1', 'authorization_sha256': name,
                'claim_sha256': digest(claim), 'storage_owner_uid': uid,
                'Owner_OS_separation_qualified': False, 'protected_read_permitted': False}
    finally:
        os.close(fd)

def _owner_identity():
    need(os.getuid() == os.geteuid() == 0 and os.environ.get('SUDO_UID') == '501'
         and sys.stdin.isatty(), 'B53_INDEPENDENT_OWNER_TERMINAL_REQUIRED')

def publish_owner(raw, context):
    """Prospective independently authenticated Owner operation; never called here."""
    _owner_identity()  # BEFORE any authority/protected namespace access.
    validate(raw, context, synthetic=False, root=PROTECTED_ROOT)
    fd = publication.open_root_chain(PUBLICATION_ROOT)
    try:
        return _store_publication(fd, raw, 0)
    finally:
        os.close(fd)

def claim_owner(raw, context):
    """Prospective Owner-only one-way storage, not an executor privilege bridge."""
    _owner_identity()
    validate(raw, context, synthetic=False, root=PROTECTED_ROOT)
    fd = publication.open_root_chain(PUBLICATION_ROOT)
    try:
        _publication_readback(fd, raw, 0)
    finally:
        os.close(fd)
    fd = publication.open_root_chain(CLAIM_ROOT)
    try:
        return _claim(fd, raw, 0)
    finally:
        os.close(fd)

def verify_protected(*args, **kwargs):
    """No approved atomic claim-to-executor handoff exists in this candidate.

    A readable completed claim could be replayed; it is not a read permit.
    Never open/stat/resolve the protected root, even with caller 'approval'.
    """
    raise B53Stop('B53_PROTECTED_DISABLED__OS_CLAIM_HANDOFF_UNQUALIFIED')

def _synthetic_slot(slot):
    p = Path(slot)
    need(p.is_absolute() and '..' not in p.parts and p.parent == SYNTHETIC_AREA,
         'B53_SYNTHETIC_AUTHORITY_PATH_REQUIRED')
    # Walk existing task-local components without symlink traversal.
    fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for name in ('fixtures', 'b53_authority', p.name):
            next_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        _check_directory(fd, 501)
        return fd
    except BaseException:
        os.close(fd)
        raise

def publish_synthetic(raw, context, *, slot, root):
    """Storage-model exercise by SAME uid501; explicitly NOT Owner authority."""
    need(os.getuid() == os.geteuid() == 501, 'B53_SYNTHETIC_PRINCIPAL')
    validate(raw, context, synthetic=True, root=root)
    fd = _synthetic_slot(slot)
    try:
        return _store_publication(fd, raw, 501)
    finally:
        os.close(fd)

def compare_synthetic(raw, context, *, publication_slot, claim_slot, root, expectation):
    """New contract storage chain feeds the unchanged SYNTHETIC comparator.

    No caller token can promote this separate fixture interface to protected use.
    """
    need(os.getuid() == os.geteuid() == 501, 'B53_SYNTHETIC_PRINCIPAL')
    validate(raw, context, synthetic=True, root=root)
    fd = _synthetic_slot(publication_slot)
    try:
        _publication_readback(fd, raw, 501)
    finally:
        os.close(fd)
    fd = _synthetic_slot(claim_slot)
    try:
        claim = _claim(fd, raw, 501)
    finally:
        os.close(fd)
    # Refresh source/freshness AFTER durable storage, before comparator I/O.
    validate(raw, context, synthetic=True, root=root)
    result = _compare_fixed_synthetic(context, root, expectation)
    return {'qualification': 'SYNTHETIC_STORAGE_MODEL__NOT_OWNER_OS_AUTHORITY',
            'claim': claim, 'comparison': result}

def _compare_fixed_synthetic(context, root, expectation):
    """Unchanged comparator, with two fixed NONPRODUCTION instability cases.

    The two exact fixture names deliberately mutate only their new opaque
    UID501-owned selected test body AFTER reading and BEFORE the original final
    stability check. This supplies deterministic OS-test coverage without
    changing the comparator or accepting caller-injected code. Ordinary cases
    never install the test hook. Protected entrypoints remain disabled.
    """
    import membership_readonly
    original = membership_readonly.Membership.finish
    unstable = Path(root) in {ROOT/'fixtures/class_b53'/name for name in
                             ('unstable_match', 'unstable_mismatch')}
    def final_test_mutation(scope):
        need(scope.root == Path(root), 'B53_NP_INSTABILITY_SCOPE')
        parent, leaf, before = scope.files[KEY]
        fd = os.open(leaf, os.O_WRONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            s = os.fstat(fd)
            need(membership_readonly.signature(s) == before and stat.S_ISREG(s.st_mode)
                 and s.st_nlink == 1 and s.st_uid == 501 and s.st_size == 13118,
                 'B53_NP_INSTABILITY_OBJECT')
            view = memoryview(b'Z'*13118)
            while view:
                n = os.write(fd, view)
                need(n > 0, 'B53_NP_INSTABILITY_WRITE')
                view = view[n:]
            os.fsync(fd)
        finally:
            os.close(fd)
        return original(scope)
    if unstable:
        membership_readonly.Membership.finish = final_test_mutation
    try:
        return context.recovery.verify_selective_content(
            root=root, expectation=expectation, expectation_sha256=digest(expectation),
            authority={'task_id': context.recovery._CLASS_B53_TASK,
                       'scope': 'SOURCE_BOUND_CLASS_B53_SYNTHETIC_FIXTURES_ONLY',
                       'expectation_sha256': digest(expectation)},
            mode='SYNTHETIC_NONPRODUCTION', source_context=context,
            contract='CLASS_B53_HASH_ONLY_NONPRODUCTION')
    finally:
        if unstable:
            membership_readonly.Membership.finish = original

def _verify_child_credentials():
    # POSIX permits getgroups() to include the effective primary group. Admit
    # only the fixed primary20; privileged/admin supplementary groups reject.
    groups = os.getgroups()
    need(os.getuid() == os.geteuid() == 501 and os.getgid() == os.getegid() == 20
         and type(groups) is list and all(type(g) is int and g == 20 for g in groups),
         'B53_CHILD_PRIVILEGE_DROP_FAILED')

def _open_os_fixture(relative):
    """Fixed disposable fixture only; never relax the production root helper.

    /private/tmp is a root-owned sticky shared parent. Its single fixed child
    must be root-owned and nonwritable by the executor. All later components
    are root-controlled, descriptor-relative and nofollow. Actual OS behavior
    requires the separately approved distinct-principal qualification.
    """
    need(relative in ('', 'publications', 'claims', 'runtime'), 'B53_OS_FIXED_PATH')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open('/', flags)
    try:
        _check_directory(fd, 0)
        for name in ('private', 'tmp', OS_FIXTURE.name):
            child = os.open(name, flags, dir_fd=fd)
            os.close(fd)
            fd = child
            s = os.fstat(fd)
            need(stat.S_ISDIR(s.st_mode) and s.st_uid == s.st_gid == 0 and
                 stat.S_IMODE(s.st_mode) == (0o1777 if name == 'tmp' else 0o755),
                 'B53_OS_FIXTURE_CHAIN')
        if relative:
            child = os.open(relative, flags, dir_fd=fd)
            os.close(fd)
            fd = child
            _check_directory(fd, 0)
        return fd
    except BaseException:
        os.close(fd)
        raise

def _owner_np_snapshot(context):
    """Owner installation must authenticate bytes BEFORE executing this code.

    These runtime checks defend the frozen installation after that external
    approval. Running executor-writable engineering bytes as root is forbidden.
    No installer, privilege acquisition or installation fallback is provided.
    """
    _owner_identity()  # first gate, before any OS fixture or source access
    need(ROOT == OS_RUNTIME and os.isatty(1) and os.isatty(2),
         'B53_OWNER_INSTALLED_TERMINAL_ONLY')
    fd = _open_os_fixture('runtime')
    os.close(fd)
    binding = source_binding(context)
    relatives = [*binding['source_closure'], 'composition.py',
                 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json',
                 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256',
                 'evidence/B53_SYNTHETIC_EXPECTATION_SPECIFICATION.json']
    # Check every source/control ancestor and file, not only the final inode.
    for relative in relatives:
        fd = _open_os_fixture('runtime')
        try:
            parts = Path(relative).parts
            for name in parts[:-1]:
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
                _check_directory(fd, 0)
            handle = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            try:
                s = os.fstat(handle)
                need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and
                     s.st_uid == s.st_gid == 0 and stat.S_IMODE(s.st_mode) == 0o444,
                     'B53_OWNER_SOURCE_NOT_IMMUTABLE')
            finally:
                os.close(handle)
        finally:
            os.close(fd)
    return binding

def _os_request(raw, context, case_name):
    _owner_np_snapshot(context)
    need(type(case_name) is str and case_name in ('match', 'mismatch', 'unstable_match', 'unstable_mismatch'),
         'B53_OS_FIXED_CASE')
    root = str(ROOT / 'fixtures/class_b53' / case_name)
    validate(raw, context, synthetic=True, root=root)
    spec = _parse((ROOT / 'evidence/B53_SYNTHETIC_EXPECTATION_SPECIFICATION.json').read_bytes())
    expectation = canonical(spec['declaration'])
    need(digest(expectation) == context.recovery._CLASS_B53_EXPECTATION_PIN,
         'B53_OS_EXPECTATION_IDENTITY')
    return root, expectation

def publish_owner_np(raw, context, *, case_name):
    """Fixed disposable Owner publication. Does not publish protected authority."""
    _os_request(raw, context, case_name)
    fd = _open_os_fixture('publications')
    try:
        return _store_publication(fd, raw, 0)
    finally:
        os.close(fd)

def _fork_fixed_synthetic(context, root, expectation):
    """One fork after reservation; fixed credential drop; no retry or token.

    There is no caller-supplied executable, argv, UID, environment, callback or
    launch command. Root never runs the comparator. Child output is closed
    nonpayload JSON on the independent Owner terminal. Parent never re-launches
    after a fork/wait failure, interrupted process or ambiguous child status.
    """
    pid = os.fork()
    if pid == 0:
        try:
            import resource
            limit = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
            need(type(limit) is int and 3 <= limit <= 65536, 'B53_CHILD_DESCRIPTOR_LIMIT')
            os.close(0)
            os.closerange(3, limit)  # no inherited writable authority descriptors
            os.setgroups([])
            os.setgid(20)
            os.setuid(501)
            _verify_child_credentials()
            try:
                os.setuid(0)
            except PermissionError:
                pass
            else:
                os._exit(126)
            result = _compare_fixed_synthetic(context, root, expectation)
            output = canonical({'principal': {'uid': os.getuid(), 'euid': os.geteuid(),
                                              'gid': os.getgid(), 'egid': os.getegid()},
                                'comparison': result, 'protected_read_permitted': False})
            need(len(output) <= 4096, 'B53_CHILD_OUTPUT_BOUND')
            view = memoryview(output)
            while view:
                n = os.write(1, view)
                need(n > 0, 'B53_CHILD_OUTPUT_FAILED')
                view = view[n:]
            os._exit(0 if result['result'] in ('MATCH', 'MISMATCH') else 2)
        except BaseException:
            os.write(2, b'B53_SYNTHETIC_CHILD_REJECT\n')
            os._exit(125)
    # A failed wait leaves the permanent claim intact; never retry the launch.
    _, status = os.waitpid(pid, 0)
    return {'child_pid': pid, 'wait_status': status, 'launch_attempts': 1,
            'protected_read_permitted': False, 'automatic_retry': False}

def compare_owner_np_once(raw, context, *, case_name):
    """One authorization -> at most one fixed unprivileged comparator child.

    Reserve BEFORE fork. No receipt is accepted as a handoff credential and no
    incomplete slot is repaired. Crash durability beyond observed fsync/OS
    tests remains unresolved; no mathematical power-loss guarantee is claimed.
    """
    root, expectation = _os_request(raw, context, case_name)
    fd = _open_os_fixture('publications')
    try:
        _publication_readback(fd, raw, 0)
    finally:
        os.close(fd)
    fd = _open_os_fixture('claims')
    try:
        _claim(fd, raw, 0)
    finally:
        os.close(fd)
    # Validation failure after consumption is terminal too; no cleanup path.
    _os_request(raw, context, case_name)
    return _fork_fixed_synthetic(context, root, expectation)
