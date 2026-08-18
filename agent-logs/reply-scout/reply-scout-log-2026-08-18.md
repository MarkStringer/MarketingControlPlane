---
id: reply-scout-log-2026-08-18
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Status of that URL this run: still dead, twenty-fifth consecutive run. It now returns HTTP 429
rather than the consent redirect seen previously. Either way it is unusable and should be treated
as permanently gone.

Engines used, and what each was worth:

1. **WebSearch, bare brief query.** Returned the same stale 2022 to 2023 glossary set it has
   returned for weeks, plus three Wikipedia articles. Zero selectable results. Logged as rejections
   below rather than silently dropped.
2. **Brave via WebFetch.** Worked, but rate limited far harder than on 2026-08-17. Roughly one
   query in three succeeded, and the successful ones returned thin LinkedIn indexes. Eight queries
   attempted, four returned results, two of those were productive. Full list below.
3. **Bing, Startpage, Mojeek, DuckDuckGo, Ecosia, Yandex, Stract, two SearXNG instances.** All
   tried, all dead ends. Detail under Notes. None of these should be retried next run.
4. **LinkedIn public top-content hubs.** New route found this run and the source of one selection
   lead. Detail under Notes.
5. **Activity ID date decoding** run on every shortlisted result before spending a fetch, using
   `datetime.fromtimestamp((activity_id >> 22) / 1000)`. Twenty-four dates decoded for free. All
   four subsequently fetched posts matched their decoded date, which is now twenty for twenty
   across four runs. Still the highest value filter available and still the correct first step.

Five post fetches spent, two of them productive.

# Posts considered

## Selected

- **SELECTED** Kanyinsola Saheed, "Project Management doesn't replace Business Analysis" (2026-07-31,
  36 reactions, 4 comments). Makes one falsifiable causal claim about why projects solve the wrong
  problem, and the claim is half right in a way that has consequences. New author, and business
  analysis is a theme with no coverage at all in the 255 file queue.
- **SELECTED** Lenka Pincot, "Agile transformed teams. But it didn't transform how organizations
  run." (2026-03-20, 86 reactions, 5 comments). Correct observation with an explanation that does
  not follow from it, which leaves room for a mechanism. New author. Ends on an open question the
  reply can answer directly.

## Rejected, WebSearch stale set

- **REJECTED** Sonal Sharma, "What Is Project Management?" (2022). Definition post, link bait, no claim.
- **REJECTED** Chat Engineer, "Project Management (The Basics)" (2023). Glossary content.
- **REJECTED** Project Management Information, "#projectmanagement #planning" (2023). Job titles and a salary figure. Listicle.
- **REJECTED** Kory Kogon, "What Is Project Management? Everything You Need To Know" (2023). Explainer, nothing to counter.
- **REJECTED** Three Wikipedia articles returned as results. Not LinkedIn posts.

## Rejected, Brave query 1, bare brief query with past week filter

- **REJECTED** PMI Sydney, PMI Australia Project Management Awards nominations (2026-08-11). Awards promotion.
- **REJECTED** My Project School, "AI Fluency is becoming a core Project Management skill" (2026-08-12). Course provider promotion.
- **REJECTED** Hanny Alshazly, PMI and Sobha Group partnership (2026-08-12). Corporate announcement.
- **REJECTED** PMI Uganda Chapter, national conference report (2026-08-12). Event report.
- **REJECTED** PMI Uganda Chapter, Global Summit Series Africa countdown (2026-08-11). Event promotion.
- **REJECTED** Leah Umeokeke, PMI certification for students (2026-08-11). Certification promotion.
- **REJECTED** PMI UK, "Project Management asks: Can we deliver? Social Leadership ensures: People believe in the delivery" (2026-08-12). The cleanest claim in this set and there is a real counterpoint in it, that belief in delivery is the opposite of what you want, but it is institutional promotion for coaching skills and falls under the corporate promotional exclusion.
- **REJECTED** Samarth Jobs, senior manager façade projects (2026-08-12). Job advert.
- **REJECTED** Faisal Aldajani, quarterly performance recognition (2026-08-11). Personal recognition post.
- **REJECTED** Bincy Baby, ESG for Project Managers event (2026-08-10). Event thanks post.

## Rejected, Brave query 2, "nobody wants to say" fragment

