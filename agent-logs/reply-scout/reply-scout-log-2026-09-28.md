---
id: reply-scout-log-2026-09-28
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes named in the brief were attempted first, as required.

- **WebSearch, bare brief query.** Returned the same stale nine-result glossary/listicle/vendor set
  logged on every run since 2026-07-23 (Project Management Cheat Sheet, 49 Processes, "Project
  Management on LinkedIn" hashtag post, 40 Essential Templates, Kory Kogon's "What Is Project
  Management?", Chat Engineer's basics post, Rachel Oddie's 5-skills post, a Harvard ManageMentor
  completion post, Whitney Akabike's post). Zero selectable posts. Confirmed dead again.
- **Google time-filtered URL.** `curl` (desktop Chrome UA) returned HTTP 200, 91,981 bytes, page
  title literally `Google Search`, and zero `linkedin.com/posts/` links anywhere in the body. Same
  empty-results-shell failure shape logged 2026-09-22, confirmed again rather than a consent
  redirect this time. Checked via curl directly, not WebFetch.

Per the routing memory, skipped straight to the nested `top-content` hub route rather than
spending further calls on search engines.

# What worked this run

1. Built a "never re-fetch" filter by extracting every backtick-quoted slug-like token from all 124
   prior `reply-scout-log-*.md` files (611 distinct tokens after sort -u), then diffed it against a
   fresh `curl` of each of the three open parent trees' current sub-slug lists: `change-management`
   (98 sub-slugs, 66 unmined), `leadership` (127 sub-slugs, 98 unmined), `organizational-culture`
   (121 sub-slugs, 93 unmined). Ninth widening pass across the three trees combined, still no sign
   of exhaustion.
2. Hand-picked 12 unmined sub-hubs (4 per tree), weighted toward argument-shaped rather than
   generic/industry-vertical slugs: `building-resilience-during-change`,
   `communicating-change-to-employees`, `change-management-and-team-dynamics`,
   `change-management-resource-allocation` (change-management); `leading-with-empathy`,
   `setting-boundaries-as-a-leader`, `emotional-resilience-for-leaders`, `empowering-team-members`
   (leadership); `fostering-a-sense-of-belonging`, `role-of-empathy-in-culture`,
   `team-autonomy-and-culture`, `creating-safe-spaces-for-dialogue` (organizational-culture).
3. `curl` (desktop Chrome UA, ~1.4s delay) on all 12 nested hubs, all HTTP 200 (373KB-443KB each,
   no shell-failure sizes). Extracted 109 post URLs via
   `grep -oE 'https://www\.linkedin\.com/posts/[a-zA-Z0-9_-]+activity-[0-9]+[a-zA-Z0-9_-]*'`.
4. Built a dedup index from every `post_url` in `observed/replies/*.md` and
   `queue/reply-candidates/*.md` (299 distinct URLs). 107 of 109 fresh URLs were new by exact
   match; 2 dropped as already-queued.
5. Activity-ID decoding (`activity_id >> 22` as epoch milliseconds) on all 107 before spending a
   read, sorted newest first. Range: 2024-09-16 to 2026-09-11. Newest URL reached was 17 days old,
   consistent with every prior run's finding that the hub route cannot reach the last 24 hours.
6. Triaged on slug wording and cross-checked candidate author handles against `agent-logs/reply-
   scout/reply-scout-log-*.md` prose (post-level-duplication check) before shortlisting. One
   near-miss: `jeroenkraaijenbrink` surfaced again (`psychological-safety-is-not-about-being-nice`);
   he already carries two unposted candidates against different posts and has been repeatedly
   flagged (2026-09-18, 2026-09-23, 2026-09-24 logs) as consistently deprioritised in favour of new
   authors when other slots are available. Dropped from the shortlist on that basis with 15 other
   candidates available, not treated as a hard veto.
7. Shortlisted 16 for full read (15 fresh + 1 swap-in after dropping Kraaijenbrink:
   `onlypranavgupta`). `curl` on all 16, ~1.3s delay, no rate limiting. 15 of 16 returned recoverable
   JSON-LD `articleBody`; 1 (`alexey6`, "Miracle House Wasn't a Miracle, It Was Graceful
   Degradation") had none, and the JSON-LD `description` field read "Video Captions for Miracle
   House...", confirming a video-caption post per the 2026-09-21 finding. Dropped unread, no second
   fetch spent.
8. Confirmed the change-management/leadership/organizational-culture authorship bug again on all 4
   selected posts: JSON-LD `author.name` named a different, unrelated person in every case
   (Sandeep Nair's post claimed "Ashiish V Patil"; Desmond Dunn's claimed "Stephanie Kuczynski";
   Nancy Duarte's claimed "Habeeb Rasul"; Amir Satvat's claimed "Richard Browne"). `og:title` and
   the `aria-label="View profile for <name>"` attribute both independently confirmed the correct
   author in every case, and each confirmed name matched the URL vanity slug.
9. Verified `datePublished` against the activity-ID decode on all 4 selected posts; all 4 matched
   exactly (2025-01-12, 2026-03-24, 2025-12-17, 2025-09-08).

Total cost: 1 WebSearch and 1 curl confirming both brief routes still dead, 3 parent-hub curl
fetches, 12 nested-hub curl fetches, 16 post curl fetches. Zero wasted fetches beyond the one
expected video-caption drop.

# Posts considered

109 distinct fresh URLs reached across 12 newly-mined sub-hubs in the three continued parent
trees, 107 new by exact-URL dedup. 16 read in full (15 with recoverable body text, 1 dropped
unread as a video-caption post). 4 selected.

## Read and individually judged

**SELECTED — Desmond Dunn (`desmondcdunn`), `the-hard-part-of-mixed-income-housing-is`,
2026-03-24, 384 reactions, 63 comments.** Argues mixed-income housing developments hit their
compliance ratios and still fail as places, because the math is necessary but not sufficient;
what actually works is shared space, street-level programming, consistent dignity across unit
types, and management as social infrastructure. Not a listicle-is-the-substance post: the
sub-headers are elaboration on one governing claim ("mixed-income is not a compliance strategy,
it's a social project"), the shape credited in past logs to Lusiyano/Kline. Selected as a
structural argument transferable to project delivery generally: hitting budget, schedule and
scope percentage is routinely treated as the definition of success even though none of those
measure whether the delivered thing works for the people using it.

**SELECTED — Nancy Duarte (`nancyduarte`), `as-a-leader-the-way-you-deliver-bad-news`,
2025-12-17, 509 reactions, 24 comments.** Argues that how a leader delivers bad news matters more
than the content, and proposes a four-way diagnostic (Fix It, Bounce Back, Shut It Down, Move On)
illustrated with her own firm's mistake plus Airbnb, Instagram and Steve Jobs examples. Her own
original framework, not a restatement of someone else's named model, so it clears the
framework-restatement rejection that a Lencioni or Tuckman recap would trip. Selected on the
repeatable "argue with the reason, not the advice" move: her two diagnostic questions are both
about the content of the news, neither is about timing, and a well-delivered message that arrives
late changes category regardless of tone.

**SELECTED — Amir Satvat (`amirsatvat`), `when-you-are-firing-employees-just-say-you`,
2025-09-08, 367 reactions, 44 comments.** Argues leaders should announce layoffs in plain,
specific language instead of corporate euphemism, listing roughly thirty examples ("rightsizing,"
"recalibrating our workforce," etc.) as illustration of a single claim, not the substance itself.
Selected because the reply can trace the euphemism back past the announcement to an earlier,
unstated bet (the growth plan that justified the original hiring was never named as a bet with a
downside), which is a different and earlier point in the causal chain than the one he makes.

**SELECTED — Sandeep Nair (`sandeepnairtvpm`), `when-junior-team-members-speak-last-meetings`,
2025-01-12, 1,644 reactions, 72 comments.** Describes a P&G practice of having the most junior
person in the room speak first in meetings, crediting the result to confidence-building and
efficiency. Selected because the reply supplies a sharper, more specific mechanism than the one
offered: speaking order changes outcomes through anchoring, not just confidence, meaning a senior
opinion voiced first edits everyone's later answer before they're aware it's happened.

## Rejected, read in full

- **Sandeep Nair-adjacent check, `elfriedsamba`, `when-your-best-people-start-to-go-quiet`,
  2024-11-07, low engagement not separately captured.** Opens on a strong claim (silence from core
  talent is a culture signal, not an ideas gap) but resolves into a 4-item numbered
  "how to fix it" list that carries the entire prescriptive content. Listicle-is-the-substance.
- **Omar Halabieh (`omarhalabieh`), `i-thought-i-knew-what-ownership-was-but`, 2024-12-18.**
  Personal-reflection post resolving into two 3-item numbered lists (what I used to think / what
  I've learned), closing on an engagement question and a follow-me CTA. Generic career-advice
  shape; ownership-as-a-theme is also already covered by the 2026-09-24 Koldas "unowned risk"
  candidate from a sharper, incident-grounded angle.
- **Dr. Chris Mullen (`chrismmullen`), `most-teams-arent-unsafe-theyre-afraid`, 2025-04-10.** Sharp
  negated-premise opener ("not about being nice... about building an environment where truth can
  exist") that resolves into "10 Ways to Foster Psychological Safety" (actually 15 numbered items).
  Listicle-is-the-substance, closes with a repost CTA and a daily-posting plug.
- **Jonathan Vanderford (`jonathan-vanderford`), `we-tried-every-ai-team-structure-they-all`,
  2025-08-20.** Genuinely argument-shaped opening (stop treating AI as a team member, organise
  around problems not roles) but the substance is a five-role "pod" org chart delivered as a
  bulleted list, and the domain (AI team structure) skews toward the AI-hype content the
  2026-09-24 log flagged as off the brief's domain.
- **Richard Harpin (`rharpin`), `most-people-are-taught-how-to-be-high-performers`, 2025-08-05.**
  Restates seven borrowed, named frameworks in sequence (Sinek's Start With Why, the 70-20-10 rule,
  Frei's Trust Triangle, the Tuckman model, the Johari Window, an "Energy/Impact Matrix," the RAPID
  model), each with its own sub-bullets, closing with a link to the author's own book. Textbook
  framework-restatement rejection, worse than usual for stacking seven models in one post.
- **Justin Wright (`jwmba`), `i-managed-teams-for-10-years-before-i-learned`, 2025-08-21.**
  Anecdote opener resolves into an 8-item bulleted "ways to show empathy" list, closes with a
  lead-magnet plug ("Get my 99 best cheat sheets"). Listicle-is-the-substance plus promotional
  close.
- **Ashley Couto (`ashleycouto`), `some-people-call-empathy-a-pathological`, 2026-04-10.**
  Provocative opener (empathy called a "pathological weakness") resolves into a description of
  Danish childhood education delivered as two bulleted lists plus three headline statistics,
  closing on an engagement question and a repost/follow CTA. Adjacent-domain (education policy)
  but list-shaped and thin on a falsifiable claim beyond "empathy is good."
- **Pranav Gupta (`onlypranavgupta`), `saturday-appreciation-monday-layoff`, 2025-04-04.** Sharp
  contrast opener resolves into a numbered "how to prepare for a layoff" list (Resume = Living
  Document, etc). Listicle-is-the-substance.
- **David Carlin (`david-carlin7`), `underwriting-the-transition`, 2025-06-08.** Announcement of a
  UN-convened insurance-industry report on climate transition underwriting guidance. Corporate/
  institutional promotional content naming a specific report and initiative, excluded per the
  brief's corporate-promotional-content rule.
- **Ravit Jain (`ravitjain`), `resilience-is-a-design-choice-not-a-lucky`, 2025-11-20.** Strong
  negated-premise opener immediately pivots into promoting "two reads worth your time from
  Cloudera," a named vendor's architecture whitepapers. Vendor-promotional content, excluded.
- **John P. Carter (`johnpcarter`), `as-chief-engineer-of-strategic-ballistic`, 2025-08-25.**
  Submarine-engineering anecdote resolves into a 5-item bulleted list of leadership principles
  (Delegation, Intent-based leadership, etc), then pivots explicitly into startup-scaling
  leadership-coaching content with a 6-hashtag stack. Listicle-is-the-substance plus off-domain
  pivot.

## Rejected unread (no recoverable body text)

- **Alexey Navolokin (`alexey6`), `the-miracle-house-wasnt-a-miracle-it`, 2026-09-01.** No
  JSON-LD `articleBody`; the `description` field read "Video Captions for Miracle House Wasn't a
  Miracle, It Was Graceful Degradation," confirming a video-caption post. Dropped unread per the
  2026-09-21 finding; no second fetch spent. Genuinely the sharpest opening line of the run's
  shortlist (negated-premise, engineering-adjacent) and the only loss of this kind this run.

**Rejected unread tally: 1 (video-caption).**

# Replies drafted

- `reply-candidate-2026-09-28-001-dunn-the-math-was-never-the-hard-part.md` — Desmond Dunn, deliver
  the possible not the fantasy / all projects are swamps.
- `reply-candidate-2026-09-28-002-duarte-timing-is-the-missing-axis.md` — Nancy Duarte, bad news is
  data.
- `reply-candidate-2026-09-28-003-satvat-the-euphemism-started-earlier.md` — Amir Satvat, the
  project is a bet / bad news is data.
- `reply-candidate-2026-09-28-004-nair-whoever-speaks-first-wins-the-room.md` — Sandeep Nair, point
  of view is worth 80 IQ points.

# Notes

- New mined sub-hubs this run, do not re-fetch: `building-resilience-during-change`,
  `communicating-change-to-employees`, `change-management-and-team-dynamics`,
  `change-management-resource-allocation`, `leading-with-empathy`, `setting-boundaries-as-a-leader`,
  `emotional-resilience-for-leaders`, `empowering-team-members`, `fostering-a-sense-of-belonging`,
  `role-of-empathy-in-culture`, `team-autonomy-and-culture`, `creating-safe-spaces-for-dialogue`.
- The three trees remain nowhere near exhaustion (66/98/93 unmined slugs respectively after this
  run), consistent with the finding logged every run since 2026-09-16.
- **Framework-restatement is still the single most common rejection ground after listicle shape,
  and today's Harpin post is the densest example logged to date** — seven distinct named,
  borrowed frameworks stacked in one post, closing on a book plug. Worth flagging as a distinct
  severity tier from a single-framework restatement (e.g. Kraaijenbrink, Bolgar), since the only
  available reply to a seven-framework stack would have to pick one framework to engage with and
  ignore the rest, which reads as arbitrary.
- **Author-dedup near-miss handled per the standing working rule.** Jeroen Kraaijenbrink surfaced a
  third time (now across 2026-09-18, 2026-09-23/24 mentions and this run); he was again
  deprioritised rather than vetoed, consistent with the pattern that authors closest to the book's
  material keep resurfacing and keep losing out to unseen authors when the shortlist has slack.
  Worth flagging to Mark directly: if the unposted 2026-04-27 and 2026-07-13 Kraaijenbrink
  candidates are still good, they're sitting unposted while newer material keeps taking priority
  by default; that's a queue-management question rather than a sourcing one.
- **Corporate/vendor-promotional rejections clustered unusually this run**, 2 of 11 full-body
  rejections (Carlin's UN report, Jain's Cloudera plug) against roughly 1 in 10 on a typical prior
  run. Both had strong opening lines that only revealed the promotional pivot a paragraph in,
  consistent with the 2026-09-16 finding that a post's shape often only becomes clear after the
  opening line, not from it.
- Four selections, at the top of the brief's 2-4 range, judged justified because all four cleared
  the bar independently (distinct book themes, distinct mechanisms, no shared reply logic with
  each other or with the two most recent runs) rather than being padded to hit a count.
- 15-of-16 `articleBody` recovery this run, consistent with the recent run of high recovery rates
  (12-for-12 on 2026-09-22, 16-for-16 on 2026-09-25) rather than the 60-70% baseline seen in mid-
  September; still likely hub/sub-hub dependent per the 2026-09-18 finding rather than a fixed
  baseline.
