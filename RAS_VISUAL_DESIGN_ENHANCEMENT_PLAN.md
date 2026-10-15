# RAS Visual Design Enhancement Plan

## 1. Outcome

Upgrade RAS from a structurally correct report generator into a design-led
publishing system that produces polished, distinctive, brandable DOCX and PDF
reports without weakening evidence controls, accessibility, or resumability.

The enhancement keeps the existing six `visual_style` values, but makes each
one materially different in typography, composition, page furniture,
component variants, chart language, and diagram treatment. User brand profiles
remain an overlay rather than a replacement for the report design system.

The default result should feel intentionally art-directed even when the user
provides no brand profile or design instructions.

## 2. Current-state diagnosis

The present implementation is visually plain for architectural reasons, not
because the colors need minor adjustment:

1. The six visual styles are routing labels only. They do not select different
   layout recipes, typography systems, covers, component variants, or page
   furniture.
2. The brand profile exposes a small token set, but most of those tokens are
   not consumed by the renderers.
3. Both formats use one linear flow: centered title, heading, paragraph, basic
   table or image, sources, quality receipt.
4. There is no semantic component library for key findings, KPI cards,
   recommendations, risks, pull quotes, timelines, decision matrices, or
   section openers.
5. Page composition is not modeled. There are no grids, columns, sidebars,
   bands, section-level geometry, or visual hierarchy budgets.
6. Charts support only basic single-series bar, line, and pie forms with fixed
   axes, labels, and decoration.
7. Diagram families share nearly the same box-and-arrow treatment; the family
   name does not yet produce a family-specific layout.
8. Font handling prioritizes availability over art direction. PDF uses one
   general fallback and charts/diagrams use Pillow's default bitmap font.
9. QA proves that files open and render, but does not measure visual quality,
   layout rhythm, overfull pages, hierarchy, or regression against approved
   page designs.

The remedy is a theme compiler, semantic component system, and page-layout IR;
adding more color values to the current renderers would not be sufficient.

## 3. Product principles

- **Design is semantic.** A finding, decision, risk, metric, quote, and source
  register receive different visual treatments because they communicate
  different things.
- **Themes are coherent systems.** Typography, spacing, geometry, charts,
  diagrams, tables, and page furniture change together.
- **Branding overlays themes.** Brand colors, fonts, logo, and attribution are
  applied to a proven theme without erasing its layout logic.
- **Content remains canonical.** DOCX and PDF consume the same semantic report
  and layout intent; format-specific renderers may degrade gracefully where a
  feature is unsafe in Word.
- **Decoration must earn its place.** Visual richness may improve hierarchy,
  orientation, recall, or comprehension; it may not imply evidence or make a
  sparse report look more certain.
- **Accessibility is part of the design.** Contrast, minimum type sizes,
  reading order, alt text, grayscale legibility, and non-color cues are design
  requirements.
- **Offline rendering remains deterministic.** Renderers perform no network
  access. Fonts, templates, and icons used at build time are local and
  licensed.

## 4. Target visual styles

The existing identifiers stay stable for compatibility. Each becomes a
built-in theme pack with distinct composition rules.

| Style | Visual identity | Default composition | Best fit |
|---|---|---|---|
| `minimal` | Quiet sans-serif system, one accent, fine rules, generous whitespace | Compact cover, single-column body, restrained callouts | Briefs, policies, general professional reports |
| `editorial` | Serif display headings, sans body, asymmetric title pages, pull quotes and folio details | Editorial cover, wider opening paragraphs, occasional side notes | Research, case studies, public-facing narratives |
| `data-forward` | Dense but clean sans typography, KPI cards, strong chart hierarchy, tabular numerals | Dashboard opening, card grid, full-width charts, analytic annotations | KPI, performance, comparative and analytical reports |
| `institutional` | Formal navy/slate palette, numbered sections, conservative rules and headers | Branded cover, running header, strict grid, formal tables | Audit, compliance, governance, board materials |
| `technical` | Structured grid, slate/cyan palette, mono labels, code and specification panels | Architecture cover, section index, two-column specifications, large diagrams | Architecture, engineering, incident and investigation reports |
| `narrative` | Strong chapter openers, larger display type, controlled imagery, quote and milestone emphasis | Hero cover, chapter dividers, alternating text/visual rhythm | Strategy, roadmap, proposal and case-study reports |

