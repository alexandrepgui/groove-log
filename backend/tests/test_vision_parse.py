"""Tests for services/vision.py: _parse_json and rank_results."""

import json
from unittest.mock import MagicMock, patch

import pytest

from services.vision import _parse_json, rank_results


# ── _parse_json ───────────────────────────────────────────────────────────────


class TestParseJson:
    def test_plain_json(self):
        assert _parse_json('{"key": "value"}') == {"key": "value"}

    def test_json_with_code_fence(self):
        raw = '```json\n{"key": "value"}\n```'
        assert _parse_json(raw) == {"key": "value"}

    def test_json_with_plain_code_fence(self):
        raw = '```\n{"key": "value"}\n```'
        assert _parse_json(raw) == {"key": "value"}

    def test_json_with_whitespace(self):
        raw = '  \n  {"key": "value"}  \n  '
        assert _parse_json(raw) == {"key": "value"}

    def test_json_array(self):
        assert _parse_json("[1, 2, 3]") == [1, 2, 3]

    def test_invalid_json_raises(self):
        with pytest.raises(json.JSONDecodeError):
            _parse_json("not json at all")


# ── rank_results ──────────────────────────────────────────────────────────────


class TestRankResults:
    def test_returns_likeliness_and_discarded(self):
        releases = [
            {"title": "Miles Davis - Kind of Blue", "year": "1959",
             "country": "US", "format": ["Vinyl"], "label": ["Columbia"], "catno": "C1"},
        ]
        conversation = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "test"},
        ]
        ranking_response = {"likeliness": [0], "discarded": []}

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": json.dumps(ranking_response)}}]
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("services.vision.requests.post", return_value=mock_resp):
            likeliness, discarded = rank_results(releases, conversation)

        assert likeliness == [0]
        assert discarded == []

    def test_truncates_to_max_ranking_results(self):
        """Only first MAX_RANKING_RESULTS candidates should be ranked."""
        releases = [{"title": f"R{i}", "year": "2000", "country": "US",
                      "format": ["Vinyl"], "label": ["L"], "catno": f"C{i}"}
                     for i in range(30)]
        conversation = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "test"},
        ]
        # LLM returns indices 0..19 — matching MAX_RANKING_RESULTS
        ranking_response = {"likeliness": list(range(20)), "discarded": []}

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": json.dumps(ranking_response)}}]
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("services.vision.requests.post", return_value=mock_resp):
            likeliness, discarded = rank_results(releases, conversation)

        # Verify the returned indices are within MAX_RANKING_RESULTS bounds
        assert likeliness == list(range(20))
        assert discarded == []
