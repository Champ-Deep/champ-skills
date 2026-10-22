# Competitor Engagement Agent

Finds people engaging with a competitor's content, qualifies them, and drafts a first touch that never attacks the competitor.

## Give Claude
- The competitor name and pasted text of their recent posts, with dates
- Any engagement you can see, pasted: names, titles, comments or reactions
- What you offer and how you differ, in two lines, with no competitor bashing
- Optional: your ICP, to filter who counts as a fit
- Optional: how old a post may be and still count (default: 30 days)

## Claude does
1. List every person engaging with the competitor content, with their comment or reaction, the post date and the source.
2. Classify each engagement: evaluating (asking questions, comparing), defending (loyal), casual (light reaction).
3. Score fit against your ICP where the pasted data allows; mark no data otherwise.
4. Rank: evaluating plus fit first, then evaluating without fit data, then drop defenders with a note.
5. For the top ranked, draft a first touch that opens on their stated interest, not on the competitor, under 100 words.
6. Give the qualifying question for their reply: what they need that the current setup may not cover, asked neutrally.
7. List who to skip and why, so effort stays on the people actually evaluating.
8. Note the age of each signal, so stale engagement is not worked like fresh engagement.

## Output
- Engagement table: `person | title | comment | post date | type | fit | action`.
- Ranked shortlist, with a first-touch draft per person (up to five) and one shared template beyond that.
- Skip list with reasons.
- The qualifying question to ask once they reply.
- Age note per signal: post date, days old, inside or outside the window.

## Rules
- Never disparage the competitor in any draft. Interest in them is a buying signal, not an insult.
- Only people whose engagement was pasted appear; no guessed lurkers.
- Engagement older than the stated window is dropped, with a note.
- Do not invent titles, comments or reactions; mark unknown as unknown.
- One qualifying question per person, neutral in wording.
- Public posts only; never claim to have seen private activity or messages.
