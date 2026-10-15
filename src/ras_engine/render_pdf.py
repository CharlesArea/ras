"""Theme-aware PDF renderer for the canonical RAS model."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .components import component_colors, component_kind, component_variant, semantic_label
from .markdown import Element, inline_markup, parse_markdown
from .models import ReportProject


class RenderError(RuntimeError):
    """Raised when the optional PDF runtime is unavailable."""


def render_pdf(project: ReportProject, output_path: str | Path, visuals: dict[str, dict[str, str]] | None = None) -> Path:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import A4, landscape, portrait
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.platypus import Image, ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise RenderError("reportlab is required for PDF output") from exc

    visuals = visuals or {}
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    design = project.design
    palette = design.get("palette", {}) or {}
    table_map = project.brand.get("table", {}) or {}
    page = design.get("page", {}) or {}
    margins = page.get("margins", {}) or {}
    geometry = project.style.page_geometry
    pagesize = landscape(A4) if geometry == "landscape" else portrait(A4)
    left_margin = float(margins.get("left", 0.68)) * inch
    right_margin = float(margins.get("right", 0.68)) * inch
    top_margin = float(margins.get("top", 0.62)) * inch + 0.16 * inch
    bottom_margin = float(margins.get("bottom", 0.62)) * inch + 0.22 * inch
    doc = SimpleDocTemplate(str(output), pagesize=pagesize, rightMargin=right_margin, leftMargin=left_margin, topMargin=top_margin, bottomMargin=bottom_margin)

    cjk_font = None
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        cjk_font = "STSong-Light"
    except Exception:  # pragma: no cover - reportlab install variation
        pass
    typography = design.get("typography", {}) or {}
    latin_body = "Times-Roman" if str(typography.get("body", "")).startswith("Times") else "Helvetica"
    latin_heading = "Times-Bold" if str(typography.get("heading", "")).startswith("Times") else "Helvetica-Bold"
    use_cjk = bool(cjk_font and _contains_cjk(_project_text(project)))
    body_font = cjk_font if use_cjk else latin_body
    heading_font = cjk_font if use_cjk else latin_heading
    mono_font = "Courier"
    ink = _color(colors, palette.get("ink", "#17202A"))
    muted = _color(colors, palette.get("muted", "#5D6B78"))
    accent = _color(colors, palette.get("accent", "#2563EB"))
    surface = _color(colors, palette.get("surface", "#F5F7FA"))
    soft_accent = _color(colors, palette.get("accent_soft", palette.get("surface", "#F5F7FA")))
    rule = _color(colors, palette.get("rule", "#D7DEE5"))
    styles = getSampleStyleSheet()
    body = ParagraphStyle("RASBody", parent=styles["BodyText"], fontName=body_font, fontSize=9.5, leading=14, textColor=ink, spaceAfter=7)
    heading1 = ParagraphStyle("RASH1", parent=styles["Heading1"], fontName=heading_font, fontSize=16, leading=20, textColor=accent, spaceBefore=17, spaceAfter=8, keepWithNext=True)
    heading2 = ParagraphStyle("RASH2", parent=styles["Heading2"], fontName=heading_font, fontSize=12, leading=16, textColor=accent, spaceBefore=10, spaceAfter=5, keepWithNext=True)
    caption = ParagraphStyle("RASCAPTION", parent=body, fontSize=7.5, leading=10, textColor=muted, alignment=TA_CENTER, spaceAfter=6)
    small = ParagraphStyle("RASSMALL", parent=body, fontSize=7.5, leading=10, textColor=muted)
    cover_eyebrow = ParagraphStyle("RASCoverEyebrow", parent=small, fontName=heading_font, fontSize=8.5, leading=11, textColor=accent, spaceAfter=6)
    cover_title = ParagraphStyle("RASCoverTitle", parent=styles["Title"], fontName=heading_font, fontSize=27, leading=32, alignment=TA_LEFT, textColor=ink, spaceAfter=8)
    cover_subtitle = ParagraphStyle("RASCoverSubtitle", parent=body, alignment=TA_LEFT, fontSize=10, leading=14, textColor=muted, spaceAfter=5)
    panel_label = ParagraphStyle("RASPanelLabel", parent=small, fontName=heading_font, fontSize=8, leading=10, textColor=accent, spaceAfter=0)
    panel_body = ParagraphStyle("RASPanelBody", parent=body, spaceAfter=0)
    code = ParagraphStyle("RASCode", parent=body, fontName=mono_font, fontSize=8, leading=11, backColor=surface, borderColor=rule, borderWidth=0.5, borderPadding=7)

    story: list[Any] = [_cover_flowable(project, design, doc.width, Table, TableStyle, Paragraph, cover_eyebrow, cover_title, cover_subtitle, small, accent, surface, soft_accent, rule, muted)]
    story.append(Spacer(1, 0.18 * inch))
    figure_index = 0
    for index, block in enumerate(project.blocks, start=1):
        if bool((block.spec.presentation or {}).get("break_before")) and index > 1:
            story.append(PageBreak())
        kind = component_kind(block)
        story.append(Paragraph(_escape(f"{index:02d}  {block.spec.title}"), heading1))
        if kind in {"summary", "finding", "recommendation"}:
            story.append(_semantic_panel(block, design, doc.width, Table, TableStyle, Paragraph, panel_label, panel_body, small, colors, rule))
            story.append(Spacer(1, 0.06 * inch))
        elements = parse_markdown(block.body)
        if elements and elements[0].kind == "heading" and _same_heading(elements[0].text, block.spec.title):
            elements = elements[1:]
        figure = visuals.get(block.spec.id)
        visual_first = project.style.emphasis == "visual-first" or bool(block.spec.visual.get("position") == "before")
        if visual_first and figure:
            figure_index += 1
            story.extend(_visual_flowable(figure, block.spec.visual, figure_index, Image, Paragraph, caption, small, inch, doc.width))
        story.extend(_element_flowables(elements, body, heading2, code, colors, table_map, design, Paragraph, ListFlowable, ListItem, Preformatted, Table, TableStyle, doc.width))
        if not visual_first and figure:
            figure_index += 1
            story.extend(_visual_flowable(figure, block.spec.visual, figure_index, Image, Paragraph, caption, small, inch, doc.width))

    if project.sources:
        story.append(Paragraph("Sources", heading1))
        data = [[Paragraph("ID", small), Paragraph("Source", small), Paragraph("Details", small)]]
        for source in project.sources:
            detail = "; ".join(item for item in [source.author or source.publisher, source.url or source.file, source.publication_date] if item)
            data.append([Paragraph(_escape(source.id), small), Paragraph(_escape(source.title), small), Paragraph(_escape(detail), small)])
        table = Table(data, colWidths=[0.65 * inch, doc.width * 0.40, doc.width * 0.60 - 0.65 * inch], repeatRows=1)
        table.setStyle(_table_style(colors, table_map, palette, TableStyle, zebra=True))
        story.append(table)

    assumptions = project.raw_manifest.get("assumptions", []) or []
    omitted = project.raw_manifest.get("omitted_material", []) or []
    if assumptions or omitted:
        story.append(Paragraph("Quality receipt", heading1))
        for label, values in (("Assumptions", assumptions), ("Omitted or unresolved material", omitted)):
            if values:
                story.append(Paragraph(_escape(label), heading2))
                story.append(ListFlowable([ListItem(Paragraph(_escape(str(item)), body)) for item in values], bulletType="bullet", leftIndent=18))

    def page_chrome(canvas: Any, built_doc: Any) -> None:
        _page_chrome(canvas, built_doc, project, design, colors, heading_font)

    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    return output


def _cover_flowable(project: ReportProject, design: dict[str, Any], width: float, Table: Any, TableStyle: Any, Paragraph: Any, eyebrow: Any, title: Any, subtitle: Any, small: Any, accent: Any, surface: Any, soft_accent: Any, rule: Any, muted: Any) -> Any:
    from reportlab.lib.styles import ParagraphStyle

    palette = design.get("palette", {}) or {}
    theme = str(design.get("theme_id", "minimal"))
    dark_cover = theme in {"institutional", "technical", "data-forward"}
    title_style = title
    eyebrow_style = eyebrow
    subtitle_style = subtitle
    text_color = palette.get("paper", "#FFFFFF") if dark_cover else palette.get("ink", "#17202A")
    if dark_cover:
        title_style = ParagraphStyle("RASDarkCoverTitle", parent=title, textColor=_color_from_palette(text_color))
        eyebrow_style = ParagraphStyle("RASDarkCoverEyebrow", parent=eyebrow, textColor=_color_from_palette(text_color))
        subtitle_style = ParagraphStyle("RASDarkCoverSubtitle", parent=subtitle, textColor=_color_from_palette(text_color))
    title_text = Paragraph(_escape(project.title), title_style)
    subtitle_text = Paragraph(_escape(f"{project.style.archetype.replace('-', ' ').title()}  ·  {project.style.tone.title()}  ·  {design.get('display_name', 'RAS')}"), subtitle_style)
    receipt = str((project.raw_manifest.get("style_decision", {}) or {}).get("style_receipt", project.style.rationale))
    receipt_style = small
    if dark_cover:
        receipt_style = ParagraphStyle("RASDarkCoverReceipt", parent=small, textColor=_color_from_palette(palette.get("paper", "#FFFFFF")))
    receipt_text = Paragraph(_escape(receipt), receipt_style)
    label = Paragraph(_escape(f"RAS / {design.get('display_name', 'Report')}".upper()), eyebrow_style)
    data = [[label], [title_text], [subtitle_text], [receipt_text]]
    table = Table(data, colWidths=[width])
    background = _color_from_palette(palette.get("accent", "#2563EB")) if dark_cover else surface
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.8, rule),
        ("LINEBEFORE", (0, 0), (0, -1), 8, _color_from_palette(palette.get("accent", "#2563EB"))),
        ("LEFTPADDING", (0, 0), (-1, -1), 22),
        ("RIGHTPADDING", (0, 0), (-1, -1), 22),
        ("TOPPADDING", (0, 0), (-1, 0), 17),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
        ("TOPPADDING", (0, 1), (-1, 1), 8),
        ("TOPPADDING", (0, 2), (-1, 2), 0),
        ("TOPPADDING", (0, 3), (-1, 3), 8),
    ]))
    return table


def _semantic_panel(block: Any, design: dict[str, Any], width: float, Table: Any, TableStyle: Any, Paragraph: Any, label_style: Any, body_style: Any, small: Any, colors: Any, rule: Any) -> Any:
    kind = component_kind(block)
    accent_hex, soft_hex, _ = component_colors(design, kind)
    label = semantic_label(kind) or kind.title()
    variant = component_variant(block, design)
    label_text = Paragraph(_escape(f"{label}  /  {variant}"), label_style)
    body_text = Paragraph(_escape(block.spec.goal or "Evidence-led report component"), body_style)
    panel = Table([[label_text, body_text]], colWidths=[width * 0.25, width * 0.75])
    panel.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), _color(colors, soft_hex)),
        ("LINEBEFORE", (0, 0), (0, -1), 5, _color(colors, accent_hex)),
        ("BOX", (0, 0), (-1, -1), 0.45, rule),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return panel


def _element_flowables(elements: list[Element], body: Any, heading2: Any, code: Any, colors: Any, table_map: dict[str, Any], design: dict[str, Any], Paragraph: Any, ListFlowable: Any, ListItem: Any, Preformatted: Any, Table: Any, TableStyle: Any, width: float) -> list[Any]:
    output: list[Any] = []
    palette = design.get("palette", {}) or {}
    for element in elements:
        if element.kind == "heading":
            output.append(Paragraph(_escape(element.text), heading2))
        elif element.kind == "paragraph":
            output.append(Paragraph(_escape(element.text), body))
        elif element.kind == "bullet_list":
            output.append(ListFlowable([ListItem(Paragraph(_escape(item), body)) for item in element.items or []], bulletType="bullet", leftIndent=18))
        elif element.kind == "callout":
            note_style = ParagraphStyle("RASNote", parent=body, fontSize=7.5, leading=9, textColor=_color(colors, palette.get("accent", "#2563EB")), fontName=body.fontName)
            panel = Table([[Paragraph("NOTE", note_style), Paragraph(_escape(element.text), body)]], colWidths=[0.16 * width, 0.84 * width])
            panel.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), _color(colors, palette.get("accent_soft", palette.get("surface", "#F5F7FA")))),
                ("LINEBEFORE", (0, 0), (0, -1), 4, _color(colors, palette.get("accent", "#2563EB"))),
                ("BOX", (0, 0), (-1, -1), 0.4, _color(colors, palette.get("rule", "#D7DEE5"))),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            output.append(panel)
        elif element.kind == "code":
            output.append(Preformatted(element.text, code))
        elif element.kind == "table":
            rows = element.rows or []
            if not rows:
                continue
            data = [[Paragraph(_escape(value), body) for value in row] for row in rows]
            table = Table(data, repeatRows=1, hAlign="LEFT")
            table.setStyle(_table_style(colors, table_map, palette, TableStyle, zebra=True))
            output.append(table)
    return output


def _table_style(colors: Any, table_map: dict[str, Any], palette: dict[str, Any], TableStyle: Any, zebra: bool = False) -> Any:
    commands: list[tuple[Any, ...]] = [
        ("BACKGROUND", (0, 0), (-1, 0), _color(colors, table_map.get("header_fill", palette.get("accent_soft", "#EAF2FF")))),
        ("TEXTCOLOR", (0, 0), (-1, 0), _color(colors, palette.get("ink", "#17202A"))),
        ("GRID", (0, 0), (-1, -1), 0.35, _color(colors, table_map.get("border", palette.get("rule", "#CBD5E1")))),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if zebra:
        commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [_color(colors, palette.get("paper", "#FFFFFF")), _color(colors, table_map.get("stripe_fill", palette.get("surface", "#F8FAFC")))]))
    return TableStyle(commands)


def _visual_flowable(figure: dict[str, str], spec: dict[str, Any], index: int, Image: Any, Paragraph: Any, caption: Any, small: Any, inch: Any, width: float) -> list[Any]:
    path = figure.get("png") or figure.get("svg")
    if not path or not Path(path).exists():
        return []
    target_width = 7.6 * inch if width > 8.0 * inch else 6.2 * inch
    image_width = min(target_width, width)
    image = Image(path, width=image_width, height=image_width * 0.52, kind="proportional")
    alt = str(spec.get("alt_text") or figure.get("alt_text") or "Informative report visual")
    label = str(spec.get("caption", "")).strip()
    result: list[Any] = [image]
    if label:
        result.append(Paragraph(_escape(f"Figure {index}. {label}"), caption))
    result.append(Paragraph(_escape(f"Alternative text: {alt}"), small))
    return result


def _page_chrome(canvas: Any, doc: Any, project: ReportProject, design: dict[str, Any], colors: Any, heading_font: str) -> None:
    palette = design.get("palette", {}) or {}
    canvas.saveState()
    width, height = doc.pagesize
    canvas.setFillColor(_color(colors, palette.get("paper", "#FFFFFF")))
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    accent = _color(colors, palette.get("accent", "#2563EB"))
    muted = _color(colors, palette.get("muted", "#5D6B78"))
    rule = _color(colors, palette.get("rule", "#D7DEE5"))
    header_mode = str((design.get("page", {}) or {}).get("header", "compact"))
    band_height = 12 if header_mode in {"dashboard", "official", "blueprint"} else 5
    canvas.setFillColor(accent)
    canvas.rect(0, height - band_height, width, band_height, fill=1, stroke=0)
    canvas.setStrokeColor(rule)
    canvas.setLineWidth(0.55)
    canvas.line(doc.leftMargin, height - doc.topMargin + 13, width - doc.rightMargin, height - doc.topMargin + 13)
    canvas.setFont(heading_font, 7.5)
    canvas.setFillColor(muted)
    canvas.drawString(doc.leftMargin, height - doc.topMargin + 19, project.title[:100])
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(width - doc.rightMargin, 0.31 * 72, f"{design.get('theme_id', 'minimal')}  ·  Page {doc.page}")
    canvas.setStrokeColor(rule)
    canvas.line(doc.leftMargin, 0.47 * 72, width - doc.rightMargin, 0.47 * 72)
    canvas.restoreState()


def _project_text(project: ReportProject) -> str:
    return " ".join([project.title] + [block.body for block in project.blocks])


def _contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", value))


def _escape(value: str) -> str:
    return inline_markup(value)


def _color(colors: Any, value: str) -> Any:
    return colors.HexColor(str(value))


def _color_from_palette(value: str) -> Any:
    from reportlab.lib import colors

    return colors.HexColor(str(value))


def _same_heading(left: str, right: str) -> bool:
    return "".join(char for char in left.lower() if char.isalnum()) == "".join(char for char in right.lower() if char.isalnum())
