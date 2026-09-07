# SPDX-License-Identifier: AGPL-3.0-or-later
"""Interface tests for the outbound email queue repository (store.email_queue).

Verifies the extracted module resolves the connection seam via
`database.get_connection` and that `database` re-exports the identical objects,
so legacy callers and existing monkeypatches keep working unchanged. Mirrors
`test_store_ranking.py` / `test_store_profile.py`; the seam is the test surface.
"""

import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import database
from store import email_queue

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_REEXPORTED = (
    "schedule_email",
    "get_pending_emails",
    "mark_email_sent",
    "mark_email_failed",
    "cancel_emails_for_building",
    "get_email_stats",
)


class _FakeCursor:
    def __init__(self, rows=None, one=None, rowcount=0):
        self.rows = rows or []
        self.one = one
        self.rowcount = rowcount
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.one

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class _FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


def _conn_ctx(cursor):
    @contextmanager
    def _factory():
        yield _FakeConnection(cursor)

    return _factory


def test_database_reexports_are_identical_objects():
    for name in _REEXPORTED:
        assert getattr(database, name) is getattr(email_queue, name), name


def test_store_email_queue_imports_without_database_bootstrap():
    result = subprocess.run(
        [sys.executable, "-c", "import store.email_queue; print('ok')"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_email_queue_uses_database_connection_seam(monkeypatch):
    # Monkeypatching database.get_connection must affect store.email_queue calls,
    # proving the seam is shared (not a stale direct import binding).
    cur = _FakeCursor(rows=[{"id": 1, "email": "a@b.ch"}])
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    rows = email_queue.get_pending_emails()
    assert rows == [{"id": 1, "email": "a@b.ch"}]
    assert "scheduled_emails" in cur.executed[0][0]
    assert cur.executed[0][1] == (50,)


def test_schedule_email_skips_duplicate(monkeypatch):
    # An already pending/sent template for the building returns False without insert.
    cur = _FakeCursor(one=(1,))
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert email_queue.schedule_email("b1", "a@b.ch", "welcome", 0.0) is False


# === Data hygiene contract (#519) ===


def test_mark_email_sent_scrubs_the_recipient_address(monkeypatch):
    """Success ends the address's need: the row stays for the audit trail,
    the personal data goes."""
    cur = _FakeCursor(rowcount=1)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert email_queue.mark_email_sent(1) is True

    query, params = cur.executed[0]
    assert "status = 'sent'" in query
    assert "email = %s" in query
    assert params == ("", 1)


def test_cancel_emails_for_building_scrubs_addresses(monkeypatch):
    """Unsubscribe must not leave usable addresses behind in the queue."""
    cur = _FakeCursor(rowcount=2)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert email_queue.cancel_emails_for_building("b1") == 2

    query, params = cur.executed[0]
    assert "status = 'cancelled'" in query
    assert "email = %s" in query
    assert params == ("", "b1")


def test_mark_email_failed_retries_within_bounds_then_terminates(monkeypatch):
    """A delivery failure returns the entry to the queue until the attempt
    bound is reached; only then does it become terminal."""
    assert email_queue.MAX_EMAIL_ATTEMPTS == 3

    retry_cur = _FakeCursor(one={"retry_count": 1}, rowcount=1)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(retry_cur))
    assert email_queue.mark_email_failed(1, "SMTP down") is True
    query, params = retry_cur.executed[0]
    assert "retry_count = retry_count + 1" in query and params == ("SMTP down", 1)
    assert "status = 'pending'" in retry_cur.executed[1][0]

    terminal_cur = _FakeCursor(one={"retry_count": 3}, rowcount=1)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(terminal_cur))
    assert email_queue.mark_email_failed(2, "SMTP down") is True
    assert "status = 'failed'" in terminal_cur.executed[1][0]


def test_mark_email_failed_unknown_entry_is_false(monkeypatch):
    cur = _FakeCursor(one=None, rowcount=0)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert email_queue.mark_email_failed(99, "x") is False


def test_cleanup_finished_emails_uses_the_named_retention_horizon(monkeypatch):
    cur = _FakeCursor(rowcount=7)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert email_queue.cleanup_finished_emails() == 7

    query, params = cur.executed[0]
    assert "DELETE FROM scheduled_emails" in query
    for status in ("sent", "failed", "cancelled"):
        assert f"'{status}'" in query
    assert params == (email_queue.EMAIL_QUEUE_RETENTION_DAYS,)


def test_retention_horizon_is_a_bounded_constant_with_rationale():
    assert 0 < email_queue.EMAIL_QUEUE_RETENTION_DAYS <= 365
    module = email_queue.__doc__ or ""
    assert "retention" in module.lower()


def test_queue_rows_cannot_outlive_or_send_after_their_building():
    """The FK is ON DELETE CASCADE, so a deleted building takes its queue
    rows with it; the pending listing joins buildings, so a row whose
    building is gone is never handed to the sender."""
    schema = (PROJECT_ROOT / "store" / "schema.py").read_text(encoding="utf-8")
    create_index = schema.index("CREATE TABLE IF NOT EXISTS scheduled_emails")
    next_table = schema.index("CREATE TABLE", create_index + 1)
    block = schema[create_index:next_table]
    assert "REFERENCES buildings(building_id) ON DELETE CASCADE" in block
    assert "ADD COLUMN IF NOT EXISTS retry_count" in schema

    source = (PROJECT_ROOT / "store" / "email_queue.py").read_text(encoding="utf-8")
    pending_query = source.split("def get_pending_emails", 1)[1]
    pending_query = pending_query.split("def ", 1)[0]
    assert "JOIN buildings b ON se.building_id = b.building_id" in pending_query


def test_database_reexports_cleanup_too():
    assert database.cleanup_finished_emails is email_queue.cleanup_finished_emails
