---
date: 2026-09-18
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Akshay Saini
post_url: https://www.linkedin.com/posts/akshaymarch7_what-happened-with-cloudflare-and-what-can-activity-7397147901912707072-7mUA
post_summary: >
  Recaps the 18 November 2025 Cloudflare global outage: a database-permission change caused a Bot
  Management "feature file" to double in size, which crashed core proxy software and produced
  widespread HTTP 5xx errors, taking down X, ChatGPT, Canva and NJ Transit among others. Not a
  cyberattack. Cloudflare rolled back and restored service by ~17:06 UTC. The post then lists five
  numbered lessons: dependency risk is real, internal config changes are high risk, build robust
  rollback/kill-switch mechanisms, transparent incident comms matter, design for failure always.
  Verified by direct curl fetch; full JSON-LD articleBody recovered. Posted 2025-11-20 (datePublished
  confirmed against activity-ID decode), so about 10 months old. 1,317 reactions, 28 comments
  (commentCount confirmed in JSON-LD). Author display name confirmed via the page's
  "View profile for Akshay Saini" aria-label (JSON-LD author.name field returned an unrelated
  name, "Savio D'souza" - the known batch-misattribution bug flagged on 2026-09-10 and again
  2026-09-16/17, so og:title/aria-label was used instead). Dedup: akshaymarch7 not present in
  observed/replies or any existing queue/reply-candidates file; clean author and URL dedup.
book_themes:
  - the project is a bet
  - bad news is data
stance: reframe
risk: low
notes: >
  Selected despite the numbered-list shape because the list is a real incident's factual timeline
  plus a genuinely illustrative "lessons" list hanging off one load-bearing, falsifiable claim
  buried in item 1: the failure came from an internal, trusted pipeline, not an external attacker.
  The reply does not restate the five lessons (that would be pure agreement, the explicit reject
  case). Instead it argues the structural reason trusted-internal changes get less scrutiny than
  external threats, and draws the parallel to project status reporting: the parts of a project
  nobody prices as risk are the ones that look too routine to be risk, not the ones everyone is
  already watching. Only facts stated in the post are used (date, cause, outcome); nothing about
  Cloudflare's internal processes is asserted beyond what the poster wrote. No prior candidate or
  observed reply targets this post or this author.
---

Every one of those five lessons is right. Dependency risk, rollback and kill-switches, transparent comms, designing for failure. No argument there.

But the line that matters most is buried halfway down the list, not at the top of it: the outage wasn't caused by an external threat. It was caused by an internal, trusted pipeline.

That is the part worth sitting with. Organisations build real defences against attackers, because attackers are visible and expected. Nobody builds the same defences against their own "we do this every week" process, because trusted things don't look like risk. They look like plumbing.

Projects fail the same way. The status report nobody double-checks because the same person has always filed it. The internal handoff that skips review because it is internal. Every project is a bet, and the part of the bet that sinks it is rarely the risk everyone is watching. It is the one nobody thought to price, because it looked too routine to be a risk at all.

Cloudflare's transparency after the fact was the right call. The harder discipline is before the fact: treat "trusted and internal" as a reason to look closer, not a reason to look away.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
