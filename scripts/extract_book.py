#!/usr/bin/env python3
"""Extract Agentic Architectural Patterns PDF into chapter markdown, code, and figure assets."""

from __future__ import annotations

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "source" / "Agentic Architectural Patterns for Building Multi-Agent Systems.pdf"
KB = ROOT / "kb"
CHAPTERS_DIR = KB / "chapters"
CODE_DIR = KB / "code"
ASSETS_DIR = KB / "assets"
META_FILE = KB / "extraction-meta.json"

DPI = 200
PAGE_WIDTH_PT = 540.0
PAGE_HEIGHT_PT = 666.0

CHAPTERS: list[tuple[int, str, str, int, int, int]] = [
    (1, "genai-in-the-enterprise", "GenAI in the Enterprise: Landscape, Maturity, and Agent Focus", 40, 61, 1),
    (2, "agent-ready-llms", "Agent-Ready LLMs: Selection, Deployment, and Adaptation", 62, 93, 1),
    (3, "llm-adaptation-rag-to-finetuning", "The Spectrum of LLM Adaptation for Agents: RAG to Fine-tuning", 94, 131, 1),
    (4, "agentic-ai-architecture", "Agentic AI Architecture: Components and Interactions", 132, 155, 1),
    (5, "multi-agent-coordination-patterns", "Multi-Agent Coordination Patterns", 156, 219, 2),
    (6, "explainability-compliance-patterns", "Explainability and Compliance Agentic Patterns", 220, 241, 2),
    (7, "robustness-fault-tolerance-patterns", "Robustness and Fault Tolerance Patterns", 242, 317, 2),
    (8, "human-agent-interaction-patterns", "Human-Agent Interaction Patterns", 318, 345, 2),
    (9, "agent-level-patterns", "Agent-Level Patterns", 346, 375, 2),
    (10, "system-level-production-patterns", "System-Level Patterns for Production Readiness", 376, 403, 2),
    (11, "advanced-adaptation", "Advanced Adaptation: Building Agents That Learn", 404, 443, 2),
    (12, "practical-roadmap-maturity", "A Practical Roadmap: Implementing Agentic Patterns by Maturity Level", 444, 459, 3),
    (13, "use-case-single-agent-loan", "Use Case: A Single Agent for Loan Processing", 460, 485, 3),
    (14, "use-case-multi-agent-loan", "Use Case: A Multi-Agent System for Loan Processing", 486, 507, 3),
    (15, "agent-frameworks-comparison", "Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph", 508, 545, 3),
    (16, "conclusion", "Conclusion: Charting Your Agentic AI Journey", 546, 573, 3),
]

PART_NAMES = {
    1: "Part 1: Foundations and Core Agent Concepts",
    2: "Part 2: Agentic Design Patterns",
    3: "Part 3: Execution: Strategy, Use Cases, and The Future",
}

IDX_RE = re.compile(r"idx_[a-f0-9]+")
FIGURE_CAPTION_RE = re.compile(r"^Figure\s+(\d+\.\d+)\s*[–-]\s*(.+)$", re.I)
FIGURE_INLINE_RE = re.compile(r"Figure\s+(\d+\.\d+)\s*[–-]\s*([^\n]+)")
CHAPTER_HEADER_RE = re.compile(r"^Chapter\s+\d+\s*$")
PAGE_NUM_ONLY_RE = re.compile(r"^\d{1,3}$")
CODE_START_RE = re.compile(
    r"^(class |def |async def |import |from \w+ import|@|# |if __name__)"
)
SUMMARY_RE = re.compile(r"^Summary\s*$", re.I)
MAX_CODE_LINES = 400
MIN_CODE_LINES = 3
PYTHON_SIGNAL_RE = re.compile(r"^\s*(def |class |import |from \w+ import)")


@dataclass
class FigureInfo:
    number: str
    caption: str
    page: int
    chapter: int
    asset_path: str


@dataclass
class ChapterMeta:
    number: int
    slug: str
    title: str
    start_page: int
    end_page: int
    part: int
    figures: list[FigureInfo] = field(default_factory=list)
    code_files: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)


