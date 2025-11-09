import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from math import radians, sin, cos, sqrt, atan2

# --- NEU: Eigenständige Distanz-Funktion ---
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points (in meters)."""
    R = 6371e3  # Earth radius in meters
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2) * sin(delta_phi / 2) + \
        cos(phi1) * cos(phi2) * \
        sin(delta_lambda / 2) * sin(delta_lambda / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# --- Profil-Generator ---

def generate_mock_profiles(annual_consumption_kwh, potential_pv_kwp, num_intervals=35040):
    """Generiert vereinfachte 15-Minuten-Zeitreihenprofile."""
    timestamps = pd.date_range(start='2025-01-01', periods=num_intervals, freq='15min')
    
    time_of_day = timestamps.hour + timestamps.minute / 60
    consumption_shape = np.cos((time_of_day - 13.5) * (np.pi / 12))**2
    consumption_shape[ (time_of_day < 6) | (time_of_day > 22) ] *= 0.5
    
    # Verhindere Division durch Null, wenn Summe 0 ist
    if consumption_shape.sum() == 0:
        normalized_consumption = np.zeros_like(consumption_shape)
    else:
        normalized_consumption = consumption_shape / consumption_shape.sum()
        
    consumption_profile_kw = normalized_consumption * (annual_consumption_kwh / 0.25)
    
    day_of_year = timestamps.dayofyear
    seasonal_factor = 1 + 0.5 * np.cos((day_of_year - 172) * (2 * np.pi / 365))
    pv_shape = np.sin(np.maximum(0, (time_of_day - 6) * (np.pi / 12)))**1.5
    pv_shape = pv_shape * seasonal_factor
    
    if pv_shape.max() > 0:
        normalized_pv = pv_shape / pv_shape.max()
    else:
        normalized_pv = np.zeros_like(pv_shape)
        
    pv_profile_kw = normalized_pv * potential_pv_kwp

    return pd.DataFrame({
        'consumption_kw': consumption_profile_kw,
        'production_kw': pv_profile_kw
    }, index=timestamps)

# --- Autarkie-Simulator ---

def calculate_community_autarky(community_buildings_df, all_profiles):
    """
    (Schnell) Berechnet den Autarkie-Score für einen Cluster.
    `all_profiles` wird ignoriert (kann None sein), da Profile neu generiert werden.
    """
    
    # 1. Profile für Simulation generieren
    all_profiles_sim = {}
    if community_buildings_df.empty:
        return 0.0, 0, 0

    first_building_id = None
    
    for _, row in community_buildings_df.iterrows():
        building_id = row['building_id']
        if first_building_id is None:
            first_building_id = building_id
            
        all_profiles_sim[building_id] = generate_mock_profiles(
            row['annual_consumption_kwh'],
            row['potential_pv_kwp']
        )

    if first_building_id is None:
         return 0.0, 0, 0

    # Holen Sie sich einen gültigen Index aus dem ersten Profil
    sim_index = all_profiles_sim[first_building_id].index
    
    community_consumption = pd.Series(0.0, index=sim_index)
    community_production = pd.Series(0.0, index=sim_index)
    
    for building_id in community_buildings_df['building_id']:
        community_consumption += all_profiles_sim[building_id]['consumption_kw']
        community_production += all_profiles_sim[building_id]['production_kw']
        
    net_load_kw = community_consumption - community_production
    energy_kwh = net_load_kw * 0.25
    grid_import_kwh = energy_kwh[energy_kwh > 0].sum()
    total_consumption_kwh = community_consumption.sum() * 0.25
    
    if total_consumption_kwh == 0: return 0.0, 0, 0
        
    autarky_score = (total_consumption_kwh - grid_import_kwh) / total_consumption_kwh
    return autarky_score, total_consumption_kwh, (community_production.sum() * 0.25)


# --- Cluster-Analyse ---

def get_cluster_info(community_df, cluster_id):
    """
    (Schnell) Hilfsfunktion, um die Details eines Clusters für das API-Response vorzubereiten.
    Fügt Koordinaten der Mitglieder hinzu.
    """
    autarky_score, total_consumption, total_production = calculate_community_autarky(
        community_df, None # Profile werden in der Fkt. neu generiert
    )
    
    # Extrahiere Koordinaten für die Kartenvisualisierung
    members = []
    for _, row in community_df.iterrows():
        members.append({
            'building_id': row['building_id'],
            'lat': row['lat'],
            'lon': row['lon']
        })

    return {
        'community_id': int(cluster_id) if isinstance(cluster_id, (int, np.integer)) else cluster_id,
        'num_members': len(community_df),
        'building_ids': list(community_df['building_id']), # Behalten für Logik
        'members': members, # NEU: Für Karten-Pins
        'autarky_percent': autarky_score * 100,
        'total_consumption_mwh': total_consumption / 1000,
        'total_production_mwh': total_production / 1000,
    }

def find_optimal_communities(building_data_df, radius_meters=150, min_community_size=3):
    """
    (Langsam) Main ML function (DBSCAN + Simulation).
    Gibt die gerankten Ergebnisse UND den DataFrame mit Cluster-Zuweisungen zurück.
    """
    if building_data_df.empty or len(building_data_df) < min_community_size:
        print(f"[ML] Zu wenig Daten für Clustering (min. {min_community_size} benötigt, {len(building_data_df)} vorhanden).")
        if not building_data_df.empty:
             building_data_df['cluster'] = -1
        return [], building_data_df
        
    print(f"[ML] Starte ML-Clustering (DBSCAN) für {len(building_data_df)} Gebäude...")
    
    coords = building_data_df[['lat', 'lon']].values
    coords_rad = np.radians(coords)
    
    earth_radius_m = 6371e3
    eps_rad = radius_meters / earth_radius_m

    # Führe DBSCAN mit Haversine-Distanz (echte Erddistanz) aus
    db = DBSCAN(eps=eps_rad, min_samples=min_community_size, algorithm='ball_tree', metric='haversine').fit(coords_rad)
    
    building_data_df['cluster'] = db.labels_
    
    num_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print(f"[ML] DBSCAN fand {num_clusters} potenzielle Gemeinschaften.")

    print("[ML] Simuliere Autarkie für jeden Cluster...")
    results = []
    for cluster_id in set(db.labels_):
        if cluster_id == -1: continue # Rauscht-Cluster (isolierte Gebäude)
            
        community_buildings_df = building_data_df[building_data_df['cluster'] == cluster_id]
        
        # Ruft die aktualisierte Funktion auf
        cluster_info = get_cluster_info(community_buildings_df, cluster_id)
        results.append(cluster_info)

    # Sortiere nach höchster Autarkie
    ranked_results = sorted(results, key=lambda x: x['autarky_percent'], reverse=True)
    
    return ranked_results, building_data_df


if __name__ == "__main__":
    print("Dieses Skript ist ein Modul und sollte von app.py importiert werden.")
    print("Es kann nicht direkt ausgeführt werden.")

