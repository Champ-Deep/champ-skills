---
name: "visual-verify"
description: "Mandatory closing gate for anything visual. Renders the built output in a real browser, captures screenshots at multiple breakpoints and themes, runs a deterministic interface audit (contrast maths, tap targets, layout animation, accessible names, overflow, AI-slop tells), then requires the agent to LOOK at its own screenshots and critique them before reporting done. Use at the end of every frontend build, landing page, dashboard, artifact, one-pager, report, deck, or theme change. MANDATORY TRIGGER after frontend-design, ui-polish, landing-page, web-artifacts-builder, theme-factory, power-design, page-refresh, executive-one-pager, visual-report-builder, graphify, or any time HTML, a component, a chart, or a rendered document is produced. Also triggers on 'check my design', 'does this look right', 'screenshot it', 'audit the UI', 'is this accessible', 'test the responsive layout'."
---

# Visual Verify

Every design skill in circulation shares one defect: **it designs blind.** It writes rules into a file, the agent obeys them as prose, and nobody ever looks at the result. The rule "check contrast" gets read, agreed with, and never executed. The layout that collapses at 390px ships because nothing rendered it at 390px.

This skill closes that loop. It is not a rulebook. It is a **machine that renders, measures, and shows you the output**, and a protocol that forces you to actually look.

The order matters and is not negotiable:

```
build  →  audit (machines catch what eyes miss)
       →  screenshot (render at real breakpoints)
       →  LOOK (read the PNGs, judge them)
       →  fix
       →  re-run until clean
       →  only then report done
```

**A screenshot you did not open has verified nothing.** The single most common failure mode is running the script, seeing "captured 6 files", and reporting success. That is worse than not running it, because it manufactures false confidence.

---

## Setup

Both scripts need Playwright with Chromium. Check once per session:

```bash
python3 -c "import playwright" 2>/dev/null || pip install playwright --break-system-packages
python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.launch().close()" \
  2>/dev/null || playwright install chromium
```

In sandboxes where Chromium is preinstalled, it is already on the path and no download is needed. If a page must be served rather than opened as a file, start the static server as a background process in one call and run the audit or shoot script in a separate call: chaining `python3 -m http.server` and the Playwright script in one foreground command gets rejected as a long-lived process and runs neither. If a browser genuinely cannot be obtained, say so plainly, fall back to the manual checklist in `reference/critique-protocol.md`, and label the output **unverified**. Never silently skip the gate and imply it passed.

---

## Step 1: Audit — the machine pass

```bash
python3 scripts/audit.py <url-or-file> --width 1440
python3 scripts/audit.py <url-or-file> --width 390          # the one that actually breaks
python3 scripts/audit.py <url-or-file> --width 1440 --theme dark   # if dark mode ships
```

The audit runs the live page in Chromium and checks the **computed** styles, not the source. It catches:

| Class | What it measures |
|---|---|
| Contrast | Real text colour against its real composited background, including transparency stacking. Not the hex you intended, the pixel that renders. |
| Tap targets | Geometry of every interactive element. 44px floor on mobile, 24px on pointer. Inline prose links exempt. |
| Accessible names | Icon-only buttons, unlabelled inputs, missing alt, placeholder standing in for a label. |
| Motion | Transitions on layout properties, `transition: all`, animation with no `prefers-reduced-motion` branch. |
| Layout integrity | Horizontal overflow with the culprit element named, flex children that cannot truncate. |
| Semantics | Missing title, missing or duplicated h1, skipped heading levels, blocked pinch zoom. |
| Slop tells | Coloured side-stripe borders, gradient-clipped text, static glass, emoji in chrome, default fonts, three identical cards, leftover placeholder content, over-long measure. |

Severities: **FAIL** blocks delivery. **WARN** needs a reason to ignore. **INFO** is a nudge. The script exits 1 on any FAIL so it can gate a build.

