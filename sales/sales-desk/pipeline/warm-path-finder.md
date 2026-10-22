# Warm Path Finder

Finds a non-cold way into an account from mutual connections, shared history, events and content engagement you paste in.

## Give Claude
- The account and the target person: name and title
- Your background in a few lines: past employers, schools, cities, groups, events you attend
- Optional: a pasted list of your connections with titles and companies
- Optional: their recent posts or comments, pasted, and any event attendee lists
- Optional: colleagues' backgrounds, if a teammate holds the warmer tie

## Claude does
1. Match their title and company against your connection list and list every overlap with tie strength (direct, one-hop, colleague of colleague).
2. Match their background against yours: shared employer, school, city, group or event, with dates where given.
3. Read the pasted posts for engagement signals: repeated topics, who they tag, what they argue for.
4. Rank all paths warmest first and give an opening line for each that names the actual overlap.
5. Mark weak or one-hop paths "needs an intro" and name who could make the intro, from the input only.
6. Pick one recommended path and draft a two-sentence opener for it.
7. List the topics they engage with, so later content choices are not random.
8. If nothing warm exists, say so plainly and give the best cold opener instead of forcing a path.

## Output
- Path table: `path type | the overlap | tie strength | opening line | status (direct / needs intro)`.
- Recommended path, plus a two-sentence draft opener you can send.
- Engagement signals: topic, evidence from their own post.
- Colleague-held ties if any: teammate, their overlap, why it is stronger than yours.
- If cold: one cold opener and the research you would do first.

## Rules
- Only use connections and history present in the input. Never invent a mutual connection.
- An intro is a request, not a fact: never write "X will intro me".
- A one-hop through a stranger is not warm; label it weak.
- No personal details beyond what you pasted.
- Recommend exactly one path even when several exist.
- Opening lines must name the real overlap; no vague "we have people in common".
