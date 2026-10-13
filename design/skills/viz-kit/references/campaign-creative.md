# Campaign creative mode

Use this workflow for advertising and campaign showcases. The objective is a set of distinct, usable creative options, not a report decorated with repeated ad mockups. Keep the chart workflow for actual data questions.

## 1. Establish the brief and evidence boundary

Identify the advertised brand, buyer, campaign objective, host/presenter brand, factual sources and approval state from available context. Ask only about ambiguities that change the work. Separate confirmed claims from proposed audiences, offers and routes. Do not invent results, savings, product screens, live events, dates, speakers, integrations, budgets or approval.

Load the relevant brand guidelines plus `prospect-creative-campaign-builder`, `vinh-copywriting`, `impeccable`, `carousel-funnel`, `no-ai-slop` and `visual-verify`. Load `media-use` for imagery and motion, then the provider or rendering skill it routes to. Prefer Higgsfield for commissioned conceptual artwork when connected and appropriate; use approved photography or another available production route when it is not. Do not spend or open a new paid subscription merely to satisfy a format checklist.

## 2. Design the option matrix before the gallery

For an open-ended kit, default to five campaign directions. Choose meaningful business jobs, such as acquisition, existing-customer expansion, product demand, events and retargeting. Substitute jobs that fit the business: a services firm without software does not need a fabricated product campaign. Three service names using the same ad layout do not constitute a broad campaign set.

Record these fields for each direction:

| Field | Required decision |
|---|---|
| Campaign job | What this option should accomplish |
| Buyer situation | Who sees it and why the message matters now |
| Offer | What the person receives or can discuss |
| Hook and post copy | Concrete buyer language, grounded in the evidence |
| Format | Static image, document carousel or motion |
| Visual treatment | Composition, image role and typography hierarchy |
| Primary CTA | One action, with a proposed destination and follow-up owner |
| Evaluation | Relevant response to measure, without invented performance targets |

Default output is five static executions, one narrative carousel and one rendered motion execution, with editable copy/source and a review gallery. These are production defaults, not mandatory campaign counts for every ask. A request for one ad gets one ad; a request for one chart stays in data mode.

## 3. Make the raw designs distinct

Build and inspect full-size standalone creatives before the presentation shell. Use a contact sheet to judge the set, then inspect individual exports at full size and at phone/feed scale.

Vary the visual grammar, not only colours. Useful treatments include an image-led editorial ad, a document or checklist-led ad, a product-category composition, a typographic invitation, and a restrained reminder. At least three clearly different composition families should be visible across an open-ended set. A buyer should be able to distinguish the options before reading their category labels.

Let images occupy enough of the ad to carry meaning. Avoid the repeated formula of a plain black background, oversized headline, small pasted image and floating CTA. Dark backgrounds are acceptable when justified by the brand and composition; they are not the default sophistication shortcut. Do not force photography into a type-led concept merely for consistency.

Use official logo originals and verified brand typography. Generate art separately from logos and exact copy, then composite the verified assets. Never fabricate a logo or present a generated interface as the real product. Keep presenter branding in gallery chrome and advertised-brand styling inside the exported assets.

Use one principal CTA per ad. A decorative button and a different footer action compete even if neither is clickable in the exported image. Keep CTAs rectangular with regular-weight text unless the user's explicit brand contract overrides that treatment. Keep logos unboxed. Avoid decorative rules before eyebrows. Reserve sufficient space for copy and action without covering the visual subject.

Write specific, readable copy. Replace vague directions such as 'explore the relevant solution' with a named product area or clear action supported by the source. Keep approval-process commentary in the review wrapper, not inside the buyer's message. Clearly label the package as proposed without inventing event details to make an invitation look finished.

## 4. Build each format as its own execution

### Static ads

Export usable PNG or JPEG assets, not only screenshots embedded in the gallery. For LinkedIn/feed concepts, 1080 x 1350 is a useful default; adapt dimensions to the requested placement. Include primary post copy, headline and platform CTA alongside each asset. Do not infer that an available CTA is approved or that a destination is live.

### Document carousel

