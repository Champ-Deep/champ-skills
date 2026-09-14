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

In sandboxes where Chromium is preinstalled, it is already on the path and no download is needed. If a browser genuinely cannot be obtained, say so plainly, fall back to the manual checklist in `reference/critique-protocol.md`, and label the output **unverified**. Never silently skip the gate and imply it passed.

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

A clean audit is **necessary, not sufficient.** It cannot tell you the page is ugly, the hierarchy is flat, or the hero says nothing. That is Step 3.

---

## Step 2: Shoot — render at real sizes

```bash
python3 scripts/shoot.py <url-or-file> --out .verify --widths 390,834,1440 --themes light,dark
```

Captures above-the-fold and full-page at each width and theme, at 2x scale, with mobile emulation and touch below 700px. It waits for fonts and network idle, and reports any console errors, which are defects regardless of how the page looks.

Useful flags:

- `--reduced-motion` also captures the `prefers-reduced-motion: reduce` variant. Use it whenever the expressive tier is in play: the reduced version is what most conservative users actually see, and it is usually the one nobody checked.
- `--selector "[data-loaded]"` waits for a real readiness signal instead of guessing at a timeout.
- `--wait 2000` for pages with slow entrance choreography.

For a non-web deliverable (PDF, PPTX, DOCX, poster, chart image), you still shoot it: convert a page to PNG and read that. Rendering a slide to an image and looking at it catches overflowing text boxes and clipped charts that no amount of reading the source will.

```bash
pdftoppm -png -r 110 deck.pdf .verify/page      # PDFs
soffice --headless --convert-to pdf deck.pptx   # decks, then pdftoppm
```

---

## Step 3: Look — the part that gets skipped

**Read every PNG with the Read tool.** You have vision. Use it. Then critique against the protocol.

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

Sources this synthesises: the [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) for the machine-checkable rule set, [Impeccable](https://github.com/pbakaus/impeccable) for the anti-pattern catalogue, and [taste-skill](https://github.com/Leonxlnx/taste-skill) for the pre-flight discipline. The contribution here is that these are executed rather than recited.
