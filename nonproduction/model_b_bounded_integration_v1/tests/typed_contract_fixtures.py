"""In-memory synthetic REAL-contract shapes; never serialized to an active locator."""

import copy,hashlib

import owner_publication as pub

def h(label): return hashlib.sha256(('SYNTHETIC_NONPRODUCTION_ONLY:' + label).encode()).hexdigest()

def clone(value): return copy.deepcopy(value)

def refresh(doc):
    t = doc['target_authorization']; cfg = t['base_deployment_configuration']; b = doc['execution_binding']
    t['deployment_identity'] = pub.digest(pub.canonical(cfg))
    b['target_deployment_identity'] = t['deployment_identity']
    if 'effects' in b: b['effects']['runtime']['target_configuration_sha256'] = t['deployment_identity']
    if 'authorization_policy' in t:
        policy = t['authorization_policy']
        for key in policy:
            if key in t: policy[key] = t[key]
        t['authorization_policy_sha256'] = pub.digest(pub.canonical(policy))
    return doc

def a11_fixture():
    env = {'HOME':'/synthetic/home', 'PATH':pub.REAL_A11_RUNTIME_ROOT + '/task_runtime/bin:/usr/local/bin:/usr/bin:/bin',
           'LANG':'C.UTF-8', 'LC_ALL':'C'}
    spec = {'path':{'prefix':pub.REAL_A11_RUNTIME_ROOT + '/task_runtime/bin',
                    'remainder':'/usr/local/bin:/usr/bin:/bin'}, 'synthetic_only':True}
    cfg = dict(execution_mode='REAL', runtime_root=pub.REAL_A11_RUNTIME_ROOT, unit_id='U0012',
        max_new_units=1, u0013_prohibited=True, real_activation='HARD_DISABLED',
        operational_context={'attempt_ordinal':11}, release_sha256=h('release11'), detached_pin_sha256=h('pin11'),
        composition_source_sha256=h('composition11'), capture_configuration_sha256=h('capture11'),
        recovery_sha256=h('recovery11'), recovery_compatibility_binding_sha256=h('recoverycompat11'),
        policy_b_sha256=h('policyb11'), checkpoint={'checkpoint_identity':h('checkpoint54'), 'historical_attempt_count':10},
        selected_source_sha256={'synthetic_component.py':h('component11')}, capture_environment=env,
        environment_identity=pub.digest(pub.canonical(env)), runtime_compatibility=spec,
        python_compatibility_identity=pub.digest(pub.canonical(spec)),
        transport={'environment':clone(env), 'v2_stdin_sha256':h('input11')},
        capture_executable='/synthetic/never-executed/python', capture_argv=['-c','pass'], capture_cwd='/synthetic/never-created')
    t = dict(project='QUANTITATIVE_TRADING_RESEARCH_PLATFORM', batch='BATCH0004', role='PRIMARY', phase='S05',
        environment='REAL', unit_id='U0012', attempt_id='SYNTHETIC_NONPRODUCTION_ATTEMPT11_IDENTITY',
        next_attempt_sequence=11, historical_attempt_count=10, checkpoint_sequence=54,
        checkpoint_identity=h('checkpoint54'), max_new_units=1, u0013_prohibited=True,
        single_use=True, replay_protected=True, consumed=False, dispatched=False, activation_gate='HARD_DISABLED',
        base_deployment_configuration=cfg)
    keys = ('environment','unit_id','attempt_id','next_attempt_sequence','historical_attempt_count',
            'max_new_units','u0013_prohibited','checkpoint_identity')
    effects = {key:t[key] for key in keys}
    effects.update(authorized_positions=list(range(1776,1801)), runtime=dict(
        capture_config_sha256=cfg['capture_configuration_sha256'], input_sha256=cfg['transport']['v2_stdin_sha256'],
        candidate_release_sha256=cfg['release_sha256'], target_composition_source_sha256=cfg['composition_source_sha256'],
        target_checkpoint_sequence=54, target_recovery_source_sha256=cfg['recovery_sha256'],
        target_recovery_compatibility_binding_sha256=cfg['recovery_compatibility_binding_sha256'], policy_b_sha256=cfg['policy_b_sha256']))
    b = {key:t[key] for key in keys}
    b.update(authorized_positions=list(range(1776,1801)), effects=effects,
             launch_permission='EXACT_OWNER_PUBLICATION_AND_DURABLE_SINGLE_USE_CONSUMPTION')
    policykeys = ('project','batch','role','phase','unit_id','attempt_id','next_attempt_sequence','historical_attempt_count',
                  'max_new_units','u0013_prohibited','single_use','replay_protected','environment','activation_gate')
    t['authorization_policy'] = {**{key:t[key] for key in policykeys}, 'scope':pub.REAL_A11_SCOPE}
    return refresh(dict(schema=pub.REAL_A11_SCHEMA, scope=pub.REAL_A11_SCOPE, consumer_uid=501,
                        target_authorization=t, execution_binding=b))
