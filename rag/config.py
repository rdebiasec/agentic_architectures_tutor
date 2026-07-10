from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "kb"
CHAPTERS_DIR = KB_DIR / "chapters"
CODE_DIR = KB_DIR / "code"
CHROMA_DIR = Path(os.getenv("CHROMA_PATH", str(ROOT / ".rag" / "chroma")))
# local = embedded disk | cloud = Chroma Cloud | server = self-hosted HttpClient
CHROMA_MODE = os.getenv("CHROMA_MODE", "local").strip().lower()
CHROMA_HOST = os.getenv("CHROMA_HOST", "").strip()
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
CHROMA_SSL = os.getenv("CHROMA_SSL", "false").lower() in {"1", "true", "yes"}
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY", "").strip()
CHROMA_TENANT = os.getenv("CHROMA_TENANT", "").strip()
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "").strip()
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "agentic_architectures")


@dataclass(frozen=True)
class RAGConfig:
    embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    max_chunk_chars: int = 1500
    chunk_overlap_chars: int = 200
    top_k: int = 6

    @property
    def api_key(self) -> str:
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        return key
