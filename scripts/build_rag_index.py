#!/usr/bin/env python3
"""Build the local vector index from kb/ using OpenAI embeddings."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.load_env import load_project_env

load_project_env()

from rag.config import CHROMA_MODE, RAGConfig
from rag.store import build_index


def main() -> None:
    config = RAGConfig()
    stats = build_index(config=config, reset=True)
    print(f"Indexed {stats['chunks_indexed']} chunks into collection '{stats['collection']}'")
    if CHROMA_MODE == "local":
        print(f"Store path: {ROOT / '.rag' / 'chroma'}")
    else:
        print(f"Chroma mode: {CHROMA_MODE}")


if __name__ == "__main__":
    main()
