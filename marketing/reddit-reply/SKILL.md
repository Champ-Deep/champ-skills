---
name: reddit-reply
description: "Draft and vet Reddit comments that read as a practitioner rather than a vendor. Use for any Reddit reply, r/Coldemailing daily engagement, or whenever a reply could touch a Champions Group product."
---

# Reddit Reply

Reddit is the one channel where the LinkedIn register actively costs you. This skill exists to stop a founder who owns companies in the space from writing comments that read like a vendor wandered in. It is deliberately restrictive. The gates are the product.

The governing idea: **credibility is spent, not earned, by mentioning your own company.** Every mention draws down a balance built by comments that mentioned nothing. This skill tracks that balance and refuses to overdraw it.

---

## Phase 0: Recon (blocking, never skip)

Do not draft a single word before all four checks pass.

1. **Read the subreddit rules.** Open the sidebar and read them verbatim. Cache them to `Atlas/Social Triage/Reddit/Subreddit Rules Cache.md` with the date. Re-read if the cache is over 30 days old. Many subs ban self-promotion and vendor recommendations outright, including disclosed ones. If the rules ban it, disclosure does not rescue it. Mode C is off for that sub, permanently, and you say so rather than looking for a workaround.
2. **Check the account's standing in that sub.** Read `Atlas/Social Triage/Reddit/Reddit Engagement Ledger.md`. A comment mentioning a company you own, from an account with no history in the sub, is astroturf no matter how well written.
3. **Check the post is worth answering.** Older than 7 days is a necro, skip it. Already has a good top comment saying your point, skip it or reply to that comment instead of the OP. Under ~5 upvotes and 2 hours old, it may not survive; deprioritise.
4. **Check for the only-he-knows-this angle.** Score the post 0 to 3 on whether Deep has first-hand operating knowledge the thread does not already contain. Score 0 or 1 means do not reply. Generic best-practice restated in a friendly voice is filler, and filler from an account that later mentions a product is exactly the pattern people call out.

---

## The ratio gate

Read the ledger. Enforce it mechanically.

| Gate | Rule |
|---|---|
| First mention in a sub | 10 Mode A comments in that sub first |
| Subsequent mentions | 8 Mode A comments since the last one |
| Frequency ceiling | Never two Mode C comments in one calendar week, across all of Reddit |
| Counting | Only comments verified visible in a logged-out window count |

If the gate is not met, say so plainly and draft Mode A instead. Do not negotiate with yourself about whether this particular post is a special case. It never is.

---

## The three modes

**Mode A: pure value.** Default. Target ~90% of all comments. Zero mention of anything Deep owns, no disclosure needed because there is nothing to disclose. Just the answer.

**Mode B: disclosed expertise.** Discloses the vantage point without naming or linking anything. "I run a B2B data company, so I see this from the ugly side" tells the reader why to weight your answer and costs you nothing. No product name, no link, no company name. This is the highest mode most comments should ever reach.

**Mode C: disclosed mention.** All of the following must be true, and if any one fails, drop to Mode B:

- The sub's rules permit it.
- The ratio gate is met.
- OP explicitly asked for tool or vendor recommendations.
- The thing you own is honestly among the best two or three answers to the question actually asked.
- You can name at least two competitors and say plainly where they beat you.

Mode C format, in order: disclosure first, before the mention, never in a footnote. One sentence naming the thing. At least one thing it is bad at. Named alternatives with honest reasons to prefer them. No link unless OP asked for one.

---

## Conflict map (Champions Group)

The risk is not uniform across properties and subs. Judge by how the mention reads to a hostile reader.

| Property | r/Coldemailing | Elsewhere |
|---|---|---|
| Lake B2B, SPAN, Ampliz | **Mode C banned.** A list vendor recommending buying lists is the worst available read, and this sub is openly hostile to data vendors. Mode B at most, and even then say "a B2B data company" not the name. | Mode C possible in data or ops subs once the gate is met |
| Champmail, Lake Stream, Champ IQ | Mode C possible once the gate is met, but the tool must genuinely fit OP's question | Same |
| Champions Group, Accelerator, InfraTech, Ranch, Club | Irrelevant here, do not mention | Only where actually on topic |

The honest read on r/Coldemailing: Deep's real edge there is running actual sending infrastructure and seeing data quality at source. Domain warmup, SPF/DKIM/DMARC, what a burned domain looks like, why a list decays, what a vendor's "verified" actually means. That expertise is rare in the sub and buys enormous credibility, and it buys the most when nothing is being sold. The pitch is the thing that would waste it.

---

## Voice

Deep's default register is executive and LinkedIn-shaped. On Reddit that register is the tell. Correct for it deliberately.

**Strip:**

