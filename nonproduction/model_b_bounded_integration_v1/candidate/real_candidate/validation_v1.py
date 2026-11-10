"""Source-pinned adapter to unchanged accepted v3/V6 scientific validator.

Nonproduction tests use frozen synthetic S04 fixtures. Real inputs must later
be provided only by a separately trusted source verifier under REAL activation.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from pathlib import Path
import importlib.util,json
from trusted_stage.staging_v1 import require,sha,canonical,safe_read
from real_candidate.capture_v1 import ControlledLocalCapture,LocalObservation

def _validated_output_hash(value):
    """Type-strict, field-complete, order-sensitive canonical JSON digest.

    Refuse non-JSON objects, mixed/non-string map keys, NaN/infinities and
    unsupported types instead of losing type information during serialization.
    """
    def walk(v):
        t=type(v)
        if t is dict:
            require(all(type(k) is str for k in v),'VALIDATED_OUTPUT_NON_STRING_KEY')
            for child in v.values(): walk(child)
        elif t is list:
            for child in v: walk(child)
        elif t is float:
            require(math.isfinite(v),'VALIDATED_OUTPUT_NONFINITE_FLOAT')
        else:
            require(t in (str,int,bool,type(None)),'VALIDATED_OUTPUT_UNSUPPORTED_TYPE')
    walk(value)
    return sha(canonical(value))

VALIDATOR_SHA='d8946ad938d409328818012d19fc42095898abad4d47b777879fda923b28ff42'

@dataclass(frozen=True, slots=True)
class ValidatedObservedUnit:
    capture: LocalObservation
    payload: dict
    actual_input_bytes: bytes
    actual_input_sha256: str
    validator_sha256: str
    validated_output_sha256: str
    _seal: object

class BoundAcceptedValidator:
    def __init__(self, *, accepted_root: Path, supervisor: ControlledLocalCapture,
                 partition_path:Path, evidence_path:Path, reason_path:Path,
                 partition_sha256:str,evidence_sha256:str,reason_sha256:str):
        self.supervisor=supervisor
        file=Path(accepted_root)/'accepted_recovery/reference/v6_accepted/partition_contract_nonproduction_v1.py'
        require(sha(safe_read(file))==VALIDATOR_SHA,'ACCEPTED_VALIDATOR_IDENTITY_CHANGED')
        spec=importlib.util.spec_from_file_location('accepted_validator_real_adapter_test',file)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.module=mod
        self._sources=((Path(partition_path),partition_sha256),
                       (Path(evidence_path),evidence_sha256),(Path(reason_path),reason_sha256))
        self._seal=object();self._receipts={}
        self._read_sources()

    def _read_sources(self):
        raws=[]
        for path,pin in self._sources:
            raw=safe_read(path)
            require(sha(raw)==pin,'ACCEPTED_S04_SOURCE_IDENTITY_DRIFT')
            raws.append(raw)
        partition=json.loads(raws[0]); evidence=json.loads(raws[1]); reason=json.loads(raws[2])
        require(self.module.verify_manifest(partition,evidence),'INVALID_S04_PARTITION')
        return partition,evidence,reason

    def _agent_message(self,capture):
        # REAL Codex JSONL event stream is not equivalent to local process
        # success. Only a completed turn with a single final agent message
        # is accepted. Nonproduction uses direct agent JSON for tests.
        text=capture.stdout.decode('utf8',errors='strict')
        if capture.mode=='NONPRODUCTION_TEST':
            d=json.loads(text)
            require(type(d) is dict and type(d.get('rows')) is list,'NONPRODUCTION_AGENT_MESSAGE_INVALID')
            return text
        events=[json.loads(line) for line in text.splitlines() if line.strip()]
        require(events and all(type(e) is dict for e in events), 'CODEX_JSONL_INVALID')
        finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and
                type(e.get('item')) is dict and e['item'].get('type')=='agent_message' and
                type(e['item'].get('text')) is str]
        require(len(finals)==1 and sum(e.get('type')=='turn.completed' for e in events)==1,
                'CODEX_FINAL_OUTPUT_INCOMPLETE_OR_AMBIGUOUS')
        return finals[0]

    def validate(self, capture, *, input_path:Path, input_sha256:str):
        self.supervisor.verify(capture,input_file=input_path,pinned_input_sha256=input_sha256)
        partition,evidence,reason=self._read_sources()
        unit=self.module.unit_evidence(partition,evidence,'U0012')
        actual_input_bytes=canonical(unit)
        require(type(capture.actual_input_sha256) is str and
                capture.actual_input_sha256==input_sha256 and
                sha(safe_read(input_path))==input_sha256,'ACTUAL_EXECUTED_INPUT_IDENTITY_CHANGED')
        # Future trusted runner must bind precisely canonical(unit) to input
        # before invoking Codex; nonproduction probe input may differ.
        if capture.mode=='REAL':
            require(capture.actual_input_sha256==sha(actual_input_bytes),'UNIT_S04_INPUT_NOT_EXECUTED')
        result={'process_started':True,'return_code':capture.exit_code,
                'termination_state':capture.termination,'timeout_status':capture.timeout,
                'context_id':capture.invocation_id,'agent_message':self._agent_message(capture)}
        checked=self.module.validate_semantic_unit(partition,evidence,reason,'U0012',result,'PRIMARY')
        require(len(checked['validated_rows'])==25 and len(checked['raw_rows'])==25,
                'ACCEPTED_REAL_VALIDATOR_INCOMPLETE')
        checked['row_count']=25
        receipt=ValidatedObservedUnit(capture,checked,actual_input_bytes,sha(actual_input_bytes),VALIDATOR_SHA,
                                      _validated_output_hash(checked),self._seal)
        self._receipts[capture.invocation_id]=(receipt,receipt.validated_output_sha256)
        return receipt

    def verify_receipt(self, receipt, capture):
        require(type(receipt) is ValidatedObservedUnit and receipt.capture is capture and
                receipt._seal is self._seal and self._receipts.get(capture.invocation_id) is not None and
                self._receipts[capture.invocation_id][0] is receipt and
                self._receipts[capture.invocation_id][1]==receipt.validated_output_sha256 and
                receipt.validator_sha256==VALIDATOR_SHA,'FORGED_VALIDATOR_RECEIPT')
        partition,evidence,reason=self._read_sources()
        require(receipt.actual_input_bytes==canonical(self.module.unit_evidence(partition,evidence,'U0012')) and
                sha(receipt.actual_input_bytes)==receipt.actual_input_sha256 and
                len(receipt.payload['validated_rows'])==25 and
                _validated_output_hash(receipt.payload)==receipt.validated_output_sha256,
                'VALIDATOR_INPUT_OR_OUTPUT_DRIFT')
        return True
