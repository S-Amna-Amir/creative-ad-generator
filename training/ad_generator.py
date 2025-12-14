import os
import torch
import mlflow
from transformers import pipeline

# Set MLflow tracking
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
mlflow.set_experiment("ad_generation")


class AdGenerator:
    def __init__(self):
        with mlflow.start_run(run_name="load_model"):
            self.generator = pipeline(
                "text-generation",
                model="gpt2",
                device=-1  # CPU; set to 0 for GPU
            )
            mlflow.log_param("model", "gpt2")

    def generate(self, product_name: str, description: str) -> str:
        prompt = (
            f"Create a short, catchy social media ad.\n"
            f"Product: {product_name}\n"
            f"Description: {description}\n"
            f"Ad:"
        )

        with mlflow.start_run(run_name="generate_ad", nested=True):
            output = self.generator(
                prompt,
                max_length=80,
                temperature=0.9,
                do_sample=True
            )
            mlflow.log_metric("output_length", len(output[0]["generated_text"]))

        return output[0]["generated_text"]
