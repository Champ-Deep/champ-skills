# ICP to Account List

Turns a plain-language ICP into a ranked list of target accounts with a why-fit line each, for a rep opening a territory or starting a campaign.

## Give Claude
- Your ICP in plain words: industry, company size, geography, tools they use, the role you sell to
- A list of company names to score, pasted one per line or as CSV
- Optional: two or three known-good customers, so Claude can see what real fit looks like
- Optional: disqualifiers, the company types you must never pursue
- Optional: facts you already have per company (size, tools, news), pasted next to the name
- Optional: your own criteria and weights, if you already have them

## Claude does
1. Rewrite the ICP into six testable criteria, each with a yes or no check and a weight, weights totalling 100.
2. Score every pasted company 0 to 100 against those criteria, showing passed, failed or no data per criterion.
3. Rank the companies by score, highest first, ties broken by how much data was available.
4. Write a one-line why-fit per account in words you could say out loud on a call.
5. Split the list into three buckets: pursue now (70 plus), worth a look (40 to 69), skip (under 40).
6. List the companies held back only by missing data, with the exact fact you need to look up.
7. Point out the criteria that produced the most partial credit, so you can tighten the ICP next pass.

## Output
- Criteria table with this header: `criterion | how to check | weight`, weights totalling 100.
- Account table with this header: `rank | company | score | why-fit | bucket | data gaps`.
- Lookup list: company, fact needed, typical place to find it.
- One short paragraph: what this ICP over-weights or under-weights based on this run.
- Example why-fit, one line: "Same 200-seat support team, same tooling, same trigger as the last deal we won."

## Rules
- Never invent company facts. Missing data is marked "no data" and never assumed.
- Only score companies that were pasted. Do not add names of your own.
- Scores are a rule of thumb for ranking, not researched valuations.
- One why-fit line per account, plain words, no adjectives you cannot support.
- If the pasted list has no facts at all, say the ranking will be weak and ask for one fact per company.
- Do not change the bucket thresholds without saying so.
