#!/usr/bin/env python3
"""Export a text-hash manifest of the active Chroma index for parity checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.load_env import load_project_env

load_project_env()

from rag.config import CHROMA_MODE, COLLECTION_NAME
from rag.store import get_collection

CLOUD_PAGE_SIZE = 300


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_all_records() -> list[dict]:
    collection = get_collection(reset=False)
    total = collection.count()
    if total == 0:
        raise RuntimeError("Collection is empty. Run scripts/build_rag_index.py first.")

    records: list[dict] = []
    offset = 0
    while offset < total:
        limit = min(CLOUD_PAGE_SIZE, total - offset)
        batch = collection.get(
            limit=limit,
            offset=offset,
            include=["documents", "metadatas"],
        )
        ids = batch.get("ids") or []
        docs = batch.get("documents") or []
        metas = batch.get("metadatas") or []
        for chunk_id, doc, meta in zip(ids, docs, metas):
            meta = meta or {}
            chapter = meta.get("chapter", -1)
            records.append(
                {
                    "chunk_id": chunk_id,
                    "source_path": meta.get("source_path", ""),
                    "chapter": None if chapter == -1 else chapter,
                    "section": meta.get("section", ""),
                    "text_hash": text_hash(doc or ""),
                }
            )
        if not ids:
            break
        offset += len(ids)

    records.sort(key=lambda r: r["chunk_id"])
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Chroma index manifest (text hashes)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output JSON path (default: .rag/manifest-<mode>.json)",
    )
    args = parser.parse_args()

    records = fetch_all_records()
    output = args.output or (ROOT / ".rag" / f"manifest-{CHROMA_MODE}.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "chroma_mode": CHROMA_MODE,
        "collection": COLLECTION_NAME,
        "chunk_count": len(records),
        "records": records,
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} records to {output}")


if __name__ == "__main__":
    main()
