#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
source "$SCRIPT_DIR/_career_cv_demo_common.sh"

ensure_az_login

if ! resource_exists az containerapp show --name "$APP_NAME" --resource-group "$RG"; then
  echo "Container App not found: $APP_NAME in $RG" >&2
  exit 3
fi

FQDN="$(get_fqdn)"
write_state

log "Health check"
curl -fsS "https://$FQDN/health"
printf '\n'

log "One live review check"
curl -fsS -X POST "https://$FQDN/review" \
  -H "Content-Type: application/json" \
  -d "$(sample_cv_json)"
printf '\n'

log "Scale settings"
az containerapp show \
  --name "$APP_NAME" \
  --resource-group "$RG" \
  --query '{fqdn:properties.configuration.ingress.fqdn,minReplicas:properties.template.scale.minReplicas,maxReplicas:properties.template.scale.maxReplicas,provisioningState:properties.provisioningState,latestRevision:properties.latestRevisionName}' \
  -o json
