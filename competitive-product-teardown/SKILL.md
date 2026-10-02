---
name: competitive-product-teardown
description: "Compare our product to a competitor or upstream repo."
---

# Competitive Product Teardown

Compare a product or codebase against a competitor, an upstream fork, or a reference
implementation, and turn the result into a fix plan someone can execute in order.

**Trigger on:** 'compare this to <repo>', 'how do we compare to <product>', 'what can we
take from <repo>', 'we forked <project>, what did we miss', 'are we behind <competitor>',
'what should we build next based on <this tool>', 'audit our scoring/accuracy pipeline'.
Also use when the user pastes a GitHub URL next to the name of one of their own products
and asks what to do with it.

Shares its verification methodology with `site-growth-audit` (live sites, SEO/conversion).
Use that one when the target is a deployed property; use this one when the target is code.

## The README is not the product

Read the source. Every claim in a competitor's README, roadmap, or docs is a hypothesis
until you find the code that implements it.

In one teardown the competitor's flagship enrichment class was **never registered in
production**, so its cache, its best-of-N, and its confidence early-exit were all
unreachable. Their largest cost lever was wired to a path nothing called. Two files had a
comment that swallowed an import and would `NameError` at runtime. Their roadmap listed as
future work a feature we had already shipped.

A README comparison produces a plan built on the other project's marketing. A source
comparison produces a plan built on what runs.

Corollary: a **roadmap is not a feature.** When the user asks "what can we implement from
X", check whether the item is shipped, in-progress, or aspirational before ranking it.

## Phase 1: own ground truth first, before delegating

Do not open with a fan-out. Establish the baseline yourself, because you need it to judge
the specialists against, and you will be wrong in front of the user otherwise.

```bash
# locate the local repo before anything else. A broad search over the home directory
# times out and skips protected macOS folders; list the known project parent instead.
ls -d /Users/deep/Apps\&Projects/*/

git -C <repo> log --oneline -25
git -C <repo> branch -a
git -C <repo> remote -v
git -C <repo> diff main..<branch> --stat | tail -30
```

Then read the scoring, validation, and refresh paths **yourself** before dispatching. That
is where the load-bearing findings live, and reading them first is what lets you catch a
specialist ranking a symptom above its cause.

## Phase 2: fan out one specialist per area

One brief per independent area, dispatched in a single call. Each child has no memory of
the conversation, so give it: the repo paths, what you already verified, the specific
questions, and a demand for `file:line` evidence with real quoted code.

**Ask for the capability inventory AND the honest gap list in the same brief.** A
specialist asked only for capabilities reports the competitor's intent; asked for gaps, it
hunts for what is broken. You want both, and one pass gets them consistently.

Tell them to return findings in the response, not to disk.

## Phase 3: re-verify before it reaches the user

**Child reports are self-reports, and the first pass systematically under-ranks.** In one
session the initial summary surfaced six issues; the full reports, delivered later, held
four more severe than any of the first six, including a data-integrity bug and a
customer-visible billing bug.

1. Re-read the source behind every finding headed for the top tier. One `read_file` each.
   The cost is minutes; the cost of being wrong is a plan built on a false premise.
2. **Watch for the batch-completion re-delivery.** Background delegations return a
   *truncated* summary in the conversation and save the full text to a file. Read the file
   before concluding the work is done; grep the transcript for the writeup rather than
   trusting the summary block.
3. Say plainly when you added findings after verification, and **lead with the
   correction.** The user's first read of your conclusion was wrong in a way that changed
   their plan, so the correction is the headline, not a footnote.

Two failure modes worth expecting:

- **A degraded path that scores better than a healthy one.** Look for the default used when
  a check is *unavailable*. A fit score of `undefined` mapping to the maximum multiplier
  means judging failure rewards rows. Any "we could not check" branch must resolve to worst
  case, never neutral or best.
- **A gate that is advisory but reads as enforcing.** A verdict computed and then attached
  to the output, while the expensive work already happened, saves nothing. Confirm the
  branch that would have skipped the cost actually skips it.

## Phase 4: rank by severity, not effort, when the work is bugs

If the audit found defects rather than gaps, order by **severity first, effort second**, and
bugs precede features. Two customer-visible problems outrank every differentiator you could
ship this quarter. Say which findings are bugs and which are improvements; the user is
deciding what to do this week.

- **Damage control.** Wrong scores, lost data, mis-billed quotas, provenance pointing at the
  wrong entity. Cheap, and nothing built on top compounds.
- **Foundations.** Structural ceilings that make other work ineffective (unbounded queries,
  O(n^2) scans on the hot path, unpinned dependencies).
- **Enhancement.** Real improvements that are not load-bearing.

## Always include these three sections

1. **What we already do better, with evidence.** Say it early and say it specifically. A
   teardown that only lists problems sends someone to re-fix working things and destroys
   trust in the rest of the document. In one comparison the competitor had six times the
   code and no cell-level diffing, which was the user's single best feature.
2. **Where the competitor is weak, so the user does not chase it.** Their dead code and
   broken tools are as useful to you as their good ideas.
3. **Open questions only the user can answer.** Name the specific decision and why code
   cannot settle it. When a prompt legend and a validator disagree on a scale, do not infer
   the intent and proceed: write it up as a decision they own, because a scoring change
   built on a guess is worse than no change.

## Output

One document in the user's vault, under the product's effort folder. Do not add another
undated plan to a pile: if prior plans exist, say so and put damage control ahead of them.

Before delivering, run the vault's mechanical checks on the file itself:

```bash
# no em/en dashes: they break the vault rendering rule
python3 -c "import re,sys;t=open(sys.argv[1]).read();b=[i+1 for i,l in enumerate(t.split(chr(10))) if re.search(r'[\u2014\u2013\u2012\u2015]',l)];print('violations:',len(b),b[:5])" <file>
```

Deliver the path as `MEDIA:` so it renders as an openable card, never a bare path. Lead the
chat reply with the finding that changes the plan most. Do not replay the process.

## Upstream fork sync

When our product started as a fork, "what should we pull" is a diff question. **Never merge
upstream wholesale.** Do the file-set difference first:

```python
import os
def files(root, sub):
    out = []
    for dp, dn, fn in os.walk(os.path.join(root, sub)):
        dn[:] = [d for d in dn if d not in ('node_modules','dist','.mastra','__pycache__')]
        for f in fn:
            if f.endswith(('.ts','.tsx','.mjs','.yml','.json','.sql')):
                out.append(os.path.relpath(os.path.join(dp,f), root))
    return set(out)
for sub in ["backend/src", "frontend/convex", "frontend/components"]:
    b, c = files(UPSTREAM, sub), files(FORK, sub)
    print(sub, "only upstream:", sorted(b-c), "only ours:", sorted(c-b))
```

Read the two lists differently. **Only in upstream** is usually packaging infrastructure for
*their* distribution model (desktop installer, OS keychain bridge, release CLI) that our
deployment does not need. **Only in ours** is the honest measure of how far the fork moved:
report it as a number, because it changes how the user reads every other recommendation.

Then read shared-file diffs in **one direction** only, since the goal is "what does upstream
have that we lack":

```bash
diff -u "$UPSTREAM/path/file.ts" "$FORK/path/file.ts" | grep '^-' | grep -v '^---'
```

A numeric tuning constant that differs between fork and upstream is a **decision, not a
typo**. Use pickaxe to find the commit that set it (`git log --oneline -8 -S "MAX_CONCURRENT"
-- <file>`). If the fork raised it and upstream never touched it, recommend taking upstream's
value, and give the reason as cost, not correctness.

Also scan upstream history for security-shaped commits and audit our tree against them
rather than assuming we inherited them. Moving a package off npm, clearing a scanner's
alert batch, or pinning a base image are cheap wins that are invisible when skipped. State
them as "audit whether we have this" unless you verified the file.

What a diff cannot tell you: whether removing a vendor shrank your effective surface.
Removing a paid search API is not removing sources, because the replacement may fan out to
the same underlying engines by default. Say this explicitly, because the user will otherwise
assume the surface shrank.

## Evaluating a third-party tool before adopting it

When a much-hyped dependency lands in the request ("can we use X", "test the new Y system"),
the deliverable is a decision, not a survey.

**Stars are not maturity.** Record `git log -1 --format="%H %ad"` and `git log --oneline |
wc -l`. A tool can have a very large star count, an impressive demo video, and a
three-commit history that has not moved in weeks. That is a polished demo, and adopting it
means owning code you did not write and cannot pace. State the discrepancy plainly; it is
the most decision-relevant fact in the evaluation and it is never in the tool's own README.

**Separate the transferable idea from the product.** The pattern in one recent case: instead
of asking a model to generate an action, enumerate the action space in your own harness,
hand the model an indexed element table, and ask it only to index. Two typed questions, one
network round trip. Applied to our own per-result classification loop, that cut the
dominant LLM cost from one call per item to one call per batch. The product in that same
case was a browser agent needing a live browser and two API keys, which would have been a
large regression for code that only reads static pages. Name the pattern, map it to a
specific file, and price the product separately.

**Test against our real failure cases, not the vendor's demo.** Our own error branches
enumerate our pain (`grep -n -E "error|blocked|timeout|403|429" <our fetch layer>`). Run
incumbent and candidate on the same N; measure correctness, wall time, and cost per item.

**Set the decision rule before you run it,** or you will rationalize whatever comes back. A
good default is narrow: does the candidate beat the existing cheap fallback on a meaningful
minority of the failures? If yes it may earn an opt-in slot behind the **existing provider
seam**, never as the default and never in the critical path. Timebox it, use a branch, and
commit the harness so the result is reproducible.

**Fail-closed check on anything that calls a model vendor.** Before recommending a pinned
model slug or endpoint, ask what happens when the vendor retires or renames that
identifier. A pinned string plus a fail-closed branch plus a downstream default that treats
unavailability as *acceptable* is a silent accuracy regression with no error anywhere. Check
the branch exists and check what value unavailability maps to. Also note whether the client
is a hand-rolled HTTP call or the vendor's SDK, and distinguish a transient
timeouts-and-retries issue from an auth or quota wall.

## Pitfalls

- **Do not let a line-count diff stand in for substance.** More lines across a shared file can
  be entirely your own feature work.
- **Do not adopt a tool because it is the topic of the week.** Check maturity signals, and
  separate the idea from the product.
- **Do not report a foreign repo's self-declared status as fact.** "Experimental" or
  "pre-beta" tells you their posture, not their capability. Different claims.
- **Do not let the plan's scope silently absorb the whole ask.** "Address all weaknesses"
  usually means a bug-fix tier and a feature tier; sequence them separately so the bugs do
  not wait behind the features.
- **Do not add another undated plan to a pile of undated plans.** That is not progress.
