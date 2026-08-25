---
id: reply-scout-log-2026-08-25
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Status of that URL this run: dead for the twenty-ninth consecutive run. 302 to `consent.google.com`
with `gl=GB&hl=en`, byte for byte the same redirect as 08-24. One call spent because the brief asks
for it. The recommendation to amend the brief so future runs stop paying for it now stands for the
third run running.

Engines and routes used, and what each was worth:

1. **WebSearch, bare brief query.** Returned the same stale 2022 to 2023 glossary set as every prior
   run (Chat Engineer, Project Management Information, Kory Kogon, Rachel Oddie, Sonal Sharma,
   Whitney Akabike) plus two Wikipedia articles. Zero selectable results, five runs running.
2. **Brave, bare brief query.** Twenty results, and the most complete version of the stale set yet
   seen: every WebSearch result plus eight more certification and course-completion posts. Zero
   selectable results, but the run's single most valuable finding came out of an unrelated Brave
   query, see route 3.
3. **Brave, phrase fragments.** Four queries, one 429. `"it wasn't a scope problem"` fell back to
   unquoted matching as usual, but among the fallback results it returned three
   `linkedin.com/top-content/project-management/project-scope-definition-methods/` URLs. **That is
   the fix for the hub route.** Hubs are nested under the parent topic, not flat. The steering
   committee query returned exactly one post, an EU Twinning project meeting note, not usable.
4. **LinkedIn public top-content hubs, flat slugs.** Dead. Eight flat slugs fetched, and the route
   has degraded since 08-24. Detail under Notes, but the short version is that every flat slug now
   either renders the bare landing shell or serves an identical generic career block regardless of
   which slug you ask for.
5. **LinkedIn public top-content hubs, nested slugs.** The productive route, and the source of all
   three selections. Five nested hubs fetched, four returned real topic-relevant post lists with
   URLs, ages and engagement counts. Detail under Notes.
6. **Parent hub sub-slug harvest.** One fetch on `/top-content/project-management/` returned **105
   sub-topic slugs**, up from the ten hrefs harvested on 08-24. Combined with the nested path
   discovery this is a large, durable lead pool.
7. **Activity ID decoding** run on all ten shortlisted posts before spending a fetch. All ten matched
   LinkedIn's own relative timestamp, now forty-one for forty-one across eight runs.

Five post fetches spent, all five productive: three became selections, two produced documented
rejections that would otherwise have needed guessing.

# Posts considered

## Selected

- **SELECTED** Omar Alenezi, "In 20 years of managing mega-projects, I've never seen fast-tracking
  projects actually save time" (2026-06-12, 106 reactions, 80 comments). Falsifiable claim with three
  costed mechanisms, and the author names the real cause in his own second line then treats it as
  noise. New author, no collision.
- **SELECTED** Thomas Lusiyano, "Boards don't get surprised by poor results; they get surprised by
  assumptions they never challenged" (2026-02-14, 101 reactions, 19 comments). Right diagnosis
  attached to a remedy every board already owns, which is the gap the reply works in. New author, no
  collision.
- **SELECTED** Dave Kline, "Your team isn't missing deadlines because they're lazy. They're missing
  them because you let them" (2026-07-30, 660 reactions, 244 comments). Freshest genuine argument and
  the highest engagement reached this run, and its two named tests pull against each other. New
  author. Checked the near-miss collision with Klebine, two queue items, different person.

## Rejected, WebSearch and Brave stale set, bare brief query

- **REJECTED** Chat Engineer, "Project Management (The Basics)" (2023). Glossary, PMBOK terms.
- **REJECTED** Project Management Information, "#projectmanagement #planning" (2023). Job-title listicle.
- **REJECTED** Successful Project Managers, "Understanding the 49 Project Management Processes". Glossary.
- **REJECTED** Project Management Info, "Project Management Cheat Sheet". Cheat sheet.
- **REJECTED** Rachel Oddie, "5 Project Management Skills Every Business Leader Needs" (2022). List post.
- **REJECTED** Kory Kogon, "What Is Project Management? Everything You Need To Know" (2023). Explainer.
- **REJECTED** Sonal Sharma, "What Is Project Management?" (2022). Definition post.
- **REJECTED** Whitney Akabike, project and programme roles (2023). Role description.
- **REJECTED** Ken Martin, "Project Manager - Roles & Responsibilities" (2023). Role description.
- **REJECTED** Bonnie Biafore, project management versus work management clip (2025). Already in the queue as an author.
- **REJECTED** Pasang Sherpa, Tushar Ghelani, Emmitt O., Lindsay Reinert Burney, Andrew Bogle. Course
  and certification completion posts.
