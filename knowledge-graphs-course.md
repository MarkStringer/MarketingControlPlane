# Knowledge Graphs: A Working Course

A practical course on the most important aspects of knowledge graphs, grounded in a real example: the graph that already lives in this repository. Every abstract idea below is illustrated with concrete nodes and edges from `graph/nodes.ndjson` and `graph/edges.ndjson`, so you can read the theory and then go look at the thing itself.

Roughly 4,000 words. Read it top to bottom once; after that, treat the section headings as a reference.

---

## 1. What a knowledge graph actually is

A knowledge graph is a way of representing information as a network of **things** and the **relationships between them**, rather than as rows in a table or paragraphs in a document.

That sounds simple, and the simplicity is the point. Three modelling choices make a graph different from the data structures you already know:

1. **Things are first-class.** Each entity — a book, a post, a person, a concept, a file — is a distinct object with its own identity. You can point at it, attach facts to it, and ask what it connects to.
2. **Relationships are first-class too.** The link between two things is not buried inside a foreign key or implied by a paragraph. It is an explicit object with its own type and, often, its own properties. "Post A *responds to* external post B" is a thing you can store, query, and count.
3. **The structure is the data.** In a spreadsheet, meaning lives in the cells. In a knowledge graph, a large part of the meaning lives in the *shape* of the connections. Which node has the most edges? Which node sits between two otherwise-separate clusters? Those structural facts are answers to real questions.

This repo is a good teaching case because it is not a toy. It is a "marketing control plane" for an author marketing a book (*Delivering the Impossible*) and an Edinburgh Fringe show (*You Can Write a Book*). Every markdown file — source material, drafted posts, published posts, replies, strategy documents, agent logs — becomes a node, and the meaningful relationships between those files become edges. The result currently holds **157 nodes and 843 edges** in the deterministic graph, and a richer semantic layer with hundreds more.

The reason to build it is stated plainly in `graph_schema.md`: to answer questions that are painful to answer against a pile of files, such as *"what source material grounds this candidate post?"*, *"which themes or metaphors are overused?"*, and *"which source files have never turned into a post?"* Those are all relationship questions. A folder of files cannot answer them; a graph can.

---

## 2. The atomic unit: nodes, edges, and triples

Strip a knowledge graph down to its smallest meaningful statement and you get a **triple**: *subject — predicate — object*. Two things and the named relationship between them.

In this repo the format is written exactly that way in the schema:

```
(from_node) -[EDGE_TYPE]-> (to_node)
```

A real edge from the data:

```json
{
  "from": "node:desired-state/cadence.md",
  "to":   "node:queue/post-candidates/post-candidate-2026-03-27-002-bad-news-is-data-not-disloyalty.md",
  "type": "constrains",
  "weight": 0.95,
  "evidence": {"method": "default_control_plane_rule"}
}
```

Read it as a sentence: *the cadence rules constrain this bad-news post candidate.* That single triple is the whole graph in miniature. Stack up hundreds of these statements and you have a network you can traverse and reason over.

Two properties of edges matter from the very start:

- **Edges are directed.** `constrains` points *from* the strategy *to* the post, not the other way around. Direction encodes meaning: "grounds" runs from source to post, "published_as" runs from a draft to the thing it became. Reverse the arrow and you change the claim.
- **Edges are typed.** The relationship is not a vague "related to". It is `constrains`, or `grounds`, or `responds_to`. The type tells you *how* two things relate, which is usually more valuable than the bare fact that they relate at all.

A graph made only of untyped, undirected links is just a web. A *knowledge* graph earns the word "knowledge" because its edges carry meaning.

---

## 3. Nodes carry properties, not just identity

A node is more than a name. Each node here is a structured record. From `graph_schema.md`, the shape of a node is:

```json
{
  "id": "node:source/book/metaphors.md",
  "path": "source/book/metaphors.md",
  "node_type": "source_metaphor_index",
  "title": "Metaphors",
  "status": "draft",
  "tags": ["metaphors", "book", "source"],
  "themes": ["ways_of_seeing", "swamp", "bets"],
  "metaphors": ["swamp", "bets", "pirate_ships"],
  "channel": null,
  "date_published": null,
  "summary": "Index of core metaphors from the book."
}
```