def clean_text(text: str) -> str:
    text = IDX_RE.sub(" ", text)
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"  +", " ", text)
    text = re.sub(r" +([,.;:!?])", r"\1", text)
    text = re.sub(r"(?<=\s)c\s+ontent\b", " content", text)
    text = re.sub(r"^ontent\b", "content", text, flags=re.M)
    return text.strip()


def extract_page_text(reader: PdfReader, page_num: int) -> str:
    return reader.pages[page_num - 1].extract_text() or ""


def parse_page_words(page_num: int) -> list[dict]:
    cmd = ["pdftotext", "-bbox", "-f", str(page_num), "-l", str(page_num), str(PDF), "-"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    root = ET.fromstring(result.stdout)
    words = []
    for page in root.findall(".//page"):
        for word in page.findall("word"):
            words.append(
                {
                    "text": (word.text or "").strip(),
                    "xMin": float(word.get("xMin", 0)),
                    "yMin": float(word.get("yMin", 0)),
                    "xMax": float(word.get("xMax", 0)),
                    "yMax": float(word.get("yMax", 0)),
                }
            )
    return words


def find_figure_captions(words: list[dict]) -> list[tuple[str, str, float]]:
    """Return list of (figure_num, caption_text, caption_yMin)."""
    lines: dict[float, list[dict]] = {}
    for w in words:
        if not w["text"] or w["text"].startswith("idx_"):
            continue
        key = round(w["yMin"], 1)
        lines.setdefault(key, []).append(w)

    captions = []
    for y in sorted(lines.keys()):
        line_words = sorted(lines[y], key=lambda w: w["xMin"])
        line_text = " ".join(w["text"] for w in line_words)
        line_text = IDX_RE.sub("", line_text).strip()
        m = FIGURE_CAPTION_RE.match(line_text)
        if m:
            captions.append((m.group(1), m.group(2).strip(), y))
    return captions


def figure_crop_box(words: list[dict], caption_y: float) -> tuple[int, int, int, int] | None:
    """Compute crop box in pixel coords for figure region above caption."""
    content_words = [
        w for w in words if w["text"] and not w["text"].startswith("idx_") and w["yMax"] < caption_y - 8
    ]
    if not content_words:
        return None

    header_cutoff = 110.0
    body_words = [w for w in content_words if w["yMin"] < caption_y - 40]
    if not body_words:
        return None

    text_lines: dict[float, list[dict]] = {}
    for w in body_words:
        key = round(w["yMin"], 1)
        text_lines.setdefault(key, []).append(w)

    sorted_ys = sorted(text_lines.keys())
    figure_top = header_cutoff
    for y in sorted_ys:
        if y > header_cutoff and y < caption_y - 60:
            line_words = sorted(text_lines[y], key=lambda x: x["xMin"])
            line = " ".join(w["text"] for w in line_words)
            if FIGURE_CAPTION_RE.match(IDX_RE.sub("", line)):
                break
            figure_top = max(figure_top, text_lines[y][0]["yMax"] + 12)

    figure_bottom = caption_y - 10
    if figure_bottom - figure_top < 80:
        figure_top = header_cutoff
        figure_bottom = caption_y - 10
    if figure_bottom - figure_top < 60:
        return None

    scale = DPI / 72.0
    left = int(50 * scale)
    right = int((PAGE_WIDTH_PT - 50) * scale)
    top = int(figure_top * scale)
    bottom = int(figure_bottom * scale)
    return left, top, right, bottom


def render_page_png(page_num: int, out_path: Path) -> Path:
    prefix = out_path.with_suffix("")
    cmd = ["pdftoppm", "-png", "-r", str(DPI), "-f", str(page_num), "-l", str(page_num), str(PDF), str(prefix)]
    subprocess.run(cmd, capture_output=True, check=True)
    generated = Path(f"{prefix}-{page_num:02d}.png" if page_num < 100 else f"{prefix}-{page_num}.png")
    if not generated.exists():
        candidates = list(out_path.parent.glob(f"{prefix.name}-*.png"))
        if not candidates:
            raise FileNotFoundError(f"No PNG rendered for page {page_num}")
        generated = candidates[0]
    img = Image.open(generated)
    img.save(out_path)
    generated.unlink(missing_ok=True)
    return out_path


def slugify_caption(text: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].strip("-")


def page_embedded_images(page_num: int, tmp_dir: Path) -> list[Path]:
    prefix = tmp_dir / f"p{page_num}"
    subprocess.run(
        ["pdfimages", "-f", str(page_num), "-l", str(page_num), "-png", str(PDF), str(prefix)],
        capture_output=True,
        check=True,
    )
    imgs = list(tmp_dir.glob(f"p{page_num}-*.png"))
    scored: list[tuple[int, Path]] = []
    for img_path in imgs:
        try:
            with Image.open(img_path) as img:
                w, h = img.size
        except OSError:
            continue
        if w < 180 or h < 120:
            continue
        scored.append((w * h, img_path))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored]


