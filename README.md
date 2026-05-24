# KOICA-TIU Hackathon Sample 2026

Template repository for the KOICA-TIU 2026 hackathon (June 20). Clone this repo, swap the prompts and data for your team's project, and ship a working Azure AI demo in a day or less.

The sample is intentionally minimal: FastAPI backend, static frontend, a single Azure OpenAI client with a mock-mode fallback, and copy-paste prompt examples. Nothing here you cannot read in 30 minutes.

> **Full guides on the public site**: [Build paths](https://koica-tiu.halla.ai/hackathon/build-paths) · [Sample tracks](https://koica-tiu.halla.ai/hackathon/samples) · [D-Day flow](https://koica-tiu.halla.ai/hackathon/d-day) · [Judging](https://koica-tiu.halla.ai/hackathon/judging) · [Submission](https://koica-tiu.halla.ai/hackathon/submission)

> 🚀 **Working example**: A complete end-to-end deploy example (CV Feedback Bot → Azure Container Apps, ~₩900 per team) lives on the [`example/career-cv`](https://github.com/halla-ai/hackathon-sample-2026/tree/example/career-cv) branch. The full step-by-step walkthrough is in [`example/career-cv/docs/WALKTHROUGH.md`](https://github.com/halla-ai/hackathon-sample-2026/blob/example/career-cv/docs/WALKTHROUGH.md), also summarized at [koica-tiu.halla.ai/hackathon/walkthrough](https://koica-tiu.halla.ai/hackathon/walkthrough).

---

## Prerequisites

- **Python 3.10+** (`python3 --version`)
- **git** (`git --version`)
- **An Azure account** assigned by the operations team — you only need the endpoint, key, and deployment name (your tutor will provide these on D-day)
- **Docker** (optional) — only if you want to deploy via Container Apps later
- **A terminal you are comfortable with** — macOS Terminal, Windows PowerShell or WSL, or Linux

You can finish the 30-minute path without Azure credentials thanks to mock mode.

---

## Quick Start

Five commands. Should take under five minutes.

```bash
# 1. Create your own repo from this template
#    On GitHub, click "Use this template" -> "Create a new repository".
#    Then clone YOUR new repo locally.
git clone <your-repo-url>
cd <your-repo-name>

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the env template
cp .env.example .env               # leave the values empty for now

# 5. Run the dev server
uvicorn src.main:app --reload
```

Expected output:

```
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Application startup complete.
```

Open <http://127.0.0.1:8000> and submit a question. Without Azure credentials, the app replies with a deterministic mock response that starts with `[mock mode]` — that is the expected state for the 30-minute path.

Need a slower walkthrough? Read [docs/QUICKSTART.md](docs/QUICKSTART.md).

---

## Connect Azure OpenAI

When the tutor confirms your team's Foundry project and the assigned model deployment, edit `.env`:

```bash
AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key-from-foundry>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Restart the server (`Ctrl-C`, then re-run `uvicorn`). The next question you submit returns a real Azure response, and the `mode` indicator in the UI switches from `mock` to `azure`.

Never commit `.env`. The repo's `.gitignore` already excludes it.

---

## Project Shape

```text
src/
  main.py            FastAPI app, routes /, /health, /ask
  ai_client.py       Azure OpenAI client + mock fallback
  prompts.py         DEFAULT_SYSTEM_PROMPT + PROJECT_COACH_PROMPT
  __init__.py
static/
  index.html         single-page UI (textarea + response panel)
  app.js             fetch /ask on form submit
  style.css          minimal styling
docs/
  QUICKSTART.md         first-time setup walkthrough with expected output
  PROMPT_PACK.md        copy-paste prompts for ideation, RAG, evaluation, pitch
  PROJECT_IDEAS.md      six starter project ideas with MVP rules
  AZURE_DEPLOY.md       Azure AI Foundry setup + App Service deployment
  CONTAINER_APPS.md     Azure Container Apps deployment alternative
  TROUBLESHOOTING.md    common errors, symptom → cause → fix
  HACKATHON_DAY.md      June 20 operating checklist
  TUTOR_REVIEW.md       tutor rubric and intervention rules
tests/
  test_health.py     /health and / endpoint smoke tests
Dockerfile           multi-stage build for App Service / Container Apps
.dockerignore
.github/workflows/
  ci.yml             pytest on push and pull request
  deploy.yml         App Service deploy template (commented out by default)
.env.example         endpoint / key / deployment / api_version (empty values)
requirements.txt     fastapi, uvicorn, openai, python-dotenv, pytest, httpx
```

---

## Build Paths

Pick the path that matches the time you have. The public site has [more detail](https://koica-tiu.halla.ai/hackathon/build-paths).

### 30 minutes — Hello-world demo

Goal: prove your team can run the sample and get one mock response on screen.

1. Run the Quick Start above.
2. Open the UI, submit one question, confirm you see `[mock mode]` output.
3. Take a screenshot. Save it to `demo/screenshot.png`.
4. Skim `docs/PROMPT_PACK.md` and pick one prompt that matches your project idea.

**Expected token use**: 0 (mock mode). **Deliverable**: one screenshot.

### 2 hours — One task working end-to-end

Goal: a working assistant for one task with your team's prompt and data.

1. Finish the 30-minute path.
2. Edit `src/prompts.py` `DEFAULT_SYSTEM_PROMPT` for your task. One paragraph, plain English. Name the role, the allowed scope, and the refusal sentence.
3. Open `static/index.html` and update the placeholder text + page title to match your project.
4. Get your tutor's Azure values, fill `.env`, restart `uvicorn`.
5. Submit two test queries — one in-scope (should succeed) and one out-of-scope (should refuse politely). Save the transcripts.

**Expected token use**: 30K-50K tokens (≈ ₩1,500-2,500). **Deliverable**: working azure-mode response + two transcripts.

### 1 day — Grounded prototype + polished demo

Goal: a leaderboard-quality submission with grounded answers, citations, and a recorded demo.

1. Finish the 2-hour path.
2. Pick one of the six [sample tracks](https://koica-tiu.halla.ai/hackathon/samples) (Education, Career, Public service, Tourism, Business, Real estate). Read its architecture and prompt pack.
3. Upload 3-5 small public documents to your team's Foundry project (Data + indexes blade).
4. Switch `src/ai_client.py` to pass the `data_sources` parameter so answers are grounded.
5. Iterate on the system prompt until the response includes citation titles.
6. Polish the UI: page title, empty state, suggested prompts.
7. Record a 90-second screen capture of the working flow. Save to `demo/recording.mp4`.
8. Write the 5-line risk register at the bottom of your team README (prompt injection, hallucination, privacy, cost, mitigation owner).

**Expected token use**: 200K-400K tokens (≈ ₩10,000-20,000). **Deliverable**: live demo + recording + 5-slide deck + README.

---

## Team Workflow

1. Pick one project idea ([docs/PROJECT_IDEAS.md](docs/PROJECT_IDEAS.md)) and one target user.
2. Replace `DEFAULT_SYSTEM_PROMPT` in `src/prompts.py`.
3. Add 5-10 sample questions for your target user (save to `docs/SAMPLE_QUESTIONS.md` if you want them under version control).
4. Test response quality with prompts from [docs/PROMPT_PACK.md](docs/PROMPT_PACK.md).
5. Rehearse a 3-minute demo following the structure: problem → user → demo flow → Azure use → impact → next step.
6. Run your tutor through the [docs/TUTOR_REVIEW.md](docs/TUTOR_REVIEW.md) rubric before the final pitch.

---

## Verify You Are Done

Before you stop, confirm:

- [ ] `pytest tests/` passes locally
- [ ] `uvicorn src.main:app --reload` starts without warnings
- [ ] `/health` returns `{"status":"ok"}`
- [ ] `/ask` returns a sensible response (mock or azure) for one in-scope query
- [ ] `/ask` returns a polite refusal for one out-of-scope query
- [ ] `.env` is NOT in `git status` output
- [ ] README and slide reference Azure services without exposing keys
- [ ] Demo backup (screenshot or recording) exists in `demo/`

---

## Common Errors

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for symptom → cause → fix tables covering:

- `pip install` failures (Python version, pyenv conflicts)
- `uvicorn` port already in use
- `.env` values not loading
- Azure 401 / 403 responses
- Deployment-name mismatch
- Content safety filter triggered
- App Service deploy stuck
- Mock-mode never switches to azure

---

## Deploy

Two supported targets:

- **Azure App Service (B1)** — what the operations team provisions per team. Step-by-step in [docs/AZURE_DEPLOY.md](docs/AZURE_DEPLOY.md).
- **Azure Container Apps** — alternative if you prefer scale-to-zero or a containerized workflow. Walkthrough in [docs/CONTAINER_APPS.md](docs/CONTAINER_APPS.md).

A `Dockerfile` is included; `docker build -t hackathon-sample-2026 . && docker run -p 8000:8000 hackathon-sample-2026` reproduces the local dev server in a container.

A GitHub Actions deploy workflow template is in `.github/workflows/deploy.yml` (commented out by default — uncomment and add secrets when you are ready).

---

## Submission Requirements

See [docs/HACKATHON_DAY.md](docs/HACKATHON_DAY.md) for the full checklist. Short version:

1. Team repository with source code, README, `.env.example` (no `.env`), and no real secrets in commit history
2. 5-slide deck: problem · user · Azure workflow · demo result · limitation
3. Live demo URL OR backup screenshot/video saved in `demo/`
4. Short cost note in your team README explaining which Azure services were used

The full submission guide with templates is at [koica-tiu.halla.ai/hackathon/submission](https://koica-tiu.halla.ai/hackathon/submission).

---

## Cost Guardrails

The KOICA-TIU project shares one annual Azure credit across two semesters and two hackathons. Help keep it healthy:

- One Foundry project per team (do not create extras)
- Keep `max_tokens` ≤ 600 while iterating
- No background polling loops — Ctrl-C any retry script before lunch
- Stop App Service slots after the demo
- Watch the [admin credit page](https://koica-tiu-azure-admin.halla.ai/admin/credit) — if you see your team near 70%, ping your tutor

Full credit-safety rules: [koica-tiu.halla.ai/azure-lab](https://koica-tiu.halla.ai/azure-lab).

---

## License

MIT
