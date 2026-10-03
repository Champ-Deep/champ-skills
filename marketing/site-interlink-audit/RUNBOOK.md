# Interlink Audit - Team Runbook

Point it at any client site. It crawls, analyses the internal linking, and produces a
self-contained HTML report you can send to the client or open in a standup.

---

## Quick start

```bash
cd ~/.hermes/cache/scratch/sitearch
python3 -B interlink_audit.py <domain> -o /tmp/<client>.html
```

Example:

```bash
python3 -B interlink_audit.py www.spanglobalservices.com -o /tmp/span.html
```

Flags:

| Flag | Default | When to use it |
|---|---|---|
| `--cap N` | 6000 | Cap on pages fetched. Lower it for a fast look, raise it for a big site. |
| `--no-verify` | off | Skip the automated checks. Only for debugging. |
| `--no-audit` | off | Skip the visual audit. Slightly faster. |
| `-o PATH` | `/tmp/interlink-<domain>.html` | Where the report lands. |

The command prints a summary, runs 29 automated DOM checks, and a visual audit at 1440px
and 390px. **A green run ends with `passed, 0 failed` and `audit OK` on both widths.**

---

## Reading the report

Three tabs.

**Site map** - a treemap. Each tile is a section of the site, sized by page count and
coloured by how much of it is stranded (no inbound links). Red means stranded. Open it for
detail.

**Entities** - the topics the site is *about*, learned from the site's own pages. Each row
is an entity, how many pages it owns, and how many of those pages are stranded. This is the
list of link targets you will build toward.

**Worklist** - the actual edits, ranked. Each row is a page and the specific links to add.
Tick them off as you go; progress is saved in the browser.

---

## What the numbers mean

| KPI | Meaning |
|---|---|
| `pages with no inbound link` | Orphaned. No page links to them, so they cannot rank and readers cannot find them. |
| `pages with no outbound link` | Dead ends. Nothing to click onward from. |
| `commercial pages with no research page` | Missing the top of the funnel. A sales page with nothing to inform a buyer first. |
| `links to add` | Mentions already present in the copy that were never turned into links. Cheapest wins, no new writing. |
| `pages in the XML sitemap` | Discovery. Being listed is not the same as being linked. |

Read the **Key Findings** cards at the top first. They are generated from the crawl, not
from a template, and they state the actual verdict.

---

## The three-layer model

Every finding maps to one architecture problem:

- **L1 TOFU** - research page that answers the question (what is X, how does it work)
- **L2 MOFU** - comparison, alternatives, pricing context
- **L3 BOFU** - the commercial users-list / demo page

A healthy entity has all three. Most B2B sites have only L3, which is why commercial pages
convert poorly: a buyer cannot find the L1 page that would convince them.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `cannot resolve <domain>` | Typo, or the domain does not exist. | Check the domain. Pass the full URL if unsure. |
| `crawl found only N pages` | robots.txt blocks everything, no sitemap, or a client-side app with no static HTML. | Confirm the site has crawlable HTML. Raise `--cap` if it was a cap issue. |
| `Crawl was capped` finding appears | Fewer pages fetched than the sitemap lists. | Re-run with a higher `--cap`. The report says so itself; the figures are honest about coverage. |
| `entities: 0` | The bundle was built without page text. | Re-run the crawl; the pipeline now fails loudly on this rather than degrading quietly. |
| `REPORT FAILED VERIFICATION` | A DOM or visual check failed. | Read the failing line. It names the tile, label or contrast value. Fix and rebuild. |

---

## Rebuilding from saved data

A crawl is the slow part (minutes to tens of minutes). Once you have
`bundle-<domain>.json`, the analysis and report are fast:

```bash
python3 -B plan.py   bundle-<domain>.json
python3 report.py bundle-<domain>.json bundle-<domain>-plan.json -o /tmp/out.html
python3 -B verify_report.py /tmp/out.html
```

Tweak a filter in `entities.py`, re-run `plan.py` and `report.py`, and you have a new
report in seconds without re-crawling.

---

## Before you send it to a client

1. Open the report and read the **Key Findings** cards. If a number looks wrong, check the
   crawl actually covered the site (`pages crawled` vs the sitemap count).
2. Confirm the entity list is names you recognise. If junk appears, it is a marketing-copy
   word that slipped through; add it to `VERB` in `entities.py`.
3. Run the tests if you changed any code:
   ```bash
   python3 -B test_units.py       # 44 checks on the logic
   python3 -B verify_report.py <report.html>   # 29 checks on the render
   ```

---

## Files

All code is in `scripts/`. Run commands from that directory.

| File | Role |
|---|---|
| `interlink_audit.py` | One-command entry point. Crawl, plan, report, verify. |
| `discover.py` | Finds every page: robots.txt, nested sitemaps, WordPress REST. |
| `pipeline.py` | Crawl and build the bundle. |
| `extract.py` | Pulls clean body text out of a page. |
| `classify.py` | Labels each page TOFU / MID / BOFU / HUB / THIN. |
| `entities.py` | Learns the site's entity taxonomy from its own pages. |
| `plan.py` | Scores every missing link, ranks the worklist. |
| `squarify.py` | Exact treemap geometry. |
| `report.py` + `report_template.html` | Renders the client report. |
| `verify_report.py` | 29 DOM assertions on the built report. |
| `test_units.py` | 44 unit tests on the logic. |

---

## What is verified

| Site | Pages | DOM checks | Visual |
|---|---|---|---|
| spanglobalservices.com | 3,218 | 29/29 | 0 fail @1440, 390 |
| www.apollo.io | 1,199 | 29/29 | 0 fail |
| www.activecampaign.com | 800 | 29/29 | 0 fail |
| deependhq.com | 35 | 26/26 | 0 fail |

`test_units.py` covers the failures that actually happened during development: a footer CTA
misclassifying every page as BOFU, a hidden checkbox truncating a 2,964-word page to 72
words, a bare `a` prefix in the article filter discarding Adobe and Amazon, and a
competitive-set cap that silently dropped 34 of 60 entities.

---

## Known limits

- A crawl over the cap reports partial coverage and says so in a finding card.
- Entity quality tracks copy quality. A site whose content is mostly adjectives will
  surface adjectives. Filter `VERB` in `entities.py` when that happens.
- Link suggestions are scored, not written. Every suggestion needs a human read to confirm
  the sentence still makes sense.
