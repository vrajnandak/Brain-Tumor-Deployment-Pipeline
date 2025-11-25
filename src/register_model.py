import mlflow
import mlflow.tensorflow
import tensorflow as tf

MODEL_PATH = "models/vgg16_brain_tumor.h5"

def register_model():

    # Load your Keras model
    model = tf.keras.models.load_model(MODEL_PATH)

    # MLflow tracking server
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("SPE_Project")

    with mlflow.start_run():

        mlflow.tensorflow.log_model(
            model=model,                       # <-- correct argument
            artifact_path="model",
            registered_model_name="SPE_Brain_Tumor_Classifier"
        )

        print("\nModel successfully registered in MLflow Model Registry!\n")


if __name__ == "__main__":
    register_model()