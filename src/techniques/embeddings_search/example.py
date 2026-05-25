from __future__ import annotations

import math
import os
import re
from collections import Counter
from typing import Iterable

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


CORPUS = [
    "Python backend internship with FastAPI, testing, and Docker.",
    "Computer vision project for document screenshots and form extraction.",
    "Data analyst role using SQL, dashboards, and business metrics.",
    "MLOps assistant for deployment checks, monitoring, and cost logs.",
    "Frontend role building accessible React interfaces for students.",
    "Prompt engineering project with evaluation rubrics and safety reviews.",
    "Agent triage project routing FAQ questions and tutor escalations.",
    "Vision reader project extracting fields from document screenshots.",
    "Streaming chat tutor that shows partial answers during practice.",
    "Semantic search over student skills, project ideas, and learning gaps.",
]


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def local_vector(text: str) -> Counter[str]:
    return Counter(tokens(text))


def cosine(left: Counter[str], right: Counter[str]) -> float:
    keys = set(left) | set(right)
    dot = sum(left[k] * right[k] for k in keys)
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    return dot / (left_norm * right_norm or 1.0)


def local_search(query: str, corpus: Iterable[str], top_k: int = 3) -> list[tuple[float, str]]:
    qv = local_vector(query)
    scored = [(cosine(qv, local_vector(text)), text) for text in corpus]
    return sorted(scored, reverse=True)[:top_k]


def azure_embeddings_search(query: str, corpus: list[str], top_k: int = 3) -> list[tuple[float, str]] | None:
    if os.getenv("USE_AZURE_EMBEDDINGS") != "1" or AzureOpenAI is None:
        return None
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "").strip()
    if not endpoint or not key or not deployment:
        return None

    client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version="2024-12-01-preview")
    vectors = client.embeddings.create(model=deployment, input=[query, *corpus]).data
    qv = vectors[0].embedding

    def dense_cosine(vec: list[float]) -> float:
        dot = sum(a * b for a, b in zip(qv, vec))
        return dot / ((sum(a * a for a in qv) ** 0.5) * (sum(b * b for b in vec) ** 0.5) or 1.0)

    return sorted([(dense_cosine(item.embedding), text) for item, text in zip(vectors[1:], corpus)], reverse=True)[:top_k]


if __name__ == "__main__":
    query = "I know Python and Docker and want a backend internship."
    results = azure_embeddings_search(query, CORPUS) or local_search(query, CORPUS)
    for rank, (score, text) in enumerate(results, start=1):
        print(f"{rank}. {score:.3f} - {text}")
