---
id: reply-scout-log-2026-08-31
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes in the brief were attempted first, as required, and both failed again.

- **WebSearch, bare brief query.** Returned the same stale 2022 to 2023 evergreen set that every run
  since 2026-07-23 has seen: Chat Engineer "Project Management (The Basics)", "Understanding the 49
  Project Management Processes", a project management cheat sheet, Rachel Oddie's five skills post,
  Kory Kogon's "What Is Project Management?", plus two Wikipedia articles. Every one is a list,
  glossary or definition post. All fall under the standing rejection rules. Zero selections, seven
  runs running.
- **Google time-filtered URL.** HTTP 302 to `consent.google.com`, which cannot be cleared from here.
  Still unusable. (Previous run hit a 429 instead; either way it does not work.)
- **Brave, bare brief query and a past-week variant.** "Too few matches were found." The unfiltered
  Brave query returned the same evergreen glossary set as WebSearch.
- **DuckDuckGo html endpoint.** CAPTCHA challenge page, no results.
- **Three topical WebSearch variants** (deadlines/estimates, AI replacing PMs, status reports and
  steering committees). All returned LinkedIn Pulse articles, LinkedIn Learning courses and tool
  round-ups rather than feed posts. Nothing usable.

# What worked this run

The nested top-content hub route from the 2026-08-28 run, carried out entirely over `curl`. It
worked exactly as documented and needed no WebFetch calls at all for post reading.

1. `curl` on the parent `top-content/project-management` hub. Yielded 107 distinct sub-slugs, two
   fewer than the 2026-08-28 run reported.
2. `curl` across 14 nested hubs, chosen for argument density rather than tooling: post-mortems,
   lessons learned, decision analysis, crisis management, monitoring and controlling,
   risk assessment, stakeholder engagement, leadership skills, conflict resolution, trend analysis,
   performance metrics, scope definition, feedback integration, predictive strategies. Post URLs
   extracted with a regex for `linkedin.com/posts/...activity-<id>`.
3. Activity-ID decoding on all 134 distinct URLs before spending any read, using the documented
   `(activity_id >> 22) / 1000` shift. Confirmed exact against LinkedIn's own `datePublished`
   structured data on all three selected posts, which is the sixth consecutive run the decoder has
   been exact.
4. `curl` on 9 shortlisted posts, returning 8 full bodies and 1 partial. Then `curl` again on the 3
   selected for reaction and comment counts.

Total cost: 6 WebFetch calls, every one of them spent on the failed search engines before falling
back, plus 5 WebSearch calls. Zero WebFetch spent on hubs or posts. Zero rate limiting on curl.

# Posts considered

134 distinct posts reached and triaged on decoded date plus opening line. 9 read (8 full bodies, 1
partial). 3 selected.

## Read and individually judged

**SELECTED — Prof. Bent Flyvbjerg, `new-paper-the-small-is-safe-myth-is-ruining`, 2026-07-20, 634
reactions, 59 comments.** Highest-engagement and highest-quality post of the run. One falsifiable
claim carrying real numbers from 5,094 IT projects: the smallest 20% have the worst cost
performance, mean overrun 192%. Mark can grant the data entirely and move the mechanism, arguing
that a review threshold is a published price list that shapes what "small" means, and that
exempting a project from review removes not just the check but the addressee for bad news.

