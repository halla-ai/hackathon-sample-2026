# Troubleshooting

Common issues during the hackathon, in symptom → cause → fix format. Read top to bottom — issues are roughly ordered by when teams hit them.

If your symptom is not here, ping your tutor in the Tutors Telegram group and share the exact error message.

---

## 1. `pip install -r requirements.txt` fails

**Symptom**: `ERROR: Could not find a version that satisfies the requirement openai` or similar.

**Cause**: Python version older than 3.10. The `openai` package needs 3.10+.

**Fix**:
```bash
python3 --version           # if < 3.10, install a newer Python
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
# Then recreate the venv with the new interpreter
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. `pip` command not found

**Symptom**: shell says `pip: command not found` even after `python3 -m venv .venv`.

**Cause**: virtual environment was created but not activated. The `pip` on the system PATH is missing or under a different name.

**Fix**:
```bash
source .venv/bin/activate            # macOS / Linux / WSL
# OR
.venv\Scripts\Activate.ps1            # Windows PowerShell

which python3                         # should show a path inside .venv
python3 -m pip install -r requirements.txt   # works even without `pip` alias
```

---

## 3. `uvicorn` says port 8000 already in use

**Symptom**:
```
ERROR: [Errno 48] Address already in use
```

**Cause**: another process (often a previous uvicorn that did not exit cleanly) is bound to 8000.

**Fix** — pick one:
```bash
# Option A: use a different port
uvicorn src.main:app --reload --port 8001

# Option B: kill the old process (macOS / Linux)
lsof -ti:8000 | xargs kill -9
```

---

## 4. App always returns `[mock mode]` even after editing `.env`

**Symptom**: you pasted Azure values into `.env`, restarted uvicorn, but `/ask` still returns the mock response.

**Cause** — most common in order:
1. You did not restart the server after editing `.env`.
2. One of the three required values (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`) is empty or has surrounding whitespace.
3. `.env` is in the wrong directory — must be at the repo root, next to `requirements.txt`.

**Fix**:
```bash
# Confirm .env exists and has all four lines
cat .env
# Confirm values are not blank
grep -E "^AZURE_OPENAI_(ENDPOINT|API_KEY|DEPLOYMENT)=." .env
# Restart cleanly
# Ctrl-C the running uvicorn, then:
uvicorn src.main:app --reload
```

---

## 5. Azure returns HTTP 401 Unauthorized

**Symptom**: response panel shows an exception message containing `401` or `Unauthorized`.

**Cause**: wrong `AZURE_OPENAI_API_KEY` (typo, copied from wrong project, or rotated by ops).

**Fix**:
1. Open Azure AI Foundry → your team project → Keys + endpoint.
2. Copy the key again (use "Copy" button, not manual selection — easy to miss characters).
3. Paste into `.env`, restart `uvicorn`.
4. If the key still fails, your tutor needs to confirm the project assignment from `/admin/setup`.

---

## 6. Azure returns HTTP 404 — deployment not found

**Symptom**: response contains `404` or `DeploymentNotFound` or `The API deployment for this resource does not exist`.

**Cause**: `AZURE_OPENAI_DEPLOYMENT` does not match the actual deployment name in Foundry.

**Fix**:
1. Open Foundry → your project → Models + endpoints.
2. Copy the exact deployment name (case-sensitive). For the current hackathon setup, expect `gpt-4o-mini` unless tutors announce another shared deployment.
3. Paste into `.env` exactly, restart server.

---

## 7. Content safety filter blocks a response

**Symptom**: response is empty or contains a refusal mentioning `content_filter`.

**Cause**: Foundry's content safety filter classified the response as Hate / Sexual / Violence / Self-harm above the threshold. Often a false positive in Russian / Uzbek translations or in medical / legal Q&A.

**Fix**:
1. Rephrase the test query to be neutral and direct.
2. If the issue is systemic for your project, ask your tutor to lower the filter to Medium in the project safety policy (operations approval needed for High → Medium changes).
3. Document the trade-off in your README risk register.

---

## 8. App Service deploy stuck at "Running"

**Symptom**: Azure portal shows the deploy as Running for more than 10 minutes.

**Cause** — common causes:
- Startup command not set (App Service tries to detect, fails, hangs).
- App Service runtime stack does not match what we are deploying (must be Python 3.11+ on Linux).
- Container is being pulled from a private registry without credentials.

**Fix**:
1. App Service → Configuration → General settings — confirm:
   - Stack: **Python**
   - Major version: **3.11** (or higher)
   - Startup command: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
2. App Service → Log stream — read the actual error message.
3. If the deploy was triggered from a Container Registry, confirm the App Service identity has `AcrPull` role on the registry.
4. Worst case: stop the deploy, fix configuration, redeploy.

---

## 9. `/health` works locally but App Service shows "Application Error"

**Symptom**: `https://<your-app>.azurewebsites.net/health` returns the default App Service error page.

**Cause** — pick one:
- Environment variables not configured in App Service. App Service does not read your local `.env`.
- The app is binding to `127.0.0.1` instead of `0.0.0.0`. App Service requires `0.0.0.0`.
- The app crashed on startup because a dependency is missing — `requirements.txt` did not install correctly.

**Fix**:
1. App Service → Configuration → Application settings — add the four `AZURE_OPENAI_*` variables.
2. Confirm the startup command uses `--host 0.0.0.0 --port 8000`.
3. Open Log stream and re-deploy. Watch the startup logs for the actual exception.

---

## 10. GitHub Actions CI fails on `pytest`

**Symptom**: `.github/workflows/ci.yml` run shows a red X with pytest errors.

**Cause**: tests rely on a real `.env` or live Azure connection. The CI environment has neither.

**Fix**: tests should never touch Azure. Use the `AzureOpenAISettings.from_env()` returning `None` path — the client falls back to `mock_answer`. If you wrote a new test that requires Azure, mark it with `@pytest.mark.skipif(...)` based on env var presence.

---

## Still stuck?

1. Read the exact error message — most Azure errors include a request ID you can search for.
2. Open `docs/HACKATHON_DAY.md` — table near the end maps common D-day symptoms to tutor actions.
3. Ping your tutor with: (a) the command you ran, (b) the exact error text, (c) what you have already tried. Tutors respond faster to specific reports than to "it doesn't work".
