"""Command-line interface for `ras-report`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .build import BuildError, build_project
from .design import THEME_PACKS, resolve_design
from .models import ReportProject
from .project import init_project, regenerate_block
from .qa import run_qa
from .planning import DEPTHS, RESEARCH_MODES
from .validation import has_errors, issues_to_text, validate_project
from .templates import get_template, template_ids, template_summary


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ras-report", description="Build evidence-grounded RAS reports.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize a canonical report package")
    init.add_argument("directory", type=Path)
    init.add_argument("--request", default="Create a concise, evidence-grounded report from the supplied material.")
    init.add_argument("--title", default=None)
    init.add_argument("--archetype", default=None)
    init.add_argument("--visual-style", dest="visual_style", default=None)
    init.add_argument("--density", default=None)
    init.add_argument("--tone", default=None)
    init.add_argument("--emphasis", default=None)
    init.add_argument("--evidence-level", dest="evidence_level", default=None)
    init.add_argument("--page-geometry", dest="page_geometry", default=None)
    init.add_argument("--template", dest="template_id", choices=template_ids(), default=None, help="Scaffold a reusable report template")
    init.add_argument("--depth", choices=DEPTHS, default=None, help="Content depth; otherwise infer quick, standard, or deep from the request")
    init.add_argument("--research", choices=RESEARCH_MODES, default=None, help="Research mode; web explicitly authorizes external research")
    init.add_argument("--pages", type=_positive_int, default=None, help="Target page count; adjusts the selected content profile")
    init.add_argument("--force", action="store_true", help="Allow initialization in a non-empty directory")

    validate = sub.add_parser("validate", help="Validate a report manifest and its blocks")
    validate.add_argument("manifest", type=Path)
    validate.add_argument("--json", action="store_true", dest="as_json")

    build = sub.add_parser("build", help="Render DOCX, PDF, and/or PPTX")
    build.add_argument("manifest", type=Path)
    build.add_argument("--formats", default=None, help="Comma-separated formats: docx,pdf,pptx")

    qa = sub.add_parser("qa", help="Run structural and page-level quality assurance")
    qa.add_argument("manifest", type=Path)
    qa.add_argument("--json", action="store_true", dest="as_json")

    plan = sub.add_parser("plan", help="Show the resolved content and research plan")
    plan.add_argument("manifest", type=Path)

    regenerate = sub.add_parser("regenerate", help="Reset or replace one independent block")
    regenerate.add_argument("manifest", type=Path)
    regenerate.add_argument("--block", required=True, dest="block_id")
    regenerate.add_argument("--body-file", type=Path, default=None, help="Optional Markdown body/full block inside the report workspace")

    theme = sub.add_parser("theme", help="Inspect built-in RAS visual themes")
    theme_sub = theme.add_subparsers(dest="theme_command", required=True)
    theme_sub.add_parser("list", help="List available theme packs")
    inspect = theme_sub.add_parser("inspect", help="Print a resolved theme pack")
    inspect.add_argument("theme_id", choices=sorted(THEME_PACKS))

    template = sub.add_parser("template", help="Inspect reusable report templates")
    template_sub = template.add_subparsers(dest="template_command", required=True)
    template_sub.add_parser("list", help="List available report templates")
    template_inspect = template_sub.add_parser("inspect", help="Print a report template blueprint")
    template_inspect.add_argument("template_id", choices=template_ids())
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            overrides = {key: value for key, value in {
                "archetype": args.archetype,
                "visual_style": args.visual_style,
                "density": args.density,
                "tone": args.tone,
                "emphasis": args.emphasis,
                "evidence_level": args.evidence_level,
                "page_geometry": args.page_geometry,
            }.items() if value}
            manifest = init_project(
                args.directory,
                request=args.request,
                title=args.title,
                overrides=overrides,
                template_id=args.template_id,
                depth=args.depth,
                research=args.research,
                pages=args.pages,
                force=args.force,
            )
            print(f"Initialized RAS project: {manifest}")
            return 0
        if args.command == "validate":
            project = ReportProject.load(args.manifest)
            issues = validate_project(project)
            if args.as_json:
                print(json.dumps([issue.to_dict() for issue in issues], ensure_ascii=False, indent=2))
            else:
                print(issues_to_text(issues))
            return 1 if has_errors(issues) else 0
        if args.command == "build":
            formats = [item.strip() for item in args.formats.split(",") if item.strip()] if args.formats else None
            result = build_project(args.manifest, formats)
            print(f"Built {', '.join(result['outputs'])}:")
            for fmt, path in result["outputs"].items():
                print(f"  {fmt}: {path}")
            if result["issues"]:
                print("Warnings:")
                print(issues_to_text(result["issues"]))
            return 0
        if args.command == "qa":
            result = run_qa(args.manifest)
            if args.as_json:
                print(json.dumps(result["receipt"], ensure_ascii=False, indent=2))
            else:
                print(f"QA {'PASS' if result['passed'] else 'FAIL'}: {result['report']}")
                if result["issues"]:
                    print(issues_to_text(result["issues"]))
            return 0 if result["passed"] else 1
        if args.command == "plan":
            project = ReportProject.load(args.manifest)
            print(json.dumps({
                "content_plan": project.raw_manifest.get("content_plan", {}),
                "research": project.raw_manifest.get("research", {}),
            }, ensure_ascii=False, indent=2))
            return 0
        if args.command == "regenerate":
            path = regenerate_block(args.manifest, args.block_id, args.body_file)
            print(f"Prepared block for regeneration: {path}")
            return 0
        if args.command == "theme":
            if args.theme_command == "list":
                for theme_id, pack in THEME_PACKS.items():
                    print(f"{theme_id}: {pack['display_name']}")
                return 0
            print(json.dumps(resolve_design(args.theme_id), ensure_ascii=False, indent=2))
            return 0
        if args.command == "template":
            if args.template_command == "list":
                for template_id in template_ids():
                    item = template_summary(template_id)
                    print(f"{template_id}: {item['display_name']} — {item['description']}")
                return 0
            print(json.dumps(get_template(args.template_id), ensure_ascii=False, indent=2))
            return 0
    except (BuildError, FileExistsError, FileNotFoundError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2
