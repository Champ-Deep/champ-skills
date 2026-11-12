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

Produce a shortlist of creators a brand can actually pay for, each pick justified against the brief. The output is a vault shortlist file plus a decision card if an earlier draft already exists. Full detail on sources and fit signals lives in `references/rate-and-fit-sources.md`; stats gathering lives in `scripts/creator_stats.py`, which accepts `@handle`, `channel/UC...` and bare channel ids, so a `yt-dlp` search harvest can be fed straight in.

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
- **Name the platform you harvested.** A YouTube-only screen of B2B creators is a first pass, not a market view: many GTM and demand-gen educators publish on LinkedIn or a newsletter first and their YouTube numbers understate them. When only one platform was searched, say so in the limits line and offer the platform-agnostic screen as the next step rather than letting a thin list read as exhaustive.

## Procedure

1. **Pin the brief**: who the client is, what they sell, the audience that buys it, budget total, format (video / social / newsletter), and what positioning the client needs. If a budget is given, do the arithmetic early: a pick whose band exceeds the whole budget is reference material, not a recommendation.
2. **Harvest candidates**: search the buyer's actual questions, not only the product name ("how to do X without Y", "X tutorial", "best X alternatives"), because the creators who answer them are the ones whose audience is already in market. One command per query, printing channel plus median recent views so weak channels are visible before you spend a call on them:
   `yt-dlp --socket-timeout 20 --flat-playlist --playlist-end 12 --print '%(channel)s | %(channel_url)s | %(view_count)s | %(title)s' "ytsearch12:<query>"`
   Group by channel. Vendor channels (the product's own and its competitors') are not influencers; skip them, they are the competition for a paid data or tool offer. Keep individual educators who answer buyer questions.
3. **Measure each candidate** with `scripts/creator_stats.py <channel> [...]`: subscriber count from the channel page, median views across the last 15 uploads from the YouTube RSS feed, and Fuse price bands when a creator slug exists. Pass whatever the harvest printed: `@handle`, `channel/UC...`, and bare `UC...` are all accepted, so there is no separate step to turn a search result into a handle. Median views beats subscriber count because estimator pricing is subscriber-based and misprices channels whose videos outdraw their subs.
4. **Verify conflicts**: fetch the creator's X and LinkedIn headline. Record current employer, agency affiliation, and whether they already take affiliate deals in the same category. Sweep the title and description of every upload in the median sample (all 15, not the newest 5) with one fixed term list (the brief's named competitors plus scraping, data providers and discount codes such as Apollo, ZoomInfo, Lusha, Seamless, Cognism, scrap, GetLeads, Prospeo, Jev, Treg, Clay), print the hits per creator, and paste the command in the deliverable. A top-viewed tutorial for a competitor sits outside the newest 5 more often than inside it.
   Write the drop rule once (which hits drop, which are tool use only) and apply it to every creator; a keep whose hits match a sibling's drop reason is a contradiction the reviewer will return.
5. **Verify availability**: look for a sponsorship/media page or sold-out notice for newsletters and networks.
6. **Score against the brief**: keep the top 3-5 with a one-line fit reason each; explicitly drop the prior list's picks that fail the new brief with the reason.
7. **Recommend a budget split**: combinations whose combined bands fit the stated total, best views per dollar first, plus a single-pick fallback.
8. **Write the shortlist file** in the effort's folder: verdict table on prior picks, new shortlist table (subscribers, typical views, est. price, fit), recommendation, not-checked line. Then surface any stale unsent draft as a decision card naming the exact draft. A first-pass screen with no quotes and no conflict checks is written as a **screening list, not a recommendation**, and it carries the stop rule Deep must set before anyone is contacted: the cap, the cost per sales-accepted lead that ends it, and the review date.

## Pitfalls

- **Do not report a search snippet as a fact about a person.** A search-engine preview of a profile can be years stale; fetch the profile page and read the live headline before using someone's employer as evidence.
- **Do not quote a client-side price calculator through web_extract.** Dynamic rate pages return navigation shell text with no numbers; use the estimator's static creator page (getfused.io/creators/<slug>), which carries the bands in HTML.
- **Do not hand a broad "find influencers" brief back as famous newsletters.** Big names are sold out or four-figure; a small budget targets niche-prominent creators, and saying so up front prevents a second round.
- **Do not treat an affiliate-heavy creator as neutral.** A creator whose recent video argues the product category is free will not sell a paid provider; flag the risk in the pick rather than hiding it.
- **Name the contact route's kind.** Record what the URL actually holds (published email, contact form, speaking or podcast request form, calendar booking link) from the fetched page, not a generic "email page or contact form" note. A booking calendar is not a contact form, and a speaking-request form is not a sponsorship intake.
- **Do not leave an unsent draft recommending dropped picks.** When a prior draft to a stakeholder now lists rejected options, end with a decision card naming that exact draft (replace body / delete / brief another way).
