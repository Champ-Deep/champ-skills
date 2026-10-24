---
name: "visual-verify"
description: "Mandatory closing gate for anything visual. Renders the built output in a real browser, captures screenshots at multiple breakpoints and themes, runs a deterministic interface audit (contrast maths, tap targets, layout animation, accessible names, overflow, AI-slop tells), then requires the agent to LOOK at its own screenshots and critique them before reporting done. Use at the end of every frontend build, landing page, dashboard, artifact, one-pager, report, deck, or theme change. MANDATORY TRIGGER after frontend-design, ui-polish, landing-page, web-artifacts-builder, theme-factory, power-design, page-refresh, executive-one-pager, visual-report-builder, graphify, or any time HTML, a component, a chart, or a rendered document is produced. Also triggers on 'check my design', 'critique this page', 'review the UI', 'does this look right', 'screenshot it', 'audit the UI', 'is this accessible', 'test the responsive layout'."
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

Both scripts need Playwright with Chromium. The interpreter on `PATH` is often NOT the
one that has it, so probe first and pick the winner rather than installing blind:

```bash
for p in "$(command -v python3)" /opt/anaconda3/bin/python3 /opt/homebrew/bin/python3 \
         /usr/bin/python3 "$HOME"/.hermes/*/bin/python* "$HOME"/.hermes/*/*/bin/python*; do
  [ -x "$p" ] && "$p" -c "import playwright" 2>/dev/null && { echo "USE=$p"; break; }
done
```

Then check the browser against that same interpreter:

```bash
<the-winner> -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.launch().close()" \
  2>/dev/null || playwright install chromium
```

Only install into a fresh environment if no interpreter probes clean. Re-running an
install against the PATH python while a working one already exists elsewhere just
repeats the same failure with a different interpreter.

In sandboxes where Chromium is preinstalled, it is already on the path and no download is needed. When neither script's browser works, the one-shot fallback that still lets you LOOK is a headless Chrome screenshot fed to a vision call: `"<chrome>" --headless=new --disable-gpu --hide-scrollbars --window-size=1200,<full height> --virtual-time-budget=10000 --screenshot=out.png <file>` then `vision_analyze` on the PNG. Keep `--virtual-time-budget` in that line: without it the shutter can fire before webfonts and images finish loading, and the look pass then judges fallback typefaces and empty boxes instead of the build. Size the window tall enough to cover the whole page, or say plainly which sections the shot did not reach: a partial screenshot reported as a full check is the same false pass the gate exists to prevent. If a page must be served rather than opened as a file, start the static server as a background process in one call and run the audit or shoot script in a separate call: chaining `python3 -m http.server` and the Playwright script in one foreground command gets rejected as a long-lived process and runs neither. If a browser genuinely cannot be obtained, say so plainly, fall back to the manual checklist in `reference/critique-protocol.md`, and label the output **unverified**. Never silently skip the gate and imply it passed.

---

## Step 0: the dash count, before anything renders

Any generated HTML or vault write for Deep carries a hard zero em dash and en dash rule. Visual inspection cannot settle it (a dash inside a headline still looks fine), and it is a one-line machine check, so run it before the browser:

```bash
grep -c $'\xe2\x80[\x93\x94]' file.html   # literal UTF-8 dashes, must print 0
grep -c '—\|–' file.html       # numeric/named entities, must print 0
```

The byte pattern only catches raw UTF-8 dashes, and generated markup routinely emits the entity form (`—`) instead, which that grep counts as zero while the dash still renders on screen. Check both forms, fix every hit, then proceed. On a non-UTF-8 locale `grep` can abort on the very bytes you are counting with `illegal byte sequence` and print nothing or an error instead of `0`, so pin the locale for the run (`LC_ALL=C.UTF-8 grep -c $'\xe2\x80[\x93\x94]' file.html`) or count in Python (`text.count('—') + text.count('–') == 0`), and treat an errored grep as unverified rather than as a zero. When a page ships through a build script, put this check in the script so the count gates the build rather than the review.

## Step 0.5: did the requested change actually land?

