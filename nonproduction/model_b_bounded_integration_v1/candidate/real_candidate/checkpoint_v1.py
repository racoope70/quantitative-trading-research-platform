"""Read-only attestation of an existing S05 checkpoint. No mutation or resume.

Source identity is externally pinned. This is a chain/byte/position attestor,
not a substitute for the accepted engine's scientific semantic readback.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
from trusted_stage.staging_v1 import require, safe_read, sha, canonical

ATTEMPT='BATCH0004_S05_PRIMARY_REAL_SIZE25_V1_A361F621CBA64AC4AAC19AACFAEF778F'
STOP='CONTROLLED_STOP__RETURN_TO_MANAGING'
PHASE_RECOVERY_SOURCE_SHA256 = '60ce8dd5af3d40d93a2f8c357f5b6074af0b4ee1eeb59e06752caac6ed585ce6'

def source_digest(obj):return sha(canonical(obj)[:-1])

@dataclass(frozen=True,slots=True)
class CheckpointAttestation:
    identity: str
    sequence: int
    frozen_units: int
    frozen_rows: int
    first_unfinished: str
    u0012_attempts: int
    u0013_attempts: int
    _seal: object
    _phase: bytes | None = None

class PersistedCheckpointAttestor:
    def __init__(self, root:Path, *, pinned_checkpoint_sha256:str, expected_history=None, read_bytes=None, snapshot_paths=None, path_exists=None):
        self.root=Path(root)
        require(type(pinned_checkpoint_sha256) is str and len(pinned_checkpoint_sha256)==64, 'NO_TRUSTED_CHECKPOINT_ANCHOR')
        self.expected=pinned_checkpoint_sha256
        self._seal=object()
        self._last=None
        self._recovery_phase=None
        self.expected_history=expected_history
        self._read_bytes=read_bytes or safe_read
        self._snapshot_paths=snapshot_paths
        self._path_exists=path_exists or (lambda path: Path(path).exists())
        if read_bytes is not None or snapshot_paths is not None or path_exists is not None:
            require(callable(read_bytes) and snapshot_paths is not None and callable(path_exists),
                    'INCOMPLETE_CONFINED_READ_INTERFACE')
        if expected_history is not None:
            require(type(expected_history) is list and len(expected_history)==10 and
                    [a.get('attempt_number') for a in expected_history]==list(range(1,11)),
                    'EXACT_CURRENT_HISTORY_DRIFT')

    def verify(self) -> CheckpointAttestation:
        root=self.root
        if self._snapshot_paths is None:
            require(root.is_dir() and not root.is_symlink(), 'CHECKPOINT_ROOT_UNSAFE')
        workspace=root/'PRIMARY'
        folder=workspace/'checkpoints'
        if self._snapshot_paths is None:
            require(folder.is_dir() and not folder.is_symlink(), 'CHECKPOINT_FOLDER_UNSAFE')
        head=json.loads(self._read_bytes(workspace/'checkpoint_head.json'))
        require(set(head)=={'sequence','snapshot_file','snapshot_file_sha256','checkpoint_manifest_sha256'},'CHECKPOINT_HEAD_INVALID')
        count=head['sequence']
        require(type(count) is int and (count==54 if self.expected_history is not None else 1<=count<=10000),'CHECKPOINT_SEQUENCE_INVALID')
        paths=sorted(self._snapshot_paths if self._snapshot_paths is not None else folder.glob('checkpoint_*.json'))
        require(len(paths)==count,'CHECKPOINT_GAP_OR_EXTRANEOUS_SNAPSHOT')
        previous=None
        for idx,path in enumerate(paths,1):
            require(path.name==f'checkpoint_{idx:06d}.json','CHECKPOINT_SEQUENCE_GAP')
            raw=self._read_bytes(path)
            item=json.loads(raw)
            require(raw==canonical(item),'CHECKPOINT_NONCANONICAL_BYTES')
            require(item['checkpoint_sequence']==idx and
                    item['previous_checkpoint_sha256']==previous,'CHECKPOINT_LINKAGE_MISMATCH')
            require(item['checkpoint_manifest_sha256']==source_digest({k:v for k,v in item.items()
                    if k!='checkpoint_manifest_sha256'}),'CHECKPOINT_SELF_HASH_MISMATCH')
            require(item['role']=='PRIMARY' and item['attempt_identity']==ATTEMPT,'CHECKPOINT_ATTEMPT_DRIFT')
            previous=item['checkpoint_manifest_sha256']
        require(head['snapshot_file']==paths[-1].name and
                head['snapshot_file_sha256']==sha(self._read_bytes(paths[-1])) and
                head['checkpoint_manifest_sha256']==previous==self.expected,
                'CHECKPOINT_HEAD_OR_EXTERNAL_ANCHOR_MISMATCH')
        latest=item
        require(latest['global_state']==STOP and latest['first_unfinished_unit']=='U0012',
                'CHECKPOINT_NOT_CONTROLLED_STOP')
        units=latest['units']
        require(len(units)==20 and [u['unit_id'] for u in units]==[f'U{i:04d}' for i in range(1,21)],
                'UNIT_ORDER_OR_COUNT_DRIFT')
        frozen=[u for u in units if u['state']=='FROZEN']
        require(len(frozen)==11 and frozen==units[:11], 'FROZEN_PREFIX_DRIFT')
        validated_count=0
        for u in frozen:
            raw=self._read_bytes(workspace/'frozen_units'/u['unit_id']/'unit_result.json')
            data=json.loads(raw)
            rows=data.get('validated_rows')
            require(sha(raw)==u['frozen_output_sha256'] and
                    data.get('unit_id')==u['unit_id'] and data.get('role')=='PRIMARY' and
                    data.get('context_id')==u['frozen_context_id'] and
                    type(rows) is list and len(rows)==25,
                    'FROZEN_OUTPUT_BINDING_DRIFT')
            require(source_digest(rows)==data['unit_output_sha256'] and
                    source_digest(data['raw_rows'])==data['raw_rows_sha256'],
                    'FROZEN_ROW_DIGEST_DRIFT')
            require([r['authorized_population_position'] for r in rows]==list(range(u['position_start'],u['position_end']+1)),
                    'FROZEN_POSITION_DRIFT')
            validated_count+=len(rows)
        require(validated_count==275, 'FROZEN_ROW_COUNT_DRIFT')
        u12,u13=units[11],units[12]
        require(u12['state']=='PENDING' and u12['attempt_count']==(10 if self.expected_history is not None else 9) and len(u12['attempts'])==(10 if self.expected_history is not None else 9) and
                u13['state']=='PENDING' and u13['attempt_count']==0 and not u13['attempts'] and
                not self._path_exists(workspace/'frozen_units'/'U0012') and
                not self._path_exists(workspace/'frozen_units'/'U0013'),
                'U0012_OR_U0013_ATTEMPT_DRIFT')
        # Fail-closed: check no additional snapshot was written during reading.
        require(self._read_bytes(workspace/'checkpoint_head.json')==canonical(head),
                'CHECKPOINT_HEAD_CHANGED_DURING_ATTESTATION')
        if self.expected_history is not None:
            require(canonical(u12['attempts'])==canonical(self.expected_history),'EXACT_CURRENT_HISTORY_DRIFT')
        rec=CheckpointAttestation(previous,count,11,validated_count,'U0012',u12['attempt_count'],0,self._seal)
        if self._last is None:
            self._last=rec
        return rec

    def arm_recovery_successor(self, transaction, *, checkpoint,
                               pinned_owner_authorization_sha256,
                               pinned_owner_consumption_sha256):
        """Bind one successor to an already verified/consumed transaction.

        Must be called at the exact PENDING predecessor, after independent
        Owner publication verification and durable consumption. This attestor
        grants no execution authority. Receipt identity remains the authorized
        predecessor: the operational proof separately records the verified successor.
        """
        import recovery_two_attempt_v3 as recovery
        require(sha(safe_read(Path(recovery.__file__)))==PHASE_RECOVERY_SOURCE_SHA256,
                'PHASE_RECOVERY_SOURCE_DRIFT')
        require(type(transaction) is recovery.ControlledStopRecovery,
                'UNTRUSTED_PHASE_RECOVERY_INTERFACE')
        require(self._recovery_phase is None, 'RECOVERY_PHASE_ALREADY_BOUND')
        self.verify_receipt(checkpoint)  # original PENDING verification unchanged
        require(transaction.engine.root==self.root and
                transaction.case['checkpoint_manifest_sha256']==self.expected,
                'PHASE_PREDECESSOR_OR_ROOT_MISMATCH')
        binding=transaction.proof_checkpoint_binding(
            owner_authorization_sha256=pinned_owner_authorization_sha256,
            owner_consumption_sha256=pinned_owner_consumption_sha256,executing=False)
        workspace=self.root/'PRIMARY'
        paths=sorted((workspace/'checkpoints').glob('checkpoint_*.json'))
        prefix=tuple((p.name,sha(safe_read(p))) for p in paths)
        predecessor=safe_read(paths[-1])
        require(json.loads(predecessor)['checkpoint_manifest_sha256']==checkpoint.identity and
                len(paths)==checkpoint.sequence, 'PHASE_PREDECESSOR_CHANGED')
        # Catch an intervening mutation during binding as well as on issuance.
        self.verify_receipt(checkpoint)
        require(transaction.proof_checkpoint_binding(
            owner_authorization_sha256=pinned_owner_authorization_sha256,
            owner_consumption_sha256=pinned_owner_consumption_sha256,executing=False)==binding,
            'PHASE_TRANSACTION_CHANGED_DURING_BINDING')
        phase=canonical({'binding_sha256':sha(binding),'predecessor_bytes_sha256':sha(predecessor),
                         'predecessor_identity':checkpoint.identity,'sequence':checkpoint.sequence})
        count=len(transaction._historical_attempts)
        require(count in (9,10) and checkpoint.u0012_attempts==count,
                'PHASE_HISTORY_COUNT_DRIFT')
        if count==10:
            require(checkpoint.sequence==54,'PHASE_PREDECESSOR_CHANGED')
            recovery.prospective_attempt_context(transaction.case,
                synthetic=not (type(transaction.engine) is recovery.BoundCheckpointEngine and transaction.engine.real_source))
        self._recovery_phase=(transaction,binding,predecessor,prefix,
                              pinned_owner_authorization_sha256,pinned_owner_consumption_sha256)
        receipt=CheckpointAttestation(checkpoint.identity,checkpoint.sequence,11,275,'U0012',count,0,self._seal,phase)
        self._last=receipt  # old PENDING receipts cannot be reused in this phase
        return receipt

    def _verify_recovery_successor(self,receipt):
        import recovery_two_attempt_v3 as recovery
        require(sha(safe_read(Path(recovery.__file__)))==PHASE_RECOVERY_SOURCE_SHA256,
                'PHASE_RECOVERY_SOURCE_DRIFT')
        require(self._recovery_phase is not None,'NO_AUTHORIZED_RECOVERY_PHASE')
        transaction,binding,predecessor_raw,prefix,owner_pin,consumption_pin=self._recovery_phase
        require(type(transaction) is recovery.ControlledStopRecovery,
                'UNTRUSTED_PHASE_RECOVERY_INTERFACE')
        workspace=self.root/'PRIMARY'
        require(receipt.u0012_attempts==len(transaction._historical_attempts),
                'PHASE_HISTORY_COUNT_DRIFT')
        folder=workspace/'checkpoints'
        require(self.root.is_dir() and not self.root.is_symlink() and
                workspace.is_dir() and not workspace.is_symlink() and
                folder.is_dir() and not folder.is_symlink(), 'PHASE_CHECKPOINT_PATH_UNSAFE')
        require(transaction.engine.root==self.root and
                transaction.case['checkpoint_manifest_sha256']==self.expected==receipt.identity,
                'PHASE_PREDECESSOR_OR_ROOT_MISMATCH')
        expected_phase=canonical({'binding_sha256':sha(binding),'predecessor_bytes_sha256':sha(predecessor_raw),
                                  'predecessor_identity':receipt.identity,'sequence':receipt.sequence})
        require(receipt._phase==expected_phase,'PHASE_RECEIPT_BINDING_DRIFT')
        # These guards re-read the full accepted engine state, journal and
        # immutable mode contract. No caller-provided successor hash is used.
        current_binding=transaction.proof_checkpoint_binding(
            owner_authorization_sha256=owner_pin,owner_consumption_sha256=consumption_pin,executing=True)
        require(current_binding==binding,'PHASE_TRANSACTION_BINDING_DRIFT')
        head_raw=safe_read(workspace/'checkpoint_head.json')
        head=json.loads(head_raw)
        require(head_raw==canonical(head) and set(head)=={
            'sequence','snapshot_file','snapshot_file_sha256','checkpoint_manifest_sha256'},
            'PHASE_HEAD_INVALID')
        require(type(head['sequence']) is int and head['sequence']==receipt.sequence+1,
                'PHASE_NOT_IMMEDIATE_SUCCESSOR')
        paths=sorted(folder.glob('checkpoint_*.json'))
        require(len(paths)==receipt.sequence+1 and
                tuple((p.name,sha(safe_read(p))) for p in paths[:-1])==prefix,
                'PHASE_PREDECESSOR_CHAIN_CHANGED')
        previous=None
        for index,path in enumerate(paths,1):
            raw=safe_read(path);item=json.loads(raw)
            require(path.name==f'checkpoint_{index:06d}.json' and raw==canonical(item),
                    'PHASE_SEQUENCE_OR_SERIALIZATION_DRIFT')
            require(item['checkpoint_sequence']==index and
                    item['previous_checkpoint_sha256']==previous and
                    item['checkpoint_manifest_sha256']==source_digest({k:v for k,v in item.items()
                        if k!='checkpoint_manifest_sha256'}), 'PHASE_CHAIN_OR_SELF_HASH_DRIFT')
            require(item['role']=='PRIMARY' and item['attempt_identity']==ATTEMPT,
                    'PHASE_ATTEMPT_DRIFT')
            previous=item['checkpoint_manifest_sha256']
        predecessor=json.loads(predecessor_raw)
        require(safe_read(paths[-2])==predecessor_raw and
                predecessor['checkpoint_manifest_sha256']==receipt.identity and
                predecessor['checkpoint_sequence']==receipt.sequence,
                'PHASE_AUTHORIZED_PREDECESSOR_CHANGED')
        successor=item
        require(head['snapshot_file']==paths[-1].name and head['snapshot_file_sha256']==sha(raw) and
                head['checkpoint_manifest_sha256']==previous==transaction._executing_checkpoint_sha256,
                'PHASE_SUCCESSOR_HEAD_DRIFT')
        # The accepted _snapshot mechanism changes only these four metadata
        # fields and the authorized U0012 state. Full object equality protects
        # all scientific identities, historical attempts, frozen units/suffix.
        expected=json.loads(predecessor_raw)
        expected['units'][11]['state']='EXECUTING'
        expected['checkpoint_sequence']+=1
        expected['previous_checkpoint_sha256']=receipt.identity
        timestamp=successor['checkpoint_timestamp']
        require(type(timestamp) is str and
                datetime.fromisoformat(timestamp).tzinfo is not None and
                datetime.fromisoformat(timestamp)>=datetime.fromisoformat(predecessor['checkpoint_timestamp']),
                'PHASE_TIMESTAMP_INVALID')
        expected['checkpoint_timestamp']=timestamp
        expected['checkpoint_manifest_sha256']=source_digest({k:v for k,v in expected.items()
            if k!='checkpoint_manifest_sha256'})
        require(canonical(successor)==canonical(expected),'PHASE_UNAUTHORIZED_CHECKPOINT_CHANGE')
        require(transaction.proof_checkpoint_binding(
            owner_authorization_sha256=owner_pin,owner_consumption_sha256=consumption_pin,executing=True)==binding
            and safe_read(workspace/'checkpoint_head.json')==head_raw,
            'PHASE_CHANGED_DURING_ATTESTATION')
        return True

    def verify_receipt(self,receipt):
        require(type(receipt) is CheckpointAttestation and receipt._seal is self._seal and
                receipt is self._last,'CALLER_FORGED_CHECKPOINT_ATTESTATION')
        if receipt._phase is not None:
            return self._verify_recovery_successor(receipt)
        current=self.verify()
        require(current.identity==receipt.identity and current.sequence==receipt.sequence and
                current.frozen_units==receipt.frozen_units and current.frozen_rows==receipt.frozen_rows and
                current.first_unfinished==receipt.first_unfinished and current.u0012_attempts==receipt.u0012_attempts and
                current.u0013_attempts==receipt.u0013_attempts,
                'CHECKPOINT_CHANGED_SINCE_ATTESTATION')
        return True
