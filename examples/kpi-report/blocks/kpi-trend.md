---
schema_version: 1
id: kpi-trend
type: chart
title: Monthly active users
goal: Show the reported monthly trend without implying unsupported causation.
audience: operating team
status: draft
source_refs:
  - S1
required_facts:
  - Monthly active users
layout_budget: half-page
visual:
  required: true
  kind: line
  title: Monthly active users
  labels:
    - Jan
    - Feb
    - Mar
    - Apr
    - May
    - Jun
  values:
    - 120
    - 134
    - 141
    - 139
    - 153
    - 161
  caption: Monthly active users reported in the operating dataset.
  alt_text: Line chart showing monthly active users: Jan 120, Feb 134, Mar 141, Apr 139, May 153, Jun 161.
---

The KPI increased from 120 in January to 161 in June [S1]. The small April decline is retained in the chart so the report does not flatten a mixed month-to-month pattern.
