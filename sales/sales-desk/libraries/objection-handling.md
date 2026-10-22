# Objection Handling Library

Twelve common B2B objections, each with an acknowledge, reframe and question, for use live on a call or when drafting a reply.

## Give Claude
- The objection as the prospect said it, with as much context as you have
- Optional: deal stage, who said it, and what you had just shown them
- Optional: your own wording preference (blunt, warm, formal)

## Claude does
1. Match the pasted objection to the closest one in the bank below and output its three-part response.
2. Adjust the wording to the words they used, keeping the order: acknowledge, reframe, question.
3. If nothing matches, say so and give a generic acknowledge and question pair instead of forcing a match.

## Output
Response: acknowledge (one line), reframe (one to two lines), question (one open line). Bank below:
**1. "You are too expensive."**
Acknowledge: Fair to check, and price should be judged against what it returns.
Reframe: Most teams compare the sticker price against nothing rather than against the cost of the problem staying.
Question: What is the current approach costing you today?
**2. "We are already working with someone on this."**
Acknowledge: Good, that means the problem matters enough to solve.
Reframe: Most teams keep a first vendor and add a second where the first does not reach, rather than rip anything out.
Question: Where does your current setup stop short?
**3. "Now is not the right time."**
Acknowledge: Timing matters, and forcing a bad window helps nobody.
Reframe: The cost of waiting usually lands before the next good window opens, which is worth checking now.
Question: What would have to be true for this to move up the list?
**4. "I need to talk to my boss / the team."**
Acknowledge: Sure, decisions like this are rarely made alone.
Reframe: The conversation goes better with your read on what they will ask, so we can answer it before you ask.
Question: What do you think their first question will be?
**5. "We tried something like this and it failed."**
Acknowledge: That is useful information, and it is worth understanding what went wrong.
Reframe: A past failure usually points at fit or rollout, not at the idea itself, so the failure details decide this.
Question: What specifically failed last time?
**6. "Send me some information first."**
Acknowledge: Happy to, and it is more useful if I know what to send.
Reframe: One page aimed at your situation beats a generic deck you have to skim.
Question: What do you most want to know before we talk?
**7. "We can build this ourselves."**
Acknowledge: You have the people for it, which is a real option.
Reframe: Building the first version is the cheap part; running and updating it is where the cost lands.
Question: What would your team build first, and who maintains it after?
**8. "How do I know this will work for us?"**
Acknowledge: You should not take that on faith.
Reframe: The honest answer comes from a small test on your own data, not from a promise here.
Question: What would a believable test look like to you?
**9. "We have no budget this year."**
Acknowledge: Budgets are real constraints, not objections to argue with.
Reframe: The question is whether this saves or earns enough to be funded from somewhere, or waits for the next cycle.
Question: When does next year's planning start, and who owns that number?
**10. "You do not understand our industry."**
Acknowledge: Fair, I should not pretend otherwise.
Reframe: What transfers is the process problem; what I need from you is where your industry bends the rules.
Question: Where does your industry make this different from the general case?
**11. "We are too busy to implement anything right now."**
Acknowledge: Busy teams have no slack for new projects, and that is a fair concern.
Reframe: The right rollout starts by replacing the heaviest manual step, so it gives time back in week one.
Question: Which part of the process eats the most hours today?
**12. "I got a cheaper quote elsewhere."**
Acknowledge: Worth knowing, and cheaper is a legitimate priority if the scope matches.
Reframe: Compare what each quote actually includes before the number, since gaps usually hide in the scope.
Question: What is included in their quote that I should compare line by line?

## Rules
- Acknowledge comes first and must be real; never open by arguing, and keep the question open, one line, answerable without a presentation.
- No statistics, benchmarks or claims of superiority in any reframe.
- Never disparage a competitor by name in a response; use their words back, not jargon they did not use.
- If the objection is really a stalling line, say so instead of playing along.
