# Flight Delay Pipeline

Production-style end-to-end data pipeline for flight delay analytics using Python, Parquet, PostgreSQL, BigQuery, dbt, and Apache Airflow.

## Architecture

Raw Data → Python Ingestion → Parquet → PostgreSQL → BigQuery → dbt → Airflow

## What This Project Does

This project implements a complete analytics pipeline for U.S. flight delay data.

It ingests multiple data sources including flight records, weather data, and holiday information, transforms them into standardized datasets, models them in BigQuery using dbt, and orchestrates the workflow with Apache Airflow.

The goal of the project is to answer business and operational questions such as:

- Which airlines experience the highest delays?
- Which airports show the worst departure delay performance?
- How much do weather conditions affect delays?
- Do holidays increase delay rates?
- Which factors drive delay variation most strongly?

## Pipeline Overview

- **Ingestion:** Python scripts collect and process flight, weather, and holiday data
- **Storage:** Data is standardized and persisted as parquet files
- **Database Loading:** Processed data is loaded into PostgreSQL for intermediate storage and validation
- **Warehouse:** Curated datasets are loaded into BigQuery
- **Transformation:** dbt builds staging and mart models
- **Orchestration:** Airflow schedules and runs `dbt run` and `dbt test`
- **Validation:** dbt tests enforce data quality and model reliability

## Tech Stack

- Python
- PostgreSQL
- Google Cloud Storage
- Google BigQuery
- dbt
- Apache Airflow
- Docker
- Parquet

## Project Structure

```text
.
├── airflow/            # Airflow Docker setup and DAGs
├── data/               # Local raw and processed data (not tracked in Git)
├── flight_dbt/         # dbt project
├── notebooks/          # EDA and prototyping
├── src/ingestion/      # Python ingestion scripts
├── .env.example        # Example local configuration
├── requirements.txt    # Python dependencies
└── README.md
```

## Core Components

- `src/ingestion/ingest_raw.py`  
  Converts raw flight CSV files into parquet format

- `src/ingestion/ingest_weather_api.py`  
  Fetches historical weather data from Open-Meteo API

- `src/ingestion/holidays.py`  
  Loads U.S. holiday data into PostgreSQL

- `src/ingestion/parquet_to_db.py`  
  Loads curated parquet datasets into PostgreSQL

- `flight_dbt/models/staging/`  
  Staging layer models for standardized source access

- `flight_dbt/models/marts/`  
  Analytics-ready mart models and KPI tables

- `airflow/dags/flight_dbt_dag.py`  
  Airflow DAG that orchestrates `dbt run` and `dbt test`

## Key Features

- End-to-end pipeline from ingestion to orchestration
- Multi-source data integration
- Modular dbt modeling with staging and marts layers
- Automated Airflow scheduling
- Retry handling and failure alerting
- Data quality testing with dbt
- Environment-based configuration without hardcoded secrets
- Portable local setup using Docker

## Setup

### 1. Create Python environment

```bash
python3.11 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

### 2. Configure local environment variables

Create `.env` from `.env.example` and provide your PostgreSQL connection details.

### 3. Configure dbt profile for Airflow

Create:

```text
airflow/dbt/profiles.yml
```

from:

```text
airflow/dbt/profiles.yml.example
```

and add your BigQuery project configuration.

### 4. Configure Airflow

Create:

```text
airflow/.env
```

from:

```text
airflow/.env.example
```

This file can be used to override Airflow admin credentials, alert email, and mount paths.

### 5. Start Airflow

```bash
cd airflow
docker compose up --build
```

Then open:

```text
http://localhost:8080
```

### 6. Run dbt manually (optional)

```bash
cd flight_dbt
dbt run
dbt test
```

## Data Models

The dbt project is structured into two main layers:

- **Staging**  
  Standardized source-facing models used to isolate upstream schema changes

- **Marts**  
  Business-facing analytical models used to answer project questions

Main mart outputs include:

- `enriched_flights`
- `fct_airline_delay_summary`
- `fct_airport_departure_delay_summary`
- `fct_weather_delay_impact_summary`
- `fct_holiday_delay_impact_summary`

## Repository Notes

- Large datasets are intentionally not tracked in Git
- Credentials, Airflow metadata, dbt artifacts, and local logs are excluded via `.gitignore`
- Example config files are included for reproducibility
- Real secrets must remain local

## Current Status

This project is end-to-end and portfolio-ready.

Completed components:

- ingestion layer
- parquet-based storage layer
- PostgreSQL loading
- BigQuery warehouse loading
- dbt staging and mart models
- dbt data quality tests
- Airflow orchestration
- scheduling, retries, and failure notifications

## Known Limitations

- Weather enrichment uses a simplified approach and does not yet represent full airport-level weather coverage for every flight
- Airflow setup is designed for local development, not a distributed production deployment
- Secrets are managed locally through ignored config files rather than a managed secret service

## Future Improvements

- Add ingestion tasks directly into the Airflow DAG
- Add BI / dashboard layer
- Add source freshness monitoring
- Integrate managed secrets storage
- Add CI/CD checks for dbt and pipeline validation

## Summary

This project demonstrates how to design and implement a production-style end-to-end data pipeline with ingestion, transformation, testing, and orchestration layers.

It focuses on modularity, reproducibility, data quality, and analytics readiness, while also reflecting real-world engineering concerns such as scheduling, retries, alerting, and configuration management.
