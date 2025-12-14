from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_preprocessing():
    subprocess.run(
        ["python", "/opt/project/training/preprocess.py"],
        check=True
    )
    subprocess.run(
        ["python", "/opt/project/training/prepare_prompts.py"],
        check=True
    )

with DAG(
    dag_id="product_data_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    preprocess_task = PythonOperator(
        task_id="preprocess_product_data",
        python_callable=run_preprocessing
    )
