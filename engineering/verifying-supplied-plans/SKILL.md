---
name: verifying-supplied-plans
description: "Use when someone hands you a plan or audit to build."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [review, verification, ground-truth, plan, audit, claims]
    related_skills: [site-growth-audit, site-interlink-audit, verification-gate-integrity]
---

# Verifying a supplied plan

Someone else's plan, audit, prototype or proposal is a **list of claims written from a
snapshot**, by someone who may not have measured. It is not a brief. Treating it as a brief
is how you spend a week fixing the wrong thing and report a defect that was never there.

The deliverable is a verdict: what holds, what is wrong, what was missed, what that does to
the priority order, and what you could not check.

## The rule

**Verify the claims, not the document.** A plan can be directionally excellent and still have
its most urgent item be a misdiagnosis. Acting on the misdiagnosis changes nothing and the
real risk survives into production.

## Procedure

### 1. Extract a claim table before reading for conclusions

Go through the supplied material and list every factual assertion with how you will settle
it. Generic classes of claim and the check that settles each:

| Plan asserts | Settle it with |
|---|---|
| a page has a specific defect | fetch it and read the body, not the metadata |
| N pages exist | count in the sitemap, then count in your own crawl, compare |
| a page has traffic or inbound links | read the real count from your crawl |
| a slug should be renamed | check whether the rename is even the bug |
| two pages compete | compare their inbound counts before prescribing a merge |
| X is better than Y | check whether Y was measured against its current state |
| search volume / traffic estimate | usually unverifiable; mark as the author's estimate |

### 2. Fetch, do not assume

```bash
curl -sL --compressed -A "Mozilla/5.0 (Macintosh)" -o /tmp/p.html \
     -w "http=%{http_code} type=%{content_type} size=%{size_download}\n" "<url>"
```

`--compressed` matters: without it a gzip response decodes to mojibake and you will read
binary as prose. Read `content_type` in the same breath, then confirm the response is the
page you asked for (`grep -o -m1 '<title>[^<]*</title>'`) rather than a bot wall, a redirect
or an interstitial. A page that looks garbled is frequently a real `text/html` response with
a correct title above it, so check the title before believing the body is broken.

### 3. Read the body, because the defect is usually one level deeper than stated

Title, H1, slug and body are four independent things and a plan may have diagnosed the wrong
one. A page can carry a correct title, a correct H1 and an opening paragraph about an
entirely different subject, which happens when content is templated across a large catalog.

- Read the first 200 to 600 characters of extracted body text and ask what the page is
  actually about.
- Group pages by a hash of their full body. Pages sharing one body are the same page with
  different URLs, and that cluster is where copy-paste defects live.
- Compare the slug's meaningful words against the opening text. A slug naming one brand whose
  opening never mentions it is a content bug, not a naming one.

**When the plan prescribes a metadata fix, confirm the metadata is actually broken before
recommending it.** Correcting a title that was already correct produces no change and burns
the team's trust in the rest of the review.

### 4. Do not repeat a remediation the evidence makes cheaper

Read the loser's inbound links before copying a canonical or a merge into your plan. A page
with zero inbound links has nothing to compete with and nothing to lose, so a plain redirect
does the whole job and the canonical is scope nobody needs. Look for the same downgrade
anywhere a plan proposes the heavyweight version of a fix.

### 5. Treat a dramatic negative as your bug first

An obviously wrong result is nearly always a query bug, not a site defect. "Zero links into
the largest section of the site" is not a finding, it is a filter on the wrong field: link
graph records typically carry anchor text in one position and node ids in another, so
searching the text field returns zero while the true count is in the thousands.

Resolve ids to urls and recount. Generalize it: before any surprising number reaches a
deliverable, confirm the field you searched is the field you meant.

### 6. Separate the site's defects from your instrument's artifacts

Before reporting corrupt or duplicated content, rule out your own pipeline. Binary stored as
text usually means the URL returned an image at HTTP 200. Check `content_type`, then check
whether your classifier already routed that node to `media`, because if it did the artifact
never reached the content findings and is not a site defect at all.

### 7. State the boundary of what you verified

Name the numbers you could not check, third-party estimates behind a login being the usual
ones, and assess the plan on everything else. Say plainly which recommendations survive on
the verifiable evidence alone.

## Output shape

Lead with the verdict and the finding that changes the plan most. Then, in this order:

1. **Confirmed**, with the number or the fetch that confirms it, and the consequence if it
   is worse than stated.
2. **Wrong**, as a short table of claim against truth against the corrected instruction.
3. **Missed**, especially free wins: an asset that already exists and is simply unlinked.
4. **Reordered priorities**, so the team acts on the corrected sequence.
5. **Not verified**, with what it would take.

Include the disclosure when your own instrument produced a number that turned out to be
wrong. Owning a corrected count costs nothing and is worth more than the quiet fix, because
the reader has to trust every other number too.

## Pitfalls

- **Do not execute a supplied plan before the claim table exists.** Sequencing is cheap now
  and expensive after the wrong page is rewritten.
- **Do not treat a third party's tooling as ground truth.** Their numbers came from a
  snapshot and often a partial one, so an internal crawl usually disagrees with them.
- **Do not soften a wrong claim into ambiguity.** "The plan is right that this page needs
  attention but names the wrong defect" is the useful sentence. Confirming the finding and
  adding a caveat buries the correction.
- **Do not skip the items that would embarrass the client.** Wrong copy on a page about to be
  featured prominently is a reputational risk and outranks a traffic optimization, even
  though the plan ranked it lower.
- **Do not let unverifiable estimates drive a build decision.** If the whole case rests on a
  search-volume table nobody can re-run, say so and rank on evidence you can check.
- **Deliver paths as `MEDIA:`**, not as bare filesystem paths, so the reader can open them.