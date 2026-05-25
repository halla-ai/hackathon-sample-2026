from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


async def mock_stream() -> AsyncIterator[str]:
    text = "Streaming lets the user see progress while the final answer is still being generated."
    for token in text.split():
        await asyncio.sleep(0.03)
        yield token + " "


async def azure_stream(prompt: str) -> AsyncIterator[str] | None:
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
    stream = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Answer in one short paragraph."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
        max_tokens=200,
    )

    async def iterator() -> AsyncIterator[str]:
        for chunk in stream:
            piece = chunk.choices[0].delta.content or ""
            if piece:
                yield piece

    return iterator()


async def main() -> None:
    prompt = "Explain why streaming improves a hackathon demo."
    stream = await azure_stream(prompt) or mock_stream()
    async for piece in stream:
        print(piece, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
