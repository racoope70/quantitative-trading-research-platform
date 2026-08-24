"""Offline contract tests for canonical TM-078/TM-081 dataset publication.

TM-081 historical source attribution:
``racoope70/ppo-trading-pipeline`` at immutable source commit
``072103f43d8b2488c3efca183f637ab0508a193a``, historical path
``tests/test_ppo_v2_parquet_writer_contract.py``.
"""

from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pyarrow as pa
import pyarrow.parquet as pq
import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import quantitative_trading_research.artifacts.dataset_publication as publication
from quantitative_trading_research.artifacts.dataset_publication import (
    CHECKSUMS_FILENAME,
    CHECKSUMS_SCHEMA_ID,
    CHECKSUMS_SCHEMA_VERSION,
    DATASET_FILENAME,
    MANIFEST_FILENAME,
    MANIFEST_SCHEMA_ID,
    MANIFEST_SCHEMA_VERSION,
    PARQUET_ENGINE,
    PUBLICATION_TYPE,
    SCIENTIFIC_ACCEPTANCE_STATUS,
    WRITER_CONTRACT_ID,
    DatasetPublicationCollisionError,
    DatasetPublicationError,
    DatasetPublicationUnsupportedPrimitiveError,
    DatasetPublicationVerificationError,
    publish_dataset,
    verify_published_dataset,
)


def _table() -> pa.Table:
    return pa.table(
        {
            "symbol": ["AAA", "BBB", "CCC"],
            "value": [1.25, 2.5, 3.75],
            "sequence": [1, 2, 3],
        }
    )


def _publication_arguments(destination: Path) -> dict[str, object]:
    return {
        "table": _table(),
        "destination": destination,
        "dataset_id": "synthetic-dataset-v1",
        "provenance": {
            "source": "synthetic_fixture",
            "source_id": "tm078-tm081-test",
        },
        "metadata": {
            "purpose": "offline_contract_verification",
            "accepted_dataset": False,
        },
    }


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_canonical_json(path: Path, payload: object) -> None:
    path.write_bytes(publication._canonical_json_file_bytes(payload))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _staging_entries(root: Path, destination_name: str = "published") -> list[Path]:
    prefix = f".{destination_name}.staging-"
    return [
        path
        for path in root.iterdir()
        if path.name.startswith(prefix)
    ]


def _assert_no_staging(root: Path, destination_name: str = "published") -> None:
    assert _staging_entries(root, destination_name) == []


def _refresh_manifest_checksum(destination: Path) -> None:
    manifest_path = destination / MANIFEST_FILENAME
    checksums_path = destination / CHECKSUMS_FILENAME
    checksums = _read_json(checksums_path)
    checksums["files"][MANIFEST_FILENAME] = _sha256(manifest_path)
    _write_canonical_json(checksums_path, checksums)


def test_atomic_publication_creates_exact_verified_bundle(tmp_path):
    destination = tmp_path / "published"

    manifest = publish_dataset(**_publication_arguments(destination))

    assert destination.is_dir()
    assert {path.name for path in destination.iterdir()} == {
        DATASET_FILENAME,
        MANIFEST_FILENAME,
        CHECKSUMS_FILENAME,
    }

    assert manifest["schema_id"] == MANIFEST_SCHEMA_ID
    assert manifest["schema_version"] == MANIFEST_SCHEMA_VERSION
    assert manifest["publication_type"] == PUBLICATION_TYPE
    assert manifest["dataset_id"] == "synthetic-dataset-v1"
    assert (
        manifest["scientific_acceptance_status"]
        == SCIENTIFIC_ACCEPTANCE_STATUS
    )
    assert verify_published_dataset(destination) == manifest
    _assert_no_staging(tmp_path)


