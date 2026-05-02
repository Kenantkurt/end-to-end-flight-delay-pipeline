# ✈️ Flight Delay Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-2.9.1-017CEE?logo=apache-airflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-latest-FF6849?logo=dbt&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

An end-to-end **ELT analytics pipeline** for U.S. domestic flight delay data, built with Python, Apache Airflow, dbt, and Google BigQuery — from raw CSV ingestion to business-ready analytics models.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Running the Pipeline](#running-the-pipeline)
- [dbt Models](#dbt-models)
- [Data Quality](#data-quality)
- [Key Findings](#key-findings)
- [Design Decisions & Limitations](#design-decisions--limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

This pipeline answers operational and business questions about U.S. domestic flight delays:

- Which airlines experience the highest delay rates?
- Which airports show the worst departure delay performance?
- How much do weather conditions affect delays?
- Do holidays increase delay rates?
- Which factors drive delay variation most strongly?

**Pattern:** ELT — data is ingested and loaded into the warehouse first, then transformed in-place using dbt.

---

## Architecture

```
Raw Data (BTS CSV + Weather API + Holidays)
            ↓
Python Ingestion (src/ingestion/)
            ↓
Parquet → PostgreSQL (local staging)
            ↓
Google BigQuery (warehouse)
            ↓
dbt Transformations (Staging → Marts)
            ↑
Apache Airflow (daily @ 9 AM UTC)
            ↓
BI Dashboard
```

---

## Tech Stack

| Layer | Tool | Notes |
|-------|------|-------|
| Language | Python 3.11 | Ingestion & scripting |
| Storage | Parquet + PostgreSQL | Local staging |
| Warehouse | Google BigQuery | Cloud analytics |
| Transformation | dbt (dbt-bigquery) | Staging + Mart layers |
| Orchestration | Apache Airflow 2.9.1 | Dockerized |
| Containerization | Docker Compose | Local dev environment |
| Weather API | Open-Meteo | Free, no API key needed |

---

## Project Structure

```
├── airflow/
│   ├── dags/
│   │   └── flight_dbt_dag.py        # Main DAG — edit here to change schedule
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
│
├── flight_dbt/
│   └── models/
│       ├── staging/                 # Source isolation layer
│       │   ├── stg_flight_delays.sql
│       │   ├── stg_airlines.sql
│       │   ├── stg_airports.sql
│       │   ├── stg_weather.sql
│       │   └── stg_holidays.sql
│       └── marts/                   # Business-facing models
│           ├── enriched_flights.sql
│           ├── fct_airline_delay_summary.sql
│           ├── fct_airport_departure_delay_summary.sql
│           ├── fct_weather_delay_impact_summary.sql
│           └── fct_holiday_delay_impact_summary.sql
│
├── src/
│   └── ingestion/
│       ├── ingest_raw.py            # CSV → Parquet
│       ├── ingest_weather_api.py    # Open-Meteo API → Parquet
│       ├── holidays.py              # Holiday calendar → PostgreSQL
│       └── parquet_to_db.py         # Parquet → PostgreSQL
│
├── notebooks/                       # EDA & prototyping
├── .env.example
├── requirements.txt
└── README.md
```

---

## Data Sources

| Dataset | Source | Update Frequency | Cost |
|---------|--------|------------------|------|
| Flight Delays | [BTS On-Time Performance](https://www.transtats.bts.gov/) | Monthly | Free |
| Weather | [Open-Meteo API](https://open-meteo.com/) | Real-time | Free |
| U.S. Holidays | Hardcoded | Annual | N/A |

**How to download flight data:**
1. Visit [BTS Website](https://www.transtats.bts.gov/)
2. Select "On-Time Performance" dataset
3. Choose your date range and download CSV
4. Save to: `data/raw/flights_YYYYMM.csv`

---

## Quick Start

**Prerequisites:** Python 3.11+, Docker & Docker Compose, Google Cloud account

```bash
git clone https://github.com/Kenantkurt/end-to-end-flight-delay-pipeline.git
cd end-to-end-flight-delay-pipeline
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp airflow/.env.example airflow/.env
cp airflow/dbt/profiles.yml.example airflow/dbt/profiles.yml
cd airflow && docker compose up --build
# Open http://localhost:8080
```

---

## Environment Variables

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=flight_delays

# Google Cloud
GCP_PROJECT_ID=your-gcp-project
GCP_REGION=us-central1

# dbt
DBT_DATASET=flight_analytics

# Airflow
AIRFLOW_ADMIN_EMAIL=your@email.com
AIRFLOW_ADMIN_PASSWORD=your-password
```

---

## Running the Pipeline

### First Time Setup

```bash
python src/ingestion/ingest_raw.py
python src/ingestion/ingest_weather_api.py
python src/ingestion/holidays.py
python src/ingestion/parquet_to_db.py
cd flight_dbt && dbt run && dbt test
```

### Daily Automated Runs

Once configured, the Airflow DAG runs automatically **daily at 9 AM UTC**:
- dbt run → dbt test → email alert on failure

### Changing the Schedule

Edit `airflow/dags/flight_dbt_dag.py`:
```python
schedule_interval='0 9 * * *'   # Daily at 9 AM UTC
schedule_interval='0 2 * * 0'   # Weekly on Sunday
schedule_interval='0 1 * * 1-5' # Weekdays at 1 AM
```

---

## dbt Models

### Staging Layer — Source Isolation

| Model | Description |
|-------|-------------|
| `stg_flight_delays` | Flight-level delay records |
| `stg_airlines` | Airline reference data |
| `stg_airports` | Airport reference data |
| `stg_weather` | Weather enrichment at airport-day level |
| `stg_holidays` | U.S. federal holiday calendar |

### Marts Layer — Business Models

| Model | Description |
|-------|-------------|
| `enriched_flights` | Joined flights + weather + holidays |
| `fct_airline_delay_summary` | Delay metrics aggregated by airline |
| `fct_airport_departure_delay_summary` | Airport performance with composite score |
| `fct_weather_delay_impact_summary` | Delay rates by weather condition |
| `fct_holiday_delay_impact_summary` | Holiday vs. non-holiday comparison |

**Design decision:** Ingestion scripts handle all cleaning. Staging models focus on source isolation — keeping Python and SQL responsibilities clearly separated.

---

## Data Quality

| Test | Purpose |
|------|---------|
| `not_null` | Key columns must have values |
| `unique` | No duplicate primary keys |
| `unique_combination_of_columns` | Composite key at flight grain |
| `accepted_range` | `delay_rate` bounded 0–1, `total_flights` ≥ 1 |

```bash
cd flight_dbt && dbt test
dbt test --select fct_airline_delay_summary
```

---

## Key Findings

- **Weather:** Delay rates moderately higher under bad weather — confirms environmental impact
- **Holidays:** Holiday periods do NOT significantly affect delay rates — stable scheduling during peak travel
- **Airports:** Considerable variation across airports — operational inefficiencies at specific locations
- **Carriers:** High-volume airlines maintain more stable performance than smaller carriers
- **Primary driver:** Airport-level differences outweigh weather and holiday factors

---

## Design Decisions & Limitations

**Why ELT?** Load first into BigQuery, transform with dbt. Keeps Python focused on ingestion, SQL on transformation.

**Weather enrichment:** Averaged at airport-day level — does not represent exact flight-level conditions.

**Airflow metadata:** SQLite for local dev simplicity. PostgreSQL backend required for production.

**Secrets:** Managed locally via `.env`. GCP Secret Manager recommended for production.

**Ingestion:** Currently run manually. Moving into Airflow as tasks is the primary planned improvement.

---

## Future Improvements

- [ ] Orchestrate ingestion scripts inside Airflow DAG
- [ ] Switch Airflow metadata from SQLite to PostgreSQL
- [ ] Add GCP Secret Manager for credential management
- [ ] Improve weather enrichment to flight-level granularity
- [ ] Add incremental dbt models to reduce BigQuery costs
- [ ] Add unit tests for Python ingestion scripts
- [ ] Add pipeline monitoring dashboard

---

## Author

**Kenan Kurt** — Aspiring Data Engineer

- 📧 [kenankurt@gmail.com](mailto:kenankurt@gmail.com)
- 🔗 [LinkedIn](https://www.linkedin.com/in/kenan-tufan-k-263000308/)
- 🐙 [GitHub](https://github.com/Kenantkurt)
- 📍 Utrecht, Netherlands
