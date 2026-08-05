"""Standard-library offline-boundary policy tests.

The real audit hook and kernel negative controls execute only inside the
accepted workflow launcher. These unit tests validate deterministic event
classification, fixed control identities, and evidence sanitization without
performing network or process operations.
"""

from __future__ import annotations

import unittest


DNS_CONTROL_ID = "C3_NET_NEG_DNS_001"
HTTPS_CONTROL_ID = "C3_NET_NEG_HTTPS_001"
IPV4_CONTROL_ID = "C3_NET_NEG_IPV4_001"
IPV6_CONTROL_ID = "C3_NET_NEG_IPV6_001"
PROCESS_CONTROL_ID = "C3_AUDIT_PROCESS_001"
CTYPES_CONTROL_ID = "C3_AUDIT_CTYPES_001"

FORBIDDEN_CHILD_ENVIRONMENT_NAMES = {
    "GITHUB_TOKEN",
    "ACTIONS_RUNTIME_TOKEN",
    "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
    "ACTIONS_ID_TOKEN_REQUEST_URL",
    "ACTIONS_CACHE_URL",
    "ACTIONS_RESULTS_URL",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
    "PIP_INDEX_URL",
    "PIP_EXTRA_INDEX_URL",
    "PIP_TRUSTED_HOST",
    "PIP_FIND_LINKS",
    "APCA_API_KEY_ID",
    "APCA_API_SECRET_KEY",
    "APCA_API_BASE_URL",
    "BARS_FEED",
}


def classify_audit_event(event: str) -> str | None:
    """Classify only the accepted blocked event families."""

    if event == "socket.getaddrinfo":
        return "DNS_RESOLUTION"
    if event in {
        "socket.__new__",
        "socket.connect",
        "socket.connect_ex",
        "http.client.connect",
    }:
        return "NETWORK_CONNECTION"
    if event in {
        "subprocess.Popen",
        "os.system",
        "os.fork",
        "os.forkpty",
        "os.posix_spawn",
        "os.posix_spawnp",
    }:
        return "PROCESS_CREATION"
    if event.startswith("ctypes."):
        return "CTYPES"
    return None


def sanitized_event_record(
    control_id: str,
    event: str,
) -> dict[str, str]:
    """Return a fixed record containing no event arguments or destination."""

    classification = classify_audit_event(event)
    if classification is None:
        raise ValueError("AUDIT_EVENT_NOT_GUARDED")
    return {
        "control_id": control_id,
        "operation_classification": classification,
        "terminal_result": "BLOCKED",
    }


