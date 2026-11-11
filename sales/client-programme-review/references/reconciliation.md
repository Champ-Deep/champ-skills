# Reconciliation: discrepancy classes and the question for each

The page is checked by people who hold their own records. Each class below has caught a real build. For each: how it shows up, how to find it, the question to put to the account owner, and the default when nobody answers.

## How to ask

- One batch (the question tool where there is one), at most five questions, recommended option first.
- Each question carries both values and both sources: "Their sheet says X (rows pasted today). Ours says Y (delivery record, dated). Which goes on the page?"
- Never ask the owner to trust a number. Ask them to pick between sources or to name who can confirm.
- Record the answer in the ledger entry's `by`, with the date.

## Classes

| Class | How it shows up | How to find it | Question | Default if unanswered |
|---|---|---|---|---|
| Count mismatch | Our total differs from the client's | Compare totals first | "Their count is X, ours is Y. Use theirs?" | `open` |
| Set mismatch | Same total, different members | Diff by company, never by total | "These N are on their sheet and not ours, these M the reverse. Which list is the record?" | `open` |
| Date drift | Same lead, different date | Diff the date column | None: correct ours to theirs, report the count of changes | Corrected, `matched` |
| Label drift | "Qualified" on the page, "delivered" in the contract; nurture leads counted as leads | Read the order and the client's column headers | "The order calls these X. Some were sent as Y. Which word goes in the headline?" | Use the client's word |
| Recap figure | A number that exists only in a call recap or chat summary | Trace every figure to a file; anything that ends at a recap is this class | "This is from a recap, not a pull. Confirm, soften, or cut?" | `open` |
| Joined records | Copy paired with a send, a report paired with a week | List every place two records are joined by position or order | "Did these go out in this order?" | `open`, or caveat plus an on-page selector |
| Detail only we hold | Qualification answers on each lead | Mark which columns come from our notes | None: caveat it on the page | `caveated` |
| Stale period | A one-week measurement read as the whole programme | Check the period on every report | None: state the period beside the number | `caveated` |
| Story contradicted | A lesson or closing line the client's own picks contradict | After any confirmed fact, recompute and reread every lesson | "Their picks point the other way. Rewrite the lesson, leave it, or hold?" | `open` |
| Standing hold | A memo or dispute that bars a figure from going to the client | Search the client's notes for holds before building | "This hold is still on file. Has it been lifted, and by whom?" | Leave the figure out |
| Internal only | Partner names, our costs, prices, internal disputes | Search the built page and the PDF text for each | None: remove | Removed |
| Panel honesty | Simulation reported on the audience size, not the scored count | Count scored reactions | None: state n of N | Stated |

## What the owner should hear back

After the round, one short block: what matched, what was corrected to the client's record and how many rows, what was softened and with which words, what was cut, what is still open and who can close it. The owner should be able to read it in the minute before a call and know where the soft spots are.
