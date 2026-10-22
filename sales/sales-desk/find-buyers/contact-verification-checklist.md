# Contact Verification Checklist

Confirms a person is still in role and reachable, with no guessed email addresses, before you spend a touch on them.

## Give Claude
- The person's name, current title and company as you have them
- Optional: the email address or profile link you found, and where you found it
- Optional: pasted LinkedIn profile text, company team page text, or a recent email signature
- Optional: the source and date of your original data, so stale sources can be identified
- Optional: the email pattern quoted exactly as it appeared in a pasted signature

## Claude does
1. List the checks needed: name matches, title matches public sources, current dates on the profile, one reachable channel.
2. For each check, give the exact search string using the name, title and company you pasted.
3. Turn the checks into a pass, fail or unknown checklist with one line of evidence each.
4. For email: only if you pasted the company's pattern (for example first.last at the domain), list pattern-based candidates, each marked UNCONFIRMED.
5. Weigh the evidence: a profile showing current title and dates passes; a directory with no date does not.
6. Output a verdict: VERIFIED, UNVERIFIED, or STALE, with the one detail that decided it.
7. If stale, give the updated search string and what to correct in your records.
8. If two sources disagree, output STALE and show both rather than picking one.
9. Repeat the same checks for anyone else pasted in the run, keeping one verdict per person.

## Output
- Checklist table: `check | search string | evidence | pass / fail / unknown`.
- Verdict line: VERIFIED / UNVERIFIED / STALE plus a one-line reason.
- If stale: what changed, the corrected title or company, the new search string.
- Candidate emails only as a labelled list: address, pattern used, UNCONFIRMED.
- If the verdict is unverified: the one check most likely to settle it, with its search string.

## Rules
- Never generate an email address from a guess. Pattern candidates only when you pasted the pattern, always marked unconfirmed.
- Never output VERIFIED without a dated source in the input showing current role.
- Do not treat an old directory listing as proof of anything current.
- No dates in the input means the verdict cannot be VERIFIED.
- Do not include personal contact details beyond what you pasted.
- One verdict per person; never soften STALE into VERIFIED.
