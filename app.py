import os
import time
import uuid
import threading # NEU: Für asynchrone Tasks
from flask import Flask, request, jsonify, render_template, redirect
from twilio.rest import Client
import pandas as pd
import numpy as np # NEU: Für Distanzberechnung
try:
    from scipy.spatial import ConvexHull
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("[WARNUNG] scipy nicht verfügbar, verwende einfache Polygon-Generierung")

# --- Import unserer ML- und Geo-Logik ---
import data_enricher
import ml_models

# --- App-Konfiguration ---
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# --- Twilio SMS-Konfiguration ---
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'DEIN_ACCOUNT_SID_HIER')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'DEIN_AUTH_TOKEN_HIER')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+41000000000')
APP_BASE_URL = "http://localhost:5003" # Basis-URL für Bestätigungslinks

if TWILIO_ACCOUNT_SID != 'DEIN_ACCOUNT_SID_HIER':
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("[INIT] Twilio SMS-Service ist KONFIGURIERT.")
else:
    twilio_client = None
    print("[INIT] WARNUNG: Twilio SMS-Service ist NICHT konfiguriert.")


# --- Simulierte In-Memory-Datenbank ---
DB_BUILDINGS = {} # Vollständig registrierte Gebäude
DB_INTEREST_POOL = {} # Anonyme Interessenten (Schlüssel: building_id)
DB_MATCH_TOKENS = {} # Temporäre Tokens für SMS-Bestätigung

# --- NEU: Cache für ML-Ergebnisse ---
# Hält das Ergebnis des letzten langsamen ML-Laufs
DB_CLUSTERS = {} # z.B. {'building_abc': 1, 'building_xyz': 1}
DB_CLUSTER_INFO = {} # z.B. {1: {'autarky_percent': 75.2, ...}}
db_lock = threading.Lock() # Verhindert Race Conditions

print(f"[INIT] Leere Datenbank und ML-Cache initialisiert.")


# --- Kernfunktionen ---

def send_sms_notification(phone_number, cluster_id, autarky_score, notification_type='match'):
    """
    Sendet die SMS-Benachrichtigung an einen anonymen Nutzer.
    notification_type: 'match' (Match gefunden) oder 'new_member' (Neues Mitglied im Cluster)
    """
    # 1. Einzigartigen Bestätigungs-Token erstellen (nur für 'match')
    token = None
    building_id = None
    
    if notification_type == 'match':
        token = str(uuid.uuid4())
        # Finde die building_id, die zu dieser Telefonnummer gehört
        building_id = next((bid for bid, data in DB_INTEREST_POOL.items() if data['phone'] == phone_number), None)
        
        if not building_id:
            return # Sollte nicht passieren

        # Token speichern, damit wir wissen, wer bestätigt hat
        with db_lock:
            DB_MATCH_TOKENS[token] = {
                'building_id': building_id,
                'cluster_id': cluster_id
            }
    
    if notification_type == 'match':
        confirmation_url = f"{APP_BASE_URL}/confirm/{token}"
        message_body = (
            f"Gute Neuigkeiten von 'badenleg.ch'! \n\n"
            f"Wir haben einen passenden Energie-Partner in Ihrer Nachbarschaft gefunden "
            f"(Potenzielle Autarkie: {autarky_score:.1f}%). \n\n"
            f"Möchten Sie matchen? Bestätigen Sie Ihr Interesse hier: {confirmation_url}"
        )
    else:  # 'new_member'
        message_body = (
            f"Gute Neuigkeiten von 'badenleg.ch'! \n\n"
            f"Ein neues Mitglied hat sich in Ihrem Energie-Cluster registriert.\n"
            f"Cluster-Autarkie: {autarky_score:.1f}%\n\n"
            f"Besuchen Sie {APP_BASE_URL} für weitere Details."
        )
    
    print(f"\n--- [SMS-SIMULATION] ---")
    print(f"AN: {phone_number}")
    print(f"TYP: {notification_type}")
    print(message_body)
    print("--------------------------\n")

    if twilio_client:
        try:
            twilio_client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number # Muss eine E.164 formatierte Nummer sein (z.B. +4179...)
            )
            print("[SMS OK] Benachrichtigung erfolgreich an Twilio API gesendet.")
        except Exception as e:
            print(f"[SMS FEHLER] Twilio API-Fehler: {e}")

