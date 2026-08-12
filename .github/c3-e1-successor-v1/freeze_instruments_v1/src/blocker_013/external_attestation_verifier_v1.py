from __future__ import annotations
import fcntl
import hashlib
import os
import secrets
import ssl
import socket
import struct
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from identity_io_v1 import canonical_bytes, canonical_loads, canonical_sha256, read_json, validate_schema_file, require_file_identity, assert_resolved, durable_write
from measured_boot_replay_v1 import parse_event_log, replay as boot_replay
from ima_replay_v1 import parse_native_binary_measurements, replay_records
from ak_provenance_v1 import verify_binding, verify_ek_certificate

class VerificationError(RuntimeError):
    pass

_LEN = struct.Struct('>Q')
PRE = b'C3_E1_QUOTE_QUALIFICATION_V1\0'
POST = b'C3_E1_POST_OBSERVATION_CHECKPOINT_ATTESTATION_V1\0'
_REGISTRY_VERSION = 1
_CHALLENGE_STATES = {'ISSUED', 'CONSUMED', 'EXPIRED'}


def _recv_exact(sock, n):
    out = bytearray()
    while len(out) < n:
        b = sock.recv(n - len(out))
        if not b:
            raise VerificationError('TLS transaction truncated')
        out.extend(b)
    return bytes(out)


def recv_object(sock, max_bytes):
    n = _LEN.unpack(_recv_exact(sock, _LEN.size))[0]
    if n <= 0 or n > max_bytes:
        raise VerificationError('TLS transaction size invalid')
    return canonical_loads(_recv_exact(sock, n))


def send_object(sock, obj):
    raw = canonical_bytes(obj)
    sock.sendall(_LEN.pack(len(raw)) + raw)


