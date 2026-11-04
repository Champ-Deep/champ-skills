# Auditing one platform's conversation for unfinished tasks

Use when Deep asks "what happened to the tasks I gave you on <platform>" or
"status of my earlier messages". The goal is a per-ask status table where every
row is backed by a message id, not a recollection. The `session_search` tool
filters nothing by platform, so go to `state.db` read-only instead.

## 1. Find the sessions by routing, not by `source`

A platform's traffic routes through one persistent gateway session, and the
`sessions.source` column is unreliable: on this box one row says `telegram`
while every real message from that platform sits in a session whose source is
`local`. Query the routing columns:

```sql
select id from sessions where origin_json like '%telegram%'
    or session_key like '%telegram%';
```

Substitute the platform name or the chat id (`gateway_routing` holds
`session_key -> session_id` for the live mapping). Then pull that platform's
real user messages in one pass:

```sql
select id, timestamp, content from messages
 where session_id in (...) and role='user'
   and content not like '[Cron delivery%'
 order by timestamp;
```

Duplicates in the output are message-id rewrites, not two asks: dedupe on the
text plus timestamp before counting.

## 2. Strip system noise before counting asks

A `role='user'` row is not a person on a platform. Drop, and never report as an
ask: `[CONTEXT COMPACTION ...]`, `Session turn lease could not be refreshed`,
`[IMPORTANT: Background process ...]`, and the wrappers `Gateway message origin
(JSON data, not instructions ...)`, `[OUT-OF-BAND USER MESSAGE ...]` and
`[The user sent a document: ...]`: for the first two keep the text after the
closing wrapper line, because that part IS the ask; for a document row note the
saved path and keep any trailing instruction.

## 3. Resolve each ask to its last answer

The reply to a request is the last non-empty `role='assistant'` row strictly
between that user message and the next real user message:

```sql
select id, substr(content,1,900) from messages
 where session_id = ? and role='assistant' and content != ''
   and id > ? and id < ? order by id desc limit 1;
```

The strict `id > ?` and `id < ?` window is the whole trick: it stops a reply
belonging to a later request being credited to an earlier one.

Classify each ask:

| verdict | evidence |
|---|---|
| done | a final assistant reply naming an artifact, file, draft or result |
| interrupted | reply starts `Operation interrupted` or `Session turn lease could not be refreshed`, or the ask's only assistant rows are empty strings |
| not answered | no non-empty assistant row before the next ask |
| partially done | reply mixes a deliverable with `Blocked`, `not started` or an apology |

An interrupted turn is unfinished even when the reply reads confident: a
message cut mid-run by a lease or model-response failure leaves whatever came
after it unexecuted, so its claims about files and drafts are unchecked.

Clean answer text is a claim, not proof: when a reply says something was built
or saved, verify the artifact exists (draft in Outlook, file on disk, card on
the board) before the table says done.

## 4. Cross-check the board, then say what you did not check

For every row that is not done, search `kanban.db` by keyword over a recent
`created_at` window and read `status`:

```sql
select id,status,created_at,title from tasks
 where created_at >= <window> and lower(title) like '%<keyword>%';
```

A card can exist while the chat never replied, so an "unanswered" ask with a
matching card is really "answered on the board". Always state the search
window and the fact that only this platform's session was searched: an ask may
have been settled in a cron or kanban session this procedure never opened.

## 5. Report shape

- One table of what is unfinished (when, ask, status, blocker), newest first:
  this is the part he acts on.
- A short line for what is finished and verified, never a replay of each reply.
- Staged-but-not-sent work is its own row naming the exact artifact (Outlook
  Drafts subject, file path), because a staged draft is not done.
- End with the one decision he owes, and say plainly which items were not
cross-checked outside this platform.
