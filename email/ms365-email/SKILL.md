---
name: ms365-email
description: "Use when drafting Outlook mail with attachments via ms365."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [Email, Outlook, Microsoft365, Drafts, Attachments, MCP]
    related_skills: [email-inbox-triage, himalaya, google-workspace]
---

# ms365 Email (Outlook connector)

Provider commands for Deep's Outlook mailbox through the configured `ms365` MCP server (`mcp__ms365__*` tools): compose, attach, and read-back verification. `email-inbox-triage` owns thread policy and prioritization; `himalaya` owns terminal IMAP/SMTP.

## When to Use

- New outbound mail must exist as an unsent Outlook draft, optionally with a document attached.
- Verify a draft's recipients, subject, attachments, or draft state before Deep sends it.
- Attach a file to an existing draft when only the message id is known.
- Deep has explicitly approved sending a staged draft, and the send must be executed and proven by read-back.

Don't use for: inbox triage or reply policy (`email-inbox-triage`), terminal IMAP/SMTP (`himalaya`), Gmail or Drive (`google-workspace`).

## Always-on rules

- Stage as a draft first; never send without Deep's explicit approval of that exact mail in the conversation. When he approves it, follow the Send procedure below: the send is irreversible, so it gets its own read-back verification. Return the draft's `webLink`, never the raw message id, so he can open it in one click.
- Deliver attachments inside the draft. If Deep asks for "the doc", the file is attached to the Outlook draft, not merely linked in chat.
- Every write is verified by read-back before it is reported done. A successful tool call is not a successful draft.
- Never put a link in the body that was not actually produced. Omit the sentence and say the link is unavailable rather than inserting a placeholder.

## Procedure

- **Ground the draft in the live thread.** Before writing, find what the team already said: one `mcp__ms365__list_mail_messages` call with a KQL `search` OR-ing `to:`/`from:` addresses and a `received>=` floor, `select` limited to id/subject/from/receivedDateTime/bodyPreview/isRead, `top: 25`, then page with `@odata.nextLink`. Read full bodies only for the threads in scope via `get_mail_message`. Re-drafting an unanswered thread without its last reply loses the promised date and the ticket number. **A mailbox search only proves what arrived:** when the question is whether an outgoing message exists at all, also search `list_mail_folder_messages` on `drafts` and `sentitems`, because unsent work lives in Drafts and `$search` over received mail never sees it. Full recipe: `references/thread-search-recipes.md`.
1. **Resolve scope.** Recipient address(es) and display names, subject, body facts, attachment file path. Confirm the attachment exists, is non-empty, and note its size and MIME type before creating anything. Settle every fact before this point: person names checked against a source (vault, thread, the document itself) rather than retyped from meeting notes, amounts read out of the source PDF or invoice line by line, and the full attachment list final. A draft cannot be edited in place, so a fact fixed later means a replacement draft plus a stale duplicate Deep must delete by hand. **What the draft says is not this skill's call:** voice, structure and body formatting come from `deep-email-voice`, which also owns the recipient-resolution lookup order. Follow it before step 2.
2. **Create the draft.** `mcp__ms365__create_draft_email` with explicit `toRecipients`/`ccRecipients`/`bccRecipients`, `subject`, and `body: {contentType: "text", content: ...}` unless `deep-email-voice` specifies html. Set every recipient field explicitly rather than relying on defaults. Keep the returned `id` and `webLink`.
3. **Attach the file.** Build `body` as `@odata.type: #microsoft.graph.fileAttachment`, `name`, `contentType`, `isInline: false`, `contentBytes` as base64 of the raw bytes, with `messageId` as the top-level argument.
   - **Base64 larger than ~2-3 KB goes through the stdio recipe in `references/direct-stdio-mcp.md`, never an inline tool call.** Past that size an inline argument can break the tool call's own JSON envelope (rejected as invalid JSON before it executes), so inline is not a fallback worth trying: go straight to stdio. Even when it does parse, emitting the blob as a tool-call argument means generating the whole base64 through my own output tokens: a 20 KB zip costs ~27 KB of typed text and a single transcription error corrupts the attachment with no error surfacing. Generate the base64 inside `execute_code`/stdio code. This applies whether or not the tool is exposed in the live toolset; use stdio whenever the payload is big, not only when the tool is missing.
   - If Graph rejects `contentBytes` on size, switch to `create_mail_attachment_upload_session`.
