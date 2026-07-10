"""Load project environment files in priority order."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_project_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    for name in (".env", ".env.local"):
        path = ROOT / name
        if path.exists():
            load_dotenv(path)
            return
