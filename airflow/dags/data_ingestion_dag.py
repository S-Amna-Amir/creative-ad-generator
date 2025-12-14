from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

PROJECT_ROOT = "/opt/project/training"


def run_preprocess():
    subprocess.run(
        ["python", f"{PROJECT_ROOT}/preprocess.py"],
        check=True
    )


def run_prepare_prompts():
    subprocess.run(
        ["python", f"{PROJECT_ROOT}/prepare_prompts.py"],
        check=True
    )


with DAG(
    dag_id="product_data_ingestion",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
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