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

def register_model():
    subprocess.run(
        ["python", f"{PROJECT_ROOT}/register_model.py"],
        check=True
    )

with DAG(
    dag_id="model_registration_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # manual trigger (best practice)
    catchup=False,
    default_args=default_args,
    tags=["mlflow", "model"],
) as dag:

    register_task = PythonOperator(
        task_id="register_ad_generator_model",
        python_callable=register_model
    )
