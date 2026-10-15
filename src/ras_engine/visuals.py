"""Prepare user assets, charts, and RAS diagrams for rendering."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .charts import render_chart
from .diagrams import render_diagram
from .security import ensure_within, safe_asset_path, sanitize_svg


def prepare_visuals(project: Any, build_dir: str | Path) -> dict[str, dict[str, str]]:
    output = Path(build_dir) / "visuals"
    output.mkdir(parents=True, exist_ok=True)
    prepared: dict[str, dict[str, str]] = {}
    design = project.design
    for block in project.blocks:
        spec = dict(block.spec.visual or {})
        block_type = block.spec.type.lower().replace("-", "_")
        kind = str(spec.get("kind", "")).lower().replace("-", "_")
        stem = _safe_stem(block.spec.id)
        if block_type in {"chart", "data_chart"} or kind in {"chart", "bar", "line", "pie"}:
            chart_spec = dict(spec)
            if kind in {"bar", "line", "pie"}:
                chart_spec.setdefault("kind", kind)
            prepared[block.spec.id] = render_chart(chart_spec, output, stem, design)
        elif block_type in {"diagram", "ras_diagram", "timeline", "architecture"} or kind in {"diagram", "flow", "hierarchy", "timeline", "lifecycle", "architecture", "relationship", "comparison", "matrix", "process", "cause_effect"}:
            diagram_spec = dict(spec)
            if kind not in {"diagram", ""}:
                diagram_spec.setdefault("family", kind)
            prepared[block.spec.id] = render_diagram(diagram_spec, output, stem, design)
        elif spec.get("asset") or spec.get("path"):
            prepared[block.spec.id] = _prepare_asset(project.root, output, str(spec.get("asset", spec.get("path"))), stem)
    return prepared


def _prepare_asset(root: Path, output: Path, relative: str, stem: str) -> dict[str, str]:
    source = safe_asset_path(root, relative, suffixes={".png", ".jpg", ".jpeg", ".webp", ".svg"})
    if not source.exists():
        raise FileNotFoundError(f"Visual asset does not exist: {relative}")
    destination = output / f"{stem}{source.suffix.lower()}"
    if source.suffix.lower() == ".svg":
        destination.write_text(sanitize_svg(source.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        return {"svg": str(destination), "png": str(destination), "alt_text": "User-supplied SVG asset"}
    shutil.copy2(source, destination)
    return {"png": str(destination), "alt_text": "User-supplied visual asset"}


def _safe_stem(value: str) -> str:
    return "".join(char if char.isalnum() or char in "-_" else "-" for char in value).strip("-") or "visual"
