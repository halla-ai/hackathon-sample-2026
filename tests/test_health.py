from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_mock_mode() -> None:
    response = client.post("/ask", json={"question": "Suggest a hackathon idea"})
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] in {"mock", "azure"}
    assert body["answer"]
