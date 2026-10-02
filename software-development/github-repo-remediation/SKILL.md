---
name: github-repo-remediation
description: "Fix metadata, branches and docs across many GitHub repos."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, gh, repos, metadata, topics, branch-protection, readme, bulk, remediation]
    category: software-development
    related_skills: [github, github-portfolio-audit, visual-verify]
---

# GitHub Repo Remediation

Apply governance, metadata and documentation fixes across a whole repository
portfolio. This is the **write** phase that follows an audit. If you have not
established the true owned-repo count and the gap list yet, do that first, read-only,
and agree the plan before mutating anything.

Covers: topics, descriptions, default branches, branch protection, and generated
documentation committed through pull requests.

## Core rule: a 2xx is not proof

**Every bulk write must be followed by an independent read of the same resource,
compared against what you sent.** This is not paranoia, it is the single most
expensive trap in this workflow: some endpoints accept a field, return success, and
change nothing. A run that reports "53 repos updated" against repos that are still
untagged is worse than a run that failed, because it is believed.

```python
written = gh(f"repos/{full}/topics", "PUT", json.dumps({"names": topics}))
check  = gh(f"repos/{full}/topics")            # separate read
assert sorted(check["names"]) == sorted(topics) # compare, do not trust
```

Report counts you verified. If a write cannot be verified, say so rather than
counting it.

## Order of operations

Cheapest and most reversible first, so the user sees visible progress early and a
later failure costs less. Do not reorder to "finish the important bit" first.

| # | Step | Reversal | Creates history |
|---|------|----------|-----------------|
| 1 | Topics + description | one call each | no |
| 2 | Default branch | one PATCH | no |
| 3 | Branch protection | one DELETE | no |
| 4 | Files (README, LICENSE) | revert commit | **yes** |
| 5 | Archive / delete | unarchive / restore | no |

Step 2 must be followed by step 3. Protection is attached to a branch *name*, so
changing the default branch leaves protection stranded on the old name and the repo
ends up less protected than before you touched it. See `references/bulk-write-api.md`.

## Establishing scope honestly

A linked profile page shows only public repos and paginates at 30. Enumerate via
paginated REST and filter by `owner.login`, since `affiliation=owner` also returns
repos where the user is merely a member. Report the delta in one line
("97 owned, 42 public; your profile page shows 30") rather than letting the user
believe the smaller number.

Before and after, the population must be the same set of repos. Writing a real
description to a repo that used to read `Backup of local project X` moves it out of
the backup bucket and into the active portfolio, which shifts every denominator.
Compare on the intersection of before/after and exclude empty repos from
branch-protection counts, or both show as phantom improvements.

## Writing documentation that is worth reading

Read the repo's own manifests, route tables, migrations, ADRs and setup docs before
writing a sentence. A templated README is worse than none, because it signals a
maintained project that nobody has read.

- **Match the house style already in the account**, taken from its best-maintained
  repo. Do not invent a new one.
- **If the repo already has a strong `CLAUDE.md` / `CONTEXT.md` / PRD, link to it and
  add the reader-facing layer.** Duplicating the content is how the two drift apart.
- **Where evidence is too thin to write honestly (an empty repo), decline and leave
  it for the user.** Never invent a description to fill a gap.

Commit each file on a branch, open a PR, merge, delete the branch, then read the file
back off the default branch and compare bytes. A direct commit to the default branch
is faster and is the one change nobody can revert cleanly.

## Classifying repos from evidence, not names

When grouping repos into domains or deriving topics, rank the sources by reliability:

- **Manifest dependencies** are what the author declared they built with. Trustworthy.
- **File paths are not.** A repo with a `data/video/voice/` directory is not a video
  product; keyword matching on paths produces confident, wrong answers.
- **Author prose** (description, README opening) is the only place intent is stated on
  purpose. Strip markup before matching - a shields.io badge reading `?style=social`
  will otherwise tag a PDF tool as a social-media project. Anchor short keywords with
  word boundaries, or `imap` matches "map" and `design` matches "sign".

Cap topics at a handful; a 20-topic repo is one nobody reads. Keep genuinely ambiguous
classifications in an explicit, visible override table so the judgement can be argued
with, and assert the final grouping still sums to the input count.

## When a generated report is the deliverable

A remediation summary is usually an HTML artifact, and generating it from data has
failure modes no HTML validator catches:

- **Derive every container's height from the contents it encloses.** Re-adding the
  top padding inside the height calculation double-counts the offset, inflates every
  box, and pushes trailing elements such as a legend past the viewBox, where they are
  invisible. Assert trailing-element Y against the viewBox height before writing.
- **Run the visual verification gate and actually look at the screenshots.** Reading
  the source cannot tell you a legend rendered off-canvas. When a screenshot crop
  seems to show a missing element, measure the element's real bounding box in the
  browser before concluding it is absent; a crop boundary is a common false negative.
- Check contrast against the composited background, honour
  `prefers-reduced-motion` for any animation, and keep heading levels contiguous.

## Pitfalls

- A `200` from a bulk write may mean nothing changed. Read back and compare.
- A cached record of a failed fetch must be re-fetched, not replayed, or one failure
  becomes a permanent phantom result. A per-item `except` must print the failure; a
  silent one is indistinguishable from "no data" and hides real bugs.
- Falsy-zero: `days_idle == 0` means "pushed today". Never classify with
  `idle or 9999` / `idle or 0`; compare the value instead, or the freshest repos fall
  through every bucket and the counts stop summing to the total.
- Mutating an object in place while preparing it for the next stage (rewriting a dict
  into a string, say) breaks the consumer that runs later. Normalize both shapes
  through one helper rather than assuming a single type.
- `403` on a write is a plan limitation, not a bug to retry. Determine the account
  or org policy once, then report it rather than retrying per repo.
- Deleting repos may exceed token scope. Flag what needs manual web cleanup instead
  of assuming the API will do it.

## Verification

- Every reported count is re-read from the API after the change, never taken from a
  write response.
- Before/after tables compare the same repo set, and the set is named in the output.
- Tier or bucket counts sum exactly to the population; assert it in the generator.
- Merged files are byte-compared against the source on the default branch.
- If any figure could not be verified, it is labelled unverified rather than reported.

## Supporting files

- `references/bulk-write-api.md` - endpoint-level traps: the topics endpoint, request
  bodies via `gh`, default-branch changes vs protection, plan limits, the contents
  API, and safe protection payloads.