A user reviewing your output can see at once that none of their requested changes
appeared, which means the report and the disk disagreed. Before reporting any edit
as done, grep the file on disk for the new value (a token name, the new class, the
string that must now be absent) and paste that hit. A tool call that returned
success is not proof the bytes are there, and a build that passes proves only
that the old code still compiles. For a change made in several places (a
replaced logo, a renamed section), grep the whole tree and show the count, not
one hit.

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
| Tap targets | Geometry of every interactive element. 44px floor on mobile, 24px on pointer. The prose-link exemption is not reliable: skip links, footer links and mono-styled inline links still FAIL at 390, so size the anchor itself (`display:flex; align-items:center; min-height:44px; min-width:44px`) rather than trusting the exemption. |
| Accessible names | Icon-only buttons, unlabelled inputs, missing alt, placeholder standing in for a label. |
| Motion | Transitions on layout properties, `transition: all`, animation with no `prefers-reduced-motion` branch. |
| Layout integrity | Horizontal overflow with the culprit element named, flex children that cannot truncate. |
| Semantics | Missing title, missing or duplicated h1, skipped heading levels, blocked pinch zoom. |
| Slop tells | Coloured side-stripe borders, gradient-clipped text, static glass, emoji in chrome, default fonts, three identical cards, leftover placeholder content, over-long measure. |

Severities: **FAIL** blocks delivery. **WARN** needs a reason to ignore. **INFO** is a nudge. The script exits 1 on any FAIL so it can gate a build.

**A cluster of ~1:1 contrast FAILs is the checker, not your design.** Chrome returns `color(srgb r g b / a)` for every `color-mix(...)` result, with 0-to-1 channels, and a `[\d.]+` regex reads those channels as 0-to-255, so every translucent colour in the page audits as near black at once: nav bars, text on dark bands and translucent backgrounds all FAIL at 1.0 to 2.8:1 together. `scripts/audit.py` scales `color(` channels by 255; if you run a vendored or plugin copy of the script, carry that fix. Prove the gate before you distort the palette.

**Chart text in the failure zone gets its ink from one computed value, not from a
step index.** A sequential palette assigns text by ramp position ("step 3 and above
use light ink"), and the same index resolves differently per theme: if dark theme's
step 3 sits near mid-luminance while light theme's step 3 is a pale tone, one rule
puts near-black on near-black in one theme and white on green in the other, at
ratios like 3.2:1 and 3.8:1. Never pick tile ink by index. Pick it by measuring:
compute the luminance of every palette step in every theme against both candidate
inks (ten lines of Python), keep whichever clears 4.5:1 for each step/theme cell,
and store the answer as one variable per step per theme (`--sink0..N` beside the
`--s0..N` swatches) so components reference `var(--sink${k})` instead of encoding
the threshold. Report the resulting ratio matrix with the fix. Two cells may land
below 4.5 if no ink clears them: either darken that palette step or drop the label
size to large-text, and say which.

**A `border-radius` probe on a visible leaf can be a measurement artifact, not a defect.** A repeated "not fully rounded" FAIL at 1.00:1-style ratios on pills and cards usually comes from sampling the antialiased corner of a rounded element against a background it does not own (a gradient band, a card edge). Settle it the same way as the contrast cluster: run the identical audit on a known-good reference page built on the same system, and if it fails the same checks, read the screenshot for the real verdict and record the checker limitation instead of squaring off the design.

**Re-run the vision pass after the fix and read what it says.** A critique run through an auxiliary vision call is only trusted when the same question, asked again on the fixed build, comes back with the named defects gone. If the second pass reports a new break (a diagram clipped at the right edge, a label cut off), treat it as a fresh hypothesis: confirm against a geometry probe (`scrollWidth` of the container, `getBoundingClientRect().right`) and, where the claim is about a component in isolation, shoot that element (`locator(selector).screenshot()`) rather than the full-page crop.

**A vision pass states colours, asset identities and geometry as fact and is often
wrong. Probe its factual claims, not just its geometric ones.** An art-directed
read of a panel will assert "white text on the orange background, low contrast"
on a panel that ships ink text, name the wrong logo, or report an overlap that
rect coordinates show is clear. Probe them instead of re-reading the frame: colour claims against `getComputedStyle`, asset claims against the element's `src`, and overlap, clipping and alignment claims against bounding boxes (`getBoundingClientRect().right > innerWidth + 1`, `scrollHeight` vs `clientHeight`, both columns' `top`). Ask the next pass about the region the element actually lives in rather than re-reading the same crop; the crop's own edge is the usual culprit when a vision claim names a clipped or missing element.
Keep only what the probe confirms, and name the disproved claims in the
report. Geometric claims from a downsampled full-page capture are the weak case;
a colour or identity claim is weaker still, because the model reads the design
expectation, not the pixel. Treating the critique as fact spends a fix round on a
defect that was never there.