def send_email_notification(email, cluster_id, autarky_score, new_member_count):
    """Sendet E-Mail-Benachrichtigung an registrierte Nutzer."""
    message_body = (
        f"Gute Neuigkeiten von 'badenleg.ch'!\n\n"
        f"Ein neues Mitglied hat sich in Ihrem Energie-Cluster registriert.\n"
        f"Cluster-Autarkie: {autarky_score:.1f}%\n"
        f"Anzahl Mitglieder: {new_member_count}\n\n"
        f"Besuchen Sie {APP_BASE_URL} für weitere Details."
    )
    
    print(f"\n--- [EMAIL-SIMULATION] ---")
    print(f"AN: {email}")
    print(message_body)
    print("--------------------------\n")
    
    # Hier könnte man z.B. Flask-Mail oder einen E-Mail-Service integrieren
    # Für MVP: Nur Logging
    # TODO: E-Mail-Service integrieren (z.B. SendGrid, AWS SES, etc.)

def get_all_known_profiles():
    """Hilfsfunktion: Sammelt alle Profile aus DB und Pool."""
    all_profiles = []
    with db_lock:
        for building in DB_BUILDINGS.values():
            all_profiles.append(building['profile'])
        for building in DB_INTEREST_POOL.values():
            all_profiles.append(building['profile'])
    return all_profiles

def run_full_ml_task(new_building_id=None):
    """
    (ASYNC-TASK) Führt die langsame, vollständige ML-Analyse im Hintergrund aus.
    Aktualisiert den globalen Cache und löst SMS-Trigger aus.
    
    Args:
        new_building_id: Optional. Die building_id des neu registrierten Nutzers.
                        Wenn angegeben, werden alle Mitglieder seines Clusters benachrichtigt.
    """
    print("\n[ASYNC-TASK] Starte langsame ML-Neuberechnung im Hintergrund...")
    
    all_profiles_list = get_all_known_profiles()
    
    if len(all_profiles_list) < 2:
        print("[ASYNC-TASK] -> Nicht genügend Nutzer für Clustering. Breche ab.")
        return

    # Erstelle DataFrame mit normalem Index, um Index-Probleme zu vermeiden
    building_data = pd.DataFrame(all_profiles_list)
    # Stelle sicher, dass wir einen normalen RangeIndex haben
    if not isinstance(building_data.index, pd.RangeIndex):
        building_data = pd.DataFrame(building_data.to_dict('records'))
    
    # 1. Langsame ML-Analyse ausführen
    ranked_communities, buildings_with_clusters = ml_models.find_optimal_communities(
        building_data,
        radius_meters=150,
        min_community_size=2
    )
    
    # 2. Globalen Cache aktualisieren
    with db_lock:
        DB_CLUSTERS.clear()
        DB_CLUSTER_INFO.clear()
        
        # Stelle sicher, dass building_id vorhanden ist
        if 'building_id' in buildings_with_clusters.columns:
            for _, row in buildings_with_clusters.iterrows():
                building_id = row.get('building_id')
                if building_id:
                    DB_CLUSTERS[building_id] = row.get('cluster', -1)
            
        for community in ranked_communities:
            DB_CLUSTER_INFO[community['community_id']] = community
            
    print(f"[ASYNC-TASK] -> ML-Cache aktualisiert: {len(ranked_communities)} Cluster gefunden.")

    # 3. SMS-Trigger prüfen (für anonyme Nutzer, die jetzt Matches haben)
    print("[ASYNC-TASK] -> Prüfe auf neue SMS-Benachrichtigungen...")
    check_for_new_matches(buildings_with_clusters)
    
    # 4. NEU: Benachrichtige alle Cluster-Mitglieder, wenn sich jemand Neues registriert hat
    if new_building_id:
        print(f"[ASYNC-TASK] -> Benachrichtige alle Mitglieder im Cluster des neuen Nutzers {new_building_id}...")
        notify_all_cluster_members(new_building_id, buildings_with_clusters)
    
    print("[ASYNC-TASK] -> Hintergrund-Task abgeschlossen.\n")


