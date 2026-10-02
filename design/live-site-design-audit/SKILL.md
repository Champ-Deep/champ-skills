---
name: live-site-design-audit
description: "Use when auditing or redesigning a live website."
---

# Live Site Design Audit

Take a live web property from "it feels flat" to a verified, opinionated redesign.

Triggers: "audit my site", "my homepage looks plain", "add scroll animations", "make
this less boring", "redesign the hero", "this feels stale", "review Dribbble", "apply
the taste scale", "give me a fresh design for", "this feels lackluster", "add motion to
the landing page".

Three deliverables, in this order: **what is actually being served**, **a working
concept file**, **a written audit note**. Never a slide of suggestions.

## 1. Establish what is served before designing anything

The single most common finding in this class of work: the redesign already exists in
the repo and is not deployed. Do not open a design tool until you have answered this.

```bash
# 1a. what does the live URL actually return
curl -sI <live-url> | head -20
curl -s <live-url> | grep -oE '<script[^>]*src="[^"]*"' | head -20   # framework fingerprints

# 1b. what implementations exist in the repo, side by side
ls -la <site-dir>/                      # legacy static kit?
ls -la <site-dir>/*/package.json        # a newer app (Next/Vite/Astro)?
cat <site-dir>/*/package.json | grep -E '"(next|vite|astro|react)"'

# 1c. build the newer one and prove it works
cd <app> && npm run build               # must exit 0
```

A repo can hold a complete Next.js rewrite with all the motion already written while
production still serves a no-build static kit. Then the request is not a design task,
it is a deploy decision, and saying so is the highest-value thing you can deliver.

If a newer app exists: build it, serve it locally, screenshot both, and put them side
by side on measured numbers (see step 2). Report the delta as a table. Never assert
which to ship without the numbers.

## 2. Measure the incumbent, do not eyeball it

Run `scripts/page-audit.py` against the live URL and against the local candidate. It
returns paint timings, transferred bytes, canvas count, running animations, section
count, horizontal overflow, sub-44px tap targets, text nodes carrying opacity, em dash
count, and the reduced-motion state. Two widths minimum, 1440 and 390.

Rules for reading the numbers:

- **Running animations is the diagnostic for "it feels dead".** A page with thousands
  of pixels of scroll and zero running animations reads as a static document no matter
  how good the cards are. That single number usually explains the complaint.
- **`canvas: 0` plus `runningAnims: 0` means there is no visual instrument at all.**
  Not a weak one. None.
- Count `@keyframes`, `transition` rules, and `IntersectionObserver` / scroll listeners
  in the source. Zero scroll-linked motion across a long page is the cause, stated as
  fact rather than taste.
- Bytes and paint timings decide whether a heavier approach is even affordable. If the
  incumbent ships 530 KB of JS for a static page, the motion budget is already blown.

Then look at it. Screenshot every viewport height down the page, tile the frames into
one contact sheet, and read that single image. Tiling is not optional: nine separate
frames cost nine tool calls and you lose the rhythm judgement that only a contact sheet
gives you.

## 3. Name the real cause, not the surface complaint

"Very plain" and "lacks scrolling animations" are symptoms. Sort them into causes and
say which dominate:

| Cause | How to detect it |
|---|---|
| No scroll-linked motion | `runningAnims: 0`, no `IntersectionObserver`, no scroll listener |
| Card grammar everywhere | Every section is a bordered rectangle with text; only one section has a distinctive shape |
| Best real estate spent on the weakest content | Hero is stat tiles while the differentiating asset sits below the fold |
| Repetition | Two or more sections sharing a layout family |
| Dead data | Cards rendering "no entry" or "coming soon" where real content exists |

Rank by blast radius, not by count. Lead with the one that makes the page read as flat,
not the one with the most instances.

## 4. Set the taste dials out loud, and justify each

State the design read in one line (page kind, audience, language), then three dials
1 to 10 and why each got its number:

- `DESIGN_VARIANCE`: layout experimentation. Raise it for a redesign that is meant to
  break the incumbent's grid.
- `MOTION_INTENSITY`: animation depth. This is usually the dial the user actually
  asked about; do not bury it at 3 to be safe.
- `VISUAL_DENSITY`: information per viewport. Do not dilute an information-dense site
  to look "clean". Above 7, generic card containers are banned: data breathes in plain
  layout and 1px lines, and cards survive only where content is genuinely enumerable.

Two constraints that decide most motion work:

- **Marquee max one per page.** Two horizontal scrollers read as filler.
- **Every animation needs a one-sentence reason** (hierarchy, storytelling, feedback,
  state transition). "It looked cool" is not one. If you cannot articulate it, cut it.

High density and high motion can coexist. They are separate dials.

## 5. Pick a mechanic that could only belong to this site

Generic fade-up-on-scroll is available to every site on the internet. The concept has
to be impossible to paste onto a competitor.

The test: **what does this property have that nobody else does, and can motion be
driven by it?** A dated activity log, a live counter, a real dataset, a physical
process. Then make the scroll position *be* that asset rather than decorate around it.

