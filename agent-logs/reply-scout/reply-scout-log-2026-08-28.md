---
id: reply-scout-log-2026-08-28
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes in the brief were attempted first, as required, and both failed as they have on every
run since 2026-07-23.

- **WebSearch, bare brief query.** Returned the same stale 2022 to 2023 glossary set as the previous
  five runs: Chat Engineer "Project Management (The Basics)", "Understanding the 49 Project
  Management Processes", a project management cheat sheet, Rachel Oddie's five skills post, Kory
  Kogon's "What Is Project Management?", plus two Wikipedia articles. Every one is a list or
  definition post and every one falls under the standing rejection rules. Zero selections, six runs
  running.
- **Google time-filtered URL.** HTTP 429. Previously it 302'd to a consent page that could not be
  cleared; it now rate limits outright. Still unusable.

# What actually worked this run

**The nested top-content hub route carried the run, and it got materially cheaper.** The significant
finding is that **`curl` against a nested hub returns clean post URLs, and `curl` against a post URL
returns the full post body**, both for free and without spending a single WebFetch call.

Three WebFetch calls were spent on hubs before this was discovered, and all three came back with
"URL: Not provided in excerpt" because the summarising model dropped the links. The same three pages
fetched via curl yielded ten post URLs each. After that, every hub and every post on this run was
read through curl.

Concretely, this run cost 5 WebFetch calls total and reached 82 distinct posts with dates and 9 full
post bodies. Previous runs spent one WebFetch per post read.

**Route used, in order:**

1. One WebFetch on the parent `project-management` hub to harvest sub-slugs. Yielded 107 slugs, up
   from 105 on 2026-08-25.
2. `curl` across 10 nested hubs, extracting post URLs with a regex for
   `linkedin.com/posts/...activity-<id>`.
3. Activity-ID decoding on all 82 URLs before spending any read. Dates were then confirmed against
   LinkedIn's own `datePublished` structured data on the three selected posts and matched exactly
   on all three, which is the fifth consecutive run the decoder has been exact.
4. `curl` on 9 shortlisted posts for full body text and engagement counts.

Zero Brave queries were needed. Zero rate limiting was encountered on curl.

# Posts considered

82 distinct posts were reached and triaged on decoded date plus opening line. 9 were read in full.
3 were selected.

## Read in full and individually judged

**SELECTED — Steve Schmitz, `pmo-advice-keeps-answering-how-the-work-gets`, 2026-04-30, 163
reactions, 25 comments.** Single sustained argument, no list, no framework: PMO advice answers how
work gets done but never whether the portfolio matches the chosen strategy, and that question has no
owner. Mark can argue it has no *date* rather than no owner, and that a PMO asking it well argues
itself smaller.

**SELECTED — Dr Sunita Gandhi, `i-eliminated-all-deadlines-projects-finished`, 2025-12-08, 58
reactions, 12 comments.** Specific falsifiable claim with two worked outcomes. Mark can grant the
result and overturn the mechanism: she removed the penalty for an honest date, not the date.

**SELECTED — Charles Stevenson, `you-paid-400000-for-netsuite-and-you`, 2026-02-27, 272 reactions,
39 comments.** Taken under the list-post rule: six prescriptive steps hanging off one falsifiable
causal claim, "this isn't an ERP problem, it's a behavior problem", which stands without them. Mark
can argue the workaround is unreported fit data whose suppression is reputational, not behavioural.
Highest engagement reached on the run.

**REJECTED — Francesca Gino, `collaborations-benefit-from-pre-mortems`, 2026-07-21.** The closest
near miss of the run and the most recent post reached. Summarises a 1989 prospective-hindsight study
and advocates pre-mortems and team charters. A genuine counterpoint exists, that pre-mortems are run
after money is committed, which is when the useful answers can no longer change anything. Rejected
on saturation: the timing of honest risk talk relative to commitment is already argued by
`2026-08-26-002-gudorf-uncertainty-avoidance-on-credit` and
`2026-08-26-001-donohue-the-cheap-test-is-the-expensive-one`. Worth revisiting if that ground clears.