def check_for_new_matches(buildings_with_clusters):
    """
    Prüft (nach einem ML-Lauf), ob ein Cluster
    anonyme *und* registrierte Nutzer enthält.
    """
    with db_lock:
        # Finde alle anonymen Nutzer, die jetzt in einem Cluster sind
        for building_id, data in DB_INTEREST_POOL.items():
            if building_id not in DB_CLUSTERS or DB_CLUSTERS[building_id] == -1:
                continue # Dieser anonyme Nutzer ist (noch) nicht geclustert
            
            cluster_id = DB_CLUSTERS[building_id]
            
            # Prüfe, ob in DIESEM Cluster (ID) ein *registrierter* Nutzer ist
            cluster_members = buildings_with_clusters[buildings_with_clusters['cluster'] == cluster_id]
            
            # Suche nach einem 'echten' Mitglied (nicht der anonyme Nutzer selbst)
            has_registered_member = any(
                member_id in DB_BUILDINGS 
                for member_id in cluster_members['building_id'] 
                if member_id != building_id
            )
            
            if has_registered_member:
                print(f"[MATCHING] -> Cluster {cluster_id} hat ein Match ausgelöst!")
                cluster_info = DB_CLUSTER_INFO[cluster_id]
                
                # Sende SMS an den anonymen Nutzer
                send_sms_notification(
                    phone_number=data['phone'],
                    cluster_id=cluster_id,
                    autarky_score=cluster_info['autarky_percent'],
                    notification_type='match'
                )

def notify_all_cluster_members(new_building_id, buildings_with_clusters):
    """
    Benachrichtigt ALLE Mitglieder eines Clusters, wenn sich jemand Neues registriert.
    
    Args:
        new_building_id: Die building_id des neu registrierten Nutzers
        buildings_with_clusters: DataFrame mit allen Gebäuden und ihren Cluster-Zuweisungen
    """
    with db_lock:
        # Finde den Cluster des neuen Nutzers
        if new_building_id not in DB_CLUSTERS or DB_CLUSTERS[new_building_id] == -1:
            print(f"[NOTIFY] Neuer Nutzer {new_building_id} ist nicht in einem Cluster.")
            return
        
        cluster_id = DB_CLUSTERS[new_building_id]
        
        if cluster_id not in DB_CLUSTER_INFO:
            print(f"[NOTIFY] Cluster {cluster_id} nicht gefunden.")
            return
        
        cluster_info = DB_CLUSTER_INFO[cluster_id]
        cluster_members = buildings_with_clusters[buildings_with_clusters['cluster'] == cluster_id]
        
        print(f"[NOTIFY] Benachrichtige alle {len(cluster_members)} Mitglieder von Cluster {cluster_id}...")
        
        # Benachrichtige alle Mitglieder (außer dem neuen Nutzer selbst)
        notified_count = 0
        for _, member_row in cluster_members.iterrows():
            member_id = member_row['building_id']
            
            if member_id == new_building_id:
                continue  # Überspringe den neuen Nutzer selbst
            
            # Prüfe, ob Mitglied anonym oder registriert ist
            if member_id in DB_INTEREST_POOL:
                # Anonymer Nutzer: SMS
                anon_data = DB_INTEREST_POOL[member_id]
                send_sms_notification(
                    phone_number=anon_data['phone'],
                    cluster_id=cluster_id,
                    autarky_score=cluster_info['autarky_percent'],
                    notification_type='new_member'
                )
                notified_count += 1
            elif member_id in DB_BUILDINGS:
                # Registrierter Nutzer: E-Mail
                building_data = DB_BUILDINGS[member_id]
                send_email_notification(
                    email=building_data['email'],
                    cluster_id=cluster_id,
                    autarky_score=cluster_info['autarky_percent'],
                    new_member_count=cluster_info['num_members']
                )
                notified_count += 1
        
        print(f"[NOTIFY] -> {notified_count} Mitglieder benachrichtigt.")