Those fields — `themes`, `metaphors`, `status`, `channel`, `date_published` — are the node's **properties** (also called attributes). They do two jobs.

First, they let you **filter and group** without traversing edges at all: "show me every node where `status` is `draft`", or "every node published on the LinkedIn `channel`".

Second, and more interestingly, properties are the *raw material from which edges get derived*. If two different files both list `swamp` in their `metaphors` array, a build step can create a `same_metaphor_as` edge between them automatically. The property on the node becomes a relationship in the graph. This is one of the central tricks of graph construction: lift shared attributes up into explicit connections so you can traverse them.

This style — nodes and edges that both carry arbitrary key/value properties — is called the **property graph** model. It is the model used by tools like Neo4j, and it is what this repo uses. (The other major model, RDF, is covered in Section 11.)

---

## 4. The schema (ontology): the contract that makes a graph legible

If every node and edge invented its own vocabulary, the graph would be unsearchable. The **schema** — in graph circles often called the **ontology** — is the agreed list of node types and edge types. It is the contract that says "these are the kinds of things that exist, and these are the kinds of relationships allowed between them."

This repo's schema defines a controlled vocabulary of node types, each tied to where the file lives:

| node_type | what it is |
|---|---|
| `source_document` | book chapters, keynote and video transcripts |
| `source_chapter_summary` | per-chapter summaries of the book |
| `source_metaphor_index` | the index of the book's core metaphors |
| `candidate_post` / `candidate_reply` | drafts awaiting approval |
| `observed_post` / `observed_reply` | things actually published |
| `desired_goal`, `desired_cadence`, `desired_audience`, … | strategy and constraints |
| `action_item` | operational tasks |
| `log_content_scout`, `log_reply_scout`, … | per-agent run logs |

And a controlled vocabulary of edge types, each with a precise meaning:

| edge_type | meaning |
|---|---|
| `grounds` | source material directly supports a candidate post |
| `informs` | source material shapes strategy |
| `constrains` | strategy limits or shapes queue/observed content |
| `same_theme_as` | two nodes share a theme |
| `same_metaphor_as` | two nodes use the same metaphor |
| `published_as` | a candidate became an observed post |
| `responds_to` | a reply responds to an external post |

The discipline here is the lesson. A good ontology is **small enough to remember and rich enough to be useful**. Ten edge types is plenty for this domain; a hundred would be unmanageable and inconsistently applied. When you design your own graph, the hardest and most valuable work is usually this: deciding what counts as a node, what counts as an edge, and what each name precisely means. Get the ontology right and everything downstream — extraction, querying, analytics — becomes tractable. Get it wrong and you spend forever reconciling synonyms.

A practical note visible in the live data: real graphs always contain a generic escape hatch. Here it is the `markdown_document` node type, used for files like `CLAUDE.md` and `README.md` that do not fit a specific category. Every ontology needs a way to admit "this is a node, but I haven't classified it precisely yet" — otherwise you either lose data or force bad classifications.

---

## 5. Identity: stable IDs and entity resolution

A graph is only coherent if "the book" is *one* node that everything points to, not five near-duplicates. This is the **identity** problem, and it is where many graph projects quietly fail.

This repo solves the easy half with **stable, deterministic IDs**. Every node's id is derived from its file path: `node:source/book/metaphors.md`. Edge ids are derived from their endpoints and type: `edge:node:desired-state/cadence.md->constrains->node:...`. Because the id is a pure function of the path, rebuilding the graph from scratch produces the same ids, so the graph is reproducible and diffable in git. The schema calls this out as a goal: "easy to diff, easy to rebuild." Deterministic identity is what makes that possible.

