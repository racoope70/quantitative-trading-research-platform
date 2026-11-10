#!/usr/bin/env python3
"""V6 event-type invariant control classification and completed-inspection audit. NONPRODUCTION ONLY.

Phase A normalizes every defined executor control field independent of rows.
Malformed/unknown failure-bearing metadata is a hard stop. Phase B may pause
only if all collected evidence has no hard-stop or unclassified failures.
No arbitrary scanning of scientific rows, bodies, or output payloads.
"""
from __future__ import annotations
import json
import re
from availability_classifier_v3 import (
    HARD_STOP_PATTERNS, EXTERNAL_STATUSES, HARD_STOP_STATUSES, FLAG_CLASSES,
    FAILURE_TEXT_FIELDS, CHILD_OBJECT_FIELDS, ERROR_GROUP_CLASSES,
    GENERIC_FAILURE, USAGE_PATTERNS, SERVICE_PATTERNS, STATUS_FIELDS,
    ERROR_TYPES, _status, _signal,
)

# One additional explicit HTTP status alias accepted by V6 registry.
STATUS_FIELDS=tuple(dict.fromkeys((*STATUS_FIELDS, 'http_code')))

# Authoritative accepted types: key -> kind. Present/null is explicitly
# represented in the audit ledger even when there is nothing to classify.
# Text error fields may be null or string; 'error' alone may be a nested object.
FIELD_SCHEMA = {
    **{name:'text_or_null' for name in FAILURE_TEXT_FIELDS},
    **{name:'status_or_null' for name in STATUS_FIELDS},
    **{name:'class_or_null' for name in ('failure_status','error_class','failure_class')},
    'failure_statuses':'list_or_null',
    **{name:'bool_or_null' for name in FLAG_CLASSES},
    **{name:'error_group_or_null' for name in ERROR_GROUP_CLASSES},
    **{name:'object_or_null' for name in CHILD_OBJECT_FIELDS if name not in FAILURE_TEXT_FIELDS},
    'termination_state':'termination_or_null',
    'timeout_status':'bool_or_null',
    'return_code':'return_code_or_null',
    'raw_stdout':'raw_text_or_null',
    'raw_stderr':'raw_text_or_null',
    'agent_message':'raw_text_or_null',
}
FIELD_SCHEMA['error']='text_object_or_null'
# Error group fields accept a nonempty list of typed strings/objects; the list
# itself is classified as a hard-stop based on the field's named class.
SUPPORTED_TERMINATIONS={'ERROR','FAILED','INTERRUPTED','NORMAL_SUCCESS','TIMEOUT'}


# Field registry is the single authoritative discovery/normalization schema.
# Nested paths are declared by their parent-object type and the same typed
# child schema: all executor_metadata.* fields, including failure_statuses.
CONTROL_FIELD_REGISTRY = {
    field: {'path':field, 'schema':kind, 'malformed':'MALFORMED_FAILURE_METADATA'}
    for field,kind in FIELD_SCHEMA.items()
}
NESTED_CONTROL_REGISTRY = {
    f'{parent}.{field}':{'path':f'{parent}.{field}', 'schema':kind,
                           'malformed':'MALFORMED_FAILURE_METADATA'}
    for parent in CHILD_OBJECT_FIELDS if parent in FIELD_SCHEMA
    for field,kind in FIELD_SCHEMA.items()
}
CONTROL_FIELD_REGISTRY.update(NESTED_CONTROL_REGISTRY)


def classify_http_status(value):
    """Pure schema-bound classification: NEVER inspect event type or event eligibility.

    2xx are neutral; 429/503 are approved explicit availability codes; other
    3-digit non-2xx statuses are independent nonavailability failures.
    """
    if type(value) is int:
        code=value
    elif isinstance(value,str) and re.fullmatch(r'[0-9]{3}',value):
        code=int(value)
    else:
        return ('MALFORMED_FAILURE_METADATA', 'UNACCEPTED_HTTP_STATUS_TYPE')
    if code<100 or code>599:
        return ('MALFORMED_FAILURE_METADATA','HTTP_STATUS_OUT_OF_RANGE')
    if code==429:return ('CODEX_USAGE_LIMIT','ISOLATED_HTTP_STATUS')
    if code==503:return ('SERVICE_UNAVAILABLE','ISOLATED_HTTP_STATUS')
    if 200<=code<300:return ('NONE','SUCCESS_HTTP_STATUS')
    return ('NONEXTERNAL_HTTP_FAILURE','UNAPPROVED_NONEXTERNAL_HTTP_STATUS')


