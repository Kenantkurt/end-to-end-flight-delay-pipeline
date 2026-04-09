from pathlib import Path
import pandas as pd

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
PARQUET_DIR = BASE_DIR / "data" / "processed" / "parquet"

CHUNK_SIZE = 1_000_000


FILES = {
    "alljoined_airlines": "alljoined_airlines.csv",
    "airline_key": "airline_key.csv",
    "airport_info": "airport_info.csv",
}


def ensure_dirs():
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


# LARGE FILE → PARTITIONED PARQUET
def ingest_large_csv(input_path: Path, output_dir: Path):
    print(f"Processing LARGE file: {input_path.name}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(
        pd.read_csv(
            input_path,
            chunksize=CHUNK_SIZE,
            low_memory=False  
        )
    ):
        print(f"Chunk {i} -> {chunk.shape}")

        chunk = standardize_columns(chunk)

        chunk_path = output_dir / f"part_{i}.parquet"
        chunk.to_parquet(chunk_path, engine="pyarrow", index=False)

    print(f"Finished: {output_dir}\n")


# SMALL FILE → SINGLE PARQUET
def ingest_small_csv(input_path: Path, output_path: Path):
    print(f"Processing SMALL file: {input_path.name}")

    df = pd.read_csv(
        input_path,
        low_memory=False 
    )

    df = standardize_columns(df)

    df.to_parquet(output_path, engine="pyarrow", index=False)

    print(f"Finished: {output_path.name}\n")


def ingest():
    ensure_dirs()

    for dataset_name, filename in FILES.items():
        input_path = RAW_DIR / filename

        if not input_path.exists():
            raise FileNotFoundError(f"{filename} not found in raw folder")

        # LARGE DATASET
        if dataset_name == "alljoined_airlines":
            output_path = PARQUET_DIR / dataset_name
            ingest_large_csv(input_path, output_path)

        # SMALL DATASETS
        else:
            output_path = PARQUET_DIR / f"{dataset_name}.parquet"
            ingest_small_csv(input_path, output_path)


if __name__ == "__main__":
    ingest()