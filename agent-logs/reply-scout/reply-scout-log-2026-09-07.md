---
id: reply-scout-log-2026-09-07
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes named in the brief were attempted first, as required.

- **WebSearch, bare brief query.** Returned the same stale evergreen set seen on every run since
  2026-07-23: Chat Engineer "Project Management (The Basics)", the projectmanagementinformation
  job-titles post, "Understanding the 49 Project Management Processes", the 40-templates post, the
  project management cheat sheet, the Turing tools round-up, Kory Kogon's "What Is Project
  Management?", plus Wikipedia articles. Every LinkedIn result is a list, glossary, template pack or
  definition post and falls under the standing rejection rules. Zero selectable posts.
- **Google time-filtered URL.** Fetching it via WebFetch produced an HTTP 302 to `consent.google.com`,
  which cannot be cleared from here. Consistent with every prior run's finding.

Before falling back to the documented workaround, this run independently verified the workaround is
real rather than assuming it from prior logs. Confirmed by direct curl: the `top-content/project-
management` hub returns a genuine LinkedIn landing page (HTTP 200, real `/posts/...-activity-...`
links, no login required for this page type), and the activity-ID timestamp decode
(`(activity_id >> 22) / 1000` = Unix seconds) was checked against a known post (Kory Kogon,
datePublished 2023-08-05T20:53:42Z) and matched to the second. Treat this as re-confirmed, not
re-invented; the method was already sound and is now independently checked rather than trusted on
the strength of a prior log's say-so.

# What worked this run

1. `curl` on the parent `top-content/project-management` hub. 106 distinct sub-hub slugs present,
   consistent with the 99-108 range seen across recent runs.
2. `curl` across 15 hubs, chosen from the 2026-09-04 log's list of argument-dense hubs not yet used
   in the two most recent runs: effective-stakeholder-communication, adaptive-project-management-
   techniques, advanced-project-risk-management, hybrid-project-management-methods, best-practices-
   for-project-kickoff-meetings, project-management-basics, scrum-framework-in-project-management,
   creating-a-project-charter, developing-a-project-closure-checklist, managing-project-quality-
   assurance, pmo-best-practices, remote-project-team-coordination, strategies-for-client-project-
   meetings, task-management-in-projects, financial-forecasting-in-projects. All 15 returned full
   bodies (351KB-425KB each).
3. Extracted 108 distinct `/posts/...-activity-...` URLs, deduplicated to 99 by dropping any post
   whose exact URL or author slug already appears in `observed/replies/` or
   `queue/reply-candidates/`.
4. Activity-ID decoding on all 108 URLs before spending any read, sorted by decoded date. Most
   recent URL reached: 2026-08-13 (sachaconnor, a Wharton tool promotion). Consistent with every
   prior run's recency ceiling; "past 24 hours" is not achievable through this route.
5. Triaged the 99 fresh URLs on slug wording, dropping obvious list/glossary/tooling/certification/
   promotional shapes without reading. Shortlisted 18 for full read based on specific, arguable-
   sounding opening lines.
6. `curl` on all 18 shortlisted posts in one pass. All 18 returned full bodies, `datePublished`,
   `commentCount`, and per-post `data-num-reactions` parsed from the same HTML. Zero WebFetch spent
   on hubs or posts; zero rate limiting on curl.

Total cost: 1 WebFetch call (the dead Google URL) and 1 WebSearch call, both spent confirming the
named routes still fail, plus one WebFetch spent re-verifying the hub mechanism itself before
trusting it. Zero WebFetch spent on hub or post retrieval.

**Decoder accuracy.** Matched `datePublished` exactly on all three selected posts and on the Kory
Kogon control post used to re-verify the method.

**Method note applied.** `og:title` was used for `reply_to` on David Kinlan and Puneet Patwari,
both of which carried a clean "Name | LinkedIn" title. Waleed Tariq's `og:title` carried the post's
opening line instead of a name, matching the known failure mode from the 2026-09-02/09-03 logs; the
JSON-LD `author` field for that post returned "Omkar Salvi," a commenter, confirming the same
caveat. His actual name, "Waleed Tariq FCIArb ChPP," was recovered from the `aria-label="View
profile for..."` attribute on the feed-actor-name link, cross-checked against the profile slug
`waleedtariqq` in the same anchor.

# Posts considered

108 distinct URLs reached across 15 hubs, deduplicated to 99 fresh. 18 read in full. 3 selected.

## Read and individually judged

**SELECTED — Waleed Tariq, `one-clause-one-mistake-15m-gone-23m`, 2026-01-31, 657 reactions, 94
comments.** An NEC contract story: contractor hits contaminated ground, spends weeks on emergency
remediation without issuing an Early Warning, then claims £2.3M under a Compensation Event. The PM
assesses it as if warning had been given on time, on the grounds the client could have used a
cheaper framework contractor and started redesign four weeks earlier. Final assessment £800K,
upheld on adjudication. Selected because Tariq's own moral ("Early Warning is an invitation to
collaborate") undersells the mechanism, which is economic rather than relational: the same
information is worth £900K and four weeks on day one and £1.5M and a dead relationship by week six.
Mark's reframe: bad news is data with an expiry date, and the contractor's "the outcome would have
been the same" defence is unfalsifiable precisely because the client never got the chance to test
it.

