# Railway Deployment Setup

## Schritt 1: Railway Account erstellen

1. Gehe zu https://railway.app
2. Sign in mit GitHub (verbinde dein GitHub Account)
3. Klicke auf "New Project"

## Schritt 2: Projekt erstellen

1. Wähle "Deploy from GitHub repo"
2. Wähle das Repository `wgusta/badenleg`
3. Railway erstellt automatisch ein neues Projekt

## Schritt 3: Environment Variables setzen

Im Railway Dashboard → dein Projekt → Variables:

Füge diese Environment Variables hinzu:

```
FLASK_ENV=production
FLASK_DEBUG=False
APP_BASE_URL=https://www.badenleg.ch
SECRET_KEY=<generiere einen sicheren Key>
ALLOWED_HOSTS=badenleg.ch,www.badenleg.ch
```

**SECRET_KEY generieren:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Schritt 4: Railway Token und Service ID holen

### Railway Token:
1. Railway Dashboard → Account Settings → Tokens
2. "New Token" → Name: `github-actions-deploy`
3. Token kopieren (wird nur einmal angezeigt!)

### Service ID:
1. Railway Dashboard → dein Projekt
2. Klicke auf den Service (z.B. "badenleg")
3. Settings → General
4. Kopiere die "Service ID" (z.B. `abc123-def456-...`)

## Schritt 5: GitHub Secrets hinzufügen

Gehe zu: https://github.com/wgusta/badenleg/settings/secrets/actions

Füge diese Secrets hinzu:

- **RAILWAY_TOKEN**: Der Token aus Schritt 4
- **RAILWAY_SERVICE_ID**: Die Service ID aus Schritt 4

## Schritt 6: Custom Domain hinzufügen

1. Railway Dashboard → dein Projekt → Service → Settings → Networking
2. Klicke "Custom Domain"
3. Füge hinzu: `badenleg.ch` und `www.badenleg.ch`
4. Railway zeigt dir DNS-Einträge an

## Schritt 7: DNS konfigurieren

In deinem Domain-Manager (Infomaniak):

- **CNAME Record** für `badenleg.ch` → Railway zeigt dir den Wert (z.B. `xxx.up.railway.app`)
- **CNAME Record** für `www.badenleg.ch` → gleicher Wert

ODER (wenn Railway eine IP gibt):

- **A Record** für `badenleg.ch` → Railway IP
- **A Record** für `www.badenleg.ch` → Railway IP

## Schritt 8: Deployment testen

1. Push zu `main` Branch:
   ```bash
   git push origin main
   ```

2. GitHub Actions wird automatisch ausgelöst
3. Railway deployt automatisch
4. Nach 2-3 Minuten sollte die Site live sein

## Troubleshooting

### Deployment schlägt fehl:
- Prüfe Railway Logs: Dashboard → Service → Deployments → Logs
- Prüfe GitHub Actions Logs: Repository → Actions

### Domain funktioniert nicht:
- Prüfe DNS Propagation: https://dnschecker.org
- Warte 5-10 Minuten nach DNS-Änderung
- Prüfe Railway Custom Domain Status (muss "Active" sein)

### Environment Variables fehlen:
- Prüfe Railway Dashboard → Variables
- Stelle sicher, dass alle Variablen gesetzt sind

## Railway CLI (Optional)

Falls du lokal testen möchtest:

```bash
# Railway CLI installieren
npm i -g @railway/cli

# Login
railway login

# Link zum Projekt
railway link

# Lokal deployen (optional)
railway up
```