def run_checkquote(tool, args):
    if not isinstance(tool, str) or not tool.startswith('/'):
        raise VerificationError('absolute checkquote path required')
    cp = subprocess.run([tool, *args], shell=False, capture_output=True)
    if cp.returncode:
        raise VerificationError(f'quote signature/PCR verification failed: exit={cp.returncode}')
    return {'stdout_sha256': hashlib.sha256(cp.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(cp.stderr).hexdigest()}


def decode_objects(bundle):
    objects = {}
    for role, meta in bundle['objects'].items():
        if meta['role'] != role:
            raise VerificationError(f'object role binding mismatch: {role}')
        try:
            raw = bytes.fromhex(meta['data_hex'])
        except ValueError as exc:
            raise VerificationError(f'object hex invalid: {role}') from exc
        if len(raw) != meta['byte_count'] or hashlib.sha256(raw).hexdigest() != meta['sha256']:
            raise VerificationError(f'object identity mismatch: {role}')
        objects[role] = raw
    return objects


def bind_exact_object_set(bundle, objects):
    if set(bundle['objects']) != set(objects):
        raise VerificationError('attestation object set mismatch')
    for role, raw in objects.items():
        meta = bundle['objects'][role]
        if len(raw) != meta['byte_count'] or hashlib.sha256(raw).hexdigest() != meta['sha256']:
            raise VerificationError(f'object identity mismatch {role}')
    return True


def validate_quote_pcrs(quoted, expected):
    if quoted != expected:
        raise VerificationError('PCR mismatch')
    return 'PASS'


def compare_host_tcb(observed, expected):
    if not isinstance(observed, dict) or not isinstance(expected, dict) or set(observed) != set(expected):
        raise VerificationError('host TCB member-set mismatch')
    for role, value in expected.items():
        if not isinstance(role, str) or not role or not isinstance(value, str) or len(value) != 64 or value.lower() != value:
            raise VerificationError('expected host TCB identity malformed')
        if observed.get(role) != value:
            raise VerificationError(f'host TCB mismatch: {role}')
    return 'PASS'


def canonical_result(transaction_type, bundle, classification, checks, checkpoint_sha256=None):
    obj = {
        'transaction_type': transaction_type,
        'runtime_instance_uuid': bundle['runtime_instance_uuid'],
        'observation_nonce': bundle['observation_nonce'],
        'verifier_manifest_sha256': bundle['verifier_manifest_sha256'],
        'runtime_instantiation_attestation_record_sha256': bundle['runtime_instantiation_attestation_record_sha256'],
        'attestation_bundle_sha256': canonical_sha256(bundle),
        'classification': classification,
        'checks': checks,
    }
    if checkpoint_sha256 is not None:
        obj['final_checkpoint_sha256'] = checkpoint_sha256
    return obj, canonical_sha256(obj)


def _manifest(cfg, role):
    bindings = cfg.get('expected_manifest_bindings')
    if not isinstance(bindings, dict) or role not in bindings:
        raise VerificationError(f'verifier-side manifest binding missing: {role}')
    spec = bindings[role]
    if set(spec) not in ({'path', 'sha256'}, {'path', 'sha256', 'byte_count'}):
        raise VerificationError(f'verifier-side manifest binding fields: {role}')
    try:
        assert_resolved(spec, f'verifier-side {role} manifest')
    except Exception as e:
        raise VerificationError(str(e)) from e
    require_file_identity(spec['path'], spec['sha256'], spec.get('byte_count'))
    obj = read_json(spec['path'])
    if obj.get('manifest_role') != role:
        raise VerificationError(f'verifier-side manifest role mismatch: {role}')
    return obj


def load_verifier_expectations(cfg):
    roles = ('pcr_policy', 'ima_policy', 'host_tcb_manifest', 'ak_ek_policy', 'runtime_binding_policy')
    out = {role: _manifest(cfg, role) for role in roles}
    manifest_hashes = {role: cfg['expected_manifest_bindings'][role]['sha256'] for role in roles}
    expected_verifier_manifest = hashlib.sha256(canonical_bytes(manifest_hashes)).hexdigest()
    if cfg['verifier_manifest_sha256'] != expected_verifier_manifest:
        raise VerificationError('verifier manifest identity does not bind admitted expectation manifests')
    out['verifier_manifest_sha256'] = expected_verifier_manifest
    return out


def _pre_quote_qualification(bundle):
    return hashlib.sha256(
        PRE
        + uuid.UUID(bundle['runtime_instance_uuid']).bytes
        + bytes.fromhex(bundle['observation_nonce'])
        + bytes.fromhex(bundle['runtime_instantiation_attestation_record_sha256'])
        + bytes.fromhex(bundle['verifier_manifest_sha256'])
    ).hexdigest()


def _post_quote_qualification(bundle, checkpoint):
    return hashlib.sha256(
        POST
        + uuid.UUID(bundle['runtime_instance_uuid']).bytes
        + bytes.fromhex(bundle['observation_nonce'])
        + bytes.fromhex(bundle['fresh_challenge'])
        + checkpoint['final_host_sequence'].to_bytes(8, 'big')
        + bytes.fromhex(checkpoint['final_record_sha256'])
        + bytes.fromhex(bundle['final_checkpoint_sha256'])
        + checkpoint['observation_start_host_sequence'].to_bytes(8, 'big')
        + checkpoint['observation_end_host_sequence'].to_bytes(8, 'big')
        + bytes.fromhex(bundle['runtime_instantiation_attestation_record_sha256'])
        + bytes.fromhex(bundle['verifier_manifest_sha256'])
    ).hexdigest()


def _runtime_record_check(bundle, objects, cfg, policy):
    if policy.get('manifest_role') != 'runtime_binding_policy':
        raise VerificationError('runtime binding policy identity')
    allowed = policy.get('allowed_transaction_types')
    if not isinstance(allowed, list) or bundle['transaction_type'] not in allowed:
        raise VerificationError('transaction type not admitted by verifier-side runtime policy')
    raw = objects.get('runtime_instantiation_record')
    if not isinstance(raw, bytes):
        raise VerificationError('observed runtime instantiation record required')
    record = canonical_loads(raw)
    validate_schema_file(record, cfg['freeze_record_schema_path'])
    if canonical_sha256(record) != bundle['runtime_instantiation_attestation_record_sha256']:
        raise VerificationError('runtime instantiation record object hash mismatch')
    if record['runtime_instance_uuid'] != bundle['runtime_instance_uuid'] or record['observation_nonce'] != bundle['observation_nonce']:
        raise VerificationError('runtime instantiation record runtime binding mismatch')
    expected = policy.get('expected_runtime_record_fields')
    if not isinstance(expected, dict) or not expected:
        raise VerificationError('verifier-side expected runtime record fields required')
    for key, value in expected.items():
        if key not in record or record[key] != value:
            raise VerificationError(f'verifier-side runtime record mismatch: {key}')
    return record


def checkquote_from_objects(cfg, bundle, objects, expected_qualification):
    if bundle['quote_qualification'] != expected_qualification:
        raise VerificationError('quote qualification mismatch')
    tool = cfg.get('tpm2_checkquote_path')
    if str(tool).startswith('UNRESOLVED'):
        raise VerificationError('tpm2_checkquote identity unresolved')
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for role in ('ak_tpmt_public', 'quote_message', 'quote_signature', 'quoted_pcr_bytes'):
            path = Path(td) / role
            path.write_bytes(objects[role])
            paths[role] = str(path)
        args = ['-u', paths['ak_tpmt_public'], '-m', paths['quote_message'], '-s', paths['quote_signature'], '-f', paths['quoted_pcr_bytes'], '-g', 'sha256', '-q', bundle['quote_qualification']]
        return run_checkquote(tool, args)


def verify_pre_e1(bundle, objects, cfg, expectations):
    validate_schema_file(bundle, cfg['attestation_schema_path'])
    bind_exact_object_set(bundle, objects)
    _runtime_record_check(bundle, objects, cfg, expectations['runtime_binding_policy'])
    if bundle['verifier_manifest_sha256'] != expectations['verifier_manifest_sha256']:
        raise VerificationError('verifier manifest binding mismatch')
    pcr = expectations['pcr_policy']
    ima_policy = expectations['ima_policy']
    host_policy = expectations['host_tcb_manifest']
    ak_policy = expectations['ak_ek_policy']
    enrollment = canonical_loads(objects['ak_enrollment_record'])
    ak = verify_binding(enrollment, ak_policy.get('ak_expected_fields', {}), tpmt_public_bytes=objects['ak_tpmt_public'], parent_qualified_name_hex=ak_policy.get('ak_parent_qualified_name'))
    if 'ek_certificate' in objects:
        if str(cfg.get('openssl_path', '')).startswith('UNRESOLVED') or str(cfg.get('ek_trust_store', '')).startswith('UNRESOLVED'):
            raise VerificationError('EK verification dependencies unresolved')
        with tempfile.NamedTemporaryFile() as cert:
            cert.write(objects['ek_certificate'])
            cert.flush()
            verify_ek_certificate(cfg['openssl_path'], cert.name, cfg['ek_trust_store'], ak_policy['ek_expected_pubkey_sha256'])
    bp = boot_replay(parse_event_log(objects['measured_boot_event_log'], pcr['measured_boot_format']), pcr['pcr_selection'])
    normalized_boot = {str(k): v.hex() for k, v in bp.items()}
    if normalized_boot != pcr['expected_boot_pcrs']:
        raise VerificationError('measured boot replay mismatch')
    ima = replay_records(parse_native_binary_measurements(objects['ima_binary_measurements'], ima_policy['ima_format_descriptor']), 10, ima_policy['ima_pcr_algorithm']).hex()
    if ima != ima_policy['expected_ima_pcr10']:
        raise VerificationError('IMA replay mismatch')
    if hashlib.sha256(objects['quoted_pcr_bytes']).hexdigest() != pcr['quoted_pcr_bytes_sha256']:
        raise VerificationError('quoted PCR bytes identity mismatch')
    checkquote_from_objects(cfg, bundle, objects, _pre_quote_qualification(bundle))
    observed_tcb = canonical_loads(objects['host_tcb_observation'])
    checks = {'ak_provenance': ak, 'measured_boot_replay': 'PASS', 'ima_replay': 'PASS', 'quote': 'PASS', 'host_tcb': compare_host_tcb(observed_tcb, host_policy['members'])}
    return canonical_result('PRE_E1_RESULT', bundle, 'PASS', checks)


def _challenge_registry_parameters(cfg):
    path = Path(cfg.get('challenge_registry_path', ''))
    ttl = cfg.get('challenge_ttl_seconds')
    if not path.is_absolute():
        raise VerificationError('absolute verifier challenge registry path required')
    if not isinstance(ttl, int) or isinstance(ttl, bool) or ttl <= 0:
        raise VerificationError('positive verifier challenge TTL required')
    return path, ttl


def _validate_registry(registry):
    if not isinstance(registry, dict) or set(registry) != {'registry_version', 'challenges'} or registry['registry_version'] != _REGISTRY_VERSION or not isinstance(registry['challenges'], dict):
        raise VerificationError('verifier challenge registry structure invalid')
    required = {
        'transaction_id', 'runtime_instance_uuid', 'observation_nonce', 'final_checkpoint_sha256',
        'verifier_manifest_sha256', 'fresh_challenge', 'issued_at_unix_ns', 'expires_at_unix_ns',
        'single_use_state', 'consumed_at_unix_ns'
    }
    for transaction_id, entry in registry['challenges'].items():
        if not isinstance(entry, dict) or set(entry) != required or entry.get('transaction_id') != transaction_id:
            raise VerificationError('verifier challenge registry entry invalid')
        if entry['single_use_state'] not in _CHALLENGE_STATES:
            raise VerificationError('verifier challenge state invalid')
    return registry


def _load_registry(path):
    if not path.exists():
        return {'registry_version': _REGISTRY_VERSION, 'challenges': {}}
    try:
        return _validate_registry(canonical_loads(path.read_bytes()))
    except Exception as exc:
        if isinstance(exc, VerificationError):
            raise
        raise VerificationError('verifier challenge registry unreadable') from exc


def _registry_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path) + '.lock', os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def _registry_unlock(fd):
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _store_registry(path, registry):
    _validate_registry(registry)
    durable_write(path, canonical_bytes(registry), 0o600)


