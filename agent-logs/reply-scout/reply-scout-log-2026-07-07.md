---
id: reply-scout-log-2026-07-07
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Note: the `tbs=qdr:d` Google URL again hit the GB consent-page redirect (302 to consent.google.com) and could not be fetched. WebSearch was used instead across several targeted queries; it surfaces mostly evergreen posts rather than strictly last-24h, so selection leaned on substance of claim and non-repetition of recent themes/authors.

# Posts considered

- Ben Sands — "Most teams don't have a talent problem, they have a clarity problem" + 10 wording swaps. SELECTED. Specific arguable thesis; Mark can reframe vague language as a survival strategy (bad news is data), not a vocabulary gap.
- Kyle Nitchen — client delivery makes you a commodity, client experience makes you irreplaceable. SELECTED. Specific claim; Mark can move the line to bad-news-under-pressure being where trust is actually earned.
- Gary O'Reilly — PM delivers the project, program manager delivers the benefit. REJECTED. Same post already replied to on 2026-06-29 (oreilly-delivery-benefit-split); no repeats.
- Oyvind Henriksen — "Translated: we're three project members down, so the project is screwed." REJECTED. One-line joke, nothing structural to add.
- K N Majdalani — "Successful project managers have ownership attitude combined with knowledge and experience." REJECTED. Generic aphorism; only possible reply is agreement.
- Ben Sands (Rachel Oddie / Kory Kogon / Sonal Sharma / Chat Engineer "What is project management") — REJECTED. Glossary / "what is PM" explainer posts.
- "Understanding the 49 Project Management Processes" / Rachel Oddie "5 skills every business leader needs" / Whitney Akabike skills list. REJECTED. List / glossary posts.
- Bonnie Biafore — project vs work management clip. REJECTED. Definitional; and Biafore theme covered recently (biafore posts on 05-20, 06-09).
- Terry Mustard — "I often see projects managed very poorly." REJECTED. Mustard covered recently (06-30 mustard-engineer-personality-badnews).
- Steve McDonald — "Why Project Management is (often) a really bad idea" (Pulse article). REJECTED. Pulse article not a post; McDonald covered 06-22 (mcdonald-project-product-bet).
- Kurtis Graham "The Perfect Plan is a Trap" / Michelle Gibbings "Are you falling into a planning trap?" / David Nash "3 Types of Terrible Project Planner". REJECTED. Pulse articles, and planning-trap theme heavily covered recently.
- David Odeleye "7 things nobody tells you about being a project manager" / Albin Herlant "13 Common Truths about Projects". REJECTED. List posts.
- RAG-status honesty articles (institutebprojectmanagement, ClearPoint, Designveloper, LinkedIn advice). REJECTED. Blog/advice articles, not individual posts; bad-news-hiding theme heavily covered (giller, doshi, mustard, mcnamara).
- Dan Gardner "When Confidence Helps Project Managers." REJECTED. Gardner covered twice recently (04-24, 05-07).
- Tyler Caskey "Do most project managers suck." REJECTED. Caskey covered recently (07-02 caskey-most-pms-suck).

# Replies drafted

- reply-candidate-2026-07-07-001-sands-clarity-problem.md — reframes Ben Sands' "clarity problem": vague language is a survival strategy where bad news is punished; wording swaps just produce crisper fictions. Fix the safety, not the phrasing.
- reply-candidate-2026-07-07-002-nitchen-experience-under-bad-news.md — moves Kyle Nitchen's delivery/experience line: attentiveness on a green project is easy; the irreplaceable partner is the one who brings bad news early, while it's still cheap to act on.

# Notes

- Two candidates selected (target is 2–4). Held to selection discipline rather than forcing a third from a list post or repeating a recent author.
- Signature phrase "bad news is data" used naturally in both; Sands draft also leans on the safety-of-bad-news structural theme, Nitchen draft on early honest reporting.
- Voice checks: no hashtags, no em-dashes, no bullet points in the reply bodies, each ends on a point not a question.
- Recurring blocker: the `qdr:d` Google URL is unusable from GB due to consent redirect. Consider adding `&gl=us` / a consent-cookie workaround, or relying on WebSearch date-scoped queries in a future iteration.
