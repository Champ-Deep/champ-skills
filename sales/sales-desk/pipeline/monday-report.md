# Monday Report

Turns a week of call breakdowns into a pipeline report a sales lead can read in one minute.

## Give Claude
- The week's call breakdowns, pasted one after another, each labelled with account and date
- Optional: your stage definitions, one line each
- Optional: last week's report, so movement can be compared
- Optional: the reporting period dates
- Optional: deals that slipped or died, so they are counted honestly

## Claude does
1. Group calls by account and stage, counting: calls held, deals touched, advanced, stalled, created, lost.
2. Build the deal table with one row per account: stage, last call date, next step, date, owner.
3. Pull the top three risks across the week, each with the account and the question that closes it.
4. List next steps falling in the coming week, sorted by date, owner where given.
5. Compare with last week if pasted: what advanced, what slipped, what died, what is new.
6. Flag data gaps: calls with no next step, no date or no owner, listed by account.
7. Keep the report to what was pasted. Nothing estimated, nothing carried over unless it is in the input.

## Output
- Snapshot line: calls held, deals touched, advanced, stalled, created, lost.
- Deal table: `account | stage | last call date | next step | next date | owner`.
- Top three risks, each with account and closing question.
- This week's dated next steps, in date order.
- Week-over-week lines, only if last week's report was pasted.
- Data gaps list: account, field missing.

## Rules
- Count only what was pasted. Never estimate or extrapolate totals.
- Use the stage names given; if none were given, describe stages plainly instead of inventing labels.
- Every deal needs a next step or an explicit "no next step set".
- Comparison lines appear only when last week's report is in the input.
- No rankings of reps, no performance commentary, no forecasts.
- Keep it to one minute of reading: table first, prose last.
