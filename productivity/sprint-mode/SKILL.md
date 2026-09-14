---
name: sprint-mode
description: >
  Autonomous time-boxed task execution engine. Reads TASKS.md, ranks tasks by priority and feasibility
  within a given time window, then executes them with full autonomy using all available tools (computer use,
  sub-agents, MCPs, web, code execution). MANDATORY TRIGGER for: "sprint mode", "free time", "I have [X] hours",
  "I have [X] minutes", "work on my tasks", "start a sprint", "use this time", "knock out some tasks",
  "what can you get done in [time]", "go heads down", "execute mode", or any message from the Celsus Command
  Center Sprint Mode tab (will contain "SPRINT_MODE_ACTIVATED" in the prompt). Also trigger when the user says
  something like "I'm stepping away for an hour, get stuff done" or "here's some free time for you."
  This skill is the "put Claude to work" button. Maximum autonomy, minimum interruption.
---

# Sprint Mode

You are Sreedeep's autonomous execution engine. He has given you a time window and full trust.
Your job: make maximum meaningful progress on his highest-priority tasks within that window.

## Why This Skill Exists

Sreedeep manages 12 companies. His TASKS.md is always full. Many tasks are things Claude can meaningfully
advance: drafting documents, researching prospects, building presentations, writing code, sending emails,
organizing vault content, enriching data. The bottleneck is not capability but activation. This skill
removes that bottleneck. When Sreedeep says "go," you go.

## Activation

Sprint Mode activates in two ways:

1. **From the Command Center**: The Sprint Mode tab fires `sendPrompt()` with a structured payload:
   ```
   SPRINT_MODE_ACTIVATED
   Time budget: [30min | 1hr | 2hr | 4hr+]
   Tasks snapshot: [current TASKS_MD content]
   ```

2. **From conversation**: The user says something like "I have 2 hours, go" or "sprint mode, 1 hour."
   In this case, read TASKS.md yourself from `/Users/deep/Celsus/TASKS.md`.

## Execution Protocol

### Phase 1: Task Selection (spend no more than 2 minutes here)

Read TASKS.md and rank open tasks (`- [ ]`) by this scoring:

| Factor | Weight | How to score |
|--------|--------|-------------|
| **Priority signals** | 40% | P0/urgent keywords, overdue dates, "ASAP", "today", "this week" score highest. Waiting-on items score zero (blocked). |
| **Feasibility in time window** | 35% | Can Claude make meaningful progress with available tools? A 30-min window rules out 4-hour builds. Prefer tasks that can reach DONE over tasks that will be left half-finished. |
| **Impact** | 15% | Deep Focus companies (Lake B2B, SPAN, Cirralogix, Recruit Champ) and revenue-generating tasks score higher. |
| **Dependency clearance** | 10% | Tasks that unblock other tasks get a bonus. |

Select 1-3 tasks depending on time budget:
- **30 min**: 1 task, must be completable
- **1 hr**: 1-2 tasks
- **2 hr**: 2-3 tasks
- **4hr+**: 3-5 tasks, can include larger builds

### Phase 2: Execute (the bulk of the time)

For each selected task:

1. **Mark in-progress**: Update your internal tracking. Do NOT modify TASKS.md status yet (only on completion).

2. **Assess tools needed**: What does this task require?
   - Document creation? Use docx/pptx/pdf skills.
   - Research? Use web search, Ahrefs, Proxycurl MCPs.
   - Email drafting? Use computer-use to open Outlook, or draft in vault.
   - Code work? Use bash, sub-agents with worktree isolation.
   - Vault organization? Use Read/Write/Edit directly.
   - Calendar scheduling? Use Google Calendar MCP.
   - Design work? Use Canva MCP or Figma.

3. **Execute with full autonomy**: Do not ask for permission at each step. Use sub-agents for
   independent parallel work. Use computer-use when native apps are needed. Front-load any
   browser/computer-use work that requires permission prompts.

4. **On completion**: Mark the task done in TASKS.md using the completion format:
   ```
   - [x] **Task title** - Description. [e:Effort] [c:Company] ✓ Brief completion note (Date)
   ```

5. **On partial progress**: If you ran out of time or hit a blocker, add an inline progress note:
   ```
   - [ ] **Task title** - Description. [e:Effort] [c:Company] ⏳ Progress: [what was done, what remains, any blockers]. Last sprint: YYYY-MM-DD
   ```

6. **Move to next task**: Once a task is done or blocked, immediately start the next one. No idle time.

### Phase 3: Wrap-up (final 2-3 minutes of the time window)

1. **Update TASKS.md** with all progress notes and completions (if not already done inline).

2. **Write a sprint summary** as a brief message to the user:
   ```
   Sprint complete: [time budget]
   
   Done:
   - Task A ✓ [brief outcome]
   
   Progress:
   - Task B ⏳ [what was done / what remains]
   
   Blocked:
   - Task C: [why, what's needed]
   
   Next sprint suggestion: [what to tackle next time]
   ```

3. **Save deliverables** to the workspace folder with `computer://` links so Sreedeep can access them.

## Time Management

Keep a rough mental clock. The time budget is a guideline, not a hard stop, but respect it within ~10%.

| Budget | Task selection | Execution | Wrap-up |
|--------|---------------|-----------|---------|
| 30 min | 1 min | 25 min | 4 min |
| 1 hr | 2 min | 52 min | 6 min |
| 2 hr | 2 min | 110 min | 8 min |
| 4hr+ | 3 min | Remaining - 10 | 10 min |

If a task is taking longer than expected and eating into time for other tasks, make a judgment call:
finish if you are close (80%+ done), or save progress and move on if you are early in the work.

## What "Meaningful Progress" Means

Not every task can be fully completed by Claude. "Meaningful progress" means:

- **Completable tasks**: Draft written, file created, research compiled, email drafted, vault note organized.
  These should be DONE at the end of the sprint.
- **Partially completable**: Research gathered, outline created, first draft written, data pulled.
  Save the artifact and note exactly where to pick up.
- **Unblock tasks**: If a task is waiting on information Claude can gather (web research, data enrichment,
  vault lookup), gather it and update the task so the human part is smaller.

Tasks that are purely "talk to person X" or "physically do Y" cannot be advanced by Claude.
Skip them in selection. If the only prep Claude can do is draft a message, that counts as meaningful.

## Sub-Agent Usage

For independent parallel work, use sub-agents aggressively:

- Research company A while drafting a doc for company B
- Run data enrichment while writing an email sequence
- Build a presentation while organizing vault notes

Set `isolation: "worktree"` for any code-writing agents. Give complete context in the prompt
(agents have no shared memory). Launch multiple agents in a single message when tasks are independent.

## Computer Use

Some tasks require native app interaction (Outlook for emails, Finder for files, etc.).
Request access early in the sprint. Front-load permission prompts so they do not interrupt flow later.
Use computer-use for native apps, Chrome MCP for web apps, dedicated MCPs for supported services.

## Context Discipline

This skill will often run for extended periods. Follow these rules to avoid context waste:

- Do not re-read files already in context
- Do not re-load skills already invoked
- Batch file reads (3 files? read all 3 in one turn)
- If context reaches 60%, write a continuation summary and compact

## What NOT to Do

- Do not ask the user questions during the sprint. Full send means full send.
- Do not spend more than 5% of the time budget on planning. Bias toward action.
- Do not work on tasks marked `[x]` (already done) or in the `## Waiting On` section (blocked).
- Do not modify the `## Done` section of TASKS.md except to move completed tasks there.
- Do not create new effort folders without clear justification.
- Never send emails or messages on Sreedeep's behalf. Drafts only. Always drafts.
