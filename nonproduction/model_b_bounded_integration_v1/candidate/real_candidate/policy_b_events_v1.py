"""Strict complete-capture Policy B equivalence derivation; no authority API."""
import hashlib
import json
import re
from dataclasses import dataclass

MAX_BYTES = 16 * 1024 * 1024
MAX_EVENTS = 4096
MAX_MESSAGES = 1024
LABEL = 'POLICY_B_EXACT_COMPLETE_MESSAGE_VALUE_V1'


class Rejected(RuntimeError):
    pass


def need(ok, reason):
    if not ok:
        raise Rejected(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=False, allow_nan=False) + '\n').encode('utf8')


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def constant(_):
        raise Rejected('NONFINITE_JSON_NUMBER')
    try:
        result = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
        # Also reject nonfinite exponents and unpaired surrogate strings.
        canonical(result)
        return result
    except (ValueError, UnicodeError, RecursionError, OverflowError) as exc:
        raise Rejected('STRICT_JSON_INVALID') from exc


@dataclass(frozen=True)
class Analysis:
    common_result: bytes
    witness: dict


def _command_execution(item, expected_status):
    """Recognize one exact non-result CLI command lifecycle envelope.

    Command/output text never becomes a qualifying scientific message. The
    original complete-capture hash continues to bind those bytes in the proof.
    """
    need(type(item) is dict and set(item) ==
         {'id','type','command','aggregated_output','exit_code','status'},
         'COMMAND_EXECUTION_SCHEMA')
    need(item['type'] == 'command_execution' and
         type(item['command']) is str and bool(item['command']) and
         type(item['aggregated_output']) is str,
         'COMMAND_EXECUTION_FIELD_TYPES')
    need(type(item['id']) is str and
         re.fullmatch(r'item_(0|[1-9][0-9]{0,9})',item['id']) is not None,
         'CLI_LOCAL_ITEM_ID_REQUIRED')
    need(item['status'] == expected_status,'COMMAND_EXECUTION_STATUS')
    if expected_status == 'in_progress':
        need(item['exit_code'] is None,'COMMAND_START_EXIT_CODE')
    else:
        need(type(item['exit_code']) is int and item['exit_code'] == 0,
             'COMMAND_EXECUTION_FAILED')
    return int(item['id'][5:])


