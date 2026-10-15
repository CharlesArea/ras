"""Semantic report components shared by DOCX, PDF, and visual renderers.

The component layer intentionally stays small. It gives renderers the same
meaningful design decision without forcing them to share their layout APIs.
"""

from __future__ import annotations

from typing import Any


def component_kind(block: Any) -> str:
    spec = getattr(block, "spec", block)
    presentation = getattr(spec, "presentation", {}) or {}
    requested = str(presentation.get("component", "")).lower().replace("-", "_")
    requested_map = {
        "executive_summary": "summary",
        "key_finding": "finding",
        "insight": "finding",
        "recommendation": "recommendation",
        "action_strip": "recommendation",
        "kpi": "visual",
        "source_register": "source",
    }
    if requested in requested_map:
        return requested_map[requested]
    block_type = str(getattr(spec, "type", "narrative")).lower().replace("-", "_")
    if block_type in {"executive_summary", "summary", "abstract", "overview", "metric_panel"}:
        return "summary"
    if block_type in {"finding", "analysis", "insight", "observation", "risk", "issue"}:
        return "finding"
    if block_type in {"recommendation", "decision", "action", "next_step", "proposal"}:
        return "recommendation"
    if block_type in {"chart", "data_chart", "diagram", "ras_diagram", "timeline", "architecture", "table_visual"}:
        return "visual"
    if block_type in {"source", "sources", "bibliography"}:
        return "source"
    return "narrative"


def component_variant(block: Any, design: dict[str, Any]) -> str:
    spec = getattr(block, "spec", block)
    visual = getattr(spec, "visual", {}) or {}
    presentation = getattr(spec, "presentation", {}) or {}
    explicit = presentation.get("variant") or presentation.get("component") or visual.get("component") or visual.get("variant")
    if explicit:
        return str(explicit)
    kind = component_kind(block)
    return str((design.get("components", {}) or {}).get(kind, "default"))


def semantic_label(kind: str) -> str:
    return {
        "summary": "Executive summary",
        "finding": "Key finding",
        "recommendation": "Recommended action",
        "visual": "Evidence visual",
        "source": "Sources",
        "narrative": "",
    }.get(kind, "")


def component_colors(design: dict[str, Any], kind: str) -> tuple[str, str, str]:
    palette = design.get("palette", {}) or {}
    accent = str(palette.get("accent", "#2563EB"))
    if kind == "recommendation":
        accent = str(palette.get("positive", accent))
    elif kind == "finding":
        accent = str(palette.get("accent", accent))
    elif kind == "source":
        accent = str(palette.get("muted", accent))
    return accent, str(palette.get("accent_soft", palette.get("surface", "#F5F7FA"))), str(palette.get("ink", "#17202A"))


__all__ = ["component_colors", "component_kind", "component_variant", "semantic_label"]