**A cluster of ~1:1 contrast FAILs is the checker, not your design.** Chrome returns `color(srgb r g b / a)` for every `color-mix(...)` result, with 0-to-1 channels, and a `[\d.]+` regex reads those channels as 0-to-255, so every translucent colour in the page audits as near black at once: nav bars, text on dark bands and translucent backgrounds all FAIL at 1.0 to 2.8:1 together. `scripts/audit.py` scales `color(` channels by 255; if you run a vendored or plugin copy of the script, carry that fix. Prove the gate before you distort the palette.

**Transparent chrome over content audits against the wrong ground, too.** A fixed nav that is clear at the top of the page, or any element sitting on a gradient band, gets composited against the body colour instead of what actually renders behind it, so it FAILs at ratios like 1.1, 1.7 and 2.4 while the page is fine. Before touching the palette, compute the ratio by hand: the element's text colour against the ground colour it actually sits on (the hero's own colour, not the body). Real luminance maths in about ten lines of Python settles whether the FAIL is the checker or the page. If it passes by hand, do not desaturate the design; change the element's ground to something a machine can composite (a solid `background-color` under the gradient, an opaque scrolled state) or record it as a known checker limitation in the report, naming the measured ratios. Report FAILs you leave standing as measured passes, never as ignored.

A clean audit is **necessary, not sufficient.** It cannot tell you the page is ugly, the hierarchy is flat, or the hero says nothing. That is Step 3.

---

## Step 2: Shoot — render at real sizes

```bash
python3 scripts/shoot.py <url-or-file> --out .verify --widths 390,834,1440 --themes light,dark
```

Captures above-the-fold and full-page at each width and theme, at 2x scale, with mobile emulation and touch below 700px. It waits for fonts and network idle, and reports any console errors, which are defects regardless of how the page looks.

Useful flags:

- `--reduced-motion` also captures the `prefers-reduced-motion: reduce` variant. Use it whenever the expressive tier is in play: the reduced version is what most conservative users actually see, and it is usually the one nobody checked. Treat it as a separate implementation surface, not a frozen default: a control hidden until an interaction (an email row that appears after file choose) still fires its native form submit in that state, so state-only bugs such as a field value leaking into a URL query live here and nowhere else. Screenshot it and probe its flows, not just the animated default.
- `--selector "[data-loaded]"` waits for a real readiness signal instead of guessing at a timeout.
- `--wait 2000` for pages with slow entrance choreography.
- `scripts/offline-check.py <target>` proves a local-only claim: it runs the page with the browser offline and exits 1 on any external request, console error or storage write. Run it on every artifact that promises no CDN, no remote fonts and no telemetry, and on anything delivered as a single file that must open from disk.

For a non-web deliverable (PDF, PPTX, DOCX, poster, chart image), you still shoot it: convert a page to PNG and read that. Rendering a slide to an image and looking at it catches overflowing text boxes and clipped charts that no amount of reading the source will.

```bash
pdftoppm -png -r 110 deck.pdf .verify/page      # PDFs
soffice --headless --convert-to pdf deck.pptx   # decks, then pdftoppm
```

---

## Step 3: Look — the part that gets skipped

**Read every PNG with the Read tool.** You have vision. Use it. Then critique against the protocol.

A set too large to open yourself still has to be opened. Past about eight PNGs the look pass outgrows one context, so fan it out: parallel vision subagents, one per batch of up to eight shots, each returning defects as shot / element / observation / fix / severity plus its swap and accessory test, then you merge the findings and fix. The fold shots stay yours: a subagent's summary of a screenshot is not a screenshot.

**One tall full-page capture is not readable either.** At 2x a 6000px page comes back as a thumbnail in which a misaligned divider and a clipped caption are both invisible, and the vision model will report the section that happens to be centred while missing the one at the seam. Slice the full-page shot into bands and judge each separately, naming which section it covers so every defect stays addressable:

```bash
python3 -c "
from PIL import Image
im = Image.open('.verify/full-1440.png'); W, H = im.size
for i, y in enumerate(range(0, H, 1500)):
    im.crop((0, y, W, min(H, y + 1500))).save(f'.verify/band-{i}.png')"
```

Nine bands for a landing page is normal and still cheaper than a subagent. Keep the 390px band count separate from the 1440px one: the defect list differs, because the layouts differ.

→ Full procedure in [critique-protocol.md](reference/critique-protocol.md).

The short form, in the order that finds the most problems fastest:

1. **Squint test.** Blur your reading of it. Does one thing dominate? If three elements compete equally for attention, the hierarchy has failed and no amount of colour tuning fixes it.
2. **The five-second test.** Looking only at the fold: what is this, who is it for, what do I do next. If any of the three is unanswerable, the content failed, not the design.
3. **Name the defect, do not rate the vibe.** "The spacing feels off" is useless. "The gap above the h2 is the same as the gap below it, so the heading reads as belonging to the section above" is actionable. Every critique line must name an element and a specific change.
4. **Compare the breakpoints side by side.** The 390 shot and the 1440 shot should look like the same product making different decisions, not a desktop page squeezed. Look specifically for: text that stayed 48px, a grid that became one sad column of stretched cards, a nav that turned into a wall.
5. **The swap test.** Could this screenshot be dropped onto a competitor's site with only the logo changed and nobody would notice? If yes, there is no design here, only competence.
6. **Count the accessories.** Gradient, glow, glass, badge, icon tile, animated border, decorative blur. Pick the least load-bearing one and remove it. The professional version of almost every AI-built screen is a calmer one.

Write the critique down as a numbered list of defects before you fix anything. Fixing while looking produces one fix and three missed problems.

---

## Step 4: Fix and re-run

Apply the fixes, then run Steps 1 and 2 again. Two rounds is normal. If round three still has FAILs, the problem is structural: stop patching and reconsider the layout or the design system.

**Measure before you fix.** A clipping, overflow, or animation-state claim read off a screenshot is a hypothesis, not a finding: a full-page shot captures scrollable panels in whatever scroll state they happened to be in, and a vision read will happily report a border that does not exist. Confirm with a DOM probe first, `getBoundingClientRect()` of the control against its scroll container plus `scrollHeight` vs `clientHeight`. For scrubbed or pinned sections, settle the scroll (`window.scrollTo`, wait for the scrub to catch up; `mouse.wheel` mid-flight lags), then read computed styles: the progress custom property, headline opacity, scene opacity. A screenshot blamed for "the transition never ran" at a mid-scrub frame is the frame, not the code; probe the numbers before spending a fix round. If the probe matches intent, the layout is fine and the screenshot misled you. Fixing on the screenshot's word spends a whole round on a defect that was never there.

**`document.scrollWidth` does not prove there is no overflow.** A root with `overflow-x: hidden` (or an ancestor clip) reports `scrollWidth === innerWidth` while children are twice the viewport wide and half of them are invisibly cut off. Measure geometry instead: walk `getBoundingClientRect().right > innerWidth + 1` over the page's elements, excluding nodes that scroll by design (table wrappers, the sidebar rail, canvases). The two probes disagree, and the rect walk is the one telling the truth.

**A grid track sized `1fr` cannot overflow; it expands.** `1fr` computes to `minmax(auto, 1fr)`, so a column's min-content floor lets it grow past the viewport while every descendant reports a tidy bounding box. Declare `minmax(0, 1fr)` on the track and `min-width: 0` on the child that must be allowed to shrink (the `main` inside a shell), and re-measure. Fixing a root `overflow` property instead just hides the defect and leaves the clipped content unreachable.

**Give every wide data table its own scroll box.** A table wider than the screen must scroll inside `overflow-x: auto` on its own wrapper. Without one it either forces the page to scroll horizontally or gets cut off by the root clip, and the audit will name the root as the culprit rather than the table.

