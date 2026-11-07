---
name: kanban-task-intake
description: "Use when Deep hands over tasks or asks about blocked cards."
---

# Kanban task intake

## Block creation rule

Never create a bare blocked card. A blocked creation needs `initial_block_kind` and `initial_block_reason`; for a human decision, use `needs_input` and the section 3 `DECISION` shape with A (recommended) first. Create one decision parent and make every preparation a `todo` child with `parents=[decision card]`. A missing kind or reason is rejected, so agent-doable work must be created as todo or triage instead.

Deep wants every task he gives in chat to land on the Kanban board (`hermes kanban`, default board, `~/.hermes/kanban.db`) and every block to read as a decision he can answer in one word. Three things auto-feed the board: this skill in chat, the Issue Autopilot (GitHub issues), cron `d741846ee693` meeting-action-watcher (every 20 min 09:00 to 01:59 IST, 48 h lookback deduped by meeting id because Wispr notes finalize late: each finished Wispr meeting becomes Outlook drafts (sent automatically once a send tool exists and recipients were on the call or internal), running cards for docs and NDAs, ideation prep notes plus a 30-minute slot for plans, blocked decision cards for real decisions after the clef gate in factory-decision-gate, TASKS.md rows tagged `[draft:outlook:<subject>]`, `[sent:<date>]` or `[kanban:<id>]`, and a telegram-brief), and cron `9a042ac04419` kanban-intake-sweep (six times a day, 15:20 to 01:20 IST). The sweep cards every open TASKS.md row under This Week and Active that has no `[kanban:<id>]` tag, plus Wispr scratchpad to-dos. Agent-doable rows become `--triage` cards; Deep-only rows become blocked decision cards (assignee default, section 3 body, plus an optional `Prep:` triage card for a draftable step). P0/P1 rows are always in scope (any date, no cap); other rows only if captured in the last 10 days, max 8 per run. Telegram: only P0/P1 agent cards are subscribed; decision cards and P2+ cards are never subscribed, Deep reviews decisions in the swipe digest. The row is stamped `[kanban:<id>]` so it is never carded twice. Wispr meetings reach the board through zoom-meeting-followup-sweep writing TASKS.md rows first. Triage cards are auto-decomposed or specified by the aux LLM each dispatcher tick (`kanban.auto_decompose`, default true), so a triage card becomes running work within minutes without anyone touching it. To re-card a row, delete its `[kanban:]` tag.

## 1. Intake: split the list, then create cards

For each task Deep gives (a list, a pasted plan, a run sheet):

| Task type | Card | Why |
|---|---|---|
| An agent can finish it end to end (draft, research, code, file, verify) | `kanban_create(assignee=..., initial_status="running")` so the dispatcher spawns a worker | Work starts within 60 s, no human in the loop |
| Needs Deep's own hands (send a WhatsApp, call Chief, approve money, sign) or a ruling only he can make | `kanban_create(initial_status="blocked", initial_block_kind="needs_input", initial_block_reason="<DECISION line>")` with the body written as a **decision card** (section 3) | Sits in Blocked from birth, no worker burnt, his answer unblocks it and a worker does the follow-through |
| Already a TASKS.md row | Still create the card; put `[TASKS.md: <row title>]` in the body so the vault row and the card are the same work | One surface for "what is waiting on me" |

Assignees, since 2026-11-05 (lane table in `_config/bots.md`): `planner` (Opus) for anything that needs a PRD, a brief or a decomposition before work can start; `default` for vault, backend and ops work with a judgment call; `worker` for cheap mechanical lanes; `frontend` for UI; `inbox` for every Outlook draft or triage (default has calendar read only, no mail tools); `content` for Deep's public writing. Unassigned cards fall to `worker` (`kanban.default_assignee`), so an unassigned judgment card is a routing bug. Route by asking, not guessing: one `mcp_clef_ask` choice question per card (`kind`: plan / implement / ui / mechanical / content / email / decide) with the title and first lines of the body as state, then map kind to assignee; `decide` becomes a blocked decision card. Clef runs locally for free; TypeSafe Jev is the paid fallback when `TYPESAFE_API_KEY` exists (it does not today). Cross-provider routing happens only here, at the card: the per-turn Jev plugin can only re-tier inside one provider. Set `parents` when a card cannot start until another finishes (dependency, not a block). Before naming a lane, and before telling Deep which model a fan-out will use, read the `model-routing` skill: a `delegate_task` child runs on the root config's `delegation:` provider and model, never the chat's model, and work he asks to run "in this chat" is not delegated at all.

