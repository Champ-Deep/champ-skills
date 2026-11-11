---
name: meta-ads-low-budget
description: Use when planning or reviewing Meta (Facebook and Instagram) paid lead generation on a small budget: offer, opt-in, angle tests, account structure, scaling, and phone follow-up.
---

# Meta ads on a low budget

A planning and review playbook for small-budget Meta lead generation. Written for LakeB2B and Champions Yacht Club Goa, usable for any brand. It sits upstream of `nostalgia-angle-ads` (concepts) and `span-ad-creative` (render pipeline): this skill decides the offer, the funnel, the test and the readout; those two make the pictures.

## Source and trust

The six tactics come from a video summary Deep pasted on 11 Nov 2026 (timestamps are the summary's). I did not watch the video and the creator's figures (lead cost, product price, the 80/20 split) are claims, not results we have seen. Everything marked PROPOSED below is our reconstruction. Numbers in this skill that come from the vault are cited to their file; numbers from the video are labelled.

## Step 0: fit gate (do this before any spend)

| Check | Pass condition | If it fails |
|---|---|---|
| Is Meta the right channel for this buyer? | The buyer is a person who browses Instagram or Facebook and decides on their own, or a small decision-maker group reachable by broad targeting | Use LinkedIn or search. LakeB2B parked Meta ("off for B2B") in the Q4 2026 plan (`Efforts/Active/Q4 Campaign Theme/Q4 Campaign Theme.md`). Re-opening it is a decision for Deep, as a capped test, not a default |
| Is there a high-value offer? | One product or package where one closed sale pays for many leads | Fix the offer first |
| Is there a measured next step? | Leads land in the CRM or WhatsApp inbox with source and campaign, and a person owns calling them | Fix tracking first (see Readout) |
| Is the legal and consent path ready? | Opt-in text, privacy policy link, and a lawful way to call or message (India: DPDP Act consent and TRAI calling rules; from general knowledge, not checked here, confirm with legal) | No spend until consent text exists |

## The six tactics

### 1. One specific, urgent offer with a hero mechanism (summary 0:50 to 2:03)

Pick a high-value product (the summary says $2,500 and up) and give it a mechanism that makes it different from the competitor set, not a discount. Write the offer in one sentence: who it is for, what they get, why it is only this way here, why now. Urgency must be real (capacity, a date, a cap), never invented.

### 2. Sell the report, not the call (2:07 to 5:11)

Send traffic to an opt-in page for a useful free guide, not a booking page. Leads come cheaper (the summary says $10 to $25 each; unverified) and the list becomes an outbound calling list. The guide must be genuinely useful and contain only facts we can defend (`defensible-data-counts`: no buyer-visible number we cannot trace).

### 3. Test angles, not formats (5:26 to 8:30)

Mine the customer's own words (the video calls this the Halo strategy: Reddit threads, Amazon-style reviews) to find pains and desires. Choose two distinct angles. Run each in static images, one in a "breaking news" look and one in a "raw, native" look, so the test reads angle, not polish. Copy and picture are two things; change one at a time.

### 4. Broad targeting, simple structure (10:16 to 11:16)

No interest stacking. Broad audience, one campaign, one ad set per angle, each with its own ad-set budget so every angle gets spend and a clean read.

### 5. Use AI to read the data, then scale (11:28 to 14:24)

Export the ad data, have a model summarise winners and losers and suggest tests, then a person decides. Scale winners by moving 80 percent of budget into a campaign-budget-optimised (CBO) campaign and keep 20 percent for new tests. The split is the creator's; treat 80/20 as a starting point to review after two weekly readouts.

### 6. Phone the lead inside 60 seconds (17:48 to 18:32)

Call fast, ask why they opted in and what they were hoping for, and write down the exact words. Those words feed the next angle, the next headline and the offer. Calls are research as much as sales.

## Build order (the checklist to run)

1. Fit gate passes. Offer sentence written and approved by the brand owner.
2. Angle research: 20 to 30 verbatim quotes from Reddit, reviews and sales calls, each with its source link. Cluster into pains and desires. Pick two angles that differ in the buyer's belief, not in wording.
3. Opt-in page and the guide: one page, one field set (name, phone or email as the follow-up needs), consent line, thank-you page with the turnaround. No page, no spend.
4. Creative: two angles by two looks is four ads at most for the first round (PROPOSED). Static, brand-compliant, no unverified claim, no counts. Load the brand skill, then `nostalgia-angle-ads` rules 6 to 8 for the image.
5. Account: broad audience, one campaign, one ad set per angle, ad-set budgets.
6. Tracking: UTM on every ad (source meta, campaign, angle, look), CRM Lead Source set at form submit, thank-you page event. The CRM is the source of truth (Q4 note: GA showed 282 and the CRM 198 for September, an 84 lead gap).
7. Phone: named caller, 60 second target, a one-page call script with the five questions below, call notes into the CRM.
8. Readout after a fixed window (see below), then scale or stop by a rule written before launch.

Five call questions: What made you sign up today? What have you tried so far? What almost stopped you? What would make this a clear yes? Who else decides?

## Readout rules (PROPOSED, set the numbers with the brand owner before launch)

- Judge on cost per sales-accepted lead and per closed deal, not cost per lead. A cheap lead nobody can reach is a loss.
- Do not call a winner on fewer than about 30 to 50 leads per ad set or less than 7 days (a common rule of thumb, not from the video; tighten with real data).
- Write the stop rule first: total test cap, the cost per accepted lead that ends a test, the review date.
- Keep one variable per round. If both angle and look changed, the readout says "combined", not "angle".
- Record every call's top two phrases in the register; the next round's angles must cite at least one of them.

## Relation to the Q4 2026 LakeB2B and SPAN test

That test held the pain point and offer fixed and varied the look (a nostalgia world, two arms). This skill says the next round should vary the angle with the look held fixed, so together they tell you what to say and how to show it. Ask Megha and Abhishek for the LinkedIn readout before designing round two; it has not been seen.

## Brand applications

Details, drafted angles, funnel and test plan: `references/lakeb2b-and-goa-applications.md`.

## Guardrails

- No spend is approved by this skill. Every plan ends in a stop rule and a decision for Deep.
- No claim in an ad that is not confirmed in writing by the brand owner (counts, turnaround, safety, fleet ownership, awards).
- No competitor names in our ad copy or opt-in pages. Competitor reviews are research only.
- Opt-in and calling consent are required before any outreach; stage legal review, do not assume.
- A model reads data and suggests; it never launches, pauses or scales a campaign.

## Not verified

The video itself. Cost per lead and sale figures. The 80/20 rule. Meta policy limits for each of our categories (check Meta's advertising standards before launch). Current Meta account state for either brand.
