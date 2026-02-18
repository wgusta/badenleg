# Deployment Guide

## Infrastructure

Infomaniak VPS (83.228.223.66), Docker Compose, Caddy with auto TLS.

SSH: `ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66`

## Services

| Service | Image | Port | Domain |
|---------|-------|------|--------|
| flask | Custom (Python 3.11) | 5000 | badenleg.ch |
| postgres | postgres:16-alpine | 5432 | internal |
| openclaw | Custom (Node) | 18789 | openclaw.badenleg.ch |
| caddy | caddy:latest | 80, 443 | reverse proxy |

## Deploy Changes

```bash
# Sync files to VPS
rsync -avz --exclude='.git' --exclude='.env' --exclude='__pycache__' \
  -e "ssh -i ~/.ssh/infomaniak_badenleg" \
  /Users/gusta/Projects/badenleg/ \
  root@83.228.223.66:/opt/badenleg/

# Rebuild and restart
ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66 \
  "cd /opt/badenleg && docker compose up -d --build"
```

To rebuild only flask: `docker compose up -d --build flask`

## First Time Setup

1. Provision VPS, install Docker
2. Create `/opt/badenleg/` directory
3. rsync project files
4. Create `.env` from `.env.example` with real secrets
5. `docker compose up -d`
6. Verify: `curl https://badenleg.ch`

## Database

PostgreSQL 16, data in Docker volume `postgres_data`.

Tables auto-created by `database.py:init_db()` on first Flask boot.

### Backup

```bash
ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66 \
  "docker exec badenleg-postgres pg_dump -U badenleg badenleg" > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
cat backup.sql | ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66 \
  "docker exec -i badenleg-postgres psql -U badenleg badenleg"
```

## Data Migration from Railway

```bash
# 1. Dump from Railway
pg_dump "RAILWAY_DATABASE_URL" > railway_dump.sql

# 2. Copy to VPS
scp -i ~/.ssh/infomaniak_badenleg railway_dump.sql root@83.228.223.66:/tmp/

# 3. Restore into container
ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66 \
  "docker exec -i badenleg-postgres psql -U badenleg badenleg < /tmp/railway_dump.sql"

# 4. Verify row counts
ssh -i ~/.ssh/infomaniak_badenleg root@83.228.223.66 \
  "docker exec badenleg-postgres psql -U badenleg badenleg -c 'SELECT schemaname, relname, n_live_tup FROM pg_stat_user_tables ORDER BY relname;'"
```

## DNS

A records pointing to 83.228.223.66:
- `badenleg.ch`
- `www.badenleg.ch`
- `openclaw.badenleg.ch`

Caddy handles TLS certificates automatically.

## Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f flask
docker compose logs -f postgres
```

## Troubleshooting

```bash
# Check container health
docker compose ps

# Restart all
docker compose restart

# Rebuild from scratch
docker compose down && docker compose up -d --build

# Check postgres connectivity
docker exec badenleg-postgres pg_isready -U badenleg
```

## Verification Checklist

- [ ] `curl https://badenleg.ch` returns landing page
- [ ] `curl https://openclaw.badenleg.ch` returns WebChat UI
- [ ] `/admin/overview` works with ADMIN_TOKEN
- [ ] Address autocomplete works
- [ ] Registration flow completes
- [ ] Email confirmation sends
- [ ] Caddy logs show TLS certs issued
