---
type: context
status: active
company: "[[Company]]"
updated: {YYYY-MM-DD}
tags: [context, handoff]
---

# Handoff: {Cover A} and {Cover B} cover {Absent person}'s {systems}

Rules for this document, before filling it: no key values anywhere in the file (manifest lists slots and policies only); phase estimates come from the effort's PLAN.md, never invented; every unresolved name or acronym from the dictated ask lands as a row in section 7 with its nearest-match hypothesis, never as a silent guess; no em dashes.

**What this is.** One document for the covers of {Absent}, out {dates}. They run {system 1} and {system 2} until he returns, and they can start today without asking a follow-up question.

**Why now.** {The call and date this came from, plus the agreed cover.}

**Priority order (from Deep).** {His words, in order. For example: onboarding and ESS first, the rest after.}

---

## 1. Current state and today's fires

| Item | State | What to do |
|---|---|---|
| {system} | {what broke / what is mid-way / what nobody may touch} | {action} |

## 2. Task split

| Lane | Owner | Tasks |
|---|---|---|
| {lane name} | {Cover A} | {concrete tasks} |
| {lane name} | {Cover B} | {concrete tasks} |

Split is ownership, not isolation. Lanes may swap, but one name owns each line so nothing is orphaned.

## 3. Combined study plan

The goal: each cover can explain the other's half after three days.

- **Day 0 to 1 (joint):** read this document, then the effort's `PLAN.md`. Then split for a first pass, one architecture note each: what it is, how it runs, where the logic lives, what is broken.
- **Day 2:** cross-teach, 30 minutes each, from the notes. Ship one fix together as the first piece of joint work.
- **Cadence:** {existing cadence: daily standup, midweek pair, Friday demo}.
- **Study outputs:** (1) {output 1}, (2) {output 2}, (3) {output 3}, (4) {output 4}.

## 4. Access and credentials

### Repos

| System | Where | Notes |
|---|---|---|
| {system} | `{org}/{repo}` or local path | {GitHub, local-only, live URL, what it runs on} |

### Credentials manifest (no values in this document, by policy)

Actual key values never go in this document or in git. Deep delivers them in a private channel.

| Credential | For | Delivery | Policy |
|---|---|---|---|
| {key slot} | {system} | {who creates and shares} | {one key per app/feature/user, rotate unused first, never share across tools} |

## 5. The logic of the system

{How each system works at the level a cover will debug it: entry points, data flow, the decisions that shaped it.}

## 6. The future plan

{Phases with scope, estimate and done-when, copied from the effort's PLAN.md. Plus what happens after the cover ends.}

## 7. Open questions for Deep

| Question | Why it matters |
|---|---|
| {unresolved term/name from the dictated ask, with nearest-match hypothesis} | {wrong scope means wrong work / wrong person booked} |

**Primary sources:** {call transcript link, plan file paths, desk note paths}.

Related: [[Cover A]], [[Cover B]], [[Company]]
