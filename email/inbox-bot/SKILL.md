---
name: inbox-bot
description: "Use when changing or testing Deep's inbox_bot.py."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Email, Inbox, Outlook, Bot, Python, Tests]
    related_skills: [email-inbox-triage, ms365-email, deep-email-voice, model-routing]
---

# Inbox bot (Deep's automated reply drafter)

The inbox agent is one fixed Python workflow at `~/.hermes/profiles/inbox/inbox-bot/inbox_bot.py` (plus `test_inbox_bot.py` beside it). It drafts and never sends. This skill covers changing and testing that code.

## When to Use

- A rendering or formatting complaint about a bot-drafted reply ("format them like this, not like that").
- Adding or changing a draft action, guard, or formatting rule in `inbox_bot.py`.
- Running or extending the inbox bot's test suite, or debugging a draft the bot produced.

Don't use for: routing which lane runs the bot or firing it ad hoc (`model-routing`), triage and reply policy (`email-inbox-triage`), what the reply says (`deep-email-voice`), provider commands for hand-made drafts (`ms365-email`). Which lane it runs in and how to fire it ad hoc: `model-routing`. What a reply should say: `deep-email-voice`. Provider commands for hand-made drafts: `ms365-email`.

## Always-on rules

- Draft-only by construction: `TOOLS_ALLOWED` never grows a send tool, whatever the task asks for. Verifying a send path belongs to a human-approved flow outside this script.
- Formatting is judged by how the draft renders in Outlook, not by a tool call returning success: paragraphs separated, divider present, quoted history styled.
- `build_clean_reply_html` inside `inbox_bot.py` is the one canonical reply formatter. Copies in scratch probe scripts are throwaway and never become the place a fix lands.
- The test suite gates every change, but it runs against fakes: green proves behavior, not delivery. A formatting change additionally needs a read-back of a real draft.

## The reply draft pipeline

`create_reply_draft` (and the reply-all path) produces the approved look in five steps:

1. Create with `create-reply-draft` / `create-reply-all-draft`, passing the reply text as `Comment`. The comment arrives as one run-on block: Graph stores it as a string and the quoted history lands underneath unstyled.
2. Read the draft back (`get-mail-message`, `select=id,isDraft,body`) and take the body for what it is: Graph returns `body` as either a `{contentType, content}` object or a raw string, so branch on `isinstance` before calling `.get()`.
3. Format with `build_clean_reply_html(reply_text, raw_body, raw_type)`. Feed it plain paragraphs separated by a blank line (it splits on `\n\n`). It emits reply paragraphs as 11pt Aptos `<p>` blocks, a thin divider, then the quoted history carried over from the read-back body as a bold From/Sent/To/Cc header block over grey 10pt paragraphs.
4. Patch the body: `update-mail-message` with the message body `{'contentType': 'html', 'content': formatted}`.
5. Read back again and assert two things: `isDraft` is still true, and the reply text is present in the body. The update call's own success proves neither; the content assertion is what catches a patch that silently no-ops.

Never rebuild the body from the reply text alone: the quoted history read in step 2 must be re-embedded by the formatter, or the draft ships with no thread.

## The formatting standard

Deep approves drafts by eye against his own Outlook-composed replies. Clean means one `<p>` per paragraph at 11pt Aptos with 1.4 line height, a thin divider above the quoted history, and the quoted history rendered as a bold From/Sent/To/Cc header block over grey 10pt paragraphs. Shabby means the raw quote dumped as one block, run-on paragraphs with no line breaks, or unstyled `<div>` text prepended over the original body. When a formatting change lands, look at the rendered draft (or its screenshot) before reporting done.

## The no-draft policy (`playbook.json` → `no_draft_rules`)

The one place to stop the bot drafting for a sender or a class of mail. Each entry is `{why, action, <match keys>}`: `action` is `label` (label only, stay silent) or `brief` (surface to Deep, still no draft). Match keys are ANDed: `sender_contains` (substring of the from address or the display name), `intent` (the classifier intent), `subject_contains`, `scheduling_only` (classifier intent is scheduling, or the subject or the new body text reads as a calendar or slot mail). First match wins. A rule with no match key is ignored by design, and `selftest` fails a rule that would match every message or carry an action other than label or brief.

Two guards in `decide`: a `label` rule never fires for a P0 or a VIP (that mail keeps its normal handling), and the check sits before the confidence check so muted mail cannot reach Deep as a brief.

Temporary holds (a thread Deep answers himself once the work behind it lands) live in the same list; clear one by deleting its entry. Two kinds of entry exist today: silent mutes (spam, team-owned scheduling, a booked calendar invite) and holds that brief Deep (a parked thread).

## Proving a policy change on real mail

A dry run only re-decides mail the state file has not already recorded, so it cannot show a rule firing on yesterday's thread. Prove it directly instead: import `inbox_bot` in a scratch script with `STATE`, `LEDGER`, `LOCK`, `REPORT_DIR` and `CONTACTS` repointed into the scratch dir, fetch the real message by `list-mail-messages(search='"from:<sender>"')`, run `classify_prompt` + `complete_json` + `decide` on it, and print the action. That is read-only and shows the before (the triage report's action) and after (the printed action) side by side.

## Running the tests

```bash
cd ~/.hermes/profiles/inbox/inbox-bot
env -u PYTHONPATH -u PYTHONHOME ~/.hermes/hermes-agent/venv/bin/python -m unittest -v test_inbox_bot
```

Strip `PYTHONPATH`/`PYTHONHOME` exactly as an ad hoc run of the script does (`model-routing`): the gateway exports them and they pull the wrong modules into the interpreter.

## Pitfalls

- Chaining `.get()` on a Graph field whose shape varies: `((got.get("body") or {}).get("content"))` type-errors the moment `body` comes back as a string. Narrow with `isinstance` and give every branch a default.
- Reporting a body patch from the update call's success. The draft renders what Graph stored, so assert the text on a fresh read-back.
- Letting a scratch probe script grow its own copy of `build_clean_reply_html`: the next fix lands in the copy and production keeps the old look.
- Fixing only the reply text and dropping the quoted history: the create response still looks right and the mail ships as a threadless new approach to someone already answered.
- Treating a green unittest run as proof the rendered draft is fixed: the fakes accept any body, so the real proof is the Outlook rendering plus the content assertion in step 5.
