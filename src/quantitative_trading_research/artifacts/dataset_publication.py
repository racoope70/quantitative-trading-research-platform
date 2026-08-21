"""Atomic offline publication of checksummed dataset bundles.

Reimplemented with attribution from ``racoope70/ppo-trading-pipeline`` at
immutable source commit ``072103f43d8b2488c3efca183f637ab0508a193a``,
historical path ``src/ppo_v2_parquet_writer.py``.

The historical source intentionally prohibited dataset writing at its original
checkpoint. This selected C4 responsibility replaces that inert authorization
guard with bounded offline publication mechanics only.

This module accepts an explicit caller-supplied ``pyarrow.Table`` and publishes
a deterministic Parquet bundle into an explicit new destination directory using
same-parent staging, checksums, deterministic manifests, verified readback, and
a Linux atomic no-replace namespace commit.

A successful atomic no-replace rename is the publication commit point. Failures
before that point clean uncommitted staging state where safely possible.
Failures after that point are reported fail closed while preserving the
committed destination for diagnosis and recovery.

Publication does not establish scientific dataset acceptance, provider truth,
training readiness, model qualification, final-holdout eligibility, or any
paper/live trading state. No provider or network access occurs here.
"""

from __future__ import annotations

import ctypes
import errno
import hashlib
import hmac
import json
import math
import os
from os import PathLike
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any


MANIFEST_SCHEMA_ID = "C4_DATASET_PUBLICATION_MANIFEST_V1"
MANIFEST_SCHEMA_VERSION = 1
CHECKSUMS_SCHEMA_ID = "C4_DATASET_PUBLICATION_CHECKSUMS_V1"
CHECKSUMS_SCHEMA_VERSION = 1
PUBLICATION_TYPE = "offline_dataset_publication"
SCIENTIFIC_ACCEPTANCE_STATUS = "NOT_ESTABLISHED_BY_PUBLICATION"
CHECKSUM_ALGORITHM = "sha256"

DATASET_FILENAME = "dataset.parquet"
MANIFEST_FILENAME = "manifest.json"
CHECKSUMS_FILENAME = "checksums.json"

WRITER_CONTRACT_ID = "C4_PYARROW_PARQUET_WRITER_V1"
PARQUET_ENGINE = "pyarrow"

PARQUET_WRITER_OPTIONS: dict[str, Any] = {
    "version": "2.6",
    "compression": "snappy",
    "row_group_size": 65536,
    "use_dictionary": False,
    "write_statistics": True,
    "store_schema": True,
}

AT_FDCWD = -100
RENAME_NOREPLACE = 1

_REQUIRED_BUNDLE_FILES = {
    DATASET_FILENAME,
    MANIFEST_FILENAME,
    CHECKSUMS_FILENAME,
}

_MANIFEST_KEYS = {
    "schema_id",
    "schema_version",
    "publication_type",
    "dataset_id",
    "dataset_file",
    "row_count",
    "column_count",
    "column_names",
    "arrow_schema_sha256",
    "dataset_size_bytes",
    "dataset_sha256",
    "writer_contract",
    "provenance",
    "metadata",
    "scientific_acceptance_status",
}

_CHECKSUMS_KEYS = {
    "schema_id",
    "schema_version",
    "algorithm",
    "files",
}

_CHECKSUM_FILE_KEYS = {
    DATASET_FILENAME,
    MANIFEST_FILENAME,
}


class DatasetPublicationError(ValueError):
    """Base fail-closed error for invalid dataset publication."""


class DatasetPublicationCollisionError(DatasetPublicationError):
    """Raised when the requested publication destination already exists."""


class DatasetPublicationVerificationError(DatasetPublicationError):
    """Raised when a staged or published bundle fails readback verification."""


class DatasetPublicationUnsupportedPrimitiveError(DatasetPublicationError):
    """Raised when atomic no-replace publication is unavailable."""


def _load_pyarrow() -> tuple[Any, Any]:
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise DatasetPublicationError(
            "canonical dataset publication requires pyarrow"
        ) from exc
    return pa, pq


