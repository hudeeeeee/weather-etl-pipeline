from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'dat_do',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_pipeline_v1',
    default_args=default_args,
    start_date=datetime(2026, 6, 15),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Thu thập dữ liệu
    get_data = BashOperator(
        task_id='fetch_weather',
        bash_command='python /opt/airflow/src/pipeline.py'
    )

    # Task 2: Bơm dữ liệu
    load_data = BashOperator(
        task_id='load_to_sql',
        bash_command='python /opt/airflow/src/load_to_sql.py'
    )

    # Thiết lập thứ tự: Fetch xong -> Load
    get_data >> load_data