from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'dat_do',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'weather_pipeline_v1',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Khởi chạy script kéo dữ liệu thời tiết
    fetch_weather = BashOperator(
        task_id='fetch_weather',
        bash_command='python /opt/airflow/src/fetch_weather.py'
    )

    # Khởi chạy script bơm dữ liệu vào SQL Server
    load_to_sql = BashOperator(
        task_id='load_to_sql',
        bash_command='python /opt/airflow/src/load_to_sql.py'
    )

    # Thiết lập thứ tự chạy: Kéo dữ liệu xong mới được bơm
    fetch_weather >> load_to_sql