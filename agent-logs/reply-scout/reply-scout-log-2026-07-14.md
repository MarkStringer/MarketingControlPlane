---
id: reply-scout-log-2026-07-14
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Note: the dated `tbs=qdr:d` URL again returned a 302 to `consent.google.com` (GB consent wall) and could not be fetched, including with `&gl=us&hl=en` appended (still redirected to the GB consent page). Known recurring block, logged every run since 2026-06-30. Posts therefore came from WebSearch on the base query plus targeted variants (stakeholder/sponsor/governance, risk/uncertainty/assumptions, lessons-learned/retrospective/postmortem, "the real problem"/nobody/truth, status report/RAG/honest, accountability/blame, AI replacing PMs, change management/resistance, the plan/reality/contingency, morale/trust/psychological safety, decision-making/committees). WebSearch does not honour the 24-hour window, so several hits are older evergreen posts surfaced by relevance rather than recency.

All three selected posts were fetched directly and their arguments confirmed (full text visible, no sign-in wall) before drafting, per content policy. Posts that could not be verified were not drafted against.

# Posts considered

- Justin Lake — "Why project managers get blamed for everything." Argues PMs are unfairly blamed even though they are usually the only ones willing to own it; frames blame as proof of commitment ("if you're good you'll get blamed because you cared enough to own it") and casts the PM as scapegoat at the intersection of scope, people and delivery — SELECTED (001). Fresh author, not in observed/replies or the candidate queue. Verified by fetch (full text visible). Non-obvious addition: blame is a function of the seat, not the caring. The PM is the one role handed responsibility for the whole project without the authority to move most of it, so when the collective bet fails the org needs one name and yours is the only one written against the entire thing. Caring harder doesn't change that; matching authority to accountability does. The project is a bet the whole room placed. Bad news is data, so is which desk it lands on. Distinct from the 07-13 sunk-cost-in-the-org-chart reply (that was about who folds; this is about responsibility without authority).
- Abhishek Kumar — "Smarter Decisions, Not More Data." Argues Agile teams suffer from too much data not too little; wants patterns not numbers, insights not dashboards, conversations powered by data not controlled by it — SELECTED (002). Fresh angle, not previously replied to. Verified by fetch (full text visible). Reframe available: the cause isn't data hygiene, it's that a dashboard is a place to leave a decision so nobody has to be the one who made it. If the number is wrong the number takes the hit; if a person calls it, the person does. "We need more data" is a request for cover, not insight, and a tighter metric set still can't take a view and own it. Point of view is worth 80 IQ points; no dashboard has one.
- Tim Hillison — "Why Decisions Get Delayed in Buying Committees." Argues bigger committees produce more stakeholders, more alignment and less accountability to decide; nobody wants to be wrong in front of everyone, so safety looks like progress while nothing gets decided — SELECTED (003). Fresh author. Framed for go-to-market/sales but the dynamic is identical to project steering committees, and the reply bridges it explicitly. Verified by fetch (full text quoted). Reframe: adding people to a decision doesn't spread the risk, it removes the owner. A decision needs one person for whom being wrong costs something; a big room shares that cost down to nothing while keeping the cost of being the one who called it whole. Inaction wins because inaction has no author. Fix: shrink the number who can say no, name the one who has to say yes. All projects are swamps; a big enough room is how a swamp votes to stay wet.
- Jonty Plewes — "What does a Change Manager actually do?" — REJECTED. On fetch this turned out to be a five-point explainer of change-manager responsibilities (strategy, resistance, comms, training, adoption) with no single contestable thesis of his own. The promising "most changes fail because the people side wasn't managed well" claim I hoped to counter was adjacent reshared content, not Plewes's own words. Drafting a counterpoint against a claim he didn't make would breach the content policy on unsupported claims about external posts.
- Michael Otjen — "When Will This Project Go Live?" (no plan, no credible date) — REJECTED. Already replied to on 2026-07-03 (otjen-plan-is-a-bet).
- Maarten Dalmijn — "Why do many tech companies suck at planning" — REJECTED. Dalmijn replied to repeatedly (04-29, 05-15, 05-27); planning/estimation theme heavily worked.
- Jeroen Kraaijenbrink — strategy-is-not-a-plan / strategy execution posts — REJECTED. Replied to on 2026-07-13 (kraaijenbrink-clarity-vs-credibility).
- Tyler Caskey — "Do most project managers suck?" — REJECTED. Already replied to on 2026-07-02.
- Terry Prater — "What is project management and why should PMs do it?" — REJECTED. Already replied to (04-20, 05-12).
- Gary O'Reilly — "The difference between project managers and program managers" — REJECTED. Definitional; already replied to (06-29).
- Bonnie Biafore — project vs work management clip — REJECTED. Biafore replied to repeatedly (05-20, 06-09).
- Dan Gardner — "When Confidence Helps Project Managers" — REJECTED. Already replied to twice (04-27, 05-07).
- Andrew Ramdayal — "Project Manager Burnout: Managing Uncertainty" — REJECTED. Ramdayal replied to repeatedly (05-06, 06-02, 06-12, 06-18); burnout theme worked.
- Alex Lyaschenko — "The Critical Path Method is more than you think" — REJECTED. Lyaschenko replied to (04-22, 06-24).
- Michael Lloyd / Sam Aquino / Holly Knoll / Cindy Okosun — REJECTED. All previously replied to (Lloyd 05-08/06-16, Aquino 07-09, Knoll 05-22, Okosun 05-18).
- John McIntyre — "There's a misconception I see frequently when PMs are working" — REJECTED. Replied to yesterday (2026-07-13, 002).
- John Sills — "You don't have a people problem, you have a process problem" — REJECTED. Generic org-behaviour aphorism, not PM-specific; the process-vs-people frame invites agreement not a reframe. (Also surfaced and rejected on 07-13.)
- Vernon Shen — "Bad Project Management: Blame, Credit, and Leadership" — REJECTED. "Not-to-do" listicle of bad-PM behaviours, no single contestable claim.
- Justin Lake adjacency / Leila Hormozi — "The worst managers blame their team" / Karan Hasija — "Is it right to blame managers when employees quit?" — REJECTED. Generic management-blame aphorisms, not project-specific, agreement-only.
- Roger Martin — "Why Planning Over Strategy?" / "#strategy" — REJECTED. Strategy-vs-planning; theme covered (kraaijenbrink 05-01/07-13, moss 05-29) and these are short link-share posts.
- Melissa Perri — "What is the Cost of Delay?" — REJECTED. Definitional/product-management; product-vs-project already covered.
- John Cutler — "You can't prioritize something unless you deprioritize something else" — REJECTED. Cutler replied to (06-15, 06-25); this one is a short aphorism.
- Harry Hall — "What is Risk Threshold" / "What is a Pre-Mortem?" — REJECTED. Glossary/definitional.
- Kevin DiGilio — "Difference Between Risk and Issue" — REJECTED. Glossary/definitional.
- Preparationinfo / atRISK — Monte Carlo / risk modelling — REJECTED. Tool and method promotion; Monte Carlo already covered (04-22 preparationinfo).
- Taskleon — "Eliminate Execution Uncertainty with PM tools" — REJECTED. Already replied to on 2026-06-30 (taskleon-tools-eliminate-uncertainty).
- Sangam Pandey — "Removing uncertainty: the tip of the iceberg" — REJECTED. Already replied to (06-26, pandey-uncertainty-sequence).
- Oyvind Henriksen — "We're three project members down, so the project is screwed" — REJECTED. Already replied to (2026-07-09, 001).
- Joshua Teter — "What is a 'status' report? Word nerd alert" — REJECTED. Definitional/etymology post, no contestable thesis; status-report/RAG theme also heavily worked (07-09 vanbinsbergen).
- William Meller — "The Project Manager's Playbook for Staying Updated" — REJECTED. Listicle; Meller listed in prior rejections.
- Albin Herlant — "13 Common Truths about Projects" / Pritesh Jagani — "Product vs Project vs Technical Program Manager" / Ken Martin — "PM Roles & Responsibilities" — REJECTED. Listicles and definitional role comparisons.
- Semih Kumluk / Foresight / Malina Sos / Liza Yakimchuk / Dan Ryan / Capterra / Rishi Kapil / Fintech Association of Kenya — "How AI will transform/redefine project management" — REJECTED. AI-hype reshares and tool/credential promotion; AI-PM theme heavily covered (05-18, 05-22, 06-02, 06-05, tiwari 05-27).
- Jonty Plewes adjacency / Friska Wirya / Brittany Stone / Manjeet Kaur / Rikard Bergstrom / PCE / Hina Sohrab / PMIWDC — change-management explainers, transformation reshares, tool and event promotion — REJECTED. Explainer/listicle/promotional; no single contestable thesis.
- Oludayo Sokunbi / Morgan Davis / Irila Marr / Scott McKissock / Parabol / Catapult Labs / Lenny Rachitsky (Shreyas Doshi) — retrospective and post-mortem how-tos and reshares — REJECTED. Method explainers; pre-mortem/retro theme already covered (05-06); agreement-only.
- Daniel Bouchard — "Establish Team Morale" / Patricia Cadavid Mesa — "Reenergize Your Team When Morale Is Low" / HBR + jeremy barnes + others — psychological safety reshares — REJECTED. Generic morale/psych-safety content, article reshares, agreement-only. (HBR psych-safety piece and reshares also rejected on 07-10.)
- Kory Kogon / Pasang Sherpa / Chat Engineer / Marco Kalz / Successful Project Managers (49 processes, templates) / Whitney Akabike / Sandra Boyle / projectmanagementinformation / Center for Project Innovation / Hiu Fu Shun / Soksamnang Phouk — REJECTED. Glossary, basics, course-completion brags, templates and tool promotion. No claim to engage.
- STS / Quarrydale / Nilesh Rathi / TEAM 1144 / projectworks.io / Tulsi Soni / The Digital Project Manager (Top 81 influencers) — REJECTED. Product, recruitment, event and influencer-list promotion.

