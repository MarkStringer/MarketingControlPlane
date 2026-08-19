---
id: reply-scout-log-2026-08-19
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Status of that URL this run: still dead, twenty-sixth consecutive run. It returned a 302 to
`consent.google.com` rather than yesterday's 429. Unusable either way. Treat as permanently gone
and stop spending a call on it.

Engines used, and what each was worth:

1. **WebSearch, bare brief query.** Returned the same stale 2022 to 2023 glossary set as every
   previous run, plus three Wikipedia articles. Zero selectable results, logged as rejections below.
2. **WebSearch, targeted phrasing.** Materially better than the bare query and not rate limited at
   all. It surfaced real 2026 content and, more usefully, two working `top-content` hub slugs that
   could not have been guessed. It rarely returns a usable `/posts/` URL, so treat it as a lead
   generator rather than a source of citable links.
3. **Brave via WebFetch.** Worked, rate limited on roughly one call in four, which is better than
   yesterday. Nine queries attempted, seven returned results, one was productive. Confirmed again
   that recency filters (`tf=pw`, `tf=pm`) collapse the result set to institutional PMI content or
   nothing.
4. **LinkedIn public top-content hubs.** Mixed. The root hub and one sub-hub rendered real posts.
   Three other sub-hubs rendered only the navigation shell. Detail under Notes.
5. **Public recent-activity pages.** New route found this run, and the thing that unblocked the
   first selection. Detail under Notes. This is the answer to the "good lead, no URL" failure that
   killed three candidates yesterday.
6. **Activity ID date decoding** run on every shortlisted result before spending a fetch. Fourteen
   dates decoded for free. All four subsequently fetched posts matched their decoded date, now
   twenty-four for twenty-four across five runs.

Four post fetches spent, three of them productive.

# Posts considered

## Selected

- **SELECTED** Yuri Nedre, "Project Managers are not reminder machines" (2026-06-16, 1,027
  reactions, 62 comments). Falsifiable causal claim about why PMs chase people, wrong in a way that
  has consequences, and by far the highest engagement of any real argument reached this run. New
  author.
- **SELECTED** Stephen Brown, "Is PMO a bad word?" (2025-07-09, 40 reactions, 14 comments).
  Specific claim that renaming the function changes its standing, with the causation running
  backwards. New author, and PMO was flagged as under-served in yesterday's log.

## Rejected, WebSearch stale set, bare brief query

- **REJECTED** Sonal Sharma, "What Is Project Management?" (2022). Definition post, link bait.
- **REJECTED** Chat Engineer, "Project Management (The Basics)" (2023). Glossary content.
- **REJECTED** Project Management Information, "#projectmanagement #planning" (2023). Job titles listicle.
- **REJECTED** Kory Kogon, "What Is Project Management? Everything You Need To Know" (2023). Explainer.
- **REJECTED** Three Wikipedia articles returned as results. Not LinkedIn posts.

## Rejected, Brave, bare brief query and past-week variant

- **REJECTED** Bonnie Biafore, project management versus work management clip (2025-01-23). Already in the queue as an author.
- **REJECTED** Pasang Sherpa, Harvard ManageMentor completion (2023). Course completion post.
- **REJECTED** Rachel Oddie, "5 project management skills every business..." (2022). List post.
- **REJECTED** Lindsay Reinert Burney, PMP application submitted (2022). Certification post.
- **REJECTED** Project Management Info, "Project Management Cheat Sheet" (2026). Cheat sheet.
- **REJECTED** Whitney Akabike, "I transform strategies into realities" (2023). Personal positioning.
- **REJECTED** Wayne Lewis, Excel and MPP plans (2020). Tooling preference.
- **REJECTED** Matt Quick, "5 free Project Management Institute courses" (2025). Course promotion.
- **REJECTED** Successful Project Managers, "Understanding the 49 Project Management Processes" (2025). List post.
- **REJECTED** Tulsi Soni, "7 top project management websites of 2023". Link list.
- **REJECTED** Mahesh EV, KPIs as a compass (2024-02-10). Metaphor plus a KPI list, no claim to contest.
- **REJECTED** Emmitt O., PMP credential issued (2022). Certification post.
- **REJECTED** Ken Martin, project manager roles and responsibilities (2023). Role explainer.
- **REJECTED** Andrew Bogle, LinkedIn Learning course milestone (2021). Course promotion.
- **REJECTED** Ishan Jagdipbhai Jadav, "Project Management is Changing Faster Than Ever, AI is No Longer Optional" (2026-08). The AI-will-not-replace-PMs genre is now pure agreement content and the counterpoint is already in the queue.
- **REJECTED** IPMA, untitled chapter post (2026-08). Institutional announcement.
- **REJECTED** PMI Uganda Chapter, annual national conference recap (2026-08-12). Event report.
- **REJECTED** PMI UK, "Can You Deliver and Can People Believe in the Delivery" (2026-08-12). Same post rejected on 2026-08-18. There is a real counterpoint in it, that belief in delivery is close to the opposite of what you want, but it remains institutional promotion for coaching services.

