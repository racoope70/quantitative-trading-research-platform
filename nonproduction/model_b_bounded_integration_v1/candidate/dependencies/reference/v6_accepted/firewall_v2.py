"""Batch 0004 S07/S08 standalone fail-closed firewall component.

NOT an integrated orchestrator. Caller MUST supply hash-pinned, out-of-band
S04 source identities. Do not derive trusted hashes from package contents.
Production activation requires independent review of original v1 sources.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat
import unicodedata

PROHIBITED = frozenset({
    'primary_body_disposition', 'primary_disposition', 'primary_reason_code',
    'primary_rationale', 'primary_aggregate_counts',
    'primary_mismatch_expectation', 'final_reconciliation', 'primary_ledger',
})
EVIDENCE_KEYS = frozenset({
    'schema_version', 'batch_id', 'canonical_source_identity',
    'authorized_population_position', 'record_ordinal',
    'metadata_ledger_position', 'notice_class', 'accepted_record',
    'canonical_locator', 'retrieval_status', 'body_available', 'body_sha256',
    'extracted_body_sha256', 'extracted_header_sha256',
    'identity_reconciliation_status', 'valid_extraction',
    'body_evidence_member', 'header_evidence_member', 's03_validation',
})
CONSTRUCTION_KEYS = frozenset({
    'artifact_id', 'source_s04_manifest_sha256', 'primary_ledger_included',
    'primary_semantic_fields_included', 'primary_aggregate_counts_included',
    'mismatch_expectations_included', 'final_reconciliation_included',
    'allowed_sources',
})
FREEZE_KEYS = frozenset({
    'artifact_id', 'file_allowlist', 'file_hashes', 'contamination_check',
    'source_lineage', 'primary_semantic_output_present',
})
ROOT_NAMES = frozenset({
    'neutral_semantic_evidence.jsonl', 'semantic_rule_v2.json',
    'reason_precedence_v2.json', 'independent_package_construction_manifest.json',
    'independent_package_manifest.json', 'SHA256SUMS.txt', 'bodies',
})
H64 = re.compile(r'^[0-9a-f]{64}$')


@dataclass(frozen=True)
class TrustedInputs:
    s04_manifest_sha256: str
    neutral_evidence_sha256: str
    semantic_rule_sha256: str
    reason_precedence_sha256: str
    body_sha256_by_path: dict[str, str]


class FirewallViolation(Exception):
    pass


def stop(reason: str):
    raise FirewallViolation(reason)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _pairs_no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            stop('DUPLICATE_JSON_OBJECT_KEY')
        result[k] = v
    return result


def _bad_constant(value):
    stop('INVALID_JSON_CONSTANT_' + str(value))


def parse_strict(raw: bytes):
    try:
        decoded = raw.decode('utf-8', errors='strict')
    except UnicodeError:
        stop('INVALID_ENCODING')
    if decoded.startswith('\ufeff'):
        stop('BOM_NOT_ALLOWED')
    try:
        return json.loads(decoded, object_pairs_hook=_pairs_no_duplicates,
                          parse_constant=_bad_constant)
    except FirewallViolation:
        raise
    except (ValueError, json.JSONDecodeError, RecursionError):
        stop('MALFORMED_JSON')


def parse_jsonl_strict(raw: bytes):
    try:
        decoded = raw.decode('utf-8', errors='strict')
    except UnicodeError:
        stop('INVALID_ENCODING')
    if decoded.startswith('\ufeff'):
        stop('BOM_NOT_ALLOWED')
    records = []
    for lineno, line in enumerate(decoded.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line, object_pairs_hook=_pairs_no_duplicates,
                                parse_constant=_bad_constant)
        except FirewallViolation:
            raise
        except (ValueError, json.JSONDecodeError, RecursionError):
            stop(f'MALFORMED_JSONL_LINE_{lineno}')
        records.append(record)
    if not records:
        stop('EMPTY_JSONL')
    return records


def _scan_keys(obj):
    stack = [obj]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                if not isinstance(key, str):
                    stop('NONSTRING_KEY')
                if key.casefold() in PROHIBITED:
                    stop('PROHIBITED_FIELD__' + key)
                stack.append(value)
        elif isinstance(node, list):
            stack.extend(node)


def _keys(obj, expected, label):
    if not isinstance(obj, dict):
        stop('SCHEMA_NOT_OBJECT__' + label)
    if set(obj) != expected:
        stop('SCHEMA_FIELD_MISMATCH__' + label)


def _relpath(text):
    if not isinstance(text, str) or not text:
        stop('INVALID_RELATIVE_PATH')
    if '\\' in text or '\x00' in text or text.startswith('/') or ':' in text:
        stop('PATH_ESCAPE')
    p = PurePosixPath(text)
    if any(segment in ('.', '..', '') for segment in text.split('/')) or p.is_absolute():
        stop('PATH_ESCAPE')
    if str(p) != text:
        stop('NONCANONICAL_PATH')
    if unicodedata.normalize('NFC', text) != text:
        stop('NONCANONICAL_UNICODE_PATH')
    return text


def _check_sources(trusted: TrustedInputs):
    for field in ('s04_manifest_sha256', 'neutral_evidence_sha256',
                  'semantic_rule_sha256', 'reason_precedence_sha256'):
        if not H64.fullmatch(getattr(trusted, field)):
            stop('INVALID_TRUSTED_SHA__' + field)
    for path, digest in trusted.body_sha256_by_path.items():
        _relpath(path)
        if not path.startswith('bodies/') or not H64.fullmatch(digest):
            stop('INVALID_TRUSTED_BODY_MAP')


def _tree(root: Path):
    if root.is_symlink() or not root.is_dir():
        stop('INVALID_PACKAGE_ROOT')
    files = {}
    seen = set()
    for parent, dirs, names in os.walk(root, topdown=True, followlinks=False):
        for entry in dirs + names:
            path = Path(parent) / entry
            rel = path.relative_to(root).as_posix()
            _relpath(rel)
            key = unicodedata.normalize('NFC', rel).casefold()
            if key in seen:
                stop('CASE_OR_PATH_COLLISION')
            seen.add(key)
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                stop('SYMLINK_ESCAPE_OR_ALIAS')
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                stop('UNSUPPORTED_FILESYSTEM_MEMBER')
            if not rel.startswith('bodies/') and rel not in ROOT_NAMES:
                stop('FILE_NOT_ALLOWLISTED__' + rel)
            if rel.startswith('bodies/') and stat.S_ISREG(mode) and path.suffix != '.txt':
                stop('BODY_UNEXPECTED_EXTENSION')
            if rel.startswith('bodies/') and not path.is_file():
                if rel != 'bodies':
                    stop('UNEXPECTED_BODY_SUBDIRECTORY')
            if stat.S_ISREG(mode):
                if path.stat().st_nlink != 1:
                    stop('HARDLINK_ALIAS')
                files[rel] = path
        if Path(parent) == root and 'bodies' not in dirs:
            stop('MISSING_BODY_DIRECTORY')
    return files


def _as_hash(value, label):
    if not isinstance(value, str) or not H64.fullmatch(value):
        stop('SCHEMA_INVALID_HASH__' + label)


def scan_independent_package(root: Path, trusted: TrustedInputs, *, phase: str = 'construction', expected_record_count: int = 500) -> dict:
    """Raise FirewallViolation on any uncertainty; success is conditional on supplied trusted identities.

    phase='construction' scans S07 pre-freeze tree; phase='freeze' validates S08 manifest/checksums.
    """
    if phase not in ('construction', 'freeze'):
        stop('UNKNOWN_PHASE')
    if type(expected_record_count) is not int or not 1 <= expected_record_count <= 500:
        stop('INVALID_EXPECTED_RECORD_COUNT')
    _check_sources(trusted)
    files = _tree(Path(root))
    base = {'neutral_semantic_evidence.jsonl', 'semantic_rule_v2.json',
            'reason_precedence_v2.json', 'independent_package_construction_manifest.json'}
    needed = base if phase == 'construction' else base | {'independent_package_manifest.json', 'SHA256SUMS.txt'}
    if not needed.issubset(files):
        stop('MISSING_REQUIRED_FILE')
    if phase == 'construction' and any(n in files for n in ('independent_package_manifest.json', 'SHA256SUMS.txt')):
        stop('PREMATURE_FREEZE_ARTIFACT')
    for rel in files:
        if rel not in needed and not rel.startswith('bodies/'):
            stop('UNEXPECTED_PACKAGE_MEMBER__' + rel)

    structures = {}
    for rel in sorted(files):
        path = files[rel]
        if rel.endswith('.json'):
            obj = parse_strict(path.read_bytes())
            _scan_keys(obj)
            structures[rel] = obj
        elif rel.endswith('.jsonl'):
            rows = parse_jsonl_strict(path.read_bytes())
            for row in rows:
                _scan_keys(row)
            structures[rel] = rows
        elif rel == 'SHA256SUMS.txt' or rel.startswith('bodies/'):
            pass
        else:
            stop('UNKNOWN_FORMAT')

    rows = structures['neutral_semantic_evidence.jsonl']
    referenced = {}
    seen_ids, seen_positions = set(), set()
    for row in rows:
        _keys(row, EVIDENCE_KEYS, 'NEUTRAL_EVIDENCE')
        if row['batch_id'] != 'BATCH_0004':
            stop('INCORRECT_BATCH_ID')
        sid = row['canonical_source_identity']
        position = row['authorized_population_position']
        if not isinstance(sid, str) or not sid or sid in seen_ids:
            stop('DUPLICATE_OR_INVALID_SOURCE_IDENTITY')
        if type(position) is not int or not 1501 <= position <= 2000 or position in seen_positions:
            stop('DUPLICATE_OR_INVALID_POSITION')
        seen_ids.add(sid)
        seen_positions.add(position)
        for key in ('accepted_record', 's03_validation'):
            if not isinstance(row[key], dict):
                stop('INVALID_STRUCTURED_SOURCE__' + key)
        for member_key, sha_key in (('body_evidence_member', 'extracted_body_sha256'),
                                    ('header_evidence_member', 'extracted_header_sha256')):
            member = row[member_key]
            if member is None:
                continue
            _relpath(member)
            if not member.startswith('bodies/'):
                stop('BODY_OR_HEADER_WRONG_PATH')
            digest = row[sha_key]
            _as_hash(digest, sha_key)
            if member in referenced and referenced[member] != digest:
                stop('CONFLICTING_EVIDENCE_REFERENCE')
            referenced[member] = digest
    if len(rows) != expected_record_count or seen_positions != set(range(1501, 1501 + expected_record_count)):
        stop('RECORD_COUNT_OR_POSITION_SET_FAILURE')
    bodypaths = set(path for path in files if path.startswith('bodies/'))
    if bodypaths != set(referenced) or bodypaths != set(trusted.body_sha256_by_path):
        stop('BODY_SOURCE_PATH_SET_MISMATCH')
    for path, digest in referenced.items():
        if digest != trusted.body_sha256_by_path[path] or _sha(files[path]) != digest:
            stop('BODY_SOURCE_HASH_MISMATCH')

    construction = structures['independent_package_construction_manifest.json']
    _keys(construction, CONSTRUCTION_KEYS, 'CONSTRUCTION_MANIFEST')
    if construction['source_s04_manifest_sha256'] != trusted.s04_manifest_sha256:
        stop('UNAPPROVED_SOURCE_PROVENANCE')
    if construction['artifact_id'] != 'BATCH0004_CLEAN_INDEPENDENT_PACKAGE_CONSTRUCTION':
        stop('CONSTRUCTION_IDENTITY_MISMATCH')
    for flag in ('primary_ledger_included', 'primary_semantic_fields_included',
                 'primary_aggregate_counts_included', 'mismatch_expectations_included',
                 'final_reconciliation_included'):
        if construction[flag] is not False:
            stop('PROHIBITED_LINEAGE_FLAG__' + flag)
    if construction['allowed_sources'] != [
            'S04_NEUTRAL_EVIDENCE', 'SEMANTIC_RULE_V2', 'REASON_PRECEDENCE_V2']:
        stop('UNAPPROVED_SOURCE_PROVENANCE')

    for rel, pinned in (
        ('neutral_semantic_evidence.jsonl', trusted.neutral_evidence_sha256),
        ('semantic_rule_v2.json', trusted.semantic_rule_sha256),
        ('reason_precedence_v2.json', trusted.reason_precedence_sha256)):
        if _sha(files[rel]) != pinned:
            stop('FROZEN_SOURCE_SHA_MISMATCH__' + rel)
    hashes = {rel: _sha(file) for rel, file in sorted(files.items())}
    if phase == 'freeze':
        manifest = structures['independent_package_manifest.json']
        _keys(manifest, FREEZE_KEYS, 'PACKAGE_MANIFEST')
        premanifest = {k: hashes[k] for k in hashes if k not in ('independent_package_manifest.json', 'SHA256SUMS.txt')}
        if manifest['artifact_id'] != 'BATCH0004_INDEPENDENT_CLEAN_PACKAGE_FREEZE' or \
           manifest['file_allowlist'] != sorted(premanifest) or \
           manifest['file_hashes'] != premanifest or \
           manifest['contamination_check'] != 'PASS' or \
           manifest['source_lineage'] != 'S04_NEUTRAL_EVIDENCE_ONLY' or \
           manifest['primary_semantic_output_present'] is not False:
            stop('PACKAGE_MANIFEST_MISMATCH')
        try:
            sums = files['SHA256SUMS.txt'].read_bytes().decode('ascii', errors='strict')
        except UnicodeError:
            stop('INVALID_SHA256SUMS_ENCODING')
        expected_sums = ''.join(f'{hashes[p]}  {p}\n' for p in sorted(hashes) if p != 'SHA256SUMS.txt')
        if sums != expected_sums:
            stop('SHA256SUMS_MISMATCH')
    return {'status': 'PASS', 'phase': phase, 'record_count': len(rows),
            'source_identities': len(seen_ids), 'body_file_count': len(bodypaths),
            'file_sha256': hashes}


def validate_frozen_zip(zip_path: Path, frozen_root: Path, trusted: TrustedInputs,
                        *, expected_record_count: int = 500, expected_zip_sha256: str | None = None) -> dict:
    """Verify a ZIP corresponds byte-for-byte to a validated frozen source tree, without extraction."""
    import zipfile
    checked = scan_independent_package(frozen_root, trusted,
                                       phase='freeze', expected_record_count=expected_record_count)
    zip_path = Path(zip_path)
    if zip_path.is_symlink() or not zip_path.is_file():
        stop('INVALID_ARCHIVE_PATH')
    archive_sha = _sha(zip_path)
    if expected_zip_sha256 is not None and archive_sha != expected_zip_sha256:
        stop('ZIP_SHA256_MISMATCH')
    seen = set()
    entries = set()
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for info in zf.infolist():
                rel = _relpath(info.filename)
                norm = unicodedata.normalize('NFC', rel).casefold()
                if norm in seen:
                    stop('DUPLICATE_ARCHIVE_MEMBER_AMBIGUITY')
                seen.add(norm)
                if info.is_dir():
                    stop('UNEXPECTED_ARCHIVE_DIRECTORY')
                if rel not in checked['file_sha256']:
                    stop('UNEXPECTED_ARCHIVE_PATH')
                source = Path(frozen_root) / rel
                if info.file_size != source.stat().st_size:
                    stop('ARCHIVE_SOURCE_SIZE_MISMATCH')
                digest = hashlib.sha256()
                with zf.open(info, 'r') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                if digest.hexdigest() != checked['file_sha256'][rel]:
                    stop('ARCHIVE_SOURCE_HASH_MISMATCH')
                entries.add(rel)
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        stop('INVALID_ARCHIVE__' + type(exc).__name__)
    if entries != set(checked['file_sha256']):
        stop('ARCHIVE_MEMBER_SET_MISMATCH')
    return {'status': 'PASS', 'zip_sha256': archive_sha, 'member_count': len(entries)}
