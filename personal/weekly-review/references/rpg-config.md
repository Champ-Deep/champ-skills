---
name: rpg-config
description: XP table, level thresholds, class definitions and brand colours for the weekly review.
---

# RPG configuration for the weekly review

## XP awards

| Action | XP | Notes |
|---|---|---|
| Task completed | +10 | Each `[x]` checkbox in daily notes |
| Meeting attended | +15 | Each row in the Meetings table |
| Effort advanced | +25 | Effort whose status changed during the week |
| Deliverable shipped | +30 | Each asset in the deliverables table |
| Decision made | +20 | Each bullet in a Decisions section |
| Daily note written | +5 | Per day that has a daily note |
| Weekly review streak | +50 | Consecutive weeks with a completed review |
| Perfect attendance | +25 | All 5 weekdays have daily notes |
| Zero carry-forward | +40 | Nothing carried to next week |

## Level thresholds (cumulative XP)

| Level | Title | XP | Level | Title | XP |
|---|---|---|---|---|---|
| 1 | Apprentice | 0 | 6 | Grandmaster | 3000 |
| 2 | Journeyman | 200 | 7 | Legend | 5000 |
| 3 | Specialist | 500 | 8 | Mythic | 8000 |
| 4 | Expert | 1000 | 9 | Transcendent | 12000 |
| 5 | Master | 1800 | 10 | Eternal | 20000 |

XP to next level = `threshold[current + 1] - cumulative`.
Progress % = `(cumulative - threshold[current]) / (threshold[current+1] - threshold[current]) * 100`.

## Character classes

Primary signal is the quiz heat map; fallback is counting activity types in the
daily notes. Assign when one category exceeds 40% of activity points, otherwise
`Multi-Class`. On a tie, prefer the category with the higher quiz satisfaction
score.

| Class | Signal | Colour |
|---|---|---|
| Strategy Sage | decisions + strategy-tagged efforts | `#6D08BE` |
| Build Beast | product/dev efforts and code sessions | `#E8033A` |
| Deal Closer | sales meetings and deal deliverables | `#FFB703` |
| Growth Hacker | marketing efforts and content deliverables | `#0095A0` |
| Ops Commander | ops meetings, operational tasks, vault maintenance | `#FF6903` |
| Multi-Class | no single category above 40% | gradient |

## Streak bonuses

Consecutive completed reviews: 1-3 weeks +50 XP, 4 weeks +75, 8 weeks +100,
12 weeks +150, 26 weeks +200, 52 weeks +500. A missed week resets to 0.

## Lake B2B brand colours for the HTML report

Header gradient `#FFB703` to `#E8033A` to `#6D08BE`. Body `#0F0F1A`. Card
`rgba(18,18,30,0.9)` with border `rgba(109,8,190,0.3)`. Text `#E4E4EB`, dim
`#8888A0`, accent `#6D08BE`. Complete: `#22C55E`, carried: `#F59E0B`. Font
Montserrat (300/400/600/800), fallback Arial.

## Weekly XP log

Persist to `Calendar/Weekly Reviews/weekly_xp_log.json`: a `history` array of
per-week entries (date range, xp earned, breakdown, cumulative, level, class,
stats), plus `current_streak`, `all_time_xp`, `highest_weekly_xp`,
`favorite_class` and a `class_history` counter per class. Append, never
overwrite, and compute deltas against the previous entry when displaying
week-over-week change.