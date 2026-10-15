"""Compile a theme, brand overlay, and report modifiers into design tokens."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

from .themes import theme_pack


def resolve_design(theme_id: str, brand: dict[str, Any] | None = None, *, custom_brand: bool = False, density: str = "standard", tone: str = "professional", emphasis: str = "text-balanced") -> dict[str, Any]:
    design = theme_pack(theme_id)
    brand = brand or {}
    if custom_brand:
        _apply_brand_overlay(design, brand)
    _apply_modifiers(design, density, tone, emphasis)
    design["theme_id"] = theme_id if theme_id in {"minimal", "editorial", "data-forward", "institutional", "technical", "narrative"} else "minimal"
    design["density"] = density
    design["tone"] = tone
    design["emphasis"] = emphasis
    design["resolved_brand"] = str(brand.get("name", "RAS Neutral")) if custom_brand else "RAS Neutral"
    design["receipt"] = {
        "theme": design["theme_id"],
        "brand": design["resolved_brand"],
        "density": density,
        "tone": tone,
        "emphasis": emphasis,
        "custom_brand": custom_brand,
    }
    return design


def project_design(project: Any) -> dict[str, Any]:
    custom_brand = bool(project.raw_manifest.get("brand_file")) or (project.root / ".ras" / "brand.yaml").exists()
    request = project.raw_manifest.get("design", {}) or {}
    theme_id = str(request.get("theme", project.style.visual_style))
    density = str(request.get("density", project.style.density))
    tone = str(request.get("tone", project.style.tone))
    emphasis = str(request.get("emphasis", project.style.emphasis))
    brand = getattr(project, "brand_overrides", None) or project.brand
    return resolve_design(theme_id, brand, custom_brand=custom_brand, density=density, tone=tone, emphasis=emphasis)


def design_signature(design: dict[str, Any]) -> str:
    """Return a stable signature for visual-regression receipts."""

    payload = {
        "theme_id": design.get("theme_id"),
        "palette": design.get("palette", {}),
        "typography": design.get("typography", {}),
        "page": design.get("page", {}),
        "components": design.get("components", {}),
        "chart": design.get("chart", {}),
        "diagram": design.get("diagram", {}),
        "ornament": design.get("ornament", {}),
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:20]


def pillow_font_path(kind: str = "body") -> str | None:
    """Find a practical local font for raster visuals without requiring fonts."""

    candidates = {
        "body": ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
        "heading": ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "serif": ["C:/Windows/Fonts/times.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "mono": ["C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
    }
    for candidate in candidates.get(kind, candidates["body"]):
        if Path(candidate).exists():
            return candidate
    return None


def _apply_brand_overlay(design: dict[str, Any], brand: dict[str, Any]) -> None:
    if isinstance(brand.get("colors"), dict):
        design["palette"].update({str(key): str(value) for key, value in brand["colors"].items()})
    if isinstance(brand.get("fonts"), dict):
        font_map = {"heading": "heading", "body": "body", "mono": "mono", "cjk_fallback": "cjk"}
        for source, target in font_map.items():
            if brand["fonts"].get(source):
                design["typography"][target] = str(brand["fonts"][source])
    for section in ("spacing", "page", "components", "chart", "diagram", "identity", "logo", "table"):
        if isinstance(brand.get(section), dict):
            design.setdefault(section, {}).update(deepcopy(brand[section]))
    spacing = brand.get("spacing", {}) or {}
    if spacing.get("page_margin") is not None:
        margin = float(spacing["page_margin"])
        design.setdefault("page", {})["margins"] = {side: margin for side in ("top", "right", "bottom", "left")}
    if brand.get("name"):
        design["brand_name"] = str(brand["name"])


def _apply_modifiers(design: dict[str, Any], density: str, tone: str, emphasis: str) -> None:
    page = design.setdefault("page", {})
    if density == "concise":
        page["compactness"] = 1.12
        page["margins"] = {key: max(0.42, float(value) - 0.04) for key, value in page.get("margins", {}).items()}
    elif density == "deep":
        page["compactness"] = 0.92
        page["margins"] = {key: float(value) + 0.03 for key, value in page.get("margins", {}).items()}
    else:
        page["compactness"] = 1.0
    if tone == "executive":
        design.setdefault("components", {})["summary"] = "executive-deck"
    if tone == "academic":
        design.setdefault("components", {})["source_register"] = "formal-register"
    if emphasis == "evidence-first":
        design.setdefault("components", {})["finding"] = "evidence-callout"
    if emphasis == "visual-first":
        design.setdefault("components", {})["summary"] = "visual-deck"
