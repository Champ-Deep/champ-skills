# Job-Change Agent

Finds contacts who changed jobs inside your ICP and drafts a first touch for the 90-day new-in-role window.

## Give Claude
- The person's name, old company, new company, new title and the date you learned of the move, pasted
- Optional: your prior relationship: calls, emails, what you last discussed
- Optional: your ICP and what you sell, in two lines
- Optional: other contacts in the same format, to batch the run
- Optional: the date to measure the window against (default: today)

## Claude does
1. Confirm the window: days since the move date, and whether it falls inside 90 days; flag anything outside.
2. Build the situation summary: new role, what someone in that role typically owns in the first quarter, phrased as a hypothesis.
3. Pick the angle from their situation: rebuilding a team, inheriting a tool stack, proving early wins. Mark each as hypothesis to test.
4. Draft the first touch under 100 words: one line of congrats, the angle, one question about their new mandate.
5. Draft a second variant that leans on your prior relationship, if history was pasted.
6. List what to avoid: putting down their old employer, assuming budget, assuming they remember you.
7. Give the follow-up question for their reply, the one that confirms or kills the hypothesis.
8. For a batch, sort the list inside-window first, then soonest to cross 90 days.

## Output
- Window line: move date, days elapsed, inside or outside 90 days, status.
- Situation summary: three lines, each labelled hypothesis.
- Two message drafts: new-contact version, prior-relationship version.
- Avoid list, one line each.
- The hypothesis-testing question to use on their reply.
- Batch view if several contacts were pasted: name, days elapsed, window, draft status.

## Rules
- Never assume why they moved, what their budget is, or that they remember you.
- The angle stays a hypothesis until they confirm it.
- Inside 90 days only. Outside gets a different play, not this one.
- Congrats gets one sentence, then straight to relevance. No flattery.
- No message mentions the old employer in a negative way.
- Dates come from the pasted input; with no date, mark the window unknown.
