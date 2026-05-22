import torch
import torch.optim as optim
from torchvision import datasets, transforms
from PIL import Image
import numpy as np
import pandas as pd
import json
import joblib

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from app.models.cnn_encoder import CNNEncoder
from app.models.classifier import FinalClassifier


def generate_metadata(n):

    rng = np.random.default_rng(42)

    return {
        "pen_pressure": rng.uniform(0.5, 1.5, n),
        "writer_age": rng.integers(10, 80, n),
        "handedness": rng.choice(["left", "right"], n)
    }


def save_example_files(img_array, metadata_row):

    img = Image.fromarray(
        (img_array * 255).astype("uint8"),
        mode="L"
    )

    img.save("artifacts/example_digit.png")

    with open("artifacts/example_metadata.json", "w") as f:
        json.dump(metadata_row, f, indent=2)


def train():

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Using device: {device}")

    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    dataset = datasets.MNIST(
        "./data",
        train=True,
        download=True,
        transform=transform
    )

    images = dataset.data.numpy().astype(np.float32) / 255.0

    images = np.expand_dims(images, 1)

    labels = dataset.targets.numpy()

    print("Generating metadata...")

    metadata_dict = generate_metadata(len(images))

    metadata_df = pd.DataFrame(metadata_dict)

    encoder = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                ["pen_pressure", "writer_age"]
            ),
            (
                "cat",
                OneHotEncoder(),
                ["handedness"]
            )
        ]
    )

    encoder.fit(metadata_df)

    meta_encoded = encoder.transform(
        metadata_df
    ).astype(np.float32)

    X_img = torch.tensor(images)

    X_meta = torch.tensor(meta_encoded)

    y = torch.tensor(
        labels,
        dtype=torch.long
    )

    image_model = CNNEncoder().to(device)

    final_model = FinalClassifier(
        metadata_dim=X_meta.shape[1]
    ).to(device)

    optimizer = optim.Adam(
        list(image_model.parameters()) +
        list(final_model.parameters()),
        lr=1e-3
    )

    loss_fn = torch.nn.CrossEntropyLoss()

    print("Starting training...")

    for i in range(0, len(X_img), 128):

        batch_img = X_img[i:i + 128].to(device)

        batch_meta = X_meta[i:i + 128].to(device)

        batch_y = y[i:i + 128].to(device)

        optimizer.zero_grad()

        img_feat = image_model(batch_img)

        logits = final_model(
            img_feat,
            batch_meta
        )

        loss = loss_fn(logits, batch_y)

        loss.backward()

        optimizer.step()

        if i % 20000 == 0:
            print(
                f"Training step {i}, "
                f"loss={loss.item():.4f}"
            )

    print("Saving model artifacts...")

    torch.save(
        image_model.state_dict(),
        "artifacts/image_model.pth"
    )

    torch.save(
        final_model.state_dict(),
        "artifacts/final_classifier.pth"
    )

    joblib.dump(
        encoder,
        "artifacts/metadata_encoder.joblib"
    )

    example_img = images[0].squeeze()

    example_meta_row = metadata_df.iloc[0].to_dict()

    save_example_files(
        example_img,
        example_meta_row
    )

    print(
        "✅ Training complete. "
        "Model + encoder + example files saved."
    )


if __name__ == "__main__":
    train()