def _inspection_stage(stage,field):
    """Adversarial injection seam; never records inspection completion."""
    return None


def _completed_stage(stage,field):
    """Explicit false or interruption means inspection did NOT complete."""
    if _inspection_stage(stage,field) is False:
        raise RuntimeError('INCOMPLETE_INSPECTION_EARLY_RETURN')

class ControlFieldLedger:
    """Separate discovery and inspection operations: discovery NEVER inspects.

    Only typed executor control locations are visited. Scientific rows/body
    payloads are intentionally never traversed.
    """
    def __init__(self):
        self.present=set()
        self.inspected=set()
    def discover_path(self,source):
        self.present.add(source)
    def mark_inspected(self,source):
        self.inspected.add(source)
    def missing(self):
        return self.present-self.inspected
    def discover_object(self,obj,source,*,depth=0):
        if not isinstance(obj,dict) or depth>12:return
        for key,value in obj.items():
            if key not in FIELD_SCHEMA:continue
            field=f'{source}.{key}'
            self.discover_path(field)
            kind=FIELD_SCHEMA[key]
            if isinstance(value,dict) and kind in ('text_object_or_null','object_or_null'):
                self.discover_object(value,field,depth=depth+1)
            elif isinstance(value,list) and kind in ('list_or_null','error_group_or_null'):
                for i,member in enumerate(value):
                    src=f'{field}[{i}]';self.discover_path(src)
                    if isinstance(member,dict):self.discover_object(member,src,depth=depth+1)