**A composite of image assets gets a fabricated punch list, and the single asset is
the only probe.** When the deliverable is a set of exported PNGs (a profile grid, a
contact sheet, an ad tile set) there is no DOM to measure, so an open "critique this
as an art director" prompt run over the composite invents per-asset defects: overlay
text reported illegible on every tile when each tile read alone is legible, subjects
reported cropped out of frames that contain them, artefacts blamed on photos the
prompt never resolved. Treat that critique as a hypothesis list and settle each claim
by opening the one asset at full size and asking a narrow literal question: what text
is present exactly, what sits directly behind it, does the frame cut anything. Keep
only what the per-asset read confirms, report which claims it disproved, and open
every type tile plus a sample of the photo tiles rather than judging the set from the
grid shot. A literal question is answerable from pixels; an evaluative one invites
the model to supply the answer.

**Transparent chrome over content audits against the wrong ground, too.** A fixed nav that is clear at the top of the page, or any element sitting on a gradient band, gets composited against the body colour instead of what actually renders behind it, so it FAILs at ratios like 1.1, 1.7 and 2.4 while the page is fine. Before touching the palette, compute the ratio by hand: the element's text colour against the ground colour it actually sits on (the hero's own colour, not the body). Real luminance maths in about ten lines of Python settles whether the FAIL is the checker or the page. If it passes by hand, do not desaturate the design; change the element's ground to something a machine can composite (a solid `background-color` under the gradient, an opaque scrolled state) or record it as a known checker limitation in the report, naming the measured ratios. Report FAILs you leave standing as measured passes, never as ignored.

**Prove which app is listening before you shoot it.** A dev server or other project can own loopback while your server owns the wildcard interface, so `localhost:<port>` renders a completely different app that passes every visual check with the wrong content. Run `lsof -nP -iTCP:<port> -sTCP:LISTEN`, then grep the fetched HTML for a string only your build contains, and drive the LAN address when loopback is contested. A green gate run against the wrong app is the one failure that produces no symptom at all.

**An isolated component shot must come from the page it ships on, not a test harness.** A
component preview routed through one query parameter hides whatever that param drives (the
price plan, the option set), so every card in a multi-card component shoots identically and
its card-specific fields audit as present when they were never rendered. Load the real
production route, drive the state (plan buttons, open accordion), and assert the state
signal: an accordion panel's `maxHeight` greater than zero, and visible plan name and price
drawn from a log the render wrote. A harness render is also where layout rules get tested in
isolation and pass while the page's grid stretches the same element into a different shape.

**For an async component, drive the flow and shoot each state separately.** An idle screenshot of a search box that morphs into a thinking orb proves nothing about the states that matter: the tools default to the load state, and a defect that exists only during the animation disappears the moment it finishes. Drive the real interaction (type, submit, wait for the async work), capture idle, mid-flight and settled states as separate PNGs, assert the state from a DOM signal (a phase attribute, an element mount) rather than a sleep, and check the console for errors each state produced. This is the multi-state requirement above applied to one component rather than a whole page.

**Disambiguate same-tag elements before scripting an interaction.** Once a page ships two `<canvas>` elements (a search orb and a globe) or several buttons sharing a class, a bare selector drives whichever one DOM order puts first, and the focus, keyboard or click test silently exercises the wrong element while reporting green. Select on a distinguishing attribute (`canvas[tabindex]`), and assert an observable consequence (caption text changed, route opened) rather than the focus move alone, since a page can hold focus somewhere other than the element you asked for.

**Re-run the audit in each state the flow can reach, not only the load state.** A default-page audit of a multi-step app measures only its empty state, and every control that renders after an interaction (a mapping select populated from the uploaded file, the remove chip that appears once a chip exists) is absent from the default DOM, so the audit reports clean while an undersized or unlabelled control sits one click away. Drive the flow to each state that ships controls (uploaded, configured, results, signed in) and run the audit plus a shoot at that state. States nobody screenshots are states nobody audits, and the interactive states are exactly where the touch-target and labelling FAILs hide.

**Prove an interactive component by driving the real interaction, then reading computed state, not pixels.** A screenshot of a slider, compare handle or hover-driven reveal at rest shows the default state and nothing else. Drive it (mouse coordinates from the element's own bounding box, `scrollIntoView` with instant scroll before the move, the range input's `value`, a tap on one side of a split), then read the state signal: the custom property (`--p`), the `clip-path` it drives, and the element under the pointer (`document.elementFromPoint` or the pane whose click handler fired). Two traps: a smooth-scroll still animating when the pointer moves leaves the pointer outside the element and `pointerleave` resets the state, so force `scrollBehavior = 'auto'` first; and a state asserted from a `locator` bounding box taken during the scroll has the same stale-coordinate problem. Probe `pointerdown` targets by click, not by proximity: a pane claiming the right half must actually receive the click that lands there.

A clean audit is **necessary, not sufficient.** It cannot tell you the page is ugly, the hierarchy is flat, or the hero says nothing. That is Step 3.

---

