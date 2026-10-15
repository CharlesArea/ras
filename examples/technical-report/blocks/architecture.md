---
schema_version: 1
id: architecture
type: diagram
title: Request path
goal: Explain the supported request path and system boundaries.
audience: engineering team
status: draft
source_refs:
  - S1
required_facts:
  - Request path components
layout_budget: half-page
visual:
  required: true
  kind: diagram
  family: architecture
  caption: Original RAS architecture diagram based on the supplied component notes.
  alt_text: Architecture diagram showing Client, API gateway, Service, and Data store connected in request order.
  nodes:
    - id: client
      label: Client
      level: 0
    - id: gateway
      label: API gateway
      level: 1
    - id: service
      label: Service
      level: 2
    - id: data
      label: Data store
      level: 3
  edges:
    - from: client
      to: gateway
    - from: gateway
      to: service
    - from: service
      to: data
---

The supplied component notes describe a request path from the client through the API gateway to the service and data store [S1]. The diagram makes that relationship explicit without adding deployment details.
