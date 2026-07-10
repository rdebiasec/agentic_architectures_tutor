#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

check() {
  local label="$1"
  shift
  if "$@"; then
    echo "OK  $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL $label"
    FAIL=$((FAIL + 1))
  fi
}

echo "==> Smoke test: Agentic Architectures RAG"

# 1. venv + imports
check "venv and dependencies" bash -c '
  source .venv/bin/activate
  python3 -c "import chromadb, fastapi, openai, dotenv"
'

# 2. local env active
./scripts/use-env.sh local >/dev/null
check "CHROMA_MODE=local" bash -c 'grep -q "^CHROMA_MODE=local$" .env'

# 3. local collection has chunks
check "local index count > 0" bash -c '
  source .venv/bin/activate
  python3 - <<PY
from scripts.load_env import load_project_env
load_project_env()
from rag.store import get_collection
assert get_collection(reset=False).count() > 0
PY
'

# 4. search returns chapter 5 hits
check "search Supervisor Architecture" bash -c '
  source .venv/bin/activate
  python3 scripts/rag_query.py "Supervisor Architecture" --search-only --top-k 3 2>/dev/null | grep -q "ch=5"
'

# 5. optional API health (skip if port busy)
if command -v curl >/dev/null 2>&1; then
  if ! lsof -i :8000 >/dev/null 2>&1; then
    (
      source .venv/bin/activate
      uvicorn app.main:app --port 8000 >/tmp/agentic-smoke-uvicorn.log 2>&1 &
      echo $! > /tmp/agentic-smoke-uvicorn.pid
      sleep 3
    )
    if curl -sf http://127.0.0.1:8000/health | grep -q '"status":"ok"'; then
      echo "OK  API /health"
      PASS=$((PASS + 1))
    else
      echo "FAIL API /health"
      FAIL=$((FAIL + 1))
    fi
    if [ -f /tmp/agentic-smoke-uvicorn.pid ]; then
      kill "$(cat /tmp/agentic-smoke-uvicorn.pid)" 2>/dev/null || true
      rm -f /tmp/agentic-smoke-uvicorn.pid
    fi
  else
    echo "SKIP API /health (port 8000 in use)"
  fi
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