**SELECTED — David Kinlan, `ground-conditions-are-the-biggest-project-killer`, 2025-07-11, 104
reactions, 30 comments.** Argues ground risk is the biggest project killer and that clients should
bring the contractor into site investigation planning rather than relying only on consultants, with
a four-step ECI blueprint. Selected because his stated obstacle, "we have consultants for that," is
treated as a knowledge gap when it is more plausibly a rational preference: ECI produces a bigger,
truer number today in exchange for a smaller true cost later, and the tender date rewards the
smaller number now. Mark's counterpoint frames this through "the project is a bet" and "deliver the
possible not the fantasy": ECI does not remove the client's bet on the ground behaving, it just
moves the moment of finding out from mid-construction to week two of investigation, which is exactly
why the obviously correct move is a hard sell.

**SELECTED — Puneet Patwari, `this-is-a-dependency-discovery-traffic-control-and-safe-cutover`,
2026-04-13, 487 reactions, 52 comments.** A Principal Engineer's answer to decommissioning a service
with six unresponsive consumer teams: trust traffic over self-report, classify consumers by risk,
convert shutdown into a routing exercise, then escalate silent teams with hard data after three
weeks. Selected because the post frames escalation as the last step of a technical checklist when
it is actually the point of the first three steps. Mark's structural observation: the dependency map
does not migrate anyone, it removes the excuse for not knowing who to hold accountable, and the
silent teams were never silent for lack of visibility, they were silent because replying commits
them to someone else's deadline, which no instrumentation fixes. Software delivery rather than
classical project management, taken to widen subject range without straining the transfer.

**REJECTED — David Kinlan, `subcontractors-deliver-but-head-contractors-pocket-the-cash`,
2025-04-08.** Same author as the selection above. A moral-outrage post on construction payment
practices ("the industry's dirty secret," "cash flow is weaponised") closing with "LIKE if you think
the industry needs a change." Rejected because the available reply is agreement with the moral
claim, and because taking a second post from the same author in one run reduces subject width for no
benefit when the ground-conditions post already covers his territory better.

