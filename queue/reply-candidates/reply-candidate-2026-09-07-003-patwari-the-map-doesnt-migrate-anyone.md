---
date: 2026-09-07
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Puneet Patwari
post_url: https://www.linkedin.com/posts/puneet-patwari_this-is-a-dependency-discovery-traffic-control-activity-7449421629325217792-VkCT
post_summary: >
  Puneet Patwari answers a hypothetical about decommissioning an old service when six consumer teams
  have not confirmed migration. He argues, as a Principal Engineer would, that "migration emails are
  not your source of truth, traffic is": build a hard dependency map from request logs, tracing, and
  gateway metrics rather than trusting team replies. He then classifies consumers by risk (migrated,
  low-risk with fallback, high-risk on critical paths, unknown/unowned), converts the shutdown into
  a routing exercise using per-caller rules, feature flags, canary cutover and kill switches rather
  than "a trust exercise," and states that after three weeks of silence the six teams become "a
  leadership and risk issue" to be escalated with hard data (RPM by team, business criticality,
  cutoff date, blast radius). Closes with a staged four-week shutdown plan and a plug for his
  interview-prep guide. Verified by direct fetch of full post text and structured data;
  datePublished 2026-04-13T11:41:59Z (decoded from the activity ID, exact match), so about five
  months old, not same-day. 487 reactions, 52 comments at time of fetch. Checked against
  observed/replies/ and queue/reply-candidates/: existing drafts on technical debt and systemic
  engineering-management blame exist but none on dependency mapping, deprecation, or self-report
  versus instrumented evidence; Puneet Patwari is new to the repo.
book_themes:
  - bad news is data
stance: structural observation
risk: low
notes: >
  Selected because Patwari has already built the correct instrument (traffic over self-report) but
  the post treats the escalation in step four as the last item on a checklist rather than as the
  actual point of the first three steps. Mark's addition names what the dependency map is actually
  for: not migrating anyone, but removing the excuse for not knowing who to hold accountable once
  the deadline lands. It also adds the reason the six teams were silent that no amount of
  observability fixes: replying commits them to someone else's deadline, which is a people problem
  the traffic data cannot solve, only make impossible to hide from. All RPM figures, the four
  consumer categories, and the staged plan are his; no numbers of Mark's own are used. Software
  delivery rather than construction or classic PM, which widens the post's subject range for this
  run without straining the transfer, since dependency ownership and deadline avoidance are not
  domain specific.
---

Steps one through three are good, and they are also not the hard part. Replacing "did you migrate" with the request logs just swaps a self-report for an instrument, and once you have the instrument the six silent teams stop being a mystery and start being a number: 11,000 requests a minute, two owners, one deadline.

That is bad news is data, done properly. Nobody has to believe the silent teams are behaving. You can check.

But notice what the whole exercise actually produces. It is not a migration. It is a document that says who has to answer for the risk once the deadline arrives, backed by traffic nobody can argue with. The dependency map does not migrate anyone. It removes the excuse for not knowing who to point at.

The six teams were never silent because they lacked visibility into their own traffic. They were silent because replying commits them to a date that is not their priority, and no amount of instrumentation changes that calculation for them. What it changes is the calculation for you. Before the map, escalating is a complaint. After it, escalating is a fact with a number attached, and that is the entire point of building it.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
