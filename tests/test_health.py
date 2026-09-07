# SPDX-License-Identifier: AGPL-3.0-or-later
"""Health endpoint tests."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def health_app():
    """Minimal Flask app with health blueprint."""
    from flask import Flask

    from health import health_bp

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(health_bp)
    return app


@pytest.fixture
def health_client(health_app):
    return health_app.test_client()


class TestHealthEndpoint:
    def test_health_ok(self, health_client):
        with patch("health.db") as mock_db:
            mock_conn = MagicMock()
            mock_db.get_connection.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_db.get_connection.return_value.__exit__ = MagicMock(return_value=False)
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__ = MagicMock(
                return_value=mock_cursor
            )
            mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

            resp = health_client.get("/health")
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["status"] == "healthy"
            assert data["db"] == "connected"

    def test_health_db_down(self, health_client):
        with patch("health.db") as mock_db:
            mock_db.get_connection.side_effect = Exception("connection refused")

            resp = health_client.get("/health")
            assert resp.status_code == 503
            data = resp.get_json()
            assert data["status"] == "degraded"
            assert data["db"] == "disconnected"

    def test_livez(self, health_client):
        resp = health_client.get("/livez")
        assert resp.status_code == 200
        assert resp.data == b"ok"


class TestCacheUnavailabilityReporting:
    """The health body must reflect a down cache (#529). The overall status
    stays healthy: a cache loss degrades to the backing store and never
    locks users out, so it must not page the same way a DB loss does."""

    def test_cache_down_is_reported_in_the_body_while_status_stays_healthy(
        self, health_client
    ):
        with patch("health.db") as mock_db:
            mock_conn = MagicMock()
            mock_db.get_connection.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_db.get_connection.return_value.__exit__ = MagicMock(return_value=False)
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__ = MagicMock(
                return_value=mock_cursor
            )
            mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
            with patch("cache._get_redis", side_effect=ConnectionError("down")):
                resp = health_client.get("/health")

        body = resp.get_json()
        assert body["redis"] == "disconnected"
        assert body["db"] == "connected"
        assert body["status"] == "healthy"
        assert resp.status_code == 200

    def test_cache_down_is_reported_by_ping_refusal_not_import(self, health_client):
        """A hanging ping is what an unbounded socket timeout produces; the
        health check must see the connection failure, not hang."""
        client = MagicMock()
        client.ping.side_effect = ConnectionError("down")
        with patch("health.db") as mock_db:
            mock_conn = MagicMock()
            mock_db.get_connection.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_db.get_connection.return_value.__exit__ = MagicMock(return_value=False)
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__ = MagicMock(
                return_value=mock_cursor
            )
            mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
            with patch("cache._get_redis", return_value=client):
                resp = health_client.get("/health")

        assert resp.get_json()["redis"] == "disconnected"
        assert client.ping.call_count == 1
