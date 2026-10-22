# Fit Score

Scores an account 0 to 100 against weighted criteria you can edit, so ranking a list stays consistent instead of a gut call.

## Give Claude
- Your criteria and weights if you have them; otherwise start from defaults: company size 25, industry match 25, role match 20, tool fit 15, geography 10, timing signal 5
- The account details as text: size, industry, roles, tools, location, any recent news
- Optional: a second account to score in the same run
- Optional: your band thresholds (defaults: 70 plus pursue, 40 to 69 nurture, under 40 skip)
- Optional: a pasted list of accounts, to score the whole list at once

## Claude does
1. Confirm the weights total 100. If they do not, rebalance proportionally and show the change before scoring.
2. Score each criterion from 0 up to its weight, with a one-line reason tied to the pasted facts.
3. Mark criteria with no supporting fact as "no data" and exclude them from the total.
4. Sum to a total out of 100, plus a second total scaled to the weight of the criteria that had data.
5. Assign a band from your thresholds and state it in words (pursue, nurture, skip).
6. Output the criteria as an editable block, one criterion and weight per line, so you can change one and ask for a rescore.
7. If more than one account was pasted, score all of them under identical weights and sort by total.

## Output
- Score table: `criterion | weight | score | reason | data status`, one row per criterion.
- Totals line: raw score, score with no-data criteria excluded, band.
- Editable weights block, one `criterion = weight` per line.
- For a list: `rank | account | score | band | biggest data gap`.
- One line naming the criterion that moved the score most.
- Band flip note: which single criterion, if it changed, would move the account into the next band.

## Rules
- Never rebalance weights without showing the change first.
- Do not score a criterion on a fact that is not in the input: mark no data.
- Bands are a rule of thumb, adjustable by you, not an industry standard.
- Every criterion carries a weight. Zero weight only if you set it.
- Accounts in one run are always scored on the same weights.
- Do not turn the score into a win probability. It measures fit, not likelihood.