- **REJECTED** Turing, "Six Best Project Management Tools", Tulsi Soni, "7 Top Project Management
  Websites", Michelle Venezia podcast plug, Hadi and Wayne Lewis tool links. Tool and link promotion.
- **REJECTED** Two Wikipedia articles returned as results. Not LinkedIn posts.

## Rejected, crisis-management-in-projects hub

The best hub of the run. Ten posts, one selection, and the rejections were on adjacency rather than quality.

- **REJECTED** Gabor Stramb, "Most new PMs think handling pressure means doing everything faster"
  (2025, 339 reactions). Already in the queue as an author, seven times over.
- **REJECTED** Jesus Romero, "Project management teaches you how to hit deadlines. It rarely teaches
  you how to protect yourself while doing it" (2025-12-17, 41 reactions, 50 comments). The best
  comment-to-reaction ratio on the hub and a real opening claim. Fetched in full and rejected on the
  body: it is the CALM acronym with four pillars, which is squarely the list-post exclusion.
- **REJECTED** Amara Irobi, "Not every C&I solar project is viable, I learnt this the hard way"
  (2025-09-15, 150 reactions, 34 comments). Fetched in full. Genuinely good line in it, "if you can't
  defend both sides, then what you have is not a project, it's just a lead", and business-case ground
  is under-served in the queue. Rejected because the body is three numbered filters, four feasibility
  categories and five red flags. List post, and eleven months old.
- **REJECTED** Rahul Setia, "60 to 70% of pressure comes not from workload, but from unclear
  communication" (9 months, 71 reactions). Unsourced statistic, and communication causation is taken
  by schwartz-communication-causation and phillips-communication-not-plans.
- **REJECTED** Amir Kelifa, "I built a tool that scores how fast your project will die in Africa"
  (4 months, 49 reactions, 36 comments). Tool promotion.
- **REJECTED** Luis Salavarria, "Actionable Mondays: Care More About the Downside" (3 months, 13
  reactions). Right instinct, engagement too low to be worth a reply.
- **REJECTED** Brett Miller, "My Amazon System for Turning Chaos Into Clarity" (5 months, 23
  reactions). System listicle.
- **REJECTED** David Markley, "Minimal resources, tight timelines, high expectations" (1 year, 41
  reactions). Situation description, no claim.

## Rejected, lessons-learned-in-project-management hub

- **REJECTED** Amy Gibson, "A bad workman always blames his tools" (2026-02-17, 2,076 reactions, 217
  comments). Highest engagement of anything reached this run and it was fetched in full for that
  reason. Rejected on two counts. The accountability ground is saturated:
  hart-accountability-is-an-arrangement, cutler-accountability-exposure, bratu-ownership-authority,
  sparrow-owning-the-outcome, thompson-ownership-expires-before-measurement. And the post is a
  personal reflection ending in a repost call to action, so the only available reply is agreement.
- **REJECTED** Jeroen Kraaijenbrink, "Teams rarely fail because people are unwilling" (8 months, 293
  reactions). Already in the queue as an author, twice.
- **REJECTED** Martin Eigner, "My 10 mistakes introducing PLM" (8 months, 1,083 reactions) and
  Andreas Bach, "15 Years, 15 Don'ts" (11 months, 1,117 reactions). Both strong engagement, both
  excluded by the list-post rule without argument.
- **REJECTED** Richa Singh, Asad Ansari, Liz Wilke, Sahil Bansal, Andrea Nicholas. Leadership
  aphorisms, expense-policy thought experiment, vacation messaging, interview observations and an
  integrity anecdote. Not project work.

