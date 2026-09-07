# SPDX-License-Identifier: AGPL-3.0-or-later
"""The data catalog stays truthful against the schema (#516).

Every store domain has a catalog section, and the field names the catalog
cites are real schema names. If a field is renamed or a section drifts, this
test fails instead of letting the catalog rot.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG = PROJECT_ROOT / "docs" / "data-catalog.md"
SCHEMA = PROJECT_ROOT / "store" / "schema.py"

# Store modules a maintainer can touch; each must have a catalog section.
# schema.py owns the DDL itself and __init__/api_client are covered by their
# own sections; api_client IS a store module and appears in the list.
STORE_MODULES = [
    path.stem
    for path in sorted((PROJECT_ROOT / "store").glob("*.py"))
    if path.stem not in ("__init__", "schema")
]


def test_every_store_domain_has_a_catalog_section():
    text = CATALOG.read_text(encoding="utf-8")
    missing = [name for name in STORE_MODULES if f"## store/{name}" not in text]
    assert not missing, f"catalog sections missing for: {missing}"


def test_cited_personal_fields_are_real_schema_names():
    text = CATALOG.read_text(encoding="utf-8")
    schema = SCHEMA.read_text(encoding="utf-8")
    # The fields this catalog exists to describe; each must exist in the
    # schema the store modules own.
    critical = (
        "building_id",
        "share_with_neighbors",
        "share_with_utility",
        "consent_version",
        "annual_consumption_kwh",
        "potential_pv_kwp",
        "total_kwh",
        "metering_point_id",
        "internal_price_chf_per_kwh",
        "policy_snapshot",
        "template_key",
        "retry_count",
        "token_hash",
        "event_type",
        "community_id",
        "referrer_id",
        "revoked_at",
        "window_start",
    )
    for field in critical:
        assert field in schema, f"{field} is not a schema name"
        assert f"`{field}`" in text, f"the catalog must cite {field}"


def test_the_data_policy_is_stated_where_it_binds():
    text = CATALOG.read_text(encoding="utf-8")
    for phrase in (
        "stays within each LEG",
        "never sold",
        "never aggregated for third parties",
    ):
        assert phrase in text, f"the binding data policy must state: {phrase}"
    # The domains that hold meter-adjacent data must sit under the policy.
    for domain in ("store/metering", "store/meter", "store/building"):
        section = text.split(f"## {domain}", 1)[1].split("## store/", 1)[0]
        assert "never sold" in section or "citizen meter data" in section.lower(), (
            f"{domain} must carry the binding policy statement"
        )


def test_every_consent_gated_domain_names_its_gate():
    text = CATALOG.read_text(encoding="utf-8")
    for domain in ("store/building", "store/referral", "store/formation"):
        section = text.split(f"## {domain}", 1)[1].split("## store/", 1)[0]
        assert "share_with_neighbors" in section or "pinned by #518" in section, (
            f"{domain} must name its consent gate"
        )
