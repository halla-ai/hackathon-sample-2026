# Agent Orchestration

## What this demonstrates

A tiny tool-calling loop where the model chooses between a public FAQ lookup and a tutor escalation.

## Why your hackathon project might want it

Use this when a single answer is not enough and the assistant must choose a next action. It maps to the ReAct and agentic workflow lessons, but keeps the implementation small enough for one day.

## Run it locally

```bash
cd src/techniques/agent_orchestration
python example.py
```

No Azure credentials are required. With no `.env`, the script returns a deterministic mock result.

## Read it line-by-line

The example defines two tools, routes a sample question, executes the selected Python function, and prints the final agent state. If Azure credentials are present, it shows the same pattern with `tool_calls`.

## Extend it

- How could your version remember the last unresolved issue for each team?
- What tool should be human-only because it touches private accounts?
- How would the UI show the tool decision without exposing hidden prompts?
- What should happen when two tools both look relevant?

## Watch out for

- Symptom: the model invents a tool. Cause: the tool schema is too vague. Fix: keep tool names and parameters narrow.
- Symptom: the agent loops forever. Cause: no stop rule. Fix: cap tool calls per request.
- Symptom: private data leaks into logs. Cause: raw user input is stored. Fix: redact before persistence.

## Where to go next

- Public deep dive: https://koica-tiu.halla.ai/hackathon/samples/agent-triage
- Technique catalog: ../../../../docs/TECHNIQUES.md
- Microsoft Learn: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/function-calling