Theme selection remains independent from archetype. For example, a decision
memo may be `minimal`, `institutional`, or `data-forward` depending on audience
and evidence shape.

## 5. Design-system architecture

### 5.1 Theme packs

Add versioned theme files under `skills/ras/assets/themes/` and make them
available to the Python package as package data. A theme contains complete
design behavior, not only colors.

Proposed contract:

```yaml
schema_version: 2
id: editorial
display_name: Editorial
palette:
  paper: "#FCFBF8"
  surface: "#F2EFE8"
  ink: "#202124"
  muted: "#64615B"
  accent: "#9A3E32"
  accent_soft: "#F4E5E1"
  positive: "#287A55"
  warning: "#9B6500"
  negative: "#A43A36"
typography:
  display: Source Serif 4
  heading: Source Serif 4
  body: Source Sans 3
  mono: IBM Plex Mono
  cjk: Noto Sans CJK TC
  scale: {display: 32, h1: 20, h2: 14, body: 10, caption: 8}
page:
  size: A4
  margins: {top: 18, right: 18, bottom: 20, left: 22}
  grid: {columns: 12, gutter: 5}
  header_variant: folio
  footer_variant: source-line
components:
  cover: editorial-asymmetric
  executive_summary: opening-deck
  key_finding: margin-rule
  recommendation: accent-band
  table: editorial-rules
  source_register: compact-register
charts:
  palette: ["#9A3E32", "#355C7D", "#5C7A5A", "#B28345"]
  grid: horizontal-light
  label_policy: direct
diagrams:
  node_variant: editorial-card
  connector_variant: fine-orthogonal
```

Create six complete built-in themes plus a neutral compatibility theme. Themes
may `extends` another theme to avoid duplicated tokens, but the compiled theme
must be fully resolved before rendering.

### 5.2 Brand profiles v2

Separate brand identity from report theme. A brand profile may override:

- Primary, secondary, neutral, semantic, and data-series color ramps
- Display, heading, body, mono, and CJK fonts with explicit fallback chains
- Primary/reversed/monochrome logos, minimum size, clear space, and placement
- Organization name, legal line, attribution, confidentiality, and document ID
- Corner radius, rule weight, icon style, table density, and chart defaults
- Cover image policy, image treatment, and co-branding behavior
- Print-safe and grayscale alternatives

Resolution order becomes:

1. Built-in base theme selected by `visual_style`
2. Archetype layout recipe
3. Density, tone, emphasis, evidence level, and geometry modifiers
4. Project brand profile
5. Explicit report or block presentation overrides
6. Renderer-safe fallback with a recorded explanation

### 5.3 Theme compiler

Add a deterministic compiler that converts the layers above into a
`ResolvedDesign` object. It must:

- Resolve inheritance and fallback values
- Normalize colors, lengths, and font chains
- Generate tonal ramps when only a primary color is supplied
- Check text, UI, chart, and diagram contrast
- Select format-safe fonts and record substitutions
- Derive component variants and chart/diagram palettes
- Produce a design receipt with theme, brand, overrides, substitutions, and
  accessibility results

The renderers consume only `ResolvedDesign`; they must not contain hard-coded
theme colors or typography beyond emergency fallbacks.

### 5.4 Canonical layout IR

Introduce an intermediate layout model between content blocks and renderers.
It should describe semantic page intent without leaking DOCX or ReportLab
internals.

Core types:

- `DocumentPlan`: page size, margins, grid, master pages, section sequence
- `SectionPlan`: opener variant, geometry, columns, page-break policy
- `ComponentPlan`: semantic component, variant, span, priority, keep policy
- `TextRun`: emphasis, citation, link, language, direction
- `TablePlan`: widths, alignment, header, column roles, split policy
- `FigurePlan`: source, crop, placement, caption, alt text, credit
- `ChartPlan` and `DiagramPlan`: data/specification plus resolved visual tokens
- `PageFurniture`: running header, footer, folio, confidentiality, source line