def crop_page_region(page_num: int, region: str) -> Image.Image:
    page_png = ASSETS_DIR / f"_tmp-page-{page_num}.png"
    render_page_png(page_num, page_png)
    img = Image.open(page_png)
    w, h = img.size
    if region == "top":
        box = (int(w * 0.05), int(h * 0.12), int(w * 0.95), int(h * 0.52))
    else:
        box = (int(w * 0.05), int(h * 0.48), int(w * 0.95), int(h * 0.88))
    cropped = img.crop(box)
    page_png.unlink(missing_ok=True)
    return cropped


def extract_figures(chapter: ChapterMeta, reader: PdfReader) -> list[FigureInfo]:
    figures: list[FigureInfo] = []
    asset_dir = ASSETS_DIR / f"ch{chapter.number:02d}"
    asset_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = asset_dir / "_tmp"
    tmp_dir.mkdir(exist_ok=True)

    for page_num in range(chapter.start_page, chapter.end_page + 1):
        text = clean_text(extract_page_text(reader, page_num))
        matches: list[tuple[str, str]] = []
        for line in text.split("\n"):
            line = line.strip()
            m = FIGURE_CAPTION_RE.match(line)
            if m:
                matches.append((m.group(1), m.group(2).strip()))
        if not matches:
            continue

        embedded = page_embedded_images(page_num, tmp_dir)
        for idx, (fig_num, caption) in enumerate(matches):
            fname = f"fig-{fig_num.replace('.', '-')}-{slugify_caption(caption)}.png"
            out = asset_dir / fname

            if idx < len(embedded):
                Image.open(embedded[idx]).save(out)
            elif len(matches) == 2 and len(embedded) == 0:
                crop = crop_page_region(page_num, "top" if idx == 0 else "bottom")
                crop.save(out)
            elif embedded:
                Image.open(embedded[0]).save(out)
            else:
                crop = crop_page_region(page_num, "top")
                crop.save(out)

            rel = f"../assets/ch{chapter.number:02d}/{fname}"
            figures.append(
                FigureInfo(
                    number=fig_num,
                    caption=caption,
                    page=page_num,
                    chapter=chapter.number,
                    asset_path=rel,
                )
            )

    for p in tmp_dir.glob("*"):
        p.unlink()
    tmp_dir.rmdir()
    return figures


def is_heading_line(line: str) -> bool:
    if not line or len(line) > 100 or len(line) < 8:
        return False
    if line.endswith((".", ",", ";")):
        return False
    if line.startswith(("•", "-", "Figure ", "Table ", "Chapter ", "http", "In this chapter")):
        return False
    if re.match(r"^\d+\.?\d*\s", line) or re.match(r"^\d+[A-Z]", line):
        return False
    if line in {"Focus", "Free Benefits with Your Book"}:
        return False
    skip = ("your purchase", "scan the qr", "packtpub", "download", "example", "imagine ")
    if any(s in line.lower() for s in skip):
        return False
    words = line.split()
    if len(words) < 3:
        return False
    if line.isupper() and len(words) >= 3:
        return True
    if line.endswith(":"):
        return True
    titleish = sum(1 for w in words if w and w[0].isupper()) / len(words)
    return titleish >= 0.85 and not any(w.lower() in {"the", "and", "for", "with", "that", "this", "from"} for w in words[-2:])


def is_prose_line(line: str) -> bool:
    if is_heading_line(line):
        return True
    words = line.split()
    if len(words) > 18:
        return True
    if line.endswith(".") and len(words) >= 8:
        lowerish = sum(1 for w in words if w and w[0].islower())
        if lowerish / len(words) >= 0.55:
            return True
    return False


