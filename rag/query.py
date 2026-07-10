from __future__ import annotations

from openai import OpenAI

from rag.config import RAGConfig
from rag.store import search

SYSTEM_PROMPT = """You are a study assistant for the book "Agentic Architectural Patterns for Building Multi-Agent Systems".

Answer using ONLY the provided context from the knowledge base.
If the context is insufficient, say what is missing and suggest which chapter topic to read.
Be precise, practical, and cite chapter/section names from the context when relevant.
"""


def format_context(hits: list[dict]) -> str:
    blocks = []
    for i, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        label = meta.get("title", "unknown")
        section = meta.get("section", "")
        source = meta.get("source_path", "")
        blocks.append(
            f"[Source {i}] {label} / {section} ({source})\n{hit['text']}\n"
        )
    return "\n---\n".join(blocks)


def search_chunks(
    question: str,
    *,
    config: RAGConfig | None = None,
    top_k: int | None = None,
    chapter: int | None = None,
) -> list[dict]:
    return search(question, config=config, top_k=top_k, chapter=chapter)


def answer_question(
    question: str,
    *,
    config: RAGConfig | None = None,
    top_k: int | None = None,
    chapter: int | None = None,
) -> dict:
    config = config or RAGConfig()
    hits = search_chunks(question, config=config, top_k=top_k, chapter=chapter)
    context = format_context(hits)

    client = OpenAI(api_key=config.api_key)
    response = client.chat.completions.create(
        model=config.chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nContext:\n{context}",
            },
        ],
        temperature=0.2,
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content or "",
        "sources": hits,
    }