4. **Verify.** `get_mail_message` (expect `isDraft: true`, `hasAttachments: true`, correct recipients and subject) and `list_mail_attachments` (exact filename, size, contentType). Report only what the read-back shows. For several drafts created in one turn, read every one back: the create response for draft A does not prove draft B exists or that its To field is right.
5. **Replace a stale attachment.** If the local file changed after it was attached, the draft still serves the old bytes. Re-run `add_mail_attachment` with the new content, then `delete_mail_attachment` the old attachment id (`confirm: true`), then `list_mail_attachments` again and confirm the list contains exactly the intended set: new file present, old id gone, expected count.
6. **Deep asks "confirm it has the changes".** Filename and size are not proof of content. Download the attached bytes with `mcp__ms365__download_bytes_to_file` (target `/me/messages/{messageId}/attachments/{attachmentId}/$value`, write to a scratch path that does not exist yet) and byte-compare against the canonical local file before answering. For a small text or HTML attachment there is a shorter path: `list_mail_attachments` already returns `contentBytes`, so decode it in code and sha256-compare against the local file, no download round-trip. Graph's reported `size` can exceed the real decoded byte count, so neither a size match nor a size mismatch proves anything; the hash is the proof.
7. **Hand back.** Reply with the clickable `webLink`, recipient, subject, attachment filename, and any body content still awaiting Deep's decision. The draft stays unsent until step 8.
8. **Send, only on explicit approval.** The tool description's promise of a send path is not evidence: confirm a send-capable tool actually exists in the live toolset before building a plan around one, and say plainly which mechanism you found or didn't. When Deep has approved sending this exact mail:
   - **Resolve the send mechanism at scope time (step 1), not at the end.** Probe in order: (a) `tools/list` on the ms365 server for a send-capable tool, (b) Outlook for Mac via AppleScript, (c) `himalaya account list` for a configured SMTP account. Raise any missing permission, or the fallback of Deep pressing Send on the staged draft, as a decision card while the draft is being staged, so a grant never becomes the last blocker right before a deadline.
   - **Probe macOS automation consent with a real object query, never `get version`.** `tell application "Microsoft Outlook" to get version` answers even when automation consent is missing, so it proves nothing about the send path; query an object instead (`count messages of folder "Drafts"`). Error `-1743 Not authorized to send Apple events` means the TCC automation grant is absent: Deep enables it at System Settings → Privacy & Security → Automation → (host app) → Microsoft Outlook, or sends the staged draft himself.
   - **Send, then prove it.** After the send call returns, read back: `get_mail_message` shows `isDraft: false` with `sentDateTime` set, or the subject appears in Sent Items. The send call's own success is not proof; a mail that silently stays in Drafts looks exactly like success from the caller's side.
   - If no mechanism is available, say so plainly, leave the draft staged with its `webLink`, and name the decision card. Never claim sent.
9. **Batch staging for a handoff pack.** When a task batch needs many mails staged: resolve every recipient first by searching the vault (regex a person-name fragment against `[a-z0-9._-]+@domain` across `Atlas/`, `_config/`, `Calendar/`, `Efforts/`); then create the drafts, several `create_draft_email` calls per turn is fine. Deliver them as a per-day pack at `Atlas/Ops/Dispatch/Ready to Send <date>.md` with four sections: **GO** (table: subject | To | Kanban card id), paste-ready WhatsApp/Flock texts, **WAIT** (drafts held and why), and work running without Deep. Each GO row ties to a card whose body names the exact draft subject, so one reply (`sent`) closes both surfaces. The card is created blocked with the `kanban-task-intake` decision shape and lists every staged subject with its To and cc, because Deep answers from the card and never opens the Drafts folder to discover what he is approving; state the default (`hold`) and its deadline so silence is an answer. Address discovery, batch drafting and card pairing are coordinated with `kanban-task-intake`.

## Pitfalls

