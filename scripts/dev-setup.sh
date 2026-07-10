#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Agentic Architectures — dev setup"
echo "Project: $ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "==> Creating .venv"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing dependencies"
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.local" ]; then
  echo "==> Activating .env.local"
  cp .env.local .env
fi

if [ -z "${OPENAI_API_KEY:-}" ] && [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "WARN: OPENAI_API_KEY not set. Add it to .env.local before indexing or querying."
else
  echo "OK: OPENAI_API_KEY is set"
fi

echo ""
echo "Setup complete. Next steps:"
echo "  source .venv/bin/activate"
echo "  ./scripts/use-env.sh local"
echo "  python3 scripts/build_rag_index.py    # if index missing"
echo "  python3 scripts/rag_query.py \"your question\""
echo ""
echo "Chroma CLI (optional): export PATH=\"\$HOME/.local/bin:\$PATH\""