# Replies drafted

- reply-candidate-2026-07-14-001-lake-blame-authority-sink.md — Justin Lake. The blame is real but "you get blamed because you cared" is a story that keeps you standing there. You get blamed because of where you sit: the PM is the one seat handed responsibility for the whole project without the authority to move most of it, so when the collective bet fails the org needs one name and yours is the only one written against the entire thing. Caring harder doesn't change that. The project is a bet the whole room placed; fight for authority that matches the accountability, and refuse to own a number you're not allowed to change. Bad news is data, so is which desk it lands on.
- reply-candidate-2026-07-14-002-kumar-dashboard-hides-decision.md — Abhishek Kumar. Agreed on the symptom, wrong on the cause: teams don't accumulate dashboards from indiscipline, they accumulate them because a dashboard is a place to leave a decision so nobody has to be the one who made it. If the number is wrong the number takes the hit; if a person calls it, the person does. "We need more data" is a request for cover, not insight, and a tighter metric set still can't take a view and own it. Point of view is worth 80 IQ points; no dashboard has one. Give people permission to be wrong in public and the data problem mostly disappears.
- reply-candidate-2026-07-14-003-hillison-committee-no-owner.md — Tim Hillison. This is every steering committee, just with a sales label. Adding people to a decision doesn't spread the risk, it removes the owner: a decision needs one person for whom being wrong costs something, and a big room shares that cost down to nothing while keeping whole the cost of being the one who called it. Alignment, next steps and follow-ups produce artefacts, not decisions, because a decision is the one output with a name attached. Inaction wins because inaction has no author. Shrink the number who can say no, name the one who has to say yes. All projects are swamps; a big enough room is how a swamp votes to stay wet.