def find_provisional_matches(new_profile):
    """
    (FAST-TASK) Findet schnelle "provisorische" Matches für die sofortige API-Antwort.
    Prüft nur die Distanz, führt KEIN DBSCAN aus.
    """
    print("[API] Starte schnelle, provisorische Match-Suche...")
    all_profiles = get_all_known_profiles()
    
    if not all_profiles:
        return None # Der erste Nutzer findet nie ein Match
        
    new_coords = (new_profile['lat'], new_profile['lon'])
    provisional_cluster_profiles = [new_profile] # Starte Cluster mit neuem Nutzer
    
    for profile in all_profiles:
        existing_coords = (profile['lat'], profile['lon'])
        distance = ml_models.calculate_distance(new_coords[0], new_coords[1], existing_coords[0], existing_coords[1])
        
        if distance <= 150: # (Hardcodierter Radius)
            provisional_cluster_profiles.append(profile)
            
    if len(provisional_cluster_profiles) < 2:
        print("[API] -> Provisorische Suche: Keine Nachbarn gefunden.")
        return None # Kein Match
        
    print(f"[API] -> Provisorische Suche: {len(provisional_cluster_profiles)-1} Nachbarn gefunden.")
    
    # Erstelle einen temporären DataFrame, um Autarkie zu simulieren
    # Verwende to_dict('records') um sicherzustellen, dass wir einen normalen Index haben
    community_df = pd.DataFrame(provisional_cluster_profiles)
    # Stelle sicher, dass der Index normal ist
    if not isinstance(community_df.index, pd.RangeIndex):
        community_df = pd.DataFrame(community_df.to_dict('records'))
    
    # Simuliere Autarkie für DIESE KLEINE GRUPPE
    autarky_score, _, _ = ml_models.calculate_community_autarky(community_df, None)
    
    # Baue Cluster-Info für die API-Antwort (ohne ML-Clustering-ID)
    members = [{
        'building_id': p['building_id'], 
        'lat': p['lat'], 
        'lon': p['lon']} for p in provisional_cluster_profiles
    ]
    
    cluster_info = {
        'community_id': 'provisional', # Kennzeichnen als provisorisch
        'num_members': len(members),
        'members': members,
        'autarky_percent': autarky_score * 100,
    }
    
    return cluster_info


# --- API-Endpunkte ---

@app.route("/")
def index():
    """Zeigt das HTML-Frontend an."""
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("WARNUNG: 'templates'-Ordner wurde erstellt. Bitte 'index.html' dort ablegen.")
    return render_template('index.html')

@app.route("/api/suggest_addresses")
def api_suggest_addresses():
    """
    (Schnell) Gibt Adressvorschläge basierend auf einem Suchbegriff zurück.
    Je länger der Query, desto spezifischer die Ergebnisse.
    """
    query = request.args.get('q', '').strip()
    print(f"[API] Adressvorschläge angefragt für: '{query}'")
    
    if not query or len(query) < 2:
        return jsonify({"suggestions": []})
    
    # Mehr Ergebnisse für längere Queries (bessere Filterung)
    limit = 15 if len(query) < 5 else 10
    suggestions = data_enricher.get_address_suggestions(query, limit=limit)
    print(f"[API] {len(suggestions)} Vorschläge gefunden")
    
    return jsonify({"suggestions": suggestions})