def is_valid_python_block(code: str) -> bool:
    lines = [line for line in code.splitlines() if line.strip()]
    if len(lines) < MIN_CODE_LINES or len(lines) > MAX_CODE_LINES:
        return False

    signal_types = 0
    for pattern in (r"^\s*def ", r"^\s*class ", r"^\s*import ", r"^\s*from \w+ import"):
        if any(re.match(pattern, line) for line in lines):
            signal_types += 1
    if signal_types < 2:
        return False

    code_like = sum(1 for line in lines if PYTHON_SIGNAL_RE.match(line) or line.startswith((" ", "\t")))
    if code_like / len(lines) < 0.35:
        return False

    prose_like = sum(1 for line in lines if is_prose_line(line))
    if prose_like / len(lines) > 0.25:
        return False

    return True


def lines_to_markdown(lines: list[str], figure_map: dict[str, FigureInfo]) -> str:
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []

    def flush_code():
        nonlocal code_buf, in_code
        if code_buf:
            out.append("```python")
            out.extend(code_buf)
            out.append("```")
            out.append("")
            code_buf = []
        in_code = False

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            if in_code:
                flush_code()
            else:
                if out and out[-1] != "":
                    out.append("")
            i += 1
            continue

        if CHAPTER_HEADER_RE.match(line) or PAGE_NUM_ONLY_RE.match(line):
            i += 1
            continue

        fig_match = FIGURE_CAPTION_RE.match(line)
        if fig_match:
            if in_code:
                flush_code()
            fig_num = fig_match.group(1)
            caption = fig_match.group(2).strip()
            info = figure_map.get(fig_num)
            if info:
                out.append(f"![Figure {fig_num} – {caption}]({info.asset_path})")
                out.append("")
                out.append(f"*Figure {fig_num} – {caption}*")
            else:
                out.append(f"**Figure {fig_num} – {caption}**")
            out.append("")
            i += 1
            continue

        if SUMMARY_RE.match(line):
            if in_code:
                flush_code()
            out.append("## Summary")
            out.append("")
            i += 1
            continue

        if CODE_START_RE.match(line) or in_code:
            if not in_code and is_heading_line(line):
                pass
            elif in_code and is_prose_line(line):
                flush_code()
                out.append(line)
                i += 1
                continue
            else:
                in_code = True
                code_buf.append(line)
                i += 1
                continue

        if is_heading_line(line) and not line.startswith("Get This Book"):
            if in_code:
                flush_code()
            out.append(f"## {line}")
            out.append("")
            i += 1
            continue

        if line.startswith("• "):
            if in_code:
                flush_code()
            out.append(line.replace("• ", "- ", 1))
            i += 1
            continue

        out.append(line)
        i += 1

    if in_code:
        flush_code()

    return "\n".join(out)


def extract_code_blocks(markdown: str, chapter: ChapterMeta) -> tuple[str, list[str]]:
    code_files: list[str] = []
    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    idx = 0

    def replacer(match: re.Match) -> str:
        nonlocal idx
        code = match.group(1).strip()
        if not is_valid_python_block(code):
            return match.group(0)
        idx += 1
        fname = f"ch{chapter.number:02d}-snippet-{idx:02d}.py"
        path = CODE_DIR / fname
        path.write_text(code + "\n", encoding="utf-8")
        code_files.append(fname)
        return f"{match.group(0)}\n\n*[Code file: `code/{fname}`]*\n"

    updated = pattern.sub(replacer, markdown)
    return updated, code_files


def detect_patterns(text: str) -> list[str]:
    patterns = set()
    for m in re.finditer(r"(?:Pattern|Architecture|Framework):\s*([^\n\.]{5,80})", text, re.I):
        patterns.add(m.group(1).strip())
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4}\s+(?:Pattern|Architecture|Framework))\b", text):
        patterns.add(m.group(1).strip())
    return sorted(patterns)[:40]


