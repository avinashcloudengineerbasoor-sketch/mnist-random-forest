from PIL import Image
import numpy as np
import json


def load_example_input(image_path, metadata_path):

    img = Image.open(image_path).convert("L")

    img = np.array(img).astype("float32") / 255.0

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return img, metadata
