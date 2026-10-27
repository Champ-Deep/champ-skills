---
name: markdown-doc-sites
description: "Use when converting markdown docs into shareable HTML pages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docs, pandoc, html, export, verification]
    related_skills: [visual-verify, span-brand-guidelines]
---

# Markdown docs to shareable HTML

## When to Use

- Deep asks to turn docs, briefs, guides or scripts into HTML he can share or present.
- Regenerating or repairing an existing `docs/html/` build (Pandoc, shared nav and CSS).
- A markdown deliverable must be clickable, on-brand and readable on a phone.

Not for designing a new interface (that is `frontend-design`) or building a visual report from scratch (that is `visual-report-builder`).

Deep hands over markdown (a briefing, an intern guide, a session script, a reference note) and asks for HTML he can share and click through while he talks. The markdown stays the source of truth; HTML is generated from it, never edited by hand, so the next content change is one rebuild.

## Procedure

1. **Confirm the source of truth.** One markdown file per page. If the content only exists in chat, write it to a `.md` first, then build. Hand-editing generated HTML is the failure mode: the next markdown edit silently loses it.
2. **Write one `build.sh` that renders every page**, so regeneration is a single command:
   ```bash
   pandoc "$src" -f gfm -t html5 --standalone \
     --metadata pagetitle="$title" \
     --include-before-body=nav.html -c span.css -o "$out"
   ```
   Take the title from the doc's own H1 or pass it as an argument. Use one shared stylesheet and one shared nav include so all pages look identical and a nav change is one edit.
3. **Style with brand tokens, not ad-hoc colours.** Load the relevant `*-brand-guidelines` skill for palette and type, then map them to CSS custom properties at the top of the stylesheet. Everything else reads the variables, so a colour correction is one line.
4. **Build the mobile rules into the stylesheet from the start** (see Pitfalls): scrollable tables, wrapping long strings, an active-page nav state.
5. **Run the verification gate before reporting done** (see below). Fix, rebuild, re-run until it is clean.
6. **Commit the generated HTML together with the sources** when the pages are meant to be shared as files, so a recipient who clones gets them without running the build.
7. **Deliver as `MEDIA:/abs/path/file.html` cards**, one per page, named so he knows which is which. Say which page is the one to open first.

## Verification gate (load-bearing, never skip)

A page that renders for you can still be broken for the reader on a phone. Check every generated page, at both widths, in a real browser:

```python
# for each page, at width 390 and 1440:
#   goto file:// URL, wait, then:
#   document.documentElement.scrollWidth > document.documentElement.clientWidth  # must be False
#   console errors                                                     # must be empty
#   assert page has exactly one <h1
#   screenshot at 1440 for the visual read
```

Then **look at the screenshots** and check contrast, table styling and nav legibility before you claim it works. Report the per-page result, not a single overall pass.

## Pitfalls

- **Pass the title as `pagetitle`, never `title`.** Pandoc's `--metadata title=` emits its own H1 title-block on top of the source's own heading, so every page ships two H1s. `pagetitle` sets only the browser `<title>`. Assert exactly one `<h1` per page, because the duplicate is invisible in a desktop screenshot and shows up as a repeated heading.
- **Give tables `display:block; overflow-x:auto` in the shared CSS.** Pandoc emits bare `<table>` with no wrapping, so a wide table widens the whole document and the phone view scrolls sideways with no way to reach the right-hand columns. Scoping it to the table keeps the page width fixed and the table scrollable on its own.
- **Set `overflow-wrap:anywhere` on paragraphs and list items.** A long URL or path in a bullet has no break opportunity, and one of them is enough to push `documentElement.scrollWidth` past the viewport. Wrapping it inside the line is cheaper than hunting the offender after the fact.
- **Wire the nav's active state.** A shared nav include renders the same markup on every page, so without a per-page active class the reader cannot tell which page they are on. Set it from the page name in `build.sh`.
- **Never invent a success the gate did not produce.** If a page overflowed and you ran out of attempts, name the page and what remains rather than summarising the set as verified.
