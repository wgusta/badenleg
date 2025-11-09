# badenleg.ch - MVP

Ein "Blue Ocean" MVP für lokale Energiegemeinschaften (LEG/ZEV) in der Region Baden/Limmattal (Schweiz).

## Projektbeschreibung

badenleg.ch löst das "Henne-Ei-Problem" für die Gründung von lokalen Energiegemeinschaften durch einen zweistufigen "Interessen-Pool". Die Plattform ermöglicht es Nutzern, passende Energie-Partner in der Nachbarschaft zu finden, ohne sofortige Registrierung zu erfordern.

## Features

- **Map-First Design**: Interaktive Karte mit Leaflet.js
- **Mobile-First**: Optimiert für mobile Geräte
- **Speed-Optimiert**: Asynchrone ML-Analyse im Hintergrund
- **Blue Ocean Strategie**: Zweistufiger Interessen-Pool (anonym → registriert)
- **ML-basiertes Matching**: DBSCAN-Clustering für optimale Gemeinschaften
- **SMS-Benachrichtigungen**: Twilio-Integration für anonyme Nutzer

## Technologie-Stack

- **Backend**: Python (Flask)
- **ML**: Scikit-learn (DBSCAN), Pandas, Numpy
- **Frontend**: Single HTML-Datei mit Leaflet.js, TailwindCSS, Vanilla JavaScript
- **APIs**: Requests (für Opendata), Twilio (für SMS)
- **Geo-Daten**: geo.admin.ch, sonnendach.ch (simuliert für MVP)

## Setup & Installation

### 1. Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Twilio-Konfiguration (Optional)

Für SMS-Benachrichtigungen benötigen Sie ein Twilio-Konto:

1. Erstellen Sie ein (kostenloses) Twilio-Konto auf [twilio.com](https://www.twilio.com)
2. Holen Sie sich ACCOUNT_SID, AUTH_TOKEN und eine PHONE_NUMBER
3. Setzen Sie die Umgebungsvariablen:

```bash
# Linux/macOS
export TWILIO_ACCOUNT_SID='IHRE_SID'
export TWILIO_AUTH_TOKEN='IHR_TOKEN'
export TWILIO_PHONE_NUMBER='+41IHRENUMMER'

# Windows CMD
set TWILIO_ACCOUNT_SID=IHRE_SID
set TWILIO_AUTH_TOKEN=IHR_TOKEN
set TWILIO_PHONE_NUMBER=+41IHRENUMMER
```

**Hinweis**: Ohne Twilio-Konfiguration funktioniert die App, aber SMS-Benachrichtigungen werden nur simuliert (in der Konsole ausgegeben).

### 4. Anwendung starten

```bash
# Option 1: Mit Flask CLI
export FLASK_APP=app.py
flask run

# Option 2: Direkt mit Python
python app.py
```

Die Anwendung läuft dann auf [http://localhost:5002](http://localhost:5002)

## Projektstruktur

```
badenleg/
├── app.py                 # Flask-Backend (Haupt-Controller)
├── ml_models.py           # ML-Service (DBSCAN, Autarkie-Simulation)
├── data_enricher.py       # Opendata-Service (Geo-APIs, Mock-Daten)
├── requirements.txt        # Python-Dependencies
├── templates/
│   └── index.html         # Frontend (Single-Page-App)
└── README.md              # Diese Datei
```

## Nutzer-Flow

1. **Karte laden**: Nutzer öffnet badenleg.ch, Karte wird sofort geladen
2. **Marker laden**: Asynchron werden existierende Nutzer-Pins geladen
3. **Potenzial-Check**: Nutzer gibt Adresse ein und klickt "Prüfen"
4. **Backend-Anreicherung**: Adresse wird mit Opendata-APIs angereichert
5. **ML-Matching (FAST)**: Schnelle Geo-Distanz-Abfrage für provisorische Matches
6. **Interaktive Antwort**: 
   - **Szenario A**: Kein Match → "Anonymer Pool"-Popup
   - **Szenario B**: Match gefunden → "Registrieren"-Popup mit Partner-Pins
7. **Registrierung**: Nutzer registriert sich (anonym oder voll)
8. **Hintergrund-Task**: Langsame DBSCAN-Analyse läuft asynchron
9. **SMS-Trigger**: Bei neuem Match wird SMS an anonyme Nutzer gesendet

## API-Endpunkte

- `GET /` - Frontend (index.html)
- `GET /api/get_all_buildings` - Alle bekannten Gebäudepositionen
- `POST /api/check_potential` - Adresse prüfen und Matches finden
- `POST /api/register_anonymous` - Anonyme Registrierung (Pool)
- `POST /api/register_full` - Vollständige Registrierung
- `GET /confirm/<token>` - SMS-Bestätigungslink

## Entwicklung

### Mock-Modus

Die Anwendung verwendet standardmäßig `get_mock_energy_profile_for_address()` für schnelle Entwicklung. Um echte APIs zu verwenden, ändern Sie in `app.py`:

```python
# Zeile ~200: Von Mock zu Echt
estimates, profiles = data_enricher.get_energy_profile_for_address(address)
```

### Testing

Testen Sie den Flow mit verschiedenen Adressen in der Region Baden:
- "Stadtturm, 5400 Baden"
- "Bahnhofstrasse, 5430 Wettingen"
- "Limmattalstrasse, 5400 Baden"

## Lizenz

Dieses Projekt ist ein MVP für Demonstrationszwecke.

## Kontakt

Für Fragen oder Anregungen öffnen Sie bitte ein Issue.