## Step 2: Shoot — render at real sizes

```bash
python3 scripts/shoot.py <url-or-file> --out .verify --widths 390,834,1440 --themes light,dark
```

Captures above-the-fold and full-page at each width and theme, at 2x scale, with mobile emulation and touch below 700px. It waits for fonts and network idle, and reports any console errors, which are defects regardless of how the page looks.

When your own capture script scrolls to each section before shooting, force instant scrolling first (`html{scroll-behavior:auto!important}` injected, or `scrollTo({top, behavior:'instant'})`) and pause before the shutter: a shot taken mid smooth-scroll lands wherever the animation happens to be, and the screenshot then gets blamed on the page for content it never framed.

Useful flags:

- `--reduced-motion` also captures the `prefers-reduced-motion: reduce` variant. Use it whenever the expressive tier is in play: the reduced version is what most conservative users actually see, and it is usually the one nobody checked. Treat it as a separate implementation surface, not a frozen default: a control hidden until an interaction (an email row that appears after file choose) still fires its native form submit in that state, so state-only bugs such as a field value leaking into a URL query live here and nowhere else. Screenshot it and probe its flows, not just the animated default.
- `--selector "[data-loaded]"` waits for a real readiness signal instead of guessing at a timeout.
- `--wait 2000` for pages with slow entrance choreography.
- `scripts/offline-check.py <target>` proves a local-only claim: it runs the page with the browser offline and exits 1 on any external request, console error or storage write. Pass a local file as `file:///abs/path`; a bare filesystem path is rejected as an invalid URL. Run it on every artifact that promises no CDN, no remote fonts and no telemetry, and on anything delivered as a single file that must open from disk.

For a non-web deliverable (PDF, PPTX, DOCX, poster, chart image), you still shoot it: convert a page to PNG and read that. Rendering a slide to an image and looking at it catches overflowing text boxes and clipped charts that no amount of reading the source will.

```bash
pdftoppm -png -r 110 deck.pdf .verify/page      # PDFs
soffice --headless --convert-to pdf deck.pptx   # decks, then pdftoppm
```

---

## Step 3: Look — the part that gets skipped

**Read every PNG with the Read tool.** You have vision. Use it. Then critique against the protocol.

When the look pass runs through an auxiliary vision call instead of your own eyes (a batch too large for one context, a non-vision model, a fan-out to subagents), the prompt decides the yield. Prime a role and a cap: *"Critique as an art director for <this product's category>. Name the three most damaging problems, each naming the element and the specific change, five sentences max."* An open-ended "describe this screen" returns an inventory of what is on the screen and no punch list. Then re-run the identical prompt after the fix round and check each named defect is gone: the same question twice turns the before/after into a mechanical comparison instead of a judgement call.

A set too large to open yourself still has to be opened. Past about eight PNGs the look pass outgrows one context, so fan it out: parallel vision subagents, one per batch of up to eight shots, each returning defects as shot / element / observation / fix / severity plus its swap and accessory test, then you merge the findings and fix. The fold shots stay yours: a subagent's summary of a screenshot is not a screenshot.

**One tall full-page capture is not readable either.** At 2x a 6000px page comes back as a thumbnail in which a misaligned divider and a clipped caption are both invisible, and the vision model will report the section that happens to be centred while missing the one at the seam. Slice the full-page shot into bands and judge each separately, naming which section it covers so every defect stays addressable:

```bash
python3 -c "
from PIL import Image
im = Image.open('.verify/full-1440.png'); W, H = im.size
for i, y in enumerate(range(0, H, 1500)):
    im.crop((0, y, W, min(H, y + 1500))).save(f'.verify/band-{i}.png')"
```

Nine bands for a landing page is normal and still cheaper than a subagent. Keep the 390px band count separate from the 1440px one: the defect list differs, because the layouts differ, so the two crops cover different sections and the section name in the prompt has to come from the crop's own y-range, not from the other width's list.

→ Full procedure in [critique-protocol.md](reference/critique-protocol.md).

The short form, in the order that finds the most problems fastest:

1. **Squint test.** Blur your reading of it. Does one thing dominate? If three elements compete equally for attention, the hierarchy has failed and no amount of colour tuning fixes it.
2. **The five-second test.** Looking only at the fold: what is this, who is it for, what do I do next. If any of the three is unanswerable, the content failed, not the design.
3. **Name the defect, do not rate the vibe.** "The spacing feels off" is useless. "The gap above the h2 is the same as the gap below it, so the heading reads as belonging to the section above" is actionable. Every critique line must name an element and a specific change.
4. **Compare the breakpoints side by side.** The 390 shot and the 1440 shot should look like the same product making different decisions, not a desktop page squeezed. Look specifically for: text that stayed 48px, a grid that became one sad column of stretched cards, a nav that turned into a wall.
5. **The swap test.** Could this screenshot be dropped onto a competitor's site with only the logo changed and nobody would notice? If yes, there is no design here, only competence.
6. **Count the accessories.** Gradient, glow, glass, badge, icon tile, animated border, decorative blur. Pick the least load-bearing one and remove it. The professional version of almost every AI-built screen is a calmer one.
7. **Check fidelity agreement.** Every layer on screen should share one level of detail and one edge quality: a hard-outlined pixel sprite sitting over a smooth anti-aliased gradient, or a crisp illustration beside soft-shadowed cards, reads as two art directions stacked no matter how good each piece is. Name the layer that disagrees with the rest.

Write the critique down as a numbered list of defects before you fix anything. Fixing while looking produces one fix and three missed problems.

### When the critique must be independent of the builder

