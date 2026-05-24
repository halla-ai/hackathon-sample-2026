# KOICA-TIU Hackathon Sample 2026

KOICA-TIU 2026 hackathon teams can use this repository as a template for Azure
AI Foundry and Azure OpenAI projects. The sample is intentionally small:
FastAPI backend, static frontend, prompt examples, and deployment notes.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload
```

Open `http://127.0.0.1:8000` and ask a question. Without Azure credentials,
the app returns a deterministic mock answer so teams can build UI and workflow
first.

## Connect Azure OpenAI

Create an Azure AI Foundry project, deploy a chat model, then fill `.env`:

```bash
AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Restart the server after updating `.env`.

## Project Shape

```text
src/main.py          FastAPI app and API routes
src/ai_client.py     Azure OpenAI client with mock fallback
src/prompts.py       reusable prompt templates
static/              simple web UI
docs/PROMPT_PACK.md  copy-paste prompts for teams
docs/PROJECT_IDEAS.md starter project ideas
docs/AZURE_DEPLOY.md Azure setup and deployment checklist
docs/TUTOR_REVIEW.md tutor review rubric and coaching flow
```

## Team Workflow

1. Pick one project idea and one target user.
2. Replace the system prompt in `src/prompts.py`.
3. Add 5-10 sample questions for your target user.
4. Test the response quality with `docs/PROMPT_PACK.md`.
5. Prepare a 3-minute demo: problem, user flow, Azure service, result, next step.

## Cost Guardrails

- Use one shared deployment per team unless the tutor assigns more.
- Keep max output tokens low while prototyping.
- Do not paste private personal data into prompts.
- Stop background tests after the demo.
- Record expected daily token use in your team log.

## License

MIT
