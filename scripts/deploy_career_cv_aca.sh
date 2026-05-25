#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
source "$SCRIPT_DIR/_career_cv_demo_common.sh"

ensure_az_login

log "Registering required resource providers"
run az provider register --namespace Microsoft.App --wait
run az provider register --namespace Microsoft.ContainerRegistry --wait
run az provider register --namespace Microsoft.CognitiveServices --wait

log "Ensuring resource group"
run az group create \
  --name "$RG" \
  --location "$LOCATION" \
  --tags purpose=career-cv-demo owner=koica-tiu cost-control=scale-to-zero delete-after=2026-06-21 suffix="$SUFFIX"

log "Ensuring Azure OpenAI resource"
if resource_exists az cognitiveservices account show --name "$OPENAI_NAME" --resource-group "$RG"; then
  echo "Azure OpenAI resource exists: $OPENAI_NAME"
else
  run az cognitiveservices account create \
    --name "$OPENAI_NAME" \
    --resource-group "$RG" \
    --kind OpenAI \
    --sku S0 \
    --location "$LOCATION" \
    --custom-domain "$OPENAI_NAME" \
    --yes \
    --tags purpose=career-cv-demo owner=koica-tiu cost-control=one-demo-call delete-after=2026-06-21 suffix="$SUFFIX"
fi

log "Ensuring model deployment"
MODEL_SKU_NAME="$(detect_model_sku)"
if resource_exists az cognitiveservices account deployment show --resource-group "$RG" --name "$OPENAI_NAME" --deployment-name "$DEPLOYMENT_NAME"; then
  echo "Model deployment exists: $DEPLOYMENT_NAME"
else
  echo "Using model SKU: $MODEL_SKU_NAME"
  run az cognitiveservices account deployment create \
    --resource-group "$RG" \
    --name "$OPENAI_NAME" \
    --deployment-name "$DEPLOYMENT_NAME" \
    --model-name "$MODEL_NAME" \
    --model-version "$MODEL_VERSION" \
    --model-format OpenAI \
    --sku-capacity 10 \
    --sku-name "$MODEL_SKU_NAME"
fi

log "Ensuring Azure Container Registry"
if resource_exists az acr show --name "$ACR_NAME" --resource-group "$RG"; then
  echo "ACR exists: $ACR_NAME"
else
  run az acr create \
    --resource-group "$RG" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled true \
    --tags purpose=career-cv-demo owner=koica-tiu delete-after=2026-06-21 suffix="$SUFFIX"
fi

log "Building container image in ACR"
run az acr build \
  --registry "$ACR_NAME" \
  --image "$IMAGE_NAME" \
  .

log "Ensuring Container Apps environment"
if resource_exists az containerapp env show --name "$ENV_NAME" --resource-group "$RG"; then
  echo "Container Apps environment exists: $ENV_NAME"
else
  run az containerapp env create \
    --resource-group "$RG" \
    --name "$ENV_NAME" \
    --location "$LOCATION" \
    --tags purpose=career-cv-demo owner=koica-tiu delete-after=2026-06-21 suffix="$SUFFIX"
fi

log "Reading deployment values"
ENDPOINT="$(az cognitiveservices account show --name "$OPENAI_NAME" --resource-group "$RG" --query properties.endpoint -o tsv)"
API_KEY="$(az cognitiveservices account keys list --name "$OPENAI_NAME" --resource-group "$RG" --query key1 -o tsv)"
ACR_LOGIN="$(az acr show --name "$ACR_NAME" --resource-group "$RG" --query loginServer -o tsv)"
ACR_PASSWORD="$(az acr credential show --name "$ACR_NAME" --query 'passwords[0].value' -o tsv)"
IMAGE="$ACR_LOGIN/$IMAGE_NAME"

log "Creating or updating Container App"
if resource_exists az containerapp show --name "$APP_NAME" --resource-group "$RG"; then
  run az containerapp secret set \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --secrets azure-openai-key="$API_KEY"
  run az containerapp registry set \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --server "$ACR_LOGIN" \
    --username "$ACR_NAME" \
    --password "$ACR_PASSWORD"
  run az containerapp update \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --image "$IMAGE" \
    --min-replicas 0 \
    --max-replicas 1 \
    --cpu 0.5 \
    --memory 1.0Gi \
    --set-env-vars \
      AZURE_OPENAI_ENDPOINT="$ENDPOINT" \
      AZURE_OPENAI_API_KEY=secretref:azure-openai-key \
      AZURE_OPENAI_DEPLOYMENT="$DEPLOYMENT_NAME" \
      AZURE_OPENAI_API_VERSION="$API_VERSION"
else
  run az containerapp create \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --environment "$ENV_NAME" \
    --image "$IMAGE" \
    --target-port 8000 \
    --ingress external \
    --min-replicas 0 \
    --max-replicas 1 \
    --cpu 0.5 \
    --memory 1.0Gi \
    --registry-server "$ACR_LOGIN" \
    --registry-username "$ACR_NAME" \
    --registry-password "$ACR_PASSWORD" \
    --env-vars \
      AZURE_OPENAI_ENDPOINT="$ENDPOINT" \
      AZURE_OPENAI_API_KEY=secretref:azure-openai-key \
      AZURE_OPENAI_DEPLOYMENT="$DEPLOYMENT_NAME" \
      AZURE_OPENAI_API_VERSION="$API_VERSION" \
    --secrets azure-openai-key="$API_KEY" \
    --tags purpose=career-cv-demo owner=koica-tiu cost-control=scale-to-zero delete-after=2026-06-21 suffix="$SUFFIX"
fi

FQDN="$(get_fqdn)"
write_state

log "Verifying deployed app"
curl -fsS "https://$FQDN/health"
printf '\n'
curl -fsS -X POST "https://$FQDN/review" \
  -H "Content-Type: application/json" \
  -d "$(sample_cv_json)"
printf '\n'

log "Deployment complete"
echo "APP_URL=https://$FQDN"
echo "RESOURCE_GROUP=$RG"
echo "Estimated model calls in this script: 1"
