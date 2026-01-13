import pandas as pd
import os
import mlflow
import mlflow.pyfunc
from transformers import pipeline

from ad_generator import AdGenerator
from quality_check import validity_score


mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
)
mlflow.set_experiment("ad_generation_inference")

BASE_DATA_PATH = os.getenv("DATA_ROOT", "data")
INPUT_PATH = f"{BASE_DATA_PATH}/processed/prompts.csv"
OUTPUT_PATH = f"{BASE_DATA_PATH}/processed/generated_ads.csv"

MODEL_NAME = "ad-generator"


class FlanT5Wrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.generator = pipeline(
            task="text2text-generation",
            model="google/flan-t5-small",
            device=-1
        )

    def predict(self, context, model_input):
        prompts = (
            model_input
            if isinstance(model_input, list)
            else model_input.iloc[:, 0].tolist()
        )
        outputs = self.generator(prompts, max_length=60)
        return [o["generated_text"] for o in outputs]


def main():
    with mlflow.start_run(run_name="batch_generation"):
        df = pd.read_csv(INPUT_PATH)
        generator = AdGenerator()

        ads = []
        scores = []

        for _, row in df.iterrows():
            ad_text = generator.generate(
                product_name=row.get("product_name", ""),
                description=row.get("description", "")
            )
            ads.append(ad_text)
            scores.append(validity_score(ad_text))

        df["generated_ad"] = ads
        df["quality_score"] = scores
        df.to_csv(OUTPUT_PATH, index=False)

        # ---- Metrics ----
        mlflow.log_metric("num_ads", len(df))
        mlflow.log_metric("avg_quality_score", sum(scores) / len(scores))
        mlflow.log_metric("min_quality_score", min(scores))
        mlflow.log_metric("max_quality_score", max(scores))

        # ---- Params ----
        mlflow.log_param("base_model", "google/flan-t5-small")
        mlflow.log_param("generation_temperature", 0.9)
        mlflow.log_param("max_length", 60)

        # ---- Artifacts ----
        mlflow.log_artifact(OUTPUT_PATH)

        # ---- Model registration ----
 

        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=FlanT5Wrapper(),
            registered_model_name=MODEL_NAME
        )

        print(f"Generated ads saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
