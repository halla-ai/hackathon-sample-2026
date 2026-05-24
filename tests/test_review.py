from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


SAMPLE_CV = """
Aisha Karimova
Tashkent International University, BSc in Computer Science (2024-)
Email: aisha.k@example.edu

Projects:
- Campus FAQ Bot (Python, FastAPI, Azure OpenAI) — solo project, 100 sample
  questions, 80 percent answer accuracy on held-out test set.

Skills: Python, Git, basic React.
"""


def test_review_mock_mode(monkeypatch) -> None:
    """Without Azure env, /review should return the deterministic mock JSON."""
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)

    response = client.post("/review", json={"cv": SAMPLE_CV})
    assert response.status_code == 200

    body = response.json()
    assert body["mode"] == "mock"
    assert isinstance(body["strengths"], list)
    assert isinstance(body["weaknesses"], list)
    assert isinstance(body["suggestions"], list)
    assert isinstance(body["red_flags"], list)
    # Mock has 3 each of strengths/weaknesses/suggestions.
    assert len(body["strengths"]) == 3
    assert len(body["weaknesses"]) == 3
    assert len(body["suggestions"]) == 3
    assert all(item.startswith("[mock]") for item in body["strengths"])


def test_review_rejects_short_input() -> None:
    response = client.post("/review", json={"cv": "too short"})
    assert response.status_code == 422


def test_review_rejects_huge_input() -> None:
    response = client.post("/review", json={"cv": "x" * 9000})
    assert response.status_code == 422
