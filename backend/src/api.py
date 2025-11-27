import io
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']
IMAGE_SIZE = 128

# -------------------------------
# LOAD MODEL LOCALLY FROM DOCKER
# -------------------------------
MODEL_PATH = "model.h5"

print(f"🔄 Loading model from local file: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully!")


def preprocess_image(image):
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = image.convert("RGB")

    img = np.array(image, dtype=np.float32)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img_bytes = file.read()

    try:
        image = Image.open(io.BytesIO(img_bytes))
    except:
        return jsonify({"error": "Invalid image format"}), 400

    img_array = preprocess_image(image)
    preds = model.predict(img_array)

    class_index = int(np.argmax(preds))
    class_name = CLASSES[class_index]
    confidence = float(np.max(preds))

    return jsonify({
        "filename": file.filename,
        "prediction": class_name,
        "confidence": confidence
    })


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "HI, How are you?"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
