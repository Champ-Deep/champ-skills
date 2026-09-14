# Morning Routine — Phase 5 Addition

## Where to Insert

Add the following Phase 5 block AFTER Phase 4 (Day Planner) and BEFORE the "Adaptive Behavior" section in the morning-routine SKILL.md.

---

### Phase 5: Meeting Prep (Meeting Prep Skill)

**Goal:** Ensure Sreedeep walks into every meeting prepared — with continuity from previous meetings, relevant context, and strategic questions ready.

**Steps:**

1. **Scan today's calendar**
   - Use `gcal_list_events` for today's date range (IST timezone)
   - Pull all meetings with their attendees, descriptions, and durations

2. **Classify each meeting**
   - Follow the Meeting Classification rules in `.skills/skills/meeting-prep/SKILL.md`
   - Categorize into: 🔴 DEEP / 🟡 MEDIUM / 🟢 LIGHT / ⚪ SKIP

3. **Present meeting summary to user**
   - Show classified list with prep tier recommendations
   - Auto-generate LIGHT and MEDIUM preps immediately
   - Ask which DEEP preps to run (resource-intensive)

4. **Generate prep documents**
   - For each meeting needing prep, follow the meeting-prep skill's data retrieval strategy
   - Pull context from: Google Calendar, Notion Meeting Notes, Celsus Vault, Google Drive
   - Generate prep documents at the appropriate depth tier

5. **Save and inject**
   - Save DEEP and MEDIUM preps to `Calendar/Meetings/` in the vault
   - Inject LIGHT preps into today's daily note under `📅 Meetings`
   - Update the Day Planner's time blocks to include meeting prep time

**Handoff:** Morning routine complete. User has a productivity plan AND meeting preps ready.

---

## Updated System Architecture (replace the existing one)

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
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Phase 4      │  PLANNING                              │
│  │ Day Planner  │──→ Map calendar constraints            │
│  │              │──→ Time-block by energy curve          │
│  │              │──→ Prioritize tasks by impact          │
│  │              │──→ Output: Productivity Plan           │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Phase 5      │  MEETING PREP                          │
│  │ Meeting Prep │──→ Scan today's calendar               │
│  │              │──→ Classify meetings by prep depth     │
│  │              │──→ Retrieve historical context          │
│  │              │──→ Generate prep documents              │
│  │              │──→ Save to vault + daily note          │
│  └──────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

## Updated Integration Points Table

Add this row to the existing table:

| **Meeting Prep** | `.skills/skills/meeting-prep/` | Phase 5 — scan calendar, classify meetings, generate prep docs |

## Updated Adaptive Behavior Table

Add this row:

| Meeting-heavy day | Phase 5 generates preps for all meetings; Day Planner (Phase 4) allocates buffer time before each |

## Updated "For individual phases" section

Add:
- "prep my meetings" → Phase 5 only (meeting prep)
