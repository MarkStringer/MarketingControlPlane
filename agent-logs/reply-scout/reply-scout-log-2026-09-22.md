---
id: reply-scout-log-2026-09-22
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes named in the brief were attempted first, as required.

- **WebSearch, bare brief query.** Returned nine results, the same stale glossary/listicle/vendor
  set logged on every run since 2026-07-23 (Project Management Cheat Sheet, the 49 Processes post,
  40 Essential Templates, Chat Engineer's basics post, Kory Kogon's "What Is Project Management?",
  Turing's "Six Best Tools for 2023," a Harvard ManageMentor completion post, Whitney Akabike's
  post, a bare #projectmanagement post). Zero selectable posts. Confirmed dead for an eleventh
  consecutive run.
- **Google time-filtered URL.** Fetched directly with curl (desktop Chrome user agent). Returned
  HTTP 200 for the first time without a consent-page redirect, but the response body contained
  zero `linkedin.com/posts/` links on inspection (`grep -c 'linkedin.com/posts'` found one
  incidental mention, not an actual result link) and the page title was the generic "Google
  Search" shell rather than a results page. New failure shape from the 09-21 log's consent-redirect
  finding, but the practical outcome is the same: confirmed dead again.

Per the routing memory, the `top-content/project-management/` hub tree remains fully mined out
(107/107 slugs), and the `change-management`, `leadership` and `organizational-culture` trees
opened 2026-09-16/17 continue to be the productive route. This run made a fifth widening pass on
those three trees.

# What worked this run

1. `curl` (desktop Chrome user agent, ~1.3-1.5s delay, no rate limiting observed) on all three
   parent hubs to re-harvest current slug counts: `change-management` (98 sub-slugs), `leadership`
   (127 sub-slugs), `organizational-culture` (121 sub-slugs).
2. Built a "never re-fetch" filter by extracting every backtick-quoted slug-like token mentioned
   across all prior `reply-scout-log-*.md` files (391 tokens, a mix of hub slugs and rejected
   post-title slugs) and diffing it against each tree's current slug list. Left 82 unmined
   change-management slugs, 114 unmined leadership slugs, 109 unmined organizational-culture
   slugs — comfortably enough headroom that none of the three trees is close to exhausted at the
   current per-run mining rate.
3. Hand-picked 12 unmined sub-hubs, weighted toward specific, argument- or myth-shaped slugs over
   generic/glossary-sounding ones: `change-management-metrics-and-kpis`,
   `establishing-a-change-management-office`, `change-management-budget-planning`,
   `executive-roles-in-transformation` (change-management); `leadership-and-accountability-practices`,
   `conducting-performance-reviews`, `leadership-transition-planning`,
   `feedback-and-coaching-for-leaders` (leadership); `aligning-culture-with-strategy`,
   `creating-a-feedback-culture`, `employee-surveys-for-culture-insights`,
   `cultural-challenges-in-mergers` (organizational-culture).
4. `curl` on all 12 nested hubs, ~1.3s delay, no rate limiting, all HTTP 200 (350KB-461KB each).
   Extracted 110 post URLs via
   `grep -oE 'https://www\.linkedin\.com/posts/[a-zA-Z0-9_-]+activity-[0-9]+[a-zA-Z0-9_-]*'`.
5. Built a dedup index from every URL in `observed/replies/*.md` and `queue/reply-candidates/*.md`
   (297 distinct URLs). 109 of 110 fresh URLs were new by exact match; 1 dropped (a repeat
   Francesca Gino post already carrying a candidate).
6. Activity-ID decoding (`activity_id >> 22` as epoch milliseconds) on all 109 before spending a
   read. Range: 2024-08-14 to 2026-07-21. Sorted newest first and triaged on slug wording, favouring
   negated-premise and specific-claim openers over "N ways/tips" shapes and generic career/
   milestone posts. Author-slug dedup check against existing candidate files caught two authors
   already in the queue on different posts (Cicely Simpson, Charles L. Stevenson) and one likely
   near-duplicate-by-topic (Stevenson's new post is another NetSuite cost anecdote, same theme as
   his existing 2026-08-28 candidate); neither was shortlisted, per the working rule that an
   unposted candidate against a different post is a note not a veto, but reaching for a genuinely
   new author was preferred when 12 shortlist slots were available regardless.
7. Shortlisted 12 for full read. `curl` on all 12, ~1.3s delay, no rate limiting. All 12 returned
   recoverable JSON-LD `articleBody` — the first run in the log history with zero no-articleBody
   drops on a 12-post shortlist, against a stable 60-100% recovery rate on every prior run since
   2026-09-14.

Total cost: 1 WebSearch and 1 curl fetch of the brief's named routes (confirming both still dead,
as required), then 3 parent-hub curl fetches, 12 nested-hub curl fetches, and 12 post curl fetches.
Zero WebFetch calls spent on hub or post retrieval; zero Brave or DuckDuckGo queries needed.