## Rejected, Brave, "RAG status"

- **REJECTED** Shawn Wallack, "Can you use RAG status in Agile?" (2025-07-11). Already in the queue as an author.
- **REJECTED** Intelogy, RAG status for SharePoint review dates (2023). Product tutorial.
- **REJECTED** Ahmad Alkhateeb, "RAG status means Red Amber Green status" (2025-08-04). Definition post.
- **REJECTED** Merve Öztekin, team swapping statuses (2025-08-28). No snippet obtainable from any engine and the fragment gives nothing to argue with. Not worth a fetch.

## Rejected, Brave, "the project was green" and red/amber/green status queries

Brave ignored the quoted phrase both times and fell back to unquoted term matching. The second
query returned thirteen results about a company called Amber and one about complementary colours.

- **REJECTED** 6Green Project, two EU research consortium posts (2023). Not project management.
- **REJECTED** Joelma Almeida, green investment investigation (2022). Sector commentary.
- **REJECTED** Steve Icke, "What is a green belt project?" (2022). Certification explainer.
- **REJECTED** Amber Infrastructure Limited, three infrastructure financing posts (2022 to 2023). Corporate announcements.
- **REJECTED** Amber Marie Green, Amber Electric (twice), Amber Horton, Amber Ritschel, Amber-Louise Pocklington, Amber Mac, Emily Rubin, Premium Pack, Shaun Hughes. Ten further results matched on the word Amber alone. None about projects.

## Rejected, Brave, "delivery problem" and "prioritisation problem"

The theme is good and under-served, but every result is at least two years old and the two authors
worth replying to are already in the queue.

- **REJECTED** Michael Goitein, "The One Reason Why Prioritization Frameworks Will Never Work" (2024-02-02). Already in the queue as an author.
- **REJECTED** John Cutler, "why do most lists of top-level priorities..." (2023-09-18) and "You can't prioritize something unless you deprioritize something else" (2023-08-18). Already in the queue as an author, and the second is an aphorism.
- **REJECTED** Itamar Gilad, "Why prioritization is so damn hard" (2023-10-09) and the impact-effort matrix post (2022). Method advice.
- **REJECTED** Kenny Alami, "What's harder than prioritizing? Deprioritizing" (2021). Aphorism.
- **REJECTED** Saeed K., "Why you should avoid prioritization frameworks" (2023-01-15). Framework critique, three years old and the ground is covered.
- **REJECTED** Nicole Tietz-Sokolskaya, "I see a problem and no one is prioritizing it" (2024-02-26). Individual frustration, no structural claim.
- **REJECTED** Mind the Product, Jared Owen, Buddhika W., Kieran Shelley, Siva Balu, Yiwen Rong, Anna Strinadko, Prasad Rao, Queen Adebiyi, Jeff Schneider, Zepto case study, Windward. Twelve results, all either product backlog advice, sales time management, or literal parcel delivery.
- **REJECTED** Stuart Easton, project prioritisation posts. Real theme and a new author, but every post an engine would surface is TransparentChoice webinar or software promotion, which is the corporate promotional exclusion.
- **REJECTED** Guy Thorpe, prioritisation content surfaced via profile. Already in the queue as an author.

