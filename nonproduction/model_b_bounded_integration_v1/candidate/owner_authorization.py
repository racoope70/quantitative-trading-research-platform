"""Exact Owner readback/consumption adapter; no key or signer derivation.

Authority comes from the existing root-owned publication boundary. The old
protected NONPRODUCTION document supplies reference deployment identities only;
it is already consumed and is never used to authorize another execution.
"""
from pathlib import Path
import ast,copy,json,os
import owner_publication as publication

DEPLOY=Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1')
REAL_CHECKPOINT=Path('/Users/richardcooper/Downloads/batch0004_REAL_S05_BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F_PRIMARY_checkpoint')
REFERENCE_ROOT=Path('/private/var/db/qtrp-owner-auth-nonproduction-v1')
REFERENCE_SHA='cd990c2a8f03c1c20e407fd21892c9ef95b458c759ef7ac2588115a510958d22'
REFERENCE_LENGTH=48028
need=publication.need
canonical=publication.canonical
digest=publication.digest
_LOADED_SOURCE_SHA256=digest(Path(__file__).read_bytes())

# Finalized in dependency order before installation; no configuration digest here.
PROSPECTIVE_SOURCE_PINS = {'owner_publication.py': '6783256282e150076288454d5dec09fa3732d0008e667fd42dbbde6066031fe7', 'prospective_adapter_v1.py': 'f7c89bd4e497086b91f2dc26310680dcf373a04be4e20b4bbfe92372e18241bb', 'real_candidate/activation_v1.py': 'ace4a82dc33f39caf9a79884f0165a94f97a224011537edaccd529e537b5c41a', 'real_candidate/capture_v1.py': 'd8cdd455ba90552334eed1cba9df484d99fe0fdb5ed3dc8005309f7aa399ddf7', 'real_candidate/checkpoint_v1.py': 'fe8dccdbb2d6215d9e36e226f8e1e0b5986622a2231adf4ceee9903516f5e155', 'real_candidate/engine_v1.py': '11b79292d48c9103dde04f5a04f775515a4b84a107142691fadffff83ad52abd', 'real_candidate/executor_v1.py': 'fae7907da55a84540a0411df7558ee42bb2c1b55f7efcfd6f99e9a1c32b2deb9', 'real_candidate/policy_b_events_v1.py': '52e0448e6c4a2b69301346cb7741e889b501d50092b1c184d79233338e1ad1d2', 'real_candidate/policy_b_proof_v1.py': '8cfc5c2e455b9fdcadf1832dcce84b1379d1075664177ae82426b6bba2e5dfba', 'real_candidate/policy_b_validation_v1.py': '6dba4b8796c6437cf5f8f94fbd4c10d0e6eda5e36f546f816ce0f4742ca4371e', 'real_candidate/proof_issuer_v1.py': 'b79ad20faf776c2b838f2edbca2a19ef8704284d9bb530e87cbadcf3ea1b1bb8', 'real_candidate/proof_path_v1.py': '4471adbadbc03e788bde4d0bf24dca5627631e1e987779ab379257b0b8cfad34', 'real_candidate/real_binding_v1.py': 'b41d5a33f1bfda759c7549936f0340c77aa1a85329ce304e96190de549a8ff0e', 'real_candidate/release_v1.py': '20efd0e2ea60eaf9e0e592dd2e2e178eff2241ea35180260b8988b65d022ef9a', 'real_candidate/validation_v1.py': '9293273b70b153adea9034e60d98de900cbcb91f56a3fe2c367c1acd7d4a844e', 'recovery_bounded_v4.py': 'aeed2b56deea5960a97553604ea45c9d15c096c2575afabf11dc132465e56ca8'}
SUPERSEDING_RELEASE_SHA = '7151bbbbd4b41dccdceff20d48abd445ed882e7682a7efef7f670594b35f1c1b'
PROSPECTIVE_BINDING_SHA = 'b4dce0c0d76d7ae2608ca06de17c97ebd3ca91fd0e3924a0f93b3837a86b1cca'
MANIFEST_FILE = 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json'
COMPATIBILITY_SOURCE_PINS = {'owner_publication.py': '996cee63f8b23b5685d7fd8beafcb38dadaef48208a0f28532720b4cdb3c4471', 'prospective_adapter_v1.py': '2315601c2f83fa18107257025ec94ef85d65b12c7a38e4a2c44066d77d3723ac', 'real_candidate/activation_v1.py': '6b473d6b272088ac635ff0981a4a82f88e634d75e3a47fc6730ceb49261bc385', 'real_candidate/capture_v1.py': 'c96e082ccbea70da28efac448583566b70ac3fbba74a2fd5292462801442cb6b', 'real_candidate/checkpoint_v1.py': 'b6f73e6c5b5f000c89cc665e75006f37c2ff6fa24be85e867b16a2f0d4d4aa3e', 'real_candidate/engine_v1.py': '64cccf083cd036d78345b2b96971353c135b300afcaa20c670bc8dbde0a26e60', 'real_candidate/executor_v1.py': '7254dba7a9cd153d3f8aea2ff4605ae5631541297fdb4071c75cea71f5cde07c', 'real_candidate/policy_b_events_v1.py': '52e0448e6c4a2b69301346cb7741e889b501d50092b1c184d79233338e1ad1d2', 'real_candidate/policy_b_proof_v1.py': '5f082cf22f78d886cb143b622988a9e8a22b4581e46c85160b941ddae7b8d553', 'real_candidate/policy_b_validation_v1.py': '6dba4b8796c6437cf5f8f94fbd4c10d0e6eda5e36f546f816ce0f4742ca4371e', 'real_candidate/proof_issuer_v1.py': 'b79ad20faf776c2b838f2edbca2a19ef8704284d9bb530e87cbadcf3ea1b1bb8', 'real_candidate/proof_path_v1.py': '4471adbadbc03e788bde4d0bf24dca5627631e1e987779ab379257b0b8cfad34', 'real_candidate/real_binding_v1.py': 'b41d5a33f1bfda759c7549936f0340c77aa1a85329ce304e96190de549a8ff0e', 'real_candidate/release_v1.py': '50e735a712dcf0a7a44ba75cd9d99823c89c7404bc97acf7f071303627347cd3', 'real_candidate/validation_v1.py': '9293273b70b153adea9034e60d98de900cbcb91f56a3fe2c367c1acd7d4a844e', 'recovery_bounded_v4.py': 'c00c215876270594c4a3b197c62a19f288ff6f3e8be40e80709bd4ab29cf97be', 'membership_readonly.py': '4afebb18b53fa0985dabcf10b56d08427334096c3223fc5b1a7a9698aa79884c'}
COMPATIBILITY_RELEASE_SHA = '0b12fe4dd4dc07fe1e3163a0f6b4e8d3745ade96bd68757149bd577052962bd9'
COMPATIBILITY_BINDING_SHA = 'f9879f8062e291121a8c9e4710c6358d647025c18b2689764840a23790e2d87c'

