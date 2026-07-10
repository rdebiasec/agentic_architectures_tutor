"""Minimal RAG API for Render / production."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.load_env import load_project_env

load_project_env()

from rag.config import CHROMA_MODE, COLLECTION_NAME, RAGConfig
from rag.query import answer_question, search_chunks
from rag.store import get_collection

app = FastAPI(
    title="Agentic Architectures RAG",
    description="Query the Packt book knowledge base (Chroma + OpenAI).",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=4000)
    top_k: int = Field(default=6, ge=1, le=20)
    chapter: Optional[int] = Field(default=None, ge=1, le=16)


@app.get("/health")
def health() -> dict[str, Any]:
    try:
        count = get_collection(reset=False).count()
        return {
            "status": "ok",
            "chroma_mode": CHROMA_MODE,
            "collection": COLLECTION_NAME,
            "chunks_indexed": count,
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/query")
def query(req: QueryRequest) -> dict[str, Any]:
    try:
        return answer_question(
            req.question,
            config=RAGConfig(),
            top_k=req.top_k,
            chapter=req.chapter,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/search")
def search(
    q: str = Query(..., min_length=3),
    top_k: int = Query(default=6, ge=1, le=20),
    chapter: Optional[int] = Query(default=None, ge=1, le=16),
) -> dict[str, Any]:
    try:
        hits = search_chunks(q, config=RAGConfig(), top_k=top_k, chapter=chapter)
        return {"question": q, "results": hits}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
