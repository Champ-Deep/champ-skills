---
name: reach-engage
description: REACH Stage E. Write a personalized cold outreach message that proves real research, using 3-layer personalization (company, role, individual). Use when someone says "write a cold email to [name]", "draft outreach to [company]", "personalize this", "write the first touch", or after a prospect brief exists. Part of the Champions Group REACH sales system. Tailor the bracketed values once, then reuse.
---

# REACH: Engage (Stage E)

Turn a prospect brief into a message that earns the open and the reply. No "Hi first name" filler. The draft is the skill's job. The one human line is the rep's.

## Tailor this first (edit once, then save your copy)

```
MY NAME / TITLE: [name, title]
MY COMPANY: [company]
WHAT WE SELL: [one line]
DEFAULT ASK: [e.g. "a 15-minute call next week"]
BRAND VOICE: [e.g. "warm, confident, concise, no hype, no em-dashes"]
PROOF POINTS I CAN USE: [1 to 3 stats or named wins]
```

## When to use

A brief or research exists and the rep needs the first touch (or a rewrite of a weak one). Trigger after Research, before Activate.

## The workflow

1. Take the prospect brief (or ask the rep to paste it). If none exists, send them to `reach-research` first.
2. Write the email under these rules:
   - Under 110 words.
   - Three layers of personalization: one line on their company, one on their role, one on them specifically.
   - Lead with THE WEDGE and WHY NOW from the brief, not with us.
   - Exactly one call to action (the DEFAULT ASK unless the rep overrides).
   - Tone matched to seniority (C-suite, Director, or IC) and to BRAND VOICE.
   - Subject line under 6 words: curiosity or specificity, never clickbait.
3. Return three things: the subject line, the email, and one alternate opening line the rep can swap in.
4. Flag the single spot where the rep should add a genuine human detail (something they noticed that no model would know).

## Output

A ready-to-send email plus one alternate opener. Keep it tight. If the rep asks, produce a LinkedIn DM variant in the same voice.

## Power-ups (optional)

- Skills: `outbound-email`, `sales:draft-outreach`, and your brand skill (`champions-group-brand`, `lakeb2b-brand-guidelines`, or `ampliz-brand-guidelines`) for on-voice output.
- Connectors: HubSpot for CRM context, Gmail or MS365 to draft in place.

## Hand off to

`reach-activate` to turn this into a full multi-channel play, or `reach-cadence` to build the follow-up sequence.
