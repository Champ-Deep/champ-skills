---
name: champions-hour
description: The Champions Group REACH orchestrator. Runs one full daily REACH pass on a single account (Research, Engage, Activate, Cadence, Hold) and ends with a scoreboard. Use when someone says "champion's hour", "run my power hour", "work this account end to end", "do a full REACH pass", "win back my hour", or wants the whole sales loop in one go. Routes to reach-research, reach-engage, reach-activate, reach-cadence, and reach-hold. Tailor the bracketed values once, then reuse.
---

# The Champion's Hour (REACH Orchestrator)

The daily ritual that makes the system real. Sixty minutes, one account, one full REACH pass. The skill runs the first three stages for the rep in about fifteen minutes, then hands them the human work for the rest.

## Tailor this first (edit once, then save your copy)

```
MY NAME / COMPANY: [name, company]
WHAT WE SELL: [one line]
OUR ICP: [who we sell to]
BRAND VOICE: [e.g. "warm, confident, concise, no em-dashes"]
DEFAULT CHANNELS: [email, LinkedIn, voice, WhatsApp]
```

## When to use

A rep wants to run their daily Champion's Hour, or work one account from cold to coordinated outreach in a single sitting.

## The workflow

Ask the rep for one account (name, company, URL) and the goal, then run the loop:

1. RESEARCH (R): produce the 5-minute prospect brief with the wedge and the why now. (Logic from `reach-research`.)
2. ENGAGE (E): write the 3-layer wedge email plus one alternate opener. (Logic from `reach-engage`.)
3. ACTIVATE (A): spin the brief into a multi-channel surround-sound play. (Logic from `reach-activate`.)
4. Then tell the rep clearly: "Claude has done Research, Engage and Activate. The next two stages are yours, this is the hour you just won back."
5. CADENCE (C): offer to draft the six-touch follow-up sequence. (Logic from `reach-cadence`.)
6. HOLD (H): if this is an existing account, run the account-depth pulse or call prep. (Logic from `reach-hold`.)
7. SCOREBOARD: at the end, format the session into a quick end-of-day line the rep can paste in their channel: touches by channel, the hot lead and its next step, anything at risk, and tomorrow's top three.

If a deeper version of any stage is needed, point the rep to that stage's standalone skill.

## Output

A complete worked account in one pass: brief, email, multi-channel assets, cadence, and a scoreboard line. Keep each stage tight so the whole thing fits in an hour.

## The two truths to remind the rep

1. Buyers reply at touch five. Run the cadence.
2. Deals come from proximity, not prospecting. Spend the hour you won back on the relationship.

## Power-ups (optional)

Install the five stage skills (`reach-research`, `reach-engage`, `reach-activate`, `reach-cadence`, `reach-hold`) for deeper, tailored control of each stage. Add connectors (enrichment, CRM, calendar) so live data flows in.
