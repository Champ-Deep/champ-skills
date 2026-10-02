---
name: plan-and-prd-review
description: "Adversarially review an existing plan or PRD for gaps."
---

# Plan and PRD review

Stress-test a plan or PRD that **already exists**, then patch it. This is not a
drafting workflow and not a teardown.

**Trigger on:** 'assess this plan', 'adversarial review of the plan', 'what is
missing from this', 'does this have a clear goal and endpoint', 'what does done
look like', 'is the functionality complete end-to-end', 'go ahead and add all of
those'.

Sits beside two related skills. `decision-grill` turns a *spoken brief* into
dated rulings. `competitive-product-teardown` produces a plan *from a
competitor*. This one takes a finished artifact and asks whether it can be
executed and falsified. When a plan came out of a teardown, review both.

## Read the whole artifact, and its siblings, before judging

Read every line first. A review built on a skim produces the same generic
gaps every time and the user can tell.

Then find the documents that share ownership with it: sibling PRDs in the
vault, the effort note, the product's own README. Two documents claiming the
same subsystem in the same repo is a **real defect in the plan**, and it is the
finding most likely to change what gets built next.

## The falsifiability gate

The most common defect is a plan whose definition of done cannot fail.

> It is done when, over a measured 30 days, we can state our own measured rate.

Measure 8 percent, report it honestly, and the plan is satisfied. There is no
threshold anywhere, so nothing was ever at risk.

**The test: could you measure a bad number and still honestly report success?**
If yes, the plan is not falsifiable and needs thresholds before anything else.

Every acceptance criterion is one of two kinds:

- *demonstrate the mechanism* - the seam works against real data
- *meet a bar* - the mechanism clears a number

A plan made entirely of the first kind never fails. Fix it by attaching a
**ship / stretch / kill** value to each metric, and give every metric a
measurement method **and a named denominator**. Without the denominator the
number is argueable later: "8 percent of sessions" and "8 percent of identified
sessions" are different products.

Prioritise the threshold that decides whether the effort ships at all. The rest
are instrumentation.

## The structural completeness checklist

Architecture documents get mistaken for PRDs. Telltale signs: sections named
*Phasing*, *Architecture*, *Success looks like*; no screen list; no verbatim
copy; escalation or handoff mentioned in passing and specified nowhere.

For any user-facing feature, check these seven. They are the ones that were
missing in a full plan that otherwise had a clear goal, verified research, and a
credible build sequence.

| Gap | The question that exposes it |
|---|---|
| Thresholds | What number makes us stop? |
| End-to-end journey | What does the user see in the first three seconds, and what are the named paths through? |
| Handoff spec | What triggers escalation, what does the human receive, where, how fast, and what is the user told about the wait? |
| Security and abuse | Prompt injection through the user's own input, data retention, tenant isolation as a *threat*, cost exhaustion on an unauthenticated endpoint, third-party script surface |
| Cost model | Cost per interaction, then per outcome, then break-even against the value of one outcome |
| Failure modes | One row per dependency: what the user sees when it is down, rate limited, or returns empty |
| Feedback loop | What is collected, reviewed on what cadence, and which single number is trended |

`references/plan-audit-checklist.md` has the per-section question list to walk
a document against.

**Report the cheap wins as arithmetic, not as features.** Cost modelling
frequently inverts a standing assumption about what the constraint is, and that
reordering is worth more than the section itself.

## Plan-versus-reality drift

A plan being executed against goes stale, and a plan patched after the build has
moved is stale in a second way. After adding sections, also correct:

- the **header status line**, which usually still describes the doc as unbuilt
- **each phase's own status**, split into what is built, what is verified live,
  and what is outstanding. "Built and tested" and "proven against a real
  calendar" are different claims; say which one is true.
- any **gate the build already crossed**. Say plainly that it was crossed
  before the current thresholds existed, and that is why they are written down
  rather than assumed.
- **"not decided here" lists** that still describe something as deferred to a
  phase which deliberately did not build it.
- **thresholds that contradict a number written earlier in the same document**,
  and note the revision in place rather than silently replacing it.

## Stopping a build cleanly when the scope moves

When the user pivots from building to documenting, record the state first so the
document can describe reality: branch, commit, test count, and what is verified
against live systems versus only covered by tests. A plan that claims more than
was verified is worse than one that claims less.

## Adding the missing sections

Land them in place, not as an appended bolt-on. Write the block, splice it at
the anchor heading, then fix the status lines that the new sections made
stale, in the same pass.

Verify mechanically before delivering:

```bash
# no em/en dashes anywhere in the vault file
python3 -c "import re,sys;t=open(sys.argv[1]).read();b=[i+1 for i,l in enumerate(t.split(chr(10))) if re.search(r'[—–‒―]',l)];print('violations:',len(b),b[:5])" <file>
```

Then check heading order with a grep, and confirm every `section N` reference in
the body resolves to a heading that exists. Cross-references break silently
when sections are inserted and nothing looks wrong.

Deliver the path as `MEDIA:` so it renders as an openable card, never a bare
path. Summarise what landed and what is still the user's to rule on. Propose
numbers as **proposals until ruled**, not as decisions taken.

## Pitfalls

- **Do not invent what is missing from a skim.** Read all of it first, then
  name gaps by quoting the section that has the gap.
- **Do not treat a plan with a clear goal as a finished review.** A strong goal
  and a complete end-to-end specification are independent, and having the first
  is what makes people stop looking for the second.
- **Do not soften a kill threshold into a discussion.** A threshold with no
  kill value is a preference.
- **Do not claim a gap is real without checking the sibling docs and the code.**
  Another PRD may already own the subsystem, and a doc section with no working
  code behind it is a docs fix, not a rewrite.
- **Do not bury the ownership conflict in a list of improvements.** It changes
  what gets built next and belongs near the top.
- **No em dashes in any vault write.** Verify on the whole file after splicing,
  since a merge can reintroduce one.
- **Do not append an `UPDATE:` block under a sentence that was wrong.** Edit the
  sentence; a document that contradicts itself is worse than one that was
  briefly incomplete.