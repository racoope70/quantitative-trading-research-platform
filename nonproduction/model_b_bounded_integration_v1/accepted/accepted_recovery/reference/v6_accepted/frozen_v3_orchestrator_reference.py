from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
import zipfile


STATE_MACHINE_VERSION = (
    "D1_BATCH0004_S04_S16_EXECUTABLE_ORCHESTRATION_V1"
)

IMPLEMENTATION_CONTRACT_VERSION = (
    "S04_S16_IMPLEMENTATION_CONTRACT_V1"
)

SEMANTIC_RULE_VERSION = (
    "D1_BODY_SEMANTIC_RULE_CLARIFIED_V2"
)

NORMALIZED_INTERFACE_VERSION = (
    "D1_BATCH_RECORD_NORMALIZED_INTERFACE_V2"
)

HASH_CHAIN_VERSION = (
    "D1_CUMULATIVE_HASH_CHAIN_SERIALIZATION_V1"
)

ALLOWED_DISPOSITIONS = {
    "BODY_CONFIRMED_CALENDAR_OR_SESSION_RELEVANT",
    "BODY_CONFIRMED_NONCALENDAR",
    "BODY_INACCESSIBLE_OR_UNRESOLVED",
}

STATE_SEQUENCE = [
    "S04_PRIMARY_INPUT_FREEZE",
    "S05_PRIMARY_SEMANTIC_ADJUDICATION",
    "S06_PRIMARY_LEDGER_FREEZE",
    "S07_INDEPENDENT_PACKAGE_CONSTRUCTION",
    "S08_INDEPENDENT_PACKAGE_FREEZE",
    "S09_INDEPENDENT_SEMANTIC_ADJUDICATION",
    "S10_INDEPENDENT_LEDGER_FREEZE",
    "S11_DETERMINISTIC_COMPARISON",
    "S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED",
    "S13_FINAL_BATCH_LEDGER_FREEZE",
    "S14_CUMULATIVE_ACCOUNTING",
    "S15_HASH_CHAIN",
    "S16_BATCH_COMPLETE_PENDING_MANAGING_REVIEW",
]

REQUIRED_TRANSITION_FIELDS = {
    "REQUIRED_INPUTS",
    "INPUT_HASH_VALIDATION",
    "EXECUTABLE_ACTION",
    "OUTPUT_ARTIFACTS",
    "OUTPUT_HASHES",
    "HARD_GATES",
    "FAIL_CLOSED_CONDITIONS",
    "NEXT_STATE",
    "STATE_TRANSITION_LOG_ENTRY",
}

CUMULATIVE_FIELDS = [
    "ACCEPTED_SOURCE_IDENTITY",
    "BATCH_ID",
    "BODY_CONTENT_AVAILABLE_FOR_INTERPRETATION",
    "BODY_DISPOSITION",
    "BODY_RETRIEVAL_STATUS",
    "BODY_SHA256",
    "CANONICAL_LOCATOR",
    "CONCISE_REVIEW_RATIONALE",
    "CUMULATIVE_POSITION",
    "EXTRACTED_BODY_SHA256",
    "IDENTITY_RECONCILIATION_STATUS",
    "NOTICE_CLASS",
    "REASON_CATEGORY",
    "REASON_CODE",
    "RECORD_ORDINAL_OR_ACCEPTED_RECORD_KEY",
    "SEMANTIC_ROW_REINTERPRETED",
    "SEMANTIC_RULE_VERSION",
    "SOURCE_ACCEPTED_LEDGER_CLASS",
    "SOURCE_ACCEPTED_LEDGER_SHA256",
    "SOURCE_BATCH_POSITION",
    "SOURCE_ROW_SHA256",
]


class ControlledStop(RuntimeError):
    pass


def stable_json(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_bytes(data):
    return hashlib.sha256(
        data
    ).hexdigest()


def sha256_text(text):
    return sha256_bytes(
        text.encode("utf-8")
    )


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def read_jsonl(path):
    rows = []

    with Path(path).open(
        "r",
        encoding="utf-8",
    ) as f:
        for line in f:
            if line.strip():
                rows.append(
                    json.loads(line)
                )

    return rows


def write_json_exclusive(path, obj):
    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(
            json.dumps(
                obj,
                sort_keys=True,
                indent=2,
                ensure_ascii=False,
            )
        )
        f.write("\n")
        f.flush()
        os.fsync(
            f.fileno()
        )

    return sha256_file(path)


def write_jsonl_exclusive(path, rows):
    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for row in rows:
            f.write(
                stable_json(row)
                + "\n"
            )

        f.flush()
        os.fsync(
            f.fileno()
        )

    return sha256_file(path)


def write_text_exclusive(path, text):
    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(text)
        f.flush()
        os.fsync(
            f.fileno()
        )

    return sha256_file(path)


def canonical_row_sha256(row):
    return sha256_text(
        stable_json(row)
        + "\n"
    )


def verify_expected_sha(path, expected, label):
    observed = sha256_file(
        path
    )

    if observed != expected:
        raise ControlledStop(
            label
            + "__SHA256_MISMATCH"
        )

    return observed


def require_exact_positions(
    rows,
    *,
    position_field,
    position_start,
    position_end,
):
    positions = [
        row[position_field]
        for row in rows
    ]

    expected = list(
        range(
            position_start,
            position_end + 1,
        )
    )

    if sorted(positions) != expected:
        raise ControlledStop(
            "POSITION_COVERAGE_FAILURE"
        )

    if len(set(positions)) != len(positions):
        raise ControlledStop(
            "DUPLICATE_POSITION_FAILURE"
        )


def require_unique_identities(
    rows,
    *,
    identity_field,
    expected_count,
):
    identities = [
        row[identity_field]
        for row in rows
    ]

    if len(rows) != expected_count:
        raise ControlledStop(
            "ROW_COUNT_FAILURE"
        )

    if len(set(identities)) != expected_count:
        raise ControlledStop(
            "IDENTITY_UNIQUENESS_FAILURE"
        )

    return set(identities)


def load_reason_contract(precedence_path):
    data = read_json(
        precedence_path
    )

    result = {}

    for disposition in ALLOWED_DISPOSITIONS:
        values = data.get(
            disposition
        )

        if not isinstance(
            values,
            list,
        ):
            raise ControlledStop(
                "REASON_PRECEDENCE_SCHEMA_FAILURE"
            )

        disposition_map = {}

        for item in values:
            code = item.get(
                "reason_code"
            )

            rank = item.get(
                "rank"
            )

            if (
                not isinstance(code, str)
                or not isinstance(rank, int)
            ):
                raise ControlledStop(
                    "REASON_PRECEDENCE_ENTRY_FAILURE"
                )

            disposition_map[
                code
            ] = {
                "rank":
                    rank,
                "category":
                    item.get(
                        "category"
                    ),
            }

        result[
            disposition
        ] = disposition_map

    return result


def reason_category(
    reason_contract,
    disposition,
    reason_code,
):
    return (
        reason_contract[
            disposition
        ][
            reason_code
        ].get(
            "category"
        )
    )


def validate_semantic_rows(
    semantic_rows,
    evidence_rows,
    reason_contract,
):
    expected_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in evidence_rows
    }

    if (
        len(semantic_rows)
        != len(evidence_rows)
    ):
        raise ControlledStop(
            "SEMANTIC_ROW_COUNT_FAILURE"
        )

    observed_ids = set()

    validated = []

    for row in semantic_rows:
        source_id = row.get(
            "canonical_source_identity"
        )

        if (
            source_id
            not in expected_by_id
        ):
            raise ControlledStop(
                "SEMANTIC_UNEXPECTED_IDENTITY"
            )

        if source_id in observed_ids:
            raise ControlledStop(
                "SEMANTIC_DUPLICATE_IDENTITY"
            )

        observed_ids.add(
            source_id
        )

        evidence = expected_by_id[
            source_id
        ]

        if (
            row.get(
                "authorized_population_position"
            )
            != evidence[
                "authorized_population_position"
            ]
        ):
            raise ControlledStop(
                "SEMANTIC_POSITION_MISMATCH"
            )

        disposition = row.get(
            "body_disposition"
        )

        reason_code = row.get(
            "reason_code"
        )

        rationale = row.get(
            "concise_review_rationale"
        )

        if disposition not in ALLOWED_DISPOSITIONS:
            raise ControlledStop(
                "INVALID_BODY_DISPOSITION"
            )

        if (
            reason_code
            not in reason_contract[
                disposition
            ]
        ):
            raise ControlledStop(
                "INVALID_REASON_CODE_FOR_DISPOSITION"
            )

        if (
            not isinstance(
                rationale,
                str,
            )
            or not rationale.strip()
        ):
            raise ControlledStop(
                "SEMANTIC_RATIONALE_MISSING"
            )

        if (
            evidence[
                "body_available"
            ]
            is False
            and (
                disposition
                != "BODY_INACCESSIBLE_OR_UNRESOLVED"
                or reason_code
                != "U1_AUTHORITATIVE_BODY_NOT_AVAILABLE"
            )
        ):
            raise ControlledStop(
                "UNAVAILABLE_BODY_SEMANTIC_INFERENCE_FAILURE"
            )

        validated.append({
            "canonical_source_identity":
                source_id,
            "authorized_population_position":
                evidence[
                    "authorized_population_position"
                ],
            "body_disposition":
                disposition,
            "reason_code":
                reason_code,
            "reason_category":
                reason_category(
                    reason_contract,
                    disposition,
                    reason_code,
                ),
            "concise_review_rationale":
                rationale.strip(),
        })

    if observed_ids != set(
        expected_by_id
    ):
        raise ControlledStop(
            "SEMANTIC_MISSING_IDENTITY"
        )

    return sorted(
        validated,
        key=lambda row:
            row[
                "authorized_population_position"
            ],
    )


def parse_json_agent_message(text):
    value = text.strip()

    if value.startswith(
        "```"
    ):
        lines = value.splitlines()

        if (
            lines
            and lines[0].startswith(
                "```"
            )
        ):
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip()
            == "```"
        ):
            lines = lines[:-1]

        value = "\n".join(
            lines
        ).strip()

    try:
        return json.loads(
            value
        )
    except json.JSONDecodeError as exc:
        raise ControlledStop(
            "SEMANTIC_EXECUTOR_JSON_PARSE_FAILURE"
        ) from exc


def parse_codex_json_events(stdout):
    thread_ids = []

    agent_messages = []

    for line in stdout.splitlines():
        if not line.strip():
            continue

        try:
            event = json.loads(
                line
            )
        except json.JSONDecodeError:
            continue

        if (
            event.get("type")
            == "thread.started"
            and isinstance(
                event.get(
                    "thread_id"
                ),
                str,
            )
        ):
            thread_ids.append(
                event[
                    "thread_id"
                ]
            )

        if (
            event.get("type")
            == "item.completed"
            and isinstance(
                event.get("item"),
                dict,
            )
            and event[
                "item"
            ].get(
                "type"
            )
            == "agent_message"
        ):
            message = event[
                "item"
            ].get(
                "text"
            )

            if isinstance(
                message,
                str,
            ):
                agent_messages.append(
                    message
                )

    if not thread_ids:
        raise ControlledStop(
            "SEMANTIC_EXECUTOR_CONTEXT_ID_MISSING"
        )

    if not agent_messages:
        raise ControlledStop(
            "SEMANTIC_EXECUTOR_FINAL_MESSAGE_MISSING"
        )

    return {
        "context_id":
            thread_ids[-1],
        "agent_message":
            agent_messages[-1],
    }


def executor_now_utc():
    return datetime.now(timezone.utc).isoformat()


