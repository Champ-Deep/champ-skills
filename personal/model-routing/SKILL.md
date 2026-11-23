---
name: model-routing
description: Use when routing work across subscription and API lanes.
version: 1.0.0
author: Champ
platforms: [macos, linux]
metadata:
  hermes:
    tags: [routing, delegation, kanban, cost]
---

# Model routing

## Current override: use hosted Jev, not Clef

Deep directs Jev for routing and decision scoring. Do not invoke Clef or fall back to it, even where older sections below still name it. Use the existing typed client `request(payload)` in `/Users/deep/.hermes/scripts/celsus_jev.py`: TypeSafe direct when configured, otherwise OpenRouter Decisions API with `typesafe/jev-1.14`. It uses the normal Hermes credential loader; never inspect or print credential values. Check OpenRouter remaining budget before a paid probe. Validate answers with the client's `parse_answer` and report the returned model. Missing configuration, quota or malformed output is an explicit blocker, not permission to silently use Clef. The separate `jev_route` plugin only classifies model tiers and can return `no config`; that does not mean the hosted decision client is unavailable. Keep irreversible and people/data/legal/payment judgments with the main lane and Deep's approval gates. A model confidence is not authorization.

You are the main agent and you run on Claude (Anthropic subscription). You own ideation, architecture, backend design and code, workflow and process design, and all review. You do not hand those off.

Six other lanes exist (table of record: `_config/bots.md`, rebuilt 2026-11-05). Use them.

| Lane | Model | Tool scope |
|---|---|---|
| `planner` | Opus 5.5, Anthropic | read, web, kanban, context7, 21st; no cron, delegation, memory |
| `reviewer` | Opus 5.5, Anthropic | full code tools + skill_manage; no cron, delegation, memory |
| `frontend` | gpt-6.2-astra, always the frontier GPT (Deep, 2026-11-21); ChatGPT window, waits at the reserve, never downgraded | code tools, 21st, context7, awwwards, dembrandt, clerk |
| `content` | gpt-6.2-sol (latest Sol), ChatGPT window | file, web, wispr, notion only; no email MCP |
| `worker` | gpt-6.2-sol (latest Sol, permanent since 2026-11-21; Astra `gpt-6.2-astra` pinned per heavier card only), ChatGPT subscription first; bounded OpenRouter Auto fallback | terminal, file, kanban, web; no browser, cron, delegation, memory |
| `inbox` | deepseek/deepseek-v4.1-flash, OpenRouter | terminal, file, kanban + the only Outlook mail MCP (draft-only allowlist) |

Every implementing lane ends with `kanban_request_review(reviewer="reviewer")`. The reviewer, not the main lane, completes the card and patches the skill that caused a miss. `kanban.default_assignee` is `worker`, so a card you forget to assign lands on the cheap lane, not on Claude.

The default profile has calendar read only on ms365 since 2026-11-05: an Outlook draft is always an `inbox` card (recipient, subject, points, source note). Crons `daily-email-triage` and `draft-dispatch` run on the inbox profile; `meeting-action-watcher`, `team-nudge` and `zoom-meeting-followup-sweep` stay on default and card their drafts to inbox.

**Per-turn Jev routing cannot cross providers.** The `hermes-jev-routing` plugin rewrites the model on the provider already bound to the turn (its LIMITATIONS.md, item 2), and it needs `TYPESAFE_API_KEY`, which is not set. Routing across subscriptions is a card property (assignee + `model`/`provider` pin), decided at intake with local Clef (`kanban-task-intake`). An OpenRouter auto-router would only ever see OpenRouter models.

## Lane 1: frontend profile (GPT-6.1 Sol on the ChatGPT subscription)

Use for: building or changing UI, pages, components, styling, frontend features, and for executing a written spec or task list step by step.

**Check the clock before you queue.** A card only lands after the dispatcher tick plus a worker run, so when a deliverable is due within the hour (a call starting soon, a share needed now), build it in the main lane and run the chain yourself: the design skill, the brand skill, 21st.dev sourcing, `visual-verify`. Under a fuse the shortcut that gets taken is skipping the skills, not skipping the lane, and that is the worse failure: a hand-written page with no kit, no brand and no component sourcing is rejected on sight and rebuilt anyway. Decide in one line (route or build here), then build by the skill either way. Queue the card for anything with real lead time.

**"Real lead time" means you can state an ETA you earned before the scheduled use, not merely hours on the clock.** The clock check above is not passed by a lead time of hours when the deliverable is a page for a meeting happening today: the card still has to survive the dispatcher tick, an unknown worker run and a QA pass, so the honest read is that you cannot confirm it lands first. Carding it anyway, then naming an ETA you have not measured, forces the same hand-built fallback later while the card races the file, and the fallback arrives with no skills. For a same-day meeting, either prove the lane will beat the meeting (a running card with files already on disk, checked) or treat the window as measured in minutes and build here now, and say in the reply which of the two you judged so the shortcut reads as a call rather than a routing slip.

How: create a kanban card pinned to the frontend profile. Write the card body as a complete brief: goal, files or repo path, acceptance criteria, what not to touch, and how to prove it works (screenshot, test command, URL). Assemble it from `references/frontend-brief-template.md`: reuse inventory, deliverable format, design tokens with reference-mapping, section-by-section spec, data-honesty rules, named QA gates, handover contract. The lane executes exactly what is written, so every design decision belongs in the card.

```
kanban_create(
  title="Build the pricing page",
  assignee="frontend",
  body="<full brief>",
  skills=["frontend-design"]       # optional, any installed skill names
)
```

