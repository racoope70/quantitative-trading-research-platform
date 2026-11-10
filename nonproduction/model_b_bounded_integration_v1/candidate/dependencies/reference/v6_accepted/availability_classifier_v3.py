#!/usr/bin/env python3
"""Batch0004 V3 two-phase availability adjudication, synthetic-ready only.

Collect *all* failure-bearing evidence before making a decision. Centralized
hard-stop taxonomy overrides approved, bounded external signals everywhere.
This component does not invoke Codex or change scientific rules.
"""
from __future__ import annotations
import json
import re
from availability_classifier_v1 import (
    USAGE_PATTERNS, SERVICE_PATTERNS, STATUS_FIELDS, ERROR_TYPES,
    _status, _signal,
)

# Central taxonomy. Every pattern matches an explicit class, never a numeric
# substring or generic successful-content phrase. One taxonomy for all channels.
HARD_STOP_PATTERNS = (
    ('SEMANTIC_FAILURE', r'\b(?:semantic (?:validation |adjudication |review )?(?:failure|failed|error|mismatch)|(?:semantic|scientific) inconsistency|review incomplete|incomplete adjudication)\b'),
    ('VALIDATION_FAILURE', r'\b(?:validation (?:failure|failed|error|mismatch)|invalid (?:output|disposition|reason)|wrong (?:identity|position)|(?:identity|position) mismatch|missing (?:identity|position|records|rows))\b'),
    ('IMPLEMENTATION_FAILURE', r'\b(?:implementation (?:failure|failed|error|defect)|(?:software|runtime|logic|coding|internal) (?:error|failure|defect)|traceback|assertionerror|typeerror|keyerror)\b'),
    ('IDENTITY_FAILURE', r'\b(?:identity (?:failure|failed|error)|(?:invalid|duplicate|unexpected|missing) identit(?:y|ies)|identity(?:\s+coverage)? mismatch)\b'),
    ('POSITION_FAILURE', r'\b(?:position (?:failure|failed|error)|(?:invalid|duplicate|unexpected|missing) positions?|position(?:\s+coverage)? mismatch|wrong positions?)\b'),
    ('ROW_COUNT_FAILURE', r'\b(?:row[ -]?count (?:failure|failed|error|mismatch)|wrong (?:row[ -]?count|number of rows)|(?:incorrect|missing|extra|duplicate) rows|(?:rows|row[ -]?count) (?:expected|mismatch))\b'),
    ('MALFORMED_OUTPUT', r'\b(?:malformed (?:output|json|response|result)|(?:invalid|corrupt) (?:json|serialization)|parse (?:failure|failed|error))\b'),
    ('SERIALIZATION_FAILURE', r'\b(?:serialization (?:failure|failed|error|mismatch)|failed to seriali[sz]e|serialization error)\b'),
    ('READBACK_FAILURE', r'\b(?:readback|deserialization|read[- ]back) (?:failure|failed|error|mismatch)\b'),
    ('ISOLATION_FAILURE', r'\b(?:isolation (?:failure|failed|error|breach)|(?:primary|independent) (?:data|output|leak) (?:contamination|leak)|data leakage|cross[- ]role contamination)\b'),
    ('UNKNOWN_EXECUTOR_FAILURE', r'\b(?:unknown|unexpected|unclassified) (?:executor |runtime |process )?(?:failure|failed|error|exception)\b'),
    ('UNCLASSIFIED_NONEXTERNAL_FAILURE', r'\b(?:unclassified failure|unknown failure|unhandled exception|unrecognized failure|unidentified error)\b'),
)
EXTERNAL_STATUSES = {
    'CODEX_USAGE_LIMIT': 'CODEX_USAGE_LIMIT',
    'CODEX_QUOTA_OR_CREDIT_EXHAUSTION': 'CODEX_USAGE_LIMIT',
    'SERVICE_UNAVAILABLE': 'SERVICE_UNAVAILABLE',
}
HARD_STOP_STATUSES = {
    'SEMANTIC_FAILURE','VALIDATION_FAILURE','IMPLEMENTATION_FAILURE','IDENTITY_FAILURE',
    'POSITION_FAILURE','ROW_COUNT_FAILURE','MALFORMED_OUTPUT','SERIALIZATION_FAILURE',
    'READBACK_FAILURE','ISOLATION_FAILURE','UNKNOWN_EXECUTOR_FAILURE',
    'UNCLASSIFIED_FAILURE','UNCLASSIFIED_NONEXTERNAL_FAILURE',
}
FLAG_CLASSES = {
    'semantic_failure': 'SEMANTIC_FAILURE',
    'validation_failure': 'VALIDATION_FAILURE',
    'implementation_failure': 'IMPLEMENTATION_FAILURE',
    'identity_mismatch':'IDENTITY_FAILURE','identity_failure':'IDENTITY_FAILURE',
    'position_mismatch':'POSITION_FAILURE','position_failure':'POSITION_FAILURE',
    'row_count_failure':'ROW_COUNT_FAILURE','malformed_output':'MALFORMED_OUTPUT',
    'serialization_failure':'SERIALIZATION_FAILURE','readback_failure':'READBACK_FAILURE',
    'isolation_failure':'ISOLATION_FAILURE','unknown_executor_failure':'UNKNOWN_EXECUTOR_FAILURE',
}
# Reused for root result, executor errors, metadata, and final JSON, never if/elif.
FAILURE_TEXT_FIELDS = (
    'error','message','detail','error_description','reason','failure_reason',
    'termination_reason','validation_error','semantic_error','implementation_error',
    'identity_error','position_error','serialization_error','readback_error',
    'isolation_error','failure_message','error_message',
)
CHILD_OBJECT_FIELDS = ('error','item','response','termination_metadata',
    'executor_metadata','failure_metadata','validation_metadata','result_metadata')
