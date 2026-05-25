SYSTEM_PROMPT = """
You are a service triage agent for a student-facing hackathon demo.
Pick one small tool call at a time, explain the result, and escalate when
the question needs a human tutor or private account access.
""".strip()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_faq",
            "description": "Look up a public hackathon FAQ answer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Short topic such as schedule, submission, cost, or azure.",
                    }
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Create a concise tutor escalation note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "urgency": {"type": "string", "enum": ["low", "normal", "high"]},
                },
                "required": ["reason", "urgency"],
            },
        },
    },
]
