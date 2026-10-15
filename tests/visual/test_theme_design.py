from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ras_engine.charts import render_chart
from ras_engine.design import THEME_PACKS, design_signature, resolve_design
from ras_engine.layout import plan_project
from ras_engine.models import ReportProject


class ThemeDesignTests(unittest.TestCase):
    def test_all_theme_packs_have_distinct_layout_intent(self) -> None:
        self.assertEqual(set(THEME_PACKS), {"minimal", "editorial", "data-forward", "institutional", "technical", "narrative"})
        covers = {theme["components"]["cover"] for theme in THEME_PACKS.values()}
        accents = {theme["palette"]["accent"] for theme in THEME_PACKS.values()}
        headers = {theme["page"]["header"] for theme in THEME_PACKS.values()}
        self.assertEqual(len(covers), 6)
        self.assertEqual(len(accents), 6)
        self.assertEqual(len(headers), 6)

    def test_resolver_keeps_density_tone_and_emphasis_receipt(self) -> None:
        design = resolve_design("editorial", density="concise", tone="executive", emphasis="evidence-first")
        self.assertEqual(design["theme_id"], "editorial")
        self.assertEqual(design["density"], "concise")
        self.assertEqual(design["tone"], "executive")
        self.assertEqual(design["emphasis"], "evidence-first")
        self.assertEqual(design["components"]["finding"], "evidence-callout")
        self.assertEqual(design["receipt"]["custom_brand"], False)

    def test_brand_overlay_changes_palette_without_erasing_theme_components(self) -> None:
        design = resolve_design(
            "technical",
            {"name": "Acme", "colors": {"accent": "#7A1FA2"}, "components": {"summary": "custom-summary"}},
            custom_brand=True,
        )
        self.assertEqual(design["palette"]["accent"], "#7A1FA2")
        self.assertEqual(design["components"]["summary"], "custom-summary")
        self.assertEqual(design["components"]["finding"], "technical-note")
        self.assertEqual(design["resolved_brand"], "Acme")

    def test_chart_pixels_follow_resolved_theme(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            spec = {"kind": "bar", "title": "Theme test", "labels": ["A", "B"], "values": [1, 2]}
            first = render_chart(spec, temp, "minimal", resolve_design("minimal"))
            second = render_chart(spec, temp, "editorial", resolve_design("editorial"))
            self.assertNotEqual(Path(first["svg"]).read_text(encoding="utf-8"), Path(second["svg"]).read_text(encoding="utf-8"))
            self.assertNotEqual(Path(first["png"]).read_bytes(), Path(second["png"]).read_bytes())

    def test_layout_plan_and_signature_are_theme_sensitive(self) -> None:
        editorial = ReportProject.load(ROOT / "examples" / "executive-brief" / "manifest.yaml")
        technical = ReportProject.load(ROOT / "examples" / "technical-report" / "manifest.yaml")
        editorial_plan = plan_project(editorial).to_dict()
        technical_plan = plan_project(technical).to_dict()
        self.assertEqual(editorial_plan["theme_id"], "editorial")
        self.assertEqual(technical_plan["theme_id"], "technical")
        self.assertNotEqual(design_signature(editorial.design), design_signature(technical.design))
        self.assertTrue(editorial_plan["sections"][0]["component"]["keep_together"])
