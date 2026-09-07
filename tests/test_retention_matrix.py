# SPDX-License-Identifier: AGPL-3.0-or-later
"""The retention matrix stays truthful against the catalog and the code (#530).

One row per catalog domain, the revocation-versus-deletion distinction
stated, and the horizons the code actually implements cited under the names
the code uses.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG = PROJECT_ROOT / "docs" / "data-catalog.md"
MATRIX = PROJECT_ROOT / "docs" / "retention-matrix.md"


def _catalog_domains():
    text = CATALOG.read_text(encoding="utf-8")
    return re.findall(r"^## (store/\S+)", text, flags=re.MULTILINE)


def test_every_catalog_domain_has_a_matrix_row():
    matrix = MATRIX.read_text(encoding="utf-8")
    missing = [domain for domain in _catalog_domains() if f"| {domain} |" not in matrix]
    assert not missing, f"matrix rows missing for: {missing}"


def test_revocation_is_stated_as_visibility_not_deletion():
    text = MATRIX.read_text(encoding="utf-8")
    assert "Revocation is not deletion" in text, (
        "the distinction between consent revocation (future visibility) and "
        "deletion (records) must be stated"
    )


def test_code_implemented_horizons_are_cited_by_their_code_names():
    text = MATRIX.read_text(encoding="utf-8")
    schema = (PROJECT_ROOT / "store" / "schema.py").read_text(encoding="utf-8")
    queue = (PROJECT_ROOT / "store" / "email_queue.py").read_text(encoding="utf-8")

    assert "EMAIL_QUEUE_RETENTION_DAYS = 90" in queue
    assert "EMAIL_QUEUE_RETENTION_DAYS = 90" in text, (
        "the queue's implemented horizon must be cited by its code name"
    )
    assert "confirm_profile_deletion" in text, (
        "the profile-deletion trigger must be cited at its seam"
    )
    assert "ON DELETE SET NULL" in schema, (
        "the metering-point detach behaviour the matrix describes is real"
    )


def test_overstated_promises_are_filed_not_hidden():
    text = MATRIX.read_text(encoding="utf-8")
    assert "Overstated promises" in text
    assert "unsubscribe.html" in text and "datenschutz.html" in text
    assert "filed" in text.lower()
