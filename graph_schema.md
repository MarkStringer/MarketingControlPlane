# Markdown Graph Schema for MarketingControlPlane

This document defines a concrete graph schema for the markdown files in the repo.

The graph is intended to help agentic workflows answer questions like:

- what source material grounds this candidate post?
- what did we just publish that should have a follow-on post?
- which themes or metaphors are overused?
- which source files have never turned into candidate or observed posts?
- which desired-state files are actually shaping outputs?
- which show themes overlap with book themes and could generate cross-promotion content?
- which parts of the show script have no corresponding book material (gaps in the connection)?

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
```

---

## 4. Node types

### Book source material
| node_type | path pattern | description |
|---|---|---|
| `source_metaphor_index` | `source/book/metaphors.md` | Index of book metaphors |
| `source_document` | `source/book/**`, `source/youtubeTranscripts/**` | Book chapters, keynote/video transcripts |

### Show source material
| node_type | path pattern | description |
|---|---|---|
| `source_show_script` | `source/show/*.md` | Script drafts for "You Can Write a Book" Edinburgh Fringe show |
| `source_show_notes` | `source/show/*-gaps.md`, `source/show/*-notes.md` | Production notes, gap analyses, directorial annotations |
| `source_show_background` | `source/show/*-highlights.md` | Background reading and research that informs the show (e.g. Kindle highlights) |

### Desired state
| node_type | path pattern | description |
|---|---|---|
| `desired_audience` | `desired-state/audiences.md` | Target audience definitions |
| `desired_cadence` | `desired-state/cadence.md` | Publishing cadence rules |
| `desired_channel_strategy` | `desired-state/channel-strategy.md` | Channel usage rules |
| `desired_content_policy` | `desired-state/content-policy.md` | Content approval policy |
| `desired_goal` | `desired-state/launch-goals.md` | Launch and marketing goals |
| `desired_message_house` | `desired-state/message-house.md` | Core message and pillars |

### Queue
| node_type | path pattern | description |
|---|---|---|
| `candidate_post` | `queue/post-candidates/**` | Post drafts awaiting approval |

### Observed
| node_type | path pattern | description |
|---|---|---|
| `observed_post` | `observed/posts/**` | Published posts |

---

## 5. Edge types

| edge_type | meaning |
|---|---|
| `grounds` | source material directly supports a candidate post |
| `informs` | source material shapes desired state or strategy |
| `constrains` | desired state limits or shapes queue/observed content |
| `same_theme_as` | two nodes share a theme |
| `same_metaphor_as` | two nodes use the same metaphor |
| `inspired_by` | candidate was inspired by a source node |
| `published_as` | candidate was published as an observed post |
| `follow_on_from` | post is a natural follow-on to another |
| `responds_to` | reply post responds to an observed external post |
