from pathlib import Path

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "staging" / "weather.parquet"

URL = (
    "https://archive-api.open-meteo.com/v1/archive?"
    "latitude=40.71427&longitude=-74.00597&start_date=2018-01-01"
    "&end_date=2022-07-31&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_sum,snowfall_sum,rain_sum&timezone=America%2FNew_York"
)


def fetch_weather():
    print("Fetching weather data...")

    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["daily"])
    df["date"] = pd.to_datetime(data["daily"]["time"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"Saved weather data to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_weather()
