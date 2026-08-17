---
id: reply-scout-log-2026-08-17
type: agent_log
agent: reply_scout
status: draft
---

# Daily search query

Google: `site:linkedin.com/posts "project management"`

Full URL (past 24 hours): `https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d`

Status of that URL this run: still dead. It 302s to `consent.google.com` with `gl=GB&hl=en`,
and the consent page cannot be cleared by WebFetch. Unusable for the twenty-fourth consecutive run.

Engines actually used:

1. WebSearch on the bare brief query. Returned the same stale 2022 to 2023 glossary set it has
   returned for weeks, plus three Wikipedia articles. Zero selectable results. Logged below as
   rejections rather than silently dropped.
2. Brave, query 1: `site:linkedin.com/posts "you don't have a capacity problem" OR "the deadline
   was never the problem"`. Twenty results, the productive query of the run, source of two of the
   three selections.
3. Brave, query 2: `site:linkedin.com/posts "it wasn't a communication problem" OR "we didn't have
   a process problem" OR "the project didn't fail because"`. Twenty results, source of the third
   selection.

Brave did not rate limit this run. Two queries were enough, so the six to eight query budget was
never tested. Five post fetches spent, four of them productive.

Activity ID date decoding was run on every shortlisted result before any fetch was spent, using
`datetime.fromtimestamp((activity_id >> 22) / 1000)`. Fourteen dates decoded for free. All four
subsequently fetched posts matched their decoded date, which is now sixteen for sixteen across
three runs. This remains the highest value filter available and should stay the first step.

# Posts considered

## Selected

- **SELECTED** Trey Sheneman, "Want to know why your team misses deadlines" (2026-03-13, 10
  reactions, 2 comments). Makes a real causal claim and prescribes a specific method, so there is
  something to argue with. Freshest post reached this run and a new author.
- **SELECTED** Josh Singer, "Most People Don't Have a Deadline Problem. They Have a Communication
  Problem." (2025-11-20, 8 reactions, 4 comments). Clean falsifiable thesis that is half right, and
  the half that is wrong has practical consequences. New author.
- **SELECTED** Sridhar G S, "I resigned as CTO. No job lined up." (2025-12-31, 1,903 reactions, 143
  comments). Highest engagement post reached by a wide margin, strong argument, and its closing
  advice does not follow from its own diagnosis. New author, and outside project management proper.

## Rejected, WebSearch stale set

- **REJECTED** Sonal Sharma, "What Is Project Management?" (2022). Definition post, link bait, no claim.
- **REJECTED** Chat Engineer, "Project Management (The Basics)". Glossary content.
- **REJECTED** Project Management Information, "#projectmanagement #planning" (2023). Hashtag listicle.
- **REJECTED** Kory Kogon, "What Is Project Management? Everything You Need To Know" (2023). Explainer, nothing to counter.
- **REJECTED** Three Wikipedia articles returned as results. Not LinkedIn posts.

## Rejected, Brave query 1, deadlines and capacity

- **REJECTED** Dwight Braswell, "How to Handle Missed Deadlines Like a Leader" (2025-08-17). Leadership advice listicle, the only available reply is agreement.
- **REJECTED** Jordan Cutler, "Estimates are not deadlines" (2024-01-17). Author already in the queue, and estimation is saturated.
- **REJECTED** Gil Broza, "Next time you attach a deadline to some work, check your assumptions" (2023-10-17). Author already in the queue.
- **REJECTED** John Crickett, "Deadlines are rarely immovable" (2023-08-03). Author already in the queue.
- **REJECTED** Wes Kao, "Everything takes longer than you think" (2023-07-20). Good argument and a new author, but three years old and the point is already covered by planport-missed-deadlines-upstream.
- **REJECTED** Rian Doris, "Here's Why You Never Have Time" (2023-10-10). Time optimism bias, individual productivity framing rather than project structure.
- **REJECTED** Lucas da Costa, "Why deadlines are pointless" (2022-09-22). Arguable, but four years old and the thesis is already answered in the queue.
- **REJECTED** Hylton Bellinger, "I don't think it's deadlines that make things happen" (2023-09-03). Reflection without a mechanism to engage.
- **REJECTED** Cathy Bennett, "The Magic of the Imminent Deadline" (2023). Motivational productivity content.
- **REJECTED** Jenn Deal, "Artificial and arbitrary deadlines are inevitable" (2022-11-17). Coaching content, reply would be agreement.
- **REJECTED** Scott Smith, Duke Ellington deadline quote (2022). Quote card.
- **REJECTED** Jonathan Ewing, "Dear Strategists, Please respect the deadline" (2022). Complaint post, no argument.
- **REJECTED** Hugo Attal, "Make deadlines. Don't meet them" (2022). Personal productivity, not projects.
- **REJECTED** 48 Days, "Obstacles are often just delays" (2023). Dan Miller quote card.
- **REJECTED** Vedran Kuharic, "Your work deadline is meaningless" (2022). Stress advice, no structural claim.
- **REJECTED** Arthur K. Richards, "Data and Deadlines" (2023-03-01). Advocates over-communication, close to the Singer selection but weaker and older.
- **REJECTED** Harvard Business Review, "Why We Procrastinate When We Have Long Deadlines" (2020). Already in the queue as an author, and it is a syndicated article share.
- **REJECTED** Peter Lucas, "Time is the scarcest resource" (2023). Aphorism.

