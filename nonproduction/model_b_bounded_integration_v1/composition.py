"""Source-bound prospective U0012 composition; REAL activation remains denied."""
from pathlib import Path
import copy,hashlib,importlib.util,json,os,sys
REFERENCE_DEPLOY=Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1')
ROOT=REFERENCE_DEPLOY/'deployed_runtime_composition_g01_g05_resumed_v1'
DEPLOY=Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1')
CORRECTION=DEPLOY/'candidate'
CHECKPOINT=Path('/Users/richardcooper/Downloads/batch0004_REAL_S05_BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F_PRIMARY_checkpoint')
REFERENCE_RELEASE_SHA='00d35a429b23e3967478778f9c28c1265fd25dad0f0da5d7feba55d0a6fb9260'
REFERENCE_BINDING_SHA='2ce533284245735e960c6e3694bf9f9abf8b8bb30fcff1b32da0970f2e79994e'
RELEASE_SHA = '7151bbbbd4b41dccdceff20d48abd445ed882e7682a7efef7f670594b35f1c1b'
SOURCE_SHA256 = {'owner_publication.py': '6783256282e150076288454d5dec09fa3732d0008e667fd42dbbde6066031fe7', 'prospective_adapter_v1.py': 'f7c89bd4e497086b91f2dc26310680dcf373a04be4e20b4bbfe92372e18241bb', 'real_candidate/activation_v1.py': 'ace4a82dc33f39caf9a79884f0165a94f97a224011537edaccd529e537b5c41a', 'real_candidate/capture_v1.py': 'd8cdd455ba90552334eed1cba9df484d99fe0fdb5ed3dc8005309f7aa399ddf7', 'real_candidate/checkpoint_v1.py': 'fe8dccdbb2d6215d9e36e226f8e1e0b5986622a2231adf4ceee9903516f5e155', 'real_candidate/engine_v1.py': '11b79292d48c9103dde04f5a04f775515a4b84a107142691fadffff83ad52abd', 'real_candidate/executor_v1.py': 'fae7907da55a84540a0411df7558ee42bb2c1b55f7efcfd6f99e9a1c32b2deb9', 'real_candidate/policy_b_events_v1.py': '52e0448e6c4a2b69301346cb7741e889b501d50092b1c184d79233338e1ad1d2', 'real_candidate/policy_b_proof_v1.py': '8cfc5c2e455b9fdcadf1832dcce84b1379d1075664177ae82426b6bba2e5dfba', 'real_candidate/policy_b_validation_v1.py': '6dba4b8796c6437cf5f8f94fbd4c10d0e6eda5e36f546f816ce0f4742ca4371e', 'real_candidate/proof_issuer_v1.py': 'b79ad20faf776c2b838f2edbca2a19ef8704284d9bb530e87cbadcf3ea1b1bb8', 'real_candidate/proof_path_v1.py': '4471adbadbc03e788bde4d0bf24dca5627631e1e987779ab379257b0b8cfad34', 'real_candidate/real_binding_v1.py': 'b41d5a33f1bfda759c7549936f0340c77aa1a85329ce304e96190de549a8ff0e', 'real_candidate/release_v1.py': '20efd0e2ea60eaf9e0e592dd2e2e178eff2241ea35180260b8988b65d022ef9a', 'real_candidate/validation_v1.py': '9293273b70b153adea9034e60d98de900cbcb91f56a3fe2c367c1acd7d4a844e', 'recovery_bounded_v4.py': 'aeed2b56deea5960a97553604ea45c9d15c096c2575afabf11dc132465e56ca8', 'owner_authorization.py': 'cc8f3512e5429f2dfdea39108eb7f8de2c2806df1436d8b7bafba328b49d1352'}
BRIDGE_SHA='c3673d27f95f6d11950d2ddcc534e2768c169a8dd99d1982f92857774f8cae3b'
PREPARATION_SHA='dafb1ebba47545e080274b6822f2ad7de8bea5a68b16af531f6508d72f3fe76a'
UNIT_SHA='42ee433de5090dee6c6c8446c28cb90c88a8088bfcedcd414554e1118855f828'
RECOVERY_SHA = 'aeed2b56deea5960a97553604ea45c9d15c096c2575afabf11dc132465e56ca8'
RECOVERY_BINDING_SHA = 'b4dce0c0d76d7ae2608ca06de17c97ebd3ca91fd0e3924a0f93b3837a86b1cca'
CHECKPOINT_SHA = '379a49d3d476599ea888326db581a20d62b7873bddb723f649ac9404323e53fe'
BRIDGE_FILE=REFERENCE_DEPLOY/'real_s04_validator_input_bridge_v1/real_s04_validator_input_bridge_v3.py'
PREPARED=BRIDGE_FILE.parent/'prepared_inputs_v1'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n').encode()

def model_b_technical_configuration(operands):
 """Complete NP facts only; consumption independently derives these operands.

 No caller flag supplies completeness and no REAL configuration is produced.
 """
 require(Path(__file__).resolve()==NONPRODUCTION_ROOT/'composition.py' and
         file_sha(__file__)==_LOADED_COMPOSITION_SOURCE_SHA256,'MODEL_B_COMPOSITION_DRIFT')
 _verify_nonproduction_sources()
 required={'environment','real_execution_authorized','batch_id','role','unit_id','attempt_id',
   'checkpoint_sequence','checkpoint_identity','historical_attempts','historical_attempt_count',
   'attempt_ordinal','sources','composition_sha256','release_sha256','recovery_compatibility_sha256',
   'input','raw_neutral_input_sha256','capture','runtime_sha256','policy_sha256','operational',
   'max_new_units','u0013_prohibited','real_activation'}
 require(type(operands) is dict and set(operands)==required,'MODEL_B_INCOMPLETE_OPERANDS')
 o=copy.deepcopy(operands)
 recovery.verify_attempt_lineage({'attempts':o['historical_attempts'],
   'attempt_count':o['historical_attempt_count']},o['historical_attempts'])
 require(o['environment']=='SYNTHETIC_NONPRODUCTION' and o['real_execution_authorized'] is False
   and o['batch_id']=='BATCH0004' and o['role']=='PRIMARY' and o['unit_id']=='U0012'
   and o['historical_attempt_count']==10 and o['attempt_ordinal']==11
   and o['checkpoint_sequence']==54 and len(o['historical_attempts'])==10
   and [x['attempt_number'] for x in o['historical_attempts']]==list(range(1,11))
   and o['max_new_units']==1 and o['u0013_prohibited'] is True
   and o['real_activation']=='HARD_DISABLED','MODEL_B_OPERAND_SCOPE')
 require(o['sources']==_NONPRODUCTION_SOURCE_CLOSURE and o['release_sha256']==RELEASE_SHA
   and o['recovery_compatibility_sha256']==RECOVERY_BINDING_SHA
   and o['composition_sha256']==_LOADED_COMPOSITION_SOURCE_SHA256,'MODEL_B_OPERAND_SOURCE_DRIFT')
 capture=o['capture'];op=o['operational']
 require(set(capture)=={'executable','argv','cwd','env','adapter_sha256','mode','max_output_bytes',
   'input_delivery','timeout_policy'} and type(capture['argv']) in (list,tuple)
   and all(type(a) is str for a in capture['argv']) and type(capture['env']) is dict
   and type(capture['env'].get('PATH')) is str
   and all(type(k) is str and type(v) is str for k,v in capture['env'].items())
   and capture['adapter_sha256']==_NONPRODUCTION_SOURCE_CLOSURE['candidate/real_candidate/policy_b_proof_v1.py']
   and type(capture['max_output_bytes']) is int and 0<capture['max_output_bytes']<=16*1024*1024
   and set(capture['timeout_policy'])=={'policy','prelaunch_budget_seconds','post_popen_capture_budget_seconds',
     'popen_strictly_interruptible','total_transaction_ceiling_seconds'},'MODEL_B_INCOMPLETE_CAPTURE_OPERANDS')
 input_fields={'path','sha256','length'}
 if capture['input_delivery']=='FILE_IDENTITY_FRAME':input_fields.add('file_identity')
 require(set(op)=={'work_root','input_directory','evidence_root','stage_root','checkpoint_root','recovery_journal'}
   and set(o['input'])==input_fields,'MODEL_B_INCOMPLETE_PHYSICAL_OPERANDS')
 for key in ('checkpoint_identity','raw_neutral_input_sha256','runtime_sha256','policy_sha256'):
  require(type(o[key]) is str and len(o[key])==64 and set(o[key])<=set('0123456789abcdef'),
    'MODEL_B_MISSING_IDENTITY_OPERAND')
 require(o['policy_sha256']==file_sha(DEPLOY/'candidate/real_candidate/policy_b_policy_v1.json'),
   'MODEL_B_POLICY_OPERAND_DRIFT')
 for key in ('work_root','input_directory','evidence_root','stage_root','checkpoint_root','recovery_journal'):
  owner_publication.model_b_root(op[key])
 owner_publication.model_b_root(o['input']['path'])
 if capture['input_delivery']=='FILE_IDENTITY_FRAME':
  require(o['input']['file_identity']==owner_authorization.model_b_frame_identity(o['input']['path']),
    'MODEL_B_FILE_IDENTITY_OPERAND_DRIFT')
 require(capture['executable']=='/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12',
   'MODEL_B_EXACT_SYNTHETIC_EXECUTABLE_REQUIRED')
 require(capture['mode']=='NONPRODUCTION_TEST' and capture['input_delivery'] in ('STDIN','FILE_IDENTITY_FRAME')
   and file_sha(capture['executable'])==o['runtime_sha256']
   and capture['cwd']==op['input_directory']
   and op['input_directory']==str(Path(op['work_root'])/'PRIMARY/U0012/A0011/input')
   and op['evidence_root']==str(Path(op['input_directory']).parent/'v3_executor_raw_evidence')
   and o['input']['sha256']==file_sha(o['input']['path'])
   and o['input']['length']==Path(o['input']['path']).stat().st_size,'MODEL_B_OPERAND_RUNTIME_OR_INPUT_DRIFT')
 o['execution_configuration_complete']=True
 return o
def require(ok,code):
 if not ok:raise RuntimeError(code)
def pinned(p,pin):
 p=Path(p);require(p.is_file() and not p.is_symlink() and file_sha(p)==pin,'IDENTITY_DRIFT__'+str(p));return p

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m

