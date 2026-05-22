from app.services.preprocessing import load_example_input
from app.services.predictor import run_inference

img, meta = load_example_input(
    "artifacts/example_digit.png",
    "artifacts/example_metadata.json"
)

result = run_inference(img, meta)

print(result)