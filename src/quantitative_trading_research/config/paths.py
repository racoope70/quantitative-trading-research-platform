"""Platform-neutral C4 path-resolution boundary.

Adapted from ``racoope70/ppo-trading-pipeline`` at immutable source commit
``072103f43d8b2488c3efca183f637ab0508a193a``, historical path ``src/paths.py``.

This module resolves repository-relative paths from an explicitly supplied base
directory. It performs no filesystem creation or mutation, including at import
time, and contains no provider, dataset, model, training, holdout, broker, or
execution-path semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike
from pathlib import Path


class PathConfigurationError(ValueError):
    """Fail-closed error for invalid path configuration."""


def _validated_base_path(base_path: str | PathLike[str]) -> Path:
    """Return an existing directory as an absolute, normalized base path."""
    if isinstance(base_path, str) and not base_path.strip():
        raise PathConfigurationError("base_path must not be empty")

    try:
        resolved = Path(base_path).expanduser().resolve(strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        raise PathConfigurationError(
            "base_path must identify an existing directory"
        ) from exc

    if not resolved.is_dir():
        raise PathConfigurationError("base_path must identify an existing directory")

    return resolved


@dataclass(frozen=True, init=False)
class ProjectPaths:
    """Resolve deterministic paths beneath an explicitly configured base."""

    base_path: Path

    def __init__(self, base_path: str | PathLike[str]) -> None:
        object.__setattr__(self, "base_path", _validated_base_path(base_path))

    @classmethod
    def from_base_path(cls, base_path: str | PathLike[str]) -> "ProjectPaths":
        """Create a resolver from an explicit existing base directory."""
        return cls(base_path)

    def resolve(self, *parts: str | PathLike[str]) -> Path:
        """Resolve relative path components beneath the configured base."""
        if not parts:
            return self.base_path

        normalized_parts: list[Path] = []
        for part in parts:
            candidate = Path(part)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise PathConfigurationError(
                    "resolved paths must remain relative to base_path"
                )
            normalized_parts.append(candidate)

        return self.base_path.joinpath(*normalized_parts)