**SELECTED — Melissa Perri, `your-annual-planning-process-is-probably`, 2026-03-15, 185 reactions,
23 comments.** Sustained argument, no list. She states the problem exactly ("no one has permission
to say so out loud") and then prescribes strategic intents instead of features, which does not touch
permission. Mark can argue the swap has an unpriced cost: a feature list is a bad plan and a good
alarm, and an intent absorbs any twelve months and still reads as on track.

**SELECTED — Rony Rozen, `if-the-decision-meeting-is-exciting-i`, 2025-12-22, 33 reactions, 13
comments.** Lowest engagement of the three and the sharpest argument to push back on. Pre-socialise
every objection so the go/no-go is boring. Mark can concede the case against ambush and then argue
that a privately handled objection leaves no witnesses and no date, and that Rozen's own success
criterion, absence of drama, is satisfied both by a resolved disagreement and by one that went
underground.

**REJECTED — Jeroen Kraaijenbrink, `teams-rarely-fail-because-people-are-unwilling`, 2025-12-05.**
The best-written rejection of the run. A careful walk through Lencioni's Five Dysfunctions attached
to a visual. Rejected as a framework explainer: the post restates a model rather than making a
claim, so any reply is either agreement or an argument with Lencioni rather than with the author.

**REJECTED — Chris Ortega (Fresh CFO), `i-thought-we-would-have-seen-results-by`, 2026-07-17.**
Client-conversation anecdote resolving into "trust is built in uncomfortable conversations" plus
three numbered lessons and a closing question. Genuine and entirely unarguable. The only available
reply is agreement.

**REJECTED — Christian Wattig, `you-cant-treat-every-forecast-the-same`, 2026-04-09.** Three
forecasting techniques (avoid assumption stacking, run what-if analysis, show a range) with a
template lead magnet. There is a real reply buried in it, that a published range gets collapsed to
one number by whoever reads it, but the post is a list post with a download attached and it is FP&A
rather than project management. Closest of the rejections to a fourth selection.

**REJECTED — George Zeidan, `decision-avoidance-in-leadership-is-rarely`, 2025-12-23.** Executive
broetry: one-line paragraphs, bulleted pressures, four disciplined practices, "follow for more
insights". Generic leadership content with nothing specific enough to argue with.

**REJECTED — Ivan Garcia Dominguez, `most-teams-measure-success-by-deadlines-met`, 2025-11-06.**
Outcomes over outputs, adoption over delivery, five hashtags and an employer mission statement.
Correct and unfalsifiable. Reply would be generic commentary.

**REJECTED — James Saunders, `heres-how-a-single-stakeholder-sunk-a-30m`, 2025-11-05.** Read
partially only; the fetch returned the opening but truncated before the resolution. A £30m FM bid
lost because the tender was built on one stakeholder's stated priority. A decent structural reply
exists, that the error was treating a stated priority as a fact rather than a bet. Rejected on
recency and saturation without completing the read: it is ten months old and sits very close to
reply-candidate-2026-08-25-002-lusiyano, which already argues about assumptions travelling upward
unchallenged.

## Triaged on headline and date, not read

The remaining 125 fell into the standing rejection categories on their opening line alone: tool
comparisons and software round-ups, certification and course announcements, "N mistakes I made"
listicles, engagement-bait questions, conference promotion, and vendor content.

Two are worth naming because of their position in the list. **Dr Michael White,
`waterfall-vs-agile-ba-do-you-know-the-differences`, 2026-08-02** was the single most recent post
reached on the whole run and is a straight comparison-table post, rejected on its slug under the
list and glossary rule. **Zubin Rashid,
`most-ld-professionals-learned-the-kirkpatrick`, 2026-08-01** was the second most recent and is
learning-and-development rather than project management.

Three further posts were skipped on author dedup rather than quality, having already been drafted
against this month: Thomas Lusiyano
(`boards-dont-get-surprised-by-poor-results`), Omar Alenezi
(`in-20-years-of-managing-mega-projects-i`), and Dave Kline
(`your-team-isnt-missing-deadlines-because`, 2026-07-30, which would otherwise have been a strong
read given it is the third most recent post reached).

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-31-001-flyvbjerg-bad-news-with-no-address.md`
  Stance: reframe. Risk: low. Themes: bad news is data, the project is a bet. Nothing to verify.
- `queue/reply-candidates/reply-candidate-2026-08-31-002-perri-a-bet-you-cannot-lose.md`
  Stance: counterpoint. Risk: low. Themes: the project is a bet, bad news is data. Nothing to
  verify.
- `queue/reply-candidates/reply-candidate-2026-08-31-003-rozen-boring-and-unwitnessed.md`
  Stance: counterpoint. Risk: medium. Themes: bad news is data, point of view is worth 80 IQ points.
  **Needs Mark's sign-off on one point:** paragraph five compresses the big-room planning beat from
  `observed/replies/2026-04-02-langin-bad-guy-reply.md`, which has already been posted on LinkedIn
  once. No new detail was invented, but the reuse is his call.

# Notes

- **The open question from the 2026-08-25 and 2026-08-26 runs is now answered in practice.** Both
  runs flagged that Flyvbjerg's "small is safe" post kept being rejected purely against an unposted
  candidate from 2026-05-07, and asked whether author dedup should have a re-reply exception. This
  run took it, on the grounds that the earlier candidate has never been posted, targets a different
  post from 2022, and makes a different argument. If Mark disagrees with that call, candidate 001
  is the one to drop and the rule should be written down.
- The hub route reaches good posts and old ones. Of 134 URLs, only 5 were from the last 60 days.
  LinkedIn's top-content hubs are curated for durability, not recency, so the "past 24 hours"
  framing in the brief is not achievable through this route and has not been achievable through any
  route for seven runs. Worth deciding whether the brief should be rewritten to say "recent and not
  previously covered" rather than "past 24 hours".
- Saturation warning. Three of the ten posts read in full were about surfacing uncomfortable
  information, and two of the three selections argue about it from different angles. The Rozen draft
  is also adjacent to `reply-candidate-2026-08-24-001-simpson-the-meeting-was-insurance`. If both
  Rozen and Simpson are approved, they should not be posted in the same week.
- Author dedup was run against the full contents of `observed/replies/` and
  `queue/reply-candidates/`. One prior Flyvbjerg candidate exists (2026-05-07) against a different
  and much older post; the two arguments do not overlap and the difference is recorded in the new
  candidate's notes.