# Posts considered

110 distinct fresh URLs reached across 12 newly-mined sub-hubs in the three continued parent trees,
109 new by exact-URL dedup. 12 shortlisted for full read; all 12 returned usable body text. 4
selected.

## Read and individually judged

**SELECTED — Ben Redhead, `your-engagement-survey-isnt-failing-to-detect`, 2026-07-21, 355
reactions, 48 comments.** Argues employee engagement surveys have become part of the problem they
measure, because response rates fall exactly where leaders most need to hear, and "listening
infrastructure" has outpaced "acting infrastructure." Prescribes response architecture: decide who
acts on what, by when, before asking. Freshest post reached this run (two months old). Selected as
a genuine structural claim with a real closing question, not engagement bait. Extension added:
project status reporting has the identical failure mode, a RAG rating nobody is accountable for
acting on.

**SELECTED — Jared Spencer, `quick-math-that-should-bother-every-ops-director`, 2026-02-19, 38
reactions.** Describes a food manufacturer's OEE dashboard reporting 78% by excluding planned
changeover downtime from the denominator; true OEE was closer to 61%, hiding roughly $2M a year in
labour and lost throughput. Coins "OEE Theater." Selected as a specific, numbered structural claim
(the metric was gamed by definition, not by lying) rather than generic dashboard complaint. Reframe
added: the metric wasn't lying, it was measuring exactly what it was built to measure, and the real
finding was that someone had to stand on the floor to find the gap.

**SELECTED — Howard Yu, `the-ceo-of-boeing-once-said-out-loud-that`, 2026-06-02, 1,287 reactions,
281 comments.** Traces Boeing's shift from engineering-led to finance-led culture after the 1997
McDonnell Douglas merger, citing the 2001 Seattle-to-Chicago headquarters move and tracing a
documented line through outsourcing and MCAS to the two 737 MAX crashes. Argues Boeing "optimized
everything legible" and lost the illegible judgement that kept it safe. Selected as a rare post
grounding a structural claim in cited history rather than an anecdote. Reframe added: generalised
the legible-vs-illegible mechanism beyond Boeing, and read the 1,700-mile move as a distance
metaphor the post implies but doesn't name.

