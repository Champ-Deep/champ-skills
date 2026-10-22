# Call Breakdown

Turns a pasted call transcript or rough notes into what they said, what it means, the next step, the risks and a CRM-ready summary.

## Give Claude
- The full transcript or your notes, pasted as text
- Optional: who was on the call and their titles
- Optional: what you sell and the stage you believe you are in
- Optional: what you committed to before the call, so new commitments stand out

## Claude does
1. Pull their direct statements, grouped by topic: pain, current state, process, budget, timing, decision process.
2. For each statement, write what it means for the deal in one line.
3. Extract commitments: who agreed to what, with their exact words where given.
4. List risks: unanswered questions, missing people, competitor mentions, timeline gaps, each with the question that would close it.
5. Note what was not discussed at all, since silence on budget or process is itself a risk.
6. Write a CRM-ready summary under 80 words: situation, pain, next step, no adjectives.
7. Write the next step as action, owner and date; if no date was set, write "date not set".
8. List the open questions you owe them, so the reply does not drop them.

## Output
- Their words: `topic | their quote or paraphrase | what it means`.
- Commitments: `owner | commitment | where it was said`.
- Risks: risk, closing question, severity (high / medium / low).
- CRM summary paragraph, 80 words maximum.
- Next step line: action, owner, date or "date not set".
- Open questions you owe them, one line each.

## Rules
- Quotes must come from the pasted text or be marked paraphrase. Never put words in their mouth.
- Do not invent names, dates, commitments or products that were not in the text.
- If no transcript was pasted, ask for it instead of summarising from memory.
- Risks include what was not said; state the gap plainly.
- The CRM summary stays under 80 words with no hype words such as great call or strong interest.
- Every risk gets a closing question, otherwise it is a complaint, not a risk.