def build_chapter_markdown(chapter: ChapterMeta, reader: PdfReader) -> str:
    raw_parts = []
    for page_num in range(chapter.start_page, chapter.end_page + 1):
        raw_parts.append(extract_page_text(reader, page_num))
    raw = clean_text("\n\n".join(raw_parts))

    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    # Drop repeated headers/footers and Packt promos
    filtered = []
    skip_phrases = (
        "Get This Book's PDF Version",
        "Scan the QR code",
        "packtpub.com/unlock",
        "Share your thoughts",
        "Free Benefits with Your Book",
        "Your purchase includes a free PDF",
        "Download a PDF of this book",
    )
    for line in lines:
        if any(p in line for p in skip_phrases):
            continue
        if CHAPTER_HEADER_RE.match(line) or line in {"•", "-"}:
            continue
        if re.match(rf"^{chapter.number}\s*$", line):
            continue
        if re.match(rf"^{chapter.number}[A-Za-z]", line):
            line = re.sub(rf"^{chapter.number}", "", line).strip()
            if not line:
                continue
        filtered.append(line)

    figure_map = {f.number: f for f in chapter.figures}
    body = lines_to_markdown(filtered, figure_map)
    body, code_files = extract_code_blocks(body, chapter)
    chapter.code_files = code_files
    chapter.patterns = detect_patterns(body)

    md = [
        "---",
        f"chapter: {chapter.number}",
        f'title: "{chapter.title}"',
        f"part: {chapter.part}",
        f'part_name: "{PART_NAMES[chapter.part]}"',
        f"pdf_pages: [{chapter.start_page}, {chapter.end_page}]",
        f"figures: {len(chapter.figures)}",
        f"code_files: {json.dumps(code_files)}",
        f"patterns: {json.dumps(chapter.patterns)}",
        "---",
        "",
        f"# Chapter {chapter.number}: {chapter.title}",
        "",
        body,
    ]
    return "\n".join(md)


def extract_summary_section(markdown: str) -> str:
    m = re.search(r"## Summary\s*\n+(.*?)(?:\n## |\Z)", markdown, re.DOTALL | re.I)
    if m:
        return clean_text(m.group(1))[:500]
    return ""


def extract_pattern_headings(metas: list[ChapterMeta]) -> dict[int, list[str]]:
    catalog: dict[int, list[str]] = {}
    skip_fragments = ("the key", "that govern", "if task", "def", "==", "following:", "as follows:")
    keep_tokens = ("pattern", "architecture", "framework", "topology", "hub", "delegation", "coordination", "compliance", "interaction", "adaptation", "observability", "guardrail", "supervisor", "blackboard", "consensus", "negotiation", "auction", "market", "swarm", "pipeline", "orchestr")
    for m in metas:
        if m.number < 5 or m.number > 11:
            continue
        path = CHAPTERS_DIR / f"{m.number:02d}-{m.slug}.md"
        if not path.exists():
            continue
        headings: list[str] = []
        seen: set[str] = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("## ") or line.startswith("## Summary"):
                continue
            title = line[3:].strip()
            low = title.lower()
            if len(title) < 6 or len(title) > 90:
                continue
            if any(s in low for s in skip_fragments):
                continue
            if not any(t in low for t in keep_tokens) and not title.istitle():
                continue
            if title not in seen:
                seen.add(title)
                headings.append(title)
        catalog[m.number] = headings
    return catalog