def inspect_envelope(raw, *, expected_context, frozen_extract):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'CAPTURE_BOUND')
    need(expected_context.get('mode') in ('REAL','SYNTHETIC_NONPRODUCTION') and
         expected_context.get('batch') == 'BATCH0004' and
         expected_context.get('role') == 'PRIMARY' and
         expected_context.get('unit') == 'U0012' and
         type(expected_context.get('attempt')) is str and bool(expected_context['attempt']) and
         type(expected_context.get('checkpoint')) is str and
         re.fullmatch('[0-9a-f]{64}', expected_context['checkpoint']) is not None and
         type(expected_context.get('max_new_units')) is int and
         expected_context['max_new_units'] == 1 and
         expected_context.get('u0013_prohibited') is True, 'POLICY_B_SCOPE_REQUIRED')
    for key in ('input_sha256', 'runtime_sha256', 'configuration_sha256'):
        need(type(expected_context.get(key)) is str and
             re.fullmatch('[0-9a-f]{64}', expected_context[key]) is not None,
             'POLICY_B_IDENTITY_REQUIRED')
    try:
        text = raw.decode('utf8', errors='strict')
    except UnicodeError as exc:
        raise Rejected('CAPTURE_UTF8_INVALID') from exc
    # The prototype deliberately supports a conservative subset of CLI events.
    # Unknown item kinds/lifecycles are rejected, never silently discarded.
    lines = text.split('\n')
    if lines[-1] == '':
        lines.pop()
    need(1 <= len(lines) <= MAX_EVENTS, 'EVENT_BOUND')
    need(all(line.strip() for line in lines), 'EMPTY_EVENT_LINE')
    occurrences = []
    thread = None
    started = False
    terminal = False
    last_local_id = -1
    common = None
    pending_commands = {}
    for ordinal, line in enumerate(lines, 1):
        event = strict_json(line)
        need(type(event) is dict and type(event.get('type')) is str, 'EVENT_SCHEMA')
        need(not terminal, 'EVENT_AFTER_TERMINAL')
        kind = event['type']
        if kind == 'thread.started':
            need(ordinal == 1 and set(event) == {'type', 'thread_id'} and
                 type(event['thread_id']) is str and event['thread_id'] and
                 len(event['thread_id']) <= 200, 'THREAD_IDENTITY')
            thread = event['thread_id']
        elif kind == 'turn.started':
            need(thread is not None and not started and ordinal == 2 and
                 set(event) == {'type'}, 'TURN_START')
            started = True
        elif kind == 'item.started':
            need(started and set(event) == {'type','item'},'ITEM_SCHEMA')
            item=event['item']
            number=_command_execution(item,'in_progress')
            need(number > last_local_id,'CLI_LOCAL_ITEM_ID_DUPLICATE_OR_ORDER')
            last_local_id=number
            pending_commands[item['id']]=item['command']
        elif kind == 'item.completed':
            need(started and set(event) == {'type', 'item'} and
                 type(event['item']) is dict, 'ITEM_SCHEMA')
            item = event['item']
            if item.get('type') == 'command_execution':
                _command_execution(item,'completed')
                need(item['id'] in pending_commands,'COMMAND_COMPLETION_WITHOUT_START')
                need(item['command'] == pending_commands[item['id']],
                     'COMMAND_LIFECYCLE_IDENTITY_DRIFT')
                del pending_commands[item['id']]
                continue
            need(set(item) == {'id', 'type', 'text'} and
                 item['type'] == 'agent_message' and type(item['text']) is str,
                 'SUPPORTED_AGENT_MESSAGE_REQUIRED')
            need(type(item['id']) is str and
                 re.fullmatch(r'item_(0|[1-9][0-9]{0,9})', item['id']) is not None,
                 'CLI_LOCAL_ITEM_ID_REQUIRED')
            number = int(item['id'][5:])
            need(number > last_local_id, 'CLI_LOCAL_ITEM_ID_DUPLICATE_OR_ORDER')
            last_local_id = number
            body = item['text'].encode('utf8', errors='strict')
            need(body, 'EMPTY_MESSAGE')
            if common is None:
                common = body
            else:
                need(body == common, 'QUALIFYING_MESSAGE_BYTES_DIFFER')
            occurrences.append({'occurrence': len(occurrences) + 1,
                                'event_ordinal': ordinal, 'item_id': item['id'],
                                'text_sha256': sha(body), 'text_length': len(body)})
            need(len(occurrences) <= MAX_MESSAGES, 'MESSAGE_BOUND')
        elif kind == 'turn.completed':
            need(started and set(event) == {'type', 'usage'} and
                 type(event['usage']) is dict and set(event['usage']) ==
                 {'input_tokens', 'cached_input_tokens', 'output_tokens'} and
                 all(type(v) is int and v >= 0 for v in event['usage'].values()),
                 'SUCCESS_TERMINAL_SCHEMA')
            need(not pending_commands,'UNFINISHED_COMMAND_EXECUTION')
            terminal = True
        else:
            raise Rejected('UNSUPPORTED_OR_FAILED_EVENT__' + kind)
    need(terminal and occurrences, 'MISSING_SUCCESS_OR_RESULT')
    result = strict_json(common)
    need(type(result) is dict and type(result.get('rows')) is list and
         len(result['rows']) == 25 and all(type(row) is dict for row in result['rows']),
         'COMPLETE_25_ROW_RESULT_REQUIRED')
    selected = frozen_extract(text)
    need(type(selected) is dict and set(selected) == {'context_id', 'agent_message'},
         'FROZEN_EXTRACTION_SCHEMA')
    selected_thread, selected_text = selected['context_id'], selected['agent_message']
    need(selected_thread == thread and selected_text.encode('utf8') == common,
         'FROZEN_EXTRACTION_DISAGREEMENT')
    witness = {'label': LABEL, 'capture_sha256': sha(raw), 'capture_length': len(raw),
               'capture_invocation_identity': dict(expected_context),
               'thread_id_scope': 'CLI_REPORTED_THREAD_ONLY__NOT_PROVIDER_IDENTITY',
               'cli_thread_id': thread, 'message_count': len(occurrences),
               'completed_turn_count': 1, 'captured_event_count': len(lines),
               'all_qualifying_occurrences': occurrences,
               'ordered_message_text_hashes': [x['text_sha256'] for x in occurrences],
               'common_result_sha256': sha(common), 'common_result_length': len(common),
               'frozen_selected_occurrence': len(occurrences),
               'frozen_selected_text_sha256': sha(selected_text.encode('utf8')),
               'provider_message_identity': 'NOT_AVAILABLE',
               'transport_delivery_identity': 'NOT_AVAILABLE',
               'message_phase': 'NOT_AVAILABLE',
               'accepted_trusted_proof': 'NOT_ESTABLISHED'}
    return Analysis(common, witness)


def verify_consistency(raw, witness, *, expected_capture_sha256,
                       expected_context, frozen_extract):
    """Rebuild from fixed external test inputs, never from submitted claims.

    This tests omitted/tampered witness rejection only. The independent test
    inputs are synthetic; they are not trusted OS provenance or REAL authority.
    """
    need(sha(raw) == expected_capture_sha256, 'EXTERNAL_CAPTURE_HASH_MISMATCH')
    rebuilt = inspect_envelope(raw, expected_context=expected_context,
                               frozen_extract=frozen_extract)
    need(canonical(rebuilt.witness) == canonical(witness), 'WITNESS_BINDING_MISMATCH')
    return True
