"""Existing Owner boundary: default denial; exact consumed authority per operation."""
from trusted_stage.staging_v1 import StageStop,require

CONTRACT_UNIT='U0012'
MAX_NEW_UNITS=1
U0013_PROHIBITED=True
REAL_ACTIVATION_GATE_STATE='HARD_DISABLED'

def check_candidate_preconditions(*, release_sha256, checkpoint_sha256,
        runtime_sha256, mode, proof_implementation_sha256, trusted_real_authorization,
        unit_id, max_new_units, u0013_prohibited=True):
    for name,value in [('release',release_sha256),('checkpoint',checkpoint_sha256),
                       ('runtime',runtime_sha256),('proof_implementation',proof_implementation_sha256)]:
        require(type(value) is str and len(value)==64 and set(value)<=set('0123456789abcdef'),
                'MISSING_OR_INVALID_'+name.upper()+'_IDENTITY')
    require(mode=='REAL' and unit_id=='U0012' and type(max_new_units) is int and max_new_units==1
            and u0013_prohibited is True,'REAL_MODE_UNIT_BOUNDARY_FAILURE')
    require(type(trusted_real_authorization) is str and len(trusted_real_authorization)==64,
            'MISSING_TRUSTED_REAL_AUTHORIZATION')
    # Precondition evaluation is NOT authorization and never returns a dispatch permit.
    return True

def production_activation(transaction=None,*,phase='RESERVED'):
    # No global enable or transferable permit. Every protected operation repeats
    # fixed-root readback, exact physical-effect binding and durable consumption.
    return verify_owner_real_activation(transaction,phase=phase)

def verify_owner_real_activation(transaction,*,phase='RESERVED'):
    """Verify this exact operation; the returned observations are never authority."""
    import owner_authorization as owner
    import recovery_two_attempt_v3 as recovery
    t=transaction
    require(type(t) is recovery.ControlledStopRecovery,
            'REAL_ACTIVATION_HARD_DISABLED__EXACT_OWNER_TRANSACTION_REQUIRED')
    require(phase in ('RESERVED','EXECUTING','MUTATION'),'INVALID_REAL_ACTIVATION_PHASE')
    count=len(t._historical_attempts)
    require(type(t.engine) is recovery.BoundCheckpointEngine and t.engine.real_source is True
            and t.case==(recovery.A11_CASE if count==10 else recovery.REAL_CASE),
            'EXACT_REAL_ENGINE_AND_CASE_REQUIRED')
    doc=owner.verify_real_consumption_context(t)
    context=t._real_owner_context
    executor=context[2];proof_path=context[3]
    require(type(executor) is recovery.V3CodexUnitAdapter and executor.real_source is True
            and executor is t._bound_adapter and executor.execution_context.transaction is t
            and executor.execution_context.proof_path is proof_path
            and proof_path.supervisor is executor.execution_context.supervisor
            and proof_path.supervisor.mode=='REAL' and not proof_path.supervisor._allow_test,
            'EXACT_REAL_OWNER_EXECUTION_COMPONENTS_REQUIRED')
    if phase=='MUTATION':
        # Snapshot callers have already changed in-memory U0012 state. Do not
        # refresh/reset engine.state here; recovery guards bind persisted phases.
        t._mode_guard()
    else:
        owner.verify_real_publication(*context[:2],t,*context[2:],phase=phase)
    effects=owner.execution_facts(doc)
    expected_scope=owner.publication.real_publication_contract(
        owner.derive_target(checkpoint_phase='FACTS',prospective_a11=count==10))[1]
    require(doc['scope']==expected_scope and effects['environment']=='REAL'
            and doc['execution_binding']['launch_permission']==
                'EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION',
            'REAL_OWNER_LAUNCH_CONTRACT_REQUIRED')
    check_candidate_preconditions(release_sha256=effects['runtime']['candidate_release_sha256'],
        checkpoint_sha256=effects['checkpoint_identity'],runtime_sha256=doc['target_authorization']['deployment_identity'],
        mode='REAL',proof_implementation_sha256=effects['runtime']['proof_implementation_sha256'],
        trusted_real_authorization=context[0],unit_id='U0012',max_new_units=1,u0013_prohibited=True)
    return {'authorization_sha256':context[0],'consumption_sha256':t._real_consumption_durable[1],
        'authorization_domain':'REAL','effect_environment':effects['environment'],
        'preconditions':'VERIFIED','phase':phase,'real_launch_permitted':True,
        'real_activation':'EXACT_OWNER_AUTHORIZED_OPERATION_ONLY'}

