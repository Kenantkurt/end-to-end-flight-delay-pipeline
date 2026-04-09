import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "raw" / "us_holidays.csv"

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df = pd.read_csv(RAW_PATH)

print(df.head())
print(df.shape)

df.to_sql(
    name="us_holidays",
    con=engine,
    if_exists="replace",
    index=False
)

print("DONE")
