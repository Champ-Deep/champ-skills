# VERIFICATION: template-v2.html (task t_160c02b9)

Brief: `docs/ui-brief-v2.md`. Run on 2026-11-05 IST, macOS, Chromium via Playwright (`/opt/anaconda3/bin/python3`). `template.html` and `examples/*/site.json` are unchanged: `git diff --quiet HEAD -- template.html examples` is clean, and the last commit touching `template.html` is c9f9040 (2026-10-26).

## Changed files

| File | Change |
|---|---|
| `template-v2.html` | new. A calm navy and white layout with no dither and no halftone, built from v1 markup and JS that is still in use, plus a v2 CSS layer |
| `build.py` | `--template PATH` (default `template.html`), plus three placeholders that only v2 uses: `{{faq.accordion}}`, `{{hero.stream}}`, `{{trust.fields}}`. The v1 output is byte-identical to the pre-change build (`cmp` on both examples) |
| `tests/test_build.py` | new `test_v2_template_keeps_the_contract` |
| `tests/v2_check.py` | new browser gate: overflow, contrast, form fold, sticky CTA, FAQ, console, dashes, flat sweep (no gradients, no empty bars, every FAQ panel opened), screenshots to `qa/v2/` |
| `tests/v2_live.py` | new live (non-static) probe: stream rotation, Pause, reveal end states, beat rail, count-up, accordion keyboard, reduced motion |
| `qa/v2/` | 28 PNGs plus `v2_check.json` |
| `programmatic-demo/make_demo.py` | reads env `SPAN_TEMPLATE` and passes `--template` |
| `programmatic-demo/check_demo.py` | when `SPAN_TEMPLATE` is set, shots go to `shots-template-v2/`; `DEMO_PORT` override (3147 was held by an unrelated next-server, pid 87420) |
| `programmatic-demo/SPAN_msp-*.html` | rebuilt with v2 |

## Gates (brief section 8)

1. **Unit tests**: `python3 -m unittest discover -s tests -v`: `Ran 18 tests ... OK`. The new test builds both examples with v2 and asserts the H1, the noindex meta, no `dither`, `halftone` or `canvas`, and every `data-` hook from the v1 build. It also checks that the band appears only with counts and that there is one accordion trigger per FAQ item.
2. **Builds**: `python3 build.py examples/span-msp-us --template template-v2.html --out /tmp/v2-msp.html` and the PEO/EOR equivalent: both `built`; `band msp=0 peo=1`.
3. **Demo**: `SPAN_TEMPLATE=.../template-v2.html python3 make_demo.py && DEMO_PORT=3148 check_demo.py`: 6 URL checks plus the switcher click, 7 PASS:
   ```
   PASS /SPAN_msp-us.html -> Your Next MSP Customer Starts With The Right Contact.
   PASS /SPAN_msp-us.html?hl=mssp -> Reach The MSSPs That Sell Managed Security.
   PASS /SPAN_msp-healthcare.html -> Reach The MSPs That Keep Hospitals And Clinics Running.
   PASS /SPAN_msp-healthcare.html?hl=hipaa -> Reach The MSPs That Handle HIPAA Workloads.
   PASS /SPAN_msp-recruiting.html -> Reach The MSPs That Run IT For Staffing Firms.
   PASS /SPAN_msp-recruiting.html?hl=payroll -> Reach The MSPs Behind Payroll And Onboarding Systems.
   PASS switcher click navigates to healthcare variant
   ```
4. **Contrast** (`tests/v2_check.py`). It walks every text node in `.bar`, `.hero` and `.closer`, then composites the computed colour over its computed background stack. 0 nodes are below 4.5:1.

   | page@width | text nodes | min ratio | min node |
   |---|---|---|---|
   | msp-us@390 | 41 | 5.03 | Illustrative, not real data |
   | msp-us@834 | 46 | 5.03 | Illustrative, not real data |
   | msp-us@1440 | 46 | 5.03 | Illustrative, not real data |
   | peo-eor@390 | 25 | 6.14 | PEO and EOR competitive intelligence |
   | peo-eor@834 | 25 | 6.14 | PEO and EOR competitive intelligence |
   | peo-eor@1440 | 25 | 6.14 | PEO and EOR competitive intelligence |
