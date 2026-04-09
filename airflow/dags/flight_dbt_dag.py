import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


ALERT_EMAIL = os.getenv("AIRFLOW_ALERT_EMAIL", "alerts@example.com")

with DAG(
    dag_id='flight_dbt_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 9 * * *',
    catchup=False,
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'email': [ALERT_EMAIL],
        'email_on_failure': True,
        'email_on_retry': False,
    }
) as dag:
    
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/flight_dbt && dbt run',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/flight_dbt && dbt test',
    )

    dbt_run >> dbt_test
