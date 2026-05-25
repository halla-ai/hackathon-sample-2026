# Walkthrough — Deploy a CV Feedback Bot to Azure Container Apps

End-to-end recipe. You start with a clone of this branch and finish with a publicly reachable URL serving an Azure-powered CV review API. Designed for **minimum cost**: idle ≈ ₩0, one demo hour ≈ ₩900.

If you only have 30 minutes, do steps 1-2 (local mock mode). If you have 90 minutes, do steps 1-7. Step 8 (teardown) is mandatory before you walk away from the keyboard.

There are three supported deployment paths:

- **Tutor/admin console**: use the KOICA-TIU Azure Admin page when operations staff need to run the demo and show the live progress.
- **GitHub Actions**: run the `Career CV Demo` workflow when you want a reproducible cloud-side deployment without using your laptop as the deploy machine.
- **Local Azure CLI**: run the scripts in `scripts/` or follow the manual commands below when students need to learn each Azure step.

---

## What you build

A small FastAPI app that accepts CV text and returns four lists:

- **Strengths** — three short bullets the CV does well
- **Weaknesses** — three short bullets the CV does poorly
- **Suggestions** — three concrete one-sentence improvements
- **Red flags** — any private contact info (phone, address) the CV exposes

UI is a single-page static form. Backend is Azure OpenAI (`gpt-4o-mini`) called via the official `openai` SDK. Hosting is Azure Container Apps with `--min-replicas 0` so the bill stops when nobody is using it.

Screenshot of the working UI:

```
+-----------------------+--------------------------+
| KOICA-TIU 2026        |                          |
| CV Feedback Bot       |  ✓ Strengths             |
|                       |   • Clear structure...   |
|  [Paste your CV here] |  ✗ Weaknesses            |
|  [Review CV]          |   • No internships...    |
|                       |  → Suggestions           |
|                       |   • Add metrics to...    |
+-----------------------+--------------------------+
```

---

## Cost expectation

| Component | Quantity | Unit cost | Total |
|---|---|---|---|
| Azure OpenAI `gpt-4o-mini` input | 50 calls × ~1.2K tokens | $0.00015 / 1K | ~₩12 |
| Azure OpenAI `gpt-4o-mini` output | 50 calls × ~300 tokens | $0.00060 / 1K | ~₩12 |
| Azure Container Apps compute | 0.5 vCPU × 1 GiB × 60 min | ~$0.10 / hour | ~₩135 |
| Azure Container Registry (Basic, shared) | 1 month / 8 teams | ₩6,000 / 8 | ~₩750 |
| Idle outside the demo hour | `--min-replicas 0` | ₩0 | ₩0 |
| **Per-team total** | | | **~₩900** |

If you skip ACR and build with `az containerapp up` source-to-cloud (step 5b below), the ACR line drops to zero — but cold-start times get longer.

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Python | 3.10+ | `brew install python@3.12` / `apt install python3.12` |
| Docker | any recent | <https://docs.docker.com/desktop/> (optional if you use `az containerapp up`) |
| Azure CLI | ≥ 2.50 | `brew install azure-cli` / `curl -sL https://aka.ms/InstallAzureCLIDeb \| sudo bash` |
| git | any | already on macOS, `apt install git` on Ubuntu |

Azure access:

- An **Azure subscription** — your team's KOICA-TIU slot from operations, OR a personal free Azure trial (12 months, $200 credit). The free trial covers everything in this walkthrough multiple times over.
- The **`Microsoft.App`** and **`Microsoft.ContainerRegistry`** resource providers registered in your subscription (one-time, done in step 3).

Confirm you are signed in:

```bash
az login
az account show -o table
```

Expected output (one row):

```
Name                CloudName    SubscriptionId                          State    IsDefault
------------------  -----------  --------------------------------------  -------  -----------
Azure subscription  AzureCloud   76505dd8-7eae-4c34-8683-ae617aa01e9d    Enabled  True
```

If `IsDefault` is False, run `az account set --subscription <id>`.

---

## Step 1 — Clone and switch to the example branch

```bash
git clone https://github.com/halla-ai/hackathon-sample-2026.git cv-bot
cd cv-bot
git checkout example/career-cv
```

You should see `docs/WALKTHROUGH.md` (this file) and a modified `src/main.py` containing the `/review` endpoint.

> **Why a branch?** The `main` branch keeps the template generic. The `example/career-cv` branch has the working code so you can either copy it straight, or treat it as a reference while applying the changes to your own template.

---

## Step 2 — Run locally in mock mode

