# Morning Interview Quiz, Blueprint

This is the specification for the interactive HTML quiz generated during Phase 3 of the
morning routine. The quiz serves as a "morning interviewer" that helps the user think
through their day while collecting structured data for the Day Planner.

## Quiz Metadata

- **Title:** "Daily Kickoff, {date}"
- **Subtitle:** "Your afternoon interviewer. ~2 minutes to a focused day."
- **Layout:** Scrollable (6-7 questions = all visible)
- **Theme:** Dark with glassmorphism, accent color `#7c3aed` (purple)
- **Time estimate badge:** "~2 min"

## Questions & Interaction Patterns

### Q1: Energy Check
**Question:** "How's your energy right now?"
**Pattern:** Animated Radio Cards
**Options:**
- 🔴 High Energy, "Ready to crush it. Deep work mode."
- 🟡 Moderate, "Solid. Can handle focused work with breaks."
- 🟠 Low, "Running on fumes. Keep it light."
- 🔵 Recovering, "Need a gentle day. Review and organize."
**Priority tag:** Critical (red)
**State key:** `energy`

### Q2: Priority Ranking
**Question:** "What matters most today?"
**Pattern:** Priority Ranking Tiles (tap-to-cycle: Skip → 🔥 Must Do → ⚡ Nice to Have)
**Options:** Dynamically populated from:
- Active efforts in `Efforts/Active/` (e.g., "[[ChampIQ Experiment]]", "[[Email Outreach Engine]]")
- Phase 2 inbox priorities (e.g., "Reply to [[Gary]] re: pipeline")
- Carried-forward tasks from yesterday
- Add 2-3 standing options: "Clear inbox", "Deep thinking time", "Team check-ins"
**Priority tag:** Critical (red)
**State key:** `priorities` (object mapping each item to must/nice/skip)

### Q3: Time Budget
**Question:** "How much time do you have today?"
**Pattern:** Gradient Slider
**Range:** 1 hour → 10 hours
**default:** 5 hours
**Labels:** "Quick Sprint" (left) → "Marathon Day" (right)
**Floating label shows:** "{X} hours"
**Priority tag:** Important (amber)
**State key:** `time_hours`

### Q4: Focus Mode
**Question:** "How do you want to work today?"
**Pattern:** Concept Cards (single-select with illustration)
**Options:**
- 🎯 **Deep Dive**, "Long focused blocks on 1-2 priorities. Minimize context-switching."
- ⚡ **Power Bursts**, "45-min sprints with breaks. Mix of deep and light work."
- 🔀 **Variety Pack**, "Jump between tasks. Good for admin-heavy or meeting-heavy days."
- 🌊 **Flow State**, "No fixed schedule. Work on whatever pulls you in."
**Priority tag:** Important (amber)
**State key:** `focus_mode`

### Q5: [[Meeting Prep]]
**Question:** "Any meetings you need to prep for?"
**Pattern:** Tag Builder (type + Enter to add pills)
**Placeholder:** "Type a meeting name and press Enter..."
**Pre-populated suggestions** (from calendar if available): upcoming meetings for today
**Priority tag:** Nice to Have (cyan)
**State key:** `meeting_prep` (array of strings)

### Q6: Today's Win
**Question:** "If today goes perfectly, what's the ONE thing you'll have accomplished?"
**Pattern:** Styled Textarea
**Placeholder:** "The single most important outcome for today..."
**Character limit:** 280 characters
**Priority tag:** Critical (red)
**State key:** `todays_win`

### Q7 (Optional): Wildcards
**Question:** "Anything else on your mind?"
**Pattern:** Split Drop Zones
**Left zone:** "🔥 Must Address Today", things not captured above
**Right zone:** "📌 Park for Later", things to remember but not today
**Priority tag:** Nice to Have (cyan)
**State key:** `wildcards_today` and `wildcards_later` (arrays)

## Summary Output Format

When "Generate Summary" is clicked, compile into this structured format:

```
═══ DAILY KICKOFF, {date} ═══

⚡ ENERGY: {High/Moderate/Low/Recovering}
⏰ TIME BUDGET: {X} hours
🎯 FOCUS MODE: {Deep Dive/Power Bursts/Variety Pack/Flow State}

🔥 MUST DO TODAY:
• {priority 1}
• {priority 2}
• {priority 3}

⚡ NICE TO HAVE:
• {priority A}
• {priority B}

📞 MEETINGS TO PREP:
• {meeting 1}
• {meeting 2}

🏆 TODAY'S WIN: {todays_win text}

🔥 ALSO ADDRESS:
• {wildcard_today items}

📌 PARKED FOR LATER:
• {wildcard_later items}
```

This output is designed to be copy-pasted directly into the Day Planner or into the daily note.

## Dynamic Contextualization

The quiz is not static, it should be regenerated each day with fresh context:

1. **Effort names** in Q2 come from scanning `Efforts/Active/` at generation time
2. **Inbox priorities** in Q2 come from Phase 2 analysis
3. **Meeting suggestions** in Q5 come from calendar data (if available)
4. **Yesterday's carried-forward tasks** appear in Q2 options
5. **The date** in the title updates automatically

When generating, read the celsus-cortex analysis output and inject relevant items into the quiz options.

## Interaction Pattern Reference

For implementation details of each pattern, refer to:
- `.skills/skills/interactive-quiz/SKILL.md`, Core patterns and implementation guide
- `.skills/skills/interactive-quiz/references/interaction-patterns.md`, CSS/JS snippets

Ensure the diversity rule is maintained: 6-7 questions should use at least 5 different patterns.
The quiz above uses: Animated Radio Cards, Priority Ranking Tiles, Gradient Slider,
Concept Cards, Tag Builder, Styled Textarea, and Split Drop Zones, 7 unique patterns for
7 questions. Maximum variety.
