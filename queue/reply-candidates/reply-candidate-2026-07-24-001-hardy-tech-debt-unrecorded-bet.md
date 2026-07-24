---
date: 2026-07-24
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Graham Hardy
post_url: https://www.linkedin.com/posts/gthardy_engineering-leadership-technicaldebt-activity-7319661897740406784-Tzdr
post_summary: Graham Hardy argues that technical debt is a myth and is really a business clarity problem. He says most tech teams reserve 20% of their time for technical debt and that this is the wrong approach, that tech debt is not about bad code but about outdated business context, and that engineers talk about paying it down without connecting it to business value. He reports asking engineers "Why?" when they want to refactor, getting "The code is messy", and answering "So what?". He quotes an unnamed product development leader as saying "The thing about Spaghetti Code is it's battle tested". He argues product teams should be 100% committed to delivering customer value rather than carving out separate technical debt time, and that the question is not "Is this code clean?" but "Does this code prevent us from delivering what customers need RIGHT NOW?". Full text confirmed by direct fetch; 77 reactions, 74 comments, posted roughly April 2025 per LinkedIn's relative date, so older than 24 hours.
---

"Does this code prevent us from delivering what customers need right now" is a good question. It is also the exact mechanism that produces the thing you are saying does not exist.

Run that test on every decision for two years. Each individual answer is correct. Nothing in front of you right now is blocked, so you ship. The cost turns up later, in somebody else's estimate, on a piece of work neither of you is on. By then it is not traceable to any particular decision, which is precisely why it ends up getting called debt rather than a choice somebody made.

The Spaghetti Code line is true and it is a trap. Battle tested code is fine until the day you have to change it. Nobody refactors code they never touch. The messy code that actually costs you is always the code sitting underneath the next thing the business asks for, and you find out which code that is after the business has asked.

So I would keep the word. Debt is a decent name for a cost you have already incurred and have not paid yet.

What is missing is not business clarity. It is a record. Every shortcut is a bet that you will not have to come back to that part of the system. Sometimes that bet is right and you never pay a penny, and nobody ever writes those ones up as a triumph either. The problem is that nobody writes the bet down at all, so when it loses two years later it reads as engineering incompetence rather than as a decision the business made deliberately and would probably make again.

Engineers asking for twenty percent are not asking for tidying up time. They are asking you to settle bets you placed and forgot.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
