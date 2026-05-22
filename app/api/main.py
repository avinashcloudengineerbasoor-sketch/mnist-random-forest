from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import numpy as np
import json

from app.services.predictor import run_inference

app = FastAPI(
    title="MNIST Digit Predictor API"
)


@app.get("/")
def root():

    return {
        "message": "MNIST Prediction API Running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    metadata: str = Form(...)
):

    try:

        img = Image.open(image.file).convert("L")

        img = img.resize((28, 28))

        img_array = np.array(img).astype("float32") / 255.0

        metadata_dict = json.loads(metadata)

        result = run_inference(
            img_array,
            metadata_dict
        )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }