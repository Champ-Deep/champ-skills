---
name: site-growth-audit
description: "Audit a live site and turn findings into a ranked plan."
---

# Site Growth Audit

Turn a running site into a verified, prioritized plan. The deliverable is a document someone can act on in order, not a list of things that could be better.

**Trigger on:** 'audit my site', 'why isn't my site ranking', 'site strategy', 'improve conversions', 'visitor tracking', 'what should I fix first', 'review my personal brand site', 'plan growth for <site>'. Also use when a named tool, folder or doc in the user's request turns out not to exist and the plan has to be grounded in what is actually deployed.

## Before anything else: the site is not what you were told

Users describe their own stack and goals from memory, and they are frequently wrong in ways that change the plan. Do not build on the description. Verify each named component exists before planning around it.

- Search the repo and the filesystem for the tool by name **and by near-miss spellings** before concluding it is missing. A near-miss hit is often the thing meant (`Widgo` read as `Wingo`).
- When a referenced folder, spec or doc does not exist, say so plainly and ask where to look rather than silently substituting your own design. Inventing the missing requirement produces work that gets thrown away.
- Ask for the one decision you cannot infer: **who pays**, and **what is sold**. Ranking, conversion, measurement and offer design all branch off those two answers. Guessing them wastes the entire audit.

Batch these into a single `clarify` call, 4 to 5 questions, then stop asking. Infer the rest from the repo and state assumptions.

## Phase 1: establish ground truth yourself, before delegating

Run these directly. Specialists cannot be trusted on load-bearing claims, and you need the real baseline to judge their reports against.

```bash
# does the live site serve what the repo says it serves
curl -sI https://<site>/ | grep -iE '^HTTP|content-security-policy|location'
curl -s https://<site>/robots.txt
curl -s https://<site>/sitemap.xml | grep -c '<loc>'

# unique vs duplicate: THE highest-signal single check on any site
# hash several sibling URLs. Identical hashes mean the "pages" are one page.
for u in a b c; do echo "$u $(curl -s "https://<site>/$u" | md5 -q)"; done
# include one deliberately BOGUS url. If the fake one matches, the real ones
# are being served a default, not their own content.

# what the data layer actually claims
node -e "const d=require('./content.json');console.log(d.brand, d.stats)"

# no commit history means no revert. Check before recommending any edit.
git log --oneline 2>&1 | head -3
```

**The duplicate-content check is the one that finds the big defect.** Sibling entity URLs on a site built with one prerendered file per page type will all hash identically, and a nonexistent slug will hash identically too. That single test finds more ranking damage than any amount of tag auditing, and it is four lines of shell.

**Always check the git history before recommending edits.** A worktree with zero commits has no `git revert`, which changes the risk calculus of every change in the plan. Say so in the plan and make a backup step phase zero.

## Phase 2: fan out specialists by concern

One specialist per independent workstream, dispatched in a single call so they run in parallel. Give each one everything it needs: it has no memory of the conversation and no idea what the others are doing.

Good splits for a growth audit: technical SEO, conversion and offer design, measurement and privacy, any named third-party integration's feasibility, and content or showcase surfaces.

In every brief include:

- The verified current state, so specialists confirm rather than rediscover. You save them the ground-truth phase.
- The user's stated goals and the decisions already made.
- Hard constraints, especially privacy promises and design-system rules.
- **A standing instruction to verify claims rather than recall them**, and to mark anything unverified as such. Ask for code and diffs returned in the response, never written to disk, unless you explicitly want files changed.
- Tell them **not to design the other workstreams**, so you can compose rather than reconcile.

Never let a subagent's summary be the evidence. Child reports are self-reports.

## Phase 3: re-verify the findings that will drive the plan

Specialists will confidently report wrong root causes and will rank a symptom above its cause. Re-run the checks behind any finding you are about to put in the top tier of the plan. The cost is one shell call; the cost of being wrong is a plan built on a false premise.

Three failure modes worth expecting:

- **Symptom ranked above cause.** Duplicate titles get reported as the headline defect when the real cause is that every entity URL serves one file. Fixing titles then decorates N copies of one page.
- **A gate that reports clean because it has nothing to check.** A denylist shipped with empty arrays passes forever and prints reassuring output. Verify a passing gate has non-empty inputs, and confirm a name or term is actually live on a public surface.
- **Correct behavior verified against the wrong premise.** A bot classifier that matches its own health checks will mark every scripted fetch as a crawler, and a passing test then proves nothing. When a gate or classifier passes unexpectedly, suspect the test.

Also check the reverse: **a claimed hard blocker may not be one.** A documented pricing or platform limit may already have changed. Re-read the vendor's current docs before repeating a limit as fact, and label what you could not confirm as needing verification.

## Phase 4: rank by leverage, and lead with damage control