def test_manifest_and_checksum_contracts_are_exact(tmp_path):
    destination = tmp_path / "published"

    manifest = publish_dataset(**_publication_arguments(destination))
    checksums = _read_json(destination / CHECKSUMS_FILENAME)

    assert checksums["schema_id"] == CHECKSUMS_SCHEMA_ID
    assert checksums["schema_version"] == CHECKSUMS_SCHEMA_VERSION
    assert checksums["algorithm"] == "sha256"
    assert set(checksums["files"]) == {
        DATASET_FILENAME,
        MANIFEST_FILENAME,
    }

    dataset_path = destination / DATASET_FILENAME
    manifest_path = destination / MANIFEST_FILENAME

    assert checksums["files"][DATASET_FILENAME] == _sha256(dataset_path)
    assert checksums["files"][MANIFEST_FILENAME] == _sha256(manifest_path)
    assert manifest["dataset_sha256"] == _sha256(dataset_path)
    assert manifest["dataset_size_bytes"] == dataset_path.stat().st_size


def test_writer_contract_is_explicit_pyarrow_only(tmp_path):
    destination = tmp_path / "published"

    manifest = publish_dataset(**_publication_arguments(destination))
    writer = manifest["writer_contract"]

    assert writer["contract_id"] == WRITER_CONTRACT_ID
    assert writer["engine"] == PARQUET_ENGINE == "pyarrow"
    assert writer["options"] == {
        "version": "2.6",
        "compression": "snappy",
        "row_group_size": 65536,
        "use_dictionary": False,
        "write_statistics": True,
        "store_schema": True,
    }


