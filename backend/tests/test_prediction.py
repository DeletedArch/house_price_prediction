import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_price_success():
    payload = {
        "location": "Whitefield",
        "total_sqft": 1200.0,
        "bath": 2,
        "bhk": 2
    }
    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0
    assert data["features_used"]["location"] == "Whitefield"


def test_predict_price_invalid_input():
    payload = {
        "location": "Whitefield",
        "total_sqft": -500.0,
        "bath": 0,
        "bhk": 0
    }
    response = client.post("/api/v1/predict/", json=payload)
    assert response.status_code == 422