**REJECTED — G R Malik, `a-company-doesnt-stall-because-people-are`, 2026-02-24.** Good negated-premise
opening, but the list is the substance (document judgment, design frameworks, identify friction,
convert work to structure, train for outcomes) and it duplicates the systems-versus-behaviour ground
the Stevenson selection covers better.

**REJECTED — Ayushi Malviya, `sprint-capacity-planning-committing-to-what`, 2026-07-05.** Pure
explainer with a worked arithmetic example. Glossary post under the standing rule.

**REJECTED — Ivan Garcia Dominguez, `most-failed-projects-never-lacked-a-plan`, 2025-11-11.** Strong
negated-premise opening but resolves into a three-item charter checklist, and the alignment and
shared-understanding ground is already carried by `2026-08-13-002-attieh-the-ambiguity-was-the-
settlement` and `2026-08-18-001-saheed-the-answer-gets-frozen-at-funding`.

**REJECTED — Bruno Celso Freitas, `everyone-says-pmos-should-be-lean-i-say`, 2025-06-21.** Contrarian
opening, but the post is a three-layer PMO org model. The list is entirely the substance.

**REJECTED — Pete Modigliani, `in-a-dynamic-world-why-are-we-still-anchoring`, 2025-05-20.** Author
dedup. Already drafted yesterday as `2026-08-27-001-modigliani-the-baseline-was-never-a-forecast`.

## Triaged on decoded date and opening line, not read in full

Rejected without a full read for the reason marked against each hub. No post below survived both the
list/glossary rule and the author-dedup check on its opening line.

### adaptive-project-management-techniques

**Leaks badly into generic leadership and time management.** 8 posts. Produced the Malik read. Contains a "7 time management tips" post and an Advent-of-Code day 14 post, so the slug is not reliably on topic.

- 2026-02-24 | `grmalik29_a-company-doesnt-stall-because-people-are`
- 2025-12-14 | `borjamenendezmoreno_day-14-of-the-adventofor-2025-the-single`
- 2025-09-30 | `lucy-philip_you-cant-call-it-partnership-if-stakeholders`
- 2025-09-01 | `linksrinivasan_for-all-of-us-time-is-the-most-valuable`
- 2025-07-23 | `nsauvage_capital-is-not-the-bottleneck-execution`
- 2025-06-28 | `jennymfernandez_pov-yes-there-are-enough-hours-in-a-dayif`
- 2025-05-21 | `rahul-patil1999_i-was-once-working-on-a-project-where-one`
- 2025-03-26 | `coachmallikarao_7-time-management-tips-that-work`

### building-project-management-offices

**Usable, thin.** 7 posts. PMO org-structure models, PMO-layer explainers, certificate announcements and "when you need a PMO" advice. Freitas and Bandukwala read and rejected as list posts. Everything else is a role explainer.

- 2026-08-04 | `giovana-dalascio_pmi-pmo-certificate`
- 2026-04-30 | `steve-c-schmitz_pmo-advice-keeps-answering-how-the-work-gets`
- 2026-03-31 | `brianlemmings_the-pmo-should-be-woven-into-business-strategy`
- 2026-03-03 | `hussainbandukwala_you-just-became-a-pmo-leader-congrats-youre`
- 2025-12-22 | `elizabethdworkin_when-you-need-a-pmo`
- 2025-11-10 | `sohamdasgupta22_pmo-layers-explained-enterprise-vs-program`
- 2025-06-21 | `brunocelsofreitas_everyone-says-pmos-should-be-lean-i-say`

### creating-a-project-charter

**Usable.** 10 posts. Produced the Gino near miss and the Ivan Garcia read. The rest are charter templates and "key elements of" checklists, which is the glossary pattern this slug will always attract.