def normalize_publication_value(value: Any) -> Any:
    """Return a deterministic JSON-compatible representation."""
    if value is None or type(value) in (str, bool, int):
        return value

    if type(value) is float:
        if not math.isfinite(value):
            raise DatasetPublicationError(
                "publication metadata does not permit non-finite floats"
            )
        return value

    if type(value) is dict:
        if any(not isinstance(key, str) for key in value):
            raise DatasetPublicationError(
                "publication mapping keys must be strings"
            )

        normalized: dict[str, Any] = {}
        for key in sorted(value):
            normalized[key] = normalize_publication_value(value[key])
        return normalized

    if type(value) in (list, tuple):
        return [
            normalize_publication_value(item)
            for item in value
        ]

    raise DatasetPublicationError(
        "unsupported publication value type: "
        f"{type(value).__name__}"
    )


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize supported publication metadata deterministically."""
    normalized = normalize_publication_value(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _canonical_json_file_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_sha256_hex(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _require_mapping(
    name: str,
    value: Any,
    *,
    allow_empty: bool,
) -> dict[str, Any]:
    if type(value) is not dict:
        raise DatasetPublicationError(f"{name} must be a dict")

    if not allow_empty and not value:
        raise DatasetPublicationError(f"{name} must not be empty")

    normalized = normalize_publication_value(value)
    if type(normalized) is not dict:
        raise DatasetPublicationError(
            f"{name} must normalize to a dict"
        )

    return normalized


def _require_dataset_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DatasetPublicationError(
            "dataset_id must be a non-empty string"
        )

    if value != value.strip():
        raise DatasetPublicationError(
            "dataset_id must not contain surrounding whitespace"
        )

    return value


def _coerce_new_destination(
    destination: str | PathLike[str],
) -> Path:
    if isinstance(destination, str) and not destination.strip():
        raise DatasetPublicationError(
            "destination must not be empty"
        )

    try:
        candidate = Path(destination)
    except (TypeError, ValueError) as exc:
        raise DatasetPublicationError(
            "destination must be a filesystem path"
        ) from exc

    if not candidate.is_absolute():
        raise DatasetPublicationError(
            "destination must be an absolute path"
        )

    if candidate.name in ("", ".", ".."):
        raise DatasetPublicationError(
            "destination must name a publication directory"
        )

    try:
        parent = candidate.parent.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise DatasetPublicationError(
            "destination parent must be an existing directory"
        ) from exc

    if not parent.is_dir():
        raise DatasetPublicationError(
            "destination parent must be an existing directory"
        )

    final = parent / candidate.name

    # Early diagnostic only. Correctness does not depend on this check:
    # _atomic_no_replace_commit() is the authoritative collision boundary.
    if os.path.lexists(final):
        raise DatasetPublicationCollisionError(
            "publication destination already exists"
        )

    return final


def _coerce_existing_publication(
    destination: str | PathLike[str],
) -> Path:
    if isinstance(destination, str) and not destination.strip():
        raise DatasetPublicationVerificationError(
            "publication path must not be empty"
        )

    try:
        candidate = Path(destination)
    except (TypeError, ValueError) as exc:
        raise DatasetPublicationVerificationError(
            "publication path must be a filesystem path"
        ) from exc

    if not candidate.is_absolute():
        raise DatasetPublicationVerificationError(
            "publication path must be absolute"
        )

    if candidate.is_symlink():
        raise DatasetPublicationVerificationError(
            "publication directory must not be a symlink"
        )

    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise DatasetPublicationVerificationError(
            "publication directory does not exist"
        ) from exc

    if not resolved.is_dir():
        raise DatasetPublicationVerificationError(
            "publication path must identify a directory"
        )

    return resolved


def _write_exclusive_file(path: Path, payload: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise DatasetPublicationError(
            f"failed to write publication file: {path.name}"
        ) from exc


def _fsync_existing_file(path: Path) -> None:
    try:
        with path.open("rb") as handle:
            os.fsync(handle.fileno())
    except OSError as exc:
        raise DatasetPublicationError(
            f"failed to synchronize publication file: {path.name}"
        ) from exc


def _fsync_directory(path: Path) -> None:
    """Synchronize directory metadata at an explicit durability boundary."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)

    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise DatasetPublicationError(
            f"failed to open publication directory for synchronization: {path.name}"
        ) from exc

    try:
        os.fsync(descriptor)
    except OSError as exc:
        raise DatasetPublicationError(
            f"failed to synchronize publication directory: {path.name}"
        ) from exc
    finally:
        os.close(descriptor)


