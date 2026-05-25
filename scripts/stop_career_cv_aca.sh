#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
source "$SCRIPT_DIR/_career_cv_demo_common.sh"

ensure_az_login

if ! resource_exists az containerapp show --name "$APP_NAME" --resource-group "$RG"; then
  echo "Container App already absent: $APP_NAME in $RG"
  exit 0
fi

log "Deactivating active revisions"
revisions="$(az containerapp revision list \
  --name "$APP_NAME" \
  --resource-group "$RG" \
  --query "[?properties.active].name" \
  -o tsv)"

if [[ -z "$revisions" ]]; then
  echo "No active revisions found."
else
  while IFS= read -r revision; do
    [[ -z "$revision" ]] && continue
    run az containerapp revision deactivate \
      --name "$APP_NAME" \
      --resource-group "$RG" \
      --revision "$revision"
  done <<< "$revisions"
fi

log "Stop complete"
az containerapp revision list \
  --name "$APP_NAME" \
  --resource-group "$RG" \
  --query '[].{name:name,active:properties.active,createdTime:properties.createdTime}' \
  -o table
