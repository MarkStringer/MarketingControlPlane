---
id: reply-scout-log-2026-07-08
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Note: the dated `tbs=qdr:d` Google URL again redirects to the GB consent wall (302 to consent.google.com) and cannot be fetched in this environment. Known recurring block. Posts came from WebSearch on the base query plus targeted variants (risk register theater, lessons learned, status green, assumptions in planning, gut feel vs data, Brooks's Law / adding people, managing up the sponsor). WebSearch does not honour the 24-hour window, so some hits are older posts surfaced by relevance. The three selected posts were fetched directly and their claims quoted before drafting, per content policy.

# Posts considered

- Ravi Prakash — "Assumptions don't kill projects, unverified assumptions do" (document, time-bound, review, convert to risk) — SELECTED (001). Specific contestable thesis; reframe available: the assumptions that hurt are the invisible ones you never wrote down, and a tidy log doesn't drain the swamp. The project is a bet / all projects are swamps. Fresh author, not previously replied to.
- Matt Watson — "This is what happens when you just add more devs" (Brooks's Law, adding engineers to a late project makes it worse) — SELECTED (002). Restates a correct law but leaves room to move the point: the lateness was baked in when the plan pretended the work was smaller; adding people avoids the real conversation. Deliver the possible not the fantasy. Brooks's Law / staffing-panic theme not covered in the queue; fresh author.
- Jon Hall — "Lessons learned from a project that went sideways" (five crisis-leadership practices; defense project you cannot cancel or shelve) — SELECTED (003). Specific claim plus a concrete constraint (can't cancel). Reframe: when the escape hatch is bolted shut, the only lever left is how early the truth reaches someone who can act; standards are the plumbing for bad news. Bad news is data. Fresh author, defense angle distinct.
- Anne Nnamani — "Gut feeling vs data-driven decisions: which wins" — REJECTED. Not really project management, and the post already lands on a balanced "use both" conclusion, so the only available reply is agreement.
- Dr. Mohamed Hussien — "Monday green, Tuesday green... Friday 4:56pm stakeholder 'just one small thing' → red" — REJECTED. Meme-format post; the structural point (status stays green until it doesn't) is bad-news territory already heavily worked (giller, doshi, mustard, mcnamara, thorpe).
- Ravi Prakash (assumption-log explainers: certificationshub, projectmanagementinformation, Dr Tony Prensa, Mustafa Katary, Cloudwards) — REJECTED. Glossary / how-to posts on the assumption log; no contestable argument.
- Matthijs Cox / Iqbal Baouche / Robert McKnight / Daniel Hansen — Brooks's Law restatements — REJECTED. Same law, less argument than the Watson post; Watson selected as the representative with a concrete claim.
- Noah Berk / Guru Karur — "Here's why all your projects are always late" — REJECTED. Listicle/advice reshares, no single contestable thesis.
- Jon Hall's peers (William Meller "Playbook for Staying Updated") — REJECTED. Roundup/list.
- John Sills — "You don't have a people problem, you have a process problem" — REJECTED. Not PM-specific, and the reframe overlaps the Ben Sands clarity reply already drafted (07-07).
- Kate Zepernick / August Ball / David McNamara — REJECTED. Already replied to on 2026-07-06.
- Ben Sands — "clarity problem" — REJECTED. Already replied to on 2026-07-07.
- Tyler Caskey — "Do most project managers suck" — REJECTED. Already replied to (07-02).
- Terry Prater — "what is project management" — REJECTED. Already replied to (04-20, 05-12).
- Gary O'Reilly — PM vs program manager — REJECTED. Already replied to (06-29).
- Bonnie Biafore — project vs work management clip — REJECTED. Definitional; Biafore replied to repeatedly (05-20, 06-09).
- Harry Hall — "What is Risk Threshold" — REJECTED. Glossary/definitional.
- Kory Kogon / Sonal Sharma / Chat Engineer / Rachel Oddie / Whitney Akabike / Successful Project Managers / projectmanagementinformation / Pasang Sherpa — glossary, basics, skills lists, links, course brags — REJECTED. No contestable claim.
- Harvard Business Review — "Planning Doesn't Have to Be the Enemy of Agile" — REJECTED. 2021 article share; planning theme heavily covered.
- Cindy Okosun — AI predictive scheduling — REJECTED. Okosun replied to (05-18); AI-PM theme worn.
- Lisa-Marie Nociforo — "Are you a Project Manager AND Project Sponsor?" — REJECTED. Reasonable post but authority/ownership theme covered recently (bratu 06-29); Brooks's Law is fresher for the third slot.
- Various template/tool promos (Center for Project Innovation, Digital Project Manager, Rocketsheets, Planview) — REJECTED. Template/product promotion.

# Replies drafted

- reply-candidate-2026-07-08-001-prakash-unverified-assumptions.md — Ravi Prakash. "Unverified assumptions" frames it as hygiene; the ones that sink you are the invisible assumptions nobody wrote down. A project is a bet on a visible stack and a bigger unseen stack. You drain the swamp by getting in the water early, not by keeping a tidy log. The project is a bet / all projects are swamps.
- reply-candidate-2026-07-08-002-watson-brooks-law-fantasy.md — Matt Watson. Brooks's Law is right but answers the wrong question; the project became late the day the plan pretended the work was smaller than it was. Adding people looks like action and dodges the real conversation, that the scope was a fantasy. Change what you promised, not who's carrying it. Deliver the possible not the fantasy.
- reply-candidate-2026-07-08-003-hall-cant-cancel-bad-news.md — Jon Hall. When you can't cancel a project, the only lever is how early the truth reaches someone who can act; standards are the plumbing that carries bad news while it's small. Humility over ego is the same point: dropping a bad plan means saying the bet went wrong, which no alignment makes safe if it gets punished. Bad news is data.

# Notes

- 3 candidates drafted from 30+ posts considered.
- Three distinct themes chosen deliberately (assumptions as the bet, staffing-panic / Brooks's Law, the project you can't cancel), each carrying a different signature idea: "the project is a bet" / "all projects are swamps", "deliver the possible not the fantasy", "bad news is data".
- Three fresh authors this run (Prakash, Watson, Hall), none previously replied to, and no theme duplicating recent queue runs (clarity problem, delivery/experience, rot-not-a-layer, resistance-is-data, budget-as-a-bet).
- All three selected posts were fetched and quoted before drafting, so post summaries are grounded rather than inferred from search snippets, per content policy.
- All drafts follow reply voice rules: no hashtags, no em-dashes, no bullet points, ends on a point not a question.
- Recurring blocker: the `qdr:d` Google URL remains unusable from GB due to the consent redirect. A `&gl=us` parameter or consent-cookie workaround would restore true 24-hour recency.
