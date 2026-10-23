# Worker secrets, bindings and operator rows

Three different things people call "the Cloudflare config". Mixing them up is
why a feature ships enabled in code and silently off in production.

## Set secrets in bulk, from the repo

```bash
cd /Users/deep/repos/deependhq-refresh
npx wrangler whoami               # proves auth before anything else
cp .env.example .dev.vars          # gitignored template, comments say where each key comes from
# fill .dev.vars, then:
npx wrangler secret bulk .dev.vars # every KEY=VALUE in one request, up to 100 keys
```

- **`wrangler secret bulk` works even though `wrangler dev` does not.** A broken
  `workerd` binary only affects local dev; auth, secrets and API calls go over
  plain HTTPS. `whoami` returned an OAuth login on this machine, so no
  `CLOUDFLARE_API_TOKEN` is needed. Check auth first rather than assuming a
  token exists somewhere.
- **Secrets vs bindings vs rows.** A secret is `KEY=VALUE` in `.dev.vars`. A
  binding (`TOOLKIT_DB`, `ANALYTICS`) lives in `wrangler.jsonc`, created with
  `npx wrangler d1 create <name>` and its id added to the config before the next
  deploy, with its schema applied via `wrangler d1 execute <name> --remote
  --file=migrations/...`. An operator setting like `welcome_credits` is a D1
  row, not an env var: no secret enables a feature that reads a missing row, and
  the feature stays silently off.
- **`.gitignore` is the trap.** `.env*` and `.dev.vars*` are ignored;
  `!.env.example` is the deliberate exception, so the template ships to git and
  the filled file never does. Run `git check-ignore -v <file>` before
  committing a template you just wrote.
- **`.dev.vars` is also read by `wrangler dev`.** A real paid-provider key left
  in it bills real calls from any local run. Blank values are safe by design on
  this site: the toolkit reads every optional `env.*` key and fails closed
  (sign-in hidden, tool disabled) instead of erroring, so partial files deploy
  fine and can be filled in later.
- **A public key is fine as a secret.** Clerk's publishable key and script URL
  are public by nature; storing them as secrets is harmless because the Worker
  reads them either way. Only `whsec_` and `sk_` values are actually sensitive.

## Key inventory for this Worker

Read the names off the code, not memory: `grep -ohE "env\.[A-Z_]{4,}" worker/*.js | sort -u`.

| Key | Kind | Consequence when absent |
|---|---|---|
| `CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY` | secret | sign-in hidden, toolkit fails closed |
| `CLERK_WEBHOOK_SIGNING_SECRET` | secret | paid grants from billing webhooks not verified |
| `CLERK_JWT_KEY`, `CLERK_JS_URL`, `CLERK_ADMIN_IDS`, `CLERK_AUTHORIZED_PARTIES` | secret | optional; falls back to defaults in code |
| `TREG_API_KEY`, `OPENROUTER_API_KEY`, `JEV_API_KEY`, `LEAD_SCORER_MODEL` | secret | that tool disables itself |
| `TOOLKIT_DB` | D1 binding | wallet and billing unavailable, tools refuse to run |
| `ANALYTICS` | Analytics Engine binding | `/api/collect` answers 204 and records nothing |
