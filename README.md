# RAS — Report Anything Skill

An agent skill that turns a request and its evidence into a finished, source-aware report.

Six visual themes. Sixteen report archetypes. One canonical model rendered to DOCX and PDF.

[Quickstart](#quickstart) · [What it makes](#what-it-makes) · [How it works](#how-it-works) · [Design system](#design-system) · [Evidence model](#evidence-model) · [Development](#development)

```text
Request + source material
          ↓
  structured report project
          ↓
  validated DOCX + PDF
          ↓
  rendered-page QA receipt
```

## What it makes

Ask for the report in plain language:

- “Write a concise executive brief from these service review notes.”
- “Compare the options and recommend a path for the board.”
- “Turn this research into an evidence-grounded synthesis.”
- “Create a KPI review with a trend chart.”
- “Explain the incident, root cause, impact, and corrective actions.”
- “Produce a technical architecture report with an original diagram.”

RAS routes the request to the right report shape, keeps content in resumable blocks, records source support, and produces a designed deliverable instead of a plain text dump.

| Starting point | RAS output |
| --- | --- |
| Request, notes, files, or approved research | A structured report package |
| Independent Markdown blocks | DOCX and PDF from one canonical model |
| Source ledger and claim references | Visible `[S1]` citations and a source register |
| Visual intent and brand tokens | Theme-aware panels, tables, charts, and diagrams |
| Build receipt | Structural QA and rendered-page integrity checks |

## Install

From a checkout:

```bash
git clone https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

The host-facing skill lives at [`skills/ras/SKILL.md`](skills/ras/SKILL.md). Plugin manifests for Codex and Claude are included in [`.codex-plugin`](.codex-plugin/plugin.json) and [`.claude-plugin`](.claude-plugin/plugin.json).

## Quickstart

Initialize a report project:

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

Edit the generated `manifest.yaml`, `sources.yaml`, and Markdown blocks, then validate and build:

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf
ras-report qa reports/my-report/manifest.yaml
```

Inspect the available visual themes:

```bash
ras-report theme list
ras-report theme inspect data-forward
```

The canonical project layout is:

```text
reports/my-report/
├── manifest.yaml
├── sources.yaml
├── blocks/*.md
├── assets/
├── build/
├── qa/
└── dist/
    ├── my-report.docx
    └── my-report.pdf
```

## How it works

### 1. Route the request

RAS identifies the report archetype and resolves the visual treatment from explicit user signals, report intent, audience, evidence level, and page geometry. Explicit overrides win.

Supported archetypes include executive briefs, decision memos, research syntheses, analytical deep dives, comparisons, proposals, roadmaps, KPI reviews, audits, risk reports, technical architectures, incident postmortems, investigations, SOPs, and case studies.

### 2. Build independent blocks

Every block has a stable ID, communication goal, audience, status, source references, layout budget, and optional visual contract. Blocks can be drafted, validated, regenerated, or replaced without rebuilding the whole content model by hand.

### 3. Resolve one design system

The design compiler resolves theme, brand, density, tone, emphasis, typography, component variants, and page geometry before either renderer runs. DOCX and PDF therefore receive the same design decision instead of drifting into separate templates.

### 4. Render and verify

The build writes a canonical model, renders DOCX and PDF, and records the resolved design receipt. QA validates the evidence ledger, output structure, titles, section parity, accessibility metadata, PDF readability, and rendered-page integrity.

## Design system

Six built-in themes give the report a deliberate visual language:

| Theme | Intent |
| --- | --- |
| `minimal` | Quiet, compact, low-ornament reports |
| `editorial` | Magazine-like hierarchy and narrative pacing |
| `data-forward` | Charts, metrics, dashboards, and comparisons |
| `institutional` | Formal, policy, audit, and compliance work |
| `technical` | Architecture, systems, and operational detail |
| `narrative` | Story-led reports with stronger visual rhythm |

Themes affect more than color. They resolve palette roles, typography, cover treatment, semantic panels, tables, charts, diagrams, spacing, and layout rhythm. A project-level `.ras/brand.yaml` can overlay the theme with brand colors, fonts, spacing, component tokens, chart palettes, and diagram tokens.

The report engine supports inline Markdown formatting in both output formats, including **bold**, *italic*, and `inline code`, while preserving citation markers such as `[S1]`.

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

Blocks cite sources with stable markers:

```markdown
The supported finding is stated here [S1].
```

Validation checks that cited sources exist, claim references resolve, required visuals have captions and alternative text, unsafe paths are rejected, and unresolved placeholders do not reach the deliverable.

## Visuals and accessibility

Charts accept `bar`, `line`, and `pie` specifications with labels, values, captions, and alternative text. Diagrams use a small semantic grammar and render to original SVG and PNG assets rather than relying on a separate diagram service.

Informative visuals receive:

- a visible caption;
- alternative text in the report;
- embedded image metadata in DOCX;
- a deterministic visual asset in the build model.

The built-in visual pipeline is intentionally dependency-light: Pillow and SVG primitives are used for charts and diagrams, while ReportLab and python-docx produce the final outputs.

## Examples and fixtures

- [`examples/executive-brief`](examples/executive-brief) — concise management review
- [`examples/kpi-report`](examples/kpi-report) — data-forward chart report
- [`examples/technical-report`](examples/technical-report) — technical report with diagram
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK rendering acceptance fixture
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — evidence-gap behavior fixture

Generated `build/`, `qa/`, and `dist/` directories are ignored so source packages stay reviewable and reproducible.

## Development

Run the standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

The repository has no mandatory network dependency for rendering. Optional render dependencies are declared in [`pyproject.toml`](pyproject.toml):

```bash
python -m pip install -e ".[render]"
```

For a full acceptance pass:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf
ras-report qa examples/executive-brief/manifest.yaml
```

## Scope

RAS v1 focuses on paginated DOCX and PDF reports. Presentation decks, web reports, spreadsheet appendices, and collaborative editing workflows are intentionally outside the current renderer contract.

## License

See [`LICENSE`](LICENSE).