def _superseding_target(reference, *, candidate_nonproduction=False, prospective_a11=False,
                        expected_configuration_sha256=None):
    """Derive the prospective subject from immutable lineage and actual bytes."""
    need(type(prospective_a11) is bool and not (prospective_a11 and candidate_nonproduction),
         'PROSPECTIVE_A11_SELECTOR')
    if prospective_a11:
        if reference:
            return prospective_a11_target(reference,
                expected_configuration_sha256=expected_configuration_sha256)
        return _prospective_a11_identity_target(reference)
    if candidate_nonproduction:
        return _nonproduction_compatibility_target(reference)
    root=Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1')
    own=root/'candidate/owner_authorization.py'
    need(Path(__file__).resolve()==own.resolve(),'CORRECTED_AUTHORIZATION_PATH_DRIFT')
    own_sha=digest(own.read_bytes())
    need(own_sha==_LOADED_SOURCE_SHA256,'LOADED_AUTHORIZATION_SOURCE_DRIFT')
    selected=dict(PROSPECTIVE_SOURCE_PINS);selected['owner_authorization.py']=own_sha
    expected={'SOURCE_SHA256':selected,'RELEASE_SHA':SUPERSEDING_RELEASE_SHA,
        'RECOVERY_SHA':selected['recovery_bounded_v4.py'],
        'RECOVERY_BINDING_SHA':PROSPECTIVE_BINDING_SHA,
        'REFERENCE_RELEASE_SHA':'00d35a429b23e3967478778f9c28c1265fd25dad0f0da5d7feba55d0a6fb9260',
        'REFERENCE_BINDING_SHA':'2ce533284245735e960c6e3694bf9f9abf8b8bb30fcff1b32da0970f2e79994e',
        'CHECKPOINT_SHA':'379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe'}
    source=(root/'composition.py').read_bytes();constants={}
    for node in ast.parse(source).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in expected:
                need(name not in constants,'DUPLICATE_COMPOSITION_BINDING')
                constants[name]=ast.literal_eval(node.value)
    need(constants==expected,'CORRECTED_COMPOSITION_BINDING_DRIFT')
    for name,pin in selected.items():
        need(digest((root/'candidate'/name).read_bytes())==pin,'CORRECTED_SOURCE_DRIFT__'+name)
    raw=(root/MANIFEST_FILE).read_bytes();need(digest(raw)==SUPERSEDING_RELEASE_SHA,'CORRECTED_RELEASE_DRIFT')
    descriptor=json.loads(raw)
    compatibility=(root/'candidate/recovery_compatibility_bounded_v4.json').read_bytes()
    need(digest(compatibility)==PROSPECTIVE_BINDING_SHA,'CORRECTED_RECOVERY_BINDING_DRIFT')
    cfg=copy.deepcopy(reference['base_deployment_configuration'])
    runtime=root/'runtime'
    operation=runtime/'operational_evidence_attempt10_policy_b_v1'
    work=operation/'executor_work';stage=operation/'unit_transaction'
    directory=work/'PRIMARY/U0012/A0010/input'
    transport=copy.deepcopy(cfg['transport'])
    transport['scientific_file_sizes']={name:(Path(transport['scientific_directory'])/name).stat().st_size
        for name in transport['scientific_files_sha256']}
    argv=list(transport['scientific_argv']);argv[argv.index('-C')+1]=str(directory)
    native=transport['executable_chain']['codex_native']
    transport['scientific_directory']=str(directory);transport['scientific_argv']=argv
    transport['target_argv']=[native['path'],*argv]
    transport['reference_guard_sha256']=transport.pop('guard_sha256')
    transport['input_delivery']='FILE_IDENTITY_FRAME'
    capture={'executable':native['path'],'argv':argv,'cwd':str(runtime),'env':cfg['capture_environment'],
             'adapter_sha256':selected['prospective_adapter_v1.py'],'mode':'REAL',
             'max_output_bytes':16*1024*1024,'input_delivery':'FILE_IDENTITY_FRAME',
             'timeout_policy':{'policy':'OWNER_OPTION_B_POST_POPEN_CAPTURE_V1',
                'prelaunch_budget_seconds':1800,'post_popen_capture_budget_seconds':300,
                'popen_strictly_interruptible':False,'total_transaction_ceiling_seconds':None}}
    cfg.update(timeout_policy=copy.deepcopy(capture['timeout_policy']),
        release_sha256=SUPERSEDING_RELEASE_SHA,accepted_components=descriptor,
        recovery_sha256=expected['RECOVERY_SHA'],recovery_compatibility_binding_sha256=PROSPECTIVE_BINDING_SHA,
        recovery_binding=json.loads(compatibility),composition_source_sha256=digest(source),
        selected_source_sha256=selected,reference_release_sha256=expected['REFERENCE_RELEASE_SHA'],
        reference_deployment_binding_sha256=expected['REFERENCE_BINDING_SHA'],transport=transport,
        capture_executable=native['path'],capture_argv=argv,capture_cwd=str(runtime),
        capture_configuration_sha256=digest(canonical(capture)),
        scientific_directory_identity=digest(canonical({'path':str(directory),'files':transport['scientific_files_sha256']})),
        prospective_executor_sha256=selected['real_candidate/executor_v1.py'],
        prospective_executor_interface_sha256=selected['prospective_adapter_v1.py'],
        historical_corrected_release_sha256='1b1f9e867cb921910031fa7fba6296c31808df4da627f6eefed1fd0b26f79a93',
        historical_corrected_configuration_sha256='e253311696cc1a05d6232a422ffc4c6cf1d8ff8b9a71e7320437744cc194fea6',
        operational_context={'work_root':str(work),'stage_root':str(stage),
            'durable_root':str(stage/'U0012/A0010'),
            'failure_root':str(work/'PRIMARY/U0012/A0010/v3_executor_raw_evidence'),
            'writing_uid':501,'writing_euid':501,
            'controller_confinement':'HOST_UID501_SOURCE_BOUND__CHILD_READ_ONLY',
            'max_output_bytes':16*1024*1024,'max_new_units':1,'attempt_ordinal':10,'u0013_prohibited':True},
        proof_interface='PolicyBProofPath; independent complete-occurrence/scientific reconstruction; Owner publication remains separate',
        scientific_acceptance_contract='POLICY_B_EXACT_COMPLETE_MESSAGE_VALUE_V1',
        policy_b_sha256=descriptor['new_integration_components']['POLICY_B_POLICY']['sha256'])
    target=copy.deepcopy(reference)
    target['protected_reference']={'authorization_sha256':REFERENCE_SHA,'authorization_length':REFERENCE_LENGTH,
        'target_authorization':copy.deepcopy(reference)}
    target.pop('deployment_manifest_sha256');target.pop('signer')
    target.update(project='QUANTITATIVE_TRADING_RESEARCH_PLATFORM',batch='BATCH0004',role='PRIMARY',phase='S05',
        attempt_id=publication.REAL_ATTEMPT,checkpoint_sequence=reference['checkpoint_head']['sequence'],
        base_deployment_configuration=cfg,deployment_identity=digest(canonical(cfg)))
    target.update(checkpoint_sequence=52,checkpoint_head={'checkpoint_manifest_sha256': '379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe', 'sequence': 52, 'snapshot_file': 'checkpoint_000052.json', 'snapshot_file_sha256': '26b4005ffab3b554d416b8bb65501ff9d79b118b7be59b5cb87db1d275f6e1a6'},checkpoint_identity='379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe',historical_attempt_count=9,historical_attempts=json.loads(compatibility)['historical_attempts'],next_attempt_sequence=10)
    cfg['checkpoint'].update(checkpoint_identity=target['checkpoint_identity'],historical_attempt_count=9,historical_attempts=copy.deepcopy(target['historical_attempts']))
    target['deployment_identity']=digest(canonical(cfg))
    target['authorization_policy']={key:target[key] for key in
        ('project','batch','role','phase','unit_id','attempt_id','next_attempt_sequence','historical_attempt_count',
         'max_new_units','u0013_prohibited','single_use','replay_protected','environment','activation_gate')}
    target['authorization_policy'].update(scope=publication.REAL_SCOPE,
        timeout_policy=copy.deepcopy(cfg['timeout_policy']),
        execution_contract=descriptor['owner_authorized_execution_contract'],
        accessible_trust_policy_sha256=descriptor['accepted_components']['ACCESSIBLE_TRUST_POLICY']['sha256'],
        scientific_policy_sha256=descriptor['accepted_components']['V7_V2_POLICY']['sha256'],
        scientific_result_value_policy_sha256=descriptor['new_integration_components']['POLICY_B_POLICY']['sha256'])
    target['authorization_policy_sha256']=digest(canonical(target['authorization_policy']))
    return target


