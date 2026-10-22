# Lookalike Expansion

Turns three of your best customers into a trait profile and 20 similar accounts, for a rep who needs targets but has no ICP document.

## Give Claude
- Three best customers: name, industry, size band, what they bought, and why they chose you if you know it
- Optional: a list of accounts you have already worked, so they get excluded
- Optional: hard constraints: geography, no SMB, must use a named tool, must not be a customer of a competitor
- Optional: a longer source list of candidate companies to filter, pasted as names
- Optional: the market or region to draw candidates from

## Claude does
1. Extract shared traits: traits common to all three customers, traits common to two, traits unique to one.
2. Drop the unique traits and write a five-line lookalike profile from what remains, each line checkable from public information.
3. Note where the three customers differ, since that is where the profile is weakest.
4. Pull 20 candidates that fit the profile: from your pasted source list if you gave one, otherwise from general market knowledge, each marked as needing verification.
5. Exclude anything from your worked-accounts list, even when it fits perfectly.
6. Score each candidate against the five traits, showing matched, unmatched or unknown per trait.
7. Rank by matches, then write one line per candidate on why it looks alike.
8. Mark confidence: high (four or five traits confirmed from input), medium (three), low (assumed).

## Output
- Trait analysis: common to all three, common to two, dropped as unique.
- Five-line lookalike profile.
- Candidate table: `rank | company | traits matched | confidence | why it looks alike`, 20 rows.
- Excluded list: company, reason (already worked, failed a trait, out of region).
- Weakest-trait note: which trait the profile rests on thinnest evidence.

## Rules
- Never claim a company matches a trait you have no input for; mark the trait unknown.
- Candidates must fit the profile, not just be well-known names in the industry.
- Do not count an account from your worked list.
- Confidence comes from the input only. Candidates from general knowledge start at low.
- If the three customers share no real traits, say so and ask for a fourth customer instead of padding.
- Exactly 20 candidates, or fewer with the reason stated.
