# Quickstart

First-time setup with annotated output. Read this when the [README Quick Start](../README.md#quick-start) feels too compressed.

Target audience: a student who has installed Python and git, but never run a FastAPI app or an Azure SDK call.

Total time: 15-20 minutes the first run, under 2 minutes after.

---

## Step 1 — Use the template to create your team repo

On GitHub, open this repository and click the green **Use this template** button → **Create a new repository**. Name it `<team-name>-hackathon` or similar. Keep visibility public unless your tutor says otherwise.

Then clone YOUR new repo locally:

```bash
git clone <your-team-repo-url>
cd <your-team-repo-name>
```

You should see:

```
README.md  docs  requirements.txt  src  static  tests  Dockerfile  .env.example  .gitignore
```

> **Why not clone halla-ai/hackathon-sample-2026 directly?** Because you need your own repo to push commits, run CI, and deploy. Templates exist for exactly this case.

---

## Step 2 — Create a Python virtual environment

```bash
python3 -m venv .venv
```

This creates a `.venv/` directory. Activate it:

```bash
# macOS / Linux / WSL
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

After activation your prompt should start with `(.venv)`. If it doesn't, the activation script failed — check `which python3` returns a path inside `.venv/bin/`.

---

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

Expected last line:

```
Successfully installed annotated-types-... anyio-... certifi-... ... uvicorn-...
```

If you see a `pip: command not found`, your venv did not activate — repeat Step 2. If `pip install` fails on `openai`, your Python version is too old (need 3.10+).

---

## Step 4 — Create your local .env

```bash
cp .env.example .env
```

Leave the values empty for the first run — the app will fall back to mock mode. The file looks like:

```dotenv
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

> **When your tutor gives you Azure values** (usually on D-day morning), paste them here. Until then, leave empty.

`.gitignore` already excludes `.env`. Verify with `git status` — you should NOT see `.env` in the output.

---

## Step 5 — Run the dev server

```bash
uvicorn src.main:app --reload
```

Expected output:

```
INFO:     Will watch for changes in these directories: ['/Users/.../hackathon-sample-2026']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12348]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

If port 8000 is busy: `uvicorn src.main:app --reload --port 8001`.

---

## Step 6 — Verify the app works

Open <http://127.0.0.1:8000> in a browser. You should see a two-panel UI with a "Question" textarea and a "Response" panel showing `Ask a question to test the sample app.`

Type a question — anything — and click **Ask**. The response panel should fill with something like:

```
[mock mode] Azure credentials are not configured yet.

Question: your question

Suggested next step: define the target user, expected output, and one
evaluation example. Then connect an Azure OpenAI deployment through .env.
```

The mode indicator (top right of the response panel) should read `mock`.

This means the full request → backend → mock client → UI loop works. Your 30-minute path is complete.

---

## Step 7 — (Optional) Connect Azure OpenAI

Only do this when your tutor has confirmed your team's Foundry project and the assigned model deployment.

Edit `.env`:

```dotenv
AZURE_OPENAI_ENDPOINT=https://koicatiu-team05.openai.azure.com/
AZURE_OPENAI_API_KEY=<paste-from-tutor>
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Stop the server (`Ctrl-C`) and restart:

```bash
uvicorn src.main:app --reload
```

Submit a question again. The response should now be a real Azure OpenAI completion and the mode indicator should switch to `azure`.

If you see an HTTP 401 error in the response, your key or endpoint is wrong — go to [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Step 8 — Run the tests

```bash
pytest tests/
```

Expected:

```
======================== test session starts ========================
collected 2 items

tests/test_health.py ..                                       [100%]

======================== 2 passed in 0.5s ========================
```

If a test fails, your environment is broken — most likely Python version or missing dependency. Re-run Steps 3 and 5.

---

## What now?

Pick a build path in the [README](../README.md#build-paths):

- **30 minutes** — Quick Start complete, screenshot saved
- **2 hours** — Add your prompt + data, run two test queries
- **One day** — Polish, ground, record, submit

Or open [PROJECT_IDEAS.md](PROJECT_IDEAS.md) and pick a track.
