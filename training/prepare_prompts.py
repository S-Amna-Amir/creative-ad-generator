import pandas as pd
import mlflow
import os
from pathlib import Path

BASE_DATA_PATH = os.getenv("DATA_ROOT", "data")

INPUT_PATH = f"{BASE_DATA_PATH}/processed/products_clean.csv"
OUTPUT_PATH = f"{BASE_DATA_PATH}/processed/prompts.csv"



mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
)
mlflow.set_experiment("product_data_pipeline")

def prepare_prompts():
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    with mlflow.start_run(run_name="prepare_prompts"):
        df = pd.read_csv(INPUT_PATH)

        prompt_template = "Create an ad for {product}: {description}"
        df["prompt"] = df.apply(
            lambda r: prompt_template.format(
                product=r.product_name,
                description=r.description
            ),
            axis=1
        )

        df[["prompt"]].to_csv(OUTPUT_PATH, index=False)

        # ---- Logging ----
        mlflow.log_param("prompt_template", prompt_template)
        mlflow.log_metric("num_prompts", len(df))
        mlflow.log_artifact(OUTPUT_PATH)

if __name__ == "__main__":
    prepare_prompts()
