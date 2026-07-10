from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from rag.config import CHAPTERS_DIR, CODE_DIR, KB_DIR

MAX_EMBED_CHARS = 6000

TEXT_FIXUPS = (
    (re.compile(r"(?<=\s)c\s+ontent\b"), " content"),
    (re.compile(r"^ontent\b", re.M), "content"),
    (re.compile(r"\bgentic\b"), "agentic"),
    (re.compile(r"\bta structure\b"), "data structure"),
)

# Lines that look like prose but were emitted as ## headings in chapter markdown
FALSE_HEADING_RE = re.compile(
    r"^(?:However|Therefore|Furthermore|In contrast|For example|This (?:chapter|section|pattern)|"
    r"When |While |Although |Because |Note that |It is |These |Those |The following )",
    re.I,
)

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.M)


def _normalize_text(text: str) -> str:
    for pattern, replacement in TEXT_FIXUPS:
        text = pattern.sub(replacement, text)
    return text


@dataclass
class DocumentChunk:
    id: str
    text: str
    source_type: str
    source_path: str
    chapter: int | None
    title: str
    part: int | None
    section: str


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---\n", 4)
        if end != -1:
            block = text[4:end]
            body = text[end + 5 :]
            for line in block.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip().strip('"')
    return meta, body


def _split_long_text(text: str, max_chars: int, overlap: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split_at = text.rfind("\n\n", start, end)
            if split_at > start + max_chars // 2:
                end = split_at
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _chunk_markdown(path: Path, max_chars: int, overlap: int) -> list[DocumentChunk]:
    raw = _normalize_text(path.read_text(encoding="utf-8"))
    meta, body = _parse_frontmatter(raw)
    chapter = int(meta["chapter"]) if meta.get("chapter", "").isdigit() else None
    title = meta.get("title", path.stem)
    part = int(meta["part"]) if meta.get("part", "").isdigit() else None

    sections: list[tuple[str, str]] = []
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        sections.append(("Overview", body.strip()))
    else:
        preamble = body[: matches[0].start()].strip()
        if preamble:
            sections.append(("Overview", preamble))
        for i, match in enumerate(matches):
            heading = match.group(2).strip()
            if FALSE_HEADING_RE.match(heading) or len(heading.split()) > 14:
                continue
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            content = body[start:end].strip()
            if content:
                sections.append((heading, content))
        if not sections:
            sections.append(("Overview", body.strip()))

    chunks: list[DocumentChunk] = []
    chunk_idx = 0
    rel = str(path.relative_to(KB_DIR.parent))
    for section, content in sections:
        for piece in _split_long_text(content, max_chars, overlap):
            chunk_idx += 1
            header = f"Chapter {chapter}: {title}\nSection: {section}\n\n" if chapter else f"{title}\nSection: {section}\n\n"
            chunks.append(
                DocumentChunk(
                    id=f"{path.stem}-{chunk_idx:03d}",
                    text=header + piece,
                    source_type="chapter",
                    source_path=rel,
                    chapter=chapter,
                    title=title,
                    part=part,
                    section=section,
                )
            )
    return chunks


def _chunk_code(path: Path, max_chars: int, overlap: int) -> list[DocumentChunk]:
    code = _normalize_text(path.read_text(encoding="utf-8")).strip()
    if len(code) < 40:
        return []
    m = re.match(r"ch(\d+)-", path.name)
    chapter = int(m.group(1)) if m else None
    rel = str(path.relative_to(KB_DIR.parent))
    chunks: list[DocumentChunk] = []
    for i, piece in enumerate(_split_long_text(code, max_chars, overlap), start=1):
        chunks.append(
            DocumentChunk(
                id=f"{path.stem}-{i:02d}" if i > 1 else path.stem,
                text=f"Code example ({path.name}, part {i}):\n\n```python\n{piece}\n```",
                source_type="code",
                source_path=rel,
                chapter=chapter,
                title=path.name,
                part=None,
                section="code",
            )
        )
    return chunks


def load_all_chunks(max_chars: int = 1800, overlap: int = 200) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    kb_map = KB_DIR / "KB-MAP.md"
    if kb_map.exists():
        meta, body = _parse_frontmatter(kb_map.read_text(encoding="utf-8"))
        for i, piece in enumerate(_split_long_text(body, max_chars, overlap), start=1):
            chunks.append(
                DocumentChunk(
                    id=f"kb-map-{i:03d}",
                    text=f"KB Map / Book Index\n\n{piece}",
                    source_type="index",
                    source_path=str(kb_map.relative_to(KB_DIR.parent)),
                    chapter=None,
                    title="KB-MAP",
                    part=None,
                    section="index",
                )
            )

    for path in sorted(CHAPTERS_DIR.glob("*.md")):
        chunks.extend(_chunk_markdown(path, max_chars, overlap))

    for path in sorted(CODE_DIR.glob("*.py")):
        chunks.extend(_chunk_code(path, max_chars, overlap))

    return chunks
