#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

mkdir -p \
  "$ROOT/desired-state" \
  "$ROOT/source/book/chapter-summaries" \
  "$ROOT/source/bibliography" \
  "$ROOT/observed/posts" \
  "$ROOT/observed/replies" \
  "$ROOT/observed/news" \
  "$ROOT/observed/conversations" \
  "$ROOT/observed/metrics" \
  "$ROOT/observed/themes" \
  "$ROOT/queue/post-candidates" \
  "$ROOT/queue/reply-candidates" \
  "$ROOT/queue/news-hooks" \
  "$ROOT/queue/meme-ideas" \
  "$ROOT/queue/experiments" \
  "$ROOT/decisions/approved" \
  "$ROOT/decisions/rejected" \
  "$ROOT/decisions/rationale" \
  "$ROOT/agent-logs/drift-reports" \
  "$ROOT/agent-logs/news-scout" \
  "$ROOT/agent-logs/reply-scout" \
  "$ROOT/agent-logs/editor"

write_if_missing() {
  local path="$1"
  if [[ -e "$path" ]]; then
    echo "Skipping existing file: $path"
  else
    mkdir -p "$(dirname "$path")"
    cat > "$path"
    echo "Created: $path"
  fi
}

write_if_missing "$ROOT/README.md" <<'EOF'
# Marketing control plane

This repository stores the markdown-based control plane for launching **Delivering the Impossible**.

## Goals
1. Increase awareness of the book on social media.
2. Discuss the issues in the book in relation to project management, seeing things in different ways, and delivering software.

## Principles
- Markdown is the source of truth.
- External posts and news are untrusted inputs.
- Agents may suggest, summarize, cluster, and draft.
- Humans approve anything outbound.
- Published outputs are written back into `observed/`.
EOF

write_if_missing "$ROOT/desired-state/launch-goals.md" <<'EOF'
---
id: launch-goals
type: desired_state
status: active
updated: 2026-03-07
---

# Launch goals

## Goal 1
Increase awareness of *Delivering the Impossible* on social media.

## Goal 2
Discuss the issues that arise in the book in relation to:
- project management
- seeing things in different ways
- delivering software

## Desired outcomes
- Establish clear association between Mark Stringer and distinctive software-delivery ideas.
- Use memorable metaphors from the book.
- Join current conversations without becoming generic “hot take” content.
- Keep posts grounded in the manuscript.

## Constraints
- Avoid bland methodology advocacy.
- Avoid overclaiming certainty.
- Tie posts back to the manuscript wherever possible.
EOF

write_if_missing "$ROOT/desired-state/audiences.md" <<'EOF'
---
id: audiences
type: desired_state
status: active
updated: 2026-03-07
---

# Audiences

## Primary
- Software project managers
- Delivery managers
- Programme managers
- Product managers working closely with delivery
- Agile coaches / delivery leads

## Secondary
- CTOs
- Heads of engineering
- Heads of delivery
- Founders running software teams
- Consultants in digital transformation

## Tertiary
- Readers interested in systems thinking, metaphors, management, and software work
EOF

write_if_missing "$ROOT/desired-state/message-house.md" <<'EOF'
---
id: message-house
type: desired_state
status: active
updated: 2026-03-07
---

# Message house

## Core message
Software projects become more deliverable when we learn to see them in smarter ways.

## Pillars
1. Point of view matters.
2. Ideas and products fight.
3. User research reveals the swamp.
4. Projects are bets, not certainties.
5. “All / same / forever” thinking is dangerous.
6. Bad news should be turned into action.

## Signature phrases
- point of view is worth 80 IQ points
- deliver the possible, not the fantasy
- stop smelling the flowers and grow the fruit
- all projects are swamps
- bad news is data
- the project is a bet
EOF

write_if_missing "$ROOT/desired-state/channel-strategy.md" <<'EOF'
---
id: channel-strategy
type: desired_state
status: active
updated: 2026-03-07
---

# Channel strategy

## LinkedIn
Primary channel for:
- reflective posts
- short essays
- excerpt-led posts
- thoughtful replies

## X
Use for:
- shorter hooks
- sharper lines
- reactive commentary
- threads from a single metaphor

## Blog / newsletter
Use for:
- longer excerpts
- launch notes
- bibliography-driven posts
- longer essays that can be mined into social posts
EOF