def _nonproduction_compatibility_target(request):
    """Candidate-only environment derivation; no protected reference or grant."""
    from real_candidate.capture_v1 import (
        COMPATIBILITY_CANDIDATE_ROOT, PINNED_PYTHON, PINNED_PYTHON_SHA256,
        task_python_compatibility, PRELAUNCH_BUDGET_SECONDS,
        CHILD_CAPTURE_BUDGET_SECONDS, TIMEOUT_POLICY,
    )
    root = Path('/private/tmp/QTRP_BATCH0004_C06_TO_A11_READINESS_CANDIDATE_V1')
    need(COMPATIBILITY_CANDIDATE_ROOT == root, 'COMPATIBILITY_CANDIDATE_ROOT')
    need(Path(__file__).resolve() == root / 'candidate/owner_authorization.py',
         'COMPATIBILITY_CANDIDATE_OWNER_SOURCE')
    need(type(request) is dict and set(request) == {'argv'}, 'COMPATIBILITY_SYNTHETIC_REQUEST')
    argv = request['argv']
    need(type(argv) is tuple and len(argv) == 3 and argv[:2] == ('-I', '-c')
         and type(argv[2]) is str, 'COMPATIBILITY_SYNTHETIC_ARGV')
    own_sha = digest(Path(__file__).read_bytes())
    need(own_sha == _LOADED_SOURCE_SHA256, 'LOADED_AUTHORIZATION_SOURCE_DRIFT')
    raw = (root / MANIFEST_FILE).read_bytes()
    descriptor = json.loads(raw)
    need(raw == canonical(descriptor) and digest(raw) == COMPATIBILITY_RELEASE_SHA
         and (root / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256').read_bytes() ==
         (COMPATIBILITY_RELEASE_SHA + '\n').encode(), 'COMPATIBILITY_CANDIDATE_RELEASE')
    need(descriptor['release_is_approved_for_real_use'] is False
         and descriptor['real_activation_eligible'] is False
         and descriptor['production_activation_gate'] == 'HARD_DISABLED',
         'COMPATIBILITY_NONPRODUCTION_RELEASE_REQUIRED')
    for name in ('real_candidate/capture_v1.py', 'recovery_bounded_v4.py'):
        need(digest((root / 'candidate' / name).read_bytes()) == COMPATIBILITY_SOURCE_PINS[name],
             'COMPATIBILITY_CANDIDATE_SOURCE_DRIFT')
    need(descriptor['new_integration_components']['CAPTURE_V1']['sha256'] ==
         COMPATIBILITY_SOURCE_PINS['real_candidate/capture_v1.py']
         and descriptor['prospective_components']['RECOVERY']['sha256'] ==
         COMPATIBILITY_SOURCE_PINS['recovery_bounded_v4.py'], 'COMPATIBILITY_CANDIDATE_RELEASE')
    compatibility = (root / 'candidate/recovery_compatibility_bounded_v4.json').read_bytes()
    need(digest(compatibility) == COMPATIBILITY_BINDING_SHA ==
         descriptor['prospective_components']['RECOVERY_COMPATIBILITY']['sha256']
         and json.loads(compatibility)['prospective_source_sha256']['real_candidate/capture_v1.py'] ==
         COMPATIBILITY_SOURCE_PINS['real_candidate/capture_v1.py'],
         'COMPATIBILITY_CANDIDATE_RECOVERY_BINDING')
    specification = task_python_compatibility()
    environment = {'__CF_USER_TEXT_ENCODING': f'0x{os.getuid():X}:0x0:0x0',
                   'HOME': str(root / 'task_runtime'),
                   'PATH': specification['path']['prefix'] + ':' + specification['path']['remainder'],
                   'PAGER': 'cat', 'GIT_PAGER': 'cat', 'LANG': 'C.UTF-8', 'LC_ALL': 'C',
                   'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'}
    binding = {'release_sha256': COMPATIBILITY_RELEASE_SHA,
               'owner_source_sha256': own_sha,
               'composition_source_sha256': digest((root / 'composition.py').read_bytes())}
    capture = {'executable': str(PINNED_PYTHON), 'argv': argv,
               'cwd': str(root / 'task_runtime'), 'env': environment,
               'adapter_sha256': COMPATIBILITY_SOURCE_PINS['prospective_adapter_v1.py'],
               'mode': 'NONPRODUCTION_TEST', 'max_output_bytes': 16384,
               'input_delivery': 'STDIN', 'runtime_compatibility': specification,
               'candidate_binding': binding,
               'timeout_policy': {'policy': TIMEOUT_POLICY,
                   'prelaunch_budget_seconds': PRELAUNCH_BUDGET_SECONDS,
                   'post_popen_capture_budget_seconds': CHILD_CAPTURE_BUDGET_SECONDS,
                   'popen_strictly_interruptible': False, 'total_transaction_ceiling_seconds': None}}
    cfg = {'execution_mode': 'NONPRODUCTION_TEST', 'unit_id': 'U0012', 'max_new_units': 1,
           'u0013_prohibited': True, 'real_activation': 'HARD_DISABLED',
           'release_sha256': COMPATIBILITY_RELEASE_SHA, 'capture': capture,
           'capture_environment': environment, 'transport': {'environment': copy.deepcopy(environment)},
           'capture_configuration_sha256': digest(canonical(capture)),
           'environment_identity': digest(canonical(environment)),
           'composition_source_sha256': binding['composition_source_sha256'],
           'selected_source_sha256': {**COMPATIBILITY_SOURCE_PINS, 'owner_authorization.py': own_sha}}
    return {'environment': 'SYNTHETIC_NONPRODUCTION', 'real_execution_authorized': False,
            'base_deployment_configuration': cfg, 'deployment_identity': digest(canonical(cfg))}

def _prospective_a11_identity_target(request):
    """Exact inert technical identity; never a capture or authorization document.

    Scientific/checkpoint/capture-command inputs and the Attempt11 publication
    contract remain separate mandatory readiness gates. No REAL API is called.
    """
    from real_candidate.capture_v1 import (
        COMPATIBILITY_CANDIDATE_ROOT, PROSPECTIVE_A11_RUNTIME_ROOT,
        task_python_compatibility,
    )
    from real_candidate.release_v1 import verify_release
    engineering = Path('/private/tmp/QTRP_BATCH0004_C06_TO_A11_READINESS_CANDIDATE_V1')
    future = Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a11_u0012_attempt11_runtime_v1')
    source = Path(__file__)
    need(source.absolute() == source.resolve() and source.resolve() in (
        engineering / 'candidate/owner_authorization.py',
        future / 'candidate/owner_authorization.py'), 'PROSPECTIVE_A11_SOURCE_LOCATION')
    local = source.resolve().parent.parent
    need(COMPATIBILITY_CANDIDATE_ROOT == engineering and PROSPECTIVE_A11_RUNTIME_ROOT == future,
         'PROSPECTIVE_A11_ROOT_BINDING')
    need(type(request) is dict and request == {}, 'PROSPECTIVE_A11_REQUEST_OVERRIDES_FORBIDDEN')
    own_sha = digest(source.read_bytes())
    need(own_sha == _LOADED_SOURCE_SHA256, 'LOADED_AUTHORIZATION_SOURCE_DRIFT')
    need(verify_release(local) == COMPATIBILITY_RELEASE_SHA, 'PROSPECTIVE_A11_RELEASE_IDENTITY')
    raw = (local / MANIFEST_FILE).read_bytes()
    descriptor = json.loads(raw)
    pin = (local / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256').read_bytes()
    need(raw == canonical(descriptor) and digest(raw) == COMPATIBILITY_RELEASE_SHA
         and pin == (COMPATIBILITY_RELEASE_SHA + '\n').encode(), 'PROSPECTIVE_A11_RELEASE_IDENTITY')
    need(descriptor['production_activation_gate'] == 'HARD_DISABLED'
         and descriptor['release_is_approved_for_real_use'] is False
         and descriptor['real_activation_eligible'] is False
         and descriptor['real_authorization_prepared'] is False,
         'PROSPECTIVE_A11_NONACTIVATING_RELEASE_REQUIRED')
    for relative, expected in COMPATIBILITY_SOURCE_PINS.items():
        need(digest((local / 'candidate' / relative).read_bytes()) == expected,
             'PROSPECTIVE_A11_SOURCE_IDENTITY_DRIFT')
    compatibility = (local / 'candidate/recovery_compatibility_bounded_v4.json').read_bytes()
    need(digest(compatibility) == COMPATIBILITY_BINDING_SHA
         and json.loads(compatibility)['prospective_source_sha256']['real_candidate/capture_v1.py']
         == COMPATIBILITY_SOURCE_PINS['real_candidate/capture_v1.py'],
         'PROSPECTIVE_A11_RECOVERY_IDENTITY_DRIFT')
    specification = task_python_compatibility(prospective_a11=True)
    environment = {'__CF_USER_TEXT_ENCODING': f'0x{os.getuid():X}:0x0:0x0',
                   'HOME': str(future / 'task_runtime'),
                   'PATH': specification['path']['prefix'] + ':' + specification['path']['remainder'],
                   'PAGER': 'cat', 'GIT_PAGER': 'cat', 'LANG': 'C.UTF-8', 'LC_ALL': 'C',
                   'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'}
    selected = {**COMPATIBILITY_SOURCE_PINS, 'owner_authorization.py': own_sha}
    locations = {'composition.py': str(future / 'composition.py'),
                 **{'candidate/' + relative: str(future / 'candidate' / relative) for relative in selected}}
    configuration = {'execution_mode': 'REAL', 'unit_id': 'U0012', 'max_new_units': 1,
        'u0013_prohibited': True, 'real_activation': 'HARD_DISABLED',
        'runtime_root': str(future), 'release_sha256': COMPATIBILITY_RELEASE_SHA,
        'release_descriptor_path': str(future / MANIFEST_FILE),
        'detached_pin_path': str(future / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256'),
        'detached_pin_sha256': digest(pin),
        'capture_environment': environment, 'environment_identity': digest(canonical(environment)),
        'transport': {'environment': copy.deepcopy(environment)},
        'runtime_compatibility': specification, 'python_compatibility_identity': digest(canonical(specification)),
        'composition_source_sha256': digest((local / 'composition.py').read_bytes()),
        'selected_source_sha256': selected, 'source_locations': locations,
        'launch_entrypoint': {'qualified_name': 'real_candidate.activation_v1.run_owner_real_domain',
            'release_root': str(future),
            'source_sha256': descriptor['new_integration_components']['ACTIVATION_V1']['sha256'],
            'owner_contract': descriptor['owner_authorized_execution_contract'],
            'launch_permission': 'HARD_DISABLED'}}
    return {'environment': 'INERT_PROSPECTIVE_REAL', 'real_execution_authorized': False,
            'configuration_scope': 'A11_TECHNICAL_IDENTITY_SPECIFICATION_ONLY',
            'execution_configuration_complete': False,
            'base_deployment_configuration': configuration,
            'deployment_identity': digest(canonical(configuration))}

def fsync_directory(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)

def _read_protected(root,expected_sha,expected_length,scope):
    need(type(expected_sha) is str and len(expected_sha)==64 and set(expected_sha)<=set('0123456789abcdef')
         and type(expected_length) is int and expected_length>0,'BAD_PUBLICATION_ID')
    directory=Path(root)/expected_sha
    fd=publication.open_root_chain(directory)
    try:
        complete=publication.completion_receipt(expected_sha,expected_length,scope=scope)
        marker=os.open('publication_complete.json',os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        try:need(publication.read_snapshot(marker,len(complete),0,0o444)==complete,'PUBLICATION_COMPLETION_RECEIPT_MISMATCH')
        finally:os.close(marker)
        item=os.open('authorization.json',os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        try:raw=publication.read_snapshot(item,expected_length,0,0o444)
        finally:os.close(item)
    finally:os.close(fd)
    need(digest(raw)==expected_sha,'PUBLICATION_HASH_MISMATCH')
    doc=publication.validate_owner_document(raw)
    need(doc['scope']==scope,'CROSS_DOMAIN_PUBLICATION_REJECTED')
    return doc

def prospective_a11_target(reference, *, expected_configuration_sha256):
    """Pure technical comparison against independently supplied expectations.

    This is not an authorization or a current-content declaration. The caller
    must obtain the expectation independently of any submitted Owner document.
    No runtime, scientific object, publication or consumption is accessed.
    """
    need(type(reference) is dict and type(expected_configuration_sha256) is str,
         'A11_EXECUTION_CONFIGURATION_REQUIRED')
    target=copy.deepcopy(reference)
    cfg=target.get('base_deployment_configuration')
    need(type(cfg) is dict and digest(canonical(cfg))==expected_configuration_sha256,
         'A11_INDEPENDENT_CONFIGURATION_DRIFT')
    need(target.get('deployment_identity')==expected_configuration_sha256 and
         target.get('checkpoint_sequence')==54 and target.get('historical_attempt_count')==10
         and type(target.get('next_attempt_sequence')) is int and target['next_attempt_sequence']==11,
         'A11_TARGET_CONTEXT_DRIFT')
    import recovery_two_attempt_v3 as recovery
    need(target.get('checkpoint_identity')==recovery.CURRENT_CHECKPOINT_MANIFEST and
         target.get('historical_attempts')==recovery.A11_CASE['historical_attempts'],
         'A11_CHECKPOINT_OR_HISTORY_DRIFT')
    need(target.get('unit_id')=='U0012' and type(target.get('max_new_units')) is int and
         target['max_new_units']==1 and target.get('u0013_prohibited') is True and
         target.get('environment')=='REAL' and target.get('activation_gate')=='HARD_DISABLED'
         and target.get('consumed') is False and target.get('dispatched') is False,
         'A11_UNIT_OR_AUTHORITY_CONTEXT_DRIFT')
    need(cfg.get('runtime_root')==publication.REAL_A11_RUNTIME_ROOT and
         cfg.get('execution_mode')=='REAL' and cfg.get('real_activation')=='HARD_DISABLED'
         and cfg.get('unit_id')=='U0012' and cfg.get('max_new_units')==1 and
         cfg.get('u0013_prohibited') is True,'A11_RUNTIME_SCOPE_DRIFT')
    for key in ('capture_executable','capture_argv','capture_cwd','capture_configuration_sha256',
                'checkpoint','recovery_sha256','recovery_compatibility_binding_sha256','policy_b_sha256'):
        need(key in cfg and cfg[key] is not None,'A11_EXECUTION_CONFIGURATION_REQUIRED')
    need(type(cfg['capture_executable']) is str and bool(cfg['capture_executable']) and
         type(cfg['capture_argv']) is list and bool(cfg['capture_argv']) and
         all(type(v) is str for v in cfg['capture_argv']) and
         type(cfg['capture_cwd']) is str and bool(cfg['capture_cwd']),
         'A11_CAPTURE_CONFIGURATION_DRIFT')
    need(cfg['checkpoint'].get('checkpoint_identity')==target['checkpoint_identity'] and
         cfg['checkpoint'].get('historical_attempt_count')==10 and
         cfg['checkpoint'].get('historical_attempts')==target['historical_attempts'],
         'A11_CHECKPOINT_OR_HISTORY_DRIFT')
    need(cfg.get('operational_context',{}).get('attempt_ordinal')==11 and
         cfg.get('transport',{}).get('input_delivery')=='FILE_IDENTITY_FRAME',
         'A11_PHYSICAL_EFFECT_CONTEXT_DRIFT')
    need(cfg.get('policy_b_sha256')=='faf83af7402808844154435dc02e735e04530d4184a2082ef78db62a39a92ca0',
         'A11_POLICY_B_IDENTITY_DRIFT')
    need(cfg.get('release_sha256')==COMPATIBILITY_RELEASE_SHA and
         cfg['recovery_sha256']==COMPATIBILITY_SOURCE_PINS['recovery_bounded_v4.py'] and
         cfg.get('selected_source_sha256')=={**COMPATIBILITY_SOURCE_PINS,
                                           'owner_authorization.py':_LOADED_SOURCE_SHA256},
         'A11_SOURCE_OR_RELEASE_IDENTITY_DRIFT')
    schema,scope,_=publication.real_publication_contract(target)
    need(scope==publication.REAL_A11_SCOPE and schema==publication.REAL_A11_SCHEMA,
         'A11_PUBLICATION_CONTEXT_DRIFT')
    need(target.get('authorization_policy',{}).get('scope')==scope,
         'A11_PUBLICATION_CONTEXT_DRIFT')
    return target


def derive_target(*,checkpoint_phase='PENDING',prospective_a11=False):
    need(checkpoint_phase in ('PENDING','FACTS'),'INVALID_TARGET_CHECKPOINT_PHASE')
    need(type(prospective_a11) is bool,'PROSPECTIVE_A11_SELECTOR')
    if prospective_a11:
        # The accepted technical specification is intentionally incomplete.
        # Never manufacture the missing REAL capture/current-content operands
        # from A10, synthetic data or a submitted authorization document.
        technical=_superseding_target({},prospective_a11=True)
        need(technical.get('execution_configuration_complete') is True,
             'A11_EXECUTION_CONFIGURATION_REQUIRED')
    """Refresh accepted metadata/hashes, without the retired signer source."""
    reference=_read_protected(REFERENCE_ROOT,REFERENCE_SHA,REFERENCE_LENGTH,publication.SCOPE)
    target=copy.deepcopy(reference['target_authorization']);cfg=target['base_deployment_configuration']
    manifest=DEPLOY/'deployed_runtime_composition_g01_g05_resumed_v1/DEPLOYED_RUNTIME_BINDING_MANIFEST.json'
    need(digest(manifest.read_bytes())==target['deployment_manifest_sha256'],'TARGET_DEPLOYMENT_MANIFEST_DRIFT')
    deployment=json.loads(manifest.read_bytes())
    need(deployment['binding_identity']==target['deployment_identity'] and deployment['configuration']==cfg,
         'TARGET_DEPLOYMENT_CONFIGURATION_DRIFT')
    release=DEPLOY/'REAL_RUNTIME_CANDIDATE_RELEASE_MANIFEST_V2.json'
    need(digest(release.read_bytes())==cfg['release_sha256'],'TARGET_RELEASE_DRIFT')
    for group in ('accepted_components','new_integration_components'):
        for item in json.loads(release.read_bytes())[group].values():
            need(digest((DEPLOY/item['path']).read_bytes())==item['sha256'],'TARGET_SOURCE_IDENTITY_DRIFT__'+item['path'])
    composition=DEPLOY/'deployed_runtime_composition_g01_g05_resumed_v1'
    for path,pin in [(composition/'composition.py',cfg['composition_source_sha256']),
        (composition/'transport_guard.py',cfg['transport']['guard_sha256']),
        (composition/'v2_unit_input.json',cfg['transport']['v2_stdin_sha256']),
        (DEPLOY/'two_attempt_recovery_compatibility_v1/recovery_two_attempt_v3.py',cfg['recovery_sha256']),
        (DEPLOY/'two_attempt_recovery_compatibility_v1/recovery_compatibility_binding.json',cfg['recovery_compatibility_binding_sha256'])]:
        need(digest(path.read_bytes())==pin,'TARGET_RUNTIME_BINDING_DRIFT__'+path.name)
    for item in cfg['transport']['executable_chain'].values():
        need(digest(Path(item['path']).read_bytes())==item['sha256'],'TARGET_EXECUTABLE_CHAIN_DRIFT')
    for name,pin in cfg['transport']['scientific_files_sha256'].items():
        need(digest((Path(cfg['transport']['scientific_directory'])/name).read_bytes())==pin,
             'TARGET_INPUT_BYTES_DRIFT__'+name)
    bound=json.loads((Path(__file__).parent/'recovery_compatibility_bounded_v4.json').read_bytes())
    need(digest((Path(__file__).parent/'recovery_compatibility_bounded_v4.json').read_bytes())==PROSPECTIVE_BINDING_SHA,'CURRENT_CHECKPOINT_BINDING_DRIFT')
    for name,pin in bound['checkpoint_files_sha256'].items():
        if checkpoint_phase=='FACTS' and name=='PRIMARY/checkpoint_head.json':continue
        need(digest((REAL_CHECKPOINT/name).read_bytes())==pin,'TARGET_CHECKPOINT_EVIDENCE_DRIFT__'+name)
    head=(json.loads((REAL_CHECKPOINT/'PRIMARY/checkpoint_head.json').read_bytes())
          if checkpoint_phase=='PENDING' else {'checkpoint_manifest_sha256': '379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe', 'sequence': 52, 'snapshot_file': 'checkpoint_000052.json', 'snapshot_file_sha256': '26b4005ffab3b554d416b8bb65501ff9d79b118b7be59b5cb87db1d275f6e1a6'})
    need(head=={'checkpoint_manifest_sha256': '379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe', 'sequence': 52, 'snapshot_file': 'checkpoint_000052.json', 'snapshot_file_sha256': '26b4005ffab3b554d416b8bb65501ff9d79b118b7be59b5cb87db1d275f6e1a6'} and head['checkpoint_manifest_sha256']=='379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe',
         'TARGET_CHECKPOINT_HEAD_DRIFT')
    stopped=json.loads((REAL_CHECKPOINT/'PRIMARY/checkpoints'/head['snapshot_file']).read_bytes())
    need(stopped['attempt_identity']==publication.REAL_ATTEMPT and stopped['first_unfinished_unit']=='U0012' and
         stopped['units'][11]['state']=='PENDING' and stopped['units'][11]['attempt_count']==9 and
         stopped['units'][11]['attempts']==bound['historical_attempts'] and
         stopped['units'][12]['state']=='PENDING' and stopped['units'][12]['attempt_count']==0,
         'TARGET_REAL_ATTEMPT_OR_UNIT_DRIFT')
    return _superseding_target(target)

def verify_real_engine_configuration(root,role,source_root,identity_manifest_path,attempt_id,*,prospective_a11=False):
    """Read-only construction facts; this returns no Owner authority or permit.

    The independently published Owner document and durable single-use receipt
    remain mandatory at the existing recovery reservation and execution sinks.
    """
    target=derive_target(checkpoint_phase='PENDING',prospective_a11=prospective_a11);cfg=target['base_deployment_configuration']
    lineage=cfg['source_lineage']
    need(Path(root)==REAL_CHECKPOINT and role=='PRIMARY' and attempt_id==publication.REAL_ATTEMPT,
         'ENGINE_CONFIGURATION_SCOPE_MISMATCH')
    need(Path(source_root)==Path(lineage['authoritative_s04_root']) and
         Path(identity_manifest_path)==Path(lineage['authoritative_partition_manifest']),
         'ENGINE_CONFIGURATION_SOURCE_PATH_MISMATCH')
    need(target['project']=='QUANTITATIVE_TRADING_RESEARCH_PLATFORM' and target['batch']=='BATCH0004'
         and target['role']=='PRIMARY' and target['phase']=='S05' and target['unit_id']=='U0012'
         and target['checkpoint_sequence']==(54 if prospective_a11 else 52)
         and target['historical_attempt_count']==(10 if prospective_a11 else 9)
         and type(target['next_attempt_sequence']) is int and target['next_attempt_sequence']==(11 if prospective_a11 else 10)
         and type(target['max_new_units']) is int and target['max_new_units']==1
         and target['u0013_prohibited'] is True and cfg['real_activation']=='HARD_DISABLED',
         'ENGINE_CONFIGURATION_BINDING_MISMATCH')
    need(not os.path.lexists(REAL_CHECKPOINT/'PRIMARY/executor_attempts/U0012'/
                            ('A0011' if prospective_a11 else 'A0010')),
         'ENGINE_ATTEMPT_ALREADY_EXISTS')
    return {'configuration_identity':target['deployment_identity'],
        'checkpoint_identity':target['checkpoint_identity'],'authority':'NONE__READ_ONLY_CONFIGURATION',
        'real_activation':'HARD_DISABLED'}

def runtime_binding(t,a,path,binding,frame,release_root,*,phase='PENDING'):
    import recovery_two_attempt_v3 as recovery
    from real_candidate.proof_path_v1 import BoundProofPath
    from real_candidate.policy_b_proof_v1 import PolicyBProofPath
    from real_candidate.release_v1 import verify_release
    need(type(t) is recovery.ControlledStopRecovery and type(t.engine) is recovery.BoundCheckpointEngine and
         type(t.engine.real_source) is bool,'ONLY_EXACT_BOUND_RECOVERY_ALLOWED')
    need(type(a) is recovery.V3CodexUnitAdapter and a.real_source is t.engine.real_source,
         'EXACT_ENGINE_EXECUTOR_EFFECT_MODE_REQUIRED')
    if not a.real_source:need(a.codex_path=='/usr/bin/false','ONLY_EXACT_INERT_EXECUTOR_ALLOWED')
    need(type(path) in (BoundProofPath,PolicyBProofPath) and path.supervisor.mode==('REAL' if a.real_source else 'NONPRODUCTION_TEST'),
         'EXACT_PROOF_EFFECT_MODE_REQUIRED')
    if phase=='PENDING':t.check_preconditions()
    elif phase=='RESERVED':t.verify_authorization()
    elif phase=='EXECUTING':t._fresh_pre_dispatch_guard()
    elif phase=='FACTS':pass  # facts only; existing recovery guards validate each checkpoint phase
    else:need(False,'INVALID_BINDING_PHASE')
    binding.verify();path.supervisor._fresh();path.validator._read_sources()
    path._fresh_sources()
    need(path.checkpoint_attestor.root==t.engine.root and
         path.checkpoint_attestor.expected==t.case['checkpoint_manifest_sha256'],
         'OWNER_ATTESTOR_CHECKPOINT_BINDING_DRIFT')
    need(not Path(frame).is_symlink() and Path(frame).resolve().is_relative_to(t.engine.root.parent.resolve()),
         'OWNER_INPUT_PATH_BINDING_DRIFT')
    need(verify_release(release_root)==path.release_identity,'INERT_RELEASE_IDENTITY_DRIFT')
    need(Path(frame).read_bytes()==canonical(recovery.unit_evidence(t.engine.partition,t.engine.evidence,'U0012')) and
         digest(Path(frame).read_bytes())==binding.unit_input_sha256,'INERT_INPUT_BINDING_DRIFT')
    mode=recovery.immutable_mode_contract(t.engine,a)
    planned=t.engine.workspace/'recovery_transactions'/recovery.case_and_mode_sha(t.case,mode)
    count=len(t._historical_attempts)
    if count==10:recovery.prospective_attempt_context(t.case,synthetic=not t.engine.real_source)
    target=derive_target(checkpoint_phase='PENDING' if phase=='PENDING' else 'FACTS',
                         prospective_a11=count==10);cfg=target['base_deployment_configuration']
    if a.real_source:
        expected_root=(publication.REAL_A11_RUNTIME_ROOT if count==10 else
            '/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1')
        need(Path(release_root).resolve()==Path(expected_root).resolve()
             and path.release_identity==cfg['release_sha256']
             and path.supervisor.config_sha256==cfg['capture_configuration_sha256']
             and binding.unit_input_sha256==cfg['transport']['v2_stdin_sha256']
             and t.case['checkpoint_manifest_sha256']==target['checkpoint_identity'],
             'CORRECTED_REAL_EXECUTION_BINDING_DRIFT')
        from real_candidate.executor_v1 import ExecutionContext,verify_runtime_context
        ctx=a.execution_context
        need(type(ctx) is ExecutionContext and ctx.transaction is t and ctx.proof_path is path and
             ctx.binding is binding and Path(ctx.frame).resolve()==Path(frame).resolve() and
             ctx.composition.identity==target['deployment_identity'] and
             str(a.work_root)==cfg['operational_context']['work_root'],'PROSPECTIVE_EXECUTION_CONTEXT_DRIFT')
        verify_runtime_context(ctx,phase='STATIC')
    return {'environment':'REAL' if a.real_source else 'SYNTHETIC_NONPRODUCTION','unit_id':'U0012','attempt_id':t.case['attempt_id'],
        'historical_attempt_count':count,'next_attempt_sequence':count+1,'max_new_units':1,'u0013_prohibited':True,
        'checkpoint_root':str(t.engine.root),'checkpoint_identity':t.case['checkpoint_manifest_sha256'],
        'input_path':str(Path(frame).resolve()),
        'case':copy.deepcopy(t.case),'execution_mode_contract':mode,'planned_consumption_journal':str(planned),
        'authorized_positions':list(range(1776,1801)),
        'runtime':{'capture_config_sha256':path.supervisor.config_sha256,'input_sha256':binding.unit_input_sha256,
            'recovery_raw_input_sha256':digest(t.raw_unit_input),'candidate_release_sha256':path.release_identity,
            'target_configuration_sha256':target['deployment_identity'],
            'target_composition_source_sha256':cfg['composition_source_sha256'],
            'target_checkpoint_sequence':target['checkpoint_sequence'],
            'target_recovery_source_sha256':cfg['recovery_sha256'],
            'target_recovery_compatibility_binding_sha256':cfg['recovery_compatibility_binding_sha256'],
            'authorization_policy_sha256':target['authorization_policy_sha256'],
            **({'policy_b_sha256':cfg['policy_b_sha256']} if count==10 else {}),
            'proof_schema':(__import__('real_candidate.policy_b_proof_v1',fromlist=['VERSION']).VERSION if type(path) is PolicyBProofPath else __import__('real_candidate.proof_issuer_v1',fromlist=['VERSION']).VERSION),
            'proof_implementation_sha256':path.issuer.issuer_source_sha256,
            'proof_mechanism':'CANONICAL_SHA256_PLUS_INDEPENDENT_EXPECTED_CLAIMS',
            'source_sha256':{str(p):digest(p.read_bytes()) for p in
                [Path(__file__),Path(publication.__file__),Path(recovery.__file__),
                 Path(__file__).parent/'real_candidate/checkpoint_v1.py',Path(__file__).parent/'real_candidate/activation_v1.py']}}}

def prepare_candidate(t,candidate,a,path,binding,frame,release_root):
    doc={'schema':publication.SCHEMA,'scope':publication.SCOPE,'consumer_uid':501,
        'target_authorization':derive_target(),
        'fixture_binding':runtime_binding(t,a,path,binding,frame,release_root)}
    raw=canonical(doc);publication.validate_inert_document(raw)
    fd=os.open(candidate,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:publication.write_all(fd,raw)
    finally:os.close(fd)
    need(Path(candidate).read_bytes()==raw,'CANDIDATE_READBACK_FAILED')
    return {'sha256':digest(raw),'length':len(raw)}

def verify_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,*,phase='PENDING'):
    doc=_read_protected(publication.PROTECTED_ROOT,expected_sha,expected_length,publication.SCOPE)
    need(os.getuid()==os.geteuid()==doc['consumer_uid']==501,'WRONG_EXECUTION_IDENTITY')
    need(canonical(doc['target_authorization'])==canonical(derive_target()),'CURRENT_REAL_TARGET_BINDING_DRIFT')
    need(canonical(doc['fixture_binding'])==canonical(runtime_binding(t,a,path,binding,frame,release_root,phase=phase)),
         'CURRENT_EXECUTION_BINDING_DRIFT')
    return doc

def consume_verified_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root):
    doc=verify_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root)
    need(not t.journal.exists(),'AUTHORIZATION_ALREADY_RESERVED_OR_CONSUMED')
    t.authorize_nonproduction(a)
    verify_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,phase='RESERVED')
    receipt={'schema':'OWNER_AUTHORIZATION_CONSUMPTION_V1','authorization_identity':expected_sha,
        'authorization_length':expected_length,'checkpoint_before':doc['fixture_binding']['checkpoint_identity'],
        'unit_id':'U0012','next_attempt_sequence':3,'max_new_units':1,'scope':publication.SCOPE,
        'real_execution_authorized':False}
    import recovery_two_attempt_v3 as recovery
    recovery.unique_write(t.journal/'owner_authorization_consumed.json',canonical(receipt))
    for directory in (t.journal,t.journal.parent,t.engine.workspace):fsync_directory(directory)
    return digest(canonical(receipt))

def execution_facts(doc):
    if doc['scope'] in (publication.REAL_SCOPE, publication.REAL_A11_SCOPE):
        return doc['execution_binding']['effects']
    need(doc['scope']==publication.SCOPE,'PUBLICATION_SCOPE_INVALID')
    return doc['fixture_binding']

def verify_real_document_bindings(doc, *, target, execution_binding, expected_sha, expected_length):
    """Shared pure comparison; REAL expectations come from fresh derivation.

    Synthetic callers qualify this mechanism only. Submitted metadata cannot
    replace independently derived target facts or typed physical effects.
    """
    raw=canonical(doc)
    publication.validate_owner_document(raw)
    schema,scope,_=publication.real_publication_contract(target)
    need(doc['schema']==schema and doc['scope']==scope,'REAL_ATTEMPT_CROSS_USE_REJECTED')
    need(digest(raw)==expected_sha and type(expected_length) is int and len(raw)==expected_length,
         'REAL_AUTHORIZATION_IDENTITY_DRIFT')
    need(canonical(doc['target_authorization'])==canonical(target),'CURRENT_REAL_TARGET_BINDING_DRIFT')
    need(canonical(doc['execution_binding'])==canonical(execution_binding),'CURRENT_REAL_EXECUTION_BINDING_DRIFT')
    return doc

def require_unreserved_authorization(journal_exists):
    """Existing per-attempt exclusive journal reservation; never retry it."""
    need(type(journal_exists) is bool and not journal_exists,'AUTHORIZATION_ALREADY_RESERVED_OR_CONSUMED')

def real_execution_binding(t,a,path,binding,frame,release_root,*,target=None):
    """REAL authorization subject and independently derived physical effects.

    No flag changes an execution mode: exact engine/adapter/capture objects
    determine effects. Each operation still requires fresh consumed authority.
    """
    count=len(t._historical_attempts)
    target=derive_target(checkpoint_phase='FACTS',prospective_a11=count==10) if target is None else target
    effects=runtime_binding(t,a,path,binding,frame,release_root,phase='FACTS')
    need(effects['environment']=='REAL','REAL_AUTHORITY_REQUIRES_REAL_PHYSICAL_EFFECTS')
    return {'environment':'REAL','attempt_id':publication.REAL_ATTEMPT,'unit_id':'U0012',
        'historical_attempt_count':count,'next_attempt_sequence':count+1,'max_new_units':1,'u0013_prohibited':True,
        'authorized_positions':list(range(1776,1801)),'checkpoint_identity':target['checkpoint_identity'],
        'target_deployment_identity':target['deployment_identity'],
        'launch_permission':'EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION',
        'effects':effects}

def prepare_real_candidate(t,candidate,a,path,binding,frame,release_root):
    """Prepare exact bytes only; no publication, privilege or execution occurs."""
    t.check_preconditions()
    target=derive_target(prospective_a11=len(t._historical_attempts)==10)
    schema,scope,_=publication.real_publication_contract(target)
    doc={'schema':schema,'scope':scope,'consumer_uid':501,
        'target_authorization':target,
        'execution_binding':real_execution_binding(t,a,path,binding,frame,release_root,target=target)}
    raw=canonical(doc);publication.validate_owner_document(raw)
    fd=os.open(candidate,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:publication.write_all(fd,raw)
    finally:os.close(fd)
    need(Path(candidate).read_bytes()==raw,'CANDIDATE_READBACK_FAILED')
    return {'sha256':digest(raw),'length':len(raw)}

def _verify_real_context(t,context):
    """Fresh authority from fixed root readback, never from context values alone."""
    need(type(context) is tuple and len(context)==7,'REAL_OWNER_CONTEXT_REQUIRED')
    expected_sha,expected_length,a,path,binding,frame,release_root=context
    a11=len(t._historical_attempts)==10
    if a11:
        target=derive_target(checkpoint_phase='FACTS',prospective_a11=True)
        _,scope,root=publication.real_publication_contract(target)
    else:scope,root=publication.REAL_SCOPE,publication.REAL_PROTECTED_ROOT
    doc=_read_protected(root,expected_sha,expected_length,scope)
    need(os.getuid()==os.geteuid()==doc['consumer_uid']==501,'WRONG_EXECUTION_IDENTITY')
    if not a11:target=derive_target(checkpoint_phase='FACTS')
    need(canonical(doc['target_authorization'])==canonical(target),'CURRENT_REAL_TARGET_BINDING_DRIFT')
    need(canonical(doc['execution_binding'])==canonical(real_execution_binding(
        t,a,path,binding,frame,release_root,target=target)),'CURRENT_REAL_EXECUTION_BINDING_DRIFT')
    verify_real_document_bindings(doc,target=target,execution_binding=doc['execution_binding'],
        expected_sha=expected_sha,expected_length=expected_length)
    if t._bound_adapter is not None:need(t._bound_adapter is a,'OWNER_BOUND_EXECUTOR_SUBSTITUTED')
    return doc

def verify_real_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,*,phase='PENDING'):
    context=(expected_sha,expected_length,a,path,binding,Path(frame),Path(release_root))
    doc=_verify_real_context(t,context)  # all immutable bindings before state or journal changes
    prior=t._real_owner_context
    if prior is not None:
        need(prior[:2]==context[:2] and all(x is y for x,y in zip(prior[2:5],context[2:5])) and
             prior[5:]==context[5:],'OWNER_CONTEXT_ALREADY_BOUND')
    t._real_owner_context=context  # locator only; every use repeats independent root readback
    try:
        if phase=='PENDING':t.check_preconditions()
        elif phase=='RESERVED':t.verify_authorization()
        elif phase=='EXECUTING':t._fresh_pre_dispatch_guard()
        else:need(False,'INVALID_BINDING_PHASE')
    except BaseException:
        t._real_owner_context=prior
        raise
    if t.engine.real_source:
        need(getattr(t.engine,'_owner_transaction',None) in (None,t),'ENGINE_OWNER_TRANSACTION_CHANGED')
        t.engine._owner_transaction=t  # locator only; every mutation repeats protected readback
    return doc

def verify_real_recovery_context(t):
    return _verify_real_context(t,t._real_owner_context)

def _real_consumption_bytes(t,doc):
    context=t._real_owner_context;effects=execution_facts(doc)
    schema,scope,_=publication.real_publication_contract(doc['target_authorization'])
    need(doc['schema']==schema and doc['scope']==scope,'REAL_ATTEMPT_CROSS_USE_REJECTED')
    receipt={'schema':'OWNER_REAL_AUTHORIZATION_CONSUMPTION_V1',
        'authorization_identity':context[0],'authorization_length':context[1],
        'authorization_domain':'REAL','scope':scope,
        'authorization_attempt_id':doc['target_authorization']['attempt_id'],'effect_attempt_id':t.case['attempt_id'],
        'checkpoint_before':t.case['checkpoint_manifest_sha256'],
        'target_checkpoint':doc['target_authorization']['checkpoint_identity'],
        'execution_binding_sha256':digest(canonical(doc['execution_binding'])),
        'recovery_binding_sha256':t.binding_hash,'journal_sha256':t._authorized_event_sha256,
        'effect_environment':effects['environment'],'unit_id':'U0012','next_attempt_sequence':doc['target_authorization']['next_attempt_sequence'],
        'max_new_units':1,'u0013_prohibited':True,'real_execution_authorized':False,
        'launch_permission':'HARD_DISABLED'}
    if t.engine.real_source:
        from real_candidate.executor_v1 import serialization_size
        maximum=t._bound_adapter.execution_context.storage_contract()['artifact_bytes']
        serialization_size(receipt,maximum,ensure_ascii=False,indent=None,separators=(',',':'))
    return canonical(receipt)

def consume_real_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root):
    doc=verify_real_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root)
    require_unreserved_authorization(t.journal.exists())
    t.authorize_real_domain(a)  # same exclusive accepted recovery reservation
    verify_real_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,phase='RESERVED')
    raw=_real_consumption_bytes(t,doc)
    import recovery_two_attempt_v3 as recovery
    receipt=t.journal/'owner_authorization_consumed.json'
    recovery.unique_write(receipt,raw)
    for directory in (t.journal,t.journal.parent,t.engine.workspace):fsync_directory(directory)
    need(receipt.read_bytes()==raw,'REAL_CONSUMPTION_READBACK_FAILED')
    # Completion state proves this process finished durable IO, not Owner
    # authority. Root publication, every byte and journal identity are freshly
    # reverified below. A partial operation or new process cannot resume it.
    t._real_consumption_durable=(expected_sha,digest(raw))
    verify_real_consumption_context(t)
    return digest(raw)