Blocks gain optional renderer-independent presentation hints:

```yaml
presentation:
  component: key-finding
  variant: accent
  span: 6
  emphasis: primary
  break_before: false
  keep_together: true
```

The system remains usable without hints; archetype recipes choose defaults.

## 6. Semantic component library

Implement reusable components with theme-specific variants:

- Cover, compact cover, and hero cover
- Contents and section divider
- Executive-summary deck
- Key-finding, insight, implication, and evidence-gap callouts
- Recommendation, decision, and action strips
- KPI card, delta card, progress card, and metric group
- Comparison matrix and option scorecard
- Risk card, risk register, and likelihood/impact matrix
- Timeline, roadmap, milestone, and action-plan table
- Quote, pull quote, case-study sidebar, and narrative highlight
- Methodology, limitations, assumption, and warning panels
- Architecture/specification panel and code block
- Source register, footnote/endnote, image credit, and quality receipt

Each component must define:

- Semantic purpose and permitted content
- Default variants per theme and archetype
- Minimum/maximum content budgets
- Grid span and break behavior
- DOCX-safe rendering strategy
- PDF reference rendering strategy
- Accessibility behavior and text alternative requirements

Components replace renderer-specific special cases. A recommendation is
planned once, then rendered as a stable Word table/band or a vector PDF panel.

## 7. Page composition and layout recipes

Create archetype recipes that map report structure to components and grids.
Recipes should be composable, not fixed templates.

Examples:

- Executive brief: compact cover, summary deck, three key findings, action band
- Decision memo: decision statement, criteria strip, option cards, comparison
  matrix, recommendation, risks
- KPI review: dashboard opener, KPI cards, trend charts, driver analysis,
  owner/action table
- Technical report: architecture opener, full-width diagram, specification
  panels, interface tables, operational considerations
- Incident postmortem: impact band, timeline, causal diagram, contributing
  factors, corrective-action register
- Audit report: opinion/assessment panel, findings cards, severity register,
  remediation plan
- Strategy/roadmap: ambition statement, strategic pillars, phased roadmap,
  measures and dependencies

Layout features required in v2:

- 12-column grid for PDF and logical grid mapping for DOCX
- One- and two-column sections
- Full-width, half-width, and sidebar components
- Section-level portrait/landscape switching
- Master pages and running page furniture
- Section openers and intentional page breaks
- Keep-with-next/together rules and predictable table splitting
- Widow/orphan control and minimum bottom-of-page remainder
- Content-density budgets that trigger alternate variants or page breaks

## 8. Typography and fonts

Add a font manager with deterministic resolution and language-aware fallback.

Recommended redistributable font families, subject to license review:

- Source Sans 3 for professional body text
- Source Serif 4 for editorial display text
- IBM Plex Sans/Mono for technical treatments
- Noto Sans CJK TC for Traditional Chinese coverage

Requirements:

- Store licenses in `THIRD_PARTY_LICENSES.md`
- Embed fonts in PDF and chart/diagram exports where licensing permits
- Use DOCX theme fonts and optionally embedded fonts; otherwise record a safe
  substitution
- Support tabular numerals, small caps where available, language-specific line
  wrapping, and minimum type sizes
- Use an explicit typographic scale, line height, paragraph measure, and spacing
  rhythm per theme

## 9. Chart engine v2

Replace fixed chart drawing with a declarative chart specification and a
vector-first renderer. Matplotlib is the preferred reference engine because it
supports reliable axes, typography, SVG/PDF export, and annotation.

Initial chart families:

- Vertical and horizontal bar
- Grouped and stacked bar
- Line and area
- Scatter and bubble
- Donut only when part-to-whole is genuinely useful
- Waterfall
- Bullet/progress chart
- Heatmap
- Small multiples and sparklines

Capabilities:

- Multiple series, legends, direct labels, annotations, targets, uncertainty,
  reference bands, and source notes
- Numeric, percentage, currency, date, and compact-number formatting
- Theme-aware palettes with color-blind-safe defaults
- Pattern, marker, and label redundancy so color is not the only signal
- Automatic label collision handling and sensible axis bounds
- Transparent/vector export for PDF and high-resolution PNG/SVG for DOCX
- Chart accessibility summary generated from the plotted data
- Validation that displayed values, labels, units, and citations match the
  source data