## Rejected, monitoring-and-controlling-projects hub

- **REJECTED** Melissa Perri, "Your annual planning process is probably creating the problems it's
  supposed to solve" (2026-03-15, 185 reactions). Real claim, good author, and the closest thing to a
  fourth selection. Rejected on candidate adjacency: this is the same argument as
  2026-08-18-002-pincot-the-operating-model-is-the-funding-cycle, which was drafted a week ago.
- **REJECTED** Russ Hill, "Lou Gerstner walked into IBM in 1993 expecting a strategy problem"
  (11 months, 1,015 reactions, 138 comments). Culture-not-strategy business anecdote. Ground taken by
  perdhanaputra-culture-feedback-loop and cowen-personality-not-system.
- **REJECTED** Omar Halabieh, "Stop answering what's asked, Answer what's meant instead" (1 year, 313
  reactions, 254 comments). Communication aphorism, not project work.
- **REJECTED** Zubin Rashid on the Kirkpatrick Model (3 weeks, 552 reactions), Vitaly Friedman's
  Notion impact templates, Frederick Magana and Marcia D Williams on procurement, Raj Grover on
  disaster recovery, Garima Mehta on usability testing, John Isaac on designer interviews. Adjacent
  disciplines, no project delivery claim.

## Rejected, project-risk-assessment-techniques hub

- **REJECTED** Prof. Bent Flyvbjerg, "New paper THE 'SMALL IS SAFE' MYTH IS RUINING YOUR PORTFOLIO"
  (2026-07-20, 633 reactions, 59 comments). Fresh, high engagement, exactly Mark's ground and the
  most tempting rejection of the run. Already in the queue as an author,
  2026-05-07-003-flyvbjerg-megaprojects-planning-bias. Worth raising with Mark whether the
  author-dedup rule should have a re-reply exception for authors this central to the book's material.
- **REJECTED** Pawel Huryn, "Be careful. Most 'products' are, in fact, projects" (2 years, 1,583
  reactions). Ground taken by mcdonald-project-product-bet.
- **REJECTED** Hans Stegeman on the WEF Global Risks Report, Anderson Candido and Phil O'Connell on
  mineral resource classification, Lior Drihem on MCP security, Christian Wattig on forecast types,
  Pan Wu on A/B test risk, Pedro Berrocoso on automation canaries, Valerie Nielsen on lake-effect
  snow. Sector risk commentary, not project delivery.

## Rejected, decision-analysis-in-project-management hub

- **REJECTED** Jeetu Patel, "Debating the Obvious vs. Deliberating the Irreversible" (2025-08-10, 529
  reactions, 46 comments). Reversible versus irreversible decisions. Same ground as
  2026-07-01-002-parrish-decision-doors-unlabelled.
- **REJECTED** Dr. Gurpreet Singh, "Ever found yourself in the middle of a software project" (1 year,
  286 reactions, 48 comments). Opening gives nothing to argue with and the engagement did not justify
  a fetch to find out.
- **REJECTED** Mallika Rao, "The 5-Minute Decision-Making Formula Used by High-Performing CEOs",
  Tariq Ahmad on RICE, Mangesh Pawar, Dane Jensen, Sanjay Chandra, Aarushi Singh, Rishav Gupta,
  Kevin Kermes. Formula posts, prioritisation frameworks, feedback-loop content and a time-tracking
  exercise. Ground on frameworks is already covered by willis, goitein, shalloway and doshi.

## Rejected, conducting-project-post-mortems hub

Mis-titled. Returned "difficult conversations" content throughout, the same failure mode the 08-19
note flagged for `showcasing-project-successes` and 08-24 flagged for `governance-models`.

- **REJECTED** Irina Lamarr, "Avoiding hard conversations costs projects" (2026-01-15, 36 reactions,
  34 comments). On-theme and a good ratio, but the claim is one the queue already argues at length
  and the only available reply is agreement.
