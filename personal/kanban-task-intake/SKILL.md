---
name: kanban-task-intake
description: "Use when Deep hands over tasks or asks about blocked cards."
---

# Kanban task intake

Deep wants every task he gives in chat to land on the Kanban board (`hermes kanban`, default board, `~/.hermes/kanban.db`) and every block to read as a decision he can answer in one word. Three things auto-feed the board: this skill in chat, the Issue Autopilot (GitHub issues), cron `d741846ee693` meeting-action-watcher (every 20 min 09:00 to 01:59 IST: each finished Wispr meeting becomes Outlook drafts for the emails Deep owes, running cards for bigger deliverables, TASKS.md rows tagged `[draft:outlook:<subject>]` or `[kanban:<id>]`, and a telegram-brief), and cron `9a042ac04419` kanban-intake-sweep (six times a day, 15:20 to 01:20 IST). The sweep cards every open TASKS.md row under This Week and Active that has no `[kanban:<id>]` tag, plus Wispr scratchpad to-dos. Agent-doable rows become `--triage` cards; Deep-only rows become blocked decision cards (assignee default, section 3 body, plus an optional `Prep:` triage card for a draftable step). P0/P1 rows are always in scope (any date, no cap); other rows only if captured in the last 10 days, max 8 per run. Telegram: only P0/P1 agent cards are subscribed; decision cards and P2+ cards are never subscribed, Deep reviews decisions in the swipe digest. The row is stamped `[kanban:<id>]` so it is never carded twice. Wispr meetings reach the board through zoom-meeting-followup-sweep writing TASKS.md rows first. Triage cards are auto-decomposed or specified by the aux LLM each dispatcher tick (`kanban.auto_decompose`, default true), so a triage card becomes running work within minutes without anyone touching it. To re-card a row, delete its `[kanban:]` tag.

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

**Write scope as a boundary, not a literal instruction.** A card that says "lift this file, adapting imports only" blocks the moment the donor code contradicts it, because the worker cannot tell whether fixing a hard FK, a wrong default or a missing test is in scope. The block is the card's fault, not the worker's: state the intent ("minimal behavioral and schema changes inside these named files where the target requires them") next to what stays out (unrelated modules, other subsystems), and the worker proceeds without asking. A literal rule reads as precise but is the fragile version of a boundary.

Then approve the boundary where it lands: comment the ruling on the card **and** on any sibling or sub-card that inherits the original wording, and unblock. Approvals exist only on cards, so a ruling scoped to one card leaves the next worker to guess the same boundary again.

**Pin the spec, not the workspace.** Name the spec's absolute path in every card body as read-only, and state where work may live (scratch, `~/repos/<name>`). Never let a card imply a checkout inside the Obsidian vault: a codebase in the vault breaks every vault-wide script. When a card body does name a wrong path, correct it with a comment on the next worker's card before it runs, not in chat.

**Declare tool dependencies in the card body.** A card that needs a tool the worker's profile may not carry (an MCP connector, a credential) must name it and state the failure move: "If Outlook is unreachable, block with kind=capability and say so." Otherwise the worker either stalls on an unclear error or silently produces work from no source. Blocking for a missing tool is a capability block, never needs_input.

**Pair cards with staged artifacts.** When a card's action is "Deep sends the thing you drafted", the body names the artifact precisely enough to find it unaided: surface and exact title (e.g. `Outlook Drafts, "<subject>"`), what still has to be filled (an empty To field), and the closing reply (`sent` or `A on <id>`). A card that says "send the recap" without saying where the recap lives strands the next reader.

**A staged draft is not done.** If the card's last mile is Deep sending, posting or paying, the card ends blocked with a decision card naming the exact draft, never `kanban_complete`. In Oct 2026 at least 8 cards closed as done with the send still on Deep and the TASKS.md rows stayed open, which is how tasks slipped. Batch the day's staged sends into one blocked `Send Pack <date>` card instead of one card each.

