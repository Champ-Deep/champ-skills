# Interview question design

How to build the question set for a call where Deep is the interviewer. SKILL.md's Interview
Mode section carries the procedure; this file is the depth behind it.

## The shape of a good question

Every question row carries three parts:

| Part | What it is | Example |
|---|---|---|
| The ask | One sentence, plainly worded, no jargon a candidate could bluff through | "Your classifier scores 97 percent and still fails in production. How?" |
| The proves line | One sentence naming what a strong answer contains | "Proves class imbalance, leakage, wrong metric or drift." |
| The push | The single follow-up, used once per answer | "show me" / "why that choice" / "when did it break" |

No proves line and it is a vocabulary quiz. No push and it rewards rehearsal.

## The mix

Split every panel across two halves and mark the deciding questions beforehand.

**Technique, about two thirds.** Fundamentals where one surviving follow-up is the proof;
a live diagnosis over the team's own system rather than a textbook; a screen-shared walk
through code the candidate wrote, asked from the screen and never from memory. "Trained or
evaluated, not used" beats a library name every time.

**The person, about one third.** How they taught themselves something with no syllabus; a
time they were wrong about something technical and what they did next; the hardest bug they
fixed unaided; and what they would own in month one next to agents that write most of the
code. The last one is the team-mix question: it shows ambition scale, finish instinct, and
whether they understand the working rhythm (monthly cycles, a demo at the end of every
month).

## Live rounds: AI allowed and AI banned

Announce the rule in the question row, before the answer starts.

- One question **allows any AI tool** and grades how they drive it: do they steer, check and
catch the tool being wrong, or accept output on faith?
- One question **forbids AI** and must be answered live, showing unaided reasoning.

Mixed rules with no visible label are unfair and worthless as evidence, because a fast
answer becomes indistinguishable from a memorised one.

## What AI companies publish about their own hiring

Borrow from these when writing questions, and check the current version before quoting one
in a page, since hiring pages change:

| Source | What it gives you |
|---|---|
| `openai.com/interview-guide/` | Ramp speed over credentials, show how you reason, some rounds allow AI and some do not |
| `anthropic.com/candidate-ai-guidance` | AI for prep and refinement, none in a live round; the values round is where most candidates slip |
| Coverage of OpenAI's pilot mission interview (Fortune) | A round with no right answer, judged on judgment and tradeoffs |
| Published founder accounts of intern screening (India Today, Highperformr) | Application volume proves nothing: most applicants never attempt the task, and the attempts still fail on reasoning |
| DeepMind student researcher program material | Research roles screen for the ability to explain an experiment, not its buzzwords |

## Scoring and close

- Score in the two minutes after the call, while the answers are fresh. The pattern across
  the whole set outweighs any single reply.
- Three outcomes, decided the same night: advance, one timeboxed take-home, or a no. Both
  candidates get a decision; neither waits on the other's.
- Hand back the last two minutes for their questions and listen to what they ask.
- Report back with one line to the talent owner: yes, no, or take-home sent.

## Honest gaps

A missing resume, requisition or note goes on the page as a count ("0 of 2 resumes on hand")
plus an offer to fetch it. Never fill a gap with plausible-sounding candidate detail.