def executor_error_indicated(payload):
    """Reject material top-level executor error/noncompletion indications."""
    if not isinstance(payload, dict):
        return True
    failure_keys = (
        "error", "errors", "failure", "failure_status", "noncompletion",
        "not_completed", "incomplete", "timeout", "timed_out",
    )
    for key in failure_keys:
        value = payload.get(key)
        if value is None or value is False or value == [] or value == {}:
            continue
        if isinstance(value, str) and value.strip().lower() in {
            "", "none", "null", "false", "no", "success", "completed"
        }:
            continue
        if value == 0:
            continue
        return True
    for key in ("status", "completion_status", "executor_status"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip().lower() in {
            "error", "failed", "failure", "incomplete", "partial",
            "noncompletion", "not_complete", "timed_out", "timeout",
            "cancelled", "canceled", "aborted"
        }:
            return True
    return False


def persist_executor_attempt(
    *, evidence_root, role, backend, command, working_directory,
    start_timestamp_utc, end_timestamp_utc, stdout, stderr,
    return_code, termination_state, timeout_status,
    context_id, final_message, failure_status,
):
    """Exclusive, fail-closed persistence of every executor attempt's raw evidence."""
    root = Path(evidence_root)
    root.mkdir(parents=True, exist_ok=True)
    prefix = role.lower()
    files = {
        "raw_stdout": root / (prefix + "_executor_raw_stdout.jsonl"),
        "raw_stderr": root / (prefix + "_executor_raw_stderr.txt"),
        "final_message": root / (prefix + "_executor_attempt_final_message.txt"),
    }
    hashes = {
        "raw_stdout": write_text_exclusive(files["raw_stdout"], stdout),
        "raw_stderr": write_text_exclusive(files["raw_stderr"], stderr),
        "final_message": write_text_exclusive(files["final_message"],
                                              final_message if final_message is not None else ""),
    }
    manifest = {
        "role": role,
        "backend": backend,
        "command": command,
        "working_directory": str(working_directory),
        "start_timestamp_utc": start_timestamp_utc,
        "end_timestamp_utc": end_timestamp_utc,
        "process_return_code": return_code,
        "process_termination_state": termination_state,
        "timeout_status": timeout_status,
        "execution_context_identity": context_id,
        "final_agent_message_present": final_message is not None,
        "failure_status": failure_status,
        "artifacts": {name: {"path": str(files[name]), "sha256": hashes[name]}
                      for name in files},
    }
    manifest_path = root / (prefix + "_executor_attempt_manifest.json")
    hashes["manifest"] = write_json_exclusive(manifest_path, manifest)
    files["manifest"] = manifest_path
    return {"paths": files, "hashes": hashes, "manifest": manifest}


def run_codex_executor(*, working_directory, prompt, codex_path,
                       evidence_root=None, role="PRIMARY"):
    command = [
        str(codex_path), "exec", "--ephemeral", "--ignore-user-config",
        "--ignore-rules", "--skip-git-repo-check", "--sandbox", "read-only",
        "--json", "-C", str(working_directory), prompt,
    ]
    stdout, stderr = "", ""
    return_code = None
    termination = "UNKNOWN"
    timeout = False
    context_id = None
    final_message = None
    failure = None
    began = executor_now_utc()
    try:
        try:
            result = subprocess.run(
                command, text=True, capture_output=True, check=False,
                timeout=3600,
                env={**os.environ, "PAGER": "cat", "GIT_PAGER": "cat"},
            )
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            return_code = result.returncode
            termination = "NORMAL_SUCCESS" if return_code == 0 else (
                "SIGNAL" if return_code < 0 else "ERROR")
        except subprocess.TimeoutExpired as exc:
            stdout = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            timeout = True
            termination = "TIMEOUT"
            failure = "SEMANTIC_EXECUTOR_TIMEOUT"
            raise ControlledStop(failure) from exc
        except OSError as exc:
            termination = "ERROR"
            failure = "SEMANTIC_EXECUTOR_START_FAILURE__" + type(exc).__name__
            raise ControlledStop(failure) from exc
        # Attempt to retain context/final message even if a nonzero return occurs.
        try:
            parsed = parse_codex_json_events(stdout)
            context_id = parsed["context_id"]
            final_message = parsed["agent_message"]
        except ControlledStop:
            if return_code == 0:
                raise
        if return_code != 0:
            failure = "SEMANTIC_EXECUTOR_NONZERO_RETURN"
            raise ControlledStop(failure)
        return {
            "backend": "codex_ephemeral", "context_id": context_id,
            "agent_message": final_message, "stdout": stdout, "stderr": stderr,
            "command": command, "working_directory": str(working_directory),
            "process_started": True, "return_code": return_code,
            "termination_state": termination, "timeout_status": timeout,
            "start_timestamp_utc": began,
        }
    except ControlledStop as exc:
        if not failure:
            failure = str(exc)
        raise
    finally:
        if evidence_root is not None:
            persist_executor_attempt(
                evidence_root=evidence_root, role=role,
                backend="codex_ephemeral", command=command,
                working_directory=working_directory,
                start_timestamp_utc=began, end_timestamp_utc=executor_now_utc(),
                stdout=stdout, stderr=stderr, return_code=return_code,
                termination_state=termination, timeout_status=timeout,
                context_id=context_id, final_message=final_message,
                failure_status=failure,
            )


def run_mock_executor(*, role, fixture_path, context_id,
                      working_directory=None, evidence_root=None):
    began = executor_now_utc()
    command = ["MOCK_FILE", role, str(fixture_path)]
    try:
        payload = read_json(fixture_path)
        message = stable_json(payload)
        if not isinstance(context_id, str) or not context_id:
            raise ControlledStop("SEMANTIC_EXECUTOR_CONTEXT_ID_MISSING")
        if evidence_root is not None:
            persist_executor_attempt(
                evidence_root=evidence_root, role=role, backend="mock_file",
                command=command, working_directory=working_directory or fixture_path.parent,
                start_timestamp_utc=began, end_timestamp_utc=executor_now_utc(),
                stdout="", stderr="", return_code=0,
                termination_state="NORMAL_SUCCESS", timeout_status=False,
                context_id=context_id, final_message=message, failure_status=None,
            )
        return {
            "backend": "mock_file", "context_id": context_id,
            "agent_message": message, "stdout": "", "stderr": "",
            "command": command, "working_directory": str(working_directory or fixture_path.parent),
            "process_started": True, "return_code": 0,
            "termination_state": "NORMAL_SUCCESS", "timeout_status": False,
            "start_timestamp_utc": began,
        }
    except Exception as exc:
        if evidence_root is not None:
            # A mock input failure is also preserved as an attempted execution.
            if not (Path(evidence_root) / (role.lower() + "_executor_attempt_manifest.json")).exists():
                persist_executor_attempt(
                    evidence_root=evidence_root, role=role, backend="mock_file",
                    command=command, working_directory=working_directory or fixture_path.parent,
                    start_timestamp_utc=began, end_timestamp_utc=executor_now_utc(),
                    stdout="", stderr="", return_code=None,
                    termination_state="ERROR", timeout_status=False,
                    context_id=context_id, final_message=None,
                    failure_status=type(exc).__name__ + ":" + str(exc),
                )
        raise


def execute_semantic_worker(ctx, *, role, working_directory, prompt):
    backend = ctx["config"]["semantic_executor"]["backend"]
    root = Path(ctx["run_root"]) / {
        "PRIMARY": "S05_PRIMARY_SEMANTIC_ADJUDICATION",
        "INDEPENDENT": "S09_INDEPENDENT_SEMANTIC_ADJUDICATION",
        "RECONCILIATION": "S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED",
    }[role]
    if backend == "mock_file":
        fixture_path = Path(ctx["config"]["semantic_executor"]["mock_outputs"][role])
        context_id = ctx["config"]["semantic_executor"]["mock_context_ids"][role]
        return run_mock_executor(role=role, fixture_path=fixture_path,
                                 context_id=context_id, working_directory=working_directory,
                                 evidence_root=root)
    if backend == "codex_ephemeral":
        codex_path = ctx["config"]["semantic_executor"].get("codex_path") or shutil.which("codex")
        if not codex_path:
            # Missing executable is an attempted-but-not-started execution.
            persist_executor_attempt(
                evidence_root=root, role=role, backend="codex_ephemeral",
                command=["codex", "exec"], working_directory=working_directory,
                start_timestamp_utc=executor_now_utc(), end_timestamp_utc=executor_now_utc(),
                stdout="", stderr="", return_code=None, termination_state="ERROR",
                timeout_status=False, context_id=None, final_message=None,
                failure_status="CODEX_EXECUTOR_UNAVAILABLE",
            )
            raise ControlledStop("CODEX_EXECUTOR_UNAVAILABLE")
        return run_codex_executor(working_directory=working_directory, prompt=prompt,
                                  codex_path=codex_path, evidence_root=root, role=role)
    raise ControlledStop("UNKNOWN_SEMANTIC_EXECUTOR_BACKEND")


def require_executor_success(result):
    if (result.get("process_started") is not True
        or result.get("return_code") != 0
        or result.get("termination_state") != "NORMAL_SUCCESS"
        or result.get("timeout_status") is not False
        or not isinstance(result.get("context_id"), str)
        or not result["context_id"]
        or not isinstance(result.get("agent_message"), str)
        or not result["agent_message"].strip()):
        raise ControlledStop("SEMANTIC_EXECUTOR_INCOMPLETE_OR_ABNORMAL")


def semantic_input_binding(ctx, *, independent=False):
    """Verify immutable S04 evidence, rule, and reason identity before adjudication PASS."""
    # Reuse the existing strict S04 source manifest/file-set/sha256 validator.
    # This also verifies every frozen BODY and HEADER before semantic PASS.
    trusted_s04_inputs(ctx)
    s04 = ctx["s04_paths"]
    manifest = read_json(s04["manifest"])
    required = {
        "neutral_semantic_evidence.jsonl": s04["evidence"],
        "semantic_rule_v2.json": s04["rule"],
        "reason_precedence_v2.json": s04["precedence"],
    }
    for label, path in required.items():
        if sha256_file(path) != manifest["file_hashes"][label]:
            raise ControlledStop("S04_INPUT_BINDING_HASH_MISMATCH__" + label)
    source_transitions = [row for row in load_transition_log(ctx)
                          if row.get("STATE") == "S04_PRIMARY_INPUT_FREEZE"]
    if len(source_transitions) != 1 or source_transitions[0].get("STATUS") != "PASS":
        raise ControlledStop("S04_FROZEN_TRANSITION_UNAVAILABLE")
    bound = source_transitions[0].get("OUTPUT_HASHES", {})
    if (sha256_file(s04["manifest"]) != bound.get("manifest")
        or sha256_file(s04["evidence"]) != bound.get("evidence")
        or sha256_file(s04["sha256sums"]) != bound.get("sha256sums")):
        raise ControlledStop("S04_FROZEN_TRANSITION_IDENTITY_MISMATCH")
    if len(ctx["s04_evidence_rows"]) != 500 or len({
            row["canonical_source_identity"] for row in ctx["s04_evidence_rows"]}) != 500:
        raise ControlledStop("S04_EVIDENCE_COUNT_OR_IDENTITY_FAILURE")
    manifest_sources = manifest.get("source_hashes", {})
    expected = ctx["config"].get("expected_hashes", {})
    for key, label in (("semantic_rule", "semantic_rule_v2.json"),
                       ("reason_precedence", "reason_precedence_v2.json")):
        if (manifest_sources.get(key) != manifest["file_hashes"][label]
            or (key in expected and manifest_sources.get(key) != expected[key])):
            raise ControlledStop("S04_SOURCE_RULE_BINDING_MISMATCH__" + key)
    if ctx["config"].get("execution_mode") == "REAL_BATCH0004":
        if manifest_sources.get("semantic_rule") != "a424085098e871e7f555b29caf3641c5317ac581c9130ba28971385f98aa4fa3":
            raise ControlledStop("SEMANTIC_RULE_IDENTITY_MISMATCH")
        if manifest_sources.get("reason_precedence") != "57a7827a23b4c7aa47c19ad950b59871dcff7301addf84f7a2fca580a90f9445":
            raise ControlledStop("REASON_PRECEDENCE_IDENTITY_MISMATCH")
    if independent:
        package_root = ctx["s08_paths"]["root"]
        for name, s04_path in required.items():
            if sha256_file(package_root / name) != sha256_file(s04_path):
                raise ControlledStop("INDEPENDENT_NEUTRAL_INPUT_BINDING_FAILURE")
    return sha256_file(s04["manifest"])


def validate_complete_semantic_result(ctx, result, *, role, independent=False):
    require_executor_success(result)
    payload = parse_json_agent_message(result["agent_message"])
    if not isinstance(payload, dict) or "rows" not in payload or not isinstance(payload["rows"], list):
        raise ControlledStop("SEMANTIC_OUTPUT_ROWS_MISSING_OR_INVALID")
    if executor_error_indicated(payload):
        raise ControlledStop("SEMANTIC_EXECUTOR_EXPLICIT_NONCOMPLETION")
    if len(payload["rows"]) != 500:
        raise ControlledStop("SEMANTIC_ROW_COUNT_FAILURE")
    if not all(isinstance(item, dict) for item in payload["rows"]):
        raise ControlledStop("SEMANTIC_ROW_STRUCTURE_FAILURE")
    input_identity = semantic_input_binding(ctx, independent=independent)
    reason_contract = load_reason_contract(ctx["s04_paths"]["precedence"])
    validated = validate_semantic_rows(payload["rows"], ctx["s04_evidence_rows"], reason_contract)
    # Require exactly the authorized position domain in addition to validator alignment.
    require_exact_positions(validated, position_field="authorized_population_position",
                            position_start=1501, position_end=2000)
    if len({row["canonical_source_identity"] for row in validated}) != 500:
        raise ControlledStop("SEMANTIC_IDENTITY_COUNT_FAILURE")
    return payload["rows"], validated, input_identity


def write_and_verify_semantic_candidate(ctx, *, path, raw_rows, validated, independent=False):
    try:
        candidate_sha = write_jsonl_exclusive(path, raw_rows)
        if not Path(path).stat().st_size:
            raise ControlledStop("SEMANTIC_CANDIDATE_EMPTY_AFTER_SERIALIZATION")
        if sha256_file(path) != candidate_sha:
            raise ControlledStop("SEMANTIC_CANDIDATE_WRITE_HASH_FAILURE")
        reread = read_jsonl(path)
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        raise ControlledStop("SEMANTIC_CANDIDATE_SERIALIZATION_READBACK_FAILURE") from exc
    if len(reread) != 500:
        raise ControlledStop("SEMANTIC_CANDIDATE_READBACK_COUNT_FAILURE")
    reason_contract = load_reason_contract(ctx["s04_paths"]["precedence"])
    checked = validate_semantic_rows(reread, ctx["s04_evidence_rows"], reason_contract)
    require_exact_positions(checked, position_field="authorized_population_position",
                            position_start=1501, position_end=2000)
    if checked != validated:
        raise ControlledStop("SEMANTIC_CANDIDATE_READBACK_IDENTITY_FAILURE")
    semantic_input_binding(ctx, independent=independent)
    return candidate_sha

def deterministic_zip(
    *,
    root,
    relative_files,
    zip_path,
):
    root = Path(root)
    zip_path = Path(
        zip_path
    )

    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with zipfile.ZipFile(
        zip_path,
        "x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zf:
        for rel in sorted(
            relative_files
        ):
            source = (
                root
                / rel
            )

            data = source.read_bytes()

            info = zipfile.ZipInfo(
                str(rel).replace(
                    os.sep,
                    "/",
                )
            )

            info.date_time = (
                1980,
                1,
                1,
                0,
                0,
                0,
            )

            info.compress_type = (
                zipfile.ZIP_DEFLATED
            )

            info.external_attr = (
                0o100644
                << 16
            )

            zf.writestr(
                info,
                data,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )

    return sha256_file(
        zip_path
    )


def transition_log_path(ctx):
    return (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "state_transition_log.jsonl"
    )


def load_transition_log(ctx):
    path = transition_log_path(
        ctx
    )

    if not path.exists():
        return []

    return read_jsonl(
        path
    )


def append_transition(
    ctx,
    *,
    state,
    required_inputs,
    executable_action,
    output_artifacts,
    output_hashes,
    hard_gates,
    fail_closed_conditions,
    next_state,
):
    prior = load_transition_log(
        ctx
    )

    if prior:
        previous = prior[-1]

        if previous.get(
            "STATUS"
        ) != "PASS":
            raise ControlledStop(
                "PREVIOUS_STATE_NOT_PASS"
            )

    entry = {
        "STATE":
            state,
        "STATUS":
            "PASS",
        "REQUIRED_INPUTS":
            required_inputs,
        "INPUT_HASH_VALIDATION":
            "PASS",
        "EXECUTABLE_ACTION":
            executable_action,
        "OUTPUT_ARTIFACTS":
            output_artifacts,
        "OUTPUT_HASHES":
            output_hashes,
        "HARD_GATES":
            hard_gates,
        "FAIL_CLOSED_CONDITIONS":
            fail_closed_conditions,
        "NEXT_STATE":
            next_state,
        "STATE_TRANSITION_LOG_ENTRY":
            "PASS",
    }

    if not REQUIRED_TRANSITION_FIELDS.issubset(
        entry
    ):
        raise ControlledStop(
            "TRANSITION_CONTRACT_FIELD_FAILURE"
        )

    path = transition_log_path(
        ctx
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "a",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(
            stable_json(
                entry
            )
            + "\n"
        )

        f.flush()
        os.fsync(
            f.fileno()
        )

    return entry


def s04_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S04_PRIMARY_INPUT_FREEZE"
    )

    return {
        "root":
            root,
        "evidence":
            root
            / "neutral_semantic_evidence.jsonl",
        "rule":
            root
            / "semantic_rule_v2.json",
        "precedence":
            root
            / "reason_precedence_v2.json",
        "bodies":
            root
            / "bodies",
        "manifest":
            root
            / "s04_primary_input_manifest.json",
        "sha256sums":
            root
            / "SHA256SUMS.txt",
    }


def run_s04(ctx):
    cfg = ctx[
        "config"
    ]

    inputs = cfg[
        "paths"
    ]

    expected = cfg[
        "expected_hashes"
    ]

    population_path = Path(
        inputs[
            "accepted_population"
        ]
    )

    retrieval_path = Path(
        inputs[
            "s02_retrieval_ledger"
        ]
    )

    s03_validation_path = Path(
        inputs[
            "s03_validation_ledger"
        ]
    )

    rule_path = Path(
        inputs[
            "semantic_rule"
        ]
    )

    precedence_path = Path(
        inputs[
            "reason_precedence"
        ]
    )

    body_root = Path(
        inputs[
            "body_root"
        ]
    )

    verify_expected_sha(
        population_path,
        expected[
            "accepted_population"
        ],
        "S04_ACCEPTED_POPULATION",
    )

    verify_expected_sha(
        retrieval_path,
        expected[
            "s02_retrieval_ledger"
        ],
        "S04_RETRIEVAL_LEDGER",
    )

    verify_expected_sha(
        s03_validation_path,
        expected[
            "s03_validation_ledger"
        ],
        "S04_S03_VALIDATION_LEDGER",
    )

    verify_expected_sha(
        rule_path,
        expected[
            "semantic_rule"
        ],
        "S04_SEMANTIC_RULE",
    )

    verify_expected_sha(
        precedence_path,
        expected[
            "reason_precedence"
        ],
        "S04_REASON_PRECEDENCE",
    )

    population = read_jsonl(
        population_path
    )

    retrieval = read_jsonl(
        retrieval_path
    )

    s03_validation = read_jsonl(
        s03_validation_path
    )

    expected_count = cfg[
        "expected_record_count"
    ]

    position_start = cfg[
        "position_start"
    ]

    position_end = cfg[
        "position_end"
    ]

    require_unique_identities(
        population,
        identity_field="source_identity",
        expected_count=expected_count,
    )

    require_exact_positions(
        population,
        position_field="authorized_population_position",
        position_start=position_start,
        position_end=position_end,
    )

    require_unique_identities(
        retrieval,
        identity_field="accepted_source_identity",
        expected_count=expected_count,
    )

    require_exact_positions(
        retrieval,
        position_field="authorized_population_position",
        position_start=position_start,
        position_end=position_end,
    )

    require_unique_identities(
        s03_validation,
        identity_field="canonical_source_identity",
        expected_count=expected_count,
    )

    require_exact_positions(
        s03_validation,
        position_field="authorized_population_position",
        position_start=position_start,
        position_end=position_end,
    )

    population_by_id = {
        row[
            "source_identity"
        ]:
            row
        for row in population
    }

    retrieval_by_id = {
        row[
            "accepted_source_identity"
        ]:
            row
        for row in retrieval
    }

    validation_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in s03_validation
    }

    if (
        set(population_by_id)
        != set(retrieval_by_id)
        or set(population_by_id)
        != set(validation_by_id)
    ):
        raise ControlledStop(
            "S04_IDENTITY_ALIGNMENT_FAILURE"
        )

    paths = s04_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    paths[
        "bodies"
    ].mkdir()

    shutil.copyfile(
        rule_path,
        paths[
            "rule"
        ],
    )

    shutil.copyfile(
        precedence_path,
        paths[
            "precedence"
        ],
    )

    evidence_rows = []

    copied_members = [
        Path(
            paths[
                "rule"
            ].name
        ),
        Path(
            paths[
                "precedence"
            ].name
        ),
    ]

    for source_id in sorted(
        population_by_id,
        key=lambda sid:
            population_by_id[
                sid
            ][
                "authorized_population_position"
            ],
    ):
        pop = population_by_id[
            source_id
        ]

        ret = retrieval_by_id[
            source_id
        ]

        val = validation_by_id[
            source_id
        ]

        position = pop[
            "authorized_population_position"
        ]

        if (
            ret[
                "authorized_population_position"
            ]
            != position
            or val[
                "authorized_population_position"
            ]
            != position
        ):
            raise ControlledStop(
                "S04_POSITION_ALIGNMENT_FAILURE"
            )

        mandatory_s03_true = [
            "normalized_interface_identity_match",
            "record_metadata_exact_match",
            "body_manifest_ledger_match",
            "sha256sums_record_targets_verified",
            "body_sha256_verified",
            "response_headers_sha256_verified",
            "extracted_body_sha256_verified",
            "extracted_header_sha256_verified",
            "challenge_classification_matches_frozen_retrieval",
        ]

        for field in mandatory_s03_true:
            if val.get(
                field
            ) is not True:
                raise ControlledStop(
                    "S04_S03_HARD_GATE_FAILURE__"
                    + field
                )

        body_available = bool(
            ret[
                "body_content_available_for_interpretation"
            ]
        )

        body_member = None

        header_member = None

        if body_available:
            body_source = (
                body_root
                / ret[
                    "relative_extracted_body_path"
                ]
            )

            header_source = (
                body_root
                / ret[
                    "relative_extracted_header_path"
                ]
            )

            if (
                not body_source.is_file()
                or not header_source.is_file()
            ):
                raise ControlledStop(
                    "S04_AUTHORITATIVE_EVIDENCE_FILE_MISSING"
                )

            if (
                sha256_file(
                    body_source
                )
                != ret[
                    "extracted_body_sha256"
                ]
            ):
                raise ControlledStop(
                    "S04_EXTRACTED_BODY_HASH_FAILURE"
                )

            if (
                sha256_file(
                    header_source
                )
                != ret[
                    "extracted_header_sha256"
                ]
            ):
                raise ControlledStop(
                    "S04_EXTRACTED_HEADER_HASH_FAILURE"
                )

            body_member = (
                Path("bodies")
                / (
                    f"{position:06d}_"
                    f"{source_id[:12]}_body.txt"
                )
            )

            header_member = (
                Path("bodies")
                / (
                    f"{position:06d}_"
                    f"{source_id[:12]}_header.txt"
                )
            )

            shutil.copyfile(
                body_source,
                paths[
                    "root"
                ]
                / body_member,
            )

            shutil.copyfile(
                header_source,
                paths[
                    "root"
                ]
                / header_member,
            )

            copied_members.extend([
                body_member,
                header_member,
            ])

        evidence_rows.append({
            "schema_version":
                NORMALIZED_INTERFACE_VERSION,
            "batch_id":
                cfg[
                    "batch_id"
                ],
            "canonical_source_identity":
                source_id,
            "authorized_population_position":
                position,
            "record_ordinal":
                pop[
                    "record_ordinal"
                ],
            "metadata_ledger_position":
                pop[
                    "metadata_ledger_position"
                ],
            "notice_class":
                pop[
                    "notice_class"
                ],
            "accepted_record":
                pop[
                    "record"
                ],
            "canonical_locator":
                ret[
                    "canonical_locator"
                ],
            "retrieval_status":
                ret[
                    "body_retrieval_status"
                ],
            "body_available":
                body_available,
            "body_sha256":
                ret[
                    "body_sha256"
                ],
            "extracted_body_sha256":
                ret[
                    "extracted_body_sha256"
                ],
            "extracted_header_sha256":
                ret[
                    "extracted_header_sha256"
                ],
            "identity_reconciliation_status":
                ret[
                    "identity_reconciliation_status"
                ],
            "valid_extraction":
                ret[
                    "valid_extraction"
                ],
            "body_evidence_member":
                (
                    str(body_member)
                    if body_member
                    else None
                ),
            "header_evidence_member":
                (
                    str(header_member)
                    if header_member
                    else None
                ),
            "s03_validation":
                val,
        })

    evidence_sha = write_jsonl_exclusive(
        paths[
            "evidence"
        ],
        evidence_rows,
    )

    copied_members.append(
        Path(
            paths[
                "evidence"
            ].name
        )
    )

    file_hashes = {}

    for rel in sorted(
        copied_members,
        key=lambda p:
            str(p),
    ):
        file_hashes[
            str(rel)
        ] = sha256_file(
            paths[
                "root"
            ]
            / rel
        )

    manifest = {
        "artifact_id":
            "BATCH0004_S04_PRIMARY_INPUT_FREEZE",
        "state_machine_version":
            STATE_MACHINE_VERSION,
        "batch_id":
            cfg[
                "batch_id"
            ],
        "position_start":
            position_start,
        "position_end":
            position_end,
        "row_count":
            len(
                evidence_rows
            ),
        "unique_source_identities":
            len({
                row[
                    "canonical_source_identity"
                ]
                for row in evidence_rows
            }),
        "semantic_answers_present":
            False,
        "canonical_order":
            "AUTHORIZED_POPULATION_POSITION_ASCENDING",
        "file_hashes":
            file_hashes,
        "source_hashes": {
            "accepted_population":
                expected[
                    "accepted_population"
                ],
            "s02_retrieval_ledger":
                expected[
                    "s02_retrieval_ledger"
                ],
            "s03_validation_ledger":
                expected[
                    "s03_validation_ledger"
                ],
            "semantic_rule":
                expected[
                    "semantic_rule"
                ],
            "reason_precedence":
                expected[
                    "reason_precedence"
                ],
        },
    }

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        manifest,
    )

    checksum_lines = []

    checksum_targets = [
        paths[
            "evidence"
        ],
        paths[
            "rule"
        ],
        paths[
            "precedence"
        ],
        *[
            paths[
                "root"
            ]
            / rel
            for rel in copied_members
            if str(rel).startswith(
                "bodies/"
            )
        ],
        paths[
            "manifest"
        ],
    ]

    for target in sorted(
        set(
            checksum_targets
        ),
        key=lambda p:
            str(
                p.relative_to(
                    paths[
                        "root"
                    ]
                )
            ),
    ):
        checksum_lines.append(
            sha256_file(
                target
            )
            + "  "
            + str(
                target.relative_to(
                    paths[
                        "root"
                    ]
                )
            )
        )

    sums_sha = write_text_exclusive(
        paths[
            "sha256sums"
        ],
        "\n".join(
            checksum_lines
        )
        + "\n",
    )

    append_transition(
        ctx,
        state="S04_PRIMARY_INPUT_FREEZE",
        required_inputs=[
            str(
                population_path
            ),
            str(
                retrieval_path
            ),
            str(
                s03_validation_path
            ),
            str(
                rule_path
            ),
            str(
                precedence_path
            ),
        ],
        executable_action=(
            "Constructed deterministic neutral "
            "Primary semantic-input freeze."
        ),
        output_artifacts=[
            str(
                paths[
                    "evidence"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
            str(
                paths[
                    "sha256sums"
                ]
            ),
        ],
        output_hashes={
            "evidence":
                evidence_sha,
            "manifest":
                manifest_sha,
            "sha256sums":
                sums_sha,
        },
        hard_gates={
            "row_count":
                "PASS",
            "identity_alignment":
                "PASS",
            "position_alignment":
                "PASS",
            "s03_validation":
                "PASS",
            "body_hash_validation":
                "PASS",
            "semantic_answers_absent":
                "PASS",
        },
        fail_closed_conditions=[
            "INPUT_HASH_MISMATCH",
            "ROW_COUNT_FAILURE",
            "IDENTITY_ALIGNMENT_FAILURE",
            "POSITION_ALIGNMENT_FAILURE",
            "S03_HARD_GATE_FAILURE",
            "AUTHORITATIVE_EVIDENCE_HASH_FAILURE",
        ],
        next_state=(
            "S05_PRIMARY_SEMANTIC_ADJUDICATION"
        ),
    )

    ctx[
        "s04_evidence_rows"
    ] = evidence_rows

    ctx[
        "s04_paths"
    ] = paths

    return paths


def semantic_prompt(
    *,
    role,
    evidence_filename,
):
    if role == "PRIMARY":
        role_text = (
            "You are the isolated Primary semantic adjudicator."
        )
    elif role == "INDEPENDENT":
        role_text = (
            "You are the fresh isolated Independent "
            "semantic adjudicator."
        )
    else:
        raise ControlledStop(
            "UNKNOWN_SEMANTIC_ROLE"
        )

    return (
        role_text
        + "\n"
        + "Review every row in "
        + evidence_filename
        + " using ONLY the files in this working directory. "
        + "For each row with an available authoritative body, "
        + "read the complete referenced body and header evidence. "
        + "Apply semantic_rule_v2.json and reason_precedence_v2.json. "
        + "Do not infer from headline alone, metadata alone, keywords, "
        + "prior answers, expected totals, or other unavailable context. "
        + "For unavailable evidence use BODY_INACCESSIBLE_OR_UNRESOLVED "
        + "with U1_AUTHORITATIVE_BODY_NOT_AVAILABLE. "
        + "Return ONLY valid JSON with shape "
        + '{"rows":[{"canonical_source_identity":"...",'
        + '"authorized_population_position":1,'
        + '"body_disposition":"...",'
        + '"reason_code":"...",'
        + '"concise_review_rationale":"..."}]}. '
        + "Return exactly one row for every evidence row."
    )


def s05_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S05_PRIMARY_SEMANTIC_ADJUDICATION"
    )

    return {
        "root":
            root,
        "candidate":
            root
            / "primary_semantic_candidate.jsonl",
        "executor_manifest":
            root
            / "primary_executor_manifest.json",
        "raw_message":
            root
            / "primary_executor_final_message.txt",
        "attempt_manifest": root / "primary_executor_attempt_manifest.json",
    }


def run_s05(ctx):
    s04 = ctx["s04_paths"]
    paths = s05_paths(ctx)
    paths["root"].mkdir(parents=True, exist_ok=False)
    # Preserve executor evidence even if the subprocess fails before producing a candidate.
    result = execute_semantic_worker(
        ctx, role="PRIMARY", working_directory=s04["root"],
        prompt=semantic_prompt(role="PRIMARY", evidence_filename=s04["evidence"].name),
    )
    raw_rows, validated, s04_manifest_sha = validate_complete_semantic_result(
        ctx, result, role="PRIMARY")
    candidate_sha = write_and_verify_semantic_candidate(
        ctx, path=paths["candidate"], raw_rows=raw_rows, validated=validated)
    raw_sha = write_text_exclusive(paths["raw_message"], result["agent_message"] + "\n")
    attempt_sha = sha256_file(paths["attempt_manifest"])
    executor_manifest = {
        "role": "PRIMARY_SEMANTIC_EXECUTOR", "backend": result["backend"],
        "execution_context_identity": result["context_id"],
        "input_manifest_identity": s04_manifest_sha,
        "input_evidence_identity": sha256_file(s04["evidence"]),
        "semantic_rule_identity": sha256_file(s04["rule"]),
        "reason_precedence_identity": sha256_file(s04["precedence"]),
        "candidate_output_identity": candidate_sha,
        "candidate_row_count": 500,
        "raw_message_sha256": raw_sha,
        "executor_attempt_manifest_sha256": attempt_sha,
        "start_state": "S05_PRIMARY_SEMANTIC_ADJUDICATION",
        "end_state": "S05_PRIMARY_SEMANTIC_ADJUDICATION",
        "failure_status": None, "command": result["command"],
    }
    executor_sha = write_json_exclusive(paths["executor_manifest"], executor_manifest)
    append_transition(
        ctx, state="S05_PRIMARY_SEMANTIC_ADJUDICATION",
        required_inputs=[str(s04["manifest"]), str(s04["evidence"])],
        executable_action="Executed isolated Primary semantic executor; validated complete output and serialized readback before PASS.",
        output_artifacts=[str(paths["candidate"]), str(paths["executor_manifest"]), str(paths["attempt_manifest"])],
        output_hashes={"candidate": candidate_sha, "executor_manifest": executor_sha,
                       "raw_message": raw_sha, "executor_attempt_manifest": attempt_sha},
        hard_gates={"executor_return": "PASS", "context_identity_exposed": "PASS",
                    "candidate_json_parse": "PASS", "complete_500_row_semantics": "PASS",
                    "exact_identity_position_binding": "PASS", "reason_contract": "PASS",
                    "s04_input_binding": "PASS", "candidate_readback": "PASS"},
        fail_closed_conditions=["EXECUTOR_FAILURE", "EXPLICIT_NONCOMPLETION",
                                "INCOMPLETE_SEMANTIC_ROWS", "INPUT_IDENTITY_MISMATCH",
                                "SERIALIZATION_OR_READBACK_FAILURE"],
        next_state="S06_PRIMARY_LEDGER_FREEZE",
    )
    ctx["primary_context_id"] = result["context_id"]
    ctx["s05_paths"] = paths
    return paths

def s06_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S06_PRIMARY_LEDGER_FREEZE"
    )

    return {
        "root":
            root,
        "ledger":
            root
            / "primary_semantic_ledger.jsonl",
        "manifest":
            root
            / "primary_freeze_manifest.json",
    }