@app.route("/api/get_all_buildings")
def api_get_all_buildings():
    """
    (Schnell) Gibt die Koordinaten aller bekannten (anonymen
    und registrierten) Gebäude zurück, um die Karte zu füllen.
    """
    print("[API] Lade alle bekannten Gebäudepositionen...")
    locations = []
    
    with db_lock:
        # Anonyme Pool-Mitglieder
        for profile_data in DB_INTEREST_POOL.values():
            locations.append({
                'lat': profile_data['profile']['lat'],
                'lon': profile_data['profile']['lon'],
                'type': 'anonymous'
            })
        # Voll registrierte Mitglieder
        for profile_data in DB_BUILDINGS.values():
            locations.append({
                'lat': profile_data['profile']['lat'],
                'lon': profile_data['profile']['lon'],
                'type': 'registered'
            })
        
    print(f"  -> {len(locations)} Gebäude gefunden.")
    return jsonify({"buildings": locations})

@app.route("/api/get_all_clusters")
def api_get_all_clusters():
    """
    (Schnell) Gibt alle existierenden ZEV/LEG-Cluster als Polygone zurück.
    """
    print("[API] Lade alle Cluster...")
    clusters = []
    
    try:
        with db_lock:
            for cluster_id, cluster_info in DB_CLUSTER_INFO.items():
                if cluster_id == 'provisional':
                    continue  # Überspringe provisorische Cluster
                
                # Erstelle Polygon-Koordinaten aus den Mitgliedern
                members = cluster_info.get('members', [])
                if len(members) < 2:
                    continue
                
                # Erstelle ein einfaches Polygon (Convex Hull) um die Punkte
                try:
                    coords = [[m.get('lat'), m.get('lon')] for m in members if m.get('lat') and m.get('lon')]
                    if len(coords) < 2:
                        continue
                    
                    # Einfacher Convex Hull Algorithmus
                    polygon_coords = create_simple_polygon(coords)
                    
                    clusters.append({
                        'cluster_id': cluster_id,
                        'members': members,
                        'polygon': polygon_coords,
                        'autarky_percent': cluster_info.get('autarky_percent', 0),
                        'num_members': cluster_info.get('num_members', len(members))
                    })
                except Exception as e:
                    print(f"  [API] Fehler beim Erstellen des Polygons für Cluster {cluster_id}: {e}")
                    continue
        
        print(f"  -> {len(clusters)} Cluster gefunden.")
        return jsonify({"clusters": clusters})
    except Exception as e:
        print(f"[API] Fehler in api_get_all_clusters: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"clusters": [], "error": str(e)}), 500

def create_simple_polygon(coords):
    """
    Erstellt ein einfaches Polygon um die gegebenen Koordinaten.
    Verwendet einen einfachen Convex Hull Ansatz.
    """
    if len(coords) < 3:
        # Wenn weniger als 3 Punkte, erstelle ein kleines Quadrat um den Punkt
        if len(coords) == 1:
            lat, lon = coords[0]
            offset = 0.0005  # ~50m
            return [
                [lat - offset, lon - offset],
                [lat + offset, lon - offset],
                [lat + offset, lon + offset],
                [lat - offset, lon + offset],
                [lat - offset, lon - offset]  # Schließe Polygon
            ]
        elif len(coords) == 2:
            # Erstelle ein Rechteck zwischen den beiden Punkten
            lat1, lon1 = coords[0]
            lat2, lon2 = coords[1]
            offset = 0.0003  # ~30m
            return [
                [lat1 - offset, lon1 - offset],
                [lat2 + offset, lon1 - offset],
                [lat2 + offset, lon2 + offset],
                [lat1 - offset, lon2 + offset],
                [lat1 - offset, lon1 - offset]
            ]
    
    # Für 3+ Punkte: Convex Hull oder einfaches Rechteck
    if HAS_SCIPY:
        try:
            points = np.array(coords)
            hull = ConvexHull(points)
            polygon = [coords[i] for i in hull.vertices]
            polygon.append(polygon[0])  # Schließe Polygon
            return polygon
        except:
            pass
    
    # Fallback: Einfaches Rechteck um alle Punkte
    lats = [c[0] for c in coords]
    lons = [c[1] for c in coords]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    offset = 0.0003
    return [
        [min_lat - offset, min_lon - offset],
        [max_lat + offset, min_lon - offset],
        [max_lat + offset, max_lon + offset],
        [min_lat - offset, max_lon + offset],
        [min_lat - offset, min_lon - offset]
    ]


@app.route("/api/check_potential", methods=['POST'])
def api_check_potential():
    """
    (Schnell) Nimmt eine Adresse entgegen, reichert sie an und
    findet provisorische Matches.
    """
    try:
        if not request.json:
            return jsonify({"error": "Keine Daten empfangen."}), 400
            
        address = request.json.get('address', '').strip()
        if not address:
            return jsonify({"error": "Adresse fehlt."}), 400
            
        # 1. Adresse anreichern (verwende echte API, da wir die richtige URL haben)
        print(f"[API] Analysiere Adresse: '{address}'")
        estimates = None
        profiles = None
        
        try:
            estimates, profiles = data_enricher.get_energy_profile_for_address(address)
            if not estimates:
                # Fallback auf Mock, falls echte API fehlschlägt
                print(f"[API] Echte API fehlgeschlagen, verwende Mock für: '{address}'")
                estimates, profiles = data_enricher.get_mock_energy_profile_for_address(address)
        except Exception as e:
            print(f"[API] Fehler bei Adress-Analyse: {e}")
            import traceback
            traceback.print_exc()
            # Fallback auf Mock
            try:
                estimates, profiles = data_enricher.get_mock_energy_profile_for_address(address)
            except Exception as mock_error:
                print(f"[API] Auch Mock fehlgeschlagen: {mock_error}")
                return jsonify({"error": f"Adresse konnte nicht verarbeitet werden: {str(e)}"}), 500
        
        if not estimates:
            return jsonify({"error": "Adresse konnte nicht analysiert werden."}), 404
    except Exception as e:
        print(f"[API] Unerwarteter Fehler in api_check_potential: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server-Fehler: {str(e)}"}), 500
        
    # 2. Schnelle, provisorische Match-Suche
    cluster_info = find_provisional_matches(estimates)
            
    if not cluster_info:
        # Szenario A: Kein Match
        return jsonify({
            "potential": False,
            "message": "Keine direkten Partner gefunden.",
            "profile_summary": estimates
        })
    else:
        # Szenario B: Match gefunden!
        return jsonify({
            "potential": True,
            "message": f"Partner gefunden! Potenzielle Autarkie: {cluster_info['autarky_percent']:.1f}%",
            "cluster_info": cluster_info, # Enthält jetzt Koordinaten
            "profile_summary": estimates
        })

