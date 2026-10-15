"""Automatic archetype and style routing."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from .models import (
    ARCHETYPES,
    DENSITIES,
    EMPHASES,
    EVIDENCE_LEVELS,
    GEOMETRIES,
    TONES,
    VISUAL_STYLES,
    StyleDecision,
)


KEYWORDS: dict[str, tuple[str, ...]] = {
    "decision-memo": ("decide", "decision", "options", "recommend", "trade-off", "tradeoff", "approve"),
    "research-synthesis": ("research", "literature", "sources", "evidence", "synthesis", "studies"),
    "analytical-deep-dive": ("analyze", "analysis", "deep dive", "drivers", "why", "model"),
    "comparative-evaluation": ("compare", "comparison", "benchmark", "alternatives", "versus", " vs "),
    "proposal-business-case": ("proposal", "business case", "investment", "funding", "roi", "pitch"),
    "strategy-roadmap": ("strategy", "roadmap", "milestones", "initiative", "north star"),
    "status-progress": ("status", "progress", "completed", "blocker", "next steps", "weekly update"),
    "performance-kpi": ("kpi", "metric", "metrics", "performance", "dashboard", "trend"),
    "audit-assessment": ("audit", "assessment", "control", "finding", "remediation"),
    "compliance-risk": ("compliance", "risk", "obligation", "regulation", "control gap"),
    "technical-architecture": ("technical", "architecture", "system design", "interface", "api", "deployment"),
    "incident-postmortem": ("incident", "outage", "postmortem", "rollback", "timeline", "impact"),
    "investigation-root-cause": ("investigate", "investigation", "root cause", "hypothesis", "forensic"),
    "policy-sop": ("policy", "sop", "procedure", "handbook", "standard operating", "rules"),
    "case-study": ("case study", "customer story", "intervention", "lessons learned", "narrative"),
    "executive-brief": ("executive", "brief", "leadership", "senior management", "summary", "overview"),
}


def normalize_request(request: str, source_names: list[str] | None = None) -> str:
    text = (request or "").strip()
    if source_names:
        text += "\nSource material: " + ", ".join(source_names)
    return re.sub(r"\s+", " ", text).strip()


def route_request(request: str, overrides: dict[str, Any] | None = None) -> StyleDecision:
    overrides = overrides or {}
    text = normalize_request(request).lower()
    scores: Counter[str] = Counter()
    signals: list[str] = []
    for archetype, terms in KEYWORDS.items():
        matches = [term for term in terms if term in text]
        if matches:
            scores[archetype] += len(matches)
            signals.extend(f"{archetype}:{term}" for term in matches[:2])
    archetype = scores.most_common(1)[0][0] if scores else "executive-brief"
    rationale = f"Matched the dominant purpose to {archetype}." if scores else "No strong purpose signal; selected the simplest general-purpose brief."

    decision = StyleDecision(
        archetype=archetype,
        visual_style="data-forward" if any(word in text for word in ("kpi", "metric", "chart", "data", "trend")) else "minimal",
        density="deep" if any(word in text for word in ("deep", "comprehensive", "detailed", "full")) else "concise" if any(word in text for word in ("concise", "one-page", "short")) else "standard",
        tone="executive" if any(word in text for word in ("executive", "leadership", "board", "senior management")) else "academic" if any(word in text for word in ("academic", "literature", "citation")) else "professional",
        emphasis="visual-first" if any(word in text for word in ("visual", "dashboard", "show me", "chart")) else "evidence-first" if any(word in text for word in ("evidence", "auditable", "audit")) else "text-balanced",
        evidence_level="auditable" if any(word in text for word in ("audit", "compliance", "regulated", "auditable")) else "sourced" if any(word in text for word in ("source", "research", "citation", "evidence")) else "informational",
        page_geometry="landscape" if any(word in text for word in ("landscape", "wide", "dashboard", "comparison matrix")) else "portrait",
        rationale=rationale,
        signals=signals,
    )

    explicit = {
        "archetype": "archetype",
        "visual_style": "visual_style",
        "visual": "visual_style",
        "density": "density",
        "tone": "tone",
        "emphasis": "emphasis",
        "evidence_level": "evidence_level",
        "page_geometry": "page_geometry",
        "geometry": "page_geometry",
    }
    allowed = {
        "archetype": set(ARCHETYPES),
        "visual_style": set(VISUAL_STYLES),
        "density": set(DENSITIES),
        "tone": set(TONES),
        "emphasis": set(EMPHASES),
        "evidence_level": set(EVIDENCE_LEVELS),
        "page_geometry": set(GEOMETRIES),
    }
    for key, attr in explicit.items():
        if key not in overrides or overrides[key] in (None, ""):
            continue
        value = str(overrides[key])
        if value in allowed[attr]:
            setattr(decision, attr, value)
            decision.signals.append(f"explicit:{key}={value}")
        else:
            decision.fallback = f"Ignored unsupported {key}={value!r}; kept {getattr(decision, attr)!r}."
    if decision.fallback:
        decision.rationale += " " + decision.fallback
    return decision


def style_receipt(decision: StyleDecision) -> str:
    return (
        f"{decision.archetype}; {decision.visual_style} visuals; {decision.density} density; "
        f"{decision.tone} tone; {decision.emphasis}; {decision.evidence_level} evidence; "
        f"{decision.page_geometry} pages. {decision.rationale}"
    )
