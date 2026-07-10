from __future__ import annotations

from typing import Iterable

import chromadb
from chromadb.api.models.Collection import Collection
from openai import OpenAI

from rag.chunker import DocumentChunk, load_all_chunks, MAX_EMBED_CHARS
from rag.config import (
    CHROMA_API_KEY,
    CHROMA_DATABASE,
    CHROMA_DIR,
    CHROMA_HOST,
    CHROMA_MODE,
    CHROMA_PORT,
    CHROMA_SSL,
    CHROMA_TENANT,
    COLLECTION_NAME,
    RAGConfig,
)


def _prepare_for_embedding(text: str) -> str:
    if len(text) <= MAX_EMBED_CHARS:
        return text
    return text[:MAX_EMBED_CHARS] + "\n\n[... truncated for embedding ...]"


def _embed_texts(client: OpenAI, model: str, texts: list[str]) -> list[list[float]]:
    prepared = [_prepare_for_embedding(t) for t in texts]
    response = client.embeddings.create(model=model, input=prepared)
    return [item.embedding for item in response.data]


def get_chroma_client():
    mode = CHROMA_MODE
    if mode == "cloud":
        if not CHROMA_API_KEY:
            raise RuntimeError("CHROMA_MODE=cloud requires CHROMA_API_KEY")
        kwargs: dict = {"api_key": CHROMA_API_KEY}
        if CHROMA_TENANT:
            kwargs["tenant"] = CHROMA_TENANT
        if CHROMA_DATABASE:
            kwargs["database"] = CHROMA_DATABASE
        return chromadb.CloudClient(**kwargs)

    if mode == "server" or CHROMA_HOST:
        return chromadb.HttpClient(
            host=CHROMA_HOST or "localhost",
            port=CHROMA_PORT,
            ssl=CHROMA_SSL,
            headers={"Authorization": f"Bearer {CHROMA_API_KEY}"} if CHROMA_API_KEY else None,
        )

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(reset: bool = False) -> Collection:
    db = get_chroma_client()
    if reset:
        try:
            db.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return db.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def build_index(config: RAGConfig | None = None, reset: bool = True) -> dict[str, int]:
    config = config or RAGConfig()
    client = OpenAI(api_key=config.api_key)
    chunks = load_all_chunks(config.max_chunk_chars, config.chunk_overlap_chars)
    collection = get_collection(reset=reset)

    batch_size = 64
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        embeddings = _embed_texts(client, config.embedding_model, [c.text for c in batch])
        collection.add(
            ids=[c.id for c in batch],
            documents=[c.text for c in batch],
            embeddings=embeddings,
            metadatas=[
                {
                    "source_type": c.source_type,
                    "source_path": c.source_path,
                    "chapter": c.chapter if c.chapter is not None else -1,
                    "title": c.title,
                    "part": c.part if c.part is not None else -1,
                    "section": c.section,
                }
                for c in batch
            ],
        )

    return {"chunks_indexed": len(chunks), "collection": COLLECTION_NAME}


def search(
    query: str,
    *,
    config: RAGConfig | None = None,
    top_k: int | None = None,
    chapter: int | None = None,
    source_type: str | None = None,
) -> list[dict]:
    config = config or RAGConfig()
    client = OpenAI(api_key=config.api_key)
    collection = get_collection(reset=False)
    if collection.count() == 0:
        raise RuntimeError("RAG index is empty. Run: python3 scripts/build_rag_index.py")

    query_embedding = _embed_texts(client, config.embedding_model, [query])[0]
    where: dict | None = None
    filters = []
    if chapter is not None:
        filters.append({"chapter": chapter})
    if source_type is not None:
        filters.append({"source_type": source_type})
    if len(filters) == 1:
        where = filters[0]
    elif len(filters) > 1:
        where = {"$and": filters}

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k or config.top_k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    hits: list[dict] = []
    for doc, meta, distance in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    ):
        hits.append(
            {
                "text": doc,
                "metadata": meta,
                "score": 1 - distance,
            }
        )
    return hits
