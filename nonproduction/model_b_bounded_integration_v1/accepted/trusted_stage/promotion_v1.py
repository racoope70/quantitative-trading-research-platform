"""Promote VERIFIED raw staged bytes, never reserialize, via exclusive atomic link.

The staging and final files have separate inodes; publishing final is atomic.
No scientific checkpoint mutations are performed by this module.
"""
from __future__ import annotations
import os
from pathlib import Path
import uuid
from .staging_v1 import (StageStop, require, safe_folder, safe_read,
                         verify_stage, sha, StagedArtifact, same_name)


def promote_exact_bytes(root: Path, stage: StagedArtifact, *, proof_verified: bool,
                        v7_decision: str, expected_sha256: str):
    require(proof_verified is True,'UNVERIFIED_PROOF')
    require(v7_decision=='NO_EXTERNAL_SIGNAL','V7_NOT_NONBLOCKING')
    raw=verify_stage(stage)
    require(stage.staged_bytes_sha256==expected_sha256,'STAGED_REFERENCE_MISMATCH')
    folder=safe_folder(safe_folder(root)/'frozen_units')
    target=folder/(same_name(stage.binding.unit_id)+'.json')
    require(not target.exists() and not target.is_symlink(),'FINAL_FROZEN_ARTIFACT_EXISTS')
    # New inode, append-only atomic publication. Copy bytes without regenerating JSON.
    temp=folder/('.pending_'+uuid.uuid4().hex)
    committed=False
    try:
        fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o400)
        try:
            with os.fdopen(fd,'wb',closefd=False) as f:
                f.write(raw);f.flush();os.fsync(f.fileno())
        finally: os.close(fd)
        require(safe_read(temp)==raw,'TEMP_PROMOTION_MISMATCH')
        require(verify_stage(stage)==raw,'STAGED_BYTES_CHANGED_DURING_PROMOTION')
        os.link(temp,target,follow_symlinks=False)
        committed=True
        # temp and target are same inode momentarily. Drop temp before verifying
        # because safe_read requires nlink == 1.
        temp.unlink()
        final=safe_read(target)
        require(final==raw and len(final)==stage.file_size and sha(final)==stage.staged_bytes_sha256,
                'FINAL_PROMOTION_BYTE_MISMATCH')
        require(verify_stage(stage)==final, 'FINAL_STAGED_BYTES_DIVERGENCE')
        return {'final_file':str(target),'sha256':sha(final),'file_size':len(final),
                'row_count':stage.row_count,'byte_equal':True,'append_only':True}
    finally:
        if temp.exists(): temp.unlink()
        # A post-publication verification failure MUST stay visible as
        # controlled-stop; never delete or overwrite an uncertain frozen file.


def verify_promoted_bytes(stage: StagedArtifact, receipt: dict):
    """Read-only post-promotion proof of frozen/staged byte identity."""
    require(type(receipt) is dict and type(receipt.get('final_file')) is str,
            'INVALID_PROMOTION_RECEIPT')
    final=Path(receipt['final_file'])
    require(final.name==same_name(stage.binding.unit_id)+'.json', 'FINAL_UNIT_BINDING_MISMATCH')
    frozen=safe_read(final)
    staged=verify_stage(stage)
    require(frozen==staged and len(frozen)==stage.file_size and
            sha(frozen)==stage.staged_bytes_sha256==receipt.get('sha256') and
            type(receipt.get('row_count')) is int and receipt['row_count']==stage.row_count,
            'POST_PROMOTION_BYTE_IDENTITY_FAILURE')
    return True