5. **Responsive** at 390, 834 and 1440. `geometry()` from `browser_check.py` reports no overflow at any width. Form card at 1440 (top/bottom in a 900px viewport): msp 104/797 and peo 104/826, so it is fully visible. The sticky CTA is visible after the hero at 390 and 834 and absent at 1440. Bar height is 57px (56 plus a 1px hairline) with safe-area padding. 50 of 50 checks PASS (round 2 adds the flat sweep at each page and width).
6. **Weight and blocking.** I did not run Lighthouse. The equivalent: there are 0 `<script src>` and the only stylesheet is Google Fonts (`display=swap`). Built size is 152,481 bytes for MSP and 151,213 for PEO; without the inlined logo that is 139,869 and 138,601 bytes, about 137KB, under 400KB.
7. **Screenshots**: `qa/v2/{msp-us,peo-eor}-{hero,faq,closer,full}-{390,834,1440}.png`, plus `qa/v2/{msp-us,peo-eor}-faq0{3,4}-1440.png` with FAQ 03 and 04 open (round 2). All were opened and read (critique below).
8. **This file.**

Also run:
- `tests/v2_live.py`: 38 PASS, 0 fail. With motion: the stream rotates, Pause holds the rows and sets `aria-pressed`, every `.rv` ends at opacity 1, the rail walks 01 to 05, the progress line ends full, band figures end at the markup values (`331,816`, `28`, `70+`, `30 days`), ArrowDown moves between triggers, Enter opens one panel, and closed panels are `inert`. With reduced motion there is no rotation and no Pause button, and everything else is the same.
- visual-verify `audit.py` at 390 and 1440 on both builds: **0 FAIL**. WARNs left: `default-font` (Inter is the SPAN Brand dialect body font, a brand contract) and, on MSP only, `glass-count` / `static-glass` on the Orbit selector nodes. The brief says to keep Orbit as is.
- Dashes: 0 in both builds and in `template-v2.html`.
- Forbidden strings in the output: `TODO` 0, `lorem` 0, `XXXX` 0.
- Skip link: Tab gives focus at top 0, opacity 1, and Enter goes to `#main`.
- Sheet header at phone width (390x500): `position: sticky`; the header offset is 0 after scrolling the sheet container.

## Round 2 (review comment on t_160c02b9): flat fills only

The review found brief section 4 hard rejects in the rendered builds. All non-Orbit gradients are now removed from the source: `grep gradient template-v2.html` outside `.ot-*` lines returns 0, and the same holds for the three rebuilt demo pages.

| Finding | Fix |
|---|---|
| MSP FAQ 04 record widget: 4 empty gradient bars (`.record__row i`) | bars and their leader lines hidden; the record lists its field names with icons, one column |
| MSP FAQ 03 funnel: text on gradients, mint and teal steps | flat steps #1B6B3A, #155A30, #1A3A4A, #0F2B3C, white text on all four (min 6.07:1 measured in every open panel) |
| `.hero::after` and `.form::before` green to teal stripes | rules deleted |
| Submit, sticky, strip CTA and FAQ ask buttons: `linear-gradient` | flat SPAN Green (sticky, closer and FAQ ask keep the v2 Light Green with navy text) |
| PEO `.dossier::before` pointer glow | rule and its pointermove JS deleted |
| Also flattened (same rule, not named in review) | narrowing diagram steps (same four flat steps), market map regions, picker first card, fan out hub, sheet placeholder shimmer, column sweep, closer background, `.vis` ground, `--diagram-data` |

Gate: `tests/v2_check.py` now runs `flat_sweep()` at 390, 834 and 1440 on both builds. It opens every FAQ panel in turn and fails on any computed `gradient` in `backgroundImage` on a visible element or its `::before`/`::after`, or any filled bar (wider than 40px, 14px or shorter) with no text, outside `.ot-*`. Exempt: `.wg__bar`, the PEO share meter, whose width is the share figure printed beside it. Negative control against the pre-fix template: MSP reports `empty bar accp4 i` x3, `gradient accp3 button.funnel__band`, `gradient accp4 i`; PEO reports `gradient dossier ::before`. After the fix: 6 of 6 PASS, 0 failures overall.

FAQ widget contrast (not covered by gate 4, probed with the same compositing function, every panel open, 390 and 1440): MSP min 5.83, PEO min 5.21, 0 nodes below 4.5.

Rerun after the fix: unittest 18 OK; both builds `built`, band msp=0 peo=1; `v2_live.py` 38 PASS, 0 fail; `audit.py` 0 FAIL at 390 and 1440 on both builds (same WARNs as round 1); demo rebuilt with `SPAN_TEMPLATE`, `DEMO_PORT=3150 check_demo.py` 7 PASS; dashes 0; `template.html` and `examples` clean against HEAD. Built size now 150,095 (MSP) and 148,827 (PEO) bytes.

