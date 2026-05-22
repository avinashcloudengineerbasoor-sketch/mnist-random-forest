import torch
import pandas as pd
import joblib

from app.models.cnn_encoder import CNNEncoder
from app.models.classifier import FinalClassifier

image_model = CNNEncoder()
image_model.load_state_dict(torch.load("artifacts/image_model.pth"))
image_model.eval()

metadata_encoder = joblib.load("artifacts/metadata_encoder.joblib")

meta_dim = metadata_encoder.transform(
    pd.DataFrame([{"pen_pressure": 1.0,
                   "writer_age": 30,
                   "handedness": "right"}])).shape[1]

final_model = FinalClassifier(metadata_dim=meta_dim)
final_model.load_state_dict(torch.load("artifacts/final_classifier.pth"))
final_model.eval()


def run_inference(img_array, metadata_dict):
    img_tensor = torch.tensor(img_array,
                              dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    meta_df = pd.DataFrame([metadata_dict])
    meta_encoded = metadata_encoder.transform(meta_df).astype("float32")
    meta_tensor = torch.tensor(meta_encoded)

    with torch.no_grad():
        img_feat = image_model(img_tensor)
        logits = final_model(img_feat, meta_tensor)
        pred = torch.argmax(logits, dim=1).item()
    return {"predicted_digit": pred}
