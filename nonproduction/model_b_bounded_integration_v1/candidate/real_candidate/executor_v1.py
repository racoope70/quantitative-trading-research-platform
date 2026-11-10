"""Prospective bounded derivative of frozen V3 executor/persistence, never REAL authority.

The frozen historical runner and its event parser are retained unchanged. This
adapter uses the existing ControlledLocalCapture, records the same raw artifact
names, and passes successful observations through the existing BoundProofPath.
"""
from __future__ import annotations

import dataclasses
import ast
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import stat
import sys
import time
import types

from trusted_stage.staging_v1 import StageStop, canonical, require, safe_read, sha
from .capture_v1 import ControlledLocalCapture

MAX_CAPTURE_BYTES = 16 * 1024 * 1024
# Standing Owner reserve is additional to the unchanged execution envelope.
OWNER_STORAGE_HEADROOM_BYTES = 2_000_000_000
FROZEN_EXECUTOR_SHA256 = 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0'
FROZEN_EXECUTOR_PATH = Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/two_attempt_recovery_compatibility_v1/dependencies/reference/v6_accepted/frozen_v3_orchestrator_reference.py')
# This isolated derivative uses the same immutable, hash-checked source already
# in its accepted closure. Historical/REAL source locations remain unchanged.
if Path(__file__).absolute() == Path('/private/tmp/QTRP_MODEL_B_A11_REAL_CONTRACT_NONPRODUCTION_QUALIFICATION_V1/candidate/real_candidate/executor_v1.py'):
    FROZEN_EXECUTOR_PATH = Path(__file__).absolute().parents[2] / 'accepted/accepted_recovery/reference/v6_accepted/frozen_v3_orchestrator_reference.py'
_frozen_module = None


def source_sha():
    return sha(safe_read(Path(__file__)))


def structural_event_evidence(stdout):
    """Bounded local structure only; never an acceptance decision or provider ID.

    Predicates match the pinned frozen extraction and validator. Witness lists
    retain the first 64 local occurrences; full counts and the last frozen
    selection remain explicit. No event value other than those predicates is
    copied into the diagnostic receipt.
    """
    require(type(stdout) is bytes and len(stdout) <= MAX_CAPTURE_BYTES,
            'RAW_EVIDENCE_LIMIT_EXCEEDED')
    result = {'schema': 'CAPTURED_EVENT_STRUCTURE_V1',
              'scope': 'CAPTURED_STDOUT_ONLY__NOT_PROVIDER_PROVENANCE',
              'ordinal_basis': 'ONE_BASED_NONBLANK_CAPTURED_LINE',
              'occurrence_basis': 'ONE_BASED_QUALIFYING_MESSAGE_IN_CAPTURE_ORDER',
              'witness_limit': 64, 'witness_lists_truncated': False,
              'captured_event_count': 0, 'qualifying_final_message_count': 0,
              'completed_turn_count': 0, 'final_message_event_ordinals': [],
              'completed_turn_event_ordinals': [],
              'frozen_selected_message_occurrence_index': 'FIELD_NOT_AVAILABLE',
              'frozen_selected_event_ordinal': 'FIELD_NOT_AVAILABLE',
              'provider_event_identity': 'FIELD_NOT_AVAILABLE',
              'transport_delivery_identity': 'FIELD_NOT_AVAILABLE',
              'event_timestamp': 'FIELD_NOT_AVAILABLE',
              'validator_cardinality_qualification': 'FIELD_NOT_AVAILABLE',
              'parse_status': 'COMPLETE_JSON_OBJECT_LINES'}
    try:
        lines = stdout.decode('utf-8', errors='strict').splitlines()
        for line in lines:
            if not line.strip():
                continue
            result['captured_event_count'] += 1
            ordinal = result['captured_event_count']
            event = json.loads(line)
            if type(event) is not dict:
                result['parse_status'] = 'NON_OBJECT_EVENT'
                break
            if (event.get('type') == 'item.completed'
                    and type(event.get('item')) is dict
                    and event['item'].get('type') == 'agent_message'
                    and type(event['item'].get('text')) is str):
                result['qualifying_final_message_count'] += 1
                result['frozen_selected_message_occurrence_index'] = result['qualifying_final_message_count']
                result['frozen_selected_event_ordinal'] = ordinal
                if len(result['final_message_event_ordinals']) < result['witness_limit']:
                    result['final_message_event_ordinals'].append(ordinal)
                else:
                    result['witness_lists_truncated'] = True
            if event.get('type') == 'turn.completed':
                result['completed_turn_count'] += 1
                if len(result['completed_turn_event_ordinals']) < result['witness_limit']:
                    result['completed_turn_event_ordinals'].append(ordinal)
                else:
                    result['witness_lists_truncated'] = True
    except (UnicodeDecodeError, ValueError, RecursionError):
        result['parse_status'] = 'INVALID_ENCODING_OR_JSON'
    if result['parse_status'] == 'COMPLETE_JSON_OBJECT_LINES':
        result['validator_cardinality_qualification'] = (
            'CARDINALITY_ONLY_PASS' if result['qualifying_final_message_count'] == 1
            and result['completed_turn_count'] == 1 else 'CARDINALITY_REJECT')
    else:
        # Partial counts are explicitly identified; they never assert a full
        # envelope result or successful frozen extraction.
        result['frozen_selected_message_occurrence_index'] = 'FIELD_NOT_AVAILABLE'
        result['frozen_selected_event_ordinal'] = 'FIELD_NOT_AVAILABLE'
    return result


