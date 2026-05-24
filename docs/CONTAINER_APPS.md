# Azure Container Apps (alternative deployment)

Use **Azure Container Apps** if your team prefers a containerized workflow with scale-to-zero. Recommended only if your tutor approves — App Service B1 is the default and the operations team monitors it.

If you do not know whether you need this, you do not — read [AZURE_DEPLOY.md](AZURE_DEPLOY.md) instead.

---

## When to choose Container Apps over App Service

| Need | App Service (B1) | Container Apps |
|---|---|---|
| Always-on (demo never cold-starts) | ✅ default | requires min-replicas ≥ 1 |
| Scale to zero when idle | ❌ | ✅ default |
| Custom OS-level dependencies | limited | ✅ full Dockerfile control |
| Pre-provisioned by ops team | ✅ | ❌ team self-serves |
| Cost when idle | ≈ ₩52K / month | ≈ ₩0 (scaled to zero) |
| Cold start latency | none | 5-15 seconds |

For the 6/20 hackathon demo specifically, **App Service is safer** — cold starts during a live demo are a documented disaster. Container Apps make more sense for the second-semester carry-over project.

---

## Prerequisites

- Azure CLI (`az --version` ≥ 2.50)
- Docker Desktop (for local image build)
- Permission to create a Container Apps Environment in your team resource group (`Contributor` on the RG)
- The same `AZURE_OPENAI_*` environment variables as App Service

Install Container Apps CLI extension if you have not:

```bash
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

---

## 1. Build the Docker image

The repo ships a `Dockerfile`. Build locally first to confirm:

```bash
docker build -t hackathon-sample:local .
docker run --rm -p 8000:8000 hackathon-sample:local
```

Visit <http://localhost:8000>. You should see the same UI as the dev server.

---

## 2. Push to Azure Container Registry (ACR)

If your team already has an ACR, use it. Otherwise the ops team can create one shared registry.

```bash
# Login to ACR
az acr login --name <registry-name>

# Tag and push
docker tag hackathon-sample:local \
  <registry-name>.azurecr.io/hackathon-sample-teamXX:v1
docker push <registry-name>.azurecr.io/hackathon-sample-teamXX:v1
```

---

## 3. Create the Container Apps Environment

```bash
LOCATION=koreacentral
RG=rg-hackathon-teamXX
ENV_NAME=cae-hackathon-teamXX

az containerapp env create \
  --resource-group $RG \
  --name $ENV_NAME \
  --location $LOCATION
```

This takes 2-3 minutes the first time.

---

## 4. Deploy the container

```bash
az containerapp create \
  --name ca-hackathon-teamXX \
  --resource-group $RG \
  --environment $ENV_NAME \
  --image <registry-name>.azurecr.io/hackathon-sample-teamXX:v1 \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 1 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/" \
    AZURE_OPENAI_API_KEY="secretref:azure-openai-key" \
    AZURE_OPENAI_DEPLOYMENT="<deployment>" \
    AZURE_OPENAI_API_VERSION="2024-12-01-preview" \
  --secrets azure-openai-key="<key>"
```

The output prints the public FQDN — visit `https://<fqdn>` and confirm the UI works.

---

## 5. Verify

```bash
FQDN=$(az containerapp show \
  --name ca-hackathon-teamXX \
  --resource-group $RG \
  --query properties.configuration.ingress.fqdn -o tsv)

curl -sS "https://$FQDN/health"
# Expected: {"status":"ok"}

# Note: first call after idle takes 5-15s because of scale-to-zero
curl -sS -X POST "https://$FQDN/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"hello"}'
```

---

## 6. Updates and clean up

```bash
# Push a new image version
docker tag hackathon-sample:local <registry>.azurecr.io/hackathon-sample-teamXX:v2
docker push <registry>.azurecr.io/hackathon-sample-teamXX:v2

# Update the container app
az containerapp update \
  --name ca-hackathon-teamXX \
  --resource-group $RG \
  --image <registry>.azurecr.io/hackathon-sample-teamXX:v2

# Delete when finished
az containerapp delete \
  --name ca-hackathon-teamXX \
  --resource-group $RG \
  --yes
```

---

## Cost notes

- With `--min-replicas 0`, the app costs nothing when idle.
- Each cold-start request takes 5-15 seconds — **do not demo from an idle Container App**. Send one warm-up request 1 minute before your pitch.
- `cpu 0.5 / memory 1Gi` is enough for the sample. Do not over-provision.

For the hackathon-day demo, App Service is the recommended target. Use Container Apps for the post-hackathon project that runs in the second semester.
