# Container deploys

Depth for deploying an image-based Cloudflare Worker app from a repo deploy
script. The always-on rules in the main skill cover reading back what is live;
this covers performing the deploy and diagnosing a run that died.

## Read the script's step order before trusting a failed run

The typical order is: validate env, confirm the local container daemon, **apply
remote schema migrations**, build and push images, wait for the rollout, health
check. Because the migration step runs before any image work, a run that dies at
the image build has already applied the schema.

- Never assume "the deploy failed, so nothing changed". Determine what landed with
  `npx wrangler d1 migrations list <db> --remote`, run from the directory holding
  `wrangler.jsonc`; it answers `No migrations to apply!` when the journal is fully
  applied. Additive migrations leave the old app serving normally, so the real
  exposure is that a rollback now runs old code against a newer schema, and the
  destructive fix (dropping the added tables) is the wrong one. Report the schema
  as ahead of the code rather than omitting it.

## Secret-push mode is a tradeoff, not a default

The script's default repushes the repo's env file over the live secrets, which can
replace a newer dashboard value with a stale one; keys the file does not list stay
untouched either way. Ship code only (`KEEP_DASHBOARD_SECRETS=1` in the Cloudflare
script) when secrets may have been rotated since the last push, and name which mode
you chose and why in the report.

## The local container daemon, not your code

A container build that dies with `rpc error ... Unavailable` or `error reading from
server: EOF` failed because the local container daemon went away, not because of
the Dockerfile or your changes. Run `docker info` before reading a single build
step, and expect a multi-minute image build to be exactly where a daemon stop
surfaces; the daemon being healthy at the start of the run proves nothing about
minute ten.

On a Mac running OrbStack rather than Docker Desktop, `open -a Docker` fails
outright with "Unable to find application named Docker". Use `open -a OrbStack` and
then `orb start`: opening the app can leave the engine reporting `Stopped` (which
`orb status` shows), so confirm `docker info` succeeds before relaunching anything,
then re-run the deploy unchanged. The retry is safe because the migration step
idempotently reports nothing left to apply.

## Verifying the new build

The deploy script bakes a build id of timestamp plus git short SHA, exposed at
`/api/version`. That id is the only cheap proof the new code is serving: an HTTP
200, a warm link, or the old version string all describe the previous build.
Read it after the rollout line, never during the build window.