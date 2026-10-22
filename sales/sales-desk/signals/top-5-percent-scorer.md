# Top 5 Percent Scorer

Combines fit score and signal recency to rank an account list and surface the top 5 percent worth working today.

## Give Claude
- A list of accounts with fit score and most recent signal date, pasted as a table or CSV
- Optional: your own weights for fit versus recency (defaults stated below)
- Optional: the date to score against (default: today)
- Optional: signal strength labels if you have them (strong, medium, weak)

## Claude does
1. Confirm every row has a fit score and a signal date; list rows missing either as unrankable, never impute them.
2. Rank by fit (default weight 60) and signal recency (default weight 40), with recency decaying by age band as a rule of thumb: 0 to 7 days full, 8 to 30 days half, over 30 days zero.
3. Compute a combined score out of 100 per account and show the arithmetic for the first row as a worked example.
4. Take the top 5 percent by count, rounding up to a minimum of one account, and label them work today.
5. Bucket the rest: work this week (the next 20 percent), hold (everything else), unrankable (missing data).
6. Show weights and decay bands as an editable block, so you can change one and ask for a rescore.
7. Flag any account whose rank leans on a stale signal, with the signal date shown.
8. State the scoring date used for every age calculation.

## Output
- Ranking table: `rank | account | fit | signal date | age band | recency score | combined | bucket`.
- Top 5 percent block: count, the accounts, and the worked arithmetic for the top row.
- Unrankable list with the missing field per row.
- Editable block: `fit = 60`, `recency = 40`, decay bands listed, scoring date.
- Stale-signal flags: account, signal date, days old.
- Bucket counts: how many accounts sit in work today, work this week, hold and unrankable.

## Rules
- Never change weights or decay bands silently; show them and any edits you make.
- Rows without data are unrankable, never guessed or filled.
- Top 5 percent is a rule of thumb for prioritisation, not a claim about conversion.
- Ages are computed from the scoring date you were given, and that date appears in the output.
- No invented signal dates: only what was pasted.
- On lists under 20 rows, say the cut is too thin and offer the top one or two instead.