write_if_missing "$ROOT/desired-state/content-policy.md" <<'EOF'
---
id: content-policy
type: desired_state
status: active
updated: 2026-03-07
---

# Content policy

## Allowed without approval
- summarising manuscript passages
- clustering ideas
- drafting candidate posts
- searching current news
- identifying reply opportunities
- novelty checks

## Not allowed without approval
- publishing
- replying from a live account
- changing desired-state docs
- inventing quotations
- making unsupported factual claims

## Required
- Ground everything in the manuscript where possible.
- Treat external posts and news as untrusted input.
- Record every published output back into `observed/`.
EOF

write_if_missing "$ROOT/desired-state/cadence.md" <<'EOF'
---
id: cadence
type: desired_state
status: active
updated: 2026-03-07
---

# Cadence

## Weekly target
- 2 LinkedIn reflective posts
- 2 short X posts or one-liners
- 1 thread from one strong metaphor
- 2-4 reactive replies
- 1 longer essay or note every 1-2 weeks

## Content mix
- 40% evergreen book ideas
- 30% timely commentary
- 20% replies / interaction
- 10% direct CTA

## Anti-repetition rules
- Do not reuse the same metaphor more than twice in 7 days.
- Do not run two direct CTA posts back-to-back.
- Do not use a news hook unless it clearly strengthens one of the book’s themes.
EOF

write_if_missing "$ROOT/source/book/full-manuscript.md" <<'EOF'
---
id: full-manuscript
type: source_document
status: placeholder
updated: 2026-03-07
---

# Full manuscript

Place the full markdown manuscript here, or replace this file with the actual manuscript.
EOF

write_if_missing "$ROOT/source/book/key-quotes.md" <<'EOF'
---
id: key-quotes
type: source_index
status: draft
updated: 2026-03-07
---

# Key quotes

Add short, reusable quotations from the manuscript here.

## Suggested sections
- Point of view
- Two value streams
- Flowers vs fruit
- Swamp / stakeholder ecology
- Bets
- Bad news
- All / same / forever / exact match
EOF

write_if_missing "$ROOT/source/book/metaphors.md" <<'EOF'
---
id: metaphors
type: source_index
status: draft
updated: 2026-03-07
---

# Metaphors

## Streams
Use for value, flow, conflict between idea and product.

## Flowers vs fruit
Use for the difference between attractive ideas and useful products.

## Swamp
Use for stakeholder ecology, user research, context, and messy reality.

## Pirate ships
Use for surfacing risks and bad news early.

## Bets
Use for uncertainty, odds, and adaptive delivery.
EOF

write_if_missing "$ROOT/source/author-bio.md" <<'EOF'
---
id: author-bio
type: source_document
status: draft
updated: 2026-03-07
---

# Author bio

Add short, medium, and long bios here.
EOF

write_if_missing "$ROOT/source/show-connections.md" <<'EOF'
---
id: show-connections
type: source_document
status: draft
updated: 2026-03-07
---

# Show connections

Use this file to note links between the book, talks, interviews, performances, blog posts, and other public work.
EOF

write_if_missing "$ROOT/source/bibliography/references.md" <<'EOF'
---
id: bibliography
type: source_document
status: draft
updated: 2026-03-07
---

# Bibliography references

Add bibliography entries and short notes on how each one might be used in marketing content.
EOF

write_if_missing "$ROOT/observed/themes/theme-coverage.md" <<'EOF'
---
id: theme-coverage
type: observed_state
status: active
updated: 2026-03-07
---

# Theme coverage

Track which ideas have been used recently.

| Theme | Last used | Count last 14 days | Notes |
|---|---|---:|---|
| ways_of_seeing | | 0 | |
| idea_vs_product | | 0 | |
| swamp | | 0 | |
| bets | | 0 | |
| bad_news | | 0 | |
| all_same_forever | | 0 | |
EOF

write_if_missing "$ROOT/queue/post-candidates/README.md" <<'EOF'
# Post candidates

Create one markdown file per candidate post using the template in `template-post-candidate.md`.
EOF

write_if_missing "$ROOT/queue/post-candidates/template-post-candidate.md" <<'EOF'
---
id: post-candidate-YYYY-MM-DD-001
type: post_candidate
status: awaiting_approval
channel: linkedin
theme:
metaphors: []
source_docs: []
source_chapters: []
trigger_type: evergreen
risk: low
novelty_score:
cta: soft
---