## Rejected, Brave query 2, communication and process

- **REJECTED** John Sills, "You don't have a people problem, you have a process problem" (2025-03-18). Strong post, but author already used in reply-candidate-2026-08-12-003-sills-who-the-process-is-actually-for.
- **REJECTED** John Cutler, "Process is always there" and "Our strategy is OK, our big problem is execution". Author already in the queue twice.
- **REJECTED** Matt Watson, two CTO posts. Author already in the queue.
- **REJECTED** Jason Knight, "Why can't the engineers just work harder?" Author already in the queue.
- **REJECTED** Joe Peppard, "Why Do Companies' IT Projects Fail So Often?" Author already in the queue.
- **REJECTED** Martina Amui, "70% of projects fail due to poor communication" (2025-01). Unsourced statistic post, and arguing with the number is not interesting.
- **REJECTED** George P., "Why Do Companies' IT Projects Fail So Often?" (2023). Reshare of the same article as Peppard, with percentages.
- **REJECTED** Uttam Pai, "Poor vs Wrong vs No Communication: Which is WORSE?" Engagement bait framed as a question.
- **REJECTED** Vachan Singh, "Project Delays: Few Contributing factors" (2025). List post.
- **REJECTED** Franck Blondel, "I sent laptops to 7 remote hires. 5 quit." (2025-03-18). Considered seriously and dropped: the causal story is thin and the remote onboarding frame pulls away from projects.
- **REJECTED** Ben Heselton, Duolingo company handbook (2025). Reshare of a handbook, promotional.
- **REJECTED** Alvin Foo, "90% of all management problems are caused by miscommunication" (2023). Quote card with a fabricated sounding statistic.
- **REJECTED** Adamantia Velonis, "We freed 13.8 hours per week" (2025-11). Legal tech vendor content.
- **REJECTED** Thinkgrid Labs, software project failure analysis (2022). Corporate promotional.
- **REJECTED** Project Performance International, tree swing analogy (2021). Reposted classic cartoon.
- **REJECTED** Jeff White, "I've made a lot of mistakes in my career" (2023). Career reflection, reply would be agreement.

# Replies drafted

- `queue/reply-candidates/reply-candidate-2026-08-17-001-sheneman-the-word-doing-the-work-is-period.md`
  Counterpoint. Concedes the 25 to 30 hours correction, then argues the method is addressed to
  someone who does not exist: "Period" names an authority to refuse work, and anyone holding it was
  never overcommitted in the first place. The commitment arrives at the planning meeting rather
  than being made there. Closes on predictability bought by committing to less than you can do,
  which reads identically to health from upstream. Themes: all projects are swamps, bad news is
  data. Risk low.
- `queue/reply-candidates/reply-candidate-2026-08-17-002-singer-early-is-not-about-respect.md`
  Reframe. Grants the thesis and attacks the reason: early updates work because they hand back a
  decision while the decision still exists, not because they demonstrate respect. Same sentence on
  day three and day forty transfers an option or a fact. Notes that "set deadlines with buffer"
  contradicts the communication thesis. Ends on a test: can the recipient now do something they
  could not do yesterday. Theme: bad news is data. Risk low.
- `queue/reply-candidates/reply-candidate-2026-08-17-003-sridhar-you-cannot-interview-for-this.md`
  Structural observation. Avoids the saturated authority argument entirely. Argues the three
  screening questions fail because interviews are rooms where both sides are selling, and the
  organisations that fail the test will answer warmly and sincerely. Then moves to "I stayed too
  long" and argues the missing thing was a threshold agreed in advance, not information. Themes:
  bad news is data, the project is a bet. Risk medium, see notes in the file.

# Notes

- Three selections against roughly forty posts considered. All three authors are new, which is a
  change from the last three runs where author deduplication was the dominant rejection reason. It
  still accounted for eight rejections here, but the deadline vein turned out to be less picked over
  than expected.
- The productive query shape was again a **negated premise**, consistent with 08-12 and 08-13.
  `"you don't have a capacity problem"` worked despite "capacity" being logged on 08-14 as a
  collision term. The correction is that capacity collides as a bare noun and behaves well inside a
  negated-premise phrase. Quoting the whole argumentative clause suppresses the collision.
- The unreached lead carried from 08-14, Jake Calabrese on capacity versus commitment, was the
  seed for query 1 and still did not resolve to a post URL. Josh Singer and Trey Sheneman came back
  in its place. Treat the lead as closed rather than pending.
- Two selections argue with the *reason* a piece of advice works rather than with the advice. That
  is a repeatable move against LinkedIn advice posts, which tend to have correct prescriptions
  attached to flattering explanations, and it avoids the trap of disagreeing with something the
  audience knows from experience is true.
- Duplicate risk needing a human eye: 003 and the 08-14 Rachitsky candidate both close on writing
  something down. The objects differ, a personal exit threshold versus a project bet, but they were
  drafted three days apart and should be read together before both go out.
- Bing was not probed this run. Two Brave queries produced enough material, and the probe is only
  worth spending when Brave is failing.
- Nothing was found inside the 24 hour window. Selected posts are five, eight and nine months old.
  That is the tooling limitation recorded in every log since 2026-07-23, not an editorial choice.