## Rejected, Brave, PMO queries

- **REJECTED** Hussain Bandukwala, "Running a PMO is the loneliest job in the..." (2026-02-11). The freshest PMO post reached this run, but it is a peer support post about isolation rather than an argument about what a PMO is for.
- **REJECTED** Ben Eckwahl, "The one-person PMO is a reality for more..." (2026-01-15, 69 reactions, 10 comments). Fetched in full. Genuinely useful post, and there is a reply in it, that a one-person PMO is a decision the organisation has already made about how much it wants to know. Rejected because the body is four numbered recommendations, intake form, status report, RAID log, weekly meeting, which is squarely the list post exclusion.
- **REJECTED** Fatima Habbouchi, "the harsh reality of being a PMO manager" (2025). Same person as Fatimah Abbouchi, already in the queue as an author.
- **REJECTED** Andrew L., "The PMO is often overlooked but is critical" (2023-08-26). Agreement content.
- **REJECTED** Md. Houmaun Kabir, PMO meaning explainer (2024-02-27). Definition post.
- **REJECTED** Ali Ormerod, last week as Head of PMO (2023-09-29). Career announcement.
- **REJECTED** Christie Struckman, "Dear presidents of projects and outcomes" (2024-02-05). Real structural proposal, but two and a half years old and Gartner-institutional in framing.
- **REJECTED** Step5 Group, "How to define your PMO and drive value" (2022). Consultancy promotion.
- **REJECTED** The PMO Guy, strategy execution and business alignment (2025-10-15). Hashtag-led positioning post with no argument in the snippet.

## Rejected, Brave, "benefits realisation"

- **REJECTED** Amgad Badewi, benefits realisation post (2026-01). Already in the queue as an author.
- **REJECTED** IIBA Australia, FOBA 2026 conference post (2026). Event promotion.

## Rejected, Brave, "not a communication problem"

- **REJECTED** Paolo Belcastro, "you don't have a communication problem, you have a delegation and knowledge-sharing problem" (2025-10-13). The closest near miss in this set. Real claim and a real reply available, but it is about team inefficiency in a marketing organisation rather than project structure, and the post is a lead-in to a productivity product.
- **REJECTED** Simon Jude Nwachukwu, "the world doesn't have a communication problem, it has a dialogue problem" (2026-04-29). Aphorism, not about projects.
- **REJECTED** Natalia Volotskaia, "10 communication tips for project managers" (2023). List post.
- **REJECTED** Curt Gratz, listening as the gateway to stakeholder needs (2023-11-06). Agreement content.
- **REJECTED** Alvin Foo, "90% of all management problems are caused by miscommunication" (2023). Statistic card.
- **REJECTED** Rohan Parmar, "we listen to respond" (2022), Kurtay Toros, Andreas Knopf, Tim Arnold, Ms. Neela Cezair, Scott Frazier, Philip Baum, Ashley Jones, Lois Lim, Uttam Pai Umesh, Kay Nadel, Madison Crane, Donald Showens, Jeremy Brooks, Shefali Kunwar. Fifteen results, all general communication or coaching content.

## Rejected, Brave, "delivered on time" and "nobody used it"

Brave matched on "delivery" in the logistics sense and on LinkedIn growth content. Nothing in the
set was a project post.

- **REJECTED** Cano Steel, "Delivered on time. Every time." (2026-07). Company advertising.
- **REJECTED** Dave Farley, continuous delivery fundamentals (2025-06). No snippet, and the post is a course link.
- **REJECTED** Casper Rouchmann, Ryan Kelly, Jason S. Baker, Hemanth Reddy, Commit Consulting, Martin Peterson, James Smith, Scott Smith. Eight results about parcel delivery, SAP tolerances, DNS and a horse racing festival.
- **REJECTED** Maryam Asim, Sam G. Winsbury, Jamie Brindle, Eduardo Middleton, Aastha K., Kadria Kutlukaeva, Lucy Fisher, Matt Barker, Zayd Syed Ali, Dina Mainville. Ten LinkedIn growth and personal branding posts. Not project management. Several of these recur run to run on any query containing a common verb.