Avoid 3D charts, decorative gauges, and unsupported smoothing.

## 10. Diagram engine v2

Give each semantic family a real layout algorithm and component vocabulary.

- Flow/process: ranked layout, gateways, starts/ends, swimlanes
- Hierarchy/org: level alignment, manager grouping, compact and radial options
- Timeline/roadmap: date scale, phases, milestones, dependencies
- Lifecycle: circular/radial stages with a clear reading order
- Architecture: containers, systems, boundaries, interfaces, trust zones
- Relationship: hubs, clusters, labelled relationships
- Comparison: parallel structures and aligned attributes
- Matrix: quadrant labels, axes, items, thresholds
- Cause/effect: causal chain and fishbone-style grouping

Add:

- Family-specific node shapes and semantic icons
- Group/container backgrounds and labelled boundaries
- Edge labels, ports, line routing, and collision avoidance
- Complexity budgets with overview/detail splitting
- Theme-aware node/connector variants
- Consistent typography using the font manager
- SVG as the canonical diagram output, with PNG generated from the same model

## 11. Imagery and iconography

Add an optional art-direction layer while retaining the current authorization
rules.

- User-provided imagery remains first priority
- Define cover, hero, inline, and background image roles
- Support focal-point cropping, safe text zones, tint/duotone overlays, credits,
  and print-safe conversion
- Supply a small original semantic icon set for findings, actions, risks,
  evidence, time, systems, and people
- Do not use generic decorative imagery when a chart, diagram, or strong
  typographic composition communicates better
- Generated or sourced imagery remains opt-in and must record provenance

## 12. Renderer upgrades

### PDF

Treat PDF as the reference-quality renderer:

- Build page masters, grids, columns, panels, rules, backgrounds, and vector
  components directly through ReportLab
- Register and embed resolved fonts
- Embed chart and diagram vector output where supported
- Implement section geometry changes and master-page variants
- Add internal links for contents and cross-references
- Preserve accessible reading order as far as the PDF library permits; record
  limitations in the quality receipt

### DOCX

Prioritize visual quality with Word-native stability:

- Use theme styles, section breaks, controlled tables, paragraph borders,
  shading, tabs, columns, headers, and footers
- Build covers and component bands from stable table/paragraph structures
- Use floating shapes only when their behavior is verified across Word and
  LibreOffice; otherwise use inline/table-based composition
- Implement explicit table widths, repeat headers, row-split policies, and cell
  padding
- Map PDF-only variants to documented DOCX-safe variants
- Preserve native editability for text, tables, captions, and headings

Cross-format parity means equivalent hierarchy and meaning, not pixel-identical
pages.

## 13. Schema and migration

Introduce `schema_version: 2` for the manifest, block presentation hints, brand
profiles, chart specifications, and diagrams. Do not reinterpret v1 silently.

Add:

```text
ras-report migrate <manifest> --to 2
ras-report theme list
ras-report theme inspect <theme-or-brand>
ras-report preview <manifest> --theme <id> --pages 1,2
```

Migration behavior:

- Preserve content, evidence, output settings, and block IDs
- Map current colors/fonts into a v2 brand overlay
- Map `visual_style` to the corresponding built-in theme
- Translate current chart/diagram specs where possible
- Record unsupported values and renderer fallbacks
- Write a migration receipt and keep a recoverable copy of the original files

## 14. Quality assurance v2

Extend QA from structural correctness to visual confidence.

### Automated checks

- Resolve and validate every theme/brand token
- WCAG contrast checks for all text/background and chart combinations
- Font availability, substitution, embedding, and missing-glyph checks
- Page overflow, clipping, overlap, and out-of-bounds detection
- Minimum font size and line-height checks
- Heading hierarchy, reading order, keep rules, widows, and orphans
- Table width, split, repeated-header, and dense-cell checks
- Figure resolution, crop, caption, alt text, and credit checks
- Chart-data parity, axis/label completeness, and color-only encoding checks
- Diagram collisions, unreadable labels, unconnected nodes, and complexity
  budgets
