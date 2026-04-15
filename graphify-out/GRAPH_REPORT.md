# Graph Report - .  (2026-04-12)

## Corpus Check
- Large corpus: 187 files · ~877,450 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 835 nodes · 1195 edges · 56 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Bad News is Data` - 31 edges
2. `You Can Write a Book (Edinburgh Fringe Show)` - 24 edges
3. `Delivering the Impossible (Book)` - 21 edges
4. `Delivering the Impossible — Agile Yorkshire Talk (Oct 2024)` - 19 edges
5. `Reading Candidates 2026-04-05 (001)` - 16 edges
6. `Delivering the Impossible (Book)` - 16 edges
7. `main()` - 15 edges
8. `Deliver the Possible Not the Fantasy` - 15 edges
9. `You Can Write a Book (show)` - 14 edges
10. `The Project Is a Bet` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Embedded PM vs Reporter Dichotomy` --semantically_similar_to--> `PM as Interface (multi-dimensional)`  [INFERRED] [semantically similar]
  queue/reply-candidates/reply-candidate-2026-04-10-003-mcintyre-pm-embedded-agile.md → observed/replies/2026-04-05-brown-ultimate-problem-pm.md
- `Post Candidate Photo — The Shitty First Draft (Mark Stringer in Park)` --conceptually_related_to--> `You Can Write a Book (Edinburgh Fringe Show)`  [INFERRED]
  queue/post-candidates/assets/post-candidate-2026-03-27-001-the-shitty-first-draft.jpg → observed/posts/2026-03-27-why-the-show-is-called-you-can-write-a-book.md
- `Screenshot — How to Build a Plan for March` --conceptually_related_to--> `Delivering the Impossible (Book)`  [INFERRED]
  source/Screenshot_20260316_144105.png → observed/posts/2026-02-26-on-not-doing-much.md
- `Book Message Pillars (6 Pillars)` --semantically_similar_to--> `Theme: Ways of Seeing`  [INFERRED] [semantically similar]
  desired-state/message-house.md → observed/themes/theme-coverage.md
- `Book Message Pillars (6 Pillars)` --semantically_similar_to--> `Theme: Idea vs Product`  [INFERRED] [semantically similar]
  desired-state/message-house.md → observed/themes/theme-coverage.md

