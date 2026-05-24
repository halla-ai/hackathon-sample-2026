from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .ai_client import answer_question
from .prompts import DEFAULT_SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "static"

app = FastAPI(title="KOICA-TIU Hackathon Sample", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)
    system_prompt: Optional[str] = Field(default=None, max_length=4000)


class AnswerResponse(BaseModel):
    answer: str
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