- **REJECTED** Andrew Ramdayal, "Project managers need to stop being afraid of conflict" (2026-08-06). Genuinely arguable and the freshest real argument reached this run, but Andrew Ramdayal is already in the queue as an author.
- **REJECTED** Ouitis Imed, "The biggest challenge isn't scope, budgets or schedules. It's managing change." (2026-07-28, 1 reaction). Fetched in full. There is a reply here, that adaptability is not a personal capability but a permission granted by the funding structure, and a PM who adapts without authority is just absorbing variance personally. Rejected on reach rather than substance: one reaction, and the post itself is the generic adaptive-leader genre. Worth revisiting only if the same argument turns up on a post people are actually reading.
- **REJECTED** Kayinsola Saheed's post appears in this set too and is the first selection above.
- **REJECTED** James Katumba, "the biggest shifts have happened in conversations" (2026-07-31). Reflection with no mechanism to engage.
- **REJECTED** PMI UK, "Lead with Influence, Not Volume" (2026-07-28). Coaching skills promotion.
- **REJECTED** Successful Project Managers, "Types of Project Management" (2026-07-22). List post.
- **REJECTED** Successful Project Managers, "Core Elements of Successful Planning" (2026). List post.
- **REJECTED** Successful Project Managers, "A Complete Plan in Layered Structure" (2026). List post.
- **REJECTED** Successful Project Managers, "The Future of Project Management" (2026). Trend listicle.
- **REJECTED** Successful Project Managers, "Top 10 Tips for Project Managers" (2026). List post.
- **REJECTED** Successful Project Managers, communication plan, stakeholder register, risk dashboard, closure report and timesheet Excel templates (2026). Five template download posts.
- **REJECTED** Sania Butt, two reshares of Successful Project Managers content (2026-07-25 and earlier). Reshares of list posts.
- **REJECTED** Callahan Construction Managers, project manager vacancy (2026). Job advert.

## Rejected, Brave query 3, "everyone knew it was going to be late" fragment set

Brave ignored the quoted phrases and returned twenty results of general LinkedIn content. Nothing
in the set was a project management post making an argument.

- **REJECTED** Derry Holt, "this is not a calendar problem. It's a respect problem" (2026-04-16). Meeting lateness and attendance. Directly overlaps yesterday's Josh Singer selection, reply-candidate-2026-08-17-002-singer-early-is-not-about-respect.
- **REJECTED** Maryam Asim, "I studied 500 LinkedIn posts this year", and five further LinkedIn growth and viral hook posts. Content marketing, not project management.
- **REJECTED** Glenn Burchard, Hans Bernard, Bret Havekost, Martin du Rand, Juliana Matheus Pires, Marika Lesell, Samantha Hueman, Chloe Shih, Naomi Blackman, Christopher Heimann, Dina Mainville, Zayd Syed Ali, Matter Creative. Thirteen results, none about projects. Quote cards, personal announcements, a scam warning and a B2B sales post.

## Rejected, Brave query 4, "the project didn't fail because" fragment set

Old and heavily saturated. Every result predates 2025 except where noted.

- **REJECTED** Harvard Business Review, "Why Big Projects Fail" (2023), twice, plus "Keep Your AI Projects on Track" (2023). HBR is already in the queue as an author and these are syndicated article shares.
- **REJECTED** Joe Peppard, "Why Do Companies' IT Projects Fail So Often?" (2023). Already in the queue as an author.
- **REJECTED** Jason Knight, "Why can't the engineers just work harder?" (2023). Already in the queue as an author.
- **REJECTED** Harvard Business Review, "Many Strategies Fail Because They're Not Actually Strategies", three separate reshares (2021 to 2023). Article shares.
- **REJECTED** Alvin FSC, "Why innovation requires failure" (2024). Aphorism.
- **REJECTED** Joe Aiken, "a very wise man once told me" (2021). Advice anecdote with no structural claim.
- **REJECTED** Alan Dyke, "We have to be willing to fail" (2022). Quote card.
- **REJECTED** Travis Dahlin, "#failforward #failfast" (2022). Hashtag post.
- **REJECTED** Gloabroad and Adela Javier Sanguyo, near identical "most businesses fail because they solve a problem that doesn't exist" posts (2023). Startup platitude.
- **REJECTED** Matthew Lerner, "Team grow fast and Team don't f up" (2023). Quality versus risk tolerance, but three years old and the point is covered by existing queue items.
- **REJECTED** Cindy Gallop, tech executive know-it-all problem (2022). Not about projects.
- **REJECTED** Russell Sarder, "What is a Chief Product Officer" (2025). Role explainer.
- **REJECTED** Julie Parker Communications, employee advocacy pilots (2026). Marketing, not projects.

## Rejected, LinkedIn top-content hub, project management