_REJECTION_KEYS = ('FIRST_REJECTING_GUARD_ID', 'SAFE_NONPAYLOAD_REASON_CODE')
_UNKNOWN_REJECTION = ('UNKNOWN', 'UNKNOWN')


def _rejection_sources():
    """Only existing release-pinned code; never a traceback-supplied data path."""
    from .release_v1 import MANIFEST_FILE
    root = Path(__file__).resolve().parents[2]
    descriptor = json.loads(safe_read(root / MANIFEST_FILE))
    sources = {}
    for group in ('accepted_components', 'new_integration_components', 'prospective_components'):
        for item in descriptor[group].values():
            if item['path'].endswith('.py'):
                sources[(root / item['path']).resolve()] = item['sha256']
    sources[FROZEN_EXECUTOR_PATH.resolve()] = FROZEN_EXECUTOR_SHA256
    sources[(root / 'accepted/accepted_recovery/reference/v6_accepted/frozen_v3_orchestrator_reference.py').resolve()] = FROZEN_EXECUTOR_SHA256
    return sources


def _literal_rejection_code(node):
    # Extract a source literal prefix, never an evaluated argument or exc text.
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        node = node.left
    if isinstance(node, ast.Constant) and type(node.value) is str:
        code = node.value.rstrip('_')
        if re.fullmatch(r'[A-Z][A-Z0-9_]{0,79}', code):
            return code
    return None


def _site_reason(node):
    if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args:
        return _literal_rejection_code(node.exc.args[0])
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in ('require', 'ensure', 'need') and len(node.args) == 2):
        return _literal_rejection_code(node.args[1])
    return None


def _code_tree(code):
    yield code
    for item in code.co_consts:
        if isinstance(item, types.CodeType):
            yield from _code_tree(item)


