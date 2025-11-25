import tensorflow as tf
import mlflow
import mlflow.tensorflow

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

def build_model():
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(128, 128, 3)
    )
    
    # Freeze base model
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    output = Dense(len(CLASSES), activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer=Adam(1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def save_and_register_model():

    mlflow.set_experiment("brain_tumor_mobilenetv2")

    with mlflow.start_run():

        model = build_model()

        # Save as .h5 (optional)
        model.save("models/mobilenetv2_brain_tumor.h5")

        # Log MLflow model + Register
        mlflow.tensorflow.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="BrainTumorMobileNetV2"
        )

        print("\nMobileNetV2 model saved & registered successfully!\n")


if __name__ == "__main__":
    save_and_register_model()
