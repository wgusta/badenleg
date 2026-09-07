# SPDX-License-Identifier: AGPL-3.0-or-later
"""Rate limiting on public endpoints, with the measured posture pinned (#524).

Security wins the trade-off, but the cost is stated: named limits per surface
class with rationale, a clean 429 with a machine-readable retry hint, and a
limiter that degrades open when its backing store is unavailable.
"""

from flask import Flask, jsonify

from security_extensions import limiter


def _wired_app(storage_uri, rate_limit_rule, probe_name):
    """A small app wired exactly like the real app: same shared limiter, same
    app-wide 429 handler. The probe function name is unique per test because
    the shared limiter marks routes by qualified function name."""
    from app import main_bp

    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        RATELIMIT_STORAGE_URI=storage_uri,
        RATELIMIT_ENABLED=True,
        APP_BASE_URL="http://localhost:5000",
    )
    application.register_blueprint(main_bp)
    limiter.init_app(application)

    if probe_name == "probe_strict":

        @application.route("/probe_strict")
        @limiter.limit(rate_limit_rule)
        def probe_strict():
            return jsonify({"ok": True})

    elif probe_name == "probe_generous":

        @application.route("/probe_generous")
        @limiter.limit(rate_limit_rule)
        def probe_generous():
            return jsonify({"ok": True})

    else:
        raise AssertionError(f"unknown probe name {probe_name}")

    return application


class TestRetryHint:
    def test_exceeding_the_limit_returns_a_clean_429_with_a_retry_hint(self):
        application = _wired_app("memory://", "2 per minute", "probe_strict")
        limiter.reset()
        client = application.test_client()
        env = {"REMOTE_ADDR": "192.0.2.10"}

        statuses = [
            client.get("/probe_strict", environ_overrides=env).status_code
            for _ in range(3)
        ]

        assert statuses[:2] == [200, 200]
        assert statuses[2] == 429
        breach = client.get("/probe_strict", environ_overrides=env)
        assert breach.status_code == 429
        assert breach.headers.get("Retry-After") is not None, (
            "a 429 must carry a machine-readable retry hint"
        )
        body = breach.get_json()
        assert body["retry_after_seconds"] == int(breach.headers["Retry-After"])
        assert "Zu viele Anfragen" in body["error"]


class TestFailOpen:
    def test_an_unreachable_limiter_store_never_locks_out_normal_traffic(self):
        """Redis unreachable: the limiter must degrade, not error, and normal
        traffic must keep being served (#524, consistent with #529). The
        limit here is far above anything a human or a shared frontend does;
        only abuse patterns would notice."""
        application = _wired_app(
            "redis://127.0.0.1:1/0", "1000 per minute", "probe_generous"
        )
        client = application.test_client()
        env = {"REMOTE_ADDR": "192.0.2.11"}

        statuses = [
            client.get("/probe_generous", environ_overrides=env).status_code
            for _ in range(6)
        ]

        assert all(status == 200 for status in statuses), statuses


class TestSurfaceClasses:
    def test_limits_are_named_constants_with_rationale(self):
        from pathlib import Path

        import security_extensions

        source = Path(security_extensions.__file__).read_text(encoding="utf-8")
        assert security_extensions.RATE_LIMIT_ANONYMOUS_READ == "240 per minute"
        assert security_extensions.RATE_LIMIT_CALCULATOR == "30 per minute"
        assert security_extensions.RATE_LIMIT_RETRY_AFTER_SECONDS == 60
        for constant in (
            "RATE_LIMIT_ANONYMOUS_READ",
            "RATE_LIMIT_CALCULATOR",
            "RATE_LIMIT_RETRY_AFTER_SECONDS",
        ):
            rationale = source[: source.index(constant)]
            assert rationale.count("#") >= 4, (
                f"{constant} needs its stated rationale in the source"
            )

    def test_the_public_api_is_limited_as_anonymous_reads(self):
        """The public API blueprint carries the anonymous-read class on GET/HEAD
        without overriding the app-wide default."""
        from api_public import public_api_bp
        from security_extensions import RATE_LIMIT_ANONYMOUS_READ

        blueprint_limits = limiter.limit_manager._blueprint_limits.get(
            public_api_bp.name, []
        )
        applied = [str(route.limit_provider) for route in blueprint_limits]
        assert RATE_LIMIT_ANONYMOUS_READ in applied, applied
        methods = {method for route in blueprint_limits for method in route.methods}
        assert {"get", "head"} <= methods
        assert all(not route.override_defaults for route in blueprint_limits), (
            "the app-wide default must keep applying alongside the class limit"
        )