def _load_renameat2() -> Any:
    """Load Linux renameat2 without providing a weaker fallback."""
    if sys.platform != "linux":
        raise DatasetPublicationUnsupportedPrimitiveError(
            "atomic no-replace publication requires Linux renameat2"
        )

    try:
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = libc.renameat2
    except (OSError, AttributeError) as exc:
        raise DatasetPublicationUnsupportedPrimitiveError(
            "Linux renameat2 is unavailable"
        ) from exc

    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    return renameat2


def _atomic_no_replace_commit(stage: Path, final_destination: Path) -> None:
    """Atomically commit ``stage`` only if ``final_destination`` is absent.

    There is deliberately no fallback to plain ``os.rename``, check-then-rename,
    copying, or any other weaker publication primitive.
    """
    renameat2 = _load_renameat2()

    ctypes.set_errno(0)
    result = renameat2(
        AT_FDCWD,
        os.fsencode(stage),
        AT_FDCWD,
        os.fsencode(final_destination),
        RENAME_NOREPLACE,
    )

    if result == 0:
        return

    error_number = ctypes.get_errno()

    if error_number in {
        errno.EEXIST,
        getattr(errno, "ENOTEMPTY", errno.EEXIST),
    }:
        raise DatasetPublicationCollisionError(
            "publication destination already exists"
        )

    unsupported_errors = {
        errno.ENOSYS,
        errno.EINVAL,
    }
    if hasattr(errno, "EOPNOTSUPP"):
        unsupported_errors.add(errno.EOPNOTSUPP)
    if hasattr(errno, "ENOTSUP"):
        unsupported_errors.add(errno.ENOTSUP)

    if error_number in unsupported_errors:
        raise DatasetPublicationUnsupportedPrimitiveError(
            "atomic no-replace publication primitive is unsupported"
        )

    # This check is diagnostic only and occurs after the atomic primitive
    # itself failed. It cannot cause replacement of the destination.
    if os.path.lexists(final_destination):
        raise DatasetPublicationCollisionError(
            "publication destination already exists"
        )

    raise DatasetPublicationError(
        "atomic no-replace dataset publication commit failed "
        f"with errno={error_number}"
    )


def _cleanup_uncommitted_stage(stage: Path) -> None:
    """Remove uncommitted staging state or make cleanup failure observable."""
    if not os.path.lexists(stage):
        return

    try:
        shutil.rmtree(stage)
    except OSError as exc:
        raise DatasetPublicationError(
            "failed to clean uncommitted publication staging directory"
        ) from exc

    if os.path.lexists(stage):
        raise DatasetPublicationError(
            "uncommitted publication staging directory remains after cleanup"
        )


def _schema_sha256(schema: Any) -> str:
    try:
        encoded = schema.serialize().to_pybytes()
    except Exception as exc:
        raise DatasetPublicationError(
            "unable to serialize Arrow schema identity"
        ) from exc
    return _sha256_bytes(encoded)


def _writer_contract() -> dict[str, Any]:
    return {
        "contract_id": WRITER_CONTRACT_ID,
        "engine": PARQUET_ENGINE,
        "options": dict(PARQUET_WRITER_OPTIONS),
    }


def _validate_input_table(table: Any) -> tuple[Any, Any]:
    pa, pq = _load_pyarrow()

    if not isinstance(table, pa.Table):
        raise DatasetPublicationError(
            "dataset must be supplied as a pyarrow.Table"
        )

    column_names = list(table.column_names)

    if not column_names:
        raise DatasetPublicationError(
            "dataset must contain at least one column"
        )

    if any(not isinstance(name, str) or not name for name in column_names):
        raise DatasetPublicationError(
            "dataset column names must be non-empty strings"
        )

    if len(set(column_names)) != len(column_names):
        raise DatasetPublicationError(
            "dataset column names must be unique"
        )

    return pa, pq