## Hyperedges (group relationships)
- **Graph Build-Query-Edit Pipeline** — build_markdown_graph_script, ask_graph_script, edit_graph_script, graph_nodes_ndjson, graph_edges_ndjson [INFERRED 0.90]
- **Content Production Pipeline** — run_content_scout_script, queue_post_candidates_dir, linkedin_post_script, observed_posts_dir [INFERRED 0.85]
- **LinkedIn Auth and Post Pipeline** — linkedin_auth_script, linkedin_post_script, dotenv_file [EXTRACTED 0.95]
- **Bad News Handling: PM Replies Cluster** — reply_hemhauser_duct_tape, reply_langin_bad_guy, reply_benhamouda_10_skills, reply_cockburn_pm_role_agile, concept_bad_news_is_data, concept_pm_attitude_to_bad_news, concept_pm_honesty_bad_news, concept_saying_what_everyone_thinks [INFERRED 0.85]
- **Uncertainty Tolerance in PM: Replies Cluster** — reply_lockett_negative_capability, concept_negative_capability, concept_tolerance_of_uncertainty, concept_false_certainty, person_john_keats [INFERRED 0.85]
- **PM Role Definition: Replies Cluster** — reply_brown_ultimate_problem, reply_cockburn_pm_role_agile, reply_rajveer_scrum_mastery, concept_pm_as_interface, concept_cube_of_pm_positions, concept_context_dependent_pm, concept_pm_visibility [INFERRED 0.80]
- **Posts Promoting You Can Write a Book Show** — post_why_show_called_you_can_write, post_wip_london_shows, post_negative_capability, post_no_mirrors_only_prisms, post_you_are_not_paul_mccartney_fringe, post_grammar_for_people_who_arent, post_the_shitty_first_draft, show_you_can_write_a_book [INFERRED 0.90]
- **Writing Craft Concepts Referenced Across Posts** — concept_shitty_first_draft, concept_one_inch_window, concept_prisms_not_mirrors, concept_fooling_hypnotising_reader, ref_bird_by_bird, concept_writing_longhand [INFERRED 0.85]
- **Core Project Management Concepts in Book** — concept_agreed_activity, concept_trouble_salad, concept_bad_news_is_data, concept_projects_discover_value, concept_project_complexity_uncertainty, concept_biscuit_tin_vs_biscuit, book_delivering_the_impossible [INFERRED 0.90]
- **Delivering the Impossible Audience Segments** — audiences_book_primary, audiences_book_secondary, audiences_book_tertiary, entity_delivering_the_impossible [EXTRACTED 1.00]
- **You Can Write a Book Audience Segments** — audiences_show_primary, audiences_show_secondary, entity_you_can_write_a_book [EXTRACTED 1.00]
- **Book Message House Components** — messagehouse_book_core, messagehouse_book_pillars, messagehouse_book_phrases, entity_delivering_the_impossible [EXTRACTED 1.00]
- **Show Message House Components** — messagehouse_show_core, messagehouse_show_pillars, messagehouse_show_phrases, entity_you_can_write_a_book [EXTRACTED 1.00]
- **WIP Theatre Outreach Venues** — conv_theatre_outreach, conv_theatre_golden_goose, conv_theatre_hen_and_chickens, conv_theatre_cavendish_arms [EXTRACTED 1.00]
- **All Content Distribution Channels** — channelstrategy_linkedin, channelstrategy_youtube, channelstrategy_threads, channelstrategy_blog [EXTRACTED 1.00]
- **Content Governance Framework** — contentpolicy_allowed, contentpolicy_not_allowed, contentpolicy_required, cadence_weekly_target, cadence_content_mix, cadence_anti_repetition [EXTRACTED 1.00]
- **Edinburgh Fringe 2026 Logistics** — conv_edinburgh_accommodation, conv_theatre_outreach, entity_you_can_write_a_book [INFERRED 0.85]
- **Edinburgh Fringe 2026 Payment Actions** — action_20260409_001_pay_fringe_balance, action_20260409_002_pay_accommodation_balance, action_20260409_003_find_payment_dates [EXTRACTED 1.00]
- **Reading Candidates Generated 2026-04-05** — reading_candidate_20260405_001, reading_candidate_20260405_002, reading_candidate_20260405_003, reading_candidate_20260405_004 [EXTRACTED 1.00]
- **You Can Write a Book Fringe Show Production Actions** — action_20260328_001_book_fringe_venue, action_20260328_002_get_poster_printed, action_20260328_003_book_london_venues, entity_you_can_write_a_book_show [EXTRACTED 1.00]
- **Writing Craft Theme (grammar, shitty draft, negative capability, voice)** — postcandidate_shitty_first_draft, postcandidate_grammar_for_people, postcandidate_negative_capability, postcandidate_you_are_not_mccartney, postcandidate_mccartney_fringe [INFERRED 0.85]
- **Bad News / PM Role Cluster** — postcandidate_bad_news_is_data, postcandidate_pm_bad_news, concept_bad_news_is_data, concept_pm_no_skin_in_game, concept_trusted_advisor [INFERRED 0.85]
- **Fringe Show Promotion Cluster** — postcandidate_grammar_for_people, postcandidate_negative_capability, postcandidate_mccartney_fringe, postcandidate_shitty_first_draft, postcandidate_wip_london_shows, show_you_can_write_a_book [EXTRACTED 1.00]
- **Core Book Theme Cluster: Bad News + Project as Bet** — concept_bad_news_is_data, concept_project_is_a_bet, concept_deliver_possible_not_fantasy, concept_all_projects_are_swamps [INFERRED 0.90]
- **Scrum and AI Debate (West, Sutherland)** — reply_20260404_002_west_scrum_ai, reply_20260404_004_sutherland_scrum_ai, concept_scrum_master_ai_catalyst, concept_scrum_is_ai_protocol, concept_social_political_bottleneck, concept_transparency_inspection_adaptation [INFERRED 0.85]
- **Project Failure Root Cause Discussion** — reply_20260409_003_failure_symptoms, reply_20260410_001_mecham_plans, concept_structural_failure_causes, concept_plan_as_bet, concept_project_is_a_bet [INFERRED 0.85]
- **Reply Scout Daily Search and Draft Cycle** — replyscout_log_20260403, replyscout_log_20260404, replyscout_log_20260407, replyscout_log_20260408, replyscout_log_20260409, replyscout_log_20260410, replyscout_template [INFERRED 0.95]
- **Content Scout March 2026 Runs** — contentscout_20260307, contentscout_20260309, contentscout_20260311 [EXTRACTED 1.00]
- **Bad News Is Data Concept Cluster** — concept_bad_news_is_data, postcandidate_bad_news_data_20260307, postcandidate_bad_news_hear_20260309, postcandidate_bad_news_data_20260311, replycandidate_crickett_deadlines_20260408 [INFERRED 0.85]
- **Project Is a Bet Concept Cluster** — concept_project_is_a_bet, concept_deliver_possible_not_fantasy, concept_deadlines_encode_fantasy, concept_maximum_ignorance_commitment, replycandidate_project_bet_hildick_20260407, replycandidate_mecham_plans_20260410, replycandidate_failure_symptoms_20260409 [INFERRED 0.85]
- **Mark Stringer Voice Guidance System** — postvoicebrief_markstringer_voice, styleguide_voice_persona, styleguide_sentence_structure, styleguide_transitions, styleguide_linkedin_specific [EXTRACTED 1.00]
- **Software Escape Concept Cluster** — wegotta_software_escape, software_escape_transcript, wegotta_we_gotta_get_outta_here, keynote_delivering_the_impossible, software_escape_power_dynamic [INFERRED 0.85]
- **Biscuit Tin / Descriptions vs Reality Cluster** — biscuit_tin_concept, biscuit_tin_full_transcript, biscuit_explainer, biscuit_explainer_substrate, biscuit_tin_godels, biscuit_explainer_orgs [EXTRACTED 1.00]
- **Creativity Obstacles Cluster** — biscuit_tin_agreed_activity, biscuit_tin_perfectionism, shuddering_halt_shoulds, impro_agreed_activity, biscuit_tin_emotional_labor [INFERRED 0.80]
- **Some vs All / Asymmetrical Thinking Cluster** — some_vs_all_concept, some_vs_all_matte_blanco, some_vs_all_agile_asymmetry, some_vs_all_prioritisation, keynote_delivering_the_impossible [EXTRACTED 0.95]
- **Delivering the Impossible Core Metaphors** — metaphors_streams, metaphors_swamp, metaphors_pirate_ships, metaphors_bets, metaphors_flowers_vs_fruit [EXTRACTED 1.00]
- **Symmetrical vs Asymmetrical Thinking Cluster** — ch9_symmetrical_thinking, ch9_asymmetrical_thinking, ch10_bi_logic, ch10_agile_injects_asymmetry, ch12_conscious_asymmetry, talk_ay_ignacio_matte_blanco [EXTRACTED 1.00]
- **Projects as Bets and Risk Management Cluster** — ch6_project_as_bet, ch6_hiding_hand, ch6_pm_theater, ch7_nonsense_accumulator, ch7_theory_of_constraints, ch6_incremental_delivery, ch6_phone_the_banker, talk_ay_hirschman [EXTRACTED 1.00]
- **Agile Yorkshire Talk Themes** — talk_agile_yorkshire_2024, ch4_pirate_ship, ch4_agreed_activity, ch6_project_as_bet, ch3_escape, ch1_two_value_streams, ch8_commitment_consistency, ch9_symmetrical_thinking, ch7_nonsense_accumulator [EXTRACTED 1.00]
- **Core Show Concepts: Prisms, Tenth-of-an-Arse, Biscuit Tin, Nakedness** — prisms_not_mirrors_concept, tenth_of_an_arse_concept, biscuit_tin_concept, nakedness_of_sharing_concept [INFERRED 0.90]
- **Show Draft v1 Structural Elements** — show_writing_exercise, show_sharing_exercise, mcCartney_section, hypnotising_writing_concept, richard_toye_framework_in_show [EXTRACTED 1.00]
- **Authority Arc: Book + Publisher + Cover + Admission** — authority_arc_concept, book_contract_story, book_cover_story_file, delivering_the_impossible_book [EXTRACTED 1.00]
- **Grammar Section Components** — grammar_morning_coat_analogy, grammar_readability_goal, sex_ed_teacher_analogy, voice_as_reward_concept [EXTRACTED 1.00]
- **Lamott Source Concepts for Show** — shitty_first_draft_concept, lamott_hypnosis_quote, lamott_voice_concept, lamott_writing_daily_discipline [EXTRACTED 1.00]
- **Delivering the Impossible Poster Font Variants** — dti_poster_imfelldoublepica_regular, dti_poster_cinzel_bold, dti_poster_cinzel_extrabold, dti_poster_palatino, dti_poster_permanent_marker, dti_poster_insta [INFERRED 0.90]
- **Work in Progress Show Poster Variants** — wip_poster_insta_you_can_write_a_book, wip_poster_cavendish_you_can_write_a_book, wip_poster_a4_you_can_write_a_book, wip_poster_june16_you_can_write_a_book, wip_poster_june30_you_can_write_a_book, wip_cover_a5_you_can_write_a_book, wip_eventbrite_you_can_write_a_book [INFERRED 0.90]
- **Edinburgh Fringe 2026 Show Marketing Assets** — fringe_poster_you_can_write_a_book, fringe_eventbrite_you_can_write_a_book, event_fringe_2026, venue_greenside_riddles_court [EXTRACTED 1.00]
- **Book Proposal Core: Why This, Why Me, Why Now** — speakeasy_s1_why_this, speakeasy_s1_why_me, speakeasy_s1_why_now, speakeasy_s1_core_message_framework [EXTRACTED 1.00]
- **The Two Big Mistakes in Book Proposals** — speakeasy_s1_big_mistake_1, speakeasy_s1_big_mistake_2, speakeasy_s1_book_proposal_course [EXTRACTED 1.00]
- **Substance of the Proposal (Title, Description, Chapter Synopsis)** — speakeasy_s2_core_of_proposal, speakeasy_s2_identifying_market, speakeasy_s2_identifying_competition, speakeasy_s2_selling_yourself [EXTRACTED 1.00]
- **Two Value Streams in Software Development** — fullms_idea_value_stream, fullms_product_value_stream, fullms_two_value_streams_fight, fullms_project_in_desert [EXTRACTED 1.00]
- **Book's Collection of Ways of Seeing Projects** — fullms_value_stream, fullms_swamp_chapter, fullms_pirate_ship_chapter, fullms_project_is_bet, fullms_all_same_chapter, fullms_commitment_consistency [EXTRACTED 1.00]
- **Lean/Toyota to Software Development Lineage** — fullms_toyota_production_system, fullms_kanban_anderson, fullms_lean_software_poppendieck, fullms_just_in_time, fullms_value_stream [EXTRACTED 1.00]

