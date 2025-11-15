# Railway Volume Setup - Schritt für Schritt

## Problem
Die Daten werden bei jedem Railway-Neustart gelöscht, weil sie in In-Memory-Dictionaries gespeichert werden.

## Lösung: Persistent Volume

Die Anwendung verwendet jetzt ein **Railway Persistent Volume** zur Datenspeicherung.

---

## Schritt 1: Volume in Railway erstellen

1. Gehe zu deinem Railway Dashboard: https://railway.app
2. Wähle dein Projekt aus
3. Klicke auf deinen **Service** (z.B. "badenleg")
4. Gehe zum Tab **"Volumes"**
5. Klicke **"New Volume"**
6. **Mount Path:** `/data`
7. **Size:** 1GB (oder mehr je nach Bedarf)
8. Klicke **"Create"**

**Wichtig:** Der Mount Path muss genau `/data` sein, da die Anwendung diesen Pfad verwendet.

---

## Schritt 2: Environment Variable setzen (Optional)

Falls du einen anderen Pfad verwenden möchtest:

1. Railway Dashboard → Dein Projekt → Variables
2. Füge hinzu:
   ```
   DATA_DIR=/data
   ```
3. Klicke "Add"

**Standard:** Wenn `DATA_DIR` nicht gesetzt ist, verwendet die Anwendung automatisch `/data`.

---

## Schritt 3: Deployment testen

1. **Deploye die Anwendung:**
   ```bash
   git push origin main
   ```

2. **Prüfe die Logs:**
   - Railway Dashboard → Service → Deployments → Logs
   - Suche nach: `[PERSISTENCE] Daten geladen` oder `[PERSISTENCE] Keine bestehende Datenbank gefunden`

3. **Teste Persistenz:**
   - Registriere einen Test-User
   - Starte den Service neu (Railway Dashboard → Service → Settings → Restart)
   - Prüfe, ob die Daten noch vorhanden sind

---

## Wie es funktioniert

- **Beim Start:** Die Anwendung lädt automatisch alle Daten aus `/data/database.json`
- **Bei Änderungen:** Daten werden automatisch nach 5 Sekunden gespeichert (Debouncing)
- **Backup:** Bei jedem Speichern wird ein Backup erstellt: `/data/database.backup.json`
- **Thread-safe:** Alle Speichervorgänge sind thread-safe

---

## Troubleshooting

### Daten werden nicht gespeichert

**Prüfe:**
1. Ist das Volume korrekt gemountet?
   - Railway Dashboard → Service → Volumes → Prüfe Mount Path
2. Hat der Service Schreibrechte?
   - Prüfe Railway Logs auf Fehler: `[PERSISTENCE] Fehler beim Speichern`
3. Ist genug Speicherplatz vorhanden?
   - Railway Dashboard → Volumes → Prüfe Size

### Daten gehen verloren

**Mögliche Ursachen:**
1. Volume wurde nicht erstellt oder nicht gemountet
2. Service läuft auf einem anderen Container (Railway verteilt Workloads)
3. Volume wurde gelöscht

**Lösung:**
- Prüfe, ob das Volume existiert und gemountet ist
- Erstelle ein neues Volume falls nötig
- Nutze die Backup-Funktion von Railway (Railway Dashboard → Volumes → Backups)

---

## Backup-Strategie

### Automatische Backups
Railway erstellt automatisch Backups von Volumes. Du kannst:
- Manuelle Backups erstellen: Railway Dashboard → Volumes → Backups → "Create Backup"
- Automatische Backups planen: Railway Dashboard → Volumes → Backups → "Schedule Backup"

### Lokale Backups
Die Anwendung erstellt bei jedem Speichern ein Backup: `/data/database.backup.json`

---

## Monitoring

**Logs prüfen:**
```bash
# Railway Dashboard → Service → Logs
# Suche nach:
[PERSISTENCE] Daten geladen: X Gebäude, Y Interessenten
[PERSISTENCE] Daten gespeichert: X Gebäude, Y Interessenten
```

**Volume-Status:**
- Railway Dashboard → Volumes → Prüfe "Size" und "Used"

---

## Weitere Informationen

Siehe auch: `RAILWAY_PERSISTENCE.md` für technische Details und alternative Lösungen.

