"""Small dependency-light chart renderer used by both report formats."""

from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .design import pillow_font_path


class VisualError(ValueError):
    """Raised when a chart specification is incomplete or unsafe."""


def render_chart(spec: dict[str, Any], output_dir: str | Path, stem: str, design: dict[str, Any] | None = None) -> dict[str, str]:
    labels = [str(item) for item in spec.get("labels", []) or []]
    raw_values = spec.get("values", []) or []
    if isinstance(raw_values, dict):
        labels = [str(item) for item in raw_values]
        raw_values = list(raw_values.values())
    try:
        values = [float(item) for item in raw_values]
    except (TypeError, ValueError) as exc:
        raise VisualError("Chart values must be numeric") from exc
    if not values or not labels or len(values) != len(labels):
        raise VisualError("Charts require equally sized non-empty labels and values")
    kind = str(spec.get("kind", spec.get("chart_type", "bar"))).lower()
    if kind not in {"bar", "line", "pie"}:
        raise VisualError(f"Unsupported chart kind: {kind}")

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    png_path = target_dir / f"{stem}.png"
    svg_path = target_dir / f"{stem}.svg"
    design = design or {}
    palette_map = design.get("palette", {}) or {}
    chart_map = design.get("chart", {}) or {}
    width, height = 1400, 760
    paper = str(palette_map.get("paper", "#FFFFFF"))
    surface = str(palette_map.get("surface", "#F8FAFC"))
    ink = str(palette_map.get("ink", "#17202A"))
    muted = str(palette_map.get("muted", "#5D6B78"))
    rule = str(palette_map.get("rule", "#D7DEE5"))
    accent = str(palette_map.get("accent", "#2563EB"))
    image = Image.new("RGB", (width, height), paper)
    draw = ImageDraw.Draw(image)
    font = _load_font(pillow_font_path("body"), 20)
    title_font = _load_font(pillow_font_path("heading"), 30)
    title = str(spec.get("title", ""))
    draw.rounded_rectangle((24, 24, width - 24, height - 24), radius=18, fill=surface, outline=rule, width=2)
    draw.rectangle((24, 24, width - 24, 34), fill=accent)
    if title:
        draw.text((62, 56), title, fill=ink, font=title_font)
    left, top, right, bottom = 120, 135, width - 72, height - 112
    palette = [str(c) for c in spec.get("palette", chart_map.get("palette", ["#175CD3", "#7F56D9", "#039855", "#DC6803", "#D92D20"]))]
    grid = str(chart_map.get("grid_color", rule))
    line_width = max(2, int(float(chart_map.get("line_width", 3))))

    if kind == "pie":
        _draw_pie(draw, labels, values, (430, 410), 238, palette, font, muted)
    else:
        maximum = max(max(values), 0.0)
        minimum = min(min(values), 0.0)
        span = maximum - minimum or 1.0
        for step in range(6):
            value = minimum + span * step / 5
            y = bottom - (value - minimum) / span * (bottom - top)
            draw.line((left, y, right, y), fill=grid, width=1)
            draw.text((38, y - 10), _format_number(value), fill=muted, font=font)
        zero_y = bottom - (0 - minimum) / span * (bottom - top) if minimum < 0 < maximum else None
        if zero_y is not None:
            draw.line((left, zero_y, right, zero_y), fill=muted, width=2)
        if kind == "bar":
            slot = (right - left) / len(values)
            bar_width = max(12, slot * 0.58)
            for index, value in enumerate(values):
                x = left + slot * index + (slot - bar_width) / 2
                y_value = bottom - (value - minimum) / span * (bottom - top)
                y_zero = bottom - (0 - minimum) / span * (bottom - top)
                draw.rectangle((x, min(y_value, y_zero), x + bar_width, max(y_value, y_zero)), fill=palette[index % len(palette)])
                _label(draw, labels[index], x + bar_width / 2, bottom + 22, font, muted)
        else:
            points: list[tuple[float, float]] = []
            slot = (right - left) / max(1, len(values) - 1)
            for index, value in enumerate(values):
                x = left + slot * index
                y = bottom - (value - minimum) / span * (bottom - top)
                points.append((x, y))
                _label(draw, labels[index], x, bottom + 22, font, muted)
            if len(points) > 1:
                draw.line(points, fill=palette[0], width=line_width + 1)
            for x, y in points:
                draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=palette[0], outline=surface, width=3)
        draw.line((left, top, left, bottom), fill=muted, width=2)
        draw.line((left, bottom, right, bottom), fill=muted, width=2)
    image.save(png_path, format="PNG", optimize=True)
    svg_path.write_text(_chart_svg(spec, labels, values, kind, width, height, palette, design), encoding="utf-8", newline="\n")
    alt = str(spec.get("alt_text", "")) or f"{kind.title()} chart showing " + ", ".join(f"{label}: {_format_number(value)}" for label, value in zip(labels, values))
    return {"png": str(png_path), "svg": str(svg_path), "alt_text": alt}


