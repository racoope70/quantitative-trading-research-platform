from __future__ import annotations

import os
from pathlib import Path
import socket
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
PYTEST_INI = ROOT / "pytest.ini"
CONFTEST = ROOT / "tests" / "conftest.py"

PROHIBITED_MARKERS = {
    "network",
    "credential",
    "provider",
    "training",
    "order",
}


def _run_pytest(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_pytest_discovery_self_test(tmp_path):
    (tmp_path / "pytest.ini").write_text(
        PYTEST_INI.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    tests = tmp_path / "tests"
    tests.mkdir()

    (tests / "test_visible.py").write_text(
        '''
def test_function_probe():
    pass


class TestClassProbe:
    def test_method_probe(self):
        pass
''',
        encoding="utf-8",
    )

    (tests / "visible_test.py").write_text(
        '''
def test_must_not_be_discovered():
    pass
''',
        encoding="utf-8",
    )

    result = _run_pytest(["--collect-only"], tmp_path)
    output = result.stdout + result.stderr

    assert result.returncode == 0, output
    assert "tests/test_visible.py::test_function_probe" in output
    assert "tests/test_visible.py::TestClassProbe::test_method_probe" in output
    assert "test_must_not_be_discovered" not in output


def test_prohibited_markers_are_registered(pytestconfig):
    registered = {
        entry.split(":", 1)[0].strip()
        for entry in pytestconfig.getini("markers")
    }
    assert PROHIBITED_MARKERS <= registered


def test_prohibited_marker_fails_closed(tmp_path):
    (tmp_path / "pytest.ini").write_text(
        PYTEST_INI.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    tests = tmp_path / "tests"
    tests.mkdir()

    (tests / "conftest.py").write_text(
        CONFTEST.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tests / "test_prohibited.py").write_text(
        '''
import pytest


@pytest.mark.network
def test_prohibited_probe():
    pass
''',
        encoding="utf-8",
    )

    result = _run_pytest([], tmp_path)
    output = result.stdout + result.stderr

    assert result.returncode != 0
    assert "prohibited TM-044 marker(s)" in output
    assert "network" in output


def test_no_network_default():
    assert socket.socket.connect.__name__ == "_deny_network"
    assert socket.socket.connect_ex.__name__ == "_deny_network"
    assert socket.create_connection.__name__ == "_deny_network"
    assert socket.getaddrinfo.__name__ == "_deny_network"

    with pytest.raises(RuntimeError, match="network access prohibited"):
        socket.create_connection(None)

    with pytest.raises(RuntimeError, match="network access prohibited"):
        socket.getaddrinfo("example.com", 443)
