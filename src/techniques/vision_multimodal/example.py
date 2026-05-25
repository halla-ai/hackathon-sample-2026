from __future__ import annotations

import base64
import json
import mimetypes
import os
import sys
from pathlib import Path

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


PROMPT = """
Extract a compact JSON object from this document image:
title, detected_fields, missing_fields, confidence, next_step.
Use null when the image does not contain enough information.
""".strip()


def mock_extract(image_path: str) -> dict[str, object]:
    return {
        "mode": "mock",
        "image": image_path,
        "title": "Sample student form",
        "detected_fields": ["name", "project topic", "team number"],
        "missing_fields": ["tutor approval"],
        "confidence": 0.72,
        "next_step": "Ask the user to confirm missing fields before submission.",
    }


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def azure_extract(image_path: str) -> dict[str, object] | None:
    if AzureOpenAI is None:
        return None
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
    path = Path(image_path)
    if not endpoint or not key or not deployment or not path.exists():
        return None

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    )
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_uri(path)}},
                ],
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=400,
    )
    result = json.loads(response.choices[0].message.content or "{}")
    result["mode"] = "azure"
    return result


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "sample-document.png"
    print(json.dumps(azure_extract(image_path) or mock_extract(image_path), indent=2))