ERROR_GROUP_CLASSES = {
    'semantic_errors':'SEMANTIC_FAILURE',
    'validation_errors':'VALIDATION_FAILURE',
    'implementation_errors':'IMPLEMENTATION_FAILURE',
    'identity_errors':'IDENTITY_FAILURE',
    'position_errors':'POSITION_FAILURE',
    'row_count_errors':'ROW_COUNT_FAILURE',
    'serialization_errors':'SERIALIZATION_FAILURE',
    'readback_errors':'READBACK_FAILURE',
    'isolation_errors':'ISOLATION_FAILURE',
    'unknown_errors':'UNKNOWN_EXECUTOR_FAILURE',
}
# Explicit nonavailability-failure tokens remaining after removal of a bounded
# external phrase. Distinguishes e.g. quota + unrecognized failure from quota-only.
GENERIC_FAILURE = re.compile(r'\b(?:failure|failed|error|mismatch|exception|corrupt|invalid|broken|malformed|defect|crash(?:ed)?|denied)\b',re.I)


def decide_availability(result, *, semantic_validator=None):
    """Global Phase A collect; Phase B decide. Unknown error evidence fails shut.

    The signal and conflict arrays record each inspected channel and never
    return early. Semantic row validation is still separately enforced by V3.
    """
    signals=[]; conflicts=[]; inspected=[]; unclassified=[]

    def conflict(source, cls, evidence=''):
        entry={'source_field':source,'failure_class':cls,'evidence':str(evidence)[:300]}
        conflicts.append(entry)
        if cls=='UNCLASSIFIED_NONEXTERNAL_FAILURE':unclassified.append(entry)

    def signal(source, cls, evidence, pattern):
        signals.append({'classification':cls,'matched_signal':str(evidence),
                        'source_field':source,'matched_pattern':pattern})

    def inspect_text(text,source,*,error_bearing=True):
        inspected.append(source)
        if not isinstance(text,str):
            conflict(source,'MALFORMED_OUTPUT','NONSTRING_ERROR_FIELD');return
        if not text.strip():
            if error_bearing:conflict(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE','EMPTY_ERROR_FIELD')
            return
        categories=[cls for cls,pattern in HARD_STOP_PATTERNS if re.search(pattern,text,re.I)]
        for cls in categories:conflict(source,cls,text)
        s=_signal(text)
        if s:signal(source,s[0],s[1],s[1])
        # An independently explicit but unrecognized nonavailability failure
        # also wins over an affirmative external phrase in the SAME text.
        residue=re.sub(r'^\s*(?:(?:ERROR|FATAL|FAILURE)\s*:\s*)+', '', text,flags=re.I)
        for _,pattern in (*USAGE_PATTERNS,*SERVICE_PATTERNS):
            residue=re.sub(pattern,' ',residue,flags=re.I)
        if not categories and GENERIC_FAILURE.search(residue):
            conflict(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE',text)
        elif error_bearing and not categories and not s:
            conflict(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE',text)

    def inspect_object(obj,source,*,error_context=True,depth=0):
        if depth>12:
            conflict(source,'MALFORMED_OUTPUT','EXCEEDED_NESTING_LIMIT');return
        if not isinstance(obj,dict):
            conflict(source,'MALFORMED_OUTPUT','NONOBJECT_FAILURE_METADATA');return
        inspected.append(source)
        for key,value in obj.items():
            field=source+'.'+str(key)
            if key in STATUS_FIELDS:
                inspected.append(field)
                approved=_status(value)
                if approved is not None:
                    signal(field,'CODEX_USAGE_LIMIT' if approved==429 else 'SERVICE_UNAVAILABLE',approved,'ISOLATED_HTTP_STATUS')
                elif error_context and value not in (None,'',0,200):
                    # Other status numbers are not established external pauses.
                    conflict(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE',value)
            elif key in ('failure_status','error_class','failure_class'):
                inspected.append(field)
                if isinstance(value,str) and value in EXTERNAL_STATUSES:
                    signal(field,EXTERNAL_STATUSES[value],value,'APPROVED_STRUCTURED_STATUS')
                elif isinstance(value,str) and value in HARD_STOP_STATUSES:
                    conflict(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE' if value=='UNCLASSIFIED_FAILURE' else value,value)
                elif value not in (None,'','ERROR','FAILED','INTERRUPTED'):
                    if isinstance(value,str):inspect_text(value,field)
                    else:conflict(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE',value)
            elif key in FLAG_CLASSES:
                inspected.append(field)
                if value is True:conflict(field,FLAG_CLASSES[key],value)
                elif value not in (None,False,''):conflict(field,'UNCLASSIFIED_NONEXTERNAL_FAILURE',value)
            elif key in ERROR_GROUP_CLASSES:
                inspected.append(field)
                if value:conflict(field,ERROR_GROUP_CLASSES[key],value)
            elif key in CHILD_OBJECT_FIELDS and isinstance(value,dict):
                inspect_object(value,field,error_context=True,depth=depth+1)
            elif key in FAILURE_TEXT_FIELDS:
                # Each present field independently evaluated. No elif on
                # error/message; no discard of nested event messages.
                if value is not None and value!='':
                    inspect_text(value,field,error_bearing=True)
                elif key=='error' and error_context:
                    inspected.append(field)
            elif key=='failure_statuses' and isinstance(value,list):
                for i,v in enumerate(value):
                    inspect_text(v,f'{field}[{i}]')
            elif key in CHILD_OBJECT_FIELDS and value is not None:
                inspect_text(value,field)

    if not isinstance(result,dict):
        conflict('result','MALFORMED_OUTPUT','NONDICT_EXECUTOR_RESULT')
        result={}
    # PHASE A: accumulate all relevant channels BEFORE any pause is permitted.
    inspect_object(result,'result',error_context=False)

    raw=result.get('raw_stdout','')
    if not isinstance(raw,str):
        conflict('raw_stdout','MALFORMED_OUTPUT','NONSTRING_EVENTS');raw=''
    for i,line in enumerate(raw.splitlines(),1):
        if not line.strip():continue
        source=f'raw_stdout[{i}]'
        try:
            event=json.loads(line)
            if not isinstance(event,dict):raise ValueError('EVENT_NOT_OBJECT')
        except (ValueError,TypeError):
            conflict(source,'MALFORMED_OUTPUT','NON_JSON_ERROR_EVENT');continue
        kind=event.get('type')
        eligible=(kind in ERROR_TYPES or ('error' in event and event['error'] not in (None,''))
                  or event.get('failure_status') not in (None,'')
                  or any(event.get(k) for k in (*ERROR_GROUP_CLASSES,*FLAG_CLASSES)))
        if not eligible:continue
        nsignals=len(signals);nconflicts=len(conflicts)
        inspect_object(event,source)
        if len(signals)==nsignals and len(conflicts)==nconflicts:
            conflict(source,'UNCLASSIFIED_NONEXTERNAL_FAILURE','UNRECOGNIZED_ERROR_EVENT')

    stderr=result.get('raw_stderr','')
    if not isinstance(stderr,str):
        conflict('raw_stderr','MALFORMED_OUTPUT','NONSTRING_STDERR');stderr=''
    for i,line in enumerate(stderr.splitlines(),1):
        if not line.strip():continue
        if (_signal(line) or GENERIC_FAILURE.search(line)
            or any(re.search(p,line,re.I) for _,p in HARD_STOP_PATTERNS)):
            inspect_text(line,f'raw_stderr[{i}]')

    final=result.get('agent_message','')
    if not isinstance(final,str):
        conflict('agent_message','MALFORMED_OUTPUT','NONSTRING_FINAL');final=''
    if final.strip():
        try:obj=json.loads(final)
        except (ValueError,TypeError):
            # The normal non-JSON *successful* final is for V3 validation.
            # Explicit non-JSON standalone error notices remain eligible.
            if signals or result.get('return_code') not in (0,None):
                before=len(signals)
                inspect_text(final,'agent_message',error_bearing=True)
                if len(signals)==before and not any(x['source_field']=='agent_message' for x in conflicts):
                    conflict('agent_message','MALFORMED_OUTPUT','NONJSON_FAILURE_FINAL')
        else:
            if not isinstance(obj,dict):
                if signals:conflict('agent_message','MALFORMED_OUTPUT','NONOBJECT_FINAL')
            elif 'rows' in obj:
                if signals:
                    conflict('agent_message.rows','VALIDATION_FAILURE','ROWS_PRESENT_WITH_EXTERNAL_ERROR')
                    if semantic_validator is not None:
                        try:semantic_validator(obj)
                        except Exception as exc:conflict('agent_message.rows','VALIDATION_FAILURE',type(exc).__name__)
            else:
                inspected.append('agent_message')
                before=len(signals);before_conflict=len(conflicts)
                inspect_object(obj,'agent_message')
                # An unexplained error-result object concurrent with a pause
                # cannot be accepted merely because another channel signalled.
                if signals and len(signals)==before and len(conflicts)==before_conflict:
                    conflict('agent_message','UNCLASSIFIED_NONEXTERNAL_FAILURE','UNEXPLAINED_FINAL_ERROR')

    term=result.get('termination_state')
    if term not in ('ERROR','FAILED','INTERRUPTED','NORMAL_SUCCESS','TIMEOUT',None):
        conflict('result.termination_state','UNCLASSIFIED_NONEXTERNAL_FAILURE',term)
    if result.get('timeout_status') is True:
        conflict('result.timeout_status','UNCLASSIFIED_NONEXTERNAL_FAILURE','TIMEOUT_NOT_APPROVED_AVAILABILITY')
    if signals and result.get('return_code')==0 and term=='NORMAL_SUCCESS':
        conflict('result.return_code','VALIDATION_FAILURE','EXTERNAL_ERROR_WITH_SUCCESS_RETURN')
    if len({s['classification'] for s in signals})>1:
        conflict('signals','UNCLASSIFIED_NONEXTERNAL_FAILURE','INCONSISTENT_EXTERNAL_CLASSES')

    # PHASE B: global precedence, *after* complete evidence collection.
    if conflicts:decision='CONTROLLED_STOP';classification='CONFLICTING_OR_UNKNOWN_FAILURE'
    elif signals:decision='PAUSED_EXTERNAL_AVAILABILITY';classification=signals[0]['classification']
    else:decision='NO_EXTERNAL_SIGNAL';classification='NONE'
    head=signals[0] if signals else {}
    return {
        'classification':classification,'matched_signal':head.get('matched_signal'),
        'source_field':head.get('source_field'),'matched_pattern':head.get('matched_pattern'),
        'conflicting_failure_present':bool(conflicts),'decision':decision,
        'signal_count':len(signals),'conflict_kinds':sorted({c['failure_class'] for c in conflicts}),
        'external_signal_detected':bool(signals),'external_signal_source':head.get('source_field'),
        'external_signal_pattern_or_status':head.get('matched_pattern'),
        'conflicting_failure_detected':bool(conflicts),
        'conflicting_failure_source':conflicts[0]['source_field'] if conflicts else None,
        'conflicting_failure_class':conflicts[0]['failure_class'] if conflicts else None,
        'final_decision':decision,'signal_evidence':signals,'conflict_evidence':conflicts,
        'inspected_failure_fields':sorted(set(inspected)),
        'detected_hard_stop_classes':sorted({c['failure_class'] for c in conflicts}),
        'unclassified_failure_evidence':unclassified,
        'precedence_algorithm':'PHASE_A_COLLECT_ALL__PHASE_B_STOP_BEFORE_PAUSE',
    }