def run_s06(ctx):
    paths = s06_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    evidence_rows = ctx[
        "s04_evidence_rows"
    ]

    candidate_rows = read_jsonl(
        ctx[
            "s05_paths"
        ][
            "candidate"
        ]
    )

    reason_contract = load_reason_contract(
        ctx[
            "s04_paths"
        ][
            "precedence"
        ]
    )

    validated = validate_semantic_rows(
        candidate_rows,
        evidence_rows,
        reason_contract,
    )

    ledger_sha = write_jsonl_exclusive(
        paths[
            "ledger"
        ],
        validated,
    )

    manifest = {
        "artifact_id":
            "BATCH0004_PRIMARY_LEDGER_FREEZE",
        "row_count":
            len(
                validated
            ),
        "unique_source_identities":
            len({
                row[
                    "canonical_source_identity"
                ]
                for row in validated
            }),
        "position_start":
            validated[
                0
            ][
                "authorized_population_position"
            ],
        "position_end":
            validated[
                -1
            ][
                "authorized_population_position"
            ],
        "ledger_sha256":
            ledger_sha,
        "primary_context_id":
            ctx[
                "primary_context_id"
            ],
        "frozen":
            True,
    }

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        manifest,
    )

    os.chmod(
        paths[
            "ledger"
        ],
        0o444,
    )

    os.chmod(
        paths[
            "manifest"
        ],
        0o444,
    )

    ctx[
        "primary_ledger_sha256"
    ] = ledger_sha

    append_transition(
        ctx,
        state="S06_PRIMARY_LEDGER_FREEZE",
        required_inputs=[
            str(
                ctx[
                    "s05_paths"
                ][
                    "candidate"
                ]
            ),
        ],
        executable_action=(
            "Validated complete Primary semantic output "
            "and froze immutable Primary ledger."
        ),
        output_artifacts=[
            str(
                paths[
                    "ledger"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "ledger":
                ledger_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "row_count":
                "PASS",
            "unique_identities":
                "PASS",
            "position_coverage":
                "PASS",
            "reason_contract":
                "PASS",
            "freeze":
                "PASS",
        },
        fail_closed_conditions=[
            "PRIMARY_INCOMPLETE_OUTPUT",
            "PRIMARY_DUPLICATE_IDENTITY",
            "INVALID_DISPOSITION",
            "INVALID_REASON_CODE",
            "POST_FREEZE_MUTATION",
        ],
        next_state=(
            "S07_INDEPENDENT_PACKAGE_CONSTRUCTION"
        ),
    )

    ctx[
        "s06_paths"
    ] = paths

    return paths


def s07_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S07_INDEPENDENT_PACKAGE_CONSTRUCTION"
    )

    return {
        "root":
            root,
        "manifest":
            root
            / "independent_package_construction_manifest.json",
    }



# Batch 0004 recovery v2: reject malformed, off-schema, untrusted or leaked
# Independent inputs; PIN source hashes to the already-frozen S04 transition.
from firewall_v2 import (
    TrustedInputs, FirewallViolation,
    scan_independent_package as _strict_independent_scan,
    validate_frozen_zip as _strict_validate_frozen_zip,
)


def trusted_s04_inputs(ctx):
    source = ctx["s04_paths"]
    manifest_path = source["manifest"]
    transition_rows = load_transition_log(ctx)
    s04 = [row for row in transition_rows if row.get("STATE") == "S04_PRIMARY_INPUT_FREEZE"]
    if len(s04) != 1 or s04[0].get("STATUS") != "PASS":
        raise ControlledStop("S04_FROZEN_TRANSITION_MISSING_OR_AMBIGUOUS")
    hashes = s04[0].get("OUTPUT_HASHES", {})
    if sha256_file(manifest_path) != hashes.get("manifest") or \
       sha256_file(source["evidence"]) != hashes.get("evidence") or \
       sha256_file(source["sha256sums"]) != hashes.get("sha256sums"):
        raise ControlledStop("S04_TRANSITION_IDENTITY_MISMATCH")
    manifest = read_json(manifest_path)
    expected_keys = {
        "artifact_id", "state_machine_version", "batch_id", "position_start",
        "position_end", "row_count", "unique_source_identities",
        "semantic_answers_present", "canonical_order", "file_hashes", "source_hashes",
    }
    if set(manifest) != expected_keys or \
       manifest["artifact_id"] != "BATCH0004_S04_PRIMARY_INPUT_FREEZE" or \
       manifest["batch_id"] != "BATCH_0004" or \
       manifest["position_start"] != 1501 or manifest["position_end"] != 2000 or \
       manifest["row_count"] != 500 or manifest["unique_source_identities"] != 500 or \
       manifest["semantic_answers_present"] is not False or \
       manifest["canonical_order"] != "AUTHORIZED_POPULATION_POSITION_ASCENDING":
        raise ControlledStop("S04_MANIFEST_SCHEMA_OR_IDENTITY_MISMATCH")
    file_hashes = manifest["file_hashes"]
    if not isinstance(file_hashes, dict):
        raise ControlledStop("S04_FILE_HASHES_INVALID")
    paths = source["root"]
    source_files = {p.relative_to(paths).as_posix() for p in paths.rglob("*") if p.is_file()}
    if source_files != set(file_hashes) | {"s04_primary_input_manifest.json", "SHA256SUMS.txt"}:
        raise ControlledStop("S04_FROZEN_SOURCE_FILE_SET_MISMATCH")
    for rel, digest in file_hashes.items():
        if not isinstance(rel, str) or "/../" in rel or rel.startswith("/") or "\\" in rel:
            raise ControlledStop("S04_SOURCE_PATH_INVALID")
        if sha256_file(paths / rel) != digest:
            raise ControlledStop("S04_FROZEN_SOURCE_SHA_MISMATCH")
    if manifest["source_hashes"].get("semantic_rule") != \
       ctx["config"]["expected_hashes"]["semantic_rule"] or \
       manifest["source_hashes"].get("reason_precedence") != \
       ctx["config"]["expected_hashes"]["reason_precedence"]:
        raise ControlledStop("S04_SOURCE_PROVENANCE_MISMATCH")
    return TrustedInputs(
        s04_manifest_sha256=hashes["manifest"],
        neutral_evidence_sha256=file_hashes["neutral_semantic_evidence.jsonl"],
        semantic_rule_sha256=file_hashes["semantic_rule_v2.json"],
        reason_precedence_sha256=file_hashes["reason_precedence_v2.json"],
        body_sha256_by_path={rel: digest for rel, digest in file_hashes.items()
                             if rel.startswith("bodies/")},
    )


def scan_independent_package(root, trusted, *, phase="construction", expected_record_count=500):
    return _strict_independent_scan(
        root, trusted, phase=phase, expected_record_count=expected_record_count,
    )


def enforce_independent_package(root, trusted, *, phase="construction"):
    try:
        return scan_independent_package(root, trusted, phase=phase)
    except FirewallViolation as exc:
        raise ControlledStop("INDEPENDENT_PACKAGE_CONTAMINATION__" + str(exc)) from exc


def run_s07(ctx):
    source = ctx[
        "s04_paths"
    ]

    frozen_trusted = trusted_s04_inputs(ctx)
    paths = s07_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    for filename in [
        "neutral_semantic_evidence.jsonl",
        "semantic_rule_v2.json",
        "reason_precedence_v2.json",
    ]:
        shutil.copyfile(
            source[
                "root"
            ]
            / filename,
            paths[
                "root"
            ]
            / filename,
        )

    shutil.copytree(
        source[
            "bodies"
        ],
        paths[
            "root"
        ]
        / "bodies",
    )

    lineage = {
        "artifact_id":
            "BATCH0004_CLEAN_INDEPENDENT_PACKAGE_CONSTRUCTION",
        "source_s04_manifest_sha256":
            sha256_file(
                source[
                    "manifest"
                ]
            ),
        "primary_ledger_included":
            False,
        "primary_semantic_fields_included":
            False,
        "primary_aggregate_counts_included":
            False,
        "mismatch_expectations_included":
            False,
        "final_reconciliation_included":
            False,
        "allowed_sources": [
            "S04_NEUTRAL_EVIDENCE",
            "SEMANTIC_RULE_V2",
            "REASON_PRECEDENCE_V2",
        ],
    }

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        lineage,
    )

    enforce_independent_package(paths["root"], frozen_trusted, phase="construction")

    append_transition(
        ctx,
        state="S07_INDEPENDENT_PACKAGE_CONSTRUCTION",
        required_inputs=[
            str(
                source[
                    "manifest"
                ]
            ),
        ],
        executable_action=(
            "Constructed clean Independent package "
            "from neutral S04 evidence only."
        ),
        output_artifacts=[
            str(
                paths[
                    "root"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "construction_manifest":
                manifest_sha,
        },
        hard_gates={
            "file_allowlist":
                "PASS",
            "field_allowlist":
                "PASS",
            "prohibited_primary_field_scan":
                "PASS",
            "primary_ledger_absent":
                "PASS",
        },
        fail_closed_conditions=[
            "FILE_ALLOWLIST_FAILURE",
            "PROHIBITED_PRIMARY_FIELD",
            "PRIMARY_LEDGER_PRESENT",
            "PRIMARY_DERIVED_SEMANTICS_PRESENT",
        ],
        next_state=(
            "S08_INDEPENDENT_PACKAGE_FREEZE"
        ),
    )

    ctx[
        "s07_paths"
    ] = paths

    return paths


def s08_paths(ctx):
    root = ctx[
        "s07_paths"
    ][
        "root"
    ]

    return {
        "root":
            root,
        "manifest":
            root
            / "independent_package_manifest.json",
        "sha256sums":
            root
            / "SHA256SUMS.txt",
        "zip":
            Path(
                ctx[
                    "run_root"
                ]
            )
            / "S08_INDEPENDENT_PACKAGE_FREEZE"
            / "independent_clean_package.zip",
        "freeze_manifest":
            Path(
                ctx[
                    "run_root"
                ]
            )
            / "S08_INDEPENDENT_PACKAGE_FREEZE"
            / "independent_package_freeze_manifest.json",
    }


def run_s08(ctx):
    frozen_trusted = trusted_s04_inputs(ctx)
    paths = s08_paths(
        ctx
    )

    paths[
        "zip"
    ].parent.mkdir(
        parents=True,
        exist_ok=False,
    )

    enforce_independent_package(paths["root"], frozen_trusted, phase="construction")

    package_members = [
        path.relative_to(
            paths[
                "root"
            ]
        )
        for path in paths[
            "root"
        ].rglob("*")
        if (
            path.is_file()
            and path
            not in {
                paths[
                    "manifest"
                ],
                paths[
                    "sha256sums"
                ],
            }
        )
    ]

    member_hashes = {
        str(rel):
            sha256_file(
                paths[
                    "root"
                ]
                / rel
            )
        for rel in sorted(
            package_members,
            key=lambda p:
                str(p),
        )
    }

    package_manifest = {
        "artifact_id":
            "BATCH0004_INDEPENDENT_CLEAN_PACKAGE_FREEZE",
        "file_allowlist":
            sorted(
                member_hashes
            ),
        "file_hashes":
            member_hashes,
        "contamination_check":
            "PASS",
        "source_lineage":
            "S04_NEUTRAL_EVIDENCE_ONLY",
        "primary_semantic_output_present":
            False,
    }

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        package_manifest,
    )

    package_members.append(
        paths[
            "manifest"
        ].relative_to(
            paths[
                "root"
            ]
        )
    )

    checksum_lines = []

    for rel in sorted(
        package_members,
        key=lambda p:
            str(p),
    ):
        checksum_lines.append(
            sha256_file(
                paths[
                    "root"
                ]
                / rel
            )
            + "  "
            + str(rel)
        )

    sums_sha = write_text_exclusive(
        paths[
            "sha256sums"
        ],
        "\n".join(
            checksum_lines
        )
        + "\n",
    )

    package_members.append(
        paths[
            "sha256sums"
        ].relative_to(
            paths[
                "root"
            ]
        )
    )

    zip_sha = deterministic_zip(
        root=paths[
            "root"
        ],
        relative_files=package_members,
        zip_path=paths[
            "zip"
        ],
    )

    enforce_independent_package(paths["root"], frozen_trusted, phase="freeze")
    try:
        _strict_validate_frozen_zip(paths["zip"], paths["root"], frozen_trusted,
                                    expected_record_count=500,
                                    expected_zip_sha256=zip_sha)
    except FirewallViolation as exc:
        raise ControlledStop("S08_FROZEN_PACKAGE_FIREWALL_FAILURE__" + str(exc)) from exc

    freeze_manifest = {
        "package_sha256":
            zip_sha,
        "package_manifest_sha256":
            manifest_sha,
        "sha256sums_sha256":
            sums_sha,
        "contamination_check":
            "PASS",
        "frozen":
            True,
    }

    freeze_manifest_sha = write_json_exclusive(
        paths[
            "freeze_manifest"
        ],
        freeze_manifest,
    )

    append_transition(
        ctx,
        state="S08_INDEPENDENT_PACKAGE_FREEZE",
        required_inputs=[
            str(
                ctx[
                    "s07_paths"
                ][
                    "root"
                ]
            ),
        ],
        executable_action=(
            "Froze deterministic clean Independent "
            "package, manifest, checksums, and package SHA."
        ),
        output_artifacts=[
            str(
                paths[
                    "zip"
                ]
            ),
            str(
                paths[
                    "freeze_manifest"
                ]
            ),
        ],
        output_hashes={
            "package":
                zip_sha,
            "package_manifest":
                manifest_sha,
            "sha256sums":
                sums_sha,
            "freeze_manifest":
                freeze_manifest_sha,
        },
        hard_gates={
            "contamination_check":
                "PASS",
            "package_manifest":
                "PASS",
            "sha256sums":
                "PASS",
            "deterministic_package":
                "PASS",
        },
        fail_closed_conditions=[
            "INDEPENDENT_CONTAMINATION",
            "PACKAGE_HASH_FAILURE",
            "PACKAGE_MANIFEST_FAILURE",
        ],
        next_state=(
            "S09_INDEPENDENT_SEMANTIC_ADJUDICATION"
        ),
    )

    ctx[
        "s08_paths"
    ] = paths

    return paths


def s09_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S09_INDEPENDENT_SEMANTIC_ADJUDICATION"
    )

    return {
        "root":
            root,
        "candidate":
            root
            / "independent_semantic_candidate.jsonl",
        "executor_manifest":
            root
            / "independent_executor_manifest.json",
        "raw_message":
            root
            / "independent_executor_final_message.txt",
        "attempt_manifest": root / "independent_executor_attempt_manifest.json",
    }