Use `carousel-funnel` for narrative structure and its renderer. Build an argument with one idea per slide: hook, useful progression, a concrete working aid and next step. Vary slide blocks instead of repeating service tiles. A compact eight-page guide is a useful default when the story supports it; do not pad to a fixed count.

Deliver the multi-page PDF and individual page images. Test the gallery reader in the intended host. For restrictive previews, use accessible native radio controls with CSS page selection plus an expandable all-pages view. Test every page with JavaScript disabled and in a restrictive srcdoc iframe. Fragment links can navigate away from srcdoc, so do not assume standalone anchor tests prove embedded behavior. Keep labels touch-sized, preserve keyboard selection and provide the PDF independently.

For a live distribution request, complete the destination, comment-link and measurement workflow from `carousel-funnel`. For an unapproved concept, record those items as activation gates. Do not invent a published asset, tracked link or installed analytics integration.

### Motion ads

Produce an actual playable video, not a storyboard labelled as a finished motion ad. Keep good supplied footage when the user likes it; redesign framing, typography and action independently. A short silent feed cut is a useful starting point, not a universal duration requirement.

Make footage the main visual. Place text in a deliberate safe region or a separate branded band. Do not put an oversized CTA over the subject. Prefer a platform-level CTA outside the rendered footage when an in-frame action would obscure it. Controls must not cover essential text; test the actual playback controls at phone size.

Inspect frames across the full timeline, including the end, for generated cuts, malformed objects, copy collisions and logo integrity. Report actual output dimensions and duration rather than treating a provider tier label as measured resolution. Supply a poster and MP4. If generation or rendering is blocked, disclose the missing deliverable and finish the viable assets; never substitute a static image or invented job result and call motion complete.

## 5. Assemble a work-first gallery

Show the creative range near the top, then provide larger assets and usable copy. Keep strategy, audience and implementation notes secondary, preferably inside native expandable sections on mobile. Avoid making the user scroll through long repeated briefing tables to reach the work.

Keep the gallery full width and responsive. For an offline/self-contained delivery, embed fonts, images, document pages and video or provide a complete local bundle. This overrides the data-mode remote-font convention. Do not call a file offline-ready until offline checks pass. Offer individual assets and a tested ZIP, not only a gallery-dependent export mechanism.

## 6. Verify the assets and the presentation separately

| Gate | Required evidence |
|---|---|
| Raw design | Contact sheet plus inspection of individual assets. Distinct compositions, readable feed-scale copy, intact logo, one primary CTA, no subject-obscuring controls. |
| Carousel | Page count matches PDF and exports; every page selector works; expandable reading view works; phone-scale text and closing CTA remain legible. |
| Motion | Playable media, inspected frame sequence, actual dimensions/duration, no CTA or text collisions. |
| Gallery | Mobile, tablet and desktop renders; no horizontal page overflow; working downloads and playback; keyboard and reduced-motion behavior where applicable. |
| Host compatibility | Actual target preview tested when reachable. Otherwise explicitly label it unverified and report the fallback environment that was exercised. |
| Claims and copy | Evidence boundary respected, proposed status clear, no fabricated results, no em or en dashes, no-ai-slop review complete. |

Use `visual-verify` and inspect the screenshots, not just its exit code. A green DOM audit does not establish creative quality. For a multi-format kit or a revision after design rejection, obtain a fresh creative review and fix material findings before delivery. Assess reviewer observations against actual assets and measurements rather than accepting every aesthetic preference as a defect.

## Regression checks for future edits

- Broad campaign kit: produces distinct business jobs and composition families with static, document and playable motion outputs, subject to disclosed capability limits.
- Single chart: remains one evidence-backed chart; does not generate an ad package.
- One-format request: respects the requested scope instead of forcing the default bundle.
- Script-blocked preview: page controls still work, with a complete reading fallback; actual-host verification is not claimed from a standalone test.
- Missing video access: reports the missing motion output instead of quietly downgrading the deliverable or inventing generation success.
- Multiple brands: host chrome and ad exports retain separate brand rules; no mixed-brand creative or generated logo.