# Notes

- 3 candidates drafted from 60+ posts considered.
- All three selected authors (Lake, Kumar, Hillison) are fresh, not previously replied to per `observed/replies/` and the candidate queue. Caveat: "Abhishek Kumar" is a common name and the queue holds an unrelated `kumar-complexity-real-issue` (06-12) on a different topic; treated as a distinct author/post, flagging for Mark's judgement.
- Theme spread is deliberate and non-overlapping: responsibility-without-authority / blame (001), data-as-cover for unmade decisions (002), and committee diffusion of decision ownership (003). 001 shares the "org chart" instinct with the 07-13 sunk-cost reply but argues a different mechanism (authority vs accountability, not who folds). 002 and 003 both touch decision-making but from opposite ends (avoiding a call via data vs avoiding a call via crowd); written to stay distinct.
- Each selected post was fetched and its argument confirmed (full text visible, no sign-in wall) before drafting, so the post_summary fields are grounded rather than inferred from search snippets, per content policy.
- Hillison's post is framed for go-to-market/sales rather than project management, but the buying-committee dynamic is identical to steering-committee decision paralysis; the reply bridges this explicitly rather than pretending the post is about projects.
- `queue/reply-candidates/template-reply-candidate.md` still does not exist (missing since at least 2026-06-26). Format was matched to recent candidates (2026-07-13 series). Should either be created or the task instruction updated to point at an existing example.
- Recurring blocker: the `qdr:d` Google URL remains unusable from GB due to the consent redirect, even with `&gl=us` appended. A stored consent cookie would restore true 24-hour recency. Until then this agent searches an evergreen corpus, so cross-checking against `observed/replies/` and the candidate queue does most of the recency and de-duplication work.
