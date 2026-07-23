---
date: 2026-07-23
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Martin Hinshelwood
post_url: https://www.linkedin.com/posts/martinhinshelwood_stop-putting-acceptance-criteria-on-the-definition-activity-7411457346914344960-NvGB
post_summary: Martin Hinshelwood argues that putting acceptance criteria into the Definition of Done is a category error that weakens both. The DoD is an objective, universal, non-negotiable quality baseline answering "is the Increment releasable" and should cover security, telemetry, testing, deployment readiness and compliance. Acceptance criteria are item-specific, negotiable, and answer "did we build the right thing". He says mixing them replaces an objective quality constraint with subjective negotiation, and advises promoting any always-applicable criterion into the DoD rather than using the DoD as a dumping ground. Full text confirmed by direct fetch; 91 reactions, 28 comments, posted roughly January 2026 per LinkedIn's relative date, so older than 24 hours. No prior reply to this author in the queue or in observed/replies.
---

The taxonomy is right. I don't think it's a category error though. I think it's smuggling, and it's rational.

The Definition of Done is the only artefact on most projects that the organisation has publicly agreed not to argue with. So that is exactly where people park the things they know would otherwise get traded away. Accessibility. Security. Telemetry. As an acceptance criterion, each of those is a conversation you have to win again every sprint. In the DoD it's a fact. Anyone who has watched accessibility get deferred four sprints running learns where to put it the fifth time.

Which points at the more awkward thing. The DoD isn't sacrosanct. It's non-negotiable right up until a date is at risk, and then it gets relaxed just for this release and quietly never restored. The category stays clean and the protection turns out to be fictional, which is how you end up with a pristine one-page DoD and a security review nobody has run since March.

So the question isn't whether your DoD has become a dumping ground. It's why the team decided they needed a locked drawer. They were telling you something about what happens to quality the moment it becomes negotiable, and on the evidence they were right.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