def run_s09(ctx):
    paths = s09_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    primary_roots = [
        ctx[
            "s05_paths"
        ][
            "root"
        ],
        ctx[
            "s06_paths"
        ][
            "root"
        ],
    ]

    original_modes = {}

    primary_ledger_sha_before = (
        sha256_file(
            ctx[
                "s06_paths"
            ][
                "ledger"
            ]
        )
    )

    try:
        for root in primary_roots:
            original_modes[
                root
            ] = stat.S_IMODE(
                root.stat().st_mode
            )

            os.chmod(
                root,
                0o000,
            )

        probe = subprocess.run(
            [
                "/bin/cat",
                str(
                    ctx[
                        "s06_paths"
                    ][
                        "ledger"
                    ]
                ),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        if probe.returncode == 0:
            raise ControlledStop(
                "INDEPENDENT_FILESYSTEM_ISOLATION_FAILURE"
            )

        result = execute_semantic_worker(
            ctx,
            role="INDEPENDENT",
            working_directory=ctx[
                "s08_paths"
            ][
                "root"
            ],
            prompt=semantic_prompt(
                role="INDEPENDENT",
                evidence_filename=(
                    "neutral_semantic_evidence.jsonl"
                ),
            ),
        )

    finally:
        for root, mode in original_modes.items():
            os.chmod(
                root,
                mode,
            )

    if (
        result[
            "context_id"
        ]
        == ctx[
            "primary_context_id"
        ]
    ):
        raise ControlledStop(
            "INDEPENDENT_CONTEXT_NOT_FRESH"
        )

    if (
        sha256_file(
            ctx[
                "s06_paths"
            ][
                "ledger"
            ]
        )
        != primary_ledger_sha_before
    ):
        raise ControlledStop(
            "PRIMARY_LEDGER_MUTATED_DURING_INDEPENDENT"
        )

    raw_rows, validated, s04_manifest_sha = validate_complete_semantic_result(
        ctx, result, role="INDEPENDENT", independent=True)
    candidate_sha = write_and_verify_semantic_candidate(
        ctx, path=paths["candidate"], raw_rows=raw_rows, validated=validated, independent=True)
    raw_sha = write_text_exclusive(paths["raw_message"], result["agent_message"] + "\n")
    attempt_sha = sha256_file(paths["attempt_manifest"])
    executor_manifest = {
        "role": "INDEPENDENT_SEMANTIC_EXECUTOR", "backend": result["backend"],
        "execution_context_identity": result["context_id"],
        "primary_context_identity": ctx["primary_context_id"],
        "context_identity_distinct": True,
        "filesystem_primary_ledger_read_denied": True,
        "input_package_sha256": sha256_file(ctx["s08_paths"]["zip"]),
        "s04_input_manifest_sha256": s04_manifest_sha,
        "candidate_output_identity": candidate_sha,
        "candidate_row_count": 500, "raw_message_sha256": raw_sha,
        "executor_attempt_manifest_sha256": attempt_sha,
        "failure_status": None, "command": result["command"],
    }
    executor_sha = write_json_exclusive(paths["executor_manifest"], executor_manifest)
    append_transition(
        ctx, state="S09_INDEPENDENT_SEMANTIC_ADJUDICATION",
        required_inputs=[str(ctx["s08_paths"]["zip"])],
        executable_action="Executed fresh isolated Independent executor; validated complete output and serialized readback before PASS.",
        output_artifacts=[str(paths["candidate"]), str(paths["executor_manifest"]), str(paths["attempt_manifest"])],
        output_hashes={"candidate": candidate_sha, "executor_manifest": executor_sha,
                       "raw_message": raw_sha, "executor_attempt_manifest": attempt_sha},
        hard_gates={"fresh_context": "PASS", "filesystem_isolation": "PASS",
                    "primary_ledger_immutable": "PASS", "candidate_json_parse": "PASS",
                    "complete_500_row_semantics": "PASS", "exact_identity_position_binding": "PASS",
                    "reason_contract": "PASS", "s04_input_binding": "PASS",
                    "candidate_readback": "PASS"},
        fail_closed_conditions=["PRIMARY_FILESYSTEM_READABLE", "CONTEXT_IDENTITY_REUSED",
                                "PRIMARY_LEDGER_MUTATION", "INDEPENDENT_EXECUTOR_FAILURE",
                                "INCOMPLETE_SEMANTIC_ROWS", "SERIALIZATION_OR_READBACK_FAILURE"],
        next_state="S10_INDEPENDENT_LEDGER_FREEZE",
    )
    ctx["independent_context_id"] = result["context_id"]
    ctx["s09_paths"] = paths
    return paths

def s10_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S10_INDEPENDENT_LEDGER_FREEZE"
    )

    return {
        "root":
            root,
        "ledger":
            root
            / "independent_semantic_ledger.jsonl",
        "manifest":
            root
            / "independent_freeze_manifest.json",
    }


def run_s10(ctx):
    paths = s10_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    evidence_rows = ctx[
        "s04_evidence_rows"
    ]

    candidate_rows = read_jsonl(
        ctx[
            "s09_paths"
        ][
            "candidate"
        ]
    )

    reason_contract = load_reason_contract(
        ctx[
            "s04_paths"
        ][
            "precedence"
        ]
    )

    validated = validate_semantic_rows(
        candidate_rows,
        evidence_rows,
        reason_contract,
    )

    ledger_sha = write_jsonl_exclusive(
        paths[
            "ledger"
        ],
        validated,
    )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "artifact_id":
                "BATCH0004_INDEPENDENT_LEDGER_FREEZE",
            "row_count":
                len(
                    validated
                ),
            "unique_source_identities":
                len({
                    row[
                        "canonical_source_identity"
                    ]
                    for row in validated
                }),
            "ledger_sha256":
                ledger_sha,
            "independent_context_id":
                ctx[
                    "independent_context_id"
                ],
            "comparison_information_received_before_freeze":
                False,
            "frozen":
                True,
        },
    )

    os.chmod(
        paths[
            "ledger"
        ],
        0o444,
    )

    os.chmod(
        paths[
            "manifest"
        ],
        0o444,
    )

    append_transition(
        ctx,
        state="S10_INDEPENDENT_LEDGER_FREEZE",
        required_inputs=[
            str(
                ctx[
                    "s09_paths"
                ][
                    "candidate"
                ]
            ),
        ],
        executable_action=(
            "Validated and froze complete Independent ledger "
            "before comparison."
        ),
        output_artifacts=[
            str(
                paths[
                    "ledger"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "ledger":
                ledger_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "row_count":
                "PASS",
            "identity_coverage":
                "PASS",
            "reason_contract":
                "PASS",
            "comparison_information_pre_freeze":
                "ABSENT",
        },
        fail_closed_conditions=[
            "INDEPENDENT_INCOMPLETE_OUTPUT",
            "INDEPENDENT_DUPLICATE_IDENTITY",
            "INVALID_DISPOSITION",
            "INVALID_REASON_CODE",
        ],
        next_state=(
            "S11_DETERMINISTIC_COMPARISON"
        ),
    )

    ctx[
        "independent_ledger_sha256"
    ] = ledger_sha

    ctx[
        "s10_paths"
    ] = paths

    return paths


def s11_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S11_DETERMINISTIC_COMPARISON"
    )

    return {
        "root":
            root,
        "full":
            root
            / "primary_independent_comparison.jsonl",
        "disposition_mismatches":
            root
            / "disposition_mismatch_only.jsonl",
        "reason_only":
            root
            / "reason_code_only_differences.jsonl",
        "manifest":
            root
            / "comparison_manifest.json",
    }


def run_s11(ctx):
    paths = s11_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    primary = read_jsonl(
        ctx[
            "s06_paths"
        ][
            "ledger"
        ]
    )

    independent = read_jsonl(
        ctx[
            "s10_paths"
        ][
            "ledger"
        ]
    )

    primary_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in primary
    }

    independent_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in independent
    }

    duplicate_count = (
        len(primary)
        - len(primary_by_id)
        + len(independent)
        - len(independent_by_id)
    )

    missing_primary = (
        set(independent_by_id)
        - set(primary_by_id)
    )

    missing_independent = (
        set(primary_by_id)
        - set(independent_by_id)
    )

    if (
        duplicate_count
        or missing_primary
        or missing_independent
    ):
        raise ControlledStop(
            "S11_IDENTITY_ALIGNMENT_FAILURE"
        )

    full_rows = []

    disposition_mismatches = []

    reason_only = []

    for source_id in sorted(
        primary_by_id,
        key=lambda sid:
            primary_by_id[
                sid
            ][
                "authorized_population_position"
            ],
    ):
        p = primary_by_id[
            source_id
        ]

        i = independent_by_id[
            source_id
        ]

        if (
            p[
                "authorized_population_position"
            ]
            != i[
                "authorized_population_position"
            ]
        ):
            raise ControlledStop(
                "S11_POSITION_ALIGNMENT_FAILURE"
            )

        disposition_match = (
            p[
                "body_disposition"
            ]
            == i[
                "body_disposition"
            ]
        )

        reason_match = (
            p[
                "reason_code"
            ]
            == i[
                "reason_code"
            ]
        )

        row = {
            "canonical_source_identity":
                source_id,
            "authorized_population_position":
                p[
                    "authorized_population_position"
                ],
            "primary":
                p,
            "independent":
                i,
            "body_disposition_match":
                disposition_match,
            "reason_code_match":
                reason_match,
            "reason_code_only_difference":
                (
                    disposition_match
                    and not reason_match
                ),
        }

        full_rows.append(
            row
        )

        if not disposition_match:
            disposition_mismatches.append(
                row
            )

        elif not reason_match:
            reason_only.append(
                row
            )

    full_sha = write_jsonl_exclusive(
        paths[
            "full"
        ],
        full_rows,
    )

    mismatch_sha = write_jsonl_exclusive(
        paths[
            "disposition_mismatches"
        ],
        disposition_mismatches,
    )

    reason_only_sha = write_jsonl_exclusive(
        paths[
            "reason_only"
        ],
        reason_only,
    )

    disposition_match_count = (
        len(full_rows)
        - len(
            disposition_mismatches
        )
    )

    manifest = {
        "aligned_rows":
            len(
                full_rows
            ),
        "exact_disposition_match_count":
            disposition_match_count,
        "scientific_disposition_mismatch_count":
            len(
                disposition_mismatches
            ),
        "reason_code_only_difference_count":
            len(
                reason_only
            ),
        "identity_alignment_failure_count":
            0,
        "missing_primary_count":
            0,
        "missing_independent_count":
            0,
        "duplicate_identity_count":
            0,
        "primary_ledger_sha256":
            ctx[
                "primary_ledger_sha256"
            ],
        "independent_ledger_sha256":
            ctx[
                "independent_ledger_sha256"
            ],
        "full_comparison_sha256":
            full_sha,
        "disposition_mismatch_sha256":
            mismatch_sha,
        "reason_only_sha256":
            reason_only_sha,
    }

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        manifest,
    )

    ctx[
        "s11_manifest"
    ] = manifest

    append_transition(
        ctx,
        state="S11_DETERMINISTIC_COMPARISON",
        required_inputs=[
            str(
                ctx[
                    "s06_paths"
                ][
                    "ledger"
                ]
            ),
            str(
                ctx[
                    "s10_paths"
                ][
                    "ledger"
                ]
            ),
        ],
        executable_action=(
            "Aligned frozen ledgers by canonical source "
            "identity and compared deterministically."
        ),
        output_artifacts=[
            str(
                paths[
                    "full"
                ]
            ),
            str(
                paths[
                    "disposition_mismatches"
                ]
            ),
            str(
                paths[
                    "reason_only"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "full_comparison":
                full_sha,
            "disposition_mismatches":
                mismatch_sha,
            "reason_only":
                reason_only_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "identity_alignment":
                "PASS",
            "comparison_completeness":
                "PASS",
            "semantic_reconciliation_performed":
                "NO",
        },
        fail_closed_conditions=[
            "IDENTITY_ALIGNMENT_FAILURE",
            "POSITION_ALIGNMENT_FAILURE",
            "MISSING_LEDGER_ROW",
            "DUPLICATE_IDENTITY",
        ],
        next_state=(
            "S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED"
        ),
    )

    ctx[
        "s11_paths"
    ] = paths

    return paths


def s12_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED"
    )

    return {
        "root":
            root,
        "input":
            root
            / "reconciliation_input.jsonl",
        "candidate":
            root
            / "reconciliation_candidate.jsonl",
        "ledger":
            root
            / "reconciliation_ledger.jsonl",
        "manifest":
            root
            / "reconciliation_manifest.json",
    }


def reconciliation_prompt():
    return (
        "You are the separate mismatch-only semantic reconciliation executor. "
        "Review ONLY rows in reconciliation_input.jsonl. "
        "Each row contains the frozen authoritative evidence reference, "
        "frozen Primary judgment, and frozen Independent judgment for a "
        "scientific BODY_DISPOSITION mismatch. Apply semantic_rule_v2.json "
        "and reason_precedence_v2.json. Do not reopen agreed rows. "
        "Return ONLY JSON with shape "
        '{"rows":[{"canonical_source_identity":"...",'
        '"authorized_population_position":1,'
        '"outcome":"PRIMARY_BETTER_SUPPORTED|'
        'INDEPENDENT_BETTER_SUPPORTED|CONSERVATIVE_UNRESOLVED|'
        'NEW_SYSTEMATIC_SCIENTIFIC_DEFECT",'
        '"final_body_disposition":"...",'
        '"final_reason_code":"...",'
        '"final_concise_review_rationale":"..."}]}. '
        "For PRIMARY_BETTER_SUPPORTED or INDEPENDENT_BETTER_SUPPORTED, "
        "the final disposition/reason must exactly match the selected frozen "
        "judgment. For CONSERVATIVE_UNRESOLVED use "
        "BODY_INACCESSIBLE_OR_UNRESOLVED with an applicable semantic-"
        "applicability unresolved reason. If a recurring rule boundary "
        "cannot be deterministically governed, return "
        "NEW_SYSTEMATIC_SCIENTIFIC_DEFECT."
    )


def run_s12(ctx):
    paths = s12_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    mismatch_rows = read_jsonl(
        ctx[
            "s11_paths"
        ][
            "disposition_mismatches"
        ]
    )

    if not mismatch_rows:
        ledger_sha = write_jsonl_exclusive(
            paths[
                "ledger"
            ],
            [],
        )

        manifest_sha = write_json_exclusive(
            paths[
                "manifest"
            ],
            {
                "status":
                    "NOT_APPLICABLE",
                "disposition_mismatch_rows":
                    0,
                "reconciliation_ledger_sha256":
                    ledger_sha,
                "new_systematic_scientific_defect":
                    False,
            },
        )

        append_transition(
            ctx,
            state="S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED",
            required_inputs=[
                str(
                    ctx[
                        "s11_paths"
                    ][
                        "disposition_mismatches"
                    ]
                ),
            ],
            executable_action=(
                "No disposition mismatches; reconciliation "
                "recorded as NOT_APPLICABLE."
            ),
            output_artifacts=[
                str(
                    paths[
                        "ledger"
                    ]
                ),
                str(
                    paths[
                        "manifest"
                    ]
                ),
            ],
            output_hashes={
                "ledger":
                    ledger_sha,
                "manifest":
                    manifest_sha,
            },
            hard_gates={
                "reconciliation_completeness":
                    "NOT_APPLICABLE",
                "agreed_rows_reopened":
                    "NO",
            },
            fail_closed_conditions=[
                "UNEXPECTED_RECONCILIATION_REQUIRED",
            ],
            next_state=(
                "S13_FINAL_BATCH_LEDGER_FREEZE"
            ),
        )

        ctx[
            "s12_paths"
        ] = paths

        return paths

    evidence_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in ctx[
            "s04_evidence_rows"
        ]
    }

    reconciliation_input = []

    for row in mismatch_rows:
        source_id = row[
            "canonical_source_identity"
        ]

        evidence = evidence_by_id[
            source_id
        ]

        reconciliation_input.append({
            "canonical_source_identity":
                source_id,
            "authorized_population_position":
                row[
                    "authorized_population_position"
                ],
            "authoritative_evidence":
                evidence,
            "primary":
                row[
                    "primary"
                ],
            "independent":
                row[
                    "independent"
                ],
        })

    input_sha = write_jsonl_exclusive(
        paths[
            "input"
        ],
        reconciliation_input,
    )

    shutil.copyfile(
        ctx[
            "s04_paths"
        ][
            "rule"
        ],
        paths[
            "root"
        ]
        / "semantic_rule_v2.json",
    )

    shutil.copyfile(
        ctx[
            "s04_paths"
        ][
            "precedence"
        ],
        paths[
            "root"
        ]
        / "reason_precedence_v2.json",
    )

    bodies_target = (
        paths[
            "root"
        ]
        / "bodies"
    )

    bodies_target.mkdir()

    needed_members = set()

    for row in reconciliation_input:
        evidence = row[
            "authoritative_evidence"
        ]

        for key in [
            "body_evidence_member",
            "header_evidence_member",
        ]:
            member = evidence.get(
                key
            )

            if member:
                needed_members.add(
                    member
                )

    for member in sorted(
        needed_members
    ):
        src = (
            ctx[
                "s04_paths"
            ][
                "root"
            ]
            / member
        )

        dst = (
            paths[
                "root"
            ]
            / member
        )

        dst.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copyfile(
            src,
            dst,
        )

    result = execute_semantic_worker(
        ctx,
        role="RECONCILIATION",
        working_directory=paths[
            "root"
        ],
        prompt=reconciliation_prompt(),
    )

    payload = parse_json_agent_message(
        result[
            "agent_message"
        ]
    )

    candidate_rows = payload.get(
        "rows"
    )

    if not isinstance(
        candidate_rows,
        list,
    ):
        raise ControlledStop(
            "RECONCILIATION_ROWS_MISSING"
        )

    write_jsonl_exclusive(
        paths[
            "candidate"
        ],
        candidate_rows,
    )

    expected_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in reconciliation_input
    }

    reason_contract = load_reason_contract(
        ctx[
            "s04_paths"
        ][
            "precedence"
        ]
    )

    observed = set()

    validated = []

    systematic = False

    for row in candidate_rows:
        source_id = row.get(
            "canonical_source_identity"
        )

        if (
            source_id
            not in expected_by_id
            or source_id
            in observed
        ):
            raise ControlledStop(
                "RECONCILIATION_IDENTITY_FAILURE"
            )

        observed.add(
            source_id
        )

        source = expected_by_id[
            source_id
        ]

        if (
            row.get(
                "authorized_population_position"
            )
            != source[
                "authorized_population_position"
            ]
        ):
            raise ControlledStop(
                "RECONCILIATION_POSITION_FAILURE"
            )

        outcome = row.get(
            "outcome"
        )

        if outcome not in {
            "PRIMARY_BETTER_SUPPORTED",
            "INDEPENDENT_BETTER_SUPPORTED",
            "CONSERVATIVE_UNRESOLVED",
            "NEW_SYSTEMATIC_SCIENTIFIC_DEFECT",
        }:
            raise ControlledStop(
                "RECONCILIATION_OUTCOME_FAILURE"
            )

        if (
            outcome
            == "NEW_SYSTEMATIC_SCIENTIFIC_DEFECT"
        ):
            systematic = True

            validated.append(
                row
            )

            continue

        disposition = row.get(
            "final_body_disposition"
        )

        reason_code = row.get(
            "final_reason_code"
        )

        rationale = row.get(
            "final_concise_review_rationale"
        )

        if (
            disposition
            not in ALLOWED_DISPOSITIONS
            or reason_code
            not in reason_contract[
                disposition
            ]
            or not isinstance(
                rationale,
                str,
            )
            or not rationale.strip()
        ):
            raise ControlledStop(
                "RECONCILIATION_FINAL_JUDGMENT_FAILURE"
            )

        selected = None

        if outcome == "PRIMARY_BETTER_SUPPORTED":
            selected = source[
                "primary"
            ]

        elif outcome == "INDEPENDENT_BETTER_SUPPORTED":
            selected = source[
                "independent"
            ]

        if selected is not None:
            if (
                disposition
                != selected[
                    "body_disposition"
                ]
                or reason_code
                != selected[
                    "reason_code"
                ]
            ):
                raise ControlledStop(
                    "RECONCILIATION_SELECTED_SIDE_MUTATION"
                )

        if outcome == "CONSERVATIVE_UNRESOLVED":
            if (
                disposition
                != "BODY_INACCESSIBLE_OR_UNRESOLVED"
                or not reason_code.startswith(
                    "SEMANTIC_APPLICABILITY_UNRESOLVED"
                )
            ):
                raise ControlledStop(
                    "CONSERVATIVE_UNRESOLVED_CONTRACT_FAILURE"
                )

        validated.append({
            "canonical_source_identity":
                source_id,
            "authorized_population_position":
                source[
                    "authorized_population_position"
                ],
            "outcome":
                outcome,
            "final_body_disposition":
                disposition,
            "final_reason_code":
                reason_code,
            "final_reason_category":
                reason_category(
                    reason_contract,
                    disposition,
                    reason_code,
                ),
            "final_concise_review_rationale":
                rationale.strip(),
        })

    if observed != set(
        expected_by_id
    ):
        raise ControlledStop(
            "RECONCILIATION_INCOMPLETE"
        )

    ledger_sha = write_jsonl_exclusive(
        paths[
            "ledger"
        ],
        validated,
    )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "status":
                (
                    "CONTROLLED_STOP"
                    if systematic
                    else "PASS"
                ),
            "disposition_mismatch_rows":
                len(
                    mismatch_rows
                ),
            "reconciliation_rows":
                len(
                    validated
                ),
            "reconciliation_input_sha256":
                input_sha,
            "reconciliation_ledger_sha256":
                ledger_sha,
            "execution_context_id":
                result[
                    "context_id"
                ],
            "new_systematic_scientific_defect":
                systematic,
        },
    )

    if systematic:
        raise ControlledStop(
            "NEW_SYSTEMATIC_SCIENTIFIC_DEFECT"
        )

    append_transition(
        ctx,
        state="S12_MISMATCH_ONLY_RECONCILIATION_IF_REQUIRED",
        required_inputs=[
            str(
                ctx[
                    "s11_paths"
                ][
                    "disposition_mismatches"
                ]
            ),
        ],
        executable_action=(
            "Executed separate semantic reconciliation "
            "only for disposition-mismatch rows."
        ),
        output_artifacts=[
            str(
                paths[
                    "ledger"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "ledger":
                ledger_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "mismatch_only_scope":
                "PASS",
            "agreed_rows_reopened":
                "NO",
            "reconciliation_completeness":
                "PASS",
            "new_systematic_scientific_defect":
                "NO",
        },
        fail_closed_conditions=[
            "AGREED_ROW_REOPENED",
            "RECONCILIATION_INCOMPLETE",
            "NEW_SYSTEMATIC_SCIENTIFIC_DEFECT",
        ],
        next_state=(
            "S13_FINAL_BATCH_LEDGER_FREEZE"
        ),
    )

    ctx[
        "s12_paths"
    ] = paths

    return paths


def s13_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S13_FINAL_BATCH_LEDGER_FREEZE"
    )

    return {
        "root":
            root,
        "ledger":
            root
            / "batch0004_final_accounting_ledger.jsonl",
        "manifest":
            root
            / "batch0004_final_accounting_manifest.json",
    }


def run_s13(ctx):
    paths = s13_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    comparison = read_jsonl(
        ctx[
            "s11_paths"
        ][
            "full"
        ]
    )

    reconciliation_rows = read_jsonl(
        ctx[
            "s12_paths"
        ][
            "ledger"
        ]
    )

    reconciliation_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in reconciliation_rows
        if row.get(
            "outcome"
        )
    }

    evidence_by_id = {
        row[
            "canonical_source_identity"
        ]:
            row
        for row in ctx[
            "s04_evidence_rows"
        ]
    }

    reason_contract = load_reason_contract(
        ctx[
            "s04_paths"
        ][
            "precedence"
        ]
    )

    final_rows = []

    for comp in comparison:
        source_id = comp[
            "canonical_source_identity"
        ]

        primary = comp[
            "primary"
        ]

        independent = comp[
            "independent"
        ]

        if not comp[
            "body_disposition_match"
        ]:
            recon = reconciliation_by_id.get(
                source_id
            )

            if recon is None:
                raise ControlledStop(
                    "S13_RECONCILIATION_ROW_MISSING"
                )

            disposition = recon[
                "final_body_disposition"
            ]

            reason_code = recon[
                "final_reason_code"
            ]

            rationale = recon[
                "final_concise_review_rationale"
            ]

            reconciliation_outcome = recon[
                "outcome"
            ]

        else:
            disposition = primary[
                "body_disposition"
            ]

            reconciliation_outcome = (
                "NOT_APPLICABLE"
            )

            if (
                primary[
                    "reason_code"
                ]
                == independent[
                    "reason_code"
                ]
            ):
                reason_code = primary[
                    "reason_code"
                ]

                rationale = primary[
                    "concise_review_rationale"
                ]

            else:
                p_rank = reason_contract[
                    disposition
                ][
                    primary[
                        "reason_code"
                    ]
                ][
                    "rank"
                ]

                i_rank = reason_contract[
                    disposition
                ][
                    independent[
                        "reason_code"
                    ]
                ][
                    "rank"
                ]

                if p_rank <= i_rank:
                    selected = primary
                else:
                    selected = independent

                reason_code = selected[
                    "reason_code"
                ]

                rationale = selected[
                    "concise_review_rationale"
                ]

        evidence = evidence_by_id[
            source_id
        ]

        final_rows.append({
            "accepted_source_identity":
                source_id,
            "batch_id":
                evidence[
                    "batch_id"
                ],
            "authorized_population_position":
                evidence[
                    "authorized_population_position"
                ],
            "record_ordinal":
                evidence[
                    "record_ordinal"
                ],
            "metadata_ledger_position":
                evidence[
                    "metadata_ledger_position"
                ],
            "notice_class":
                evidence[
                    "notice_class"
                ],
            "canonical_locator":
                evidence[
                    "canonical_locator"
                ],
            "body_content_available_for_interpretation":
                evidence[
                    "body_available"
                ],
            "body_retrieval_status":
                evidence[
                    "retrieval_status"
                ],
            "body_sha256":
                evidence[
                    "body_sha256"
                ],
            "extracted_body_sha256":
                evidence[
                    "extracted_body_sha256"
                ],
            "identity_reconciliation_status":
                evidence[
                    "identity_reconciliation_status"
                ],
            "body_disposition":
                disposition,
            "reason_code":
                reason_code,
            "reason_category":
                reason_category(
                    reason_contract,
                    disposition,
                    reason_code,
                ),
            "concise_review_rationale":
                rationale,
            "semantic_rule_version":
                SEMANTIC_RULE_VERSION,
            "reconciliation_outcome":
                reconciliation_outcome,
        })

    final_rows = sorted(
        final_rows,
        key=lambda row:
            row[
                "authorized_population_position"
            ],
    )

    require_unique_identities(
        final_rows,
        identity_field="accepted_source_identity",
        expected_count=ctx[
            "config"
        ][
            "expected_record_count"
        ],
    )

    require_exact_positions(
        final_rows,
        position_field="authorized_population_position",
        position_start=ctx[
            "config"
        ][
            "position_start"
        ],
        position_end=ctx[
            "config"
        ][
            "position_end"
        ],
    )

    ledger_sha = write_jsonl_exclusive(
        paths[
            "ledger"
        ],
        final_rows,
    )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "artifact_id":
                "BATCH0004_FINAL_ACCOUNTING_LEDGER",
            "row_count":
                len(
                    final_rows
                ),
            "unique_source_identities":
                len({
                    row[
                        "accepted_source_identity"
                    ]
                    for row in final_rows
                }),
            "position_start":
                ctx[
                    "config"
                ][
                    "position_start"
                ],
            "position_end":
                ctx[
                    "config"
                ][
                    "position_end"
                ],
            "ledger_sha256":
                ledger_sha,
            "primary_ledger_sha256":
                ctx[
                    "primary_ledger_sha256"
                ],
            "independent_ledger_sha256":
                ctx[
                    "independent_ledger_sha256"
                ],
            "frozen":
                True,
        },
    )

    os.chmod(
        paths[
            "ledger"
        ],
        0o444,
    )

    os.chmod(
        paths[
            "manifest"
        ],
        0o444,
    )

    append_transition(
        ctx,
        state="S13_FINAL_BATCH_LEDGER_FREEZE",
        required_inputs=[
            str(
                ctx[
                    "s11_paths"
                ][
                    "full"
                ]
            ),
            str(
                ctx[
                    "s12_paths"
                ][
                    "ledger"
                ]
            ),
        ],
        executable_action=(
            "Constructed deterministic final Batch ledger "
            "from agreements, reason precedence, and frozen reconciliation."
        ),
        output_artifacts=[
            str(
                paths[
                    "ledger"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "ledger":
                ledger_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "full_batch_accounting":
                "PASS",
            "unique_identities":
                "PASS",
            "position_coverage":
                "PASS",
            "primary_independent_ledgers_rewritten":
                "NO",
        },
        fail_closed_conditions=[
            "MISSING_RECONCILIATION",
            "FINAL_BATCH_ROW_COUNT_FAILURE",
            "FINAL_BATCH_DUPLICATE_IDENTITY",
            "FINAL_BATCH_POSITION_FAILURE",
        ],
        next_state=(
            "S14_CUMULATIVE_ACCOUNTING"
        ),
    )

    ctx[
        "final_batch_ledger_sha256"
    ] = ledger_sha

    ctx[
        "s13_paths"
    ] = paths

    return paths


def s14_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S14_CUMULATIVE_ACCOUNTING"
    )

    return {
        "root":
            root,
        "ledger":
            root
            / "d1_positions_1_to_2000_cumulative_accounting_ledger.jsonl",
        "manifest":
            root
            / "d1_positions_1_to_2000_cumulative_accounting_manifest.json",
    }


def run_s14(ctx):
    paths = s14_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    prior_path = Path(
        ctx[
            "config"
        ][
            "paths"
        ][
            "prior_cumulative_ledger"
        ]
    )

    expected_prior_sha = (
        ctx[
            "config"
        ][
            "expected_hashes"
        ][
            "prior_cumulative_ledger"
        ]
    )

    verify_expected_sha(
        prior_path,
        expected_prior_sha,
        "S14_PRIOR_CUMULATIVE",
    )

    prior = read_jsonl(
        prior_path
    )

    current = read_jsonl(
        ctx[
            "s13_paths"
        ][
            "ledger"
        ]
    )

    require_unique_identities(
        prior,
        identity_field="ACCEPTED_SOURCE_IDENTITY",
        expected_count=1500,
    )

    require_exact_positions(
        prior,
        position_field="CUMULATIVE_POSITION",
        position_start=1,
        position_end=1500,
    )

    prior_ids = {
        row[
            "ACCEPTED_SOURCE_IDENTITY"
        ]
        for row in prior
    }

    current_ids = {
        row[
            "accepted_source_identity"
        ]
        for row in current
    }

    if prior_ids & current_ids:
        raise ControlledStop(
            "S14_DUPLICATE_IDENTITY_ACROSS_CUMULATIVE_BOUNDARY"
        )

    final_ledger_sha = ctx[
        "final_batch_ledger_sha256"
    ]

    new_rows = []

    for row in current:
        source_row_sha = canonical_row_sha256(
            row
        )

        cumulative_row = {
            "ACCEPTED_SOURCE_IDENTITY":
                row[
                    "accepted_source_identity"
                ],
            "BATCH_ID":
                row[
                    "batch_id"
                ],
            "BODY_CONTENT_AVAILABLE_FOR_INTERPRETATION":
                row[
                    "body_content_available_for_interpretation"
                ],
            "BODY_DISPOSITION":
                row[
                    "body_disposition"
                ],
            "BODY_RETRIEVAL_STATUS":
                row[
                    "body_retrieval_status"
                ],
            "BODY_SHA256":
                row[
                    "body_sha256"
                ],
            "CANONICAL_LOCATOR":
                row[
                    "canonical_locator"
                ],
            "CONCISE_REVIEW_RATIONALE":
                row[
                    "concise_review_rationale"
                ],
            "CUMULATIVE_POSITION":
                row[
                    "authorized_population_position"
                ],
            "EXTRACTED_BODY_SHA256":
                row[
                    "extracted_body_sha256"
                ],
            "IDENTITY_RECONCILIATION_STATUS":
                row[
                    "identity_reconciliation_status"
                ],
            "NOTICE_CLASS":
                row[
                    "notice_class"
                ],
            "REASON_CATEGORY":
                row[
                    "reason_category"
                ],
            "REASON_CODE":
                row[
                    "reason_code"
                ],
            "RECORD_ORDINAL_OR_ACCEPTED_RECORD_KEY":
                row[
                    "record_ordinal"
                ],
            "SEMANTIC_ROW_REINTERPRETED":
                False,
            "SEMANTIC_RULE_VERSION":
                row[
                    "semantic_rule_version"
                ],
            "SOURCE_ACCEPTED_LEDGER_CLASS":
                "BATCH0004_FINAL_ACCEPTED_LEDGER",
            "SOURCE_ACCEPTED_LEDGER_SHA256":
                final_ledger_sha,
            "SOURCE_BATCH_POSITION":
                row[
                    "authorized_population_position"
                ],
            "SOURCE_ROW_SHA256":
                source_row_sha,
        }

        if sorted(
            cumulative_row
        ) != sorted(
            CUMULATIVE_FIELDS
        ):
            raise ControlledStop(
                "S14_CUMULATIVE_SCHEMA_FAILURE"
            )

        new_rows.append(
            cumulative_row
        )

    cumulative = sorted(
        prior
        + new_rows,
        key=lambda row:
            row[
                "CUMULATIVE_POSITION"
            ],
    )

    require_unique_identities(
        cumulative,
        identity_field="ACCEPTED_SOURCE_IDENTITY",
        expected_count=2000,
    )

    require_exact_positions(
        cumulative,
        position_field="CUMULATIVE_POSITION",
        position_start=1,
        position_end=2000,
    )

    if (
        {
            row[
                "ACCEPTED_SOURCE_IDENTITY"
            ]
            for row in cumulative[
                :1500
            ]
        }
        != prior_ids
    ):
        raise ControlledStop(
            "S14_PRIOR_PUBLICATION_DISAPPEARED"
        )

    ledger_sha = write_jsonl_exclusive(
        paths[
            "ledger"
        ],
        cumulative,
    )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "artifact_id":
                "D1_POSITIONS_1_TO_2000_CUMULATIVE_ACCOUNTING_LEDGER",
            "authorization":
                "DETERMINISTIC_ACCOUNTING_INTEGRATION_ONLY",
            "prior_cumulative_ledger_sha256":
                expected_prior_sha,
            "batch0004_final_ledger_sha256":
                final_ledger_sha,
            "cumulative_ledger_sha256":
                ledger_sha,
            "cumulative_rows":
                2000,
            "position_start":
                1,
            "position_end":
                2000,
            "unique_source_identities":
                2000,
            "missing_positions":
                0,
            "duplicate_positions":
                0,
            "no_prior_publication_disappeared":
                True,
            "no_duplicate_accepted_publication_entered":
                True,
            "semantic_rows_reinterpreted":
                False,
        },
    )

    append_transition(
        ctx,
        state="S14_CUMULATIVE_ACCOUNTING",
        required_inputs=[
            str(
                prior_path
            ),
            str(
                ctx[
                    "s13_paths"
                ][
                    "ledger"
                ]
            ),
        ],
        executable_action=(
            "Merged prior accepted cumulative ledger with "
            "current final Batch ledger deterministically."
        ),
        output_artifacts=[
            str(
                paths[
                    "ledger"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "ledger":
                ledger_sha,
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "cumulative_rows":
                "PASS",
            "identity_uniqueness":
                "PASS",
            "position_continuity":
                "PASS",
            "prior_preservation":
                "PASS",
            "semantic_reinterpretation":
                "NO",
        },
        fail_closed_conditions=[
            "LOST_PRIOR_RECORD",
            "DUPLICATE_IDENTITY",
            "MISSING_CURRENT_BATCH_RECORD",
            "POSITION_CONTINUITY_FAILURE",
        ],
        next_state=(
            "S15_HASH_CHAIN"
        ),
    )

    ctx[
        "new_cumulative_ledger_sha256"
    ] = ledger_sha

    ctx[
        "s14_paths"
    ] = paths

    return paths


def s15_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S15_HASH_CHAIN"
    )

    return {
        "root":
            root,
        "payload":
            root
            / "cumulative_hash_chain_payload.json",
        "manifest":
            root
            / "cumulative_hash_chain_manifest.json",
    }


def run_s15(ctx):
    paths = s15_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    cfg = ctx[
        "config"
    ]

    payload = {
        "hash_chain_version":
            HASH_CHAIN_VERSION,
        "prior_cumulative_state_identity":
            cfg[
                "expected_hashes"
            ][
                "prior_cumulative_ledger"
            ],
        "current_final_batch_identity":
            ctx[
                "final_batch_ledger_sha256"
            ],
        "deterministic_accounting_payload": {
            "prior_cumulative_manifest_sha256":
                cfg[
                    "expected_hashes"
                ][
                    "prior_cumulative_manifest"
                ],
            "new_cumulative_ledger_sha256":
                ctx[
                    "new_cumulative_ledger_sha256"
                ],
            "cumulative_rows":
                2000,
            "position_start":
                1,
            "position_end":
                2000,
            "unique_source_identities":
                2000,
            "semantic_rule_sha256":
                cfg[
                    "expected_hashes"
                ][
                    "semantic_rule"
                ],
            "reason_precedence_sha256":
                cfg[
                    "expected_hashes"
                ][
                    "reason_precedence"
                ],
        },
    }

    canonical = (
        stable_json(
            payload
        )
        + "\n"
    )

    chain_identity = sha256_text(
        canonical
    )

    payload_sha = write_text_exclusive(
        paths[
            "payload"
        ],
        canonical,
    )

    if payload_sha != chain_identity:
        raise ControlledStop(
            "S15_HASH_CHAIN_REPRODUCTION_FAILURE"
        )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "hash_chain_version":
                HASH_CHAIN_VERSION,
            "canonical_serialization":
                "stable_json(payload)+NEWLINE",
            "prior_cumulative_state_identity":
                payload[
                    "prior_cumulative_state_identity"
                ],
            "current_final_batch_identity":
                payload[
                    "current_final_batch_identity"
                ],
            "new_cumulative_hash_chain_identity":
                chain_identity,
            "hash_chain":
                "PASS",
        },
    )

    append_transition(
        ctx,
        state="S15_HASH_CHAIN",
        required_inputs=[
            str(
                ctx[
                    "s14_paths"
                ][
                    "ledger"
                ]
            ),
            str(
                ctx[
                    "s13_paths"
                ][
                    "ledger"
                ]
            ),
        ],
        executable_action=(
            "Bound prior cumulative identity, current final "
            "Batch identity, and deterministic accounting payload "
            "using frozen canonical serialization."
        ),
        output_artifacts=[
            str(
                paths[
                    "payload"
                ]
            ),
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "hash_chain_payload":
                payload_sha,
            "hash_chain_manifest":
                manifest_sha,
            "new_cumulative_hash_chain_identity":
                chain_identity,
        },
        hard_gates={
            "hash_chain":
                "PASS",
            "reproduction":
                "PASS",
        },
        fail_closed_conditions=[
            "HASH_CHAIN_REPRODUCTION_FAILURE",
            "LINEAGE_IDENTITY_MISSING",
        ],
        next_state=(
            "S16_BATCH_COMPLETE_PENDING_MANAGING_REVIEW"
        ),
    )

    ctx[
        "new_cumulative_hash_chain_identity"
    ] = chain_identity

    ctx[
        "s15_paths"
    ] = paths

    return paths


