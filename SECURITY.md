# Security checklist (before git init)

## Rotate exposed keys

The Chroma **dev** API key was previously shared in chat. Rotate it in the Chroma Cloud dashboard:

1. Log in at https://www.trychroma.com/
2. Open **Settings → API keys**
3. Revoke the old dev key and create a new one
4. Update credentials:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   chroma db connect agenticArchitecturesDev --env-vars   # paste into .env.cloud-dev
   chroma db connect agenticArchitecturesProd --env-vars  # paste into .env.cloud-prod
   ```

Prod and dev databases use **different** API keys. Never reuse one key across both.

## Files that must stay out of git

Verified in `.gitignore`:

- `.env`, `.env.local`, `.env.cloud-prod`, `.env.cloud-dev`
- `.rag/` (local vector store + manifests)
- `.venv/`
- `source/*.pdf`

## Pre-commit check

```bash
git status   # after git init — ensure no .env or .rag/ files are staged
```
