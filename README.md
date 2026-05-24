# KOICA-TIU Hackathon Sample 2026

KOICA-TIU 2026 hackathon teams can use this repository as a template for Azure
AI Foundry and Azure OpenAI projects. The sample is intentionally small:
FastAPI backend, static frontend, prompt examples, and deployment notes.

## Quick Start

Use this order during the hackathon:

1. Start in mock mode so the UI and README are ready before spending Azure quota.
2. Add the assigned Azure values to `.env`.
3. Run one short model call and save a backup screenshot.

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
docs/HACKATHON_DAY.md first 30 minutes, roles, submission checklist
```

## Build Paths

| Path | Target |
|---|---|
| 30 minutes | Run mock mode, rename the project, define one user, prepare one demo question. |
| 2 hours | Connect Azure OpenAI, add a small public or synthetic context, show one complete user flow. |
| One day | Polish the UI, add evaluation questions, prepare backup screenshots, rehearse the 3-minute demo. |

## Team Workflow

1. Pick one project idea and one target user.
2. Replace the system prompt in `src/prompts.py`.
3. Add 5-10 sample questions for your target user.
4. Test the response quality with `docs/PROMPT_PACK.md`.
5. Prepare a 3-minute demo: problem, user flow, Azure service, result, next step.
6. Ask your tutor to review the project with `docs/TUTOR_REVIEW.md`.

## Required Submission

- Team repository with source code, README, `.env.example`, and no real secrets.
- 5-slide deck: problem, user, Azure workflow, demo result, limitation/next step.
- Demo link or backup screenshots/video.
- Short cost note explaining which Azure services were used.

## Cost Guardrails

- Use one shared deployment per team unless the tutor assigns more.
- Keep max output tokens low while prototyping.
- Do not paste private personal data into prompts.
- Stop background tests after the demo.
- Record expected daily token use in your team log.

## License

MIT