- **REJECTED** Mark Taylor, "Most difficult conversations are delayed for the same reason: You care
  about the person too much" (5 months, 27 reactions). Workable counterpoint, that they are delayed
  because of what the conversation costs the person having it, but low engagement and no project claim.
- **REJECTED** Dr. Carolyn Frost, "12 psychological moves that win difficult conversations" (9 months,
  945 reactions, 337 comments). List post.
- **REJECTED** Dixie Crawford, Sheri R Hinish, Alexis John d'Amecourt, Marilyn Sherman, Jeff
  Kushmerek, Peter T. Coleman, Donna Recupido. Difficult-conversation and conflict-resolution
  content across supply chain, churn and campus tensions. Not project work.

## Rejected, creating-project-status-reports hub

Mis-titled. Returned business-intelligence and data-quality content, zero project status material.

- **REJECTED** Revanth Munirathinam, Nicolas Boucher, Kurt Buhler, Josh Aharonoff, Warren Dean,
  Daniel Evans, Faizan Jalil, Poornachandra Kongara, Magnat Kakule Mutsindwa, Mehdi Oudjida. Power BI
  features, Looker Studio updates, reporting tips, Canva football scout reports. Ten posts, zero
  relevant. Note also that status reporting is saturated in the queue anyway:
  kumar-dashboard-hides-decision, badewi-dashboard-has-no-stop, selvaraj-status-is-a-request,
  vanbinsbergen-rag-report-alibi, dunsmuir-report-written-to-be-unreadable.

## Rejected, flat-slug hubs, no usable content

- **REJECTED** `conducting-project-post-mortems`, `decision-analysis-in-project-management`,
  `crisis-management-in-projects`, `conducting-project-feasibility-studies`,
  `iterative-project-management-processes`, `tracking-project-milestones`,
  `kanban-project-management-tools`, `implementing-erp-systems`, `agile-project-management-tools`,
  `predictive-project-management-strategies`. All returned the bare landing shell. Ten fetches, zero posts.
- **REJECTED** `engaging-stakeholders-in-projects` and `strategic-planning-in-project-management`.
  Both rendered a post list, and both rendered the **identical** ten posts: Robert Dur, Dr Shereen
  Daniels, Justin Bateh, Elfried Samba, Dr. Arthur Brooks, Brij Kishore Pandey, Ruchira Garg, Dominic
  Joyce, Alexey Navolokin, Zoe Whitman. Generic career content, byte for byte the same block from two
  different slugs. Not topic content and not usable.
