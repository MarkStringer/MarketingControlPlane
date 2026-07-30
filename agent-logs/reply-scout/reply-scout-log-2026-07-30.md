---
id: reply-scout-log-2026-07-30
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Actual routing used, in order:

1. **WebSearch** on the brief's query. Returned the same four stale index entries as every previous run (Sonal Sharma 2022, Chat Engineer 2023, Project Management Information 2023, Kory Kogon 2023). All previously rejected.
2. **The Google URL from the brief.** Still dead from this location. 302 to `consent.google.com/ml?...&gl=GR&hl=el`, a Greek consent interstitial. No results. Sixth consecutive run with this failure.
3. **Brave Search**, five queries. Productive for two of the three selections, then began returning HTTP 429 partway through the run.
4. **DuckDuckGo HTML endpoint**, tried as a substitute once Brave rate-limited. Yielded one usable hit (Tochukwu) before serving a CAPTCHA challenge and becoming unusable.
5. **Targeted WebSearch** on exact quoted post text, used to correct a misattributed URL (see Notes).

No post found today was published in the last 24 hours. Every selected post was verified by direct fetch of its URL, and the relative age LinkedIn reports is recorded in each candidate's front matter.

# Posts considered

| Author | Post | Verdict | Reason |
|---|---|---|---|
| Daniel Hemhauser | "No one likes you, Project Managers... wear those eye-rolls like badges of honor. They're proof you're doing something right." | **SELECTED** | Specific, falsifiable claim to push against: unpopularity treated as evidence of competence. Mark can show the badge destroys the only instrument the PM had, since the obstructive PM and the truth-telling PM get identical eye-rolls. 3,248 reactions, 667 comments, the highest-reach post found in any run so far. Repeat author, flagged below. |
| Joyce Tochukwu | "Day 1 of 10 Project Management Myths I Disagree With" — deviating from the plan is not failure, it is learning and adaptability | **SELECTED** | Arguable claim with a genuinely non-obvious counter: once deviation counts as learning, nothing counts as failure, and a pivot becomes indistinguishable from a rout. Reply adds the missing mechanism, a written stopping condition. Post ends on a direct question, which gives the reply a natural opening. |
| David Rullmann | "Beyond the Iron Triangle: Coherence in Project Management" — goal, value, norm, constraint; "Time, money, scope are real. But they're not sovereign." | **SELECTED** | One sharp sentence to attack. Reply argues constraints are sovereign by definition, that the triangle survives because it is falsifiable, and that coherence is an outcome dressed as an input. Structural observation rather than agreement. |
| John Crickett | "Too many software projects fail because of poor requirements" — NIST 30x defect cost curve, eight qualities of good requirements | REJECTED | **Exact duplicate.** Same post URL already drafted against on 2026-05-14 (`reply-candidate-2026-05-14-002-crickett-requirements-backwards.md`). Caught only by URL comparison, not by author name. Strongest claim found today and it was already used. |
| William Meller | "The Project Manager's Playbook for Staying Updated" | REJECTED | Newsletter teaser with a Substack link; the post body carries no argument. Also the source of a misattribution, see Notes. |
| David Pančur | "Every project manager knows this truth: the risk isn't in any single system. It's in space." | REJECTED | Opens as a real observation about interface risk between suppliers, then turns into a product pitch for the Alpha platform / FlexAir ecosystem. Corporate promotional. Posted 1 day ago, the only genuinely fresh post found all run, and unusable. |
| dōnō consulting | "Why AI projects fail quietly in 2026" — RAND 80.3%, MIT Sloan 95% | REJECTED | Roundup of quoted expert opinions plus consulting promotion. No position of its own to argue with. |
| Jinfeng Zhang | "Why million dollar knowledge graph projects fail" — completeness over utility, "capture everything before shipping anything" | REJECTED | Real claim, but the counterpoint available is standard ship-early advice. Held as a fallback. |
| Bonnie Biafore | Project Management Triangle clip; separate lessons learned clip | REJECTED | Post bodies are links to video clips. Also previously evaluated and rejected on 2026-07-29. The triangle theme is covered better by Rullmann this run. |
| Jason Knight | "Why can't the engineers just work harder" — the real problems are systemic, tech debt nobody is allowed to fix | REJECTED | Tech debt covered on 2026-07-24 (Hardy). |
| Sam Aquino | "Project Lead vs Project Manager" | REJECTED | Title taxonomy. Also rejected 2026-07-29. |
| Pritesh Jagani | "Product Manager vs Project Manager vs Technical PM" | REJECTED | Role taxonomy post. |
| Terry Prater | Meme reaction post about project management | REJECTED | Meme. Also rejected 2026-07-29. |
| Cezar Babes / Marios Malos / Tyler Caskey / Michael Lloyd / Albin Herlant | Anti-PM and "13 common truths" posts | REJECTED | All evaluated and rejected in prior runs; Caskey and Lloyd already replied to on 2026-07-24. |
| Mohamed R. | "I HATE being a Project Manager" | REJECTED | Venting, no argument. |
| Mohammad Hamid | "The Art of Saying No in Project Management" | REJECTED | Saying no covered on 2026-04-13 (Samuel) and 2026-07-20 (Cutler). |
| Successful Project Managers (3 posts) | Decisions not tools; process discipline; failures as accumulated small gaps | REJECTED | Template and list marketing account, rejected in prior runs. |
| Miguel Medina / MIGSO-Pcubed | "Too many projects and not enough visibility causes chaos" | REJECTED | PPM vendor promotion. |
| Brad Miller / Erin Erginer / Steve Tan / Gracie Perez-Marcojos | "How to Stay Focused If You're Assigned to Multiple Projects at Once" | REJECTED | Four reposts of the same LinkedIn Learning listicle. |
| Dan Alcalde / Dan Ryan / Amna Mazhar | Multitasking cost; 15 signs a solopreneur has too many projects; QA lessons | REJECTED | List posts. |
| CA Deepak Shah / Istio / Turkana County / Suzan Bibawi / UEGCL | Steering committee announcements and site visit photos | REJECTED | Announcements and institutional updates, no claim. |
| Seipi Riala / Asar Group / Vikas Sharma / Marzena C / United BIM / Jamile Cruz | Assorted "lessons from failed projects" posts | REJECTED | Generic lessons-learned content; only available reply is agreement. |
| Tareka Wheeler / Leadership and Management / Matt Quick | PMI awards call, Google PM certificate promotion | REJECTED | Promotion. |
| Melissa Jones / Malenie Zeng | "The most underrated skill in project management" | REJECTED | Engagement-bait framing with no stated position. |
| Mark Bruins / John Simmons / George P. Prior / Ken Martin / Wayne Lewis / Sam Undzyn / Meg Bartelt / Marjan Pantic / EFA Freelancers | 9 common mistakes, 99% of big projects fail, IT project failure, PM responsibilities, tool preference, approval tactics, inclusion practices, delivery-room joke, bottleneck webinar | REJECTED | List posts, definitional posts, memes or promotion. |
| Ryan Peterman / a16z / Aishwarya Srinivasan / Josh Payne / Jasmin Alić / Will McTighe / Sam G. Winsbury / and other LinkedIn-growth and side-project results | Off-topic results pulled in by loose query terms | REJECTED | Not about project management. |

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-07-30-001-hemhauser-eye-rolls-not-evidence.md` — Hemhauser tells PMs to wear eye-rolls as badges of honour. Reply accepts the rest of the post and attacks that line: the obstructive PM and the honest PM collect identical eye-rolls, so treating them as proof discards the only instrument available. Then the structural point, that organisations are happy to fund one designated unpopular person because it is cheaper than fixing whatever made the truth unsayable. Uses "bad news is data" and puts a condition on it. Ends on the test that actually matters, whether anything in the plan moved.
- `queue/reply-candidates/reply-candidate-2026-07-30-002-tochukwu-stopping-condition.md` — Tochukwu says deviation from the plan is learning, not failure. Reply grants it, then argues the reframe costs you the word failure entirely, that a pivot and a rout are indistinguishable from the inside and worse in retrospectives written by the survivors. Supplies the missing mechanism, a stopping condition written before kickoff. Uses "the project is a bet" and the folding metaphor.
- `queue/reply-candidates/reply-candidate-2026-07-30-003-rullmann-constraints-are-sovereign.md` — Rullmann proposes coherence across goal, value, norm and constraint in place of the iron triangle. Reply targets "they're not sovereign", argues the triangle survives sixty years of criticism because it is falsifiable and forces a choice, that goal, value and norm cannot lose an argument and so evaporate at the first real trade-off, and that coherence is an outcome wearing the costume of an input. Uses "all projects are swamps".

# Notes

- Three candidates drafted, all counterpoint or reframe replies rather than agreement, all verified by direct fetch.
- **Duplicate caught late.** John Crickett's requirements post was independently rediscovered this run and was the single best claim found, and it turned out to be the exact same URL already drafted against on 2026-05-14. The author name alone would not have caught it, because the 2026-05-14 file is one of two Crickett candidates in the queue. Worth adding a URL-level check against `queue/reply-candidates/` and `observed/replies/` early in the run rather than at draft time.
- **Misattribution caught and corrected.** Brave returned the "No one likes you, Project Managers" text under William Meller's URL, and WebSearch then repeated that attribution. Direct fetch of Meller's URL showed a completely different post about staying updated. An exact-phrase search traced the post to Daniel Hemhauser, and direct fetch of the Hemhauser URL confirmed the full text. Nothing was drafted against the unverified pairing. This is the concrete reason the direct-fetch rule matters, and it is the second search layer that introduced the error, not the first.
- **Repeat author, needs a decision.** Hemhauser was already replied to on 2026-04-02 on a different post. That reply's recorded themes were pm-relationship-to-bad-news and bad-news-is-data, and this draft also leans on "bad news is data", though the argument is about unpopularity as false evidence rather than about bad news reaching the sponsor. Reach is very high, 3,248 reactions. Flagging rather than spiking it. Zhang's knowledge graph post is the fallback if Mark would rather not go back to the same author.
- Themes deliberately avoided as saturated in the recent queue: scope creep, green and RAG status reporting, estimates versus deadlines, ownership of outcomes, coordination as a defence of the role, meetings, saying no, tech debt.
- Rullmann's reply engages an audience that skews towards systems and transformation consulting rather than delivery practitioners. Less of a stretch than last run's Project Controls candidate, but noting it.
- **Infrastructure, now failing on six consecutive runs.** There is no working route to LinkedIn posts published in the last 24 hours from this location. Google is blocked by a consent interstitial, WebSearch serves a stale index, Brave rate-limits after roughly five queries and has no reliable recency filter for `site:`, and DuckDuckGo CAPTCHAs. Every run is therefore drafting against posts one month to two years old, and the queue is starting to collide with itself, as the Crickett duplicate shows. This needs a tooling decision, either a LinkedIn API-based feed using the token already in `.env` or an accepted change to the brief that drops the 24-hour requirement.
