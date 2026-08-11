#!/usr/bin/env python3
"""C3 E1 successor V1 canonical JSON implementation.

Identity: C3_E1_SUCCESSOR_CANONICAL_JSON_V1

This module deliberately supports only the identity-bearing JSON domain
accepted for the successor V1 contract:
object, array, NFC-normalized string, bounded integer, boolean, and null.

Floating-point and exponent notation are prohibited.
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

CANONICALIZATION_IDENTITY = "C3_E1_SUCCESSOR_CANONICAL_JSON_V1"
NORMALIZATION_FORM = "NFC"
NORMALIZATION_PROVIDER = "python-unicodedata"
UNICODE_DATA_VERSION = unicodedata.unidata_version
EXPECTED_UNICODE_DATA_VERSION = "15.0.0"

if UNICODE_DATA_VERSION != EXPECTED_UNICODE_DATA_VERSION:
    raise RuntimeError(
        "C3_E1_SUCCESSOR_CANONICAL_JSON_V1 normalization database mismatch: "
        f"expected {EXPECTED_UNICODE_DATA_VERSION}, observed {UNICODE_DATA_VERSION}"
    )

_NAMED_CONTROL_ESCAPES = {
    0x08: r"\b",
    0x09: r"\t",
    0x0A: r"\n",
    0x0C: r"\f",
    0x0D: r"\r",
}


class CanonicalJSONError(ValueError):
    pass

INT64_MIN = -9223372036854775808
INT64_MAX = 9223372036854775807


def _validate_bounded_integer(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CanonicalJSONError("identity-domain integer required")
    if value < INT64_MIN or value > INT64_MAX:
        raise CanonicalJSONError(
            f"integer outside signed-int64 identity domain: {value}"
        )
    return value


def _reject_float(token: str) -> Any:
    raise CanonicalJSONError(
        f"floating-point/exponent token prohibited in identity domain: {token}"
    )


def _parse_int(token: str) -> int:
    # json's lexer already rejects +7 and 001. Enforce the remaining V1 rules.
    if token == "-0":
        return 0
    if token.startswith("+"):
        raise CanonicalJSONError("plus sign prohibited")
    if token.startswith("0") and token != "0":
        raise CanonicalJSONError("leading zero prohibited")
    if token.startswith("-0") and token != "-0":
        raise CanonicalJSONError("leading zero prohibited")
    return _validate_bounded_integer(int(token, 10))


def _validate_unicode_scalar_string(value: str) -> None:
    for ch in value:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise CanonicalJSONError("unpaired UTF-16 surrogate prohibited")


def _normalize_string(value: str) -> str:
    _validate_unicode_scalar_string(value)
    normalized = unicodedata.normalize(NORMALIZATION_FORM, value)
    _validate_unicode_scalar_string(normalized)
    return normalized


def _object_pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen_source: set[str] = set()
    seen_normalized: set[str] = set()
    out: dict[str, Any] = {}
    for raw_key, value in pairs:
        if raw_key in seen_source:
            raise CanonicalJSONError(f"duplicate object key prohibited: {raw_key!r}")
        seen_source.add(raw_key)
        key = _normalize_string(raw_key)
        if key in seen_normalized:
            raise CanonicalJSONError(
                f"distinct object keys collide after NFC normalization: {key!r}"
            )
        seen_normalized.add(key)
        out[key] = value
    return out


def loads_strict(text: str) -> Any:
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs_hook,
            parse_int=_parse_int,
            parse_float=_reject_float,
            parse_constant=lambda token: (_ for _ in ()).throw(
                CanonicalJSONError(f"non-finite token prohibited: {token}")
            ),
        )
    except UnicodeError as exc:
        raise CanonicalJSONError(f"invalid Unicode: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CanonicalJSONError(f"invalid JSON input: {exc}") from exc
    return _normalize_value(value)


def load_strict_bytes(data: bytes) -> Any:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise CanonicalJSONError(f"invalid UTF-8: {exc}") from exc
    if text.startswith("\ufeff"):
        raise CanonicalJSONError("UTF-8 BOM prohibited")
    return loads_strict(text)


def _normalize_value(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return _validate_bounded_integer(value)
    if isinstance(value, str):
        return _normalize_string(value)
    if isinstance(value, list):
        # Arrays are never reordered by the canonicalizer.
        return [_normalize_value(item) for item in value]
    if isinstance(value, dict):
        # Keys were normalized/collision-checked by strict parsing. This path
        # also supports programmatically constructed objects.
        out: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            if not isinstance(raw_key, str):
                raise CanonicalJSONError("JSON object key must be a string")
            key = _normalize_string(raw_key)
            if key in out:
                raise CanonicalJSONError(
                    f"object keys collide after NFC normalization: {key!r}"
                )
            out[key] = _normalize_value(raw_value)
        return out
    raise CanonicalJSONError(f"unsupported identity-domain type: {type(value).__name__}")


def _escape_string(value: str) -> str:
    value = _normalize_string(value)
    out = ['"']
    for ch in value:
        cp = ord(ch)
        if ch == '"':
            out.append(r"\"")
        elif ch == "\\":
            out.append(r"\\")
        elif cp in _NAMED_CONTROL_ESCAPES:
            out.append(_NAMED_CONTROL_ESCAPES[cp])
        elif 0x00 <= cp <= 0x1F:
            out.append(f"\\u{cp:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def dumps_canonical(value: Any) -> str:
    value = _normalize_value(value)
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        # Minimal base-10; -0 is impossible after parsing and int normalization.
        return str(value)
    if isinstance(value, str):
        return _escape_string(value)
    if isinstance(value, list):
        return "[" + ",".join(dumps_canonical(item) for item in value) + "]"
    if isinstance(value, dict):
        keys = sorted(value.keys())
        return "{" + ",".join(
            _escape_string(key) + ":" + dumps_canonical(value[key]) for key in keys
        ) + "}"
    raise CanonicalJSONError(f"unsupported type: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    return dumps_canonical(value).encode("utf-8", "strict")


def canonicalize_bytes(data: bytes) -> bytes:
    return canonical_bytes(load_strict_bytes(data))


def sha256_hex(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def self_test() -> dict[str, str]:
    tests: dict[str, str] = {}

    cases = [
        (b'{"b":2,"a":1}', b'{"a":1,"b":2}'),
        ('{"s":"e\\u0301"}'.encode(), '{"s":"é"}'.encode()),
        (b'{"i":-0,"t":true,"f":false,"n":null}', b'{"f":false,"i":0,"n":null,"t":true}'),
        (b'{"c":"\\b\\t\\n\\f\\r\\u0001"}', b'{"c":"\\b\\t\\n\\f\\r\\u0001"}'),
    ]
    for idx, (raw, expected) in enumerate(cases, 1):
        actual = canonicalize_bytes(raw)
        if actual != expected:
            raise AssertionError((idx, actual, expected))
    tests["byte_exact_positive_cases"] = "PASS"

    rejects = [
        b'{"a":1,"a":2}',
        '{"e\\u0301":1,"é":2}'.encode(),
        b'{"x":1.0}',
        b'{"x":1e3}',
        b'{"x":NaN}',
        b'\xef\xbb\xbf{"x":1}',
    ]
    for raw in rejects:
        try:
            canonicalize_bytes(raw)
        except CanonicalJSONError:
            continue
        raise AssertionError(f"expected rejection: {raw!r}")
    tests["strict_rejection_cases"] = "PASS"

    if canonical_bytes({"x": [3, 2, 1]}) != b'{"x":[3,2,1]}':
        raise AssertionError("array order was changed")
    tests["array_order_preserved"] = "PASS"

    if canonical_bytes({"x": -0}) != b'{"x":0}':
        raise AssertionError("negative zero not canonicalized")
    tests["integer_serialization"] = "PASS"

    for raw in (
        b'{"x":9223372036854775808}',
        b'{"x":-9223372036854775809}',
    ):
        try:
            canonicalize_bytes(raw)
        except CanonicalJSONError:
            continue
        raise AssertionError(f"out-of-range integer accepted: {raw!r}")
    try:
        canonical_bytes({"x": 9223372036854775808})
    except CanonicalJSONError:
        pass
    else:
        raise AssertionError("programmatic out-of-range integer accepted")
    tests["integer_bounds"] = "PASS"

    if canonical_bytes({"t": True, "f": False, "n": None}) != b'{"f":false,"n":null,"t":true}':
        raise AssertionError("boolean/null canonical tokens drift")
    tests["boolean_null_tokens"] = "PASS"

    if canonicalize_bytes('{"e\u0301":"A\u030A"}'.encode()) != '{"é":"Å"}'.encode():
        raise AssertionError("NFC normalization of keys/values drift")
    tests["nfc_keys_and_values"] = "PASS"
    if UNICODE_DATA_VERSION != EXPECTED_UNICODE_DATA_VERSION:
        raise AssertionError("Unicode normalization database identity drift")
    tests["unicode_data_version"] = UNICODE_DATA_VERSION
    return tests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return 0
    if not args.path:
        parser.error("path required unless --self-test")
    data = Path(args.path).read_bytes()
    sys.stdout.buffer.write(canonicalize_bytes(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
