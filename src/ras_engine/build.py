"""Build orchestration for DOCX, PDF, and PPTX outputs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .design import design_signature
from .models import ReportProject
from .layout import plan_project
from .project import slugify
from .render_docx import render_docx
from .render_pdf import render_pdf
from .render_pptx import render_pptx
from .routing import style_receipt
from .validation import has_errors, validate_project
from .visuals import prepare_visuals


class BuildError(RuntimeError):
    """Raised when a report cannot be built safely."""


def build_project(manifest_path: str | Path, formats: list[str] | None = None, *, allow_validation_warnings: bool = True) -> dict[str, Any]:
    project = ReportProject.load(manifest_path)
    issues = validate_project(project)
    if has_errors(issues):
        raise BuildError("Validation failed before rendering: " + "; ".join(issue.message for issue in issues if issue.severity == "error"))
    requested = [str(item).lower().lstrip(".") for item in (formats or project.raw_manifest.get("outputs", {}).get("formats", ["docx", "pdf"]))]
    unsupported = sorted(set(requested) - {"docx", "pdf", "pptx"})
    if unsupported:
        raise BuildError(f"Unsupported output format(s): {', '.join(unsupported)}")
    build_dir = project.root / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    visuals = prepare_visuals(project, build_dir)
    output_dir = project.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = slugify(str((project.raw_manifest.get("outputs", {}) or {}).get("filename", project.report_id)), project.report_id)
    outputs: dict[str, str] = {}
    for fmt in requested:
        target = output_dir / f"{filename}.{fmt}"
        if fmt == "docx":
            render_docx(project, target, visuals)
        elif fmt == "pdf":
            render_pdf(project, target, visuals)
        elif fmt == "pptx":
            render_pptx(project, target, visuals)
        outputs[fmt] = str(target)
    model_path = build_dir / "canonical-model.json"
    model = {
        "schema_version": 1,
        "report_id": project.report_id,
        "title": project.title,
        "style_decision": project.style.to_dict(),
        "content_plan": project.raw_manifest.get("content_plan", {}),
        "research": project.raw_manifest.get("research", {}),
        "design": {
            "theme_id": project.design.get("theme_id"),
            "display_name": project.design.get("display_name"),
            "resolved_brand": project.design.get("resolved_brand"),
            "signature": design_signature(project.design),
            "receipt": project.design.get("receipt", {}),
        },
        "layout": plan_project(project).to_dict(),
        "blocks": [{"id": block.spec.id, "type": block.spec.type, "title": block.spec.title, "text": block.body} for block in project.blocks],
        "sources": [source.to_dict() for source in project.sources],
        "claims": [claim.to_dict() for claim in project.claims],
        "outputs": outputs,
    }
    model_path.write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    project.raw_manifest.setdefault("outputs", {})["formats"] = requested
    project.raw_manifest.setdefault("style_decision", {})["style_receipt"] = style_receipt(project.style)
    project.raw_manifest.setdefault("progress", {})["status"] = "built"
    project.raw_manifest.setdefault("progress", {})["completed_blocks"] = [block.spec.id for block in project.blocks]
    project.raw_manifest.setdefault("progress", {})["last_build"] = datetime.now(timezone.utc).isoformat()
    project.raw_manifest.setdefault("qa", {})["status"] = "not_run"
    project.raw_manifest.setdefault("qa", {})["results"] = []
    project.update_block_statuses("complete")
    project.save_manifest()
    return {"project": project, "outputs": outputs, "visuals": visuals, "issues": issues, "model": str(model_path)}
