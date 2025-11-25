import tensorflow as tf
import mlflow
import mlflow.tensorflow

from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Flatten, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from dataloader import load_processed_data

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

def build_model():
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.4)(x)
    output = Dense(len(CLASSES), activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(
        optimizer=Adam(1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def train():
    X_train, X_val, y_train, y_val = load_processed_data()

    mlflow.set_experiment("brain_tumor_vgg16")

    with mlflow.start_run():
        model = build_model()

        # history = model.fit(
        #     X_train, y_train,
        #     validation_data=(X_val, y_val),
        #     epochs=1,
        #     batch_size=32
        # )

        # Log validation accuracy
        # mlflow.log_metric("val_acc", max(history.history["val_accuracy"]))

        # Save local model file
        model.save("models/vgg16_model.h5")

        # Log raw .h5 file as artifact
        mlflow.log_artifact("models/vgg16_model.h5", artifact_path="model_file")

        # Log and register MLflow model (NO standalone Keras needed)
        mlflow.tensorflow.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="BrainTumorVGG16"
        )

        print("\n✅ Model successfully logged & registered in MLflow.\n")

if __name__ == "__main__":
    train()
