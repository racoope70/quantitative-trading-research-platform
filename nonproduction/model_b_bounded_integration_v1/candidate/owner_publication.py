"""Fixed, one-shot NONPRODUCTION publisher. No service, execution or signing API.

This file must be invoked by MAIN's reviewed, hash-pinned Owner terminal action.
Importing it never elevates privilege or publishes anything.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

PROTECTED_ROOT = Path('/private/var/db/qtrp-owner-auth-nonproduction-v1')
SCHEMA = 'QTRP_OWNER_PUBLICATION_NONPRODUCTION_V1'
SCOPE = 'INERT_U0012_ATTEMPT3_ONLY__REAL_EXECUTION_FORBIDDEN'
# Separate namespace prevents a consumed inert publication from becoming REAL
# authority. No directory or authorization is created merely by importing this.
REAL_PROTECTED_ROOT = Path('/private/var/db/qtrp-owner-auth-real-u0012-attempt10-v1')
REAL_SCHEMA = 'QTRP_OWNER_PUBLICATION_REAL_U0012_ATTEMPT10_V1'
REAL_SCOPE = 'BATCH0004_PRIMARY_S05_REAL_U0012_ATTEMPT10_ONE_SHOT'
REAL_ATTEMPT = 'BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
REAL_A11_PROTECTED_ROOT = Path('/private/var/db/qtrp-owner-auth-real-u0012-attempt11-v1')
REAL_A11_SCHEMA = 'QTRP_OWNER_PUBLICATION_REAL_U0012_ATTEMPT11_V1'
REAL_A11_SCOPE = 'BATCH0004_PRIMARY_S05_REAL_U0012_ATTEMPT11_ONE_SHOT'
REAL_A11_RUNTIME_ROOT = '/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a11_u0012_attempt11_runtime_v1'

class PublicationStop(RuntimeError):
    pass

def need(value, code):
    if not value:
        raise PublicationStop(code)

def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def completion_receipt(expected_sha256, expected_length, *, scope=SCOPE):
    need(scope in (SCOPE, REAL_SCOPE, REAL_A11_SCOPE), 'PUBLICATION_SCOPE_INVALID')
    return canonical({'schema': 'OWNER_PUBLICATION_COMPLETE_V1', 'sha256': expected_sha256,
                      'length': expected_length, 'scope': scope, 'real_activation': 'HARD_DISABLED'})

def write_all(fd, raw):
    remaining = memoryview(raw)
    while remaining:
        n = os.write(fd, remaining)
        need(n > 0, 'SHORT_PUBLICATION_WRITE')
        remaining = remaining[n:]
    os.fsync(fd)

def open_root_chain(path):
    """Capture descriptor-relative root-owned, nonwritable directory chain."""
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'UNTRUSTED_DIRECTORY_PATH')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open('/', flags)
    try:
        for component in path.parts[1:]:
            parent = os.fstat(fd)
            need(parent.st_uid == 0 and parent.st_gid == 0 and not parent.st_mode & 0o022,
                 'UNTRUSTED_DIRECTORY_ANCESTOR')
            next_fd = os.open(component, flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        st = os.fstat(fd)
        need(stat.S_ISDIR(st.st_mode) and st.st_uid == 0 and st.st_gid == 0
             and not st.st_mode & 0o022, 'UNTRUSTED_DIRECTORY')
        return fd
    except BaseException:
        os.close(fd)
        raise

def read_snapshot(fd, expected_length, expected_uid, expected_mode=None):
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_uid == expected_uid,
         'UNTRUSTED_FILE_TYPE_LINK_OR_OWNER')
    if expected_uid == 0:
        need(before.st_gid == 0, 'UNTRUSTED_PUBLICATION_GROUP')
    if expected_mode is not None:
        need(stat.S_IMODE(before.st_mode) == expected_mode, 'UNTRUSTED_FILE_PERMISSIONS')
    need(before.st_size == expected_length, 'PUBLICATION_LENGTH_MISMATCH')
    chunks = []
    remaining = expected_length + 1
    while remaining:
        part = os.read(fd, min(65536, remaining))
        if not part:
            break
        chunks.append(part)
        remaining -= len(part)
    raw = b''.join(chunks)
    after = os.fstat(fd)
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
         == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns),
         'PUBLICATION_CHANGED_DURING_READ')
    need(len(raw) == expected_length, 'PUBLICATION_INCOMPLETE')
    return raw

def validate_inert_document(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'DUPLICATE_JSON_FIELD')
            result[key] = value
        return result
    doc = json.loads(raw, object_pairs_hook=pairs)
    need(raw == canonical(doc), 'NONCANONICAL_PUBLICATION')
    need(set(doc) == {'schema', 'scope', 'consumer_uid', 'target_authorization', 'fixture_binding'},
         'PUBLICATION_SCHEMA')
    need(doc['schema'] == SCHEMA and doc['scope'] == SCOPE, 'NONPRODUCTION_SCOPE_REQUIRED')
    need(type(doc['consumer_uid']) is int and doc['consumer_uid'] == 501, 'WRONG_CONSUMER_UID')
    target = doc['target_authorization']
    need(target['environment'] == 'REAL' and target['unit_id'] == 'U0012'
         and type(target['next_attempt_sequence']) is int and target['next_attempt_sequence'] == 3
         and target['historical_attempt_count'] == 2 and type(target['max_new_units']) is int
         and target['max_new_units'] == 1 and target['u0013_prohibited'] is True
         and target['activation_gate'] == 'HARD_DISABLED' and target['dispatched'] is False
         and target['consumed'] is False, 'WRONG_REVIEW_TARGET_SCOPE')
    fixture = doc['fixture_binding']
    need(fixture['environment'] == 'SYNTHETIC_NONPRODUCTION' and fixture['unit_id'] == 'U0012'
         and fixture['next_attempt_sequence'] == 3 and fixture['historical_attempt_count'] == 2
         and type(fixture['max_new_units']) is int and fixture['max_new_units'] == 1 and fixture['u0013_prohibited'] is True
         and fixture['case']['real_execution_authorized'] is False,
         'INERT_FIXTURE_REQUIRED')
    return doc

def real_publication_contract(target):
    """Two explicit contexts; no increment, retry, or execution authority.

    Execution must select from independently derived facts, not submitted bytes.
    """
    need(type(target) is dict, 'REAL_ATTEMPT_CONTEXT_REQUIRED')
    number = target.get('next_attempt_sequence'); count = target.get('historical_attempt_count')
    need(type(number) is int and type(count) is int, 'REAL_ATTEMPT_CONTEXT_INVALID')
    if number == 10 and count == 9:
        return REAL_SCHEMA, REAL_SCOPE, REAL_PROTECTED_ROOT
    if number == 11 and count == 10:
        return REAL_A11_SCHEMA, REAL_A11_SCOPE, REAL_A11_PROTECTED_ROOT
    need(False, 'REAL_ATTEMPT_CONTEXT_INVALID')

def _validate_a11_document(doc):
    """Envelope consistency only, followed by fresh independent execution checks.

    Hash-shaped values do not establish provenance. This never derives missing
    scientific identities, prepares an authorization, or grants a REAL permit.
    """
    try:
        need(set(doc) == {'schema', 'scope', 'consumer_uid', 'target_authorization', 'execution_binding'}
             and doc['schema'] == REAL_A11_SCHEMA and doc['scope'] == REAL_A11_SCOPE, 'PUBLICATION_SCHEMA')
        need(type(doc['consumer_uid']) is int and doc['consumer_uid'] == 501, 'WRONG_CONSUMER_UID')
        t = doc['target_authorization']; b = doc['execution_binding']
        need(real_publication_contract(t)[:2] == (REAL_A11_SCHEMA, REAL_A11_SCOPE), 'A11_ATTEMPT_CONTEXT')
        need(t['project'] == 'QUANTITATIVE_TRADING_RESEARCH_PLATFORM' and t['batch'] == 'BATCH0004'
             and t['role'] == 'PRIMARY' and t['phase'] == 'S05' and t['environment'] == 'REAL'
             and t['unit_id'] == 'U0012' and type(t['attempt_id']) is str and bool(t['attempt_id'])
             and type(t['checkpoint_sequence']) is int and t['checkpoint_sequence'] == 54, 'A11_TARGET_SCOPE')
        need(type(t['max_new_units']) is int and t['max_new_units'] == 1 and t['u0013_prohibited'] is True
             and t['single_use'] is True and t['replay_protected'] is True and t['consumed'] is False
             and t['dispatched'] is False and t['activation_gate'] == 'HARD_DISABLED', 'A11_SINGLE_USE_SCOPE')
        cfg = t['base_deployment_configuration']; effects = b['effects']; runtime = effects['runtime']
        need(t['deployment_identity'] == digest(canonical(cfg)), 'A11_CONFIGURATION_IDENTITY')
        need(cfg['execution_mode'] == 'REAL' and cfg['runtime_root'] == REAL_A11_RUNTIME_ROOT
             and cfg['unit_id'] == 'U0012' and type(cfg['max_new_units']) is int and cfg['max_new_units'] == 1
             and cfg['u0013_prohibited'] is True and cfg['real_activation'] == 'HARD_DISABLED', 'A11_RUNTIME_SCOPE')
        need(type(cfg['operational_context']['attempt_ordinal']) is int
             and cfg['operational_context']['attempt_ordinal'] == 11, 'A11_ATTEMPT_ORDINAL')
        for field in ('release_sha256', 'detached_pin_sha256', 'composition_source_sha256',
                      'capture_configuration_sha256', 'recovery_sha256', 'recovery_compatibility_binding_sha256',
                      'policy_b_sha256', 'environment_identity', 'python_compatibility_identity'):
            need(type(cfg[field]) is str and re.fullmatch('[0-9a-f]{64}', cfg[field]) is not None, 'A11_MANDATORY_IDENTITY')
        need(type(t['checkpoint_identity']) is str and re.fullmatch('[0-9a-f]{64}', t['checkpoint_identity']) is not None
             and cfg['checkpoint']['checkpoint_identity'] == t['checkpoint_identity']
             and type(cfg['checkpoint']['historical_attempt_count']) is int
             and cfg['checkpoint']['historical_attempt_count'] == 10, 'A11_CHECKPOINT_BINDING')
        need(type(cfg['selected_source_sha256']) is dict and bool(cfg['selected_source_sha256'])
             and all(type(v) is str and re.fullmatch('[0-9a-f]{64}', v) is not None
                     for v in cfg['selected_source_sha256'].values()), 'A11_COMPONENT_IDENTITIES')
        need(type(cfg['capture_environment']) is dict
             and cfg['environment_identity'] == digest(canonical(cfg['capture_environment']))
             and cfg['transport']['environment'] == cfg['capture_environment'], 'A11_ENVIRONMENT_BINDING')
        spec = cfg['runtime_compatibility']
        need(cfg['python_compatibility_identity'] == digest(canonical(spec))
             and cfg['capture_environment']['PATH'] == spec['path']['prefix'] + ':' + spec['path']['remainder'],
             'A11_PATH_COMPATIBILITY_BINDING')
        # Mandatory execution fields exclude the earlier technical-only spec.
        need(type(cfg['capture_executable']) is str and bool(cfg['capture_executable'])
             and type(cfg['capture_argv']) is list and bool(cfg['capture_argv'])
             and all(type(v) is str for v in cfg['capture_argv'])
             and type(cfg['capture_cwd']) is str and bool(cfg['capture_cwd']), 'A11_CAPTURE_CONFIGURATION_REQUIRED')
        need(type(cfg['transport']['v2_stdin_sha256']) is str
             and re.fullmatch('[0-9a-f]{64}', cfg['transport']['v2_stdin_sha256']) is not None, 'A11_INPUT_IDENTITY_REQUIRED')
        for field in ('environment', 'unit_id', 'attempt_id', 'next_attempt_sequence',
                      'historical_attempt_count', 'max_new_units', 'u0013_prohibited', 'checkpoint_identity'):
            need(type(b[field]) is type(t[field]) and b[field] == t[field], 'A11_EXECUTION_TARGET_BINDING')
            need(type(effects[field]) is type(t[field]) and effects[field] == t[field], 'A11_PHYSICAL_EFFECT_BINDING')
        need(b['authorized_positions'] == effects['authorized_positions'] == list(range(1776, 1801))
             and b['target_deployment_identity'] == t['deployment_identity']
             and b['launch_permission'] == 'EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION', 'A11_EXECUTION_SCOPE')
        for field, value in {
            'capture_config_sha256': cfg['capture_configuration_sha256'], 'input_sha256': cfg['transport']['v2_stdin_sha256'],
            'candidate_release_sha256': cfg['release_sha256'], 'target_configuration_sha256': t['deployment_identity'],
            'target_composition_source_sha256': cfg['composition_source_sha256'], 'target_checkpoint_sequence': 54,
            'target_recovery_source_sha256': cfg['recovery_sha256'],
            'target_recovery_compatibility_binding_sha256': cfg['recovery_compatibility_binding_sha256'],
            'policy_b_sha256': cfg['policy_b_sha256'],
        }.items():
            need(type(runtime[field]) is type(value) and runtime[field] == value, 'A11_RUNTIME_IDENTITY_BINDING')
        policy = t['authorization_policy']
        need(t['authorization_policy_sha256'] == digest(canonical(policy)) and policy['scope'] == REAL_A11_SCOPE,
             'A11_AUTHORIZATION_POLICY_BINDING')
        for field in ('project', 'batch', 'role', 'phase', 'unit_id', 'attempt_id', 'next_attempt_sequence',
                      'historical_attempt_count', 'max_new_units', 'u0013_prohibited', 'single_use',
                      'replay_protected', 'environment', 'activation_gate'):
            need(type(policy[field]) is type(t[field]) and policy[field] == t[field], 'A11_AUTHORIZATION_POLICY_BINDING')
    except (KeyError, TypeError, AttributeError):
        need(False, 'A11_MISSING_OR_INVALID_MANDATORY_FIELD')
    return doc

def validate_owner_document(raw):
    """Exact inert or future REAL publication schema; not an activation gate.

    REAL documents are neither prepared nor published by the correction tests.
    Their separately fixed root and scope are mandatory on later readback.
    """
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'DUPLICATE_JSON_FIELD');result[key]=value
        return result
    doc=json.loads(raw,object_pairs_hook=pairs)
    need(raw==canonical(doc),'NONCANONICAL_PUBLICATION')
    if doc.get('schema')==SCHEMA:
        return validate_inert_document(raw)
    if doc.get('schema')==REAL_A11_SCHEMA:
        return _validate_a11_document(doc)
    need(set(doc)=={'schema','scope','consumer_uid','target_authorization','execution_binding'} and
         doc['schema']==REAL_SCHEMA and doc['scope']==REAL_SCOPE,'PUBLICATION_SCHEMA')
    need(type(doc['consumer_uid']) is int and doc['consumer_uid']==501,'WRONG_CONSUMER_UID')
    target=doc['target_authorization'];binding=doc['execution_binding']
    need(target['environment']=='REAL' and target['unit_id']=='U0012' and
         type(target['next_attempt_sequence']) is int and target['next_attempt_sequence']==10 and
         target['historical_attempt_count']==9 and type(target['max_new_units']) is int and
         target['max_new_units']==1 and target['single_use'] is True and target['replay_protected'] is True and
         target['consumed'] is False and target['dispatched'] is False and target['u0013_prohibited'] is True,
         'WRONG_REVIEW_TARGET_SCOPE')
    need(binding['environment']=='REAL' and binding['attempt_id']==REAL_ATTEMPT and
         binding['unit_id']=='U0012' and type(binding['next_attempt_sequence']) is int and
         binding['next_attempt_sequence']==10 and binding['historical_attempt_count']==9 and
         type(binding['max_new_units']) is int and binding['max_new_units']==1 and
         binding['u0013_prohibited'] is True and binding['authorized_positions']==list(range(1776,1801)),
         'REAL_BINDING_SCOPE_INVALID')
    return doc

def publish(candidate, expected_sha256, expected_length):
    need(os.getuid() == 0 and os.geteuid() == 0, 'EXPLICIT_OWNER_PRIVILEGE_REQUIRED')
    need(os.environ.get('SUDO_UID') == '501', 'OWNER_TERMINAL_SUDO_CONTEXT_REQUIRED')
    need(os.isatty(0), 'OWNER_INTERACTIVE_TERMINAL_REQUIRED')
    os.umask(0o022)
    need(re.fullmatch('[0-9a-f]{64}', expected_sha256) is not None
         and type(expected_length) is int and expected_length > 0, 'INVALID_REVIEW_IDENTITIES')
    fd = os.open(candidate, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        raw = read_snapshot(fd, expected_length, 501, 0o600)
    finally:
        os.close(fd)
    need(digest(raw) == expected_sha256, 'OWNER_REVIEWED_BYTES_MISMATCH')
    doc=validate_owner_document(raw)
    protected_root=(REAL_A11_PROTECTED_ROOT if doc['scope']==REAL_A11_SCOPE else
                    (PROTECTED_ROOT if doc['scope']==SCOPE else REAL_PROTECTED_ROOT))
    parent = open_root_chain(protected_root.parent)
    base = slot = output = None
    try:
        try:
            os.mkdir(protected_root.name, mode=0o755, dir_fd=parent)
        except FileExistsError:
            pass
        base = os.open(protected_root.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        st = os.fstat(base)
        need(st.st_uid == 0 and st.st_gid == 0 and stat.S_IMODE(st.st_mode) == 0o755,
             'PROTECTED_ROOT_WRONG_OWNER_OR_PERMISSIONS')
        os.fsync(parent)
        # A failed or partial reservation is deliberately retained and blocks retry.
        os.mkdir(expected_sha256, mode=0o755, dir_fd=base)
        slot = os.open(expected_sha256, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=base)
        os.fsync(base)
        output = os.open('authorization.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o400, dir_fd=slot)
        os.fchown(output, 0, 0)
        write_all(output, raw)
        # Unprivileged readers receive access only after complete durable bytes exist.
        os.fchmod(output, 0o444)
        os.fsync(output)
        os.close(output)
        output = None
        check = os.open('authorization.json', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=slot)
        try:
            need(read_snapshot(check, expected_length, 0, 0o444) == raw, 'PUBLICATION_READBACK_MISMATCH')
        finally:
            os.close(check)
        os.fsync(slot)
        # A partially written authorization is never sufficient for verification.
        # This receipt is exposed only after the authorization and directory fsyncs.
        completion = completion_receipt(expected_sha256, expected_length, scope=doc['scope'])
        output = os.open('publication_complete.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o400, dir_fd=slot)
        os.fchown(output, 0, 0)
        write_all(output, completion)
        os.fchmod(output, 0o444)
        os.fsync(output)
        os.close(output)
        output = None
        os.fsync(slot)
        check = os.open('publication_complete.json', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=slot)
        try:
            need(read_snapshot(check, len(completion), 0, 0o444) == completion,
                 'COMPLETION_RECEIPT_READBACK_MISMATCH')
        finally:
            os.close(check)
        return {'status': 'PUBLISHED_NONPRODUCTION_ONLY' if doc['scope']==SCOPE else 'PUBLISHED_REAL_AUTHORIZATION__NOT_ACTIVATED', 'sha256': expected_sha256,
                'length': expected_length, 'destination': str(protected_root / expected_sha256 / 'authorization.json'),
                'owner_uid': 0, 'owner_gid': 0, 'directory_mode': '0755', 'file_mode': '0444',
                'completion_receipt_sha256': digest(completion),
                'execution_authorized': False, 'real_activation': 'HARD_DISABLED'}
    finally:
        for descriptor in (output, slot, base, parent):
            if descriptor is not None:
                os.close(descriptor)

def owner_terminal_action(args):
    """One Owner action, no cached/passwordless publication and no credential IO."""
    need(os.getuid() == os.geteuid() == 501 and os.isatty(0), 'OWNER_TERMINAL_REQUIRED')
    source = Path(__file__).resolve()
    raw = source.read_bytes()
    need(args.source_sha256 is not None and digest(raw) == args.source_sha256,
         'OWNER_REVIEWED_PUBLICATION_SOURCE_MISMATCH')
    # Root executes a captured byte snapshot after verifying MAIN's literal pin.
    # No user-writable module is imported by this isolated system Python process.
    bootstrap = ('import os,stat,hashlib,sys;'
                 'p='+repr(str(source))+';'
                 'f=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);s=os.fstat(f);'
                 'assert stat.S_ISREG(s.st_mode) and s.st_uid==501 and s.st_nlink==1;'
                 'b=os.read(f,'+str(len(raw)+1)+');os.close(f);'
                 'assert len(b)=='+str(len(raw))+' and hashlib.sha256(b).hexdigest()=='+repr(args.source_sha256)+';'
                 'sys.argv=[p]+sys.argv[1:];exec(compile(b,p,"exec"),{"__name__":"__main__","__file__":p})')
    command = ['/usr/bin/python3', '-I', '-B', '-c', bootstrap,
               '--candidate', args.candidate, '--sha256', args.sha256, '--length', str(args.length)]
    sudo = ['/usr/bin/sudo', '-k', '-u', 'root', '-g', 'wheel', '--']
    environment = dict(os.environ, LC_ALL='C', LANG='C')
    # Same root command and argv, but no terminal stdin. If unattended sudo could
    # execute it, its TTY guard stops before publication and this action aborts.
    probe = subprocess.run([sudo[0], '-n', *sudo[1:], *command], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, env=environment, timeout=10, close_fds=True)
    need(probe.returncode == 1 and probe.stderr.strip() == 'sudo: a password is required',
         'FRESH_OWNER_AUTHENTICATION_NOT_ESTABLISHED__NO_PUBLICATION')
    # -k with a command ignores existing credentials and does not refresh cache.
    # stdin/stdout/stderr stay attached to the Owner terminal; passwords are never
    # read, captured, passed, stored or logged by this implementation.
    return subprocess.run([*sudo, *command], env=environment, close_fds=True).returncode

MODEL_B_SCOPE = 'MODEL_B_SYNTHETIC_EXACT_ONE_UNIT_V1'
MODEL_B_TASK = 'QTRP_MODEL_B_A11_REAL_CONTRACT_NONPRODUCTION_QUALIFICATION_V1'
MODEL_B_ROOT = Path('/private/tmp/QTRP_MODEL_B_A11_REAL_CONTRACT_NONPRODUCTION_QUALIFICATION_V1')
MODEL_B_LOADED_SOURCE_SHA256 = digest(Path(__file__).read_bytes())

def model_b_root(path):
    """Fixed disposable namespace; never select a REAL publication locator."""
    need(Path(__file__).resolve() == MODEL_B_ROOT/'candidate/owner_publication.py'
         and os.getuid() == os.geteuid() == 501, 'MODEL_B_FIXED_UNPRIVILEGED_SOURCE_REQUIRED')
    need(digest(Path(__file__).read_bytes()) == MODEL_B_LOADED_SOURCE_SHA256,
         'MODEL_B_PUBLICATION_SOURCE_DRIFT')
    path = Path(path).absolute()
    need(path.is_relative_to(MODEL_B_ROOT/'fixtures') and path.resolve() == path,
         'MODEL_B_DISPOSABLE_NAMESPACE_REQUIRED')
    return path

def validate_model_b_document(raw):
    doc = json.loads(raw)
    need(raw == canonical(doc) and set(doc) ==
         {'schema','scope','consumer_uid','target_authorization','fixture_binding','execution_binding'},
         'MODEL_B_CANONICAL_AUTHORIZATION_REQUIRED')
    need(doc['schema'] == SCHEMA and doc['scope'] == MODEL_B_SCOPE
         and type(doc['consumer_uid']) is int and doc['consumer_uid'] == 501,
         'MODEL_B_AUTHORIZATION_DOMAIN_REQUIRED')
    t = doc['target_authorization']
    need(type(t) is dict and t.get('environment') == 'SYNTHETIC_NONPRODUCTION'
         and t.get('real_execution_authorized') is False and t.get('unit_id') == 'U0012'
         and type(t.get('attempt_ordinal')) is int and t['attempt_ordinal'] == 11
         and type(t.get('historical_attempt_count')) is int and t['historical_attempt_count'] == 10
         and type(t.get('checkpoint_sequence')) is int and t['checkpoint_sequence'] == 54
         and type(t.get('max_new_units')) is int and t['max_new_units'] == 1
         and t.get('u0013_prohibited') is True and t.get('expected_rows') == 25
         and t.get('real_activation') == 'HARD_DISABLED', 'MODEL_B_EXACT_UNIT_ATTEMPT_SCOPE')
    need(type(t.get('attempt_id')) is str and t['attempt_id'].startswith('SYNTHETIC_POLICY_B_MODEL_B_'),
         'MODEL_B_SYNTHETIC_ATTEMPT_REQUIRED')
    for key in ('checkpoint_identity','input_sha256','runtime_sha256','configuration_sha256',
                'policy_sha256','release_sha256','case_sha256'):
        need(type(t.get(key)) is str and re.fullmatch('[0-9a-f]{64}',t[key]) is not None,
             'MODEL_B_REQUIRED_IDENTITY')
    model_b_root(t['checkpoint_root'])
    need(type(doc['fixture_binding']) is dict, 'MODEL_B_SOURCE_BINDING_REQUIRED')
    cfg=t.get('configuration')
    need(type(cfg) is dict and cfg.get('execution_configuration_complete') is True
         and cfg.get('environment')=='SYNTHETIC_NONPRODUCTION'
         and cfg.get('real_execution_authorized') is False
         and digest(canonical(cfg))==t['configuration_sha256'], 'MODEL_B_COMPLETE_CONFIGURATION_REQUIRED')
    effects=doc['execution_binding']
    need(type(effects) is dict and effects.get('environment')=='SYNTHETIC_NONPRODUCTION'
         and effects.get('real_execution_authorized') is False
         and effects.get('target_sha256')==digest(canonical(t))
         and effects.get('configuration_sha256')==t['configuration_sha256']
         and effects.get('attempt_ordinal')==11 and effects.get('historical_attempt_count')==10
         and effects.get('unit_id')=='U0012' and effects.get('max_new_units')==1
         and effects.get('u0013_prohibited') is True, 'MODEL_B_PHYSICAL_EFFECT_BINDING_REQUIRED')
    return doc

def model_b_sync_directory(directory):
    directory=model_b_root(directory)
    fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try: os.fsync(fd)
    finally: os.close(fd)

def model_b_unique_record(path, raw):
    """Exclusive durable append; retain incomplete records to prohibit retry."""
    path=model_b_root(path)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try: write_all(fd,raw);os.fsync(fd)
    finally: os.close(fd)
    model_b_sync_directory(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try: need(read_snapshot(fd,len(raw),501,0o600)==raw,'MODEL_B_RECORD_READBACK_FAILED')
    finally: os.close(fd)

def model_b_completion(pin, length):
    return canonical({'scope':MODEL_B_SCOPE,'authorization_sha256':pin,
        'authorization_length':length,'publication_complete':True,'real_authority':False})

def publish_model_b(candidate, expected_sha256, expected_length, *, approval_fd, directory):
    """Owner process supplies an exact approval over a read-only anonymous pipe.

    This adapts the existing publisher only inside the fixed synthetic capsule.
    The executor receives neither this pipe nor a publication API capability.
    Same-UID malicious tampering is outside the adopted cooperative Model B.
    """
    import fcntl
    directory = model_b_root(directory)
    need(type(approval_fd) is int and approval_fd > 2, 'MODEL_B_OWNER_APPROVAL_CHANNEL_REQUIRED')
    flags = fcntl.fcntl(approval_fd, fcntl.F_GETFL)
    need(flags & os.O_ACCMODE == os.O_RDONLY and stat.S_ISFIFO(os.fstat(approval_fd).st_mode),
         'MODEL_B_READ_ONLY_OWNER_PIPE_REQUIRED')
    approval = b''
    while len(approval) <= 4096:
        part = os.read(approval_fd,4097-len(approval))
        if not part: break
        approval += part
    os.close(approval_fd)
    a = json.loads(approval)
    need(approval == canonical(a) and set(a) == {'task_id','sha256','length','owner_pid'},
         'MODEL_B_OWNER_APPROVAL_SCHEMA')
    need(a['task_id'] == MODEL_B_TASK
         and a['sha256'] == expected_sha256 and a['length'] == expected_length
         and type(a['length']) is int and a['length']>0
         and type(a['owner_pid']) is int and a['owner_pid'] == os.getppid()
         and a['owner_pid'] != os.getpid(), 'MODEL_B_EXPLICIT_OWNER_APPROVAL_MISMATCH')
    candidate = model_b_root(candidate)
    fd = os.open(candidate,os.O_RDONLY|os.O_NOFOLLOW)
    try: raw = read_snapshot(fd,expected_length,501,0o600)
    finally: os.close(fd)
    need(digest(raw) == expected_sha256, 'MODEL_B_CANDIDATE_DIGEST_MISMATCH')
    validate_model_b_document(raw)
    directory.mkdir(mode=0o700,exist_ok=False)
    model_b_sync_directory(directory.parent)
    model_b_unique_record(directory/'authorization.json',raw)
    completion=model_b_completion(expected_sha256,expected_length)
    model_b_unique_record(directory/'publication_complete.json',completion)
    return {'scope':MODEL_B_SCOPE,'sha256':expected_sha256,'length':expected_length,
            'completion_sha256':digest(completion),
            'owner_pid':a['owner_pid'],'publisher_pid':os.getpid(),'real_authority':False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--length', type=int, required=True)
    parser.add_argument('--owner-terminal', action='store_true')
    parser.add_argument('--source-sha256')
    args = parser.parse_args()
    # Only MAIN's separately reviewed Owner terminal action may invoke publish().
    try:
        if args.owner_terminal:
            return owner_terminal_action(args)
        print(json.dumps(publish(args.candidate, args.sha256, args.length), sort_keys=True))
    except (OSError, ValueError, KeyError, PublicationStop, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'CONTROLLED_STOP', 'error_type': type(exc).__name__,
                          'failure_classification': str(exc) if isinstance(exc, PublicationStop) else type(exc).__name__,
                          'errno': getattr(exc, 'errno', None), 'automatic_retry': False,
                          'real_activation': 'HARD_DISABLED'}, sort_keys=True))
        return 77
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
