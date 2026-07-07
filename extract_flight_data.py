import os
import json
import requests
import pandas as pd
from datetime import datetime

def fetch_live_flights():
    """Extracts live aircraft state vectors from the open-source OpenSky API."""
    print(f"[{datetime.now()}] Initializing connection to OpenSky Network API...")
    url = "https://opensky-network.org"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        states = data.get("states", [])
        if not states:
            print("No active flight data found in the current stream.")
            return None
        print(f"Successfully ingested {len(states)} raw aircraft records.")
        return states
    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")
        return None

def process_and_save_data(raw_states):
    """Structures raw data arrays into an enterprise-ready dataset."""
    columns = [
        "icao24_id", "flight_callsign", "origin_country", "time_position", 
        "last_contact", "longitude", "latitude", "baro_altitude", 
        "on_ground", "velocity_mph", "true_track", "vertical_rate"
    ]
    structured_records = []
    for flight in raw_states[:1000]: # Cap data size for cloud storage performance
        record = [
            flight[0] if len(flight) > 0 else None,
            str(flight[1]).strip() if len(flight) > 1 else None,
            flight[2] if len(flight) > 2 else None,
            flight[3] if len(flight) > 3 else None,
            flight[4] if len(flight) > 4 else None,
            flight[5] if len(flight) > 5 else None,
            flight[6] if len(flight) > 6 else None,
            flight[7] if len(flight) > 7 else None,
            flight[8] if len(flight) > 8 else None,
            flight[9] if len(flight) > 9 else None,
            flight[10] if len(flight) > 10 else None,
            flight[11] if len(flight) > 11 else None
        ]
        structured_records.append(record)
    df = pd.DataFrame(structured_records, columns=columns)
    output_dir = "data_lake/landing_zone"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{output_dir}/flights_{timestamp}.csv"
    df.to_csv(file_path, index=False)
    print(f"[{datetime.now()}] Data pipeline ingestion complete. Saved to: {file_path}")

if __name__ == "__main__":
    raw_data = fetch_live_flights()
    if raw_data:
        process_and_save_data(raw_data)
