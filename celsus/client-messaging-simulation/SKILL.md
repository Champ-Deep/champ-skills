---
name: client-messaging-simulation
description: Use when building a ChampOracle client messaging report.
---

# Client messaging simulation reports

ChampOracle judges a client's live copy with a simulated audience and renders one
self-contained HTML report per account. The positioning is fixed: **a simulation
chooses which messages deserve a limited test budget, it never replaces the test.**
That disclaimer and the "happy to go deeper" close are in the template already;
do not soften or drop them, because the whole consultative angle depends on the
report being honest about what it is.

Repo: `~/repos/champoracle-agent` (uv, Python, `uv run champoracle ...`).

## Procedure

1. **Write the brief first** (`data/briefs/<client>.json`, template in
   `templates/brief.json` of this skill). Per account: `client`, `icp`
   (description, roles, geos, pains, intent), `site_url` and/or `ads`
   (1 to 3 pieces with headline/body/url), `ads_channel` (`meta_ad` or
   `search_ad`), `contact`, `panel_size` (20 default), optional `mix`.
   - Pull the client's real copy from their public site and Meta Ad Library;
     never invent placeholder copy and never paraphrase their ads.
   - ICP comes from the vault client note when one exists. Roles are segments
     the report will report on, so name them as the client would.
2. **Run it live**:
   ```
   cd ~/repos/champoracle-agent && set -a && source ~/.hermes/.env && set +a
   export CHAMPORACLE_LLM_MODEL=deepseek/deepseek-v4.1-flash
   uv run champoracle report data/briefs/<client>.json --out data/reports/<client>-<date>.html
   ```
   Key comes from `CHAMPORACLE_LLM_KEY` or `OPENROUTER_API_KEY` in `~/.hermes/.env`;
   the model defaults to `anthropic/claude-haiku-4.5` when `CHAMPORACLE_LLM_MODEL`
   is unset. Never print the key. Without any key the run falls back to the builtin
   panel, which is fine for tests and wrong for a client deliverable.
3. **Verify before showing anyone**: `uv run pytest -q` (17+ tests, the report test
   uses the builtin panel so it needs no key) and `uv run ruff check .` (line-length 140).
   Then read the HTML back: assert no em dash or en dash anywhere, the disclaimer
   box present, and the close present. Then render it at 1440 and 390 with the
   browser (`Emulation.setDeviceMetricsOverride`) and check `scrollWidth == innerWidth`
   plus a screenshot read, because the report is a client artifact and a broken
   phone layout is the failure Deep notices first.
4. **Stage the send, never send**: create a kanban card for the `inbox` lane with
   recipient, subject, three points, and the report path. Deep presses Send.
   APAC accounts are Rupak's; do not draft those.

## Hosted path (jobs + share link)

- `POST /v1/reports` (X-API-Key, brief JSON) queues a report in a thread and returns `{id, token, status}`;
  `GET /v1/reports/{id}` polls; when `status` is `done`, `share_path` is `/r/<token>`. `GET /r/<token>` is
  public (no key): the designed `web/report.html` when it exists, else the server HTML; `/r/<token>.json`
  is the data for the universe view. Workspace ids are stripped from the public JSON; keep it that way.
- deependhq.com proxies it: `POST /api/oracle/reports` and `GET /api/oracle/reports/<id>` with header
  `x-passcode` (Worker env `ORACLE_URL`, `ORACLE_KEY`, `ORACLE_PASSCODE`); `share_url` comes back absolute.
  Prove the proxy with `node scripts/oracle-proxy-selftest.mjs` against a local `champoracle serve`,
  because `wrangler dev` dies with `spawn EBADF` under the agent terminal.
- UI briefs with the decided 21st.dev ids: `champoracle-agent/docs/ui-brief-v1.md` (share view) and
  `deependhq-site/docs/ui-brief-oracle-v1.md` (toolkit page). The 21st.dev MCP may not be loaded in the
  main lane; call `https://21st.dev/api/mcp` directly with `tools/call` `search` (key from `~/.hermes/.env`,
  never printed) and open 3 preview images with vision before writing a component table.
- Hosting is a Deep decision (Clef: client-facing plus spend). Deep chose Cloudflare on 2026-11-09.

## Cloudflare deployment (`cf/` in champoracle-agent)

- Worker `champoracle` + `OracleContainer` (Container class, `basic`, `sleepAfter 30m`, `max_instances 1`) built from the root
  Dockerfile; URL https://champoracle.deep-ae0.workers.dev. Deploy: `cd cf && CI=1 npx wrangler deploy` (Docker via OrbStack must
  be running: `open -a OrbStack`). A config-only or secret-only deploy does not restart the container; only an image change rolls it.
- Disk is ephemeral. `persist.py` restores `/data/champoracle.db` from the Worker's `/_restore` on boot and PUTs a sqlite-backup
  snapshot to `/_backup` (R2 bucket `champoracle-data`) every 30s when changed and on shutdown. A failed restore disables backups
  for that run so an empty DB never overwrites a good snapshot. Cloudflare returns 403 to the default `Python-urllib` agent, so
  the client sends `User-Agent: ChampOracle/0.2`. Inspect the snapshot with `wrangler r2 object get champoracle-data/champoracle.db --remote`.
- Secrets on the Worker: `CHAMPORACLE_BOOTSTRAP_KEY` (the ops workspace key; `db.workspace_for_key` mints the workspace on first
  use, so rotation needs a container restart but no shell), `CHAMPORACLE_BACKUP_SECRET`, `CHAMPORACLE_LLM_KEY` (Deep pastes it).
  Generate random secrets with `openssl rand` piped straight into `wrangler secret put`; never print them, never keep the temp file.
- deependhq has an undeployed version, so `wrangler secret put` there fails; use `wrangler versions secret put` and let the page
  card deploy the version.
- Wrangler API calls 504 during Cloudflare partial outages (check cloudflarestatus.com); retry the deploy, do not change code.
  `ImagePullError: runtime failed unpacking the image` in `wrangler containers info <app>` is the same class of transient.

## Pitfalls

- **`mix` must null out the B2B dimensions for a B2C audience** (`"seniority": null,
  "company_size": null, "decision_role": null, "inbox_load": null`). The ICP builder
  defaults every audience to B2B traits, so a Bengaluru shopper panel otherwise gets
  personas whose `seniority` is `unknown`, which wastes prompt tokens and can leak
  into persona names and quotes.
- **Panel calls run serially**: a 20-persona, 2-channel run is about 4.5 minutes on
  DeepSeek Flash. Budget it, run it in the background with a notify, and do not
  re-run the whole report to change one line of copy; edit the brief and re-run only
  when the change actually moves a variant.
- **Analyst prose comes out dense with `n=`, `mean=`, `positive=`** because the
  summary is generated from raw stats. That is acceptable for Deep's review; if the
  report goes to a client, rewrite the summary bullets in plain language yourself
  rather than shipping the raw notation.
- **The Oracle rewrite is LLM copy**: read it before any client sees it, and confirm
  it invents no price, place or feature the current copy does not state (the rewrite
  prompt already forbids this, but check).
- **Em dash filtering happens at render time** in the HTML escaper, not in the data.
  If you surface raw panel quotes anywhere else (an email, a chat message), strip
  dashes there too.
- **The report is committed, the data is not**: `data/` is gitignored, so briefs and
  reports never leave the machine through a push. Commit only `src/` and `tests/` on
  a feature branch; do not merge without Deep.