## Communities

### Community 0 - "Writing Craft & Creative Voice"
Cohesion: 0.04
Nodes (72): Bird by Bird (Anne Lamott), Passive vs Active Aesthetics (Borges), Cargo-Culting Genius Habits, Being Comfortable with Not Knowing, Craft vs Natural Talent, False Certainty as PM Failure Mode, Flyering Me (Alternative Self When Promoting), Fooling or Hypnotising the Reader (+64 more)

### Community 1 - "PM Truth-Telling & Bad News"
Cohesion: 0.04
Nodes (69): Delivering the Impossible — Chapter: COMMIT, PM as Advocate for the Project, Agile Manifesto Values, AI Impact on Project Management, Bad News is Data, Deadlines Encode the Fantasy Not the Possible, Elephant in the Room (Speaking Hard Truths), Emperor's New Clothes (Hans Christian Andersen) (+61 more)

### Community 2 - "Symmetrical Thinking & Bi-Logic"
Cohesion: 0.04
Nodes (63): Agile as Injecting Asymmetry, Agile Manifesto, Bi-Logic (Symmetrical and Asymmetrical Coexist), Expert Bi-Logic, Bi-Logic: Combining Consistency and Asymmetry, Conscious Asymmetry (Step 3), Four-Step Journey to Conscious Principles, Shadow Beliefs (Harmful Project Metaphors) (+55 more)