- **REJECTED** Daniel Pink, "Want to stay motivated every single day?" (12 months). Already in the queue as an author.
- **REJECTED** Chris Do, "Scope creep isn't a them problem. It's a you problem" (9 months). Already in the queue as an author, and scope creep is saturated.
- **REJECTED** Jingjin Liu, "They didn't even cc me" (1 year). Workplace alliances, not project structure.
- **REJECTED** Andrew Ng, "One Agent For Many Worlds" (2 years). AI agent workflows.
- **REJECTED** Gaurav Sharma, zero-based budgeting explainer (3 months). Finance explainer.
- **REJECTED** Pierre Le Manh, PMI Project Success study release (1 year). Institutional research announcement.
- **REJECTED** Hans Stegeman, WEF Global Risks Report 2026 (7 months). Macro risk commentary.
- **REJECTED** Severin Hacker, Google 20% time (2 years). Innovation practice.
- **REJECTED** Vitaly Friedman, "60 UX Strategy Methods" (1 year) and "How To Tackle Large, Complex Projects" (1 year). The second has a real claim, allocate 20 to 45 percent of effort to planning, but it is a methods list and the planning-effort argument is already answered several times in the queue.
- **REJECTED** Brij Kishore Pandey, pandas cheatsheet (1 year). Not project management.
- **REJECTED** Justin Bateh, "My S.C.O.P.E. Framework" (2 years). Acronym framework post.
- **REJECTED** Jesus Romero, "READY Checklist for Project Readiness" (1 year). Checklist.
- **REJECTED** Angela Wick, "Most teams struggle with done" (8 months). Strong candidate on the snippet, and there is a good counterpoint in it about widening the definition of done until it sits somewhere the team cannot reach. Could not locate the post URL through any available engine, so it could not be verified or fetched. Carry forward.
- **REJECTED** Lenka Pincot, "You can't move fast without clarity" (6 months). Same problem, URL not locatable. A different Pincot post was reachable and is the second selection.
- **REJECTED** Surya Vajpeyi, "Juggling 4 Projects at Once" (1 year). Personal productivity.
- **REJECTED** Sandeep Y., "$135 million lost for every $1 billion spent" (1 year). Statistic card.
- **REJECTED** Sonu Dev Joshi, "9 Principles for Successful Project Delivery" (1 year). List post.
- **REJECTED** Andy Werdin, requirements gathering for data projects (2 years). Method advice.
- **REJECTED** Richa Mamtora, "Is It Possible for a Fresher to Get a Project Manager Job?" (1 year). Careers content.

## Rejected, LinkedIn top-content hub, change management and governance

- **REJECTED** Eric Partaker, "70% of change initiatives fail. And it's rarely because the idea was bad." (1 year, 3,816 likes, 787 comments). By far the highest engagement post reached this run and the 70 percent figure is a zombie statistic worth attacking. Rejected because the body is a match-the-model-to-the-initiative list covering ADKAR, Lewin, Kotter and Nudge Theory, which falls squarely under the list post exclusion. Flagged as the strongest carry-forward if the exclusion is ever relaxed for high reach posts.
- **REJECTED** Jeroen Kraaijenbrink, ADKAR and the human journey (9 months). Already in the queue as an author.
- **REJECTED** Vineet Nayar, "IndiGo Crisis Wasn't in the Skies. It Was in the Leadership Cabin" (8 months, 3,282 likes, 330 comments). Real argument and high reach, and there is a structural reply about escalation paths having no capacity so the front line absorbs the failure. Rejected on two grounds: replying well would require factual claims about IndiGo's operations that cannot be grounded in anything under source/, and no post URL was obtainable.
- **REJECTED** Elfried Samba, hiring for potential over experience (2 years). Recruitment.
- **REJECTED** Cherie Hu, music tech ownership map (1 year). Sector analysis.
- **REJECTED** Steve Bartel, recruiting email analysis (1 year). Sales data.
- **REJECTED** Travis Bradberry, seven signs of emotional intelligence (1 year). Listicle.
- **REJECTED** Suniel Shetty, foundation partnership story (3 years). CSR.
- **REJECTED** Joshua Miller, reframing stress (12 months). Coaching content.
- **REJECTED** Yashara Malshani, Usama Israr, Poonath Sekar, Mohanraj S, Govind Tiwari, Somesh Rathor, Daniel Amundsen, CS Kamlesh Mishra, Angela Johnson. Nine results from the governance models hub, all QA and compliance checklists. The hub slug does not return governance content.

## Rejected, WebSearch targeted follow-ups