def verify_real_consumption_context(t):
    doc=verify_real_recovery_context(t)
    need(t._prepared,'REAL_RECOVERY_RESERVATION_REQUIRED')
    t.verify_authorization_event_only(allow_dispatched=True)
    raw=_real_consumption_bytes(t,doc)
    need(t._real_consumption_durable==(t._real_owner_context[0],digest(raw)),
         'REAL_CONSUMPTION_DURABILITY_NOT_ESTABLISHED')
    p=t.journal/'owner_authorization_consumed.json'
    need(p.is_file() and not p.is_symlink(),'REAL_CONSUMPTION_MISSING')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:observed=publication.read_snapshot(fd,len(raw),501)
    finally:os.close(fd)
    need(observed==raw,'REAL_CONSUMPTION_BYTES_OR_IDENTITY_DRIFT')
    return doc

def verify_transaction_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,*,phase):
    if t._real_owner_context is not None:
        doc=verify_real_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,phase=phase)
        verify_real_consumption_context(t)
        return doc
    return verify_publication(expected_sha,expected_length,t,a,path,binding,frame,release_root,phase=phase)

def activate_real(transaction=None,*,phase='RESERVED'):
    from real_candidate.activation_v1 import production_activation
    return production_activation(transaction,phase=phase)

def model_b_document(t, executor, path, binding, frame, release_root):
    """Independent exact expected facts; no authority is returned by derivation."""
    import checkpoint_resume_activation_trusted_v1 as core
    import recovery_two_attempt_v3 as recovery
    from real_candidate.policy_b_proof_v1 import PolicyBProofPath,PolicyBCapturedFixtureExecutor
    from real_candidate.release_v1 import verify_release
    from trusted_stage.staging_v1 import UnitBinding,safe_read
    publication.model_b_root(t.engine.root)
    publication.model_b_root(frame)
    publication.model_b_root(path.supervisor.cwd)
    need(t.engine.workspace==t.engine.root/'PRIMARY' and t.engine.head==t.engine.workspace/'checkpoint_head.json',
         'MODEL_B_ENGINE_LOCATOR_SUBSTITUTION')
    need(type(t) is recovery.ControlledStopRecovery and type(t.engine) is core.CheckpointEngine
         and not hasattr(t.engine,'real_source') and t._real_owner_context is None
         and type(executor) is PolicyBCapturedFixtureExecutor and executor.path is path
         and type(path) is PolicyBProofPath and path.synthetic_engine is t.engine
         and type(binding) is UnitBinding, 'MODEL_B_EXACT_SYNTHETIC_COMPONENTS')
    if t._prepared:
        if t._dispatched:t._fresh_pre_dispatch_guard()
        else:t._fresh_pre_mutation_guard()
    else:
        t.check_preconditions()
    need(binding.execution_mode == 'SYNTHETIC_NONPRODUCTION' and binding.unit_id == 'U0012'
         and binding.max_new_units == 1 and binding.attempt_id == t.case['attempt_id']
         and len(t._historical_attempts) == 10 and t.case['real_execution_authorized'] is False,
         'MODEL_B_EXACT_RECOVERY_SCOPE')
    need(Path(release_root).resolve() == publication.MODEL_B_ROOT
         and path.release_root == publication.MODEL_B_ROOT, 'MODEL_B_SOURCE_ROOT')
    binding.verify(); supervisor=path.supervisor; supervisor._fresh()
    need(supervisor.mode == 'NONPRODUCTION_TEST' and supervisor._allow_test,
         'MODEL_B_CANNOT_AUTHORIZE_REAL')
    partition,evidence,reason=path.validator._read_sources()
    rows=path.validator.module.unit_evidence(partition,evidence,'U0012')
    need(safe_read(frame)==canonical(rows) and digest(safe_read(frame))==binding.unit_input_sha256
         and binding.checkpoint_identity==t.case['checkpoint_manifest_sha256']
         and binding.mode_binding_sha256==supervisor.config_sha256,
         'MODEL_B_INPUT_CHECKPOINT_CONFIGURATION_MISMATCH')
    need(t.case['unit_input_sha256']==digest(t.raw_unit_input), 'MODEL_B_RECOVERY_INPUT_MISMATCH')
    policy=publication.MODEL_B_ROOT/'candidate/real_candidate/policy_b_policy_v1.json'
    import sys
    modules=[m for m in tuple(sys.modules.values()) if getattr(m,'__file__',None)
        and Path(m.__file__).absolute()==publication.MODEL_B_ROOT/'composition.py']
    need(len(modules)==1,'MODEL_B_EXACT_LOADED_COMPOSITION_REQUIRED')
    composition=modules[0]
    history=copy.deepcopy(t._historical_attempts)
    recovery.verify_attempt_lineage({'attempts':history,'attempt_count':len(history)},history)
    need(canonical(history)==canonical(t.case['historical_attempts']), 'MODEL_B_HISTORY_SUBSTITUTION')
    work=supervisor.cwd.parents[3]
    need(supervisor.cwd==work/'PRIMARY/U0012/A0011/input','MODEL_B_A11_CAPTURE_PATH_MISMATCH')
    mode=recovery.immutable_mode_contract(t.engine,executor)
    journal=t.engine.workspace/'recovery_transactions'/recovery.case_and_mode_sha(t.case,mode)
    operands={'environment':'SYNTHETIC_NONPRODUCTION','real_execution_authorized':False,
        'batch_id':'BATCH0004','role':'PRIMARY','unit_id':'U0012','attempt_id':binding.attempt_id,
        'checkpoint_sequence':54,'checkpoint_identity':binding.checkpoint_identity,
        'historical_attempts':history,'historical_attempt_count':10,'attempt_ordinal':11,
        'sources':dict(composition._NONPRODUCTION_SOURCE_CLOSURE),
        'composition_sha256':digest(safe_read(composition.__file__)),
        'release_sha256':verify_release(release_root),
        'recovery_compatibility_sha256':digest(safe_read(publication.MODEL_B_ROOT/'candidate/recovery_compatibility_bounded_v4.json')),
        'input':{'path':str(frame),'sha256':binding.unit_input_sha256,'length':len(safe_read(frame))},
        'raw_neutral_input_sha256':digest(t.raw_unit_input),'capture':supervisor._configuration_payload(),
        'runtime_sha256':supervisor._original_executable_sha,'policy_sha256':digest(safe_read(policy)),
        'operational':{'work_root':str(work),'input_directory':str(supervisor.cwd),
            'evidence_root':str(supervisor.cwd.parent/'v3_executor_raw_evidence'),
            'stage_root':str(t.engine.root.parent/'stage'),'checkpoint_root':str(t.engine.root),
            'recovery_journal':str(journal)},
        'max_new_units':1,'u0013_prohibited':True,'real_activation':'HARD_DISABLED'}
    cfg=composition.model_b_technical_configuration(operands)
    target={'environment':'SYNTHETIC_NONPRODUCTION','real_execution_authorized':False,
        'unit_id':'U0012','attempt_id':binding.attempt_id,'attempt_ordinal':11,
        'historical_attempt_count':10,'checkpoint_sequence':54,'expected_rows':25,
        'max_new_units':1,'u0013_prohibited':True,'real_activation':'HARD_DISABLED',
        'checkpoint_identity':binding.checkpoint_identity,'checkpoint_root':str(t.engine.root),
        'input_sha256':binding.unit_input_sha256,'runtime_sha256':supervisor._original_executable_sha,
        'configuration_sha256':digest(canonical(cfg)),'policy_sha256':digest(safe_read(policy)),
        'release_sha256':verify_release(release_root),'case_sha256':recovery.case_binding_sha(t.case),
        'batch_id':'BATCH0004','role':'PRIMARY','configuration':cfg}
    effects={'environment':'SYNTHETIC_NONPRODUCTION','real_execution_authorized':False,
        'batch_id':'BATCH0004','role':'PRIMARY','unit_id':'U0012','attempt_id':binding.attempt_id,
        'attempt_ordinal':11,'historical_attempt_count':10,'checkpoint_sequence':54,
        'checkpoint_identity':binding.checkpoint_identity,'history_sha256':digest(canonical(history)),
        'input_sha256':binding.unit_input_sha256,'target_sha256':digest(canonical(target)),
        'configuration_sha256':target['configuration_sha256'],'runtime_sha256':supervisor._original_executable_sha,
        'operational':cfg['operational'],'capture_configuration_sha256':supervisor.config_sha256,
        'source_sha256':digest(canonical(cfg['sources'])),'release_sha256':target['release_sha256'],
        'policy_sha256':target['policy_sha256'],'max_new_units':1,'u0013_prohibited':True,
        'expected_rows':25,'launch_permission':'EXACT_MODEL_B_OWNER_APPROVAL_AND_DURABLE_NP_CONSUMPTION'}
    doc={'schema':publication.SCHEMA,'scope':publication.MODEL_B_SCOPE,'consumer_uid':501,
        'target_authorization':target,'execution_binding':effects,'fixture_binding':{'sources':path._fresh_sources(),
        'recovery_input_sha256':digest(t.raw_unit_input),'capture_configuration':supervisor._configuration_payload(),
        'owner_authorization_source_sha256':_LOADED_SOURCE_SHA256,
        'owner_publication_source_sha256':publication.MODEL_B_LOADED_SOURCE_SHA256}}
    publication.validate_model_b_document(canonical(doc))
    return doc

