import tensorflow as tf
import mlflow
import mlflow.tensorflow

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

IMG_SIZE = 128
BATCH_SIZE = 16
EPOCHS = 5


def load_data():
    datagen = ImageDataGenerator(
        rescale=1/255.0,
        validation_split=0.2
    )

    train_gen = datagen.flow_from_directory(
        "data/raw/Training",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        subset="training"
    )

    val_gen = datagen.flow_from_directory(
        "data/raw/Training",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        subset="validation"
    )

    return train_gen, val_gen


def load_test_data():
    test_datagen = ImageDataGenerator(rescale=1/255.0)

    test_gen = test_datagen.flow_from_directory(
        "data/raw/Testing",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=False
    )

    return test_gen


def build_model():
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )

    base_model.trainable = False  # Freeze base model

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

    mlflow.set_tracking_uri("file:///home/madhav/Desktop/BrainTumor-SPE/mlruns")
    mlflow.set_experiment("brain_tumor_mobilenetv2")

    train_gen, val_gen = load_data()
    test_gen = load_test_data()

    with mlflow.start_run():

        model = build_model()

        # Train model
        model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS
        )

        # Evaluate on test dataset
        test_loss, test_acc = model.evaluate(test_gen)
        print(f"\n🧪 Test Accuracy: {test_acc:.4f}")
        print(f"🧪 Test Loss: {test_loss:.4f}\n")

        # Log metrics to MLflow
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_loss", test_loss)

        # Save locally
        model.save("models/mobilenetv2_brain_tumor.h5")

        # Register in MLflow
        mlflow.tensorflow.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="BrainTumorMobileNetV2"
        )

        print("\n🚀 Model trained, tested & registered successfully!\n")


if __name__ == "__main__":
    save_and_register_model()