The hard half is **entity resolution** (also called deduplication or record linkage): deciding when two differently-named things are actually the same thing. You can see the seam in this repo's richer semantic layer. The graph report lists *both* `Delivering the Impossible (Book)` with 21 edges *and another* `Delivering the Impossible (Book)` with 16 edges as separate "god nodes." Those are almost certainly the same book, split into two nodes because they were extracted from different files under slightly different names. That split is the single most common defect in real knowledge graphs: the same entity fragmented across several nodes, so its connections are scattered and its true importance is understated.

Two takeaways. First, file-path identity is robust precisely because it is mechanical — there is no judgement involved. Second, the moment you start extracting *concepts* (not files) as nodes, you inherit the resolution problem, and you need a deliberate strategy: canonical names, alias tables, or a similarity threshold that merges near-duplicates. Identity is not a detail; it is a foundation.

---

## 6. Building a graph: deterministic extraction vs. semantic enrichment

Where do the nodes and edges come from? This repo is an unusually clear example because it has **two layers**, and understanding the contrast teaches you the whole landscape of graph construction.

**Layer one — the deterministic builder (`scripts/build_markdown_graph.py`).** This walks the repo, turns every markdown file into a node, and derives edges from rules. It reads YAML frontmatter to populate properties, infers `node_type` from the file path, and creates edges from concrete signals: shared `themes` produce `same_theme_as` edges, shared `metaphors` produce `same_metaphor_as`, an explicit `source_docs` list produces `grounds` edges, strategy files `constrain` queue files via default rules. This layer is **mechanical, fast, free, and perfectly reproducible**. Run it twice, get the same graph. Its edges are trustworthy because each one traces to an explicit rule — note the `"evidence": {"method": "default_control_plane_rule"}` stamped on every edge.

The edge-type distribution in the current graph shows what rule-based extraction produces in practice:

```
596  same_channel_as     <- everything on the same channel links to everything else
132  same_theme_as
 26  informs
 26  constrains
 19  grounds
  8  same_metaphor_as
```

That `same_channel_as` count is itself a lesson (see Section 9): a rule that links *every* pair sharing an attribute explodes combinatorially and can drown out the signal. Mechanical extraction is reliable but not automatically *wise*.

**Layer two — semantic extraction (the `graphify-out/` output).** A second pipeline uses a language model to read the *content* of files and extract finer-grained nodes and edges — not "file A links to file B" but "the *concept* `Bad News is Data` is referenced by these eight posts and contradicts that one." This produces a far richer graph (the report mentions on the order of 835 nodes and 1,195 edges) including concepts, people, and quotes that never had their own file. The report labels each extracted relationship: **89% EXTRACTED** (read directly from text) versus **11% INFERRED** (reasoned by the model), with the inferred edges carrying an average confidence of 0.82.

The two layers represent the fundamental trade-off in graph construction:

- **Rule-based / deterministic:** precise, cheap, reproducible, auditable — but it only finds relationships you already knew how to look for, and it misses everything implicit in prose.
- **Model-based / semantic:** finds rich, surprising, human-meaningful connections — but it costs tokens, is non-deterministic, and produces some edges that are wrong and must be marked, scored, and verified.

Mature systems use both: deterministic structure as the trustworthy skeleton, semantic extraction as the enrichment layer, with provenance recorded so you always know which is which.

---

## 7. Provenance: every edge should know where it came from

Notice that both layers attach **evidence** to their edges. The deterministic edges carry `"method": "default_control_plane_rule"`. The semantic edges carry an `EXTRACTED` / `INFERRED` label and a confidence score.

This is **provenance**, and it is one of the most underrated aspects of a serious knowledge graph. A graph is a giant pile of assertions, and not all assertions are equally trustworthy. Some are facts read directly from a file; some are a model's educated guess. If you cannot tell which is which, you cannot trust the graph for anything that matters, and you cannot improve it because you cannot tell good edges from bad.

The discipline to adopt: **never store a bare edge.** Store the edge plus *how you know* — the rule that fired, the source span, the model and confidence. When someone later asks "is this connection real?", provenance is the difference between an answer and a shrug. The repo's own graph report leans on this directly, surfacing questions like *"Are the 13 inferred relationships involving `Bad News is Data` actually correct?"* — a question you can only ask because the inferred edges were tagged as inferred.

