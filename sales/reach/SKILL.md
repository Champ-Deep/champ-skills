---
name: reach
description: >-
  The Champions Group REACH sales system in one skill: Research, Engage, Activate, Cadence, Hold, plus the full Champion's Hour pass and the Champions Growth Profiler. Research profiles any person or company and maps it to the right Champions Group brand (LakeB2B, Champion Lagoons and Infratech, Smart Beach Cities, Champions Club) with the wedge and the Why Now. MANDATORY TRIGGER for: "champion's hour", "power hour", "full REACH pass", "work this account end to end", "research [company]", "profile this company", "prospect brief", "is [X] a fit for us", "which Champions brand fits", "how do we pitch them", a pasted LinkedIn URL or company name with intent to engage, "write a cold email to [name]", "surround sound", "battle card", "follow-up sequence", "nurture cadence", "they went quiet", "prep me for my call with [account]", "account review". Replaces champions-hour, reach-research, reach-engage, reach-activate, reach-cadence, reach-hold and champions-growth-profiler.
---

# REACH

One skill, five stages, one orchestrator. Pick the stage from the ask, read only that stage's file, and run it. Do not load every stage for a single-stage request.

| Mode | Use when | Read |
|---|---|---|
| **champions-hour** | Full daily pass on one account: R, E, A for the rep, then C and H, ending with a scoreboard line | `modes/champions-hour/MODE.md` |
| **reach-research** | Stage R. Fast prospect brief: the wedge and the Why Now | `modes/reach-research/MODE.md` |
| **champions-growth-profiler** | Stage R, deep version. Brand-fit profile across Champions Group brands with Problem, Champions solution, Expected outcome mapping, priority rating and next step. Use it when the ask is to qualify, size up or match a brand, or when Research needs more than a 5-minute brief | `modes/champions-growth-profiler/MODE.md` |
| **reach-engage** | Stage E. 3-layer personalized first touch (company, role, individual) | `modes/reach-engage/MODE.md` |
| **reach-activate** | Stage A. Multi-channel surround-sound play, one-page asset, optional deck | `modes/reach-activate/MODE.md` |
| **reach-cadence** | Stage C. Six-touch follow-up cadence: Day 1, 3, 7, 14, 21, 30 | `modes/reach-cadence/MODE.md` |
| **reach-hold** | Stage H. Existing account depth, call prep, what to ask | `modes/reach-hold/MODE.md` |

## Routing rules

1. A request that names one stage runs that stage only.
2. "Research" defaults to `reach-research`. Switch to `champions-growth-profiler` when the user asks which brand fits, wants a qualification or priority rating, or the target is an investor, developer or executive rather than a B2B data buyer.
3. The Champion's Hour runs stages in order and hands each stage's output to the next. Where the orchestrator file says "logic from reach-X", read `modes/reach-X/MODE.md`.
4. Every stage ends with the no-ai-slop pass on anything the prospect will read. Where the vinh-copywriting style is required for persuasive copy, use that instead of no-ai-slop.
5. Never invent customer names, data counts or statistics. Unverified numbers are labeled as estimates.
