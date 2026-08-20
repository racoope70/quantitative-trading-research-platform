"""Fail-closed canonical PPO configuration and authorization boundary.

Adapted from ``racoope70/ppo-trading-pipeline`` at immutable source commit
``072103f43d8b2488c3efca183f637ab0508a193a``, historical path
``src/ppo_v2_retraining_config.py``.

This C4 module is configuration-only. It does not define provider, dataset,
universe, feature, split, model-qualification, artifact-path, final-holdout-use,
broker, paper-trading, or live-trading behavior. It performs no filesystem,
network, training, or execution work.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json


SCHEMA_ID = "C4_PPO_CONFIGURATION_BOUNDARY_V1"
SCHEMA_VERSION = 1


class PPOConfigurationError(ValueError):
    """Fail-closed error for invalid canonical PPO configuration."""


@dataclass(frozen=True)
class PPOAuthorizationBoundary:
    """Explicit C4 authorization state; every operational capability is closed."""

    training_enabled: bool = False
    dataset_generation_enabled: bool = False
    model_artifact_creation_enabled: bool = False
    final_holdout_access_enabled: bool = False
    provider_operations_enabled: bool = False
    paper_order_submission_enabled: bool = False
    live_order_submission_enabled: bool = False

    def as_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class PPOConfiguration:
    """Versioned, deterministic, non-executing PPO configuration boundary."""

    schema_id: str = SCHEMA_ID
    schema_version: int = SCHEMA_VERSION
    authorization: PPOAuthorizationBoundary = field(
        default_factory=PPOAuthorizationBoundary
    )

    def canonical_payload(self) -> bytes:
        """Serialize the complete configuration deterministically."""
        return json.dumps(
            asdict(self),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def checksum_sha256(self) -> str:
        """Return the deterministic SHA-256 identity of this configuration."""
        return hashlib.sha256(self.canonical_payload()).hexdigest()

    def validate(self, expected_checksum: str | None = None) -> None:
        """Fail closed on schema, authorization, or expected-identity mismatch."""
        if self.schema_id != SCHEMA_ID:
            raise PPOConfigurationError("unsupported PPO configuration schema_id")

        if type(self.schema_version) is not int:
            raise PPOConfigurationError(
                "PPO configuration schema_version must be an int"
            )

        if self.schema_version != SCHEMA_VERSION:
            raise PPOConfigurationError(
                "unsupported PPO configuration schema_version"
            )

        if not isinstance(self.authorization, PPOAuthorizationBoundary):
            raise PPOConfigurationError(
                "authorization must be a PPOAuthorizationBoundary"
            )

        authorization_values = self.authorization.as_dict()

        malformed = sorted(
            name
            for name, value in authorization_values.items()
            if type(value) is not bool
        )
        if malformed:
            raise PPOConfigurationError(
                "PPO authorization capabilities must be bool: "
                + ", ".join(malformed)
            )

        enabled = sorted(
            name
            for name, value in authorization_values.items()
            if value
        )
        if enabled:
            raise PPOConfigurationError(
                "PPO operational authorization must remain fail closed: "
                + ", ".join(enabled)
            )

        if expected_checksum is not None:
            if not isinstance(expected_checksum, str):
                raise PPOConfigurationError(
                    "expected PPO configuration checksum must be a string"
                )

            normalized = expected_checksum.strip().lower()
            if len(normalized) != 64 or any(
                character not in "0123456789abcdef" for character in normalized
            ):
                raise PPOConfigurationError(
                    "expected PPO configuration checksum must be SHA-256 hex"
                )

            if self.checksum_sha256() != normalized:
                raise PPOConfigurationError(
                    "PPO configuration checksum mismatch"
                )


def build_default_ppo_configuration() -> PPOConfiguration:
    """Return the canonical fail-closed C4 PPO configuration."""
    configuration = PPOConfiguration()
    configuration.validate()
    return configuration