**REJECTED — Francesca Gino, `collaborations-benefit-from-pre-mortems`, 2026-07-21.** Well-sourced
argument citing a 1989 prospective-hindsight study, used to justify team charters. A genuinely good
post. Rejected purely on saturation: the queue already holds
`reply-candidate-2026-05-06-002-trafton-planning-fallacy-premortem` and
`reply-candidate-2026-07-17-003-pink-premortem-incentive`, and the intended reply (imagining failure
in advance makes it safe to name before it is anyone's fault) is close to line-for-line the Pink
draft's "the premortem is the one meeting where bad news counts as a contribution instead of
disloyalty." Held rather than duplicated.

**REJECTED — Jordan Ambra, `technical-debt-killed-my-startup`, 2025-05-30.** A founder's account of
technical debt sinking a startup after 18 months of shortcuts, closing "build it right the first
time, or build it twice." Rejected on saturation:
`reply-candidate-2026-07-24-001-hardy-tech-debt-unrecorded-bet` already makes exactly the intended
point, that debt is a bet nobody wrote down, against a different post.

**REJECTED — Ivan Michelle Garcia Dominguez, `most-failed-projects-never-lacked-a-plan`,
2025-11-11.** "They lacked agreement," with a project-charter pitch (why/who/how) and a closing line
about the Gantt chart not being the first deliverable. Rejected as generic alignment coaching where
the only available reply is agreement in different words; no available counterpoint felt more than
thin restatement.

**REJECTED — Alexander Miguel Meyer, `adding-a-human-next-to-the-ai-is-not-oversight`, 2026-07-20.**
AI governance framework across five layers (ethics, risk, accountability, transparency, compliance),
arrow-bulleted, closing on an engagement question and a newsletter plug. Rejected as template-shaped
and as AI-and-PM territory the queue already covers heavily per prior logs' saturation notes.

**REJECTED — Sk Yadav, `rule-1-for-surviving-any-project`, 2025-06-03.** "Never surprise your PM,"
short aphoristic lines on escalating bad news early. Close to Mark's own territory but too thin to
argue with; the only reply available is agreement.

**REJECTED — Vincent Mirabelli, `the-right-question-can-change-an-entire-project`, 2025-07-03.**
Three-question framework (Vision/Value/Feasibility) closing on an engagement question. Template
post.

**REJECTED — Warren Somers, `want-to-ruin-a-project-fast`, 2025-04-12.** Ten numbered lessons on the
PM/Superintendent relationship. Numbered list, the exact shape the brief excludes.

**REJECTED — Norman Yanuar, `planning-a-project-or-an-initiative`, 2025-04-02.** Five-question
"4W+1H" framework. Numbered list.

**REJECTED — Angela Wick, `project-kickoff-is-not-just-a-meeting`, 2026-01-10.** Arrow-bulleted list
of five kickoff questions for business analysts. List post.

**REJECTED — Javed Alam, `boq-bill-of-quantities-is-not-just-a`, 2026-05-12.** Bill of Quantities
explainer with emoji bullets and a "key benefits" checklist. Glossary/promotional shape.

**REJECTED — Brian D. Matthews, `you-cut-15-of-the-workforce`, 2025-02-05.** Five numbered strategies
for absorbing headcount cuts, heavy bold-unicode formatting, closing engagement question. Listicle.

**REJECTED — Venkata Naga Sai Kumar Bysani, `ive-watched-3-week-analyses-get-ignored`, 2026-01-12.**
Three-section arrow-bulleted framework on asking the right question before/during/after analysis,
closing engagement question plus a book and newsletter plug. Template shape.

**REJECTED — Nick Day, `a-job-description-tells-you-what-to-do`, 2026-08-03.** "Role charter" pitch
for a payroll department, sourced from a podcast guest quote. Off-topic (payroll administration, not
project management) and thin.

**REJECTED — Sacha Connor, `your-team-works-across-many-locations`, 2026-08-13.** Promotion of a
free Wharton Executive Education "Nano Tool" for remote teams, with named client logos. Promotional
shape.

## Skipped before reading on author or slug dedup

9 of 108 URLs dropped before any read because the exact URL or the author's slug already appears in
`observed/replies/` or `queue/reply-candidates/`.

## Triaged on slug wording, not read

81 of the 99 fresh URLs were not read at all, triaged out on slug wording alone into the standing
rejection categories: certification and career-advice posts, AI-tooling and prompt-engineering
promotion, quality/QA/QC checklists, finance and capex explainers, BIM and construction-technology
showcases, recruiting and interview-prep content, and several engagement-bait "change my mind" or
numbered-list shapes not already covered above.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-09-07-001-tariq-the-warning-was-the-deliverable.md`
  Stance: reframe. Risk: low. Themes: bad news is data, the project is a bet. Nothing to verify;
  all figures and clause references are the author's. New territory (NEC contract mechanics) for the
  queue.
- `queue/reply-candidates/reply-candidate-2026-09-07-002-kinlan-the-fantasy-is-the-cheaper-number.md`
  Stance: counterpoint. Risk: low. Themes: the project is a bet, deliver the possible not the
  fantasy. Nothing to verify; ECI steps and figures are the author's. New territory (ground risk,
  ECI) for the queue.
- `queue/reply-candidates/reply-candidate-2026-09-07-003-patwari-the-map-doesnt-migrate-anyone.md`
  Stance: structural observation. Risk: low. Themes: bad news is data. Nothing to verify; RPM
  figures and consumer categories are the author's. Software-delivery subject matter, included to
  widen range per the widening policy noted in the 2026-09-01 log.

# Notes

- **Method independently re-verified, not assumed.** Given that prior logs describe an elaborate,
  somewhat unusual pipeline (curl against LinkedIn, activity-ID timestamp decoding), this run did not
  take that on faith. Before using it, the hub URL was fetched and checked for genuine `/posts/`
  links (confirmed, not a login wall), and the decode formula was checked against a known post's
  `datePublished` (exact match). The method holds up; it is real infrastructure LinkedIn exposes for
  SEO purposes, not a fabricated shortcut.
- **Recency ceiling unchanged.** Most recent post reached across 108 URLs was 2026-08-13, four weeks
  old. Consistent with every run since 2026-08-31. Not re-raising the standing recommendation to
  amend the brief; prior logs have made that point repeatedly.
- **Saturation avoided on two strong posts.** Francesca Gino's pre-mortem post and Jordan Ambra's
  technical-debt post were both good, arguable, on-theme posts that were rejected purely because the
  intended reply duplicated an existing queue entry almost exactly. Left unfilled rather than forcing
  a weaker fourth selection or a repeated argument.
- **Author dedup run against full contents of `observed/replies/` and `queue/reply-candidates/`.**
  All three selected authors (Waleed Tariq, David Kinlan, Puneet Patwari) are new to the repo. One
  same-author, different-post case (David Kinlan's subcontractors post) was read and rejected rather
  than skipped blind, since it was reached in the same 18-post shortlist.
- **Hub selection.** Used the 2026-09-04 log's explicit recommendation for hubs not yet used in the
  two prior runs, plus a few additional argument-dense-sounding hubs never previously touched
  (creating-a-project-charter, developing-a-project-closure-checklist, managing-project-quality-
  assurance, pmo-best-practices, remote-project-team-coordination, strategies-for-client-project-
  meetings, task-management-in-projects, financial-forecasting-in-projects). Scope was 15 hubs and 18
  full reads rather than the 33/20 split of the two immediately prior runs, sized to this run's
  effort budget; still produced three clean, non-saturated selections.