- 2026-07-21 | `francescagino_collaborations-benefit-from-pre-mortems`
- 2026-05-07 | `businesscoachradhikadhawan_i-have-watched-so-many-hours-wasted-in-businesses`
- 2026-04-07 | `amcclain_im-currently-in-week-three-of-my-new-role`
- 2026-01-31 | `adamstoverink_most-teams-have-unspoken-rules-the-best`
- 2025-11-12 | `ugochinyereamaonyeanaso_before-you-start-any-project-you-need-a`
- 2025-11-11 | `ivan-garcia-dominguez-delivery-manager_most-failed-projects-never-lacked-a-plan`
- 2025-07-07 | `ferraroroberto_ive-watched-so-many-hours-wasted-because`
- 2025-05-08 | `francismbunya_key-elements-of-a-powerful-agile-team-charter`
- 2024-11-12 | `adam-open-org_if-youre-a-hr-people-leader-struggling`
- 2023-09-27 | `justinbateh_the-quickest-way-to-create-project-charters`

### defense-acquisition-processes

**Usable but mostly news and policy.** 7 posts. NDAA language, drone marketplaces, defence investment commentary. Modigliani sits here and was dedup-rejected. Argument density is low because most posts are reporting rather than claiming.

- 2026-07-05 | `stuolden_buying-the-dip-actually-the-defence-investment`
- 2026-03-19 | `jonmost_proposed-ndaa-language`
- 2026-03-03 | `relentless_ready-for-prime-time-over-the-past-two-years`
- 2026-01-14 | `mike-wior_we-can-no-longer-afford-to-wait-a-decade`
- 2025-08-13 | `matt-higgins-rse_army-poised-to-build-drone-marketplace-for`
- 2025-08-06 | `carlo-viray_i-just-went-to-one-of-the-most-impressive`
- 2025-05-20 | `petermodigliani_in-a-dynamic-world-why-are-we-still-anchoring`

### earned-value-management-in-projects

**Mis-titled. Returns construction and EPC contract law, not earned value.** 9 posts covering contract types, EPC lifecycles and procurement clauses. Not one post about EVM. Add to the mis-titled list; never fetch again.

- 2025-10-18 | `head-of-procurement-supply-chain-manager_in-procurement-choosing-the-right-contract`
- 2025-09-01 | `anjola-ige_from-studying-finance-in-my-mba-to-practicing`
- 2025-05-16 | `davidkinlan_7-hidden-traps-in-design-construct-contracts`
- 2025-04-22 | `ali-hazrat-0300_do-you-understand-the-full-epc-project-lifecycle`
- 2025-04-01 | `antonia-botero-ra-ncarb-6473282b_here-are-some-construction-contract-fundamentals`
- 2025-02-19 | `eyad-al-ali_how-contractual-is-the-programme-different`
- 2025-01-06 | `eng-waana-luvila-426442257_epc-contract-management`
- 2024-12-06 | `itsakhilmishra_a-few-months-ago-i-spoke-to-a-project-manager`
- 2024-09-01 | `colinslevy_as-a-corporate-saas-lawyer-i-want-to-dive`

### evaluating-project-performance-metrics

**Leaks into unrelated evaluation domains.** 8 posts, including RAG-system evaluation, Web3 and techno-economic energy modelling. Measurement is also the single most saturated theme in the queue, so even the on-topic ones were dropped.

- 2025-11-06 | `ivan-garcia-dominguez-delivery-manager_most-teams-measure-success-by-deadlines-met`
- 2025-09-15 | `antonionietorodriguez_hi-everyone-would-you-drive-a-car-without`
- 2025-09-01 | `a-bach_if-you-benchmark-projects-on-kwp-you-miss`
- 2025-07-20 | `singhsidhukuldeep_unlocking-the-next-era-of-rag-system-evaluation`
- 2025-04-07 | `nadine-zidani_everyones-talking-about-impact-but-very`
- 2025-01-31 | `phillionaire_you-cant-manage-what-you-dont-measure`
- 2024-12-30 | `dawidhanak_the-harsh-truth-without-proper-techno-economic`
- 2024-09-27 | `arjunvirsingh_web3-the-household-name-in-the-making`

### implementing-erp-systems

**Good, and outside project management proper, which is where selections keep coming from.** 9 posts. Produced the Stevenson selection. Two posts make the identical "buying tech is easy, getting adoption is hard" argument (Hammond, Rogers) and were dropped as duplicates of each other and of the weaker half of Stevenson.