**SELECTED — Jennifer Ayres, `if-you-think-change-management-is-a-cost`, 2025-10-10, 24 reactions.**
Argues change management is "risk insurance," citing unsourced stats (143% of expected ROI, 93% of
initiatives meeting objectives) as settled fact. Selected despite low engagement (per standing rule
that engagement isn't a useful triage signal) because the stats themselves are a genuinely arguable
target, unlike the underlying advice. Counterpoint added: those numbers are retrospective labels
applied to projects that already succeeded; "insurance" is the wrong word for a bet that gets
relabelled as wisdom by whoever wins it.

**REJECTED — Bill Staikos, `your-cx-north-star-should-not-be-nps`, 2025-05-04, 60 reactions.**
Promotional Substack post selling a paid "operating kit" (worksheets, templates, dashboard specs);
the free portion is a lead magnet, not an independent argument.

**REJECTED — Oana Labes, `most-ceos-get-a-20-page-financial-package`, 2025-12-22, 695 reactions,
102 comments.** Opens with a real hook (CEOs don't know which numbers matter) but resolves into a
six-item metrics listicle promoting a paid guide via link. Listicle-is-the-substance plus explicit
lead-magnet CTA.

**REJECTED — Carl Seidman, `forecasts-lose-trust-when-they-have-bad-assumptions`, 2025-12-08, 141
reactions.** Technical how-to on forecast documentation practices, numbered-list-is-the-substance,
generically agreeable premise (bad assumptions make forecasts untrustworthy) with no independent
claim to counter.

**REJECTED — Justin Ramdeen, `every-major-consulting-firm-published-research`, 2025-12-27, 956
reactions, 163 comments.** Aggregates named consulting-firm research on transformation failure into
a listicle with a reading-list of external links. Genuinely interesting through-line (leadership
misdiagnoses failure causes) but shape and self-promotional reading-list format tip it into
listicle-is-the-substance.

**REJECTED — Adam Danyal, `ai-talent-is-becoming-an-org-design-problem`, 2026-06-08, 1,652
reactions, 151 comments.** Sharp opening claim immediately undercut by an embedded newsletter ad
mid-post, then resolves into a fifteen-plus role listicle. Promotional content plus
listicle-is-the-substance.

**REJECTED — Meera Remani, `your-peer-became-your-boss-three-weeks-ago`, 2026-05-19, 1,432
reactions, 327 comments.** Named-example career-advice post (Jason and Maria) resolving into a
numbered "what to do instead" list. Generic executive-presence coaching, off-domain from projects
and organisational structure.

**REJECTED — Jennifer Motles (Philip Morris International), `measuring-transformation-at-pmi`,
2026-04-13, 196 reactions.** Official corporate content marketing for PMI's own transformation
metrics programme. Corporate promotional content per the brief's explicit rejection criteria.

**REJECTED — Mary O'Carroll, `hot-take-the-legalengineer-is-now-the-most`, 2026-04-02, 949
reactions, 121 comments.** Thin "hot take" asserting a new role's importance without independent
argument, closes with an outbound link (her own product/company). Self-promotional, not a claim to
counter.

## Not read

98 of 110 fresh URLs were triaged out on slug wording before any fetch: generic inspirational
openers, personal-milestone and career-transition posts, "N ways/lessons/tips" titles, and posts by
authors already carrying an existing candidate on a different post (Cicely Simpson,
`most-mid-year-reviews-are-performative`; Charles L. Stevenson, `ive-seen-companies-spend-500k-on-
netsuite`, a likely near-duplicate of his existing NetSuite candidate) not distinctive enough on
slug wording alone to justify a read when 12 other shortlist slots were available.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-09-22-001-redhead-the-photograph-is-not-the-response.md`
  Stance: extension. Risk: low. Themes: bad news is data, point of view is worth 80 IQ points.
  Freshest selection this run (two months old); extends listening/acting infrastructure to project
  status reporting.
- `queue/reply-candidates/reply-candidate-2026-09-22-002-spencer-the-metric-was-built-that-way.md`
  Stance: reframe. Risk: low. Themes: bad news is data, deliver the possible not the fantasy.
  Lowest engagement selection this run (38 reactions), selected on argument strength per standing
  rule that engagement isn't a triage signal.
- `queue/reply-candidates/reply-candidate-2026-09-22-003-yu-legible-beat-right.md`
  Stance: reframe. Risk: low. Themes: point of view is worth 80 IQ points, all projects are swamps.
  Highest-engagement selection this run (1,287 reactions); rare post grounded in cited, documented
  history rather than personal anecdote.
- `queue/reply-candidates/reply-candidate-2026-09-22-004-ayres-insurance-is-the-wrong-word.md`
  Stance: counterpoint. Risk: low. Themes: bad news is data, the project is a bet. Only true
  counterpoint (disputes the post's central evidence, not just its framing) drafted this run; flag
  for Mark that the reply asserts a general survivorship pattern in unnamed statistics, not a
  specific methodological claim, since the underlying study isn't linked.

# Notes

- **Both of the brief's named search routes were re-verified dead this run, and the Google route's
  failure shape changed again.** WebSearch is the stale glossary set for an eleventh consecutive
  run. The Google time-filtered URL returned HTTP 200 without a consent redirect for the first time
  in the log history, but the response contained no actual `linkedin.com/posts/` result links, a
  generic "Google Search" page title, and the practical outcome (zero usable results) is unchanged.
  Worth tracking whether this is Google serving an empty results shell rather than a consent wall,
  in case the underlying block softens further on a future run.
- **The three widened trees show no sign of exhaustion after a fifth pass.** 82-114 unmined slugs
  remain per tree even after subtracting every slug ever mentioned in a prior log, comfortably
  beyond what a handful of future runs will consume at 4 sub-hubs per tree per run.
- **A 12-for-12 articleBody recovery rate is the best run on record.** Every prior run since
  2026-09-14 lost at least one shortlisted post to a carousel/video/image-card page with no
  recoverable body text; this run lost zero. Sample size is one run, so treat as a data point, not
  a trend, consistent with the 2026-09-18 finding that the rate varies by hub tree and sub-hub
  rather than settling to a fixed baseline.
- **Author dedup near-miss, not exact-URL duplication, caught two candidates before a read was
  spent.** Cicely Simpson and Charles L. Stevenson both already carry unposted candidates against
  different posts. Per the working rule (adopted 2026-08-31), neither is an automatic veto, but
  Stevenson's new post restates the same NetSuite-cost argument as his existing candidate, which is
  a genuine reason to deprioritise rather than the dedup rule itself; noted here so a future run
  doesn't spend a read rediscovering the same overlap.
- **Selection mix this run leaned toward reframe (2) and extension (1) over counterpoint (1),
  consistent with the queue's general pattern** — most selectable LinkedIn arguments are basically
  sound and benefit from a structural mechanism added underneath them, rather than being wrong
  outright.

Related: [[reference-reply-scout-search-routing]]
