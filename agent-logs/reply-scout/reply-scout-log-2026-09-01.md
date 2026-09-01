---
id: reply-scout-log-2026-09-01
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Both routes named in the brief were attempted first, as required. Both failed again, for the eighth
consecutive run.

- **WebSearch, bare brief query.** Returned the identical stale evergreen set seen on every run
  since 2026-07-23: Chat Engineer "Project Management (The Basics)", "Understanding the 49 Project
  Management Processes", a project management cheat sheet, Turing's "Six Best Project Management
  Tools for 2023", Kory Kogon's "What Is Project Management?", a 40-templates-and-dashboards post,
  plus two Wikipedia articles. Every LinkedIn result is a list, glossary, tool round-up or
  definition post, and all fall under the standing rejection rules. Zero selectable posts, eight
  runs running.
- **Google time-filtered URL.** HTTP 302 to `consent.google.com`, which cannot be cleared from here.
  Unchanged from the previous run and still unusable.
- **Brave, past-week variant.** "Too few matches were found." Brave reported that it did not apply
  the search operators at all, so the `site:` filter was ignored. No LinkedIn URLs returned.

# What worked this run

The nested top-content hub route, carried out over `curl`. It worked as documented and consumed no
WebFetch calls for hub or post reading.

1. `curl` on the parent `top-content/project-management` hub. Yielded 107 distinct sub-slugs,
   unchanged from the 2026-08-31 run. The older `pulse/topics/project-management-s5788` path now
   returns a 301 with an empty body and should be considered dead.
2. `curl` across 22 nested hubs, deliberately chosen to avoid the 14 used on 2026-08-31 so the
   sampled population would differ: earned value management, governance models, setting project
   deadlines, creating project status reports, cost control, prioritising project tasks, quality
   assurance, project management roles, strategic planning, developing KPIs, portfolio management,
   budget monitoring, methodologies, innovation management, continuous improvement, evaluating
   performance metrics, trend analysis, PMO functionality, tracking milestones, showcasing project
   successes, integration techniques. One hub (`continuous-improvement-in-project-management`)
   returned nothing on the first pass because of a filename collision in the fetch loop and was
   re-fetched successfully in the second pass.
3. Activity-ID decoding on all 171 distinct URLs before spending any read, using the documented
   `(activity_id >> 22) / 1000` shift, then sorting by decoded date.
4. `curl` on 14 shortlisted posts. All 14 returned full bodies. Engagement counts and
   `datePublished` were parsed from the same fetched HTML, so no second pass was needed.

Total cost: 2 WebFetch calls and 1 WebSearch call, all three spent on the failed search engines
before falling back. Zero WebFetch spent on hubs or posts. Zero rate limiting on curl.

**Decoder accuracy.** The decoded date matched the page's own `datePublished` structured data
exactly on all three selected posts. That is the seventh consecutive run the decoder has been exact.

**One method regression to note.** LinkedIn's rendered relative timestamp ("3 weeks ago" and so on)
could not be read reliably this run. The values now come back as minified tokens in the fetched DOM,
so the regex used on previous runs returns junk. Dates in all three candidates therefore rest on the
`datePublished` structured data rather than the relative timestamp the template asks for. That is
the stronger source, not a weaker one, but the template wording should probably be updated to say so.

# Posts considered

171 distinct posts reached and triaged on decoded date plus opening line. 14 read in full.
3 selected.

## Read and individually judged

**SELECTED — Mira Sarac, `every-mining-investment-is-approved-on-forecasts`, 2026-08-02, 68
reactions, 19 comments.** Sustained argument, no list, and the second most recent post reached on
the whole run. Every mining investment is approved on forecasts, so governance should quantify how
much movement the case can absorb before the recommendation changes. Mark can grant all of it and
argue that sensitivity analysis produces a switching point, which is a decision rule written in
advance, and that nobody converts it into a trigger with a date and an owner, so the condition the
Board said it would refuse arrives later as a line in a monthly report.

**SELECTED — Chris Danek, `our-contract-manufacturer-was-rapidly-falling`, 2026-07-29, 59
reactions, 16 comments.** A worked anecdote resolving into a falsifiable causal claim: adoption is
not a willpower problem, people adopt what costs less and gets more. Mark can concede the claim and
argue that what the Post-it board removed was exposure rather than effort, that what got cheaper was
the promise, and that this is why the contract manufacturer voluntarily rolled it out to every other
client.

**SELECTED — Neelam Heera-Shergill, `public-involvement-should-not-be-free-every`, 2026-08-04, 86
reactions, 10 comments.** The single most recent post reached on the entire run. Public involvement
should be budgeted from the start, because payment is equity and paid involvement is more
representative. Mark can agree and supply the mechanism: her own comparison list is the tell, since
venues and catering are budgeted because they issue invoices, and work with no invoice never enters
the plan, so it cannot be late or under-delivered and is therefore unfalsifiable. Flagged below as a
deliberate widening of subject matter.

