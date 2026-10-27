---
name: span-landing-page
description: Use when building or refreshing a SPAN landing page.
version: 1.1.0
author: Champions Accelerator
metadata:
  hermes:
    tags: [span, landing-page, conversion, static-html]
    related_skills: [span-brand-guidelines, microsite-refresh, visual-verify]
---

# SPAN Landing Page

Turn a source URL, HTML file or approved brief into a single-offer SPAN Global Services landing-page preview. Deliver HTML, editable site.json and VERIFICATION.md. For the complete workflow read references/workflow.md, then reuse assets/campaign-landing/build.py and its examples. Do not write a second renderer.

Load span-brand-guidelines, frontend-design and visual-verify. Main owns content judgments and review; route UI implementation to a frontend Kanban card, never delegate_task. Keep full microsites on microsite-refresh and corporate homepages on venture-story. For the toy microsite genre Deep calls "dopamine sites" (single-screen brand toy, no conversion goal, shared result card), use `references/dopamine-sites.md`.

## Standing rules

Keep the established Dither Grid hero, prominent offer line, four primary fields, visual question rail and halftone footer behind the links. Verified count comparisons use separate adjustable bento boards, not one combined board or a reveal slider.

A stat band after the dark hero is always white with SPAN Green figures, readable muted labels and hairlines. Preserve this inverse scheme across future skins. If source counts are absent, omit the band, do not invent figures to fill it.

Every section explains with a playable component, never a static diagram or wireframe: masked realistic sample records (fictional, at most three leading characters visible, job titles in full) in the hero card and the sample sheet, the Orbit selector (vanilla port of the 21st.dev Orbit Timeline) for segment choice wired to the form, and one interactive widget kind per FAQ answer (see assets/campaign-landing/VISUALS.md). Empty bars, Venn rings and hand-drawn SVG were rejected by Deep three times; do not reintroduce them.

Optional band, clients, compare and citations disappear when unsupported. Never inherit PEO figures, dates, clients, SLAs, verification or compliance claims into a different offer. Sample layouts are clearly illustrative. Preserve the source's optional phone and custom-requirement semantics.

Local validation is not lead capture. Unwired preview feedback says nothing was sent, with no personal-payload logging or conversion event. Endpoint, tracking and final production URL are launch blockers, not invented defaults.

## Run

From assets/campaign-landing/:

```bash
python3 build.py examples/span-msp-us --out /absolute/path/SPAN_MSP_US_LandingPage.html
python3 -m unittest discover -s tests -v
```

Use examples/span-peo-eor for the count-backed case. Change copied site.json, never generated HTML. Check both examples after renderer changes. Run real browser checks at 390, 834 and 1440, open section screenshots and write the verification report before delivery. A single file uses external Google Fonts and citation favicons, not a fully offline dependency set.
