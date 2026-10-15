"""Project initialization and canonical package helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION, StyleDecision, today_iso
from .routing import route_request, style_receipt
from .security import ensure_within
from .yamlio import dump_yaml, parse_frontmatter, write_yaml


def slugify(value: str, fallback: str = "report") -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", (value or "").strip().lower()).strip("-")
    return text[:80] or fallback


def init_project(
    directory: str | Path,
    *,
    request: str = "Create a concise, evidence-grounded report from the supplied material.",
    title: str | None = None,
    overrides: dict[str, Any] | None = None,
    force: bool = False,
) -> Path:
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()) and not force:
        raise FileExistsError(f"Refusing to initialize a non-empty directory without --force: {root}")
    (root / "blocks").mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "build").mkdir(parents=True, exist_ok=True)
    (root / "qa").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(parents=True, exist_ok=True)
    report_title = title or "Report draft"
    report_id = slugify(root.name)
    decision = route_request(request, overrides)
    block_id = "executive-summary"
    block_file = f"blocks/{block_id}.md"
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "report_id": report_id,
        "title": report_title,
        "request": {
            "text": request,
            "audience": "general",
            "overrides": overrides or {},
        },
        "style_decision": {**decision.to_dict(), "style_receipt": style_receipt(decision)},
        "blocks_directory": "blocks",
        "sources_file": "sources.yaml",
        "blocks": [
            {
                "id": block_id,
                "type": "executive_summary",
                "title": "Executive summary",
                "goal": "State the most important supported finding, implication, and next action.",
                "audience": "general",
                "status": "draft",
                "file": block_file,
                "required_facts": [],
                "source_refs": [],
                "layout_budget": "half-page",
                "visual": {"required": False, "caption": "", "alt_text": ""},
            }
        ],
        "outputs": {"directory": "dist", "formats": ["docx", "pdf"], "filename": report_id},
        "progress": {"status": "draft", "completed_blocks": [], "last_build": ""},
        "assumptions": ["No external research is performed unless explicitly authorized."],
        "omitted_material": [],
        "research": {"performed": False, "authorized": False, "notes": ""},
        "qa": {"status": "not_run", "results": []},
        "created_at": today_iso(),
    }
    write_yaml(root / "manifest.yaml", manifest)
    write_yaml(root / "sources.yaml", {"schema_version": SCHEMA_VERSION, "sources": [], "claims": []})
    frontmatter = {
        "schema_version": SCHEMA_VERSION,
        "id": block_id,
        "type": "executive_summary",
        "title": "Executive summary",
        "goal": "State the most important supported finding, implication, and next action.",
        "audience": "general",
        "status": "draft",
        "source_refs": [],
        "required_facts": [],
        "layout_budget": "half-page",
        "visual": {"required": False, "caption": "", "alt_text": ""},
    }
    block_body = (
        "# Executive summary\n\n"
        "No source material has been added yet. Add source records and claims before making substantive conclusions.\n\n"
        "## Implication\n\n"
        "The report will distinguish supported findings, assumptions, and unresolved evidence gaps.\n"
    )
    (root / block_file).write_text(f"---\n{dump_yaml(frontmatter)}---\n\n{block_body}", encoding="utf-8", newline="\n")
    (root / "README.md").write_text(
        f"# {report_title}\n\nThis is a RAS report package. Edit `blocks/*.md` and `sources.yaml`, then run:\n\n"
        "```text\nras-report validate manifest.yaml\nras-report build manifest.yaml --formats docx,pdf\nras-report qa manifest.yaml\n```\n",
        encoding="utf-8",
        newline="\n",
    )
    return root / "manifest.yaml"


def regenerate_block(manifest_path: str | Path, block_id: str, body_file: str | Path | None = None) -> Path:
    """Reset or replace one block while preserving every other block.

    Content generation itself belongs to the host skill/model. This helper
    provides the safe, resumable file operation that lets a host replace one
    generated block without rebuilding the rest of the report package.
    """

    from .models import ReportProject

    project = ReportProject.load(manifest_path)
    selected = next((block for block in project.blocks if block.spec.id == block_id), None)
    if selected is None:
        raise ValueError(f"Unknown block ID: {block_id}")
    target = ensure_within(project.root, selected.path)
    if body_file is not None:
        source = ensure_within(project.root, body_file, allow_missing=False)
        replacement = source.read_text(encoding="utf-8")
        if replacement.startswith("---"):
            target.write_text(replacement, encoding="utf-8", newline="\n")
        else:
            frontmatter = selected.frontmatter or selected.spec.to_dict()
            frontmatter["status"] = "generated"
            target.write_text(f"---\n{dump_yaml(frontmatter)}---\n\n{replacement.lstrip()}", encoding="utf-8", newline="\n")
        new_status = "generated"
    else:
        new_status = "draft"
    for entry in project.raw_manifest.get("blocks", []) or []:
        if isinstance(entry, dict) and entry.get("id") == block_id:
            entry["status"] = new_status
    project.raw_manifest.setdefault("progress", {})["status"] = "draft"
    project.raw_manifest.setdefault("progress", {})["completed_blocks"] = [item.spec.id for item in project.blocks if item.spec.id != block_id]
    project.raw_manifest.setdefault("qa", {})["status"] = "not_run"
    project.save_manifest()
    return target