def _model_b_read(path, expected_sha, expected_length):
    need(digest(Path(__file__).read_bytes())==_LOADED_SOURCE_SHA256,'MODEL_B_AUTHORIZATION_SOURCE_DRIFT')
    path=publication.model_b_root(path)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try: raw=publication.read_snapshot(fd,expected_length,501,0o600)
    finally: os.close(fd)
    need(digest(raw)==expected_sha,'MODEL_B_AUTHORIZATION_HASH_MISMATCH')
    return raw

def consume_model_b(expected_sha,expected_length,*,directory,t,executor,path,binding,frame,release_root):
    directory=publication.model_b_root(directory)
    need(getattr(t,'_model_b_owner_context',None) is None and
         not t._prepared and not t._dispatched,'MODEL_B_CONSUMED_OR_DISPATCHED')
    raw=_model_b_read(directory/'authorization.json',expected_sha,expected_length)
    completion=publication.model_b_completion(expected_sha,expected_length)
    _model_b_read(directory/'publication_complete.json',digest(completion),len(completion))
    submitted=publication.validate_model_b_document(raw)
    need(canonical(submitted)==canonical(model_b_document(t,executor,path,binding,frame,release_root)),
         'MODEL_B_INDEPENDENT_IDENTITY_BINDING_MISMATCH')
    t.check_preconditions()
    context=(directory,expected_sha,expected_length,t,executor,path,binding,Path(frame),Path(release_root))
    consumed=canonical({'scope':publication.MODEL_B_SCOPE,'authorization_sha256':expected_sha,
        'authorization_length':expected_length,'checkpoint_root':str(t.engine.root),
        'unit_id':'U0012','attempt_ordinal':11,'real_authority':False})
    publication.model_b_unique_record(directory/'consumed.json',consumed)
    t.authorize_nonproduction(executor)
    publication.model_b_sync_directory(t.journal)
    publication.model_b_sync_directory(t.journal.parent)
    publication.model_b_sync_directory(t.journal.parent.parent)
    publication.model_b_unique_record(directory/'consumption_complete.json',consumed)
    t._model_b_owner_context=(context,consumed)
    path.supervisor._model_b_owner_context=t
    return digest(consumed)

