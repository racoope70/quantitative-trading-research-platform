#!/usr/bin/env python3
"""PROSPECTIVE / NONPRODUCTION V7. Narrow auxiliary model-manager timeout exception.

Never substitute for the accepted historical V6 classifier or reclassify any
historical U0012 attempt. External integrity proof must come from an accepted
independent verifier in a future, separately reviewed runtime integration.
The new policy is fail-closed if any integrity proof is missing or ambiguous.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import sys

# Immutable historical classifier, read-only import. Not a new runtime activation.
_HIST=Path(__file__).resolve().parent/'historical_v6'
if str(_HIST) not in sys.path:
    sys.path.insert(0,str(_HIST))
import availability_classifier_v6 as historical_v6

NEW_POLICY_VERSION='BATCH0004_AUXILIARY_MODELS_MANAGER_REFRESH_TIMEOUT_V7_PROSPECTIVE_NONPRODUCTION_V2'
# Full-line, specific source and message. No substring matches or generic timeouts.
UNKNOWN_TIMEOUT_PATTERN = re.compile(r'\b(?:timeout|time[ -]?out|timed out|timing out)\b', re.I)
AUXILIARY_REFRESH_TIMEOUT_PATTERN = re.compile(
    r'(?:\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s+)?'
    r'ERROR\s+codex_models_manager::manager:\s+'
    r'failed to refresh available models:\s+request timed out',
    flags=re.ASCII,
)

@dataclass(frozen=True, slots=True)
class VerifiedOperationalIntegrity:
    """Externally attested operational checks, NOT scientific answer favorability.

    IMPORTANT: these are claims in a prospective interface, not a verifier.
    An eventual activation must supply each field through an independently
    trusted verifier, never by parsing arbitrary executor self-claims.
    """
    expected_rows: int
    observed_rows: int
    complete_output: bool
    output_schema_valid: bool
    identities_valid: bool
    positions_valid: bool
    serialization_readback_pass: bool
    semantic_subprocess_timeout: bool
    semantic_execution_exception: bool
    output_truncation: bool
    transport_interruption: bool
    external_availability_present: bool
    source_attested: bool


def positive_auxiliary_source(line: str) -> bool:
    """Positive source identification, not an availability/timeout heuristic."""
    return type(line) is str and AUXILIARY_REFRESH_TIMEOUT_PATTERN.fullmatch(line.strip()) is not None


def _integrity_complete(proof, result):
    if type(proof) is not VerifiedOperationalIntegrity or not isinstance(result,dict):
        return False
    bool_fields=('complete_output','output_schema_valid','identities_valid',
        'positions_valid','serialization_readback_pass','semantic_subprocess_timeout',
        'semantic_execution_exception','output_truncation','transport_interruption',
        'external_availability_present','source_attested')
    if any(type(getattr(proof,f)) is not bool for f in bool_fields):return False
    if type(proof.expected_rows) is not int or type(proof.observed_rows) is not int:return False
    if proof.expected_rows<=0 or proof.observed_rows!=proof.expected_rows:return False
    if not all((proof.complete_output,proof.output_schema_valid,proof.identities_valid,
                proof.positions_valid,proof.serialization_readback_pass,proof.source_attested)):
        return False
    if any((proof.semantic_subprocess_timeout,proof.semantic_execution_exception,
            proof.output_truncation,proof.transport_interruption,proof.external_availability_present)):
        return False
    return (type(result.get('return_code')) is int and result['return_code']==0
            and result.get('termination_state')=='NORMAL_SUCCESS'
            and type(result.get('timeout_status')) is bool
            and result['timeout_status'] is False)


def _project_current_conflicts(outcome, stops, normalized):
    """Keep the *effective* V7 verdict internally consistent.

    Original, immutable V6 diagnostics remain separately accessible through
    `historical_v6_verdict`, including the original hard-stop ledger. All
    top-level conflict fields describe the new prospective effective verdict.
    """
    kinds=sorted({entry['failure_class'] for entry in stops})
    unclassified=[entry for entry in stops
                  if entry['failure_class']=='UNCLASSIFIED_NONEXTERNAL_FAILURE']
    outcome['conflict_evidence']=stops
    outcome['conflicting_failure_present']=bool(stops)
    outcome['conflicting_failure_detected']=bool(stops)
    outcome['conflicting_failure_source']=stops[0]['source_field'] if stops else None
    outcome['conflicting_failure_class']=stops[0]['failure_class'] if stops else None
    outcome['conflict_kinds']=kinds
    outcome['hard_stop_classes']=kinds
    outcome['detected_hard_stop_classes']=kinds
    outcome['unclassified_failure_evidence']=unclassified
    outcome['normalized_failure_evidence']=normalized


def decide_availability(result, *, integrity=None, semantic_validator=None):
    """V6-first, classify exactly one positively identified auxiliary stderr.

    Never suppress any other V6 hard-stop, malformed metadata, external signal,
    or incomplete ledger. Return V6 unchanged for all non-exception paths,
    with diagnostic extension fields describing the prospective policy.
    """
    baseline=historical_v6.decide_availability(result,semantic_validator=semantic_validator)
    outcome=dict(baseline)
    # Do not allow the future effective V7 verdict to overwrite historical V6.
    outcome['historical_v6_verdict']=baseline
    outcome['new_policy_version']=NEW_POLICY_VERSION
    outcome['historical_v6_decision']=baseline['decision']
    outcome['historical_v6_classification']=baseline['classification']
    outcome['auxiliary_diagnostic_nonblocking']=False
    outcome['positive_auxiliary_source_identified']=False
    outcome['operational_classification']='V6_DECISION_PRESERVED'

    if not isinstance(result,dict):return outcome
    if (baseline['decision']=='NO_EXTERNAL_SIGNAL' and
        type(result.get('return_code')) is int and result['return_code']==0 and
        result.get('termination_state')=='NORMAL_SUCCESS' and
        type(result.get('timeout_status')) is bool and not result['timeout_status']):
        outcome['operational_classification']='NORMAL_SUCCESS'
    stderr=result.get('raw_stderr')
    if type(stderr) is not str:return outcome
    active=[(i,line.strip()) for i,line in enumerate(stderr.splitlines(),1) if line.strip()]
    # V6 may not classify a bare "timeout" token as a failure. V7 must not
    # silently pass such an unproven timeout. This extra stop is prospective
    # only; the accepted V6 function and its result remain unchanged.
    unknown=[(i,line) for i,line in active if UNKNOWN_TIMEOUT_PATTERN.search(line)
             and not positive_auxiliary_source(line)]
    if unknown:
        # A previously unrecognized stderr timeout is an independent V7 stop.
        # Preserve every original V6 signal/stop, add only newly identified
        # evidence, and update the *entire* effective result contract.
        baseline_stops=list(baseline['conflict_evidence'])
        known={(s.get('source_field'),s.get('evidence')) for s in baseline_stops}
        new_stops=[{'source_field':f'raw_stderr[{i}]',
                    'failure_class':'UNCLASSIFIED_NONEXTERNAL_FAILURE',
                    'evidence':line[:300]} for i,line in unknown
                    if (f'raw_stderr[{i}]',line[:300]) not in known]
        combined=[*baseline_stops,*new_stops]
        normalized=[*baseline['normalized_failure_evidence'],
                    *({'source_field':s['source_field'],
                       'classification':s['failure_class'],
                       'kind':'HARD_STOP'} for s in new_stops)]
        _project_current_conflicts(outcome,combined,normalized)
        outcome['decision']='CONTROLLED_STOP'
        outcome['final_decision']='CONTROLLED_STOP'
        outcome['classification']='CONFLICTING_OR_UNKNOWN_FAILURE'
        outcome['operational_classification']='UNKNOWN_TIMEOUT_FAIL_CLOSED'
        return outcome
    if len(active)!=1:return outcome
    i,line=active[0]
    if not positive_auxiliary_source(line):return outcome
    outcome['positive_auxiliary_source_identified']=True
    # V6 must contain EXACTLY one hard stop attributable to this same stderr
    # line, and must have completed all registered control inspections.
    stops=baseline.get('conflict_evidence')
    if (baseline['decision']!='CONTROLLED_STOP' or
        baseline.get('external_signal_detected') or
        baseline.get('fields_present_minus_fields_inspected') or
        baseline.get('malformed_control_fields') or
        type(stops) is not list or len(stops)!=1):return outcome
    s=stops[0]
    if (s.get('source_field')!=f'raw_stderr[{i}]' or
        s.get('failure_class')!='UNCLASSIFIED_NONEXTERNAL_FAILURE' or
        s.get('evidence')!=line[:300]):return outcome
    # Source matches alone NEVER justify dropping the hard stop.
    if not _integrity_complete(integrity,result):return outcome
    outcome['decision']='NO_EXTERNAL_SIGNAL'
    outcome['final_decision']='NO_EXTERNAL_SIGNAL'
    outcome['classification']='NONBLOCKING_AUXILIARY_EXECUTOR_DIAGNOSTIC'
    outcome['operational_classification']='NORMAL_SUCCESS_WITH_AUXILIARY_DIAGNOSTIC'
    outcome['auxiliary_diagnostic_nonblocking']=True
    outcome['auxiliary_diagnostic_evidence']={'source_field':f'raw_stderr[{i}]',
        'identifier':'CODEX_MODELS_MANAGER_REFRESH_TIMEOUT',
        'positively_identified':True,
        'independent_operational_checks':'ALL_REQUIRED_PASS'}
    # The hard stop has been resolved only for V7's narrowly proven auxiliary
    # event; project a consistent effective result without losing any original
    # V6 facts, held in historical_v6_verdict.
    _project_current_conflicts(outcome,[],[{
        'source_field':f'raw_stderr[{i}]',
        'classification':'NONBLOCKING_AUXILIARY_EXECUTOR_DIAGNOSTIC',
        'kind':'AUXILIARY_DIAGNOSTIC'}])
    return outcome
