"""Batch0004 U0012 REAL trust-boundary wiring prototype -- NONPRODUCTION ONLY.

Controlled fixture observation is actual OS subprocess observation, not Codex execution.
A controlled local stderr observation and in-process signer are NOT privileged production authorities.
Activation remains disabled; production needs separately authorized protected signing and real runner integration.
Neither REAL runner dispatch nor real checkpoint mutations exist in this module.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
import base64, hashlib, importlib.util, json, os, re, secrets, subprocess, sys, time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from cryptography.exceptions import InvalidSignature
from trusted_stage.staging_v1 import StageStop, require, safe_read, sha, canonical
from trusted_stage.promotion_v1 import promote_exact_bytes, verify_promoted_bytes
import availability_classifier_v7_prospective as v7

POLICY_SHA = 'f3747fa0712821c32a9e97a02f196133e5544fff481185517de0e3748b4eef67'
CLASSIFIER_SHA = '8c20ea1dd8507e94606af849b7e5886a738cdff2c9d7d3aa333bfef4de42c651'
VALIDATOR_SHA = 'd8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42'
V3_SHA = 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0'
RECOVERY_SHA = 'b51c63dd499c20711d153cc9abfca0361b588ad1c4ae772b1f84f464fcfba785' # accepted real mode-bound recovery identity
ENGINE_SHA = '083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27'
REAL_ENGINE_SHA = 'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1'
REAL_ADAPTER_SHA = '1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424'
MODE_DESCRIPTOR_SHA = '0adcb00fbe0c98243e4241388043640a3a7ca4a658d02f37c8a56167d4f6365b'
VERSION = 'BATCH0004_REAL_TRUST_BOUNDARY_NONPRODUCTION_V1'
EXPECTED_ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
HEX64=re.compile(r'[0-9a-f]{64}\Z')


def verify_accepted_sources(root: Path) -> bool:
    root=Path(root).resolve()
    pairs={
       'policy_v7_prospective.json':POLICY_SHA,
       'availability_classifier_v7_prospective.py':CLASSIFIER_SHA,
       'historical_v6/checkpoint_resume_readiness_v8.py':ENGINE_SHA,
       'accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py':VALIDATOR_SHA,
       'accepted_recovery/reference/v6_accepted/frozen_v3_orchestrator_reference.py':V3_SHA,
       'accepted_recovery/checkpoint_resume_activation_trusted_v1.py':REAL_ENGINE_SHA,
       'accepted_recovery/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py':REAL_ADAPTER_SHA,
       'accepted_recovery/bounded_controlled_stop_recovery_real_interface_v2.py':RECOVERY_SHA,
       'accepted_recovery/recovery_mode_binding_descriptor_v2.json':MODE_DESCRIPTOR_SHA,
    }
    for name,pin in pairs.items():
        file=root/name
        require(file.is_file() and not file.is_symlink() and sha(file.read_bytes())==pin,
                'ACCEPTED_SOURCE_IDENTITY_CHANGED__'+name)
    return True


@dataclass(frozen=True,slots=True)
class RealAuthorizationBinding:
    batch_id: str
    role: str
    unit_id: str
    attempt_id: str
    checkpoint_sha256: str
    raw_unit_input_sha256: str
    executor_sha256: str
    executor_config_sha256: str
    mode_binding_sha256: str
    provenance_sha256: str
    authorized_dispatch: bool = False
    max_new_units: int = 1

    def verify_nonexecuting(self):
        require(self.batch_id=='BATCH0004' and self.role=='PRIMARY' and self.unit_id=='U0012', 'REAL_UNIT_BINDING_FAILURE')
        require(self.attempt_id==EXPECTED_ATTEMPT and type(self.max_new_units) is int and self.max_new_units==1,'REAL_ATTEMPT_OR_ONE_UNIT_BOUNDARY')
        for x in (self.checkpoint_sha256,self.raw_unit_input_sha256,self.executor_sha256,
                  self.executor_config_sha256,self.mode_binding_sha256,self.provenance_sha256):
            require(type(x) is str and HEX64.fullmatch(x),'MISSING_OR_MALFORMED_REAL_BINDING')
        # We are only authorized to design/test future REAL compatibility.
        require(self.authorized_dispatch is False, 'REAL_DISPATCH_NOT_AUTHORIZED')
        return self


@dataclass(frozen=True,slots=True)
class CapturedOSProcess:
    """Observed by this boundary from Popen, never populated from child JSON."""
    invocation_id: str
    process_start_event: str
    process_exit_event: str
    return_code: int
    termination_state: str
    timeout: bool
    stdout: bytes
    stderr: bytes
    stdout_sha256: str
    stderr_sha256: str
    raw_output_sha256: str
    executor_sha256: str
    config_sha256: str
    capture_source_sha256: str
    transport_interrupted: bool
    external_availability: bool
    auxiliary_provenance_attested: bool
    session_nonce: str
    _capture_seal: object


class ControlledFixtureSupervisor:
    """Actual OS evidence capture over PINNED harmless fixtures, not a real runner.

    This separate API has no caller-originated process-status inputs. The
    fixture origin attestation is a supervisor-owned test observation ONLY.
    """
    def __init__(self, fixture_file: Path, *, fixture_sha256: str, test_provenance: bool):
        fixture_file=Path(fixture_file).resolve(strict=True)
        require(fixture_file.name.startswith('nonproduction_trusted_fixture_') and
                not fixture_file.is_symlink() and sha(fixture_file.read_bytes())==fixture_sha256,
                'UNPINNED_TEST_FIXTURE')
        require(type(test_provenance) is bool,'INVALID_FIXTURE_PROVENANCE')
        self._fixture=fixture_file
        self._sha=fixture_sha256
        # Compatibility-only test argument. An untrusted caller flag MUST NOT
        # attest privileged provider-internal Models Manager provenance.
        self._legacy_test_provenance_ignored=test_provenance
        self._launch_executable=Path(sys.executable).resolve(strict=True)
        self._authorized_executable_sha256=sha(safe_read(self._launch_executable))
        self._launch_env={'PATH':os.environ.get('PATH',''),'PYTHONIOENCODING':'utf-8'}
        self._launch_cwd=str(self._fixture.parent)
        self._authorized_launch_config_sha256=sha(canonical({
            'argv_prefix':[str(self._launch_executable),'-I','-c'],
            'fixture_sha256':self._sha,'cwd':self._launch_cwd,'env':self._launch_env}))
        self._seal=object()
        self._captures={}
        # Test-only pre-spawn race hook; never injected into the REAL runner.
        self._test_pre_spawn_hook=None

    def _fresh_execution_material(self):
        """Resolve fresh binary and script bytes, never accept constructor-only digests.

        The script is executed from the verified in-memory bytes via `-c` rather
        than reopening a mutable pathname in the child process. This closes the
        fixture-script pathname TOCTOU; real controlled launcher remains outside
        this NONPRODUCTION component.
        """
        require(self._fixture.is_file() and not self._fixture.is_symlink(),
                'PRELAUNCH_FIXTURE_REMOVED_OR_SYMLINK')
        script=safe_read(self._fixture)
        require(sha(script)==self._sha, 'PRELAUNCH_FIXTURE_IDENTITY_DRIFT')
        try:
            source=script.decode('utf-8', errors='strict')
        except UnicodeDecodeError as exc:
            raise StageStop('PRELAUNCH_SCRIPT_NOT_UTF8') from exc
        executable=Path(sys.executable).resolve(strict=True)
        require(executable==self._launch_executable and executable.is_file() and not executable.is_symlink(),
                'PRELAUNCH_EXECUTABLE_INVALID')
        fresh_binary_sha=sha(safe_read(executable))
        require(fresh_binary_sha==self._authorized_executable_sha256,
                'PRELAUNCH_EXECUTABLE_IDENTITY_DRIFT')
        live_config_sha=sha(canonical({
            'argv_prefix':[str(executable),'-I','-c'],
            'fixture_sha256':sha(script),'cwd':self._launch_cwd,'env':self._launch_env}))
        require(live_config_sha==self._authorized_launch_config_sha256 and
                self._launch_cwd==str(self._fixture.parent),
                'PRELAUNCH_CONFIGURATION_DRIFT')
        return executable,fresh_binary_sha,source,sha(script)

    def observe(self, *, timeout_seconds=5) -> CapturedOSProcess:
        require(type(timeout_seconds) in (int,float) and 0<timeout_seconds<=10,'INVALID_TEST_TIMEOUT')
        invocation=secrets.token_hex(24)
        nonce=secrets.token_hex(24)
        executable,exe_sha,script,script_sha=self._fresh_execution_material()
        # This hook exists exclusively to reproduce a pre-spawn swap in the
        # nonproduction harness; it cannot inject runtime success/status fields.
        hook=self._test_pre_spawn_hook
        if hook is not None:
            require(callable(hook),'INVALID_TEST_HOOK')
            hook()
        executable2,exe_sha2,script2,script_sha2=self._fresh_execution_material()
        require(exe_sha2==exe_sha and script_sha2==script_sha,
                'EXECUTION_MATERIAL_CHANGED_BETWEEN_VERIFICATION_AND_SPAWN')
        # -c consumes these exact verified source bytes. No pathname is reopened
        # by the child for its script; the interpreter is root/system-owned in
        # this test environment, not an attested real launcher.
        argv=[str(executable2),'-I','-c',script2]
        config_sha=sha(canonical({'argv':argv,'fixture_sha256':script_sha2,
                                  'env':self._launch_env,'cwd':self._launch_cwd}))
        started=time.monotonic_ns()
        process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                 stdin=subprocess.DEVNULL,cwd=self._launch_cwd,
                                 env=dict(self._launch_env),close_fds=True)
        expired=False
        try:
            out,err=process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            expired=True;process.kill();out,err=process.communicate()
        end=time.monotonic_ns()
        code=process.returncode
        state='NORMAL_SUCCESS' if not expired and code==0 else ('TIMEOUT' if expired else 'ABNORMAL_EXIT')
        raw=len(out).to_bytes(8,'big')+out+len(err).to_bytes(8,'big')+err
        captured=CapturedOSProcess(invocation,str(started),str(end),code,state,expired,
              out,err,sha(out),sha(err),sha(raw),exe_sha2,config_sha,
              sha(Path(__file__).read_bytes()),False,False,
              False,nonce,self._seal)
        self._captures[invocation]=captured
        return captured

    def verify_capture(self, captured):
        require(type(captured) is CapturedOSProcess and captured._capture_seal is self._seal,
                'CALLER_ORIGINATED_RUNTIME_STATUS_REJECTED')
        require(self._captures.get(captured.invocation_id) is captured,'CAPTURE_REPLAY_OR_SUBSTITUTION')
        require(captured.stdout_sha256==sha(captured.stdout) and captured.stderr_sha256==sha(captured.stderr),
                'STDOUT_STDERR_SUBSTITUTION')
        require(captured.process_start_event.isdigit() and captured.process_exit_event.isdigit() and
                int(captured.process_exit_event)>int(captured.process_start_event) and
                captured.raw_output_sha256==sha(len(captured.stdout).to_bytes(8,'big')+captured.stdout+
                   len(captured.stderr).to_bytes(8,'big')+captured.stderr), 'INCOMPLETE_OR_INCONSISTENT_PROCESS_EVENTS')
        executable,fresh_exe_sha,source,fresh_script_sha=self._fresh_execution_material()
        fresh_argv=[str(executable),'-I','-c',source]
        require(captured.executor_sha256==fresh_exe_sha and
                captured.config_sha256==sha(canonical({'argv':fresh_argv,
                                                     'fixture_sha256':fresh_script_sha,
                                                     'env':self._launch_env,'cwd':self._launch_cwd})),
                'EXECUTOR_IDENTITY_DRIFT')
        require(captured.capture_source_sha256==sha(Path(__file__).read_bytes()),'CAPTURE_IMPLEMENTATION_DRIFT')
        require(captured.return_code==0 and captured.termination_state=='NORMAL_SUCCESS' and
                captured.timeout is False and captured.transport_interrupted is False and
                captured.external_availability is False, 'OPERATIONAL_FAILURE')
        # Privileged provider evidence is NOT available or required under the
        # ADMIN-approved accessible basis; never claim it from local stderr.
        require(captured.auxiliary_provenance_attested is False,
                'PRIVILEGED_PROVENANCE_MUST_NOT_BE_ASSERTED')
        try:
            lines=captured.stderr.decode('utf8',errors='strict').splitlines()
        except UnicodeDecodeError as exc:
            raise StageStop('INVALID_STDERR_ENCODING') from exc
        require(len(lines)==1 and v7.positive_auxiliary_source(lines[0]),
                'UNRECOGNIZED_AUXILIARY_OR_MULTIPLE_ERRORS')
        return True


class TrustedFixtureCheckpointGuard:
    """NONPRODUCTION fixture readback; production needs accepted checkpoint engine.

    This gate rejects actual checkpoint paths and only permits newly created
    isolated sample trees. Rereads bytes at each proof boundary.
    """
    def __init__(self, path: Path, *, binding: RealAuthorizationBinding,
                 mode_contract: dict, expected_mode_sha256: str):
        self.path=Path(path).resolve(strict=True)
        require('nonproduction-realtrust-' in str(self.path) and
                self.path.name=='nonproduction_checkpoint_snapshot.json',
                'REAL_CHECKPOINT_ACCESS_FORBIDDEN')
        self.binding=binding.verify_nonexecuting()
        self.mode_contract=json.loads(canonical(mode_contract))
        self.expected_mode_sha256=expected_mode_sha256
        self.verify()

    def verify(self):
        current=safe_read(self.path)
        verify_readonly_checkpoint_binding(current,expected_sha256=self.binding.checkpoint_sha256,
                                           mode_contract=self.mode_contract,
                                           expected_mode_sha256=self.expected_mode_sha256)
        require(self.expected_mode_sha256==self.binding.mode_binding_sha256,
                'REAL_MODE_BINDING_MISMATCH')
        return sha(current)


class ProtectedRealKeyCustodyContract:
    """Design-only production KMS/HSM/keychain adapter, FAIL-CLOSED without it."""
    def sign(self, msg: bytes) -> bytes:
        raise StageStop('PRODUCTION_PROTECTED_REAL_KEY_PROVIDER_NOT_CONNECTED')


class NonproductionRealKeyCustodyEmulator:
    """Distinct REAL-purpose fixture key, never production key; no export API."""
    def __init__(self, *, synthetic_public_sha256: str):
        require(type(synthetic_public_sha256) is str and HEX64.fullmatch(synthetic_public_sha256),'INVALID_SYNTHETIC_KEY_PIN')
        self._private=Ed25519PrivateKey.generate()
        self.public=self._private.public_key()
        self.public_sha256=sha(self.public.public_bytes(Encoding.Raw,PublicFormat.Raw))
        require(self.public_sha256!=synthetic_public_sha256,'SYNTHETIC_REAL_KEY_COLLISION')
        self.environment='REAL_BOUNDARY_NONPRODUCTION_KEY_EMULATOR'
        self.key_id='nonproduction-real-emulation-'+self.public_sha256[:16]

    def sign(self, message: bytes) -> bytes:
        return self._private.sign(message)


@dataclass(frozen=True,slots=True)
class AcceptedValidatorReceipt:
    """Only emitted after the exact pinned accepted validator actually runs."""
    capture: CapturedOSProcess
    checked_payload: dict
    output_sha256: str
    validator_source_sha256: str
    validated_row_count: int
    actual_unit_input_sha256: str
    actual_unit_input_bytes: bytes
    _validator_seal: object


class AcceptedRealValidatorHarness:
    """Calls accepted real semantic function using NONPRODUCTION fixture inputs.

    Trusted caller must supply immutable S04 evidence and manifest; this harness
    NEVER claims synthetic S04 source is authoritative real U0012 evidence.
    """
    def __init__(self, root, supervisor: ControlledFixtureSupervisor, *, fixture_partition,
                 fixture_evidence, fixture_reason):
        self.root=Path(root)
        verify_accepted_validator_source(root)
        self.supervisor=supervisor
        self._seal=object()
        self._receipts={}
        module_path=self.root/'accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py'
        spec=importlib.util.spec_from_file_location('exact_pinned_real_semantic_validator_reference',module_path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._module=module
        # Freeze caller fixture data *before* it is passed to the accepted
        # validator. Fresh deserialization gives the validator its own inputs.
        self._partition_bytes=canonical(fixture_partition)
        self._evidence_bytes=canonical(fixture_evidence)
        self._reason_bytes=canonical(fixture_reason)
        module.verify_manifest(json.loads(self._partition_bytes),json.loads(self._evidence_bytes))

    def validate_observed_fixture(self, capture):
        self.supervisor.verify_capture(capture)
        result={'process_started':True,'return_code':capture.return_code,
                'termination_state':capture.termination_state,'timeout_status':capture.timeout,
                'context_id':capture.invocation_id,
                'agent_message':capture.stdout.decode('utf-8')}
        partition=json.loads(self._partition_bytes)
        evidence=json.loads(self._evidence_bytes)
        reason=json.loads(self._reason_bytes)
        unit=self._module.unit_evidence(partition,evidence,'U0012')
        actual_input_bytes=canonical(unit)
        checked=self._module.validate_semantic_unit(partition,evidence,reason,
                                                    'U0012',result,'PRIMARY')
        require(len(checked['raw_rows'])==25 and len(checked['validated_rows'])==25 and
                tuple(row['authorized_population_position'] for row in checked['raw_rows'])==tuple(range(1776,1801)) and
                [row['canonical_source_identity'] for row in checked['raw_rows']]==
                [row['canonical_source_identity'] for row in unit],
                'REAL_VALIDATOR_POSTCONDITIONS_FAILED')
        checked['row_count']=25
        receipt=AcceptedValidatorReceipt(capture,checked,sha(canonical(checked)),VALIDATOR_SHA,25,
                                         sha(actual_input_bytes),actual_input_bytes,self._seal)
        self._receipts[capture.invocation_id]=receipt
        return receipt

    def verify_receipt(self, receipt, capture):
        require(type(receipt) is AcceptedValidatorReceipt and receipt._validator_seal is self._seal and
                self._receipts.get(capture.invocation_id) is receipt and receipt.capture is capture and receipt.validator_source_sha256==VALIDATOR_SHA and
                receipt.validated_row_count==25 and
                type(receipt.actual_unit_input_bytes) is bytes and
                sha(receipt.actual_unit_input_bytes)==receipt.actual_unit_input_sha256 and
                receipt.actual_unit_input_bytes==canonical(self._module.unit_evidence(
                    json.loads(self._partition_bytes),json.loads(self._evidence_bytes),'U0012')) and
                sha(canonical(receipt.checked_payload))==receipt.output_sha256,
                'CALLER_FORGED_VALIDATOR_PASS_REJECTED')
        return True


@dataclass(frozen=True,slots=True)
class RealBoundProof:
    claims: dict
    sha256: str
    signature_b64: str


class RealBoundaryProofIssuer:
    """Accepts only controlled observed facts and exact stage/readback evidence."""
    def __init__(self, *, capture_supervisor: ControlledFixtureSupervisor, custody: NonproductionRealKeyCustodyEmulator,
                 binding: RealAuthorizationBinding, roots: Path, pinned_public_sha256: str, validator: AcceptedRealValidatorHarness,
                 checkpoint_guard: TrustedFixtureCheckpointGuard):
        verify_accepted_sources(roots)
        self.supervisor=capture_supervisor
        require(type(validator) is AcceptedRealValidatorHarness and validator.supervisor is capture_supervisor,
                'TRUSTED_VALIDATOR_BINDING_REQUIRED')
        self.validator=validator
        require(type(checkpoint_guard) is TrustedFixtureCheckpointGuard and
                checkpoint_guard.binding==binding, 'REAL_CHECKPOINT_TRUST_GUARD_REQUIRED')
        self.checkpoint_guard=checkpoint_guard
        self.custody=custody
        self.binding=binding.verify_nonexecuting()
        require(type(custody) is NonproductionRealKeyCustodyEmulator and
                custody.public_sha256==pinned_public_sha256,'REAL_PUBLIC_KEY_PIN_MISMATCH')
        self._pin=pinned_public_sha256
        self._used=set()

    def issue(self, *, capture: CapturedOSProcess, staged_file: Path, stage_sha256: str,
              readback_sha256: str, validator_receipt: AcceptedValidatorReceipt,
              checkpoint_read_sha256: str, mode_sha256: str, provenance_sha256: str,
              stage_binding=None):
        self.supervisor.verify_capture(capture)
        require(capture.invocation_id not in self._used,'PROOF_REPLAY')
        b=self.binding
        self.validator.verify_receipt(validator_receipt,capture)
        validator_sha256=validator_receipt.validator_source_sha256
        derived_input_sha=validator_receipt.actual_unit_input_sha256
        require(derived_input_sha==sha(validator_receipt.actual_unit_input_bytes) and
                derived_input_sha==b.raw_unit_input_sha256,
                'ACTUAL_INPUT_IDENTITY_MISMATCH')
        require(stage_binding is not None and
                stage_binding.unit_input_sha256==derived_input_sha and
                stage_binding.expected_positions==tuple(range(1776,1801)) and
                stage_binding.expected_identities==tuple(
                    row['canonical_source_identity'] for row in json.loads(validator_receipt.actual_unit_input_bytes)),
                'STAGING_ACTUAL_INPUT_IDENTITY_MISMATCH')
        require(self.checkpoint_guard.verify()==checkpoint_read_sha256==b.checkpoint_sha256,
                'REAL_CHECKPOINT_BINDING_INVALID')
        require(capture.executor_sha256==b.executor_sha256 and
                capture.config_sha256==b.executor_config_sha256,'REAL_EXECUTOR_IMPLEMENTATION_OR_CONFIGURATION_DRIFT')
        require(mode_sha256==b.mode_binding_sha256 and provenance_sha256==b.provenance_sha256,
                'REAL_MODE_PROVENANCE_BINDING_INVALID')
        count=validator_receipt.validated_row_count
        require(type(count) is int and count==25,'INVALID_REAL_VALIDATED_ROW_COUNT')
        require(type(stage_sha256) is str and type(readback_sha256) is str and
                stage_sha256==readback_sha256,'STAGING_READBACK_SHA_MISMATCH')
        raw=safe_read(staged_file)
        require(sha(raw)==stage_sha256 and raw==canonical(validator_receipt.checked_payload),
                'TAMPER_AFTER_STAGING_OR_VALIDATED_CONTENT_SUBSTITUTED')
        require(type(capture.stdout) is bytes and capture.return_code==0,'RAW_EXECUTOR_INVALID')
        claims={
          'PROOF_VERSION':VERSION, 'ISSUER_ENVIRONMENT':self.custody.environment,
          'KEY_ID':self.custody.key_id,'REAL_PUBLIC_KEY_SHA256':self._pin,
          'BATCH_ID':b.batch_id,'ROLE':b.role,'UNIT_ID':b.unit_id,'ATTEMPT_ID':b.attempt_id,
          'CHECKPOINT_SHA256':checkpoint_read_sha256,'UNIT_INPUT_SHA256':derived_input_sha,
          'EXECUTOR_IMPLEMENTATION_SHA256':capture.executor_sha256,
          'EXECUTOR_CONFIGURATION_SHA256':capture.config_sha256,
          'PROCESS_INVOCATION_ID':capture.invocation_id,
          'PROCESS_START_EVENT':capture.process_start_event,'PROCESS_EXIT_EVENT':capture.process_exit_event,
          'PROCESS_RETURN_CODE':capture.return_code,'PROCESS_TERMINATION':capture.termination_state,
          'STDOUT_SHA256':capture.stdout_sha256,'STDERR_SHA256':capture.stderr_sha256,
          'RAW_OUTPUT_SHA256':capture.raw_output_sha256,'TRANSPORT_INTERRUPTION':capture.transport_interrupted,
          'EXTERNAL_AVAILABILITY':capture.external_availability,
          'SEMANTIC_SUBPROCESS_TIMEOUT':capture.timeout,
          'SEMANTIC_EXECUTION_EXCEPTION':capture.termination_state!='NORMAL_SUCCESS',
          'OUTPUT_TRUNCATION':False,
          'MODE':'REAL_MODE_FIXTURE_NONPRODUCTION_ONLY',
          'MODE_BINDING_SHA256':mode_sha256,'PROVENANCE_SHA256':provenance_sha256,
          'CAPTURE_IMPLEMENTATION_SHA256':capture.capture_source_sha256,
          'REAL_VALIDATOR_SHA256':validator_sha256,
          'STAGED_BYTES_SHA256':stage_sha256,'READBACK_SHA256':readback_sha256,
          'EXPECTED_ROW_COUNT':25,'OBSERVED_ROW_COUNT':count,
          'LOCAL_EXACT_AUXILIARY_DIAGNOSTIC_OBSERVED':True,
          'PRIVILEGED_RUNTIME_TELEMETRY_OBSERVED':False,
          'PRIVILEGED_MODELS_MANAGER_PROVENANCE_OBSERVED':False,
          'AUTHORITATIVE_SERVICE_SIDE_TRANSPORT_STATUS_OBSERVED':False,
          'V7_V2_POLICY_SHA256':POLICY_SHA,'V7_V2_CLASSIFIER_SOURCE_SHA256':CLASSIFIER_SHA,
          'ISSUER_IMPLEMENTATION_SHA256':sha(Path(__file__).read_bytes()),
          'SESSION_NONCE':capture.session_nonce,
        }
        encoded=canonical(claims)
        proof=RealBoundProof(claims,sha(encoded),base64.b64encode(self.custody.sign(encoded)).decode('ascii'))
        self._used.add(capture.invocation_id)
        return proof

    def verify(self, proof: RealBoundProof, *, capture: CapturedOSProcess, staged_file: Path,
               checkpoint_read_sha256: str, mode_sha256: str, provenance_sha256: str,
               validator_receipt: AcceptedValidatorReceipt, stage_binding=None):
        self.validator.verify_receipt(validator_receipt,capture)
        derived_input_sha=validator_receipt.actual_unit_input_sha256
        require(derived_input_sha==sha(validator_receipt.actual_unit_input_bytes) and
                derived_input_sha==self.binding.raw_unit_input_sha256 and
                stage_binding is not None and
                stage_binding.unit_input_sha256==derived_input_sha,
                'ACTUAL_INPUT_OR_STAGING_BINDING_CHANGED')
        require(safe_read(staged_file)==canonical(validator_receipt.checked_payload),
                'STAGED_CONTENT_NOT_VALIDATED')
        require(type(proof) is RealBoundProof,'CALLER_CREATED_UNTRUSTED_PROOF')
        self.supervisor.verify_capture(capture)
        require(type(proof.claims) is dict and type(proof.sha256) is str,'PROOF_SHAPE_INVALID')
        claims=proof.claims
        require(sha(canonical(claims))==proof.sha256,'PROOF_DIGEST_INVALID')
        try:self.custody.public.verify(base64.b64decode(proof.signature_b64,validate=True),canonical(claims))
        except (InvalidSignature,ValueError) as ex:raise StageStop('PROOF_SIGNATURE_INVALID') from ex
        b=self.binding
        require(self.checkpoint_guard.verify()==checkpoint_read_sha256,
                'CHECKPOINT_CHANGED_BEFORE_PROOF_VERIFICATION')
        expected={
          'ISSUER_ENVIRONMENT':self.custody.environment,'KEY_ID':self.custody.key_id,
          'REAL_PUBLIC_KEY_SHA256':self._pin,'PROOF_VERSION':VERSION,
          'BATCH_ID':b.batch_id,'ROLE':b.role,'UNIT_ID':b.unit_id,'ATTEMPT_ID':b.attempt_id,
          'CHECKPOINT_SHA256':checkpoint_read_sha256,'UNIT_INPUT_SHA256':derived_input_sha,
          'PROCESS_INVOCATION_ID':capture.invocation_id,'PROCESS_START_EVENT':capture.process_start_event,
          'PROCESS_EXIT_EVENT':capture.process_exit_event,'PROCESS_RETURN_CODE':capture.return_code,
          'PROCESS_TERMINATION':capture.termination_state,'EXECUTOR_IMPLEMENTATION_SHA256':capture.executor_sha256,
          'EXECUTOR_CONFIGURATION_SHA256':capture.config_sha256,'STDOUT_SHA256':capture.stdout_sha256,
          'STDERR_SHA256':capture.stderr_sha256,'RAW_OUTPUT_SHA256':capture.raw_output_sha256,
          'TRANSPORT_INTERRUPTION':False,'EXTERNAL_AVAILABILITY':False,
          'SEMANTIC_SUBPROCESS_TIMEOUT':False,'SEMANTIC_EXECUTION_EXCEPTION':False,
          'OUTPUT_TRUNCATION':False,
          'MODE':'REAL_MODE_FIXTURE_NONPRODUCTION_ONLY','MODE_BINDING_SHA256':mode_sha256,
          'PROVENANCE_SHA256':provenance_sha256,'CAPTURE_IMPLEMENTATION_SHA256':capture.capture_source_sha256,
          'REAL_VALIDATOR_SHA256':VALIDATOR_SHA, 'STAGED_BYTES_SHA256':sha(safe_read(staged_file)),
          'READBACK_SHA256':sha(safe_read(staged_file)),
          'EXPECTED_ROW_COUNT':25,'OBSERVED_ROW_COUNT':25,
          'LOCAL_EXACT_AUXILIARY_DIAGNOSTIC_OBSERVED':True,
          'PRIVILEGED_RUNTIME_TELEMETRY_OBSERVED':False,
          'PRIVILEGED_MODELS_MANAGER_PROVENANCE_OBSERVED':False,
          'AUTHORITATIVE_SERVICE_SIDE_TRANSPORT_STATUS_OBSERVED':False,
          'V7_V2_POLICY_SHA256':POLICY_SHA,
          'V7_V2_CLASSIFIER_SOURCE_SHA256':CLASSIFIER_SHA,
          'ISSUER_IMPLEMENTATION_SHA256':sha(Path(__file__).read_bytes()),
          'SESSION_NONCE':capture.session_nonce,
        }
        require(set(claims)==set(expected) and all(type(claims[k]) is type(v) and claims[k]==v for k,v in expected.items()),
                'PROOF_BINDING_REPLAY_OR_SUBSTITUTION')
        require(checkpoint_read_sha256==b.checkpoint_sha256 and mode_sha256==b.mode_binding_sha256 and
                provenance_sha256==b.provenance_sha256,'FRESH_CHECKPOINT_OR_MODE_DRIFT')
        return True


def verify_accepted_validator_source(root):
    """Exact REAL semantic validator implementation is referenced, never replaced."""
    root=Path(root)
    validator=root/'accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py'
    frozen_v3=validator.parent/'frozen_v3_orchestrator_reference.py'
    require(sha(safe_read(validator))==VALIDATOR_SHA and sha(safe_read(frozen_v3))==V3_SHA,
            'ACCEPTED_REAL_VALIDATOR_DRIFT')
    return True


def verify_readonly_checkpoint_binding(snapshot_bytes: bytes, *, expected_sha256: str,
                                       mode_contract: dict, expected_mode_sha256: str):
    """Only a snapshot supplied by an isolated nonproduction test is supported.

    REAL activation must reread actual persisted checkpoint via accepted engine,
    under trusted runner before dispatch AND before append-only acceptance.
    """
    require(type(snapshot_bytes) is bytes and sha(snapshot_bytes)==expected_sha256,'FRESH_CHECKPOINT_DRIFT')
    require(type(mode_contract) is dict and mode_contract.get('execution_mode')=='REAL' and
            mode_contract.get('engine_mode')=='REAL' and mode_contract.get('adapter_mode')=='REAL' and
            mode_contract.get('authorization_mode')=='REAL' and mode_contract.get('expected_provenance_mode')=='REAL',
            'REAL_MODE_PROVENANCE_DRIFT')
    require(sha(canonical(mode_contract))==expected_mode_sha256,'REAL_MODE_CONTRACT_HASH_DRIFT')
    require(mode_contract.get('max_new_units')==1 and mode_contract.get('unit_id')=='U0012',
            'U0013_OR_MULTIPLE_UNIT_DISPATCH')
    return True


def production_activation(*args, **kwargs):
    raise StageStop('REAL_ACTIVATION_NOT_AUTHORIZED__NO_DISPATCH_NO_CHECKPOINT_MUTATION')


def classify_bound_nonproduction_fixture(issuer: RealBoundaryProofIssuer,proof: RealBoundProof,
                                         capture: CapturedOSProcess,stage,receipt: AcceptedValidatorReceipt,
                                         *, checkpoint_sha256: str, mode_sha256: str,
                                         provenance_sha256: str):
    """Only creates a PROSPECTIVE verdict. No real freeze or checkpoint mutation."""
    from trusted_stage.staging_v1 import verify_stage
    issuer.verify(proof,capture=capture,staged_file=stage.file,
                  checkpoint_read_sha256=checkpoint_sha256,mode_sha256=mode_sha256,
                  provenance_sha256=provenance_sha256,validator_receipt=receipt,
                  stage_binding=stage.binding)
    require(verify_stage(stage) == canonical(receipt.checked_payload),
            'STAGED_BYTES_DIVERGED_FROM_REAL_VALIDATOR')
    result={'process_started':True,'return_code':capture.return_code,
            'termination_state':capture.termination_state,'timeout_status':capture.timeout,
            'context_id':capture.invocation_id,'raw_stdout':capture.stdout.decode('utf8'),
            'raw_stderr':capture.stderr.decode('utf8'),
            'agent_message':capture.stdout.decode('utf8')}
    integ=v7.VerifiedOperationalIntegrity(
        expected_rows=25,observed_rows=receipt.validated_row_count,complete_output=True,
        output_schema_valid=True,identities_valid=True,positions_valid=True,
        serialization_readback_pass=True,semantic_subprocess_timeout=False,
        semantic_execution_exception=False,output_truncation=False,
        transport_interruption=capture.transport_interrupted,
        external_availability_present=capture.external_availability,
        # V7 V2's existing source_attested interface is satisfied by a trusted
        # LOCAL exact diagnostic observation only AFTER signed proof, OS capture,
        # validator, checkpoint, stage and readback verification. It does NOT
        # assert privileged provider-internal event provenance.
        source_attested=(proof.claims['LOCAL_EXACT_AUXILIARY_DIAGNOSTIC_OBSERVED'] is True and
                         proof.claims['PRIVILEGED_RUNTIME_TELEMETRY_OBSERVED'] is False and
                         proof.claims['PRIVILEGED_MODELS_MANAGER_PROVENANCE_OBSERVED'] is False and
                         proof.claims['AUTHORITATIVE_SERVICE_SIDE_TRANSPORT_STATUS_OBSERVED'] is False))
    verdict=v7.decide_availability(result,integrity=integ)
    require(verdict['decision']=='NO_EXTERNAL_SIGNAL' and
            verdict['classification']=='NONBLOCKING_AUXILIARY_EXECUTOR_DIAGNOSTIC' and
            verdict['conflict_evidence']==[] and verdict['hard_stop_classes']==[] and
            verdict['historical_v6_verdict']['decision']=='CONTROLLED_STOP',
            'REAL_BOUNDARY_V7_CLASSIFICATION_STOP')
    return verdict
