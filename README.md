import os
from datetime import datetime

import pandas as pd
import requests

API_URL = "https://opensky-network.org/api/states/all"
MS_TO_MPH = 2.23694
MAX_RECORDS = 1000

COLUMNS = [
    "icao24_id", "flight_callsign", "origin_country", "time_position",
    "last_contact", "longitude", "latitude", "baro_altitude_m",
    "on_ground", "velocity_mph", "true_track", "vertical_rate",
]


def fetch_live_flights():
    """Pull a snapshot of live aircraft state vectors from the OpenSky API."""
    print(f"[{datetime.now()}] Connecting to OpenSky Network API...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        states = response.json().get("states") or []
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"API error: {e}")
        return None
    if not states:
        print("No active flight data found.")
        return None
    print(f"Ingested {len(states)} raw aircraft records.")
    return states


def clean(raw_states):
    """Structure raw records, convert units, and apply basic quality checks."""
    rows = [list(s[:12]) for s in raw_states[:MAX_RECORDS]]
    df = pd.DataFrame(rows, columns=COLUMNS)

    df["flight_callsign"] = df["flight_callsign"].str.strip().replace("", None)
    df["velocity_mph"] = df["velocity_mph"] * MS_TO_MPH  # API returns m/s

    before = len(df)
    df = df.dropna(subset=["icao24_id", "latitude", "longitude"])
    df = df[df["latitude"].between(-90, 90) & df["longitude"].between(-180, 180)]
    df = df.drop_duplicates(subset=["icao24_id", "time_position"])
    print(f"Quality checks removed {before - len(df)} of {before} records.")
    return df


def save(df):
    output_dir = "data_lake/landing_zone"
    os.makedirs(output_dir, exist_ok=True)
    path = f"{output_dir}/flights_{datetime.now():%Y%m%d_%H%M%S}.csv"
    df.to_csv(path, index=False)
    print(f"[{datetime.now()}] Saved {len(df)} records to {path}")


if __name__ == "__main__":
    raw = fetch_live_flights()
    if raw:
        save(clean(raw))
