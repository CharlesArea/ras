"""Original RAS diagram renderer.

The renderer intentionally uses a small semantic grammar instead of importing
another diagram skill. The same node/edge specification produces an SVG and a
PNG that can be embedded in PDF and DOCX respectively.
"""

from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .design import pillow_font_path


FAMILIES = {"flow", "hierarchy", "timeline", "lifecycle", "architecture", "relationship", "comparison", "matrix", "process", "cause-effect"}


def render_diagram(spec: dict[str, Any], output_dir: str | Path, stem: str, design: dict[str, Any] | None = None) -> dict[str, str]:
    family = str(spec.get("family", spec.get("kind", "flow"))).lower()
    family = family.replace("_", "-")
    if family not in FAMILIES:
        raise ValueError(f"Unsupported RAS diagram family: {family}")
    nodes = spec.get("nodes", []) or []
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("RAS diagrams require a non-empty nodes list")
    normalized = [{"id": str(node.get("id", index)), "label": str(node.get("label", node.get("title", ""))), "group": str(node.get("group", "")), "level": int(node.get("level", 0) or 0)} for index, node in enumerate(nodes) if isinstance(node, dict)]
    edges = [edge for edge in spec.get("edges", []) or [] if isinstance(edge, dict)]
    positions = _layout(normalized, family)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    png = out / f"{stem}.png"
    svg = out / f"{stem}.svg"
    width, height = _canvas_size(family, positions)
    design = design or {}
    palette = design.get("palette", {}) or {}
    diagram = design.get("diagram", {}) or {}
    paper = str(palette.get("paper", "#FFFFFF"))
    surface = str(palette.get("surface", "#F8FAFC"))
    ink = str(palette.get("ink", "#17202A"))
    connector = str(diagram.get("connector", palette.get("muted", "#667085")))
    fill = str(spec.get("node_fill", diagram.get("node_fill", palette.get("accent_soft", "#EEF4FF"))))
    stroke = str(spec.get("node_stroke", diagram.get("node_stroke", palette.get("accent", "#175CD3"))))
    radius = max(2, int(diagram.get("node_radius", 10)))
    image = Image.new("RGB", (width, height), paper)
    draw = ImageDraw.Draw(image)
    font = _load_font(pillow_font_path("body"), 20)
    node_w, node_h = 220, 70
    draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=18, fill=surface, outline=str(palette.get("rule", "#D7DEE5")), width=2)
    draw.rectangle((18, 18, width - 18, 28), fill=str(palette.get("accent", stroke)))
    for edge in edges:
        start = positions.get(str(edge.get("from", edge.get("source", ""))))
        end = positions.get(str(edge.get("to", edge.get("target", ""))))
        if not start or not end:
            continue
        _draw_orthogonal(draw, start, end, node_w, node_h, connector)
    for index, node in enumerate(normalized):
        x, y = positions[node["id"]]
        draw.rounded_rectangle((x, y, x + node_w, y + node_h), radius=radius, fill=fill, outline=stroke, width=3)
        _centered_text(draw, node["label"], x + node_w / 2, y + node_h / 2, font, ink)
    image.save(png, format="PNG", optimize=True)
    svg.write_text(_diagram_svg(spec, normalized, edges, positions, width, height, node_w, node_h, design), encoding="utf-8", newline="\n")
    alt = str(spec.get("alt_text", "")) or f"{family.title()} diagram with " + ", ".join(node["label"] for node in normalized)
    return {"png": str(png), "svg": str(svg), "alt_text": alt}


