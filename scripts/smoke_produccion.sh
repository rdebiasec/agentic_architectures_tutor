#!/usr/bin/env bash
set -euo pipefail

RENDER="${RENDER_URL:-https://agentic-architectures-rag.onrender.com}"

echo "==> Production smoke test: $RENDER"
fail=0

check() {
  local label="$1"
  shift
  if "$@"; then
    echo "OK  $label"
  else
    echo "FAIL $label"
    fail=1
  fi
}

check "GET /health" curl -sf "$RENDER/health" | grep -q '"status":"ok"'
check "chunks > 0" curl -sf "$RENDER/health" | grep -q '"chunks_indexed":'
check "chroma_mode cloud" curl -sf "$RENDER/health" | grep -q '"chroma_mode":"cloud"'
check "GET /search" curl -sf "$RENDER/search?q=Supervisor+Architecture&top_k=2" | grep -q '"results"'

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "Production smoke test passed."
else
  echo "Production smoke test failed."
  exit 1
fi