@app.route("/api/register_anonymous", methods=['POST'])
def api_register_anonymous():
    """
    (Schnell) Speichert Nutzer im anonymen Pool und
    löst den langsamen ML-Task im Hintergrund aus.
    """
    phone = request.json.get('phone')
    profile = request.json.get('profile') 
    
    if not phone or not profile:
        return jsonify({"error": "Telefonnummer oder Profil fehlt."}), 400
        
    building_id = profile['building_id']
    
    with db_lock:
        DB_INTEREST_POOL[building_id] = {
            "phone": phone,
            "profile": profile,
            "registered_at": time.time()
        }
    
    print(f"[DB] Anonymer Nutzer {building_id} (Tel: {phone}) zum Pool hinzugefügt.")
    print(f"  Aktuelle Pool-Grösse: {len(DB_INTEREST_POOL)}")
    
    # NEU: Langsamen ML-Task im Hintergrund starten
    # Übergebe building_id, damit alle Cluster-Mitglieder benachrichtigt werden können
    threading.Thread(target=run_full_ml_task, args=(building_id,)).start()
    
    # Sofort antworten
    return api_get_all_buildings()

@app.route("/api/register_full", methods=['POST'])
def api_register_full():
    """
    (Schnell) Speichert Nutzer in der DB und
    löst den langsamen ML-Task im Hintergrund aus.
    """
    profile = request.json.get('profile')
    email = request.json.get('email')
    
    if not profile or not email:
        return jsonify({"error": "E-Mail oder Profil fehlt."}), 400
        
    building_id = profile['building_id']
    
    with db_lock:
        DB_BUILDINGS[building_id] = {
            "email": email,
            "profile": profile,
            "registered_at": time.time()
        }
    
    print(f"[DB] Voll registrierter Nutzer {building_id} (Mail: {email}) hinzugefügt.")
    print(f"  Aktuelle DB-Grösse: {len(DB_BUILDINGS)}")

    # NEU: Langsamen ML-Task im Hintergrund starten
    # Übergebe building_id, damit alle Cluster-Mitglieder benachrichtigt werden können
    threading.Thread(target=run_full_ml_task, args=(building_id,)).start()
    
    # Sofort antworten
    return api_get_all_buildings()