---

## 8. Querying and traversal: why a graph beats a join

Here is the practical payoff. Once information is a graph, the questions that were awkward become natural, because you answer them by **walking edges**.

**One hop.** "What grounds this post?" Stand on the post node, follow `grounds` edges backward to source documents. Done. In a relational database this is a join; in a document store it is a full-text guess. In a graph it is a single traversal step that returns exactly the supporting sources.

**Multi-hop — the thing graphs are uniquely good at.** "Which published posts trace back, through their drafts and source material, to the book's *swamp* metaphor?" That is a path:

```
metaphor:swamp  -same_metaphor_as->  source_document
                -grounds->           candidate_post
                -published_as->       observed_post
```

Three hops across three edge types. In SQL this is three joins you have to write correctly and tune; in a graph query language it is a path pattern you describe once. The deeper the chain of relationships, the more decisively graph traversal beats repeated joins — both in how the query reads and in how it performs, because the graph stores the connections directly instead of recomputing them at query time.

**Pattern matching.** Graph query languages (Cypher for property graphs, SPARQL for RDF) let you describe a *shape* and ask the graph to find every place that shape occurs: "find every `candidate_post` that has **no** `grounds` edge" — i.e. drafts with no source backing, which the content policy here would flag. That "find the missing edge" query is exactly how this repo detects ungrounded content, and it is trivial on a graph and miserable on a folder of files.

This repo wraps traversal in a question-answering interface (`scripts/ask_graph.py`, run via `./ask_graph.sh`). It retrieves the relevant nodes and their neighbours and feeds them to a model to answer in plain language — a small example of **GraphRAG**, where graph structure decides *which* context to retrieve before a model answers. The graph is the retrieval index; its edges tell the system what is relevant to what.

---

## 9. Graph analytics: the structure is itself an answer

Because relationships are explicit, you can run algorithms over the *shape* of the graph and learn things no single file contains. This is where a knowledge graph stops being a fancy database and becomes an instrument. The repo's `GRAPH_REPORT.md` is a tour of the four most important techniques.

**Degree centrality — the "god nodes."** Count each node's edges; the most-connected nodes are your core abstractions. Here the top of the list is:

```
1. Bad News is Data                          31 edges
2. You Can Write a Book (Fringe Show)        24 edges
3. Delivering the Impossible (Book)          21 edges
8. Deliver the Possible Not the Fantasy      15 edges
```

Nobody declared "Bad News is Data" the centre of this body of work. The graph *discovered* it, because that concept connects to more things than anything else. Degree centrality turns "what is this corpus actually about?" into a sort.

**Betweenness centrality — the bridges.** A different question: which nodes sit *between* otherwise-separate clusters, so that removing them would fragment the graph? The report flags `Bad News is Data` again with high betweenness (0.055), noting it "connects PM Truth-Telling to Writing Craft, Published Posts, Project Delivery Realism, and Value Streams." Bridge nodes are strategically precious: they are the ideas that tie distinct themes together, and they are exactly what you want to lead with when you need one message to span audiences. High-degree tells you what is *central*; high-betweenness tells you what is *connective*. They are not the same, and the difference matters.

**Community detection — the emergent clusters.** Algorithms group densely-interlinked nodes into communities. The report finds 56, including "PM Truth-Telling & Bad News" (69 nodes), "Symmetrical Thinking & Bi-Logic" (63), "Writing Craft & Creative Voice" (72), and tight little clusters like "Projects as Romance" (8). These are *emergent* themes — the algorithm grouped them from connection density, not from anyone's folder structure. Each community also reports a **cohesion** score; a cohesion of 1.0 on a two-node "community" is a hint that it is too small to be meaningful, while a large community with low cohesion may be a catch-all that wants splitting.

**Knowledge gaps — the absences.** The most counterintuitive analytic is what is *not* there. The report lists **276 isolated nodes** with one connection or none, and flags "thin communities." An isolated node usually means one of two things: a genuinely orphaned piece of content (source material that never became a post — one of the exact questions the schema set out to answer), or a *missing edge* the extractor failed to find. Either way it is actionable. A graph lets you query for absence, and absence is frequently the most useful thing you can know.

