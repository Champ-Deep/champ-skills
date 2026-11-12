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
     the report will report on, so name them as the client would. Exception: when
     the note or a meeting restricts the ICP to one brand group (SPAN ICP stays in
     the SPAN group), or the note holds vendor invoices, staffing or proposals, take
     personas from public site copy only and give each persona its `source_ids`.
2. **Run it live**:
   ```
   cd ~/repos/champoracle-agent && export OPENROUTER_API_KEY="$(grep '^OPENROUTER_API_KEY=' ~/.hermes/.env | cut -d= -f2-)"
   sh <skill dir>/scripts/key_health.sh   # limit fields only; stop if limit_remaining is too low
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
- Functional check of any running instance: `CHAMPORACLE_URL=... CHAMPORACLE_KEY=... uv run python scripts/hosted_smoke.py --panel 8 [--hosted]`
  (21 checks: auth, validation, job to done, share page and JSON, leak checks, backup routes). The ops key lives in the macOS
  Keychain: `security find-generic-password -s champoracle-ops -w`. Prove the LLM path on the production image locally with
  `docker run ... -e CHAMPORACLE_LLM_KEY=... co-local` rather than putting a shared key on the host.
- Never `source` or `set -a; . ~/.hermes/.env`: a malformed line echoes a secret into the transcript. Read one var with
  `grep '^NAME=' ~/.hermes/.env | cut -d= -f2-` only inside an assignment or `$(...)` that is never echoed; run bare, it prints
  the key. For key health use `scripts/key_health.sh` by path. Never paste a secret-reading command into a kanban comment or
  card body: the board redactor turns the `$(grep` and `KEY='` parts into `***`, so the stored command no longer runs and the
  worker falls back to whatever the body said.
- Wrangler API calls 504 during Cloudflare partial outages (check cloudflarestatus.com); retry the deploy, do not change code.
  `ImagePullError: runtime failed unpacking the image` in `wrangler containers info <app>` is the same class of transient.

## Pitfalls

- **Keep variant labels plain** (`Emailer 1`, not `Emailer 1: product introduction`). The panel model echoes the label back, and a label with a colon or comma comes back altered; reactions with an unknown label are dropped.
- **Email channels take `subject`, not `headline`** (`email_cold`, `email_marketing`): the channel spec's `fields` decide the key, so a brief that says `headline` for an email gets no subject line scored. Use `{label, subject, body}` for emails and `{label, headline, body}` for ads.
- **Drop the per-variant "copy fixes" diagnostics from a client page.** They print benchmark figures with no source the client can check (for example "35.7% vs 16.7%") and can flag "no call to action" on copy that has one. Keep the ranking, the drivers line in plain words and the quotes.
- **Persona names ignore the geo**: an India panel comes back with names like Ben, Marcus, Sofia and Kofi, and two personas can share a first name. Before a client sees the quotes, check the names shown, and do not put two quotes with the same name in one card unless the label says they are different readers.
- **On a client page the tool is never named.** It is the "<Brand> simulation" ("LakeB2B simulation") and the rewrite is the "<Brand> rewrite"; the model name stays out too. Rename at the point the page data is built, and search the built page and the PDF text for the tool name before delivery.
- **`analyze()` can hang for many minutes after both tests show `locked`**, because the analyst summary is one unbounded LLM call. When `tests.status` is `locked` and the process is still alive, kill it and rebuild the data with `service.get_test(ws, tid)` plus `service.breakdown(ws, tid)`; the ranking and every reaction are already in the DB, and client-facing prose is rewritten by hand anyway.
- **Count scored personas before quoting the panel size.** On DeepSeek Flash with six variants in one prompt only about half of a 24-persona panel returned a usable reaction on two runs in a row. Report "n of N returned a scored reaction", never the audience size alone.
- **To put real results beside the simulation**, pass the sends as `ads` with `ads_channel: "email_marketing"` (body only when subject lines are not on file for every send, so no variant is advantaged), then show actual click rate against the 80% band per send. The simulation reads copy only, so say that send order and list fatigue are outside it.

- **Never copy the B2C null `mix` into a B2B brief.** For agency founders, marketers or any buyer reading cold email, keep the
  default traits (`inbox_load` and `decision_role` are what a cold email is judged on) and set `icp.seniority` (for example
  `["owner", "director"]`) so personas are not `unknown`. An agency panel that nulled them came back with consumer deal attitudes
  ("discount hunter", "brand loyal") as its only trait segments.
- **The rank-1 level is often the 3.00x lift ceiling** (`agent_lifts` clips at 3.0). When the winner shows "reacts 3.00x typical
  copy", its predicted rate is the cap, not a measurement: say so, and judge the lead by panel mean, positive count and band
  overlap. Re-scoring identical copy in a second panel moved its mean from 0.343 to 0.090, so a within-run gap of that size is a lean.
- **A rewritten CTA that offers an artifact ("want the full report?") needs that artifact carded** before `final` is handed to
  staging, and the staging child must get a comment saying so. If the artifact derives from a client's report, sharing it is a
  Deep decision (needs_input), not a staging step.
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
