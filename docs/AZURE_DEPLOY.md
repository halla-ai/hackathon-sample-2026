# Azure Deployment — App Service (B1)

Step-by-step deploy to Azure App Service. This is the **primary** deployment target for the KOICA-TIU hackathon — the operations team provisions one B1 slot per team in advance.

If you want scale-to-zero or a containerized workflow, read [CONTAINER_APPS.md](CONTAINER_APPS.md) instead.

> **Tutor pre-check**: confirm your team has been assigned a resource group, a Foundry project, and a B1 App Service slot before starting. The admin team monitors these at <https://koica-tiu-azure-admin.halla.ai/admin/teams>.

---

## 1. Prerequisites

Before you deploy, verify with your tutor:

- [ ] Your team has an Azure subscription (`Reader` is enough to check).
- [ ] Your team has a resource group (`rg-hackathon-teamXX`).
- [ ] An App Service plan `plan-hackathon-teamXX` exists with a B1 SKU.
- [ ] An App Service `app-koicatiu-teamXX` exists in that plan, runtime Python 3.11 on Linux.
- [ ] A Foundry project `fdry-koicatiu-teamXX` exists with at least one chat model deployment.
- [ ] You have `Contributor` role on the App Service (not on the whole resource group — only the slot you control).

Install Azure CLI if you want command-line deploy:

```bash
# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Sign in
az login
az account set --subscription <subscription-id>
```

---

## 2. Configure environment variables in App Service

App Service does NOT read your local `.env`. You must add the values in the portal or via CLI.

### Portal route

1. Open the Azure portal: <https://portal.azure.com>
2. Navigate to **App Services** → `app-koicatiu-teamXX`.
3. In the left menu choose **Configuration** → **Application settings**.
4. Click **+ New application setting** for each:
   - `AZURE_OPENAI_ENDPOINT` = `https://<your-foundry-resource>.openai.azure.com/`
   - `AZURE_OPENAI_API_KEY` = `<key from Foundry>`
   - `AZURE_OPENAI_DEPLOYMENT` = `<your deployment name>`
   - `AZURE_OPENAI_API_VERSION` = `2024-12-01-preview`
5. Click **Save** (top of page). Confirm the **Restart** prompt.

### CLI route

```bash
az webapp config appsettings set \
  --resource-group rg-hackathon-teamXX \
  --name app-koicatiu-teamXX \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/" \
    AZURE_OPENAI_API_KEY="<key>" \
    AZURE_OPENAI_DEPLOYMENT="<deployment>" \
    AZURE_OPENAI_API_VERSION="2024-12-01-preview"
```

Never paste the key into a shell where it might land in your shell history. Use the portal if your laptop is shared.

---

## 3. Set the startup command

App Service does not auto-detect FastAPI. Tell it how to start.

### Portal

1. **Configuration** → **General settings**.
2. **Stack settings**:
   - Stack: **Python**
   - Major version: **Python 3.11** (or 3.12 if available)
   - Minor version: latest
3. **Startup Command**: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
4. Click **Save**.

### CLI

```bash
az webapp config set \
  --resource-group rg-hackathon-teamXX \
  --name app-koicatiu-teamXX \
  --startup-file "uvicorn src.main:app --host 0.0.0.0 --port 8000" \
  --linux-fx-version "PYTHON|3.11"
```

---

## 4. Deploy the code

Three options — pick one.

### Option A — `az webapp up` (simplest)

From your repo root:

```bash
az webapp up \
  --name app-koicatiu-teamXX \
  --resource-group rg-hackathon-teamXX \
  --runtime "PYTHON:3.11" \
  --sku B1
```

This creates a `.azure/config` file in your repo with the deploy target. Subsequent deploys are just `az webapp up`.

### Option B — Zip deploy

```bash
# Create a deployment zip excluding venv / cache
zip -r deploy.zip . -x ".venv/*" ".git/*" "__pycache__/*" "*.pyc" "tests/*"

az webapp deploy \
  --resource-group rg-hackathon-teamXX \
  --name app-koicatiu-teamXX \
  --src-path deploy.zip \
  --type zip
```

### Option C — GitHub Actions (continuous deploy)

Use the template at `.github/workflows/deploy.yml`. Steps:

1. In your team repo: **Settings** → **Secrets and variables** → **Actions** → add:
   - `AZURE_APP_NAME` = `app-koicatiu-teamXX`
   - `AZURE_PUBLISH_PROFILE` = paste the App Service publish profile XML (download from portal → "Get publish profile")
2. Uncomment the `deploy:` job in `.github/workflows/deploy.yml`.
3. Push to `main`. GitHub Actions builds and deploys automatically.

---

## 5. Verify

Wait 30-90 seconds after deploy for the first cold start.

```bash
APP_URL="https://app-koicatiu-teamXX.azurewebsites.net"

# 1. Health endpoint
curl -sS "$APP_URL/health"
# Expected: {"status":"ok"}

# 2. Static UI
open "$APP_URL"               # macOS; or paste into a browser

# 3. Ask endpoint (mock or azure depending on env vars)
curl -sS -X POST "$APP_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What can you help with?"}'
```

If any step fails, open **App Service** → **Log stream** (left menu) to see the runtime logs. Common errors are in [TROUBLESHOOTING.md](TROUBLESHOOTING.md) #8 and #9.

---

## 6. Stop, restart, clean up

```bash
# Stop (saves cost — App Service is billed per hour while running)
az webapp stop --resource-group rg-hackathon-teamXX --name app-koicatiu-teamXX

# Restart (after config changes)
az webapp restart --resource-group rg-hackathon-teamXX --name app-koicatiu-teamXX

# Start again (after stop)
az webapp start --resource-group rg-hackathon-teamXX --name app-koicatiu-teamXX
```

After the hackathon, **stop your App Service** before you leave. The operations team will clean up the next morning.

---

## 7. Cost expectations

| Component | Cost | Notes |
|---|---|---|
| App Service B1 | ≈ ₩52,500 / month if always on | Stop the slot when you are not demoing — costs drop to near zero |
| Azure OpenAI (GPT-4.1) | $0.005 / 1K input, $0.015 / 1K output | Hackathon day target: under 50K tokens per team |
| Storage (logs) | < ₩1,000 / month | Negligible for hackathon usage |

Per-team budget on D-day: **₩375,000** (cap). The credit-safety details are at <https://koica-tiu.halla.ai/azure-lab>.

Live team-level usage: <https://koica-tiu-azure-admin.halla.ai/admin/credit> (admin auth required).

---

## Demo readiness checklist

- [ ] `/health` returns `{"status":"ok"}` on the public URL
- [ ] `/` loads the static UI without console errors
- [ ] `/ask` returns an Azure response (not mock) for one prepared question
- [ ] App Service Application settings show all four `AZURE_OPENAI_*` keys
- [ ] No secrets visible in the deployed source (`.env` not in zip / not in git)
- [ ] You can explain in one sentence which Azure services this app uses
- [ ] You have at least three pre-tested questions ready for the demo