def decide_availability(result, *, semantic_validator=None):
    signals=[];stops=[];unclassified=[];normalized=[]
    ledger=ControlFieldLedger()
    present=ledger.present;inspected=ledger.inspected;malformed=[]

    def hard(source,kind,evidence):
        item={'source_field':source,'failure_class':kind,'evidence':str(evidence)[:300]}
        stops.append(item)
        if kind=='UNCLASSIFIED_NONEXTERNAL_FAILURE':unclassified.append(item)
        normalized.append({'source_field':source,'classification':kind,'kind':'HARD_STOP'})

    def malformed_type(source,actual):
        malformed.append({'source_field':source,'type':type(actual).__name__})
        hard(source,'MALFORMED_FAILURE_METADATA','UNACCEPTED_CONTROL_TYPE__'+type(actual).__name__)

    def external(source,kind,evidence,pattern):
        signals.append({'classification':kind,'matched_signal':str(evidence),
                        'source_field':source,'matched_pattern':pattern})
        normalized.append({'source_field':source,'classification':kind,'kind':'EXTERNAL'})

    def mark_inspected(source):
        ledger.mark_inspected(source)

    def inspect_text(v,source,*,error_bearing=True):
        if not isinstance(v,str):malformed_type(source,v);return
        if not v.strip():
            if error_bearing:hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_ERROR_FIELD')
            return
        matched=[]
        for cls,pattern in HARD_STOP_PATTERNS:
            if re.search(pattern,v,re.I):
                hard(source,cls,v);matched.append(cls)
        sig=_signal(v)
        if sig:external(source,sig[0],sig[1],sig[1])
        # Check text remaining after approved explicit availability phrases.
        residue=re.sub(r'^\s*(?:(?:ERROR|FATAL|FAILURE)\s*:\s*)+', '',v,flags=re.I)
        for _,pattern in (*USAGE_PATTERNS,*SERVICE_PATTERNS):
            residue=re.sub(pattern,' ',residue,flags=re.I)
        if not matched and GENERIC_FAILURE.search(residue):
            hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE',v)
        elif error_bearing and not matched and not sig:
            hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE',v)

    def inspect_class(v,source):
        if not isinstance(v,str):malformed_type(source,v);return
        if v in EXTERNAL_STATUSES:external(source,EXTERNAL_STATUSES[v],v,'APPROVED_STRUCTURED_STATUS')
        elif v in HARD_STOP_STATUSES:
            hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE' if v=='UNCLASSIFIED_FAILURE' else v,v)
        elif v in ('ERROR','FAILED','INTERRUPTED'):
            # Failure state without a classified cause cannot authorize pause.
            hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE',v)
        elif not v.strip():hard(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_FAILURE_CLASS')
        else:inspect_text(v,source)

    def inspect_object(obj,source,*,depth=0):
        if depth>12:hard(source,'MALFORMED_FAILURE_METADATA','NESTING_EXCEEDED');return
        if not isinstance(obj,dict):malformed_type(source,obj);return
        for key,value in obj.items():
            if key not in FIELD_SCHEMA:continue
            field=f'{source}.{key}'
            kind=FIELD_SCHEMA[key]
            # Ledger discovery occurred in independent PASS A. Inspection only
            # completes AFTER schema/normalization/classification/evidence.
            try:
                _completed_stage('VALIDATE',field)
                _completed_stage('NORMALIZE',field)
                _completed_stage('CLASSIFY',field)
                if value is not None:
                    if kind=='text_or_null':
                        if not isinstance(value,str):malformed_type(field,value)
                        elif value!='':inspect_text(value,field,error_bearing=(key!='message'))
                        elif key in ('error','error_message','failure_message'):
                            hard(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_ERROR')
                    elif kind=='text_object_or_null':
                        if isinstance(value,dict):
                            if not value:hard(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_ERROR_OBJECT')
                            elif not any(k in FIELD_SCHEMA for k in value):
                                hard(field,'MALFORMED_FAILURE_METADATA','ERROR_OBJECT_WITHOUT_SUPPORTED_FIELDS')
                            else:inspect_object(value,field,depth=depth+1)
                        elif isinstance(value,str):
                            if value!='':inspect_text(value,field)
                            else:hard(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_ERROR')
                        else:malformed_type(field,value)
                    elif kind=='object_or_null':
                        if isinstance(value,dict):inspect_object(value,field,depth=depth+1)
                        else:malformed_type(field,value)
                    elif kind=='class_or_null':inspect_class(value,field)
                    elif kind=='list_or_null':
                        if not isinstance(value,list):malformed_type(field,value)
                        else:
                            for i,member in enumerate(value):
                                member_field=f'{field}[{i}]'
                                inspect_member(member,member_field,depth)
                    elif kind=='status_or_null':
                        cls,pattern=classify_http_status(value)
                        if cls=='MALFORMED_FAILURE_METADATA':malformed_type(field,value)
                        elif cls in ('CODEX_USAGE_LIMIT','SERVICE_UNAVAILABLE'):
                            external(field,cls,str(value),pattern)
                        elif cls=='NONEXTERNAL_HTTP_FAILURE':hard(field,cls,str(value))
                    elif kind=='bool_or_null':
                        if type(value) is not bool:malformed_type(field,value)
                        elif key in FLAG_CLASSES and value:hard(field,FLAG_CLASSES[key],value)
                        elif key=='timeout_status' and value:
                            hard(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE','TIMEOUT_NOT_AVAILABILITY')
                    elif kind=='error_group_or_null':
                        if not isinstance(value,list):malformed_type(field,value)
                        else:
                            if value:hard(field,ERROR_GROUP_CLASSES[key],f'GROUP_SIZE={len(value)}')
                            for i,member in enumerate(value):
                                mf=f'{field}[{i}]';inspect_member(member,mf,depth)
                    elif kind=='termination_or_null':
                        if not isinstance(value,str):malformed_type(field,value)
                        elif value not in SUPPORTED_TERMINATIONS:
                            hard(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE',value)
                    elif kind=='return_code_or_null':
                        if type(value) is not int:malformed_type(field,value)
                    elif kind=='raw_text_or_null':
                        if not isinstance(value,str):malformed_type(field,value)
                    else:hard(field,'MALFORMED_FAILURE_METADATA','UNKNOWN_FIELD_SCHEMA_KIND')
                _completed_stage('RECORD',field)
            except Exception as exc:
                hard(field,'MALFORMED_FAILURE_METADATA',
                     'INCOMPLETE_CONTROL_INSPECTION__'+type(exc).__name__)
                # No inspected mark. PRESENT_MINUS_INSPECTED will prevent pause.
                continue
            # For nested objects, failed child inspection also blocks parent
            # completion, even when the parent branch itself returned.
            if any(x.startswith(field+'.') or x.startswith(field+'[') for x in ledger.missing()):
                continue
            mark_inspected(field)

    def inspect_member(member,source,depth):
        try:
            _completed_stage('VALIDATE',source)
            _completed_stage('NORMALIZE',source)
            _completed_stage('CLASSIFY',source)
            if isinstance(member,str):
                if not member.strip():malformed_type(source,member)
                else:inspect_class(member,source)
            elif isinstance(member,dict):
                if not member or not (set(member)&set(FIELD_SCHEMA)):
                    hard(source,'MALFORMED_FAILURE_METADATA','UNSUPPORTED_CONTROL_LIST_MEMBER')
                else:inspect_object(member,source,depth=depth+1)
            else:malformed_type(source,member)
            _completed_stage('RECORD',source)
        except Exception as exc:
            hard(source,'MALFORMED_FAILURE_METADATA',
                 'INCOMPLETE_CONTROL_INSPECTION__'+type(exc).__name__)
            return
        if any(x.startswith(source+'.') or x.startswith(source+'[') for x in ledger.missing()):
            return
        mark_inspected(source)

    if not isinstance(result,dict):
        hard('result','MALFORMED_FAILURE_METADATA','NONOBJECT_EXECUTOR_RESULT');result={}
    # PASS A: discover every present supported field independently of inspection.
    ledger.discover_object(result,'result')
    # PASS A: discover all parsed event objects; no classification yet.

    raw=result.get('raw_stdout') or ''
    parsed_events=[]
    if isinstance(raw,str):
        for i,line in enumerate(raw.splitlines(),1):
            if not line.strip():continue
            src=f'raw_stdout[{i}]'
            try:
                event=json.loads(line)
                if not isinstance(event,dict):raise ValueError('EVENT_NOT_OBJECT')
            except (ValueError,TypeError):
                hard(src,'MALFORMED_OUTPUT','NON_JSON_EXECUTOR_EVENT');continue
            # Event eligibility must not influence control-field discovery.
            ledger.discover_object(event,src)
            parsed_events.append((src,event))
    # All supported control metadata must be discovered before inspection
    # begins, including final-message fields that coexist with rows.
    final=result.get('agent_message') or ''
    if isinstance(final,str) and final.strip():
        try: pre_parsed_final=json.loads(final)
        except (ValueError,TypeError):pre_parsed_final=None
        if isinstance(pre_parsed_final,dict):
            ledger.discover_object(pre_parsed_final,'agent_message')
    # PASS B: normalize and classify root and ALL parsed events, regardless
    # of event type. Event-specific error handling follows discovery.
    inspect_object(result,'result')
    for src,event in parsed_events:
        typ=event.get('type')
        before=len(stops)+len(signals)
        inspect_object(event,src)
        if typ in ERROR_TYPES and before==len(stops)+len(signals):
            hard(src,'UNCLASSIFIED_NONEXTERNAL_FAILURE','UNCLASSIFIED_ERROR_EVENT')

    # PHASE A3: stderr, only error-bearing lines or bounded availability notices.
    stderr=result.get('raw_stderr') or ''
    if isinstance(stderr,str):
        for i,line in enumerate(stderr.splitlines(),1):
            if not line.strip():continue
            if (_signal(line) or GENERIC_FAILURE.search(line)
                or any(re.search(p,line,re.I) for _,p in HARD_STOP_PATTERNS)):
                src=f'raw_stderr[{i}]';ledger.discover_path(src)
                try:
                    _completed_stage('VALIDATE',src)
                    _completed_stage('NORMALIZE',src)
                    _completed_stage('CLASSIFY',src)
                    inspect_text(line,src)
                    _completed_stage('RECORD',src)
                except Exception as exc:hard(src,'MALFORMED_FAILURE_METADATA','INCOMPLETE_STDERR__'+type(exc).__name__)
                else:mark_inspected(src)

    # PHASE A4: final-message control keys are independent of rows/data.
    if isinstance(final,str) and final.strip():
        try:parsed=json.loads(final)
        except (ValueError,TypeError):
            if signals or result.get('return_code') not in (0,None):
                src='agent_message';ledger.discover_path(src)
                try:
                    before=len(signals)+len(stops)
                    inspect_text(final,src)
                    if before==len(signals)+len(stops):hard(src,'MALFORMED_OUTPUT','UNREADABLE_ERROR_FINAL')
                except Exception as exc:hard(src,'MALFORMED_FAILURE_METADATA','INCOMPLETE_FINAL__'+type(exc).__name__)
                else:mark_inspected(src)
        else:
            if isinstance(parsed,dict):
                inspect_object(parsed,'agent_message')
                if 'rows' in parsed and signals and semantic_validator is not None:
                    # Independent validator failure overrides any usage pause.
                    try:semantic_validator(parsed)
                    except Exception as exc:hard('agent_message.rows','VALIDATION_FAILURE',type(exc).__name__)
                    else:hard('agent_message.rows','VALIDATION_FAILURE','COMPLETED_OUTPUT_AND_AVAILABILITY_ERROR')
                elif 'rows' not in parsed and signals:
                    # A final JSON object without classified error content may
                    # conflict with a signal sourced elsewhere.
                    supported=[k for k in parsed if k in FIELD_SCHEMA]
                    if not supported and parsed:
                        hard('agent_message','UNCLASSIFIED_NONEXTERNAL_FAILURE','UNEXPLAINED_ERROR_FINAL')
            elif signals:hard('agent_message','MALFORMED_OUTPUT','NONOBJECT_JSON_FINAL')

    term=result.get('termination_state')
    if signals and result.get('return_code')==0 and term=='NORMAL_SUCCESS':
        hard('result.return_code','VALIDATION_FAILURE','EXTERNAL_ERROR_WITH_SUCCESS_RETURN')
    if len({s['classification'] for s in signals})>1:
        hard('external_signals','UNCLASSIFIED_NONEXTERNAL_FAILURE','INCONSISTENT_EXTERNAL_CLASSES')
    if ledger.missing():hard('collector','MALFORMED_FAILURE_METADATA','UNINSPECTED_CONTROL_FIELDS')

    # PHASE B: only after structural normalization and ALL evidence channels.
    if stops:decision='CONTROLLED_STOP';classification='CONFLICTING_OR_UNKNOWN_FAILURE'
    elif signals:decision='PAUSED_EXTERNAL_AVAILABILITY';classification=signals[0]['classification']
    else:decision='NO_EXTERNAL_SIGNAL';classification='NONE'
    first=signals[0] if signals else {}
    return {
        'classification':classification,'decision':decision,'final_decision':decision,
        'matched_signal':first.get('matched_signal'),'matched_pattern':first.get('matched_pattern'),
        'source_field':first.get('source_field'),'conflicting_failure_present':bool(stops),
        'signal_count':len(signals),'conflict_kinds':sorted({x['failure_class'] for x in stops}),
        'external_signal_detected':bool(signals),'external_signal_source':first.get('source_field'),
        'external_signal_pattern_or_status':first.get('matched_pattern'),
        'conflicting_failure_detected':bool(stops),
        'conflicting_failure_source':stops[0]['source_field'] if stops else None,
        'conflicting_failure_class':stops[0]['failure_class'] if stops else None,
        'signal_evidence':signals,'conflict_evidence':stops,
        'inspected_failure_fields':sorted(inspected),
        'detected_hard_stop_classes':sorted({x['failure_class'] for x in stops}),
        'unclassified_failure_evidence':unclassified,
        'supported_control_fields_present':sorted(present),
        'supported_control_fields_inspected':sorted(inspected),
        'malformed_control_fields':malformed,
        'normalized_failure_evidence':normalized,
        'hard_stop_classes':sorted({x['failure_class'] for x in stops}),
        'external_signals':signals,
        'fields_present_minus_fields_inspected':sorted(ledger.missing()),
        'control_field_discovery':'ALL_PARSED_EVENTS_EVENT_TYPE_INVARIANT_CLASSIFICATION',
        'precedence_algorithm':'V6_EVENT_INDEPENDENT_CONTROL_FIELDS__INSPECTION_COMPLETION__STOP_BEFORE_PAUSE',
        'control_field_schema_version':'BATCH0004_AVAILABILITY_CONTROL_FIELDS_V6',
    }
