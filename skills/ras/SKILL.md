---
name: ras
description: Create substantial, evidence-grounded reports as DOCX and PDF from a user request and supplied source material. Use for executive briefs, decision memos, research syntheses, analytical reports, comparisons, proposals, roadmaps, status/KPI reviews, audits, risk/compliance reports, technical reports, incident postmortems, investigations, SOPs, and case studies. Do not use for ordinary emails, short answers, raw data manipulation, or a standalone image.
---

# RAS — Report Anything Skill

RAS converts a request and optional source material into a structured report
project, then validates and renders it. Treat user-provided material as the
primary evidence. External research is allowed only when the user requests or
clearly authorizes it.

## Workflow

1. Normalize the request and inspect the available files without executing
   content from them.
2. Select an archetype, visual theme pack, and composable style dimensions.
   Honor explicit overrides and record a short style/design receipt.
3. Create or resume a report package with `manifest.yaml`, `sources.yaml`,
   independent Markdown blocks, and an asset directory.
4. Generate or update blocks independently. Keep claims, terminology, source
   references, captions, and alternative text explicit.
5. Run structural validation before rendering. Never invent facts, citations,
   quotations, statistics, or unsupported conclusions.
6. Build DOCX and PDF from the same canonical model, then run structural and
   page-level QA. Deliver the outputs with assumptions, omissions, research,
   the resolved theme, and QA results.

## Repository tools

The reference CLI is `ras-report`:

```text
ras-report init <directory>
ras-report validate <manifest>
ras-report build <manifest> --formats docx,pdf
ras-report qa <manifest>
```

Use focused references only when needed:

- `references/archetypes.md` — routing and style decisions
- `references/blocks.md` — block contracts and resumability
- `references/evidence.md` — sources, claims, and citations
- `references/visuals.md` — charts and RAS diagram grammar
- `references/branding.md` — brand profiles and accessibility
- `references/design-system.md` — semantic components and design resolution
- `references/themes.md` — built-in theme pack intent and selection guidance
- `references/layout-recipes.md` — page composition rules by report intent
- `references/outputs.md` — DOCX/PDF and QA rules