def run_model_b_synthetic(expected_sha256,expected_length,*,directory,transaction,executor,
        proof_path,binding,checkpoint,input_path,release_root,stage_root):
    """Connected synthetic path; existing REAL entrypoints are not selected."""
    import owner_authorization as owner
    owner.publication.model_b_root(stage_root)
    require(proof_path.supervisor.mode=='NONPRODUCTION_TEST' and
            binding.execution_mode=='SYNTHETIC_NONPRODUCTION','MODEL_B_CANNOT_AUTHORIZE_REAL')
    executor.configure_capture(binding=binding,checkpoint=checkpoint,input_path=input_path,stage_root=stage_root)
    consumed=owner.consume_model_b(expected_sha256,expected_length,directory=directory,
        t=transaction,executor=executor,path=proof_path,binding=binding,frame=input_path,release_root=release_root)
    transaction.bind_v7_verifier(proof_path,binding=binding,checkpoint=checkpoint,
        input_path=input_path,input_sha256=binding.unit_input_sha256,release_root=release_root)
    outcome=transaction.run_exact_unit_nonproduction(executor)
    observation=next(iter(proof_path.supervisor._observed.values())) if proof_path.supervisor._observed else None
    candidate=proof_path._candidate
    stage,proof,receipt=candidate[1:] if candidate is not None else (None,None,None)
    return {'outcome':outcome,'capture':observation,'stage':stage,'proof':proof,'receipt':receipt,
        'consumption_sha256':consumed,'real_authority':False}

def run_owner_real_domain(expected_sha256,expected_length,*,transaction,executor,proof_path,
        binding,input_path,release_root):
    import owner_authorization as owner
    t=transaction
    owner.consume_real_publication(expected_sha256,expected_length,t,executor,proof_path,binding,input_path,release_root)
    eligibility=verify_owner_real_activation(t)
    attestor=proof_path.checkpoint_attestor
    phase=attestor.arm_recovery_successor(t,checkpoint=attestor._last,
        pinned_owner_authorization_sha256=expected_sha256,
        pinned_owner_consumption_sha256=eligibility['consumption_sha256'])
    consumer=t.bind_v7_verifier(proof_path,binding=binding,checkpoint=phase,input_path=input_path,
        input_sha256=binding.unit_input_sha256,release_root=release_root)
    outcome=t.run_exact_unit_owner_authorized(executor)
    return {'outcome':outcome,**eligibility,'consumer_binding_sha256':owner.digest(consumer)}

def run_owner_authorized_inert(expected_sha256,expected_length, *, transaction,executor,
        proof_path,binding,input_path,release_root):
    """Exercise REAL-target authorization connections with an inert grant only.

    No REAL permit or REAL proof-provider claim is created. Publication readback
    is independently repeated by the consumption adapter before reservation.
    """
    import owner_authorization as owner
    t=transaction
    doc=owner.verify_publication(expected_sha256,expected_length,t,executor,proof_path,
        binding,input_path,release_root)
    target=doc['target_authorization']
    consumed=owner.consume_verified_publication(expected_sha256,expected_length,t,executor,
        proof_path,binding,input_path,release_root)
    # This existing interface evaluates the exact REAL-target preconditions,
    # and explicitly does NOT return execution authority. The operational
    # proof hash confers no Owner authority or production dispatch permit.
    check_candidate_preconditions(release_sha256=target['base_deployment_configuration']['release_sha256'],
        checkpoint_sha256=target['checkpoint_identity'],runtime_sha256=target['deployment_identity'],
        mode='REAL',proof_implementation_sha256=proof_path.issuer.issuer_source_sha256,
        trusted_real_authorization=expected_sha256,unit_id='U0012',max_new_units=1)
    attestor=proof_path.checkpoint_attestor
    phase=attestor.arm_recovery_successor(t,checkpoint=attestor._last,
        pinned_owner_authorization_sha256=expected_sha256,pinned_owner_consumption_sha256=consumed)
    consumer=t.bind_v7_verifier(proof_path,binding=binding,checkpoint=phase,input_path=input_path,
        input_sha256=binding.unit_input_sha256,release_root=release_root)
    outcome=t.run_exact_unit_nonproduction(executor)
    return {'outcome':outcome,'authorization_sha256':expected_sha256,'consumption_sha256':consumed,
        'consumer_binding_sha256':owner.digest(consumer),'activation_preconditions':'PASS_IN_INERT_SCOPE',
        'proof_mechanism':'CANONICAL_SHA256_PLUS_INDEPENDENT_EXPECTED_CLAIMS','real_dispatch_permit':False,
        'real_activation':'HARD_DISABLED'}
