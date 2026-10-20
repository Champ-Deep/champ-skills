# Grounding an Outlook draft in the live thread

Recipe for finding what the team or counterparty already said before drafting, using the `mcp__ms365__*` Graph tools.

## One-call search

`mcp__ms365__list_mail_messages`:

- `search`: one KQL string in double quotes, e.g. `"(to:ithelpdesk OR from:ithelpdesk OR from:nandish OR to:nandish) AND received>=2026-10-14"`. `$search` and `$filter` cannot be combined, so fold the date range into the KQL.
- `select`: `id,subject,from,receivedDateTime,bodyPreview,isRead`. Never request `body` on a list call.
- `top`: 25. Follow `@odata.nextLink` for more pages; a result set with `result_has_more: true` is truncated, not exhausted.
- `orderby: receivedDateTime desc` when the newest items are what matters.

## Reading the threads

- `get_mail_message` with `select: subject,body` for the two or three threads that are actually live. Fetching bodies for every search hit burns context on threads that are closed.
- Ticket metadata lives in the subject: `[Request ID :##RE-xxxxx##]` and `Ticket Created [Request ID: #xxxxx]`. Carry the ID into the draft so the team can act on it.
- An acknowledgement-only reply (`ticket created`, no work reported) means still open. A reply that reports the change means closed; drop it from the draft.

## Handoff

- Draft via `create_draft_email`, then return the `webLink` (never the OData id) plus recipient, subject, and any assumption written into the body.
- Say explicitly that the draft is unsent and list the assumptions as lines Deep can delete.
- State the search window and the surfaces not checked (chat apps, other mailboxes) when the claim is "this is everything pending".
