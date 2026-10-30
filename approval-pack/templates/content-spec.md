---
kind: template
description: Content spec skeleton for an approval pack. Copy it, keep the section order, delete what the initiative does not need.
---

# <Initiative name> approval pack: content spec

```yaml
type: build-spec
effort: <effort folder>
created: <date>
source: <path to the reasoning report this pack draws on>
sensitivity: internal
```

## Audience and use

- **Primary reader:** <name, role>.
- **Async:** what they do with the file, and what they send back.
- **In person:** the same file is the run of show for a <N> minute meeting.

## The ask (one line)

<N> decisions. Approve, approve with changes, or say no, with a reason. About <M> minutes to review.

## What we want and why

Two or three sentences: the pilot, the guardrails, and that nothing happens until sign-off.

## The decisions

Repeat per decision:

### D<n>. <title>

- **Proposal:** what we will do.
- **Why:** the reasoning, in one or two sentences.
- **Need from <stakeholder>:** the fields they fill (names, dates, owners, periods).

Keep the count at seven or fewer, each answerable in one line.

## Concerns we expect, with our answer

| Concern | Answer |
|---|---|
| <concern in their voice> | <control we lock, naming the decision that carries it> |

## Run of show (<N> minutes)

| Time | Item | Outcome |
|---|---|---|

## Next steps after sign-off

1. <step with an owner>

## Notes for the build (not shown in the pack)

- Numbers I proposed that Deep must confirm: <list>
- Assumed scope: <list>
- Conflicts folded into which decision: <list>