Before spending any Azure credit, verify the app runs locally.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # leave values empty
uvicorn src.main:app --reload
```

Expected last few lines:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open <http://127.0.0.1:8000> in a browser. Paste any 20+ character CV-shaped text, click **Review CV**. You should see four blocks of `[mock]` results and the mode indicator shows `mock`.

Run the tests:

```bash
pytest tests/
```

Expected:

```
======================== 7 passed in 0.6s ========================
```

If any of this fails, stop and read `docs/TROUBLESHOOTING.md`. Do not move on until the local mock mode works.

**Wait time so far**: ~5 minutes. **Cost so far**: ₩0.

---

## Fast path — Deploy with the provided scripts

Use this path for the official demo or for tutor-led practice. It performs the same Azure steps as the manual walkthrough, but keeps names consistent and records a small state file under `.azure/`.

Set a suffix first. Keep it lowercase, 3-19 characters, and unique per team or demo run:

```bash
export SUFFIX=cvbot01
export LOCATION=koreacentral
```

Resource names created by the scripts:

| Resource | Name pattern |
|---|---|
| Resource group | `rg-cvbot-$SUFFIX` |
| Azure OpenAI | `oai-cvbot-$SUFFIX` |
| Azure Container Registry | `acrcvbot$SUFFIX` without hyphens |
| Container Apps Environment | `cae-cvbot-$SUFFIX` |
| Container App | `ca-cvbot-$SUFFIX` |

Deploy:

```bash
bash scripts/deploy_career_cv_aca.sh
```

The script signs in with `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID` if they are present. Otherwise it uses your existing `az login` session. It registers providers, creates or reuses Azure resources, builds the container in ACR, deploys the app with `--min-replicas 0`, calls `/health`, then sends exactly one sample `/review` request.

Verify again later:

```bash
bash scripts/verify_career_cv_aca.sh
```

Stop the public app URL after a demo while keeping the resource group:

```bash
bash scripts/stop_career_cv_aca.sh
```

Delete everything for the suffix:

```bash
bash scripts/delete_career_cv_aca.sh
```

The deploy script writes `.azure/career-cv-demo-$SUFFIX.env` with non-secret values such as `APP_URL` and `RESOURCE_GROUP`. It does not write the Azure OpenAI key.

### GitHub Actions path

The same script set can run in GitHub Actions. Repository maintainers must set these four repository secrets first:

```text
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
```

Then run:

```bash
gh workflow run career-cv-demo.yml \
  --ref example/career-cv \
  -f operation=deploy \
  -f suffix=cvbot01 \
  -f location=koreacentral
```

Other supported operations are `verify`, `stop`, and `delete`:

```bash
gh workflow run career-cv-demo.yml --ref example/career-cv -f operation=verify -f suffix=cvbot01 -f location=koreacentral
gh workflow run career-cv-demo.yml --ref example/career-cv -f operation=stop   -f suffix=cvbot01 -f location=koreacentral
gh workflow run career-cv-demo.yml --ref example/career-cv -f operation=delete -f suffix=cvbot01 -f location=koreacentral
```

Watch the run in the GitHub Actions tab. The KOICA-TIU Azure Admin console uses this same workflow and shows the run status, step progress, resource group state, Container App state, and public URL in one page.

---

## Step 3 — Create Azure resources

Pick a unique suffix — your team number or a 6-character random string. The walkthrough uses `cvbot01` as the example; change it everywhere below.

```bash
SUFFIX=cvbot01
LOCATION=koreacentral
RG=rg-$SUFFIX
OPENAI_NAME=oai-$SUFFIX
ACR_NAME=acr$SUFFIX                # lowercase, no hyphens (ACR naming rule)
APP_NAME=ca-$SUFFIX
ENV_NAME=cae-$SUFFIX
DEPLOYMENT_NAME=gpt-4o-mini
MODEL_NAME=gpt-4o-mini
MODEL_VERSION=2024-07-18

# 3a. Register the providers (idempotent — safe to re-run)
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.ContainerRegistry --wait
az provider register --namespace Microsoft.CognitiveServices --wait

# 3b. Resource group
az group create --name $RG --location $LOCATION

# 3c. Azure OpenAI resource + gpt-4o-mini deployment
az cognitiveservices account create \
  --name $OPENAI_NAME \
  --resource-group $RG \
  --kind OpenAI \
  --sku S0 \
  --location $LOCATION \
  --custom-domain $OPENAI_NAME \
  --yes

az cognitiveservices account deployment create \
  --resource-group $RG \
  --name $OPENAI_NAME \
  --deployment-name $DEPLOYMENT_NAME \
  --model-name $MODEL_NAME \
  --model-version $MODEL_VERSION \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"

