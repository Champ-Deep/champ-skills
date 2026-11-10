# Bulk draft audits (read-only)

Audit a whole Outlook Drafts folder in one pass, collect every open question, get Deep's answers, then and only then rewrite. SKILL.md owns drafting and sending rules; this file owns the folder-wide sweep. `scripts/draft_audit.py` performs the fetch and the checks below.

## Rules that never bend

- The audit reads. It creates, edits, sends and deletes nothing, whatever the eventual task turns out to be.
- Confirmations before rewrites: the report ends with a table of what Deep must decide, he answers, and only then does any draft get touched. A rewrite done while a question is open is work done twice, because there is no edit-draft tool and the stale copy competes with the fixed one in the same folder.
- Nothing is sent. A cleanup pass ends with staged drafts and an explicit SEND/DELETE list per SKILL.md step 0.

## 1. Fetch every draft

Bulk route, one process over the whole folder:

```bash
env -u PYTHONPATH -u PYTHONHOME ~/.hermes/hermes-agent/venv/bin/python draft_audit.py out.json
```

The script drives the inbox profile's stdio MCP mail client at `/Users/deep/.hermes/profiles/inbox/inbox-bot/inbox_bot.py`: `open()` -> `preflight()` for the signed-in address -> `call("list-mail-folder-messages", mailbox, mailFolderId="drafts", select=..., fetchAllPages=True)` -> `close()` in a `finally`. Open that module for the current client class name before importing it.

When the pages belong in the conversation instead of on disk, the live `mcp__ms365__list_mail_folder_messages` connector performs the same fetch with the same paging discipline.

Decision points:

- **A list page is a floor, not a total.** The call returns at most 50 rows and reports `result_has_more: true` in the server's audit line. Without `fetchAllPages=True` a sweep silently covers half the folder and then reports that half as the whole folder. Count rows yourself and assert the total before quoting it.
- **The account addresses share one drafts set.** Querying both Deep's addresses returned the same message ids; treat the folder as one set, dedupe by `id`, and never publish per-account totals without an id-set diff.
- **`bodyPreview` truncates around 254 characters**, and the `[CONFIRM]` lists sit in the body. Select `body` for full text and parse both shapes: a `{contentType, content}` object from Graph and a plain string.

## 2. Checks

| Check | Match | Disposition |
|---|---|---|
| Bot verification header | `[BOT:` anywhere in the body | Blocking: it ships to the recipient verbatim (SKILL.md pitfall) |
| Unfilled confirmation | `[CONFIRM]` or `[CONFIRM: field]` | Blocking: becomes a row of the confirmation table |
| Empty recipient list | no `toRecipients` | Blocking: needs an address from Deep before anything else |
| Spam-trigger words | word list, case-insensitive over subject + body | Advisory: counts and draft numbers only; for cold outbound defer to the `outbound-email` deliverability rules |
| Em/en dash | U+2014 or U+2013 in subject or body | Advisory: house rule bans them everywhere |
| Markdown residue | `**`, `## `, `](url)` | Advisory: LLM paste marks in a business mail |
| Nameless salutation | `Hi ,` style, whitespace before the comma | Advisory: a cleared name placeholder; a plain `Hi,` is fine |

## 3. Report shape

Totals first: drafts scanned, drafts flagged, and what was not checked (attachments and binary bodies are not parsed; say so rather than implying full coverage). Then the confirmation table: draft number | subject | To | what Deep must answer. Blocking issues lead, advisory issues follow as counts with draft numbers. Redrafting starts only once the answers arrive.

## 4. The redraft pass

- Probe the live toolset for an update path (`tools/list`) before promising in-place fixes. The send-mechanism probe in SKILL.md step 9 applies to update tools the same way: a capability that is not in the toolset turns into an apology at the deadline.
- Absent an update tool, stage replacements and name the SEND/DELETE pairs per SKILL.md step 0; never leave two plausible drafts of one ask in the folder.
- Strip only the residue the audit flagged. Every other body fact stays as it was unless Deep asked for a rewrite.

## Pitfalls

- Inline `python3 -c "...f-string..."` one-liners die on nested quotes and brackets and burn rounds on syntax errors that have nothing to do with the mailbox. Write the script to a scratch file and run the file.
- The stdio server prints npm warnings and JSON audit lines into the same output stream as your prints. Parse the value returned by the call; never grep stdout for results.
- Guessing the client's class name from memory reads like an environment failure and costs a debug round: open the module and import what is actually there.
- Reporting a folder count before asserting it against the fetched row count: a paged list call under-reports by design, and the audit's credibility rests on the total.