def s16_paths(ctx):
    root = (
        Path(
            ctx[
                "run_root"
            ]
        )
        / "S16_BATCH_COMPLETE_PENDING_MANAGING_REVIEW"
    )

    return {
        "root":
            root,
        "manifest":
            root
            / "batch_complete_pending_managing_review.json",
    }


def run_s16(ctx):
    paths = s16_paths(
        ctx
    )

    paths[
        "root"
    ].mkdir(
        parents=True,
        exist_ok=False,
    )

    manifest_sha = write_json_exclusive(
        paths[
            "manifest"
        ],
        {
            "state":
                "S16_BATCH_COMPLETE_PENDING_MANAGING_REVIEW",
            "batch_id":
                ctx[
                    "config"
                ][
                    "batch_id"
                ],
            "automatic_next_batch":
                False,
            "batch_0005_authorized":
                False,
            "batch_0005_started":
                False,
            "transition_from_s16":
                "PROHIBITED",
            "new_cumulative_hash_chain_identity":
                ctx[
                    "new_cumulative_hash_chain_identity"
                ],
            "next_actor":
                "MANAGING",
        },
    )

    append_transition(
        ctx,
        state="S16_BATCH_COMPLETE_PENDING_MANAGING_REVIEW",
        required_inputs=[
            str(
                ctx[
                    "s15_paths"
                ][
                    "manifest"
                ]
            ),
        ],
        executable_action=(
            "Entered terminal Batch-complete state and "
            "prohibited automatic transition to Batch 0005."
        ),
        output_artifacts=[
            str(
                paths[
                    "manifest"
                ]
            ),
        ],
        output_hashes={
            "manifest":
                manifest_sha,
        },
        hard_gates={
            "terminal_state":
                "PASS",
            "automatic_next_batch":
                "FALSE",
            "batch_0005_started":
                "NO",
        },
        fail_closed_conditions=[
            "BATCH_0005_TRANSITION_ATTEMPT",
            "AUTOMATIC_NEXT_BATCH_ENABLEMENT",
        ],
        next_state=None,
    )

    ctx[
        "s16_paths"
    ] = paths

    return paths