# 3d. Container Registry (Basic SKU — cheapest)
az acr create \
  --resource-group $RG \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# 3e. Container Apps Environment
az containerapp env create \
  --resource-group $RG \
  --name $ENV_NAME \
  --location $LOCATION
```

`az containerapp env create` is the slowest step (~3 minutes). Wait for it to print `provisioningState: Succeeded`.

Collect the values you need for `.env`:

```bash
ENDPOINT=$(az cognitiveservices account show \
  --name $OPENAI_NAME --resource-group $RG \
  --query properties.endpoint -o tsv)

API_KEY=$(az cognitiveservices account keys list \
  --name $OPENAI_NAME --resource-group $RG \
  --query key1 -o tsv)

echo "Endpoint: $ENDPOINT"
echo "Key:      ${API_KEY:0:8}…"   # only show prefix
```

> **gpt-4o-mini region**: `koreacentral` has this model as of 2026. If `az cognitiveservices account deployment create` fails with "Model not available in this region", switch `LOCATION` to `eastus` or `swedencentral` and re-run from 3b. See [Troubleshooting #1](#troubleshooting).

**Wait time**: ~6 minutes. **Cost so far**: ₩0 (resources are created but idle).

---

## Step 4 — Configure `.env` and verify against real Azure locally

Edit `.env`:

```bash
AZURE_OPENAI_ENDPOINT=<paste $ENDPOINT here>
AZURE_OPENAI_API_KEY=<paste $API_KEY here>
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Stop the running `uvicorn` (Ctrl-C) and restart:

```bash
uvicorn src.main:app --reload
```

Submit the same CV in the UI. Now the mode indicator should switch to `azure` and the feedback should come from the live model (no `[mock]` prefix).

> **Cost check**: that one review used roughly 1,500 tokens — about ₩2. Run two or three more to confirm before moving on.

