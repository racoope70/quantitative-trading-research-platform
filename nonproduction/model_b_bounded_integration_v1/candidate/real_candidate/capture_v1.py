"""Controlled local process observation interface for future S05 REAL runtime.

REAL requests require the existing exact execution context and fresh protected
Owner readback plus durable consumption at each boundary. NONPRODUCTION fixture
permits remain separate and cannot authorize a REAL process.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib, io, json, os, secrets, selectors, shutil, signal, stat, subprocess, sys, time
from trusted_stage.staging_v1 import StageStop, require, canonical, sha, safe_read

PRELAUNCH_BUDGET_SECONDS = 1800
CHILD_CAPTURE_BUDGET_SECONDS = 300
TIMEOUT_POLICY = 'OWNER_OPTION_B_POST_POPEN_CAPTURE_V1'
MAX_TIMING_RECEIPT_BYTES = 8192

# This engineering copy has one explicit NONPRODUCTION artifact location.
# The default REAL path, permits and process-spawn authority remain unchanged.
COMPATIBILITY_CANDIDATE_ROOT = Path('/private/tmp/QTRP_BATCH0004_C06_TO_A11_READINESS_CANDIDATE_V1')
PROSPECTIVE_A11_RUNTIME_ROOT = Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a11_u0012_attempt11_runtime_v1')
PINNED_PYTHON = Path('/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12')
PINNED_PYTHON_SHA256 = 'd4f152f2a753c94e0e7935c8ebbe6b2609979e1df7898422b577d0076383d08b'
PINNED_PYTHON_VERSION = '3.12.10'
COMPATIBILITY_PATH_REMAINDER = '/usr/local/bin:/usr/bin:/bin'


def task_python_compatibility(*, prospective_a11=False):
    """Expected artifact specification; environment construction belongs to Owner."""
    require(type(prospective_a11) is bool, 'PYTHON_COMPAT_PROSPECTIVE_SELECTOR')
    if prospective_a11:
        require(Path(__file__).resolve() in (
            COMPATIBILITY_CANDIDATE_ROOT / 'candidate/real_candidate/capture_v1.py',
            PROSPECTIVE_A11_RUNTIME_ROOT / 'candidate/real_candidate/capture_v1.py'),
            'PYTHON_COMPAT_PROSPECTIVE_SOURCE')
        require(os.getuid() == os.geteuid() == 501, 'PYTHON_COMPAT_OWNER')
    root = PROSPECTIVE_A11_RUNTIME_ROOT if prospective_a11 else COMPATIBILITY_CANDIDATE_ROOT
    target = {'literal_target': str(PINNED_PYTHON), 'resolved_target': str(PINNED_PYTHON),
              'sha256': PINNED_PYTHON_SHA256, 'version': PINNED_PYTHON_VERSION}
    directory = {'path': str(root / 'task_runtime/bin'), 'uid': 501, 'mode': 0o700,
                 'entry': 'python', 'entry_type': 'symlink', 'target': target}
    path = {'prefix': directory['path'], 'remainder': COMPATIBILITY_PATH_REMAINDER}
    return {'mechanism': 'TASK_LOCAL_SINGLE_PYTHON_SYMLINK', 'target': target,
            'directory': directory, 'path': path,
            'entry_identity': sha(canonical(target)),
            'runtime_bin_identity': sha(canonical(directory)),
            'path_construction_identity': sha(canonical(path))}


def _candidate_compatibility_scope():
    require(Path(__file__).resolve() == COMPATIBILITY_CANDIDATE_ROOT /
            'candidate/real_candidate/capture_v1.py', 'PYTHON_COMPAT_CANDIDATE_SOURCE')
    require(os.getuid() == os.geteuid() == 501, 'PYTHON_COMPAT_OWNER')


def _compatibility_directory(path):
    try:
        observed = path.lstat()
    except OSError:
        raise StageStop('PYTHON_COMPAT_DIRECTORY_MISSING') from None
    require(stat.S_ISDIR(observed.st_mode), 'PYTHON_COMPAT_DIRECTORY_TYPE')
    require(observed.st_uid == 501, 'PYTHON_COMPAT_DIRECTORY_OWNER')
    require(stat.S_IMODE(observed.st_mode) == 0o700, 'PYTHON_COMPAT_DIRECTORY_PERMISSIONS')


def prepare_task_python():
    """Create once, otherwise verify; never repair a missing existing entry."""
    _candidate_compatibility_scope()
    root = COMPATIBILITY_CANDIDATE_ROOT
    _compatibility_directory(root)
    for directory in (root / 'task_runtime', root / 'task_runtime/bin'):
        created = False
        try:
            directory.mkdir(mode=0o700)
            created = True
        except FileExistsError:
            pass
        _compatibility_directory(directory)
        if directory.name == 'bin' and created:
            os.symlink(str(PINNED_PYTHON), directory / 'python')
    return task_python_compatibility()


def validate_task_python(environment, specification):
    """Fresh bounded checks under the accepted Owner-controlled-host model."""
    _candidate_compatibility_scope()
    require(specification == task_python_compatibility(), 'PYTHON_COMPAT_IDENTITY')
    root = COMPATIBILITY_CANDIDATE_ROOT
    runtime_bin = root / 'task_runtime/bin'
    for directory in (root, runtime_bin.parent, runtime_bin):
        _compatibility_directory(directory)
    require(runtime_bin.resolve(strict=True) == runtime_bin, 'PYTHON_COMPAT_DIRECTORY_IDENTITY')
    entries = {entry.name for entry in runtime_bin.iterdir()}
    require('python' in entries, 'PYTHON_COMPAT_ENTRY_MISSING')
    require(entries == {'python'}, 'PYTHON_COMPAT_EXTRA_ENTRY')
    entry = runtime_bin / 'python'
    require(stat.S_ISLNK(entry.lstat().st_mode), 'PYTHON_COMPAT_ENTRY_TYPE')
    require(os.readlink(entry) == str(PINNED_PYTHON), 'PYTHON_COMPAT_LITERAL_TARGET')
    try:
        resolved = entry.resolve(strict=True)
    except OSError:
        raise StageStop('PYTHON_COMPAT_TARGET_MISSING') from None
    require(resolved == PINNED_PYTHON and resolved.is_file(), 'PYTHON_COMPAT_RESOLVED_TARGET')
    require(os.access(resolved, os.X_OK), 'PYTHON_COMPAT_TARGET_EXECUTABLE')
    require(sha(safe_read(resolved)) == PINNED_PYTHON_SHA256, 'PYTHON_COMPAT_TARGET_SHA256')
    require(type(environment) is dict and type(environment.get('PATH')) is str,
            'PYTHON_COMPAT_PATH_REQUIRED')
    parts = environment['PATH'].split(':')
    require(parts[0] == str(runtime_bin), 'PYTHON_COMPAT_PATH_PREFIX')
    require(parts[1:] == COMPATIBILITY_PATH_REMAINDER.split(':'), 'PYTHON_COMPAT_PATH_REMAINDER')
    require(shutil.which('python', path=environment['PATH']) == str(entry), 'PYTHON_COMPAT_LOOKUP')
    try:
        version = subprocess.run([str(resolved), '-I', '-S', '-B', '-c',
                                  'import sys; print(sys.version.split()[0])'],
                                 cwd=root, env=environment, stdin=subprocess.DEVNULL,
                                 capture_output=True, timeout=10, close_fds=True)
    except (OSError, subprocess.TimeoutExpired):
        raise StageStop('PYTHON_COMPAT_VERSION_PROBE') from None
    require(version.returncode == 0 and version.stdout ==
            (PINNED_PYTHON_VERSION + '\n').encode() and not version.stderr,
            'PYTHON_COMPAT_TARGET_VERSION')
    return specification['runtime_bin_identity']


def validate_candidate_binding(binding):
    """Bind this standalone candidate to its existing descriptor, never a REAL root."""
    _candidate_compatibility_scope()
    root = COMPATIBILITY_CANDIDATE_ROOT
    require(type(binding) is dict and set(binding) ==
            {'release_sha256', 'owner_source_sha256', 'composition_source_sha256'},
            'PYTHON_COMPAT_RELEASE_BINDING')
    try:
        raw = safe_read(root / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json')
        pin = safe_read(root / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256')
        descriptor = json.loads(raw)
        require(raw == canonical(descriptor) and sha(raw) == binding['release_sha256']
                and pin == (sha(raw) + '\n').encode(), 'PYTHON_COMPAT_RELEASE_BINDING')
        from real_candidate.release_v1 import verify_release
        require(verify_release(root) == binding['release_sha256'],
                'PYTHON_COMPAT_RELEASE_BINDING')
        capture_sha = sha(safe_read(Path(__file__)))
        require(descriptor['new_integration_components']['CAPTURE_V1'] ==
                {'path': 'candidate/real_candidate/capture_v1.py', 'sha256': capture_sha},
                'PYTHON_COMPAT_RELEASE_BINDING')
        for key, relative in (('RECOVERY', 'candidate/recovery_bounded_v4.py'),
                              ('RECOVERY_COMPATIBILITY', 'candidate/recovery_compatibility_bounded_v4.json')):
            require(descriptor['prospective_components'][key] ==
                    {'path': relative, 'sha256': sha(safe_read(root / relative))},
                    'PYTHON_COMPAT_RELEASE_BINDING')
        require(sha(safe_read(root / 'candidate/owner_authorization.py')) == binding['owner_source_sha256']
                and sha(safe_read(root / 'composition.py')) == binding['composition_source_sha256'],
                'PYTHON_COMPAT_SOURCE_BINDING')
    except (OSError, ValueError, KeyError, TypeError):
        raise StageStop('PYTHON_COMPAT_RELEASE_BINDING') from None

@dataclass(frozen=True, slots=True)
class LocalObservation:
    invocation_id: str
    started_ns: int
    exited_ns: int
    exit_code: int | None
    termination: str
    stdout: bytes
    stderr: bytes
    stdout_sha256: str
    stderr_sha256: str
    raw_output_sha256: str
    executable_sha256: str
    adapter_sha256: str
    config_sha256: str
    capture_source_sha256: str
    actual_input_sha256: str
    timeout: bool
    truncated: bool
    execution_exception: bool
    local_transport_interruption: bool
    mode: str
    _seal: object
    capture_limit_bytes: int = 16*1024*1024
    limit_exceeded: bool = False
    capture_complete: bool = True
    cleanup_complete: bool = True
    capture_error: str | None = None
    input_delivery: str = 'STDIN'
    timing_receipt: bytes = b''

class ControlledLocalCapture:
    """Captures OS facts without taking status booleans from the caller or child.

    For REAL, invocation must be separately authorized; this release never
    issues the permit. Verified input is supplied as the *exact* stdin bytes.
    Only a separately permitted future runtime may dispatch external CLI.
    """
    def __init__(self, *, executable: Path, executable_sha256: str, argv: tuple[str,...],
                 cwd: Path, env: dict[str,str], adapter_sha256: str,
                 mode: str='REAL', allow_test_fixture: bool=False, max_output_bytes:int=16*1024*1024,
                 input_delivery:str='STDIN',
                 prelaunch_budget_seconds:float=PRELAUNCH_BUDGET_SECONDS,
                 child_capture_budget_seconds:float=CHILD_CAPTURE_BUDGET_SECONDS,
                 runtime_compatibility:dict|None=None, candidate_binding:dict|None=None):
        self.executable=Path(executable).resolve(strict=True)
        require(self.executable.is_file() and not self.executable.is_symlink(), 'EXECUTABLE_UNSAFE')
        require(sha(safe_read(self.executable))==executable_sha256, 'EXECUTABLE_INITIAL_DRIFT')
        require(type(argv) is tuple and len(argv)>=1 and all(type(x) is str for x in argv), 'INVALID_ARGV')
        require(type(env) is dict and all(type(k) is str and type(v) is str for k,v in env.items()), 'INVALID_ENV')
        require(type(adapter_sha256) is str and len(adapter_sha256)==64, 'UNBOUND_ADAPTER')
        require(mode in ('REAL','NONPRODUCTION_TEST'), 'INVALID_EXECUTION_MODE')
        if allow_test_fixture:
            require(mode=='NONPRODUCTION_TEST' and self.executable==Path(sys.executable).resolve(strict=True) and
                    argv[:2]==('-I','-c'), 'TEST_FIXTURE_POLICY_VIOLATION')
        require(type(max_output_bytes) is int and 1<=max_output_bytes<=16*1024*1024,
                'INVALID_CAPTURE_OUTPUT_LIMIT')
        self._max_output_bytes=max_output_bytes
        require(input_delivery in ('STDIN','FILE_IDENTITY_FRAME'),'INVALID_INPUT_DELIVERY')
        self.input_delivery=input_delivery
        require(type(prelaunch_budget_seconds) in (int,float) and 0<prelaunch_budget_seconds<=1800
                and type(child_capture_budget_seconds) in (int,float) and 0<child_capture_budget_seconds<=300,
                'INVALID_TIMEOUT_POLICY')
        self.prelaunch_budget_seconds=prelaunch_budget_seconds
        self.child_capture_budget_seconds=child_capture_budget_seconds
        self._allow_test=allow_test_fixture
        self.mode=mode
        self.argv=argv
        self.cwd=Path(cwd).resolve(strict=True)
        require(self.cwd.is_dir(), 'INVALID_CWD')
        self.env=dict(env)
        self.adapter_sha256=adapter_sha256
        self._original_executable_sha=executable_sha256
        self._runtime_compatibility = None
        self._candidate_binding = None
        if runtime_compatibility is not None:
            require(mode == 'NONPRODUCTION_TEST' and allow_test_fixture,
                    'PYTHON_COMPAT_NONPRODUCTION_ONLY')
            self._runtime_compatibility = json.loads(canonical(runtime_compatibility))
            self._candidate_binding = json.loads(canonical(candidate_binding))
            validate_candidate_binding(self._candidate_binding)
            validate_task_python(self.env, self._runtime_compatibility)
        else:
            require(candidate_binding is None, 'PYTHON_COMPAT_RELEASE_BINDING')
        self._config_sha=sha(canonical(self._configuration_payload()))
        self._seal=object()
        self._observed={}
        self._fixture_permit=None  # single-use, fixture-only internal sink permit
        self._real_capture_started=False  # local replay latch, never authority
        self._prelaunch_started_ns=None
        self._timing={}

    def _configuration_payload(self):
        payload = {'executable':str(self.executable),'argv':self.argv,
                   'cwd':str(self.cwd),'env':self.env,'adapter_sha256':self.adapter_sha256,
                   'mode':self.mode,'max_output_bytes':self._max_output_bytes,
                   'input_delivery':self.input_delivery,'timeout_policy':self.timeout_policy()}
        if self._runtime_compatibility is not None:
            payload['runtime_compatibility'] = self._runtime_compatibility
            payload['candidate_binding'] = self._candidate_binding
        return payload

    def timeout_policy(self):
        return {'policy':TIMEOUT_POLICY,'prelaunch_budget_seconds':self.prelaunch_budget_seconds,
                'post_popen_capture_budget_seconds':self.child_capture_budget_seconds,
                'popen_strictly_interruptible':False,'total_transaction_ceiling_seconds':None}

    def begin_prelaunch(self, *, _new_fixture=False):
        if _new_fixture:
            require(self._allow_test and self.mode=='NONPRODUCTION_TEST','FIXTURE_CLOCK_RESET_FORBIDDEN')
            self._prelaunch_started_ns=None
        if self._prelaunch_started_ns is None:
            require(not self._real_capture_started,'REAL_CAPTURE_ALREADY_USED')
            start=time.monotonic_ns()
            self._prelaunch_started_ns=start
            self._timing={'schema':'CAPTURE_PHASE_TIMING_OPTION_B_V1','policy':self.timeout_policy(),
                'prelaunch_start_ns':start,
                'prelaunch_deadline_ns':start+int(self.prelaunch_budget_seconds*1e9),
                'prelaunch_end_ns':None,'prelaunch_duration_ns':None,
                'popen_call_start_ns':None,'popen_return_ns':None,'popen_failure_ns':None,
                'popen_elapsed_ns':None,'child_pid':None,'post_popen_capture_start_ns':None,
                'child_capture_deadline_ns':None,'first_observable_child_io_ns':None,
                'child_timeout_ns':None,'termination_start_ns':None,'termination_complete_ns':None,
                'cleanup_complete_ns':None,'cleanup_return_code':None,'cleanup_success':None,
                'failure_classification':None,'evidence_persistence_complete_ns':None}
        return self._prelaunch_started_ns

    def check_prelaunch(self):
        self.begin_prelaunch()
        # Observable boundary enforcement, not cancellation of a synchronous call.
        now=time.monotonic_ns()
        if now>=self._timing['prelaunch_deadline_ns']:
            self._timing.update(prelaunch_end_ns=now,
                prelaunch_duration_ns=now-self._prelaunch_started_ns,
                failure_classification='PRELAUNCH_TIMEOUT')
            require(False,'PRELAUNCH_TIMEOUT')

    def timing_receipt(self):
        # Return an independent bounded nonpayload copy. No output excerpts.
        raw=canonical(self._timing)
        require(len(raw)<=MAX_TIMING_RECEIPT_BYTES,'TIMING_RECEIPT_LIMIT_EXCEEDED')
        import json
        return json.loads(raw)

    @property
    def config_sha256(self):return self._config_sha

    def _fresh(self):
        require(self.executable.is_file() and not self.executable.is_symlink() and
                sha(safe_read(self.executable))==self._original_executable_sha,
                'FRESH_PRELAUNCH_EXECUTABLE_DRIFT')
        if self._runtime_compatibility is not None:
            require(self.mode == 'NONPRODUCTION_TEST' and self._allow_test,
                    'PYTHON_COMPAT_NONPRODUCTION_ONLY')
            validate_task_python(self.env, self._runtime_compatibility)
            validate_candidate_binding(self._candidate_binding)
        require(sha(canonical(self._configuration_payload()))==self._config_sha,
                'FRESH_PRELAUNCH_CONFIGURATION_DRIFT')

    def _read_input(self, path:Path):
        # The accepted 16 MiB resource ceiling also bounds a substituted frame.
        # This is independent of a caller's smaller output budget.
        path=Path(path)
        require(not path.is_symlink(),'INPUT_PATH_UNSAFE')
        fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
        try:
            before=os.fstat(fd)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink==1,'INPUT_PATH_UNSAFE')
            require(before.st_size<=16*1024*1024,'INPUT_CAPTURE_LIMIT_EXCEEDED')
            with os.fdopen(fd,'rb',closefd=False) as stream:
                raw=stream.read(16*1024*1024+1)
            after=os.fstat(fd)
            require(len(raw)<=16*1024*1024,'INPUT_CAPTURE_LIMIT_EXCEEDED')
            require((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==
                    (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) and len(raw)==after.st_size,
                    'INPUT_CHANGED_DURING_CAPTURE_READ')
            return raw
        finally:
            os.close(fd)

    def observe(self, *, input_file:Path, pinned_input_sha256:str, timeout_seconds:float=5,
                test_only:bool=False, prelaunch_hook=None) -> LocalObservation:
        require(self._allow_test and test_only and self.mode=='NONPRODUCTION_TEST',
                'REAL_ACTIVATION_HARD_DISABLED')
        self.begin_prelaunch(_new_fixture=self._timing is not None and self._timing.get('cleanup_complete_ns') is not None)
        require(type(timeout_seconds) in (int,float) and 0<timeout_seconds<=self.child_capture_budget_seconds, 'INVALID_TIMEOUT')
        input_file=Path(input_file)
        require(input_file.is_file() and not input_file.is_symlink(), 'INPUT_PATH_UNSAFE')
        content=self._read_input(input_file)
        require(sha(content)==pinned_input_sha256,'ACTUAL_INPUT_IDENTITY_DRIFT')
        self._fresh()
        self.check_prelaunch()
        if prelaunch_hook is not None:
            require(callable(prelaunch_hook),'INVALID_TEST_HOOK')
            prelaunch_hook()
        self._fresh()
        # Public fixture path alone mints a single-use fixture permit.
        # No REAL permit is minted by this release.
        permit=object()
        self._fixture_permit=(permit,sha(content),input_file,pinned_input_sha256)
        try:
            return self._execute_verified(content,timeout_seconds,_fixture_permit=permit)
        finally:
            self._fixture_permit=None

    def _verify_real_authority(self, execution_context):
        from real_candidate.executor_v1 import verify_runtime_context
        from real_candidate.activation_v1 import production_activation
        c=execution_context
        verify_runtime_context(c,phase='EXECUTING')
        require(c.supervisor is self and self.mode=='REAL' and not self._allow_test,
                'EXACT_REAL_CAPTURE_CONTEXT_REQUIRED')
        production_activation(c.transaction,phase='EXECUTING')
        require(c._used and c._persistence_started and type(c._start_bytes) is bytes and
                safe_read(c.evidence_root/'primary_executor_process_start.json')==c._start_bytes,
                'REAL_EXECUTOR_START_RECEIPT_REQUIRED')
        return c

    def _execute_verified(self, content:bytes, timeout_seconds:float, *, _fixture_permit=None,
                          execution_context=None) -> LocalObservation:
        # ACTUAL PROCESS CREATION SINK: never trust wrapper-only checks.
        real=self.mode=='REAL'
        self.begin_prelaunch()
        self.check_prelaunch()
        if real:
            c=self._verify_real_authority(execution_context)
            require(_fixture_permit is None and self._fixture_permit is None and
                    not self._real_capture_started,'REAL_CAPTURE_ALREADY_USED_OR_FIXTURE_PERMIT')
            require(type(content) is bytes and sha(content)==c.binding.unit_input_sha256
                    and sha(self._read_input(c.frame))==c.binding.unit_input_sha256,
                    'REAL_CAPTURE_INPUT_BINDING_DRIFT')
            require(type(timeout_seconds) in (int,float) and 0<timeout_seconds<=300,
                    'INVALID_REAL_CAPTURE_TIMEOUT')
            require(timeout_seconds==self.child_capture_budget_seconds,'REAL_TIMEOUT_POLICY_DRIFT')
        else:
            require(execution_context is None and self._allow_test and self.mode=='NONPRODUCTION_TEST',
                    'TEST_FIXTURE_ONLY_SINK')
            if Path(__file__).resolve()==Path('/private/tmp/QTRP_MODEL_B_A11_AUTHORIZATION_INTERFACE_CORRECTION_V1/candidate/real_candidate/capture_v1.py'):
                import owner_authorization as owner
                owner.verify_model_b_authority(self,claim_launch=True)
            permit=self._fixture_permit
            require(permit is not None and _fixture_permit is permit[0] and
                    type(content) is bytes and sha(content)==permit[1] and
                    sha(self._read_input(permit[2]))==permit[3] and permit[1]==permit[3],
                    'MISSING_OR_FORGED_FIXTURE_EXECUTION_PERMIT')
            require(type(timeout_seconds) in (int,float) and
                    0<timeout_seconds<=self.child_capture_budget_seconds, 'INVALID_FIXTURE_TIMEOUT')
        self._fresh()  # required immediately before subprocess launch
        self.check_prelaunch()
        # Consume permit before reaching Popen; replay cannot launch twice.
        self._fixture_permit=None
        # Supplied *bytes* are the bytes the child receives; a path switch
        # after the read cannot silently change scientific input.
        invocation=secrets.token_hex(24)
        start=time.monotonic_ns()
        timeout=False;execution_exception=False;interrupted=False
        buffers={'stdout':bytearray(),'stderr':bytearray()}
        out=b'';err=b'';code=None;child=None
        limit_exceeded=False;capture_complete=False;cleanup_complete=True;capture_error=None
        selector=selectors.DefaultSelector()
        input_view=memoryview(content if self.input_delivery=='STDIN' else b'')
        input_offset=0;total=0
        deadline_ns=None
        try:
            if real:
                self._verify_real_authority(c)  # final independent check at Popen
                self._fresh()
                require(not self._real_capture_started,'REAL_CAPTURE_ALREADY_USED')
            elif Path(__file__).resolve()==Path('/private/tmp/QTRP_MODEL_B_A11_AUTHORIZATION_INTERFACE_CORRECTION_V1/candidate/real_candidate/capture_v1.py'):
                import owner_authorization as owner
                owner.verify_model_b_authority(self)  # fresh readback at the actual spawn boundary
            self.check_prelaunch()  # final check: expired verification cannot launch
            verified=time.monotonic_ns()
            self._timing.update(prelaunch_end_ns=verified,
                prelaunch_duration_ns=verified-self._prelaunch_started_ns)
            if real:
                self._real_capture_started=True  # consumed even if process creation fails
            self._timing['popen_call_start_ns']=time.monotonic_ns()
            child=subprocess.Popen([str(self.executable),*self.argv],cwd=self.cwd,
                        env=self.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,close_fds=True,bufsize=0,start_new_session=True)
            returned=time.monotonic_ns()
            deadline_ns=returned+int(timeout_seconds*1e9)
            self._timing.update(popen_return_ns=returned,
                popen_elapsed_ns=returned-self._timing['popen_call_start_ns'],
                child_pid=child.pid,post_popen_capture_start_ns=returned,
                child_capture_deadline_ns=deadline_ns)
            # A slow Popen is observed, not interrupted. Retain ownership and
            # recheck authority before capture; these checks share the child budget.
            if real:
                self._verify_real_authority(c)
                self._fresh()
            for name,pipe in (('stdout',child.stdout),('stderr',child.stderr)):
                os.set_blocking(pipe.fileno(),False)
                selector.register(pipe,selectors.EVENT_READ,name)
            if input_view:
                os.set_blocking(child.stdin.fileno(),False)
                selector.register(child.stdin,selectors.EVENT_WRITE,'stdin')
            else:
                child.stdin.close()
            while selector.get_map():
                remaining=(deadline_ns-time.monotonic_ns())/1e9
                if remaining<=0:
                    timeout=True;capture_error='TIMEOUT'
                    self._timing['child_timeout_ns']=time.monotonic_ns();break
                for key,_ in selector.select(remaining):
                    try:
                        if key.data=='stdin':
                            input_offset+=os.write(key.fd,input_view[input_offset:input_offset+io.DEFAULT_BUFFER_SIZE])
                            if self._timing['first_observable_child_io_ns'] is None:
                                self._timing['first_observable_child_io_ns']=time.monotonic_ns()
                            if input_offset==len(input_view):
                                selector.unregister(key.fileobj);key.fileobj.close()
                        else:
                            # Read at most one sentinel beyond the remaining budget.
                            # The sentinel is discarded; retained aggregate never exceeds it.
                            available=self._max_output_bytes-total
                            chunk=os.read(key.fd,min(io.DEFAULT_BUFFER_SIZE,available+1))
                            if chunk and self._timing['first_observable_child_io_ns'] is None:
                                self._timing['first_observable_child_io_ns']=time.monotonic_ns()
                            if not chunk:
                                selector.unregister(key.fileobj);key.fileobj.close()
                            elif len(chunk)>available:
                                buffers[key.data].extend(chunk[:available]);total+=available
                                limit_exceeded=True;capture_error='OUTPUT_LIMIT_EXCEEDED';break
                            else:
                                buffers[key.data].extend(chunk);total+=len(chunk)
                    except BlockingIOError:
                        continue
                    except BrokenPipeError:
                        capture_error='INCOMPLETE_STDIN';interrupted=True;break
                if limit_exceeded or interrupted:
                    break
            if capture_error is None:
                try:
                    code=child.wait(timeout=max(0,(deadline_ns-time.monotonic_ns())/1e9))
                    capture_complete=True
                except subprocess.TimeoutExpired:
                    timeout=True;capture_error='TIMEOUT'
                    self._timing['child_timeout_ns']=time.monotonic_ns()
        except OSError:
            execution_exception=True;interrupted=True;capture_error='CAPTURE_IO_ERROR'
            if child is None and self._timing['popen_call_start_ns'] is not None:
                failed=time.monotonic_ns()
                self._timing.update(popen_failure_ns=failed,
                    popen_elapsed_ns=failed-self._timing['popen_call_start_ns'],
                    failure_classification='POPEN_FAILURE')
        except Exception:
            # Preserve authorization rejection; never replace it with a timeout.
            if child is not None:
                self._timing['failure_classification']='POST_POPEN_SAFETY_REJECTION'
            elif self._timing['popen_call_start_ns'] is not None:
                failed=time.monotonic_ns()
                self._timing.update(popen_failure_ns=failed,
                    popen_elapsed_ns=failed-self._timing['popen_call_start_ns'],
                    failure_classification='POPEN_FAILURE')
            raise
        finally:
            # The dedicated session contains the child and inherited descendants.
            # Kill the group even after its leader exits, then reap with one bounded wait.
            if child is not None:
                self._timing['termination_start_ns']=time.monotonic_ns()
                try:os.killpg(child.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                except OSError:cleanup_complete=False;capture_error='PROCESS_GROUP_CLEANUP_FAILED'
                for pipe in (child.stdin,child.stdout,child.stderr):
                    if pipe is not None:
                        try:pipe.close()
                        except OSError:cleanup_complete=False;capture_error='PIPE_CLEANUP_FAILED'
                try:code=child.wait(timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    cleanup_complete=False;capture_error='PROCESS_REAP_TIMEOUT'
                    self._timing['failure_classification']='TERMINATION_TIMEOUT'
                else:self._timing['termination_complete_ns']=time.monotonic_ns()
                self._timing['cleanup_return_code']=code
            selector.close()
            input_view.release()
            self._timing.update(cleanup_complete_ns=time.monotonic_ns(),cleanup_success=cleanup_complete)
            if not cleanup_complete and self._timing['failure_classification'] is None:
                self._timing['failure_classification']='CLEANUP_FAILURE'
        out=bytes(buffers['stdout']);err=bytes(buffers['stderr'])
        end=time.monotonic_ns()
        state=('OUTPUT_LIMIT_EXCEEDED' if limit_exceeded else 'TIMEOUT' if timeout else
               'EXECUTION_EXCEPTION' if execution_exception else 'CAPTURE_FAILURE' if capture_error else
               'NORMAL_SUCCESS' if code==0 else 'ABNORMAL_EXIT')
        raw=len(out).to_bytes(8,'big')+out+len(err).to_bytes(8,'big')+err
        if timeout and self._timing['failure_classification'] is None:
            self._timing['failure_classification']=('CHILD_STARTED_NO_CAPTURED_OUTPUT_BEFORE_DEADLINE'
                if not out and not err else 'CHILD_ACTIVE_TIMEOUT')
        obs=LocalObservation(invocation,start,end,code,state,out,err,sha(out),sha(err),sha(raw),
                   self._original_executable_sha,self.adapter_sha256,self._config_sha,
                   sha(safe_read(Path(__file__))),sha(content),timeout,
                   limit_exceeded or not capture_complete,execution_exception,
                   interrupted,self.mode,self._seal,self._max_output_bytes,limit_exceeded,
                   capture_complete,cleanup_complete,capture_error,self.input_delivery,
                   canonical(self.timing_receipt()))
        self._observed[invocation]=obs
        return obs

    def verify(self, obs:LocalObservation, *, input_file:Path, pinned_input_sha256:str):
        require(type(obs) is LocalObservation and obs._seal is self._seal and
                self._observed.get(obs.invocation_id) is obs, 'CALLER_ORIGINATED_STATUS_REJECTED')
        import json
        require(type(obs.timing_receipt) is bytes and len(obs.timing_receipt)<=MAX_TIMING_RECEIPT_BYTES,
                'TIMING_RECEIPT_REQUIRED')
        timing=json.loads(obs.timing_receipt)
        require(timing.get('schema')=='CAPTURE_PHASE_TIMING_OPTION_B_V1' and
                all(type(timing.get(k)) is int for k in ('prelaunch_start_ns','prelaunch_end_ns',
                    'popen_call_start_ns','popen_return_ns','post_popen_capture_start_ns',
                    'child_capture_deadline_ns','cleanup_complete_ns')),
                'TIMING_OBSERVATIONS_MISSING')
        require(obs.started_ns<obs.exited_ns and obs.stdout_sha256==sha(obs.stdout) and
                obs.stderr_sha256==sha(obs.stderr) and obs.raw_output_sha256==
                sha(len(obs.stdout).to_bytes(8,'big')+obs.stdout+len(obs.stderr).to_bytes(8,'big')+obs.stderr),
                'CAPTURE_BYTE_INTEGRITY_FAILED')
        self._fresh()
        require(obs.executable_sha256==self._original_executable_sha and
                obs.adapter_sha256==self.adapter_sha256 and obs.config_sha256==self._config_sha and
                obs.capture_source_sha256==sha(safe_read(Path(__file__))), 'CAPTURE_RUNTIME_DRIFT')
        require(obs.actual_input_sha256==sha(self._read_input(Path(input_file)))==pinned_input_sha256 and
                obs.input_delivery==self.input_delivery,
                'CAPTURE_ACTUAL_INPUT_DRIFT')
        require(obs.exit_code==0 and obs.termination=='NORMAL_SUCCESS' and not any((obs.timeout,
                obs.truncated,obs.execution_exception,obs.local_transport_interruption,obs.limit_exceeded)) and
                obs.capture_complete and obs.cleanup_complete and obs.capture_error is None,
                'CAPTURE_FAIL_CLOSED')
        return True

    def observe_real(self, *, input_file:Path, pinned_input_sha256:str, timeout_seconds:float=None,
                     execution_context=None):
        self.begin_prelaunch()
        self.check_prelaunch()
        if timeout_seconds is None:timeout_seconds=self.child_capture_budget_seconds
        c=self._verify_real_authority(execution_context)
        require(Path(input_file)==c.frame and pinned_input_sha256==c.binding.unit_input_sha256,
                'REAL_CAPTURE_INPUT_BINDING_DRIFT')
        require(type(timeout_seconds) in (int,float) and 0<timeout_seconds<=300, 'INVALID_TIMEOUT')
        content=self._read_input(input_file)
        require(sha(content)==pinned_input_sha256,'ACTUAL_INPUT_IDENTITY_DRIFT')
        self._fresh()
        return self._execute_verified(content,timeout_seconds,execution_context=c)