## Rejected, Brave, "the technology was the easy part"

- **REJECTED** Rana Rauf, Satya Nadella digital transformation quote (2023). Quote reshare.
- **REJECTED** Hassan Rezk Habib, technology and elitism (2021). Aphorism.
- **REJECTED** Changyuan Technology Group, "Exporting Technology Is Easy. Delivering Infrastructure Is Hard" (2026-07-16). Good title, but it is a corporate capability post.

## Rejected, Brave, "business case" and "benefits", past month

- **REJECTED** Canon Business Services, "The first mistake that causes AI projects to fail? Choosing the wrong use case" (2026-07). Corporate promotional content for an AI advisory service.

## Rejected, LinkedIn top-content hub, project management root

Same cached set as 2026-08-18, unchanged. Re-listed for completeness rather than dropped.

- **REJECTED** Daniel Pink, Chris Do, Jingjin Liu. All already in the queue as authors.
- **REJECTED** Andrew Ng, AI agentic workflows (2 years). Not project management.
- **REJECTED** Gaurav Sharma, zero-based budgeting explainer (3 months). Finance explainer.
- **REJECTED** Pierre Le Manh, PMI Project Success study (1 year). Institutional research announcement.
- **REJECTED** Hans Stegeman, WEF Global Risks Report 2026 (7 months). Macro commentary.
- **REJECTED** Severin Hacker, Google 20% time (2 years). Innovation practice.
- **REJECTED** Vitaly Friedman, "60 UX Strategy Methods" (1 year). Methods list.
- **REJECTED** Brij Kishore Pandey, pandas cheatsheet (1 year). Not project management.

## Rejected, LinkedIn top-content hub, project management roles

This sub-hub rendered properly and was the most productive single page of the run.

- **SELECTED** Yuri Nedre, "Project Managers are not reminder machines" (2 months). First selection above.
- **REJECTED** Daniel Hemhauser, "Project management isn't a supporting role" (1 year, 4,630 reactions). Highest engagement on the page. Already in the queue as an author.
- **REJECTED** Gabor Stramb, "9 myths about PMs that need to stay in 2026" (7 months). Already in the queue as an author, and a list post.
- **REJECTED** Manish Kumar Sharma, "When a Project Manager Becomes Just a Meeting Scheduler" (1 year). New author and a real claim, but it is the same argument as the Nedre selection from a weaker angle. Taking both would be one theme twice.
- **REJECTED** Mohamed R., "79% of tech projects that crashed had one thing in common. Their PM never left the spreadsheet." (1 year, 71 reactions). Strongest rejected lead of the run. The 79 percent is a zombie statistic and there is a good structural reply about the spreadsheet being the artefact the organisation rewards rather than the cause of anything. Rejected because the display name gives no vanity URL, so the post could not be located, verified or cited. Carry forward if a URL ever surfaces.
- **REJECTED** Yogesh Negi, "Behind the scenes with project managers" (1 year). Role explainer.
- **REJECTED** Dave Kline, Peter Sorgenfrei, Cory Blumenfeld. Three delegation and trust posts. Management coaching rather than project structure.

## Rejected, LinkedIn top-content hub, showcasing project successes

Hub slug renders, but returns CV and personal branding content rather than project content.

- **REJECTED** Daniel Pink (again), Joshua Miller, Katie Bashant Day, Joanne Lee, Adrienne Tom, Margaret Buj, Margherita Sgorbissa, Andy G. Schmidt, Abby Hopper, Rony Rozen. Ten results, all career, CV or performance review advice.

## Rejected, LinkedIn top-content hub, setting up project management workflows