### Community 3 - "Project Delivery Realism"
Cohesion: 0.04
Nodes (61): Author Bio Document (Stub), All Projects Are Swamps, Managing Constraints (Time/Cost/Scope), Context Determines Behaviour, Deadline as Expressed Bet, Deliver the Possible Not the Fantasy, Estimates Are Not Deadlines (LinkedIn Concept), Honesty About What Is Achievable (+53 more)

### Community 4 - "Show Source Material"
Cohesion: 0.09
Nodes (44): Authority Arc (show structure), Bandler: Always Hallucinate What's Really There, Bird by Bird — Anne Lamott (highlights), Biscuit Tin and the Show (source file), Book Contract Story (date format win), Book Cover Story (source file), Borges: Passive Aesthetic of Mirrors / Active of Prisms, Delivering the Impossible (book) (+36 more)

### Community 5 - "Audiences & Channel Strategy"
Cohesion: 0.08
Nodes (37): Book Primary Audience: Project/Delivery Managers, Book Secondary Audience: CTOs, Heads of Engineering, Book Tertiary Audience: Systems Thinking Readers, Branded Notebook as Audience Bridge, Show Primary Audience: Edinburgh Fringe General Audience, Show Secondary Audience: Creativity and Writing Interested, Anti-Repetition Rules, Content Mix Strategy (40/30/20/10) (+29 more)

