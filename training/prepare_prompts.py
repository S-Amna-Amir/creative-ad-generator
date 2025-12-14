import pandas as pd
import mlflow
import os
from pathlib import Path


INPUT_PATH = "/opt/project/data/processed/products_clean.csv"
OUTPUT_PATH = "/opt/project/data/processed/prompts.csv"


mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
mlflow.set_experiment("product_data_pipeline")


def prepare_prompts():
    
    import mlflow
    import pandas as pd
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)


    with mlflow.start_run(run_name="prepare_prompts"):
        df = pd.read_csv(INPUT_PATH)
        df["prompt"] = df.apply(
        lambda r: f"Create an ad for {r.product_name}: {r.description}", axis=1
        )
        df[["prompt"]].to_csv(OUTPUT_PATH, index=False)


        mlflow.log_metric("num_prompts", len(df))
        mlflow.log_artifact(OUTPUT_PATH)

if __name__ == "__main__":
    prepare_prompts()