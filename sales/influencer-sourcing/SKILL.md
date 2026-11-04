---
name: influencer-sourcing
description: Use when shortlisting influencers for a paid collaboration.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [influencers, sponsorship, shortlist, research, b2b-marketing]
    related_skills: [signal-scout, competitive-research-verification, deep-research]
---

# Influencer sourcing

Produce a shortlist of creators a brand can actually pay for, each pick justified against the brief. The output is a vault shortlist file plus a decision card if an earlier draft already exists. Full detail on sources and fit signals lives in `references/rate-and-fit-sources.md`; stats gathering lives in `scripts/creator_stats.py`.

## When to Use

- Deep asks for influencer, creator, sponsor, or tech-creator options for a brand offer or campaign.
- He challenges a prior shortlist ("better options", "why these picks", "does this fit").
- Any paid collaboration needs candidates vetted against an audience and a budget.

## Always-on rules

- **Fit over fame.** Judge a creator by whether their audience buys what the client sells, not by subscriber count. A 200K developer channel loses to a 5K GTM-engineer channel when the product is B2B contact data. Check the buying behaviour of the audience, not just the topic match.
- **Every number is sourced.** Subscriber counts, typical views, and price bands each carry their source. Price bands from estimators (Fuse, MyCoCreator) are estimates, never quotes; label them as such in the deliverable. Never invent a rate.
- **Screen for conflicts before recommending.** Check the creator's current role (X and LinkedIn headline) before offering money. An employee of a competitor, an aggregator, or an adjacent vendor is a drop regardless of content fit.
- **Check sponsorship availability, not just interest.** Newsletter and network sponsorships often sell out for the year or sit at four-figure tiers with no public price; verify before listing.
- **Answer the reasoning question fully.** When Deep asks why a prior pick was chosen, give a per-pick verdict table (why chosen, fits the new brief, keep/drop) before presenting the new list. He is auditing judgment, not asking for a fresh list.
- **Say what was not checked** (real quotes, audience geography, business emails) in a final line. A shortlist without a limits line reads as more certain than the research is.

## Procedure

1. **Pin the brief**: who the client is, what they sell, the audience that buys it, budget total, format (video / social / newsletter), and what positioning the client needs. If a budget is given, do the arithmetic early: a pick whose band exceeds the whole budget is reference material, not a recommendation.
2. **Harvest candidates**: run YouTube searches for the niche's natural queries (e.g. "X review", "best X alternatives", "X tutorial") and group results by channel. Vendor channels (the product's own and its competitors') are not influencers; skip them. Keep individual educators who answer buyer questions.
3. **Measure each candidate** with `scripts/creator_stats.py <handle> [...]`: subscriber count from the channel page, median views across the last 15 uploads from the YouTube RSS feed, and Fuse price bands when a creator slug exists. Median views beats subscriber count because estimator pricing is subscriber-based and misprices channels whose videos outdraw their subs.
4. **Verify conflicts**: fetch the creator's X and LinkedIn headline. Record current employer, agency affiliation, and whether they already take affiliate deals in the same category.
5. **Verify availability**: look for a sponsorship/media page or sold-out notice for newsletters and networks.
6. **Score against the brief**: keep the top 3-5 with a one-line fit reason each; explicitly drop the prior list's picks that fail the new brief with the reason.
7. **Recommend a budget split**: combinations whose combined bands fit the stated total, best views per dollar first, plus a single-pick fallback.
8. **Write the shortlist file** in the effort's folder: verdict table on prior picks, new shortlist table (subscribers, typical views, est. price, fit), recommendation, not-checked line. Then surface any stale unsent draft as a decision card naming the exact draft.

## Pitfalls

- **Do not report a search snippet as a fact about a person.** A search-engine preview of a profile can be years stale; fetch the profile page and read the live headline before using someone's employer as evidence.
- **Do not quote a client-side price calculator through web_extract.** Dynamic rate pages return navigation shell text with no numbers; use the estimator's static creator page (getfused.io/creators/<slug>), which carries the bands in HTML.
- **Do not hand a broad "find influencers" brief back as famous newsletters.** Big names are sold out or four-figure; a small budget targets niche-prominent creators, and saying so up front prevents a second round.
- **Do not treat an affiliate-heavy creator as neutral.** A creator whose recent video argues the product category is free will not sell a paid provider; flag the risk in the pick rather than hiding it.
- **Do not leave an unsent draft recommending dropped picks.** When a prior draft to a stakeholder now lists rejected options, end with a decision card naming that exact draft (replace body / delete / brief another way).