def make_post_challenge(runtime_uuid, nonce, checkpoint_sha, verifier_sha, transaction_id=None, fresh_challenge=None):
    return {
        'transaction_type': 'POST_OBSERVATION_CHALLENGE',
        'transaction_id': transaction_id or secrets.token_hex(16),
        'runtime_instance_uuid': runtime_uuid,
        'observation_nonce': nonce,
        'final_checkpoint_sha256': checkpoint_sha,
        'verifier_manifest_sha256': verifier_sha,
        'fresh_challenge': fresh_challenge or secrets.token_hex(32),
    }


def issue_post_challenge(request, cfg, now_ns=None):
    path, ttl = _challenge_registry_parameters(cfg)
    now = time.time_ns() if now_ns is None else now_ns
    if not isinstance(now, int) or now < 0:
        raise VerificationError('challenge issuance time invalid')
    if request['verifier_manifest_sha256'] != cfg['verifier_manifest_sha256']:
        raise VerificationError('challenge request verifier manifest mismatch')
    fd = _registry_lock(path)
    try:
        registry = _load_registry(path)
        for _ in range(32):
            challenge = make_post_challenge(request['runtime_instance_uuid'], request['observation_nonce'], request['final_checkpoint_sha256'], request['verifier_manifest_sha256'])
            if challenge['transaction_id'] not in registry['challenges']:
                break
        else:
            raise VerificationError('verifier challenge transaction-id allocation failed')
        entry = {
            'transaction_id': challenge['transaction_id'],
            'runtime_instance_uuid': challenge['runtime_instance_uuid'],
            'observation_nonce': challenge['observation_nonce'],
            'final_checkpoint_sha256': challenge['final_checkpoint_sha256'],
            'verifier_manifest_sha256': challenge['verifier_manifest_sha256'],
            'fresh_challenge': challenge['fresh_challenge'],
            'issued_at_unix_ns': now,
            'expires_at_unix_ns': now + ttl * 1_000_000_000,
            'single_use_state': 'ISSUED',
            'consumed_at_unix_ns': 0,
        }
        registry['challenges'][challenge['transaction_id']] = entry
        _store_registry(path, registry)
        return challenge
    finally:
        _registry_unlock(fd)


