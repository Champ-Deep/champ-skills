---
name: deep-email-voice
description: "Use when drafting any email as Deep. His voice, structure, addressing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Email, Voice, Drafts, Outlook, Tone]
    related_skills: [ms365-email, email-inbox-triage, celsus-meeting-recap]
---

# Deep's email voice

Every email an agent drafts for Deep (team nudges, meeting recaps, follow-ups, inbox replies, intros) must read like he wrote it, be structured for a reader who skims, and be addressed so that pressing Send is the only step left. `ms365-email` owns the Outlook commands; this skill owns what the draft says and how it is laid out.

Calibrated from his Sent Items. When this skill feels stale, re-derive it rather than guessing: find an earlier bot draft he rewrote before sending, diff the two, and turn each correction into a rule. That diff is the method; `email-inbox-triage` step 4 documents it. Editing this file in place is the update path, never an appended note.

## 1. Voice

| Trait | What he does | What bots got wrong |
|---|---|---|
| Opening | First name greeting (`Hi Santosh,`, `Hey team,`, `Hi IT Team,`). To internal people and first contacts he often adds one warm line: `I hope you're doing well!` | Jumped straight to orders, or used a filler line like "Quick nudge so nothing slips" |
| Asks | Polite and specific: `Could you please send them, or let me know if there's a specific blocker?` | Commands: "Send it tonight even if it is rough", "tell me what is in the way" |
| Help offer | Concrete: `If it's an access issue, just let me know and we can arrange access.` | Generic: "name it and I will unblock it" |
| Warmth | `Thanks so much for your help!`, `No pressure at all`. An exclamation mark or two per email is normal | Flat, transactional |
| Facts | Exact dates with weekday (`Thursday 22 Oct`), times with zone (`4:00 PM IST`), amounts with currency, ticket ids | Fine, keep this |
| Sign-off | `Cheers,` or `Best,` or `Thanks,` then `Deep` on its own line | Sign-off glued onto the last sentence |
| Register | Warmer and softer for interns and juniors; crisp and decision-led for leaders, vendors and the Chief; external clients get the brand voice of the sending company | One register for everyone |

Never: em or en dashes, "I hope this email finds you well" to someone mid-thread, restating their message back, invented dates, prices or commitments. A missing fact becomes `[CONFIRM: what]` and is listed in the run report.

## 2. Structure

Every draft is: greeting, one context line, the body, one clear ask with a date, sign-off.

| Email type | Body shape |
|---|---|
| Nudge, 1 item | Prose. Context line, what is open and since when, the ask with a date, a concrete help offer. Never a numbered list of one |
| Nudge, 2 or more items | One context line, then a numbered list, each item `what: agreed date`, then the ask |
| Meeting recap | `Thanks for <day>.` then bold mini-heads as plain lines (`Where we landed`, `What I need from you`, `Next steps`), bullets under each, owners and dates on every action |
| Intro | Who each person is in one line each, why they should talk, the specific first step |
| Reply in a thread | Answer first, reason second, two to five sentences |
| Decision ask to a leader | The decision in the first line, options numbered, Deep's recommendation, the date he needs it by |

Length: most drafts fit on a phone screen without scrolling. Recaps may be longer but every line carries a fact.

## 3. HTML (Outlook renders exactly what you send)

Use `body.contentType: html`. Graph drafts get no Outlook signature, so the sign-off must be in the body.

```html
<p>Hi Ajay,</p>
<p>I hope you're doing well! One paragraph per p tag.</p>
<ol><li>Plain text item, no p inside li</li><li>Second item</li></ol>
<p>Could you please ... by Friday 23 Oct?</p>
<p>Cheers,<br>Deep</p>
```

No `<p>` inside `<li>` (it renders as `1.` on its own line). No `\n` inside html content. No numbered list with one item.

## 4. Addressing (the draft must be sendable as is)

Resolve every recipient before creating the draft, in this order, and stop at the first hit:

1. `Atlas/People/<Name>.md` and `_config/people.md`.
2. Outlook Sent Items: `list_mail_folder_messages(mailFolderId="sentitems", search="\"to:<first name>\"")`.
3. Whole mailbox: `list_mail_messages(search="\"<first name>\"")`, take the `from` address of a mail they sent Deep. Prefer internal domains (championsmail.com, lakeb2b.com, championsgroup.com, cirrologix.com, ampliz.com, spanglobalservices.com, metricfox.com).
4. When an address is found in steps 2 or 3 and the People note lacks it, add the address to the People note.

If still unresolved, or two different people match the name: leave `toRecipients` empty, keep the subject clean, and list the draft under NEEDS YOU as `add To: <name>`. Outlook will not send a draft with no recipient, so the gap cannot misfire.

Never address a draft to Deep himself and never put `[FILL TO: ...]` in a subject: a self-addressed placeholder draft means the recipient was never resolved, so the intended person still has not been reached, yet Outlook will happily send it to Deep.

## 5. Before you save, check every draft

- [ ] Would Deep send it without rewording? Greeting, warm line where it fits, polite ask, sign-off on its own line.
- [ ] No one-item list, no `<p>` inside `<li>`, no em or en dash.
- [ ] Every date, number and name traces to the source (thread, meeting, TASKS.md row).
- [ ] `toRecipients` holds a real address for the right person, or is empty and flagged. Never Deep.
- [ ] Subject is what the recipient should see: specific, no bracket tags.

## Worked example (bot draft, then the fix)

Bot draft: greeting, one clipped order, a single-item numbered list, a command to send tonight, sign-off glued to the last sentence, addressed to Deep with a `[FILL TO: Ajay]` subject.

In Deep's voice, addressed to the intern's own mailbox:

```
Subject: Your plan for the 30 Oct demo

Hi Ajay,

I hope you're doing well! Checking in on your plan for the mobile validation demo on Friday 30 Oct.

Could you please send me your plan through to the demo by tonight, Thursday 22 Oct? A rough version is completely fine, we can shape it together. If you need anything from the Data Team or access to a tool, just let me know and I will sort it out.

Cheers,
Deep
```
