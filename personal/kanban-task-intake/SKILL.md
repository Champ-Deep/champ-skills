---
name: kanban-task-intake
description: "Use when Deep hands over tasks or asks about blocked cards."
---

# Kanban task intake

Deep wants every task he gives in chat to land on the Kanban board (`hermes kanban`, default board, `~/.hermes/kanban.db`) and every block to read as a decision he can answer in one word. Three things auto-feed the board: this skill in chat, the Issue Autopilot (GitHub issues), cron `d741846ee693` meeting-action-watcher (every 20 min 09:00 to 01:59 IST: each finished Wispr meeting becomes Outlook drafts for the emails Deep owes, running cards for bigger deliverables, TASKS.md rows tagged `[draft:outlook:<subject>]` or `[kanban:<id>]`, and a telegram-brief), and cron `9a042ac04419` kanban-intake-sweep (six times a day, 15:20 to 01:20 IST). The sweep cards agent-doable TASKS.md rows (This Week and Active, captured in the last 10 days) and Wispr scratchpad to-dos as `--triage` cards, max 8 per run, and stamps the row with `[kanban:<id>]` so it is never carded twice. Deep-only rows with no prep step stay in TASKS.md; the sweep never creates blocked cards. Wispr meetings reach the board through zoom-meeting-followup-sweep writing TASKS.md rows first. Triage cards are auto-decomposed or specified by the aux LLM each dispatcher tick (`kanban.auto_decompose`, default true), so a triage card becomes running work within minutes without anyone touching it. To re-card a row, delete its `[kanban:]` tag.

## 1. Intake: split the list, then create cards

For each task Deep gives (a list, a pasted plan, a run sheet):

| Task type | Card | Why |
|---|---|---|
| An agent can finish it end to end (draft, research, code, file, verify) | `kanban_create(assignee=..., initial_status="running")` so the dispatcher spawns a worker | Work starts within 60 s, no human in the loop |
| Needs Deep's own hands (send a WhatsApp, call Chief, approve money, sign) or a ruling only he can make | `kanban_create(initial_status="blocked")` with the body written as a **decision card** (section 3) | Sits in Blocked from birth, no worker burnt, his answer unblocks it and a worker does the follow-through |
| Already a TASKS.md row | Still create the card; put `[TASKS.md: <row title>]` in the body so the vault row and the card are the same work | One surface for "what is waiting on me" |

Assignees: `default` for vault, email and ops work; `worker` for cheap mechanical lanes; `frontend` for UI. Set `parents` when a card cannot start until another finishes (dependency, not a block).

Subscribe every card to Telegram so blocked, review and done events reach Deep without opening the dashboard:

```bash
hermes kanban notify-subscribe <id> --platform telegram --chat-id 8225744637 --user-id 8225744637 --chat-type dm
```

Also keep the TASKS.md row (vault conventions still apply). The card is the execution surface, the row is the record.

**Bulk intake (10+ cards): create from code, not tool calls.** Write each body to a temp file and drive the CLI in one `execute_code` pass:

```bash
hermes kanban create "<title>" --body-file <tmp.md> --assignee default --priority 85 --initial-status blocked --created-by default --json
# parse the id from the JSON (fall back to grepping t_[0-9a-f]{8} from stdout), then:
hermes kanban notify-subscribe <id> --platform telegram --chat-id 8225744637 --user-id 8225744637 --chat-type dm
```

One pass creates and subscribes dozens of cards in under a minute; temp files avoid shell-quoting multi-line bodies. Emit a `tid  priority  status  title` line per card as you go so the summary you report matches what was actually created.

**Declare tool dependencies in the card body.** A card that needs a tool the worker's profile may not carry (an MCP connector, a credential) must name it and state the failure move: "If Outlook is unreachable, block with kind=capability and say so." Otherwise the worker either stalls on an unclear error or silently produces work from no source. Blocking for a missing tool is a capability block, never needs_input.

**Pair cards with staged artifacts.** When a card's action is "Deep sends the thing you drafted", the body names the artifact precisely enough to find it unaided: surface and exact title (e.g. `Outlook Drafts, "<subject>"`), what still has to be filled (an empty To field), and the closing reply (`sent` or `A on <id>`). A card that says "send the recap" without saying where the recap lives strands the next reader.

**A staged draft is not done.** If the card's last mile is Deep sending, posting or paying, the card ends blocked with a decision card naming the exact draft, never `kanban_complete`. In Oct 2026 at least 8 cards closed as done with the send still on Deep and the TASKS.md rows stayed open, which is how tasks slipped. Batch the day's staged sends into one blocked `Send Pack <date>` card instead of one card each.

**Kanban-only (standing 2026-10-22).** Deep handles all tasks on the board. Deep-only rows also become cards (created blocked, decision-card body); TASKS.md stays the record and never moves. Lanes: `default`, `worker`, `frontend`, `inbox` (mail drafts), `content` (social posts and video scripts; its SOUL carries the value-first, no-pitch voice). Profile SOULs live at `~/.hermes/profiles/<name>/SOUL.md` and are re-read at each worker spawn; `hermes profile describe <name> --text` sets the routing description.

## 2. What "blocked" means

`kanban_block(kind=...)` routes by cause. Only two kinds need Deep.

| kind | Where it goes | Who acts | Deep's move |
|---|---|---|---|
| `dependency` | `todo`, auto-promotes when the parent finishes | nobody | none |
| `needs_input` | `blocked` | Deep | answer the decision card, then unblock |
| `capability` | `blocked` | Deep or IT | grant access or a credential, then unblock |
| `transient` | `blocked` | agent | unblock, it reruns |
| (dispatcher auto-block after 2 crashes) | `blocked`, shows in Diagnostics | agent | treat as transient: unblock once; if it crashes again, read `hermes kanban log <id>` |

Loop breaker: a card blocked, unblocked and re-blocked for the same kind twice lands in `triage`. That is the board saying "the cause was never fixed", so fix the cause before unblocking a third time.

## 3. Decision card format (mandatory for every `needs_input` block)

The block reason, and the body of any card created blocked, must be this shape and nothing longer. Evidence goes in a comment, not the reason.

```
DECISION: <one question, yes/no or pick one>
A (recommended): <option, one line, what happens next>
B: <option>
C: <option, usually "hold" or "cut">
Default if silent by <date/time IST>: <A or hold>
Reply: "A on <task id>" (or comment on the card)
```

The recommended option comes first and is the one that is reversible or cheapest. If no option can be recommended honestly, say "no recommendation, need X from you" and name X.

Put the same contract in every card body you create, under a heading `If you must block`, so workers on other profiles inherit it without a config change.

## 4. Answering a block

Deep replies in chat ("A on t_63fcbc19") or on the card. Then:

```bash
hermes kanban comment <id> "Deep: A. <one line of what that means>"
hermes kanban unblock <id>
```

Quote the approval and its scope in that comment: which worktree or build it applies
to, and what remains held. Workers see the card, never the chat, so an approval scoped
only in chat leaves the next worker to guess the boundary.

For "hold" or "cut": `hermes kanban archive <id>` with a comment, do not leave it in Blocked.

## 5. Reading the board for Deep

"What is waiting on me" = `kanban_list(status="blocked")`, then present one decision card per task in the section 3 shape. Never paste a worker's full block paragraph; rewrite it as a decision card and add the rewrite as a comment on the card so the dashboard shows it too.