**Kanban-only (standing 2026-10-22).** Deep handles all tasks on the board. Deep-only rows also become cards (created blocked, decision-card body; body = `Row: TASKS.md line N` plus the section 3 shape with Do it / Already done / Drop as A/B/C, so one swipe answers it); TASKS.md stays the record and never moves. The backlog migration (2026-10-23) ticked CLOSE/ARCHIVE/MERGE rows in place with a `[migrated <date>: ...]` note; the scripts are `~/.hermes/scripts/tasks_migration_classify.py` and `tasks_migration_apply.py`. A process that carries `HERMES_DELEGATED_CHILD_CONTEXT` (some kanban workers do) cannot use `hermes kanban create`; use the `kanban_create` tool there, or run the script from a normal shell or cron, and pass `workspace_kind=scratch` (the tool defaults to a vault worktree). Section 6 covers the whole failure class this produces, board-wide as well as one card. Lanes: `default`, `worker`, `frontend`, `inbox` (mail drafts), `content` (social posts and video scripts; its SOUL carries the value-first, no-pitch voice). Profile SOULs live at `~/.hermes/profiles/<name>/SOUL.md` and are re-read at each worker spawn; `hermes profile describe <name> --text` sets the routing description.

## 1b. Clearing a blocked backlog (`~/.hermes/scripts/kanban_clear.py`)

Never present 300 blocked cards one by one. The sweep once carded every DEEP row individually, including September rows, and left 364 blocked cards. The fix is packs and expiry, then one reply line:

```bash
python3 ~/.hermes/scripts/kanban_clear.py triage      # ~/.hermes/cache/blocked-triage.md: EXPIRED / SEND / CALENDAR / KEEP, Deep approves the lists
python3 ~/.hermes/scripts/kanban_clear.py expire      # archives EXPIRED (title dated more than 3 days past) with a comment, TASKS.md row stays
python3 ~/.hermes/scripts/kanban_clear.py fold send   # one running inbox card carrying every send card's body, originals archived with a pointer
python3 ~/.hermes/scripts/kanban_clear.py sheet       # RETRY / ACCESS / DECIDE sheet for what is left
python3 ~/.hermes/scripts/kanban_clear.py apply "go t_a t_b; drop t_c; done t_d; retry all"
```

