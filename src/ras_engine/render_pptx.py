"""Native editable PPTX renderer backed by the bundled Artifact Tool runtime."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from .markdown import parse_markdown, plain_text
from .models import ReportProject


class RenderError(RuntimeError):
    """Raised when the optional PPTX runtime is unavailable or fails."""


def render_pptx(project: ReportProject, output_path: str | Path, visuals: dict[str, dict[str, str]] | None = None) -> Path:
    """Render a report into an editable PPTX and validate it with the finalizer."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    node = _find_node()
    artifact_tool = _find_artifact_tool()
    skill_dir = _find_presentations_skill()
    if not node:
        raise RenderError("PPTX output requires Node.js. Set RAS_NODE to the bundled Node executable.")
    if not artifact_tool:
        raise RenderError("PPTX output requires @oai/artifact-tool. Set RAS_NODE_MODULES or RAS_ARTIFACT_TOOL to the bundled runtime.")
    if not skill_dir:
        raise RenderError("PPTX finalization requires the Presentations skill. Set RAS_PRESENTATIONS_SKILL_DIR to its skills/presentations directory.")

    build_root = project.root / "build" / "pptx"
    run_dir = build_root / f"run-{uuid.uuid4().hex}"
    staging_dir = run_dir / "staging"
    preview_dir = run_dir / "preview"
    finalizer_root = Path(tempfile.mkdtemp(prefix="ras-pptx-finalizer-"))
    finalizer_staging_dir = finalizer_root / "staging"
    finalizer_final_dir = finalizer_root / "final"
    for directory in (staging_dir, preview_dir, finalizer_staging_dir, finalizer_final_dir):
        directory.mkdir(parents=True, exist_ok=True)
    payload_path = run_dir / "payload.json"
    candidate_path = finalizer_staging_dir / "candidate.pptx"
    finalized_path = finalizer_final_dir / output.name
    payload = _payload(project, visuals or {}, preview_dir, candidate_path, finalized_path, skill_dir, finalizer_root)
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    script = Path(__file__).with_name("pptx_renderer.mjs")
    environment = os.environ.copy()
    environment["RAS_ARTIFACT_TOOL"] = str(artifact_tool)
    environment["RAS_PYTHON"] = sys.executable
    runtime_modules = environment.get("RAS_NODE_MODULES")
    if runtime_modules:
        environment["RUNTIME_NODE_MODULES"] = runtime_modules
        environment["CODEX_PRIMARY_RUNTIME_NODE_MODULES"] = runtime_modules
    command = [node, str(script), "--input", str(payload_path), "--skill-dir", str(skill_dir)]
    completed = subprocess.run(command, cwd=run_dir, env=environment, capture_output=True, text=True)
    if completed.returncode != 0:
        receipt_path = candidate_path.parent / "pptx-validation.json"
        if not _valid_finalizer_receipt(finalized_path, receipt_path):
            detail = "\n".join(part for part in (completed.stderr, completed.stdout) if part).strip() or "PPTX renderer failed"
            raise RenderError(detail[-4000:])
    if not finalized_path.exists():
        raise RenderError(f"PPTX finalizer did not produce {finalized_path}")
    shutil.copy2(finalized_path, output)
    shutil.rmtree(finalizer_root, ignore_errors=True)
    return output


def _valid_finalizer_receipt(finalized_path: Path, receipt_path: Path) -> bool:
    """Accept a completed finalizer publish even if Artifact Tool exits after its sidecar log."""

    if not finalized_path.exists() or not receipt_path.exists():
        return False
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return receipt.get("schemaVersion") == "presentation-finalization.v1" and bool(receipt.get("finalSha256"))


def _payload(project: ReportProject, visuals: dict[str, dict[str, str]], preview_dir: Path, candidate_path: Path, finalized_path: Path, skill_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    for block in project.blocks:
        elements = parse_markdown(block.body)
        blocks.append({
            "id": block.spec.id,
            "type": block.spec.type,
            "title": block.spec.title,
            "goal": block.spec.goal,
            "source_refs": block.spec.source_refs,
            "visual": block.spec.visual,
            "presentation": block.spec.presentation,
            "body": block.body,
            "plain_text": plain_text(elements),
            "elements": [
                {
                    "kind": element.kind,
                    "text": element.text,
                    "items": element.items or [],
                    "rows": element.rows or [],
                    "level": element.level,
                }
                for element in elements
            ],
            "visual_asset": visuals.get(block.spec.id, {}),
        })
    source_rows = [
        {
            "id": source.id,
            "title": source.title,
            "publisher": source.publisher,
            "author": source.author,
            "url": source.url,
            "file": source.file,
            "publication_date": source.publication_date,
        }
        for source in project.sources
    ]
    return {
        "title": project.title,
        "report_id": project.report_id,
        "style": project.style.to_dict(),
        "design": project.design,
        "blocks": blocks,
        "sources": source_rows,
        "claims": [claim.to_dict() for claim in project.claims],
        "assumptions": project.raw_manifest.get("assumptions", []) or [],
        "omitted_material": project.raw_manifest.get("omitted_material", []) or [],
        "preview_dir": str(preview_dir),
        "candidate_path": str(candidate_path),
        "finalized_path": str(finalized_path),
        "workspace_dir": str(workspace_dir),
        "skill_dir": str(skill_dir),
    }


def _find_node() -> str | None:
    configured = os.environ.get("RAS_NODE")
    if configured and Path(configured).exists():
        return configured
    found = shutil.which("node") or shutil.which("node.exe")
    if found:
        return found
    candidates = [
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node" / "bin" / "node.exe",
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node" / "bin" / "node",
    ]
    return next((str(path) for path in candidates if path.exists()), None)


def _find_artifact_tool() -> str | None:
    configured = os.environ.get("RAS_ARTIFACT_TOOL")
    if configured and Path(configured).exists():
        return configured
    modules = os.environ.get("RAS_NODE_MODULES")
    if modules:
        candidate = Path(modules) / "@oai" / "artifact-tool" / "dist" / "artifact_tool.mjs"
        if candidate.exists():
            return str(candidate)
    candidates = [
        Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node" / "node_modules" / "@oai" / "artifact-tool" / "dist" / "artifact_tool.mjs",
    ]
    return next((str(path) for path in candidates if path.exists()), None)


def _find_presentations_skill() -> Path | None:
    configured = os.environ.get("RAS_PRESENTATIONS_SKILL_DIR")
    if configured and (Path(configured) / "container_tools" / "artifact_tool_utils.mjs").exists():
        return Path(configured)
    base = Path.home() / ".codex" / "plugins" / "cache" / "openai-primary-runtime" / "presentations"
    if base.exists():
        matches = sorted(base.glob("*/skills/presentations"), reverse=True)
        for match in matches:
            if (match / "container_tools" / "artifact_tool_utils.mjs").exists():
                return match
    return None


__all__ = ["RenderError", "render_pptx"]
