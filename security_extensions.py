# SPDX-License-Identifier: AGPL-3.0-or-later
"""Shared Flask security extensions used across blueprints."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Surface classes (#524). Jede Klasse hat eine benannte Grenze mit Begründung;
# Routen dekorieren mit diesen Konstanten, nie mit magischen Strings.
#
# ANONYMOUS_READ: oeffentliche Leseflaechen (Verzeichnisse, Rangliste,
# Gemeindeprofile, API-Doku, oeffentliche API-GETs). Grosszuegig: kein
# Mensch und kein geteiltes Frontend stoesst hier an; Scraping- und
# Missbrauchsmuster schon.
RATE_LIMIT_ANONYMOUS_READ = "240 per minute"
# CALCULATOR: Rechen-POSTs, die pro Anfrage Geoencoder- oder Datenabfragen
# ausloesen koennen. Enger, aber weit ueber interaktiver Nutzung.
RATE_LIMIT_CALCULATOR = "30 per minute"
# RETRY_HINT (#524): die kuerzeste angewandte Regelung gouverniert; ein
# frueher Retry-after kann hoechstens eine weitere 429 kosten.
RATE_LIMIT_RETRY_AFTER_SECONDS = 60

limiter = Limiter(
    get_remote_address,
    default_limits=["500 per hour"],
    strategy="fixed-window",
    # Fail open (#524, im Einklang mit #529): ist der Speicher (Redis)
    # unerreichbar, weicht der Limiter auf prozesslokalen Speicher aus,
    # statt Anfragen fehlschlagen zu lassen. Ein Bewohner wird nie wegen
    # eines Cache-Ausfalls ausgesperrt.
    in_memory_fallback_enabled=True,
)


def rate_limit(rule: str):
    """Decorate a route with a required Flask-Limiter rule."""
    return limiter.limit(rule)