Worked example worth copying: for a build-in-public site with hundreds of dated
entries, pin the hero and map scroll position to position in the log, so a giant day
number and the real entry text swap underneath as the visitor scrolls. The claim is
"one entry every weekday, gaps stay visible"; the interaction argues the thesis by
using it. That cannot be lifted by anyone else.

If the honest answer is that the site has no such asset, say so and design for its
strongest real content instead of inventing a gimmick.

## 6. Build the concept against real data

Self-contained single HTML file. No build step, no server, opens from `file://`.

- **Pull real data from the project's built artifact, not mock numbers.** Mock data in
  a concept reads as fake to anyone who knows the site, and it hides data-shape bugs.
- **Derive, never store, any count.** Stored totals drift and the site eventually
  renders "week 38 of 31".
- **No-JS is the base state.** Entrance animations are added by JS as an enhancement:
  the element is visible by default, JS adds the hidden starting state, then reveals on
  intersection. A visitor with JS off, or with `prefers-reduced-motion`, sees everything.
- Honour `prefers-reduced-motion` by collapsing to static, not by removing content.
  Verify: 0 running animations and 0 hidden elements under reduced motion.
- Stop canvas `requestAnimationFrame` loops when the tab is hidden.

## 7. Verify the mechanic actually moves

The most expensive silent bug in this class: scroll-driven code that reads correctly,
builds without error, and does nothing.

```bash
# drive real scroll positions and read the DOM back, do not trust the source
for frac in 0 0.25 0.5 0.75 1.0; do
  # scrollTo(stage.top + (stage.height - innerHeight) * frac), wait, read the value
done
```

Expect the driven value to change monotonically across the range. If it prints the same
value at every fraction, the range is computing to zero. See the pitfall below.

Re-verify after every layout change: sticky positioning, wrapper heights, and grid
changes all invalidate the geometry the mechanic was computed against.

## 8. Close the definition of done

Re-run `scripts/page-audit.py` at 1440 and 390 on the built concept. All of these must
hold before you report done:

- zero horizontal overflow at every width
- zero em dashes (and zero en dashes) in visible text
- zero sub-44px interactive targets, both axes
- zero text nodes carrying `opacity` below 1 (use a dimmer token instead)
- reduced motion: 0 running animations, 0 hidden elements
- zero console errors and zero page errors
- every mechanic exercised at 0, 25, 50, 75 and 100 percent of its range

Then deliver every file with a `MEDIA:` absolute path. Never a bare path.

## Pitfalls

- **A scroll track sized in `vh` equal to the viewport computes a zero scroll range.**
  `-r.top / (r.height - innerHeight)` divides by zero, progress pins at 0, and the
  feature never fires. The stage wrapper must be taller than the viewport, and the
  pinned child must actually be sticky. Looks perfect in source; does nothing in the
  browser. Only driving real scroll positions catches it.
- **Derived fields usually live in the built artifact, not the source.** Content
  authored as JSON often gets enrichment fields attached at build time. Reading the
  source file yields `undefined` for every row, and the fallback path renders something
  false, usually "no entry yet" on every card. Check which file actually holds the
  field before wiring a template to it.
- **Never put an async Playwright API inside a sync event listener.** `response.body()`
  is a coroutine; calling `len()` on it inside a `lambda` raises inside the event loop
  and cascades into unrelated calls failing with confusing errors. Get sizes from
  `performance.getEntriesByType('resource')` inside a single `page.evaluate` instead.
- **A single screenshot at one width proves nothing.** Breakpoints, sticky behaviour and
  scroll mechanics all hide at one viewport. Always 1440 plus 390.
- **`vision_analyze` sometimes returns a preamble instead of an answer.** If it echoes
  your question back rather than analysing the image, re-ask with a narrower, more
  concrete question. Do not treat the empty response as a finding, and do not skip the
  check.
- **Vision review finds real content bugs.** In one pass it caught every card in a grid
  rendering a placeholder because of the derived-field mistake above, and flagged a
  detached chip. Always read the contact sheet back critically before declaring done.
- **Do not invent an assessment for a name you cannot resolve.** If the user references
  a tool, vendor, or product that appears nowhere in the vault, the repos, or on the
  web, say you could not find it and ask what it is. Never fabricate a comparison.
- **Distinguish "this design is wrong" from "this migration never shipped".** Check the
  second before writing any of the first.
- **Say what the concept does not fix.** An audit that only lists wins is marketing. Name
  the known-broken items you left alone and why, and give the user the one decision that
  gates everything else.
- **A 44px tap target is about the hit area, not the visual.** A 2px rail bar needs a
  44x44 button wrapped around it. A short label like "Now" needs horizontal padding, not
  letter-spacing, and inline links inside a prose sentence cannot hold the target at all:
  turn the footer sentence into a real link list.

## Supporting files

- `scripts/page-audit.py` - deterministic Playwright probe: paint timings, bytes,
  canvas count, running animations, overflow, tap targets, opacity-on-text, em dash
  count, reduced-motion state, console and page errors. Run it against two or more URLs
  to produce the comparison table.
