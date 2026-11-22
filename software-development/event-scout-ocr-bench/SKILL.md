---
name: event-scout-ocr-bench
description: "Use when Event Scout card scans fail or OCR changes."
---

# Event Scout OCR benchmark

## Cloudflare build (branch cf/native, since 2026-11-21)

Event Scout runs as a Worker at `https://event-scout.deep-ae0.workers.dev` (code in `worker/`, D1 `event-scout-db`, KV `event-scout-files`). OCR is `ocrCard` in `worker/src/routes/core.ts`: OpenRouter only when the `OPENROUTER_API_KEY` secret is set, then Workers AI vision. Bench it through the live Worker, not Railway: `BASE=... TOKEN=<admin session> CARDS=~/repos/event-scout/bench/cards MODELS=@cf/a,@cf/b node worker/test/ocr_bench.mjs` (calls the admin-only `POST /api/admin/ocr_probe?model=`, saves nothing).

- Result 2026-11-21, 24 images (photo + glare): `@cf/mistralai/mistral-small-3.1-24b-instruct` 99.4% fields, 23/24 perfect, p50 3.6 s, p95 6.4 s; `@cf/meta/llama-4-scout-17b-16e-instruct` 97.6%, 20/24, p50 7.7 s. Mistral is primary. Never bench `@cf/moonshotai/*` (banned).
- An admin session for a bench: register a throwaway via `/api/register/`, set `is_admin=1` with `wrangler d1 execute --remote` by id (the tool masks digits in emails, so match on id), log in, and delete the user and its rows after. **Sign-up is gated since 2026-11-22** (option A ruling): `SIGNUP_DOMAINS` (championsmail.com, championsgroup.com, lakeb2b.com) and `SIGNUP_ALLOW_EMAILS` (3 named gmail users) live in `worker/wrangler.jsonc`. A register call outside that set returns 403 with "Sign-up is limited to company email addresses". For a throwaway, use a `@eventscout.dev` address and add it to `SIGNUP_ALLOW_EMAILS` (local `.dev.vars` is enough for `wrangler dev`; the live worker needs a redeploy), or insert the row with `wrangler d1 execute --remote` directly. Existing accounts keep working: the gate only stops new registrations. Python urllib gets 403 from workers.dev; use node fetch or curl. When a run needs a clean slate, delete the test user and re-register the same address: it gets a fresh id instead of inheriting the previous run's rows. Clean up with ONE D1 statement deleting the child rows (`harbinger_sync`, `contact_embeddings`, `shared_contacts`, `contacts`, `sessions`, `user_profiles`, `user_cards`) by `user_id in (select id from users where ...)` and then the user; a per-table sweep that misses a child table leaves counts that look like data loss.
- The Vercel project for this app was deleted (the ask removed the frontend host), so the app's only address is the workers.dev URL above. The remaining Railway service is API and archive only, and its own web UI no longer has a hostname.
- Local regression: `node test/smoke.mjs` with `BASE`, `CARD` and `CARD_JSON` set boots `wrangler dev --local --port 8793`, scans one card through the real extractor and cleans its own user up. Kill any stray dev process first and build assets once (`sh scripts/build-assets.sh`) or the boot serves nothing and every assertion fails. Secrets in `wrangler secret put` do NOT reach a `wrangler dev` subprocess; the test must write its own `.dev.vars.<test>` beside the test file (the format is a plain `KEY=value` body interpolated into a `writeFileSync` template), so a gated route needs its allow-list written there too, not assumed from the deployed config.
- `node test/smoke.mjs` against the **live** worker (`BASE=<workers.dev URL>`) does not boot anything: it registers its own `smoke+<nonce>@eventscout.dev` user, so a gated sign-up makes it fail at registration until that domain is in `SIGNUP_ALLOW_EMAILS`. It deletes its own rows, but the delete is a plain HTTP path, so a run that dies mid-way leaves the user behind: recount `SELECT count(*) FROM users` afterwards rather than trusting the cleanup line.
- Wrangler's `--json` output for a multi-statement `--command` cannot be parsed as one JSON array (`KeyError: -1` when indexing `results`), and a statement that errors inside the batch returns no results at all while still exiting 0 through the pipe. Run one DELETE per `wrangler d1 execute` call and grep each for `"changes"` before moving on; never batch child-then-parent cleanup into one call.
- `fetch().text()` strips the CSV's UTF-8 BOM; assert the BOM on `arrayBuffer()` bytes.
- The Railway steps below are the legacy path, kept for the archive database only.

