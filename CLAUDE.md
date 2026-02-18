# CLAUDE.md

## Project

BadenLEG: platform helping Baden (CH) residents form Local Electricity Communities (LEG) starting 2026. Flask + PostgreSQL + OpenClaw AI assistant.

## Architecture

Runs on Infomaniak VPS (83.228.223.66) via Docker Compose:
- **flask**: gunicorn on :5000, Python 3.11
- **postgres**: PostgreSQL 16, volume `postgres_data`
- **openclaw**: AI gateway on :18789 with MCP server (DB access)
- **caddy**: reverse proxy, auto TLS

Domains: `badenleg.ch` (Flask), `openclaw.badenleg.ch` (OpenClaw)

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app, all routes |
| `database.py` | PostgreSQL layer, `init_db()` creates 14 tables |
| `formation_wizard.py` | LEG formation flow |
| `ml_models.py` | DBSCAN clustering |
| `email_automation.py` | SendGrid drip campaigns |
| `security_utils.py` | Input validation, sanitization |
| `token_persistence.py` | JSON fallback token storage |
| `data_enricher.py` | Geocoding, energy profiles |

## Deploy

```bash
# From local machine
rsync -avz --exclude='.git' --exclude='.env' --exclude='__pycache__' \
  -e "ssh -i ~/.ssh/infomaniak_badenleg" \
  /Users/gusta/Projects/badenleg/ \
  root@83.228.223.66:/opt/badenleg/

# On VPS
ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66
cd /opt/badenleg && docker compose up -d --build flask
```

## Dev

```bash
# Local dev (needs .env with DATABASE_URL pointing to a Postgres instance)
python app.py  # runs on :5003
```

## Environment

All env vars in `.env` on VPS. See `.env.example`. `DATABASE_URL` set automatically in docker-compose.yml for flask and openclaw services.

## Admin

`/admin/overview` requires `ADMIN_TOKEN` header.
