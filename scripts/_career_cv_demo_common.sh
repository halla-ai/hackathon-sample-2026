#!/usr/bin/env bash
set -Eeuo pipefail

DEFAULT_SUBSCRIPTION_ID="76505dd8-7eae-4c34-8683-ae617aa01e9d"
LOCATION="${LOCATION:-koreacentral}"
SUFFIX="${SUFFIX:-demo}"
DEPLOYMENT_NAME="${DEPLOYMENT_NAME:-gpt-4o-mini}"
MODEL_NAME="${MODEL_NAME:-gpt-4o-mini}"
MODEL_VERSION="${MODEL_VERSION:-2024-07-18}"
MODEL_SKU_NAME="${MODEL_SKU_NAME:-}"
API_VERSION="${AZURE_OPENAI_API_VERSION:-2024-12-01-preview}"
SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-$DEFAULT_SUBSCRIPTION_ID}"

if [[ ! "$SUFFIX" =~ ^[a-z0-9][a-z0-9-]{1,17}[a-z0-9]$ ]]; then
  echo "SUFFIX must be 3-19 lowercase letters, numbers, or hyphens, and must start/end with alphanumeric." >&2
  exit 2
fi

ACR_SUFFIX="${SUFFIX//-/}"
if [[ ${#ACR_SUFFIX} -lt 3 || ${#ACR_SUFFIX} -gt 18 ]]; then
  echo "SUFFIX without hyphens must be 3-18 characters for ACR naming." >&2
  exit 2
fi

RG="rg-cvbot-${SUFFIX}"
OPENAI_NAME="oai-cvbot-${SUFFIX}"
ACR_NAME="acrcvbot${ACR_SUFFIX}"
APP_NAME="ca-cvbot-${SUFFIX}"
ENV_NAME="cae-cvbot-${SUFFIX}"
IMAGE_NAME="cv-bot:v1"
STATE_DIR=".azure"
STATE_FILE="${STATE_DIR}/career-cv-demo-${SUFFIX}.env"

log() {
  printf '\n==> %s\n' "$*"
}

run() {
  printf '+'
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  printf '\n'
  "$@"
}

ensure_az_login() {
  if [[ -n "${AZURE_CLIENT_ID:-}" && -n "${AZURE_CLIENT_SECRET:-}" && -n "${AZURE_TENANT_ID:-}" ]]; then
    log "Signing in with service principal"
    az login \
      --service-principal \
      --username "$AZURE_CLIENT_ID" \
      --password "$AZURE_CLIENT_SECRET" \
      --tenant "$AZURE_TENANT_ID" \
      --output none
  fi
  az account set --subscription "$SUBSCRIPTION_ID"
  az account show --query '{subscription:id,user:user.name}' -o json
}

resource_exists() {
  "$@" >/dev/null 2>&1
}

detect_model_sku() {
  if [[ -n "$MODEL_SKU_NAME" ]]; then
    echo "$MODEL_SKU_NAME"
    return
  fi

  local detected
  detected="$(az cognitiveservices model list \
    --location "$LOCATION" \
    --query "[?model.name=='${MODEL_NAME}' && model.version=='${MODEL_VERSION}'].model.skus[0].name | [0]" \
    -o tsv)"

  if [[ -z "$detected" || "$detected" == "None" ]]; then
    echo "Unable to auto-detect SKU for $MODEL_NAME $MODEL_VERSION in $LOCATION." >&2
    echo "Set MODEL_SKU_NAME=Standard or MODEL_SKU_NAME=GlobalStandard and re-run." >&2
    exit 2
  fi

  echo "$detected"
}

write_state() {
  mkdir -p "$STATE_DIR"
  {
    printf 'SUFFIX=%s\n' "$SUFFIX"
    printf 'LOCATION=%s\n' "$LOCATION"
    printf 'RG=%s\n' "$RG"
    printf 'OPENAI_NAME=%s\n' "$OPENAI_NAME"
    printf 'ACR_NAME=%s\n' "$ACR_NAME"
    printf 'APP_NAME=%s\n' "$APP_NAME"
    printf 'ENV_NAME=%s\n' "$ENV_NAME"
    printf 'DEPLOYMENT_NAME=%s\n' "$DEPLOYMENT_NAME"
    printf 'MODEL_NAME=%s\n' "$MODEL_NAME"
    printf 'MODEL_VERSION=%s\n' "$MODEL_VERSION"
    printf 'MODEL_SKU_NAME=%s\n' "$MODEL_SKU_NAME"
    printf 'AZURE_OPENAI_API_VERSION=%s\n' "$API_VERSION"
    if [[ -n "${FQDN:-}" ]]; then
      printf 'FQDN=%s\n' "$FQDN"
      printf 'APP_URL=https://%s\n' "$FQDN"
    fi
  } > "$STATE_FILE"
  echo "State file: $STATE_FILE"
}

get_fqdn() {
  az containerapp show \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --query properties.configuration.ingress.fqdn \
    -o tsv
}

sample_cv_json() {
  cat <<'JSON'
{"cv":"Aisha Karimova\nTashkent International University, BSc in Computer Science (2024-). Project: Campus FAQ Bot using Python, FastAPI, and Azure OpenAI. Evaluated 100 sample questions and reached 80 percent answer accuracy. Skills: Python, Git, basic React."}
JSON
}