- Cross-format semantic parity for sections, components, tables, visuals,
  captions, claims, and sources

### Visual regression

- Store approved reference-page PNGs for representative fixtures
- Render test pages at a fixed resolution and compare using perceptual/image
  difference thresholds
- Produce diff images when a threshold fails
- Require human approval when an intentional design change updates a baseline

### Human review rubric

Score representative pages from 1–5 on hierarchy, balance, typography,
information density, consistency, chart clarity, diagram clarity, and brand
fit. A release candidate should average at least 4 with no category below 3.

## 15. Representative test matrix

Required golden fixtures:

1. Two-page executive brief in `minimal` and `editorial`
2. Decision memo with option cards and comparison matrix
3. Research synthesis with citations, pull quote, and source register
4. KPI report with cards, multi-series charts, targets, and annotations
5. Technical report with architecture boundaries and interface table
6. Audit report with severity findings and remediation ownership
7. Incident postmortem with timeline and cause/effect diagram
8. Strategy/roadmap with phases, milestones, and dependencies
9. Traditional Chinese report using CJK typography and wrapping
10. Custom-branded report with logo and font/color overrides
11. Sparse-evidence report that looks deliberate without overstating certainty
12. Dense appendix with long tables and page splitting

Run all six themes against a smaller cross-theme fixture to prove that each
theme produces a materially different but valid result.

## 16. Repository changes

Proposed structure:

```text
skills/ras/
├── SKILL.md
├── references/
│   ├── design-system.md
│   ├── themes.md
│   ├── layout-recipes.md
│   ├── charts.md
│   ├── diagrams.md
│   └── branding.md
└── assets/
    ├── themes/*.yaml
    ├── icons/*.svg
    └── fonts/<family>/
src/ras_engine/
├── design/
│   ├── models.py
│   ├── compiler.py
│   ├── themes.py
│   ├── fonts.py
│   ├── color.py
│   └── migration.py
├── layout/
│   ├── ir.py
│   ├── planner.py
│   ├── recipes.py
│   └── pagination.py
├── components/
│   ├── registry.py
│   └── <component modules>
├── visuals/
│   ├── charts.py
│   ├── diagrams.py
│   ├── imagery.py
│   └── icons.py
├── renderers/
│   ├── base.py
│   ├── pdf.py
│   ├── docx.py
│   └── ooxml.py
└── qa/
    ├── structural.py
    ├── accessibility.py
    ├── visual.py
    └── regression.py
schemas/
├── v1/
└── v2/
tests/
├── unit/
├── integration/
├── golden/
└── fixtures/
```

Keep `SKILL.md` concise. Following the skill-creator guidance, detailed design,
theme, chart, diagram, and branding rules should live in focused references and
be loaded only when relevant.

## 17. Delivery phases and gates

### Phase 0 — Baseline and art direction

Deliver:

- Current-output baseline gallery
- One-page design brief for each of the six themes
- Low-fidelity page wireframes for the key archetypes
- Visual quality rubric and approved reference direction

Gate: the themes are visibly different before renderer code is rewritten.

### Phase 1 — Design contracts and migration

Deliver:

- v2 schemas and typed design/layout models
- Theme/brand compiler and token validation
- Six built-in theme packs plus compatibility theme
- Font manager and license inventory
- v1-to-v2 migration command and tests

Gate: any valid v2 manifest resolves to a complete `ResolvedDesign` without
renderer defaults.

### Phase 2 — Layout IR and component library

Deliver:

- Canonical layout IR and archetype recipe engine
- Cover, page furniture, summary, finding, KPI, recommendation, risk, table,
  timeline, source, and quality components
- Content-budget and pagination decisions recorded in the build model

Gate: fixtures compile into renderer-independent page/component plans.

### Phase 3 — Visual engines

Deliver:

- Chart specification v2 and vector-first chart renderer
- Family-specific diagram layouts
- Local icon system and image-treatment pipeline
- Data/visual validation and accessibility summaries

Gate: chart and diagram fixtures pass data parity, collision, contrast, and
visual-regression tests.

