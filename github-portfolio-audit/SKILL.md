---
name: github-portfolio-audit
description: "Audit a whole GitHub account's repos for governance gaps."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, audit, governance, portfolio, repos, branch-protection, ci, hygiene]
    category: software-development
    related_skills: [github, apps-projects-backup, codebase-inspection]
---

# GitHub Portfolio Audit

Sweep an entire GitHub account (all repos, including private) and report governance,
hygiene and discoverability gaps as a ranked, evidence-backed deliverable. Use when asked
to review "all my repos", find gaps, assess portfolio health, or improve how agents work
across a repo collection.

## Procedure

### 1. Establish access scope BEFORE promising anything

The GitHub profile page a user links shows only their PUBLIC repos and paginates at 30.
Never scope the audit to what that page renders.

```bash
gh auth status                      # confirm account + token scopes
gh api user/repos?per_page=100 -q 'length'   # true owned-repo count
```

Report the honest delta: "96 owned repos, 34 public, 54 private; your profile page shows 30."
A user who thinks they have 30 repos and hears 96 needs that explained in one line.

Token scopes that matter: `repo` = full read/write on private repos. `read:org` = org repos.
If `repo` is present, private-repo access needs no further setup. State this plainly rather
than manufacturing an "integration setup" task the user did not ask for.

### 2. Prefer REST over GraphQL for bulk enumeration

A nested GraphQL query asking for many fields across ~100 repos returns HTTP 504/502 and
fails outright. The same data comes back reliably from paginated REST. Start with REST for
anything touching every repo.

```bash
gh api "user/repos?per_page=100&page=$p&affiliation=owner&sort=pushed" -q '.'
```

Page until a page returns fewer than `per_page` rows. Note `affiliation=owner` still returns
repos where the user is a member, so filter by `owner.login` before counting as "owned".

### 3. Fan out per-repo detail with a thread pool + retry

A full audit is ~12 API calls per repo. Serially that is 1000+ round trips. Run 6-8 workers,
retry only on 502/503/504 with backoff, and treat 403/404 as legitimate "not configured"
answers rather than errors (that is how you detect absent branch protection and absent
Dependabot). Use `scripts/portfolio-audit.py` as a working, re-runnable implementation.

### 4. Classify before analyzing

Raw counts over 90 repos are unreadable and hide the signal. Bucket first:

- **forks** - exclude from gap stats, report separately as upstream-divergence merge debt
- **backups** - name matches `-backup`, `.backup-<ts>`, `_backup`; report as cleanup
- **Tier 1** - active work (pushed recently), sorted weakest-governance-first
- **Tier 2** - dormant, undecided
- **Tier 3** - archive candidates

Days-idle from `pushed_at` is the sort key that makes tiers meaningful.

### 5. Rank gaps by blast radius, not by count

Lead with the finding whose failure is silent and expensive, not the most numerous one. The
ordering that generalizes: unprotected branches > no CI > no tests > no agent config > no
license/discoverability. One repo with no branch protection outranks ninety missing topics.

### 6. Deliver a single-file HTML report

Dark, self-contained, no external assets. KPI strip, ranked gap table with severity, tier
tables, backup/orphan list, recommended sequence. Write it somewhere durable and hand it over
as a `MEDIA:` absolute path - never as a bare path.

State plainly in the report and the chat reply that the audit was READ-ONLY: no repos or
settings were changed. Then ask before mutating anything.

## Verification

- Parse the generated HTML with `html.parser` and assert zero unclosed tags at EOF and zero
  tag mismatches. Do not eyeball a large f-string template; a single missed brace ships broken
  markup.
- Check for unrendered template artifacts (`{{`, `{r[`, stray `None`) before delivering.
  Beware false positives: CSS media queries legitimately contain `}}`, and words like
  "gover**nan**ce" contain `nan`. Inspect the match context before "fixing" anything.
- Recount the delivered numbers against the fetched JSON. A report that says "96 audited" must
  match a list of length 96.

## Pitfalls

- `gh api --paginate -q '.'` concatenates multiple JSON documents with newlines.
  `json.load` fails with `Extra data: line 2`. Parse with a `JSONDecoder().raw_decode` loop
  instead of giving up on pagination.
- `gh repo list --json` rejects unknown field names outright (`openIssuesCount` does not
  exist) and prints the valid field list in the error. Read that list rather than guessing
  field names; `--source` is required to include private repos.
- The REST repo payload has no `subscribers_count` key. Use `.get()` for any field you did not
  confirm is present, or the audit dies on the last repo after an hour of work.
- Python sets are not JSON serializable. Built any set while computing intersections and a
  single `json.dump` will throw `Object of type set is not JSON serializable` after the whole
  fetch completed. Pass `default=list` AND write per-repo cache files incrementally, so a late
  serialization bug never costs the network work.
- If a browser/preview service is unavailable, do not conclude the HTML is broken and do not
  drop verification. Structural parsing catches the failures that matter (unclosed tags,
  template leakage).
- Check whether a configured MCP server is actually `enabled: true` before recommending it.
  A registered-but-disabled GitHub MCP entry is a config fact to report, and when `gh` already
  covers the ground, recommending the disabled server is a downgrade - say so instead.
- Backup repos whose names truncate mid-word (shell-truncated clone names) will not match a
  naive suffix split. Report unmatched backups as orphans needing manual verification rather
  than silently dropping them or assuming a base name.
- Deleting repos may be outside the token's scopes (`delete_repo`). When recommending backup
  cleanup, flag repos that need manual web cleanup rather than assuming `gh repo delete` works.

## Supporting files

- `scripts/portfolio-audit.py` - re-runnable bulk audit: REST enumeration, threaded per-repo
  detail, incremental cache writes, JSON output.
- `scripts/render_report.py` - turns the audit JSON into the single-file HTML report.
  Owns the tier classification and the gap ranking; never calls the API.
- `references/audit-endpoints.md` - the per-repo endpoint set, what each proves, and the
  gap taxonomy mapped to endpoints.

### Bugs already fixed in these scripts, do not reintroduce

- `days_idle == 0` means "pushed today". Never classify tiers with
  `idle or 9999` / `idle or 0` - zero is falsy, so the freshest repos fall
  through every bucket and the tier counts silently stop summing to the
  portfolio total. Compare the value, do not default it.
- `main()` rewrites `r["parent"]` from a dict to a plain full_name string while
  disambiguating forks. `audit_one` then calls `.get()` on that string and
  raises `AttributeError`. Normalize both shapes through one helper.
- A cached per-repo record that contains `__error__` must be re-fetched, not
  replayed. Otherwise a single failed repo looks like a repo that genuinely has
  no data, forever.
- The per-repo `except` must print the failure. A silent per-repo exception is
  indistinguishable from an absent file and will hide real bugs.
- An empty repository reports `days_idle: None`, not `0`. Treat `None` as
  "never pushed" explicitly.
