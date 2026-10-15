# Archetypes and style routing

RAS supports these primary archetypes:

`executive-brief`, `decision-memo`, `research-synthesis`, `analytical-deep-dive`,
`comparative-evaluation`, `proposal-business-case`, `strategy-roadmap`,
`status-progress`, `performance-kpi`, `audit-assessment`, `compliance-risk`,
`technical-architecture`, `incident-postmortem`, `investigation-root-cause`,
`policy-sop`, and `case-study`.

Style dimensions are independent: visual style (`minimal`, `editorial`,
`data-forward`, `institutional`, `technical`, `narrative`), density
(`concise`, `standard`, `deep`), tone (`executive`, `professional`, `academic`,
`public-friendly`), emphasis (`text-balanced`, `visual-first`, `evidence-first`),
evidence level (`informational`, `sourced`, `auditable`), and page geometry
(`portrait`, `landscape`, `mixed`).

Routing precedence is explicit overrides, dominant purpose, evidence shape,
audience/output/risk, then the simplest complete archetype. The engine stores a
style receipt with the matched signals and any fallback.
