# Flight Delay Pipeline

End-to-end flight delay analytics pipeline built with Python, Parquet, PostgreSQL, Google Cloud Storage, BigQuery, dbt, and Airflow.

## What This Project Does

This project ingests U.S. flight delay data plus external weather and holiday data, transforms them into analytics-ready models, and orchestrates the dbt workflow with Airflow.

Pipeline flow:

1. Raw flight, holiday, and weather data is collected.
2. Python ingestion scripts standardize and persist datasets as parquet.
3. Curated and intermediate outputs are loaded into storage layers.
4. BigQuery serves as the warehouse.
5. dbt builds staging and mart models.
6. Airflow orchestrates `dbt run` and `dbt test` on a schedule.

## Project Structure

```text
.
├── airflow/            # Airflow Docker setup and DAGs
├── data/               # Local raw and processed data (not tracked in Git)
├── flight_dbt/         # dbt project
├── notebooks/          # EDA and prototyping
├── src/ingestion/      # Python ingestion scripts
├── .env.example        # Example local DB config
├── requirements.txt    # Python dependencies
└── README.md
```

## Core Components

- `src/ingestion/ingest_raw.py`: converts raw CSV flight data to parquet
- `src/ingestion/ingest_weather_api.py`: pulls weather data from Open-Meteo
- `src/ingestion/holidays.py`: loads holiday data
- `src/ingestion/parquet_to_db.py`: loads curated parquet data into PostgreSQL
- `flight_dbt/models/staging/`: dbt staging models
- `flight_dbt/models/marts/`: analytics-ready mart models
- `airflow/dags/flight_dbt_dag.py`: Airflow DAG for `dbt run` and `dbt test`

## Analytics Questions Answered

- Which airlines experience the highest delays?
- Which airports have the worst departure delay performance?
- How much do weather conditions affect delays?
- Do holidays increase delay rates?
- Which factors contribute most to delay variation?

## Setup

### 1. Python environment

```bash
python3.11 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

### 2. Local environment variables

Create `.env` from `.env.example` and fill in your PostgreSQL connection settings.

### 3. dbt profile for Airflow

Create `airflow/dbt/profiles.yml` from `airflow/dbt/profiles.yml.example` and set your BigQuery project details.

### 4. Airflow local config

Create `airflow/.env` from `airflow/.env.example` if you want to override default admin credentials or mount paths.

### 5. Start Airflow

```bash
cd airflow
docker compose up --build
```

Then open:

```text
http://localhost:8080
```

### 6. Run dbt manually

```bash
cd flight_dbt
dbt run
dbt test
```

## Notes For GitHub

- Large datasets are intentionally not tracked in Git.
- Credentials, Airflow metadata, dbt target artifacts, and local logs are ignored.
- Example config files are included; real secrets must stay local.

## Current Status

This project is end-to-end and portfolio-ready:

- ingestion completed
- warehouse models completed
- dbt tests added
- Airflow orchestration added
- scheduling, retries, and failure notifications added

## Known Limitations

- Weather enrichment uses a simplified approach and may not represent full airport-level coverage for all flights.
- Airflow is configured for local development, not a production cluster deployment.
- Secrets are expected to be provided locally via ignored config files.

## Next Improvements

- Add ingestion steps to Airflow orchestration
- Add dashboarding / BI layer
- Add data freshness monitoring
- Improve secrets management with a managed secret store