- 2026-02-27 | `charleslstevenson_you-paid-400000-for-netsuite-and-you`
- 2026-01-01 | `ahmed-shalaby-sap_article-3-why-erp-workshops-are-not-meetings`
- 2025-12-02 | `daledenham_one-of-the-biggest-reasons-erp-implementations`
- 2025-12-02 | `rorythedutchie_training-isnt-a-side-thing-in-your-fo`
- 2025-11-04 | `adileh-mountain_your-erp-went-live-successfully-so-why-is`
- 2025-09-16 | `brandonhammond_buying-tech-is-easy-getting-adoption`
- 2025-05-25 | `shobhamoni_we-revived-3-failed-erp-projects-in-90-days`
- 2025-02-14 | `tomrogerscpa_buying-technology-is-easy-getting-people`
- 2024-04-05 | `geoff-baldock-cfo_are-you-considering-implementing-a-new-erp`

### research-implementation-challenges

**Off-target for replies.** Only 6 posts, and they are research-funding and health-policy commentary rather than project argument. Real domain, wrong register.

- 2026-07-06 | `natalieyeadon_vital-health-data-platform`
- 2026-02-17 | `ehsan-mirdamadi_canada-spends-50-billion-a-year-on-rd-and`
- 2026-01-09 | `eleanor-macpherson_impact-focused-funding-and-knowledge-mobilisation`
- 2025-12-22 | `oandasan_tbphc-primary-care-teams`
- 2024-11-05 | `kyle-briggs_the-biggest-hurdle-to-economic-benefit-from`
- 2024-09-18 | `jaywerber_while-some-aspects-of-research-funding-in`

### setting-project-deadlines

**Best hub of the run and the deadlines vein is confirmed still open.** 10 posts, all genuinely about deadlines, all making claims rather than defining terms. Produced the Gandhi selection. Folarin "your project plan is a lie" and Kudva "stop working 48 hours before the deadline" are both live leads left unread for a future run.

- 2025-12-08 | `dr-sunita-gandhi_i-eliminated-all-deadlines-projects-finished`
- 2025-09-21 | `jainpkk05_leadership-beyond-deadlines-in-many-organizations`
- 2025-06-27 | `chris-mielke_project-management-isnt-about-rigid-timelines`
- 2025-06-02 | `tomader-saleh-ba47b52b_why-do-agile-coaches-get-mad-when-you-ask`
- 2025-05-02 | `roopakudva_what-if-you-stopped-working-48-hours-before`
- 2025-04-06 | `thedolphin_agile-project-management-critical-chain`
- 2025-04-02 | `cassandraleecoach_trust-collapsed-after-one-missed-deadline`
- 2025-03-31 | `albert-schiller_handlingunrealisticdeadlines`
- 2025-03-17 | `fisayofolarin_your-project-plan-is-a-lie-or-becomes-one`

### tactical-planning-in-project-management

**Mis-aimed. Returns demand forecasting and retail promotion analytics, not tactical planning.** 9 posts, of which four are demand-forecasting content. Treat as a soft mis-title; not worth a second fetch.

- 2026-07-05 | `ayushi-malviya93_sprint-capacity-planning-committing-to-what`
- 2026-04-18 | `matthewcorneliusgreen_your-team-missed-forecast-by-14m-last-quarter`
- 2025-10-14 | `hiral-pandya-9a97b2b0_when-teams-grow-design-their-experience`
- 2025-04-17 | `marciadwilliams_7-red-flags-in-demand-forecasting-and-how`
- 2024-12-27 | `andrewconstable-mba_why-ethical-and-reasonable-goals-matter`
- 2024-11-11 | `panwu_buy-one-get-one-free-promotion-aware-demand`
- 2024-07-12 | `s-carolinalago_see-how-easily-you-can-project-monthly-volumes`
- 2023-10-10 | `vlafemina_nonprofit-department-heads-heres-a-critical`
- 2023-10-06 | `jeffreyrwinter_demand-forecasting-is-the-process-of-using`

## Hubs fetched via WebFetch before the curl method was found

- **`conflict-resolution-in-project-teams`** — REJECTED as a hub. 10 posts, all generic leadership,
  HR and psychological-safety content (Chris Do, Francesca Gino, Greg McKeown, Ross Dawson). No
  project argument. Adjacent-discipline leak, not a mis-title.
