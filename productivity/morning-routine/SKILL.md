---
name: morning-routine
description: >
  Multi-skill orchestrator for Sreedeep's daily startup routine — runs around 3pm (his day-start).
  Chains four skills in sequence: (1) vault-linker to connect yesterday's loose context,
  (2) celsus-cortex to analyze yesterday's wins and surface today's priorities from email,
  (3) interactive-quiz to interview the user about energy/focus/goals,
  (4) day-planner to produce a productivity plan. Use this skill whenever the user says
  "morning routine", "start my day", "daily kickoff", "afternoon planning", "plan my day",
  "what should I focus on today", or any request to review yesterday and plan today.
  MANDATORY TRIGGER for daily planning workflows. This skill coordinates other skills —
  it does not replace them. Each sub-skill can still be invoked independently.
---

# Morning Routine — Daily Orchestrator

> "The compound effect of a great daily routine is the most underestimated force in business."

## What This Skill Does

This is a **conductor**, not an instrument. It orchestrates four specialized skills into a
single coherent daily ritual that transforms scattered context into a focused productivity plan.

The routine typically runs around **3pm IST** (Sreedeep's operational day-start), but can be
triggered anytime.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  MORNING ROUTINE                         │
│               (This Orchestrator)                        │
│                                                          │
│  ┌──────────────┐                                        │
│  │ Phase 1      │  CONTEXT GATHERING                     │
│  │ Vault Linker │──→ Link yesterday's notes              │
│  │              │──→ Summarize Outlook emails (24h)      │
│  │              │──→ Inject email digest into Daily Note  │
│  │              │──→ Surface Apple Notes stubs            │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Phase 2      │  ANALYSIS                              │
│  │ Celsus Cortex│──→ What went well yesterday?           │
│  │              │──→ What needs follow-up?               │
│  │              │──→ What's urgent from email?           │
│  │              │──→ Which efforts moved forward?        │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Phase 3      │  INTERVIEW                             │
│  │ Interactive  │──→ Energy level check                  │
│  │ Quiz         │──→ Focus area selection                │
│  │              │──→ Time availability                   │
│  │              │──→ Meeting prep needs                  │
│  │              │──→ Personal objectives for the day     │
│  │              │──→ Apple Notes context questions       │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Phase 4      │  PLANNING                              │
│  │ Day Planner  │──→ Map calendar constraints            │
│  │              │──→ Time-block by energy curve          │
│  │              │──→ Prioritize tasks by impact          │
│  │              │──→ Output: Productivity Plan           │
│  └──────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

## Phase-by-Phase Execution

### Phase 1: Context Gathering (Vault Linker)

**Goal:** Ensure yesterday's context is fully connected before any analysis happens.

**Steps:**

1. **Identify yesterday's daily note**
   - Path: `Calendar/Daily Notes/YYYY-MM-DD.md` (yesterday's date)
   - If it doesn't exist, note this — the analysis phase will work with whatever context is available

2. **Run vault-linker scan on yesterday's note**
   - Follow vault-keeper skill methodology (or vault-linker if separately available)
   - Focus on: unlinked person mentions, company mentions, effort references
   - Apply fixes automatically (Full Autopilot mode)

3. **Summarize recent email communications**
   - **First check** `Atlas/Email Triage/YYYY-MM-DD.md` (previous business day's triage note) — the automated email triage runs at 9 PM IST and this is the preferred source. Read the "Tasks Extracted for Morning Routine" section directly.
   - If the triage note doesn't exist or is stale, fall back to live Outlook/email access if available
   - If no email access at all: ask the user to briefly describe their key communications
   - **Output:** A structured email digest

4. **Scan for unprocessed Apple Notes stubs**
   - Check `Inbox/Apple Notes/` for any `.md` files with `status: needs-context` in their frontmatter
   - Read each stub and extract the `NEEDS CONTEXT:` questions embedded within
   - Compile a list: **stub title → list of embedded questions**
   - If no stubs found: skip this step silently
   - If stubs found: hold them for Phase 3 (the quiz will ask about them)

5. **Inject context into today's daily note**
   - Create today's daily note if it doesn't exist (use celsus-cortex Workflow 2 or vault-keeper)
   - Add the email digest under `📧 Email & Communications`
   - Link any newly discovered people, companies, or efforts

**Handoff to Phase 2:** Yesterday's note is fully linked. Today's note exists with email context injected. Apple Notes stubs (if any) are queued for Phase 3.

---

### Phase 2: Analysis (Celsus Cortex)

**Goal:** Understand what happened yesterday and surface what matters today.

**Steps:**

1. **Read yesterday's daily note** (now fully linked from Phase 1)
   - Parse completed tasks, effort progress, meeting outcomes, ideas captured

2. **Positive momentum analysis**
   - What actions from yesterday are heading in the right direction?
   - Which efforts showed progress?
   - What should the user double down on today?
   - Present as: "🟢 Yesterday's Wins" (2-4 bullet points)

3. **Follow-up identification**
   - What was started but not finished?
   - What tasks were carried forward?
   - Any meeting action items that need attention?
   - Present as: "🟡 Needs Follow-Up" (2-4 bullet points)

4. **Email-driven priorities**
   - From the Phase 1 email digest, what's urgent or time-sensitive?
   - Any emails that need a response today?
   - External commitments or deadlines surfaced?
   - Present as: "🔴 From Your Inbox" (2-4 bullet points)

5. **Effort status snapshot**
   - Quick status of each active effort (from `Efforts/Active/`)
   - Flag any that haven't been touched in 3+ days
   - Present as a compact table

6. **Apple Notes preview** *(only if stubs found in Phase 1)*
   - Briefly mention: "I also found N Apple Notes captured last night that need a bit of context from you — I'll ask about them during the interview."
   - This sets expectations without interrupting the analysis flow

**Handoff to Phase 3:** User has a clear picture of yesterday + today's landscape. Now we need their input.

---

### Phase 3: Interview (Interactive Quiz)

**Goal:** Gather the user's subjective state — energy, priorities, available time, focus preferences.
**Secondary goal:** Resolve context gaps in any Apple Notes stubs captured overnight.

**This phase generates an interactive HTML quiz** using the interactive-quiz skill.

The quiz serves as a "morning interviewer" — it's not just collecting data, it's helping the user
think through their day. The interaction patterns should feel engaging, not like a chore.

**Quiz Structure (6-7 base questions + Apple Notes questions, scrollable layout):**

See `references/morning-quiz-blueprint.md` for the full quiz specification including
exact questions, interaction patterns, and state management.

**Apple Notes Integration — Dynamic Questions:**

If Phase 1 found stubs in `Inbox/Apple Notes/` with `NEEDS CONTEXT:` prompts, add one
question per stub to the quiz (after the standard 6-7 base questions):

```
For each stub:
  Section header: "📱 Apple Note: {stub title}"
  For each NEEDS CONTEXT question in the stub, ask it as a text input or select
  (depending on the nature of the question — use judgment)
```

Keep it conversational — frame it as: "You jotted something down last night. Let me make sure
it ends up in the right place in your vault." The user shouldn't feel interrogated; they should
feel like the vault is learning from them.

**After the quiz is submitted:**
For each Apple Notes stub that had questions answered:
1. Read the stub from `Inbox/Apple Notes/`
2. Update the frontmatter: change `status: needs-context` to `status: processed`
3. Replace each `NEEDS CONTEXT: {question}` block with the user's actual answer
4. Add/update wikilinks based on the answers (e.g., if they said "this is about Cirralogix", add `[[Cirralogix]]`)
5. Move or copy the note to its proper vault location:
   - If it's about a person → `Atlas/People/`
   - If it's about a company or client → `Atlas/Companies/` or `Atlas/Clients/`
   - If it's a project idea or effort → `Efforts/Active/` or `Inbox/`
   - If it's a general insight or resource → `Inbox/` (let vault-keeper sort it later)
   - If it's clearly just a task or reminder → add to today's daily note Tasks section
6. Delete the original stub from `Inbox/Apple Notes/` after moving

**Key Design Principles:**
- Each question uses a DIFFERENT interaction pattern (diversity rule from interactive-quiz skill)
- Dark theme with glassmorphism (matches the premium feel)
- Questions are pre-populated with context from Phase 2 (e.g., effort names appear as options)
- The summary output is structured for the Day Planner to consume
- Total completion time: ~2 minutes (+ ~30 seconds per Apple Note stub)

**Handoff to Phase 4:** Quiz responses provide energy level, priority ranking, time budget, focus preference, meeting prep needs, and resolved Apple Notes context.

---

### Phase 4: Planning (Day Planner)

**Goal:** Combine all context into an actionable productivity plan.

**Inputs consumed:**
- Phase 2 analysis (wins, follow-ups, inbox priorities, effort status)
- Phase 3 quiz responses (energy, priorities, time, focus mode)
- Today's calendar (if available)
- Active efforts from `Efforts/Active/`

**The Day Planner skill handles this phase.** See `.skills/skills/day-planner/SKILL.md`.

**Output:** A structured productivity plan saved to today's daily note under `🎯 Day at a Glance`.

---

## Adaptive Behavior

The routine adapts based on what's available:

| What's Available | Behavior |
|-----------------|----------|
| Full email access + calendar | Complete 4-phase routine with rich context |
| Email access, no calendar | Skip calendar mapping, use quiz time-budget instead |
| No email access | Phase 1 asks user for verbal summary; Phase 2 focuses on vault context |
| No yesterday daily note | Phase 1-2 are lighter; Phase 3-4 still run fully |
| User says "quick mode" | Skip quiz, use defaults: medium energy, top 3 priorities, standard day |
| Apple Notes stubs present | Phase 3 quiz gets extra questions; stubs processed and moved after quiz |
| No Apple Notes stubs | Apple Notes step runs silently and is skipped — no mention to user |

## Timing & Scheduling

The routine is designed for Sreedeep's ~3pm day-start but adapts:
- **Before 12pm:** "Early start? Let's make the most of it." — Extends the planning horizon.
- **12pm-4pm:** Standard routine — full 4 phases.
- **After 4pm:** "Late start" mode — focuses on what's still achievable today, looks ahead to tomorrow.
- **After 8pm:** "Tomorrow prep" mode — skips today planning, sets up tomorrow's priorities.

## Integration Points

| Skill | Path | How It's Used |
|-------|------|---------------|
| **Vault Keeper** | `.skills/skills/vault-keeper/` | Phase 1 — link yesterday's context |
| **Celsus Cortex** | `.skills/skills/celsus-cortex/` | Phase 2 — analyze yesterday, create daily note |
| **Interactive Quiz** | `.skills/skills/interactive-quiz/` | Phase 3 — morning interview + Apple Notes Q&A |
| **Day Planner** | `.skills/skills/day-planner/` | Phase 4 — productivity plan |
| **daily-note-recap** | `.skills/skills/daily-note-recap/` | Writes Apple Notes stubs to `Inbox/Apple Notes/` |

Each skill is independently invocable. The morning routine's value is the **orchestration** —
ensuring they run in the right order with the right data flowing between phases.

## Apple Notes Vault Loop (End-to-End)

Here's the full lifecycle of an Apple Note through the system:

```
Evening (automated):
  daily-note-recap runs at 00:30 IST
    → accesses Apple Notes via computer-use
    → creates stub in Inbox/Apple Notes/YYYY-MM-DD - {title}.md
    → stub has status: needs-context + embedded NEEDS CONTEXT: questions

Morning (interactive):
  morning-routine Phase 1 scans Inbox/Apple Notes/
    → finds stubs with status: needs-context
    → queues questions for Phase 3

  morning-routine Phase 3 quiz includes Apple Notes questions
    → user answers in the quiz UI

  Post-quiz processing:
    → stubs updated with answers
    → wikilinks applied
    → notes moved to correct vault location
    → original stubs deleted from Inbox/Apple Notes/
```

This ensures Apple Notes captured on the go never get lost — they always end up properly
contextualized and linked in the vault within 24 hours.

## Quick Invocation

Any of these trigger the full routine:
- "morning routine"
- "start my day"
- "plan my day"
- "daily kickoff"
- "afternoon planning"
- "what should I focus on today"
- "run the routine"

For individual phases:
- "just link yesterday's notes" → Phase 1 only (vault-linker/vault-keeper)
- "what happened yesterday" → Phase 2 only (cortex analysis)
- "interview me" → Phase 3 only (quiz)
- "plan my afternoon" → Phase 4 only (day planner)
- "process my Apple Notes" → Phase 1 (scan) + Phase 3 (ask questions) only

## Iteration Log

| Date | Change | Why |
|------|--------|-----|
| Initial | 4-phase orchestrator created | First daily routine skill |
| 2026-03-16 | Email triage note integration | Stop re-scanning Outlook; use pre-built triage notes |
| 2026-03-26 | Apple Notes integration | Phase 1 scans `Inbox/Apple Notes/` stubs, Phase 3 resolves context gaps via quiz questions. Full lifecycle: daily-note-recap writes stubs → morning-routine contextualizes and files them |