Reproduce with the benchmark before touching the extractor. Repo `~/repos/event-scout` (public). Scan path: `add_contact_from_image` -> `extract_contact_with_openrouter` (primary) -> `extract_contact_from_image_with_gemini` (fallback). One prompt `OCR_PROMPT`, one field set `OCR_EMPTY` (name, title, company_name, email, phone, linkedin, website). Website is stored in `links` with label `Website`; title in `contacts.title`.

## Reproduce before guessing

```bash
cd ~/repos/event-scout && railway link --project event-scout --environment production && railway service event-scout
export GEMINI_API_KEY=$(railway variables --json | python3 -c "import sys,json; print(json.load(sys.stdin)['GEMINI_API_KEY'])")   # never echo it
python3 bench/make_cards.py            # 12 synthetic cards x (clean, photo, hard glare) = 36 images with ground truth
python3 bench/ocr_bench.py --limit 3 --only "or:anthropic/claude-haiku-5.5,tesseract:local"   # smoke first, then full
```

The runner prints a markdown table (field accuracy, all-fields-per-card, p50/p95 latency, OpenRouter cost) and writes `bench/results/<ts>.{json,md}`. Read `detail[cand][i].error` before trusting an accuracy number: an error row scores zero and looks like a bad model.

## Lessons

- Prove the app with the key the app ships, not the Railway key. `scripts/prod_smoke.py` reads `APP_API_KEY` from Railway, so it passes while the live web app (`event-scout-delta.vercel.app`, hardcoded `CONFIG.API_KEY` in `mobile-frontend.html`) gets 401 on every call: "Failed to load contacts" and scans that never finish. Compare the two values in python without printing either. The fix, when they differ, is `railway variables --set APP_API_KEY=<the value the app ships>`; it needs no code change and Railway redeploy is the confirmation. After the fix, prove it as one loop with the app's key: `list_contacts` -> one scan -> `export_contacts` -> `DELETE /contact/{contact_id}?user_id=...`.
- Assert scan output against known ground truth in the right response key: `POST /add_contact_from_image` returns `extracted_fields` (parsed) alongside `contact`/`contact_id` (stored), so a checker aimed at the wrong key reports every field mismatched on a perfect extraction.
- Read `railway logs` after a passing scan to see which provider served it. A pass can hide a dead primary: OpenRouter 401s (a dead key reports `User not found`), then Gemini, at 10 to 19 s a card against a 30 s client timeout, versus 2.7 to 3.8 s on the healthy primary.
- Test contacts are deleted one at a time through `DELETE /contact/{contact_id}?user_id=...` (there is no bulk or user-level delete), so record each `contact_id` as you create it; reusing one test user across runs is still right, because every scan registers a new row.

- A 0.00 accuracy row is usually a dead key or retired model, not OCR quality. Found 2026-10-29: `gemini-2.0-flash` NOT_FOUND, Railway Gemini key free tier RESOURCE_EXHAUSTED, Railway OpenRouter key 401, `anthropic/claude-sonnet-4-5` gone from OpenRouter. Check `GET /v1beta/models?key=` and `GET openrouter.ai/api/v1/models` first.
- Pin Gemini direct to `-latest` aliases (`gemini-flash-lite-latest`); dated flash models retire within months and the scan path dies silently.
- Time the call inside the semaphore, not around it, or queue wait inflates latency.
- Real photographed cards never go into `bench/cards/` in git (public repo). `bench/cards/r*` is gitignored; add them locally with a matching `.json`.
- Result 2026-10-29 (39 images): haiku-5.5 1.00 fields, gemini-3.5-flash-lite (OR) 1.00/0.97 per card, gpt-6-luna 0.99, tesseract+regex 0.66. Haiku real latency 2.7 to 3.8s, about $0.0002 per card.
- `source ~/.hermes/.env` leaks a malformed line as a shell error; read a single key with a python regex instead.
