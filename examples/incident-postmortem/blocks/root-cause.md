---
schema_version: 1
id: root-cause
type: finding
title: Root cause and contributing factors
goal: Separate direct cause, contributing factors, and evidence.
audience: engineering and operations
status: complete
file: blocks/root-cause.md
required_facts: ["A configuration change increased request fan-out and exhausted a downstream quota"]
source_refs: ["S1"]
layout_budget: half-page
visual:
  required: false
  caption: ""
  alt_text: ""
---

# Root cause and contributing factors

## Direct cause

A configuration change increased request fan-out and exhausted a downstream quota [S1].

## Contributing factors

- The rollout did not include a staged exposure limit.
- Quota consumption was not visible in the primary service dashboard.
- The alert detected customer-facing errors but did not identify the downstream pressure early.

The evidence supports a systems and rollout gap, not an individual blame conclusion.
