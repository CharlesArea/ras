# Design system

RAS resolves every report into one semantic design object before rendering.
That object contains palette, typography, page geometry, component variants,
chart tokens, diagram tokens, and a receipt containing theme, brand, density,
tone, and emphasis.

Content blocks are classified into semantic components: summary, finding,
recommendation, visual, source, and narrative. A block can request an
explicit `visual.component` or `visual.variant`; otherwise its theme supplies
the component recipe. DOCX and PDF may use different native layout APIs, but
they must preserve the same component meaning and visual hierarchy.

Theme packs are intentionally distinct. A palette-only color swap is not a
new theme: cover treatment, page rhythm, typography, tables, callouts, charts,
and diagrams should all respond to the resolved theme.