# The only additional source authority is this exact NONPRODUCTION copy.
_B53_ENGINEERING_ROOT = Path('/private/tmp/QTRP_MODEL_B_A11_REAL_CONTRACT_NONPRODUCTION_QUALIFICATION_V1')
_B53_OS_RUNTIME = Path('/private/tmp/QTRP_B53_OWNER_EXECUTOR_OS_FIXTURE_NP_V1/runtime')
NONPRODUCTION_ROOT = (_B53_OS_RUNTIME if Path(__file__).absolute() == _B53_OS_RUNTIME/'composition.py'
                      else _B53_ENGINEERING_ROOT)
PROSPECTIVE_A11_ROOT = Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a11_u0012_attempt11_runtime_v1')
_CANDIDATE_NONPRODUCTION = Path(__file__).absolute() in (NONPRODUCTION_ROOT / 'composition.py', PROSPECTIVE_A11_ROOT / 'composition.py')
require(Path(__file__).absolute() == Path(__file__).resolve()
        and Path(__file__).resolve() in (DEPLOY / 'composition.py', NONPRODUCTION_ROOT / 'composition.py', PROSPECTIVE_A11_ROOT / 'composition.py'),
        'COMPOSITION_SOURCE_LOCATION_REJECTED')

if _CANDIDATE_NONPRODUCTION:
 DEPLOY = Path(__file__).resolve().parent
 CORRECTION = DEPLOY / 'candidate'
 RELEASE_SHA = '34d995d63c924ae9397406636d3b1f6e1e17e3c83dbc5973163fcb9c4b2176c8'
 SOURCE_SHA256 = {'owner_publication.py': 'ce9cef754186226d6bf2e6651d4a8a45a503f5ebf3af14b119481d3780fe1642', 'prospective_adapter_v1.py': '2315601c2f83fa18107257025ec94ef85d65b12c7a38e4a2c44066d77d3723ac', 'real_candidate/activation_v1.py': '6b473d6b272088ac635ff0981a4a82f88e634d75e3a47fc6730ceb49261bc385', 'real_candidate/capture_v1.py': '90179e4d829a5fb4a39b1344358b86d5e47bca20d2bd6621a7fac6ec46323f02', 'real_candidate/checkpoint_v1.py': '19bd44bc529ea370f805cd7f03d0ac54d64793b6b132a24311dc940ad8e534d7', 'real_candidate/engine_v1.py': '64cccf083cd036d78345b2b96971353c135b300afcaa20c670bc8dbde0a26e60', 'real_candidate/executor_v1.py': '6c69496f1ec6aed0f37a19cf7cc0780f6ffced49e2d400622bab3bcbe8fb55c7', 'real_candidate/policy_b_events_v1.py': '52e0448e6c4a2b69301346cb7741e889b501d50092b1c184d79233338e1ad1d2', 'real_candidate/policy_b_proof_v1.py': 'ecea353388b056fda0518491b296fbea9d1baa44304781662fef9f2b6c65342f', 'real_candidate/policy_b_validation_v1.py': '6dba4b8796c6437cf5f8f94fbd4c10d0e6eda5e36f546f816ce0f4742ca4371e', 'real_candidate/proof_issuer_v1.py': 'b79ad20faf776c2b838f2edbca2a19ef8704284d9bb530e87cbadcf3ea1b1bb8', 'real_candidate/proof_path_v1.py': '4471adbadbc03e788bde4d0bf24dca5627631e1e987779ab379257b0b8cfad34', 'real_candidate/real_binding_v1.py': 'b41d5a33f1bfda759c7549936f0340c77aa1a85329ce304e96190de549a8ff0e', 'real_candidate/release_v1.py': '50e735a712dcf0a7a44ba75cd9d99823c89c7404bc97acf7f071303627347cd3', 'real_candidate/validation_v1.py': '9293273b70b153adea9034e60d98de900cbcb91f56a3fe2c367c1acd7d4a844e', 'recovery_bounded_v4.py': '2624c60b1ed7d75221789faa8e0bfed9fbe7d78ed6451f961c503a67d6a1a645', 'membership_readonly.py': '4afebb18b53fa0985dabcf10b56d08427334096c3223fc5b1a7a9698aa79884c'}
 RECOVERY_SHA = '2624c60b1ed7d75221789faa8e0bfed9fbe7d78ed6451f961c503a67d6a1a645'
 RECOVERY_BINDING_SHA = 'a0fb4907a1cdada02c4cc500cfdc5c840363fb08bd4794510d0404c49b75545e'
 _NONPRODUCTION_SOURCE_CLOSURE = {'accepted/policy_v7_prospective.json': 'f3747fa0712821c32a9e97a02f196133e5544fff481185517de0e3748b4eef67', 'accepted/firewall_v2.py': '09cf139fc69b43d43e734f966c549ddb13efd113a57bafd0e982f675785371b4', 'accepted/ACCESSIBLE_TRUST_BASIS_POLICY_ALIGNMENT_V1.json': '0fc6838b48b775b684e10325204794e36577e1e69c37bd3136e46f36cc5f1993', 'accepted/IDENTITY_CORRECTION_SOURCE_SLICE_HASHES.json': 'e4a0a81eb9fd15c186004cbbaee01b7b9fab6d2edce382bd260728a8954981c1', 'accepted/availability_classifier_v7_prospective.py': '8c20ea1dd8507e94606af849b7e5886a738cdff2c9d7d3aa333bfef4de42c651', 'accepted/real_trust_boundary/real_boundary_v1.py': 'fcdb3a5e094050d83139e0d770cceca7b562769d1e46b9d1137d13a615845955', 'accepted/trusted_stage/staging_v1.py': 'afbae35b8a1fc9204b3e8ef9244781667315155062a4b3c54e09e156b8e38125', 'accepted/trusted_stage/promotion_v1.py': 'edc5e568e181297872e2658410b9604006730b71470b8eb75b677b5b4ea75ef7', 'accepted/trusted_stage/__init__.py': '542e458c1aaf703f234e09c5129b52cb8d494d53c0829eaab74483f37a9cad78', 'accepted/accepted_recovery/recovery_mode_binding_descriptor_v2.json': '0adcb00fbe0c98243e4241388043640a3a7ca4a658d02f37c8a56167d4f6365b', 'accepted/accepted_recovery/recovery_two_attempt_v3.py': '0376a36a82d9e18f45cdcda879c0175c2ec0dd899e32a00b8c59174082460531', 'accepted/accepted_recovery/checkpoint_resume_activation_trusted_v1.py': 'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1', 'accepted/accepted_recovery/bounded_controlled_stop_recovery_real_interface_v2.py': 'b51c63dd499c20711d153cc9abfca0361b588ad1c4ae772b1f84f464fcfba785', 'accepted/accepted_recovery/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py': '1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424', 'accepted/accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py': 'd8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42', 'accepted/accepted_recovery/reference/v6_accepted/frozen_v3_orchestrator_reference.py': 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0', 'candidate/prospective_adapter_v1.py': '2315601c2f83fa18107257025ec94ef85d65b12c7a38e4a2c44066d77d3723ac', 'candidate/b53_owner_readonly_v1.py': '4d98c09a11326ce765709e7a719511db8dc34f4eef5d65b56c6cb2c054a8c23e', 'candidate/owner_publication.py': 'ce9cef754186226d6bf2e6651d4a8a45a503f5ebf3af14b119481d3780fe1642', 'candidate/membership_readonly.py': '4afebb18b53fa0985dabcf10b56d08427334096c3223fc5b1a7a9698aa79884c', 'candidate/recovery_compatibility_bounded_v4.json': 'a0fb4907a1cdada02c4cc500cfdc5c840363fb08bd4794510d0404c49b75545e', 'candidate/owner_authorization.py': '334683297de6e1485a165d6fd18679ea0e06bb62e380248993362475474f546f', 'candidate/recovery_compatibility_binding.json': '63460e14a99e9e02be8b8a758a2b5c37f0946b81e18e090f751d8bfbad3fdcaa', 'candidate/recovery_bounded_v4.py': '2624c60b1ed7d75221789faa8e0bfed9fbe7d78ed6451f961c503a67d6a1a645', 'candidate/real_candidate/engine_v1.py': '64cccf083cd036d78345b2b96971353c135b300afcaa20c670bc8dbde0a26e60', 'candidate/real_candidate/proof_path_v1.py': '4471adbadbc03e788bde4d0bf24dca5627631e1e987779ab379257b0b8cfad34', 'candidate/real_candidate/capture_v1.py': '90179e4d829a5fb4a39b1344358b86d5e47bca20d2bd6621a7fac6ec46323f02', 'candidate/real_candidate/executor_v1.py': '6c69496f1ec6aed0f37a19cf7cc0780f6ffced49e2d400622bab3bcbe8fb55c7', 'candidate/real_candidate/checkpoint_v1.py': '19bd44bc529ea370f805cd7f03d0ac54d64793b6b132a24311dc940ad8e534d7', 'candidate/real_candidate/policy_b_events_v1.py': '52e0448e6c4a2b69301346cb7741e889b501d50092b1c184d79233338e1ad1d2', 'candidate/real_candidate/proof_issuer_v1.py': 'b79ad20faf776c2b838f2edbca2a19ef8704284d9bb530e87cbadcf3ea1b1bb8', 'candidate/real_candidate/policy_b_policy_v1.json': 'faf83af7402808844154435dc02e735e04530d4184a2082ef78db62a39a92ca0', 'candidate/real_candidate/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'candidate/real_candidate/activation_v1.py': '6b473d6b272088ac635ff0981a4a82f88e634d75e3a47fc6730ceb49261bc385', 'candidate/real_candidate/policy_b_validation_v1.py': '6dba4b8796c6437cf5f8f94fbd4c10d0e6eda5e36f546f816ce0f4742ca4371e', 'candidate/real_candidate/release_v1.py': '50e735a712dcf0a7a44ba75cd9d99823c89c7404bc97acf7f071303627347cd3', 'candidate/real_candidate/validation_v1.py': '9293273b70b153adea9034e60d98de900cbcb91f56a3fe2c367c1acd7d4a844e', 'candidate/real_candidate/policy_b_proof_v1.py': 'ecea353388b056fda0518491b296fbea9d1baa44304781662fef9f2b6c65342f', 'candidate/real_candidate/real_binding_v1.py': 'b41d5a33f1bfda759c7549936f0340c77aa1a85329ce304e96190de549a8ff0e', 'candidate/dependencies/managing_activation_gate_trusted_v1.py': 'fa370190bd59decf16162317f8334a4dddc887220c57686909fe2cc9b53b383c', 'candidate/dependencies/checkpoint_manifest_schema_integrated_v2.json': 'e4b464575dde0fcdc29f2e3c93f6666d907bd3c7d55722fe2a3db5c5dfb1ecd6', 'candidate/dependencies/checkpoint_resume_activation_trusted_v1.py': 'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1', 'candidate/dependencies/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py': '1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424', 'candidate/dependencies/synthetic_fixture/evidence.json': 'b2b7e62033261b4e3e84aff90d5510351c5c6a2b9ed8a2d57c560c5003d207d5', 'candidate/dependencies/synthetic_fixture/partition.json': '8c5b5d47bf490f0607d02cab9cef020a40a308c2a99b2d439f9e59bddbf20976', 'candidate/dependencies/synthetic_fixture/neutral_semantic_evidence.jsonl': 'b93701f318973b67959b863f3d297ecfa18d13aebccd1ef138378f96251ba3ee', 'candidate/dependencies/synthetic_fixture/reason_precedence_v2.json': 'a7c274deec148d9c4f808b37b046c9a3c2d7d2dcccb7e865c81c653a9508cf74', 'candidate/dependencies/synthetic_fixture/reason_normalized.json': '832d538f28e054b2ff116fdeebd930fb69848b6c50c4cf272b7e8f0425b4d786', 'candidate/dependencies/synthetic_fixture/full_s04_fixture/semantic_rule_v2.json': 'a159b8e10609e17feb63cc389e9f7cdf7d7f915990d39691ab1b9298c000c9b2', 'candidate/dependencies/reference/v6_accepted/policy_seal_v6.py': '6891a128c047f667051a25368c299affb780bb60fb2085dc5841f3b8936c14b2', 'candidate/dependencies/reference/v6_accepted/firewall_v2.py': '09cf139fc69b43d43e734f966c549ddb13efd113a57bafd0e982f675785371b4', 'candidate/dependencies/reference/v6_accepted/checkpoint_resume_readiness_v8.py': '083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27', 'candidate/dependencies/reference/v6_accepted/availability_classifier_v1.py': 'bc7b17c917a6221f0d61e085f3b77f01d7bb8d6cb32a00324b5d1db59074dadd', 'candidate/dependencies/reference/v6_accepted/availability_classifier_v6.py': '29d87996fc284400e2b5d47201b525b295aef0e1b6daf5ec77818c69c73dd24f', 'candidate/dependencies/reference/v6_accepted/partition_contract_nonproduction_v1.py': 'd8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42', 'candidate/dependencies/reference/v6_accepted/availability_classifier_v3.py': '0bcb0fb5d6b941fe33dbe68e47da24886801809187f1d0454be059bbd700a457', 'candidate/dependencies/reference/v6_accepted/runtime_activation_gate_v6.py': '96726fd117813fb9ff6003cdce86d53bac7bca30483b15097bb64e6f4483ad25', 'candidate/dependencies/reference/v6_accepted/checkpoint_manifest_schema_integrated_v2.json': 'e4b464575dde0fcdc29f2e3c93f6666d907bd3c7d55722fe2a3db5c5dfb1ecd6', 'candidate/dependencies/reference/v6_accepted/real_partition_manifest_v1.py': '326140d587dc3d23585fe5de466cd8624d22ad2a0781c5fa85e5beb3900bd363', 'candidate/dependencies/reference/v6_accepted/frozen_v3_orchestrator_reference.py': 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0', 'candidate/dependencies/reference/v6_accepted/v3_partition_live_adapter_readiness_v7.py': 'b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b'}

 _LOADED_COMPOSITION_SOURCE_SHA256 = file_sha(Path(__file__))

 def _verify_nonproduction_sources():
  require(DEPLOY in (NONPRODUCTION_ROOT, PROSPECTIVE_A11_ROOT) and DEPLOY.is_dir() and not DEPLOY.is_symlink()
          and DEPLOY.resolve() == DEPLOY, 'COMPATIBILITY_CANDIDATE_ROOT')
  observed = {p.relative_to(DEPLOY).as_posix()
              for folder in ('accepted', 'candidate')
              for p in (DEPLOY / folder).rglob('*') if p.is_file() or p.is_symlink()}
  require(set(_NONPRODUCTION_SOURCE_CLOSURE) <= observed, 'CANDIDATE_REQUIRED_COMPONENT_MISSING')
  require(observed == set(_NONPRODUCTION_SOURCE_CLOSURE), 'UNDECLARED_CANDIDATE_DEPENDENCY')
  require(all(not p.is_symlink() for folder in ('accepted', 'candidate')
              for p in (DEPLOY / folder).rglob('*')), 'CANDIDATE_SOURCE_SYMLINK_REJECTED')
  for relative, pin in _NONPRODUCTION_SOURCE_CLOSURE.items():
   pinned(DEPLOY / relative, pin)
  pinned(DEPLOY / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json', RELEASE_SHA)
  require((DEPLOY / 'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.sha256').read_bytes()
          == (RELEASE_SHA + '\n').encode(), 'CANDIDATE_DETACHED_PIN_MISMATCH')

 _verify_nonproduction_sources()
 _source_module_names={Path(name).stem for name in _NONPRODUCTION_SOURCE_CLOSURE
                       if name.endswith('.py') and Path(name).name!='__init__.py'}
 require(not any(name == 'real_candidate' or name.startswith('real_candidate.')
                 or name == 'trusted_stage' or name.startswith('trusted_stage.')
                 or name in _source_module_names
                 or name in ('owner_publication', 'owner_authorization',
                             'recovery_two_attempt_v3', 'recovery_bounded_v4', 'membership_readonly') for name in sys.modules),
         'PRELOADED_RUNTIME_COMPONENT_REJECTED')
 sys.path[:0] = [str(CORRECTION), str(DEPLOY / 'accepted')]
 from real_candidate.release_v1 import verify_release
 from real_candidate.capture_v1 import ControlledLocalCapture
 import owner_publication
 import owner_authorization
 for name in ('real_candidate', 'real_candidate.release_v1', 'real_candidate.capture_v1',
              'trusted_stage', 'trusted_stage.staging_v1', 'owner_publication', 'owner_authorization'):
  module = sys.modules[name]
  relative = (('accepted/' if name.startswith('trusted_stage') else 'candidate/')
              + name.replace('.', '/') + ('/__init__.py' if name in ('real_candidate', 'trusted_stage') else '.py'))
  require(Path(module.__file__).resolve() == DEPLOY / relative, 'LOADED_RUNTIME_PATH_DRIFT__' + name)
  pinned(module.__file__, _NONPRODUCTION_SOURCE_CLOSURE[relative])
 require(verify_release(DEPLOY) == RELEASE_SHA, 'CANDIDATE_RELEASE_MISMATCH')
 # Load the executing V4 through its established historical alias. The pinned
 # accepted historical artifact is custody evidence and is never imported.
 recovery=load('recovery_two_attempt_v3',CORRECTION/'recovery_bounded_v4.py')
 sys.modules['recovery_bounded_v4']=recovery
 require(Path(recovery.__file__).resolve()==CORRECTION/'recovery_bounded_v4.py',
         'LOADED_RECOVERY_PATH_DRIFT')
 _NONPRODUCTION_LOADED_ORIGINS={}
 for name,module in tuple(sys.modules.items()):
  filename=getattr(module,'__file__',None)
  if not filename:
   continue
  path=Path(filename).absolute()
  if path.is_relative_to(DEPLOY/'candidate') or path.is_relative_to(DEPLOY/'accepted'):
   relative=path.relative_to(DEPLOY).as_posix()
   require(relative in _NONPRODUCTION_SOURCE_CLOSURE and path==path.resolve(),
           'UNDECLARED_LOADED_SOURCE_ORIGIN')
   pinned(path,_NONPRODUCTION_SOURCE_CLOSURE[relative])
   _NONPRODUCTION_LOADED_ORIGINS[name]={'path':relative,'sha256':_NONPRODUCTION_SOURCE_CLOSURE[relative]}
else:
 # Static correction only: no path argument, environment switch or fallback.
 require(DEPLOY==Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1'),'ARBITRARY_RELEASE_PATH_REJECTED')
 require(DEPLOY.is_dir() and not DEPLOY.is_symlink(),'CORRECTED_RELEASE_UNAVAILABLE__NO_FALLBACK')
 pinned(DEPLOY/'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json',RELEASE_SHA)
 pinned(REFERENCE_DEPLOY/'REAL_RUNTIME_CANDIDATE_RELEASE_MANIFEST_V2.json',REFERENCE_RELEASE_SHA)
 pinned(ROOT/'DEPLOYED_RUNTIME_BINDING_MANIFEST.json',REFERENCE_BINDING_SHA)
 reference_configuration=json.loads((ROOT/'DEPLOYED_RUNTIME_BINDING_MANIFEST.json').read_bytes())['configuration']
 pinned(ROOT/'transport_guard.py',reference_configuration['transport']['guard_sha256'])
 for item in reference_configuration['transport']['executable_chain'].values():pinned(item['path'],item['sha256'])
 # Verify every selected source before importing any corrected component.
 for name,pin in SOURCE_SHA256.items():pinned(CORRECTION/name,pin)
 pinned(CORRECTION/'real_candidate/__init__.py','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
 pinned(CORRECTION/'recovery_compatibility_bounded_v4.json',RECOVERY_BINDING_SHA)
 require((CORRECTION/'dependencies')==Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1/candidate/dependencies') and
  (CORRECTION/'dependencies').is_dir() and (CORRECTION/'dependencies').resolve()==(CORRECTION/'dependencies') and
  all(not parent.is_symlink() for parent in ((CORRECTION/'dependencies'),*(CORRECTION/'dependencies').parents)) and
  all(
   {p.relative_to(CORRECTION/'dependencies').as_posix() for p in (CORRECTION/'dependencies').rglob('*') if p.is_file() or p.is_symlink()}==set(pins) and
   all(not p.is_symlink() for p in (CORRECTION/'dependencies').rglob('*')) and
   all(pinned((CORRECTION/'dependencies')/name,pin) for name,pin in pins.items())
   for pins in ({
    'checkpoint_manifest_schema_integrated_v2.json': 'e4b464575dde0fcdc29f2e3c93f6666d907bd3c7d55722fe2a3db5c5dfb1ecd6',
    'checkpoint_resume_activation_trusted_v1.py': 'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1',
    'corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py': '1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424',
    'managing_activation_gate_trusted_v1.py': 'fa370190bd59decf16162317f8334a4dddc887220c57686909fe2cc9b53b383c',
    'reference/v6_accepted/availability_classifier_v1.py': 'bc7b17c917a6221f0d61e085f3b77f01d7bb8d6cb32a00324b5d1db59074dadd',
    'reference/v6_accepted/availability_classifier_v3.py': '0bcb0fb5d6b941fe33dbe68e47da24886801809187f1d0454be059bbd700a457',
    'reference/v6_accepted/availability_classifier_v6.py': '29d87996fc284400e2b5d47201b525b295aef0e1b6daf5ec77818c69c73dd24f',
    'reference/v6_accepted/checkpoint_manifest_schema_integrated_v2.json': 'e4b464575dde0fcdc29f2e3c93f6666d907bd3c7d55722fe2a3db5c5dfb1ecd6',
    'reference/v6_accepted/checkpoint_resume_readiness_v8.py': '083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27',
    'reference/v6_accepted/firewall_v2.py': '09cf139fc69b43d43e734f966c549ddb13efd113a57bafd0e982f675785371b4',
    'reference/v6_accepted/frozen_v3_orchestrator_reference.py': 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0',
    'reference/v6_accepted/partition_contract_nonproduction_v1.py': 'd8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42',
    'reference/v6_accepted/policy_seal_v6.py': '6891a128c047f667051a25368c299affb780bb60fb2085dc5841f3b8936c14b2',
    'reference/v6_accepted/real_partition_manifest_v1.py': '326140d587dc3d23585fe5de466cd8624d22ad2a0781c5fa85e5beb3900bd363',
    'reference/v6_accepted/runtime_activation_gate_v6.py': '96726fd117813fb9ff6003cdce86d53bac7bca30483b15097bb64e6f4483ad25',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v7.py': 'b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b',
    'synthetic_fixture/full_s04_fixture/semantic_rule_v2.json': '064072b92522693ff9d892f8261399d9d8569189a15c1ce8cee4a98476dae2b1',
    'synthetic_fixture/mock_semantic_final.json': 'f092630d01bb0611680ac3940aeffc8deba89df46e8711c7b8bf5f5bc41b97b1',
    'synthetic_fixture/neutral_semantic_evidence.jsonl': '61d687a415611aa75db955485db36e90e70b0fae2b2cdd10518c6a3659c1f496',
    'synthetic_fixture/reason_precedence_v2.json': 'f663fc65909d542f9e8a07b875893bf8fee5ef67492fe8b634420184d2c6e346',
    'reference/v6_accepted/README.md': '665201dd1932ea0769a3b00c6881d94f395a335678b8fb58fbcb8349cd42d8a2',
    'reference/v6_accepted/README_V2.md': '4ffcd9683e81da0bbfa53d614b226fc14801c9fe6478b322e5903b821f503838',
    'reference/v6_accepted/README_V3.md': '568d1c5cffed9532fef9d93decf02c4e34bbdbdc47b212c096c255efb9c4826f',
    'reference/v6_accepted/README_V4.md': 'ced706ce4b8a1a0613cbb64c015d2cb2ff8dfce0556c81ecc1998f3c508b470b',
    'reference/v6_accepted/README_V5.md': 'c8ad748f2cd4adfa6d30470d72b4f46e94359bb50a9cb11d21a6aed11656df84',
    'reference/v6_accepted/availability_classifier_v2.py': '30157ee629a835bceaf06ffafa7fad6b90d41b232d8d969c8c7fe75d50422ebb',
    'reference/v6_accepted/availability_classifier_v4.py': 'a69cce07c5c0d3ab775bb5a05a5d73ac11389fcaa086b1a4dcd09bda5e258cb7',
    'reference/v6_accepted/availability_classifier_v5.py': '6f5e3330bb2926100a974d414f55358c8f6146988b929fac15af4954abe0b204',
    'reference/v6_accepted/checkpoint_legacy_53_results.txt': '09a21f999bc1b57ea4b9f106b644a8c6e5a77bbb6d741fa40331bf1026f3fa1f',
    'reference/v6_accepted/checkpoint_manifest_schema_v1.json': 'b67b0baff0efe3fa67acbb60d14f7654cbe1410fae92795c7cab608f00336268',
    'reference/v6_accepted/checkpoint_resume_integrated_v2.py': 'cc2ae6cccd953eea2e59edd7468842b84a391ce29c635c2fb61a1617ff71927a',
    'reference/v6_accepted/checkpoint_resume_nonproduction_v1.py': '63500740e08ed2bda817f062a83e8c12b256674f18cf81a771f376281efd574d',
    'reference/v6_accepted/checkpoint_resume_readiness_v3.py': '86d93848608340e85b9aad76449d37075c6b9ebe355f62da2ba496606eedd505',
    'reference/v6_accepted/checkpoint_resume_readiness_v4.py': 'e635f0ebb5a3a8221304c6d4f8499c3a8fe5640992a0bb1dec4fcd8cbda5e9ed',
    'reference/v6_accepted/checkpoint_resume_readiness_v5.py': '2af19d0918a0f414b7dceee64ea1dc59de5d318ebcd09e3e723bdfc7da5594cb',
    'reference/v6_accepted/checkpoint_resume_readiness_v6.py': '4e4f8815b124e4bd33506157285a5c3eb5e4a36161f6b56a54daedda5886a4de',
    'reference/v6_accepted/checkpoint_resume_readiness_v7.py': '34b7957301a792e1532767398895f0dc06c3bb72c39b78451f56eee23020a1ae',
    'reference/v6_accepted/integration_targeted_47_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/legacy_checkpoint_results.txt': '05764ced968d147ee3420b467faa3a2a5d5550f4fd8dd98b04868bd54c1c52fe',
    'reference/v6_accepted/legacy_integration_47_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/legacy_partition_results.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/managing_preliminary_status_v1.md': 'bf77b68f2d1a2c0b1ed1976eef407218ee0fbacb609b721fe47b6dd3306ff0c0',
    'reference/v6_accepted/managing_readiness_recovery_return_v1.md': '5ad8640b4c4bec86370ad2be75fe0d72c53d735c818297fafecebd9732a38602',
    'reference/v6_accepted/managing_readiness_recovery_return_v2.md': 'a318c756fe574759cd364e680532409135239d2436e7deae6a650cd4373bb277',
    'reference/v6_accepted/managing_readiness_recovery_return_v3.md': 'ec7891ccf4562778b0568c4eb95a6813fc98716a468b4fb338a5267cb5d17228',
    'reference/v6_accepted/managing_readiness_recovery_return_v4.md': '6d8b9f6e29dfe0b1d3fb474cb309a0594203ad76d9a1707f44ec8133c315ee06',
    'reference/v6_accepted/managing_readiness_recovery_return_v5.md': '84f1e2b995e2b31bf9356a7265f26e25706371a7e0f475d91e86ed2af6bda376',
    'reference/v6_accepted/partition_legacy_44_results_reference.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/patch_live_runtime.py': '04a27a14a413d08eb093b75d81a727533013efa4e69c4d6eda759516d8426b8c',
    'reference/v6_accepted/patch_readiness.py': 'f56038e8026065128d563c27e125fc735bb6539999b928dbf3fd6536c7f77d33',
    'reference/v6_accepted/policy_seal_v2.py': 'b9924818c5d4bab33916253e874add70574bc7f37de88e65f529e7928f9a2036',
    'reference/v6_accepted/policy_seal_v3.py': '039e77d23ef962dbe7ba3f1ba4f390904ee6b30f13e79159d7721f9397a58302',
    'reference/v6_accepted/policy_seal_v4.py': 'a39fddd4c85a27d6ff709cba4bc33dfdf75499bd957bf768d596fe9eddd803e2',
    'reference/v6_accepted/policy_seal_v5.py': '78ac8153cae85ffbefe71f75a9f3c2883103a06d0cf017067015d582bd7e62f4',
    'reference/v6_accepted/readiness_full_e2e_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/readiness_release_integrity_v1.json': '6d76ef2eddebdf8b2156f1492dd3bc95ac5857aff01386175fc99ce11b475fc9',
    'reference/v6_accepted/readiness_release_integrity_v2.json': 'b2d0632bd7e7389e29f5efe2c68f3c1295c860ae15b91ae88e1759ac45d5835d',
    'reference/v6_accepted/readiness_release_integrity_v3.json': '1e7ad3475c24cb32ae16d6bbe715099d6e5a9e73745490b9adedd651f693651d',
    'reference/v6_accepted/readiness_release_integrity_v4.json': '35db69a34a102c589a384bf7d1403c9e07ae226d6aecb22813f42df8ef6994a7',
    'reference/v6_accepted/readiness_release_integrity_v5.json': '451d23b2618bbe96c2855dd3fa6a1461fc37054ece08f230ce339257a3f831ef',
    'reference/v6_accepted/readiness_runtime_v1.py': 'a19fb865ef980a1d43435523d8252c03c8fb3b541ca03d715c02a07374d95793',
    'reference/v6_accepted/readiness_runtime_v2.py': 'a14d5ce6eddcaf479472905d8f1482f08d3ff3139de6c339a766885972921ba8',
    'reference/v6_accepted/readiness_runtime_v3.py': 'dafa24e93edb69e9df9876ea07c45a3c1fc748cc7066db54ab1720ede344111b',
    'reference/v6_accepted/readiness_runtime_v4.py': 'f4b88216659578367dd9fcef959e650daca5c83f4f3908e21bd2718a2ab8a277',
    'reference/v6_accepted/readiness_runtime_v5.py': 'e758b54b86ddb1521aa8d8a10f76a8516d1b695dbd746aaf6d73e5104864664f',
    'reference/v6_accepted/readiness_runtime_v6.py': 'f6f3bdf770c6d0b31696e06f059f2c67fcc89fb2c2825db62651f54ded0744da',
    'reference/v6_accepted/recovery_test_results.txt': '35517016772d0f013bd4f72b10d0a41c6f281b481dd3ff3e8113490e0208895e',
    'reference/v6_accepted/recovery_v2_full_synthetic_e2e_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/recovery_v2_partition_firewall_44_results.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/recovery_v2_prior_72_compatibility_results.txt': '35517016772d0f013bd4f72b10d0a41c6f281b481dd3ff3e8113490e0208895e',
    'reference/v6_accepted/recovery_v2_targeted_results.txt': '582a51de6ee1de881a793beb625e13781b66fe9f904acc618718f08ea95fd547',
    'reference/v6_accepted/recovery_v3_full_synthetic_e2e_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/recovery_v3_partition_firewall_44_results.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/recovery_v3_preserved_v1_72_results.txt': '35517016772d0f013bd4f72b10d0a41c6f281b481dd3ff3e8113490e0208895e',
    'reference/v6_accepted/recovery_v3_preserved_v2_61_results.txt': '582a51de6ee1de881a793beb625e13781b66fe9f904acc618718f08ea95fd547',
    'reference/v6_accepted/recovery_v3_targeted_results.txt': 'acfdd2fc54335b30842eb88c995e938e3c265ede61966c144a963f6ca2c98669',
    'reference/v6_accepted/release_integrity_manifest_v1.json': '6115a6d682280ab19b74805fb250020e07f33f6c8aa3e55862e68c83bbbc24fd',
    'reference/v6_accepted/runtime_activation_gate_v1.py': '2df8cf8b0f0568a29b2d7983675920f2eade8a71234e158886b812051b054b35',
    'reference/v6_accepted/runtime_activation_gate_v2.py': '49d0fb7df112dbf957b7a651ba484eb8218bdcb31eab7d97c586429b094af832',
    'reference/v6_accepted/runtime_activation_gate_v3.py': 'b7c03a24c346afa9d35b9478286c0f23f1076ce454995378cf9f209ea4be9db2',
    'reference/v6_accepted/runtime_activation_gate_v4.py': 'c5a81d6d4007f9d943844a0277c13817f41cf447306f84ef34b0b9bc320e9e91',
    'reference/v6_accepted/runtime_activation_gate_v5.py': 'ff6d6e680ac5d36d3d13222e3061cf65a4a8609a032108cc649ba02ed0302282',
    'reference/v6_accepted/runtime_activation_policy_v1.json': '69ff9ffef3861824c90e88c2a3c244acbb139c58f567ba7d5a1bedc1707e210f',
    'reference/v6_accepted/runtime_activation_policy_v2.json': 'a5d3e9ccb20b34b63687c1ffc0c7630e02912f3d1bca0f427e5ebc9715c4421e',
    'reference/v6_accepted/runtime_activation_policy_v3.json': '1d4373da7bab53cbb3397654b2715e8fe7b2896c737946c95d3b5446c5cdb742',
    'reference/v6_accepted/runtime_activation_policy_v4.json': '65de2be52496fdb32a5de941a106eaa785f15c5c9306e04f166aa7ce626a91dd',
    'reference/v6_accepted/runtime_activation_policy_v5.json': '2ed2c378e6088941813db750f58b1061723956e60416ec990c523f0add5941b3',
    'reference/v6_accepted/runtime_activation_policy_v6.json': 'db64d55bfa38fa9a6e6ecc074f348e92191215ad549d4debff67c35e8b8635de',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/SHA256SUMS.txt': '41a39f06f088c739c272cdc7546f26c387feb2b33d295c41cd5910770c73c081',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/bodies/001501_5409b60b517d_body.txt': 'c86689ac19aba33aff22dc869d3d1708926023a5e8a4ae07291ac1efd0fac4c8',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/bodies/001501_5409b60b517d_header.txt': '464c8f6580828eec84ec3d6c0a15eaade3ea2a7d350795a1691f126a5be4f88c',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/bodies/001502_8cb3040654d3_body.txt': '4fa40eb27ed8d5190f57eaf5d040aae9a945141b8c5ae997dcc0c27792e2706f',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/bodies/001502_8cb3040654d3_header.txt': '35d2e8cd0420dce70c037281faca756d7c4cf88bacd3508dec4574b3a7b09e00',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/neutral_semantic_evidence.jsonl': '61d687a415611aa75db955485db36e90e70b0fae2b2cdd10518c6a3659c1f496',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/reason_precedence_v2.json': 'f663fc65909d542f9e8a07b875893bf8fee5ef67492fe8b634420184d2c6e346',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/s04_primary_input_manifest.json': '39cfbaa78c9c55a6024595d9c28c591a08b165a98e0e79bfaa405a08aed106bb',
    'reference/v6_accepted/synthetic_fixture/full_s04_fixture/semantic_rule_v2.json': '064072b92522693ff9d892f8261399d9d8569189a15c1ce8cee4a98476dae2b1',
    'reference/v6_accepted/synthetic_fixture/mock_semantic_final.json': 'f092630d01bb0611680ac3940aeffc8deba89df46e8711c7b8bf5f5bc41b97b1',
    'reference/v6_accepted/synthetic_fixture/neutral_semantic_evidence.jsonl': '61d687a415611aa75db955485db36e90e70b0fae2b2cdd10518c6a3659c1f496',
    'reference/v6_accepted/synthetic_fixture/reason_precedence_v2.json': 'f663fc65909d542f9e8a07b875893bf8fee5ef67492fe8b634420184d2c6e346',
    'reference/v6_accepted/synthetic_runtime_authorization_v1.json': 'c78c37817180f19443633f48627883adf102f91ec565ba0b424442e330ffa446',
    'reference/v6_accepted/test_checkpoint_resume_nonproduction_v1.py': '8f7e099dfc5fccfa7f0e50befcabdb8d826d3fcdbeab4d16379f22b5388b5423',
    'reference/v6_accepted/test_partition_contract_nonproduction_v1.py': '83172263d104ad720f936529c2dbdd3733c94ca5784bf8ab0f976f3ba4588eee',
    'reference/v6_accepted/test_readiness_full_v3_e2e.py': '777594636d53685f464147d00bcd305e1e97768b6b2343e4a991ff074016165c',
    'reference/v6_accepted/test_readiness_full_v4_e2e.py': 'd0235bbb2ef74793db4eee037124f3a266678b0e292804a180e1bebe32bc1998',
    'reference/v6_accepted/test_readiness_full_v5_e2e.py': 'df36f0022857d9b228232350923e69477c475f103b554db95266a33b59aa6e81',
    'reference/v6_accepted/test_readiness_full_v6_e2e.py': '3c9e33691e9171245956f1a96ac09e7c59af304d3729f185737c07fc00341844',
    'reference/v6_accepted/test_readiness_full_v7_e2e.py': 'ecb6e585b1e980d62ae38cc1753559e86b8962abc29f8e171ce233c54dd402de',
    'reference/v6_accepted/test_readiness_recovery_v1.py': 'f95c6cf94872af135de087adcf94323fdd388e81f7de04cc44e4b22535d846a4',
    'reference/v6_accepted/test_readiness_recovery_v2.py': 'bf9e9ecb2c4ae14c8b928cc68b3625eb02822a85934a2b5c41176196e2e09491',
    'reference/v6_accepted/test_readiness_recovery_v2_baseline.py': '00944e3d283c5861e8b3a6ae19fd4a08115318a0f25a1746f3a6808bb65a422d',
    'reference/v6_accepted/test_readiness_recovery_v3.py': 'eeae44f245ba5d5870a4a8642f32d640f0d3bd7aee2c15edc16bc62b0aa616a4',
    'reference/v6_accepted/test_readiness_recovery_v4.py': 'e96feae1eec57e18cb087b0d1bdf5d620ce0a467411b05a2a029f65192d4bc2d',
    'reference/v6_accepted/test_readiness_recovery_v5.py': 'bf6e7797dcfad9f6482ad2723adc814dcc065d9b6e838c98b42332075e6e54a2',
    'reference/v6_accepted/test_readiness_recovery_v5_compat.py': '1532454f7521f70dbf21ba7af35281f2e1953bbf7b0eb7e0fd972f71d62d1da2',
    'reference/v6_accepted/test_real_manifest_live_adapter_nonproduction_v1.py': '78ea6366a7907f237f8091eb8131188c1116fa8e080c9fef86904faa0d440e39',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v2.py': 'ccc0ca3dba51d54d731f32c9e6863155e8d9c7ed255553ca7ef702049b3c195b',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v3.py': 'd6278a582089496bd01a0a54c2a06450b70670ca8f7249f55cb4d9b0dee28dc6',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v4.py': '53b1369a18851a7c313d9d75aeec20cf328d2f812fd69de88b75d41047e6d650',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v5.py': 'cd3266542ac5b9c7d28203f03ba70e860a1be20712fe794439808c7b9405b7fa',
    'reference/v6_accepted/v3_partition_live_adapter_readiness_v6.py': '80f2cd9f25707a73fe851547f24a61d98f84e3303e5ee5b34e1ed7114ad47c9a',
    'reference/v6_accepted/v3_partition_live_adapter_v1.py': '2a7a406d10b0d0e0728491db09a68c584b6a968ce7ee7c02da040da6b8140f9f',
    'reference/v6_accepted/v4_partition_firewall_44_results.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/v4_preserved_v1_72_results.txt': '35517016772d0f013bd4f72b10d0a41c6f281b481dd3ff3e8113490e0208895e',
    'reference/v6_accepted/v4_preserved_v2_61_results.txt': '582a51de6ee1de881a793beb625e13781b66fe9f904acc618718f08ea95fd547',
    'reference/v6_accepted/v4_preserved_v3_318_results.txt': 'acfdd2fc54335b30842eb88c995e938e3c265ede61966c144a963f6ca2c98669',
    'reference/v6_accepted/v4_s04_s16_synthetic_47_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/v4_targeted_1593_results.txt': '287871c81a0011202fcd91797a15156594da664a8193447d5eaac558729804c1',
    'reference/v6_accepted/v5_compat_v4_1593_results.txt': '287871c81a0011202fcd91797a15156594da664a8193447d5eaac558729804c1',
    'reference/v6_accepted/v5_full_synthetic_47_results.txt': '3ab8e242acaa604dc83e58fb5d6db88762497a4a4d0ec648a0efb3a27bbbfd4e',
    'reference/v6_accepted/v5_partition_firewall_44_results.txt': '6a017c4349ecee444f434c53f504faec991f821cfe360fe308902baba5e0e72b',
    'reference/v6_accepted/v5_preserved_v1_72_results.txt': '35517016772d0f013bd4f72b10d0a41c6f281b481dd3ff3e8113490e0208895e',
    'reference/v6_accepted/v5_preserved_v2_61_results.txt': '582a51de6ee1de881a793beb625e13781b66fe9f904acc618718f08ea95fd547',
    'reference/v6_accepted/v5_preserved_v3_318_results.txt': 'acfdd2fc54335b30842eb88c995e938e3c265ede61966c144a963f6ca2c98669',
    'reference/v6_accepted/v5_targeted_6040_results.txt': '808bc9fec7b39474dd44b357690adc6f571d813093ff50c52ec64be9dd2b7aeb',
    'reference/v6_accepted/verify_readiness_release_v1.py': '356d76e5948a905fdfd173d7bc3c7ba0792e7e5235dba25bef5ed6ce7ffcd592',
    'reference/v6_accepted/verify_readiness_release_v2.py': '14fe092ed54b3f4e9d6415e6fe68103a450f251b3eff6395485998e0ce684946',
    'reference/v6_accepted/verify_readiness_release_v3.py': 'a0b295a7794cd76dfa9f699c4f81087824bfef85dde43621e6b5b2c24e2495ba',
    'reference/v6_accepted/verify_readiness_release_v4.py': '21fb194932283c7c4b94b061c836888836332316db36b255a345ded410f4495b',
    'reference/v6_accepted/verify_readiness_release_v5.py': '62aad71ef2475b83f2088cb5a4815eb83dddd3df3dea72f96ec06b1b54fa8ddd',
   },)
  ),'RECOVERY_DEPENDENCY_PATH_DRIFT')
 require((DEPLOY/'accepted')==Path('/Users/richardcooper/Downloads/batch0004_PRIMARY_S05_V2_REAL_RUNTIME_DEPLOYMENT_BINDING_V1/a10_u0012_attempt10_runtime_v1/accepted') and
  (DEPLOY/'accepted').is_dir() and (DEPLOY/'accepted').resolve()==(DEPLOY/'accepted') and
  all(not parent.is_symlink() for parent in ((DEPLOY/'accepted'),*(DEPLOY/'accepted').parents)) and
  all(
   {p.relative_to(DEPLOY/'accepted').as_posix() for p in (DEPLOY/'accepted').rglob('*') if p.is_file() or p.is_symlink()}==set(pins) and
   all(not p.is_symlink() for p in (DEPLOY/'accepted').rglob('*')) and
   all(pinned((DEPLOY/'accepted')/name,pin) for name,pin in pins.items())
   for pins in ({
    'ACCESSIBLE_TRUST_BASIS_POLICY_ALIGNMENT_V1.json': '0fc6838b48b775b684e10325204794e36577e1e69c37bd3136e46f36cc5f1993',
    'IDENTITY_CORRECTION_SOURCE_SLICE_HASHES.json': 'e4a0a81eb9fd15c186004cbbaee01b7b9fab6d2edce382bd260728a8954981c1',
    'accepted_recovery/bounded_controlled_stop_recovery_real_interface_v2.py': 'b51c63dd499c20711d153cc9abfca0361b588ad1c4ae772b1f84f464fcfba785',
    'accepted_recovery/checkpoint_resume_activation_trusted_v1.py': 'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1',
    'accepted_recovery/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py': '1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424',
    'accepted_recovery/recovery_mode_binding_descriptor_v2.json': '0adcb00fbe0c98243e4241388043640a3a7ca4a658d02f37c8a56167d4f6365b',
    'accepted_recovery/reference/v6_accepted/frozen_v3_orchestrator_reference.py': 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0',
    'accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py': 'd8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42',
    'availability_classifier_v7_prospective.py': '8c20ea1dd8507e94606af849b7e5886a738cdff2c9d7d3aa333bfef4de42c651',
    'historical_v6/availability_classifier_v1.py': 'bc7b17c917a6221f0d61e085f3b77f01d7bb8d6cb32a00324b5d1db59074dadd',
    'historical_v6/availability_classifier_v3.py': '0bcb0fb5d6b941fe33dbe68e47da24886801809187f1d0454be059bbd700a457',
    'historical_v6/availability_classifier_v6.py': '29d87996fc284400e2b5d47201b525b295aef0e1b6daf5ec77818c69c73dd24f',
    'historical_v6/synthetic_fixture/reason_precedence_v2.json': 'f663fc65909d542f9e8a07b875893bf8fee5ef67492fe8b634420184d2c6e346',
    'policy_v7_prospective.json': 'f3747fa0712821c32a9e97a02f196133e5544fff481185517de0e3748b4eef67',
    'real_trust_boundary/real_boundary_v1.py': 'fcdb3a5e094050d83139e0d770cceca7b562769d1e46b9d1137d13a615845955',
    'trusted_stage/__init__.py': '542e458c1aaf703f234e09c5129b52cb8d494d53c0829eaab74483f37a9cad78',
    'trusted_stage/promotion_v1.py': 'edc5e568e181297872e2658410b9604006730b71470b8eb75b677b5b4ea75ef7',
    'trusted_stage/staging_v1.py': 'afbae35b8a1fc9204b3e8ef9244781667315155062a4b3c54e09e156b8e38125',
   },)
  ),'ACCEPTED_DEPENDENCY_PATH_DRIFT')
 selected_descriptor=json.loads((DEPLOY/'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json').read_bytes())
 for group in ('accepted_components','new_integration_components','prospective_components'):
  for item in selected_descriptor[group].values():pinned(DEPLOY/item['path'],item['sha256'])
 for name,pin in {
  'checkpoint_resume_activation_trusted_v1.py':'fde7d910ece9fb24254ab76af1376633d1002560c74846b570040b59d859c6c1',
  'corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py':'1887b13a4bf4546f5f375f0b4ec306c8d773847ec674b8e1d3d33bfd98fb7424',
  'reference/v6_accepted/checkpoint_resume_readiness_v8.py':'083c5c163dd7549fdc06d9def95d1af1bb648f248ca7f0327173b5ccf6f34d27',
  'reference/v6_accepted/v3_partition_live_adapter_readiness_v7.py':'b22efb727152980dd434fe4ba007e55f8cbac66a76dab42443ee93e461b8848b',
 }.items():pinned(CORRECTION/'dependencies'/name,pin)
 require(not any(name in sys.modules for name in ('real_candidate','owner_publication','owner_authorization','recovery_two_attempt_v3')),'PRELOADED_RUNTIME_COMPONENT_REJECTED')
 # Original reference paths remain immutable; never enter legacy materialization.
 require((ROOT/'scientific_input/U0012').is_dir(),'REFERENCE_INPUT_DIRECTORY_MISSING')
 require((ROOT/'v2_unit_input.json').is_file() and (ROOT/'runtime_transport_binding.json').is_file(),'REFERENCE_TRANSPORT_FILES_MISSING')

 # Bridge interpretation is established before any historical modules can shadow it.
 pinned(BRIDGE_FILE,BRIDGE_SHA)
 bridge=load('accepted_s04_bridge_composition',BRIDGE_FILE)
 def authoritative_lineage():
  pinned(REFERENCE_DEPLOY/'REAL_RUNTIME_CANDIDATE_RELEASE_MANIFEST_V2.json',REFERENCE_RELEASE_SHA)
  pinned(BRIDGE_FILE,BRIDGE_SHA);pinned(PREPARED/'preparation_binding_manifest.json',PREPARATION_SHA)
  bundle=bridge.prepare_verified_inputs(release=REFERENCE_DEPLOY,s04_root=bridge.authoritative_s04_root(),identity_manifest=bridge.identity_manifest_path())
  require(bundle.manifest_bytes==(PREPARED/'preparation_binding_manifest.json').read_bytes(),'PREPARATION_PROVENANCE_MISMATCH')
  for name,raw in bundle.files:require(raw==(PREPARED/name).read_bytes(),'PREPARED_REPRESENTATION_MISMATCH')
  return json.loads(bundle.manifest_bytes)
 LINEAGE=authoritative_lineage()
 sys.path[:0]=[str(REFERENCE_DEPLOY/'accepted'),str(DEPLOY/'candidate')]
 pinned(CORRECTION/'recovery_bounded_v4.py',RECOVERY_SHA);pinned(CORRECTION/'recovery_compatibility_bounded_v4.json',RECOVERY_BINDING_SHA)
 # Bind the pinned empty package before recovery prepends historical dependencies.
 require(not any(name=='real_candidate' or name.startswith('real_candidate.') for name in sys.modules),
         'PRELOADED_CANDIDATE_PACKAGE_REJECTED')
 candidate_package_root=CORRECTION/'real_candidate'
 candidate_package_file=pinned(candidate_package_root/'__init__.py','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
 candidate_package=load('real_candidate',candidate_package_file)
 require(sys.modules.get('real_candidate') is candidate_package and candidate_package.__package__=='real_candidate'
         and Path(candidate_package.__file__).resolve()==candidate_package_file.resolve()
         and candidate_package.__spec__.name=='real_candidate'
         and Path(candidate_package.__spec__.origin).resolve()==candidate_package_file.resolve()
         and list(candidate_package.__path__)==[str(candidate_package_root)]
         and list(candidate_package.__spec__.submodule_search_locations)==[str(candidate_package_root)],
         'CANDIDATE_PACKAGE_IDENTITY_DRIFT')
 recovery=load('recovery_two_attempt_v3',CORRECTION/'recovery_bounded_v4.py')
 require(sys.modules.get('real_candidate') is candidate_package
         and list(candidate_package.__path__)==[str(candidate_package_root)]
         and list(candidate_package.__spec__.submodule_search_locations)==[str(candidate_package_root)],
         'CANDIDATE_PACKAGE_CHANGED_DURING_RECOVERY')
 sys.modules['recovery_bounded_v4']=recovery
 # Correction prepends historical paths; restore candidate package precedence.
 sys.path[:0]=[str(REFERENCE_DEPLOY/'accepted'),str(DEPLOY/'candidate')]
 from real_candidate.capture_v1 import ControlledLocalCapture
 from real_candidate.validation_v1 import BoundAcceptedValidator
 from real_candidate.checkpoint_v1 import PersistedCheckpointAttestor
 from real_candidate.release_v1 import verify_release
 from real_candidate.proof_path_v1 import BoundProofPath
 from real_candidate.policy_b_proof_v1 import PolicyBProofPath
 owner_publication=load('owner_publication',CORRECTION/'owner_publication.py')
 owner_authorization=load('owner_authorization',CORRECTION/'owner_authorization.py')
 from real_candidate import activation_v1,executor_v1,engine_v1,real_binding_v1
 import prospective_adapter_v1
 for name,pin in SOURCE_SHA256.items():
  module=sys.modules[name.removesuffix('.py').replace('/','.')]
  require(Path(module.__file__).resolve()==(CORRECTION/name).resolve(),'LOADED_RUNTIME_PATH_DRIFT__'+name)
  pinned(module.__file__,pin)
 require(verify_release(DEPLOY)==RELEASE_SHA,'CANDIDATE_RELEASE_MISMATCH')
 transport_guard=load('transport_guard',ROOT/'transport_guard.py')
 from transport_guard import verify_inventory,verify_frame
 adapter=load('accepted_position_prompt_composition',REFERENCE_DEPLOY/'accepted/accepted_recovery/corrected_prompt_reference/v3_partition_live_adapter_position_prompt_v1.py')

def inventory(path):return {str(p.relative_to(path)):file_sha(p) for p in sorted(Path(path).rglob('*')) if p.is_file()}
def environment(home):return {'__CF_USER_TEXT_ENCODING':f'0x{os.getuid():X}:0x0:0x0','HOME':str(home),'PATH':'/usr/local/bin:/usr/bin:/bin','PAGER':'cat','GIT_PAGER':'cat','LANG':'C.UTF-8','LC_ALL':'C','PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'}
def scientific_argv(directory):
 require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
 return ['exec','--ephemeral','--ignore-user-config','--ignore-rules','--skip-git-repo-check','--sandbox','read-only','--json','-C',str(directory),adapter.unit_prompt('PRIMARY')]

def make_transport(directory,unit,mode,home):
 require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
 chain_paths={'codex_launcher':Path('/Users/richardcooper/.local/lib/node_modules/@openai/codex/bin/codex.js'),
  'codex_native':Path('/Users/richardcooper/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-x64/vendor/x86_64-apple-darwin/bin/codex'),
  'node':Path('/usr/local/bin/node'),'python':Path('/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12'),
  'platform_package':Path('/Users/richardcooper/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-x64/package.json')}
 rel=json.loads((DEPLOY/'REAL_RUNTIME_CANDIDATE_RELEASE_MANIFEST_V2.json').read_bytes())['owner_observed_executors_reference_only']
 keys={'codex_launcher':'codex_js_launcher_sha256','codex_native':'codex_native_macos_x64_sha256','node':'node_sha256','python':'python_sha256'}
 for k,key in keys.items():require(file_sha(chain_paths[k])==rel[key],'CURRENT_EXECUTABLE_IDENTITY_MISMATCH')
 args=scientific_argv(directory)
 d={'schema':'V3_FILE_ARGV_V2_STDIN_BINDING_V1','mode':mode,'scientific_directory':str(directory),
   'scientific_files_sha256':inventory(directory),'scientific_argv':args,'prompt_sha256':sha(args[-1].encode()),
   'process_directory':str(ROOT),'environment':environment(home),'guard_sha256':file_sha(ROOT/'transport_guard.py'),
   'executable_chain':{k:{'path':str(p),'sha256':file_sha(p)} for k,p in chain_paths.items()},
   'bridge_unit_sha256':sha(canonical(unit)[:-1]),'v2_stdin_sha256':sha(canonical(unit)),
   'scientific_jsonl_sha256':file_sha(directory/'neutral_semantic_evidence.jsonl'),
   'historical_stdin':'NO_SCIENTIFIC_STDIN_CONTENT; identity frame consumed before target',
   'threat_model':'EXCLUSIVE_OWNER_CONTROLLED_INPUT_AND_CODE; no hostile concurrent same-user/privileged writer during child execution',
   'real_activation':'HARD_DISABLED'}
 if mode=='REAL':d['target_argv']=[str(chain_paths['node']),str(chain_paths['codex_launcher']),*args]
 else:d['target_argv']=[str(Path(sys.executable).resolve()),'-I',str(ROOT/'fixture_child.py'),*args]
 return d

class DisabledComposition:
 @classmethod
 def for_nonproduction_compatibility(cls, *, argv):
  """Exercise the existing composition/capture boundary with synthetic input only.

  Normal initialization verifies the exact standalone NONPRODUCTION source closure.
  """
  from real_candidate.capture_v1 import COMPATIBILITY_CANDIDATE_ROOT,prepare_task_python
  require(Path(__file__).resolve()==COMPATIBILITY_CANDIDATE_ROOT/'composition.py',
   'COMPATIBILITY_CANDIDATE_COMPOSITION_SOURCE')
  prepare_task_python()
  target=owner_authorization._superseding_target({'argv':argv},candidate_nonproduction=True)
  cfg=target['base_deployment_configuration'];capture=cfg['capture']
  require(target['environment']=='SYNTHETIC_NONPRODUCTION' and target['real_execution_authorized'] is False
   and capture['mode']=='NONPRODUCTION_TEST','COMPATIBILITY_NONPRODUCTION_REQUIRED')
  self=object.__new__(cls)
  self._candidate_nonproduction=True
  self.supervisor=ControlledLocalCapture(executable=Path(capture['executable']),
   executable_sha256='d4f152f2a753c94e0e7935c8ebbe6b2609979e1df7898422b577d0076383d08b',
   argv=tuple(capture['argv']),cwd=Path(capture['cwd']),env=cfg['capture_environment'],
   adapter_sha256=capture['adapter_sha256'],mode='NONPRODUCTION_TEST',allow_test_fixture=True,
   max_output_bytes=capture['max_output_bytes'],runtime_compatibility=capture['runtime_compatibility'],
   candidate_binding=capture['candidate_binding'])
  require(self.supervisor.config_sha256==cfg['capture_configuration_sha256'],
   'PROSPECTIVE_CAPTURE_IDENTITY_DRIFT')
  self.transport=copy.deepcopy(cfg['transport'])
  self._config=cfg;self._config_bytes=canonical(cfg);self.identity=sha(self._config_bytes)
  require(self.identity==target['deployment_identity'],'COMPATIBILITY_CONFIGURATION_IDENTITY')
  return self
 @classmethod
 def for_prospective_a11_identity(cls):
  """Inert identity representation; contains no capture or authorization grant."""
  require(_CANDIDATE_NONPRODUCTION, 'PROSPECTIVE_A11_NONPRODUCTION_SOURCE_REQUIRED')
  _verify_nonproduction_sources()
  target=owner_authorization._superseding_target({},prospective_a11=True)
  require(target['real_execution_authorized'] is False
   and target['execution_configuration_complete'] is False,
   'PROSPECTIVE_A11_INERT_IDENTITY_ONLY')
  self=object.__new__(cls)
  self._prospective_a11_identity=True
  self._config=target['base_deployment_configuration']
  self._config_bytes=canonical(self._config);self.identity=sha(self._config_bytes)
  require(self.identity==target['deployment_identity'], 'PROSPECTIVE_A11_CONFIGURATION_IDENTITY')
  return self
 def __init__(self,*,unit_id='U0012',max_new_units=1,prospective_a11=False,
              current_binding=None,expected_binding_sha256=None):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  require(type(prospective_a11) is bool,'PROSPECTIVE_A11_SELECTOR')
  self._prospective_a11=prospective_a11
  self._current_binding=current_binding;self._expected_binding_sha256=expected_binding_sha256
  require(unit_id=='U0012' and type(max_new_units) is int and max_new_units==1,'INVALID_UNIT_OR_RETRY_SCOPE')
  self.lineage=authoritative_lineage();require(self.lineage['unit_input_sha256']==UNIT_SHA,'UNIT_IDENTITY_MISMATCH')
  require(verify_release(DEPLOY)==RELEASE_SHA,'CANDIDATE_RELEASE_MISMATCH')
  self.checkpoint=(recovery.verify_authoritative_compatibility(CHECKPOINT,
      current_binding=current_binding,expected_binding_sha256=expected_binding_sha256)
      if prospective_a11 else recovery.verify_authoritative_compatibility(CHECKPOINT))
  self.attestor=PersistedCheckpointAttestor(CHECKPOINT,
      pinned_checkpoint_sha256=recovery.CURRENT_CHECKPOINT_MANIFEST if prospective_a11 else CHECKPOINT_SHA,
      expected_history=recovery.A11_CASE['historical_attempts'] if prospective_a11 else None)
  self.attestation=self.attestor.verify()
  partition=json.loads((PREPARED/'partition.json').read_bytes());evidence=json.loads((PREPARED/'evidence.json').read_bytes())
  self.unit=adapter.unit_evidence(partition,evidence,'U0012')
  reference=json.loads((ROOT/'runtime_transport_binding.json').read_bytes())
  verify_inventory(ROOT/'scientific_input/U0012',reference['scientific_files_sha256'])
  self.frame_path=ROOT/'v2_unit_input.json';verify_frame(reference,self.frame_path.read_bytes())
  self.descriptor_path=ROOT/'runtime_transport_binding.json'
  cfg=owner_authorization.derive_target(prospective_a11=prospective_a11)['base_deployment_configuration']
  require(self.lineage==cfg['source_lineage'] and self.checkpoint==cfg['checkpoint'],'PROSPECTIVE_REFERENCE_LINEAGE_DRIFT')
  self.transport=copy.deepcopy(cfg['transport']);self.transport_identity=sha(canonical(self.transport))
  self.supervisor=ControlledLocalCapture(executable=Path(cfg['capture_executable']),
   executable_sha256=self.transport['executable_chain']['codex_native']['sha256'],
   argv=tuple(cfg['capture_argv']),cwd=Path(cfg['capture_cwd']),env=cfg['capture_environment'],
   adapter_sha256=SOURCE_SHA256['prospective_adapter_v1.py'],mode='REAL',
   max_output_bytes=cfg['operational_context']['max_output_bytes'],input_delivery='FILE_IDENTITY_FRAME',
   prelaunch_budget_seconds=cfg['timeout_policy']['prelaunch_budget_seconds'],
   child_capture_budget_seconds=cfg['timeout_policy']['post_popen_capture_budget_seconds'])
  require(self.supervisor.config_sha256==cfg['capture_configuration_sha256'],'PROSPECTIVE_CAPTURE_IDENTITY_DRIFT')
  self.validator=self.make_validator()
  self._config=cfg;self._config_bytes=canonical(cfg);self.identity=sha(self._config_bytes)
 def make_validator(self,*,source_paths=None):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  lineage=authoritative_lineage();expected={n:str(PREPARED/n) for n in ('partition.json','evidence.json','reason.json')}
  require(source_paths is None or canonical(source_paths)==canonical(expected),'ARBITRARY_VALIDATOR_INPUT_BYPASS')
  return BoundAcceptedValidator(accepted_root=DEPLOY/'accepted',supervisor=self.supervisor,
   partition_path=Path(expected['partition.json']),evidence_path=Path(expected['evidence.json']),reason_path=Path(expected['reason.json']),
   partition_sha256=lineage['prepared_files_sha256']['partition.json'],evidence_sha256=lineage['prepared_files_sha256']['evidence.json'],reason_sha256=lineage['prepared_files_sha256']['reason.json'])
 def configuration(self):
  if getattr(self,'_prospective_a11_identity',False):
   return owner_authorization._superseding_target({},prospective_a11=True)['base_deployment_configuration']
  if getattr(self,'_candidate_nonproduction',False):
   return owner_authorization._superseding_target({'argv':self.supervisor.argv},
    candidate_nonproduction=True)['base_deployment_configuration']
  return owner_authorization.derive_target(checkpoint_phase='FACTS',
   prospective_a11=self._prospective_a11)['base_deployment_configuration']
 def verify_runtime_sources(self):
  if getattr(self,'_prospective_a11_identity',False):
   _verify_nonproduction_sources()
   expected=self.configuration()
   require(self._config['runtime_root']==str(PROSPECTIVE_A11_ROOT)
    and self._config['source_locations']==expected['source_locations'], 'PROSPECTIVE_A11_SOURCE_LOCATION_DRIFT')
   require(self._config['environment_identity']==sha(canonical(self._config['capture_environment']))
    and self._config['capture_environment']==expected['capture_environment'], 'PROSPECTIVE_A11_ENVIRONMENT_IDENTITY_DRIFT')
   require(canonical(self._config)==canonical(expected)==self._config_bytes
    and self.identity==sha(self._config_bytes), 'PROSPECTIVE_A11_CONFIGURATION_IDENTITY_DRIFT')
   return True
  if getattr(self,'_candidate_nonproduction',False):
   _verify_nonproduction_sources()
   require(canonical(self.configuration())==self._config_bytes and sha(self._config_bytes)==self.identity,
    'LIVE_COMPOSITION_CONFIGURATION_DRIFT')
   self.supervisor._fresh()
   return True
  require(canonical(self.configuration())==self._config_bytes,'LIVE_COMPOSITION_CONFIGURATION_DRIFT')
  require(canonical(self.transport)==canonical(self._config['transport']),'LIVE_TRANSPORT_BINDING_DRIFT')
  for name,pin in SOURCE_SHA256.items():pinned(CORRECTION/name,pin)
  pinned(DEPLOY/'REAL_RUNTIME_BOUNDED_RELEASE_MANIFEST_V4.json',RELEASE_SHA)
  pinned(CORRECTION/'recovery_compatibility_bounded_v4.json',RECOVERY_BINDING_SHA)
  require(verify_release(DEPLOY)==RELEASE_SHA,'RELEASE_DRIFT')
  self.supervisor._fresh();self.validator._read_sources()
  reference=json.loads((ROOT/'runtime_transport_binding.json').read_bytes())
  verify_inventory(ROOT/'scientific_input/U0012',reference['scientific_files_sha256'])
  verify_frame(reference,self.frame_path.read_bytes())
  for entry in self.transport['executable_chain'].values():pinned(entry['path'],entry['sha256'])
  return True
 def verify(self,proposed=None):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  self.verify_runtime_sources()
  if proposed is not None:require(canonical(proposed)==self._config_bytes,'PROPOSED_CONFIGURATION_MISMATCH')
  authoritative_lineage()
  observed=(recovery.verify_authoritative_compatibility(CHECKPOINT,
      current_binding=self._current_binding,expected_binding_sha256=self._expected_binding_sha256)
      if self._prospective_a11 else recovery.verify_authoritative_compatibility(CHECKPOINT))
  require(observed==self.checkpoint,'CHECKPOINT_OR_ATTEMPT_HISTORY_DRIFT')
  self.attestor.verify_receipt(self.attestation)
  return True
 def execution_context(self,transaction,binding,proof_path):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  roots=self._config['operational_context']
  return executor_v1.ExecutionContext(composition=self,supervisor=self.supervisor,proof_path=proof_path,
   transaction=transaction,binding=binding,frame=self.frame_path,release_root=DEPLOY,
   stage_root=Path(roots['stage_root']),work_root=Path(roots['work_root']),durable_root=Path(roots['durable_root']),
   prompt=adapter.unit_prompt('PRIMARY'),codex_path=str(self.supervisor.executable),role='PRIMARY')
 def run_owner_authorized(self,authorization_sha256,authorization_length):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  self.supervisor.begin_prelaunch()
  # Eligibility readback only: no reservation, consumption or execution before
  # the existing exact context has been assembled and independently verified.
  target=owner_authorization.derive_target(prospective_a11=self._prospective_a11)
  _,scope,protected_root=owner_publication.real_publication_contract(target)
  publication=owner_authorization._read_protected(protected_root,
   authorization_sha256,authorization_length,scope)
  require(canonical(publication['target_authorization'])==canonical(
   owner_authorization.derive_target(prospective_a11=self._prospective_a11)),
   'CURRENT_REAL_TARGET_BINDING_DRIFT')
  self.verify()
  engine=recovery.BoundCheckpointEngine(CHECKPOINT,'PRIMARY',bridge.authoritative_s04_root(),
   bridge.identity_manifest_path(),real_source=True,attempt_identity=owner_publication.REAL_ATTEMPT,
   prospective_a11=self._prospective_a11).verify(expected_attempt_id=owner_publication.REAL_ATTEMPT)
  raw=(ROOT/'scientific_input/U0012/neutral_semantic_evidence.jsonl').read_bytes()
  case=recovery.A11_CASE if self._prospective_a11 else recovery.REAL_CASE
  transaction=recovery.ControlledStopRecovery(engine,copy.deepcopy(case),raw,expected_case=copy.deepcopy(case))
  from real_candidate.real_binding_v1 import FutureRealUnitBinding
  binding=FutureRealUnitBinding('BATCH0004','PRIMARY','U0012',owner_publication.REAL_ATTEMPT,self.attestation.identity,
   sha(self.frame_path.read_bytes()),'REAL',self.supervisor.config_sha256,tuple(range(1776,1801)),
   tuple(row['canonical_source_identity'] for row in self.unit))
  proof_path=PolicyBProofPath(supervisor=self.supervisor,validator=self.validator,checkpoint_attestor=self.attestor,release_root=DEPLOY)
  context=self.execution_context(transaction,binding,proof_path)
  roots=self._config['operational_context']
  executor=prospective_adapter_v1.V3CodexUnitAdapter(engine.source_root,engine.identity_manifest_path,
   Path(roots['work_root']),'PRIMARY',runner=executor_v1.run_codex_executor,real_source=True,
   codex_path=str(self.supervisor.executable),authorization_path=engine.authorization_path,
   attempt_identity=owner_publication.REAL_ATTEMPT,execution_context=context)
  self.supervisor.check_prelaunch()
  return activation_v1.run_owner_real_domain(authorization_sha256,authorization_length,transaction=transaction,
   executor=executor,proof_path=proof_path,binding=binding,input_path=self.frame_path,release_root=DEPLOY)
 def dispatch_real(self):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  activation_v1.production_activation()
 def manifest(self):
  require(not _CANDIDATE_NONPRODUCTION, 'COMPATIBILITY_NONPRODUCTION_ONLY')
  self.verify();return {'binding_identity':self.identity,'configuration':json.loads(self._config_bytes),
   'status':'SOURCE_BOUND_U0012_PROSPECTIVE_CONTEXT__REAL_HARD_DISABLED',
   'real_signer':'NOT_PROVISIONED','real_authorization':'NOT_PREPARED','real_activation':'HARD_DISABLED'}

class RecoveryHandoff:
 """Fixture proof/receipt -> accepted corrected recovery's read-only interface.
 This evidence is not an authorization, recovery transition, or REAL proof.
 """
 def __init__(self,composition):
  require(type(composition) is DisabledComposition,'UNTRUSTED_COMPOSITION_INTERFACE')
  self.composition=composition;self._consumed=set();self._verified={}
 def verify(self,fixture,*,receipt,stage,proof):
  self.composition.verify()
  require(type(fixture.path) is BoundProofPath and type(fixture.supervisor) is ControlledLocalCapture and
   type(fixture.path.validator) is BoundAcceptedValidator and fixture.path.supervisor is fixture.supervisor and
   fixture.path.validator.supervisor is fixture.supervisor and fixture.path.release_identity==RELEASE_SHA,'UNTRUSTED_HANDOFF_COMPONENT')
  require(fixture.supervisor.mode=='NONPRODUCTION_TEST' and proof.claims['EXECUTION_MODE']=='SYNTHETIC_NONPRODUCTION','REAL_FIXTURE_MISREPRESENTATION')
  require(fixture.checkpoint.identity!=CHECKPOINT_SHA and fixture.binding.checkpoint_identity==fixture.checkpoint.identity,
   'FIXTURE_CHECKPOINT_CANNOT_CLAIM_REAL_IDENTITY')
  require(all(row.get('synthetic_only') is True for row in fixture.path.validator.module.unit_evidence(*fixture.path.validator._read_sources()[:2],'U0012')),
   'NONPRODUCTION_EVIDENCE_REQUIRED')
  fixture.path.validator.verify_receipt(receipt,fixture.observation)
  verdict=fixture.path.qualify_prospective_only(capture=fixture.observation,input_path=fixture.frame,
    input_sha256=fixture.frame_sha,stage=stage,proof=proof,receipt=receipt,binding=fixture.binding,checkpoint=fixture.checkpoint)
  pinned(CORRECTION/'recovery_bounded_v4.py',RECOVERY_SHA);pinned(CORRECTION/'recovery_compatibility_bounded_v4.json',RECOVERY_BINDING_SHA)
  target=(recovery.verify_authoritative_compatibility(CHECKPOINT,
      current_binding=self.composition._current_binding,
      expected_binding_sha256=self.composition._expected_binding_sha256)
      if self.composition._prospective_a11 else recovery.verify_authoritative_compatibility(CHECKPOINT))
  case=recovery.A11_CASE if self.composition._prospective_a11 else recovery.REAL_CASE
  require(target==self.composition.checkpoint and case['historical_attempts']==target['historical_attempts'],'RECOVERY_CASE_LINEAGE_MISMATCH')
  require(case['unit_input_sha256']==self.composition.transport['scientific_jsonl_sha256'] and case['max_new_units']==1,'RECOVERY_INPUT_SCHEMA_MISMATCH')
  evidence={'schema':'NONMUTATING_PROOF_TO_CORRECTED_RECOVERY_EVIDENCE_V1','evidence_mode':'NONPRODUCTION_TEST',
   'fixture_checkpoint_sha256':fixture.checkpoint.identity,'fixture_validated_output_sha256':receipt.validated_output_sha256,
   'fixture_proof_sha256':proof.proof_sha256,'fixture_stage_sha256':stage.readback_sha256,'verdict':verdict,
   'target_configuration_identity':self.composition.identity,'target_checkpoint_sha256':target['checkpoint_identity'],
   'target_recovery_sha256':RECOVERY_SHA,'target_recovery_compatibility_binding_sha256':RECOVERY_BINDING_SHA,
   'target_historical_attempts':target['historical_attempts'],'recovery_transition_authorized':False,'real_proof_issued':False}
  self._verified[sha(canonical(evidence))]=evidence
  return evidence
 def consume_fixture_evidence_once(self,evidence):
  require(evidence['evidence_mode']=='NONPRODUCTION_TEST' and not evidence['recovery_transition_authorized'],'INVALID_HANDOFF_EVIDENCE')
  self.composition.verify()
  digest=sha(canonical(evidence));require(self._verified.get(digest) is evidence,'UNVERIFIED_HANDOFF_EVIDENCE');require(digest not in self._consumed,'HANDOFF_EVIDENCE_REPLAY');self._consumed.add(digest);return digest