- **`list_mail_attachments` on a marketing or delivery mail can return megabytes of inline base64.** Every `isInline: true` image rides along as `contentBytes`, so the tool result spills to a cache file instead of the conversation, and that spilled JSON carries raw control characters a strict `json.loads` rejects. Parse it with the tolerant `json_parse` helper from `hermes_tools`, not `json.loads`. When you only need the file inventory, ask for `name,contentType,size,id` so `contentBytes` never comes back.
- Attaching before checking the file: the draft exists but the deliverable cannot complete, leaving a half-built draft. Validate path, size, and type first.
- Base64 mistakes: `contentBytes` is base64 of the raw bytes, not a path or hex. Python: `base64.b64encode(Path(p).read_bytes()).decode()`.
- Typing `contentBytes` by hand into a tool-call argument: it multiplies output tokens by ~1.33 and a single transcription error silently corrupts the attachment. Generate the base64 in code and pass it over stdio.
- Reporting "the attachment is too fragile to add, attach it yourself" without having tried: the attachment is required, so an unattempted claim dumps the step on Deep. Attach in code first (step 3 with the stdio recipe); only a real error from Graph, quoted verbatim, downgrades the handoff to "attach before sending", and the draft then reads `hasAttachments: false` on read-back.
- Claiming success from the attach call's `success: true` alone. The only proof is `list_mail_attachments` showing the file.
- Leaving the superseded attachment in place after re-attaching an edited file: Deep sends two versions of the doc. Delete the old attachment id and re-list; the final count must match the intended set exactly.
- Stripping internal markings or reviewer notes from a file with no pre-edit snapshot: when Deep later asks "exactly what changed", you can only answer from memory. Copy the pre-cleanup file to scratch first, then diff old vs new and report the exact deltas.
- Returning the OData `id` instead of `webLink`: Deep cannot open the draft from the id.
- Parsing the `mcp_servers` block out of `config.yaml` inside `execute_code`: the sandbox has no `yaml` module. Read the block with `search_files`/`read_file` or parse it in `terminal`, which has the project interpreter.
- Draft body naming a shareable page or document link that was never actually published.
- Stating an assumption as a fact. If the draft needs a detail nobody confirmed (who approves an access request, which domain TLD to buy), write the conditional sentence with the tag `[CONFIRM: field]` so the gap is greppable, then list every such assumption in the reply so he can strike it before sending. A draft still carrying tags is not sendable as-is, so name it and its tags on the decision card rather than reporting the draft as ready.
- Guessing a recipient's address because the person is obviously real: a wrong address turns a review step into a sent misfire. Search the vault; if no address exists in the vault or the mailbox, leave `toRecipients` empty, put the draft under WAIT in the pack, and flag the missing address in your reply. Empty To is recoverable, a wrong To is not.
- Reporting old vault rows as open work without saying their state is unverified. Mail threads and task rows drift apart: label each bucket (live now, unconfirmed) and name the sources checked and not checked.
- Treating a successful `get version`, or an AppleScript that returned without an error, as proof the send path works: version answers without macOS automation consent, and the script only proves it ran, not that the message left the Drafts folder. Probe with an object query before promising the send, and read the message state back after it.
- Fixing a wrong name, amount, or missing attachment AFTER the draft exists. With no edit-draft tool, each fix is a fresh `create_draft_email` and the superseded draft lingers for Deep to delete manually. Get the facts and the attachment set right in step 1; treat the create call as irreversible.
- Leaving a superseded draft unflagged once a replacement exists. Deep sees two plausible drafts in one folder and may send the wrong one. Every replacement must restate in the same reply the exact subject of the draft to SEND and the exact subject to DELETE, so the choice never depends on opening either.

## Verification

- [ ] Draft read back with `isDraft: true` and expected recipients and subject.
- [ ] Attachment present in the read-back, or the reported reason is a quoted tool error, not an unattempted "too fragile".
- [ ] Attachment read back with exact filename and size; content-hash match when the file's contents are in question.
- [ ] Reply contains the clickable `webLink`.
- [ ] After any re-attach, the attachment list shows exactly the intended files (old ids deleted), and for content questions the downloaded bytes match the local file.
- [ ] Nothing was sent without explicit approval; on an approved send, read-back shows `isDraft: false` (or the subject in Sent Items), never just the send call's success.
