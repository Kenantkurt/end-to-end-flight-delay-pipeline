import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

BASE_DIR = Path(__file__).resolve().parents[2]

CURATED_DIR = BASE_DIR / "data" / "processed" / "curated"
INTERMEDIATE_DIR = BASE_DIR / "data" / "processed" / "intermediate"

FILES = {
    "flight_delays": CURATED_DIR / "flight_delays_curated.parquet",
    "airlines": CURATED_DIR / "airline_curated.parquet",
    "airports": CURATED_DIR / "airport_curated.parquet",
    "holidays": CURATED_DIR / "holidays.parquet",
    "weather": INTERMEDIATE_DIR / "flight_weather.parquet",
}

LARGE_TABLES = {"flight_delays", "weather"}
CHUNK_SIZE = 100_000


def load_small_table(table_name: str, file_path: Path) -> None:
    print(f"\nProcessing SMALL table: {table_name}")

    df = pd.read_parquet(file_path)
    print(f"Shape: {df.shape}")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
    )

    print(f"{table_name} loaded")


def load_large_table(table_name: str, file_path: Path) -> None:
    print(f"\nProcessing LARGE table: {table_name}")

    df = pd.read_parquet(file_path)
    total_rows = len(df)
    print(f"Total rows: {total_rows:,}")

    for start in range(0, total_rows, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, total_rows)
        chunk = df.iloc[start:end]

        print(f"Loading rows {start:,} -> {end:,} / {total_rows:,}")

        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace" if start == 0 else "append",
            index=False,
            chunksize=10_000,
            method="multi",
        )

    print(f"{table_name} loaded")


def ingest() -> None:
    for table_name, file_path in FILES.items():
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        if table_name in LARGE_TABLES:
            load_large_table(table_name, file_path)
        else:
            load_small_table(table_name, file_path)


if __name__ == "__main__":
    ingest()