### Community 6 - "Book Manuscript Core"
Cohesion: 0.07
Nodes (34): Agile / Iterative and Incremental Approaches, Alan Kay (Software Pioneer, OOP Inventor), All/Same/Forever/Exact Match Cognitive Biases Chapter, Apress / Springer (Publisher), Bad News is Data (Mark Stringer Signature Concept), Commitment and Consistency Principle (Project Management), Deliver the Possible Not the Fantasy, Delivering the Impossible (Book) (+26 more)

### Community 7 - "Content Scout Agent Code"
Cohesion: 0.14
Nodes (30): build_user_prompt(), call_anthropic(), call_model(), call_openai(), choose_context_docs(), collect_markdown_files(), compact_whitespace(), compute_score() (+22 more)

### Community 8 - "System & Graph Scripts"
Cohesion: 0.11
Nodes (30): agent-logs/content-scout/ — Content Scout Run Logs, ask_graph.py — Graph Question Answering Interface, build_markdown_graph.py — Markdown-to-Graph Builder, CLAUDE.md — Agent Instructions, Author Voice — Mark Stringer's signature phrases and reply style, Content Scout — AI-powered post candidate generator, Delivering the Impossible — book by Mark Stringer (Springer), Engagement Scoring — weighted metric for post performance (+22 more)

### Community 9 - "Published LinkedIn Posts"
Cohesion: 0.09
Nodes (30): Delivering the Impossible (Book), How Big Things Get Done (Flyvbjerg/Gardner), Agreed Activity, Auditions as the Real Job (Patrick Stewart), Biscuit Tin vs Biscuit Metaphor, Organisations Built for Descriptions Not Things, Physical Printed Copies of Book Arriving, Pirate Ship Improv Metaphor (+22 more)

### Community 10 - "Recommended Reading"
Cohesion: 0.12
Nodes (28): The Art of Possibility (Rosamund and Benjamin Zander), Artful Making (Robert Austin and Lee Devin), The Culture Code (Daniel Coyle), The Evolution of Cooperation (Robert Axelrod), Impro: Improvisation and the Theatre (Keith Johnstone), Lying (Sam Harris), Metaphors We Live By (Lakoff and Johnson), The Gift: Creativity and the Artist in the Modern World (Lewis Hyde) (+20 more)

### Community 11 - "Keynote & Impro Sources"
Cohesion: 0.1
Nodes (27): Agreed Activity (Johnstone), Impro: Improvisation and the Theatre (Johnstone notes), Spontaneity vs Suppression (Johnstone), Status as Something People Do (Johnstone), Delivering the Impossible Keynote (transcript), The Hiding Hand (Hirschman), Nonsense Accumulators (doomed projects), Deal With the Pirate Ship (metaphor) (+19 more)

### Community 12 - "Beckett & Biscuit Tin"
Cohesion: 0.1
Nodes (25): Fail Better (Beckett quote — Worstward Ho), Obligation to Express (Beckett quote), Samuel Beckett — Quotes, Biscuit Tin Explainer (2026-04-05 video), Organisations Set Up for Biscuit Tins Not Biscuits, Different Substrate (descriptions vs things), Agreed Activity (avoiding progress), Creative Capacity (sustainable power) (+17 more)

### Community 13 - "Graph Builder Code"
Cohesion: 0.17
Nodes (23): add_edge(), build_edges(), build_node(), collect_markdown_files(), derive_tags(), derive_title(), Edge, edge_id() (+15 more)

### Community 14 - "Nonfiction Book Proposal"
Cohesion: 0.09
Nodes (24): Big Mistake 1: Unclear Message / Not Stating What is New or Original, Big Mistake 2: Excess Modesty / Assuming Too Much Reader Knowledge, How to Write a Compelling Nonfiction Book Proposal (Speakeasy Course), Why This, Why Me, Why Now Framework, Modes of Persuasion: Ethos, Pathos, Logos, Four Nonfiction Book Types (Information, Advocacy, How-To, Experience), Book Proposal Purpose (Sharpen Message, Present Idea, Permission to Publish), What Publishers Want and Their Processes (+16 more)

