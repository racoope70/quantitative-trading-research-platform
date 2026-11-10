"""Bounded nonaccepting staging and exact-byte readback; no checkpoint access.

Not a REAL activation component. All paths are beneath an explicitly supplied
new synthetic workspace. Promotion and model execution occur elsewhere/never.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat

class StageStop(RuntimeError):
    pass


def require(ok, code):
    if not ok:
        raise StageStop(code)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def same_name(value):
    require(type(value) is str and re.fullmatch(r'[A-Za-z0-9_\-]{1,150}', value) is not None, 'UNSAFE_BINDING_NAME')
    return value


def safe_folder(folder: Path):
    folder = Path(folder)
    require(not folder.is_symlink(), 'SYMLINK_DIRECTORY')
    if not folder.exists():
        folder.mkdir(mode=0o700, parents=True, exist_ok=False)
    require(folder.is_dir() and not folder.is_symlink(), 'BAD_DIRECTORY')
    return folder


def safe_read(path: Path):
    path = Path(path)
    require(not path.is_symlink(), 'SYMLINK_ARTIFACT')
    flags=os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    fd=os.open(path, flags)
    try:
        mode=os.fstat(fd)
        require(stat.S_ISREG(mode.st_mode) and mode.st_nlink == 1, 'NONREGULAR_OR_MULTILINK_ARTIFACT')
        with os.fdopen(fd, 'rb', closefd=False) as f:
            return f.read()
    finally:
        os.close(fd)


def exclusive_write(path: Path, raw: bytes):
    require(type(raw) is bytes, 'INVALID_STAGING_BYTES')
    path=Path(path)
    safe_folder(path.parent)
    fd=os.open(path,os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os,'O_NOFOLLOW',0),0o400)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
    finally:
        os.close(fd)
    require(safe_read(path)==raw, 'STAGING_WRITE_READBACK_MISMATCH')
    return sha(raw)


@dataclass(frozen=True, slots=True)
class UnitBinding:
    batch_id: str
    role: str
    unit_id: str
    attempt_id: str
    checkpoint_identity: str
    unit_input_sha256: str
    execution_mode: str
    mode_binding_sha256: str
    expected_positions: tuple
    expected_identities: tuple
    max_new_units: int = 1

    def verify(self):
        for value in (self.batch_id,self.role,self.unit_id,self.attempt_id,self.checkpoint_identity): same_name(value)
        require(self.batch_id=='BATCH0004' and self.role in ('PRIMARY','INDEPENDENT'), 'INVALID_BATCH_OR_ROLE')
        require(self.execution_mode=='SYNTHETIC_NONPRODUCTION', 'REAL_MODE_FORBIDDEN_IN_NONPRODUCTION')
        require(type(self.max_new_units) is int and self.max_new_units==1, 'MAX_NEW_UNITS_VIOLATION')
        require(self.unit_id=='U0012', 'U0013_FORBIDDEN')
        for item in (self.unit_input_sha256,self.mode_binding_sha256):
            require(type(item) is str and re.fullmatch(r'[0-9a-f]{64}',item) is not None,'BAD_HASH_BINDING')
        require(type(self.expected_positions) is tuple and len(self.expected_positions)==25 and
                all(type(x) is int for x in self.expected_positions) and
                self.expected_positions==tuple(range(1776,1801)), 'UNEXPECTED_POSITION_SCOPE')
        require(type(self.expected_identities) is tuple and len(self.expected_identities)==25 and
                len(set(self.expected_identities))==25 and all(type(x) is str and x for x in self.expected_identities),'INVALID_IDENTITY_LIST')
        return self


def check_payload(payload, binding):
    require(type(payload) is dict and type(payload.get('raw_rows')) is list, 'INVALID_CHECKED_SCHEMA')
    rows=payload['raw_rows']
    require(len(rows)==25 and type(payload.get('row_count')) is int and payload['row_count']==25, 'INVALID_OUTPUT_COUNT')
    require(all(type(row) is dict for row in rows), 'BAD_ROW_SCHEMA')
    require(tuple(row.get('authorized_population_position') for row in rows)==binding.expected_positions and
            all(type(row.get('authorized_population_position')) is int for row in rows), 'POSITION_MISMATCH')
    require(tuple(row.get('canonical_source_identity') for row in rows)==binding.expected_identities,'IDENTITY_MISMATCH')
    return rows


@dataclass(frozen=True, slots=True)
class StagedArtifact:
    file: Path
    staged_bytes_sha256: str
    readback_sha256: str
    file_size: int
    row_count: int
    payload: dict
    binding: UnitBinding


def stage_validated_payload(root: Path, binding: UnitBinding, payload: dict) -> StagedArtifact:
    binding.verify()
    rows=check_payload(payload,binding)
    raw=canonical(payload)
    folder=safe_folder(safe_folder(safe_folder(root)/'staging')/binding.unit_id)
    path=folder/(same_name(binding.attempt_id)+'.json')
    staged_digest=exclusive_write(path,raw)
    readback=safe_read(path)
    require(readback==raw and sha(readback)==staged_digest, 'READBACK_BYTE_MISMATCH')
    try: decoded=json.loads(readback)
    except (ValueError,UnicodeDecodeError) as exc: raise StageStop('DESERIALIZATION_FAILURE') from exc
    require(decoded==payload,'SEMANTIC_CONTENT_CHANGED')
    check_payload(decoded,binding)
    require(len(readback)==len(raw),'STAGED_TRUNCATION')
    return StagedArtifact(path,staged_digest,sha(readback),len(readback),len(rows),decoded,binding)


def verify_stage(stage: StagedArtifact):
    require(type(stage) is StagedArtifact,'UNTRUSTED_STAGE_OBJECT')
    stage.binding.verify()
    raw=safe_read(stage.file)
    require(len(raw)==stage.file_size,'STAGED_FILE_SIZE_MISMATCH')
    require(sha(raw)==stage.staged_bytes_sha256==stage.readback_sha256,'STAGED_HASH_MISMATCH')
    try: decoded=json.loads(raw)
    except (ValueError,UnicodeDecodeError) as exc: raise StageStop('STAGED_JSON_INVALID') from exc
    require(decoded==stage.payload,'STAGED_CONTENT_CHANGED')
    check_payload(decoded,stage.binding)
    require(canonical(decoded)==raw,'NONCANONICAL_STAGED_BYTES')
    return raw

class AppendOnlyNonproductionJournal:
    """Hash-chained synthetic operational events; NOT a real checkpoint."""
    def __init__(self, root: Path, binding: UnitBinding):
        self.folder=safe_folder(safe_folder(root)/'operational_journal')
        self.binding=binding.verify()
        self.head_hash=None
        self.count=0
        self.append('SESSION_CREATED__NONPRODUCTION')

    def append(self, event: str, details=None):
        require(event in ('SESSION_CREATED__NONPRODUCTION',
                          'STAGED_FOR_OPERATIONAL_INTEGRITY_VERIFICATION',
                          'TRUSTED_PROOF_ISSUED__NONACCEPTING',
                          'SYNTHETIC_ONE_UNIT_COMPLETE__NO_DISPATCH',
                          'CONTROLLED_STOP__RETURN_TO_MANAGING'), 'BAD_JOURNAL_EVENT')
        if self.count: self.verify()
        data={'sequence':self.count+1,'previous_sha256':self.head_hash,
              'event':event,'batch_id':self.binding.batch_id,
              'unit_id':self.binding.unit_id,'attempt_id':self.binding.attempt_id,
              'checkpoint_identity':self.binding.checkpoint_identity,
              'execution_mode':self.binding.execution_mode,
              'details':details or {}}
        raw=canonical(data)
        path=self.folder/('event_%04d.json'%(self.count+1))
        exclusive_write(path,raw)
        self.count+=1; self.head_hash=sha(raw)
        self.verify()
        return self.head_hash

    def verify(self):
        require(len(list(self.folder.glob('event_*.json')))==self.count,'JOURNAL_MEMBER_COUNT_MISMATCH')
        previous=None
        for i in range(1,self.count+1):
            path=self.folder/('event_%04d.json'%i)
            raw=safe_read(path)
            try: obj=json.loads(raw)
            except (ValueError,UnicodeDecodeError) as exc:raise StageStop('JOURNAL_DECODING_FAILED') from exc
            require(raw==canonical(obj) and obj['sequence']==i and
                    obj['previous_sha256']==previous and
                    obj['checkpoint_identity']==self.binding.checkpoint_identity and
                    obj['attempt_id']==self.binding.attempt_id,'JOURNAL_CHAIN_INVALID')
            previous=sha(raw)
        require(previous==self.head_hash,'JOURNAL_HEAD_INVALID')
        return True
