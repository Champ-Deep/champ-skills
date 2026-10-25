---
name: telegram-brief
description: "Use when a run's final reply goes to Deep on Telegram."
---

# Telegram brief

Every Telegram message to Deep is a brief he reads between meetings, not a log. He must see in five seconds what needs him, what is ready to send, and what was done. Narration of the process, tool names, and paths he will never open are noise.

## Voice

Write like a sharp coworker texting Deep, not a system reporting to him. Say the thing, then stop.
- First line is the answer or the ask, in plain words. "Done, 3 drafts ready" not "Execution complete".
- Short sentences. Contractions fine. Say "I" when it is clearer ("I checked, it's clean"). No status-report phrasing, no "Reply:" boilerplate, no process narration.
- Name things the way he does (Harbinger, the Halloween list), not by id, hash or path. Ids only where he must reply with one.
- Never open with a mood word or a thank-you, never close with a summary of what you just said.

## Visuals (Telegram renders Markdown)

- One emoji leads each block, as a signal not decoration: 🙋 needs you, ✅ done, 📬 ready to send, 🚨 risk, 🚧 stuck, 👀 watching, 📎 file. Max one per line.
- **Bold** the one thing to act on per block. Hyphen or bullet lists, short. No tables, no headers, no code fences except for something he will copy.
- Anything with real shape (a plan, a comparison, a status board, a draft design) goes as an image or HTML card via MEDIA:/abs/path, with a one-line caption. Do not describe a visual in text when you can send it.
- Group repeats: "3 repos not pushed: A 5, B 7, C 2", never three lines.

## Shape (this order, omit empty sections, max 15 lines)

```
<HEADLINE: one line, outcome first, with counts>

🙋 NEEDS YOU
1. <one question> A: <recommended, what happens next> / B: <alternative>. Reply "1A".

📬 READY TO SEND
- To <name>: <subject> (Outlook Drafts)

✅ DONE
- <one line per output: what it is and where>

👀 WATCHING
- <one line per thing in flight, with the next check time>
```

## Rules

- Nothing new: the whole message is one line, `Quiet: <job> ran, nothing new.`
- NEEDS YOU holds only decisions or hands-only actions, each a question with a recommended answer.
- READY TO SEND lists Outlook drafts by recipient and subject. Never claim a draft exists without the create_draft_email result.
- DONE is one line per deliverable. No sentences about how it was produced.
- No em dashes. Vault-relative paths only. 
- Gaps and failures go in one line at the end, starting `Gap:`, with the named fix. Never fail the run over a gap.
- The Gap line is last (before any state lines a job must carry). No trailers from other modes: no "Ponytail:", no "skipped or not checked" footers, no sign-off.
- Headline is a plain outcome (`2 need you, 1 ready to send, 2 filed`), never a mood word.
- Cron scripts that print to Telegram (for example chat_digest.py) use the same voice: group, lead with an emoji, plain words, one short footer.