Vision suggestions declined in round 2: rewriting the FAQ 02 answer as bullets (copy comes from site.json) and pointing every chevron down (the open item's chevron rotates by design).

## 21st.dev components (vanilla ports)

The source was fetched through the 21st.dev MCP (`get_component`), remapped to SPAN tokens and ported to vanilla CSS and JS, because the page ships as one static file. The shadcn CLI install path does not apply. Credits sit in a CSS comment at the top of the v2 layer and as HTML comments on each region.

| id | Component | Where |
|---|---|---|
| 612 | Hero 45 (shadcnblockscom) | hero grid: copy 7/12, form 5/12 at >= 1024, stacked below; imagery dropped |
| 29368 | Streaming Data Rows (rmahammad) | hero table: 3 masked rows, the last record slides in every 4s with a cell wash, segment chip, Pause; static under reduced motion and `?static=1` |
| 35089 | Stats Band (kuratlielia) | white band, SPAN Green figures, hairline grid, count up once; final values in the markup |
| 4583 | Scroll Progress (designali-in) | 48px fixed beat rail >= 1024, 1px progress line, current beat |
| 37545 | Single Open Accordion (ibrandify) | FAQ: one panel open, rotating chevron, arrows, Home and End, `aria-expanded`, `inert` on closed panels |
| 18475 | Call to Action (felipemenezes098) | closer: one Light Green button with navy text, 48px tall, one small line |
| 26908 | Minimal Two-Column Footer (ln-dev7) | widened to `footer.columns`, with a hairline top and 13px links |

Orbit selector and sample sheet: kept from `template.html`, as the brief requires. Kokonut UI was not adopted, because the brief fixes the component ids.

## Look pass (critique and resolution)

Fixed:
- In the hero table, the masked cells inherited the v1 `.masked` dim colour on navy (1.84:1). They are now white (fixed before the contrast gate went green).
- The v1 placeholder bars inside the `sources` and `sample` FAQ widgets were empty grey bars. They are now hidden.
- The measure on section ledes and FAQ answers was about 91 characters. It is capped at 62ch.
- The `.samp` widget overflowed its flex parent at 390. Added `min-width: 0`.
- The red sample stamp was off-palette. It is now SPAN Green.
- Playwright element captures painted the off-screen skip link at the top of the section shots. It is now hidden until focused; a pixel check on the top band of the FAQ shots shows flat ground only.

Vision claims disproved by probe:
- "Green eyebrow and table headers low contrast": the eyebrow is #3DBE6E on navy, inside the measured 5.03 minimum, and the table headers are white at 72%, not green.
- "Phone number touches the right edge at 390": its right edge is at 370 of 390, a 20px margin.
- "Left-edge vertical texture": this is the specified beat rail.
- "FAQ widget clipped at 390": the open panel's `scrollHeight - clientHeight` is 0, with 0 descendants outside the clip box.
- One vision reply described a Google homepage for the FAQ viewport shot. It was discarded.

Declined: changing CTA labels and site.json copy (out of scope, since the content comes from site.json).

## Deviations from the brief

- The header is solid navy rather than transparent. It sits on the flat navy hero, so it renders the same, and the logo is forced white through a CSS filter (logo rule: white on dark).
- Stat band labels use #5C6F7E, not Muted #8FA0AC: #8FA0AC on white measures 2.70:1 and fails AA; #5C6F7E measures 5.21:1.
- The PEO/EOR example has no `sampleRecords`, so its hero object falls back to the v1 `hero.object` (ticks plus sources) instead of the stream table. Data honesty: nothing is invented.
- Phone sheet: the container is capped at 70vh with a sticky header. At today's 6 rows it does not scroll on a normal phone, so the header pins only when the records outgrow the screen.
- The trust strip "fields" line comes from `dossier.sheet.fields` when present, otherwise from the first four row labels of `dossier.columns`.
- Gate 6 used a static equivalent, not Lighthouse.
- `check_demo.py` gained `DEMO_PORT` because port 3147 was occupied.

## Launch blockers (unchanged from v1)

- Form endpoint: the form is not connected. The page says so ("Preview only ... Nothing will be sent").
- Tracking ID: `AW-XXXXXXXXX/...` is still a placeholder in site.json and is not emitted.
- Production URL: none; pages stay `noindex`.
- Phone and privacy URL: still to be confirmed from the SPAN brand book.

## Repo note

Commit `54f3f60` ("pixel-host-studio", 2026-11-05 04:37, another session) swept this task's uncommitted `build.py` edit into its commit, together with `docs/ui-brief-v2.md` and `SKILL.md`. This task ran no git write commands. Everything else listed above is still uncommitted.

## Not verified

- Real devices (Chromium emulation only). Dark mode (the page ships none). Lighthouse scores.
