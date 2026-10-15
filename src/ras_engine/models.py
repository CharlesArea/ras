"""Typed internal model for RAS projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from .security import UnsafePathError, ensure_within
from .yamlio import load_yaml, parse_frontmatter, write_yaml


SCHEMA_VERSION = 1
ARCHETYPES = [
    "executive-brief",
    "decision-memo",
    "research-synthesis",
    "analytical-deep-dive",
    "comparative-evaluation",
    "proposal-business-case",
    "strategy-roadmap",
    "status-progress",
    "performance-kpi",
    "audit-assessment",
    "compliance-risk",
    "technical-architecture",
    "incident-postmortem",
    "investigation-root-cause",
    "policy-sop",
    "case-study",
]
VISUAL_STYLES = ["minimal", "editorial", "data-forward", "institutional", "technical", "narrative"]
DENSITIES = ["concise", "standard", "deep"]
TONES = ["executive", "professional", "academic", "public-friendly"]
EMPHASES = ["text-balanced", "visual-first", "evidence-first"]
EVIDENCE_LEVELS = ["informational", "sourced", "auditable"]
GEOMETRIES = ["portrait", "landscape", "mixed"]
BLOCK_STATUSES = ["planned", "draft", "generated", "validated", "complete", "blocked"]


NEUTRAL_BRAND: dict[str, Any] = {
    "schema_version": 1,
    "name": "RAS Neutral",
    "colors": {
        "paper": "#FFFFFF",
        "surface": "#F4F6F8",
        "ink": "#17202A",
        "muted": "#5D6B78",
        "rule": "#D7DEE5",
        "accent": "#175CD3",
        "positive": "#027A48",
        "warning": "#B54708",
        "negative": "#B42318",
    },
    "fonts": {"heading": "Aptos Display", "body": "Aptos", "mono": "Consolas", "cjk_fallback": "Microsoft JhengHei"},
    "spacing": {"page_margin": 0.72, "section_gap": 0.24, "paragraph_gap": 0.08},
    "table": {"header_fill": "#EAF2FF", "stripe_fill": "#F8FAFC", "border": "#CBD5E1"},
    "chart": {"palette": ["#175CD3", "#7F56D9", "#039855", "#DC6803", "#D92D20"]},
    "diagram": {"node_fill": "#EEF4FF", "node_stroke": "#175CD3", "connector": "#667085"},
}


@dataclass
class StyleDecision:
    archetype: str = "executive-brief"
    visual_style: str = "minimal"
    density: str = "standard"
    tone: str = "professional"
    emphasis: str = "text-balanced"
    evidence_level: str = "sourced"
    page_geometry: str = "portrait"
    rationale: str = "Default neutral routing."
    signals: list[str] = field(default_factory=list)
    fallback: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "StyleDecision":
        data = data or {}
        return cls(
            archetype=str(data.get("archetype", "executive-brief")),
            visual_style=str(data.get("visual_style", data.get("visual", "minimal"))),
            density=str(data.get("density", "standard")),
            tone=str(data.get("tone", "professional")),
            emphasis=str(data.get("emphasis", "text-balanced")),
            evidence_level=str(data.get("evidence_level", "sourced")),
            page_geometry=str(data.get("page_geometry", data.get("geometry", "portrait"))),
            rationale=str(data.get("rationale", "")),
            signals=[str(item) for item in data.get("signals", []) or []],
            fallback=data.get("fallback"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "archetype": self.archetype,
            "visual_style": self.visual_style,
            "density": self.density,
            "tone": self.tone,
            "emphasis": self.emphasis,
            "evidence_level": self.evidence_level,
            "page_geometry": self.page_geometry,
            "rationale": self.rationale,
            "signals": self.signals,
            **({"fallback": self.fallback} if self.fallback else {}),
        }


@dataclass
class BlockSpec:
    id: str
    type: str
    title: str
    goal: str = ""
    audience: str = "general"
    status: str = "draft"
    file: str = ""
    required_facts: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    layout_budget: str | float = "standard"
    visual: dict[str, Any] = field(default_factory=dict)
    presentation: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any], fallback_file: str = "") -> "BlockSpec":
        block_id = str(data.get("id", ""))
        return cls(
            id=block_id,
            type=str(data.get("type", "narrative")),
            title=str(data.get("title", block_id.replace("-", " ").title())),
            goal=str(data.get("goal", "")),
            audience=str(data.get("audience", "general")),
            status=str(data.get("status", "draft")),
            file=str(data.get("file", fallback_file)),
            required_facts=[str(item) for item in data.get("required_facts", []) or []],
            source_refs=[str(item) for item in data.get("source_refs", []) or []],
            layout_budget=data.get("layout_budget", "standard"),
            visual=dict(data.get("visual", {}) or {}),
            presentation=dict(data.get("presentation", {}) or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "goal": self.goal,
            "audience": self.audience,
            "status": self.status,
            "file": self.file,
            "required_facts": self.required_facts,
            "source_refs": self.source_refs,
            "layout_budget": self.layout_budget,
            "visual": self.visual,
            "presentation": self.presentation,
        }


@dataclass
class SourceRecord:
    id: str
    title: str
    publisher: str = ""
    author: str = ""
    url: str = ""
    file: str = ""
    publication_date: str = ""
    access_date: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRecord":
        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "")),
            publisher=str(data.get("publisher", "")),
            author=str(data.get("author", "")),
            url=str(data.get("url", "")),
            file=str(data.get("file", "")),
            publication_date=str(data.get("publication_date", "")),
            access_date=str(data.get("access_date", "")),
            notes=str(data.get("notes", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in {
            "id": self.id,
            "title": self.title,
            "publisher": self.publisher,
            "author": self.author,
            "url": self.url,
            "file": self.file,
            "publication_date": self.publication_date,
            "access_date": self.access_date,
            "notes": self.notes,
        }.items() if value}


@dataclass
class ClaimRecord:
    id: str
    statement: str
    source_refs: list[str] = field(default_factory=list)
    confidence: str = "unknown"
    status: str = "unreviewed"
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClaimRecord":
        return cls(
            id=str(data.get("id", "")),
            statement=str(data.get("statement", "")),
            source_refs=[str(item) for item in data.get("source_refs", []) or []],
            confidence=str(data.get("confidence", "unknown")),
            status=str(data.get("status", "unreviewed")),
            notes=str(data.get("notes", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "source_refs": self.source_refs,
            "confidence": self.confidence,
            "status": self.status,
            **({"notes": self.notes} if self.notes else {}),
        }


@dataclass
class BlockDocument:
    spec: BlockSpec
    body: str
    path: Path
    frontmatter: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReportProject:
    root: Path
    manifest_path: Path
    raw_manifest: dict[str, Any]
    style: StyleDecision
    blocks: list[BlockDocument]
    sources: list[SourceRecord]
    claims: list[ClaimRecord]
    brand: dict[str, Any]
    brand_overrides: dict[str, Any] = field(default_factory=dict)

    @property
    def report_id(self) -> str:
        return str(self.raw_manifest.get("report_id", self.root.name))

    @property
    def title(self) -> str:
        request = self.raw_manifest.get("request", {}) or {}
        return str(self.raw_manifest.get("title", request.get("title", self.report_id.replace("-", " ").title())))

    @property
    def output_dir(self) -> Path:
        return self.root / str((self.raw_manifest.get("outputs", {}) or {}).get("directory", "dist"))

    @property
    def design(self) -> dict[str, Any]:
        """Resolved visual system shared by all output renderers."""

        from .design import project_design

        return project_design(self)

    @classmethod
    def load(cls, manifest_path: str | Path) -> "ReportProject":
        manifest = Path(manifest_path).resolve()
        root = manifest.parent
        raw = load_yaml(manifest)
        if not isinstance(raw, dict):
            raise ValueError("Manifest must be a mapping")
        style = StyleDecision.from_dict(raw.get("style_decision"))
        try:
            blocks_dir = ensure_within(root, str(raw.get("blocks_directory", "blocks")))
        except UnsafePathError:
            blocks_dir = root / "__unsafe_blocks_directory__"
        raw_blocks = raw.get("blocks", []) or []
        block_specs: list[BlockSpec] = []
        if isinstance(raw_blocks, list):
            for item in raw_blocks:
                if isinstance(item, str):
                    block_specs.append(BlockSpec.from_dict({"id": item}, f"{item}.md"))
                elif isinstance(item, dict):
                    block_specs.append(BlockSpec.from_dict(item))
        discovered = {path.stem: path for path in sorted(blocks_dir.glob("*.md"))} if blocks_dir.exists() else {}
        if not block_specs:
            block_specs = [BlockSpec.from_dict({"id": key, "file": str(path.relative_to(root))}, str(path.relative_to(root))) for key, path in discovered.items()]
        blocks: list[BlockDocument] = []
        for spec in block_specs:
            relative = spec.file or f"{spec.id}.md"
            try:
                path = ensure_within(root, relative)
                safe_block_path = True
            except UnsafePathError:
                path = (root / relative).resolve()
                safe_block_path = False
            if safe_block_path and not path.exists() and spec.id in discovered:
                path = discovered[spec.id]
            if safe_block_path and path.exists():
                frontmatter, body = parse_frontmatter(path.read_text(encoding="utf-8"))
                merged = {**spec.to_dict(), **frontmatter}
                merged["id"] = spec.id or str(frontmatter.get("id", path.stem))
                merged["file"] = str(path.relative_to(root)) if path.is_relative_to(root) else relative
                blocks.append(BlockDocument(BlockSpec.from_dict(merged, relative), body, path, frontmatter))
            else:
                blocks.append(BlockDocument(spec, "", path, {}))
        try:
            sources_file = ensure_within(root, str(raw.get("sources_file", "sources.yaml")))
        except UnsafePathError:
            sources_file = root / "__unsafe_sources_file__"
        source_raw = load_yaml(sources_file) if sources_file.exists() and sources_file.is_file() else {}
        sources = [SourceRecord.from_dict(item) for item in (source_raw.get("sources", []) if isinstance(source_raw, dict) else []) or [] if isinstance(item, dict)]
        claims = [ClaimRecord.from_dict(item) for item in (source_raw.get("claims", []) if isinstance(source_raw, dict) else []) or [] if isinstance(item, dict)]
        brand = dict(NEUTRAL_BRAND)
        brand_overrides: dict[str, Any] = {}
        project_brand = root / ".ras" / "brand.yaml"
        explicit_brand = raw.get("brand_file")
        if explicit_brand:
            try:
                project_brand = ensure_within(root, str(explicit_brand))
            except UnsafePathError:
                project_brand = root / "__unsafe_brand_file__"
        if project_brand.exists():
            loaded_brand = load_yaml(project_brand)
            if isinstance(loaded_brand, dict):
                brand_overrides = loaded_brand
                brand = deep_merge(brand, loaded_brand)
        return cls(root, manifest, raw, style, blocks, sources, claims, brand, brand_overrides)

    def save_manifest(self) -> None:
        write_yaml(self.manifest_path, self.raw_manifest)

    def update_block_statuses(self, status: str = "validated") -> None:
        by_id = {block.spec.id: block.spec for block in self.blocks}
        for entry in self.raw_manifest.get("blocks", []) or []:
            if isinstance(entry, dict) and entry.get("id") in by_id:
                entry["status"] = status


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def today_iso() -> str:
    return date.today().isoformat()
