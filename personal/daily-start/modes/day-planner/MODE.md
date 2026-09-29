<!-- Mode file, formerly the standalone skill `day-planner`. Relative paths below resolve from modes/day-planner/. -->

# Day Planner, Productivity Planning

> Turn scattered priorities into focused time blocks that respect your energy and constraints.

## What This Skill Does

Takes four inputs and produces one output:

```
Inputs:                              Output:
┌─────────────────┐
│ 📅 Calendar     │──┐
│ ⚡ Energy Level  │──┤
│ 🎯 Priorities   │──┼──→  📋 Structured Productivity Plan
│ ⏰ Time Budget  │──┤      (time blocks + task priorities)
│ 🧠 Focus Mode   │──┘
└─────────────────┘
```

## Input Sources

The Day Planner accepts context from multiple sources, adapting based on what's available:

### When Used via Morning Routine (Phase 3)
All inputs come pre-populated from earlier phases:
- **Calendar:** Pulled from calendar integration (if available)
- **Energy:** From quiz response (Phase 2)
- **Priorities:** From vault-keeper analysis (Phase 1) + quiz ranking (Phase 2)
- **Time Budget:** From quiz response (Phase 2)
- **Focus Mode:** From quiz response (Phase 2)
- **Tasks:** Parsed from `TASKS.md` at vault root (same source the dashboard reads)

### When Used Standalone
Ask the user directly:
1. "What time do you have available?" (e.g., "3pm to 8pm", "full day", "just 2 hours")
2. "How's your energy?" (high / medium / low / recovering)
3. "What are your top priorities?" (list or describe)
4. "Any fixed commitments?" (meetings, calls, deadlines)
5. "Deep work or multitask mode?" (focus vs. variety)

## Planning Algorithm

### Step 1: Map the Time Landscape

Establish the available time window:

```
Available Window: [start_time] → [end_time]
Total Hours: X.X

Fixed Blocks (non-negotiable):
├── 4:00 PM, Call with Gary (30min)
├── 5:30 PM, Team standup (15min)
└── 7:00 PM, Dinner break (30min)

Flexible Time: Y.Y hours across Z blocks
```

If calendar access is available, pull fixed blocks automatically. Otherwise, use what the user provides.

### Step 2: Apply the Energy Curve

Different energy levels get different task sequencing. The principle: **match task cognitive demand to available energy.**

| Energy Level | Strategy | Best Time Blocks |
|-------------|----------|-----------------|
| 🔴 **High** | Front-load deep work. Save admin for later. | Deep work → Strategic → Admin → Review |
| 🟡 **Medium** | Alternate deep and light. Build momentum with a quick win first. | Quick win → Deep work → Break → Light work → Review |
| 🟠 **Low** | Start with lowest-friction tasks. Protect energy for one priority item. | Admin → One priority task → Light work → Planning tomorrow |
| 🔵 **Recovering** | No deep work. Focus on review, organization, and communication. | Email → Review → Light decisions → Tomorrow prep |

### Step 3: Prioritize Tasks

Use the **Impact × Urgency matrix** to rank tasks:

```
          HIGH URGENCY          LOW URGENCY
        ┌──────────────────┬──────────────────┐
HIGH    │ 🔴 DO NOW         │ 🟡 SCHEDULE      │
IMPACT  │ (time block first)│ (deep work block)│
        ├──────────────────┼──────────────────┤
LOW     │ 🟠 DELEGATE/QUICK │ 🟢 BATCH/DEFER  │
IMPACT  │ (≤15 min or hand  │ (end of day or   │
        │  off to team)     │  this week)      │
        └──────────────────┴──────────────────┘
```

For each task, determine:
- **Estimated time:** How long will this realistically take?
- **Cognitive load:** Deep focus, moderate attention, or autopilot?
- **Dependencies:** Does anything need to happen first?
- **Effort linkage:** Which active effort does this serve? (Link to `Efforts/Active/`)

### Step 4: Construct Time Blocks

Rules for time blocking:
1. **Deep work blocks:** Minimum 45 minutes, maximum 90 minutes. One break in between.
2. **Admin blocks:** Batch small tasks together. 20-30 minutes.
3. **Buffer time:** Add 10-15 minutes between blocks for transitions and unexpected items.
4. **Energy protection:** Never schedule deep work in a low-energy slot.
5. **Meeting bookends:** 10 minutes before meetings for prep, 5 minutes after for notes.

### Step 5: Generate the Plan

The output is a structured daily plan. Format depends on context:

#### For Daily Note Injection (Morning Routine Mode)

When the plan is being injected into the daily note's `🎯 Day at a Glance` section:

```markdown
## 🎯 Day at a Glance

**Energy:** 🟡 Medium | **Focus:** Deep work blocks | **Available:** 3pm-8pm (4.5h flexible)

### Time Blocks

| Time | Block | Task | Effort | Status |
|------|-------|------|--------|--------|
| 3:00-3:15 | ⚡ Quick Win | Reply to [[Gary]] re: pipeline update | [[ChampIQ Experiment]] | ⬜ |
| 3:15-4:00 | 🧠 Deep Work | Build ChampConnect webhook integration | [[ChampIQ Product Build]] | ⬜ |
| 4:00-4:30 | 📞 Meeting | Call with [[Gary]], weekly pipeline review | [[ChampIQ Experiment]] | ⬜ |
| 4:30-4:40 | 📝 Buffer | Meeting notes + action items |, | ⬜ |
| 4:40-5:25 | 🧠 Deep Work | Draft email sequences for [[Lake B2B]] campaign | [[Email Outreach Engine MVP]] | ⬜ |
| 5:25-5:30 | ☕ Break |, |, |, |
| 5:30-5:45 | 📞 Meeting | Team standup |, | ⬜ |
| 5:45-6:15 | 📋 Admin | Clear inbox, respond to [[Syed Noor]] |, | ⬜ |
| 6:15-7:00 | 🧠 Deep Work | Review [[Corporate Focus Pivot Q1]] strategy doc | [[Corporate Focus Pivot Q1]] | ⬜ |
| 7:00-7:30 | 🍽️ Break | Dinner |, |, |
| 7:30-8:00 | 🔮 Tomorrow | Review day, update efforts, set tomorrow's top 3 |, | ⬜ |

### Today's Top 3
1. **ChampConnect webhook**, [[ChampIQ Product Build]] needs this for WhatsApp integration
2. **Lake B2B email sequences**, [[Gary]] needs these for Monday's campaign launch
3. **Corporate pivot doc**, Decision needed by end of week

### Parked (if time allows)
- Review [[Preeti]]'s SEO audit findings
- Update [[Champions Club]] membership page copy
```

#### For Standalone Mode (Quick Output)

Present a concise plan in the conversation, then offer to save it.

## Context Awareness

The Day Planner understands the Celsus vault structure and uses it:

- **TASKS.md (primary task source):** Read from vault root. This is the same file the Celsus
  dashboard (`dashboard.html`) reads to populate its task board. Tasks in TASKS.md use three
  sections: `Active`, `Waiting On`, and `Someday`. Tags: `[e:EffortName]` links a task to an
  effort, `[c:CompanyName]` links to a company, `[u:must|nice|skip]` sets urgency. Parse these
  tags when building the priority matrix and time blocks.

- **Active Efforts:** Reads `Efforts/Active/` for project context. Cross-reference with TASKS.md
  so a task tagged `[e:ChampGraph Build]` maps to the right effort description and status.

- **People:** Links people to their efforts so the user sees "call [[Gary]]" mapped to "[[ChampIQ Experiment]]"

- **Products:** Maps tasks to products when relevant

- **Yesterday:** If yesterday's daily note exists, checks for carried-forward tasks

**TASKS.md format reference:**

```markdown
## Active
- [ ] Task text [e:EffortName] [c:CompanyName] [u:must]
- [ ] Another task [e:EffortName] [u:nice]

## Waiting On
- [ ] Blocked task, waiting on Gary since April 15 [e:ChampIQ Experiment]

## Someday
- [ ] Low-priority idea [u:skip]
```

When the planner references tasks in its output, use the exact task text from TASKS.md so the
user can cross-reference with the dashboard task board without confusion.

## Adaptation Rules

| Scenario | Adaptation |
|----------|-----------|
| Only 2 hours available | Maximum 3 tasks. No deep work blocks over 45 min. |
| Full day (8+ hours) | Include lunch break, afternoon reset, and end-of-day review. |
| High urgency day | Skip "nice to have" tasks entirely. Focus on 🔴 quadrant only. |
| Recovery day | Cap at 3 light tasks. Include rest blocks. |
| Meeting-heavy day | Plan around fixed blocks. Use gaps for admin, not deep work. |
| Friday | Include weekly review block. Lighter planning, reflection focus. |
| Monday | Include weekly kickoff items. Reference last week's review if available. |

## Quick Invocation

- "plan my day" → Full standalone planning flow
- "time block my afternoon" → Quick time-block generation
- "what should I work on?" → Priority ranking only (skip time blocks)
- "schedule these tasks: X, Y, Z" → Direct task-to-time mapping
- "I have 2 hours, what's most important?" → Constrained priority filter
