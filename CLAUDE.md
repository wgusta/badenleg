# CLAUDE.md

## Project

OpenLEG: open-source Swiss energy data API + LEG intelligence platform. Municipality-facing onboarding (B2G), resident smart meter data collection (B2C), aggregated intelligence for energy providers (B2B), public data API for developers. Flask + PostgreSQL + OpenClaw AI.

Tagline: Die Intelligenz hinter dem Netz.

## Architecture

Runs on Infomaniak VPS (83.228.223.66) via Docker Compose:
- **flask**: gunicorn on :5000, Python 3.11
- **postgres**: PostgreSQL 16, volume `postgres_data`
- **openclaw**: AI gateway on :18789 with MCP server (DB access)
- **caddy**: reverse proxy, auto TLS

Domains: `openleg.ch` (Flask), `*.openleg.ch` (multi-tenant municipalities), `api.openleg.ch` (Public API), `insights.openleg.ch` (B2B API), `openclaw.openleg.ch` (OpenClaw)

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app, all routes |
| `database.py` | PostgreSQL layer, 23+ tables, all CRUD |
| `public_data.py` | ElCom SPARQL, Energie Reporter, Sonnendach fetchers + computed metrics |
| `api_public.py` | Public REST API Blueprint (`/api/v1/*`), no auth, CORS |
| `api_b2b.py` | B2B API Blueprint: auth, rate limiting, data serving |
| `tenant.py` | Multi-tenant resolution: `*.openleg.ch` |
| `municipality.py` | Municipality onboarding + profil/verzeichnis pages |
| `meter_data.py` | Smart meter CSV parsing (EKZ format) |
| `insights_engine.py` | Aggregation: load profiles, solar index, flexibility |
| `formation_wizard.py` | LEG formation flow, financial model, business case |
| `ml_models.py` | DBSCAN clustering |
| `email_automation.py` | SMTP drip campaigns |
| `security_utils.py` | Input validation, sanitization |
| `data_enricher.py` | Geocoding (Swisstopo), energy profiles (BFE Sonnendach) |

## Deploy

```bash
# From local machine
rsync -avz --exclude='.git' --exclude='.env' --exclude='__pycache__' \
  -e "ssh -i ~/.ssh/infomaniak_badenleg" \
  /Users/gusta/Projects/badenleg/ \
  ubuntu@83.228.223.66:/opt/badenleg/

# On VPS
ssh -i ~/.ssh/infomaniak_badenleg ubuntu@83.228.223.66
cd /opt/badenleg && docker compose up -d --build flask
```

## Dev

```bash
# Local dev (needs .env with DATABASE_URL pointing to a Postgres instance)
python app.py  # runs on :5003

# Run tests
pytest tests/ -v
```

## Environment

All env vars in `.env` on VPS. See `.env.example`. `DATABASE_URL` set automatically in docker-compose.yml for flask and openclaw services.

## Admin

`/admin/overview` requires `ADMIN_TOKEN` header.

## Public API

`/api/v1/*` endpoints are open, no auth required. Rate limited 60/min per IP. CORS enabled. Docs at `/api/v1/docs`.

Key endpoints:
- `GET /api/v1/municipalities` - List with profiles
- `GET /api/v1/municipalities/<bfs>/tariffs` - ElCom tariffs
- `GET /api/v1/municipalities/<bfs>/leg-potential` - Value-gap analysis
- `POST /api/v1/leg/financial-model` - 10-year projections
- `GET /api/v1/rankings` - Ranked municipalities

## B2B API

`/api/insights/*` endpoints require `X-API-Key` header. Tiers: starter, professional, enterprise.

## Cron

- `POST /api/cron/refresh-public-data` (X-Cron-Secret) - Refresh ElCom + Energie Reporter + Sonnendach for ZH
- `POST /api/cron/process-emails` (X-Cron-Secret) - Process email queue
- `POST /api/cron/refresh-insights` (X-Cron-Secret) - Recompute B2B insights

## Data Sources (public, no PII)

| Source | Data | Update |
|--------|------|--------|
| ElCom (LINDAS SPARQL) | Electricity tariffs per operator/municipality | Yearly |
| BFE Sonnendach (opendata.swiss) | Solar potential per municipality | Periodic |
| Energie Reporter (opendata.swiss) | Solar, EV, heating, consumption per municipality | Quarterly |
| Swisstopo (api3.geo.admin.ch) | Address geocoding, PLZ | Real-time |
