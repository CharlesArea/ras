# Block contracts

Each block is a Markdown file with YAML frontmatter. The frontmatter must
contain `schema_version`, stable `id`, `type`, `title`, `goal`, `audience`,
`status`, `source_refs`, `required_facts`, `layout_budget`, and a `visual`
object. The body is the human-readable content.

Blocks are independently resumable. A block can be `planned`, `draft`,
`generated`, `validated`, `complete`, or `blocked`. Regenerating one block must
not rewrite unrelated blocks. Shared claims and terminology belong in the
project's source ledger and manifest.

Supported visual block families include metric panels, tables, charts, and RAS
diagrams. Informative visuals require a caption and alternative text.

Optional renderer-independent presentation hints can refine the resolved theme
without coupling content to DOCX or PDF internals:

```yaml
presentation:
  component: key-finding
  variant: accent
  span: 6
  emphasis: primary
  break_before: false
  keep_together: true
```

Omit the hint when the archetype and theme can choose the component safely.