The lens to keep: in a knowledge graph, **the topology is data.** Centrality, bridges, clusters, and holes are answers you can compute, not opinions you have to defend.

---

## 10. Inference, hyperedges, and the trust problem

Two more advanced features in this repo's semantic layer are worth understanding because they show where graphs are heading.

**Inferred edges.** Beyond what is written down, the model proposes connections it reasons must exist — for example `Embedded PM vs Reporter Dichotomy` *semantically_similar_to* `PM as Interface`, drawn between a reply candidate and a published reply that never reference each other directly. These are powerful: they surface the "surprising connections you didn't know" the report advertises. They are also the riskiest edges in the graph, which is why every one is tagged `INFERRED` with a confidence score, and why the report explicitly generates verification questions. The principle: **inference is welcome, but it must be quarantined and labelled, never silently mixed with fact.**

**Hyperedges.** A normal edge connects exactly two nodes. A **hyperedge** connects a *group*. The report's "Bad News Handling: PM Replies Cluster" ties together four replies and four concepts as one named relationship. Some real-world relationships are genuinely n-ary — "these six files form the Graph Build-Query-Edit Pipeline" — and forcing them into pairwise edges loses the fact that they act as a set. Most property-graph tools fake hyperedges by introducing an intermediate node that everything links to; the idea is the same: relationships are not always binary.

The unifying theme of this section is **trust**. The more a graph infers, the more it can tell you and the more it can mislead you. The whole apparatus of confidence scores, EXTRACTED-vs-INFERRED labels, and auto-generated "is this real?" questions exists to manage that trade-off. A knowledge graph you cannot audit is not knowledge; it is a confident-sounding guess.

---

## 11. Two models you'll meet: property graphs and RDF

You will encounter two dominant ways to implement a knowledge graph. They are more alike than the tribal arguments suggest.

**Property graphs** (Neo4j, Memgraph, and the model this repo uses). Nodes and edges both carry arbitrary key/value properties. Edges have a type and a direction. The query language is usually **Cypher**, whose `()-[]->()` syntax is literally the `(from)-[EDGE]->(to)` notation in `graph_schema.md`. Property graphs are pragmatic, ergonomic for application developers, and excellent when relationships need their own attributes (like the `weight` and `evidence` on every edge here).

**RDF / triple stores** (the W3C semantic-web stack). Everything is a triple: subject–predicate–object, where each element is a globally unique URI. Schemas are expressed in **RDFS/OWL** ontologies, and the query language is **SPARQL**. RDF's superpower is *interoperability*: because identifiers are global URIs, separate organisations' graphs can be merged and reasoned over together, which is why RDF underpins large public knowledge bases like Wikidata. Its cost is more ceremony for everyday application work.

Rule of thumb: reach for a **property graph** when you are building one application and want relationships with rich attributes; reach for **RDF** when you need to publish, merge, or reason across data from many independent sources using shared vocabularies. The conceptual core — typed, directed relationships between identified things — is identical. The differences are about identifiers, standards, and tooling, not about what a knowledge graph fundamentally *is*.

It is also worth knowing how graphs and vector embeddings relate, because the two are increasingly combined. Embeddings capture *fuzzy similarity* ("these two paragraphs feel related"); graphs capture *precise, named, traversable structure* ("this draft was `published_as` that post"). This repo already blends them: deterministic edges give exact structure, while the semantic layer's `semantically_similar_to` edges are embedding-style similarity promoted into explicit, inspectable edges. The frontier of practical AI retrieval — GraphRAG — is exactly this marriage: use embeddings to find candidates, use the graph to find *what is connected to them*, and feed both to a model.

---

## 12. Designing your own: a short, opinionated checklist

If you take one workflow from this course, take this order of operations. It is the order this repo implicitly followed.

