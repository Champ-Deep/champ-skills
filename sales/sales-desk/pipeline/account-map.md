# Account Map

Builds one page showing an account's people, buying committee, current vendors and timing, from pasted notes, emails and profiles.

## Give Claude
- Company name and what it does
- Every name and title you have, pasted from emails, call notes or profiles, with the source noted if you know it
- Optional: pasted call notes or email thread text mentioning other people, tools or deadlines
- Optional: what you sell and who you think signs
- Optional: any org chart or team page text you have found

## Claude does
1. Organise the names into reporting lines only where the input supports it, and label each inferred line "inferred".
2. Label each person's committee role: economic buyer, champion, technical evaluator, end user, blocker, or unknown.
3. List vendors and tools mentioned, each with the exact phrase it appeared in.
4. Extract timing: dates, deadlines, fiscal-year mentions, renewal language, anything that constrains the deal.
5. Pull open questions from what the notes do not answer, one line each, phrased so you can ask them on a call.
6. Flag contradictions between sources instead of picking a winner.
7. Keep the page short: more than 15 people means move the peripheral ones to an appendix line.

## Output
- People table: `name | title | committee role | reporting line (stated / inferred) | source`.
- Vendors and tools: tool, where mentioned, replaceable (yes / no / unknown).
- Timing list: date or event, what it means for the deal.
- Gaps to fill: numbered questions, each tied to the missing fact.
- One line on the weakest part of the map, so you know what not to trust yet.
- Confidence line: which parts of the map are stated facts and which are inferred, in one sentence.

## Rules
- Never invent reporting lines, titles, vendors or dates that are not in the input.
- Every inferred link must be labelled inferred.
- Do not add people who were not pasted in.
- Conflicts are shown side by side, never silently resolved.
- The map is one page: cut people with no bearing on the decision before adding detail.
- If the input has no names at all, output the questions that would get you names, not a guessed chart.
