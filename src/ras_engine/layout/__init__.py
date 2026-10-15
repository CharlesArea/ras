"""Renderer-independent layout intent for RAS reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..components import component_kind, component_variant


@dataclass
class ComponentPlan:
    block_id: str
    kind: str
    variant: str
    span: int = 12
    priority: str = "standard"
    keep_together: bool = True
    break_before: bool = False


@dataclass
class SectionPlan:
    block_id: str
    title: str
    geometry: str
    component: ComponentPlan


@dataclass
class DocumentPlan:
    theme_id: str
    page_geometry: str
    page: dict[str, Any]
    sections: list[SectionPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def plan_project(project: Any) -> DocumentPlan:
    design = project.design
    page = design.get("page", {}) or {}
    sections: list[SectionPlan] = []
    for block in project.blocks:
        presentation = block.spec.presentation or {}
        kind = component_kind(block)
        default_span = 12 if kind in {"visual", "narrative", "source"} else 6
        raw_span = presentation.get("span", default_span)
        try:
            span = max(1, min(12, int(raw_span)))
        except (TypeError, ValueError):
            span = default_span
        component = ComponentPlan(
            block_id=block.spec.id,
            kind=kind,
            variant=component_variant(block, design),
            span=span,
            priority=str(presentation.get("emphasis", "primary" if kind in {"summary", "finding", "recommendation"} else "standard")),
            keep_together=bool(presentation.get("keep_together", True)),
            break_before=bool(presentation.get("break_before", False)),
        )
        sections.append(SectionPlan(block.spec.id, block.spec.title, project.style.page_geometry, component))
    return DocumentPlan(str(design.get("theme_id", "minimal")), project.style.page_geometry, page, sections)


__all__ = ["ComponentPlan", "DocumentPlan", "SectionPlan", "plan_project"]