Buckets are regex on title and body, so Deep approves the triage lists before `expire` or `fold` runs. The sweep now never cards a send row alone (it goes into the day's `Send Pack <date>` inbox card) and never cards a row dated more than 3 days past (tagged `[kanban:stale]`).

## 1c. Swipe triage: let Deep clear blocked cards one gesture at a time

`kanban_clear.py` is list mode (he approves a bucket). When he asks for cards "one by one" or a swipe or decision interface, use the card mode instead: `~/.hermes/scripts/swipe_triage.py`, a single-file stdlib HTTP server reading `kanban.db` read-only on `127.0.0.1:3177`.

```bash
nohup python3 ~/.hermes/scripts/swipe_triage.py >/tmp/swipe.log 2>&1 &   # restart if it is not listening
lsof -nP -iTCP:3177 -sTCP:LISTEN                                          # prove which process owns the port
curl -s localhost:3177/api/cards | python3 -c "import sys,json,collections as c;d=json.load(sys.stdin);print(len(d),c.Counter(x['kind'] for x in d))"
```

Report the composition (how many are `human` to-dos, `needs_input` decisions, `capability` blocks, how many have a lapsed default date) before he starts swiping: the mix decides whether he should run the Decisions chip first. He answers a decision by tapping an option button or pressing its letter, which comments the choice and unblocks, so a card whose options parse gets answered in one gesture instead of a chat round trip.

The three destructive-ish CLI semantics the interface is built on, all verified by running them on throwaway cards rather than from the help text:

- `hermes kanban complete` works straight from `blocked` (no unblock first); `hermes kanban archive` also works from `blocked`.
- `hermes kanban unblock` only accepts `blocked` or `scheduled`, so it fails with "not blocked/scheduled" on an already-archived card, and neither archive nor complete can be undone: there is no reopen for them.
- Therefore build the undo window in the client, not in the CLI: hold the action ~5 s behind an Undo toast and commit only when the timer fires, flushing any pending action with `navigator.sendBeacon` on unload so a tab close still commits it instead of silently dropping his decision. An immediate-fire action with an "undo" button is a lie on an irreversible command.

Prove the write path before he touches it: create a throwaway card, block it, drive the endpoint (pick, drop, malformed id), and archive the test cards. A POST that only returns 200 proves nothing; read the card's status back. Validate the id server-side (`^t_[0-9a-f]+$`) since the id arrives from the browser and goes straight into a shell command.

Always show why a card is blocked, not just the title: the reason lives in the latest `task_events` row of `kind='blocked'` (payload `reason`), not in a `tasks` column, and a reason of `initial_status` means "created blocked with no cause" and should render as empty rather than as noise. Surface a `Default if silent by <date>` that has passed as a visible flag on the card, because a lapsed default is the fastest thing to rule on. Options only become buttons when the reason follows the section 3 `A:` / `B:` shape; cards that do not, show their text only, which is the argument for keeping the format mandatory.

Serve it on 127.0.0.1 with the port read from one constant and probe the port with `lsof` before shipping the script, because ports in the 3100+ range on this machine are already claimed by other Hermes scripts and a bind failure is silent from the browser's side (the page just fails to load). Card writes go through the `hermes kanban` CLI, never raw SQL: the CLI is what records events, comments and notifications the dispatcher and dashboard read.

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

## 6. Board-wide spawn failures: diagnose and repair the class, not the card

Several cards dying at spawn with `git worktree add failed for <vault>/.worktrees/<id> ... fatal: invalid reference: HEAD` is one fault, not many. The vault is not a git repo and the nearest ancestor repo can have an unborn branch (zero commits), so no worktree command can ever succeed there. A card inherits its workspace kind from the board, so a whole board can be pointed at an impossible workspace while every card body looks fine.

Diagnose in this order, in one batch, before touching anything:

```bash
sqlite3 -header ~/.hermes/kanban.db "select status,count(*) from tasks group by status"   # blast radius first
<board dir>/board.json   # project_id: if set, open cards inherit project worktrees
git -C <vault> rev-parse --git-dir --is-inside-work-tree; git -C <parent-repo> log -1 --oneline 2>&1
node -e 'require("os").totalmem()'; grep -n max_in_progress ~/.hermes/config.yaml
```

The repair has three parts, in this order:

1. **Fix the cause before releasing work.** Unscope the board from the project (edit `board.json` / the board setting) and set `kanban.max_in_progress` explicitly. `max_in_progress` is the only concurrency brake: when unset the dispatcher derives a default from `/proc/meminfo`, which does not exist on macOS, so it silently returns None and spawns every ready card at once (200+ workers, load in the hundreds). Write the config with `hermes config set kanban.max_in_progress 6`; the file patch tool refuses to write `config.yaml` on purpose.
2. **Retarget open cards in one SQL pass, not card by card.** Back up `kanban.db` with a timestamped copy first, then set the open cards to a workspace kind that cannot fail (`workspace_kind='dir'`, `workspace_path` at the vault, `project_id` NULL) with a single UPDATE. Thousands of cards become repairable in one call.
3. **Then unblock.** Cards blocked *only* by the spawn failure: clear the block, reset `consecutive_failures` to 0, leave the error text so the history stays readable. Cards blocked for a real reason stay blocked (their `consecutive_failures` stands: those are real crashes); only their workspace is fixed.

Order matters, because unblocking releases the queue. A mass unblock on an uncapped dispatcher starts hundreds of workers in one tick, and mass-terminating them afterwards is gated on user consent and can time out silently. Set the cap first, unblock in small batches if the cap is new, and never report a kill you did not watch return 0.

Pitfalls:
- **Read the cap logic in the shipped source, not the config schema.** `resolve_max_in_progress` / `configured_max_in_progress` in `hermes_cli/kanban_db_dispatch.py` is the authority on what unset means on this machine.
- **The breaker counts every requeue.** A killed or crashed worker is one strike against a limit of two, so a wholesale kill of a just-unblocked batch walks every card to the edge of the dispatcher's circuit breaker.
- **Verify with counts, not intent.** Re-run the status GROUP BY and the worker process count (`pgrep -f 'hermes_cli.main -p .* --cli' | wc -l`) after each step; a repair that changed the DB but not the running processes is not done.
