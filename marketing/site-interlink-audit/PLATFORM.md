# Interlink Platform - What this is

Four tools that share one crawl. Use them in this order.

| Tool | Question it answers | Command |
|---|---|---|
| `refresh.py` | Is the audit current? | `python3 refresh.py --list sites.txt` |
| `semantic.py` | What ELSE could this page link to? | `python3 semantic.py bundle-<site>.json` |
| `component.py` | What should a visitor see here? | `python3 component.py --bundle bundle-<site>.json` |
| `interlink_audit.py` | One-shot audit of one domain | `python3 interlink_audit.py <domain> -o out.html` |

---

## 1. Keep it current: `refresh.py`

Drop domains into `sites.txt`, one per line. Comments and blank lines are fine. A JSON
array or a comma-separated blob also works, so paste whatever you have.

```bash
python3 refresh.py --list sites.txt          # everything in the list
python3 refresh.py --site spanglobalservices.com   # one domain
python3 refresh.py --all                     # re-audit what we already have, crawl nothing new
python3 refresh.py --list sites.txt --force  # ignore the cache and re-crawl
```

A refresh reuses the cached crawl unless `--force`, then rebuilds **four** artefacts per
site:

1. the plan (`bundle-<slug>-plan.json`)
2. the HTML report (`reports/interlink-<slug>.html`)
3. the related-link file (`bundle-<slug>-related.json`)
4. the site widget (`widget-<slug>/`)

It exits non-zero if any site fails, and writes `refresh-summary.json` with the headline
numbers per site so you can diff two runs.

**Coverage.** Discovery reads robots.txt, then nested XML sitemaps, then the WordPress REST
API as a fallback. Nothing is hardcoded to a platform or a domain. The report states its
own coverage and, when the crawl was capped, says so in a finding card.

---

## 2. Related links, not just same-technology: `semantic.py`

The obvious links are already made. This finds the ones nobody has thought of, across
sections:

```
Data Cleansing            -> What is Data Cleansing?
Healthcare List           -> What is a Healthcare Email List?
Data Profiling            -> How Data Profiling is done?
NetSuite users list       -> Sage Intacct finance page
```

It builds TF-IDF vectors over page body and title (never the URL: that rewards slug
similarity over content similarity), then finds nearest neighbours through an inverted
index over discriminating terms only. That is what keeps a 3,000-page site at ~35 seconds
instead of four minutes.

Output bands, not magnitudes:

| Band | Meaning |
|---|---|
| `strong` | Read this one first |
| `likely` | Defensible, needs an editor's eye |
| `possible` | Worth considering |
| `weak` | Below the noise floor |

The top 15 are deduplicated by target title, because 25 technology-list pages share the
title "What ROI can I expect?" and one template page repeated 25 times is one idea.

Every suggestion carries a written reason. A score nobody can justify is not deliverable.

### CLEF (Cloudflare's SystemOne model)

CLEF is wired in as an optional judge that sharpens the rule score. It is **not** required:
the rules run standalone and every score keeps its rationale.

| Mode | How to enable | Notes |
|---|---|---|
| `none` | default | Rules only. Fully functional. |
| `hosted` | `export CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=...` | Workers AI, same SystemOne API. Cheap. **Recommended.** |
| `local` | `export CLEF_PATH=<snapshot dir> CLEF_PY=<python>` | Full `clef` weights are **55 GB**; `clef-flash` is **19 GB**. Only for a machine with room. |

All questions go out in **one batched request**. A decision model evaluates each question
against the same state in isolation, so N candidates cost one round trip, not N. That is
the documented pattern and it is where the speed comes from.

Two rules the blend must keep:

- The rule score stays in its own column, so a bad judgement is visible after the fact
  rather than hidden inside a number.
- **A missing judgement never scores better than a real one.** An unjudged candidate is
  multiplied by 0.85, and a test asserts `unjudged <= judged`.

Check which mode is active:

```bash
python3 semantic.py bundle-spanglobalservices-com.json
# clef mode: none  (55 GB local weights or 19 GB flash; set CLEF_PATH or CLOUDFLARE_API_TOKEN to enable)
```

---

## 3. The on-site component: `component.py`

A drop-in carousel that recommends from a catalogue you maintain. No build step: the page
announces itself, the widget scores the catalogue against it, and only relevant entries
render.

```bash
python3 component.py --bundle bundle-spanglobalservices-com.json
# -> widget-spanglobalservices-com/related-sites.html
# -> widget-spanglobalservices-com/related-sites.js
```

### Install

```html
<!-- in <head> -->
<script src="/related-sites.js" defer></script>

<!-- per page, to sharpen results -->
<meta name="related-profile" content="data_broker">
<meta name="related-tokens" content="data,leads,email-list,healthcare">

<!-- where the carousel should appear -->
<script src="/related-sites.html" defer></script>
```

### Site profiles

The widget reads the site TYPE and tailors to it. Detected automatically from the corpus.

| Profile | For | Affinity boost |
|---|---|---|
| `data_broker` | Data and lead generation | martech, salestech, growthtech |
| `consultancy` | Advisory | - |
| `saas` | Software platform | - |

Override per page with `data-related-profile` on `<body>` or the meta tag.

### The catalogue

`catalog.json` is the file a team maintains. Add a site and it becomes eligible everywhere:

```json
{ "domain": "example.com",
  "name": "Example",
  "url": "https://example.com",
  "blurb": "One sentence a reader can act on.",
  "tags": ["data", "leads", "platform"] }
```

The widget never recommends the site you are already on. That is enforced at build time
and again at runtime against `location.hostname`.

### Theme it

The widget uses CSS custom properties. Set them on `:root`:

```css
:root { --rsw-bg:#fff; --rsw-fg:#0d1424; --rsw-mut:#5b6678;
        --rsw-line:#dde3ec; --rsw-acc:#1a56db; --rsw-face:#fbfcfe; }
```

Arrows hide themselves when everything fits, disable at each end, and the blurb clamps to
three lines. Honours `prefers-reduced-motion`.

---

## Adding a site, end to end

```bash
echo "newclient.com" >> sites.txt
python3 refresh.py --site newclient.com
open reports/interlink-newclient-com.html
```

That gives you the audit, the related links, and the widget in one command.

---

## What is verified

| Site | Pages | DOM checks | Visual @1440/390 |
|---|---|---|---|
| spanglobalservices.com | 3,218 | 29/29 | 0 fail |
| lakeb2b.com | 2,532 | 29/29 | 0 fail |
| www.apollo.io | 1,199 | 29/29 | 0 fail |
| www.activecampaign.com | 800 | 29/29 | 0 fail |
| deependhq.com | 35 | 26/26 | 0 fail |

`test_units.py` covers the failures that actually happened in development, each now a
regression test: a footer CTA misclassifying every page as BOFU, a hidden checkbox
truncating a 2,964-word page to 72, a bare `a` prefix in the article filter discarding
Adobe and Amazon, a competitive-set cap silently dropping 34 of 60 entities, a
self-referential CSS variable that erased every border, and a similarity cap that made 59%
of candidates tie at the same score.

```bash
python3 -B test_units.py          # 49 checks on the logic
python3 -B verify_report.py <report.html>   # 29 checks on a rendered report
```

---

## Honest limits

- Link suggestions are scored, not written. Someone reads the sentence and confirms the
  link still makes sense.
- Entity quality tracks copy quality. A site whose content is mostly adjectives will
  surface adjectives. Add the word to `VERB` in `entities.py`.
- CLEF in hosted mode needs your Cloudflare credentials. Nothing else here does.
- A crawl over the cap reports partial coverage and says so in a finding card.