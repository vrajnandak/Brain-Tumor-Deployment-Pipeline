import mlflow
import mlflow.tensorflow
import tensorflow as tf
from mlflow.tracking import MlflowClient
import os

# -------------------------
# CONFIGURATION
# -------------------------
MODEL_NAME = "BrainTumorMobileNetV2"
EXPORT_PATH = "model.h5"                        # output file

# -------------------------
# CONNECT TO MLFLOW SERVER
# -------------------------
mlflow.set_tracking_uri("file:///home/madhav/Desktop/BrainTumor-SPE/mlruns")
client = MlflowClient()

print(f"🔍 Checking latest Production version of model: {MODEL_NAME}")

# -------------------------
# GET LATEST PRODUCTION MODEL
# -------------------------
versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])

if len(versions) == 0:
    raise ValueError(f"No Production version found for model '{MODEL_NAME}'")

latest_model = versions[0]
model_version = latest_model.version

print(f"➡ Latest Production version: {model_version}")
print(f"➡ Source run ID: {latest_model.run_id}")

# -------------------------
# DOWNLOAD MODEL FROM REGISTRY
# -------------------------
model_uri = f"models:/{MODEL_NAME}/{model_version}"

print(f"⬇ Downloading model from MLflow Registry: {model_uri}")
tf_model = mlflow.tensorflow.load_model(model_uri)

# -------------------------
# SAVE AS model.h5
# -------------------------
tf_model.save(EXPORT_PATH)

print(f"✅ Model exported successfully → {EXPORT_PATH}")