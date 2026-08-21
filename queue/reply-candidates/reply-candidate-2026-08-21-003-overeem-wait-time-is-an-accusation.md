---
date: 2026-08-21
status: candidate
author: Mark Stringer
platform: LinkedIn
reply_to: Barry Overeem
post_url: https://www.linkedin.com/feed/update/urn:li:activity:7263454508121313280/
post_summary: >
  Introduces a technique the author calls the "Dependency Spider" for finding bottlenecks. Central
  premise in his terms: "It is hard for a team to ship fast when it has to wait on other
  departments, teams, or suppliers to do something they depend on." The technique is three steps.
  First, map dependencies visually, placing your team at the centre and drawing the teams you
  depend on around it like spider legs, tracking individual requests on sticky notes. Second,
  measure wait times, recording how many days each fulfilled request took and calculating an
  average wait per sprint. Third, discuss and improve, using the sprint review and the
  retrospective to identify actions that reduce the impact of dependencies, improve collaboration
  with the teams depended on, and enlist stakeholder support. The post closes on reflection
  questions about reducing dependencies and delivering value faster.
  Verified by direct fetch of the canonical feed/update URL, which returned the post body,
  engagement counts and the premise line above as an exact quotation. The three steps came back
  summarised rather than verbatim, so treat their wording as paraphrase. LinkedIn shows "1 year
  ago"; activity ID 7263454508121313280 decodes to 2024-11-16, which makes this the oldest post
  selected in recent runs and is the main argument against it. 284 reactions, 30 comments. The
  visible comment thread contains a terminology objection from Jens Poser about whether the team
  depicted is a genuine Scrum Team, which is a different argument from this one and leaves the
  ground clear.
  Deduplication: "Overeem" appears nowhere in observed/replies/ or in the 262 files in
  queue/reply-candidates/, and the activity ID appears in neither directory. New author, new post.
book_themes:
  - bad news is data
  - all projects are swamps
stance: structural observation
risk: low
notes: >
  Selected because the technique is sound and the failure mode is in the third step, which is where
  almost every version of this exercise dies. Steps one and two produce a number that survives an
  argument in a way an anecdote does not. Step three then routes that number into the sprint review
  and the retrospective, two rooms containing nobody with authority over the team being measured.
  The mechanism the reply adds is the audience problem. Wait time is bad news about somebody who is
  not in the room, which makes it simultaneously the most useful number the team will produce and
  the most dangerous one, because it reads as an accusation and gets treated as one. The predictable
  end state is the exercise being shut down as finger pointing a few sprints in, which looks like a
  failure of the technique and is actually a failure of routing.
  The corrective is specific and actionable rather than a general complaint: the number has to reach
  the one person whose budget covers both sides of the dependency, because that person can act on
  eleven days and a retrospective cannot. This extends "bad news is data" with the condition the
  phrase usually leaves implicit, that data only counts once it lands in front of somebody who can
  spend money on it.
  Two things for Mark to weigh before posting. First, the post is from November 2024, so this is a
  reply into a cold thread and should be judged on whether the argument is worth having rather than
  on expected engagement. Second, the "eleven days" in the reply is deliberately a hypothetical
  illustration and not a claim about the author's data. If that reads as a real figure it should be
  softened. No first person anecdote and no claims about the author's organisation.
---

The spider drawing is good and the wait times are better, because a number survives an argument that an anecdote does not.

But look at where step three sends it. You establish that the team you depend on takes eleven days on average, and then you carry that into your sprint review and your retrospective. Everybody in those rooms already knew. Nobody in those rooms can do anything about it.

Wait time is bad news about somebody who is not present. That makes it the most useful number your team will produce and the most dangerous one, because it reads as an accusation and it gets received as one. A grievance log with a chart on it.

Which is usually how the exercise dies. Three sprints in, somebody senior calls it finger pointing, and the sticky notes come down.

It only does any work when it reaches the one person whose budget covers both sides of the dependency. That person can act on eleven days. Your retro can spend a year discussing it.

So keep the measuring and change the audience. Bad news is data, but it only becomes data once it is in front of somebody who can spend money on it. Before that it is just a complaint that has learned to count.

---

Of course I'm replying to these posts to market my book - https://link.springer.com/book/10.1007/979-8-8688-2205-6
