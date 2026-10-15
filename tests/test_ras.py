from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ras_engine.build import build_project
from ras_engine.markdown import inline_markup, parse_inline
from ras_engine.models import ReportProject
from ras_engine.project import init_project, regenerate_block
from ras_engine.routing import route_request
from ras_engine.security import UnsafePathError, ensure_within
from ras_engine.validation import has_errors, validate_project


class RoutingTests(unittest.TestCase):
    def test_explicit_override_wins(self) -> None:
        decision = route_request("Compare the options for a board decision", {"archetype": "technical-architecture", "tone": "academic"})
        self.assertEqual(decision.archetype, "technical-architecture")
        self.assertEqual(decision.tone, "academic")

    def test_kpi_routes_to_performance(self) -> None:
        decision = route_request("Create a KPI dashboard with monthly metrics and a trend chart")
        self.assertEqual(decision.archetype, "performance-kpi")
        self.assertEqual(decision.visual_style, "data-forward")


class MarkdownTests(unittest.TestCase):
    def test_inline_markdown_is_parsed_for_renderers(self) -> None:
        spans = parse_inline("**Before COVID:** growth and *inflation* with `2020`")
        self.assertEqual(spans[0].text, "Before COVID:")
        self.assertTrue(spans[0].bold)
        self.assertTrue(any(span.italic for span in spans))
        self.assertTrue(any(span.code for span in spans))

    def test_inline_markup_removes_markers(self) -> None:
        rendered = inline_markup("**Before COVID:** growth")
        self.assertEqual(rendered, "<b>Before COVID:</b> growth")
        self.assertNotIn("**", rendered)


class ProjectTests(unittest.TestCase):
    def test_init_creates_resumable_package(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            manifest = init_project(Path(temp) / "demo", request="Create a status report")
            project = ReportProject.load(manifest)
            self.assertTrue((Path(temp) / "demo" / "sources.yaml").exists())
            self.assertEqual(len(project.blocks), 1)
            self.assertFalse(has_errors(validate_project(project)))

    def test_examples_validate(self) -> None:
        for manifest in [
            ROOT / "examples" / "executive-brief" / "manifest.yaml",
            ROOT / "examples" / "kpi-report" / "manifest.yaml",
            ROOT / "examples" / "technical-report" / "manifest.yaml",
            ROOT / "fixtures" / "traditional-chinese" / "manifest.yaml",
            ROOT / "fixtures" / "insufficient-evidence" / "manifest.yaml",
        ]:
            project = ReportProject.load(manifest)
            issues = validate_project(project)
            self.assertFalse(has_errors(issues), f"{manifest}: {issues}")

    def test_nested_visual_specs_load(self) -> None:
        project = ReportProject.load(ROOT / "examples" / "technical-report" / "manifest.yaml")
        visual = project.blocks[0].spec.visual
        self.assertEqual(len(visual["nodes"]), 4)
        self.assertEqual(visual["edges"][0]["from"], "client")

    def test_unsafe_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            with self.assertRaises(UnsafePathError):
                ensure_within(temp, Path(temp) / ".." / "outside.txt")

    def test_one_block_can_be_reset_without_touching_others(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = ROOT / "examples" / "executive-brief"
            target = Path(temp) / "executive-brief"
            shutil.copytree(source, target)
            original_summary = (target / "blocks" / "executive-summary.md").read_text(encoding="utf-8")
            regenerate_block(target / "manifest.yaml", "decision")
            self.assertEqual(original_summary, (target / "blocks" / "executive-summary.md").read_text(encoding="utf-8"))
            project = ReportProject.load(target / "manifest.yaml")
            self.assertEqual(project.raw_manifest["blocks"][1]["status"], "draft")


@unittest.skipUnless(__import__("importlib.util").util.find_spec("docx") and __import__("importlib.util").util.find_spec("reportlab"), "render dependencies unavailable")
class RenderTests(unittest.TestCase):
    def test_kpi_build_and_qa(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = ROOT / "examples" / "kpi-report"
            target = Path(temp) / "kpi-report"
            shutil.copytree(source, target)
            result = build_project(target / "manifest.yaml", ["docx", "pdf"])
            self.assertTrue(Path(result["outputs"]["docx"]).exists())
            self.assertTrue(Path(result["outputs"]["pdf"]).exists())
            from ras_engine.qa import run_qa

            qa = run_qa(target / "manifest.yaml")
            self.assertTrue(qa["passed"], qa["issues"])

    def test_technical_diagram_builds(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = ROOT / "examples" / "technical-report"
            target = Path(temp) / "technical-report"
            shutil.copytree(source, target)
            result = build_project(target / "manifest.yaml", ["pdf"])
            self.assertTrue(Path(result["outputs"]["pdf"]).exists())
            self.assertTrue((target / "build" / "visuals" / "architecture.png").exists())
            self.assertTrue((target / "build" / "visuals" / "architecture.svg").exists())


if __name__ == "__main__":
    unittest.main()
