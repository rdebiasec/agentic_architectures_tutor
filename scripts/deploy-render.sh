#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REPO_URL="https://github.com/rdebiasec/agentic_architectures_tutor"
BLUEPRINT_URL="https://render.com/deploy?repo=${REPO_URL}"
OPEN_BROWSER=false
if [[ "${1:-}" == "--open" ]]; then
  OPEN_BROWSER=true
fi

echo "==> Agentic Architectures — Render deploy helper"
echo ""
echo "Repository:  $REPO_URL"
echo "Blueprint:   $BLUEPRINT_URL"
echo ""

if [[ -f ".env.cloud-prod" ]]; then
  echo "Secrets to paste in Render Dashboard (from .env.cloud-prod):"
  for key in OPENAI_API_KEY CHROMA_API_KEY CHROMA_TENANT; do
    if grep -q "^${key}=" .env.cloud-prod; then
      val=$(grep "^${key}=" .env.cloud-prod | cut -d= -f2-)
      if [[ -n "$val" ]]; then
        echo "  OK  $key (set locally)"
      else
        echo "  MISSING  $key"
      fi
    else
      echo "  MISSING  $key"
    fi
  done
else
  echo "WARN: .env.cloud-prod not found — create it before deploying"
fi

echo ""
echo "Steps:"
echo "  1. Open: $BLUEPRINT_URL"
echo "  2. Sign in with GitHub (account: rdebiasec)"
echo "  3. Deploy Blueprint → paste the 3 secrets when prompted"
echo "  4. After deploy, test: ./scripts/smoke_produccion.sh"
echo ""
echo "Full guide: DEPLOY.md"

if $OPEN_BROWSER && command -v open >/dev/null 2>&1; then
  open "$BLUEPRINT_URL"
fi
