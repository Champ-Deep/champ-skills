# Bulk draft audits (read-only)

Audit a whole Outlook Drafts folder in one pass, collect every open question, get Deep's answers, then and only then rewrite. SKILL.md owns drafting and sending rules; this file owns the folder-wide sweep. `scripts/draft_audit.py` performs the fetch and the checks below.

## Rules that never bend

- The audit reads. It creates, edits, sends and deletes nothing, whatever the eventual task turns out to be.
- Confirmations before rewrites: the report ends with a table of what Deep must decide, he answers, and only then does any draft get touched. A rewrite done while a question is open is work done twice: a body edit is a whole-body patch that must be read back and asserted (section 5), so a rewrite started before the answers land has to be redone, and the stale copy competes with the fixed one in the same folder.
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

Totals first: drafts scanned, drafts flagged, the four send-readiness counts from section 4, and what was not checked (attachments and binary bodies are not parsed; say so rather than implying full coverage). Then the confirmation table: draft number | subject | To | what Deep must answer. Blocking issues lead, advisory issues follow as counts with draft numbers. Redrafting starts only once the answers arrive.

## 4. Send-readiness triage

The checks say what is wrong with a draft; this says whether it should go out at all, which is the real question behind "how many of these still need to be sent". Bucket every draft, not only the flagged ones. `scripts/draft_audit.py` prints the counts plus one row per draft with its bucket.

Partition, first match wins, so the counts sum to the folder total:

| Bucket | Rule | Meaning |
|---|---|---|
| needs-confirm | blocking flag: `bot-header` or `confirm-tag` | Cannot go out until Deep answers; a confirmation-table row |
| empty-to | no `toRecipients` | Read the body before classifying: a scraped-lead note or an internal question with no addressee is scratch and gets deleted, a real thread missing an address is blocked and needs the address from Deep |
| stale | `age_days >= 6` | Old enough that it needs a reason to still exist; list for deletion unless a live thread supersedes it |
| ready | everything else | The send list |

Rules:

- Age is `lastModifiedDateTime` (fallback `receivedDateTime`) minus now, computed in code. Never eyeball dates from the listing, and state the threshold used: it is a heuristic, not a policy.
- Advisory flags (spam words, dashes, markdown) do not move a draft out of ready or stale. They are edits for the redraft pass, not blockers.
- Name the signal that decided each non-ready draft. "13 days old" and "superseded by a reply that already went out" both end in delete, but only one of them means the content was wrong, and Deep needs to know which.
- Report the four counts beside the folder total and make them sum. A draft in two buckets or in none means the tally is wrong, and every downstream number inherits it.

## 5. The redraft pass

- Probe the live toolset for an update path (`tools/list`) before promising in-place fixes. The send-mechanism probe in SKILL.md step 9 applies to update tools the same way: a capability that is not in the toolset turns into an apology at the deadline.
- Absent an update tool, stage replacements and name the SEND/DELETE pairs per SKILL.md step 0; never leave two plausible drafts of one ask in the folder.
- Strip only the residue the audit flagged. Every other body fact stays as it was unless Deep asked for a rewrite.

### Staging a replacement as a reply

Every replacement for a draft on a live thread goes through the reply path (SKILL.md always-on rule): the quoted history is part of the deliverable, and a standalone draft with matching text is the wrong artifact.

1. **Find the inbound message.** `list-mail-folder-messages` on `inbox` with a distinctive subject fragment; assert the fragment appears in the returned subject before trusting the hit, and fall back to a search on the sender's address when the subject words do not index. Pick by subject match, not by first row: `search` also matches sender names and unrelated mail sharing a keyword.
2. **Create the reply.** `m.call('create-reply-draft', mailbox, messageId=..., body={'comment': <final body>})`. The quoted history comes along automatically.
3. **Patch what the reply got wrong, do not recreate it.** `m.call('update-mail-message', mailbox, messageId=draft_id, body={'ccRecipients': [{'emailAddress': {'address': a}} for a in addrs]})` for cc, `body={'subject': s}` for subject, `body={'body': {'contentType': 'html', 'content': formatted}}` for the body. All three go through the same tool and keep the thread linkage, so they never cost a second draft and a SEND/DELETE pair. A body patch replaces the entire body: build `formatted` with `build_clean_reply_html` (the canonical reply formatter in `inbox_bot.py`) from the reply text plus the quoted body read at step 2, then read the draft back and assert the reply text landed. A 200 on the call is not proof; only if the patch fails that read-back do you stage a replacement and name its SEND/DELETE pair.
4. **Read back and prove the linkage.** `get-mail-message` with `select=id,subject,body`: the body should be far longer than your comment and contain the prior sender's content below yours. Creation success proves the call, not the linkage. Strip em/en dashes from the subject in the same pass (house rule; the audit already flags them as advisory).
5. **If the inbound message cannot be found, stop on that one.** Report it to Deep as a draft that would ship unlinked instead of quietly creating a fresh mail under a `Re:` subject.
6. **Keep a manifest and reconcile it against the live folder.** Write every created draft (id, subject, To, cc) to a scratch JSON as you go, then after any gap where Deep may have touched the folder, re-list `drafts` and diff against the manifest: the manifest says what you intended, not what still exists, and the diff finds both drafts he deleted and ones whose create silently failed. Report the diff, never the manifest.

## Pitfalls

- Inline `python3 -c "...f-string..."` one-liners die on nested quotes and brackets and burn rounds on syntax errors that have nothing to do with the mailbox. Write the script to a scratch file and run the file.
- The stdio server prints npm warnings and JSON audit lines into the same output stream as your prints. Parse the value returned by the call; never grep stdout for results.
- Guessing the client's class name from memory reads like an environment failure and costs a debug round: open the module and import what is actually there.
- Reporting a folder count before asserting it against the fetched row count: a paged list call under-reports by design, and the audit's credibility rests on the total.
- Quoting the flagged count as the answer to "how many need sending". Flags measure problems, not intent: in a healthy folder most drafts are clean and still need Deep's send decision, so answer from the section 4 triage counts.
- Counting a draft into two triage buckets, or into none, and reporting the split anyway. The buckets are a partition by construction; verify they sum to the folder total before quoting them.
