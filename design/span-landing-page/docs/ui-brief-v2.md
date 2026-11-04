# SPAN landing page template v2: brief for the frontend lane

Owner of judgment: main lane (Deep's agent). Executor: frontend lane. Status: brief v2, 5 Nov 2026.

## 1. Goal

Replace the look of the SPAN campaign landing page with a calm, high contrast, editorial design, while keeping the same `site.json` contract, so one template still renders every variant (industry, role, headline). Deep's verdict on the current page: the pixel (dither) gradient hero was a good idea once, now it distracts and makes text hard to read. Something is missing: proof and a spine.

Deliverable: `template-v2.html` next to `template.html`, a `--template` flag on `build.py`, the three demo variants rebuilt with v2, screenshots and a verification report. `template.html` stays byte for byte as it is until Deep approves v2.

## 2. Paths

| What | Path |
|---|---|
| Builder and templates | `/Users/deep/champ-skills/design/span-landing-page/assets/campaign-landing/` |
| Current template (read, do not edit) | `template.html` |
| New template (create) | `template-v2.html` |
| Builder (edit: add `--template PATH`, default `template.html`) | `build.py` |
| Unit tests (must stay green; add one v2 case) | `tests/test_build.py` |
| Browser checks (reuse pattern) | `tests/browser_check.py` |
| Component rules | `VISUALS.md` |
| Demo variants | `/Users/deep/Celsus/Efforts/Active/Ideation/programmatic-demo/` (`make_demo.py` builds three variants, `check_demo.py` tests them; both must accept the v2 template via env `SPAN_TEMPLATE=/abs/path/template-v2.html`) |
| Brand | skill `span-brand-guidelines`, Brand dialect |

Skills to load first: `frontend-design`, `span-brand-guidelines`, `visual-verify`, `responsive-viewport-qa`.

## 3. Reuse inventory (do not reinvent)

`template.html` already has, in vanilla JS and CSS: the form with local validation and the preview-only thank you state, `?hl=` headline swap, the Orbit selector wired to the form, the masked sample record card with Pause control, the sortable sample sheet, five FAQ widget kinds (fanout, loop, narrow, anatomy, path), scroll reveal, sticky CTA, the footer. Copy the behaviour. Restyle the surface. Every `{{placeholder}}` and every `data-` hook `build.py` fills must survive with the same name, which is why `test_build.py` is the contract.

## 4. Design direction

One sentence: the product is real contact data, so the page should look like a well set data sheet, not like a poster.

| Token | Value |
|---|---|
| Dark surfaces | Dark Navy `#0F2B3C`, cards on dark Mid Navy `#1A3A4A` |
| Light surfaces | Surface White `#FFFFFF`, alternate Off-White `#F5F7F9` |
| Primary accent | SPAN Green `#1B6B3A` on light, Light Green `#3DBE6E` on dark |
| Text | Dark Text `#1E2A32`, Dim `#4D6070`, Muted `#8FA0AC`; on dark, white and `rgba(255,255,255,.72)` |
| Hairlines | Surface Border `#D9E3E9` on light, `rgba(255,255,255,.14)` on dark |
| Type | Montserrat 700 for H1 and H2, Inter 400 and 500 for everything else. H1 clamp(40px, 5.2vw, 64px), line height 1.05, letter spacing -0.02em. Body 17px / 1.6, max 68ch |
| Radius | 12px cards, 8px inputs and buttons |
| Shadow | one: `0 10px 30px rgba(15,43,60,.12)` on the form card only |
| Motion | reveal on scroll (opacity and 12px translate, 400ms, once). The sample record cycles every 4s with Pause. Nothing else loops |

Hard rejects: dither, halftone, pixel or noise textures; gradients behind text; animated backgrounds; empty bars, Venn rings, hand drawn SVG (rejected by Deep three times); decorative blur blobs; more than one accent color per section.

## 5. Section spec, top to bottom

Each section is one scroll beat with one idea. A thin left rail on desktop (>= 1024px) shows the beat number `01` to `05` and a 1px progress line; hidden below 1024px.

| # | Section | Background | Content | Visual contract |
|---|---|---|---|---|
| 0 | Header | transparent over hero | logo left, phone right, nothing else | logo min height 28px; phone is a `tel:` link |
| 1 | Hero | Dark Navy, flat | left: eyebrow (Light Green, 13px uppercase, 0.08em), H1 `{{headlines.default}}` with `id="hl"`, lede, ledeEmphasis in white 500. Right: the form card (white). Below the H1 on desktop, full width on phone: the live sample record table | the table is the hero object: 3 masked rows cycling from `sampleRecords`, columns Name, Business email, Job title, Company, Location; a chip row above it: "Illustrative, not real data" and "Fields and coverage vary by segment". Headline readable at WCAG AA on flat navy; no image, no texture |
| 2 | Trust strip | white, hairline top and bottom | three facts, each icon plus one line: "Sample before you commit", "Fields shown in every record: {{fields}}", "Team reviews every request" | pulled from `site.json` text only; no client names, no counts unless `band` exists |
| 2b | Stat band (only when `site.json` carries counts, PEO/EOR example) | white | SPAN Green figures, muted labels, hairline grid, count up on reveal | omit the whole section when no counts; never invent |
| 3 | Who is this for | Off-White | H2 `{{account.title}}`, lede, Orbit selector wired to the form (keep), `account.fit` line | Orbit items are the only interactive piece in the section |
| 4 | What the sample may include | white | H2 `{{dossier.title}}`, tag, the sortable sample sheet (keep), columns, footer | sheet header sticky inside its scroll container at phone widths |
| 5 | How teams use it | Off-White | H2 `{{faq.title}}`, sub, FAQ as a single open accordion; each open panel shows lead, detail, and its widget (keep the five kinds, restyle to flat navy and green) | one open at a time; chevron rotates; keyboard operable |
| 6 | Closer | Dark Navy | `{{closer.title}}`, text, button, small line | button Light Green background, Dark Navy text, 48px tall |
| 7 | Footer | Dark Navy, hairline top | wordmark, three columns from `footer.columns`, meta line | flat; no halftone |
| sticky | Mobile sticky CTA | Dark Navy bar | `{{form.sticky}}`, appears after the hero leaves view, below 1024px only | 56px tall, safe area padding |

Form card (unchanged behaviour): title, sub, four fields (name, work email, phone optional, requirement select), custom requirement textarea when "Custom list" is picked, consent checkbox with the privacy link, submit button SPAN Green, foot text, the preview-only notice. Labels above inputs, 15px, Dim. Inputs 48px tall, 1px Surface Border, focus ring 2px SPAN Green.

## 6. 21st.dev component table

Install via the shadcn CLI on nvm node v24 with `TWENTY_FIRST_API_KEY`, then port to vanilla HTML/CSS/JS for the static template (the page ships as one file). Name every ported component in the handover.

| Region | Component | Role | Visual contract |
|---|---|---|---|
| Hero layout | Hero 45, shadcnblockscom, id 612 | two column hero with three features under it; take the grid and spacing, drop its imagery | headline column 7/12, form 5/12 at >= 1024px; stacked below |
| Hero object | Streaming Data Rows, rmahammad, id 29368 | the live masked record table; take row insert and highlight, status pill becomes the segment chip | three rows visible, new row slides in every 4s, Pause honours `prefers-reduced-motion` |
| Stat band | Stats Band, kuratlielia, id 35089 | hairline grid of counting figures (only with counts) | figures SPAN Green, labels Muted, inline charts removed |
| Left rail | Scroll Progress, designali-in, id 4583 | the 1px vertical progress line in the beat rail | rail 48px wide, fixed, >= 1024px only |
| FAQ | Single Open Accordion, ibrandify, id 37545 | FAQ container | one open panel, 48px trigger height, hairline dividers |
| Closer | Call to Action, felipemenezes098, id 18475 | centered closer block | one button, one small line |
| Footer | Minimal Two-Column Footer, ln-dev7, id 26908 | adapt to three columns from `footer.columns` | hairline top, 13px links |

The Orbit selector and the sample sheet stay as they are in `template.html` (vanilla ports already approved by Deep).

## 7. Data honesty

Render only what `site.json` provides. No counts, clients, dates, SLAs, or compliance claims that are not in the file. The hero table and the sample sheet show the masked `sampleRecords` only, labelled illustrative. The form sends nothing and says so. Forbidden strings anywhere in the output: `TODO`, `lorem`, `XXXX` outside the tracking placeholder already in `site.json`, and any client or vendor name not present in `site.json`.

## 8. Acceptance (named gates)

1. `python3 -m unittest discover -s tests -v` green, including a new test that builds both examples with `--template template-v2.html` and asserts the H1, the noindex meta, the absence of `dither`, `halftone` and `canvas` in the output, and that every `data-` hook present in the `template.html` build is present in the v2 build.
2. `python3 build.py examples/span-msp-us --template template-v2.html --out /tmp/v2-msp.html` and the PEO/EOR example both build; PEO shows the stat band, MSP does not.
3. `SPAN_TEMPLATE=/abs/path/template-v2.html python3 make_demo.py && python3 check_demo.py` in the demo folder: all seven URL checks pass and the switcher click passes.
4. Contrast: every text node on the hero and closer measures >= 4.5:1 against its computed background (Playwright script, computed colours, numeric output in the report).
5. `responsive-viewport-qa` at 390, 834 and 1440: no horizontal overflow (reuse `geometry()` from `browser_check.py`), the form card is fully visible without scrolling at 1440, the sticky CTA appears only below 1024.
6. Lighthouse or equivalent: no render blocking beyond Google Fonts; total page under 400KB without the logo.
7. Screenshots at the three widths for hero, FAQ open state, closer, written to `qa/v2/`; open them yourself before handing over.
8. `VERIFICATION-v2.md` lists: commands run with output, the 21st.dev components ported, the launch blockers unchanged (form endpoint, tracking ID, production URL, phone and privacy URL from the brand book).

## 9. Do not touch

`template.html`, `examples/*/site.json`, `SKILL.md`, anything outside `assets/campaign-landing/` and the demo folder. The champ-skills checkout has unrelated uncommitted edits in other skills: do not stash, reset, checkout or commit anything. Leave your changes uncommitted and report the changed file list; the main lane reviews and commits.

## 10. Handover

Reply with: changed files, the eight gate results with real output, the component list, one line per deviation from this brief and why, and the path to `qa/v2/`.
