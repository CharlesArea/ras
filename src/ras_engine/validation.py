"""Structural, evidence, accessibility, and safety validation."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .models import ARCHETYPES, BLOCK_STATUSES, DENSITIES, EMPHASES, EVIDENCE_LEVELS, GEOMETRIES, TONES, VISUAL_STYLES, ReportProject
from .planning import DEPTHS, RESEARCH_MODES
from .security import ensure_within, unresolved_placeholders


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def validate_project(project: ReportProject, *, check_outputs: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    raw = project.raw_manifest
    if raw.get("schema_version") != 1:
        issues.append(Issue("error", "schema-version", "Manifest must declare schema_version: 1", str(project.manifest_path)))
    if not raw.get("report_id"):
        issues.append(Issue("error", "report-id", "Manifest requires a stable report_id", str(project.manifest_path)))
    if not raw.get("title"):
        issues.append(Issue("error", "title", "Manifest requires a report title", str(project.manifest_path)))
    if not (raw.get("request") or {}).get("text"):
        issues.append(Issue("warning", "request", "Manifest request text is empty", str(project.manifest_path)))
    for key, default in (("blocks_directory", "blocks"), ("sources_file", "sources.yaml"), ("brand_file", "")):
        configured = raw.get(key, default)
        if configured:
            try:
                ensure_within(project.root, str(configured))
            except ValueError as exc:
                issues.append(Issue("error", "unsafe-manifest-path", str(exc), f"manifest.yaml:{key}"))
    outputs = raw.get("outputs", {}) or {}
    try:
        ensure_within(project.root, str(outputs.get("directory", "dist")))
    except ValueError as exc:
        issues.append(Issue("error", "unsafe-output-path", str(exc), "manifest.yaml:outputs.directory"))
    style = project.style
    for key, value, allowed in [
        ("archetype", style.archetype, ARCHETYPES),
        ("visual_style", style.visual_style, VISUAL_STYLES),
        ("density", style.density, DENSITIES),
        ("tone", style.tone, TONES),
        ("emphasis", style.emphasis, EMPHASES),
        ("evidence_level", style.evidence_level, EVIDENCE_LEVELS),
        ("page_geometry", style.page_geometry, GEOMETRIES),
    ]:
        if value not in allowed:
            issues.append(Issue("error", f"style-{key}", f"Unsupported style value {value!r}", "style_decision." + key))
    design_request = raw.get("design", {}) or {}
    for key, value, allowed in [
        ("theme", design_request.get("theme"), VISUAL_STYLES),
        ("density", design_request.get("density"), DENSITIES),
        ("tone", design_request.get("tone"), TONES),
        ("emphasis", design_request.get("emphasis"), EMPHASES),
    ]:
        if value is not None and value not in allowed:
            issues.append(Issue("error", f"design-{key}", f"Unsupported design value {value!r}", f"design.{key}"))
    content_plan = raw.get("content_plan", {}) or {}
    if content_plan:
        profile = content_plan.get("profile")
        if profile not in DEPTHS:
            issues.append(Issue("error", "content-plan-profile", f"Unsupported content profile {profile!r}", "content_plan.profile"))
        target_pages = content_plan.get("target_pages")
        if target_pages is not None and (not isinstance(target_pages, int) or not 1 <= target_pages <= 100):
            issues.append(Issue("error", "content-plan-pages", "Content plan target_pages must be an integer between 1 and 100", "content_plan.target_pages"))
    research = raw.get("research", {}) or {}
    research_mode = research.get("mode")
    if research_mode is not None and research_mode not in RESEARCH_MODES:
        issues.append(Issue("error", "research-mode", f"Unsupported research mode {research_mode!r}", "research.mode"))
    issues.extend(_validate_brand_contrast(project))

    manifest_blocks = raw.get("blocks", []) or []
    block_ids = [block.spec.id for block in project.blocks]
    duplicates = sorted({item for item in block_ids if block_ids.count(item) > 1})
    for duplicate in duplicates:
        issues.append(Issue("error", "duplicate-block", f"Block ID is not unique: {duplicate}", "blocks"))
    source_ids = {source.id for source in project.sources}
    if len(source_ids) != len(project.sources):
        issues.append(Issue("error", "duplicate-source", "Source IDs must be unique", "sources.yaml"))
    claim_ids = {claim.id for claim in project.claims}
    if len(claim_ids) != len(project.claims):
        issues.append(Issue("error", "duplicate-claim", "Claim IDs must be unique", "sources.yaml"))
    for source in project.sources:
        if not source.id or not source.title:
            issues.append(Issue("error", "source-fields", "Every source requires id and title", "sources.yaml"))
        if source.file:
            try:
                source_path = ensure_within(project.root, source.file)
                if not source_path.exists():
                    issues.append(Issue("error", "missing-source-file", f"Source file does not exist: {source.file}", f"sources.yaml:{source.id}"))
            except ValueError as exc:
                issues.append(Issue("error", "unsafe-source-path", str(exc), f"sources.yaml:{source.id}"))
    try:
        source_ledger = ensure_within(project.root, str(raw.get("sources_file", "sources.yaml")))
    except ValueError:
        source_ledger = None
    if source_ledger is not None and not source_ledger.exists():
        issues.append(Issue("error", "missing-source-ledger", "sources_file does not exist", "manifest.yaml:sources_file"))
    for claim in project.claims:
        if not claim.id or not claim.statement:
            issues.append(Issue("error", "claim-fields", "Every claim requires id and statement", "sources.yaml"))
        for source_ref in claim.source_refs:
            if source_ref not in source_ids:
                issues.append(Issue("error", "missing-claim-source", f"Claim {claim.id} references missing source {source_ref}", "sources.yaml"))

    referenced_manifest_ids: set[str] = set()
    for block in project.blocks:
        spec = block.spec
        referenced_manifest_ids.add(spec.id)
        if not spec.id or not spec.title or not spec.goal:
            issues.append(Issue("error", "block-fields", f"Block {spec.id or '<unnamed>'} requires id, title, and goal", str(block.path)))
        if spec.status not in BLOCK_STATUSES:
            issues.append(Issue("error", "block-status", f"Unsupported block status {spec.status!r}", str(block.path)))
        if spec.word_budget is not None and spec.word_budget < 1:
            issues.append(Issue("error", "block-word-budget", f"Block {spec.id} word_budget must be positive", str(block.path)))
        try:
            ensure_within(project.root, block.path)
        except ValueError as exc:
            issues.append(Issue("error", "unsafe-block-path", str(exc), str(block.path)))
        if not block.path.exists():
            issues.append(Issue("error", "missing-block", f"Block file does not exist: {spec.file or spec.id}", str(block.path)))
        if block.frontmatter and block.frontmatter.get("id") not in {None, spec.id}:
            issues.append(Issue("error", "block-id-mismatch", f"Frontmatter id does not match manifest for {spec.id}", str(block.path)))
        for ref in spec.source_refs:
            if ref not in source_ids:
                issues.append(Issue("error", "missing-block-source", f"Block {spec.id} references missing source {ref}", str(block.path)))
        for placeholder in unresolved_placeholders(block.body):
            issues.append(Issue("error", "placeholder", f"Unresolved placeholder: {placeholder}", str(block.path)))
        citation_ids = set(re.findall(r"\[([A-Za-z][A-Za-z0-9_-]*)\]", block.body))
        for citation in sorted(citation_ids):
            if citation.startswith(("S", "SRC", "source")) and citation not in source_ids:
                issues.append(Issue("error", "missing-citation", f"Citation marker [{citation}] has no source record", str(block.path)))
        visual = spec.visual or {}
        is_visual = bool(visual.get("required")) or spec.type in {"chart", "diagram", "timeline", "metric_panel", "table_visual"}
        if is_visual:
            if not visual.get("caption"):
                issues.append(Issue("error", "visual-caption", f"Visual block {spec.id} requires a caption", str(block.path)))
            if not visual.get("alt_text"):
                issues.append(Issue("error", "visual-alt-text", f"Visual block {spec.id} requires alternative text", str(block.path)))

    manifest_set = {str(item.get("id")) for item in manifest_blocks if isinstance(item, dict) and item.get("id")}
    for block_id in sorted(manifest_set - referenced_manifest_ids):
        issues.append(Issue("error", "unloaded-block", f"Manifest block could not be loaded: {block_id}", "manifest.yaml"))
    if check_outputs:
        outputs = raw.get("outputs", {}) or {}
        for fmt in outputs.get("formats", []) or []:
            path = project.output_dir / f"{outputs.get('filename', project.report_id)}.{fmt}"
            if not path.exists():
                issues.append(Issue("error", "missing-output", f"Expected output does not exist: {path.name}", str(path)))
    return issues


def issues_to_text(issues: list[Issue]) -> str:
    if not issues:
        return "PASS: no validation issues"
    lines = [f"{issue.severity.upper()} {issue.code}: {issue.message}" + (f" [{issue.path}]" if issue.path else "") for issue in issues]
    return "\n".join(lines)


def has_errors(issues: list[Issue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def _validate_brand_contrast(project: ReportProject) -> list[Issue]:
    colors = project.brand.get("colors", {}) or {}
    paper = colors.get("paper", "#FFFFFF")
    issues: list[Issue] = []
    for role in ("ink", "muted", "accent"):
        value = colors.get(role)
        if not value:
            continue
        try:
            ratio = _contrast_ratio(str(value), str(paper))
        except ValueError:
            issues.append(Issue("error", "brand-color", f"Invalid brand color for {role}: {value!r}", f"brand.colors.{role}"))
            continue
        if ratio < 4.5:
            issues.append(Issue("error", "contrast", f"Brand color {role} has contrast ratio {ratio:.2f}:1 against paper; minimum is 4.5:1", f"brand.colors.{role}"))
    return issues


def _contrast_ratio(first: str, second: str) -> float:
    def channel(value: int) -> float:
        normalized = value / 255
        return normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4

    def luminance(value: str) -> float:
        text = value.strip().lstrip("#")
        if len(text) != 6:
            raise ValueError(value)
        red, green, blue = (int(text[index:index + 2], 16) for index in (0, 2, 4))
        return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)

    left, right = luminance(first), luminance(second)
    lighter, darker = max(left, right), min(left, right)
    return (lighter + 0.05) / (darker + 0.05)
