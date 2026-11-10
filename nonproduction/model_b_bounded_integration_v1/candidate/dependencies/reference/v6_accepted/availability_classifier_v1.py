#!/usr/bin/env python3
"""BATCH0004 availability decision, explicit + fail closed, version 1.

No arbitrary numeric substring heuristics. Conflicting independent errors override
an external-availability signal. Evaluation reads preserved event strings only.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass

ERROR_TYPES={'error','turn.failed','thread.failed','item.failed'}
# Each bounded phrase is an affirmative signal in a machine-identified error event.
USAGE_PATTERNS=(
 ('usage_limit',r"\b(?:you(?:'|’)?ve hit your usage limit|usage limit (?:reached|exceeded)|hit your usage limit)\b"),
 ('quota_exhausted',r'\bquota\s+(?:exhausted|exceeded|depleted)\b'),
 ('credits_exhausted',r'\b(?:credits?\s+(?:exhausted|depleted)|out of credits)\b'),
 ('rate_limit',r'\b(?:rate\s+limit\s+(?:reached|exceeded)|rate\s+limited|too many requests)\b'),
)
SERVICE_PATTERNS=(
 ('service_unavailable',r'\b(?:service\s+(?:temporarily\s+)?unavailable|service\s+disruption|upstream\s+unavailable)\b'),
 ('bad_gateway',r'\b(?:bad gateway|gateway timeout)\b'),
)
# Approved isolated machine fields, not arbitrary string digits.
STATUS_FIELDS=('http_status','http_status_code','status_code','response_status')
# Top-level semantically meaningful failure indications always take precedence.
CONFLICT_PATTERNS=(
 r'\b(?:semantic|validation|identity|position|serialization|readback|implementation|unknown executor|unexpected executor)\s+(?:error|failure|failed|mismatch)\b',
 r'\b(?:error|failure|failed|mismatch)\s+(?:in|at|with)\s+(?:semantic|validation|identity|position|implementation)\b',
 r'\b(?:semantic\s+(?:validation|adjudication|review)\s+(?:failed|failure|error|mismatch)|wrong row count|rows expected|not reviewed|review incomplete|cannot complete|incomplete adjudication|traceback|invalid output|missing records)\b',
)

def _status(v):
    if type(v) is int:return v if v in (429,503) else None
    if isinstance(v,str) and v in ('429','503'):return int(v)
    return None

def _signal(text):
    if not isinstance(text,str):return None
    for pat_id,pat in USAGE_PATTERNS:
        if re.search(pat,text,re.I):return ('CODEX_USAGE_LIMIT',pat_id)
    for pat_id,pat in SERVICE_PATTERNS:
        if re.search(pat,text,re.I):return ('SERVICE_UNAVAILABLE',pat_id)
    return None

def _conflict_text(text):
    if not isinstance(text,str) or not text.strip():return False
    return any(re.search(p,text,re.I) for p in CONFLICT_PATTERNS)

def decide_availability(result, *, semantic_validator=None):
    """Return audit-safe explicit decision object, never a bare regex match.

    semantic_validator(final_dict) raises on output validation problems; used for
    external + independently invalid semantic output. No validator => an output
    with `rows` is a conflict when a purported external interruption exists.
    """
    signals=[]; conflicts=[]; parse_problem=None
    raw=result.get('raw_stdout','')
    if not isinstance(raw,str):parse_problem='NONSTRING_RAW_EVENTS';events=[]
    else:
        events=[]
        for i,line in enumerate(raw.splitlines(),1):
            if not line.strip():continue
            try:
                e=json.loads(line)
                if not isinstance(e,dict):raise ValueError('NOT_OBJECT')
                events.append((i,e))
            except (ValueError,TypeError):
                parse_problem=f'NON_JSON_EVENT_LINE_{i}';break
    if parse_problem:conflicts.append({'source_field':'raw_stdout','kind':parse_problem})
    for i,event in events:
        event_type=event.get('type')
        err=event.get('error')
        considered=(event_type in ERROR_TYPES or (isinstance(err,dict) and bool(err)))
        if not considered:continue
        details=[]
        if isinstance(err,dict):
            for k in ('message','detail','error_description'):
                if isinstance(err.get(k),str):details.append((f'event[{i}].error.{k}',err[k]))
        elif isinstance(err,str): details.append((f'event[{i}].error',err))
        if isinstance(event.get('message'),str): details.append((f'event[{i}].message',event['message']))
        if isinstance(event.get('item'),dict):
            for k in ('error','message'):
                if isinstance(event['item'].get(k),str):details.append((f'event[{i}].item.{k}',event['item'][k]))
        # Code must be typed/separate status, never embedded in prose.
        isolated=[]
        for parent, prefix in ((event,f'event[{i}]'),(err,f'event[{i}].error')):
            if not isinstance(parent,dict):continue
            for key in STATUS_FIELDS:
                if key in parent and _status(parent[key]) is not None:
                    val=_status(parent[key]);isolated.append((f'{prefix}.{key}',val))
            # Nested response.status_code is structured too.
            resp=parent.get('response')
            if isinstance(resp,dict):
                for key in STATUS_FIELDS:
                    if key in resp and _status(resp[key]) is not None:
                        isolated.append((f'{prefix}.response.{key}',_status(resp[key])))
        event_signals=[];event_conflict=False
        for field,v in isolated:
            event_signals.append({'classification':'CODEX_USAGE_LIMIT' if v==429 else 'SERVICE_UNAVAILABLE',
                                  'matched_signal':str(v),'source_field':field,'matched_pattern':'ISOLATED_HTTP_STATUS'})
        for field,text in details:
            sig=_signal(text)
            if sig:
                event_signals.append({'classification':sig[0],'matched_signal':sig[1],
                                      'source_field':field,'matched_pattern':sig[1]})
            if _conflict_text(text):
                event_conflict=True
                conflicts.append({'source_field':field,'kind':'INDEPENDENT_NONAVAILABILITY_FAILURE'})
            # Unknown non-empty error detail alongside external evidence is an
            # independent error and must not be silently converted into pause.
            if text.strip() and sig is None and not _conflict_text(text):
                event_conflict=True
                conflicts.append({'source_field':field,'kind':'UNKNOWN_ERROR_TEXT'})
        signals.extend(event_signals)
        if not event_signals and not event_conflict:
            conflicts.append({'source_field':f'event[{i}]','kind':'UNCLASSIFIED_ERROR_EVENT'})
    stderr=result.get('raw_stderr','')
    if not isinstance(stderr,str):conflicts.append({'source_field':'raw_stderr','kind':'NONSTRING_STDERR'})
    elif stderr.strip():
        for i,line in enumerate(stderr.splitlines(),1):
            if not re.search(r'\b(?:ERROR|FATAL|FAIL(?:ED|URE)?)\b',line,re.I):continue
            sig=_signal(line)
            if sig:
                signals.append({'classification':sig[0],'matched_signal':sig[1],
                                'source_field':f'stderr[{i}]','matched_pattern':sig[1]})
            else:
                conflicts.append({'source_field':f'stderr[{i}]','kind':'UNCLASSIFIED_STDERR_FAILURE'})
    final=result.get('agent_message','')
    if not isinstance(final,str):
        conflicts.append({'source_field':'agent_message','kind':'NONSTRING_FINAL_MESSAGE'})
    elif final.strip() and signals:
        try:obj=json.loads(final)
        except (ValueError,TypeError):
            # An isolated, same-class availability notice is not an attempted
            # semantic result, but mixed or unknown malformed output conflicts.
            sig=_signal(final)
            if not sig:conflicts.append({'source_field':'agent_message','kind':'MALFORMED_OUTPUT'})
            elif _conflict_text(final):conflicts.append({'source_field':'agent_message','kind':'CONFLICTING_OUTPUT_TEXT'})
            elif not any(s['classification']==sig[0] for s in signals):
                conflicts.append({'source_field':'agent_message','kind':'UNBOUND_EXTERNAL_FINAL'})
        else:
            if not isinstance(obj,dict):
                conflicts.append({'source_field':'agent_message','kind':'NONOBJECT_OUTPUT'})
            elif 'rows' in obj:
                if semantic_validator is None:
                    conflicts.append({'source_field':'agent_message.rows','kind':'UNVALIDATED_SEMANTIC_OUTPUT'})
                else:
                    try:semantic_validator(obj)
                    except Exception:
                        conflicts.append({'source_field':'agent_message.rows','kind':'INVALID_SEMANTIC_OUTPUT'})
                    else:
                        # Completed valid semantic output *and* error contradict.
                        conflicts.append({'source_field':'agent_message.rows','kind':'SEMANTIC_OUTPUT_WITH_AVAILABILITY_ERROR'})
            else:
                other_keys=set(obj)-{'error','message','status'}
                if other_keys:
                    conflicts.append({'source_field':'agent_message','kind':'UNEXPECTED_OUTPUT_FIELDS'})
                txt=obj.get('error') or obj.get('message') or ''
                if not isinstance(txt,str) or not _signal(txt):
                    conflicts.append({'source_field':'agent_message','kind':'UNEXPLAINED_FINAL_OUTPUT'})
                elif not any(s['classification']==_signal(txt)[0] for s in signals):
                    conflicts.append({'source_field':'agent_message','kind':'UNBOUND_EXTERNAL_FINAL'})
    # Independent structured result failures cannot be silently made resumable.
    for key in ('semantic_failure','validation_failure','implementation_failure','identity_mismatch','serialization_failure','readback_failure'):
        if result.get(key):conflicts.append({'source_field':f'result.{key}','kind':'EXPLICIT_CONFLICTING_FAILURE'})
    # result.failure_status from executor can be an unrelated reason as well.
    fs=result.get('failure_status')
    if isinstance(fs,str) and fs and _signal(fs) is None:
        conflicts.append({'source_field':'result.failure_status','kind':'UNKNOWN_FAILURE_STATUS'})
    class_names={s['classification'] for s in signals}
    if len(class_names)>1:
        conflicts.append({'source_field':'raw_events','kind':'MULTIPLE_AVAILABILITY_CLASSES'})
    if signals and result.get('return_code')==0 and result.get('termination_state')=='NORMAL_SUCCESS':
        conflicts.append({'source_field':'result.return_code','kind':'SUCCESS_CONFLICTS_WITH_ERROR_EVENT'})
    # Empty error fields may coexist with one legitimate explicit notice.
    if conflicts:
        decision='CONTROLLED_STOP'
        classification='CONFLICTING_OR_UNKNOWN_FAILURE'
    elif signals:
        decision='PAUSED_EXTERNAL_AVAILABILITY'
        classification=signals[0]['classification']
    else:
        decision='NO_EXTERNAL_SIGNAL'
        classification='NONE'
    first=signals[0] if signals else {}
    return {'classification':classification,'matched_signal':first.get('matched_signal'),
            'source_field':first.get('source_field'), 'matched_pattern':first.get('matched_pattern'),
            'conflicting_failure_present':bool(conflicts), 'decision':decision,
            'signal_count':len(signals),'conflict_kinds':sorted(set(c['kind'] for c in conflicts))}