If the response shows `401 Unauthorized`, the key or endpoint is wrong. If it shows `404`, the deployment name does not match. See [Troubleshooting](#troubleshooting).

**Wait time**: ~3 minutes. **Cost so far**: ~₩10.

---

## Step 5 — Build and push the Docker image

Two options. **5a** is the recommended path; **5b** is the "no-Docker-installed" fallback.

### Option 5a — Local Docker → ACR

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Build and tag
docker build -t $ACR_NAME.azurecr.io/cv-bot:v1 .

# Push
docker push $ACR_NAME.azurecr.io/cv-bot:v1
```

Push takes ~30 seconds (image is ~150 MB).

### Option 5b — Source-to-cloud (no local Docker)

If Docker is not installed, ACR can build remotely:

```bash
az acr build \
  --registry $ACR_NAME \
  --image cv-bot:v1 \
  .
```

This streams the source up to ACR and runs the build there. Takes ~2 minutes.

---

## Step 6 — Deploy to Container Apps with scale-to-zero

```bash
ACR_LOGIN=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

az containerapp create \
  --name $APP_NAME \
  --resource-group $RG \
  --environment $ENV_NAME \
  --image $ACR_LOGIN/cv-bot:v1 \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 1 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --registry-server $ACR_LOGIN \
  --registry-username $ACR_NAME \
  --registry-password "$ACR_PASSWORD" \
  --env-vars \
    AZURE_OPENAI_ENDPOINT="$ENDPOINT" \
    AZURE_OPENAI_API_KEY="secretref:azure-openai-key" \
    AZURE_OPENAI_DEPLOYMENT="$DEPLOYMENT_NAME" \
    AZURE_OPENAI_API_VERSION="2024-12-01-preview" \
  --secrets azure-openai-key="$API_KEY"
```

The output prints a FQDN like `ca-cvbot01.koreablue-xxxxxxxx.koreacentral.azurecontainerapps.io`.

Save it:

```bash
FQDN=$(az containerapp show \
  --name $APP_NAME \
  --resource-group $RG \
  --query properties.configuration.ingress.fqdn -o tsv)
echo "App URL: https://$FQDN"
```

**Wait time**: ~90 seconds. **Cost so far**: ~₩20.

---

## Step 7 — Verify

```bash
# 7a. Health (instant after cold start)
curl -sS "https://$FQDN/health"
# Expected: {"status":"ok"}

# 7b. Open the UI in a browser
open "https://$FQDN"      # macOS — Linux/Windows: paste into a browser

# 7c. Review request (cold start adds 5-15 seconds to the first call)
curl -sS -X POST "https://$FQDN/review" \
  -H "Content-Type: application/json" \
  -d '{"cv":"Aisha Karimova\nBSc TIU 2024-. Project: Campus FAQ Bot (Python, FastAPI, Azure OpenAI), 80% answer accuracy. Skills: Python, Git."}'
```

Expected `/review` response shape (the actual content will vary per model run):

```json
{
  "strengths": ["Quantified the project outcome (80% accuracy)", "Lists relevant tech stack", "Identifies degree program and date"],
  "weaknesses": ["No internship or work experience", "Skills section is short", "Missing contact / email"],
  "suggestions": ["Add a short summary of the role you are targeting.", "Expand the project to include team size and dataset size.", "Add 1-2 lines about coursework relevant to the role."],
  "red_flags": [],
  "mode": "azure"
}
```

Take a screenshot of the UI showing the live response. This is your demo backup.

**Wait time**: ~30 seconds. **Cost so far**: ~₩50.

---

## Step 8 — Tear down

**Do this before you close the laptop.** The Container Apps slot is scale-to-zero, but ACR and Cognitive Services have small standing costs that add up over weeks.

```bash
# Delete the container app
az containerapp delete \
  --name $APP_NAME \
  --resource-group $RG \
  --yes

# Or delete the entire resource group (everything in one shot)
az group delete --name $RG --yes --no-wait
```

`az group delete --no-wait` returns immediately; the actual cleanup runs in the background for ~5 minutes.

Verify after a few minutes:

```bash
az group exists --name $RG
# Expected: false
```

**Total wait time**: ~15 minutes elapsed. **Total cost**: ~₩50-100 (well below the ₩900 budget because we deleted before peak hour).

If you want to keep the app for the demo day and tear down tomorrow, **stop the container app** instead:

```bash
# Stop only (preserves resource so resume is fast)
az containerapp revision deactivate \
  --revision $(az containerapp revision list --name $APP_NAME --resource-group $RG --query "[0].name" -o tsv) \
  --name $APP_NAME --resource-group $RG
```

Note: scale-to-zero already prevents most idle cost. The deactivate command is only useful if you want to disable the URL entirely.

---

## Troubleshooting

### 1. `gpt-4o-mini` not available in `koreacentral`

Azure OpenAI model availability rotates per region. As of 2026 most regions support `gpt-4o-mini`, but if your deployment create fails, switch to one of:

- `eastus`
- `swedencentral`
- `westus`
- `japaneast`

Set `LOCATION` to the new value and re-run steps 3b-3e. Container Apps Environment must be in the same region as Azure OpenAI for best latency, but they can be in different regions if needed.

### 2. ACR push fails with `unauthorized: authentication required`

`az acr login` tokens last ~3 hours. Re-run it:

```bash
az acr login --name $ACR_NAME
```

If it still fails, regenerate the admin password:

```bash
az acr credential renew --name $ACR_NAME --password-name password
```

### 3. Container Apps deploy succeeds but `/review` returns 500

Most common: env var typos. Open the live logs:

```bash
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RG \
  --follow
```

Submit a `/review` request and watch for the Python traceback. Likely culprits: wrong `AZURE_OPENAI_DEPLOYMENT` (must match what you created in 3c), wrong `AZURE_OPENAI_API_VERSION` for the model.

### 4. Cold start is 30+ seconds

`gpt-4o-mini` deployments occasionally have a multi-second warmup. Send a warm-up request 1 minute before your demo:

```bash
curl -sS "https://$FQDN/health" > /dev/null
```

Then the next `/review` call should be ~2-3 seconds.

### 5. UI shows the page but submit does nothing

Open browser dev tools → Network tab → submit. If `/review` returns `404`, the static UI is being served but the API is not. Most common cause: you forgot `--target-port 8000` in step 6. Update with:

```bash
az containerapp ingress update \
  --name $APP_NAME --resource-group $RG \
  --target-port 8000
```

### More

See `docs/TROUBLESHOOTING.md` for the general template-level errors (pip install, uvicorn port in use, etc.).

---

## What next

- **Demo on June 20**: redeploy with a fresh build the morning of the event. Keep the URL and ACR image; deploy fresh credentials only.
- **Add to your team's main repo**: copy `src/`, `static/`, `tests/`, `Dockerfile`, this walkthrough. Push to your team's repo. The branch `example/career-cv` is a reference, not your submission.
- **Extend**: swap the rubric, switch JSON schema, add a "rewrite" button. The cost per call stays under ₩2 as long as you use `gpt-4o-mini`.
- **Share back**: if you find a real-world bug in this walkthrough, open an issue against `halla-ai/hackathon-sample-2026`.

Submission requirements: see `docs/HACKATHON_DAY.md` or <https://koica-tiu.halla.ai/hackathon/submission>.
