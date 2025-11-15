# Railway Daten-Persistenz: Lösungsvorschläge

## Problem
Die Daten werden bei jedem Railway-Neustart gelöscht, weil die Daten aktuell in **In-Memory-Dictionaries** gespeichert werden:
- `DB_BUILDINGS = {}`
- `DB_INTEREST_POOL = {}`
- `DB_VERIFICATION_TOKENS = {}`
- `DB_UNSUBSCRIBE_TOKENS = {}`
- `CLUSTER_CONTACT_STATE = {}`
- `DB_CLUSTERS = {}`

Railway Container sind **ephemeral** - alle Daten im Container-Dateisystem gehen bei Neustart/Deployment verloren.

---

## Lösung 1: Railway PostgreSQL Database Service (EMPFOHLEN)

**Quelle:** [Railway PostgreSQL Documentation](https://docs.railway.com/databases/postgresql)

### Vorteile:
- ✅ Professionelle, skalierbare Lösung
- ✅ Automatische Backups
- ✅ ACID-konform, transaktionssicher
- ✅ Gute Performance bei vielen Daten
- ✅ Railway verwaltet alles (Updates, Backups, etc.)
- ✅ Kostenlos im Hobby-Plan (bis 5GB)

### Nachteile:
- ⚠️ Erfordert Code-Änderungen (SQLAlchemy/Migrations)
- ⚠️ Etwas mehr Setup-Aufwand

### Implementierung:

#### Schritt 1: PostgreSQL Service in Railway hinzufügen
1. Railway Dashboard → Dein Projekt
2. Klicke "New" → "Database" → "Add PostgreSQL"
3. Railway erstellt automatisch eine PostgreSQL-Datenbank
4. Railway setzt automatisch `DATABASE_URL` als Environment Variable

#### Schritt 2: Dependencies hinzufügen
```bash
# requirements.txt erweitern:
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.1.1
alembic==1.12.1  # Für Migrations
```

#### Schritt 3: Code-Anpassungen
```python
# app.py - Beispiel-Struktur
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, JSON, DateTime, Integer
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

# Database URL von Railway
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Models
class Building(db.Model):
    __tablename__ = 'buildings'
    building_id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    phone = Column(String)
    profile = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InterestPool(db.Model):
    __tablename__ = 'interest_pool'
    building_id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    phone = Column(String)
    profile = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Initialisierung
with app.app_context():
    db.create_all()
```

#### Schritt 4: Migration erstellen
```bash
# Alembic Setup
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**Dokumentation:**
- [Railway PostgreSQL Guide](https://docs.railway.com/databases/postgresql)
- [Railway Database Connection](https://docs.railway.com/guides/postgresql)

---

## Lösung 2: Railway Persistent Volume mit JSON-Datei

**Quelle:** [Railway Volumes Documentation](https://docs.railway.com/guides/volumes)

### Vorteile:
- ✅ Minimaler Code-Änderungsaufwand
- ✅ Schnell implementierbar
- ✅ Keine zusätzlichen Dependencies
- ✅ Funktioniert mit bestehendem Code-Struktur

### Nachteile:
- ⚠️ Nicht so robust wie PostgreSQL (keine Transaktionen)
- ⚠️ Manuelle Backup-Strategie nötig
- ⚠️ Performance kann bei vielen Daten leiden
- ⚠️ Keine automatischen Backups (muss manuell konfiguriert werden)

### Implementierung:

#### Schritt 1: Volume in Railway erstellen
1. Railway Dashboard → Dein Projekt → Service
2. Gehe zu "Volumes" Tab
3. Klicke "New Volume"
4. **Mount Path:** `/data` (oder `/app/data`)
5. **Size:** 1GB (oder mehr je nach Bedarf)
6. Klicke "Create"

#### Schritt 2: Code-Anpassungen
```python
# app.py - Persistenz-Layer hinzufügen
import json
import os
from pathlib import Path

# Persistenz-Pfad (Railway Volume)
DATA_DIR = Path(os.getenv('DATA_DIR', '/data'))
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / 'database.json'
BACKUP_FILE = DATA_DIR / 'database.backup.json'

# Lade Daten beim Start
def load_database():
    """Lädt Daten aus JSON-Datei"""
    global DB_BUILDINGS, DB_INTEREST_POOL, DB_VERIFICATION_TOKENS, DB_UNSUBSCRIBE_TOKENS, CLUSTER_CONTACT_STATE, DB_CLUSTERS
    
    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                DB_BUILDINGS = data.get('buildings', {})
                DB_INTEREST_POOL = data.get('interest_pool', {})
                DB_VERIFICATION_TOKENS = data.get('verification_tokens', {})
                DB_UNSUBSCRIBE_TOKENS = data.get('unsubscribe_tokens', {})
                CLUSTER_CONTACT_STATE = {k: set(v) for k, v in data.get('cluster_contact_state', {}).items()}
                DB_CLUSTERS = data.get('clusters', {})
                logger.info(f"[PERSISTENCE] Daten geladen: {len(DB_BUILDINGS)} Gebäude, {len(DB_INTEREST_POOL)} Interessenten")
        except Exception as e:
            logger.error(f"[PERSISTENCE] Fehler beim Laden: {e}")
            # Fallback: Leere Datenstrukturen
            DB_BUILDINGS = {}
            DB_INTEREST_POOL = {}
            DB_VERIFICATION_TOKENS = {}
            DB_UNSUBSCRIBE_TOKENS = {}
            CLUSTER_CONTACT_STATE = {}
            DB_CLUSTERS = {}
    else:
        logger.info("[PERSISTENCE] Keine bestehende Datenbank gefunden, starte mit leeren Daten")

def save_database():
    """Speichert Daten in JSON-Datei (thread-safe)"""
    try:
        # Backup erstellen
        if DB_FILE.exists():
            import shutil
            shutil.copy(DB_FILE, BACKUP_FILE)
        
        # Daten serialisieren (Sets zu Listen konvertieren)
        data = {
            'buildings': DB_BUILDINGS,
            'interest_pool': DB_INTEREST_POOL,
            'verification_tokens': DB_VERIFICATION_TOKENS,
            'unsubscribe_tokens': DB_UNSUBSCRIBE_TOKENS,
            'cluster_contact_state': {k: list(v) for k, v in CLUSTER_CONTACT_STATE.items()},
            'clusters': DB_CLUSTERS,
            'last_saved': time.time()
        }
        
        # Atomisches Schreiben (erst temp, dann rename)
        temp_file = DB_FILE.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        temp_file.replace(DB_FILE)
        logger.debug(f"[PERSISTENCE] Daten gespeichert: {len(DB_BUILDINGS)} Gebäude, {len(DB_INTEREST_POOL)} Interessenten")
    except Exception as e:
        logger.error(f"[PERSISTENCE] Fehler beim Speichern: {e}")

# Beim Start laden
load_database()

# Auto-Save nach Änderungen (mit Debouncing)
_save_timer = None
def schedule_save():
    """Plant Speicherung nach kurzer Verzögerung"""
    global _save_timer
    if _save_timer:
        _save_timer.cancel()
    _save_timer = threading.Timer(5.0, save_database)  # 5 Sekunden Verzögerung
    _save_timer.daemon = True
    _save_timer.start()

# Nach jeder Datenänderung aufrufen:
# schedule_save()
```

#### Schritt 3: Auto-Save in bestehende Funktionen integrieren
```python
# Beispiel: In register_anonymous und register_full
DB_INTEREST_POOL[building_id] = entry
schedule_save()  # ← Hinzufügen

DB_BUILDINGS[building_id] = entry
schedule_save()  # ← Hinzufügen
```

#### Schritt 4: Backup-Strategie (Optional)
```python
# Periodisches Backup (täglich)
def create_backup():
    """Erstellt tägliches Backup"""
    if DB_FILE.exists():
        backup_name = DATA_DIR / f'database.backup.{int(time.time())}.json'
        import shutil
        shutil.copy(DB_FILE, backup_name)
        logger.info(f"[BACKUP] Backup erstellt: {backup_name}")

# Scheduler (z.B. mit APScheduler oder threading)
```

**Dokumentation:**
- [Railway Volumes Guide](https://docs.railway.com/guides/volumes)
- [Railway Volume Backups](https://docs.railway.com/reference/backups)

---

## Vergleich

| Feature | PostgreSQL | Persistent Volume |
|---------|-----------|-------------------|
| Setup-Aufwand | Mittel | Niedrig |
| Code-Änderungen | Hoch | Niedrig |
| Skalierbarkeit | Hoch | Niedrig |
| Performance | Sehr gut | Gut (bei kleinen Daten) |
| Backups | Automatisch | Manuell |
| Transaktionen | ✅ | ❌ |
| Kosten | Kostenlos (Hobby) | Kostenlos (Hobby) |
| Empfohlen für | Produktion | Prototyp/kleine Daten |

---

## Empfehlung

**Für Produktion:** Lösung 1 (PostgreSQL) - professionell, skalierbar, automatische Backups

**Für schnelle Implementierung:** Lösung 2 (Persistent Volume) - minimaler Aufwand, funktioniert sofort

---

## Nächste Schritte

1. Entscheide dich für eine Lösung
2. Implementiere die gewählte Lösung
3. Teste lokal
4. Deploye zu Railway
5. Teste Persistenz (Neustart des Services)

