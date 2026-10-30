---
name: "approval-pack"
description: "Sign-off pack a stakeholder approves without a meeting."
version: "1.0.0"
author: Hermes Agent (Nous Research)
license: MIT
metadata:
  hermes:
    tags: [sign-off, decision-pack, async-approval, run-of-show, stakeholder]
    related_skills: [plan-and-prd-review, decision-grill, frontend-design, visual-verify]
---

# Approval pack

Deep needs one stakeholder to sign off a list of decisions without booking a meeting, and if a meeting happens anyway, the same artifact has to run it. One artifact, two modes: **Review** (read, mark each decision, send back) and **Meeting** (timed agenda wired to the decisions). Producing two documents is the first way to fail: they drift, and the meeting version argues with the one that was sent.

**Trigger on:** "something he can approve without a meeting", "a central file I can share for sign-off", "an approval or decision pack", "a run of show for the meeting", "get IT/the team to agree this asynchronously", and any time an external party must ratify a list of decisions the vault already holds reasoning for.

## When to Use

- The stakeholder must ratify decisions and a meeting may not happen.
- The vault already holds the reasoning, so the pack is assembled rather than argued.
- One artifact must serve both the async review and the live meeting.
- **Not for:** internal planning with no external sign-off (use a decision note), or a plan being stress-tested rather than approved (`plan-and-prd-review`).

## Procedure

### 1. Gather the decisions before formatting anything

The decisions and their reasoning come from the vault first, vendor docs second.

1. Search the vault for the decision log of this initiative: `search_files(target='content')` for the decision-note markers of the program (precedent ids, decision-desk notes, effort notes), then `read_file` the recent notes in full rather than trusting the grep lines. Decision notes record dated precedents, so find the newest one, not the first hit.
2. Read the vendor's own security or admin documentation for every claim about how the tool behaves. **Vendor docs, not memory**: a safety claim you cannot cite is a claim the stakeholder can dismiss.
3. Reconcile the record. The vault holds dated decisions that later sessions partially reverse; a conflict between two dates is itself a finding and becomes a numbered decision, not a footnote.

Output first: a **content spec** markdown beside the report. It is the source of truth for wording, decisions, and what each stakeholder must supply. The build renders it and does not change its meaning. See `templates/content-spec.md`.

### 2. Build the objections-to-resolutions table

This is the core of the pack: for each concern the stakeholder's own team will raise, the true state of the tool, and our resolution. Shape:

| <Stakeholder> concern | What is actually true | Our resolution |
|---|---|---|
| stated as the stakeholder would state it | what the docs support, without downplaying the risk | a concrete control, naming where it is enforced |

Rules:
- Rows are concerns in the stakeholder's voice: data leaving the building, commands running on company machines, users disabling controls, credentials on endpoints, installs without admin rights, malicious instructions in untrusted input, remote control channels, audit retention, support load, network scope.
- Every resolution is an action we take or a setting we lock, never an assurance.
- Where a risk is real, say so plainly. A table that resolves every row reads as advocacy and loses the reader.
- Name the compliance hooks the stakeholder cares about (log retention, data residency, data protection law) only where the control actually addresses them.

### 3. Turn the pack into decisions

Each numbered decision carries: **proposal**, **why**, **what we need from the stakeholder** (fields they fill: names, dates, owners, periods), and a verdict (Approve / Approve with changes / Not approved) with a notes box. A note is required on any verdict that is not a clean approve.

Close the pack with **one** decision for Deep where his own earlier ruling conflicts with the current direction. Options plus a recommendation, and say which downstream item must be reworded if he picks differently.

Where a period or limit is not stated anywhere, propose one and flag it to Deep as a number you invented for him to change. Never let a made-up figure present itself as settled policy.

### 4. Hand the build to the frontend lane

UI does not get built inline. `kanban_create(assignee="frontend", ...)` with a full brief:

- **Goal**, one line, naming both modes.
- **Content source**: absolute path to the content spec, with the instruction that wording may be tightened but meaning does not change.
- **Output path**: absolute, beside the spec.
- **Must have**: every behavior the stakeholder depends on. For this class: a single file with **zero external requests** (the audience is the team judging our security, so a page that phones home undermines the ask), mode toggle, per-decision verdict plus required note, reviewer name, a progress count of decisions made, persistence across reload with a confirmed clear action, a send-back that opens an email with the full plain text plus copy and download fallbacks, a print stylesheet as the record, labels, keyboard use, WCAG AA contrast, and a 375px width.
- **Do not touch**: source files, the record files. No deploy, no upload, no sending. Deep shares it himself.
- **Proof**: what must come back in the handoff. Always: the decoded body of the generated email, a reload showing answers persist, a network log showing zero external requests, and a dash count.

Pass `skills` on the card so the visual gate loads (`frontend-design`, the brand skill, `visual-verify`), and require `kanban_request_review` back to `default` rather than a bare `kanban_complete`, so the artifact is opened before Deep ever sends it.

### 5. Report with a decision card

Report what is built and how it was verified, where the files are, and what is still his. Every judgment you made for him (numbers you proposed, scope you assumed) gets named in the reply. If a numbered decision depends on an unanswered question, block a card with the options and your recommendation first.

## Pitfalls

- **Ask format questions once, in one batch.** Two rounds of clarification on output format and then on how it will be shared stall a one-file deliverable that could have been built. Batch what you cannot infer (format, who receives it, channel) in a single ask; assume everything else and state the assumption.
- **Do not ship the report and the pack as two truths.** The report is the reasoning, the pack is the sign-off surface. Both cite the same numbered decisions, or the stakeholder signs one thing and the team builds another.
- **Never let the async path depend on a backend.** The file is emailed as an attachment, so server-side submit, auth, and hosted links are unavailable. Mailto with a correctly URL-encoded body, clipboard copy, and a file download are the three routes; decode the body in a test, because clients silently truncate anything too long.
- **Do not soften an unresolved conflict into a note.** If the record contradicts itself, it becomes a numbered decision with a recommendation.
- **No em dashes in any output**, vault write, visible page text, or generated email body. Check the source spec and the generated email text, not only the page.
- **Internal references do not leave the vault.** Precedent ids, other programs' ticket numbers, and decision-desk dates belong in the reasoning report Deep reads, not in the pack the stakeholder opens.