def verify_model_b_authority(supervisor,*,claim_launch=False):
    """Fresh checks at capture and proof boundaries; exclusive one-shot claim."""
    t=getattr(supervisor,'_model_b_owner_context',None)
    need(t is not None and getattr(t,'_model_b_owner_context',None) is not None,
         'MODEL_B_MISSING_OWNER_AUTHORITY')
    context,consumed=t._model_b_owner_context
    directory,pin,length,tx,executor,path,binding,frame,release_root=context
    need(tx is t and path.supervisor is supervisor and t._real_owner_context is None,
         'MODEL_B_OWNER_CONTEXT_SUBSTITUTION')
    raw=_model_b_read(directory/'authorization.json',pin,length)
    completion=publication.model_b_completion(pin,length)
    _model_b_read(directory/'publication_complete.json',digest(completion),len(completion))
    need(raw==canonical(model_b_document(t,executor,path,binding,frame,release_root)),
         'MODEL_B_FRESH_BINDING_MISMATCH')
    need(_model_b_read(directory/'consumed.json',digest(consumed),len(consumed))==consumed,
         'MODEL_B_DURABLE_CONSUMPTION_MISMATCH')
    _model_b_read(directory/'consumption_complete.json',digest(consumed),len(consumed))
    if t._dispatched:t._fresh_pre_dispatch_guard()
    else:t.verify_authorization()
    if claim_launch:
        need(not path._consumed and executor.calls==0, 'MODEL_B_DISPATCH_ALREADY_USED')
        publication.model_b_unique_record(directory/'launch_claim.json',canonical({
            'authorization_sha256':pin,'execution_binding_sha256':digest(canonical(json.loads(raw)['execution_binding'])),
            'launch_count':1,'real_authority':False}))
    return {'authorization_domain':'OWNER_CONTROLLED_MODEL_B_SYNTHETIC',
        'authorization_sha256':pin,'consumption_sha256':digest(consumed),'real_authority':False}
