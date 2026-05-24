from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_returns_static_ui() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "CV Feedback Bot" in response.text
    assert 'lang="en"' in response.text


def test_ask_mock_mode(monkeypatch) -> None:
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    response = client.post("/ask", json={"question": "Suggest a hackathon idea"})
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "mock"
    assert body["answer"].startswith("[mock mode]")
    assert body["answer"]


def test_tracked_text_is_english_only() -> None:
    import pathlib
    import re

    root = pathlib.Path(__file__).resolve().parents[1]
    tracked_text = [
        ".env.example",
        "README.md",
        "docs/AZURE_DEPLOY.md",
        "docs/CONTAINER_APPS.md",
        "docs/HACKATHON_DAY.md",
        "docs/PROJECT_IDEAS.md",
        "docs/PROMPT_PACK.md",
        "docs/QUICKSTART.md",
        "docs/TROUBLESHOOTING.md",
        "docs/TUTOR_REVIEW.md",
        "docs/WALKTHROUGH.md",
        "src/prompts.py",
        "static/index.html",
    ]
    hangul = re.compile(r"[\u3131-\u318e\uac00-\ud7a3]")
    offenders = [
        path
        for path in tracked_text
        if hangul.search((root / path).read_text(encoding="utf-8"))
    ]
    assert offenders == []
