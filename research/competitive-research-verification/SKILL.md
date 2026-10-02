---
name: competitive-research-verification
description: "Verify a competitor or dependency before adopting it."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Competitive, Vendor, DueDiligence, Adoption, Evaluation]
    category: research
    related_skills: [grounded-citations, competitor-news-monitor]
---

# Competitive research and verification

Evaluate a competitor, vendor, open-source dependency, or SaaS tool before adopting it or
planning a build against it, and produce a decision the user can act on.

**Trigger on:** 'help me evaluate X', 'should we use X instead of Y', 'what do people complain
about X', 'is X actually better than Y', 'look at reviews of X', 'we are locked into Y, find
us an alternative', 'plan a competing version of X', 'can we self-host X', 'compare these
three tools'.

This is a **decision** deliverable, not a survey. A survey that ends in "here are six options"
has failed unless the user asked for options. End with a recommendation, the condition that
would reverse it, and the questions only they can answer.

## The core rule: claims are hypotheses until verified at the layer that decides them

Every finding that will change the plan gets verified by you, personally, at the layer where
it is true. Marketing copy is a claim. Docs are a claim. A child agent's summary is a claim.
Verify at the layer that settles it: the source for pricing, the repo for capabilities, a live
call for the API.

**Stars are not maturity.** Record `git log -1 --format="%H %ad"` and commit counts. A huge
star count with a stalled history is a polished demo, and adopting it means owning code you
cannot pace.