def consume_post_challenge(bundle, cfg, now_ns=None):
    path, _ = _challenge_registry_parameters(cfg)
    now = time.time_ns() if now_ns is None else now_ns
    fd = _registry_lock(path)
    try:
        registry = _load_registry(path)
        entry = registry['challenges'].get(bundle['transaction_id'])
        if entry is None:
            raise VerificationError('unknown verifier-issued challenge transaction_id')
        if entry['verifier_manifest_sha256'] != cfg['verifier_manifest_sha256']:
            raise VerificationError('challenge was not issued under exact admitted verifier manifest')
        expected = {
            'runtime_instance_uuid': bundle['runtime_instance_uuid'],
            'observation_nonce': bundle['observation_nonce'],
            'final_checkpoint_sha256': bundle['final_checkpoint_sha256'],
            'verifier_manifest_sha256': bundle['verifier_manifest_sha256'],
            'fresh_challenge': bundle['fresh_challenge'],
        }
        for key, value in expected.items():
            if entry[key] != value:
                raise VerificationError(f'verifier-issued challenge binding mismatch: {key}')
        if entry['single_use_state'] != 'ISSUED':
            raise VerificationError(f'verifier-issued challenge already consumed or inactive: {entry["single_use_state"]}')
        if now > entry['expires_at_unix_ns']:
            entry['single_use_state'] = 'EXPIRED'
            entry['consumed_at_unix_ns'] = now
            _store_registry(path, registry)
            raise VerificationError('verifier-issued challenge expired')
        # Consume before accepting quote/PCR evidence. A failed first attestation attempt cannot reuse the challenge.
        entry['single_use_state'] = 'CONSUMED'
        entry['consumed_at_unix_ns'] = now
        _store_registry(path, registry)
        return 'PASS'
    finally:
        _registry_unlock(fd)


