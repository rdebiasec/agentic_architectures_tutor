#!/usr/bin/env python3
"""Query the Agentic Architectures RAG index."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.load_env import load_project_env

load_project_env()

from rag.config import RAGConfig
from rag.query import answer_question, search_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the local RAG knowledge base")
    parser.add_argument("question", help="Question to ask the knowledge base")
    parser.add_argument("--top-k", type=int, default=6, help="Number of chunks to retrieve")
    parser.add_argument("--chapter", type=int, help="Restrict search to one chapter number")
    parser.add_argument("--search-only", action="store_true", help="Return retrieved chunks without LLM answer")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    config = RAGConfig()

    if args.search_only:
        hits = search_chunks(args.question, config=config, top_k=args.top_k, chapter=args.chapter)
        if args.json:
            print(json.dumps(hits, indent=2))
            return
        for i, hit in enumerate(hits, start=1):
            meta = hit["metadata"]
            print(f"\n--- Hit {i} | score={hit['score']:.3f} | ch={meta.get('chapter')} | {meta.get('section')} ---")
            print(hit["text"][:1200])
        return

    result = answer_question(
        args.question,
        config=config,
        top_k=args.top_k,
        chapter=args.chapter,
    )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(result["answer"])
    print("\nSources:")
    for i, hit in enumerate(result["sources"], start=1):
        meta = hit["metadata"]
        print(
            f"  {i}. {meta.get('source_path')} | ch={meta.get('chapter')} | {meta.get('section')} | score={hit['score']:.3f}"
        )


if __name__ == "__main__":
    main()