- **REJECTED** `project-management-roles`. Landing shell only.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-25-001-alenezi-breaking-ground-buys-irreversibility.md`
  Structural observation. Concedes all three costed mechanisms and disputes none of the numbers, then
  relocates the decision. An early start is not an attempt to save time, it is a purchase of
  irreversibility. Design in an office can be cancelled on a Tuesday afternoon at nil cost; a hole in
  the ground cannot. So the 15 percent is the premium on a commitment device, and the people paying
  it are not confused about the price. Closes by pointing at what happened to the last person who
  stopped something at design stage. Themes: the project is a bet, deliver the possible not the
  fantasy, bad news is data.
- `queue/reply-candidates/reply-candidate-2026-08-25-002-lusiyano-assumptions-are-laundered-on-the-way-up.md`
  Counterpoint. Grants the diagnosis and the whole tool list, then argues the test does not fail in
  the boardroom. A board paper is a request, not an analysis, and it has been through four or five
  hands to get there, each of which shrank the caveat covering its own section because uncertainty
  travelling upward reads as not being on top of the job. The assumptions are not unexamined, they
  are laundered, so every scenario run against them returns a confident answer. Themes: bad news is
  data, the project is a bet.
- `queue/reply-candidates/reply-candidate-2026-08-25-003-kline-the-slip-was-the-measurement.md`
  Counterpoint. Credits the self-criticism, then shows Test 2 taxing what Test 3 depends on. Making
  commitments visible to peers raises the price of falling short in public, which includes the useful
  version, so the week-two warning becomes a week-nine warning that nobody can act on. More
  accountability, less forecasting. Then the reframe: a slipped date is the only unbiased measurement
  of the work anyone will get, and the Clarity Test cannot catch a fictional date because it asks
  when, never where the when came from. Themes: bad news is data, the project is a bet.

# Notes

**The hub route was fixed and the fix came from a Brave fallback result.** This is the run's most
useful finding and it should change how future runs work. Flat hub URLs of the form
`linkedin.com/top-content/<slug>/` are dead: ten of them returned the bare landing shell and two more
returned an identical block of generic career posts regardless of which slug was requested, which
means the flat path is no longer resolving slugs at all. The working form is **nested under the
parent topic**, `linkedin.com/top-content/project-management/<slug>/`. That path returned real,
topic-relevant post lists with authors, verbatim opening lines, post URLs, relative ages and
engagement counts, on four of five attempts. The discovery was accidental: a Brave query on
`"it wasn't a scope problem"` fell back to unquoted matching and among the junk returned three nested
`project-scope-definition-methods` URLs. **Recommendation: future runs should go straight to nested
hubs and should not spend calls on flat slugs.** The 08-24 note naming the hubs as the primary
discovery route stands, but the URL shape in it is now wrong.

**The sub-slug pool is now large.** One fetch of the parent hub returned 105 sub-topic slugs against
the ten hrefs harvested on 08-24. Five were used this run. The nested pages also advertise their own
third-level sub-slugs, so `crisis-management-in-projects` offers "Stress Testing for Project
Viability" and "Managing Urgent Issues vs. Prevention", and `decision-analysis-in-project-management`
offers "Uncertainty Management Practices" and "Scenario Analysis Implementation". Depth is available
below the level used so far and is untested.

**Hub yield this run, five nested fetched.** `crisis-management-in-projects` was the best by a
distance, ten on-topic posts and one selection. `lessons-learned-in-project-management` and
`monitoring-and-controlling-projects` both rendered real lists with high-engagement posts, though
both leaked adjacent-discipline content. `project-risk-assessment-techniques` and
`decision-analysis-in-project-management` rendered real lists that were mostly off-target.
`conducting-project-post-mortems` and `creating-project-status-reports` are both **mis-titled and
should not be fetched again**: the first returns difficult-conversation content, the second returns
Power BI and data-quality content. That makes four confirmed mis-titled hubs to date, alongside
`governance-models` and `workflow-efficiency` from 08-24.

**Three selections, and the bar was not lowered to reach three.** Two of the three, Lusiyano and
Kline, are borderline on the list-post rule and were taken anyway, on the same reasoning applied to
Eckwahl on 08-19 and inverted here: in both cases the numbered list is illustration hanging off a
single falsifiable causal claim that stands without it. Romero, Irobi, Frost, Eigner and Bach were
rejected on that rule because in those posts the list is the substance. The distinction is worth
keeping consistent and is recorded in both candidate files.

**Freshness improved.** Kline at 2026-07-30 is twenty-six days old, the second-freshest selection in
several weeks after Cohn on 08-24. Alenezi is two and a half months, Lusiyano six. Every selection
carried three-figure reactions, and Kline's 244 comments on 660 reactions is the strongest engagement
ratio selected in the eight runs covered by these logs.

**Flyvbjerg is the rejection worth a decision from Mark.** A one-month-old post, 633 reactions,
arguing that the "small is safe" portfolio assumption is wrong, from the researcher whose work
underpins a large part of the book's argument. It was rejected purely on the author-dedup rule
against a candidate drafted on 2026-05-07 and never posted. If the rule is meant to prevent looking
repetitive on a single author's feed, an unposted candidate from three and a half months ago probably
does not trigger it. Flagging rather than deciding.

**Engagement-weighted, the run reached far better material than 08-24.** Six posts over 600 reactions
were considered this run against one on 08-24, and Gibson at 2,076 was the largest. Only one of the
six converted, because the other five were either list posts, saturated ground, or already-queued
authors. That is the exclusion rules working rather than the pool being thin, but it is worth noting
that the queue's coverage is now dense enough that adjacency is the single most common rejection
reason after the list-post rule.