Subscribe every card to Telegram so blocked, review and done events reach Deep without opening the dashboard:

```bash
hermes kanban notify-subscribe <id> --platform telegram --chat-id 8225744637 --user-id 8225744637 --chat-type dm
```

Also keep the TASKS.md row (vault conventions still apply). The card is the execution surface, the row is the record.

**Bulk intake (10+ cards): create from code, not tool calls.** The full fan-out procedure (one spec file, directories pre-created, one body template, idempotency keys, gated review card, TASKS.md block in the same pass, status read-back) is `references/parallel-fan-out.md`. Minimum shape: Write each body to a temp file and drive the CLI in one `execute_code` pass:

```bash
hermes kanban create "<title>" --body-file <tmp.md> --assignee default --priority 85 --initial-status blocked --initial-block-kind needs_input --initial-block-reason "<DECISION line for this card>" --created-by default --json
# parse the id from the JSON (fall back to grepping t_[0-9a-f]{8} from stdout), then:
hermes kanban notify-subscribe <id> --platform telegram --chat-id 8225744637 --user-id 8225744637 --chat-type dm
```

One pass creates and subscribes dozens of cards in under a minute; temp files avoid shell-quoting multi-line bodies. Emit a `tid  priority  status  title` line per card as you go so the summary you report matches what was actually created.

**Write scope as a boundary, not a literal instruction.** A card that says "lift this file, adapting imports only" blocks the moment the donor code contradicts it, because the worker cannot tell whether fixing a hard FK, a wrong default or a missing test is in scope. The block is the card's fault, not the worker's: state the intent ("minimal behavioral and schema changes inside these named files where the target requires them") next to what stays out (unrelated modules, other subsystems), and the worker proceeds without asking. A literal rule reads as precise but is the fragile version of a boundary.

Then approve the boundary where it lands: comment the ruling on the card **and** on any sibling or sub-card that inherits the original wording, and unblock. Approvals exist only on cards, so a ruling scoped to one card leaves the next worker to guess the same boundary again.

