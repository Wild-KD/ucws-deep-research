"""Server API tests for the self-serve workspace."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_healthz():
    pytest.importorskip("multipart")
    from server import create_app

    client = TestClient(create_app())
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_start_mock_run_with_url_config():
    pytest.importorskip("multipart")
    from server import create_app

    client = TestClient(create_app())
    resp = client.post(
        "/api/run",
        data={
            "topic": "silver",
            "provider": "mock",
            "source_urls": "https://example.com/report\nhttps://example.com/article",
            "search_mode": "augment",
            "depth": "deep",
            "language": "bilingual",
            "verification_scope": "all_nodes_and_edges",
        },
    )
    assert resp.status_code == 200
    run_id = resp.json()["run_id"]

    status = client.get(f"/api/run/{run_id}")
    assert status.status_code == 200
    data = status.json()
    assert data["provider"] == "mock"
    assert data["urls"] == 2
    assert data["config"]["depth"] == "deep"
