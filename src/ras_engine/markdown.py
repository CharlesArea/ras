"""Minimal Markdown reader for report blocks.

RAS keeps block Markdown deliberately small so the same model can render to
DOCX and PDF without depending on a browser or a full Markdown engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html import escape as html_escape
from typing import Any


@dataclass
class Element:
    kind: str
    text: str = ""
    level: int = 0
    items: list[str] | None = None
    rows: list[list[str]] | None = None
    language: str = ""


@dataclass
class InlineSpan:
    """A small renderer-neutral subset of Markdown inline formatting."""

    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False


_INLINE_TOKEN = re.compile(
    r"`([^`\n]+)`|\*\*([^*\n]+?)\*\*|__([^_\n]+?)__|(?<!\w)\*([^*\n]+?)\*(?!\w)|(?<!\w)_([^_\n]+?)_(?!\w)"
)


def parse_inline(text: str) -> list[InlineSpan]:
    """Parse the inline Markdown RAS supports without changing plain text."""

    spans: list[InlineSpan] = []
    cursor = 0
    for match in _INLINE_TOKEN.finditer(str(text)):
        if match.start() > cursor:
            spans.append(InlineSpan(str(text)[cursor:match.start()]))
        if match.group(1) is not None:
            spans.append(InlineSpan(match.group(1), code=True))
        elif match.group(2) is not None:
            spans.append(InlineSpan(match.group(2), bold=True))
        elif match.group(3) is not None:
            spans.append(InlineSpan(match.group(3), bold=True))
        elif match.group(4) is not None:
            spans.append(InlineSpan(match.group(4), italic=True))
        else:
            spans.append(InlineSpan(match.group(5), italic=True))
        cursor = match.end()
    if cursor < len(str(text)):
        spans.append(InlineSpan(str(text)[cursor:]))
    return spans or [InlineSpan(str(text))]


def inline_markup(text: str) -> str:
    """Convert supported inline Markdown to safe ReportLab paragraph markup."""

    output: list[str] = []
    for span in parse_inline(text):
        value = html_escape(span.text, quote=False).replace("\n", "<br/>")
        if span.code:
            value = f'<font name="Courier">{value}</font>'
        elif span.bold:
            value = f"<b>{value}</b>"
        elif span.italic:
            value = f"<i>{value}</i>"
        output.append(value)
    return "".join(output)


def parse_markdown(text: str) -> list[Element]:
    lines = text.replace("\r\n", "\n").split("\n")
    elements: list[Element] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    code: list[str] = []
    code_language = ""
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            elements.append(Element("paragraph", " ".join(item.strip() for item in paragraph).strip()))
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullets
        if bullets:
            elements.append(Element("bullet_list", items=list(bullets)))
            bullets = []

    def flush_code() -> None:
        nonlocal code
        if code:
            elements.append(Element("code", "\n".join(code), language=code_language))
            code = []

    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            if in_code:
                in_code = False
                flush_code()
                code_language = ""
            else:
                flush_paragraph()
                flush_bullets()
                in_code = True
                code_language = line[3:].strip()
            index += 1
            continue
        if in_code:
            code.append(line)
            index += 1
            continue
        if not line.strip():
            flush_paragraph()
            flush_bullets()
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            flush_paragraph()
            flush_bullets()
            elements.append(Element("heading", heading.group(2).strip(), level=len(heading.group(1))))
            index += 1
            continue
        if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line):
            flush_paragraph()
            bullets.append(re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", line).strip())
            index += 1
            continue
        if line.lstrip().startswith(">"):
            flush_paragraph()
            flush_bullets()
            elements.append(Element("callout", line.lstrip()[1:].strip()))
            index += 1
            continue
        if _looks_like_table(line) and index + 1 < len(lines) and _is_table_separator(lines[index + 1]):
            flush_paragraph()
            flush_bullets()
            rows = [_table_row(line)]
            index += 2
            while index < len(lines) and _looks_like_table(lines[index]) and lines[index].strip():
                rows.append(_table_row(lines[index]))
                index += 1
            elements.append(Element("table", rows=rows))
            continue
        paragraph.append(line)
        index += 1
    flush_paragraph()
    flush_bullets()
    flush_code()
    return elements


def plain_text(elements: list[Element]) -> str:
    chunks: list[str] = []
    for element in elements:
        if element.kind in {"paragraph", "heading", "callout", "code"}:
            chunks.append(element.text)
        elif element.kind == "bullet_list":
            chunks.extend(element.items or [])
        elif element.kind == "table":
            chunks.extend(" | ".join(row) for row in element.rows or [])
    return "\n".join(chunks)


def _looks_like_table(line: str) -> bool:
    return line.count("|") >= 2


def _is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]
