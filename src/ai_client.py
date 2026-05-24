from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from .prompts import DEFAULT_SYSTEM_PROMPT

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


def answer_question(question: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    settings = AzureOpenAISettings.from_env()
    if settings is None or AzureOpenAI is None:
        return mock_answer(question)

    client = AzureOpenAI(
        azure_endpoint=settings.endpoint,
        api_key=settings.api_key,
        api_version=settings.api_version,
    )
    response = client.chat.completions.create(
        model=settings.deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=600,
    )
    return response.choices[0].message.content or ""


def mock_answer(question: str) -> str:
    trimmed = " ".join(question.split())[:160]
    return (
        "[mock mode] Azure credentials are not configured yet.\n\n"
        f"Question: {trimmed}\n\n"
        "Suggested next step: define the target user, expected output, and one "
        "evaluation example. Then connect an Azure OpenAI deployment through .env."
    )