def build_context(config_path):
    config_path = Path(
        config_path
    )

    config = read_json(
        config_path
    )

    required_top = {
        "batch_id",
        "position_start",
        "position_end",
        "expected_record_count",
        "run_root",
        "execution_mode",
        "real_execution_authorized",
        "paths",
        "expected_hashes",
        "semantic_executor",
    }

    missing = (
        required_top
        - set(config)
    )

    if missing:
        raise ControlledStop(
            "CONFIG_REQUIRED_FIELD_MISSING__"
            + "__".join(
                sorted(
                    missing
                )
            )
        )

    if (
        config[
            "batch_id"
        ]
        != "BATCH_0004"
    ):
        raise ControlledStop(
            "BATCH_ID_NOT_AUTHORIZED"
        )

    if (
        config[
            "position_start"
        ]
        != 1501
        or config[
            "position_end"
        ]
        != 2000
        or config[
            "expected_record_count"
        ]
        != 500
    ):
        raise ControlledStop(
            "BATCH0004_SCOPE_FAILURE"
        )

    if (
        config[
            "execution_mode"
        ]
        == "REAL_BATCH0004"
        and config[
            "real_execution_authorized"
        ]
        is not True
    ):
        raise ControlledStop(
            "REAL_BATCH0004_EXECUTION_NOT_AUTHORIZED"
        )

    if (
        config[
            "execution_mode"
        ]
        not in {
            "SYNTHETIC_NON_PRODUCTION",
            "REAL_BATCH0004",
        }
    ):
        raise ControlledStop(
            "UNKNOWN_EXECUTION_MODE"
        )

    run_root = Path(
        config[
            "run_root"
        ]
    )

    if run_root.exists():
        raise ControlledStop(
            "RUN_ROOT_ALREADY_EXISTS"
        )

    run_root.mkdir(
        parents=True,
        exist_ok=False,
    )

    return {
        "config_path":
            config_path,
        "config":
            config,
        "run_root":
            run_root,
    }


