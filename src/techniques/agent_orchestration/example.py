from __future__ import annotations

import json
import os
from typing import Any

from prompts import SYSTEM_PROMPT, TOOLS

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore[assignment]


FAQ = {
    "schedule": "Build sprint starts at 10:30 and demo freeze is at 15:00.",
    "submission": "Submit source code, a five-slide deck, and a demo link or backup recording.",
    "cost": "Use the assigned deployment, keep outputs short, and stop background loops.",
    "azure": "Use only resources marked Allowed now unless a tutor approves an exception.",
}


def lookup_faq(topic: str) -> dict[str, str]:
    key = topic.lower().strip()
    return {"topic": key, "answer": FAQ.get(key, "No public FAQ match. Ask a tutor.")}


def escalate_to_human(reason: str, urgency: str = "normal") -> dict[str, str]:
    return {"owner": "tutor", "urgency": urgency, "reason": reason}


def mock_triage(question: str) -> dict[str, Any]:
    text = question.lower()
    if any(word in text for word in ["login", "account", "key", "private"]):
        tool = "escalate_to_human"
        result = escalate_to_human("Student account or secret-related issue", "high")
    else:
        topic = next((key for key in FAQ if key in text), "schedule")
        tool = "lookup_faq"
        result = lookup_faq(topic)
    return {
        "mode": "mock",
        "question": question,
        "tool_used": tool,
        "tool_result": result,
        "agent_reply": f"Used {tool}. Next, show the result and ask whether the user needs tutor help.",
    }


def azure_triage(question: str) -> dict[str, Any] | None:
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
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    first = client.chat.completions.create(model=deployment, messages=messages, tools=TOOLS)
    message = first.choices[0].message
    if not message.tool_calls:
        return {"mode": "azure", "agent_reply": message.content, "tool_used": None}

    call = message.tool_calls[0]
    args = json.loads(call.function.arguments or "{}")
    result = lookup_faq(**args) if call.function.name == "lookup_faq" else escalate_to_human(**args)
    messages.extend(
        [
            message.model_dump(),
            {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)},
        ]
    )
    final = client.chat.completions.create(model=deployment, messages=messages)
    return {
        "mode": "azure",
        "tool_used": call.function.name,
        "tool_result": result,
        "agent_reply": final.choices[0].message.content,
    }


if __name__ == "__main__":
    question = "What should we submit, and what if our Azure key does not work?"
    print(json.dumps(azure_triage(question) or mock_triage(question), indent=2))
