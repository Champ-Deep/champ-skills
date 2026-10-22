# High-Intent Playbook

A five-day plan that works only accounts showing buying signals, with the day-by-day action and message angle for each day.

## Give Claude
- Accounts with their signals, pasted with dates and sources
- What you sell and the outcome, in two lines
- Optional: your existing sequence touch days, so these do not clash
- Optional: proof points you are allowed to cite (named customers, verified numbers)
- Optional: how old a signal may be and still count (default: 30 days, state it)

## Claude does
1. Rank signals by strength then recency: strongest and newest first, and drop anything older than the stated window with a note.
2. Assign each surviving account a slot in the five-day run, hottest first.
3. For each day, pick the action (call, email, LinkedIn note, shared content, break-up) and tie the angle to that account's own signal.
4. Write the day-one message per account, opening on the signal with its date, under 100 words.
5. For accounts beyond five, write one shared template with {{signal}} and {{date}} slots instead of individual messages.
6. List mid-run stop conditions: signal disproved, person changed role, opt-out, no engagement by day five.
7. Note which proof point each message may use, taken only from what you pasted.
8. Give the time budget: roughly how long each day's actions take.

## Output
- Ranked signal table: `account | signal | source | date | age | rank`.
- Five-day plan: `day | action | angle | time needed`.
- Day-one message per account (up to five), or one template with slots beyond that.
- Stop conditions list, one line each.
- Approved proof points, or a line saying none were given.

## Rules
- Only accounts with a pasted signal are in this playbook. No cold accounts padded in.
- Never invent, soften or exaggerate a signal. Quote it with its date.
- Messages must reference the real signal, not a vague line about growth.
- Five days only. No extra touches invented for volume.
- If no proof points were given, make no claims about results or customers.
- An out-of-window signal is dropped, not quietly aged into relevance.