### Community 15 - "Graph Editor Code"
Cohesion: 0.22
Nodes (21): backup_file(), cmd_add_edge(), cmd_add_list_value(), cmd_delete_node(), cmd_list_edges(), cmd_list_nodes(), cmd_remove_edge(), cmd_remove_list_value() (+13 more)

### Community 16 - "Reading Suggester Code"
Cohesion: 0.17
Nodes (20): ask_claude(), ask_model(), ask_openai(), build_prompt(), compute_delta(), is_material(), last_commit_touching_graph(), main() (+12 more)

### Community 17 - "Value Streams & Delivery Gap"
Cohesion: 0.12
Nodes (20): AI Accelerates Code Production Not Delivery, Delivery Gap, Flowers vs Fruit, Two Value Streams (Idea vs Product), Content Scout Log 2026-03-07, Content Scout Log 2026-03-09, Content Scout Log 2026-03-11, CircleCI (+12 more)

### Community 18 - "Graph Q&A Code"
Cohesion: 0.28
Nodes (15): answer_question(), ask_model(), edge_text(), expand_with_neighbors(), get_openai_client(), interactive_loop(), main(), node_text() (+7 more)

### Community 19 - "Theme Analytics Code"
Cohesion: 0.22
Nodes (13): engagement_score(), fmt_val(), load_posts(), main(), metaphor_aggregate(), parse_frontmatter(), print_table(), rank_by_theme() (+5 more)

### Community 20 - "PM Role Archetypes"
Cohesion: 0.19
Nodes (14): Fried Egg Agile (Mark Stringer, prior book), Context-Dependent PM Behaviour, Cube of PM Positions (complexity × team maturity × org maturity), Embedded PM vs Reporter Dichotomy, Fry Me an Egg (authentic vs mimicry in PM), Methodology Mimicry vs Genuine Responsiveness, No-Nonsense PM Book Concept (reader framing), PM as Interface (multi-dimensional) (+6 more)

### Community 21 - "LinkedIn Post Code"
Cohesion: 0.27
Nodes (11): create_observed_post(), extract_draft(), load_env(), main(), parse_frontmatter(), post_to_linkedin(), Return (frontmatter_dict, body) from a markdown file with --- frontmatter., Extract the text between # Draft and the next # heading. (+3 more)

### Community 22 - "Reply Scout Logs"
Cohesion: 0.17
Nodes (12): LinkedIn Activity ID Timestamp Estimation Method, LinkedIn/Google Search 403 Constraint, Reply Candidate: CircleCI Software Delivery 2026-04-04, Reply Candidate: Sprint Goals (Dalmijn) 2026-04-03, Reply Candidate: Scrum Training Wheels (Hammond) 2026-04-03, Reply Candidate: Sprint Spillover (Holub) 2026-04-03, Reply Candidate: OPM Federal PM Hiring 2026-04-04, Reply Candidate: Scrum as AI Protocol (Sutherland) 2026-04-04 (+4 more)

### Community 23 - "Empirical Process Chapters"
Cohesion: 0.18
Nodes (11): Bad News as Data, Data to Information to Knowledge to Wisdom to Action, Second-Circle Communication, SNAFU Principle, Trusted Advisors (PM and Product Owner), Driving a Car Metaphor for PM, Empirical Process, Mr. Two Story (Danger of Transparency) (+3 more)

### Community 24 - "LinkedIn Auth Code"
Cohesion: 0.36
Nodes (5): BaseHTTPRequestHandler, CallbackHandler, load_env(), main(), save_env()

### Community 25 - "Projects as Romance"
Cohesion: 0.29
Nodes (8): Opera About Project Management, Every Project is a Romance, Drama Behind Why a Project Exists, Writing Longhand (Natalie Goldberg Method), Art Gallery Cafe and an Opera About Project Management (Post), Every Project is a Romance (Post/Video), Every Love Story is a Ghost Story (David Foster Wallace), Writing Down the Bones (Natalie Goldberg)

### Community 26 - "Show Production Actions"
Cohesion: 0.36
Nodes (8): Action: Book Edinburgh Fringe Venue, Action: Get Poster Printed, Action: Book London Venues, Action: Pay Fringe Venue Balance, Action: Pay Accommodation Balance, Action: Find Payment Due Dates, Greenside @ Riddles Court, You Can Write a Book (Show)