- **`mastering-proposal-development`** — **Newly confirmed mis-titled. Never fetch again.** 9 posts,
  of which six are personal-boundaries and saying-no content (Unnati Bagga, Kevin Kermes, Maryann
  Jamieson, Cory Blumenfeld). Nothing to do with proposals. Cory Blumenfeld is also already in the
  queue. This makes eight confirmed mis-titled hubs.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-28-001-schmitz-the-question-with-no-date.md` —
  structural observation. Strategic misfit is invisible because it produces no dated event, not
  because it has no owner, so the green status is honest. And a PMO that asks the question well
  argues itself smaller, so the asker cannot be the person whose budget is the answer. Ends on
  re-approval dates: a bet gets re-priced, not monitored.
- `queue/reply-candidates/reply-candidate-2026-08-28-002-gandhi-a-date-you-owe-nobody.md` — reframe.
  Two things were deleted and the wrong one gets the credit. She removed the cost of giving an
  honest date, which only the person who absorbs the consequences can do. Deadlines synchronise the
  people not doing the work, so removing one and finding nobody notices is a useful finding in
  itself.
- `queue/reply-candidates/reply-candidate-2026-08-28-003-stevenson-the-experiment-already-ran.md` —
  counterpoint. Two years of manual exports is not a behaviour problem, it is the best fit data the
  organisation will ever produce, filed as user error. It never travels upward because the
  configuration was approved by a named person, so the annual workaround cost is the price of not
  reopening a decision.

# Notes

- **Method change worth carrying forward: use `curl`, not WebFetch, for both hubs and posts.** Hubs
  return post URLs cleanly and posts return full body text in the `og:description` and
  `attributed-text-segment-list__content` fields, plus reaction counts via `data-num-reactions` and
  the exact publication date via the `datePublished` structured-data field. No rate limiting was hit
  across 10 hub fetches and 9 post fetches with a 1 to 2 second delay. This removes the per-post
  WebFetch budget that has constrained every previous run and retires the 2026-08-26 complaint that
  the hub route is capped by fetch cost. The remaining cap is real and unchanged: no pagination, ten
  posts per hub, roughly 29 of 107 slugs now mined.
- **`datePublished` is available directly, so activity-ID decoding can now be checked rather than
  trusted.** It matched on all three selected posts. Keep decoding as the cheap first filter, since
  it works on a URL alone without a fetch, but confirm from the page once a post is read.
- **Two new mis-titled hubs: `mastering-proposal-development` (boundaries content) and
  `earned-value-management-in-projects` (construction contract law).** Add `tactical-planning-in-
  project-management` as a soft mis-title returning demand forecasting.
  `setting-project-deadlines` is the best hub found this run.
- **Saturation remains the binding constraint, three runs running.** Four otherwise selectable posts
  were rejected purely on ground the queue already argues: pre-mortem timing (Gino), alignment and
  charters (Garcia), measurement (the whole performance-metrics hub). Reaching more posts is no
  longer the problem; the reachable argument space is.
- **Post age.** Selected posts are 4 months, 6 months and 9 months old. Nothing from the last 24
  hours was reachable, which is the same tooling limitation recorded on every run since 2026-07-23,
  not an editorial choice. The most recent post reached at all was 2026-07-21 (Gino, rejected on
  saturation), and the most recent in the whole 82-post pool was 2026-08-04.
- **Author dedup this run: 1 rejection (Modigliani), against 19 on 2026-08-12 and 10 on 2026-08-14.**
  That is not a sign the population has recovered. It is because widening into ERP, defence
  acquisition and PMO structure reached authors the queue has never touched. The pattern of selecting
  from outside project management proper now holds for five consecutive runs.
- **Open question for Mark, raised on 2026-08-25 and still unanswered, now with a third instance.**
  Does author dedup have a re-reply exception for candidates that were drafted but never posted? The
  Modigliani rejection today is against a candidate drafted yesterday and not yet approved. If the
  rule exists to avoid looking repetitive on one author's feed, an unposted draft arguably should not
  trigger it.