**Never let a schema, type, or model definition greenlight a capability.** Models, enums and
types routinely survive after the implementation is stripped, and they read as proof. Check
the application code exists (full-tree search for the feature's package directory), that it
is *registered* (imported by the composition root, not merely present), and that no orphaned
unit tests are all that remain. A model plus an orphaned test and zero implementation files
means the feature is gone.

**Check the vendor's own pages against each other.** The pricing table versus the homepage
versus the help centre for the same field: feature lists, limits, counts, prices.
Contradictions, unrendered stat counters, and placeholder testimonials on case-study pages
are stronger and cheaper findings than any review.

## Before you plan a build: check whether we already own it

When the ask implies building a replacement, **search our own repos and the vault before
proposing a new one.** List the project parent directory rather than searching the home
directory, which times out and skips protected folders:

```bash
ls -d /Users/deep/Apps\&Projects/*/           # local checkouts
gh api 'user/repos?per_page=100&affiliation=owner,organization_member&sort=pushed' \
  --jq '.[] | [.full_name, .pushed_at[0:10], (.private|tostring), ((.description//"")[0:60])] | @tsv'
```

Then read the candidate's build contract or spec before judging the gap. An effort folder
already named for the domain may hold a recent build with a solved availability engine, a
tested concurrency guard, and an adapter seam, in which case the plan is "extend this", not
"build this". Also check the vault for an existing effort on the topic; an adjacent effort
serving a different channel (outbound versus inbound, say) is a *separate* effort, and saying
so prevents a wrong merge later.

## Phase 1: own ground truth before delegating

Establish the baseline yourself before any fan-out. You need it to judge specialists against,
and you will be wrong in front of the user without it. Then dispatch one specialist per
independent area in a single call, giving each: the paths, what you already verified, the
specific questions, and a demand for real quoted evidence.

**Ask for the capability inventory AND the honest gap list in the same brief.** A specialist
asked only for capabilities reports intent; asked for gaps, it hunts for breakage. Tell them
to return findings in the response, not to disk.

**State the premise and ask for its refutation.** Children confirm embedded assumptions
rather than testing them. A brief saying "the community edition probably has no usable API"
tends to return confirming exactly that. Always instruct: report any finding that contradicts
the premise, prominently.

**Give an explicit honesty constraint.** Require separating verified quotes from inference
from category-level claims about other products, a confidence rating on corpus volume, and
plain statements of what could not be found. A fabricated quote is far worse than a short
answer.

## Phase 2: verify before it reaches the user

Child reports are self-reports and systematically under-rank. Re-verify every finding headed
for the top tier, one read each. Background delegations return a **truncated** summary and
save full text to a file: read the file rather than trusting the summary block.

**Re-verify vendor pricing, licence terms, and quota figures taken from a child's
paraphrase.** Plausible-sounding wrong numbers are worse than no numbers.

**Lead with the correction.** When verification changed your conclusion, that correction is
the headline, not a footnote. Say plainly what you added and what changed.

Two failure modes to expect in the target's code:

- **A degraded path scoring better than a healthy one.** Find the default used when a check
  is *unavailable*. An `undefined` score mapping to a maximum multiplier means judging failure
  rewards rows. Every "we could not check" branch must resolve to worst case.
- **A gate that is advisory but reads as enforcing.** Confirm the branch that would have
  skipped the work actually skips it.

## Phase 3: the rating and review trap

An aggregate rating is a claim about a corpus, and it is the claim most likely to be wrong.
Before repeating a directory's headline number, count what is behind it.

- **Rebrand trap:** a product renamed from a previous product keeps the old listing's reviews.
  Compare launch date to earliest review date; a review describing the old product's use case
  is a retained review.
- **Synthetic trap:** tell-tales are an all-maximum-score corpus where the floor never
  appears, review dates preceding the product, prose repeating verbatim under different
  names, an advertised count far above what the UI shows, and an API returning an empty array
  while the site's own FAQ admits the ratings are illustrative. Confirm via the API, the
  visible text, and the disclaimer. When all three agree it is manufactured, refuse the
  figure rather than caveating it.
- **Zero-corpus reframe:** when the authentic corpus is tiny, the finding is "there are no
  users to complain", followed by a separately labelled list of *inferred product risk*. Never
  let a vendor's self-description appear as reported user pain. Absence is citable evidence:
  a 0-rating listing, a 404 on Trustpilot, and `nbHits: 0` from a search API are three
  verified findings.

See `references/source-credibility.md` for the full credibility checklist.

## Phase 4: ecosystems and replacements

When hunting a replacement:

- **GitHub topics can be empty while returning HTTP 200.** Check `total_count` on the search
  API, not the page status; authoritative-sounding topic names are sometimes unpopulated.
- **A 404 on a remembered `owner/name` usually means a rename or transfer**, not that the
  project is gone. Search by description before concluding it does not exist.
- **Match the tool's domain model to the requirement,** not its feature list. A project whose
  native entities are providers-and-services has multi-person scheduling in its *schema*,
  while a larger project may have stripped it.
- **Licence gates a lot of this out.** AGPL forces source disclosure of a combined work over
  network use and usually rules out a closed hosted product. Plain GPL generally does not for
  hosted use but attaches on distribution. Flag the ambiguity, route it to counsel, do not
  resolve it in a plan.
- **A maintained image is part of maturity.** Check pull count and last push for both the old
  and new repo names. Zero pulls on the successor plus a stale last push on the predecessor
  means build-from-source and inherited maintenance duty.
- **The incumbent may have the better API,** and that is still a reason not to adopt it:
  writing into a vendor's API moves the routing and availability model into their
  infrastructure, trading one lock-in for a pricier one. Verify the "they are iframe-only"
  claim before repeating it, because it is often false.

## Output

Lead the chat reply with the finding that changes the decision most. No process replay.

Structure the deliverable so the user can act without re-reading:

1. **The goal in one line**, and **what we deliberately are not doing**, so scope cannot
   silently absorb the whole ask.
2. **What is verified broken**, with the layer of verification named for each claim.
3. **The finding that changes the plan** — usually that we already own part of this, or that
   a stated premise was wrong. Correct a wrong premise in the document itself, flagged as a
   correction, rather than leaving the false assumption standing.
4. **Recommended architecture**, with alternatives in a table and an explicit reversibility
   column so the user can see which choices are cheap to undo.
5. **Phasing**, each phase ending in something demonstrable, never starting the next before
   the previous is shown.
6. **What success looks like**, written so it can be falsified, including a **"it has failed
   if"** clause. A success definition without a failure condition is not a definition.
7. **Open decisions the user owns**, recommendation first, each marked reversible or not.
8. **Explicitly not decided**, so silence is not read as agreement.

If it goes in the user's vault, run the mechanical dash check before delivering and deliver
with `MEDIA:` plus an absolute path, never a bare path.

## Pitfalls

- **Do not let a line-count diff stand in for substance.** More lines across a shared file can
  be entirely your own feature work.
- **Do not report a foreign repo's self-declared status as fact.** "Experimental" or
  "pre-beta" tells you their posture, not their capability.
- **Do not adopt a tool because it is the topic of the week.** Check maturity, and separate the
  transferable idea from the product.
- **Do not build a duplicate.** Search our own repos and vault before proposing a new one.
- **Do not let a truncated delegation summary end your verification.** Read the saved file.
- **Do not rank by effort when the work is defects.** Severity first, effort second.
- **Do not produce a survey when the deliverable is a decision.**
- **Do not add another undated plan to a pile of undated plans.** That is not progress.