def _bind_checkpoint_to_post_bundle(bundle, checkpoint):
    if checkpoint.get('runtime_instance_uuid') != bundle['runtime_instance_uuid']:
        raise VerificationError('FAIL_ENVIRONMENT_IDENTITY_MISMATCH: final checkpoint runtime_instance_uuid mismatch')
    if checkpoint.get('observation_nonce') != bundle['observation_nonce']:
        raise VerificationError('FAIL_EVIDENCE_INTEGRITY: final checkpoint observation_nonce mismatch')
    return 'PASS'


def evaluate_post_pcr_policy(policy, objects):
    post = policy.get('post_observation') if isinstance(policy, dict) else None
    if post is None:
        return 'INCONCLUSIVE'
    if not isinstance(post, dict):
        raise VerificationError('post-observation PCR policy malformed')
    mode = post.get('evaluation_mode')
    if mode != 'QUOTED_PCR_BYTES_SHA256_ALLOWLIST':
        return 'INCONCLUSIVE'
    allowed = post.get('acceptable_quoted_pcr_bytes_sha256')
    if not isinstance(allowed, list) or not allowed:
        return 'INCONCLUSIVE'
    normalized = []
    for value in allowed:
        if not isinstance(value, str) or len(value) != 64 or value.lower() != value:
            raise VerificationError('post-observation PCR policy digest malformed')
        try:
            bytes.fromhex(value)
        except ValueError as exc:
            raise VerificationError('post-observation PCR policy digest malformed') from exc
        normalized.append(value)
    observed = hashlib.sha256(objects['quoted_pcr_bytes']).hexdigest()
    if observed not in normalized:
        raise VerificationError('post-observation PCR policy mismatch')
    return 'PASS'