Order strictly by **(impact on the user's stated goals) / effort**, and separate the two kinds of work:

- **Damage control first.** False public claims, leaked names or numbers, broken gates, dead CTAs. These are cheap and they are the reason a site cannot be trusted, so nothing built on top of them compounds.
- **Foundations second.** Structural defects that make everything else ineffective (duplicate content, missing canonicals, no measurement).
- **Enhancement last.** Everything that is a genuine improvement but not load-bearing.

Say explicitly what is **already fine**, with evidence. A plan that only lists problems sends someone to re-fix working things and destroys their trust in the rest of it.

State the unbuilt assumption in every plan that has one. If a page, endpoint or tool the user referenced does not exist, name it and say what the plan assumes in its place.

## Measurement and privacy, the standing rules

These recur on any site with a public tracking promise.

- **A public "no cookies, no trackers" claim is a binding constraint, not a marketing line.** Design inside it, or say explicitly that the promise must change and what the disclosure surface becomes. Do not quietly ship something that breaks it.
- **If a user asks for raw IPs, do not refuse and do not comply blindly.** Deliver the compliant version: truncate to the network (v4 `/24`, v6 `/48`), then HMAC-SHA256 with a secret held outside the repo. State the trade in one line, in their terms: what they lose (looking up an individual later) and what they keep (geo, new/returning, conversion, a promise that survives).
- **Use a bare hash only if you are certain it is not brute-forceable.** There are about 4.3 billion IPv4 addresses, so SHA-256 of an address is recoverable by brute force in minutes. HMAC needs the secret, which is the whole point.
- **New-versus-returning detection cannot exist without stored state.** A cookie, a KV key, localStorage or a Durable Object all violate a no-tracking promise. Say this plainly when someone asks for both, then point at arrival-shape signals (country, timezone, referrer, device) which need no identifier, cost nothing, and work with JS disabled.
- **Returning-visitor copy must only ever choose between two equally good versions.** Probabilistic identity is wrong often enough that gating anything on it produces a broken site that looks like a content bug.
- **Prefer stateless A/B assignment.** Hash an existing signal with a per-experiment salt: stable across requests, no cookie, no storage. This is what makes experimentation feel like it needs no tracking stack.
- **Count pageviews server-side in the response you already generate.** No client JS, works with JS off, cannot be blocked by an ad blocker, no extra round trip. Use `sendBeacon` with a `text/plain` blob for client events so there is no preflight.
- **Exclude bots from the event log, and check tools before browser-shaped patterns.** A naive bot list that matches `curl` classifies every scripted verification fetch as a crawler and quietly poisons the numbers.
- **Verify Cloudflare tier limits and retention behavior at use time, and label them as needing re-verification.** They change, and they are usually the entire argument for a storage choice.

## Choosing where a "ultrafast" tool can actually run

When a user wants a third-party model or classifier on the request path, establish what the thing **is** before planning around its latency. A library with a native core, a hosted HTTP endpoint, and a WASM artifact are three different things with three different cost profiles.

Check the upstream repo's actual file tree, releases and package registry for a compilable artifact. If the package is a thin client over `post_json(...)`, there is nothing to compile and no cold-start question to answer. Measure the floor from inside the runtime you would deploy in, with a dummy credential so the number is transport only, rather than quoting the vendor's own latency claim, which usually already includes the round trip.

Then sanity-check whether the tool fits the job. A classifier cannot recover an identity that was never recorded, and latency only matters where a human is waiting.

## The decision rule for the optimization loop

Instrumentation that produces numbers nobody acts on is a worse failure than no instrumentation. Ship a rule with the metric:

One number crosses its threshold, on a minimum sample, on two consecutive periods. Never act on a single day. Write the change as a one-line hypothesis naming the metric. Make it, record the build timestamp. Re-check after a fixed interval: moved, keep it; did not, revert and write down that it did not work.

The revert step is the one people skip, and skipping it is how a site accumulates permanent experiments with no record of which one won.

## Output

A single document, written to the user's vault or notes, with:

- The decisions the user made, recorded up front.
- **False or drifted public claims as the first section.** These outrank feature work.
- Findings grouped by concern, each with evidence, root cause, effort, and regression risk.
- An explicit "verified already fine, do not spend time here" section.
- A phase table with the ordering rationale, and a phase zero for backup where history is missing.
- A short "still undecided" list naming the choices that are the user's, not yours.

Lead the chat reply with the finding that changes the plan most. Do not replay the process or summarize the document back to them.

## Pitfalls

- **Do not add a strategy document to a pile of unshipped plans.** If several prior plans exist, say so and put damage control ahead of all of them. A fourth plan is not progress.
- **Do not let a vanity metric be the headline.** Entry counts, streak lengths and tool totals read as proof of stamina, not of results. Rank proof by whether money or a decision moved, and check the page is not leading with volume while the decisive evidence sits in a log.
- **Do not recommend a high-ticket engagement behind a generic "book a call".** A free call with no context converts into free advice and produces a warm contact with no revenue. Put a qualifying step in front of the call.
- **Do not feature an unlinked asset as if it were missing.** Before building a surface, check whether an equivalent one already exists and is simply not linked from anywhere. A built-but-unreachable route is the cheapest win available.
- **Do not put a price on the page for a per-engagement quote.** A visible price anchors the deal downward and caps the quote. Publish scope, hours and boundaries instead.
- **Do not send the user to a bare file path.** Deliver paths as `MEDIA:` so they render as openable cards.
- **Do not build the visual layer before the accuracy layer.** A prettier site that says something false is strictly worse, because the polish earns trust the content then breaks.

## Delegation cost note

A five-specialist fan-out on a site audit is a heavy operation. Confirm the user wants a full audit before dispatching, and prefer two to three specialists when the question is narrow.