**Animated label spans get shrunk out of their own text.** A button whose label animates through `grid-template-columns: 0fr/1fr` sits in a flex row, and the flex item's base size collapses to zero, so the label clips to a fragment ("Book a") at narrow widths while the button still measures fine. Give the button `white-space: nowrap` and the label span `min-width: max-content`, then re-shoot: the truncation only shows at 390 and only after the animation rule exists.

**A tap target is measured on the link, not the image inside it.** A nav logo rendered 44px tall still audits as an undersized target when its `<a>` wraps tightly at 34px. Set the height on the anchor (`display: flex; align-items: center; min-height: 44px`) rather than only on the `<img>`, because the anchor is what the geometry check measures.

**Two sticky bars anchored to the same `top` overlap on narrow screens.** Offset each one by the height of the bar above it in the mobile media query (`top: 60px` for the second bar under a 60px nav) or the lower bar sits underneath the upper one and its controls are unreachable.

**A canvas or WebGL page needs a second proof.** The audit inspects the DOM and sees none of the pixels, so a blank canvas audits clean. For any stateful scene: expose a read-only state hook (`window.<name>.getState()`), drive each state in Playwright, assert the state actually changed, and byte-compare one capture per state so "all five views render distinctly" is a measured claim instead of a look. Set `--selector "[data-loaded]"` only after the scene is really built, never at script start.

**Report honestly.** State what was verified and at what sizes:

> Verified at 390 / 834 / 1440, light and dark. Audit clean apart from one INFO on measure in the footer. Two rounds of critique: fixed hierarchy in the hero (headline was competing with the eyebrow) and the card grid collapsing to stretched full-width blocks on mobile.

Never write "verified" if you did not open the images.

---

## The gate

Delivery is blocked until all of these are true:

- [ ] `audit.py` run at a mobile width and a desktop width, zero FAILs, every WARN either fixed or justified in one line
- [ ] `shoot.py` run and **every PNG opened with the Read tool**
- [ ] A written critique exists, naming specific elements, not adjectives
- [ ] Fixes applied and the audit re-run clean
- [ ] Dark mode checked if it ships, reduced-motion checked if anything animates
- [ ] Console is free of errors
- [ ] Overflow checked by element rect against the viewport, not by `document.scrollWidth` (a clipped root lies), and a console-driven check of any interactive control the page ships
- [ ] Local-only or self-contained claims proved with `scripts/offline-check.py`, browser offline: zero external requests, zero storage writes
- [ ] The swap test passes: this could not be any other brand's page

If a browser is unavailable, every unchecked line above appears in the handoff as an explicit **unverified** list. An honest gap beats a fabricated pass.

---

## Working with the other skills

| Skill | How this fits |
|---|---|
| `frontend-design` | Runs as Step 5, after the polish pass. The DESIGN.md is the spec the critique judges against. |
| `ui-polish` | Run `audit.py` first, before the manual polish pass. It writes half the punch list for you. |
| `landing-page` | The five-second test and the swap test are the whole point. Run at 390 first, because that is where the traffic is. |
| `web-artifacts-builder`, `power-design`, `theme-factory`, `page-refresh` | Same gate, same scripts. |
| `executive-one-pager`, `visual-report-builder`, `graphify` | Convert to PNG and read it. Overflowing text boxes and clipped axis labels are invisible in source. |
| `microsite-refresh` | The plugin's site-refresh pipeline ends at this gate. Run these scripts and this critique as the closing step of every refresh. |
| `showcase-page` | Run the interaction test recipe from `frontend-design/reference/interior-rules.md` in Step 3 for any page with a copy button, filter pills or a section rail: the slider geometry, the failure path and the reduced-motion variant are console probes, not screenshots. |

Sources this synthesises: the [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) for the machine-checkable rule set, [Impeccable](https://github.com/pbakaus/impeccable) for the anti-pattern catalogue, and [taste-skill](https://github.com/Leonxlnx/taste-skill) for the pre-flight discipline. The contribution here is that these are executed rather than recited.
