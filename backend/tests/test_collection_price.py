"""Tests for POST /api/collection and GET /api/price/{release_id}."""

from unittest.mock import MagicMock, patch

import pytest
import requests
from fastapi.testclient import TestClient


@pytest.fixture()
def mock_repo():
    repo = MagicMock()
    repo.saved_records = []
    repo.save_collection_record.side_effect = lambda r: repo.saved_records.append(r)
    return repo


@pytest.fixture()
def client(mock_repo):
    from deps import get_repo
    from main import app

    app.dependency_overrides[get_repo] = lambda: mock_repo
    yield TestClient(app)
    app.dependency_overrides.clear()


# ── POST /api/collection ────────────────────────────────────────────────────


def test_add_to_collection_success(client, mock_repo):
    instance = {
        "instance_id": 42,
        "resource_url": "https://api.discogs.com/users/testuser/collection/folders/1/releases/123/instances/42",
    }
    with patch("routes.search.add_to_collection", return_value=instance):
        resp = client.post("/api/collection", json={"release_id": 123})
    assert resp.status_code == 200
    assert resp.json()["instance_id"] == 42
    assert mock_repo.save_collection_record.call_count == 1


def test_add_to_collection_http_404(client, mock_repo):
    http_err = requests.HTTPError(response=MagicMock(status_code=404))
    with patch("routes.search.add_to_collection", side_effect=http_err):
        resp = client.post("/api/collection", json={"release_id": 999})
    assert resp.status_code == 404


def test_add_to_collection_http_502(client, mock_repo):
    http_err = requests.HTTPError(response=MagicMock(status_code=500))
    with patch("routes.search.add_to_collection", side_effect=http_err):
        resp = client.post("/api/collection", json={"release_id": 999})
    assert resp.status_code == 502


def test_add_to_collection_unexpected_error(client, mock_repo):
    with patch("routes.search.add_to_collection", side_effect=RuntimeError("boom")):
        resp = client.post("/api/collection", json={"release_id": 123})
    assert resp.status_code == 502
    assert mock_repo.save_collection_record.call_count == 1


# ── GET /api/price/{release_id} ─────────────────────────────────────────────


def test_get_price_success(client):
    stats = {"lowest_price": {"value": 12.50}, "num_for_sale": 5}
    with patch("routes.search.get_marketplace_stats", return_value=stats):
        resp = client.get("/api/price/123")
    assert resp.status_code == 200
    assert resp.json() == {"lowest_price": 12.50, "num_for_sale": 5}


def test_get_price_scalar_lowest(client):
    stats = {"lowest_price": 9.99, "num_for_sale": 2}
    with patch("routes.search.get_marketplace_stats", return_value=stats):
        resp = client.get("/api/price/456")
    assert resp.status_code == 200
    assert resp.json()["lowest_price"] == 9.99


def test_get_price_not_found(client):
    http_err = requests.HTTPError(response=MagicMock(status_code=404))
    with patch("routes.search.get_marketplace_stats", side_effect=http_err):
        resp = client.get("/api/price/999")
    assert resp.status_code == 404


def test_get_price_discogs_error(client):
    http_err = requests.HTTPError(response=MagicMock(status_code=500))
    with patch("routes.search.get_marketplace_stats", side_effect=http_err):
        resp = client.get("/api/price/123")
    assert resp.status_code == 502


def test_get_price_unexpected_error(client):
    with patch("routes.search.get_marketplace_stats", side_effect=RuntimeError("fail")):
        resp = client.get("/api/price/123")
    assert resp.status_code == 502
