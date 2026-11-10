"""REAL-mode compatible staging contract with accepted positions/identity rules.

Stages through unchanged accepted staging_v1.stage_validated_payload.
Never invokes promotion, scientific execution or checkpoint mutation.
"""
from dataclasses import dataclass
import re
from trusted_stage.staging_v1 import UnitBinding,require,same_name

@dataclass(frozen=True, slots=True)
class FutureRealUnitBinding(UnitBinding):
    def verify(self):
        for value in (self.batch_id,self.role,self.unit_id,self.attempt_id,self.checkpoint_identity):same_name(value)
        require(self.batch_id=='BATCH0004' and self.role=='PRIMARY' and self.unit_id=='U0012',
                'REAL_UNIT_OR_ROLE_INVALID')
        require(self.execution_mode=='REAL' and self.max_new_units==1 and type(self.max_new_units) is int,
                'REAL_UNIT_MODE_OR_MAX_UNITS')
        for x in (self.checkpoint_identity,self.unit_input_sha256,self.mode_binding_sha256):
            require(type(x) is str and re.fullmatch('[0-9a-f]{64}',x),'REAL_IDENTITY_INVALID')
        require(self.expected_positions==tuple(range(1776,1801)) and
                type(self.expected_positions) is tuple,'REAL_UNIT_POSITIONS_DRIFT')
        require(type(self.expected_identities) is tuple and len(self.expected_identities)==25 and
                len(set(self.expected_identities))==25 and all(type(x) is str and x for x in self.expected_identities),
                'REAL_IDENTITY_LIST_INVALID')
        return self
