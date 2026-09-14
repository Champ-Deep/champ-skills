# Decision Flowcharts: reply handling per channel

This is the part reps most often lack. A prospect replies "what's pricing?" and the rep improvises, stalls, or quotes a firm number they shouldn't. The flowchart removes the improvisation: every realistic reply signal maps to a next action, an SLA, and an exact script.

Render flowcharts in Mermaid so they display in Obsidian and most markdown viewers. Build one per channel where reply patterns differ (email and phone diverge most). Keep the node labels short; put the actual scripts in a table beneath each chart.

## Pattern: the master reply-handling flow

```mermaid
flowchart TD
    A[Touch sent] --> B{Reply?}
    B -->|No reply| C{Touch number?}
    C -->|Not last| D[Advance to next waterfall touch]
    C -->|Last touch| E[Send breakup, soft-add to nurture]
    B -->|Positive| F{Signal type}
    B -->|Objection| G[Objection handling flow]
    B -->|Negative / not now| H[Acknowledge, add to Q-next nurture, stop sequence]
    B -->|Wrong person| I[Ask for intro, re-send to new contact same day]
    B -->|Unsubscribe / bounce| J[Suppress / find new address, never re-mail]
    F -->|Tell me more| K[2h: send one-pager + calendar + offer sample]
    F -->|Send a sample| L[4h SLA: deliver sample, book follow-up]
    F -->|What's pricing| M[4h: indicative range only + call to scope]
    F -->|Ready to talk| N[Book the meeting, move to Stage 2]
```

## Pattern: per-signal action table (pair with every chart)

| Reply signal | SLA | Action | Script seed |
|--------------|-----|--------|-------------|
| "Tell me more" | 2h | One-pager + calendar link + offer sample | "Happy to. Here's a one-pager and a link to grab 15 mins. Want a {{sample}} first?" |
| "Send a sample" | 4h | Deliver the sample, book a follow-up | "On its way. If it's useful, I'll walk you through {{the logic}} on a quick call." |
| "What's pricing?" | 4h | Indicative range only, gate firm price on scope | "Ballpark is {{range}}; the firm number depends on {{scope variables}}. 15 mins to scope it?" |
| "Not now" | 24h | Acknowledge, add to next-quarter nurture, stop | "Totally fair. I'll check back after {{moment}}. Anything useful in the meantime?" |
| "Wrong person" | 2h | Ask for the intro, re-send to the right contact same day | "Appreciate it, who owns {{area}}? Happy to loop them in." |
| Objection | 2h | Branch to objection-handling flow | See objection table |
| Unsubscribe | immediate | Suppress everywhere | none |
| Bounce | automated | Find a new verified address, never re-mail the bounce | none |

## Pattern: objection-handling sub-flow

```mermaid
flowchart TD
    O[Objection received] --> P{Which objection}
    P -->|Already using a competitor| Q[Reframe on the gap, not the swap]
    P -->|No budget / bad timing| R[Shrink the ask to a free sample/value]
    P -->|Skeptical of claims| S[Lead with proof: named ref or data]
    P -->|Not a priority| T[Tie to the why-now / moment cost of waiting]
    Q --> U[Book low-commitment call OR clean close]
    R --> U
    S --> U
    T --> U
```

| Objection | Surface response | Reframe | Walk-away |
|-----------|------------------|---------|-----------|
| "We already use {{competitor}}" | "Makes sense, most {{persona}} do." | "The gap most teams hit with {{competitor}} is {{specific gap}}. Worth 15 mins on just that?" | "No worries, I'll send one thing that helps regardless." |
| "No budget / bad timing" | "Understood." | "Then let's not talk budget. Want the free {{sample/value}} so it's on your radar for {{next window}}?" | Add to nurture, stop sequence. |
| "How do I know this works?" | "Fair question." | "{{Named reference}} in {{their vertical}} saw {{result}}. Want me to connect you, or send the data?" | Send proof, no push. |
| "Not a priority right now" | "Hear you." | "The reason I flagged it now is {{why-now}}. Waiting past {{date}} usually means {{cost}}." | "I'll circle back after {{moment}}." |

## Pattern: phone-specific flow (diverges from email)

```mermaid
flowchart TD
    A[Dial] --> B{Pick up?}
    B -->|Voicemail| C[Leave scripted VM referencing the email subject]
    C --> D[Send promised value same day]
    B -->|Answered, has time| E[Run the 30-sec why-now + offer value]
    B -->|Answered, busy| F[Ask for a better time, send value now]
    E --> G{Interested?}
    G -->|Yes| H[Book meeting on the spot, send invite in 30 min]
    G -->|Maybe| I[Send sample, set callback]
    G -->|No| J[Thank, close, suppress from dial list]
```

## Rules for building flowcharts into a playbook
- One chart per channel where the reply pattern differs; reuse the master flow where it doesn't.
- Every leaf node resolves to an action with an SLA and a script seed. No dead ends.
- Stage names in the flow must match the tracker's stage names exactly, so a rep moving a card always knows which node they're on.
- Keep firm-pricing nodes gated on sign-off; indicative ranges are pre-approved.