- Em-dashes. Standing hard rule, and separately one of the strongest AI tells on Reddit right now.
- Bold, headers, and bullet lists, unless the answer genuinely is a numbered sequence of steps.
- "Great question", "Hope this helps", "Happy to chat", "feel free to reach out".
- Tricolons and parallel structure. Three-part rhythm reads as copywriting.
- Uniform sentence length. Marketing prose is metronomic; people are not.
- TL;DR under 200 words.
- Any tidy problem to solution arc, especially one that lands on something you own.

**Add:**

- Contractions everywhere. Lowercase sentence starts are fine.
- Sentence length variance. Four words next to twenty-five.
- Specific numbers with the caveat attached in the same breath. "~14% reply rate, but warm-ish list and a tiny team, so grain of salt."
- At least one thing that did not work, ideally something that cost time or money.
- A named competitor or alternative you would honestly pick over yours in some scenario. This is the single strongest anti-shill signal available, and it is free because it is true.
- Willingness to say the unpopular thing or disagree with the thread.

**Length:** most good Reddit comments are 60 to 180 words. If the draft runs past 250, the answer is probably three answers and you should pick one.

---

## The shill self-check

Run on every draft. Any failure means rewrite, not ship.

1. **Deletion test.** Cut every reference to anything Deep owns. Does the comment still stand as a good answer? If a hole is left, it was an ad with an answer wrapped around it.
2. **Stranger test.** If a stranger posted this, would you assume they had a stake? If yes, the disclosure is doing too little or the enthusiasm too much.
3. **Enthusiasm audit.** Does any praise outrun its evidence? Adjectives without numbers behind them are the tell.
4. **Straw man audit.** Are the named alternatives all conspicuously worse? Real competitors have real advantages. Name one.
5. **Failure count.** At least one concrete thing that went wrong, with detail. Zero means rewrite.
6. **Register check.** Read it aloud. Does it sound like a comment or like a post? Comments are messier.
7. **Answer-the-question check.** Does it answer what OP asked, or what you wanted to talk about?
8. **Hostile-reply rehearsal.** Write the meanest plausible reply to your draft. If "lol found the vendor" lands cleanly, rewrite. If the meanest available reply is a substantive disagreement, ship it.

---

## Post and verify

Removals on Reddit are silent. Automod, new-account filters, and shadowbans all leave the comment looking fine to you and invisible to everyone else.

1. Post.
2. Load the thread in a logged-out or private window and confirm the comment renders.
3. Log the row in the ledger with the verification result. Unverified comments do not count toward the ratio.
4. If it was removed, do not repost. Find out which rule caught it and record that in the rules cache.

Check back once at roughly 24 hours. A reply asking a follow-up question is worth more than any number of upvotes, and leaving it unanswered wastes the comment.

---

## Daily triage integration

When invoked from `daily-social-triage` Phase 3, the run is **draft only**. Never post, upvote, or DM automatically. The LinkedIn auto-comment grant does not extend to Reddit and should not be assumed to. Write drafts into the day's triage note with direct post links for Deep to paste himself.

Judge the channel by comments that survived and drew a real reply. Not by drafts produced, not by upvotes, and never by mentions placed.

---

## Escalate to Deep, do not auto-draft

- Anyone naming a Champions Group property, positively or negatively.
- Any thread about a live deal, pricing, or a named person on the team.
- Any accusation of shilling on a past comment. That gets a human reply or none.
- Any request to DM. Reddit DMs from a founder account read as sales, always.

## Final gate: no AI slop (mandatory before delivery)

Everything this skill produces that a person will read (client, prospect, vendor, partner, public, or the sales team) passes a no-AI-slop check before it is delivered. Load the `no-ai-slop` skill in Gate mode and run its Eval on the final copy. If that skill cannot be loaded, apply this minimum:

- Zero em dashes and en dashes anywhere, including headings, titles, subject lines, and date ranges. Use periods, commas, colons, parentheses, or restructure.
- Cut binary contrasts ("It's not X, it's Y", "Not because X. Because Y."), throat-clearing openers ("Here's the thing"), faux-insight setups ("What nobody tells you"), colon reveals ("The best part: it learns"), dramatic fragments ("That's it."), rhetorical setups, fake-profound kickers, and recap endings.
- Cut puffery and weasel attribution ("a testament to", "pivotal moment", "experts agree", "studies show"). Name the source or drop the claim. Never invent a source, stat, or quote.
- Banned words: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, game changer, tapestry, realm, beacon, multifaceted, meticulous, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.
- Portability test: a sentence that could move unchanged to another company is filler. Replace it with a name, number, date, or mechanism, or cut it.
- Repeat the right word instead of cycling synonyms. Active voice, human subjects, direct verbs. No decorative bold or emoji headings.
- This gate governs style only. It never overrides this skill's factual, brand, or client-safety rules (vendor firewall, entity separation, verified numbers).