- **REJECTED** Anna Anderson, "Most project managers think AI adoption starts with buying new tools" (1 month, 13 reactions). New author and a genuine claim, but 13 reactions and 14 comments is below the reach bar and the AI adoption angle is already answered in the queue.
- **REJECTED** Barry Overeem, "Map Dependencies to Find Bottlenecks" (1 year, 284 reactions). New author, but the post is a facilitation technique rather than an argument.
- **REJECTED** Srikrishnan Ganesan, onboarding lessons (1 year). Rocketlane product marketing.
- **REJECTED** Janky Patel, Marvin Sanginés, Wajiha Haider. Three growth marketing posts.
- **REJECTED** Jatinder Verma, Jira Align interview (1 year). Tooling content.
- **REJECTED** Karandeep Singh Badwal, Biju Nair, Jonathon Hensley. Three breaking-down-silos posts, all sector-specific advice.

## Rejected, LinkedIn top-content hub, four slugs that did not render

- **REJECTED** `role-of-trust-in-managing-project-claims-and-delays`, `how-to-balance-stakeholder-priorities-in-project-management`, `how-project-managers-influence-business-outcomes`, `the-importance-of-project-managers-today`. All four are real hrefs harvested from the hub page itself, and all four returned only the navigation shell with no posts. Not an invented-slug problem, a rendering problem. See Notes.

## Rejected, WebSearch targeted follow-ups

- **REJECTED** Hariprasad P S, steering committee governance post (2026-06-25). Genuinely good argument, that a program manager sitting as a voting member "blurs the line between doing and governing" and the committee loses objectivity. Two engines returned the post's content but only ever linked the author's profile, and the profile activity page returned HTTP 999 on three attempts. Could not be verified or cited. Carry forward.
- **REJECTED** Andrew Reise, executive steering committee post (2025-10-23, 1 reaction). Fetched in full. Consultancy promotion with a link out, and no reach.
- **REJECTED** Ameer Ali and PMP Online Training, two near-identical "What is a Program Steering Committee?" posts (2025-08-04). Explainer videos.
- **REJECTED** Jordan Cutler, "Estimates are not deadlines. They get treated like them though." (2024-01). Already in the queue as an author.
- **REJECTED** Chris Mielke, "Don't know what to post about as a project manager?" (2025-09). Already in the queue as an author, and it is content advice.
- **REJECTED** Richard D., "most AI projects don't fail at launch, they fail in week 3" (2026). Real claim about post-launch decay, but the post is an AI engineering pitch and no `/posts/` URL was returned.
- **REJECTED** Martin McCullough, de-escalation script (2026-06-05). Coaching script.
- **REJECTED** B. Phil McHugh, Ronald Magcale, Paige English, and an unattributed "Escalating isn't failure. Escalating late is." Four escalation posts, all surfaced only as profile URLs. Escalation is also saturated in the queue by reply-candidate-2026-08-13-001-graham-the-escalations-that-do-not-qualify.
- **REJECTED** Carl Reader, "Unpopular opinion: discipline is boring" (2026-07-06). Not about projects.
- **REJECTED** Eleven LinkedIn Pulse articles across the RAG status, red project, sunk cost and project cancellation queries, including Vivek Ganesan, Eoin Redmond, Matt Chalmers, Bob McGannon, Brad Kerwin and Ricky Woodman-Povey. All rejected as Pulse articles rather than posts. Worth repeating yesterday's observation: red status and project cancellation are clearly live topics that people write well about, and the queue has nothing on either, but the good material is all in long-form Pulse rather than in posts.
- **REJECTED** Various LinkedIn Help, Jobs, Learning and news-story pages returned across six queries. Not posts.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-19-001-nedre-the-reminder-is-a-bid.md`
  Counterpoint. Concedes "babysitting with a dashboard" and the point about decisions living in one
  person's memory, then reverses the diagnosis. People do not forget, they rank, and the ranking is
  set by whoever writes their appraisal, which is not the project manager. So a follow-up is not an
  information transfer, it is a bid for priority, and better tooling makes the debt easier to point
  at without changing who wins when two claims land on the same person on the same day. Closes on
  the part that is actually not obvious: the reminder count is the only instrument that measures
  real priority rather than declared priority, so chasing that suddenly stops is not evidence of
  health. Lands on bad news is data from an unexpected direction.

- `queue/reply-candidates/reply-candidate-2026-08-19-002-brown-the-name-is-the-readout.md`
  Reframe. Accepts that PMOs slide down the value scale and that the acronym is now a coin flip,
  then reverses the causation. The name is not doing the damage, it is reporting it. A PMO becomes
  overhead when it is handed the duty to collect status and no power to act on it, at which point
  everything it produces is a report, and a report that cannot change a decision is overhead by
  definition. Rather than rejecting the rename, the reply takes the author's own favourite,
  Investment Delivery Office, and turns it into a test with a pass condition: the word investment
  implies the right not to invest, so the function's first act has to be folding a hand where
  everyone can see it. Ends on what happens to bad news on its way to the sponsor.

Two drafted rather than three. The brief allows two to four. The three near misses that would have
made a third are all named above with the reason: Mohamed R. and Hariprasad P S both had a real
argument and no obtainable URL, and Ben Eckwahl had an obtainable URL and a list post. None of the
three failed on substance.

# Notes

**New route found, and it is the fix for yesterday's biggest failure mode.** Public recent-activity
pages render without login at `https://www.linkedin.com/in/<vanity>/recent-activity/all/` and list
roughly nine recent posts with their opening line, relative age, and crucially the raw activity ID.
An activity ID is enough to build a canonical post URL as
`https://www.linkedin.com/feed/update/urn:li:activity:<id>/`, which fetches correctly and returns
the full post text, headline, timestamp and engagement counts. That is exactly what killed three
good leads on 2026-08-18 and it recovered the Nedre selection today.

