# SPDX-License-Identifier: AGPL-3.0-or-later
"""TDD tests for cache.py - Redis-backed caching layer."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_redis():
    mock = MagicMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.setex.return_value = True
    mock.delete.return_value = True
    with patch("cache._get_redis", return_value=mock):
        yield mock


class TestCacheOperations:
    """Test cache get/set/delete."""

    def test_cache_miss(self, mock_redis):
        from cache import cache_get

        assert cache_get("nonexistent") is None

    def test_cache_hit(self, mock_redis):
        import json

        from cache import cache_get

        mock_redis.get.return_value = json.dumps({"data": 42}).encode()
        result = cache_get("mykey")
        assert result == {"data": 42}

    def test_cache_set(self, mock_redis):
        import json

        from cache import cache_set

        cache_set("mykey", {"data": 42}, ttl=300)
        mock_redis.set.assert_called_once_with(
            "openleg:mykey", json.dumps({"data": 42}), ex=300
        )
        mock_redis.setex.assert_not_called()

    def test_cache_delete(self, mock_redis):
        from cache import cache_delete

        cache_delete("mykey")
        mock_redis.delete.assert_called_once_with("openleg:mykey")


class TestTenantCache:
    """Test tenant-specific caching."""

    def test_tenant_cache_key(self, mock_redis):
        from cache import cache_get

        cache_get("tenant:baden")
        mock_redis.get.assert_called_with("openleg:tenant:baden")

    def test_cache_fallback_on_error(self):
        """If Redis is down, cache operations return None / no-op."""
        with patch("cache._get_redis", side_effect=Exception("Connection refused")):
            from cache import cache_get, cache_set

            assert cache_get("key") is None
            cache_set("key", "val")  # should not raise


# === Unavailability posture (#529) ===


class TestCacheUnavailable:
    """What happens when the cache service is down is a documented posture,
    not an accident: reads degrade to None (backing store), writes no-op,
    one bounded attempt per operation."""

    def test_get_makes_exactly_one_attempt_and_degrades_to_none(self):
        from cache import cache_get

        client = MagicMock()
        client.get.side_effect = ConnectionError("redis down")
        with patch("cache._get_redis", return_value=client):
            assert cache_get("some-key") is None
            assert client.get.call_count == 1, (
                "no retry loop may sit inside a cache read; a recovering "
                "service must not be stampeded"
            )

    def test_set_delete_and_clear_swallow_errors_without_retry(self):
        from cache import cache_clear_prefix, cache_delete, cache_set

        set_client = MagicMock()
        set_client.set.side_effect = ConnectionError("redis down")
        delete_client = MagicMock()
        delete_client.delete.side_effect = ConnectionError("redis down")
        clear_client = MagicMock()
        clear_client.keys.side_effect = ConnectionError("redis down")

        with patch("cache._get_redis", return_value=set_client):
            cache_set("k", {"v": 1})
        with patch("cache._get_redis", return_value=delete_client):
            cache_delete("k")
        with patch("cache._get_redis", return_value=clear_client):
            cache_clear_prefix("tenant")

        assert set_client.set.call_count == 1
        assert delete_client.delete.call_count == 1
        assert clear_client.keys.call_count == 1

    def test_client_uses_bounded_socket_timeouts(self):
        """A cache outage must degrade fast, not hang request threads on an
        OS-default TCP timeout."""
        import cache

        cache._redis_client = None
        try:
            with patch("redis.from_url") as from_url:
                cache._get_redis()
                kwargs = from_url.call_args.kwargs
            assert (
                kwargs["socket_connect_timeout"] == cache.CACHE_CONNECT_TIMEOUT_SECONDS
            )
            assert kwargs["socket_timeout"] == cache.CACHE_SOCKET_TIMEOUT_SECONDS
            assert 0 < cache.CACHE_CONNECT_TIMEOUT_SECONDS <= 5
        finally:
            cache._redis_client = None
