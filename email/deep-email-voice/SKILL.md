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

When an email is anchored to a conversation (Deep says "based on my last call with X"), read the filed recap in `Calendar/Meetings/` before drafting: it carries the agreed commitments and the evidence id, and it is faster than API calls. Wispr `search_meetings` is the fallback only when no recap was filed.

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

Never: em or en dashes, "I hope this email finds you well" to someone mid-thread, restating their message back, invented dates, prices or commitments. Never attach a Markdown file (`.md`) or any other source-format file: recipients cannot open them. Attachments are PDF, HTML, Word, Excel or PowerPoint only, and always built with the sending brand's design skill (`lakeb2b-docs`, `champions-ranch-docs`, `docx`, `power-design`): a vault note run through bare pandoc or default CSS is not sendable, convert it through the brand template first. A missing fact becomes the literal tag `[CONFIRM: what]` inline in the sentence, so the gap is greppable rather than plausible, and it is listed in the run report. A draft still carrying tags is not sendable as-is: name it and its tags on the decision card instead of reporting the draft as ready.

When the ask is for data he does not have, the ask goes out as an attached input sheet rather than a list of questions in prose: prefilled with every row and column already known from the thread (names, teams, times), dropdowns on the choice fields, and a flag on any row where the recipient's own source contradicts itself. A recipient answers gaps in a table in two minutes; the same fields in an email body take a reply chain, and asking in prose for facts you hold reads as not having read the mail. The body still names the attachment and the date, and "attached" never appears until the read-back shows the file.

## 2. Structure

Every draft is: greeting, one context line, the body, one clear ask with a date, sign-off.

| Email type | Body shape |
|---|---|
| Nudge, 1 item | Prose. Context line, what is open and since when, the ask with a date, a concrete help offer. Never a numbered list of one |
| Nudge, 2 or more items | One context line, then a numbered list, each item `what: agreed date`, then the ask |
| Day plan or task sheet for a report | One context line, then a bold day mini-head per day over its own numbered list, each day closing with an `End of <day>: <deliverable>` line, then an explicit `Not expected` list and the evidence rule (one timesheet row per block). Their register: warm on the person, exact on the work | A flat undated list of everything outstanding |
| Meeting recap | `Thanks for <day>.` then bold mini-heads as plain lines (`Where we landed`, `What I need from you`, `Next steps`), bullets under each, owners and dates on every action |
| Intro | Who each person is in one line each, why they should talk, the specific first step |
| Multi-touch sequence (outbound or follow-up to a list) | Every touch keeps the context line: who Deep is, which company he writes for, and why this person is on the list, stated only as far as the list itself proves it. Vary the opening and the closing ask across touches: two touches with the same first clause or the same question shape read as a template. No two touches on the same day (email plus LinkedIn) teach the same point. A slop lint pass does not check any of this, so read the touches side by side before handoff | Four touches that each open "I suggest" and close on a near-identical question, signed `Deep` with no company, so the recipient cannot tell who is writing |
| Update plus research brief | Two bold mini-heads as plain lines (what changed, what I need from you), each over its own numbered list, then one ask naming the deliverable and a date | One long numbered list mixing changes and asks |
| Reply in a thread | Answer first, reason second, two to five sentences |
| Internal brief after a call with a counterparty | A context line thanking the team, then bold mini-heads as plain lines, in this order: what the counterparty asked for (bulleted, in their scope), our numbers and what they do and do not support, what we commit to and what we don't, how we run it, one paragraph on any claim or figure that came from the counterparty and needs a source first, how we price it, then one numbered list of what Deep needs and when. Close on what gets parked. Every figure derived rather than sourced is labelled as arithmetic, and the handback names the dates the drafter chose | A flat list of asks with no honest read of what is deliverable, or counterparty figures and deadlines restated as facts |
| Approval or payment sign-off, several lines | One context line saying the lines were reviewed one by one, then a numbered list where each line carries its own verdict: approved with its basis (period, who reviewed it, what proves it, which rate applies), or not approved with the one thing that is missing. Close with a line saying no unapproved line holds an approved one, then the ask. The confidence is stated in plain words on every line | Four names approved "in the same batch", so a name with no sheet rides through on the strength of the one with a sheet, and a rate conflict sits unread inside the batch |
| Leave or work-from-home request | Greeting, one line approving with the reason stated back to them, one line of support or of what you need instead. Approve the request that carries a stated reason (illness, safety, no transport); when a request gives no reason at all, ask for the reason and a one-line plan per day before approving, and say the request is not approved yet until that comes back. cc stays as the sender set it (attendance and the HR owner), because the approval is a record, not a private note |
| Decision ask to a leader | The decision in the first line, options numbered, Deep's recommendation, the date he needs it by |
| Confirmation of a slot he proposed | One line: does the time work, yes or no, with the exact day, date and zone repeated. No restating the thread, no new asks: he answers "yes" or "move it" and stops |

