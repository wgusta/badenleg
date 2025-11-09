import os
import time
import uuid
import threading # NEU: Für asynchrone Tasks
from flask import Flask, request, jsonify, render_template, redirect
from twilio.rest import Client
import pandas as pd
import numpy as np # NEU: Für Distanzberechnung

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
APP_BASE_URL = "http://localhost:5000" # Basis-URL für Bestätigungslinks

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

def send_sms_notification(phone_number, cluster_id, autarky_score):
    """Sendet die SMS-Benachrichtigung an einen anonymen Nutzer."""
    # 1. Einzigartigen Bestätigungs-Token erstellen
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
    
    confirmation_url = f"{APP_BASE_URL}/confirm/{token}"
    
    message_body = (
        f"Gute Neuigkeiten von 'badenleg.ch'! \n\n"
        f"Wir haben einen passenden Energie-Partner in Ihrer Nachbarschaft gefunden "
        f"(Potenzielle Autarkie: {autarky_score:.1f}%). \n\n"
        f"Möchten Sie matchen? Bestätigen Sie Ihr Interesse hier: {confirmation_url}"
    )
    
    print(f"\n--- [SMS-SIMULATION] ---")
    print(f"AN: {phone_number}")
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

def get_all_known_profiles():
    """Hilfsfunktion: Sammelt alle Profile aus DB und Pool."""
    all_profiles = []
    with db_lock:
        for building in DB_BUILDINGS.values():
            all_profiles.append(building['profile'])
        for building in DB_INTEREST_POOL.values():
            all_profiles.append(building['profile'])
    return all_profiles

def run_full_ml_task():
    """
    (ASYNC-TASK) Führt die langsame, vollständige ML-Analyse im Hintergrund aus.
    Aktualisiert den globalen Cache und löst SMS-Trigger aus.
    """
    print("\n[ASYNC-TASK] Starte langsame ML-Neuberechnung im Hintergrund...")
    
    all_profiles_list = get_all_known_profiles()
    
    if len(all_profiles_list) < 2:
        print("[ASYNC-TASK] -> Nicht genügend Nutzer für Clustering. Breche ab.")
        return

    building_data = pd.DataFrame(all_profiles_list)
    
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
        
        for _, row in buildings_with_clusters.iterrows():
            DB_CLUSTERS[row['building_id']] = row['cluster']
            
        for community in ranked_communities:
            DB_CLUSTER_INFO[community['community_id']] = community
            
    print(f"[ASYNC-TASK] -> ML-Cache aktualisiert: {len(ranked_communities)} Cluster gefunden.")

    # 3. SMS-Trigger prüfen
    print("[ASYNC-TASK] -> Prüfe auf neue SMS-Benachrichtigungen...")
    check_for_new_matches(buildings_with_clusters)
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
                    autarky_score=cluster_info['autarky_percent']
                )
                # (Hier könnte man auch eine E-Mail an die registrierten Nutzer senden)


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
    community_df = pd.DataFrame(provisional_cluster_profiles)
    
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


@app.route("/api/check_potential", methods=['POST'])
def api_check_potential():
    """
    (Schnell) Nimmt eine Adresse entgegen, reichert sie an und
    findet provisorische Matches.
    """
    address = request.json.get('address')
    if not address:
        return jsonify({"error": "Adresse fehlt."}), 400
        
    # 1. Adresse anreichern (schnell, da gemockt/gecached)
    estimates, profiles = data_enricher.get_mock_energy_profile_for_address(address)
    # (In Produktion: hier Caching für data_enricher.get_energy_profile_for_address einbauen)
    
    if not estimates:
        return jsonify({"error": "Adresse konnte nicht analysiert werden."}), 404
        
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
    threading.Thread(target=run_full_ml_task).start()
    
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
    threading.Thread(target=run_full_ml_task).start()
    
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
    
    app.run(debug=True, port=5000)

