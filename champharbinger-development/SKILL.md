---
name: champharbinger-development
description: "Use when building or debugging ChampHarbinger features."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cloudflare, d1, workers, cron, email, debugging]
    related_skills: [systematic-debugging, risky-changes, verification-gate-integrity]
---

# ChampHarbinger development

## When to Use

Any card touching this repo: a ChampHarbinger bug, feature, route, cron or job
scheduler change, domain or mailbox behaviour, or a question about what state
production is actually in. Pair with `systematic-debugging` for the general
root-cause method; this file carries the repo's own facts and traps.

ChampHarbinger is Deep's cold-email sending platform: Next.js on Cloudflare Workers, D1, Hyperdrive, sending through the InboxKit and OpenMail providers, live at `champ-harbinger.deep-ae0.workers.dev`. Feature work happens on branches with PRs; Deep merges and deploys.

## Repo identity

- Canonical checkout `/Users/deep/repos/ChampHarbinger-cf`. Per-branch worktrees appear as `/Users/deep/repos/ChampHarbinger-cf-<branch>`; run `git worktree list` before creating one so concurrent lanes do not collide, and branch off `main` unless a card says otherwise.
- Never trust a folder name: `git remote -v`, `git fetch origin`, then compare `HEAD` against `origin/main` before planning against "the local codebase".
- No em dashes in any output, including commit messages, PR bodies and UI strings.

## Where production truth lives

- The dashboard is a cache viewer. Health, limits and capacity screens read snapshot tables and fail closed, so an empty table renders as an alarming failure state. Empty means "never checked", not "failing".
- Answer "is X actually true in prod" with a read-only SELECT against the live D1 for that worker, never from a screenshot or from what the code ought to do. Diff the `jobs` table by schedule name across the gap when something "stopped working", and read `mailbox_connections` before assuming a mailbox row exists.
- The provider console (InboxKit / OpenMail) is the authority for domain DNS status and inbox credentials. Any Harbinger message that names a specific check must be backed by a row that check wrote; otherwise the message is inventing evidence.
- You have no session in production. Anything that needs Deep's auth (an import button, a manual re-check) gets an endpoint he can call while logged in; do not try to fake it.

## Cron: the in-house `d1-boss` scheduler

- `src/lib/jobs/d1-boss.ts`. Not pg-boss: runs live in the D1 `jobs` table and each scheduled run carries a singleton key `cron:<minute epoch>`, which makes a duplicate enqueue for the same minute a harmless no-op.
- Schedules resolve to per-minute slots. A schedule pinned to one minute (an hourly at `:07`) is the only kind a single missed or throwing tick can silence for a whole period, while interval schedules (every 5 minutes) keep running. That makes an outage look selective: if some jobs ran and others did not, suspect the slot bookkeeping before the job's own code.
- Correct behaviour is: walk every minute since the last successful tick (bounded, one hour), enqueue each matching schedule, and advance the stored minute only after the sends succeed. Marking the slot first turns one transient D1 error into a permanently lost period.
- Expect a one-time burst of every hourly job on the first deploy that adds catch-up.

## Build loop

1. `source ~/.nvm/nvm.sh && nvm use 24`, then `pnpm` for everything (repo tooling is pnpm).
2. Type: `pnpm exec tsc -p tsconfig.json --noEmit`. Per-file tsc is deliberately skipped by config, so only the project-wide run counts as evidence.
3. Lint: `pnpm exec eslint <touched files>`. Baseline carries pre-existing warnings (unused `_`-prefixed parameters): zero new problems, no mass cleanup of old warnings.
4. Test: `pnpm exec vitest run <touched suites>`, then the full suite before claiming green. Unit tests mock `@/db`, so they cannot touch prod state.
5. Report only gates whose command output you ran in that same turn.
6. When the full suite reports timeouts in files you did not touch, check `uptime` first: this suite pays a per-test setup cost, so a loaded machine inflates timeouts across unrelated files. Re-run the named files alone, and let CI on a clean runner arbitrate the final verdict. State in the PR body that the local run was noisy and CI is the gate, rather than re-running the whole suite until the box quiets down.
7. Poll `gh pr view <n> --json statusCheckRollup` for the conclusions (not `gh pr checks`, which reports `pending` for jobs that already finished) and require `mergeStateStatus=CLEAN` before merging.

## Shipping

