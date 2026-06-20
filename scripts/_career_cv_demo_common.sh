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

# Resource group: defaults to a per-suffix RG the script creates. Set
# RESOURCE_GROUP to deploy into a pre-provisioned group instead (e.g. a
# KOICA-TIU team RG like rg-koicatiu-team01, where students hold Contributor but
# cannot create new RGs). When RESOURCE_GROUP points at an existing group, the
# deploy script uses it as-is and does not run `az group create`.
RG="${RESOURCE_GROUP:-rg-cvbot-${SUFFIX}}"
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

latest_revision() {
  az containerapp show --name "$APP_NAME" --resource-group "$RG" \
    --query properties.latestRevisionName -o tsv 2>/dev/null || echo ""
}

# Dump why the app isn't serving: revision running/health state, replica
# container states (crash/exit reasons), and system + console logs.
dump_app_diagnostics() {
  local rev
  rev="$(latest_revision)"
  echo "===== Diagnostics for $APP_NAME (rev: ${rev:-?}) =====" >&2
  az containerapp revision show --name "$APP_NAME" --resource-group "$RG" --revision "$rev" \
    --query '{runningState:properties.runningState,healthState:properties.healthState,active:properties.active,replicas:properties.replicas,provisioningError:properties.provisioningError}' \
    -o json >&2 2>&1 || true
  echo "--- replicas (container states / termination reasons) ---" >&2
  az containerapp replica list --name "$APP_NAME" --resource-group "$RG" --revision "$rev" -o json >&2 2>&1 || true
  echo "--- system logs (tail 80) ---" >&2
  az containerapp logs show --name "$APP_NAME" --resource-group "$RG" --type system --tail 80 >&2 2>&1 || true
  echo "--- console logs (tail 80) ---" >&2
  az containerapp logs show --name "$APP_NAME" --resource-group "$RG" --type console --tail 80 >&2 2>&1 || true
}

# Poll the app's /health until it returns 200. A freshly created (or scaled-to-
# zero) Container App revision is not routable instantly — the ingress returns
# 404 until the first revision is active/healthy — so verifying with a single
# immediate curl races the activation. Fail fast if the revision has clearly
# failed to start, and on any failure dump diagnostics so a real startup crash
# is visible rather than silent.
wait_for_health() {
  local fqdn="$1" attempts="${2:-40}" delay="${3:-6}" code rstate
  log "Waiting for https://${fqdn}/health (up to $((attempts * delay))s)"
  for ((i = 1; i <= attempts; i++)); do
    code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "https://${fqdn}/health" || echo 000)"
    if [[ "$code" == "200" ]]; then
      echo "Healthy after ~$((i * delay))s (HTTP 200)"
      return 0
    fi
    if (( i % 5 == 0 )); then
      rstate="$(az containerapp revision show --name "$APP_NAME" --resource-group "$RG" \
        --revision "$(latest_revision)" --query properties.runningState -o tsv 2>/dev/null || echo '')"
      echo "  attempt ${i}/${attempts}: HTTP ${code}, revision runningState=${rstate:-?}"
      if [[ "$rstate" == "Failed" ]]; then
        echo "Latest revision runningState=Failed — not waiting further." >&2
        dump_app_diagnostics
        return 1
      fi
    else
      echo "  attempt ${i}/${attempts}: HTTP ${code} — retrying in ${delay}s"
    fi
    sleep "$delay"
  done
  echo "App did not become healthy at https://${fqdn}/health after $((attempts * delay))s" >&2
  dump_app_diagnostics
  return 1
}

sample_cv_json() {
  cat <<'JSON'
{"cv":"Aisha Karimova\nTashkent International University, BSc in Computer Science (2024-). Project: Campus FAQ Bot using Python, FastAPI, and Azure OpenAI. Evaluated 100 sample questions and reached 80 percent answer accuracy. Skills: Python, Git, basic React."}
JSON
}
