---
schema_version: 1
id: roadmap
type: timeline
title: Roadmap and milestones
goal: Sequence the work with timing, dependencies, and owners.
audience: customer operations leadership
status: complete
file: blocks/roadmap.md
required_facts: ["Foundation, pilot, and scale phases"]
source_refs: ["S1"]
layout_budget: full-page
presentation:
  break_before: true
visual:
  required: true
  kind: timeline
  family: timeline
  nodes:
    - id: foundation
      label: Q1 foundation
    - id: pilot
      label: Q2 pilot
    - id: scale
      label: Q3 scale
  edges:
    - from: foundation
      to: pilot
    - from: pilot
      to: scale
  caption: "Illustrative sequence from the supplied operating plan."
  alt_text: "Three-stage roadmap moving from foundation in Q1 to pilot in Q2 and scale in Q3."
---

# Roadmap and milestones

| Phase | Main work | Exit evidence |
| --- | --- | --- |
| Q1 foundation | Clean intake, baseline measures, and knowledge ownership | Shared definitions and a usable operating baseline [S1] |
| Q2 pilot | Test the model with one service group | Evidence of improved flow and documented gaps [S1] |
| Q3 scale | Extend the practices and governance rhythm | Repeatable reporting and ownership across groups [S1] |