**When a worker blocks because the brief conflicts with the source material, the brief is usually the defect.** Read the source lines it cites, decide the ruling, and write it into the source file itself (a doc, a spec, a copy pack) rather than only into a chat reply, then comment the ruling on the blocking card and `hermes kanban unblock`. The source file is what the next worker reads verbatim, so a conflict resolved only in chat re-litigates at the next card. The common shape is a blanket prohibition in the brief ("no client numbers", "no placeholders") that the real source violates; narrow the rule to what it was protecting (keep company facts, strip other clients' figures, keep a safe placeholder) instead of scrapping the copy.

**Close satisfied parents before completing their children.** `hermes kanban complete` refuses a card with open parents, so when one card's completion covers several sub-cards, check each parent first and complete or unlink the ones this work already settled, then complete the child. Report the cleanup in the summary so it reads as part of the work, not as scope creep, and never unlink a parent just to force a completion through.

**Pin the spec, not the workspace.** Name the spec's absolute path in every card body as read-only, and state where work may live (scratch, `~/repos/<name>`). Never let a card imply a checkout inside the Obsidian vault: a codebase in the vault breaks every vault-wide script. When a card body does name a wrong path, correct it with a comment on the next worker's card before it runs, not in chat.

**Declare tool dependencies in the card body.** A card that needs a tool the worker's profile may not carry (an MCP connector, a credential) must name it and state the failure move: "If Outlook is unreachable, block with kind=capability and say so." Otherwise the worker either stalls on an unclear error or silently produces work from no source. Blocking for a missing tool is a capability block, never needs_input.

**Answer "where are we with X" from evidence, not memory.** Batch the reads first: `kanban_list` for the cards, `git fetch` plus branch/ahead-behind and open-PR state in the repo, and the live endpoint if the thing is supposed to be deployed. Then present every claim tagged as **built / merged / deployed / none of those**, with the exact branch or card id behind it, and list the gaps as follow-up cards. A status answer that cannot name the branch, card or URL is a guess; the shared state that causes it is real: parallel lanes hold work in worktrees and separate branches that no chat history records.

**Re-run a finished card's verification before you report it.** A worker's completion summary is a self-report, not evidence: it routinely claims steps it skipped. Take its own test command, run it in your terminal, and read the output; also diff its claimed file list against what is actually on disk (`git -C <path> status --porcelain`, the named doc or script present and non-empty). Whatever its summary marks as skipped or deferred, and whatever it owes the next lane (the API contract a UI lane must build against, the branch the gate card must push), you do yourself in the same pass and land it on the branch before reporting. Report those as what you fixed, never as what the worker delivered.

**Deliverable missing is a defect, not a note.** When a card that was supposed to produce a handoff artifact (spec, contract, brief for a sibling lane) arrives without it, the fix is to write it from the code that exists, commit it on the lane's branch, and point the dependent cards at the absolute path in a comment. Leaving it as feedback for a later card strands the lane that needed it.

**A brief that assigns another lane's work is a defect even when it reads complete.** Card bodies get written fast and will hand a backend contract, a schema or a data model to a frontend lane, which then blocks asking who owns it. Before unblocking any blocked card, read its body against the routing table: any step that belongs to your lane you take back and land it yourself on the branch (endpoints, storage, base branch, tests), comment the delivered surface on the card with the commit, and only then unblock. The lane resumes on the part it can actually do; unblocking it to discover its own brief is wrong costs a whole worker cycle.

**A contract that changes while the card is running needs the lane restarted.**
Workers read the body at spawn and comments only at startup, so an edited body
never reaches a worker already in flight: edit the body, `reclaim` (uncommitted
work in the checkout survives), comment a resume note naming what to run first,
`dispatch`. The full sequence is in `model-routing`; a comment alone waits for
the next run.

**Fan out as a parent-linked card tree, block only on humans.** When one request splits into several workstreams with no decision only Deep can make, create the whole tree in one pass: an integration card, the lane cards with `parents` set to it, and a final review/gate card parented to the lanes. Gating by `parents` keeps the work in `todo` and releases it automatically; carding agent-owned work as `blocked` puts it in front of Deep for no reason. Only the inputs that genuinely need him (keys, credentials, spending approvals) become a card created with `initial_status="blocked"` plus `initial_block_kind="needs_input"` and an `initial_block_reason` in the section 3 shape, referenced by id from the gate card so the two are linked both ways.

- **Set the workspace at creation; never let a card inherit it.** A card created from a session whose active project is a vault (or any repo the work does not belong to) inherits that project, and the spawn then runs `git worktree add <that-repo>/.worktrees/<id>` in a tree that cannot host one, so the card dies twice and lands blocked with a `workspace:` reason that looks like a transient crash. Pass `workspace_kind` explicitly on every `kanban_create`, pass `project` only when the card genuinely belongs to that repo, and read `project_id` / `workspace_kind` back for the whole batch before reporting the cards as created: two failed spawns is already two wasted dispatch cycles, and the fix is one SQL pass at creation time instead of a section 6 repair later.
- **Create the children's worktrees before dispatch, then prove each path.** A `workspace_kind=dir` child inherits a path the parent was supposed to create, so the parent must `git worktree add` every sibling path from its final commit before it finishes. Preflight the parent's own path the same way at creation time. Then, immediately after dispatch, run one batched check over every path: the directory exists, it is a git worktree, and `git -C <path> log -1 --oneline` returns the expected commit. An empty directory fails silently on both sides: the child never notices and builds in the wrong folder, and the parent never notices because spawn reported success. A card whose workspace is empty gets a `kanban_comment` naming the real absolute path and branch before its agent has written anything; a comment posted after work has begun may never be read.
- **Attach evidence to the brief, not just a file name.** Name the exact identifiers a worker must pull (component ids, theme ids, endpoint paths) and the command that proves the source was reachable, so a paid connector sitting in the lane's profile gets used rather than the model inventing an approximation.
- **Every frontend card must end with a preview URL on the card.** Deep reads cards, not repos: the acceptance criteria name `~/.hermes/scripts/preview_deploy.sh <dist-or-html> <name> <task_id>`, which deploys a static build to Cloudflare Pages (`https://<name>.celsus-previews.pages.dev`, temporary, project `celsus-previews`) or, when the build calls `/api`, hosts it locally on a free 3100+ port beside its backend, then comments `PREVIEW: <url>` on the card. No preview comment, no review request. A fresh Pages project takes a few minutes before TLS answers; the hashed per-deploy URL wrangler prints works first.
- **For a UI card, make screenshots attachments, not claims.** A worker's summary saying "screenshots at 390 and 1280" with nothing on the card is not evidence; the acceptance criteria must name `kanban_attach` with the exact views to capture (filter state, drawer open, palette open, empty state), and you re-run the live check yourself before reporting the round done. State the taste skills to load in order in the body, name the component library as non-negotiable with the failure move (block kind=capability if its key is missing), and require a separate branch plus a second draft PR per round so rounds never share a branch.

**Pair cards with staged artifacts.** When a card's action is "Deep sends the thing you drafted", the body names the artifact precisely enough to find it unaided: surface and exact title (e.g. `Outlook Drafts, "<subject>"`), what still has to be filled (an empty To field), and the closing reply (`sent` or `A on <id>`). A card that says "send the recap" without saying where the recap lives strands the next reader. When the staging card completes, copy its artifact coordinates (exact subject, recipients, message or draft id, read-back result) from the report onto the decision card as a comment: the decision card is the only card Deep opens, and a staging card's metadata dies with its run. A consequential mail (a reprimand, a deadline, a money ask) carries its options as A / B / C where one option is sending as staged, one moves the date, and one holds for a call, with the consequence of each in a line, because he rules on the tone and the timing together, not just on whether to send.

****A staged draft is not done.**** If the card's last mile is Deep sending, posting or paying, the card ends blocked with a decision card naming the exact draft, never `kanban_complete`. The same gate covers every card, not only sends: "don't close things until done". Complete only when nothing of the work remains; when part remains, comment what is left and leave the card open or blocked. Draining a card beats marking it stale, and a board tidied by closing unfinished cards hides exactly the work he opened it to see. In Oct 2026 at least 8 cards closed as done with the send still on Deep and the TASKS.md rows stayed open, which is how tasks slipped. Batch the day's staged sends into one blocked `Send Pack <date>` card instead of one card each. The reverse failure is just as common: Deep sends from Outlook and never replies on the card, so Send Packs stay blocked for work already done (2026-10-30: 22 of 26 drafts on 7 open packs were already sent). Reconcile against Outlook Sent Items by subject before presenting a send list, and list Outlook Drafts directly rather than trusting the cards: drafts staged outside any card exist too. Cron `cf8a1b22741f` follow-through-reconcile does this at 15:30 and 23:30.

**Kanban-only (standing 2026-10-22).** Deep handles all tasks on the board. Deep-only rows also become cards (`hermes kanban create --initial-status blocked --initial-block-kind needs_input --initial-block-reason "<DECISION line>"`, decision-card body; body = `Row: TASKS.md line N` plus the section 3 shape with Do it / Already done / Drop as A/B/C, so one swipe answers it); TASKS.md stays the record and never moves. The backlog migration (2026-10-23) ticked CLOSE/ARCHIVE/MERGE rows in place with a `[migrated <date>: ...]` note; the scripts are `~/.hermes/scripts/tasks_migration_classify.py` and `tasks_migration_apply.py`. A process that carries `HERMES_DELEGATED_CHILD_CONTEXT` (some kanban workers do) cannot use `hermes kanban create`; use the `kanban_create` tool there, or run the script from a normal shell or cron, and pass `workspace_kind=scratch` (the tool defaults to a vault worktree). Section 6 covers the whole failure class this produces, board-wide as well as one card. For a bulk run from such a worker, schedule a one-shot `no_agent` cron job (`in 1m`, `deliver: local`) pointing at a script under `~/.hermes/scripts`: it runs in a clean environment where the CLI works. Always pass `--workspace scratch` to `hermes kanban create` (the board is project-scoped, so the default inherits a worktree and dies at spawn). Match source rows by full title, never by a stored line number (TASKS.md shifts between runs; recurring rows share a 25-char prefix) and key idempotency on a title hash. New Telegram subscriptions start caught up, so subscribing a freshly created blocked card sends nothing; `~/.hermes/scripts/tasks_migration_cards2.py` is the reference implementation. Lanes: `default`, `planner`, `reviewer`, `worker`, `frontend`, `inbox` (mail triage and drafts, the only profile with the Outlook mail MCP), `content` (social posts and video scripts; its SOUL carries the value-first, no-pitch voice). Every implementing lane hands off with `kanban_request_review(reviewer="reviewer")`; the reviewer completes or returns the card and patches the skill that caused a miss. Profile SOULs live at `~/.hermes/profiles/<name>/SOUL.md` and are re-read at each worker spawn; `hermes profile describe <name> --text` sets the routing description.

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

**Ranking: priority first, real due dates second.** Sections and sort order come from board priority (P0 = 90, P1 = 80, P2 = 60, P3 = 40, untagged 50), then due date, so P0 decision cards surface first. Before trusting the order, measure the bucket sizes (`/api/overview`, or a Counter over `/api/cards`): parse due dates only from real deadline markers, because the intake sweep's `Default if silent by <date>` line and `[captured:<date>]` tags read as due dates and stamp hundreds of cards with one fake deadline, `[e:<section>]` tags are export provenance and push cards into the wrong section, and a bucket keyed on a tag most cards carry (P1) floods the top section. Fix the parser, never the sort order.

**The decision log trains the decider.** Every ruling the swipe app commits appends a row to `~/.hermes/state/decision_log.jsonl` (id, kind, choice, answer, section, ts), and backfills from card history (blocked reasons plus the ruling comment) when the log is thin. That log is the training set for the gate; the label/tune/eval procedure lives in the `laya-local-decisions` skill.

**Composed briefs for thin block reasons.** Cards whose blocked reason gives Deep nothing to rule on get a composed decision brief (summary, the ask, options with consequences, timeline, amounts, people) from a cheap model: `~/.hermes/scripts/celsus_compose.py` composes the structure server-side and lets the model write only the text (a model asked for the whole card tree produces broken structure), posts JSON-only output to OpenRouter with reasoning explicitly disabled, and stores per-card output in `~/.hermes/state/celsus_cards.json` keyed by a digest of the prompt so a prompt change recomposes everything. The swipe app renders the brief in place of the raw reason when present. Run the first pass from a foreground shell with `--max N` so errors are visible; rerunning skips cards already composed at the current digest. A batch that returns 401 while the identical foreground command works is a stale `OPENROUTER_API_KEY` in the shell or cron environment overriding the `.env` value: read the key from `.env` inside the script and ignore the ambient variable, so background and foreground runs can never diverge. Bump `PROMPT_V` whenever SYSTEM text changes, because the digest is what forces a recompose; a stale background job then starts on the old prompt, so kill and restart running passes rather than letting two versions write to the same store.

**Confidence layer: score, gate, then let history earn the gate.** A decider can attach a per-card confidence to the same options so Deep knows which decisions are cheap to make. Score it with a local verifier, not a hosted one: no API key for the hosted variants exists on this Mac, and the local scorer runs in the same venv as the gate, so a claim about its confidence always names which scorer produced it. Then run its calibration gate before any auto-execute claim: if the 0.99 bucket has no labelled rows, `auto_allowed` stays false and nothing is executed, no matter how high the scores look. Report the histogram (how many clear 0.5 / 0.8 / 0.9 / 0.95 / 0.99) instead of an average, because the average hides that nothing qualified. The calibration set is only real when rows come from Deep's own picks, not from agent evidence comments written on a card, so treat labelled rows with a non-Deep provenance as unusable for calibration. Expect a position bias toward the first-listed option (the composer puts the recommended one first) and say so when reporting, rather than presenting agreement as accuracy.

**Filter facets come from the API, never from re-parsing titles in the client.** `GET /api/cards` carries the facets the UI sorts and filters on (`project`, `confidence`, `urgency` now/soon/later, `staleness` fresh/aging/stale, `kind`, `impact`, `effort`) computed server-side at the same moment the score is read, so a facet can never disagree with what is rendered. `project` is a closed vocabulary the composer extracts against (org-map company list plus effort names, else "Other") rather than a free title parse; add new companies by editing the prompt and bumping `PROMPT_V`. Compute urgency and staleness from priority, due and age at serve time, and check the bucket sizes afterwards: overdue dates carried from a lapsed default make most of the pile read as "now", which is a filter worth tightening, not evidence the pile is urgent.

**The board UI is the Hermes dashboard, not a separate app.** `hermes dashboard --no-open --skip-build --port 9119` serves the kanban; a dead board is a dead dashboard process, not a corrupt `kanban.db`. Order: probe `lsof -iTCP:9119 -sTCP:LISTEN -nP`, start it by hand if nothing holds the port, then prove the board answers (`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9119/`) before reporting it fixed. To make it survive reboots, write the LaunchAgent plist `ai.hermes.dashboard.plist` yourself (copy `EnvironmentVariables` from `ai.hermes.gateway.plist`); loading it is one command Deep runs in his own Terminal, since launchctl is refused inside a session (see `hermes-agent`, references/troubleshooting.md). A hand-started dashboard dies with the session, so say so rather than calling it fixed.

## 1d. Jev auto-go is live at 0.90 (Deep's ruling 2026-11-04)

`celsus_compose_cron.sh` now runs `celsus_jev.py auto --conf 0.90 --approved --apply` every 2h: a card whose scored pick clears every gate (>= 0.90, not `ask`, agrees with the composer's and the card's own recommendation, no hard rule or factory guard word) is executed. The verb comes from the picked option's label: archive/drop -> `archive` with a TL;DR comment, already done -> `complete`, hold -> left blocked for Deep, else `unblock` with the TL;DR as reason. Every execution lands in `labels.jsonl` as provenance `jev_auto`. The first pass (586 blocked) expired 79 dated cards and executed 51 picks; what stayed was 389 the model was unsure on, 48 guard-word cards (send, pay, delete, people) and 7 disagreements: those are Deep's, via the swipe app. Do not fold the SEND bucket from `kanban_clear.py triage` blind: its regex sweeps PR, merge and backlog decisions into the pack.

## 1e. Ruling pass: the main lane decides the pile (`~/.hermes/scripts/kanban_apply_rulings.py`)

When Deep says "clear my decision cards for me", the local Jev scorer has already taken what it was sure of (1d). What is left needs judgment, and that is the main lane's job, not a child's: a `delegate_task` fan-out runs on the cheap delegation model with an 8 minute cap and six children returned nothing on 85 cards each. Do it inline from compact one-liners instead; 500 cards fit in four reads of 127 lines.

1. Read `kanban.db` with Python `sqlite3` (shell `sqlite3 -json` corrupts bodies with control characters). Join each blocked card to its composed brief in `~/.hermes/state/celsus_cards.json` (summary, ask, options, recommended) and its Jev score. One line per card: `id prio kind age assignee [project] title || ask || A:.. / B:.. / C:.. rec=X`.
2. Rule every card with one of four verbs and a 1 to 3 line comment, no em dashes. `archive`: stale (2+ weeks, no sign of life), past-dated, APAC (Rupak's since 2026-10-19), duplicate or folded; the TASKS.md row survives so this is reversible. `complete`: evidence says done. `unblock` with a pick: scope, architecture, approach, approve defaults, and any to-do an agent can do end to end (draft, research, compile, stage). `hold`: money, sends and posts, deletes, credentials and console steps, people and pay, legal, his own meetings and calls, facts only he knows. Fold every per-day Send Pack into one send card and point the rest at it; Outlook Drafts is the real list. Social posts older than 3 days are stale. Where a free option exists, rule the free option; never rule a spend.
3. Cards with an empty block reason and `last_failure_error` like `workspace: git worktree add failed` or `Kanban owner refused` are spawn failures (section 6), not decisions: back up the DB, reset those you will unblock to `workspace_kind='scratch', workspace_path=NULL, project_id=NULL, consecutive_failures=0`, then unblock with a comment saying so.
4. Write the plan to JSON (`id, verb, comment`) and apply it with `python3 ~/.hermes/scripts/kanban_apply_rulings.py plan.json` in a background terminal (about 4 s a card through the CLI; it comments every card, then runs the verb, logs to `~/.hermes/state/clearout_apply.jsonl`, skips cards no longer blocked, and is idempotent on rerun). Probe two cards first and read the status back before the full run.
5. Deliver one decision sheet, not 128 cards: group the holds by the single action that clears the group (one M365 device login, one console sitting for tokens, security rotations, money, people, the one send card, legal, his own hands) and save it in the vault. Comment the standing rules applied so he can see what was decided for him.

Recurring: cron `kanban-ruling-pass` (weekly) runs this section on whatever is blocked; it only rules what the policy above allows and leaves the rest on the sheet. In a cron run `execute_code` is refused (no approver), so do the sqlite reads, plan build and sheet append with `python3 - <<'EOF'` in the terminal tool, and start the apply script with `nohup ... &` (about 4 s a card). Back up `kanban.db` first, write one script that emits both `plan.json` and the sheet lines from a single (id, verb, comment, group, sheet line) list so they cannot drift, and assert the plan ids equal the listed ids. Reasons truncated in the one-liner hide the options: peek at the full reason for any card you mean to unblock. The sheet for the day already exists after the first pass, so append an `Evening pass` section and mark ids already listed `(see above)`.

**Never `complete` a decision card that has children; archive it.** `complete` releases every dependency-gated child, and a stale October decision card can have a whole pipeline parked under it. On 2026-11-06 completing "approve the TASKS.md migration plan" as moot released three children, one of which wrote a card-creator script and put 313 blocked cards plus 32 triage cards on the board inside seven minutes. Before `complete`, check `select count(*) from task_links where parent_id=?`; if non-zero, `archive` with the same comment (archive releases nothing). Also pin every card-creating script to a one-shot: rename it `.disabled-<date>` after the run, because a worker that finds it will run it again.

**The compose and Jev lanes die with the shared OpenRouter cap.** A run of `celsus_compose.py` that prints `HTTP Error 403` on every card is the weekly limit, not the key: confirm with `curl -H "Authorization: Bearer $KEY" https://openrouter.ai/api/v1/auth/key` (`limit_remaining: 0`) and card the cap raise for Deep. Clef sweep is local and keeps running.

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

One card, one question: swipe triage renders buttons from a single `DECISION:` with `A:`/`B:` options, so a card carrying two questions gets no buttons at all. Create a second card instead. Only when both rulings genuinely belong to one reply, stack them as `1.` / `2.` each with its own `A/B/C`, and instruct `Reply with the numbers, e.g. "1A 2B"`, so one message still answers both. Do not bury the second question in a comment: comments are evidence, not decisions.

**Stacked questions must be stacked section 3 blocks, not prose with recommendations.** A numbered list where each item reads `1. Build order ... Recommended: yes` has no `A:`/`B:` lines, so swipe triage renders it as text with no buttons, no `Default if silent by` line and no `Reply:` line: exactly the shape this format exists to prevent, arriving from an architecture plan where the recommendation reads naturally as prose. Each stacked item gets the full shape (`DECISION` or bare `A (recommended)` / `B:` / `C:`), one default-by line for the whole card, and one `Reply with the numbers` line. Bundling is for rulings that are genuinely one reply (one plan, one reply); independent rulings get their own cards, because one card holding four unrelated questions is the backlog pattern the sweep then cannot triage.

**The multi-row variant: a change list he ticks.** When the ruling is "which of these should ship" rather than "which path", the body is a numbered table (the change, where it lands, why, cost) with a Yes / No / Later column left blank, plus one recommendation line and one sentence of grounding per row in an existing review or standard file. Point at that source file instead of restating it. It answers in one read and one pass, and it wins over seven separate cards when the rows are one theme. Tradeoff: it renders as text only (swipe triage buttons parse one `A:`/`B:` shape), so he answers in a comment, and the reply arrives as row numbers rather than a single option letter, so the block reason must say so. A row that is a real either-or, not a tick, gets split into its own section 3 card.

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

## Pitfalls
- **Staging a purchase the provider then rejects for missing human-only data.**
  Card the missing input as a `needs_input` decision in the section 3 shape,
  naming the exact fields the provider demands, and carry everything already
  verified onto the same card (the candidate list, the pricing, the order
  parameters). Reporting the rejection in prose strands the same order on the
  next attempt, and the order parameters die with the run.
- TASKS.md line must be flipped in the same turn as the merge or deploy: leave it at "PR only, no merge" and the next session reads stale state as current.
- **Read the cap logic in the shipped source, not the config schema.** `resolve_max_in_progress` / `configured_max_in_progress` in `hermes_cli/kanban_db_dispatch.py` is the authority on what unset means on this machine.
- **The breaker counts every requeue.** A killed or crashed worker is one strike against a limit of two, so a wholesale kill of a just-unblocked batch walks every card to the edge of the dispatcher's circuit breaker.
- **Do not bury an open ruling in a delivered document.** When a plan or note ends in a list of decisions, card them: one card per independent ruling, section 3 shape, created blocked. A card holding several questions never renders option buttons (swipe triage parses one DECISION with A:/B:), so he has to type an answer instead of tapping one, and prose decisions with no card sit unanswered until he happens to reread the doc. The document stays the record; the card is the surface. When the ask is a whole pile of threads rather than one plan, the `settlement-pack` skill owns that shape (pack note plus cards plus TASKS.md back-fill). The same applies to a
ruling raised in chat: write the card comment in the section 3 shape first, then
ask, because a chat question can time out unanswered and leaves nothing on the
board, while the comment survives the turn and is what the next session reads.
- **A decomposed block loop can invert a spend gate; check direction after every decomposition.** A needs_input card that blocks twice gets decomposed, and the decomposer has been observed parenting the decision card under its own provisioning children, so buying the thing releases the card that provisions it instead of the other way round. Re-read parent/child edges whenever a decomposition event appears in a card's history: unlink the edges, then re-link so the decision card is the parent of every card that executes the spend (`hermes kanban link <decision> <provision>`). The repair looks impossible at first because the reverse edge is still in place and `link` refuses a cycle with `would create a cycle`; that refusal is the tell that the gate is backwards, so finish unlinking the old direction before retrying. Never fix it by deleting the decision card, which is the record of the approval.
- **Vendor numbers in a spend decision card get a flag list, not a restatement.** A price quoted from a secondary source is an unconfirmed number, so re-check it on the vendor's own page and list every claim the fetch could not confirm as a flag (promo term hidden behind a checkout selector, location name missing from the SKU list, benchmark grades measured in another region). Carry the flags into the source design note or spec as well as the card, because the doc is what the next session reads and the card dies with its run. Convert each flag into an explicit stop condition at checkout ("stop if the location list has no India or the 12 month price is not X") so the approval survives being executed by someone else.
- **A conversion proposal for blocked cards reads the live board and audits its own hold buckets.** A dry-run list built from a backup snapshot is stale within hours (one pass found 212 of 306 cards already archived or done by the time Deep would read it), so carry a `live status` column read from `kanban.db` (`mode=ro`) at write time and mark resolved rows as no action. Keyword buckets mislabel both ways: a `Send` verb is not a client send, and a todo row can hide a hard hold (an HR complaint, a KRA sign-off, a `$99` subscription). Before handoff, sweep the todo bucket with spend (`\$|USD|billing|seat|invoice|charge|paywall|subscription`), HR (`complaint|KRA|timesheet|attendance|confidential|resign|candidate|interview`) and external-send regexes and move every hit to keep blocked, and make the `why` name the trigger that matched. Rows whose last block event is `gave_up` are dispatcher circuit-breaker parks (spawn failure or crash; parks before 7 Nov 2026 have no `block_kind`, newer ones carry `capability` for a `workspace:` error or `transient`), not parked to-dos: label them as such and route them through section 6.
- **Verify with counts, not intent.** Re-run the status GROUP BY and the worker process count (`pgrep -f 'hermes_cli.main -p .* --cli' | wc -l`) after each step; a repair that changed the DB but not the running processes is not done.