- **REJECTED** Matt Moore, "AI will not replace product managers" (2025). Already in the queue as an author.
- **REJECTED** PMI Open Community, "AI won't replace project managers. But it will elevate the best ones!" (2026-08-03). Webinar promotion.
- **REJECTED** Harshita Jain, Negin Zahedian, Ammad Chaudhary, three variations on "AI won't replace PMs, PMs who use AI will replace those who don't" (2026). The genre is now pure agreement content and the counterpoint has been made in the queue already.
- **REJECTED** Natasha Platt, "Project Management is Leading Change Successfully" (2026-07-29, 3 reactions). Fetched in full. Career reflection plus a seven item competency list. Nothing to argue with.
- **REJECTED** Ian McAteer, Samuel Harris, Daniel Brander, James Crawford, Samira Ayati, Faizaan Shaikh. Six job adverts.
- **REJECTED** Jodi Senese, retirement post (2025). Not project management.
- **REJECTED** Nine LinkedIn Pulse articles on RAG status, red projects and the death of the PMO, including Vivek Ganesan and Rob Thomsett, both of whom make genuinely good arguments. All rejected as Pulse articles rather than posts. Worth noting that the red status and PMO themes look under-served and would be productive if a real post on either can ever be found.
- **REJECTED** Muzzafar Siddiqi, Ethan Hills, and various LinkedIn Help pages returned on the project cancellation query. Not posts.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-18-001-saheed-the-answer-gets-frozen-at-funding.md`
  Counterpoint. Concedes that on-time-and-on-budget can still be worthless, then argues the wrong
  problem is not caused by missing analysis. Somebody nearly always asked the question. Funding the
  answer converts it from a question into the baseline everyone is measured against, so the
  requirements document becomes the obstacle to correcting course rather than the remedy. Lands on
  all projects are swamps, and closes on standing to revise a funded premise rather than on a
  better answer up front.

- `queue/reply-candidates/reply-candidate-2026-08-18-002-pincot-the-operating-model-is-the-funding-cycle.md`
  Structural observation. Agrees agile stopped at the team boundary, then supplies the mechanism:
  the team is the last level where changing how work happens costs nobody anything, and one level
  up the operating model is the annual funding commitment with names against the numbers. Adaptive
  operation therefore requires returning money mid-year and saying the bet did not pay. Answers the
  post's closing question directly. The thing that breaks first is the reporting, not the decision
  making.

Two drafted rather than three. The brief allows two to four. There was no third post this run that
met the bar without either an author collision, a list post exclusion, or an unobtainable URL. The
near misses are named above with the reason, and Angela Wick, Eric Partaker and Vineet Nayar are
all worth another attempt if their post URLs can be recovered.

# Notes

**The search infrastructure got materially worse than on 2026-08-17.** Brave was the only engine
that returned usable LinkedIn results, and it rate limited on roughly two thirds of attempts,
against zero rate limiting yesterday. Budget for that: shortlist from a small number of broad
queries rather than planning a long sequence of narrow ones.

**Brave now ignores long quoted-phrase queries.** Yesterday's productive technique, four or five
OR'd negated-premise fragments, returned pure noise twice this run. Brave appears to be falling
back to unquoted term matching when the phrase set is too specific. Two shorter quoted phrases work
better than five long ones.

**Engines confirmed dead, do not retry.**

- Google direct: HTTP 429, previously a consent redirect. Gone either way.
- Bing: silently ignores the `site:` operator and returns generic web results. Confirmed both
  through WebFetch and through curl with a browser user agent.
- Brave through curl: serves a JavaScript CAPTCHA page. Brave only works through WebFetch.
- DuckDuckGo html and lite endpoints: image CAPTCHA.
- Startpage: challenge page, 1.2KB response.
- Mojeek: HTTP 403 through both curl and WebFetch.
- Ecosia: HTTP 403.
- Yandex: SmartCaptcha.
- Stract: HTTP 404.
- SearXNG public instances, searx.be and search.disroot.org: return a stub page to GET requests.
  priv.au returns 429. A POST based approach was not attempted and might be worth one try.

**New route found: LinkedIn public top-content hubs.** `https://www.linkedin.com/top-content/<topic>/`
renders without login and lists real posts with author, headline, opening line, snippet, relative
age and engagement counts. `https://www.linkedin.com/top-content/project-management/` is the main
one, and the page carries links to roughly forty sibling topics, of which change-management,
leadership, organizational-culture and future-of-work are the relevant neighbours.

Two caveats learned the hard way. First, the hub does not expose post URLs, so a shortlisted post
still has to be located through a search engine before it can be verified or replied to, and this
run three good leads died exactly there. Second, invented sub-topic slugs do not 404, they silently
fall back to unrelated content. `stakeholder-management` returned career posts and
`project-management-governance-models` returned QA checklists. Only use slugs harvested from the
hub page itself.

The hub is sorted by engagement rather than recency, so it surfaces six to twelve month old posts.
That is consistent with what has been accepted before, given yesterday's selections dated from
November and December 2025.

**Activity ID decoding remains the best filter available.** Twenty-four IDs decoded for free this
run, twenty of twenty accurate across four runs now. Decode before spending a fetch, always.

**Queue state.** 255 candidate files before this run, 257 after. Author deduplication was run
against the combined set of `queue/reply-candidates/` and `observed/replies/`, which currently
covers roughly 175 unique authors. Both selections are new authors. Business analysis had zero
coverage in the queue before today.
