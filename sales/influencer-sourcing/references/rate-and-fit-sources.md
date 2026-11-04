# Rate sources and fit signals

## Where price bands come from

| Source | What it gives | How to read it |
|---|---|---|
| getfused.io/creators/<slug> | Dedicated video, integration mention, social post, bundle bands per YouTube creator | Static HTML, curl-able. Bands are estimates from subscriber count; channels whose videos outdraw their subs are underpriced, say so when using the band. |
| mycocreator.ai/tools/sponsorship-rates/<handle>/ | Rate calculator per handle | Client-side app; the page shell has no numbers without a rendered browser. Prefer Fuse. |
| Creator agencies (e.g. Sales Creator Collective) | Represented B2B/sales creators | Agency markup sits on top of creator rates; a small budget does not clear most agency minimums. |
| Newsletter sponsor pages | Tier pricing or sold-out status | Public price only sometimes; sold-out-for-the-year is common and disqualifies. |

Sanity math for B2B YouTube integrations: roughly $20 to $50 per 1,000 views
for niche B2B audiences. A $200 budget therefore buys around 4K to 10K views,
which sets the realistic tier: niche-prominent creators, not famous names.

## Fit signals that predict a good paid pick

- Their recent videos answer buyer questions about the exact category
  (X vs Y, how to use X, why X fails), not just adjacent strategy.
- They already review or integrate tools in the category (proves format
  familiarity and that a paid integration reads naturally).
- Audience buys the product: GTM engineers, demand gen, SDR leaders buy
  contact data; software engineers and SEO generalists mostly do not.

## Disqualifiers

- Current employee of the client's competitor or of an aggregator in the
  same category (role checked on a live profile, not a search snippet).
- Personal brand has moved to an agency/consulting selling motion that no
  longer matches the channel's audience.
- Recent content argues the category should be free or pushes an affiliate
  rival; a paid placement will read as a betrayal to their audience.
- Sponsorships sold out, agency-only, or unquoted four-figure tier when the
  budget is small.

## Deliverable shape Deep expects

1. Verdict table on any prior shortlist: pick, why it was chosen then,
   fits the new brief (yes/no + reason).
2. New shortlist table: rank, creator, subscribers, typical views, est.
   price band, one-line fit.
3. Recommended budget split that adds up inside the stated total, plus a
   one-pick fallback.
4. A "not checked" line (real quotes, audience geography, contact emails).
5. If an unsent draft already recommends dropped picks: a decision card
   naming the exact draft and the options.
