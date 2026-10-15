<div align="center">

<img src="assets/readme/ras-cover.png" alt="A finished RAS report showing a designed cover and executive summary" width="920">

# RAS — Report Anything Skill

### Turn a request and its evidence into a report people will actually read.

Six visual themes · Sixteen report archetypes · DOCX + PDF from one canonical model

<a href="#quickstart">Quickstart</a> ·
<a href="#see-it-in-action">See it in action</a> ·
<a href="#design-system">Design system</a> ·
<a href="#evidence-model">Evidence model</a> ·
<a href="#development">Development</a>

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-17202A?style=flat-square&logo=python&logoColor=white)
![Outputs](https://img.shields.io/badge/outputs-DOCX%20%2B%20PDF-117A8B?style=flat-square)
![Themes](https://img.shields.io/badge/themes-6-117A8B?style=flat-square)
![Tests](https://img.shields.io/badge/tests-16%20passing-027A48?style=flat-square)

</div>

<div align="center">

**One request. One canonical model. Two polished outputs.**

<img src="assets/readme/ras-pipeline.svg" alt="RAS pipeline from request and evidence to canonical model, designed outputs, and QA receipt" width="100%">

</div>

## Why RAS

Most report automation stops at text. RAS treats a report as a designed, auditable artifact: it chooses the communication shape, keeps the evidence trail visible, resolves a visual system, renders two formats from the same model, and checks the pages before delivery.

Ask for the outcome in plain language:

> “Compare the options for the board and recommend a path.”

> “Create a KPI review with a clear trend chart.”

> “Turn this research into an evidence-grounded synthesis.”

> “Explain the incident, root cause, impact, and corrective actions.”

RAS turns the request into a structured project with independent Markdown blocks, a source ledger, a visual contract, and a quality receipt.

## See it in action

These previews are rendered from the examples and acceptance fixtures in this repository—not stock mockups.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="Data-forward KPI report with a trend chart"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="Technical report with an original architecture diagram"></td>
  </tr>
  <tr>
    <td align="center"><sub>Data-forward KPI review</sub></td>
    <td align="center"><sub>Technical architecture report</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="Editorial executive brief with a warm paper palette"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="Global growth comparison chart in a RAS report"></td>
  </tr>
  <tr>
    <td align="center"><sub>Editorial executive brief</sub></td>
    <td align="center"><sub>Analytical comparison with chart</sub></td>
  </tr>
</table>

## Install

```bash
git clone https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

The host-facing skill lives at [`skills/ras/SKILL.md`](skills/ras/SKILL.md). Codex and Claude plugin manifests are included in [`.codex-plugin`](.codex-plugin/plugin.json) and [`.claude-plugin`](.claude-plugin/plugin.json).

## Quickstart

Initialize a report project:

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

Edit the generated `manifest.yaml`, `sources.yaml`, and Markdown blocks, then validate, build, and inspect the result:

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf
ras-report qa reports/my-report/manifest.yaml
```

Explore the visual language:

```bash
ras-report theme list
ras-report theme inspect data-forward
```

<details>
<summary><strong>What a report project contains</strong></summary>

```text
reports/my-report/
├── manifest.yaml       # request, style decision, blocks, outputs, QA receipt
├── sources.yaml        # provenance and claim support
├── blocks/*.md         # independent, resumable content units
├── assets/             # supplied or generated visual assets
├── build/              # canonical model and intermediate visuals
├── qa/                 # receipts and rendered page images
└── dist/               # final DOCX and PDF outputs
```

</details>

## What it makes

RAS supports reports that need structure, judgment, and traceability:

| Intent | Useful for |
| --- | --- |
| Executive brief | Senior-management summaries and concise reviews |
| Decision memo | Options, trade-offs, recommendations, and next actions |
| Research synthesis | Evidence-led findings across multiple sources |
| Analytical deep dive | Trends, causes, implications, and interpretation |
| Comparative evaluation | Before/after, option, vendor, or policy comparisons |
| Proposal and roadmap | Business cases, strategies, plans, and milestones |
| KPI and status review | Metrics, charts, progress, and operating cadence |
| Audit, risk, and compliance | Controls, evidence gaps, findings, and mitigations |
| Technical report | Architecture, systems, incidents, and investigations |
| SOP and case study | Repeatable procedures and documented examples |

Sixteen archetypes are available in the router, with explicit overrides when the request already tells RAS what shape it should take.

## How it works

### 1 · Route the request

RAS resolves the archetype, audience, tone, evidence level, page geometry, visual style, density, and emphasis from the request. Explicit user choices win.

### 2 · Build independent blocks

Each block has a stable ID, communication goal, status, source references, layout budget, and optional visual contract. A single block can be regenerated without disturbing the rest of the report.

### 3 · Resolve one design system

The design compiler resolves the theme, brand tokens, semantic components, typography, chart palette, diagram language, spacing, and page rhythm before rendering begins.

### 4 · Render and verify

DOCX and PDF are produced from the same canonical model. QA checks the evidence ledger, output structure, section parity, accessibility metadata, PDF readability, and rendered-page integrity.

## Design system

Themes are not just color presets. They change the report’s hierarchy, cover treatment, semantic panels, tables, charts, diagrams, typography, spacing, and composition rules.

| Theme | Personality | Best for |
| --- | --- | --- |
| `minimal` | Quiet and compact | Short, low-ornament reports |
| `editorial` | Warm and narrative | Executive briefs and story-led work |
| `data-forward` | Crisp and metric-led | KPIs, comparisons, and dashboards |
| `institutional` | Formal and structured | Policy, audit, and compliance |
| `technical` | Blueprint-like and precise | Architecture and operations |
| `narrative` | Expressive and paced | Case studies and long-form synthesis |

A project-level `.ras/brand.yaml` can overlay the theme with brand colors, fonts, spacing, component tokens, chart palettes, and diagram tokens. Inline Markdown formatting—**bold**, *italic*, and `code`—is supported consistently in both output formats.

## Evidence model

User-provided material is the primary evidence. External research is used only when the user requests or clearly authorizes it.

The source ledger records provenance:

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

Blocks cite source records with stable markers:

```markdown
The supported finding is stated here [S1].
```

Validation checks that source references resolve, claims are supported, required visuals have captions and alternative text, unsafe paths are rejected, and unresolved placeholders do not reach the deliverable.

## Visuals and accessibility

Charts accept `bar`, `line`, and `pie` specifications with labels, values, captions, and alternative text. Diagrams use a small semantic grammar and render to original SVG and PNG assets.

Informative visuals receive:

- a visible caption;
- alternative text in the report;
- embedded image metadata in DOCX;
- a deterministic asset in the build model.

The built-in visual pipeline is dependency-light: Pillow and SVG primitives handle charts and diagrams, while ReportLab and python-docx produce the final documents.

## Examples and fixtures

- [`examples/executive-brief`](examples/executive-brief) — editorial management review
- [`examples/kpi-report`](examples/kpi-report) — data-forward chart report
- [`examples/technical-report`](examples/technical-report) — technical report with diagram
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK rendering acceptance fixture
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — evidence-gap behavior fixture
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — sourced global before/after comparison package

Generated `build/`, `qa/`, and `dist/` directories are ignored so source packages stay reviewable and reproducible.

## Development

Run the standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

For a full acceptance pass:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf
ras-report qa examples/executive-brief/manifest.yaml
```

Optional render dependencies are declared in [`pyproject.toml`](pyproject.toml):

```bash
python -m pip install -e ".[render]"
```

## Scope

RAS v1 focuses on paginated DOCX and PDF reports. Presentation decks, web reports, spreadsheet appendices, and collaborative editing workflows are outside the current renderer contract.

## License

See [`LICENSE`](LICENSE).