def build_kb_map(metas: list[ChapterMeta], summaries: dict[int, str]) -> str:
    lines = [
        "# KB Map — Agentic Architectural Patterns for Building Multi-Agent Systems",
        "",
        "> Knowledge base index for learning agentic architectures. Source: Packt, Arsanjani & Bustos (2026).",
        "",
        "## Book overview",
        "",
        "This book provides design patterns and practices for building production-grade multi-agent GenAI systems,",
        "covering LLM selection, RAG/fine-tuning, coordination patterns, compliance, fault tolerance, human-agent",
        "interaction, and hands-on implementations with ADK, CrewAI, and LangGraph.",
        "",
        "## Chapter index",
        "",
        "| Ch | Title | Part | Figures | Code |",
        "|----|-------|------|---------|------|",
    ]

    for m in metas:
        lines.append(
            f"| [{m.number}](chapters/{m.number:02d}-{m.slug}.md) | {m.title} | {m.part} | {len(m.figures)} | {len(m.code_files)} |"
        )

    lines.extend(["", "## Chapter summaries", ""])
    for m in metas:
        summary = summaries.get(m.number, "_Summary not found._")
        lines.extend([f"### Chapter {m.number}: {m.title}", "", summary, ""])

    lines.extend(["", "## Parts", ""])
    for part_num, name in PART_NAMES.items():
        chs = [m for m in metas if m.part == part_num]
        lines.append(f"### {name}")
        lines.append("")
        for m in chs:
            lines.append(f"- [Chapter {m.number}](chapters/{m.number:02d}-{m.slug}.md): {m.title}")
        lines.append("")

    lines.extend(
        [
            "## Learning paths",
            "",
            "### For software architects",
            "1. [Ch 1](chapters/01-genai-in-the-enterprise.md) → [Ch 4](chapters/04-agentic-ai-architecture.md) → [Ch 5–10](chapters/05-multi-agent-coordination-patterns.md) → [Ch 12](chapters/12-practical-roadmap-maturity.md)",
            "",
            "### For AI / ML engineers",
            "1. [Ch 2](chapters/02-agent-ready-llms.md) → [Ch 3](chapters/03-llm-adaptation-rag-to-finetuning.md) → [Ch 13–15](chapters/13-use-case-single-agent-loan.md) (code)",
            "",
            "### For technical leaders",
            "1. [Ch 1 Maturity Model](chapters/01-genai-in-the-enterprise.md) → [Ch 12 Roadmap](chapters/12-practical-roadmap-maturity.md) → [Ch 16 Conclusion](chapters/16-conclusion.md)",
            "",
            "## Pattern chapters (deep dive)",
            "",
        ]
    )
    for m in metas:
        if 5 <= m.number <= 11:
            lines.append(f"- [Chapter {m.number}](chapters/{m.number:02d}-{m.slug}.md): {m.title}")

    pattern_catalog = extract_pattern_headings(metas)
    if pattern_catalog:
        lines.extend(["", "## Pattern catalog (by chapter)", ""])
        for ch_num in sorted(pattern_catalog):
            m = next(x for x in metas if x.number == ch_num)
            lines.append(f"### Chapter {ch_num}: {m.title}")
            lines.append("")
            for h in pattern_catalog[ch_num]:
                anchor = re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")
                lines.append(f"- [{h}](chapters/{m.number:02d}-{m.slug}.md#{anchor})")
            lines.append("")

    lines.extend(["", "## Code examples", ""])
    for m in metas:
        if m.code_files:
            lines.append(f"### Chapter {m.number}")
            for cf in m.code_files:
                lines.append(f"- [`code/{cf}`](code/{cf})")
            lines.append("")

    lines.extend(["", "## Figures by chapter", ""])
    for m in metas:
        if m.figures:
            lines.append(f"### Chapter {m.number}")
            for f in m.figures:
                lines.append(f"- Figure {f.number}: [{f.caption}]({f.asset_path})")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"PDF not found: {PDF}")

    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for stale in CODE_DIR.glob("*.py"):
        stale.unlink()

    reader = PdfReader(str(PDF))
    metas: list[ChapterMeta] = []
    summaries: dict[int, str] = {}

    print(f"Extracting from {PDF.name} ({len(reader.pages)} pages)...")

    for num, slug, title, start, end, part in CHAPTERS:
        print(f"  Chapter {num:02d}: pages {start}-{end}...")
        chapter = ChapterMeta(num, slug, title, start, end, part)
        chapter.figures = extract_figures(chapter, reader)
        md = build_chapter_markdown(chapter, reader)
        out_path = CHAPTERS_DIR / f"{num:02d}-{slug}.md"
        out_path.write_text(md, encoding="utf-8")
        summaries[num] = extract_summary_section(md)
        metas.append(chapter)
        print(f"    -> {len(chapter.figures)} figures, {len(chapter.code_files)} code files")

    kb_map = build_kb_map(metas, summaries)
    (KB / "KB-MAP.md").write_text(kb_map, encoding="utf-8")

    meta = {
        "source_pdf": str(PDF.relative_to(ROOT)),
        "chapters": [
            {
                "number": m.number,
                "slug": m.slug,
                "title": m.title,
                "pages": [m.start_page, m.end_page],
                "figures": len(m.figures),
                "code_files": m.code_files,
            }
            for m in metas
        ],
    }
    META_FILE.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\nDone. Chapters: {CHAPTERS_DIR}, KB map: {KB / 'KB-MAP.md'}")


if __name__ == "__main__":
    main()
