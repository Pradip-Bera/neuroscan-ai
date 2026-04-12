from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import gdown
import os

app = FastAPI()

# -------------------------------
# Model Download (Google Drive)
# -------------------------------
MODEL_PATH = "best_brain_tumor_model.h5"

if not os.path.exists(MODEL_PATH):
    url = "https://drive.google.com/uc?export=download&id=1W-PUtTe8CJN6395B0g0AU8LnCeLNJL6r"
    gdown.download(url, MODEL_PATH, quiet=False)

# Load model
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# -------------------------------
# Config
# -------------------------------
IMG_SIZE = 224
CLASS_NAMES = ['glioma', 'meningioma', 'no_tumor', 'pituitary']

# -------------------------------
# Preprocessing
# -------------------------------
def preprocess_image(image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "Brain Tumor Detection API Running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    processed = preprocess_image(image)

    predictions = model.predict(processed)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = float(np.max(predictions))

    return {
        "prediction": predicted_class,
        "confidence": confidence
    }