**Frontend always runs the frontier GPT (Deep, 2026-11-21).** The frontend profile default is `gpt-6.2-astra` with no fallback chain, the governor never pins a frontend card to Claude or Gemini (it clears any older pin it made), and at the ChatGPT reserve a frontend card waits instead of downgrading. When OpenAI ships a newer frontier GPT, move the frontend default to it the same day: "always the latest GPT" is Deep's standing rule for every GPT lane (Sol for worker and content, the frontier model for frontend). Do not pin a frontend card to any other model.

**Subscription-first routing with priority tiers (worker).** Worker cards run `gpt-6.2-sol` on `openai-codex` below priority 75, falling to Antigravity Gemini (Deep's Google plan, `antigravity-subscription-directsdk`) before any paid call; priority 75 to 89 pins Gemini 4 Hydrogen High on the Antigravity plan (Claude Sonnet at the Gemini reserve) and 90+ pins Opus, served from whichever of Anthropic direct or Antigravity Claude has more headroom. Failed builds are never auto-escalated. To move a card up its lane's queue without changing which model serves it, bump priority only inside its own tier (at most 74 under the codex tier): the guard seats by priority within the admitted profile, so a bump across a tier boundary silently swaps the model and spends the Anthropic window on work the cheaper tier was picked to absorb. Keep Anthropic for main judgment, planning and review. Explicit specialist pins remain deliberate per-card decisions. The bounded fallback is `openrouter-budget` with `openrouter/auto`, never unrestricted Auto or an uncapped provider. Follow `references/subscription-first-routing.md` for quota admission, limits, proof and known gaps. Never reclaim a running worker just to apply this policy: it keeps its current model until it finishes.

Astra burns the ChatGPT window about 4x faster than Sol, so frontend volume is the lever when the window runs short: queue fewer frontend cards rather than pinning a cheaper model.

**Deep reviews visual outputs, not only decisions (`_config/bots.md` rule 10).** Every frontend brief for a new page, new direction or redesign states the first-render CHECKPOINT block (preview URL, 390 and 1440 screenshots, the 1 to 3 things to look at), and every visual card ends in the reviewer's OUTPUT REVIEW block instead of a silent completion. Deep judges design by seeing it: a brief, plan or prose summary of a design is not something he can review, so never ask him to approve a design direction from text when a render can be produced first.

When the card comes back for review it goes to the `reviewer` profile (Opus), not to you; step in only when the reviewer returns a `needs_input` to Deep or the card touches auth, billing or legal. Request changes with `kanban_request_changes` and a precise list, or complete it.

**A rejected first round comes back into the main lane, not into a second card.** When Deep looks at a batch of lane-built UI and says the output is bad and to ideate and build it yourself, that is a verdict on the lane's judgment, which is the part a card cannot re-supply. Take the work over: keep the existing repos, folders and worker addresses as the substrate, write the direction yourself, build it yourself, verify it yourself. Archiving the cards and re-specifying the same brief sends the same judgment call back to the lane that just failed it. A minor fix request still goes back as `kanban_request_changes`; the pull-back is for a rejection of the work as a whole.

**A round that works but is not good enough goes back to the lane as a second round, not to a rebuild.** Take over only on a rejection of the work as a whole (below). For a functioning page he finds plain or ugly, keep the lane: copy the round's output to a fresh scratch dir, write the next prompt as the deltas (what he called weak, plus the design gates the first brief underweighted: named design skill, brand skill, 21st.dev component table, scroll beats over assembly heroes), and run one bounded one-shot per round with the prompt file rather than a chat. Verify each round with `vision_analyze` at two widths plus DOM probes (dash count, console errors, controls driven) before it becomes the file he opens, and hand the verified file to the lane's own final round rather than patching the deliverable yourself unless he asks. Two rounds that do not raise the quality, or a verdict on the lane's judgment, pull the work into the main lane.

### Engine-first split for MVP tools

When Deep asks to "build this as an MVP tool", the split is logic in the main lane, chrome in the frontend lane, in that order. His default framing is plural: "build these out as MVP tools, specially the one I asked" means ship the flagship end to end first, then route the adjacent tools as follow-up cards on the same engine, each card reusing the tested functions instead of reimplementing them.

1. Main lane builds the engine before any card exists: data model as one JSON file, logic as a framework-free ES module (pure functions, no imports beyond the data file), tests as `node --test <dir>/` (node:test, zero deps). Commit it on `main` first so the card has a fixed target.
2. Then create the frontend card that imports the engine directly. The card body names the engine path, every exported function with its signature and one worked example call with its real expected output, plus a "do not touch" list covering the engine files. The lane consumes the engine, it does not reimplement the logic.
3. Make at least one acceptance criterion traceable to an engine output with the exact expected value (a count, a ranked first item). A lane that must match a hard number cannot fake the wiring, and you can verify it by running the engine yourself at review.
4. Prove the engine before routing: run the test suite and one sample call from the terminal, and paste the real output into the card brief as the worked example.

## Pitfalls
- **A PDF or other file over about 100 KB cannot be attached to a card with `kanban_attach`** (inline base64 would cost the whole context), and `hermes kanban attach` is refused from a worker context ("cannot mutate Kanban tasks via the CLI"). Pass the absolute path in `kanban_request_review(artifacts=[...])` or `kanban_complete(artifacts=[...])`: the kernel copies it into the task's attachments. Read the list back with `kanban_attachments` afterwards.
- **An assertion failure in a multi-step edit script leaves the earlier steps applied and the file inconsistent.** When one `execute_code` or shell block does several `str.replace` writes and then asserts, the write happens first and the assertion second, so a failure midway reports an error while the file already holds half the changes. Make each write its own check: assert per step, or re-read the touched files after any failure before deciding what to redo. Blindly re-running the whole block patches text that is already patched and silently skips the step that broke.
- The same applies to fuzzy multi-target patches and multi-step `str.replace` scripts (`patch`, `skill_manage` batch, `execute_code` rewrites): a target that lands in the wrong place still counts as applied, and the batch aborts on the first miss. Assert or re-read per step rather than per batch, so one failure does not leave half a file rewritten while you assume the whole block ran.
- Pass `workspace_kind="scratch"` on every `kanban_create` for a card about another repo, or use CLI `--workspace scratch`. A session opened in the Celsus project auto-scopes new cards to project `celsus` with a worktree workspace. The Celsus git repo has no commits, so the dispatcher's `git worktree add` fails with `invalid reference: HEAD`, and the circuit breaker blocks the card after 2 spawns. The worker makes its own worktree of the target repo from the brief. Workspace kind cannot be edited on an existing card: recreate it with `hermes kanban create --workspace scratch --body-file`, re-link parents and children, then archive the old card with a pointer.
- Fan-out only what is independent: four research lanes on one deliverable run in one batch; heavy design and code work goes down the lane table in `_config/bots.md`, not into subagents that cannot ask questions.
- **Two open cards that edit the same repo need an explicit handoff between them.** Point both at the same `workspace_path` is fine (each card gets its own worktree), but two workers running at once on sibling branches of one repo race on pushes, on generated files and on shared build output, so give each card a distinct branch prefix in its brief, gate the later card with `parents` on the earlier one, and state in each brief the fallback base to cut from if the sibling's branch does not exist yet, so the lane never picks an arbitrary default. A brief whose named base is produced by a card that has not run yet must carry that fallback in the same sentence.
- Pitfall: `node --test <dir>` fails with MODULE_NOT_FOUND on the runtime that
  does not resolve a bare directory (node 24), while node 26 does. Name the test
  FILE in the card (`node --test engine/engine.test.mjs`) so the lane's command
  and yours agree, and source nvm before running it: the terminal tool's default
  node is not the pinned one.
- JSON import attributes (`import x from "./data.json" with { type: "json" }`) run fine in Node 26 but trip some bundler configs. Either keep the engine's data import bundler-safe (plain path, let the bundler handle JSON) or state the fallback explicitly in the brief ("import data.json directly if the attribute syntax trips the bundler"), so the lane does not stall on it.
- Provisional or shaped numbers must ship with a visible "sample data" badge requirement in the acceptance criteria, every tab. An internal tool whose placeholder counts look quotable to a client is a data-honesty failure, not a polish item.
- Deferred scope goes in the card as an explicit "deferred from this MVP" list in your completion report, not silently dropped: Deep reads it as the roadmap.
- **A `parents` chain inside one lane also waits for the reviewer between cards.** A child promotes only when its parent is done, and done means reviewed, so three sequenced frontend cards run one per reviewer pass. Read `~/.hermes/state/kanban_quota.json` before building the chain: when the reviewer's provider is over its reserve or its usage query fails, the lane is closed until the window resets and a night of open frontend capacity is spent waiting. For a dated deliverable in that state, sequence same-lane cards by priority instead (one per profile already serialises them), tell each card in a comment to proceed only when its predecessor is in review or done, and keep `parents` on the release gate so nothing ships unreviewed.
- **Never write a card id into a brief before the create call returns it.** Fill the roster after the ids exist and grep the brief and every card body for ids that are not on the board; a placeholder that looks like `t_xxxxxxxx` reads as a real card to the next lane.
- **Never set `parents` on a card that is blocked.** A child promotes only when every parent reaches done, so a parent parked in `blocked` strands the child off the dispatch queue with no error to show for it, and it reads as ready while nothing ever spawns. Relate new work to a blocked card with a comment on that card (what it is missing, what now runs in parallel), and reserve `parents` for cards you expect to reach done.
- **A created card is not a running card.** `kanban_create` returns `ready`; prove the claim with `kanban_show` (`claimed` and `spawned` events plus the worker pid) before telling Deep a lane is on it. If the status is still `ready` after the dispatcher's tick, check `~/.hermes/state/gateway.heartbeat` before reaching for a one-shot fallback: a stale heartbeat means nothing is promoting cards, and waiting does not start it.
- **Claim the card before running it as a one-shot while the dispatcher is live.** Spawning `hermes -p <profile> chat --oneshot` on a card the dispatcher can still see makes two writers on one artifact: the next tick dispatches its own worker onto the same draft or file, both edit in place, and nothing merges them back. Run `hermes kanban claim <id> --ttl <seconds>` first, confirm the status reads `running`, comment the claim plus the transcript path on the card, and only then start the one-shot; the claimed status is what the dispatcher's tick finds instead of a `ready` card to spawn.
- **Verify a lane's tool scope from the record before writing it into a card body.** A card body outlives the turn, so a capability claim taken from the one-line lane table (what a lane can read, and therefore how its output gets verified) persists as a false handoff; read `_config/bots.md` or the lane's own config and allowlist first. Where you cannot establish a lane's access, keep the standing reviewer step instead of carving an exception for it inside the card.

### Backend contract first for API-consuming cards

The engine-first split also governs any frontend card that will call a backend API, not just MVP engines. The main lane lands the endpoints, the storage and the PR base branch, and pushes them, before the card is created; the card then carries the verbatim contract.

1. Build the surface yourself: route handlers, the column/field registry, the persistence migration. Prove it with pure-function tests plus a compile check when the full app cannot boot locally (see `verification-gate-integrity` on naming the layer you did not exercise).
2. Push your branch AND push the branch the lane's PR must target. A base that exists only locally means the lane branches from whatever default it finds.
3. In the card body, paste the contract literally: every path with method, query params and response shape, the status code and `detail` for bad input, the exact headers, the branch to cut from, and the PR target. Include one worked request/response so the lane can assert on it.
4. Unblock the blocked card with the contract as a comment, not as prose in chat: workers see the card, never the conversation.

A brief that asks the lane to "establish the backend contract and publish the base" hands it architecture work, and it will block with exactly that question. When a frontend card blocks that way, the brief is the defect: absorb the backend work into the main lane, push it, comment the contract and target branch on the card, unblock. Do not re-card it or argue scope with the lane.

**When the contract changes after the card is already running, the edit does not
reach it.** Workers read the card body at spawn and comments only at startup, so
rewriting the body while the lane runs leaves the old contract in force. Run the
same sequence as the model switch above: `hermes kanban edit <id> --body ...`,
`hermes kanban reclaim <id> --reason "brief changed"`, comment a resume note
naming what changed, what to run first (usually `git merge main`, since the old
branch was cut before the new contract landed) and that uncommitted work in the
checkout survives the termination, then `hermes kanban dispatch` and confirm the
spawned process. Leaving the lane on a superseded contract costs a whole worker
round.

Pitfall: a pushed base that only tracks the files you touched is not a base. When a repo has long-lived untracked work (manifest, lockfile, build config, tests), the lane blocks on ownership instead of building. Before carding, prove the base on a clean worktree of the remote ref (`git worktree add <scratch> origin/<base>`, then the install, test and build commands the brief names) and commit the missing foundation yourself first.

Pitfall: verify the PR base exists on the remote before naming it in a brief (`git ls-remote --heads origin <base>`), and merge that base into your branch if you cut from an older point, so the lane's PR diff shows only the new work. Run `git log -1` and `git status --short` on that checkout first: a tree with **zero commits** has no base branch and no remote for the lane to target, so name the initial branch yourself and state in the brief whether the lane may commit at all. Deep approves commits case by case, so without that approval the brief says "leave changes uncommitted in the working tree and report the changed file list", otherwise the lane commits work he never reviewed.

Standing gates on every frontend deliverable for Deep, in the brief itself:

- **Human-readable HTML briefs, meeting pages, summaries and readouts require `research-to-visual` plus `executive-one-pager` before design.** State that chain in every frontend card, even for Markdown-to-HTML conversions. Add the appropriate report/showcase skill for longer formats. The brief must name the visual structure for each section, the first-screen answer/ask, the disclosure layer for full detail, and a relevant prior branded reference to inspect. Source real 21st.dev components for the information interaction; a contents rail alone is not visual storytelling. Brand and visual-verify remain mandatory. Application screens still use their appropriate UI skills rather than forcing a document template.

- Load `frontend-design`, the relevant brand skill, and `visual-verify` before any HTML/UI work; render it, open the screenshots, test the controls before handing it over.
- **Visual-first for every tool UI.** Deep's standing preference: represent state visually (glyphs, chips, meters, progress, spatial layout) as far as it can go instead of prose. State the visual contract, what each element encodes, in the brief's acceptance criteria so the lane can be graded on it, not just on layout.
- **The main lane picks the 21st.dev components before the card exists (Deep's standing rule, 2026-11-02).** Run `mcp__twentyfirst__search` (free metadata, one call per `tool_call`, 6 to 8 queries per UI: shell, status, inputs, controls, tables, upload, counters, feed, toasts), open 3 or 4 preview images with `vision_analyze` to confirm fit (a Gantt-style row layout beats a room-booking widget for a clock-time axis; the preview is what settles it), then write a component table into the brief: region, component name + author + id, role, visual contract. Commit the brief into the target repo (`docs/ui-brief-vN.md`) and point the card body at it, so the lane has a fixed file to follow. "Use 21st.dev where it fits" without ids hands the design decision to the lane, which is the part a card cannot supply. Worked example: `/Users/deep/repos/champ-softphone/docs/ui-brief-v1.md`.
- **When Deep picks the components himself, hand him a picker widget, not a table in prose.** Render one `::preview` HTML widget whose rows are the page regions and whose options are your shortlisted components, each option label carrying the 21st.dev id and each carrying `data-hermes-send="region N = <component name> <id>"`, so one tap sends a pick as a prompt. He may answer one region at a time or all regions in one compact numbered message; both count as the pick. After every answer, patch the widget to mark the chosen option (a pick he cannot see marked gets re-sent), then write the component table into the brief and commit it as above. Copy and modify `templates/component-picker.html` in this skill instead of writing the widget from scratch.
- **When the component is a source Deep pasted rather than a 21st.dev id** (the same component rolled across several repos or stacks): save the paste verbatim into the effort folder, hold the shared edit list and the targets table in one `ui-brief-vN.md` there, gather each repo's stack, data contract and branch base before writing any card, and pre-create one worktree per repo. Procedure: `references/multi-repo-component-rollout.md`.
- Use 21st.dev components for all front-end work (install via the shadcn CLI on nvm node v24 with `TWENTY_FIRST_API_KEY`). Run the `ui-library-picker` skill before the search: foundation and specialist behaviours (toasts, drawers, command menus, changing numbers, long lists) come from its registry, 21st.dev supplies the structural regions, and the brief's component table names both. The exception is a host that is not React (Svelte, plain HTML): there the picks are layout references only, the brief says so explicitly and bans installing that stack, and the lane rebuilds the layout with the host's own components while still naming the references used. When the live host cannot run a build (Plesk/static only), the constraint still holds in spirit: the lane vendors the chosen 21st.dev components as static HTML/CSS (or a build that emits static files) and names the components used in the handover, instead of dropping the gate.
- Fit at phone, tablet and laptop widths is checked by the `responsive-viewport-qa` skill; name it in the brief's acceptance criteria.
- **Preview hosting is a data-classification call.** A page carrying personal data (employee names with home locations, shift or travel times) previews on a local static server only, and the brief states that as an acceptance criterion, overriding any deploy-preview helper. The lane reports a local port and path; a public URL for that page is a review failure, not a convenience.
- The lane never overwrites the live artifact: when a repo's build output is what a served site runs from (check the bundler outDir against the server's static root first), the brief forbids building into it, routes QA through the dev server on its own port, and names swapping the served bundle as a deferred, Deep-approved step in the handover.
- For anything that leaves the company (a client or vendor sees it), the brief's acceptance criteria name the forbidden strings explicitly: the placeholder token for missing proof, the client and vendor names that may not appear without written clearance, and the internal citation words (source names, employee names, vault paths, task ids). A worker can only fail a rule the brief states, and its self-reported checks cover nothing else, so a vague "no internal references" acceptance line ships internal references.
Review the output with the `sdlc-review` skill's leak-gate reference (`sdlc-review` → `references/client-facing-leak-gates.md`), which sweeps every shipped format (HTML text, PDF text layer, PPTX slide XML, rendered pages) rather than trusting the source file.
- **Check lane admission before you card, and say which state you found.** Read `allowed_profiles` in `~/.hermes/state/kanban_quota.json` at the moment you create a lane card. An empty list means every lane is closed, so the card sits unspawned however well written it is: card it anyway (it is queued work), but say plainly in the reply that nothing has started and offer the main lane as the fallback that starts now. Reporting a card as started, in progress or "the lane has it" while admission is empty is a false handoff Deep cannot see from chat, and it delays the only route that works immediately.
- Before the first 21st.dev card of a session, prove the lane can reach it: `profiles/frontend/.env` must carry `TWENTY_FIRST_API_KEY` with no space after `=` (bash sources it too, and a space turns the value into a command), and `profiles/frontend/config.yaml` needs the `twentyfirst` MCP block from the root config. Verify with a `tools/list` POST to https://21st.dev/api/mcp under that env (200), never by printing the key. A 21st.dev "catalog search failed" with a 200 on `get_usage` is their outage, not auth: tell the lane to scaffold and retry, not to block on capability.
- When browser tools are down for the main lane, open the lane's QA screenshots
  yourself with `vision_analyze` at review instead of trusting its self-report,
  and open a second image at a small breakpoint (phone width) as a cross-check:
  one vision pass on the desktop shot is not evidence the phone layout holds.
  When the vision path itself cannot run (auth or quota), do not spend the round
  retrying it: fall back to DOM probes in a real browser (geometry, overflow,
  contrast, keyboard toggles, print behavior), leave your probe output as a
  sibling file beside the lane's `qa/` artifacts, and write "screenshot
  inspection unverified" into the card comment and the review handoff so the
  gap travels with the card instead of dying in your session.
- The frontend worker's vision aux runs on the shared OpenRouter key; when that key is capped the worker goes blind and blocks. Write composition briefs as numeric Playwright/Pillow asserts (positions, sizes, angles, counts, computed colours, alpha-fringe checks) rather than "open it with vision", and the main lane (Anthropic vision) opens the side-by-sides at review. A brief that only says "match the mock" gets a recolour of whatever already exists; list the per-section deltas and the hard rejects.

If the kanban dispatcher is not running (gateway down), fall back to a one-shot from the terminal:

```
hermes -p frontend chat -q "<full brief>"
```

**Point the card's workspace at the checkout it must edit.** A card created without
`workspace_kind` gets a fresh scratch directory, so the lane starts from none of your
uncommitted or unpushed work and from a different tree than the one you just tested.
When the card edits a repo that exists locally, pass `workspace_kind="dir"` with
`workspace_path` set to its absolute path, and name the branch to cut and the target
branch for the PR in the brief: a lane left to pick either one will branch from
whatever default it finds and may open a PR over work you have not reviewed.

### Monitoring and restarting a lane

- Judge a lane by output, not status: check for new commits, changed files and verification results on disk at intervals. A `running` status plus recent tool calls with no on-disk change for ~15 minutes means stalled, not alive. Never report a lane as progressing on liveness signals alone.
- A stalled UI lane restarts as a fresh frontend kanban card, not another `delegate_task`: the card body states the resume point (existing branch, worktree path, what is already done, what is missing), caps orientation (max 2 read batches before the first edit), sets `max_runtime_seconds`, and requires real verification output before it can be marked done. Restarting a stalled worker into the same open-ended brief stalls it again; the cheap lane loops on reading for reasoning-heavy multi-file UI work, which is why that work never belongs in `delegate_task` in the first place.
- Chain dependent lanes with `parents` on the cards instead of dispatching them together: one agent per profile at a time, and the child releases automatically when the parent completes.
- **A lane that timed out or died produced nothing to judge.** The one-shot fallback (`hermes -p <profile> chat -q`) can die mid-run with no artifact on disk; take the work over in the main lane, run the `visual-verify` gate yourself, and send the card to the reviewer with the limits named and the handoff stating that the independent review is pending. A dead lane is not evidence the build happened, and a card completed on the lane's own claim is the same failure as a green status with no output on disk.

**A request that spans lanes is one chain of `parents`, not a batch.** A campaign that has to be written, simulated and staged runs in that order, and the cards are the only place the sequence lives, since lanes never see the conversation. Build it this way:

1. Write the shared artifact path into every brief (`~/Celsus/Efforts/Active/<effort>/name.json` or `.md`). The output file is the handoff between cards; a chain that passes content through prose in card bodies loses it the moment a lane paraphrases. The final card also updates the artifact in place (`"winner"`, `"final"`), so the file ends as the record and TASKS.md points at the chain, not at four ids.
2. Put the step that needs judgment (picking the winner, signing off the copy) on the main lane as a `default` card even when the neighbors are `content` and `worker`: judgment is never delegated, and a mid-chain main-lane card is how you keep it.
3. `parents=[<previous card>]` on each downstream card, and say in each brief exactly which upstream field it consumes. The gate releases on parent completion; state it, do not assume the lane will infer it.
4. **Never let a downstream card depend on a value that does not exist yet without naming the placeholder.** A signup URL that arrives with a later app build has to be a literal `{{signup_url}}` in the copy plus one sentence saying what fills it and that the substitution is checked before anything sends. An unresolvable placeholder discovered at send time is a failed campaign, discovered at review it is a one-line fix.
5. **Staging is never sending.** Briefs that queue work in a sending system say "queue but do not process/send", name the exact button or endpoint that releases it, and hand Deep the preview plus recipient count. Then he presses it; nobody releases an external send on his behalf. An internal seed list is its own step, gated behind the same approval, never merged into the first send to save a card.
6. Close the chain with a `needs_input` decision card carrying his options and your recommendation first: a staged draft is not done while he still has to act on it.
7. Every implementing card still ends in `kanban_request_review(reviewer="reviewer")`, even mid-chain. The reviewer grades the handover (run link, counts, verification output), not the status.
- A card that blocks twice for the same reason trips block-loop detection and the auto-decomposer fans it into parallel child cards on the same `dir` workspace: several workers editing one checkout and one `globals.css`. When a UI card blocks on the capped vision aux, do the screenshot review yourself on the first block (`vision_analyze` on `qa/screenshots/*`, crop regions under 8000px) and answer with a numbered change list, so it never blocks a second time. If the fan-out already happened: `hermes kanban reclaim <id>` (terminates the worker), `hermes kanban archive <ids>`, `hermes kanban unlink <parent> <child>`, then hold the original card with a `transient` block while you review.

## Lane 2: cheap workers

Use for: anything small and well scoped that does not need judgment. File edits, renames, data munging, log reading, scripted checks, drafting from a clear outline, bulk repetitive changes. Which model fills this lane is config, not prose: read `delegation:` before naming it, and never quote a model name carried over from an older config.

How: `delegate_task`. It already routes to the cheap worker; you do not pick a model. Give each task a tight goal plus context, and an `output_schema` when you need structured results back. Batch independent tasks in one call.

**Never claim a subagent's model before reading the config.** `delegate_task` children inherit the `delegation:` block of the root config (provider and model), not the model your chat runs on, and not the model this skill last recorded: which model fills this lane is config, and it changes. Read that block (`grep -A6 '^delegation:' ~/.hermes/config.yaml`) before saying anything about which model or which subscription a fan-out will burn: the children name themselves in the summary, so a wrong guess survives until Deep catches it. Five parallel children on a cheap model are also five times the fan-out, not a way to spend one window down.

**If a run needs a specific model, pin it explicitly or use a card, then verify what actually ran.** A per-call pin can be silently overridden by that config-level `delegation:` block, and a fan-out that lands on the wrong model is a wrong result, not a billing footnote: it invalidates any comparison the run was meant to establish. Two safe patterns: pin provider and model explicitly on each `delegate_task` entry and on each `kanban_create` (`provider=`, `model=`), or route expensive work as cards instead of `delegate_task`. Either way, confirm from the child's own output which model ran before reporting the run as comparable.

When Deep's instruction is to burn down a specific quota "right now" (his Claude or ChatGPT plan before it resets), the move is to pick up board work **inside the current chat**, not to fan out: delegation is the opposite direction. Card work that is genuinely this lane's job (code review, security fixes, judgment calls) he does here; judgment and writing work he cannot inline goes to cards pinned to the quota model, never to `delegate_task`.

**Check the quota guard first: near a reset the reserve is what freezes the lanes he wants used.** `kanban_quota_guard.py` stops admitting `default`, `planner` and `reviewer` once Anthropic has 25 percent or less left, so "use my Anthropic before it resets" arrives with those lanes already frozen and 200+ ready cards behind them (`allowed_profiles` in `~/.hermes/state/kanban_quota.json` shows only the other lanes). The lever is the burn window, not a config edit: write `~/.hermes/state/quota_burn.json` as `{"provider": "anthropic", "floor": 7, "slots": 3, "until": <epoch of the window's resets_at>}`. Until `until` the guard admits that provider's lanes down to `floor` percent left and seats them first; after it the file is ignored and the normal reserves return by themselves, so nothing needs reverting. Set `floor` two points above what he asked to keep, because workers already in flight finish past it. Run `kanban_quota_cron.sh` once and read `allowed_profiles` back, then confirm a spawned pid on the lane. The 3 total and 1 per profile caps stay: they are the machine brake, and changing them needs a gateway restart that kills running workers.

For read-only evidence gathering that pairs with your own authenticated work, fan the public half to a leaf: hand it the exact URL/command list and constraints (no login, no writes, credential findings as booleans only, never print key material), while the main lane runs the control-plane CLIs (`wrangler`, `railway`, `gh`) in parallel. The leaf report lands as an async message; act on it when it arrives instead of blocking on it.

For bigger grunt jobs that should survive your session, use `kanban_create(assignee="worker", ...)` instead.

## Lane 3: inbox profile (Deep's email)

Use for anything about reading, triaging or drafting replies to Deep's mail. The routing table of record is `/Users/deep/Celsus/_config/bots.md`; read it when deciding any lane, and route instead of working inline.

The inbox bot is a fixed Python workflow (`~/.hermes/profiles/inbox/inbox-bot/inbox_bot.py`), not a free agent. Scheduled by cron `c374cac998a2`. Its subcommands cover the triage workflow only (`run`, `calibrate`, `undo`, `selftest`, `preflight`, `status`), so an ad hoc ask that is not triage goes as a card with `assignee="inbox"` whose brief states the reads and the draft directly against the ms365 tools, never as "run one subcommand and report"; running the script from the terminal with the Hermes venv python and `env -u PYTHONPATH -u PYTHONHOME` is for the triage workflow itself. Read `TOOLS_ALLOWED` in the script before writing any brief: it is that lane's real tool scope, including the read tools (`list-mail-folders`, `list-mail-folder-messages`, `list-mail-messages`, `get-mail-message`) alongside the draft tools, which the one-line lane table does not enumerate. It is draft-only by construction (no send tool, no `Mail.Send` scope); never widen `TOOLS_ALLOWED` in the script to add one. Playbook, VIP list and voice card are private: keep them out of the public champ-skills repo.

**"Did we ever send X?" is one mailbox card carrying the read and the draft, not a search you can answer locally.** The default profile holds calendar read only on ms365, so silence in the vault and the board is evidence about the record, not about Sent Items: say which tier the answer rests on instead of reporting record-silence as proof. Build the brief in two parts. (1) The read: name the folders (Sent Items, Drafts, Inbox) and the exact query strings, and accept only two outcomes, a hit list giving folder, date, subject, from and to for every match, or an explicit "no such mail in <folders>" printed with the queries used. A negative without its queries is not auditable, and the folder set is part of the answer: an empty Inbox says nothing about Sent Items. (2) The draft, only when that read came back empty: staging an ask which already went out sends a duplicate, and where a thread on the subject exists the draft is a reply into it rather than a new message. The lane's own verification goes in the acceptance criteria it must report back: `isDraft` true, exact subject, recipient, body present.

All OpenRouter lanes (worker, inbox, the DeepSeek crons) share one key with a weekly spend limit. Check `GET https://openrouter.ai/api/v1/auth/key` before blaming a lane for a 403: read `limit_remaining` and `usage_weekly` from `data` and report both with units before any run that will spend against it, since a run queued when the budget looked fine can land on a cap mid-flight. The cron `factory-ops-sweep` (`~/.hermes/scripts/factory_lib.py`) watches this and Telegrams on a cap.

A 403 on a shared key does not only mean "the key is capped". It can be an upstream model deprecation (a pinned id retired by its provider returns 403 for every lane at once while `limit_remaining` still reads healthy), so check the model's own status on `/api/v1/models` before treating the budget as the cause; a deprecation and a cap need different fixes.

A 401 (not 403) from a background shell or cron is a stale key: Hermes background shells carry an outdated `OPENROUTER_API_KEY` in their environment while the foreground shell carries none, so scripts that call OpenRouter must read `~/.hermes/.env` first and use the environment variable only as a fallback. The foreground/background split makes the same script look intermittently broken, which sends you debugging the endpoint instead of the key source.

**Bulk structured output: disable reasoning explicitly.** For batch JSON jobs against reasoning-capable OpenRouter models (composition, classification, extraction), send `reasoning: {"enabled": false}` alongside `response_format: json_object`. These models think by default, `effort: low` barely trims it, and the hidden thinking spends the output budget so the JSON returns truncated or empty. On a bulk card-composition job reasoning off measured roughly 4x cheaper and 2.5x faster with complete JSON. Verify completeness by parsing the payload (all required keys present), never by HTTP 200, before scaling a batch.

Standing rule, never ask again: basic mechanical work (YouTube or audio transcription, summarising a transcript, web extraction, log reading, report drafting from a clear outline, dependency or CI triage reports) runs on the cheap OpenRouter worker lane: `delegate_task`, or `kanban_create(assignee="worker")`, or the `-p worker` profile. Do it inline on Claude only when the cheap lane is down, and say so in the reply. When the key is capped (weekly limit), stage the card as `[staged]` + blocked and list it in `factory_config.json` `staged_cards_unblock_on_openrouter_recovery`; the sweep unblocks it when the cap clears, so Claude's window is never burned on grunt work.

## Background aux jobs (config lanes, not cards)

For a re-audit or a spend question, follow `references/aux-audit.md` first (attribute from per-profile state.db, then probe candidates).

**Change the lane Deep named, and only that lane.** "Replace my vision model"
is not licence to touch the other aux blocks: copy the pre-edit values of every
block you will not change before the first write, so the revert is byte-for-byte
instead of a re-derived guess, and say which blocks were restored. Sweeping the
whole set into one provider because that provider was the topic of the request
reads as ignoring the scope, even when every model in the sweep is a good one.

**Prove an aux lane uses an LLM at all before tuning its model.** Some lanes are
config-only and ignored: `hermes_cli/config_defaults.py` comments and the tool
description both record which ones dropped their aux LLM (`session_search` and
`web_extract` in current builds). If the lane never calls a model, picking a
better model for it changes nothing while looking like progress. Check the call
site, not the presence of a config block.

The kanban decomposer, triage specifier, title generation, approval and vision
jobs run on cheap OpenRouter models, not Claude.
They are structuring work rather than judgment work and they run constantly, so
they empty an Anthropic window faster than interactive chat does. The main
default is Claude Sonnet on the Anthropic subscription; Opus is reserved for the
review lane alone. Mixture of Agents is off by default and only fires when the
resolved provider is `moa`.

Prove any routing change before reporting it: `hermes -z "Reply with exactly:
ROUTE_OK" --usage-file <scratch>/route_probe.json`, then read `model`, `provider`
and `api_calls` (`1` means no fanout fired). Full procedure: the `hermes-agent`
skill, `provider-quota-routing` reference.

`ROUTE_OK` proves the switch landed, not that the lane can work: it exercises no
tools. Before pinning a lane onto a new provider or a subscription-backed
model, run one turn that forces a tool call (`hermes chat -q "List the files in
the current directory with your terminal tool, reply with the count only."
--provider <p> -m <m> -Q --max-turns 4`) and make sure the tool actually
executed. Tool-protocol compliance is the failure that differs per model on a
subscription provider, and a plain text reply hides it entirely.

### Lane routing is fixed when the card is created, never per turn

A per-turn router (the `hermes-jev-routing` plugin, TypeSafe, OpenRouter's
auto-router) rewrites the model on the provider request the turn already uses;
moving a turn across providers is outside that contract, so no middleware can
re-route a card between Anthropic, Codex and OpenRouter mid-flight. The Jev
plugin is installed but inert until a routes JSON is set (`config_path` empty),
and its own LIMITATIONS doc confines it to within-provider tiers anyway. So the
carrier of assignee + provider + model is the card: pin `model=`/`provider=` at
`kanban_create` (or at intake), then prove it with the ROUTE_OK probe plus one
forced tool call. Before counting on any routing plugin at all, read its
LIMITATIONS/config and confirm it is configured, not merely enabled.


## Cost questions ("cheaper model for X", "where is this OpenRouter spend coming from")

Full workflow in `references/model-cost-comparison.md`: spend attribution across Hermes configs and product repos, live pricing from the OpenRouter models API, cache-hit-rate break-even math, repo-side hardcoded price constants, and key-health checks.

Settle a reported provider from local records, never from a dashboard: `session_model_usage.billing_provider` and `billing_base_url` are the authority on which key carried a call, and OpenRouter's own activity listing rejects a normal key (403, management keys only), so name the evidence tier instead of implying you read their activity page. The tz, cache-count and session-overlap traps in the same reference are what make a windowed attribution query return the wrong rows.

A "why are we still using X" question is the full inventory in that reference (root config, every profile, the cron pins in `jobs.json`, the `bots.md` policy row, each profile's Auto Router allow/exclude lists, and any script that passes the model as a CLI argument), not a single grep; patch all of them or the change is incomplete, and when `bots.md` and the config disagree the config wins and the row is stale.

Standing rules: dated snapshots of one model family price differently (in/out can be inverted), so the cheapest depends on the workload's output share and cache behavior, never on headline rates or version recency. When the question is "route this work to something cheaper", price is only half the answer: measure the candidate on Deep's own task bank first (`llm-model-benchmarking`), and route by tier. A model that matches the subscription on routine work and fails the heavy tier needs a split route, not a single lane swap, and an overall mean hides exactly that failure.

**A tool the user asks to "make sure I have installed" is verified, not assumed, and the check runs against the live machine.** Run `which <bin> && <bin> --version`, a plugin or extension list, and a skills inventory, then report each item as installed with its version, not installed, or present under a different name. An install status read from memory or from an earlier turn in the same session is not evidence, and an item you cannot find must be reported as not found rather than carried over from the earlier list. Where the requested item list itself came from a source you could not read (a video with no transcript), say which items were checked and that the source's full list is unconfirmed.

## Review lane

`/review` runs on Claude Opus 5.5. Use it before merging anything that touches backend logic, data, auth, or billing.

## Do not

- Do not delegate ideation, architecture or review to GPT or the workers.
- Do not run frontend work through delegate_task; it lands on the cheap worker, not GPT.
- Do not pin Astra on routine cards.
- **Never use `moonshotai/*` (Kimi) on any lane, card or benchmark arm.** It is banned on the shared OpenRouter key, and a ban written in config blocks Auto Router only: a pinned card, a lane script that takes the model as an argument, or a manual call still runs it. Put a refusal guard at the entry point of any harness that spawns models from a script, and state a cost ceiling for the whole run before wiring a new OpenRouter arm, because an agent arm resends history each step so tens of calls per task accumulate far faster than the per-call price implies. The only hard cap is a key with a low limit, which Deep owns: report a ban as a block, never as a guarantee.
- Do not swap a lane onto a cheaper model because its price looks better: run it on Deep's own task bank first (`llm-model-benchmarking`). A model that passes routine work and fails the heavy tier needs a tier-split route, not a single lane swap, because an overall mean hides the tier that breaks.
- Do not move an aux job onto Claude to raise its quality. Fix the prompt or the
  spec instead; the Anthropic window belongs to the main lane and the review lane.
- Do not persist a change Deep scoped to "right now". Sweeps, monitors, config
  edits and standing rules stay untouched unless he asks for a permanent change;
  when he says "this is for now, not permanent", revert what you added and leave
  the existing setup byte-for-byte, then say what was reverted in one line.
- Do not spawn a second agent on the same profile at the same time.
- Do not let a lane publish a preview of a page carrying personal data (employee names with home locations, shift or travel times) to a public URL. The brief pins the preview local and names the path; a public URL for that page is a review failure, not a convenience.
