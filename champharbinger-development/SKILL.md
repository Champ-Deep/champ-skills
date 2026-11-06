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

## Shipping

- Structured commit body (why / what / proof), then `gh pr create` with what is in, what was verified, and what is explicitly not proven. Never push to `main`, never merge, never delete a superseded branch.
- Production deploy (the repo's Cloudflare deploy script plus its smoke checks) happens only after Deep picks a decision card: a `needs_input` kanban block with options and your recommendation first, deploy action named as the recommended option. Stage it and say where it is staged.
- Keep contract PRs (API routes other cards depend on) draft until Deep says ship them; branch later fixes off `main` so each PR stays independently mergeable.

## Pitfalls

- Never write a status or guardrail message that asserts a check which did not run. Distinguish "has not been checked yet" / "was last seen X" / "is X": the fail-closed path is where a user reads the loudest claim, and a wrong claim there sends them fixing DNS that was fine.
- Writing a child row does not write derived caches (mailbox import does not populate domain health). Refresh derived state in the same request, or the new record looks broken until some background job happens to run.
- Repeated blind `patch` calls on a large file compound into structural damage; once two edits in a region misfire, read it and rewrite the enclosing function in one write.
- Send-now from any review surface is two writes: PATCH `reviewStatus: "approved"` (send-now 409s on anything else), then POST `/api/outreach/send-now`. When the second write fails, the first one still stands: the draft is approved and the scheduler sends it at `next_send_at`. Either PATCH it back to `pending` before showing it as reviewable again, or refresh so it shows as approved. Test the failure path's writes too, not only the happy path's, because a card that shows "Ready for review" over an approved row sends mail the user was just told did not go.
- A missing value must not render as a zero on `src/components/ui/gauge.tsx` (21st Gauge 1757). With `value={0}` the primary arc stays at opacity 1 and `strokeLinecap: "round"` paints an accent dot, so a null confidence looks the same as a real score of 0. For null, draw no primary arc (`primary="transparent"`, or leave out the Gauge) and use a track that shows in dark theme (`var(--border)`, not `var(--muted)`). Then assert in a test that the primary circle is not painted. An aria-label check alone passes while the dot still shows.
- "Drafts can't be approved" is usually a gate working as designed, not a broken button. `approveDraft` (`src/lib/pilot/review.ts`) refuses on `readiness.state === "blocked"` (for example, jurisdiction when the country is unknown), on empty `citations` (research_incomplete, with no waiver), and on lint hits. Readiness is stored in `pilotMeta` when a draft is composed and is never recomputed. Fixing the contact therefore means rejecting the draft and redrafting it (the `redraft` action on the pilot drafts route), not editing the draft. Read the live `/api/pilot/<id>/review` from Deep's logged-in local browser before touching code.
- `people` has no `updatedAt` and no tenant column, so `.set({ updatedAt })` on it fails tsc. A person edit is visible to every campaign that holds that person.
- A draft's `bodyText` and `bodyHtml` can diverge (seen on prod). Reviewers read bodyText while recipients get the HTML. When auditing what was approved, compare both.
- Fail-closed reads are right for sending and wrong for diagnosis: when capacity reads zero, check the backing table before believing the business conclusion.
