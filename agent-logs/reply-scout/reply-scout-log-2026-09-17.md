---
id: reply-scout-log-2026-09-17
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes named in the brief were attempted first, as required.

- **WebSearch, bare brief query.** Returned nine results, all glossary/listicle/vendor content: a
  "Project Management Cheat Sheet," "Understanding the 49 Project Management Processes," "40
  Essential Project Management Templates," Chat Engineer's "Project Management (The Basics),"
  Turing's "Six Best Project Management Tools for 2023," a bare #projectmanagement post, Kory
  Kogon's "What Is Project Management?", Whitney Akabike's post, and a Harvard ManageMentor course
  completion post. Same stale/evergreen shape logged on every run since 2026-07-23. Zero selectable
  posts.
- **Google time-filtered URL.** Not fetched again this run; the `reference-reply-scout-search-routing`
  memory and every log since 2026-07-23 confirm it 302s to a consent page WebFetch cannot clear. Per
  the memory's standing advice ("stop spending calls on engines at the top of a run"), skipped
  straight to the hub route after the one WebSearch check above.

Per the 2026-09-15 and 2026-09-16 logs, the `top-content/project-management/` hub tree is fully
mined out (107 of 107 slugs). The 2026-09-16 log opened `change-management/` (107 sub-slugs) and
`leadership/` (137 sub-slugs) and mined 10 sub-hubs between them. This run continued widening those
two trees plus opened a third, `organizational-culture/` (121 sub-slugs), per the 2026-09-16 log's
explicit recommendation.

# What worked this run

1. `curl` (desktop Chrome user agent, no rate limiting observed) on all three parent hubs:
   `change-management` (98 sub-slugs, down from 107 reported 2026-09-16 as the list rotates),
   `leadership` (127 sub-slugs), `organizational-culture` (121 sub-slugs, first fetch of this tree).
2. Hand-picked 12 sub-hubs not mined on 2026-09-16, weighted toward specific, argument-shaped slugs
   over generic or glossary-sounding ones: `employee-engagement-during-change`,
   `the-psychology-of-change-management`, `consequences-of-mismanagement`,
   `stakeholder-engagement-during-change` (change-management); `leadership-impact-on-decision-making`,
   `data-driven-leadership`, `evaluating-leadership-effectiveness`, `handling-team-burnout`
   (leadership); `fostering-psychological-safety`, `creating-a-culture-of-transparency`,
   `toxic-work-environments`, `organizational-trust-dynamics` (organizational-culture).
3. `curl` on all 12 nested hubs, ~1.3s delay, no rate limiting, all HTTP 200 (395KB-453KB each).
   Extracted 112 post URLs via
   `grep -oE 'https://www\.linkedin\.com/posts/[a-zA-Z0-9_-]+activity-[0-9]+[a-zA-Z0-9_-]*'`.
4. Built a dedup index from every `post_url` in `observed/replies/*.md` and
   `queue/reply-candidates/*.md` (284 entries) and dropped exact URL matches: 110 of 112 URLs were
   fresh.
5. Activity-ID decoding (`activity_id >> 22` as epoch milliseconds) on all 110 before spending a
   read. Range: 2024-09-18 to 2026-08-13. Sorted newest first and triaged on slug wording, favouring
   negated-premise and specific-claim openers over "N ways/tips" shapes, generic inspirational
   openers, and personal-milestone posts. Shortlisted 15 for full read.
6. `curl` on all 15 shortlisted posts. 6 of 15 returned recoverable JSON-LD `articleBody`; 9 returned
   HTTP 200 with no `articleBody`. For 4 of those 9 the `og:title` still contained what reads like a
   complete one-sentence claim (Julie Hodges, Nancy Duarte, Deepali Vyas, Csaba Toth); rather than
   judge on that alone, checked for an alternate body source (`attributed-text-segment-list__content`,
   the JSON-LD `description` field) and found the `description` field on two of them resolved to
   `"chart, line chart"` / `"diagram"`, confirming the carousel/image-card failure mode rather than a
   text post with a body-extraction gap. Dropped all 9 unread, per the standing rule from the
   2026-09-14 through 2026-09-16 logs.

