# Flight Delay Pipeline

An end-to-end ELT analytics pipeline for U.S. flight delay data, built with Python, Parquet, PostgreSQL, BigQuery, dbt, and Apache Airflow.

---

## Architecture

```
Raw Data → Python Ingestion → Parquet → PostgreSQL → BigQuery → dbt (Staging → Marts)
                                                                        ↑
                                                               Airflow (scheduled)
```

**Pattern:** ELT — data is ingested and loaded into the warehouse first, then transformed in place using dbt.

---

## What This Project Does

This pipeline answers operational and business questions about U.S. domestic flight delays:

- Which airlines experience the highest delay rates?
- Which airports show the worst departure delay performance?
- How much do weather conditions affect delays?
- Do holidays increase delay rates?
- Which factors drive delay variation most strongly?

---

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python, Open-Meteo API |
| Storage | Parquet, PostgreSQL |
| Warehouse | Google BigQuery |
| Transformation | dbt (dbt-bigquery) |
| Orchestration | Apache Airflow 2.9.1 |
| Containerization | Docker |

---

## Project Structure

```
.
├── airflow/                  # Airflow Docker setup and DAGs
│   ├── dags/
│   │   └── flight_dbt_dag.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── flight_dbt/               # dbt project
│   └── models/
│       ├── staging/          # Source-facing standardization layer
│       └── marts/            # Business-facing analytical models
├── notebooks/                # EDA and prototyping
├── src/ingestion/            # Python ingestion scripts
├── data/                     # Local raw/processed data (not tracked in Git)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Pipeline Overview

### 1. Ingestion (`src/ingestion/`)

| Script | Description |
|---|---|
| `ingest_raw.py` | Converts raw flight CSV files to Parquet format |
| `ingest_weather_api.py` | Fetches historical weather data from Open-Meteo API |
| `holidays.py` | Loads U.S. federal holiday data into PostgreSQL |
| `parquet_to_db.py` | Loads curated Parquet datasets into PostgreSQL |

> Ingestion scripts handle all cleaning and standardization. As a result, dbt staging models focus on source isolation rather than transformation — this is an intentional design decision to keep the boundary between Python and SQL responsibilities clear.

### 2. Warehouse Loading

Curated datasets are loaded from PostgreSQL into BigQuery for transformation and analysis.

### 3. dbt Transformation

The dbt project is structured into two layers:

**Staging** — source-facing models that isolate upstream schema changes:
- `stg_flight_delays` — flight-level delay records
- `stg_airlines` — airline reference data
- `stg_airports` — airport reference data
- `stg_weather` — flight-level weather enrichment
- `stg_holidays` — U.S. holiday calendar

**Marts** — business-facing analytical models:
- `enriched_flights` — joined dataset combining flights, weather, and holidays
- `fct_airline_delay_summary` — aggregated delay metrics by airline
- `fct_airport_departure_delay_summary` — departure delay metrics by airport, with composite performance score
- `fct_weather_delay_impact_summary` — delay rate comparison across weather conditions
- `fct_holiday_delay_impact_summary` — delay rate comparison across holiday vs. non-holiday periods

### 4. Orchestration

Airflow runs on Docker and schedules daily dbt runs:

```
dbt_run >> dbt_test
```

DAG features: daily schedule (`0 9 * * *`), `catchup=False`, 1 retry with 5-minute delay, email alerting on failure.

---

## Data Quality

dbt tests are defined in `schema.yml` for both staging and mart layers:

- `not_null` on all key columns
- `unique` on primary keys (e.g. `airline_code`, `airport_id`)
- `dbt_utils.unique_combination_of_columns` on composite keys (flight-level grain)
- `dbt_utils.accepted_range` on derived metrics — `delay_rate` bounded between 0 and 1, `total_flights` must be ≥ 1

---

## Dashboard

The pipeline outputs feed a BI dashboard with four views:

**Overview** — high-level delay trends across airlines and airports

**Airline Performance** — delay rate and average delay by carrier

**Delay Drivers** — weather and holiday impact analysis

**Recommendations** — operational insights derived from the data

### Key Findings

- Delay rates are moderately higher under bad weather conditions, confirming environmental impact on operations
- Holiday periods do not significantly affect delay rates, indicating stable scheduling performance during peak travel
- Delay rates vary considerably across airports, highlighting operational inefficiencies at specific locations
- High-volume airlines tend to maintain more stable delay performance compared to smaller carriers
- Airport-level differences appear to be a stronger driver of delays than external factors like weather or holidays

---

## Setup

### 1. Create Python environment

```bash
python3.11 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your PostgreSQL connection details
```

### 3. Configure dbt profile for Airflow

```bash
cp airflow/dbt/profiles.yml.example airflow/dbt/profiles.yml
# Add your BigQuery project configuration
```

### 4. Configure Airflow

```bash
cp airflow/.env.example airflow/.env
# Set admin credentials, alert email, and mount paths
```

### 5. Start Airflow

```bash
cd airflow
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080)

### 6. Run dbt manually (optional)

```bash
cd flight_dbt
dbt run
dbt test
```

---

## Design Decisions & Known Limitations

- **Ingestion is not yet orchestrated by Airflow** — ingestion scripts are run manually. Adding ingestion as Airflow tasks is the primary planned improvement.
- **Weather enrichment uses a simplified approach** — weather is averaged at the airport-day level from Open-Meteo, and does not represent flight-level conditions at the exact departure time.
- **Airflow uses SQLite as its metadata backend** — this is intentional for local development simplicity. A PostgreSQL backend would be required for any distributed or production deployment.
- **Credentials are managed locally** — secrets are excluded from Git via `.gitignore`. A managed secrets service (e.g. GCP Secret Manager) would be appropriate for production.

---

## Repository Notes

- Large datasets are not tracked in Git (`data/` is excluded)
- Credentials, Airflow metadata, dbt artifacts, and logs are excluded via `.gitignore`
- Example config files are provided for all environment files
- Real secrets must remain local and never be committed