### Community 27 - "System Improvements Backlog"
Cohesion: 0.29
Nodes (7): Action: Get LinkedIn Access, LinkedIn Auth Script (scripts/linkedin_auth.py), Automate LinkedIn Posting, Control Plane Improvements Backlog, Script to List Open Actions, Metrics Tracking for Observed Posts, Reply Scout Agent

### Community 28 - "Romance Transcript Concepts"
Cohesion: 0.53
Nodes (6): Burning Platforms / Sinking Ships (fear-based project motivation), Drama Behind the Project, Every Project is a Romance (transcript), Every Love Story is a Ghost Story (DFW quote), Money, Love, Revenge (project motivations), Project as Romance (concept)

### Community 29 - "Agile Feedback Loops"
Cohesion: 0.6
Nodes (5): Why Agile Transformations Fail, Sprint Ceremonies as Hypothesis Testing, Outer and Inner Feedback Loops in Agile, Jason Gorman (LinkedIn), Reply to Jason Gorman: Outer/Inner Agile Loops

### Community 30 - "Team Safety & Climate"
Cohesion: 0.6
Nodes (5): Surfacing Conflicts in Teams, Low-Temperature Planning Culture, Psychological Safety in Teams, Randi Andersen (LinkedIn), Reply to Randi Andersen: Low-Temperature Planning

### Community 31 - "Organisations vs Descriptions"
Cohesion: 0.5
Nodes (5): Biscuit Tin Metaphor (Description vs Working Thing), Organisations Manage Descriptions Not Working Things, Organisations Are Biscuit Tins (Post Candidate 2026-04-05-001), Rationale: Biscuit tin post locates delivery problem at organisational level not team level, Biscuit Tin Explainer Transcript 2026-04-05

### Community 32 - "Grammar & Accessibility"
Cohesion: 0.5
Nodes (5): Grammar as Accessibility (Not Class Gatekeeping), Grammar Helps Writers Find Holes in Their Argument, Grammar for People Who Aren't Twats (Post/Video), Eats, Shoots & Leaves, Have You Grammar? (Gyles Brandreth)

### Community 33 - "Self-Doubt & Momentum"
Cohesion: 0.83
Nodes (4): Competing With Yourself Instead of Cooperating, Getting Things Done by Ignoring Shoulds, Shuddering to a Halt (Self-Doubt Blocking Action), Shuddering to a Halt (Post/Video)

### Community 34 - "Projects as Drama"
Cohesion: 0.5
Nodes (4): Project Motives (Money, Love, Revenge, Tragedy, Compliance), Projects as Drama, David Foster Wallace, Every Project Is a Drama (Post Candidate 2026-03-29-001)

### Community 35 - "Inner Critic & Inertia"
Cohesion: 0.67
Nodes (4): Internal Competition (Self vs Self), Shuddering to a Halt (Self-Doubt Paralysis), Shuddering to a Halt (Post Candidate 2026-04-10), Shuddering to a Halt Transcript 2026-04-10

### Community 36 - "Tools & Mental Models"
Cohesion: 0.67
Nodes (3): The Project Lives in the Mind, Bonnie Biafore, Reply Candidate: Biafore Tools Mental Model (2026-04-10)

### Community 37 - "Content Policy"
Cohesion: 1.0
Nodes (2): Content Policy: Allowed Without Approval, Content Policy: Not Allowed Without Approval

### Community 38 - "News Hooks"
Cohesion: 1.0
Nodes (2): News Hooks README, News Hook Template

### Community 39 - "Flowers vs Fruit Metaphor"
Cohesion: 1.0
Nodes (2): Flowers vs Fruit Key Quote Theme, Flowers vs Fruit Metaphor

### Community 40 - "README"
Cohesion: 1.0
Nodes (1): README — MarketingControlPlane Overview

### Community 41 - "YouTube Channel"
Cohesion: 1.0
Nodes (1): Channel Strategy: YouTube

### Community 42 - "Threads Channel"
Cohesion: 1.0
Nodes (1): Channel Strategy: Threads

### Community 43 - "Blog Channel"
Cohesion: 1.0
Nodes (1): Channel Strategy: Blog/Newsletter

### Community 44 - "Experiments Template"
Cohesion: 1.0
Nodes (1): Experiment Template

### Community 45 - "Action Template"
Cohesion: 1.0
Nodes (1): Action Template