**REJECTED — Nicolas Sauvage, `most-kpi-systems-fail-for-a-simple-reason`, 2026-01-11.** Opens with a
real claim, that KPI systems measure activity rather than impact and only work when designed as a
decision tool. Then spends the entire body walking through SMART letter by letter with a personal
variant on the "A". Rejected as a framework explainer with an acronym spine. The reply would argue
with SMART rather than with the author.

**REJECTED — Benjamina Mbah Acha, `status-reports-will-tell-you-everything-is`, 2026-02-16, 110 reactions, 107
comments.** The closest of all the rejections and the only one I would revisit if Mark wants a
fourth. Argues that real warning signs show up in behaviour rather than reports, and that status
reports are lagging indicators while behavioural signals are leading ones. There is a genuine reply
available, that a signal the PM notices privately and has no place to put in the report is not data
anyone is obliged to act on. Rejected on the standing list-post rule: the body is six numbered
signals each with a "what to do", which is a listicle whatever the framing. The 107 comments also
mean the obvious angles are already taken.

**REJECTED — Faizan Jalil, `the-first-thing-an-analyst-should-build-isnt`, 2026-07-18, 674
reactions.** Highest engagement of the run by a wide margin. Trust the data before you build the
dashboard. Correct, well argued, and unarguable. It is also data analytics rather than project
management, and it resolves into a checklist plus "garbage in, garbage out". Only available reply is
agreement.

**REJECTED — Rohit Madhok, `in-large-deals-the-real-competition-is-rarely`, 2026-03-17, 158
reactions, 18 comments.** Genuinely good post. Large deals are lost to inertia, deals die because
they never travelled far enough inside the organisation, and they quietly become "No Decision".
There is a strong Mark reply in the fact that nobody ever has to sign a no. Rejected purely on
saturation: that argument is already made in
`reply-candidate-2026-08-04-001-stacey-governance-carries-a-no` and
`reply-candidate-2026-08-10-003-knight-the-only-remedy-nobody-has-to-sign`, neither of which has
been posted yet. Worth reconsidering once those clear the queue.

**REJECTED — Stephanie Hills, `they-say-everythings-urgent-until-urgency`, 2026-01-02, 1,137
reactions, 404 comments.** By far the highest engagement in the sample. A short anecdote followed by
nine numbered prioritisation frameworks (Eisenhower, Pareto, 5/25, RICE, MoSCoW, ABCDE, time
blocking, eat that frog, batching) and a masterclass link. Textbook list post with a lead magnet
attached.

**REJECTED — Mohammad Alsous, `in-project-management-what-gets-reported`, 2026-01-30.** "What gets
reported gets managed, and what gets visualized gets understood", then five ticked benefits of
reporting and five bullets on what a good dashboard shows. Generic PMO content, unfalsifiable
throughout, five hashtags.

**REJECTED — Anubhav Shukla, `heres-the-uncomfortable-truth-ive-learned`, 2026-05-30.** Cost
feedback arrives after the design is frozen, so move cost visibility upstream into design. A real
and well-made argument, and structurally close to things Mark believes about moving decisions to
where options still exist. Rejected because the post is essentially correct and the only reply is
agreement with a different vocabulary, and because it is cost engineering rather than project
management. Second-closest rejection after BAMA.

**REJECTED — Mohammad Alsarfandi, `youve-selected-your-implementing-partner`, 2026-05-27.** Five-point pre-award financial assessment
framework for INGO sub-grantees, closing with a pitch for 18 Excel workbooks. List post with a
product attached.

**REJECTED — Lawrence M., `most-companies-see-knowledge-management-as`, 2026-06-12.** Average
organisation versus high-performing organisation, four arrow bullets each side, closing engagement
question. A two-column comparison list, and proposal operations rather than project management.

**REJECTED — Lukasz Lazewski, `when-projects-or-companies-scale-senior`, 2026-03-12.** Three
paragraphs on documenting senior engineers' historical context to shorten onboarding and improve
estimation accuracy. Short, entirely reasonable, and makes no claim with enough edge to argue with.

**REJECTED — Mayank Rathi, `portfolio-reporting-the-hardest-part-of`, 2026-04-14, 229 reactions.**
Detailed and specific, on parsing Indian mutual fund RTA feeds, ending in an open-source repo
announcement. Technically excellent and completely outside Mark's territory. Nothing to add that is
not domain knowledge he does not have.

## Triaged on headline and date, not read