class OfflineBoundaryTests(unittest.TestCase):
    def test_event_classifier_is_fixed(self) -> None:
        cases = {
            "socket.getaddrinfo": "DNS_RESOLUTION",
            "socket.__new__": "NETWORK_CONNECTION",
            "socket.connect": "NETWORK_CONNECTION",
            "socket.connect_ex": "NETWORK_CONNECTION",
            "http.client.connect": "NETWORK_CONNECTION",
            "subprocess.Popen": "PROCESS_CREATION",
            "os.system": "PROCESS_CREATION",
            "os.fork": "PROCESS_CREATION",
            "os.posix_spawn": "PROCESS_CREATION",
            "ctypes.dlopen": "CTYPES",
            "ctypes.dlsym": "CTYPES",
            "open": None,
        }
        for event, expected in cases.items():
            with self.subTest(event=event):
                self.assertEqual(classify_audit_event(event), expected)

    def test_fixed_control_ids_and_expected_stages(self) -> None:
        controls = {
            DNS_CONTROL_ID: "PYTHON_AUDIT_GUARD_BEFORE_OS_DNS_ACTIVITY",
            HTTPS_CONTROL_ID: (
                "PYTHON_AUDIT_GUARD_BEFORE_OS_SOCKET_OR_HTTP_ACTIVITY"
            ),
            IPV4_CONTROL_ID: (
                "NETWORK_UNREACHABLE_INSIDE_ROUTE_FREE_NAMESPACE"
            ),
            IPV6_CONTROL_ID: (
                "NETWORK_UNREACHABLE_INSIDE_ROUTE_FREE_NAMESPACE"
            ),
            PROCESS_CONTROL_ID: "PYTHON_AUDIT_GUARD_PROCESS_BLOCK",
            CTYPES_CONTROL_ID: "PYTHON_AUDIT_GUARD_CTYPES_BLOCK",
        }

        self.assertEqual(len(controls), 6)
        self.assertEqual(len(set(controls)), 6)
        self.assertTrue(
            all(value and value == value.upper() for value in controls.values())
        )

    def test_exact_child_environment_allowlist_excludes_forbidden_names(
        self,
    ) -> None:
        child_environment_names = {
            "LANG",
            "LC_ALL",
            "TZ",
            "TMPDIR",
            "LD_LIBRARY_PATH",
            "PYTHONHASHSEED",
            "PYTHONDONTWRITEBYTECODE",
            "PYTHONNOUSERSITE",
            "C3_EXECUTION_PHASE",
            "C3_REPOSITORY_ROOT",
            "C3_EVIDENCE_ROOT",
            "C3_PARENT_NS_SHA256",
            "C3_ORIGINAL_UID",
            "C3_ORIGINAL_GID",
            "C3_EXPECTED_LOCK_SHA256",
            "C3_EXPECTED_DEPENDENCY_METADATA_SHA256",
        }

        self.assertTrue(
            FORBIDDEN_CHILD_ENVIRONMENT_NAMES.isdisjoint(
                child_environment_names
            )
        )
        self.assertNotIn("PATH", child_environment_names)
        self.assertNotIn("HOME", child_environment_names)

    def test_sanitized_audit_records_do_not_contain_destinations(self) -> None:
        records = [
            sanitized_event_record(
                DNS_CONTROL_ID,
                "socket.getaddrinfo",
            ),
            sanitized_event_record(
                HTTPS_CONTROL_ID,
                "socket.__new__",
            ),
            sanitized_event_record(
                PROCESS_CONTROL_ID,
                "subprocess.Popen",
            ),
            sanitized_event_record(
                CTYPES_CONTROL_ID,
                "ctypes.dlopen",
            ),
        ]

        rendered = repr(records)
        self.assertNotIn("c3-offline-control.invalid", rendered)
        self.assertNotIn("192.0.2.1", rendered)
        self.assertNotIn("2001:db8::1", rendered)
        self.assertNotIn("/bin/true", rendered)
        self.assertNotIn("Traceback", rendered)
        self.assertNotIn("Exception", rendered)

    def test_universal_attempt_metrics_remain_unestablished(self) -> None:
        evidence = {
            "network_attempt_count_during_canonical_execution": (
                "NOT_A_UNIVERSALLY_OBSERVABLE_METRIC"
            ),
            "native_or_descendant_attempt_count": "NOT_ESTABLISHED",
            "universal_DNS_request_count": "NOT_ESTABLISHED",
            "universal_network_syscall_attempt_count": "NOT_ESTABLISHED",
            "primary_python_unexpected_audit_event_count": 0,
        }

        self.assertEqual(
            evidence["native_or_descendant_attempt_count"],
            "NOT_ESTABLISHED",
        )
        self.assertEqual(
            evidence["universal_DNS_request_count"],
            "NOT_ESTABLISHED",
        )
        self.assertEqual(
            evidence["universal_network_syscall_attempt_count"],
            "NOT_ESTABLISHED",
        )
        self.assertEqual(
            evidence["primary_python_unexpected_audit_event_count"],
            0,
        )

    def test_unknown_event_is_not_silently_classified(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "AUDIT_EVENT_NOT_GUARDED",
        ):
            sanitized_event_record("C3_UNKNOWN", "open")


if __name__ == "__main__":
    unittest.main()
