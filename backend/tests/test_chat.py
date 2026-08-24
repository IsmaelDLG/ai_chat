from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat():
    response = client.post(
        "/api/chat",
        json={"message": "Hola"},
    )

    assert response.status_code == 200
    assert response.json()["response"]