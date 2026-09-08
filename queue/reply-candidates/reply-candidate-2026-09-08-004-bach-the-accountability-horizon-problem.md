---
date: 2026-09-08
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Andreas Bach
post_url: https://www.linkedin.com/posts/a-bach_the-site-manager-saw-a-clean-installation-activity-7405559649757818880-slal
post_summary: >
  Andreas Bach describes visiting a PV plant in Germany that looked clean and "by the book" on
  inspection, but where small execution details (MC4 connectors resting on the aluminium frame, DC
  cables fixed with metal clips) create micro-environments (condensation, capillary effects,
  differential thermal expansion) that cause slow cumulative degradation invisible to SCADA. He
  quantifies it: a 100 MWp plant losing 0.5-2.0% long-term yield works out to roughly EUR 0.6 to 2.4
  million in value leakage from year 10 to year 30. His stated conclusion: execution quality is not
  a site topic, it's a portfolio and valuation topic. Closes with engagement questions asking how
  others handle these details in practice. Verified by direct curl fetch of the full post body via
  the JSON-LD articleBody field; og:title confirms the author as Andreas Bach; datePublished
  2025-12-13T10:50:09.124Z (decoded from the activity ID, exact match), so about nine months old.
  730 reactions, 227 comments at time of fetch. Checked against observed/replies/ and
  queue/reply-candidates/: no existing draft on renewable energy asset performance, PV plants, or
  this author; Andreas Bach is new to the repo.
book_themes:
  - bad news is data
  - all projects are swamps
stance: reframe
risk: low
notes: >
  Selected because Bach's own conclusion, that execution quality is a portfolio topic, is already
  sophisticated, but frames the problem as one of visibility (nobody was looking closely enough).
  Mark's reframe argues it isn't a visibility problem, it's a horizon-mismatch problem: the person
  who could fix a resting connector cheaply and the person who eventually absorbs the value leakage
  twenty years later will never be in the same conversation, because no single reporting period
  spans installation to failure. This adds a structural mechanism (accountability horizon) rather
  than restating "look closer," and connects the figures the author already supplied to bad news is
  data by arguing the data arrives, just decades late and addressed to nobody in particular. All
  figures (100 MWp, EUR 60/MWh, the EUR 0.6-2.4 million range) are the author's; nothing of Mark's
  own to verify. Adjacent to but distinct from prior asset-performance and cost-visibility
  selections (Kamesh Kanth's BOQ flatness argument, 2026-09-04); that post is about an instrument
  designed not to show consequence in the moment, this one is about consequence arriving after the
  people who could act on it have moved on, so the two should read as related but not duplicate if
  posted in the same period.
---

The site manager wasn't wrong. SCADA won't be either. That's the actual problem, not a footnote to it.

You're describing a EUR 2.4 million loss with no single moment anyone could be blamed for causing. The clip that touches the frame gets installed by someone whose job ends at handover. The revenue it quietly costs lands on a balance sheet twenty years later, read by someone who has never seen the plant and couldn't trace a euro of it back to a connector. Nobody lied and nobody was negligent. The reporting period simply doesn't span the failure.

That's not an execution quality problem, or not only one. It's an accountability horizon problem: the person who could fix this cheaply and the person who eventually pays for not fixing it are never going to be in the same room, let alone the same conversation. Bad news is data, but only if it arrives while someone is still listening and still on the hook for it. This data arrives decades late, addressed to nobody.

Your instinct to zoom in was right. The industry's instinct to sign off on "by the book" isn't stupidity. It's the absence of anyone whose bonus depends on year twenty.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