1. **Write the questions first.** This graph began with a literal list of questions in `graph_schema.md` ("what grounds this post?", "what's overused?", "what never shipped?"). Your ontology should be the *minimum structure that answers your questions* — nothing more. Design from the questions backward, never from the data forward.
2. **Define a small ontology.** List your node types and edge types, give each a one-line definition, and stop. Resist the urge to model everything. You can always extend; you can rarely simplify a vocabulary people have already used inconsistently.
3. **Fix identity early.** Decide what makes two things "the same thing." Deterministic IDs (like file paths here) where you can; an explicit resolution strategy (canonical names, aliases, similarity thresholds) where you must. The fragmented `Delivering the Impossible` node is the cautionary tale.
4. **Extract in layers, and record provenance.** Build a cheap, reproducible deterministic skeleton first. Add semantic enrichment on top. Stamp every edge with how you know it — rule, source span, or model-and-confidence — and never blur fact and inference.
5. **Mind the combinatorics.** The 596 `same_channel_as` edges are a warning: "link everything that shares attribute X" is O(n²) and can bury your signal. Prefer edges that mean something specific over edges that merely co-occur.
6. **Make it rebuildable and diffable.** NDJSON, one object per line, regenerated from source rather than hand-maintained, committed to git. A graph you can rebuild from scratch is a graph you can trust, test, and evolve.
7. **Then mine the structure.** Run centrality, community detection, and gap analysis. Let the graph tell you what your corpus is about, where its bridges are, and where its holes are. That feedback — `Bad News is Data` is your centre of gravity; 276 things are orphaned — is the entire reason you built the graph instead of a folder.

---

## 13. When *not* to reach for a knowledge graph

For balance: a knowledge graph is the wrong tool when your data is naturally tabular and your questions are aggregations ("total sales by region this quarter") — a relational database or a columnar store will be simpler and faster. It is overkill when relationships are shallow and you never traverse more than one hop. And it is premature when you have not yet articulated the relationship-shaped questions that justify the modelling cost. The graph here earns its keep because the questions are genuinely about connection — grounding, overlap, follow-on, gaps — and because those connections span many small documents. When that is your situation, a knowledge graph is not a luxury; it is the only structure that makes the questions answerable.

---

## 14. Glossary

- **Node (vertex):** a thing — entity, concept, document, person.
- **Edge (relationship):** a typed, directed link between two nodes.
- **Triple:** the atomic statement *subject–predicate–object*; one edge with its endpoints.
- **Property / attribute:** a key/value fact stored on a node or edge.
- **Schema / ontology:** the controlled vocabulary of allowed node types and edge types and their meanings.
- **Entity resolution:** deciding when two records refer to the same real-world thing.
- **Provenance:** the recorded origin and confidence of an edge or node.
- **Traversal:** answering a question by walking edges from node to node.
- **Centrality:** structural importance — degree (most connected) and betweenness (most connective/bridging).
- **Community:** a densely-interconnected cluster of nodes, detected algorithmically.
- **Inferred edge:** a relationship reasoned by a model rather than read from a source; must be labelled and scored.
- **Hyperedge:** a single relationship that connects a group of nodes rather than a pair.
- **Property graph vs RDF:** the two main implementations; property graphs (Cypher) favour rich edge attributes and application work, RDF (SPARQL) favours global identifiers and cross-source interoperability.
- **GraphRAG:** retrieval that uses graph structure to choose what context to feed a language model.

---

### Where to look next in this repo

- `graph_schema.md` — the ontology: node types, edge types, the node record shape.
- `graph/nodes.ndjson`, `graph/edges.ndjson` — the live deterministic graph (157 nodes, 843 edges).
- `scripts/build_markdown_graph.py` — deterministic, rule-based extraction.
- `graphify-out/GRAPH_REPORT.md` — the semantic layer's analytics: god nodes, communities, bridges, gaps.
- `scripts/ask_graph.py` / `ask_graph.sh` — graph-grounded question answering (GraphRAG in miniature).
- `scripts/edit_graph.py` / `graph_editor_commands.md` — manual edits and experiments on the generated graph.

Read this course once for the concepts, then open those files and watch every concept appear in the wild.
