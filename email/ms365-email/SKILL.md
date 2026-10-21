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

Don't use for: inbox triage or reply policy (`email-inbox-triage`), terminal IMAP/SMTP (`himalaya`), Gmail or Drive (`google-workspace`).

## Always-on rules

- Draft, never send. Outbound mail is irreversible and Deep reviews and sends it himself. Return the draft's `webLink`, never the raw message id, so he can open it in one click.
- Deliver attachments inside the draft. If Deep asks for "the doc", the file is attached to the Outlook draft, not merely linked in chat.
- Every write is verified by read-back before it is reported done. A successful tool call is not a successful draft.
- Never put a link in the body that was not actually produced. Omit the sentence and say the link is unavailable rather than inserting a placeholder.

## Procedure

0. **Ground the draft in the live thread.** Before writing, find what the team already said: one `mcp__ms365__list_mail_messages` call with a KQL `search` OR-ing `to:`/`from:` addresses and a `received>=` floor, `select` limited to id/subject/from/receivedDateTime/bodyPreview/isRead, `top: 25`, then page with `@odata.nextLink`. Read full bodies only for the threads in scope via `get_mail_message`. Re-drafting an unanswered thread without its last reply loses the promised date and the ticket number. Full recipe: `references/thread-search-recipes.md`.
1. **Resolve scope.** Recipient address(es) and display names, subject, body facts, attachment file path. Confirm the attachment exists, is non-empty, and note its size and MIME type before creating anything.
2. **Create the draft.** `mcp__ms365__create_draft_email` with explicit `toRecipients`/`ccRecipients`/`bccRecipients`, `subject`, and `body: {contentType: "text", content: ...}`. Set every recipient field explicitly rather than relying on defaults. Keep the returned `id` and `webLink`.
3. **Attach the file.** Build `body` as `@odata.type: #microsoft.graph.fileAttachment`, `name`, `contentType`, `isInline: false`, `contentBytes` as base64 of the raw bytes, with `messageId` as the top-level argument.
   - **Base64 larger than ~2-3 KB goes through the stdio recipe in `references/direct-stdio-mcp.md`, not an inline tool call.** Emitting the blob as a tool-call argument means generating the whole base64 through my own output tokens: a 20 KB zip costs ~27 KB of typed text and a single transcription error corrupts the attachment with no error surfacing. Generate the base64 inside `execute_code`/stdio code. This applies whether or not the tool is exposed in the live toolset; use stdio whenever the payload is big, not only when the tool is missing.
   - If Graph rejects `contentBytes` on size, switch to `create_mail_attachment_upload_session`.
4. **Verify.** `get_mail_message` (expect `isDraft: true`, `hasAttachments: true`, correct recipients and subject) and `list_mail_attachments` (exact filename, size, contentType). Report only what the read-back shows.
5. **Replace a stale attachment.** If the local file changed after it was attached, the draft still serves the old bytes. Re-run `add_mail_attachment` with the new content, then `delete_mail_attachment` the old attachment id (`confirm: true`), then `list_mail_attachments` again and confirm the list contains exactly the intended set: new file present, old id gone, expected count.
6. **Deep asks "confirm it has the changes".** Filename and size are not proof of content. Download the attached bytes with `mcp__ms365__download_bytes_to_file` (target `/me/messages/{messageId}/attachments/{attachmentId}/$value`, write to a scratch path that does not exist yet) and byte-compare against the canonical local file before answering.
7. **Hand back.** Reply with the clickable `webLink`, recipient, subject, attachment filename, and any body content still awaiting Deep's decision. The draft stays unsent.

## Pitfalls

- Attaching before checking the file: the draft exists but the deliverable cannot complete, leaving a half-built draft. Validate path, size, and type first.
- Base64 mistakes: `contentBytes` is base64 of the raw bytes, not a path or hex. Python: `base64.b64encode(Path(p).read_bytes()).decode()`.
- Typing `contentBytes` by hand into a tool-call argument: it multiplies output tokens by ~1.33 and a single transcription error silently corrupts the attachment. Generate the base64 in code and pass it over stdio.
- Claiming success from the attach call's `success: true` alone. The only proof is `list_mail_attachments` showing the file.
- Leaving the superseded attachment in place after re-attaching an edited file: Deep sends two versions of the doc. Delete the old attachment id and re-list; the final count must match the intended set exactly.
- Stripping internal markings or reviewer notes from a file with no pre-edit snapshot: when Deep later asks "exactly what changed", you can only answer from memory. Copy the pre-cleanup file to scratch first, then diff old vs new and report the exact deltas.
- Returning the OData `id` instead of `webLink`: Deep cannot open the draft from the id.
- Parsing the `mcp_servers` block out of `config.yaml` inside `execute_code`: the sandbox has no `yaml` module. Read the block with `search_files`/`read_file` or parse it in `terminal`, which has the project interpreter.
- Draft body naming a shareable page or document link that was never actually published.
- Stating an assumption as a fact. If the draft needs a detail nobody confirmed (who approves an access request, which domain TLD to buy), write the conditional sentence Deep can delete, then list every such assumption in the reply so he can strike it before sending.
- Reporting old vault rows as open work without saying their state is unverified. Mail threads and task rows drift apart: label each bucket (live now, unconfirmed) and name the sources checked and not checked.

## Verification

- [ ] Draft read back with `isDraft: true` and expected recipients and subject.
- [ ] Attachment read back with exact filename and size.
- [ ] Reply contains the clickable `webLink`.
- [ ] After any re-attach, the attachment list shows exactly the intended files (old ids deleted), and for content questions the downloaded bytes match the local file.
- [ ] Nothing was sent.
