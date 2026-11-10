#!/usr/bin/env python3
"""NON-PRODUCTION partition contract for Batch0004. No real runner and no real inputs.

No partition size is selected or authorized here. The manifest is only a
nonproduction synthetic candidate until capacity evidence and Managing approval.
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
V3_PATH = HERE / 'frozen_v3_orchestrator_reference.py'
V3_SHA = 'fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0'
if sha256(V3_PATH.read_bytes()).hexdigest() != V3_SHA:
    raise RuntimeError('FROZEN_V3_REFERENCE_IDENTITY_MISMATCH')
spec = importlib.util.spec_from_file_location('frozen_v3_partition_reference', V3_PATH)
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)

RULE_VERSION = 'BATCH0004_POSITION_ONLY_PARTITION_PROTOTYPE_V1__NONPRODUCTION'
FIRST, LAST, TOTAL = 1501, 2000, 500

class PartitionStop(RuntimeError): pass

def require(condition, message):
    if not condition:
        raise PartitionStop(message)

def canonical_json(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def digest(x):
    return sha256(canonical_json(x).encode()).hexdigest()

def validate_population(evidence):
    require(isinstance(evidence, list) and len(evidence)==TOTAL, 'POPULATION_ROW_COUNT')
    require(all(isinstance(r, dict) for r in evidence), 'POPULATION_NONOBJECT')
    positions = [r.get('authorized_population_position') for r in evidence]
    identities = [r.get('canonical_source_identity') for r in evidence]
    require(all(type(p) is int for p in positions), 'POPULATION_POSITION_TYPE')
    require(Counter(positions)==Counter(range(FIRST, LAST+1)), 'POPULATION_POSITION_COVERAGE')
    require(all(isinstance(i,str) and len(i)==64 and all(c in '0123456789abcdef' for c in i) for i in identities), 'POPULATION_IDENTITY_FORMAT')
    require(len(set(identities))==TOTAL, 'POPULATION_DUPLICATE_IDENTITY')
    return sorted(evidence, key=lambda r:r['authorized_population_position'])

def build_partition_manifest(evidence, partition_size, source_s04_manifest_sha):
    """Position-only contiguous assignment; NO token/body/headline/content-aware routing."""
    require(type(partition_size) is int and 1<=partition_size<=TOTAL, 'INVALID_PARTITION_SIZE')
    require(isinstance(source_s04_manifest_sha,str) and len(source_s04_manifest_sha)==64, 'INVALID_SOURCE_BINDING')
    ordered = validate_population(evidence)
    units=[]
    for idx, offset in enumerate(range(0,TOTAL,partition_size),1):
        group=ordered[offset:offset+partition_size]
        units.append({'unit_id':f'U{idx:04d}',
                      'position_start':group[0]['authorized_population_position'],
                      'position_end':group[-1]['authorized_population_position'],
                      'row_count':len(group),
                      'positions':[r['authorized_population_position'] for r in group],
                      'canonical_source_identities':[r['canonical_source_identity'] for r in group]})
    positions=[p for u in units for p in u['positions']]
    ids=[v for u in units for v in u['canonical_source_identities']]
    require(len(positions)==TOTAL and Counter(positions)==Counter(range(FIRST,LAST+1)), 'PARTITION_INCOMPLETE')
    require(len(ids)==TOTAL and len(set(ids))==TOTAL, 'PARTITION_IDENTITY_DUPLICATE')
    data={'rule_version':RULE_VERSION, 'assignment_rule':'SORT_AUTHORIZED_POSITION_ASCENDING__CONTIGUOUS_FIXED_SIZE',
          'content_dependent_assignment':False, 'source_s04_manifest_sha256':source_s04_manifest_sha,
          'position_start':FIRST,'position_end':LAST,'record_count':TOTAL,
          'partition_size':partition_size,'partition_count':len(units),
          'coverage_count':TOTAL,'overlap_count':0,'omission_count':0,'duplicate_count':0,
          'unique_identity_count':TOTAL,'units':units}
    return data

def verify_manifest(manifest, evidence):
    require(isinstance(manifest,dict), 'MANIFEST_NOT_OBJECT')
    require(manifest.get('rule_version')==RULE_VERSION, 'RULE_VERSION_CHANGED')
    require(manifest.get('content_dependent_assignment') is False, 'CONTENT_DEPENDENT_ASSIGNMENT')
    expected=build_partition_manifest(evidence,manifest.get('partition_size'),manifest.get('source_s04_manifest_sha256'))
    require(manifest==expected, 'PARTITION_MANIFEST_MUTATION_OR_MISMATCH')
    return True

def unit_evidence(manifest, evidence, unit_id):
    verify_manifest(manifest,evidence)
    candidates=[u for u in manifest['units'] if u['unit_id']==unit_id]
    require(len(candidates)==1, 'UNKNOWN_UNIT')
    selected=set(candidates[0]['positions'])
    rows=[r for r in validate_population(evidence) if r['authorized_population_position'] in selected]
    require([r['canonical_source_identity'] for r in rows]==candidates[0]['canonical_source_identities'], 'UNIT_IDENTITY_MISMATCH')
    return rows

def validate_semantic_unit(manifest,evidence,reason_contract,unit_id,result,role):
    """Reuses accepted V3 semantic validation on a smaller exact population."""
    require(role in ('PRIMARY','INDEPENDENT'),'INVALID_ROLE')
    unit = unit_evidence(manifest,evidence,unit_id)
    v3.require_executor_success(result)
    payload = v3.parse_json_agent_message(result['agent_message'])
    require(isinstance(payload,dict) and 'rows' in payload and isinstance(payload['rows'],list),'ROWS_MISSING_OR_NOT_LIST')
    require(not v3.executor_error_indicated(payload),'EXECUTOR_EXPLICIT_NONCOMPLETION')
    require(len(payload['rows'])==len(unit),'UNIT_INCOMPLETE_ROW_COUNT')
    require(all(isinstance(x,dict) for x in payload['rows']),'UNIT_ROW_NOT_OBJECT')
    try:
        validated=v3.validate_semantic_rows(payload['rows'],unit,reason_contract)
    except (v3.ControlledStop, KeyError,TypeError) as exc:
        raise PartitionStop('V3_SEMANTIC_UNIT_VALIDATION_FAILURE__'+type(exc).__name__+'__'+str(exc)) from exc
    expected=[r['authorized_population_position'] for r in unit]
    require([r['authorized_population_position'] for r in validated]==expected,'UNIT_POSITION_DOMAIN_MISMATCH')
    return {'role':role,'unit_id':unit_id,'context_id':result['context_id'],'raw_rows':payload['rows'],
            'validated_rows':validated,'source_s04_manifest_sha256':manifest['source_s04_manifest_sha256'],
            'unit_output_sha256':digest(validated),'raw_rows_sha256':digest(payload['rows'])}

def validate_aggregation(manifest,evidence,reason_contract,unit_results,role,*,disallowed_contexts=()):
    """No partial acceptance: either all exact units are valid or no aggregate rows."""
    verify_manifest(manifest,evidence)
    require(role in ('PRIMARY','INDEPENDENT'),'INVALID_AGGREGATE_ROLE')
    require(isinstance(unit_results,list) and len(unit_results)==manifest['partition_count'],'MISSING_OR_EXTRA_UNIT')
    expected=[u['unit_id'] for u in manifest['units']]
    observed=[u.get('unit_id') for u in unit_results]
    require(observed==expected, 'UNIT_ORDER_DUPLICATE_OR_OMISSION')
    contexts=[]
    aggregate=[]
    for item,assignment in zip(unit_results,manifest['units']):
        require(item.get('role')==role, 'UNIT_ROLE_MISMATCH')
        require(item.get('source_s04_manifest_sha256')==manifest['source_s04_manifest_sha256'], 'UNIT_SOURCE_BINDING_MISMATCH')
        ctx=item.get('context_id')
        require(isinstance(ctx,str) and ctx and ctx not in disallowed_contexts, 'ROLE_CONTEXT_ISOLATION_FAILURE')
        require(ctx not in contexts, 'DUPLICATE_EXECUTOR_CONTEXT')
        contexts.append(ctx)
        checked=item.get('validated_rows')
        require(isinstance(checked,list) and len(checked)==assignment['row_count'], 'UNIT_RESULT_COUNT_MISMATCH')
        require([r.get('authorized_population_position') for r in checked]==assignment['positions'], 'UNIT_POSITION_MISMATCH')
        require([r.get('canonical_source_identity') for r in checked]==assignment['canonical_source_identities'], 'UNIT_IDENTITY_MISMATCH')
        require(digest(checked)==item.get('unit_output_sha256'), 'UNIT_OUTPUT_HASH_MISMATCH')
        raw=item.get('raw_rows')
        require(isinstance(raw,list) and digest(raw)==item.get('raw_rows_sha256'), 'UNIT_RAW_ROW_HASH_MISMATCH')
        reason_checked=v3.validate_semantic_rows(raw, unit_evidence(manifest,evidence,assignment['unit_id']),reason_contract)
        require(reason_checked==checked, 'UNIT_RAW_TO_VALIDATED_MISMATCH')
        aggregate.extend(checked)
    require(len(aggregate)==TOTAL,'AGGREGATION_INCOMPLETE')
    require([r['authorized_population_position'] for r in aggregate]==list(range(FIRST,LAST+1)), 'AGGREGATION_POSITION_DOMAIN')
    try:
        final=v3.validate_semantic_rows(aggregate,validate_population(evidence),reason_contract)
    except (v3.ControlledStop,KeyError,TypeError) as exc:
        raise PartitionStop('V3_FULL_DOMAIN_AGGREGATE_INVALID__'+type(exc).__name__+'__'+str(exc)) from exc
    require(final==aggregate, 'AGGREGATE_CANONICALIZATION_DIFFERENCE')
    return {'role':role,'rows':final,'row_count':TOTAL,'contexts':contexts,
            'partition_manifest_sha256':digest(manifest), 'aggregate_sha256':digest(final)}