Length: most drafts fit on a phone screen without scrolling. Recaps may be longer but every line carries a fact.

A confirmation of a proposed slot is always two lines: the greeting with the
slot repeated in full, then the ask. Anything longer turns a yes or no into a
reading task, and he replies to the extra sentences instead of the time.

`references/slot-confirmations.md` carries the short patterns: confirming, moving
and holding a slot, and the three register variants.

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

0. **When Deep names a source file for a reply, read that file and verify the recipient list against it before drafting.** He is pointing at the version that carries the right addressing, so a draft built from an earlier copy repeats the defect he is asking you to fix; the recipient check comes before any wording work, because a draft cannot be edited in place.
0b. **Name the origin of a forwarded request exactly.** When several people passed the same material, state both the original sender and the forwarder in the opening line (`Ganavi shared X with Hemang, and Hemang passed it on`), not whichever name sits at the top of the newest forward. Misattributing who owns a request reads as inattention to the person who will answer it, and the correction lands in the reply instead of the draft.
0c. **For a meeting-anchored draft, the invite's own attendee list resolves addresses before the vault does.** Read the event (`get_specific_calendar_event`, or Wispr participants for a recorded call) and take each address from its attendees: a People note or an older thread keeps a previous domain, where the invite carries the address the calendar actually routes on today. Names still take the vault's spelling; only the address comes from the invite, and a mismatch between the two is reported, not silently averaged.
1. `Atlas/People/<Name>.md` and `_config/people.md`.
2. Vault-wide pattern grep: `(?i)<name>[\w.'_-]*@[\w.'-]+\.[a-z]{2,}` with `search_files` across the vault. Triage and meeting notes carry addresses the People notes never got, and one search beats two Outlook round-trips.
3. Wispr: when Deep and the person were both on a recorded call, `get_meeting_participants_enriched` on that meeting returns each participant's emails directly; find the meeting with `search_meetings` on their name.
4. Outlook Sent Items: `list_mail_folder_messages(mailFolderId="sentitems", search="\"to:<first name>\"")`.
| 5. Whole mailbox: `list_mail_messages(search="\"<first name>\"")`, take the `from` address of a mail they sent Deep. Prefer internal domains (championsmail.com, lakeb2b.com, championsgroup.com, cirrologix.com, ampliz.com, spanglobalservices.com, metricfox.com).
| 5b. **The failed link Deep is complaining about.** Read the address straight out of the URL he pasted or the one in his complaint: a SharePoint or Google share invite carries an `e=`/`uid=` token scoped to the invited recipient, so the intended To address is in the link and needs no search. Same for a `mailto:` link or an address printed in the share notification mail. |
6. When an address is found in steps 2 to 5 and the People note lacks it, add the address to the People note.
7. **Departed staff are not at their company address.** For an exit item (a relieving letter, F&F, an experience certificate), the person's company mailbox has usually been blocked since their last day. Mail sent there never reaches them. Take a personal address from their exit thread or the HR record. If neither has one, tag `[CONFIRM: personal email]` on the card and do not stage the draft to the company mailbox.

**Intermediary before empty.** When the person is real but has no address of their own anywhere (a candidate reached through a recruiter, a guest whose call a coordinator set up, an owner behind a shared mailbox), the intermediary is the resolution: address the draft to the intermediary with the ask "could you forward this to <name>", then put the intended recipient's note in the body after a `--- Note for <name> ---` divider with its own greeting and sign-off, so it reads as a letter they can forward verbatim. Also ask the intermediary to book the next slot, since the intermediary owns the scheduling. Try this before falling back to an empty To: an empty To cannot go out at all, while a forwardable draft ships today.

If still unresolved, or two different people match the name: leave `toRecipients` empty, keep the subject clean, and list the draft under NEEDS YOU as `add To: <name>`. Outlook will not send a draft with no recipient, so the gap cannot misfire. The `add To:` line lives on the decision card and in the run report, never in the draft body, even when the card text says to "add" it: a body that opens with a note to Deep is bot meta-language, and he deletes those drafts unsent. Before falling back to an empty To, run the spelling-variant sweep (Pallav/Pallab, Harshal/Harshil) against Sent Items and put the best candidate address on the card so Deep confirms in one word.

When Deep hands an address himself but hedges on it (`or something along those lines`, `I think`), treat it as a lookup key, not a literal: verify the exact form against Sent Items before drafting. Internal domains embed dots and initials inconsistently (`pogulaajay.k@` vs `pogulaajayk@`), and only the form in a sent mail is proven.

Never address a draft to Deep himself and never put `[FILL TO: ...]` in a subject: a self-addressed placeholder draft means the recipient was never resolved, so the intended person still has not been reached, yet Outlook will happily send it to Deep.