def _layout(nodes: list[dict[str, Any]], family: str) -> dict[str, tuple[int, int]]:
    positions: dict[str, tuple[int, int]] = {}
    if family in {"hierarchy", "architecture", "cause-effect"}:
        grouped: dict[int, list[dict[str, Any]]] = {}
        for node in nodes:
            grouped.setdefault(node["level"], []).append(node)
        for level, group in sorted(grouped.items()):
            offset = max(40, 160 - len(group) * 30)
            for index, node in enumerate(group):
                positions[node["id"]] = (offset + index * 270, 50 + level * 130)
    elif family == "matrix":
        for index, node in enumerate(nodes):
            positions[node["id"]] = (50 + (index % 3) * 270, 50 + (index // 3) * 130)
    else:
        for index, node in enumerate(nodes):
            positions[node["id"]] = (50 + (index % 4) * 270, 100 + (index // 4) * 150)
    return positions


def _canvas_size(family: str, positions: dict[str, tuple[int, int]]) -> tuple[int, int]:
    if not positions:
        return 800, 500
    max_x = max(x for x, _ in positions.values()) + 270
    max_y = max(y for _, y in positions.values()) + 120
    return max(800, max_x), max(500, max_y)


def _draw_orthogonal(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], node_w: int, node_h: int, color: str) -> None:
    points = _connector_points(start, end, node_w, node_h)
    draw.line(points, fill=color, width=3, joint="curve")
    previous, tip = points[-2], points[-1]
    angle = math.atan2(tip[1] - previous[1], tip[0] - previous[0])
    wing = 11
    arrow = [(tip[0], tip[1]), (tip[0] - wing * math.cos(angle - 0.45), tip[1] - wing * math.sin(angle - 0.45)), (tip[0] - wing * math.cos(angle + 0.45), tip[1] - wing * math.sin(angle + 0.45))]
    draw.polygon(arrow, fill=color)


def _connector_points(start: tuple[int, int], end: tuple[int, int], node_w: int, node_h: int) -> list[tuple[float, float]]:
    start_center = (start[0] + node_w / 2, start[1] + node_h / 2)
    end_center = (end[0] + node_w / 2, end[1] + node_h / 2)
    dx, dy = end_center[0] - start_center[0], end_center[1] - start_center[1]
    if abs(dx) >= abs(dy):
        sy, ey = start_center[1], end_center[1]
        sx = start[0] + node_w if dx >= 0 else start[0]
        ex = end[0] if dx >= 0 else end[0] + node_w
        mid_x = (sx + ex) / 2
        return [(sx, sy), (mid_x, sy), (mid_x, ey), (ex, ey)]
    sx, ex = start_center[0], end_center[0]
    sy = start[1] + node_h if dy >= 0 else start[1]
    ey = end[1] if dy >= 0 else end[1] + node_h
    mid_y = (sy + ey) / 2
    return [(sx, sy), (sx, mid_y), (ex, mid_y), (ex, ey)]


def _centered_text(draw: ImageDraw.ImageDraw, value: str, x: float, y: float, font: ImageFont.ImageFont, fill: str) -> None:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > 25 and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    heights = len(lines) * 16
    for index, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=font)
        draw.text((x - (box[2] - box[0]) / 2, y - heights / 2 + index * 16), line, fill=fill, font=font)


def _diagram_svg(spec: dict[str, Any], nodes: list[dict[str, Any]], edges: list[dict[str, Any]], positions: dict[str, tuple[int, int]], width: int, height: int, node_w: int, node_h: int, design: dict[str, Any] | None = None) -> str:
    design = design or {}
    palette = design.get("palette", {}) or {}
    diagram = design.get("diagram", {}) or {}
    paper = html.escape(str(palette.get("paper", "#FFFFFF")))
    surface = html.escape(str(palette.get("surface", "#F8FAFC")))
    ink = html.escape(str(palette.get("ink", "#17202A")))
    accent = html.escape(str(palette.get("accent", "#175CD3")))
    connector = html.escape(str(diagram.get("connector", palette.get("muted", "#667085"))))
    fill = html.escape(str(spec.get("node_fill", diagram.get("node_fill", palette.get("accent_soft", "#EEF4FF")))))
    stroke = html.escape(str(spec.get("node_stroke", diagram.get("node_stroke", palette.get("accent", "#175CD3")))))
    radius = max(2, int(diagram.get("node_radius", 10)))
    font_family = html.escape(str((design.get("typography", {}) or {}).get("body", "sans-serif")))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', f'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{connector}"/></marker></defs>', f'<rect width="100%" height="100%" fill="{paper}"/>', f'<rect x="18" y="18" width="{width - 36}" height="{height - 36}" rx="18" fill="{surface}" stroke="{html.escape(str(palette.get("rule", "#D7DEE5")))}" stroke-width="2"/>', f'<rect x="18" y="18" width="{width - 36}" height="10" fill="{accent}"/>']
    for edge in edges:
        start = positions.get(str(edge.get("from", edge.get("source", ""))))
        end = positions.get(str(edge.get("to", edge.get("target", ""))))
        if not start or not end:
            continue
        points = _connector_points(start, end, node_w, node_h)
        parts.append(f'<path d="M {points[0][0]} {points[0][1]} L {points[1][0]} {points[1][1]} L {points[2][0]} {points[2][1]} L {points[3][0]} {points[3][1]}" fill="none" stroke="{connector}" stroke-width="3" marker-end="url(#arrow)"/>')
    for node in nodes:
        x, y = positions[node["id"]]
        parts.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        parts.append(f'<text x="{x + node_w / 2}" y="{y + node_h / 2 + 6}" text-anchor="middle" font-family="{font_family}" font-size="18" fill="{ink}">{html.escape(node["label"])}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def _load_font(path: str | None, size: int) -> ImageFont.ImageFont:
    if path:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()
