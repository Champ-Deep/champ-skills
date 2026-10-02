---
name: internal-link-audit
description: Use when auditing a site's internal links or sitemap.
version: 1.0.0
license: AGPL-3.0
author: Deep
metadata:
  hermes:
    tags: [seo, internal-linking, crawl, sitemap, wordpress, graph, scoring]
    related_skills: [site-growth-audit, seo-toolkit, defensible-data-counts, visual-verify]
---

# Internal link audit

## When to use

The ask is some form of: crawl this site, find every link, tell me what should be
interlinked to what, score the low-hanging fruit. A pasted `sitemap_index.xml` plus
a request to "use something like a graph tool" is this skill. Also use it when someone
believes a page is under-linked and wants evidence, or asks which of their pages are
orphans.

The deliverable is a **ranked, grouped action list plus one visual**, not a link count.

## The three findings that reorder the whole job

Run these before proposing anything. Each one has inverted a plan in practice.

### 1. The sitemap is a claim about the site, not an inventory of it

Sitemaps go stale silently, and the drift is usually in the direction that matters:
live pages the sitemap never published. On WordPress, enumerate the real inventory from
the REST API and diff it against the sitemap.

```bash
# every post type the site actually has
curl -s https://<site>/wp-json/wp/v2/types | python3 -c "import json,sys; \
  [print(f\"{k:24s} rest={v.get('rest_base')}\") for k,v in json.load(sys.stdin).items()]"

# authoritative count per type; the header beats the body
curl -sI "https://<site>/wp-json/wp/v2/pages?per_page=1" | grep -i x-wp-total
```

Then check where the sitemap URLs actually land:

```bash
curl -sSL -o /dev/null -w "%{http_code} %{url_effective}\n" "<a-sitemap-url>"
```

A `301` into a namespace that appears nowhere in the sitemap means the sitemap is
publishing a fraction of the site, and the fraction it omits is usually the part with
the commercial pages. **Report the sitemap count and the live count side by side, and
say which one the analysis is built on.** An audit built only on the sitemap misses the
pages that were never published.

`references/live-inventory-recipe.md` has the enumeration, pagination and diff recipe.

### 2. Raw internal link counts are mostly template, and reporting them is a false claim

A shared mega-menu and footer is an internal link on every page. Counting them makes a
site with no editorial linking look heavily interlinked. Destinations present on more
than about half the pages are chrome, not signal.

```python
dest = Counter(b for a, b in contextual_edges)
boiler = {d for d, n in dest.items() if n >= 0.55 * len(pages_with_outlinks)}
contextual = [(a, b) for a, b in all_edges if b not in boiler]
```

On one 3,163-page audit this took 296,203 raw edges down to 25,695 real ones. The
"296k internal links" number is not a finding; the 25,695 is. Also report how many
pages have **zero** contextual outlinks, since that is the number a reader can act on.

Two related traps: a page with no links at all never appears as a *source* in an edge
list, so any "X of Y pages have no links" computed from the edge list silently drops
them. And a term-to-page match on body text is a candidate, not a link: verify the
destination is a real live page before scoring it.

### 3. The hubs usually already exist

Before recommending that pages be created for a named entity, technology, vertical or
geography, check whether the site already has a page for it. On a B2B data site the
FAQ or technology post types were 624 sitemap entries pointing at pages that 301-redirect
to a 515-page technology namespace the sitemap never published, clustered into 220
taxonomy categories. Every one of those was an unlinked existing page, not a gap.

```bash
# category names double as a free entity dictionary
curl -s "https://<site>/wp-json/wp/v2/categories?per_page=100&page=1&_fields=id,name,slug,count"
```

Categories, tags, and menu items are the site's own statement of what its entities are.
Use them as the term list to scan page bodies for rather than inventing one.

## Finding the opportunities

With inventory and boilerplate settled:

1. **Derive the term list from the site's own categories**, not from your own head.
2. **Scan every page body for those terms** and diff against what the page already
   links to. A named entity whose page exists but is unlinked is the cheapest win in
   SEO and the easiest to batch.
3. **Group by source page, not by target.** One page needing 19 links is one editing
   pass; 19 pages needing one link each is 19 passes. Grouping is what turns a list into
   a work queue.
4. **Read siblings for the second rule.** If a page is about one CRM, the other CRMs the
   site already covers belong on it. When pages-per-entity is small (roughly 2 to 3),
   the sibling set is small enough to hard-code per category rather than generate.

To scale the scan, use C-speed substring matching on whitespace-padded text rather than
one regex per term. Per-term regexes across thousands of pages times out; padded
`in` tests finish in seconds.

## Score with a rule engine, then let a model sharpen it

Ship a deterministic scorer that runs with no API key. Every number then carries a
written rationale, the output survives a model outage, and a bad judgement is visible
afterwards instead of baked in. A model pass can rerank what the rules already produced;
it should not be the thing that decides whether a number exists.

A weighting that held up: source-page commercial weight, target-entity specificity,
existing inbound equity, target page type, minus a peer penalty when source and target
share a category, minus an edit-effort factor. Clipped to 0 to 1. Named products score
high, broad job titles and generic geographies score deliberately low, because they are
real matches that make weak link targets. Grade into buckets rather than quoting a
magnitude; report the bucket counts and the threshold.

When a scoring API is unavailable, build the rule layer, ship it, and say plainly in the
deliverable which layer is missing. Do not stall the whole audit on it.

## Deliver

One self-contained HTML file, delivered as `MEDIA:`. It needs:

- A KPI row that puts **sitemap count next to live count**, and **raw edges next to
  contextual edges**. Those two pairs are the argument.
- The finding prose, leading with whatever inverts the plan.
- A ranked action table grouped by source page, each row scoring its own link.
- Orphan pages that exist and receive zero inbound links: the cheapest possible win,
  one link each.
- A method section stating the sources, the weights, and every unverified caveat,
  including any scoring layer that could not run.

## Pitfalls

- **Do not report a raw internal link count as a strength.** Strip the template first or
  the number describes one template, not editorial linking.
- **Do not build the whole audit on the sitemap.** It under-reports, usually omitting
  the commercially important pages, and the omission is invisible unless you diff it
  against a live inventory.
- **Do not compute a coverage ratio from an edge list.** Pages with zero links are not
  edge sources, so they vanish from the denominator. Recompute over the full page set
  and state the denominator you used.
- **Do not let a term match become a link recommendation without checking the target
  page is live.** A phrase that matches a category name can resolve to nothing.
- **Do not quote one number twice with two denominators.** If a figure moves, say so
  explicitly in the deliverable and keep the corrected value; silently shipping the
  second number leaves the reader with no way to know it moved.
- **The target may change under you mid-audit.** If a live app or a repo you are auditing
  is also being edited by another agent or a second session, check the file mtime and
  `git status` before writing, and re-verify a defect immediately before reporting it as
  still open. Someone else may have already fixed the thing you were about to patch.
- **Do not re-read a config file inside a large loop.** Loading JSON per iteration over
  hundreds of thousands of edges turns a fast script into a timeout. Hoist the load.
- **Look at the rendered output before reporting it done.** Reading the source, or seeing
  a clean audit, does not mean it looks right. This class of deliverable has failed on
  labels colliding with their own captions, and only opening the image caught it.
