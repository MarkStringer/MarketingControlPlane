---
id: reply-scout-log-2026-07-22
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Note: the `tbs=qdr:d` (past-24-hours) Google URL again returned a 302 consent-wall redirect to `consent.google.com` from the GB region, so true date-filtered results were unavailable. Sourced posts via WebSearch across several specific-argument angles (AI, estimation, contingency, metrics, psychological safety) and verified the selected posts by direct WebFetch of the post text.

# Posts considered

- Holly Knoll — "How AI will redefine project management, not replace it." AI takes admin/status/risk-analysis; human residue is EQ, trust, diplomacy; average PMs obsolete, great PMs indispensable. **SELECTED** — direct target for the "the leftover human bit is diplomacy" consensus; Mark's reframe is that the irreplaceable function is carrying bad news, not soft skills.
- Civils Bites — "Risk vs Contingency." Risk = specific identifiable events; contingency = protection against the unforeseen; conflating them damages credibility and contingency is not "fat in the budget." **SELECTED** — lets Mark make the structural point that contingency gets deleted precisely because it is an honest admission of uncertainty.
- Paul Cho — "The most common estimation biases." Optimism bias, anchoring, planning fallacy, Parkinson's law, student syndrome; frames bad estimates as cognitive error. **SELECTED** — borderline list post but makes a specific causal claim; Mark's counterpoint is that "bias" misdiagnoses an incentive as a psychology problem.
- Jason L. (Legris) — "Estimation is pointless when every alternative is equally as good." **REJECTED** — already covered by candidate 2026-05-20-001 (same author, same post).
- Michael Otjen — "When will this project go live / you can't answer without a plan." **REJECTED** — Otjen already replied to twice (07-03, 07-16).
- Oyvind Henriksen — "Translated: we're three members down, the project is screwed." **REJECTED** — Henriksen honest-status angle already covered (07-09).
- Dan Gardner — "When confidence helps PMs and when it gets them into trouble." **REJECTED** — Gardner confidence angle already covered twice (04-27, 05-07).
- Prof. Bent Flyvbjerg — megaprojects / on-time-on-budget. **REJECTED** — Flyvbjerg and the on-time-to-budget metric already covered (05-07, plus 06-03 outputs-outcomes, 06-29 delivery-benefit).
- Cindy Okosun — "AI enhances human judgment, doesn't replace it." **REJECTED** — Okosun already replied to (05-18) and thesis overlaps the selected Knoll post.
- Chat Engineer / Project Management Information / Kory Kogon / Pasang Sherpa — "PM basics", phases, glossary, course-completion posts. **REJECTED** — list/glossary/promotional, only reply would be agreement.
- Center for Project Innovation / Hiu Fu Shun / status-report template posts. **REJECTED** — free-template promotional content.
- Britney Osbern / Rikard Bergstrom / change-management resource guides. **REJECTED** — resource-list / promotional, no specific claim to engage.
- Psychological-safety posts (Emmerson, Jayarathna, Blandon, Charles). **REJECTED** — generic Edmondson restatements, no non-obvious angle to add.

# Replies drafted

- reply-candidate-2026-07-22-001-knoll-ai-carries-bad-news.md — the thing AI can't do isn't diplomacy, it's carrying bad news; bad news is data.
- reply-candidate-2026-07-22-002-civilsbites-contingency-is-honesty.md — contingency is the honest price of the part of the bet you can't see yet, which is why it gets deleted; the project is a bet.
- reply-candidate-2026-07-22-003-cho-estimation-bias-is-incentive.md — estimation "bias" is really a rational response to an incentive; fix the incentive, not the psychology; deliver the possible not the fantasy.

# Notes

- Google past-24h date filter remains blocked by the GB consent redirect (recurring since at least 06-30). WebSearch surfaces a mix of ages, so candidate freshness cannot be guaranteed to 24 hours; selections were screened against the observed/replies corpus and the reply-candidate queue to avoid repeat authors and themes.
- Marketing-critic SessionStart hook again failed with a 400 "credit balance too low" Anthropic API error. Non-blocking for this run but worth Mark topping up or disabling the hook.
- All three drafts follow the style guide: no hashtags, no em-dashes, no bullet points, each ends on a statement not a question.
