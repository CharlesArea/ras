---
schema_version: 1
id: timeline
type: timeline
title: Incident timeline
goal: Sequence the observed events and response actions.
audience: engineering and operations
status: complete
file: blocks/timeline.md
required_facts: ["Alert, mitigation, rollback, and recovery milestones"]
source_refs: ["S1"]
layout_budget: full-page
visual:
  required: true
  kind: timeline
  family: timeline
  nodes:
    - id: detect
      label: 09:14 alert
    - id: mitigate
      label: 09:26 mitigation
    - id: rollback
      label: 09:41 rollback
    - id: recover
      label: 09:56 recovery
  edges:
    - from: detect
      to: mitigate
    - from: mitigate
      to: rollback
    - from: rollback
      to: recover
  caption: "Incident response sequence from the supplied incident notes."
  alt_text: "Timeline from a 09:14 alert through mitigation at 09:26, rollback at 09:41, and recovery at 09:56."
---

# Incident timeline

| Time | Event | Response |
| --- | --- | --- |
| 09:14 | Elevated 5xx alert | On-call began investigation [S1] |
| 09:26 | Fan-out reduced | Error rate began to fall [S1] |
| 09:41 | Configuration rolled back | Downstream pressure normalized [S1] |
| 09:56 | Recovery confirmed | Incident moved to follow-up [S1] |
