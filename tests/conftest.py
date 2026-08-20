from __future__ import annotations

import socket

import pytest


PROHIBITED_MARKERS = frozenset(
    {
        "network",
        "credential",
        "provider",
        "training",
        "order",
    }
)


def _deny_network(*_args, **_kwargs):
    raise RuntimeError("network access prohibited by TM-044 offline default")


def pytest_sessionstart(session):
    socket.socket.connect = _deny_network
    socket.socket.connect_ex = _deny_network
    socket.create_connection = _deny_network
    socket.getaddrinfo = _deny_network


@pytest.fixture(autouse=True)
def enforce_tm044_prohibited_markers(request):
    prohibited = sorted(
        PROHIBITED_MARKERS.intersection(
            marker.name for marker in request.node.iter_markers()
        )
    )
    if prohibited:
        pytest.fail(
            "prohibited TM-044 marker(s) selected for ordinary canonical "
            f"verification: {', '.join(prohibited)}",
            pytrace=False,
        )