def _trace_site(tb, kind, sources):
    path = Path(tb.tb_frame.f_code.co_filename).resolve()
    pin = sources.get(path)
    if pin is None:
        return None
    raw = safe_read(path)
    if len(raw) > 512 * 1024 or sha(raw) != pin:
        return None
    code = compile(raw, tb.tb_frame.f_code.co_filename, 'exec', dont_inherit=True)
    if not any(c == tb.tb_frame.f_code for c in _code_tree(code)):
        return None
    position = list(tb.tb_frame.f_code.co_positions())[tb.tb_lasti // 2]
    line, _, col, _ = position
    if line is None or col is None:
        return None
    nodes = [n for n in ast.walk(ast.parse(raw)) if isinstance(n, kind)
             and n.lineno <= line <= n.end_lineno
             and (n.lineno != line or n.col_offset <= col)
             and (n.end_lineno != line or col < n.end_col_offset)]
    if not nodes:
        return None
    node = min(nodes, key=lambda n: (n.end_lineno - n.lineno, n.end_col_offset - n.col_offset))
    return node, pin


def _origin_rejection(exc):
    try:
        seen = set()
        for _ in range(8):
            if id(exc) in seen:
                return _UNKNOWN_REJECTION
            seen.add(id(exc))
            if exc.__cause__ is None:
                if exc.__context__ is not None:
                    return _UNKNOWN_REJECTION  # independent chronology not established
                break
            exc = exc.__cause__
        else:
            return _UNKNOWN_REJECTION
        frames = []
        tb = exc.__traceback__
        while tb is not None and len(frames) < 32:
            frames.append(tb)
            tb = tb.tb_next
        if tb is not None or not frames:
            return _UNKNOWN_REJECTION
        sources = _rejection_sources()
        site = _trace_site(frames[-1], ast.Raise, sources)
        if site is None:
            return _UNKNOWN_REJECTION
        node, pin = site
        if (not isinstance(node.exc, ast.Call) or not isinstance(node.exc.func, ast.Name)
                or frames[-1].tb_frame.f_globals.get(node.exc.func.id) is not type(exc)):
            return _UNKNOWN_REJECTION
        if _site_reason(node) is None:
            if len(frames) < 2:
                return _UNKNOWN_REJECTION
            site = _trace_site(frames[-2], ast.Call, sources)
            if site is None:
                return _UNKNOWN_REJECTION
            node, pin = site
            callee = frames[-2].tb_frame.f_globals.get(getattr(node.func, 'id', None))
            if getattr(callee, '__code__', None) is not frames[-1].tb_frame.f_code:
                return _UNKNOWN_REJECTION
        reason = _site_reason(node)
        if reason is None:
            return _UNKNOWN_REJECTION
        return f'G_{pin}_{node.lineno}_{node.col_offset}', reason
    except Exception:
        return _UNKNOWN_REJECTION


def valid_first_rejection_fields(fields):
    """Finite source-defined IDs/codes, no arbitrary messages or extra fields."""
    try:
        if type(fields) is not dict or set(fields) != set(_REJECTION_KEYS):
            return False
        guard, reason = (fields[k] for k in _REJECTION_KEYS)
        if (guard, reason) == _UNKNOWN_REJECTION:
            return True
        if type(guard) is not str or type(reason) is not str or len(guard) > 96:
            return False
        match = re.fullmatch(r'G_([0-9a-f]{64})_([1-9][0-9]{0,5})_([0-9]{1,4})', guard)
        if match is None or re.fullmatch(r'[A-Z][A-Z0-9_]{0,79}', reason) is None:
            return False
        pin, line, col = match.groups()
        for path, expected in _rejection_sources().items():
            if expected != pin:
                continue
            raw = safe_read(path)
            if len(raw) <= 512 * 1024 and sha(raw) == pin:
                return any(isinstance(n, (ast.Call, ast.Raise)) and n.lineno == int(line)
                           and n.col_offset == int(col) and _site_reason(n) == reason
                           for n in ast.walk(ast.parse(raw)))
        return False
    except Exception:
        return False


def first_rejection_fields(carrier):
    value = getattr(carrier, '_first_rejection', None)
    if value is None:
        return {}  # ordinary success gets no rejection receipt
    fields = dict(zip(_REJECTION_KEYS, value)) if type(value) is tuple and len(value) == 2 else {}
    return fields if valid_first_rejection_fields(fields) else dict(zip(_REJECTION_KEYS, _UNKNOWN_REJECTION))


def remember_first_rejection(carrier, exc=None):
    if getattr(carrier, '_first_rejection', None) is None:
        carrier._first_rejection = _origin_rejection(exc) if exc is not None else _UNKNOWN_REJECTION
    transaction = getattr(carrier, 'transaction', None)
    if transaction is not None and getattr(transaction, '_first_rejection', None) is None:
        transaction._first_rejection = carrier._first_rejection


def relay_first_rejection(context, manifest):
    """Readback is checked against independently held executor facts, not trusted alone."""
    expected = first_rejection_fields(context)
    actual = {k: manifest[k] for k in _REJECTION_KEYS if k in manifest}
    if actual != expected or (actual and not valid_first_rejection_fields(actual)):
        return False
    transaction = getattr(context, 'transaction', None)
    if expected and transaction is not None and getattr(transaction, '_first_rejection', None) is None:
        transaction._first_rejection = context._first_rejection
    return True


def _frozen():
    global _frozen_module
    require(sha(safe_read(FROZEN_EXECUTOR_PATH)) == FROZEN_EXECUTOR_SHA256,
            'HISTORICAL_FROZEN_EXECUTOR_DRIFT')
    if _frozen_module is None:
        spec = importlib.util.spec_from_file_location('prospective_executor_frozen_v3_reference', FROZEN_EXECUTOR_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _frozen_module = module
    return _frozen_module


def _path(path):
    path = Path(path)
    require(path.is_absolute() and '..' not in path.parts, 'ABSOLUTE_BOUND_PATH_REQUIRED')
    return path


def _bounded_json(value, maximum):
    """Incrementally bound serialized bytes BEFORE concatenation or persistence."""
    encoder = json.JSONEncoder(sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2)
    chunks = []
    size = 1  # terminal LF
    for part in encoder.iterencode(value):
        encoded = part.encode('utf-8')
        size += len(encoded)
        require(size <= maximum, 'SERIALIZED_ARTIFACT_CAPACITY_EXCEEDED')
        chunks.append(encoded)
    return b''.join(chunks) + b'\n'


def serialization_size(value, maximum, *, ensure_ascii=True, indent=2,
                       separators=None, allow_nan=False):
    """Bound an existing serializer's exact encoding before its full allocation.

    The optional arguments let the prospective recovery preserve its accepted
    compact UTF-8 bytes. This routine grants no path, write, or execution access.
    """
    require(type(maximum) is int and maximum >= 0, 'INVALID_SERIALIZATION_CAP')
    size = 1
    encoder = json.JSONEncoder(sort_keys=True, ensure_ascii=ensure_ascii,
        allow_nan=allow_nan, indent=indent, separators=separators)
    for part in encoder.iterencode(value):
        size += len(part.encode('utf-8'))
        require(size <= maximum, 'SERIALIZED_ARTIFACT_CAPACITY_EXCEEDED')
    return size


_serialization_size = serialization_size


def storage_contract_from_metadata(*, capture_bytes, context_facts, frame_bytes,
                                   configuration=None, checkpoint_snapshot_max_bytes=0,
                                   validator_source_sizes=(), input_file_sizes=()):
    """Calculate the complete one-attempt disk envelope from fixed metadata.

    All lengths come from the accepted source/input inventories or exact bound
    configuration/context records. No engine, constructor, source import, file
    access, or REAL action is needed to evaluate this calculation.
    """
    require(type(capture_bytes) is int and 1 <= capture_bytes <= MAX_CAPTURE_BYTES,
            'INVALID_CAPTURE_STORAGE_BOUND')
    validator_source_sizes = tuple(validator_source_sizes)
    input_file_sizes = tuple(input_file_sizes)
    sizes = (frame_bytes, checkpoint_snapshot_max_bytes,
             *validator_source_sizes, *input_file_sizes)
    require(all(type(size) is int and size >= 0 for size in sizes),
            'INVALID_FIXED_STORAGE_METADATA')
    require(type(context_facts) is dict and
            (configuration is None or type(configuration) is dict),
            'INVALID_FIXED_STORAGE_RECORD')
    fixed = len(canonical(context_facts)) + frame_bytes
    if configuration is not None:
        fixed += len(canonical(configuration))
    # The existing validator can add one reason-contract category to each of
    # the accepted maximum 25 rows. Prepared-source byte lengths bound those
    # fixed strings without reading or analysing any scientific input.
    fixed += 25 * sum(validator_source_sizes) + checkpoint_snapshot_max_bytes
    inputs = sum(input_file_sizes)
    artifact = 6 * (capture_bytes + fixed)
    receipt = 6 * fixed
    return {'capture_bytes': capture_bytes, 'fixed_metadata_bytes': fixed,
            'artifact_bytes': artifact, 'receipt_bytes': receipt,
            'raw_and_final_copies': 4 * capture_bytes,
            'staging_and_acceptance_bytes': 2 * artifact,
            'metadata_bytes': 12 * artifact, 'failure_reserve_bytes': receipt,
            'input_materialization_bytes': inputs, 'process_start_receipt_bytes': receipt,
            'peak_storage_bytes': inputs + 4 * capture_bytes + 14 * artifact + 2 * receipt + 8192,
            'timing_receipt_bytes': 8192,
            'readback_extra_bytes': 0, 'promotion_extra_inodes': 0,
            'serialization_expansion_factor': 6}


def _existing_parent(path):
    path = _path(path)
    while not path.exists():
        require(not path.is_symlink() and path.parent != path, 'UNAVAILABLE_EVIDENCE_PARENT')
        path = path.parent
    require(path.is_dir() and not path.is_symlink(), 'UNSAFE_EVIDENCE_PARENT')
    return path


def _ensure_capacity(path, required):
    require(type(required) is int and required >= 0, 'INVALID_EVIDENCE_CAPACITY_REQUIREMENT')
    fs = os.statvfs(_existing_parent(path))
    require(fs.f_bavail * fs.f_frsize >= required + OWNER_STORAGE_HEADROOM_BYTES,
            'INSUFFICIENT_EVIDENCE_CAPACITY')


def _write_exclusive(path, raw, maximum):
    require(type(raw) is bytes and len(raw) <= maximum, 'ARTIFACT_CAPACITY_EXCEEDED')
    path = Path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(fd, view)
            require(written > 0, 'INCOMPLETE_EXECUTOR_EVIDENCE_WRITE')
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    require(safe_read(path) == raw, 'EXECUTOR_EVIDENCE_READBACK_FAILURE')
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | getattr(os, 'O_NOFOLLOW', 0))
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return sha(raw)


class ExecutionContext:
    """Exact objects and paths from the existing composition; not an authorization."""
    def __init__(self, *, composition, supervisor, proof_path, transaction, binding, frame,
                 release_root, stage_root, work_root, durable_root, prompt, codex_path,
                 role='PRIMARY'):
        self.composition = composition
        self.supervisor = supervisor
        self.proof_path = proof_path
        self.transaction = transaction
        self.binding = binding
        self.frame = _path(frame)
        self.release_root = _path(release_root)
        self.stage_root = _path(stage_root)
        self.work_root = _path(work_root)
        self.durable_root = _path(durable_root)
        self._historical_attempt_count = len(transaction._historical_attempts)
        require(type(self._historical_attempt_count) is int and
                self._historical_attempt_count in (9,10),'EXECUTOR_HISTORY_CONTEXT_INVALID')
        self.working_directory = self.work_root / f'PRIMARY/U0012/A{self._historical_attempt_count+1:04d}/input'
        self.evidence_root = self.working_directory.parent / 'v3_executor_raw_evidence'
        self.prompt = prompt
        self.codex_path = str(codex_path)
        self.role = role
        self._test_only = False
        self._used = False
        self._persistence_started = False
        self._start_bytes = None
        self._original_facts = None
        self._first_rejection = None
        self._original_facts = verify_runtime_context(self)

    @classmethod
    def for_nonproduction(cls, *, supervisor, frame, work_root, stage_root, durable_root,
                          historical_attempt_count=9):
        require(type(supervisor) is ControlledLocalCapture and supervisor.mode == 'NONPRODUCTION_TEST'
                and supervisor._allow_test, 'NONPRODUCTION_CAPTURE_REQUIRED')
        self = object.__new__(cls)
        self.composition = self.proof_path = self.transaction = self.binding = None
        self.supervisor = supervisor
        self.frame = _path(frame)
        self.work_root, self.stage_root, self.durable_root = map(_path, (work_root, stage_root, durable_root))
        require(type(historical_attempt_count) is int and historical_attempt_count in (9,10),
                'EXECUTOR_HISTORY_CONTEXT_INVALID')
        self._historical_attempt_count=historical_attempt_count
        self.working_directory = self.work_root / f'PRIMARY/U0012/A{historical_attempt_count+1:04d}/input'
        self.evidence_root = self.working_directory.parent / 'v3_executor_raw_evidence'
        self.release_root = self.work_root
        self.prompt = 'INERT_BYTE_ENVELOPE_TEST_ONLY'
        self.codex_path = str(supervisor.executable)
        self.role = 'PRIMARY'
        self._test_only = True
        self._used = False
        self._persistence_started = False
        self._start_bytes = None
        self._original_facts = None
        self._first_rejection = None
        self._original_facts = verify_runtime_context(self)
        return self

    def storage_contract(self):
        facts = verify_runtime_context(self)
        configuration = None
        input_sizes = source_sizes = ()
        checkpoint_maximum = 0
        if self.composition is not None:
            configuration = self.composition.configuration()
            module = sys.modules[type(self.composition).__module__]
            original = module.reference_configuration['transport']
            input_sizes = tuple((Path(original['scientific_directory']) / name).stat().st_size
                                for name in original['scientific_files_sha256'])
            # Existing immutable inventories supply exact paths, not a new scan.
            source_sizes = [path.stat().st_size for path, _ in self.composition.validator._sources]
            cp = self.composition.attestor.root
            binding = self.composition.configuration()['recovery_binding']
            checkpoint_maximum = max((cp / name).stat().st_size
                for name in binding['checkpoint_files_sha256'] if '/checkpoints/' in name)
        # A=6(M+F), R=6F. Actual route: stage+checked result=2A; executor
        # manifest1+journals3+snapshots4+pending/new head1+checkpoint attempt
        # manifest1+validation1+proof1=12A. Raw and final text persisted twice
        # total4M; one start and one controlled-stop receipt add2R. Readback
        # uses the same inode; this caller does not invoke promotion.
        return storage_contract_from_metadata(capture_bytes=self.supervisor._max_output_bytes,
            context_facts=facts, frame_bytes=self.frame.stat().st_size,
            configuration=configuration, checkpoint_snapshot_max_bytes=checkpoint_maximum,
            validator_source_sizes=source_sizes, input_file_sizes=input_sizes)


def verify_runtime_context(context, *, phase='STATIC', working_directory=None, prompt=None,
                           codex_path=None, evidence_root=None, role=None):
    require(type(context) is ExecutionContext, 'EXACT_EXECUTION_CONTEXT_REQUIRED')
    c = context
    require(phase in ('STATIC', 'EXECUTING'), 'UNSUPPORTED_EXECUTION_CONTEXT_PHASE')
    require(c.role == 'PRIMARY' and type(c.prompt) is str and c.prompt, 'EXACT_UNIT_EXECUTOR_SCOPE_REQUIRED')
    require(type(c.supervisor) is ControlledLocalCapture and c.supervisor.input_delivery == 'FILE_IDENTITY_FRAME',
            'EXACT_FILE_INPUT_CAPTURE_REQUIRED')
    require(1 <= c.supervisor._max_output_bytes <= MAX_CAPTURE_BYTES, 'CAPTURE_BOUND_DRIFT')
    c.supervisor._fresh()
    count=c._historical_attempt_count
    require(type(count) is int and count in (9,10),'EXECUTOR_HISTORY_CONTEXT_INVALID')
    require(c.working_directory == c.work_root / f'PRIMARY/U0012/A{count+1:04d}/input'
            and c.evidence_root == c.working_directory.parent / 'v3_executor_raw_evidence', 'EXECUTOR_DESTINATION_DRIFT')
    for supplied, actual in ((working_directory, c.working_directory), (evidence_root, c.evidence_root)):
        if supplied is not None:
            require(Path(supplied) == actual, 'EXECUTOR_INVOCATION_PATH_DRIFT')
    for supplied, actual in ((prompt, c.prompt), (codex_path, c.codex_path), (role, c.role)):
        if supplied is not None:
            require(supplied == actual, 'EXECUTOR_INVOCATION_DRIFT')
    require(c.frame.is_file() and not c.frame.is_symlink() and c.frame.stat().st_size <= MAX_CAPTURE_BYTES,
            'EXECUTOR_INPUT_FRAME_UNSAFE')
    frame_sha = sha(safe_read(c.frame))
    facts = {'executor_source_sha256': source_sha(),
             'capture_source_sha256': sha(safe_read(Path(sys.modules[ControlledLocalCapture.__module__].__file__))),
             'capture_config_sha256': c.supervisor.config_sha256, 'frame_sha256': frame_sha,
             'role': 'PRIMARY', 'unit_id': 'U0012', 'next_attempt_sequence': count+1,
             'historical_attempt_count': count, 'max_new_units': 1, 'u0013_prohibited': True,
             'work_root': str(c.work_root), 'working_directory': str(c.working_directory),
             'evidence_root': str(c.evidence_root), 'stage_root': str(c.stage_root),
             'durable_root': str(c.durable_root), 'release_root': str(c.release_root),
             'codex_path': c.codex_path, 'prompt_sha256': sha(c.prompt.encode()),
             'execution_mode': c.supervisor.mode}
    facts['timeout_policy']=c.supervisor.timeout_policy()
    if c._test_only:
        require(c.supervisor.mode == 'NONPRODUCTION_TEST' and c.supervisor._allow_test,
                'NONPRODUCTION_CONTEXT_CANNOT_PROMOTE')
        require(phase == 'STATIC', 'NONPRODUCTION_CONTEXT_HAS_NO_OWNER_AUTHORITY')
        import owner_authorization as owner
        facts.update(frame_path=str(c.frame),frame_length=c.frame.stat().st_size,
                     frame_file_identity=owner.model_b_frame_identity(c.frame))
    else:
        from .proof_path_v1 import BoundProofPath
        from .policy_b_proof_v1 import PolicyBProofPath
        from .release_v1 import verify_release
        import owner_authorization as owner
        cfg = c.composition.configuration()
        module = sys.modules[type(c.composition).__module__]
        require(type(c.composition) is module.DisabledComposition
                and Path(module.__file__).resolve() == (c.release_root / 'composition.py').resolve()
                and c.composition.supervisor is c.supervisor and c.supervisor.mode == 'REAL'
                and c.proof_path.supervisor is c.supervisor and type(c.proof_path) in (BoundProofPath,PolicyBProofPath)
                and c.proof_path.validator is c.composition.validator
                and c.proof_path.checkpoint_attestor is c.composition.attestor,
                'UNTRUSTED_EXECUTOR_COMPONENT_BINDING')
        require(sha(canonical(cfg)) == c.composition.identity
                and canonical(cfg) == c.composition._config_bytes, 'EXECUTOR_CONFIGURATION_DRIFT')
        require(sha(safe_read(Path(module.__file__))) == cfg['composition_source_sha256'], 'EXECUTOR_COMPOSITION_DRIFT')
        selected = cfg['selected_source_sha256']
        require(selected['real_candidate/executor_v1.py'] == facts['executor_source_sha256']
                and selected['real_candidate/capture_v1.py'] == facts['capture_source_sha256'], 'EXECUTOR_SOURCE_BINDING_DRIFT')
        operational = cfg['operational_context']
        require({key: operational[key] for key in ('work_root', 'stage_root', 'durable_root', 'failure_root')} ==
                {'work_root': str(c.work_root), 'stage_root': str(c.stage_root),
                 'durable_root': str(c.durable_root), 'failure_root': str(c.evidence_root)}
                and operational['writing_uid'] == operational['writing_euid'] == 501
                and operational['max_output_bytes'] == MAX_CAPTURE_BYTES
                and operational['max_new_units'] == 1 and operational['attempt_ordinal'] == count+1
                and operational['u0013_prohibited'] is True, 'EXECUTOR_ROOT_BINDING_DRIFT')
        require(os.getuid() == os.geteuid() == operational['writing_uid'], 'EXECUTOR_WRITING_PRINCIPAL_DRIFT')
        require(cfg['capture_configuration_sha256'] == c.supervisor.config_sha256
                and cfg['timeout_policy']==c.supervisor.timeout_policy()
                and cfg['real_activation'] == 'HARD_DISABLED' and cfg['unit_id'] == 'U0012'
                and cfg['max_new_units'] == 1 and frame_sha == c.binding.unit_input_sha256,
                'EXECUTOR_EXACT_RUNTIME_BINDING_DRIFT')
        require(verify_release(c.release_root) == cfg['release_sha256'] == c.proof_path.release_identity,
                'EXECUTOR_RELEASE_DRIFT')
        command = (c.codex_path, 'exec', '--ephemeral', '--ignore-user-config', '--ignore-rules',
                   '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '-C', str(c.working_directory), c.prompt)
        require((str(c.supervisor.executable), *c.supervisor.argv) == command, 'EXECUTOR_COMMAND_DRIFT')
        require(c.binding.unit_id == 'U0012' and c.binding.max_new_units == 1
                and c.binding.execution_mode == 'REAL', 'EXECUTOR_UNIT_BINDING_DRIFT')
        require(c.transaction.case['first_unfinished_unit'] == 'U0012'
                and c.transaction.case['max_new_units'] == 1
                and len(c.transaction._historical_attempts)==count, 'EXECUTOR_TRANSACTION_DRIFT')
        facts.update(configuration_identity=c.composition.identity,
                     composition_source_sha256=cfg['composition_source_sha256'],
                     release_sha256=cfg['release_sha256'], binding_sha256=sha(canonical(dataclasses.asdict(c.binding))),
                     transaction_case_sha256=sha(canonical(c.transaction.case)))
        if phase == 'EXECUTING':
            c.composition.verify_runtime_sources()
            doc = owner.verify_real_consumption_context(c.transaction)
            bound = c.transaction._real_owner_context
            require(bound[3] is c.proof_path and bound[4] is c.binding and Path(bound[5]) == c.frame
                    and Path(bound[6]) == c.release_root
                    and bound[2] is c.transaction._bound_adapter
                    and bound[2].execution_context is c
                    and doc['target_authorization']['deployment_identity'] == c.composition.identity,
                    'OWNER_EXECUTOR_CONTEXT_DRIFT')
    facts['context_identity'] = sha(canonical(facts))
    if c._original_facts is not None:
        require(canonical(facts) == canonical(c._original_facts), 'SEALED_EXECUTOR_CONTEXT_DRIFT')
    return facts


def _resource_preflight(message, context):
    budget = 6 * context.storage_contract()['capture_bytes']
    value = _frozen().parse_json_agent_message(message)
    # Resource-only envelope: the accepted validator remains the sole semantic
    # authority. Two copies bound raw/validated row serialization downstream.
    rows = value.get('rows', value) if type(value) is dict else value
    _serialization_size({'raw_rows': rows, 'validated_rows': rows}, budget)


def persist_executor_attempt(*, execution_context, command, start_timestamp_utc, end_timestamp_utc,
                             stdout, stderr, return_code, termination_state, timeout_status,
                             context_id, final_message, failure_status, provider_context_id=None,
                             capture_complete=True, timing_receipt=None):
    """Same frozen artifact names/schema, bounded exclusive fsync/readback."""
    c = execution_context
    verify_runtime_context(c)
    budget = c.storage_contract()
    require(type(timing_receipt) is dict and
            timing_receipt.get('schema')=='CAPTURE_PHASE_TIMING_OPTION_B_V1',
            'EXECUTOR_PHASE_TIMING_REQUIRED')
    require(type(stdout) is bytes and type(stderr) is bytes
            and len(stdout) + len(stderr) <= budget['capture_bytes'], 'RAW_EVIDENCE_LIMIT_EXCEEDED')
    c._structural_event_evidence = structural_event_evidence(stdout)
    final_encoding_error = False
    try:
        final = b'' if final_message is None else final_message.encode('utf-8')
    except UnicodeEncodeError:
        # Preserve the exact raw JSON event bytes rather than fabricate a
        # repaired scientific message. Missing final text can never be accepted.
        final, final_message, final_encoding_error = b'', None, True
        failure_status = failure_status or 'FINAL_MESSAGE_UTF8_ENCODING_FAILURE'
    require(len(final) <= budget['capture_bytes'], 'FINAL_MESSAGE_LIMIT_EXCEEDED')
    root = c.evidence_root
    require(not root.is_symlink(), 'EXECUTOR_EVIDENCE_REPLAY')
    if root.exists():
        require(c._persistence_started and c._start_bytes is not None
                and safe_read(root / 'primary_executor_process_start.json') == c._start_bytes,
                'EXECUTOR_EVIDENCE_REPLAY')
    else:
        root.mkdir(parents=True, exist_ok=False, mode=0o700)
    paths = {'raw_stdout': root / 'primary_executor_raw_stdout.jsonl',
             'raw_stderr': root / 'primary_executor_raw_stderr.txt',
             'final_message': root / 'primary_executor_attempt_final_message.txt'}
    artifacts = (('raw_stdout', stdout), ('raw_stderr', stderr), ('final_message', final))
    hashes = {name: sha(raw) for name, raw in artifacts}
    manifest = {'role': 'PRIMARY', 'backend': 'codex_ephemeral', 'command': command,
                'working_directory': str(c.working_directory), 'start_timestamp_utc': start_timestamp_utc,
                'end_timestamp_utc': end_timestamp_utc, 'process_return_code': return_code,
                'process_termination_state': termination_state, 'timeout_status': timeout_status,
                'execution_context_identity': context_id,
                'provider_execution_context_identity': provider_context_id,
                'final_agent_message_present': final_message is not None, 'failure_status': failure_status,
                'final_message_encoding_error': final_encoding_error,
                'capture_complete': capture_complete, 'prospective_context': c._original_facts,
                'phase_timing': timing_receipt,
                'structural_event_evidence': c._structural_event_evidence,
                'artifacts': {name: {'path': str(paths[name]), 'sha256': hashes[name]} for name in paths}}
    if failure_status is not None:
        manifest.update(first_rejection_fields(c))
    raw = _bounded_json(manifest, budget['artifact_bytes'])
    _ensure_capacity(root, len(stdout) + len(stderr) + len(final) + len(raw) + budget['timing_receipt_bytes'])
    for name, contents in artifacts:
        require(_write_exclusive(paths[name], contents, budget['capture_bytes']) == hashes[name],
                'EXECUTOR_EVIDENCE_HASH_DRIFT')
    path = root / 'primary_executor_attempt_manifest.json'
    hashes['manifest'] = _write_exclusive(path, raw, budget['artifact_bytes'])
    paths['manifest'] = path
    # This timestamp covers completed raw/final/manifest fsync and readback.
    # The tail receipt's own persistence is intentionally outside that scope.
    complete=dict(timing_receipt)
    complete['evidence_persistence_complete_ns']=time.monotonic_ns()
    complete['persistence_completion_scope']='RAW_FINAL_AND_ATTEMPT_MANIFEST__TAIL_RECEIPT_EXCLUDED'
    paths['phase_timing']=root/'primary_executor_phase_timing.json'
    hashes['phase_timing']=_write_exclusive(paths['phase_timing'],
        _bounded_json(complete,budget['timing_receipt_bytes']),budget['timing_receipt_bytes'])
    return {'paths': paths, 'hashes': hashes, 'manifest': manifest}


def _prepare_process_receipt(context, command, began):
    c = context
    budget = c.storage_contract()
    # The prospective adapter has already materialized the exact input I. Its
    # pre-materialization guard reserves the complete envelope; current free
    # bytes here must cover only the remaining, not already allocated, files.
    _ensure_capacity(c.evidence_root,
        budget['peak_storage_bytes'] - budget['input_materialization_bytes'])
    require(not c.evidence_root.exists() and not c.evidence_root.is_symlink(), 'EXECUTOR_EVIDENCE_REPLAY')
    raw = _bounded_json({'schema': 'PROSPECTIVE_EXECUTOR_START_V1', 'status': 'NOT_COMPLETED',
        'command': command, 'started_utc': began, 'context': c._original_facts,
        'capture_limit_bytes': budget['capture_bytes'], 'real_authority': False}, budget['receipt_bytes'])
    c.evidence_root.mkdir(parents=True, exist_ok=False, mode=0o700)
    _write_exclusive(c.evidence_root / 'primary_executor_process_start.json', raw, budget['receipt_bytes'])
    c._start_bytes = raw
    c._persistence_started = True


def _failure_receipt(context, error):
    c = context
    budget = c.storage_contract()
    raw = _bounded_json({'schema': 'PROSPECTIVE_EXECUTOR_CONTROLLED_STOP_V1',
        'failure_type': type(error).__name__, 'complete': False, 'automatic_retry': False,
        'failure_classification':'EVIDENCE_PERSISTENCE_FAILURE',
        'unit_id': 'U0012', 'attempt_ordinal': c._original_facts['next_attempt_sequence'],
        'context_identity': c._original_facts['context_identity'],
        'phase_timing':c.supervisor.timing_receipt(),
        'evidence_persistence_failure_ns':time.monotonic_ns(),
        'structural_event_evidence': getattr(c, '_structural_event_evidence',
                                            {'status': 'FIELD_NOT_AVAILABLE'}),
        **first_rejection_fields(c)},
        budget['receipt_bytes'])
    if not c.evidence_root.exists():
        c.evidence_root.mkdir(parents=True, exist_ok=False, mode=0o700)
    _write_exclusive(c.evidence_root / 'primary_executor_controlled_stop.json', raw, budget['receipt_bytes'])


def run_codex_executor(*, working_directory, prompt, codex_path, evidence_root=None, role='PRIMARY',
                       execution_context=None):
    """Frozen call shape, one existing bounded collector, no automatic retry."""
    c = execution_context
    require(type(c) is ExecutionContext and type(c.supervisor) is ControlledLocalCapture,
            'EXACT_EXECUTION_CONTEXT_REQUIRED')
    c.supervisor.begin_prelaunch()
    verify_runtime_context(c, working_directory=working_directory, prompt=prompt,
                           codex_path=codex_path, evidence_root=evidence_root, role=role)
    if c.supervisor.mode == 'REAL':
        from .activation_v1 import production_activation
        production_activation(c.transaction,phase='EXECUTING')
        verify_runtime_context(c,phase='EXECUTING')
    require(evidence_root is not None and not c._used, 'EXECUTOR_SINGLE_USE_OR_EVIDENCE_REQUIRED')
    c._used = True
    frozen = _frozen()
    began = frozen.executor_now_utc()
    obs = None
    message = provider = failure = None
    termination, return_code, timeout = 'UNKNOWN', None, False
    stdout = stderr = b''
    command = [str(c.supervisor.executable), *c.supervisor.argv]
    try:
        _prepare_process_receipt(c, command, began)
        # Context/authority rejection still precedes any evidence writes. A
        # valid context whose budget expired retains the existing failure trail.
        c.supervisor.check_prelaunch()
        if c.supervisor.mode == 'REAL':
            verify_runtime_context(c, phase='EXECUTING')
            obs = c.supervisor.observe_real(input_file=c.frame, pinned_input_sha256=sha(safe_read(c.frame)),
                                            timeout_seconds=c.supervisor.child_capture_budget_seconds,
                                            execution_context=c)
        else:
            obs = c.supervisor.observe(input_file=c.frame, pinned_input_sha256=sha(safe_read(c.frame)),
                                       timeout_seconds=c.supervisor.child_capture_budget_seconds, test_only=True)
        stdout, stderr = obs.stdout, obs.stderr
        termination, return_code, timeout = obs.termination, obs.exit_code, obs.timeout
        if obs.capture_complete and not obs.truncated and obs.cleanup_complete:
            try:
                parsed = frozen.parse_codex_json_events(stdout.decode('utf-8', errors='strict'))
                provider, message = parsed['context_id'], parsed['agent_message']
            except (frozen.ControlledStop, UnicodeDecodeError):
                if return_code == 0 and not timeout:
                    raise
        if obs.timeout:
            failure = 'SEMANTIC_EXECUTOR_TIMEOUT'
        elif obs.limit_exceeded or obs.truncated:
            failure = 'SEMANTIC_EXECUTOR_OUTPUT_LIMIT_EXCEEDED'
        elif obs.execution_exception:
            failure = 'SEMANTIC_EXECUTOR_START_FAILURE'
        elif return_code != 0:
            failure = 'SEMANTIC_EXECUTOR_NONZERO_RETURN'
        c.supervisor.verify(obs, input_file=c.frame, pinned_input_sha256=obs.actual_input_sha256)
        require(message is not None, 'SEMANTIC_EXECUTOR_FINAL_MESSAGE_MISSING')
        _resource_preflight(message, c)
        if not c._test_only:
            stage, proof, receipt = c.proof_path.issue(capture=obs, input_path=c.frame,
                input_sha256=c.binding.unit_input_sha256, stage_root=c.stage_root,
                binding=c.binding, checkpoint=c.proof_path.checkpoint_attestor._last)
            budget = c.storage_contract()
            c.durable_root.mkdir(parents=True, exist_ok=False, mode=0o700)
            _write_exclusive(c.durable_root / 'validated_receipt.json',
                _bounded_json({'validated_output_sha256': receipt.validated_output_sha256,
                               'validator_sha256': receipt.validator_sha256,
                               'stage_sha256': stage.staged_bytes_sha256}, budget['artifact_bytes']), budget['artifact_bytes'])
            _write_exclusive(c.durable_root / 'operational_proof.json',
                _bounded_json({'claims': proof.claims, 'proof_sha256': proof.proof_sha256}, budget['artifact_bytes']), budget['artifact_bytes'])
            c.transaction.submit_v7_evidence(obs, stage, proof, receipt)
        return {'backend': 'codex_ephemeral', 'context_id': obs.invocation_id,
                'provider_context_id': provider, 'agent_message': message,
                'stdout': stdout.decode('utf-8'), 'stderr': stderr.decode('utf-8'),
                'command': command, 'working_directory': str(c.working_directory),
                'process_started': True, 'return_code': return_code, 'termination_state': termination,
                'timeout_status': timeout, 'start_timestamp_utc': began}
    except Exception as exc:
        remember_first_rejection(c, exc if failure is None else None)
        if failure is None:
            failure = type(exc).__name__
        if obs is None:
            termination = 'ERROR'
            timing=c.supervisor.timing_receipt()
            if timing.get('child_pid') is not None:
                return_code=timing.get('cleanup_return_code')
        raise
    finally:
        try:
            persist_executor_attempt(execution_context=c, command=command, start_timestamp_utc=began,
                end_timestamp_utc=frozen.executor_now_utc(), stdout=stdout, stderr=stderr,
                return_code=return_code, termination_state=termination, timeout_status=timeout,
                context_id=None if obs is None else obs.invocation_id, final_message=message,
                failure_status=failure, provider_context_id=provider,
                capture_complete=obs is not None and obs.capture_complete and not obs.truncated,
                timing_receipt=c.supervisor.timing_receipt())
        except Exception as evidence_error:
            remember_first_rejection(c, evidence_error)
            try:
                _failure_receipt(c, evidence_error)
            except Exception as fallback_error:
                raise StageStop('EXECUTOR_EVIDENCE_PRESERVATION_INCOMPLETE') from fallback_error
            raise StageStop('EXECUTOR_EVIDENCE_PERSISTENCE_FAILED__NO_ACCEPTANCE') from evidence_error
