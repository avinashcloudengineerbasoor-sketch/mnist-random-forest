from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

def test_predict_endpoint():

    with open(
        "artifacts/example_digit.png",
        "rb"
    ) as image_file:

        response = client.post(
            "/predict",
            files={
                "image": (
                    "digit.png",
                    image_file,
                    "image/png"
                )
            },
            data={
                "metadata": """
                {
                    "pen_pressure": 1.2,
                    "writer_age": 25,
                    "handedness": "right"
                }
                """
            }
        )

    assert response.status_code == 200

    body = response.json()

    assert "predicted_digit" in body

def test_invalid_handedness():

    with open(
        "artifacts/example_digit.png",
        "rb"
    ) as image_file:

        response = client.post(
            "/predict",
            files={
                "image": (
                    "digit.png",
                    image_file,
                    "image/png"
                )
            },
            data={
                "metadata": """
                {
                    "pen_pressure": 1.2,
                    "writer_age": 25,
                    "handedness": "invalid"
                }
                """
            }
        )

    assert response.status_code == 422