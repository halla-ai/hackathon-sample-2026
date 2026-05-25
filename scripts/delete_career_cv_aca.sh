#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
source "$SCRIPT_DIR/_career_cv_demo_common.sh"

ensure_az_login

if ! resource_exists az group show --name "$RG"; then
  echo "Resource group already absent: $RG"
  exit 0
fi

log "Deleting resource group"
run az group delete --name "$RG" --yes --no-wait

log "Delete started"
echo "RESOURCE_GROUP=$RG"
echo "Deletion is asynchronous. Check with: az group exists --name $RG"
