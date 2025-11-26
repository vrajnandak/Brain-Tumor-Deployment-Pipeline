import mlflow
from mlflow.tracking import MlflowClient

MODEL_NAME = "BrainTumorMobileNetV2"

mlflow.set_tracking_uri("file:///home/madhav/Desktop/BrainTumor-SPE/mlruns")
client = MlflowClient()

def promote_latest_model():
    
    latest_version = client.get_latest_versions(MODEL_NAME, stages=["None"])[0].version

    print(f"🔥 Promoting version {latest_version} to Production...")

    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=latest_version,
        stage="Production",
        archive_existing_versions=True
    )

    print(f"✅ Model version {latest_version} is now in Production!")


if __name__ == "__main__":
    promote_latest_model()