Total cost: 1 WebSearch (confirming the brief's named route is still dead, as required), then 3
parent-hub curl fetches, 12 nested-hub curl fetches, and 15 post curl fetches. Zero WebFetch calls
spent on hub or post retrieval; zero Brave or DuckDuckGo queries needed this run, since the hub route
alone produced enough shortlisted material.

# Posts considered

110 distinct fresh URLs reached across 12 newly-mined sub-hubs in three parent trees (two continued
from 2026-09-16, one new), 2 dropped on exact-URL dedup before triage. 15 shortlisted for full read;
6 of 15 returned usable body text, 9 had no recoverable `articleBody`. 3 selected.

## Read and individually judged

**SELECTED — Barbara Martin Coppola, `transformations-lose-people-at-a-predictable`, 2026-07-09,
454 reactions, 51 comments.** Argues transformations lose people at the moment they are handed a
change they had no hand in shaping, grounded in the IKEA effect (Norton, Mochon, Ariely 2012).
Prescribes leadership setting direction while teams own design and execution within it. Selected as
a genuine essay-shaped argument citing real research, not a listicle. Reframe added: her own logic
predicts the real failure point is the first time leadership overrules a team's build, not the degree
of initial consultation, and most transformations that claim co-creation cannot point to a single
decision where the team's build won over leadership's.

**SELECTED — Usman Sheikh, `most-managers-add-almost-no-value-microsofts`, 2025-05-14, 472
reactions, 129 comments.** Argues, using Microsoft's reported earnings and management layoffs as
evidence, that most managers add almost no value and that management layers grow reflexively rather
than strategically, creating decision friction rather than payroll cost. Selected as a structural
claim resting on a real, checkable public event rather than an invented anecdote. Counterpoint added:
the removed layer was also absorbing the gap between an unreal target and what execution could
tolerate; removing the manager does not make the target honest, it removes the person whose job was
catching that gap early and translating it upward as bad news. Flagged in the candidate file: same
author has an unposted 2026-08-12 candidate against a different post (Project Everest / EY) making a
different argument (governance and voting risk); per the working rule used 2026-08-31 and
2026-09-16, this is a note for Mark, not a veto.

**SELECTED — Thomas Gartenmann, PhD, `leadership-does-not-fail-because-people-lack`, 2026-02-06,
1,639 reactions, 182 comments.** Argues leadership fails when nervous systems are overwhelmed, not
from incompetence, and that "regulation precedes transformation": leaders need capacity, presence and
regulation before tools or frameworks. Selected despite heavy bullet formatting because the bullets
illustrate one repeated causal claim rather than being the substance. Reframe added: the project does
not wait for anyone's nervous system to regulate, and if the only channel for bad news to travel
upward runs through one person's regulated state, the organisation has made its reporting depend on
how well that person slept, which is a structural design failure dressed up as a personal-capacity
one.

**REJECTED — Pooja Jain, `when-a-dashboard-crashes-the-finger-pointing`, 2025-12-20, 892 reactions,
111 comments.** Strong opening line ("when a dashboard crashes, the finger-pointing starts") but
resolves into an emoji-headed listicle ("Data Governance = A Symphony, Not a Solo") with role-by-role
bullets and vendor-report statistics. Listicle and promotional shape.

**REJECTED — Paulo Henrique Bolgar, `a-bad-system-will-beat-a-good-person-every`, 2025-08-10, 8,235
reactions, 467 comments.** Highest engagement post read this run. Restates Deming's systems-thinking
model ("94% of performance comes from the system") with standard prescriptive bullets. Framework
explainer restating someone else's model; the only available argument would be with Deming, not this
poster, the same rejection pattern logged repeatedly since 2026-08-31.

**REJECTED — Jeff Winter, `an-unacknowledged-loop-costs-more-than-any`, 2025-01-10, 216 reactions, 95
comments.** Strong opening paragraph on "hidden factories" (unrecorded rework consuming 20-40% of
capacity, citing Feigenbaum) but resolves into a numbered "5 Practical Suggestions" list that carries
the back half of the post. Listicle shape.

**REJECTED — Faye Ellis, `putting-people-at-the-center-of-digital-transformation`, 2026-01-09, no
reaction count captured on this fetch.** Reads as an argument opener ("digital transformation isn't
about tools... it's about people") but is a Pluralsight-sponsored case study post with a tracked
product link and a client name (Kimberly Clark) used as a testimonial. Corporate promotional content,
explicit REJECT category in the brief.

## No recoverable `articleBody`, dropped unread

Nine of the 15 shortlisted returned HTTP 200 with no JSON-LD `articleBody`, the same carousel/
image-card failure mode logged on 2026-09-14 through 2026-09-16: Friska Wirya
(`strategy-is-a-spreadsheet-organizational`), Deepali Vyas
(`professional-burnout-typically-isnt-caused`), Roman Tsova
(`when-i-measure-psychological-safety-in-organizations`), Julie Hodges
(`many-changes-fail-even-though-brilliantly`), Nancy Duarte
(`most-change-initiatives-dont-fail-because`), Csaba Toth
(`manager-engagement-just-fell-to-22-the`), Cassie Kozyrkov
(`you-can-win-your-ai-rollout-and-still-lose`), Abi Adamson
(`culture-isnt-who-you-invite-to-the-table`). For Julie Hodges and Nancy Duarte specifically, the
`og:title` contained a complete one-sentence claim that would have been temping to reply to on title
alone (Duarte: "Most change initiatives don't fail because of the change that's happening, they fail
because of how the change is communicated"); checked the JSON-LD `description` field on the group and
found `"chart, line chart"` / `"diagram"` on two of them, confirming carousel/image-card format rather
than a text post, and dropped all of them unread per the standing rule rather than judging on the
headline alone.

## Not read

95 of 110 fresh URLs were triaged out on slug wording before any fetch: generic inspirational
openers, personal-milestone and career-transition posts, numbered "N ways/lessons/tips" titles, and
several `handling-team-burnout` and `toxic-work-environments` entries that read as motivational
quote-card or coaching-testimonial content on title alone (including one, Sonnia Singh's rejection
pattern from 2026-09-16, that would likely have hit the same named-client verification problem).

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-09-17-001-coppola-the-first-override-is-the-data.md`
  Stance: reframe. Risk: low. Themes: bad news is data, all projects are swamps. New territory
  (IKEA-effect ownership mechanics in transformation) for the queue.
- `queue/reply-candidates/reply-candidate-2026-09-17-002-sheikh-the-gap-doesnt-close-it-moves.md`
  Stance: counterpoint. Risk: medium. Themes: bad news is data, deliver the possible not the fantasy.
  Flagged: same author as an existing unposted 2026-08-12 candidate against a different post; noted
  per the working author-dedup rule rather than vetoed. Names a real company's real, public layoffs;
  flagged for Mark to confirm comfort before posting.
- `queue/reply-candidates/reply-candidate-2026-09-17-003-gartenmann-the-deadline-doesnt-regulate.md`
  Stance: counterpoint. Risk: low. Themes: bad news is data, all projects are swamps. New territory
  (nervous-system/somatic leadership content) for the queue.

# Notes

- **The change-management and leadership trees are not yet exhausted and remain productive on a
  second pass.** 12 newly-mined sub-hubs (up from 10 on 2026-09-16) produced 110 fresh URLs with only
  2 exact-URL dedup drops, and 3 of 6 full reads with recoverable body text converted to selections.
  Recommend continuing to widen across untouched sub-slugs in these two trees, plus the newly opened
  `organizational-culture` tree (only 4 of 121 slugs mined so far), before returning to the exhausted
  project-management tree.
- **The no-`articleBody` carousel/image-card failure mode is now a stable rejection category across
  four consecutive runs** (2026-09-14 through 2026-09-17), and the JSON-LD `description` field
  (`"chart, line chart"`, `"diagram"`) is a fast, cheap way to confirm the format without spending a
  second fetch, worth checking before dropping a lead with an otherwise strong `og:title`.
- **Framework-restatement rejections continue to outpace listicle rejections in raw engagement**: the
  highest-engagement post read this run (Bolgar, 8,235 reactions) was rejected on the same
  "restates someone else's named model" ground as Kraaijenbrink and Lencioni's more generic posts in
  prior logs, while genuinely original argument posts (Coppola, Sheikh, Gartenmann) all sat in the
  400-1,700 reaction range. Engagement is not a useful triage signal for this rejection category.
- **Two of three selections this run lean on cited external research or public, checkable events**
  (Coppola's IKEA-effect citation, Sheikh's Microsoft earnings) rather than the poster's own
  unverifiable anecdote, which made the content-policy check (no invented quotes, no unsupported
  claims) more straightforward than usual: the reply text attributes every fact to the original
  poster or the cited study rather than asserting anything independently.
