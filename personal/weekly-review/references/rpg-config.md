# RPG Configuration -- Weekly Review Gamification System

## XP Awards

| Action | XP | Notes |
|--------|----|-------|
| Task completed | +10 | Each `[x]` checkbox in daily notes |
| Meeting attended | +15 | Each meeting in the Meetings table |
| Effort advanced | +25 | Effort whose status changed during the week |
| Deliverable shipped | +30 | Each asset in Sales Enablement section |
| Decision made | +20 | Each bullet in Decisions Made sections |
| Daily note written | +5 | Each day that has a daily note |
| Weekly review streak | +50 | Consecutive weeks with a completed weekly review |
| Perfect attendance | +25 | All 5 weekdays have daily notes |
| Zero carry-forward | +40 | All tasks completed, nothing carried to next week |

## Level Thresholds

| Level | Title | Cumulative XP Required | Badge |
|-------|-------|----------------------|-------|
| 1 | Apprentice | 0 | Bronze Shield |
| 2 | Journeyman | 200 | Silver Shield |
| 3 | Specialist | 500 | Gold Shield |
| 4 | Expert | 1000 | Platinum Shield |
| 5 | Master | 1800 | Diamond Shield |
| 6 | Grandmaster | 3000 | Crystal Shield |
| 7 | Legend | 5000 | Obsidian Shield |
| 8 | Mythic | 8000 | Dragon Shield |
| 9 | Transcendent | 12000 | Phoenix Shield |
| 10 | Eternal | 20000 | Cosmic Shield |

XP required for next level = threshold[current_level + 1] - cumulative_xp.
Progress percentage = (cumulative_xp - threshold[current_level]) / (threshold[current_level + 1] - threshold[current_level]) * 100.

## Character Classes

Classes are determined by the dominant activity category for the week. The primary signal is the quiz heat map (if available). The fallback is counting activity types from daily notes.

### Classification Logic

1. Count "activity points" per category:
   - **Strategy:** Decisions made + strategy-tagged efforts + quiz strategy dimension score
   - **Product:** Product/dev efforts + code sessions + product-tagged meetings
   - **Sales:** Sales meetings + deal-related deliverables + sales-tagged efforts
   - **Marketing:** Marketing efforts + content deliverables + marketing meetings
   - **Ops:** Ops meetings + operational tasks + vault maintenance

2. Calculate percentage for each category: `category_points / total_points * 100`

3. Assign class:
   - If any category > 40%: assign that category's class
   - If no category > 40%: assign "Multi-Class"
   - Ties: prefer the category with the higher quiz satisfaction score

### Class Definitions

| Class | Icon | Color | Flavor Text |
|-------|------|-------|-------------|
| Strategy Sage | Crystal Ball | #6D08BE (Purple) | "The board bends to your vision. You see three moves ahead." |
| Build Beast | Hammer | #E8033A (Red) | "Code flows through your veins. Another week, another ship." |
| Deal Closer | Handshake | #FFB703 (Gold) | "Revenue recognizes hustle. The pipeline bows to your persistence." |
| Growth Hacker | Rocket | #0095A0 (Teal) | "The funnel widens. Your campaigns echo across the market." |
| Ops Commander | Shield | #FF6903 (Orange) | "The machine runs because you maintain it. Unsung, essential." |
| Multi-Class | Star | linear-gradient | "A renaissance leader. Every dimension feels your presence." |

### Class Icons (Unicode/Emoji)

Use these in the HTML report:
- Strategy Sage: (crystal ball emoji or use text icon)
- Build Beast: (hammer/anvil)
- Deal Closer: (handshake)
- Growth Hacker: (rocket)
- Ops Commander: (shield)
- Multi-Class: (star/sparkles)

## Streak System

Track consecutive weeks with a completed weekly review in `weekly_xp_log.json`.

| Streak | Bonus | Message |
|--------|-------|---------|
| 1 week | +50 XP | "First flame lit. Keep it burning." |
| 2 weeks | +50 XP | "Consistency builds empires." |
| 3 weeks | +50 XP | "Three in a row. You're building momentum." |
| 4 weeks | +75 XP | "A full month of reviews. Discipline is your superpower." |
| 8 weeks | +100 XP | "Two months strong. Legends are forged in repetition." |
| 12 weeks | +150 XP | "Quarter complete. The data tells your story." |
| 26 weeks | +200 XP | "Half a year of weekly reviews. Unstoppable." |
| 52 weeks | +500 XP | "ONE YEAR. You have mastered the art of reflection." |

Streak resets to 0 if a week is missed (no weekly review generated).

## Weekly XP Log Schema

File: `Calendar/Weekly Reviews/weekly_xp_log.json`

```json
{
  "history": [
    {
      "week": "2026-W12",
      "date_range": "2026-03-16 to 2026-03-20",
      "xp_earned": 340,
      "xp_breakdown": {
        "tasks": 150,
        "meetings": 75,
        "efforts": 50,
        "deliverables": 30,
        "decisions": 20,
        "notes": 25,
        "streak": 50,
        "bonuses": 0
      },
      "cumulative_xp": 340,
      "level": 2,
      "class": "Build Beast",
      "stats": {
        "tasks_completed": 15,
        "meetings": 5,
        "efforts_advanced": 2,
        "deliverables": 1,
        "decisions": 1,
        "days_with_notes": 5
      }
    }
  ],
  "current_streak": 1,
  "all_time_xp": 340,
  "highest_weekly_xp": 340,
  "favorite_class": "Build Beast",
  "class_history": {
    "Build Beast": 1,
    "Strategy Sage": 0,
    "Deal Closer": 0,
    "Growth Hacker": 0,
    "Ops Commander": 0,
    "Multi-Class": 0
  }
}
```

## Week-over-Week Deltas

When previous week data exists, calculate and display deltas:

| Metric | This Week | Last Week | Delta |
|--------|-----------|-----------|-------|
| XP | 340 | 280 | +60 (up arrow, green) |
| Tasks | 15 | 12 | +3 (up arrow, green) |

Delta display rules:
- Positive change: green up arrow
- Negative change: red down arrow
- No change: gray dash
- No previous data: gray "N/A"

## Achievement Badges (Future Enhancement)

These can be unlocked based on milestones. Store in xp_log.json under "badges":

| Badge | Condition | Icon |
|-------|-----------|------|
| First Blood | Complete first weekly review | Sword |
| Ironman | 5 tasks completed in one day | Flexed Bicep |
| Diplomat | 5+ meetings in one week | Globe |
| Shipper | 3+ deliverables in one week | Package |
| Philosopher | 5+ decisions in one week | Brain |
| Perfect Week | All 5 daily notes + all tasks done | Crown |
| Marathon | 4-week streak | Running Shoe |
| Centurion | 100 cumulative tasks completed | Roman Helmet |

Badges are cumulative and never reset.

## Related

[[🏠 Home]]