def _draw_pie(draw: ImageDraw.ImageDraw, labels: list[str], values: list[float], center: tuple[int, int], radius: int, palette: list[str], font: ImageFont.ImageFont, muted: str) -> None:
    total = sum(max(0.0, value) for value in values) or 1.0
    start = -90.0
    for index, value in enumerate(values):
        extent = max(0.0, value) / total * 360
        draw.pieslice((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), start, start + extent, fill=palette[index % len(palette)], outline="#FFFFFF")
        start += extent
    legend_x, legend_y = 700, 180
    for index, label in enumerate(labels):
        y = legend_y + index * 30
        draw.rectangle((legend_x, y, legend_x + 16, y + 16), fill=palette[index % len(palette)])
        draw.text((legend_x + 24, y + 2), f"{label} ({_format_number(values[index])})", fill=muted, font=font)


def _label(draw: ImageDraw.ImageDraw, value: str, x: float, y: float, font: ImageFont.ImageFont, fill: str) -> None:
    box = draw.textbbox((0, 0), value, font=font)
    draw.text((x - (box[2] - box[0]) / 2, y), value, fill=fill, font=font)


def _format_number(value: float) -> str:
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _chart_svg(spec: dict[str, Any], labels: list[str], values: list[float], kind: str, width: int, height: int, palette: list[str], design: dict[str, Any] | None = None) -> str:
    design = design or {}
    palette_map = design.get("palette", {}) or {}
    chart_map = design.get("chart", {}) or {}
    paper = html.escape(str(palette_map.get("paper", "#FFFFFF")))
    surface = html.escape(str(palette_map.get("surface", "#F8FAFC")))
    ink = html.escape(str(palette_map.get("ink", "#17202A")))
    muted = html.escape(str(palette_map.get("muted", "#5D6B78")))
    rule = html.escape(str(palette_map.get("rule", "#D7DEE5")))
    accent = html.escape(str(palette_map.get("accent", "#2563EB")))
    font_family = html.escape(str((design.get("typography", {}) or {}).get("body", "sans-serif")))
    heading_family = html.escape(str((design.get("typography", {}) or {}).get("heading", font_family)))
    line_width = max(2, float(chart_map.get("line_width", 3)))
    title = html.escape(str(spec.get("title", "")))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', f'<rect width="100%" height="100%" fill="{paper}"/>', f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="18" fill="{surface}" stroke="{rule}" stroke-width="2"/>', f'<rect x="24" y="24" width="{width - 48}" height="10" fill="{accent}"/>']
    if title:
        parts.append(f'<text x="62" y="88" font-family="{heading_family}" font-size="30" font-weight="700" fill="{ink}">{title}</text>')
    left, top, right, bottom = 120, 135, width - 72, height - 112
    if kind == "pie":
        total = sum(max(0.0, value) for value in values) or 1.0
        cx, cy, radius, start = 390, 365, 210, -90.0
        for index, value in enumerate(values):
            extent = max(0.0, value) / total * 360
            end = start + extent
            large = 1 if extent > 180 else 0
            x1, y1 = cx + radius * math.cos(math.radians(start)), cy + radius * math.sin(math.radians(start))
            x2, y2 = cx + radius * math.cos(math.radians(end)), cy + radius * math.sin(math.radians(end))
            path = f"M {cx} {cy} L {x1:.1f} {y1:.1f} A {radius} {radius} 0 {large} 1 {x2:.1f} {y2:.1f} Z"
            parts.append(f'<path d="{path}" fill="{palette[index % len(palette)]}" stroke="#fff"/>')
            start = end
    else:
        maximum, minimum = max(max(values), 0.0), min(min(values), 0.0)
        span = maximum - minimum or 1.0
        for step in range(6):
            value = minimum + span * step / 5
            y = bottom - (value - minimum) / span * (bottom - top)
            parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{rule}"/>')
        if kind == "bar":
            slot = (right - left) / len(values)
            bar_width = max(12, slot * 0.58)
            y_zero = bottom - (0 - minimum) / span * (bottom - top)
            for index, value in enumerate(values):
                x = left + slot * index + (slot - bar_width) / 2
                y = bottom - (value - minimum) / span * (bottom - top)
                parts.append(f'<rect x="{x:.1f}" y="{min(y, y_zero):.1f}" width="{bar_width:.1f}" height="{abs(y - y_zero):.1f}" rx="6" fill="{palette[index % len(palette)]}"/>')
                parts.append(f'<text x="{x + bar_width / 2:.1f}" y="{bottom + 35}" text-anchor="middle" font-family="{font_family}" font-size="18" fill="{muted}">{html.escape(labels[index])}</text>')
        else:
            slot = (right - left) / max(1, len(values) - 1)
            points = []
            for index, value in enumerate(values):
                x = left + slot * index
                y = bottom - (value - minimum) / span * (bottom - top)
                points.append((x, y))
                parts.append(f'<text x="{x:.1f}" y="{bottom + 35}" text-anchor="middle" font-family="{font_family}" font-size="18" fill="{muted}">{html.escape(labels[index])}</text>')
            points_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            parts.append(f'<polyline points="{points_text}" fill="none" stroke="{palette[0]}" stroke-width="{line_width}"/>')
            for x, y in points:
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{palette[0]}" stroke="{surface}" stroke-width="3"/>')
        parts.extend([f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{muted}" stroke-width="2"/>', f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{muted}" stroke-width="2"/>'])
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
    except TypeError:  # Pillow versions before the size argument
        return ImageFont.load_default()