def _build_manifest(
    *,
    table: Any,
    dataset_id: str,
    dataset_path: Path,
    provenance: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    dataset_sha256 = _sha256_file(dataset_path)
    dataset_size_bytes = dataset_path.stat().st_size

    return {
        "schema_id": MANIFEST_SCHEMA_ID,
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "publication_type": PUBLICATION_TYPE,
        "dataset_id": dataset_id,
        "dataset_file": DATASET_FILENAME,
        "row_count": table.num_rows,
        "column_count": table.num_columns,
        "column_names": list(table.column_names),
        "arrow_schema_sha256": _schema_sha256(table.schema),
        "dataset_size_bytes": dataset_size_bytes,
        "dataset_sha256": dataset_sha256,
        "writer_contract": _writer_contract(),
        "provenance": provenance,
        "metadata": metadata,
        "scientific_acceptance_status": SCIENTIFIC_ACCEPTANCE_STATUS,
    }


def _build_checksums(
    *,
    dataset_path: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    return {
        "schema_id": CHECKSUMS_SCHEMA_ID,
        "schema_version": CHECKSUMS_SCHEMA_VERSION,
        "algorithm": CHECKSUM_ALGORITHM,
        "files": {
            DATASET_FILENAME: _sha256_file(dataset_path),
            MANIFEST_FILENAME: _sha256_file(manifest_path),
        },
    }


def _validate_manifest_structure(manifest: Any) -> None:
    if type(manifest) is not dict:
        raise DatasetPublicationVerificationError(
            "manifest must be a dict"
        )

    if set(manifest) != _MANIFEST_KEYS:
        raise DatasetPublicationVerificationError(
            "manifest keys mismatch"
        )

    if manifest["schema_id"] != MANIFEST_SCHEMA_ID:
        raise DatasetPublicationVerificationError(
            "unsupported manifest schema_id"
        )

    if type(manifest["schema_version"]) is not int:
        raise DatasetPublicationVerificationError(
            "manifest schema_version must be an int"
        )

    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise DatasetPublicationVerificationError(
            "unsupported manifest schema_version"
        )

    if manifest["publication_type"] != PUBLICATION_TYPE:
        raise DatasetPublicationVerificationError(
            "unsupported publication type"
        )

    try:
        _require_dataset_id(manifest["dataset_id"])
    except DatasetPublicationError as exc:
        raise DatasetPublicationVerificationError(str(exc)) from exc

    if manifest["dataset_file"] != DATASET_FILENAME:
        raise DatasetPublicationVerificationError(
            "manifest dataset filename mismatch"
        )

    for name in (
        "row_count",
        "column_count",
        "dataset_size_bytes",
    ):
        value = manifest[name]
        if type(value) is not int or value < 0:
            raise DatasetPublicationVerificationError(
                f"manifest {name} must be a non-negative int"
            )

    if manifest["column_count"] < 1:
        raise DatasetPublicationVerificationError(
            "manifest column_count must be positive"
        )

    column_names = manifest["column_names"]
    if (
        type(column_names) is not list
        or len(column_names) != manifest["column_count"]
        or any(
            not isinstance(name, str) or not name
            for name in column_names
        )
        or len(set(column_names)) != len(column_names)
    ):
        raise DatasetPublicationVerificationError(
            "manifest column_names are invalid"
        )

    if not _is_sha256_hex(manifest["arrow_schema_sha256"]):
        raise DatasetPublicationVerificationError(
            "manifest Arrow schema checksum is invalid"
        )

    if not _is_sha256_hex(manifest["dataset_sha256"]):
        raise DatasetPublicationVerificationError(
            "manifest dataset checksum is invalid"
        )

    if manifest["writer_contract"] != _writer_contract():
        raise DatasetPublicationVerificationError(
            "manifest writer contract mismatch"
        )

    try:
        provenance = _require_mapping(
            "provenance",
            manifest["provenance"],
            allow_empty=False,
        )
        metadata = _require_mapping(
            "metadata",
            manifest["metadata"],
            allow_empty=True,
        )
    except DatasetPublicationError as exc:
        raise DatasetPublicationVerificationError(str(exc)) from exc

    if provenance != manifest["provenance"]:
        raise DatasetPublicationVerificationError(
            "manifest provenance is not normalized"
        )

    if metadata != manifest["metadata"]:
        raise DatasetPublicationVerificationError(
            "manifest metadata is not normalized"
        )

    if (
        manifest["scientific_acceptance_status"]
        != SCIENTIFIC_ACCEPTANCE_STATUS
    ):
        raise DatasetPublicationVerificationError(
            "publication must not establish scientific dataset acceptance"
        )


def _validate_checksums_structure(checksums: Any) -> None:
    if type(checksums) is not dict:
        raise DatasetPublicationVerificationError(
            "checksums document must be a dict"
        )

    if set(checksums) != _CHECKSUMS_KEYS:
        raise DatasetPublicationVerificationError(
            "checksums document keys mismatch"
        )

    if checksums["schema_id"] != CHECKSUMS_SCHEMA_ID:
        raise DatasetPublicationVerificationError(
            "unsupported checksums schema_id"
        )

    if type(checksums["schema_version"]) is not int:
        raise DatasetPublicationVerificationError(
            "checksums schema_version must be an int"
        )

    if checksums["schema_version"] != CHECKSUMS_SCHEMA_VERSION:
        raise DatasetPublicationVerificationError(
            "unsupported checksums schema_version"
        )

    if checksums["algorithm"] != CHECKSUM_ALGORITHM:
        raise DatasetPublicationVerificationError(
            "unsupported checksums algorithm"
        )

    files = checksums["files"]
    if type(files) is not dict or set(files) != _CHECKSUM_FILE_KEYS:
        raise DatasetPublicationVerificationError(
            "checksums file map mismatch"
        )

    for filename in sorted(_CHECKSUM_FILE_KEYS):
        if not _is_sha256_hex(files[filename]):
            raise DatasetPublicationVerificationError(
                f"invalid checksum for {filename}"
            )


def _read_json_dict(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DatasetPublicationVerificationError(
            f"{label} is unreadable or invalid JSON"
        ) from exc

    if type(payload) is not dict:
        raise DatasetPublicationVerificationError(
            f"{label} must contain a JSON object"
        )

    return payload


def verify_published_dataset(
    destination: str | PathLike[str],
) -> dict[str, Any]:
    """Verify an exact published bundle and return its validated manifest."""
    publication_dir = _coerce_existing_publication(destination)

    try:
        entries = {
            path.name
            for path in publication_dir.iterdir()
        }
    except OSError as exc:
        raise DatasetPublicationVerificationError(
            "unable to inspect publication directory"
        ) from exc

    if entries != _REQUIRED_BUNDLE_FILES:
        raise DatasetPublicationVerificationError(
            "publication bundle files mismatch"
        )

    dataset_path = publication_dir / DATASET_FILENAME
    manifest_path = publication_dir / MANIFEST_FILENAME
    checksums_path = publication_dir / CHECKSUMS_FILENAME

    for path in (
        dataset_path,
        manifest_path,
        checksums_path,
    ):
        if path.is_symlink() or not path.is_file():
            raise DatasetPublicationVerificationError(
                f"publication member is not a regular file: {path.name}"
            )

    manifest = _read_json_dict(manifest_path, "manifest")
    checksums = _read_json_dict(checksums_path, "checksums")

    _validate_manifest_structure(manifest)
    _validate_checksums_structure(checksums)

    actual_dataset_sha256 = _sha256_file(dataset_path)
    actual_manifest_sha256 = _sha256_file(manifest_path)

    expected_dataset_sha256 = checksums["files"][DATASET_FILENAME]
    expected_manifest_sha256 = checksums["files"][MANIFEST_FILENAME]

    if not hmac.compare_digest(
        actual_dataset_sha256,
        expected_dataset_sha256,
    ):
        raise DatasetPublicationVerificationError(
            "dataset checksum mismatch"
        )

    if not hmac.compare_digest(
        actual_manifest_sha256,
        expected_manifest_sha256,
    ):
        raise DatasetPublicationVerificationError(
            "manifest checksum mismatch"
        )

    if not hmac.compare_digest(
        manifest["dataset_sha256"],
        actual_dataset_sha256,
    ):
        raise DatasetPublicationVerificationError(
            "manifest dataset checksum mismatch"
        )

    if manifest["dataset_size_bytes"] != dataset_path.stat().st_size:
        raise DatasetPublicationVerificationError(
            "manifest dataset size mismatch"
        )

    _, pq = _load_pyarrow()

    try:
        table = pq.read_table(dataset_path)
    except Exception as exc:
        raise DatasetPublicationVerificationError(
            "published Parquet dataset cannot be read back"
        ) from exc

    if table.num_rows != manifest["row_count"]:
        raise DatasetPublicationVerificationError(
            "readback row count mismatch"
        )

    if table.num_columns != manifest["column_count"]:
        raise DatasetPublicationVerificationError(
            "readback column count mismatch"
        )

    if list(table.column_names) != manifest["column_names"]:
        raise DatasetPublicationVerificationError(
            "readback column names mismatch"
        )

    actual_schema_sha256 = _schema_sha256(table.schema)
    if not hmac.compare_digest(
        actual_schema_sha256,
        manifest["arrow_schema_sha256"],
    ):
        raise DatasetPublicationVerificationError(
            "readback Arrow schema identity mismatch"
        )

    return manifest


def publish_dataset(
    *,
    table: Any,
    destination: str | PathLike[str],
    dataset_id: str,
    provenance: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Publish one explicit caller-supplied Arrow table.

    Durability ordering is:

    dataset write/close/fsync
    -> manifest write/close/fsync
    -> checksums write/close/fsync
    -> staged verification
    -> staging-directory fsync
    -> atomic Linux no-replace rename (COMMIT POINT)
    -> destination-parent fsync
    -> verified published readback

    A successful no-replace rename commits the namespace transition. No
    recursive rollback of the final destination is attempted after that point.
    """
    _, pq = _validate_input_table(table)
    dataset_id = _require_dataset_id(dataset_id)
    normalized_provenance = _require_mapping(
        "provenance",
        provenance,
        allow_empty=False,
    )
    normalized_metadata = _require_mapping(
        "metadata",
        {} if metadata is None else metadata,
        allow_empty=True,
    )
    final_destination = _coerce_new_destination(destination)

    stage = Path(
        tempfile.mkdtemp(
            prefix=f".{final_destination.name}.staging-",
            dir=final_destination.parent,
        )
    )
    committed = False

    try:
        dataset_path = stage / DATASET_FILENAME
        manifest_path = stage / MANIFEST_FILENAME
        checksums_path = stage / CHECKSUMS_FILENAME

        try:
            pq.write_table(
                table,
                dataset_path,
                **PARQUET_WRITER_OPTIONS,
            )
        except Exception as exc:
            raise DatasetPublicationError(
                "failed to serialize dataset under writer contract"
            ) from exc

        _fsync_existing_file(dataset_path)

        manifest = _build_manifest(
            table=table,
            dataset_id=dataset_id,
            dataset_path=dataset_path,
            provenance=normalized_provenance,
            metadata=normalized_metadata,
        )

        _write_exclusive_file(
            manifest_path,
            _canonical_json_file_bytes(manifest),
        )

        checksums = _build_checksums(
            dataset_path=dataset_path,
            manifest_path=manifest_path,
        )

        _write_exclusive_file(
            checksums_path,
            _canonical_json_file_bytes(checksums),
        )

        verify_published_dataset(stage)
        _fsync_directory(stage)

        _atomic_no_replace_commit(stage, final_destination)

        # Successful atomic no-replace rename is the transaction commit point.
        committed = True

        # Failures from here forward are reported, but the committed final
        # destination is deliberately preserved for diagnosis and recovery.
        _fsync_directory(final_destination.parent)
        return verify_published_dataset(final_destination)

    finally:
        if not committed:
            _cleanup_uncommitted_stage(stage)
