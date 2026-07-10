#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TARGET="${1:-}"
case "$TARGET" in
  local)
    SRC=".env.local"
    ;;
  cloud-dev)
    SRC=".env.cloud-dev"
    ;;
  cloud-prod)
    SRC=".env.cloud-prod"
    ;;
  "")
    echo "Usage: $0 {local|cloud-dev|cloud-prod}"
    exit 1
    ;;
  *)
    echo "Unknown target: $TARGET"
    echo "Usage: $0 {local|cloud-dev|cloud-prod}"
    exit 1
    ;;
esac

if [ ! -f "$SRC" ]; then
  echo "ERROR: $SRC not found"
  exit 1
fi

cp "$SRC" .env
echo "Active env: $SRC -> .env"
grep -E '^CHROMA_MODE=|^CHROMA_DATABASE=|^CHROMA_PATH=' .env || true
