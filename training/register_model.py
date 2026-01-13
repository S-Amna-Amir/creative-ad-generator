import mlflow
import os
from transformers import pipeline

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
)
mlflow.set_experiment("model_registration")

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

with mlflow.start_run(run_name="register_flan_t5") as run:
    mlflow.log_param("base_model", "google/flan-t5-small")
    mlflow.log_param("framework", "transformers")

    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=FlanT5Wrapper(),
        registered_model_name=MODEL_NAME
    )

print(f"Model registered as {MODEL_NAME}")
