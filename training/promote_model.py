import mlflow
from mlflow.tracking import MlflowClient
import os

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
)

MODEL_NAME = "ad-generator"
METRIC_NAME = "avg_quality_score"

client = MlflowClient()

def promote_best_model():
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")

    best_version = None
    best_score = -1

    for v in versions:
        run = client.get_run(v.run_id)
        metrics = run.data.metrics

        score = metrics.get(METRIC_NAME)
        if score is None:
            continue

        if score > best_score:
            best_score = score
            best_version = v.version

    if best_version is None:
        raise ValueError("No valid model versions found with metric")

    for v in versions:
        tag_value = "true" if v.version == best_version else "false"
        client.set_model_version_tag(
            name=MODEL_NAME,
            version=v.version,
            key="champion",
            value=tag_value
        )

    print(
        f"Promoted model version {best_version} as champion "
        f"(score={best_score})"
    )

if __name__ == "__main__":
    promote_best_model()
