from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

from .prompts import CV_REVIEW_PROMPT, DEFAULT_SYSTEM_PROMPT

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


@dataclass(frozen=True)
class AzureOpenAISettings:
    endpoint: str
    api_key: str
    deployment: str
    api_version: str

    @classmethod
    def from_env(cls) -> "AzureOpenAISettings | None":
        load_dotenv()
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
        api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview").strip()
        if not endpoint or not api_key or not deployment:
            return None
        return cls(
            endpoint=endpoint,
            api_key=api_key,
            deployment=deployment,
            api_version=api_version,
        )


def answer_question(
    question: str,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    *,
    response_format: dict[str, str] | None = None,
    max_tokens: int = 600,
) -> str:
    settings = AzureOpenAISettings.from_env()
    if settings is None or AzureOpenAI is None:
        return mock_answer(question, response_format=response_format)

    client = AzureOpenAI(
        azure_endpoint=settings.endpoint,
        api_key=settings.api_key,
        api_version=settings.api_version,
    )
    kwargs: dict[str, Any] = {
        "model": settings.deployment,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


def mock_answer(question: str, *, response_format: dict[str, str] | None = None) -> str:
    if response_format and response_format.get("type") == "json_object":
        # Return a deterministic JSON object so the CV UI can render in mock mode.
        payload = {
            "strengths": [
                "[mock] Clear structure with sections",
                "[mock] Quantified one project outcome",
                "[mock] Concise summary at the top",
            ],
            "weaknesses": [
                "[mock] No internship or work experience listed",
                "[mock] Skills section is generic",
                "[mock] Education dates are missing",
            ],
            "suggestions": [
                "[mock] Add a short project description with metrics.",
                "[mock] Group skills by category and remove duplicates.",
                "[mock] Replace 'team player' with one concrete teamwork example.",
            ],
            "red_flags": [],
            "mock_mode": True,
        }
        return json.dumps(payload, ensure_ascii=False)

    trimmed = " ".join(question.split())[:160]
    return (
        "[mock mode] Azure credentials are not configured yet.\n\n"
        f"Question: {trimmed}\n\n"
        "Suggested next step: define the target user, expected output, and one "
        "evaluation example. Then connect an Azure OpenAI deployment through .env."
    )


def review_cv(cv_text: str) -> dict[str, Any]:
    """Run the CV reviewer prompt and return parsed JSON.

    Wraps answer_question() with json_object response format and CV_REVIEW_PROMPT.
    Returns the parsed dict including {strengths, weaknesses, suggestions, red_flags}.
    """
    raw = answer_question(
        cv_text,
        system_prompt=CV_REVIEW_PROMPT,
        response_format={"type": "json_object"},
        max_tokens=400,
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "red_flags": ["model_returned_unparseable_json"],
            "raw": raw,
        }
