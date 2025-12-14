import pandas as pd
import os
from pathlib import Path

RAW_DATA_PATH = "/opt/project/data/raw/products.csv"
PROCESSED_DATA_PATH = "/opt/project/data/processed/products_clean.csv"


def clean_text(text: str) -> str:
    return text.lower().strip()


def preprocess():
    # ⬇️ IMPORTS MUST BE INSIDE FUNCTION
    import mlflow

    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    )
    mlflow.set_experiment("product_data_pipeline")

    Path(PROCESSED_DATA_PATH).parent.mkdir(parents=True, exist_ok=True)

    with mlflow.start_run(run_name="preprocess_products"):
        df = pd.read_csv(RAW_DATA_PATH)

        df["product_name"] = df["product_name"].apply(clean_text)
        df["description"] = df["description"].apply(clean_text)
        df["category"] = df["category"].apply(clean_text)

        df.to_csv(PROCESSED_DATA_PATH, index=False)

        mlflow.log_metric("num_rows", len(df))
        mlflow.log_metric("num_columns", len(df.columns))
        mlflow.log_artifact(PROCESSED_DATA_PATH)


if __name__ == "__main__":
    preprocess()