---
name: meeting-intake
description: >
  Processes meeting notes, summaries, transcripts, or recordings into structured vault knowledge and actionable tasks.
  MANDATORY TRIGGER for: pasted meeting notes, meeting summaries, Zoom transcripts, "here are my notes from",
  "meeting with [person]", "just got out of a call", "summary from today's meeting", any block of text that looks
  like meeting minutes or action items, uploaded audio/video meeting files, or any message that starts with a
  person's name followed by discussion points. Also trigger when the user drops a wall of text with names,
  decisions, and next steps without any other instruction. The intent is: "file this, find my tasks, update my system."
  If the input even vaguely resembles meeting output, use this skill. Do NOT wait for the user to say "meeting notes."
---

# Meeting Intake

You are processing meeting content for Sreedeep Surapaneni (Deep/Champ), Group CMO of Champions Group.
Your job: turn raw meeting output into structured vault knowledge and surface HIS specific action items.

## Why This Skill Exists

Sreedeep sits across 12 companies and attends many meetings daily. The gap between "meeting happened" and
"tasks are tracked + context is searchable" is where things fall through cracks. This skill closes that gap
automatically. Every meeting should leave behind: (1) a searchable vault note, (2) tasks in TASKS.md for
anything Sreedeep personally owns.

## Input Formats

1. **Pasted text** (most common): Raw meeting notes, summary + next steps, bullet points, transcript excerpts.
   The user will often just paste content with zero preamble. Treat any large block of unstructured text with
   names, decisions, and action items as meeting input.

2. **Uploaded audio/video**: Transcribe first (use bash with available transcription tools), then process.
   If transcription tools are unavailable, tell the user and ask them to paste the transcript instead.

3. **Zoom connector** (future): When Zoom MCP is connected, pull recordings and transcripts directly.
   Build the processing pipeline so it works regardless of input source.

## Processing Pipeline

### Step 1: Parse and Extract Structure

From the raw input, identify:

| Field | How to find it |
|-------|---------------|
| **Meeting title** | Explicit title, or infer from participants + topic. Format: "Person x Person: Topic" or descriptive name |
| **Date** | Explicit date, or today's date. Always absolute (YYYY-MM-DD), never relative. |
| **Attendees** | Names mentioned. Match against known people in CLAUDE.md B2. Use [[wikilinks]] for known contacts. |
| **Company/Effort** | Which company or effort does this relate to? Match against CLAUDE.md B3/B4/B7. |
| **Summary** | 3-5 sentence executive summary of what was discussed and decided. |
| **Key decisions** | Anything agreed upon, approved, or rejected. |
| **Action items (ALL)** | Every next step mentioned, regardless of owner. |
| **Sreedeep's action items** | ONLY tasks that Sreedeep personally needs to do or follow up on. |

### Step 2: Create Vault Meeting Note

Write to: `Calendar/Meetings/YYYY-MM-DD-Meeting-Name.md`

Template:

```markdown
---
date: YYYY-MM-DD
attendees:
  - "[[Person Name]]"
company: "[[Company Name]]"
effort: "[[Effort Name]]"
tags:
  - "#meeting"
---

# Meeting Title

## Summary
[3-5 sentence executive summary]

## Key Decisions
[Each decision made]

## Action Items

| Owner | Task | Due | Status |
|-------|------|-----|--------|
| [[Person]] | Task description | Date or TBD | Open |

## Notes
[Additional context, quotes, or details worth preserving]
```

### Step 3: Update TASKS.md

For each action item where Sreedeep is the owner (or where ownership is ambiguous and he is the most likely person):

1. Read the current TASKS.md from vault root (`/Users/deep/Celsus/TASKS.md`)
2. Add new tasks under the `## Active` section
3. Use the exact format: `- [ ] **Task title** - Description. From [meeting name] [date]. [e:Effort Name] [c:Company]`
4. If the task maps to an existing effort, use that effort tag. Otherwise use `[e:Inbox]`.
5. Do NOT duplicate tasks that already exist in TASKS.md. Check existing tasks first.

### Step 4: Cross-link

- If attendees have vault notes in `Atlas/People/`, the meeting note's wikilinks already create backlinks.
- If the meeting relates to an active effort, consider whether the effort note needs a brief update.
- Update [[Meetings MOC]] if it exists (add a line linking to the new meeting note).

### Step 5: Confirm with User

After processing, show a concise summary:

```
Filed: Calendar/Meetings/YYYY-MM-DD-Meeting-Name.md
Tasks added to TASKS.md: [count]
  - Task 1 title [e:Effort] [c:Company]
  - Task 2 title [e:Effort] [c:Company]
```

If any action items had ambiguous ownership, flag them:
"These might also be yours. Want me to add them? [list]"

## Ownership Detection

**Sreedeep likely owns it if:**
- His name is explicitly mentioned as owner
- It involves strategic decisions, marketing, product direction, or cross-company coordination
- It is about following up with someone (he is often the coordinator)
- No other owner is specified and the task requires senior decision-making
- It involves his Deep Focus companies (Lake B2B, SPAN, Cirralogix, Recruit Champ)

**Sreedeep likely does NOT own it if:**
- Another person is explicitly assigned
- It is a technical implementation task for a developer (Hemang, Harsha, etc.)
- It is an operational task for a specific team member (Preeti for SEO, Murugan for nurturing)
- It is a finance/accounting task (Srivatsav's domain)

## Edge Cases

- **Multiple meetings in one paste**: Create separate vault notes for each. One meeting = one file.
- **No clear action items**: Still create the vault note. The context is valuable even without tasks.
- **Recurring meeting update**: If a meeting note already exists for this date + title, append rather than overwrite.
- **Vague notes**: If input is too sparse, ask one round of clarifying questions (max 3) via AskUserQuestion, then proceed.
- **Uncertainty signals**: If the user trails off with "things like that", "right?", "you know?" after describing the meeting, that means they are unsure about that part. Clarify before filing.