## 5. Before you save, check every draft

- [ ] Would Deep send it without rewording? Greeting, warm line where it fits, polite ask, sign-off on its own line.
- [ ] When he named a source file (`this is the source`), does the draft add substance, not just fixes? A reply that only repairs recipients or wording wastes the instruction: tighten the ask, state what was learned, or hand over something concrete (an attachment carrying the list or data he referenced), so the new draft is unambiguously better than the one it replaces.
- [ ] No one-item list, no `<p>` inside `<li>`, no em or en dash.
- [ ] Every date, number and name traces to a source, taken from the strongest tier that holds it: Deep's own reply in the thread, then the thread's own messages, then a filed recap or ledger row, then a vault note. A TASKS.md row or an auto-ingested call summary is the weakest tier and never a source for a name: those rows paraphrase speech, so a person named only there may be a transcription artifact rather than a person. Before such a name reaches a draft, sweep the mailbox for spelling variants (the same variant sweep used for an unconfirmed address, above) and assert the literal spelling occurs in a message body; a Graph search count is fuzzy and proves nothing (the name-hunt recipe lives in the `ms365-email` skill's thread-search reference). No hit means the name does not go in the mail: drop it, or tag it `[CONFIRM: who]` and put it on the decision card. Correct the record row itself when it carries the bad name, so the next ingest and every digest stop resurfacing it.
- [ ] An approval mail grounds every line separately: a name whose only source is one memo is ungrounded until a second source confirms it (a ledger row, a filed mail, a people note, the recipient's own sheet). An ungrounded line becomes an ask for that evidence, never an approval, and no batch language (`run it in the same batch`, `alongside the rest`) may carry it: one unverifiable name must not inherit the credibility of a verified one.
- [ ] An approval mail states the basis on the line it approves (period, reviewer, what proves the work, which rate) and its confidence in plain words. **Where Deep has already ruled on the very question the line settles (rate basis, eligibility, how someone is paid), read his own earlier reply in that thread first and restate his ruling with its date:** deriving a fresh basis while his words sit on the same thread contradicts him in writing to a third party, and the reply is the strongest source on the page. Only where the thread is silent does the comparison below apply. When a written policy and the person's own contract disagree on the rate, name which basis applies and why (the date the policy went out versus when the work was done) instead of settling it silently in the batch, and put the disputed figure on the decision card for Deep: a pay rate is his to rule, not mine.
- [ ] No claim comes from talking points for a conversation Deep has not held yet (a planned 1:1, a "Deep only" section). Those are his proposals, not decisions, and putting one in a mail to third parties announces it before the person it concerns has heard it. Check the board card for that conversation; if it is still open, use only what Deep already wrote as ready to send.
- [ ] Every count in the body (people, slots, groups) traces to a parse of the source table, not to a figure carried over from an earlier draft of the same mail.
- [ ] No relative time words in the body (`tomorrow`, `today`, `in 5 days`, `this week`): a draft is sent hours or days after staging, so write the absolute weekday and date (`Fri 13 Nov`), check the weekday against the calendar for that date, and check the date is still in the future at the moment of staging. When a brief or decision hands you relative wording, convert it and say so in the handback; a past date in a staged draft is a defect, not a quote.
- [ ] Every deadline is either sourced or named as mine in the handback. A deadline I chose is a proposal Deep may strike, so it never goes out silently as a fact.
- [ ] A request that sets the recipient a deadline carries a send-by date on its decision card, and that date leaves the recipient the working time the ask needs (send by the next working day, not "review before the deadline"). A counts request due Tue 17 Nov EOD that the card lets Deep review on Mon 16 or Tue 17 gives the data team under a day, so the ask is not being worked now.
- [ ] For a date invented for this draft, offer two candidates in the handback (the one written in, and a nearer or later alternative) instead of one silent proposal, so Deep picks rather than having to invent an option himself.
- [ ] Before proposing a due date, check the recipient's calendar or leave: a proposal that lands on a colleague's leave, a holiday or a milestone of theirs is called out as its own option (move the date to the next working day) in the handback, never embedded silently in the draft.
- `toRecipients` holds a real address for the right person, or is empty and flagged. Never Deep.
- When the ask is to send a pack or a bunch of information, does the draft actually attach the document? A body carrying only a URL answers a different question than the one asked.
- [ ] Before tagging an address `[CONFIRM]`, search spelling variants of the name (Akansha, Akanksha, Akankshya) and the local-part pattern (`firstname.initial@`), then corroborate a candidate by team and co-occurrence (same distribution list, same teammates, same project thread). Put the candidate and that evidence on the tag so Deep confirms in one word instead of looking it up.
- [ ] A leave or work-from-home reply says plainly whether it is approved. "I will confirm once I have the reason" is not an approval, and a draft that reads as one either way leaves the person waiting on a second mail.
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
