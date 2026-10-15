"""Path and content safety helpers used by the import and rendering paths."""

from __future__ import annotations

import re
from pathlib import Path


class UnsafePathError(ValueError):
    """Raised when a user-controlled path escapes its report workspace."""


def ensure_within(root: str | Path, candidate: str | Path, *, allow_missing: bool = True) -> Path:
    base = Path(root).resolve()
    path = Path(candidate)
    resolved = (base / path).resolve() if not path.is_absolute() else path.resolve()
    if not allow_missing and not resolved.exists():
        raise UnsafePathError(f"Path does not exist: {candidate}")
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise UnsafePathError(f"Path escapes report workspace: {candidate}") from exc
    return resolved


def safe_asset_path(root: str | Path, relative: str, *, suffixes: set[str] | None = None) -> Path:
    path = ensure_within(root, relative)
    if suffixes and path.suffix.lower() not in suffixes:
        raise UnsafePathError(f"Unsupported asset type: {path.suffix}")
    return path


def sanitize_svg(svg_text: str) -> str:
    """Remove active SVG constructs before an SVG is placed in a report."""

    lowered = svg_text.lower()
    if any(token in lowered for token in ("<script", "javascript:", "onload=", "onclick=", "<foreignobject")):
        raise ValueError("SVG contains active or embedded content")
    return re.sub(r"<!DOCTYPE[^>]*>|<!ENTITY[^>]*>", "", svg_text, flags=re.IGNORECASE | re.DOTALL)


def sanitize_html_fragment(html: str) -> str:
    if re.search(r"<\s*(script|iframe|object|embed|form)\b", html, flags=re.IGNORECASE) or re.search(r"\bon[a-z]+\s*=", html, flags=re.IGNORECASE):
        raise ValueError("HTML contains active content")
    return html


def unresolved_placeholders(text: str) -> list[str]:
    patterns = [r"\{\{[^}]+\}\}", r"\[\[\s*(?:TODO|TBD|FILL|REPLACE)[^]]*\]\]", r"\b(?:TODO|TBD|FIXME)\b"]
    found: list[str] = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return sorted(set(found))
