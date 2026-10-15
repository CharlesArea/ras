---
schema_version: 1
id: actions
type: recommendation
title: Corrective actions
goal: Set prevention, detection, and recovery actions with owners.
audience: engineering and operations
status: complete
file: blocks/actions.md
required_facts: ["Add quota guardrails, staged configuration rollout, and alert coverage"]
source_refs: ["S1"]
layout_budget: half-page
visual:
  required: false
  caption: ""
  alt_text: ""
---

# Corrective actions

| Action | Owner | Completion signal |
| --- | --- | --- |
| Add quota and fan-out guardrails | Platform team | Guardrail test passes in staging [S1] |
| Roll out configuration changes in stages | Release engineering | Progressive rollout policy is enforced [S1] |
| Add downstream quota monitoring | Observability team | Dashboard and alert are reviewed in on-call drill [S1] |

The incident is closed operationally, but the actions remain open until the completion signals are demonstrated.