### Phase 4 — PDF reference renderer

Deliver:

- Page masters, grids, columns, section geometry, vector visuals, font
  embedding, links, and all component variants
- Reference-quality golden pages for the acceptance fixtures

Gate: PDF fixture gallery passes automated QA and the human design rubric.

### Phase 5 — DOCX renderer parity

Deliver:

- DOCX-safe equivalents of every required component
- Theme styles, section layouts, headers/footers, tables, captions, and visual
  placement
- Word and LibreOffice compatibility checks

Gate: DOCX files open without repair, remain editable, and retain equivalent
hierarchy/meaning without clipping or unstable floating content.

### Phase 6 — QA, skill guidance, and release

Deliver:

- Full visual-regression and cross-format parity suite
- Updated focused skill references and examples
- Theme preview CLI and gallery
- Renderer/design receipts and migration documentation
- Final accessibility, license, security, and packaging review

Gate: all release acceptance criteria below pass.

## 18. Release acceptance criteria

A visual-design v2 release is complete only when:

- The same fixture rendered in all six themes is unmistakably different in
  typography, composition, components, charts, and page furniture.
- Every archetype has a tested layout recipe and sensible theme-independent
  fallback.
- A report with no supplied brand still looks intentionally designed.
- Brand overrides do not break contrast, hierarchy, or chart legibility.
- PDF uses embedded, consistent fonts and vector charts/diagrams where
  supported.
- DOCX remains editable, opens without repair, and has no unstable or clipped
  content in supported office suites.
- No heading, table, component, image, chart, or diagram crosses its bounds.
- Charts reproduce source values and units exactly; diagrams do not invent
  relationships.
- Essential information is never communicated by color alone.
- Traditional Chinese fixtures have correct glyphs, line breaks, punctuation,
  and fallback fonts.
- Sparse-evidence reports clearly expose uncertainty without looking broken.
- Cross-format semantic parity passes for all fixtures.
- Golden-page visual diffs pass or have an explicit approved baseline update.
- The quality receipt records theme, brand, fonts, substitutions, layout
  fallbacks, accessibility results, and renderer versions.

## 19. Risks and mitigations

| Risk | Mitigation |
|---|---|
| DOCX cannot reproduce every PDF composition | Define DOCX-safe component variants and test them as first-class designs, not degraded screenshots |
| Too many combinations become untestable | Compile dimensions into a small variant set and use pairwise/combinatorial fixture coverage |
| Brand overrides create inaccessible results | Validate resolved colors and generate or require accessible alternatives |
| Bundled fonts increase repository size or licensing complexity | Use a small, audited open-font set and make CJK packs optional if packaging requires it |
| Decorative design obscures evidence | Keep semantic component rules and evidence checks independent from theme selection |
| Visual regression becomes brittle | Compare selected golden pages with perceptual thresholds and require review only for meaningful changes |
| Renderer logic diverges | Share the layout IR, component registry, resolved design, and visual assets; keep renderer code limited to format mapping |

## 20. Recommended first implementation slice

Start with one vertical slice rather than all components at once:

1. Implement theme compiler, font manager, and layout IR.
2. Build `minimal`, `editorial`, and `data-forward` themes.
3. Implement cover, executive summary, key finding, KPI card, table, chart,
   source register, and page furniture components.
4. Render the executive-brief and KPI fixtures in PDF and DOCX.
5. Establish golden-page QA and visual review.
6. Add the remaining themes, archetypes, diagrams, and components on the proven
   architecture.

This slice tests the hardest architectural assumptions early: real theme
differentiation, reusable components, cross-format mapping, typography, data
visualization, and visual regression.

## 21. Planning assumptions

- DOCX and PDF remain the v2 output targets; PPTX and web output stay in later
  phases.
- The existing six `visual_style` identifiers remain stable.
- The built-in default becomes a polished professional theme while preserving
  a compatibility theme for users who want the current understated output.
- Rendering remains local and offline.
- The visual system is original and does not depend on another diagram or
  report-design skill.
- No user choice blocks planning. Brand personality, exact font families, and
  the preferred default theme can be finalized during Phase 0 art direction.