def verify_post(bundle, objects, cfg, expectations):
    validate_schema_file(bundle, cfg['attestation_schema_path'])
    bind_exact_object_set(bundle, objects)
    _runtime_record_check(bundle, objects, cfg, expectations['runtime_binding_policy'])
    if bundle['verifier_manifest_sha256'] != expectations['verifier_manifest_sha256']:
        raise VerificationError('verifier manifest binding mismatch')
    if hashlib.sha256(objects['final_checkpoint']).hexdigest() != bundle['final_checkpoint_sha256']:
        raise VerificationError('final checkpoint object mismatch')
    checkpoint = canonical_loads(objects['final_checkpoint'])
    validate_schema_file(checkpoint, cfg['freeze_record_schema_path'])
    _bind_checkpoint_to_post_bundle(bundle, checkpoint)
    # Registry lookup proves origin, all challenge bindings, expiration, replay prohibition, and single use.
    consume_post_challenge(bundle, cfg)
    ak_policy = expectations['ak_ek_policy']
    enrollment = canonical_loads(objects['ak_enrollment_record'])
    verify_binding(enrollment, ak_policy.get('ak_expected_fields', {}), tpmt_public_bytes=objects['ak_tpmt_public'], parent_qualified_name_hex=ak_policy.get('ak_parent_qualified_name'))
    checkquote_from_objects(cfg, bundle, objects, _post_quote_qualification(bundle, checkpoint))
    pcr_status = evaluate_post_pcr_policy(expectations['pcr_policy'], objects)
    classification = 'PASS' if pcr_status == 'PASS' else 'INCONCLUSIVE'
    checks = {
        'challenge_freshness': 'PASS',
        'quote_signature': 'PASS',
        'qualification_binding': 'PASS',
        'pcr_selection': pcr_status,
        'ak_provenance': 'PASS',
    }
    return canonical_result('POST_OBSERVATION_RESULT', bundle, classification, checks, bundle['final_checkpoint_sha256'])


def handle_transaction(req, cfg):
    validate_schema_file(req, cfg['attestation_schema_path'])
    expectations = load_verifier_expectations(cfg)
    if req['verifier_manifest_sha256'] != expectations['verifier_manifest_sha256']:
        raise VerificationError('verifier manifest binding mismatch')
    if req['transaction_type'] == 'POST_OBSERVATION_CHALLENGE_REQUEST':
        challenge = issue_post_challenge(req, cfg)
        validate_schema_file(challenge, cfg['attestation_schema_path'])
        return challenge
    objects = decode_objects(req)
    if 'verification_context' in objects:
        raise VerificationError('host-supplied verifier expectations prohibited')
    if req['transaction_type'] == 'PRE_E1_ATTESTATION':
        result, _ = verify_pre_e1(req, objects, cfg, expectations)
    elif req['transaction_type'] == 'POST_OBSERVATION_ATTESTATION':
        result, _ = verify_post(req, objects, cfg, expectations)
    else:
        raise VerificationError('unsupported transaction type')
    validate_schema_file(result, cfg['attestation_schema_path'])
    return result


def main():
    cfg = read_json('/opt/c3-e1/freeze-instruments-v1/config/blocker_013/blocker_013_config_v1.json')
    for key in ('server_cert', 'server_key', 'client_ca', 'verifier_manifest_sha256'):
        if str(cfg.get(key, '')).startswith('UNRESOLVED'):
            raise VerificationError(f'future verifier identity unresolved {key}')
    _challenge_registry_parameters(cfg)
    load_verifier_expectations(cfg)
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=cfg['client_ca'])
    ctx.minimum_version = ssl.TLSVersion.TLSv1_3
    ctx.maximum_version = ssl.TLSVersion.TLSv1_3
    ctx.load_cert_chain(cfg['server_cert'], cfg['server_key'])
    ctx.verify_mode = ssl.CERT_REQUIRED
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((cfg['listen_host'], cfg['listen_port']))
    listener.listen(1)
    try:
        conn, _ = listener.accept()
        with ctx.wrap_socket(conn, server_side=True) as tls:
            request = recv_object(tls, cfg['max_transaction_bytes'])
            response = handle_transaction(request, cfg)
            send_object(tls, response)
    finally:
        listener.close()


if __name__ == '__main__':
    main()