def test_same_input_produces_identical_publication_bytes(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_manifest = publish_dataset(**_publication_arguments(first))
    second_manifest = publish_dataset(**_publication_arguments(second))

    assert first_manifest == second_manifest
    assert (
        (first / DATASET_FILENAME).read_bytes()
        == (second / DATASET_FILENAME).read_bytes()
    )
    assert (
        (first / MANIFEST_FILENAME).read_bytes()
        == (second / MANIFEST_FILENAME).read_bytes()
    )
    assert (
        (first / CHECKSUMS_FILENAME).read_bytes()
        == (second / CHECKSUMS_FILENAME).read_bytes()
    )


def test_readback_preserves_shape_columns_and_schema_identity(tmp_path):
    destination = tmp_path / "published"

    manifest = publish_dataset(**_publication_arguments(destination))
    readback = pq.read_table(destination / DATASET_FILENAME)

    assert readback.num_rows == 3
    assert readback.num_columns == 3
    assert readback.column_names == ["symbol", "value", "sequence"]
    assert manifest["row_count"] == readback.num_rows
    assert manifest["column_count"] == readback.num_columns
    assert manifest["column_names"] == readback.column_names
    assert verify_published_dataset(destination) == manifest


@pytest.mark.skipif(
    sys.platform != "linux",
    reason="canonical no-replace primitive is Linux renameat2",
)
def test_true_noreplace_race_never_replaces_concurrent_destination(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"
    original_commit = publication._atomic_no_replace_commit

    def create_destination_immediately_before_commit(stage, final_destination):
        final_destination.mkdir()
        (final_destination / "sentinel.txt").write_text(
            "concurrent-writer",
            encoding="utf-8",
        )
        original_commit(stage, final_destination)

    monkeypatch.setattr(
        publication,
        "_atomic_no_replace_commit",
        create_destination_immediately_before_commit,
    )

    with pytest.raises(
        DatasetPublicationCollisionError,
        match="already exists",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert destination.is_dir()
    assert (
        destination / "sentinel.txt"
    ).read_text(encoding="utf-8") == "concurrent-writer"
    assert not (destination / DATASET_FILENAME).exists()
    _assert_no_staging(tmp_path)


def test_existing_directory_destination_is_rejected_and_preserved(tmp_path):
    destination = tmp_path / "published"
    destination.mkdir()
    sentinel = destination / "sentinel.txt"
    sentinel.write_text("preserve-directory", encoding="utf-8")

    with pytest.raises(
        DatasetPublicationCollisionError,
        match="already exists",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert sentinel.read_text(encoding="utf-8") == "preserve-directory"
    assert {path.name for path in destination.iterdir()} == {"sentinel.txt"}
    _assert_no_staging(tmp_path)


def test_existing_regular_file_destination_is_rejected_and_preserved(tmp_path):
    destination = tmp_path / "published"
    destination.write_bytes(b"preserve-regular-file")

    with pytest.raises(
        DatasetPublicationCollisionError,
        match="already exists",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert destination.is_file()
    assert destination.read_bytes() == b"preserve-regular-file"
    _assert_no_staging(tmp_path)


def test_existing_symlink_destination_is_rejected_and_preserved(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    sentinel = target / "sentinel.txt"
    sentinel.write_text("preserve-symlink-target", encoding="utf-8")

    destination = tmp_path / "published"
    destination.symlink_to(target, target_is_directory=True)

    original_link_target = os.readlink(destination)

    with pytest.raises(
        DatasetPublicationCollisionError,
        match="already exists",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert destination.is_symlink()
    assert os.readlink(destination) == original_link_target
    assert sentinel.read_text(encoding="utf-8") == "preserve-symlink-target"
    _assert_no_staging(tmp_path)


@pytest.mark.parametrize("unsupported_errno", [errno.ENOSYS, errno.EINVAL])
def test_unsupported_noreplace_primitive_fails_closed_without_plain_rename(
    tmp_path,
    monkeypatch,
    unsupported_errno,
):
    destination = tmp_path / "published"

    def unsupported_renameat2(*args):
        ctypes.set_errno(unsupported_errno)
        return -1

    monkeypatch.setattr(
        publication,
        "_load_renameat2",
        lambda: unsupported_renameat2,
    )
    monkeypatch.setattr(
        os,
        "rename",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("plain os.rename fallback invoked")
        ),
    )

    with pytest.raises(
        DatasetPublicationUnsupportedPrimitiveError,
        match="unsupported",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_failure_after_dataset_creation_cleans_staging(tmp_path, monkeypatch):
    destination = tmp_path / "published"

    def fail_dataset_fsync(path):
        assert path.name == DATASET_FILENAME
        raise DatasetPublicationError("injected dataset fsync failure")

    monkeypatch.setattr(
        publication,
        "_fsync_existing_file",
        fail_dataset_fsync,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected dataset fsync failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_failure_during_manifest_write_cleans_staging(tmp_path, monkeypatch):
    destination = tmp_path / "published"
    original_write = publication._write_exclusive_file

    def fail_manifest(path, payload):
        if path.name == MANIFEST_FILENAME:
            raise DatasetPublicationError("injected manifest write failure")
        return original_write(path, payload)

    monkeypatch.setattr(
        publication,
        "_write_exclusive_file",
        fail_manifest,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected manifest write failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_failure_during_checksum_write_cleans_staging(tmp_path, monkeypatch):
    destination = tmp_path / "published"
    original_write = publication._write_exclusive_file

    def fail_checksums(path, payload):
        if path.name == CHECKSUMS_FILENAME:
            raise DatasetPublicationError("injected checksum write failure")
        return original_write(path, payload)

    monkeypatch.setattr(
        publication,
        "_write_exclusive_file",
        fail_checksums,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected checksum write failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_failure_during_staged_verification_cleans_staging(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"

    def fail_staged_verification(path):
        raise DatasetPublicationVerificationError(
            "injected staged verification failure"
        )

    monkeypatch.setattr(
        publication,
        "verify_published_dataset",
        fail_staged_verification,
    )

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="injected staged verification failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_commit_primitive_failure_cleans_staging_and_leaves_final_absent(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"

    def fail_commit(stage, final_destination):
        raise DatasetPublicationError("injected commit primitive failure")

    monkeypatch.setattr(
        publication,
        "_atomic_no_replace_commit",
        fail_commit,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected commit primitive failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_staging_directory_fsync_failure_is_precommit_and_cleans_stage(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"
    original_fsync = publication._fsync_directory

    def fail_stage_fsync(path):
        if path.name.startswith(".published.staging-"):
            raise DatasetPublicationError(
                "injected staging directory fsync failure"
            )
        return original_fsync(path)

    monkeypatch.setattr(
        publication,
        "_fsync_directory",
        fail_stage_fsync,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected staging directory fsync failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    _assert_no_staging(tmp_path)


def test_parent_directory_fsync_failure_preserves_committed_destination(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"
    original_fsync = publication._fsync_directory
    resolved_parent = tmp_path.resolve()

    def fail_parent_fsync(path):
        if path == resolved_parent:
            raise DatasetPublicationError(
                "injected parent directory fsync failure"
            )
        return original_fsync(path)

    monkeypatch.setattr(
        publication,
        "_fsync_directory",
        fail_parent_fsync,
    )

    with pytest.raises(
        DatasetPublicationError,
        match="injected parent directory fsync failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert destination.is_dir()
    assert {path.name for path in destination.iterdir()} == {
        DATASET_FILENAME,
        MANIFEST_FILENAME,
        CHECKSUMS_FILENAME,
    }
    assert verify_published_dataset(destination)["dataset_id"] == (
        "synthetic-dataset-v1"
    )
    _assert_no_staging(tmp_path)


def test_postrename_verification_failure_preserves_committed_destination(
    tmp_path,
    monkeypatch,
):
    destination = tmp_path / "published"
    original_verify = publication.verify_published_dataset

    def fail_only_final(path):
        candidate = Path(path)
        if candidate.name.startswith(".published.staging-"):
            return original_verify(path)
        raise DatasetPublicationVerificationError(
            "injected post-rename verification failure"
        )

    monkeypatch.setattr(
        publication,
        "verify_published_dataset",
        fail_only_final,
    )

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="injected post-rename verification failure",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert destination.is_dir()
    assert {path.name for path in destination.iterdir()} == {
        DATASET_FILENAME,
        MANIFEST_FILENAME,
        CHECKSUMS_FILENAME,
    }
    _assert_no_staging(tmp_path)

    monkeypatch.setattr(
        publication,
        "verify_published_dataset",
        original_verify,
    )
    assert verify_published_dataset(destination)["dataset_id"] == (
        "synthetic-dataset-v1"
    )


def test_cleanup_failure_is_observable(tmp_path, monkeypatch):
    destination = tmp_path / "published"
    original_rmtree = shutil.rmtree

    def fail_write(*args, **kwargs):
        raise RuntimeError("injected parquet failure")

    def fail_cleanup(path, *args, **kwargs):
        raise OSError("injected cleanup failure")

    monkeypatch.setattr(pq, "write_table", fail_write)
    monkeypatch.setattr(shutil, "rmtree", fail_cleanup)

    with pytest.raises(
        DatasetPublicationError,
        match="failed to clean uncommitted publication staging directory",
    ):
        publish_dataset(**_publication_arguments(destination))

    assert not destination.exists()
    stages = _staging_entries(tmp_path)
    assert len(stages) == 1

    monkeypatch.setattr(shutil, "rmtree", original_rmtree)
    original_rmtree(stages[0])
    _assert_no_staging(tmp_path)


def test_incomplete_bundle_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    (destination / CHECKSUMS_FILENAME).unlink()

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="bundle files mismatch",
    ):
        verify_published_dataset(destination)


def test_dataset_checksum_tampering_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    dataset = destination / DATASET_FILENAME
    dataset.write_bytes(dataset.read_bytes() + b"tamper")

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="dataset checksum mismatch",
    ):
        verify_published_dataset(destination)


def test_manifest_checksum_tampering_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    manifest_path = destination / MANIFEST_FILENAME
    manifest = _read_json(manifest_path)
    manifest["dataset_id"] = "tampered-dataset"
    _write_canonical_json(manifest_path, manifest)

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="manifest checksum mismatch",
    ):
        verify_published_dataset(destination)


def test_direct_manifest_dataset_binding_mismatch_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    manifest_path = destination / MANIFEST_FILENAME
    manifest = _read_json(manifest_path)
    manifest["dataset_sha256"] = "0" * 64
    _write_canonical_json(manifest_path, manifest)
    _refresh_manifest_checksum(destination)

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="manifest dataset checksum mismatch",
    ):
        verify_published_dataset(destination)


def test_malformed_manifest_dataset_checksum_metadata_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    manifest_path = destination / MANIFEST_FILENAME
    manifest = _read_json(manifest_path)
    manifest["dataset_sha256"] = "not-a-sha256"
    _write_canonical_json(manifest_path, manifest)
    _refresh_manifest_checksum(destination)

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="manifest dataset checksum is invalid",
    ):
        verify_published_dataset(destination)


def test_unsupported_checksum_algorithm_metadata_is_rejected(tmp_path):
    destination = tmp_path / "published"
    publish_dataset(**_publication_arguments(destination))

    checksums_path = destination / CHECKSUMS_FILENAME
    checksums = _read_json(checksums_path)
    checksums["algorithm"] = "md5"
    _write_canonical_json(checksums_path, checksums)

    with pytest.raises(
        DatasetPublicationVerificationError,
        match="unsupported checksums algorithm",
    ):
        verify_published_dataset(destination)


@pytest.mark.parametrize(
    "dataset_id",
    [
        "",
        "   ",
        " padded ",
        None,
        123,
    ],
)
def test_invalid_dataset_identity_fails_closed(tmp_path, dataset_id):
    arguments = _publication_arguments(tmp_path / "published")
    arguments["dataset_id"] = dataset_id

    with pytest.raises(DatasetPublicationError, match="dataset_id"):
        publish_dataset(**arguments)


@pytest.mark.parametrize(
    "provenance",
    [
        {},
        [],
        "",
        False,
        {1: "bad-key"},
        {"bad": float("nan")},
    ],
)
def test_invalid_provenance_fails_closed(tmp_path, provenance):
    arguments = _publication_arguments(tmp_path / "published")
    arguments["provenance"] = provenance

    with pytest.raises(DatasetPublicationError):
        publish_dataset(**arguments)


@pytest.mark.parametrize(
    "metadata",
    [
        [],
        "",
        False,
        {1: "bad-key"},
        {"bad": float("inf")},
    ],
)
def test_invalid_metadata_fails_closed(tmp_path, metadata):
    arguments = _publication_arguments(tmp_path / "published")
    arguments["metadata"] = metadata

    with pytest.raises(DatasetPublicationError):
        publish_dataset(**arguments)


def test_non_arrow_table_is_rejected(tmp_path):
    arguments = _publication_arguments(tmp_path / "published")
    arguments["table"] = {"value": [1, 2, 3]}

    with pytest.raises(
        DatasetPublicationError,
        match="pyarrow.Table",
    ):
        publish_dataset(**arguments)


def test_duplicate_column_names_are_rejected(tmp_path):
    table = pa.Table.from_arrays(
        [
            pa.array([1, 2]),
            pa.array([3, 4]),
        ],
        names=["duplicate", "duplicate"],
    )
    arguments = _publication_arguments(tmp_path / "published")
    arguments["table"] = table

    with pytest.raises(
        DatasetPublicationError,
        match="column names must be unique",
    ):
        publish_dataset(**arguments)


def test_relative_destination_is_rejected(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    arguments = _publication_arguments(Path("relative-publication"))

    with pytest.raises(
        DatasetPublicationError,
        match="absolute path",
    ):
        publish_dataset(**arguments)


def test_publication_does_not_claim_scientific_acceptance(tmp_path):
    destination = tmp_path / "published"

    manifest = publish_dataset(**_publication_arguments(destination))

    assert (
        manifest["scientific_acceptance_status"]
        == "NOT_ESTABLISHED_BY_PUBLICATION"
    )
    serialized = json.dumps(manifest, sort_keys=True)
    assert "training_ready" not in serialized
    assert "final_holdout_eligible" not in serialized
    assert "provider_verified" not in serialized


def test_module_import_has_no_filesystem_or_network_side_effects():
    source_root = ROOT / "src"

    code = """
from unittest.mock import patch

with patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir called")), \\
     patch("pathlib.Path.write_text", side_effect=AssertionError("write called")), \\
     patch("pathlib.Path.write_bytes", side_effect=AssertionError("write called")), \\
     patch("socket.socket.connect", side_effect=AssertionError("network called")), \\
     patch("socket.create_connection", side_effect=AssertionError("network called")):
    import quantitative_trading_research.artifacts.dataset_publication
"""

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(source_root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, (
        f"stdout={completed.stdout}\nstderr={completed.stderr}"
    )
