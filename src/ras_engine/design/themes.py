"""Built-in RAS visual theme packs.

Theme packs are intentionally semantic. Renderers consume the resolved values
from the compiler rather than hard-coding a report's personality themselves.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


THEME_PACKS: dict[str, dict[str, Any]] = {
    "minimal": {
        "id": "minimal",
        "display_name": "Clear Minimal",
        "palette": {"paper": "#FFFFFF", "surface": "#F5F7FA", "ink": "#17202A", "muted": "#5D6B78", "rule": "#D7DEE5", "accent": "#2563EB", "accent_soft": "#E8F0FF", "positive": "#147D64", "warning": "#A15C00", "negative": "#B42318"},
        "typography": {"display": "Helvetica", "heading": "Helvetica-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "Noto Sans CJK TC"},
        "page": {"size": "A4", "margins": {"top": 0.62, "right": 0.68, "bottom": 0.62, "left": 0.68}, "grid_columns": 12, "gutter": 0.12, "header": "compact", "footer": "folio"},
        "components": {"cover": "minimal-band", "summary": "summary-deck", "finding": "accent-rule", "recommendation": "accent-band", "table": "clean-grid", "source_register": "compact-register", "section_opener": "rule"},
        "chart": {"palette": ["#2563EB", "#7C3AED", "#147D64", "#A15C00", "#B42318"], "grid": "light", "label_policy": "direct", "line_width": 3},
        "diagram": {"node_fill": "#EEF4FF", "node_stroke": "#2563EB", "connector": "#667085", "node_radius": 10},
        "ornament": {"cover_shape": "corner-block", "section_mark": "small-rule", "rule_width": 1},
    },
    "editorial": {
        "id": "editorial",
        "display_name": "Editorial Ledger",
        "palette": {"paper": "#FCFAF6", "surface": "#F2EFE8", "ink": "#24211F", "muted": "#6C655D", "rule": "#D8D0C3", "accent": "#9A3E32", "accent_soft": "#F4E5E1", "positive": "#287A55", "warning": "#986A21", "negative": "#A43A36"},
        "typography": {"display": "Times-Bold", "heading": "Times-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "STSong-Light"},
        "page": {"size": "A4", "margins": {"top": 0.66, "right": 0.78, "bottom": 0.64, "left": 0.82}, "grid_columns": 12, "gutter": 0.16, "header": "folio", "footer": "source-line"},
        "components": {"cover": "editorial-asymmetric", "summary": "opening-deck", "finding": "margin-rule", "recommendation": "editorial-band", "table": "editorial-rules", "source_register": "compact-register", "section_opener": "chapter-rule"},
        "chart": {"palette": ["#9A3E32", "#355C7D", "#5C7A5A", "#B28345", "#6E5B78"], "grid": "horizontal-light", "label_policy": "direct", "line_width": 2.5},
        "diagram": {"node_fill": "#F4E5E1", "node_stroke": "#9A3E32", "connector": "#7B746A", "node_radius": 4},
        "ornament": {"cover_shape": "editorial-rule", "section_mark": "double-rule", "rule_width": 1},
    },
    "data-forward": {
        "id": "data-forward",
        "display_name": "Signal Dashboard",
        "palette": {"paper": "#F7FAFC", "surface": "#FFFFFF", "ink": "#102A43", "muted": "#627D98", "rule": "#D9E2EC", "accent": "#0E7490", "accent_soft": "#DFF5F7", "positive": "#087F5B", "warning": "#B45309", "negative": "#C53030"},
        "typography": {"display": "Helvetica-Bold", "heading": "Helvetica-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "Noto Sans CJK TC"},
        "page": {"size": "A4", "margins": {"top": 0.48, "right": 0.48, "bottom": 0.52, "left": 0.48}, "grid_columns": 12, "gutter": 0.10, "header": "dashboard", "footer": "folio"},
        "components": {"cover": "dashboard-opener", "summary": "metric-deck", "finding": "metric-callout", "recommendation": "action-strip", "table": "dense-grid", "source_register": "compact-register", "section_opener": "metric-rule"},
        "chart": {"palette": ["#0E7490", "#2563EB", "#7C3AED", "#087F5B", "#B45309", "#C53030"], "grid": "horizontal", "label_policy": "annotated", "line_width": 3.5},
        "diagram": {"node_fill": "#E6F6F7", "node_stroke": "#0E7490", "connector": "#627D98", "node_radius": 6},
        "ornament": {"cover_shape": "metric-band", "section_mark": "data-rule", "rule_width": 2},
    },
    "institutional": {
        "id": "institutional",
        "display_name": "Institutional Brief",
        "palette": {"paper": "#F8FAFC", "surface": "#EEF2F6", "ink": "#1B2B3A", "muted": "#52606D", "rule": "#C9D2DC", "accent": "#123B5D", "accent_soft": "#E4EDF5", "positive": "#2F855A", "warning": "#9C6500", "negative": "#A43A36"},
        "typography": {"display": "Helvetica-Bold", "heading": "Helvetica-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "Noto Sans CJK TC"},
        "page": {"size": "A4", "margins": {"top": 0.70, "right": 0.74, "bottom": 0.72, "left": 0.74}, "grid_columns": 12, "gutter": 0.12, "header": "official", "footer": "document-id"},
        "components": {"cover": "official-cover", "summary": "assessment-panel", "finding": "numbered-finding", "recommendation": "formal-action", "table": "formal-grid", "source_register": "formal-register", "section_opener": "numbered-rule"},
        "chart": {"palette": ["#123B5D", "#44799D", "#2F855A", "#9C6500", "#A43A36"], "grid": "formal", "label_policy": "legend", "line_width": 2.5},
        "diagram": {"node_fill": "#E4EDF5", "node_stroke": "#123B5D", "connector": "#52606D", "node_radius": 2},
        "ornament": {"cover_shape": "official-bar", "section_mark": "number-tab", "rule_width": 1},
    },
    "technical": {
        "id": "technical",
        "display_name": "Technical Blueprint",
        "palette": {"paper": "#F4F8FA", "surface": "#E7F0F3", "ink": "#102A43", "muted": "#52606D", "rule": "#B8CBD2", "accent": "#006D77", "accent_soft": "#DDF3F2", "positive": "#087F5B", "warning": "#B45309", "negative": "#C53030"},
        "typography": {"display": "Helvetica-Bold", "heading": "Helvetica-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "Noto Sans CJK TC"},
        "page": {"size": "A4", "margins": {"top": 0.54, "right": 0.56, "bottom": 0.56, "left": 0.56}, "grid_columns": 12, "gutter": 0.10, "header": "blueprint", "footer": "folio"},
        "components": {"cover": "blueprint-cover", "summary": "spec-summary", "finding": "technical-note", "recommendation": "implementation-strip", "table": "spec-grid", "source_register": "compact-register", "section_opener": "blueprint-rule"},
        "chart": {"palette": ["#006D77", "#2563EB", "#7C3AED", "#087F5B", "#B45309"], "grid": "technical", "label_policy": "annotated", "line_width": 2.5},
        "diagram": {"node_fill": "#DDF3F2", "node_stroke": "#006D77", "connector": "#52606D", "node_radius": 3},
        "ornament": {"cover_shape": "grid-corner", "section_mark": "code-tab", "rule_width": 1},
    },
    "narrative": {
        "id": "narrative",
        "display_name": "Narrative Fieldbook",
        "palette": {"paper": "#FFF9F3", "surface": "#FFF0DF", "ink": "#33251F", "muted": "#79665A", "rule": "#E7C8A8", "accent": "#B45309", "accent_soft": "#FDE9D0", "positive": "#287A55", "warning": "#A15C00", "negative": "#A43A36"},
        "typography": {"display": "Times-Bold", "heading": "Times-Bold", "body": "Helvetica", "mono": "Courier", "cjk": "STSong-Light"},
        "page": {"size": "A4", "margins": {"top": 0.68, "right": 0.76, "bottom": 0.66, "left": 0.76}, "grid_columns": 12, "gutter": 0.15, "header": "chapter", "footer": "folio"},
        "components": {"cover": "hero-fieldbook", "summary": "story-deck", "finding": "quote-finding", "recommendation": "story-action", "table": "warm-grid", "source_register": "compact-register", "section_opener": "chapter-card"},
        "chart": {"palette": ["#B45309", "#9A3E32", "#355C7D", "#5C7A5A", "#6E5B78"], "grid": "soft", "label_policy": "direct", "line_width": 2.5},
        "diagram": {"node_fill": "#FDE9D0", "node_stroke": "#B45309", "connector": "#79665A", "node_radius": 12},
        "ornament": {"cover_shape": "hero-swoop", "section_mark": "chapter-rule", "rule_width": 2},
    },
}


def theme_pack(theme_id: str) -> dict[str, Any]:
    return deepcopy(THEME_PACKS.get(theme_id, THEME_PACKS["minimal"]))