The remaining 158 fell into the standing rejection categories on their opening line alone: tool
comparisons and software round-ups, certification and course announcements, ISO and audit
checklists, template packs, "N mistakes" listicles, engagement-bait questions, conference promotion
and vendor content. One of them, **Ankit Kumar,
`8d-report-a-structured-approach-to-problem`, 2026-07-01**, was shortlisted on its date and then
dropped on its headline without being fetched, as a walkthrough of the eight disciplines of the 8D
method.

Four are worth naming because of their position in the ranking. **Datatale AU,
`julys-power-bi-update-has-one-feature-worth`, 2026-07-22** was the third most recent post reached
and is a product release note. **Mike Herak, `leading-indicators`, 2026-06-24** was well placed and
was skipped on author dedup, having already been drafted against in
`reply-candidate-2026-08-27-002-herak-nobody-was-fired-for-waiting`. **Yuri Nedre,
`project-managers-are-not-reminder-machines`, 2026-06-16** likewise, see
`reply-candidate-2026-08-19-001-nedre-the-reminder-is-a-bid`. **George Zeidan,
`what-leaders-choose-not-to-do-matters-more`, 2026-03-06** is a second post by the author already
rejected on 2026-08-31 for executive broetry, and the format is unchanged.

Two further authors were skipped on dedup rather than quality: Cory Blumenfeld
(`most-managers-cant-delegate`, already covered by
`reply-candidate-2026-08-21-001-blumenfeld-delegation-needs-levers`) and Gabor Stramb
(`project-managers-are-still-wildly-misunderstood`), who has been drafted against repeatedly and is
the most over-used author in the queue.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-09-01-001-sarac-the-switching-point-has-no-date.md`
  Stance: counterpoint. Risk: low. Themes: the project is a bet, bad news is data. Nothing to
  verify. The fourteen-versus-nine month ramp-up figure is explicitly a hypothetical built on the
  author's own ramp-up example, not a claim about any real project.
- `queue/reply-candidates/reply-candidate-2026-09-01-002-danek-what-got-cheaper-was-the-promise.md`
  Stance: structural observation. Risk: low. Themes: deliver the possible not the fantasy, bad news
  is data. Nothing to verify; every figure and quoted phrase is the author's own.
- `queue/reply-candidates/reply-candidate-2026-09-01-003-heera-shergill-free-work-cannot-be-late.md`
  Stance: extension. Risk: medium. Themes: bad news is data, deliver the possible not the fantasy.
  **Needs Mark's eye before posting.** The risk is tone, not accuracy. The subject is people sharing
  deeply personal health experiences and the reply argues in the language of budget lines and
  falsifiability. It opens by granting her case outright and the argument strengthens rather than
  undercuts her, but Mark should read it once for coldness and cut the second half if it reads as
  treating people as line items.

# Notes

- **Deliberate widening of subject matter, for Mark's decision.** The Heera-Shergill post is
  research and policy involvement budgeting, not project management as the brief means it. It was
  selected because it was the most recent post reached on the entire run, it makes a clean argument
  rather than a list, and the structural point about unbudgeted work being unfalsifiable is one of
  the better ones available this month. If Mark wants the queue kept strictly inside project
  management, this is the candidate to drop and the boundary should be written into the brief.
- **The recency problem is now structural and worth fixing in the brief.** Of 171 URLs reached, six
  were from the last 60 days and the most recent post found anywhere was 2026-08-04, four weeks old.
  LinkedIn's top-content hubs are curated for durability rather than freshness, so the "past 24
  hours" framing has not been achievable through any available route for eight consecutive runs.
  The 2026-08-31 log raised this and it should now be decided rather than re-raised: the brief
  should either say "recent and not previously covered" or the scouting method needs a source that
  is not a search engine and not a curated hub.
- **Sampling worked.** Rotating to 22 previously unused hubs produced 171 URLs against the prior
  run's 134, and no post read this run had been read before. The rotation is worth keeping as
  standing practice, and the list of hubs used on each run is now recorded in these logs for that
  purpose.
- **Saturation is easing slightly.** The three selections argue about three different things: an
  unmonitored decision rule, the economics of removing a commitment, and unbudgeted work being
  unfalsifiable. None of them is another "bad news does not get surfaced" draft, which was the
  warning in the 2026-08-31 log. Two posting conflicts to respect: do not post Sarac in the same
  week as `2026-08-25-002-lusiyano` or `2026-08-27-001-modigliani`, and do not post Danek in the
  same week as `2026-08-24-001-simpson`.
- **Author dedup was run against the full contents of `observed/replies/` and
  `queue/reply-candidates/`.** All three selected authors are new to the repo with no near-miss name
  collisions. The only substring hits on "Mira" were inside the unrelated willis and cutler files.
- The `pulse/topics/project-management-s5788` URL used by earlier runs now 301s to an empty body.
  Future runs should go straight to `top-content/project-management`.