@app.route("/confirm/<token>")
def confirm_match(token):
    """
    Wird vom anonymen Nutzer via SMS-Link aufgerufen.
    """
    with db_lock:
        match_info = DB_MATCH_TOKENS.pop(token, None) # Token wird verbraucht
    
    if not match_info:
        return "<h1>Link ungültig</h1><p>Dieser Bestätigungslink ist ungültig oder wurde bereits verwendet.</p>", 404
        
    # 1. Finde den anonymen Nutzer
    with db_lock:
        building_id = match_info['building_id']
        anon_user_data = DB_INTEREST_POOL.pop(building_id, None)
    
    if not anon_user_data:
        return "<h1>Bereits bestätigt</h1><p>Ihr Profil wurde bereits bestätigt und aus dem anonymen Pool entfernt.</p>", 404
        
    # 2. Wandle anonymen Nutzer in "echten" Nutzer um
    with db_lock:
        DB_BUILDINGS[building_id] = {
            "email": f"bestaetigt_{anon_user_data['phone']}@temp.ch", # Platzhalter
            "profile": anon_user_data['profile'],
            "registered_at": time.time()
        }
    
    print(f"[MATCHING] Nutzer {building_id} hat SMS-Link bestätigt!")
    
    # 3. Benachrichtige die *anderen* Mitglieder im Cluster
    print(f"[MATCHING] Sende E-Mail-Bestätigungen an alle Mitglieder in Cluster {match_info['cluster_id']}...")
    
    return "<h1>Bestätigung erfolgreich!</h1><p>Ihr Match wurde hergestellt. Sie erhalten in Kürze eine E-Mail mit den nächsten Schritten.</p>"


if __name__ == "__main__":
    if not twilio_client:
        print("\n[WARNUNG] Führen Sie dies in Ihrer Konsole aus, um den SMS-Service zu aktivieren:")
        print("export TWILIO_ACCOUNT_SID='IHRE_SID'")
        print("export TWILIO_AUTH_TOKEN='IHR_TOKEN'")
        print("export TWILIO_PHONE_NUMBER='+41IHRENUMMER'\n")
    
    # Führe initiale ML-Analyse aus, falls bereits Gebäude vorhanden sind
    def initial_ml_analysis():
        time.sleep(2)  # Warte kurz, damit Server vollständig gestartet ist
        all_profiles = get_all_known_profiles()
        if len(all_profiles) >= 2:
            print("[INIT] Führe initiale ML-Analyse für vorhandene Gebäude durch...")
            run_full_ml_task()
    
    # Starte initiale Analyse im Hintergrund
    threading.Thread(target=initial_ml_analysis, daemon=True).start()
    
    app.run(debug=True, port=5003, host='127.0.0.1')

