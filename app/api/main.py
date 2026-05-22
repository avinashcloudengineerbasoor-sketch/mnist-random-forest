from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from pydantic import ValidationError


from PIL import Image

import numpy as np
import json
import logging

from app.services.predictor import run_inference
from app.schemas.metadata import MetadataRequest

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="MNIST Digit Predictor API"
)

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


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

        logger.info(
            f"Received request: {image.filename}"
        )

        metadata_dict = json.loads(metadata)

        validated_metadata = MetadataRequest(
            **metadata_dict
        )

        img = Image.open(image.file).convert("L")

        img = img.resize((28, 28))

        img_array = np.array(img).astype("float32") / 255.0

        result = run_inference(
            img_array,
            validated_metadata.model_dump()
        )

        logger.info(
            f"Prediction success: {result}"
        )

        return result

    except ValidationError as e:

        logger.warning(
            f"Validation failed: {str(e)}"
        )

        raise HTTPException(
            status_code=422,
            detail=e.errors()
        )

    except json.JSONDecodeError:

        logger.warning("Invalid JSON metadata")

        raise HTTPException(
            status_code=400,
            detail="Invalid metadata JSON"
        )

    except Exception as e:

        logger.error(
            f"Internal server error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )