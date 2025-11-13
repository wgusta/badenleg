# Railway Deployment Checkliste

## ✅ Bereits erledigt

1. **GitHub Repository**
   - [x] Develop und Main Branches erstellt
   - [x] GitHub Actions Workflow `.github/workflows/deploy.yml` erstellt
   - [x] Railway CLI in Workflow integriert

2. **Railway-spezifische Dateien**
   - [x] `Procfile` erstellt (`web: gunicorn app:app`)
   - [x] `railway.toml` erstellt
   - [x] `requirements.txt` mit allen Dependencies (inkl. `requests`)

3. **Security vereinfacht für Railway**
   - [x] File-Logging deaktiviert (nur StreamHandler)
   - [x] Talisman auf Minimum reduziert (kein force_https, keine CSP)
   - [x] Rate Limiting vereinfacht (500 req/hour, memory storage)
   - [x] Nur minimal Header: X-Content-Type-Options

4. **Code-Anpassungen**
   - [x] `APP_BASE_URL` auf `https://www.badenleg.ch` geändert
   - [x] Railway handled HTTPS am Edge (force_https=False)
   - [x] Alle Talisman-Argumente entfernt die Fehler verursachen

## 🚀 Deployment Steps

### 1. Railway Account & Projekt
- [ ] Railway Account erstellt (https://railway.app)
- [ ] GitHub mit Railway verbunden
- [ ] Neues Projekt erstellt: "Deploy from GitHub repo"
- [ ] Repository `wgusta/badenleg` ausgewählt

### 2. Environment Variables in Railway
Gehe zu: Railway Dashboard → Projekt → Variables

Setze diese Variablen:
```
FLASK_ENV=production
FLASK_DEBUG=False
APP_BASE_URL=https://www.badenleg.ch
SECRET_KEY=<von Terminal generiert>
ALLOWED_HOSTS=badenleg.ch,www.badenleg.ch
```

**SECRET_KEY generieren:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Railway Token & Service ID für GitHub Actions

#### Railway Token holen:
1. Railway Dashboard → Account Settings → Tokens
2. "New Token" → Name: `github-actions-deploy`
3. Token kopieren (wird nur einmal angezeigt!)

#### Service ID holen:
1. Railway Dashboard → dein Projekt
2. Klicke auf den Service (z.B. "badenleg")
3. Settings → General
4. Kopiere die "Service ID"

### 4. GitHub Secrets setzen
Gehe zu: GitHub → Repository → Settings → Secrets and variables → Actions

Füge hinzu:
- **RAILWAY_TOKEN**: `<dein Railway Token>`
- **RAILWAY_SERVICE_ID**: `<deine Service ID>`

### 5. Custom Domain in Railway
1. Railway Dashboard → Projekt → Service → Settings
2. "Domains" → "Custom Domain"
3. Domain eingeben: `www.badenleg.ch`
4. Railway zeigt CNAME-Wert an (z.B. `xxx.up.railway.app`)

### 6. DNS bei Infomaniak
Gehe zu: Infomaniak → Domains → badenleg.ch → DNS

**CNAME Record für www:**
- **Typ**: CNAME
- **Name/Host**: `www`
- **Ziel/Value**: `<Railway CNAME Wert>` (z.B. `xxx.up.railway.app`)
- **TTL**: 300 (5 min)

**Weiterleitung badenleg.ch → www.badenleg.ch:**
- Domain-Manager → Weiterleitungen → Neue Weiterleitung
- Von: `badenleg.ch` (leer oder `@`)
- Nach: `https://www.badenleg.ch`
- Typ: 301 (permanent)

### 7. Deployment testen
```bash
# Trigger Deployment
git commit --allow-empty -m "Trigger Railway deployment"
git push origin main
```

**Prüfen:**
1. GitHub Actions → "Deploy to Railway" → grüner Haken?
2. Railway Dashboard → Deployments → Status "Running"?
3. Railway Logs → Keine Fehler?
4. https://www.badenleg.ch/ → Website lädt?
5. https://www.badenleg.ch/health → JSON Response?

## 🐛 Troubleshooting

### Deployment schlägt fehl
- **GitHub Actions Logs prüfen**: Sind `RAILWAY_TOKEN` und `RAILWAY_SERVICE_ID` gesetzt?
- **Railway Logs prüfen**: Welcher Fehler tritt auf?
- **Module fehlen**: `requirements.txt` aktualisieren und pushen

### Website nicht erreichbar
- **DNS Propagation**: Kann 5-30 Minuten dauern
- **Railway Domain Settings**: Ist `www.badenleg.ch` als Custom Domain eingetragen?
- **CNAME korrekt**: Prüfe mit `dig www.badenleg.ch` oder https://mxtoolbox.com/

### 500 Error / Application Crash
- **Railway Logs**: Deploy Logs für Python Errors checken
- **Environment Variables**: Sind alle gesetzt? `SECRET_KEY`?
- **APP_BASE_URL**: Stimmt mit Custom Domain überein?

## 📝 Nach erfolgreichem Deployment

- [ ] Registrierung testen: Adresse eingeben, Email erhalten?
- [ ] Bestätigungslink testen: Token-Validierung funktioniert?
- [ ] Map laden: Marker erscheinen?
- [ ] Alle Sub-Pages testen: `/leg`, `/evl`, `/zev`, `/vergleich-leg-evl-zev`
- [ ] Impressum & Datenschutz Links funktionieren?
- [ ] Kontakt-Link öffnet Email?
- [ ] Abmelde-Flow testen?

## 🎯 Domain-Weiterleitung

Da du **nur www.badenleg.ch** nutzen möchtest:
- Setze **nur** den CNAME für `www`
- Richte Weiterleitung für Root-Domain ein (siehe Schritt 6)
- Railway Custom Domain: **nur** `www.badenleg.ch` (nicht die Root-Domain)

