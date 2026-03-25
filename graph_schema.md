# Markdown Graph Schema for MarketingControlPlane

This document defines a concrete graph schema for the markdown files in the repo.

The graph is intended to help agentic workflows answer questions like:

- what source material grounds this candidate post?
- what did we just publish that should have a follow-on post?
- which themes or metaphors are overused?
- which source files have never turned into candidate or observed posts?
- which desired-state files are actually shaping outputs?

---

## 1. Graph model

Every `.md` file in the repo is a node.

Relationships between files are represented as directed, typed edges.

Format:

`(from_node) -[EDGE_TYPE]-> (to_node)`

The graph is rebuilt from the repo, not manually maintained.

---

## 2. Output files

The graph builder should emit:

- `graph/nodes.ndjson`
- `graph/edges.ndjson`

Each line is one JSON object.

This makes the graph:

- easy to diff
- easy to rebuild
- easy to import into Neo4j, DuckDB, NetworkX, or similar tooling

---

## 3. Node schema

Each markdown file becomes a node with this shape:

```json
{
  "id": "node:source/book/metaphors.md",
  "path": "source/book/metaphors.md",
  "file_name": "metaphors.md",
  "node_type": "source_metaphor_index",
  "title": "Metaphors",
  "status": "draft",
  "tags": ["metaphors", "book", "source"],
  "themes": ["ways_of_seeing", "swamp", "bets"],
  "metaphors": ["swamp", "bets", "pirate_ships"],
  "topics": [],
  "channel": null,
  "date_published": null,
  "risk": null,
  "cta": null,
  "trigger_type": null,
  "source_docs": [],
  "summary": "Index of core metaphors from the book.",
  "source_kind": "markdown"
}