def run_pipeline(ctx):
    run_s04(
        ctx
    )

    run_s05(
        ctx
    )

    run_s06(
        ctx
    )

    run_s07(
        ctx
    )

    run_s08(
        ctx
    )

    run_s09(
        ctx
    )

    run_s10(
        ctx
    )

    run_s11(
        ctx
    )

    run_s12(
        ctx
    )

    run_s13(
        ctx
    )

    run_s14(
        ctx
    )

    run_s15(
        ctx
    )

    run_s16(
        ctx
    )

    log = load_transition_log(
        ctx
    )

    observed_states = [
        row[
            "STATE"
        ]
        for row in log
    ]

    if observed_states != STATE_SEQUENCE:
        raise ControlledStop(
            "STATE_SEQUENCE_FAILURE"
        )

    if any(
        row[
            "STATUS"
        ]
        != "PASS"
        for row in log
    ):
        raise ControlledStop(
            "NONPASS_STATE_IN_FINAL_LOG"
        )

    return {
        "status":
            "COMPLETE__READY_FOR_MANAGING_REVIEW",
        "state_machine_version":
            STATE_MACHINE_VERSION,
        "states":
            observed_states,
        "no_state_skipped":
            True,
        "s16_reached":
            True,
        "batch_0005_started":
            False,
        "new_cumulative_hash_chain_identity":
            ctx[
                "new_cumulative_hash_chain_identity"
            ],
    }


