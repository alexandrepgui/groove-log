"""Shared fixtures for the backend test suite."""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# ── Common test data ──────────────────────────────────────────────────────────

FAKE_LABEL_DATA = {
    "albums": ["Kind of Blue"],
    "artists": ["Miles Davis"],
    "country": "US",
    "format": "LP",
    "label": "Columbia",
    "catno": "CS 8163",
    "year": "1959",
}

FAKE_DISCOGS_RESULT = {
    "id": 123,
    "title": "Miles Davis - Kind of Blue",
    "year": "1959",
    "country": "US",
    "format": ["Vinyl", "LP"],
    "label": ["Columbia"],
    "catno": "CS 8163",
    "uri": "/release/123",
    "cover_image": "https://example.com/cover.jpg",
}

FAKE_RANKING = {"likeliness": [0], "discarded": []}


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def sample_image_bytes():
    """Load the sample label JPEG fixture."""
    return (FIXTURES_DIR / "sample_label.jpg").read_bytes()


@pytest.fixture()
def fake_label_data():
    """Return a copy of the standard fake label data."""
    return dict(FAKE_LABEL_DATA)


@pytest.fixture()
def fake_discogs_result():
    """Return a copy of the standard fake Discogs result."""
    return dict(FAKE_DISCOGS_RESULT)


@pytest.fixture()
def mock_repo():
    """Mock repository that captures saved records."""
    repo = MagicMock()
    repo.saved_records = []

    def capture_save(record):
        repo.saved_records.append(record)

    repo.save_search_record.side_effect = capture_save
    return repo


def make_llm_response(data):
    """Create a mock LLM HTTP response."""
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {
        "choices": [{"message": {"content": json.dumps(data)}}]
    }
    resp.raise_for_status = MagicMock()
    return resp


def make_discogs_response(results, pages=1):
    """Create a mock Discogs HTTP response."""
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {
        "results": results,
        "pagination": {"pages": pages},
    }
    resp.raise_for_status = MagicMock()
    return resp
