"""Lightweight content planning for RAS report packages.

The planner gives the host skill a clear target without turning report creation
into a questionnaire.  It infers a sensible default from the request and lets
callers override depth, research mode, or page target when they need to.
"""

from __future__ import annotations

import re
from typing import Any, Iterable


DEPTH_PROFILES: dict[str, dict[str, Any]] = {
    "quick": {
        "display_name": "Quick",
        "description": "A focused readout for a fast decision or status update.",
        "target_pages": 3,
        "page_range": [2, 4],
        "target_words": 1400,
        "word_range": [900, 2000],
        "target_slides": 5,
        "base_section_words": 350,
    },
    "standard": {
        "display_name": "Standard",
        "description": "A balanced report with enough context, evidence, and action.",
        "target_pages": 7,
        "page_range": [5, 9],
        "target_words": 3200,
        "word_range": [2200, 4500],
        "target_slides": 8,
        "base_section_words": 700,
    },
    "deep": {
        "display_name": "Deep",
        "description": "A long-form analysis with fuller context, comparisons, and implications.",
        "target_pages": 15,
        "page_range": [12, 25],
        "target_words": 7500,
        "word_range": [5500, 10000],
        "target_slides": 14,
        "base_section_words": 1100,
    },
}

DEPTHS = tuple(DEPTH_PROFILES)
RESEARCH_MODES = ("none", "provided", "web")

_DEEP_SIGNALS = (
    "deep",
    "detailed",
    "comprehensive",
    "long-form",
    "long form",
    "full analysis",
    "thorough",
    "extended",
    "in depth",
    "in-depth",
)
_QUICK_SIGNALS = (
    "concise",
    "one-page",
    "one page",
    "short",
    "quick",
    "brief summary",
)
_WEB_RESEARCH_SIGNALS = (
    "web search",
    "search online",
    "look up",
    "on the internet",
    "from the internet",
    "external research",
    "browse for",
    "latest data",
    "latest information",
    "verify against current",
)


def infer_depth(request: str) -> str:
    """Infer a content depth from ordinary language in a request."""

    text = re.sub(r"\s+", " ", (request or "").strip().lower())
    if any(signal in text for signal in _DEEP_SIGNALS):
        return "deep"
    page_match = re.search(r"\b(\d{1,3})\s*pages?\b", text)
    if page_match and int(page_match.group(1)) >= 10:
        return "deep"
    if any(signal in text for signal in _QUICK_SIGNALS):
        return "quick"
    return "standard"


def resolve_depth(request: str, requested: str | None = None) -> tuple[str, str]:
    """Return ``(depth, source)`` where source is explicit or inferred."""

    if requested:
        value = str(requested).strip().lower()
        if value not in DEPTH_PROFILES:
            raise ValueError(f"Unsupported depth {requested!r}; choose one of: {', '.join(DEPTHS)}")
        return value, "explicit"
    return infer_depth(request), "inferred"


def resolve_research_mode(requested: str | None = None, request: str | None = None) -> tuple[str, str]:
    """Return ``(mode, source)`` for the optional research phase.

    ``provided`` is the low-friction default: the host can work from material
    the user supplied, while external research remains unauthorized until the
    user explicitly selects ``web``.
    """

    if requested:
        value = str(requested).strip().lower()
        if value not in RESEARCH_MODES:
            raise ValueError(f"Unsupported research mode {requested!r}; choose one of: {', '.join(RESEARCH_MODES)}")
        return value, "explicit"
    text = re.sub(r"\s+", " ", (request or "").strip().lower())
    if any(signal in text for signal in _WEB_RESEARCH_SIGNALS):
        return "web", "inferred"
    return "provided", "default"


def _section_weight(block_id: str, role: str) -> float:
    key = f"{block_id} {role}".lower()
    if "summary" in key or "overview" in key:
        return 0.65
    if "recommend" in key or "conclusion" in key or "action" in key:
        return 0.8
    if "method" in key or "scope" in key:
        return 0.55
    return 1.0


def _layout_budget(words: int) -> str:
    if words <= 500:
        return "half-page"
    if words >= 850:
        return "full-page"
    return "standard"


def build_content_plan(
    depth: str,
    blueprints: Iterable[tuple[str, str, str, str]],
    *,
    target_pages: int | None = None,
    source: str = "inferred",
) -> dict[str, Any]:
    """Build a renderer-independent plan for the report's content blocks."""

    if depth not in DEPTH_PROFILES:
        raise ValueError(f"Unsupported depth {depth!r}; choose one of: {', '.join(DEPTHS)}")
    profile = DEPTH_PROFILES[depth]
    if target_pages is not None and (int(target_pages) < 1 or int(target_pages) > 100):
        raise ValueError("Page target must be between 1 and 100")

    page_target = int(target_pages) if target_pages is not None else int(profile["target_pages"])
    page_range = list(profile["page_range"])
    target_words = int(profile["target_words"])
    word_range = list(profile["word_range"])
    target_slides = int(profile["target_slides"])
    if target_pages is not None:
        page_range = [max(1, page_target - 2), page_target + 3]
        scale = page_target / max(1, int(profile["target_pages"]))
        target_words = max(500, int(round(target_words * scale / 100) * 100))
        word_range = [max(300, int(round(value * scale / 100) * 100)) for value in word_range]
        target_slides = max(3, int(round(target_slides * scale)))

    items = list(blueprints)
    weights = [_section_weight(block_id, role) for block_id, role, _, _ in items]
    weight_total = sum(weights) or 1.0
    sections: list[dict[str, Any]] = []
    for (block_id, role, title, _), weight in zip(items, weights):
        words = max(180, int(round(target_words * weight / weight_total / 50) * 50))
        sections.append({
            "id": block_id,
            "role": role,
            "title": title,
            "target_words": words,
            "layout_budget": _layout_budget(words),
        })

    return {
        "profile": depth,
        "display_name": profile["display_name"],
        "description": profile["description"],
        "source": source,
        "target_pages": page_target,
        "page_range": page_range,
        "target_words": target_words,
        "word_range": word_range,
        "target_slides": target_slides,
        "sections": sections,
        "instructions": [
            "Use the section targets as a guide; do not pad unsupported material.",
            "Expand with context, evidence, comparisons, implications, and limitations when the selected profile requires more depth.",
            "Keep unsupported claims and evidence gaps explicit.",
        ],
    }


def build_research_plan(mode: str, *, source: str = "default") -> dict[str, Any]:
    """Create the manifest receipt for the optional research phase."""

    if mode not in RESEARCH_MODES:
        raise ValueError(f"Unsupported research mode {mode!r}; choose one of: {', '.join(RESEARCH_MODES)}")
    if mode == "web":
        notes = "External research is authorized; record every external source before making claims."
    elif mode == "provided":
        notes = "Use supplied source material as the evidence base; external research is not required."
    else:
        notes = "Do not perform a research phase; use only facts explicitly present in the report package."
    return {
        "mode": mode,
        "source": source,
        "performed": False,
        "authorized": mode == "web",
        "notes": notes,
    }


__all__ = [
    "DEPTH_PROFILES",
    "DEPTHS",
    "RESEARCH_MODES",
    "build_content_plan",
    "build_research_plan",
    "infer_depth",
    "resolve_depth",
    "resolve_research_mode",
]
