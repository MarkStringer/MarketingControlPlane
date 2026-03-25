# Graph Editor Commands

This document describes the commands supported by `scripts/edit_graph.py`.

## Important warning

This script edits the generated graph files directly:

- `graph/nodes.ndjson`
- `graph/edges.ndjson`

If you later run `scripts/build_markdown_graph.py`, some or all manual edits may be overwritten.

Use this editor for:
- temporary graph experiments
- manual annotation
- debugging graph behavior
- small tactical fixes

For persistent changes, prefer:
- editing the underlying markdown files, or
- extending `scripts/build_markdown_graph.py`

---

## File location

Put the script here:

```text
scripts/edit_graph.py
