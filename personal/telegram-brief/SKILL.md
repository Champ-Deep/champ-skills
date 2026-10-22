---
name: telegram-brief
description: "Use when a run's final reply goes to Deep on Telegram."
---

# Telegram brief

Every Telegram message to Deep is a brief he reads between meetings, not a log. He must see in five seconds what needs him, what is ready to send, and what was done. Narration of the process, tool names, and paths he will never open are noise.

## Shape (this order, omit empty sections, max 15 lines)

```
<HEADLINE: one line, outcome first, with counts>

NEEDS YOU
1. <one question> A: <recommended, what happens next> / B: <alternative>. Reply "1A" or "A on t_xxx".

READY TO SEND
- To <name>: <subject> (Outlook Drafts)

DONE
- <one line per output: what it is and where, card id or short path>

WATCHING
- <one line per thing in flight, with the next check time>
```

## Rules

- Nothing new: the whole message is one line, `Quiet: <job> ran, nothing new.`
- NEEDS YOU holds only decisions or hands-only actions. Each one is a question with a recommended answer. If there is nothing to decide, the section does not appear.
- READY TO SEND lists Outlook drafts by recipient and subject so he can open Drafts and send from his phone. Never claim a draft exists without the create_draft_email result.
- DONE is one line per deliverable. No sentences about how it was produced.
- No markdown headers, no tables, no bold, no code fences in the message body (Telegram renders them badly). Plain lines, hyphen bullets, numbered NEEDS YOU.
- No em dashes. No paths longer than the vault-relative form. No "I" sentences.
- Gaps and failures go in one line at the end, starting `Gap:`, with the named fix. Never fail the run over a gap.
- The Gap line is the last line (before any watermark or state lines a job must carry). No trailers from other modes: no "Ponytail:", no "skipped or not checked" footers, no sign-off.
- Headline is a plain outcome (`2 need you, 1 ready to send, 2 filed`), never a mood word like "Quiet-ish".
