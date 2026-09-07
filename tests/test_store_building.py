# SPDX-License-Identifier: AGPL-3.0-or-later
"""Interface tests for the building repository module (store.building).

Buildings are the registration record: one row per household that signed up.
This module owns their persistence and resolves the connection seam via
``database.get_connection`` at call time, so existing monkeypatches keep working
and ``database`` re-exports the identical objects for legacy callers
(``import database as db; db.get_building()``).
"""

import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import database
from store import building

REEXPORTED = (
    "save_building",
    "get_building",
    "get_building_by_email",
    "get_all_buildings",
    "get_all_building_profiles",
    "get_operator_building_profiles",
    "delete_building",
    "update_building_verified",
    "get_neighbor_count_near",
    "get_building_for_dashboard",
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
        self.commits = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1


def _conn_ctx(cursor):
    @contextmanager
    def _factory():
        yield _FakeConnection(cursor)

    return _factory


def test_database_reexports_are_identical_objects():
    for name in REEXPORTED:
        assert getattr(database, name) is getattr(building, name), name


def test_the_neighbour_box_constant_moves_with_the_query():
    assert building.NEIGHBOR_BOX_HALF_WIDTH_KM == 0.5
    assert database.NEIGHBOR_BOX_HALF_WIDTH_KM == building.NEIGHBOR_BOX_HALF_WIDTH_KM


def test_store_building_imports_without_database_bootstrap():
    result = subprocess.run(
        [sys.executable, "-c", "import store.building; print('ok')"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_get_building_uses_the_database_connection_seam(monkeypatch):
    """Patching database.get_connection must reach the store, not a stale binding."""
    cur = _FakeCursor(one={"building_id": "b1", "email": "a@example.ch"})
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert building.get_building("b1") == {
        "building_id": "b1",
        "email": "a@example.ch",
    }
    query, params = cur.executed[0]
    assert "FROM buildings" in query
    assert params == ("b1",)


def test_get_building_returns_none_when_the_row_is_absent(monkeypatch):
    monkeypatch.setattr(database, "get_connection", _conn_ctx(_FakeCursor(one=None)))

    assert building.get_building("missing") is None


def test_get_building_by_email_returns_every_registration(monkeypatch):
    rows = [{"building_id": "b1"}, {"building_id": "b2"}]
    monkeypatch.setattr(database, "get_connection", _conn_ctx(_FakeCursor(rows=rows)))

    assert building.get_building_by_email("a@example.ch") == rows


def test_delete_building_reports_whether_a_row_went(monkeypatch):
    monkeypatch.setattr(database, "get_connection", _conn_ctx(_FakeCursor(rowcount=1)))
    assert building.delete_building("b1") is True

    monkeypatch.setattr(database, "get_connection", _conn_ctx(_FakeCursor(rowcount=0)))
    assert building.delete_building("b1") is False


def test_update_building_verified_reports_whether_a_row_changed(monkeypatch):
    cur = _FakeCursor(rowcount=1)
    monkeypatch.setattr(database, "get_connection", _conn_ctx(cur))

    assert building.update_building_verified("b1") is True
    _query, params = cur.executed[0]
    assert params == (True, "b1")


def test_a_broken_connection_never_leaks_the_exception(monkeypatch):
    @contextmanager
    def _broken():
        raise RuntimeError("db down")
        yield

    monkeypatch.setattr(database, "get_connection", _broken)

    assert building.get_building("b1") is None
    assert building.get_building_by_email("a@example.ch") == []
    assert building.get_all_buildings() == []
    assert building.get_all_building_profiles() == []
    assert building.get_operator_building_profiles() == []
    assert building.delete_building("b1") is False
    assert building.update_building_verified("b1") is False
    assert building.get_building_for_dashboard("b1") is None


def test_consent_gated_reads_carry_their_covering_indexes():
    """The measured covering indexes (#525) exist; the gate predicate stays
    byte-identical - an inner join on the live consent value."""
    schema = (Path(__file__).resolve().parent.parent / "store" / "schema.py").read_text(
        encoding="utf-8"
    )
    assert "idx_buildings_city_verified_latlon" in schema
    assert "ON buildings (city_id, verified, lat, lon)" in schema
    assert "idx_consents_share" in schema
    assert "ON consents (building_id) WHERE share_with_neighbors = TRUE" in schema
    source = (
        Path(__file__).resolve().parent.parent / "store" / "building.py"
    ).read_text(encoding="utf-8")
    assert source.count("c.share_with_neighbors = TRUE") >= 6, (
        "the gate predicate must stay in every branch of every gated read"
    )