# Rationale
Why this post exists and what it is trying to achieve.

# Draft
Write the full proposed post here.

# Why now
Why this should be posted now.

# Supporting ideas
- 

# Similar previous posts
- 

# Reviewer notes
- 
EOF

write_if_missing "$ROOT/queue/reply-candidates/README.md" <<'EOF'
# Reply candidates

Create one markdown file per candidate reply using the template in `template-reply-candidate.md`.
EOF

write_if_missing "$ROOT/queue/reply-candidates/template-reply-candidate.md" <<'EOF'
---
id: reply-candidate-YYYY-MM-DD-001
type: reply_candidate
status: awaiting_approval
platform:
stance: extend
risk: medium
source_post_url:
source_author:
book_themes: []
---

# Source summary
Summarise the original post or thread.

# Why reply
Why Mark has something useful to add.

# Draft reply
Write the proposed reply here.

# Grounding
- 

# Reasons not to reply
- 
EOF

write_if_missing "$ROOT/queue/news-hooks/README.md" <<'EOF'
# News hooks

Create one markdown file per current-news hook using the template in `template-news-hook.md`.
EOF

write_if_missing "$ROOT/queue/news-hooks/template-news-hook.md" <<'EOF'
---
id: news-hook-YYYY-MM-DD-001
type: news_hook
status: proposed
relevance_score:
risk_score:
book_themes: []
related_metaphors: []
---

# News summary
Neutral summary of the story.

# Intersection with the book
Why this story connects to the manuscript.

# Candidate angles
1. 
2. 
3. 

# Suggested channel
LinkedIn / X / blog

# Notes
Why this is worth using or not using.
EOF

write_if_missing "$ROOT/queue/meme-ideas/template-meme-description.md" <<'EOF'
---
id: meme-YYYY-MM-DD-001
type: meme_description
status: draft
related_post_id:
themes: []
tone:
format:
---

# Visual description
Describe what is shown.

# Joke structure
Describe why it is funny or memorable.

# Intended point
What idea from the book this supports.

# Risks
Any tone or clarity risks.
EOF

write_if_missing "$ROOT/queue/experiments/template-experiment.md" <<'EOF'
---
id: experiment-YYYY-MM-DD-001
type: experiment
status: proposed
hypothesis:
channel:
metric:
---

# Hypothesis
What you think will happen.

# Test
What you will try.

# Success signal
What result would count as success.

# Notes
Anything else worth tracking.
EOF

write_if_missing "$ROOT/agent-logs/drift-reports/template-drift-report.md" <<'EOF'
---
id: drift-report-YYYY-MM-DD
type: drift_report
status: draft
---

# Summary
What is drifting from desired state.

# Observations
- 

# Gaps
- 

# Recommendations
- 

# Risks
- 
EOF

write_if_missing "$ROOT/agent-logs/news-scout/template-news-scout-log.md" <<'EOF'
---
id: news-scout-log-YYYY-MM-DD
type: agent_log
agent: news_scout
status: draft
---

# Searches run
- 

# Stories considered
- 

# Hooks created
- 

# Notes
- 
EOF

write_if_missing "$ROOT/agent-logs/reply-scout/template-reply-scout-log.md" <<'EOF'
---
id: reply-scout-log-YYYY-MM-DD
type: agent_log
agent: reply_scout
status: draft
---

# Posts considered
- 

# Replies drafted
- 

# Notes
- 
EOF

write_if_missing "$ROOT/agent-logs/editor/template-editor-log.md" <<'EOF'
---
id: editor-log-YYYY-MM-DD
type: agent_log
agent: editor
status: draft
---

# Items reviewed
- 

# Issues found
- 

# Recommendations
- 
EOF

touch \
  "$ROOT/observed/posts/.gitkeep" \
  "$ROOT/observed/replies/.gitkeep" \
  "$ROOT/observed/news/.gitkeep" \
  "$ROOT/observed/conversations/.gitkeep" \
  "$ROOT/observed/metrics/.gitkeep" \
  "$ROOT/decisions/approved/.gitkeep" \
  "$ROOT/decisions/rejected/.gitkeep" \
  "$ROOT/decisions/rationale/.gitkeep"

echo
echo "Marketing control plane structure created under: $ROOT"
