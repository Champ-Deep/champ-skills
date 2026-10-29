---
name: event-scout-ocr-bench
description: "Use when Event Scout card scans fail or OCR changes."
---

# Event Scout OCR benchmark

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

- A 0.00 accuracy row is usually a dead key or retired model, not OCR quality. Found 2026-10-29: `gemini-2.0-flash` NOT_FOUND, Railway Gemini key free tier RESOURCE_EXHAUSTED, Railway OpenRouter key 401, `anthropic/claude-sonnet-4-5` gone from OpenRouter. Check `GET /v1beta/models?key=` and `GET openrouter.ai/api/v1/models` first.
- Pin Gemini direct to `-latest` aliases (`gemini-flash-lite-latest`); dated flash models retire within months and the scan path dies silently.
- Time the call inside the semaphore, not around it, or queue wait inflates latency.
- Real photographed cards never go into `bench/cards/` in git (public repo). `bench/cards/r*` is gitignored; add them locally with a matching `.json`.
- Result 2026-10-29 (39 images): haiku-5.5 1.00 fields, gemini-3.5-flash-lite (OR) 1.00/0.97 per card, gpt-6-luna 0.99, tesseract+regex 0.66. Haiku real latency 2.7 to 3.8s, about $0.0002 per card.
- `source ~/.hermes/.env` leaks a malformed line as a shell error; read a single key with a python regex instead.
