from __future__ import annotations

import json
import os
from typing import Any

from prompts import JUDGE_PROMPT, RUBRIC

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


TEST_CASE = {
    "question": "Where should students ask about course registration?",
    "facts": "Course registration questions should go to the registrar office. Do not invent office hours.",
    "answer": "Students should contact the registrar office for course registration. Office hours are not provided in the source.",
}


def local_evaluate(case: dict[str, str]) -> dict[str, Any]:
    answer = case["answer"].lower()
    facts = case["facts"].lower()
    issues = []
    if "registrar" not in answer:
        issues.append("Missing source-supported office.")
    if "9" in answer or "monday" in answer:
        issues.append("Invented schedule detail.")
    if len(case["answer"].split()) > 60:
        issues.append("Too long for a demo screen.")
    score = 5 - len(issues)
    return {
        "mode": "mock",
        "rubric": RUBRIC,
        "score": max(score, 1),
        "strengths": ["Uses the registrar fact"] if "registrar" in facts and "registrar" in answer else [],
        "issues": issues,
        "next_test": "Ask an out-of-scope question and verify a polite refusal.",
    }


def azure_evaluate(case: dict[str, str]) -> dict[str, Any] | None:
    if AzureOpenAI is None:
        return None
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
    if not endpoint or not key or not deployment:
        return None

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    )
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": json.dumps(case)},
        ],
        response_format={"type": "json_object"},
        max_tokens=400,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    result["mode"] = "azure"
    return result


if __name__ == "__main__":
    print(json.dumps(azure_evaluate(TEST_CASE) or local_evaluate(TEST_CASE), indent=2))