### Community 46 - "Meme Template"
Cohesion: 1.0
Nodes (1): Meme Description Template

### Community 47 - "Post Candidate Template"
Cohesion: 1.0
Nodes (1): Post Candidate Template

### Community 48 - "Reply Candidate Template"
Cohesion: 1.0
Nodes (1): Reply Candidate Template

### Community 49 - "Reply Candidate Index"
Cohesion: 1.0
Nodes (1): Reply Candidates README

### Community 50 - "Editor Log Template"
Cohesion: 1.0
Nodes (1): Editor Agent Log Template

### Community 51 - "Drift Report Template"
Cohesion: 1.0
Nodes (1): Drift Report Template

### Community 52 - "News Scout Template"
Cohesion: 1.0
Nodes (1): News Scout Log Template

### Community 53 - "Point of View Key Quote"
Cohesion: 1.0
Nodes (1): Point of View Key Quote Theme

### Community 54 - "Software Eating Everything"
Cohesion: 1.0
Nodes (1): Software Eating Everything

### Community 55 - "Why Publish a Book"
Cohesion: 1.0
Nodes (1): Reasons to Publish a Book

## Knowledge Gaps
- **276 isolated node(s):** `Very small frontmatter parser.     Supports:     ---     key: value     list_key`, `Return repo-relative markdown files under a prefix that changed recently.      P`, `Weighted engagement score. Returns None if no data at all.`, `Group posts by theme, sorted by chosen metric within each theme.`, `For each theme, aggregate metrics across all posts that use it.` (+271 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Content Policy`** (2 nodes): `Content Policy: Allowed Without Approval`, `Content Policy: Not Allowed Without Approval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `News Hooks`** (2 nodes): `News Hooks README`, `News Hook Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Flowers vs Fruit Metaphor`** (2 nodes): `Flowers vs Fruit Key Quote Theme`, `Flowers vs Fruit Metaphor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `README`** (1 nodes): `README — MarketingControlPlane Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `YouTube Channel`** (1 nodes): `Channel Strategy: YouTube`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Threads Channel`** (1 nodes): `Channel Strategy: Threads`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Blog Channel`** (1 nodes): `Channel Strategy: Blog/Newsletter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Experiments Template`** (1 nodes): `Experiment Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Action Template`** (1 nodes): `Action Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Meme Template`** (1 nodes): `Meme Description Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Post Candidate Template`** (1 nodes): `Post Candidate Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reply Candidate Template`** (1 nodes): `Reply Candidate Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reply Candidate Index`** (1 nodes): `Reply Candidates README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Editor Log Template`** (1 nodes): `Editor Agent Log Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Drift Report Template`** (1 nodes): `Drift Report Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `News Scout Template`** (1 nodes): `News Scout Log Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Point of View Key Quote`** (1 nodes): `Point of View Key Quote Theme`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Software Eating Everything`** (1 nodes): `Software Eating Everything`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Why Publish a Book`** (1 nodes): `Reasons to Publish a Book`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Bad News is Data` connect `PM Truth-Telling & Bad News` to `Writing Craft & Creative Voice`, `Published LinkedIn Posts`, `Project Delivery Realism`, `Value Streams & Delivery Gap`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Delivering the Impossible (Book)` connect `Published LinkedIn Posts` to `Writing Craft & Creative Voice`, `PM Truth-Telling & Bad News`, `Project Delivery Realism`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `You Can Write a Book (Edinburgh Fringe Show)` connect `Writing Craft & Creative Voice` to `Grammar & Accessibility`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Bad News is Data` (e.g. with `PM Attitude to Bad News` and `PM Honesty: Willingness to Say What's Actually Happening`) actually correct?**
  _`Bad News is Data` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `You Can Write a Book (Edinburgh Fringe Show)` (e.g. with `Joke Writing Exercises` and `Post Candidate Photo — The Shitty First Draft (Mark Stringer in Park)`) actually correct?**
  _`You Can Write a Book (Edinburgh Fringe Show)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Delivering the Impossible (Book)` (e.g. with `Unputdownable Book About Project Management` and `Invoice from Germany - Book Copies Arriving (Post)`) actually correct?**
  _`Delivering the Impossible (Book)` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Very small frontmatter parser.     Supports:     ---     key: value     list_key`, `Return repo-relative markdown files under a prefix that changed recently.      P`, `Weighted engagement score. Returns None if no data at all.` to the rest of the system?**
  _276 weakly-connected nodes found - possible documentation gaps or missing edges._