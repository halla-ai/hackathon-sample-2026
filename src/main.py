from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .ai_client import answer_question, review_cv
from .prompts import DEFAULT_SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "static"

app = FastAPI(title="KOICA-TIU Hackathon Sample — CV Review", version="0.2.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)
    system_prompt: Optional[str] = Field(default=None, max_length=4000)


class AnswerResponse(BaseModel):
    answer: str
    mode: str


class CVRequest(BaseModel):
    cv: str = Field(..., min_length=20, max_length=8000)


class CVResponse(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    mode: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(payload: QuestionRequest) -> AnswerResponse:
    prompt = payload.system_prompt or DEFAULT_SYSTEM_PROMPT
    answer = answer_question(payload.question, prompt)
    mode = "mock" if answer.startswith("[mock mode]") else "azure"
    return AnswerResponse(answer=answer, mode=mode)


@app.post("/review", response_model=CVResponse)
def review(payload: CVRequest) -> CVResponse:
    parsed: dict[str, Any] = review_cv(payload.cv)
    mode = "mock" if parsed.get("mock_mode") else "azure"
    return CVResponse(
        strengths=list(parsed.get("strengths") or []),
        weaknesses=list(parsed.get("weaknesses") or []),
        suggestions=list(parsed.get("suggestions") or []),
        red_flags=list(parsed.get("red_flags") or []),
        mode=mode,
    )
