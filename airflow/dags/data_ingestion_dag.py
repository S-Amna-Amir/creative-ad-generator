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

def run_preprocess():
    result = subprocess.run(
        ["python", f"{PROJECT_ROOT}/preprocess.py"],
        capture_output = True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()

def run_prepare_prompts():
    result = subprocess.run(
        ["python", f"{PROJECT_ROOT}/prepare_prompts.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()

with DAG(
    dag_id="product_data_ingestion",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["data", "mlflow"],
) as dag:

    preprocess_task = PythonOperator(
        task_id="preprocess_product_data",
        python_callable=run_preprocess
    )

    prepare_prompts_task = PythonOperator(
        task_id="prepare_prompts",
        python_callable=run_prepare_prompts
    )

    preprocess_task >> prepare_prompts_task