The look pass above is one agent judging work it just built. When the user asks for a critique, or a polish pass needs an outside verdict, fan out two isolated assessors through `delegate_task`, one task per assessor, each given only the URL or screenshots, the audience, and the instruction to review unanchored: do not read the repository, name the element and the specific change for every finding, cap the reply at the top defects by severity. Assessor A runs the design review: a 0 to 5 score per heuristic (impeccable's `critique` command or the Nielsen set) with a one-line key issue, then defects ranked by severity. Assessor B runs the deterministic evidence: `scripts/audit.py` at a mobile and a desktop width, driven interactive states, screenshots, console output. Merge into one report: the score table, the defect list with the fix named for each, a verdict (ship, fix-then-ship, rework), and a mark on any finding only one assessor saw. Convert it to a P0/P1/P2 list, apply P0 and P1 in one batch, then re-run Steps 1 and 2 and report both runs. Never report a heuristic score you did not collect: a score table assembled from memory is the same failure as an audit never run.

---

## Step 4: Fix and re-run

Apply the fixes, then run Steps 1 and 2 again. Two rounds is normal. If round three still has FAILs, the problem is structural: stop patching and reconsider the layout or the design system.

**An element-scoped default out-specifies a class override, silently.** A rule such as `.faq article{background:#fff}` outranks a component rule like `.faq__ask{background:navy}` (the tag adds specificity), so white-on-navy text lands on white while the page still looks "mostly right" in a screenshot skim. Write overrides scoped as `.parent .class` so they win by construction, and never rely on source order alone: a later rule with lower specificity still loses. The contrast audit is what catches the finished defect, so treat any unstyled-looking override as a selector-weight question first and probe `getComputedStyle` before redesigning the section.

**Namespace ids in generated repeated sections.** `getElementById('x')` and `querySelector('#x')` resolve against the whole document and return only the first match, so a template that emits the same ids for every section wires all lookups to section one: the first block renders, the rest stay blank, and console, overflow and audit all stay green because nothing threw. Prefix every generated id with its section key (`#t4-t0`) or query inside the section root, then assert content on every instance rather than the first: map each section to its block's `textContent.length` and fail the gate on a zero. This check belongs in the same probe run as the copy-button test, since a copy button can copy the right payload while the visible prompt it was supposed to fill is empty.

**Namespace a new page shell before reusing a component library.** A generic root class such as `.lab` may already mean a label inside a chart. Giving that selector `min-height: 100vh` silently stretches every KPI label while overflow and console checks remain green. Search existing class usages first, use a product-specific root class, and assert a reasonable label height in a rendered representative chart. Review at least one example of each reused component, not only the default screen.

**A control that renders correctly can still be permanently dead.** Read `.disabled` on
every button, link and control on the loaded page before you trust a click, and log any
that are disabled without an explicit `disabled` in the source: a `h(tag, attrs)`-style
DOM helper that does `setAttribute(k, v)` will turn the prop `disabled: false` into the
attribute `disabled="false"`, and HTML treats any value as disabled, so the control looks
live and silently swallows every tap. Mouse-driven automation finds this only if it
asserts the page advanced; driving with `page.click()` on an already-inert button fails
soft and the run still looks green. Sweep the default state instead:

```js
[...document.querySelectorAll('button, a, input, [role=button]')]
  .filter(b => b.disabled || b.getAttribute('aria-disabled') === 'true')
  .map(b => b.textContent.trim() + ' @ ' + b.outerHTML.slice(0, 90))
```

**Measure before you fix.** A clipping, overflow, animation-state, or contrast claim read off a screenshot is a hypothesis, not a finding: a full-page shot captures scrollable panels in whatever scroll state they happened to be in, and a vision read will happily report a border that does not exist. Confirm with a DOM probe first, `getBoundingClientRect()` of the control against its scroll container plus `scrollHeight` vs `clientHeight`. For scrubbed or pinned sections, settle the scroll (`window.scrollTo`, wait for the scrub to catch up; `mouse.wheel` mid-flight lags), then read computed styles: the progress custom property, headline opacity, scene opacity. A screenshot blamed for "the transition never ran" at a mid-scrub frame is the frame, not the code; probe the numbers before spending a fix round. If the probe matches intent, the layout is fine and the screenshot misled you. Fixing on the screenshot's word spends a whole round on a defect that was never there.

**A control a reviewer wants disabled in an error state may be the only working path left.** A "clipboard unavailable" notice sitting above a live copy button reads as a contradiction, and the instinctive fix (disable or hide the button) deletes the manual fallback instead of correcting anything. Before accepting any "turn this off in the failure state" proposal, drive that state for real (deny the permission, drop the network, reject the submit) and list what still works: auto-selected text a user can copy by hand, a retry, a draft they open themselves. Accept the fix only when no alternative route remains, and state in the report which route the change removes.

**When a vision pass returns a LIST of geometric claims, settle the whole list in one probe run.** An art-directed critique of a scaled full-page capture asserts overlapping hero columns, uneven tab widths, truncated evidence text, mismatched label weights, an off-margin footer and a floating checkbox in a single reply, and measurements show nearly all of it equal. Convert each claim to one measurable assertion (bounding-box gap, per-item widths, `scrollHeight` vs `clientHeight`, computed `font-weight`, shared left edges, control/label tops, center alignment), evaluate them in a single page probe, fix only the rows where the numbers disagree with intent, and name the disproved claims in the report so the next round does not re-litigate them. One probe beats N fix rounds, and a critique list from a thumbnail is mostly hypotheses.

**A reported word join is checked in the DOM, not in the pixels.** `proposedtechnology` in a vision read may be downscaling or may be real: read the element's `textContent`. If the words are genuinely joined, the usual cause is a `<br>` or newline suppressed by a breakpoint rule, so put a space *before* the break tag (`proposed <br/>technology`): the whitespace survives when the break itself is hidden, and only the narrow width ever shows the merged state, which the desktop capture cannot reveal.

**Shoot the settled state and a deliberate mid-state; each hides what the other shows.** A mid-frame screenshot lies about missing content (the reveal has not run yet), but the settled screenshot cannot see anything that exists only while the sequence runs: an arrowhead drawn ahead of its line, an overlay released early, a staged element visible before its cue. Once the probe numbers settle, capture one mid-progress frame alongside the final frame and check it for elements visible before their driver reaches them; defects with a time dimension never appear in the resting shot.

**A section shot must come from the element, not the scrolled viewport.** A viewport capture taken after `scroll_into_view` catches the sticky nav sitting over the section's top band, and the eye reports "the eyebrow and first row are clipped" when only the scroll position is wrong. Capture `locator(selector).screenshot()` for section review. Note that the element shot composites fixed overlays too: a mobile sticky CTA bar or cookie banner covering the element's box is painted into the PNG, so the eye reads "the last line is clipped" on text that lays out fine. Before spending a fix round on any clip or covered-text claim from an element shot, check whether an overlay owns those pixels (`document.elementFromPoint` at the claimed point, or the container's `scrollHeight` vs `clientHeight` for a genuine clip); if an overlay owns them, hide it for the shot or shoot a band above it rather than adding padding to a correct layout.

**A cropped shot's blind spots are not its defects.** The eye will report the closing statement, the table footer and the last card row as "clipped off the bottom" whenever the crop window happens to end just above them, and the fix it proposes (more padding, a taller canvas) is a fix for the crop. Before acting, compare the element's claimed position against the full-page height: if it sits below the crop range, re-crop a band that contains it. The same applies to any element named as missing when it is simply not in frame; ask the next pass about the region where it lives. Confirm both mechanically, by bounding-box measurement rather than by re-reading the same image.

**Scroll-revealed content shoots blank unless the capture can force it visible.** A reveal driven by `IntersectionObserver` never fires in a full-page capture, so whole sections come back as white space and a vision pass reports the section as "missing" or "never built". Give the page a static flag the reveal script itself honours (`if (reduce || q("static") || !("IntersectionObserver" in window))` add the visible class immediately, CSS showing the end state), then shoot with `?static=1`. Two gotchas: the query parameter must ride on the full `file:///abs/path.html?static=1` URL (passing a bare filename makes the script drop the query), and an element already at `opacity: 0` also needs a CSS branch, because JS that only skips the observer leaves it hidden. Bars and counters reveal the same way, so assert them by reading their computed end state (`transform` on a `::after` fill, `opacity` on the row), not by looking for pixels that may not have rendered yet.

**Replayed entrance animation reads as empty space.** Word-by-word and staggered reveals start from `opacity: 0`, and a page reloaded for a capture replays them from the top, so a card shot mid-reveal reports "dead space below the fold" or an invisible header as a layout defect. A capture flag the build honours in script does not reach CSS animations unless the stylesheet honours it too: force the animated end state in the CSS itself (`.static .w{animation:none;opacity:1;transform:none}`), rebuild, re-shoot. Tell the two causes apart in the shot: a mid-reveal frame shows a *partially* populated block (headline complete, subtitle ghosted); true dead space shows none of it.

**`document.scrollWidth` does not prove there is no overflow.** A root with `overflow-x: hidden` (or an ancestor clip) reports `scrollWidth === innerWidth` while children are twice the viewport wide and half of them are invisibly cut off. Measure geometry instead: walk `getBoundingClientRect().right > innerWidth + 1` over the page's elements, excluding nodes that scroll by design (table wrappers, the sidebar rail, canvases). The two probes disagree, and the rect walk is the one telling the truth.

**A grid track sized `1fr` cannot overflow; it expands.** `1fr` computes to `minmax(auto, 1fr)`, so a column's min-content floor lets it grow past the viewport while every descendant reports a tidy bounding box. Declare `minmax(0, 1fr)` on the track and `min-width: 0` on the child that must be allowed to shrink (the `main` inside a shell), and re-measure. Fixing a root `overflow` property instead just hides the defect and leaves the clipped content unreachable.

**Give every wide data table its own scroll box.** A table wider than the screen must scroll inside `overflow-x: auto` on its own wrapper. Without one it either forces the page to scroll horizontally or gets cut off by the root clip, and the audit will name the root as the culprit rather than the table.

**Stack it instead when the page is read, not scanned.** On a reference or cheat-sheet page held open during a live call, a sideways-scrolling table hides half its text off screen, so stack the rows: `table, tr, td { display:block }`, `thead{display:none}`, each `td` labelled by its column through `td::before{content:attr(data-l)}`. A rect probe passes either layout, so confirm the stacked version by eye at the mobile width: a cell wrapped to a readable stack and a cell truncated at the viewport both report tidy bounding boxes.

**Animated label spans get shrunk out of their own text.** A button whose label animates through `grid-template-columns: 0fr/1fr` sits in a flex row, and the flex item's base size collapses to zero, so the label clips to a fragment ("Book a") at narrow widths while the button still measures fine. Give the button `white-space: nowrap` and the label span `min-width: max-content`, then re-shoot: the truncation only shows at 390 and only after the animation rule exists.

**A button that is itself the grid partitions its own label.** Setting `display: grid`
on a `<button>` lays the button's children into the template, so the description meant to
span lands in the narrow icon column and wraps into a four or five line stack while
every overflow check stays green: wrapped text does not overflow, it just becomes
unreadable. Keep the button's children as one row (an inner flex wrapper holding icon,
name and price, full width) and, in the look pass, ask the shot explicitly whether
descriptions run one or two lines rather than five. Narrow stacks and clipping are
different defects and only one of them is caught by an overflow probe.

**Figure and diagram text is measured, never eyeballed.** A downsampled full-page capture routinely renders 11px labels as an illegible smudge, so a vision pass reports "labels unreadable" on drawings that are fine; and the inverse is real too, because SVG text sized in user units scales with the drawing's rendered width: probe `parseFloat(getComputedStyle(label).fontSize)` times the svg's width/viewBox ratio at each shipping width before judging legibility. When the drawing is allowed to shrink below phone width, labels fall under 9px while every audit stays green (wrapped or scaled text does not overflow), so give the svg a `min-width` inside an `overflow-x: auto` wrapper: the drawing scrolls sideways on a phone and the labels hold size. Report the computed label px per width with the fix.

**A tap target is measured on the link, not the image inside it.** A nav logo rendered 44px tall still audits as an undersized target when its `<a>` wraps tightly at 34px. Set the height on the anchor (`display: flex; align-items: center; min-height: 44px`) rather than only on the `<img>`, because the anchor is what the geometry check measures.

**Two sticky bars anchored to the same `top` overlap on narrow screens.** Offset each one by the height of the bar above it in the mobile media query (`top: 60px` for the second bar under a 60px nav) or the lower bar sits underneath the upper one and its controls are unreachable.

**A canvas or WebGL page needs a second proof.** The audit inspects the DOM and sees none of the pixels, so a blank canvas audits clean. For any stateful scene: expose a read-only state hook (`window.<name>.getState()`), drive each state in Playwright, assert the state actually changed, and byte-compare one capture per state so "all five views render distinctly" is a measured claim instead of a look. Set `--selector "[data-loaded]"` only after the scene is really built, never at script start.

**Re-verify on the deployed artifact, not the build you tested locally.** After any deploy,
the target of the gate becomes the production URL: `curl -o /dev/null -w "%{http_code}"` every
route and every static asset the app ships (nested asset paths, generated media, credit or
license files), then re-shoot the same screenshot set against the live host. A static server
that serves a path locally can 404 it in the container, and a client bundle can be stale
there while current on disk; only the production read proves it. Cursory `200` on the health
route is not verification of the surfaces people will open. Grep the served bytes too: fetch one asset the change touched and grep it for a string only the new code contains (a new identifier, a new rule), because a `200` proves the route answers, not that the container is serving the new build.

**In an overflow-constrained panel, order content by whether the table must act on it.**
A fixed-height card clips whatever sits last, so a footer prompt (vote now, act now) placed
below a variable-length readout (initiative list, log) disappears exactly when the session is
busiest and the prompt matters most. Render actionable prompts first, passive data after, and
re-shoot with every region populated at once to confirm. On a surface nobody scrolls, "it is
below the fold" and "it is clipped" are the same failure.

**Reproduce a phone-only interaction complaint before touching the code.** A defect
users hit with a finger may not reproduce under mouse automation. Emulate the device and
dispatch real touch events at the element's centre, one element per screenshot:

```js
await call('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
await call('Emulation.setTouchEmulationEnabled', { enabled: true });
// scrollIntoView({ block: 'center' }) first, then:
await call('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
await call('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
```

Then distinguish the three causes with probes, not by reading the pixels: `.disabled` is
set means the control is inert by construction; `document.elementFromPoint(cx, cy) !== el`
means something else (overlay, stacking context) owns the tap; neither means the handler
never bound, so read the console. Probes and `Runtime.evaluate` keep returning while
screenshots time out, so on a cold or slow page the probe is the reliable channel and the
shot is the bonus. Assert page state after each step (a step counter, a `.sel` class) and
let the assertion failure, not the missing highlight, drive the fix.

**A panel shorter than its column is a layout defect wearing a vaguer costume.** A two-column section whose detail panel sits at `align-items: start` ends short of the checklist beside it, and the vision pass reads it as "dead space below the card", which is the same complaint in softer words. Set `align-items: stretch` on the grid so the panel fills, re-shoot, and require both columns to end on one baseline before you call it fixed.

**Report honestly.** State what was verified and at what sizes, and when a shot only reached part of a tall page, name the sections it did not cover as unchecked rather than letting the check read as complete:

> Verified at 390 / 834 / 1440, light and dark. Audit clean apart from one INFO on measure in the footer. Two rounds of critique: fixed hierarchy in the hero (headline was competing with the eyebrow) and the card grid collapsing to stretched full-width blocks on mobile.

Never write "verified" if you did not open the images.

When the deliverable is a set of files others open later (a showcase, a handoff, a deck), persist the report beside them as `VERIFICATION.md`: checks executed with counts, visual defects found and fixed, and explicit limits (devices not tested, no deployment, what was left unverified). A chat message ages out; the file travels with the artifact and answers the reviewer's first question without a rebuild.

---

## The gate

Delivery is blocked until all of these are true:

- [ ] Dash count zero on the file (Step 0), any hits fixed before rendering
- [ ] Every requested change grepped in the files on disk (Step 0.5), with the hit count reported for anything applied in more than one place
- [ ] `audit.py` run at a mobile width and a desktop width, zero FAILs, every WARN either fixed or justified in one line
- [ ] Audit and shots cover every state that ships controls (empty, configured, results, signed in), not only the default load
- [ ] `shoot.py` run and **every PNG opened with the Read tool**
- [ ] A written critique exists, naming specific elements, not adjectives
- [ ] Fixes applied and the audit re-run clean
- [ ] Dark mode checked if it ships, reduced-motion checked if anything animates
- [ ] Any scrubbed or staged sequence sampled at a mid-state as well as settled: no element visible before its driver reaches it
- [ ] Console is free of errors
- [ ] Overflow checked by element rect against the viewport, not by `document.scrollWidth` (a clipped root lies), and any "text is clipped / element is missing" claim from a vision pass first confirmed against the full-page height, since a crop's own edge is the usual culprit
- [ ] Every interactive control the page ships, console-checked: no control is disabled in its default state without an explicit source attribute, and each one advances page state when driven
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