Two caveats. It needs the vanity slug, so it does not help when a hub shows a display name only,
which is why Mohamed R. still could not be reached. And it is heavily rate limited: it worked on
the first call, then returned HTTP 999 on five of the next six attempts across four different
profiles, including after a `www` to country-subdomain redirect. Treat it as one or two calls per
run, spent on the single lead most worth recovering, not as a route to browse.

**The right search order for the next run**, based on what actually produced results today:

1. One `top-content` hub fetch to harvest sibling slugs and candidate authors.
2. WebSearch with targeted phrasing to find leads and further working slugs. It is not rate limited
   and it surfaced two hub slugs that could not have been guessed.
3. Brave for `site:linkedin.com/posts` with one or two short quoted phrases, to convert leads into
   real URLs.
4. One recent-activity call, saved for the best lead that still has no URL.
5. Decode every shortlisted activity ID before spending a fetch.

**Hub sub-slugs are inconsistent, and it is not the invented-slug problem from yesterday.** Four
slugs harvested directly from the hub page's own hrefs returned only the navigation shell. Two
others, `project-management-roles` and `setting-up-project-management-workflows`, rendered full
post lists. There is no obvious pattern. Fetch the slug and see; do not assume a harvested slug
will work, and do not conclude the hub is dead when one fails.

**`showcasing-project-successes` is mis-titled.** It returns CV writing and performance review
advice. Skip it.

**Brave is better today than yesterday but the quoted-phrase problem is worse.** Four of the nine
queries fell back to unquoted term matching and returned pure noise, including one that matched
thirteen results on the word "Amber". Two-word quoted phrases work. Anything longer or more
distinctive gets silently discarded, and the results look plausible enough that they waste a read.

**Engines confirmed dead, do not retry.** Google direct, Bing, Brave through curl, DuckDuckGo,
Startpage, Mojeek, Ecosia, Yandex, Stract, public SearXNG instances. No change from 2026-08-18.

**Activity ID decoding remains the best filter available.** Fourteen IDs decoded for free this run,
now twenty-four for twenty-four across five runs. Decode before spending a fetch, always.

**Queue state.** 257 candidate files before this run, 259 after. Author deduplication was run
against the combined set of `queue/reply-candidates/` and `observed/replies/`, which currently
covers roughly 177 unique authors. Both selections are new authors. PMO was flagged as under-served
yesterday and now has its first candidate. Red or amber status reporting and project cancellation
are both still at zero, and both look reachable if a post rather than a Pulse article can be found.