- Structured commit body (why / what / proof), then `gh pr create` with what is in, what was verified, and what is explicitly not proven. Never push to `main`, never merge, never delete a superseded branch.
- Production deploy (the repo's Cloudflare deploy script plus its smoke checks) happens only after Deep picks a decision card: a `needs_input` kanban block with options and your recommendation first, deploy action named as the recommended option. Stage it and say where it is staged.
- Keep contract PRs (API routes other cards depend on) draft until Deep says ship them; branch later fixes off `main` so each PR stays independently mergeable.

## Sending gates (who can actually receive mail)

- `deploy/cloudflare/worker.ts` pins `PILOT_STRICT_SENDS=1`: only pilot campaigns send. A pilot campaign's `pilot_campaigns.transport` decides: `record` transmits nothing (Inbox says "Recorded only. Not sent."), `live_test` only the 10-address allowlist, `live` any recipient that clears approval, country, pause, reply and bounce gates. worker.ts sets `PILOT_DEFAULT_TRANSPORT=live` (Deep, 9 Nov), so only campaigns created after that are live. Before answering "can the team send", read `transport` for their campaigns.
- Daily cap, bounce breaker and throttle count by sending address across all users (teammates share an imported inbox). Never re-add a `clerkUserId` predicate there.
- A new env var must land in three places or the app never sees it: `deploy.sh` `OPTIONAL`, `worker.ts` `APP_ENV`, and `env.env.example`; `src/lib/deploy/cloudflare-env.test.ts` checks the first two agree.
- lakeb2b.com, engageprob2b.com and spanglobalservices.com are on SURBL abuse (`dig +short <d>.multi.surbl.org` returns 127.0.0.64). No links to them in any draft or signature.
- Admin: re-inviting an existing member's email is the password reset (new set-password link); disable ends sessions at once.
- Draft guardrail `hasLowFrictionAsk` judges the last two sentences ending in . ! or ?; the prompt appends the profile signature, so before #136 any multi-line signature sent every draft to the generic fallback. When drafts come back as "Quick note" / GENERIC-SAFE FALLBACK, read the `Rules the AI drafts broke:` suffix in `ai_reasoning`.
- A Quick Send to a freemail address (gmail) has no company to research, so no citation, so `approveDraft` refuses it (`research_incomplete`, no waiver). Live tests go to a company-domain address.
- The send window is recipient-local 08:00 to 18:00; an India recipient tested in Deep's evening is approved and deferred to 08:00 IST (`outside_send_window` 409 from send-now is the gate working). A `live_test` campaign whose recipient is on the allowlist is exempt: the pilot gate marks those decisions `test: true` and `sendClaimedDraft` skips the window for them, so an owner-approved test need not wait for morning. Cold recipients keep the window; never widen it for them.
- "Is sending actually working?" is answered by one mail, not by the state you can see: send a real message from a production sender address to a real address Deep owns, then read the row back from `outreach_emails` and quote its `id`, `from`, `to`, `status` and `error`. Sending the test to a mailbox this app itself hosts proves the pipeline moved bytes, not that a third party accepted and delivered it, so send at least one copy to a domain Harbinger does not control. Report the exact address the copy went to: a test received on one address and "missing" on another was never missing.
- Driving prod as Deep: `browser_exec(local=True)` has his session; fire long calls (`/api/quick-send` streams 30 to 60 s) without awaiting in `js()` (5 s eval cap) and read `quick_sends.stage` from D1. Pilot draft actions are POST `/api/pilot/<campaign>/drafts/<draft>` with `action` approve (needs `versionHash`), edit, reject, redraft.

## Prod reads and smoke

- Read-only D1: `CI=1 npx wrangler d1 execute champ-harbinger --remote --json --command "<select>"` from `deploy/cloudflare` with `CLOUDFLARE_ACCOUNT_ID` set. Column names: `jobs.created_on`/`state`, `mailbox_connections.created_at` (ms epoch). Take the account id from `npx wrangler whoami` and export it: with the variable unset the same read failed with error 7403. For "is channel X really in use", count rows: `outreach_messages` and `channel_accounts` hold voice, WhatsApp and LinkedIn (empty means never used in production, whatever the code says), `sent_emails` holds email, `kg_nodes`/`kg_edges`/`kg_episodes` the graph, `signals`/`signal_results` the signals engine.
- `deploy/cloudflare/smoke.sh https://champ-harbinger.deep-ae0.workers.dev` needs the base URL argument; without it it exits 1 with a usage line.
- Deploy from a clean detached worktree of `origin/main` with `ENV_FILE=<canonical checkout>/deploy/cloudflare/env.env`; the container rollout wait takes 15 to 25 minutes, so run it in the background.
- A deploy that aborts before the LIVE line changed nothing: Cloudflare rejects some pre-deploy database calls (D1 error 7403) and the script stops, so prod keeps serving the previous build. Every state you read during that window describes the old code, including the UI and a healthy-looking jobs table. Confirm identity by `/api/version` after the LIVE line, not by absence of damage.
- Pair each deploy with a re-run of `smoke.sh` and the `/api/version` read in the same background job, so a completion notification carries the evidence instead of a bare exit 0.

## Proving the review-to-send path end to end

- Pilot draft actions are POST-only on `/api/pilot/<campaignId>/drafts/<draftId>` (PATCH answers 405): `approve` (bound to the versionHash the reviewer saw), `edit`, `reject`, `redraft` (optional `country`). Each takes a JSON body. Drive them from Deep's logged-in local browser session rather than reconstructing shapes from route code.
- The reviewer's queue is `/inbox/<campaignId>`; read its JSON from that same session to see what a teammate would actually see.
- `redraft` is how you re-run research after fixing a contact: it clears the stuck draft and queues a fresh one with readiness recomputed.
- Reject test drafts you do not want sent, and say in the reason why, so a leftover draft cannot be approved later.
- After any write, read the row back from D1 (`pilot_drafts`, plus `transport` on the campaign) before claiming the path works; a 200 only proves the route ran.

## Pitfalls

- Never write a status or guardrail message that asserts a check which did not run. Distinguish "has not been checked yet" / "was last seen X" / "is X": the fail-closed path is where a user reads the loudest claim, and a wrong claim there sends them fixing DNS that was fine.
- Writing a child row does not write derived caches (mailbox import does not populate domain health). Refresh derived state in the same request, or the new record looks broken until some background job happens to run.
- Repeated blind `patch` calls on a large file compound into structural damage; once two edits in a region misfire, read it and rewrite the enclosing function in one write.
- Send-now from any review surface is two writes: PATCH `reviewStatus: "approved"` (send-now 409s on anything else), then POST `/api/outreach/send-now`. When the second write fails, the first one still stands: the draft is approved and the scheduler sends it at `next_send_at`. Either PATCH it back to `pending` before showing it as reviewable again, or refresh so it shows as approved. Test the failure path's writes too, not only the happy path's, because a card that shows "Ready for review" over an approved row sends mail the user was just told did not go.
- A missing value must not render as a zero on `src/components/ui/gauge.tsx` (21st Gauge 1757). With `value={0}` the primary arc stays at opacity 1 and `strokeLinecap: "round"` paints an accent dot, so a null confidence looks the same as a real score of 0. For null, draw no primary arc (`primary="transparent"`, or leave out the Gauge) and use a track that shows in dark theme (`var(--border)`, not `var(--muted)`). Then assert in a test that the primary circle is not painted. An aria-label check alone passes while the dot still shows.
- "Drafts can't be approved" is usually a gate working as designed, not a broken button. `approveDraft` (`src/lib/pilot/review.ts`) refuses on `readiness.state === "blocked"` (for example, jurisdiction when the country is unknown), on empty `citations` (research_incomplete, with no waiver), and on lint hits. Readiness is stored in `pilotMeta` when a draft is composed and is never recomputed. Fixing the contact therefore means rejecting the draft and redrafting it (the `redraft` action on the pilot drafts route), not editing the draft. Read the live `/api/pilot/<id>/review` from Deep's logged-in local browser before touching code. Two things misread that gate as a bug: readiness is a snapshot, so a contact fixed after compose still fails until redraft; and a consumer-domain recipient (gmail and the like) has no company to research, so citations stay empty forever. Test the approval flow with a company-domain address or you will chase a gate that is working.
- `people` has no `updatedAt` and no tenant column, so `.set({ updatedAt })` on it fails tsc. A person edit is visible to every campaign that holds that person.
- A draft's `bodyText` and `bodyHtml` can diverge (seen on prod). Reviewers read bodyText while recipients get the HTML. When auditing what was approved, compare both.
- Fail-closed reads are right for sending and wrong for diagnosis: when capacity reads zero, check the backing table before believing the business conclusion.
- Any guardrail that judges the END of a draft (an ask in the last lines, tone, length) must skip prompt-ending boilerplate. The sender's signature rides along in the model output, and splitting on newlines turns a name, title and phone line into the "last sentences", so the tail check fails on every draft from that sender and silently swaps in the generic fallback: the reviewer sees a bland template with no sign of why. Strip sign-off lines before sentence splitting, write the fallback sentence so it reads as English with or without offering data, and make the fallback record which rule the model drafts broke so the swap is diagnosable rather than looking like a model choice.
