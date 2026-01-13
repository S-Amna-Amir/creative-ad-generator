from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

PROJECT_ROOT = "/opt/project/training"

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def generate_ads():
    result = subprocess.run(
        ["python", f"{PROJECT_ROOT}/generate_ads.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()

with DAG(
    dag_id="batch_ad_generation",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["inference", "ads"],
) as dag:

    generate_task = PythonOperator(
        task_id="generate_ads_batch",
        python_callable=generate_ads
    )