def static_validate_source():
    required_functions = {
        "run_s04",
        "run_s05",
        "run_s06",
        "run_s07",
        "run_s08",
        "run_s09",
        "run_s10",
        "run_s11",
        "run_s12",
        "run_s13",
        "run_s14",
        "run_s15",
        "run_s16",
        "run_pipeline",
        "run_codex_executor",
        "run_mock_executor",
        "execute_semantic_worker",
        "scan_independent_package",
        "deterministic_zip",
    }

    present = {
        name
        for name, value
        in globals().items()
        if callable(value)
    }

    missing = (
        required_functions
        - present
    )

    if missing:
        raise ControlledStop(
            "STATIC_FUNCTION_COVERAGE_FAILURE__"
            + "__".join(
                sorted(
                    missing
                )
            )
        )

    if len(
        STATE_SEQUENCE
    ) != 13:
        raise ControlledStop(
            "STATIC_STATE_COUNT_FAILURE"
        )

    return {
        "state_machine_version":
            STATE_MACHINE_VERSION,
        "required_function_coverage":
            "PASS",
        "state_count":
            len(
                STATE_SEQUENCE
            ),
        "batch_0005_transition":
            "PROHIBITED",
        "real_execution_default_authorized":
            False,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--static-validate",
        action="store_true",
    )

    parser.add_argument(
        "--config",
    )

    args = parser.parse_args()

    if args.static_validate:
        print(
            json.dumps(
                static_validate_source(),
                sort_keys=True,
                indent=2,
            )
        )

        return 0

    if not args.config:
        print(
            "FAIL_CLOSED__CONFIG_REQUIRED",
            file=os.sys.stderr,
        )

        return 2

    try:
        ctx = build_context(
            args.config
        )

        result = run_pipeline(
            ctx
        )

        print(
            json.dumps(
                result,
                sort_keys=True,
                indent=2,
            )
        )

        return 0

    except ControlledStop as exc:
        print(
            "CONTROLLED_STOP__"
            + str(exc),
            file=os.sys.stderr,
        )

        return 3


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
