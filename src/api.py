import io
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import mlflow
import mlflow.tensorflow
import tensorflow as tf
from flask_cors import CORS
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)
CORS(app)

mlflow.set_tracking_uri("http://127.0.0.1:5000")

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

MODEL_URI = "models:/BrainTumorMobileNetV2/Production"

print(f"🔄 Loading model from MLflow Registry: {MODEL_URI}")
model = mlflow.tensorflow.load_model(MODEL_URI)
print("✅ Model loaded successfully from MLflow!")

IMAGE_SIZE = 128

def preprocess_image(image):
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = image.convert("RGB")

    img = np.array(image, dtype=np.float32)
    img = preprocess_input(img)   # MobileNetV2 preprocessing
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
