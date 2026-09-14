# Design Guardrails — No AI Slop

Derived from impeccable.style's detector rules and anti-patterns, adapted for this skill's three surfaces: PPTX decks, HTML artifacts, and Higgsfield image prompts. Read fully before generating anything. These rules exist because every model trained on the same SaaS templates produces the same tells; a client-facing sales asset that looks AI-generated undercuts the exact "precision" story we are selling.

## The banned tells (all surfaces)

1. **No purple-to-blue gradients.** The single biggest AI tell. If the brand palette is purple (LakeB2B), use it flat and confident, never as a soft gradient wash.
2. **No default fonts as the design.** Inter, Arial, and system stacks read as unstyled. Pick a deliberate pairing (a characterful grotesk for headlines + a workhorse for body, or a serif/sans pairing). In decks, Montserrat is already wired in; don't add Inter on top.
3. **No gray text on colored backgrounds.** Text on any non-white background must be explicitly white/light and contrast-checked. (Also a standing house rule.)
4. **No pure black or pure gray.** Always tint toward the brand hue (e.g. `#1A1030` not `#000000`).
5. **No cards nested inside cards.** One level of containment. If a card needs a card, the layout is wrong.
6. **No rounded-square icon tile above every heading.** Vary section anchors: numbers, rules, color blocks, photography.
7. **No bounce/elastic easing** in the HTML walkthrough or any animation. Ease-out, fast, purposeful.
8. **No dead centered-column layouts** for long content. Use active whitespace: asymmetric grids, marginalia, a sticky context rail.
9. **No section-number mono tags** ("§ 01/02"). Use content-derived labels.
10. **No em dashes in any copy.** Periods, commas, colons, or restructure.

## Image prompt rules (Higgsfield / Mode A)

Every prompt must specify, explicitly:

- **A photographic or editorial art direction** ("editorial industrial photography, raking studio light, cinematic depth of field"), never just "professional image of X". Undirected prompts return the median training image, which is the definition of slop.
- **A palette** tied to the subject and brand, and the negative: "NO purple gradients, NO generic tech glow, no cartoon 3D".
- **Headline text 12 words or fewer**, quoted exactly, with placement ("bold white grotesk headline top left"). Longer text garbles.
- **Brand wordmark line** (bottom left) and a **"Concept sample" label** (bottom right) on every client-facing mockup. Never strip the label to make the image look cleaner.
- **One idea per image.** The concept (from the playbook's visual spec) is a single visual metaphor, not a collage of dashboards.

Reject-and-regenerate triggers on review: garbled or misspelled text, extra limbs/logos, watermark-like artifacts, purple gradient backgrounds that ignored the negative, missing sample label, visual concept drifted from the brief.

## Deck rules (Mode B)

- Palette changes happen ONLY in the constants block of `generate_deck.js`. Never invent a palette for an unconfirmed brand.
- Left-rail number/title/description + right-side sample card + "why it works" callout is the system; don't add new slide archetypes ad hoc.
- Every number that isn't verified carries its "Illustrative" flag on the slide itself, not just in speaker notes.
- Run pptx validation + slide-image visual review before presenting. No exceptions under deadline pressure.

## HTML rules (walkthrough or one-pagers)

- Mobile-first CSS; executive assets get read on phones.
- Self-contained single file, no external dependencies beyond approved CDNs.
- Contrast-check every text/background pair, especially on brand-colored panels.
- CTAs carry UTM parameters (source/medium/campaign/content) when linking to LakeB2B properties.

## Pre-ship checklist

- [ ] Zero purple-blue gradients anywhere
- [ ] Typography is deliberate (named pairing, real hierarchy, no default-font body)
- [ ] All text on colored/dark backgrounds is explicitly light + contrast-checked
- [ ] No nested cards, no icon-tile-per-heading monotony
- [ ] Every unverified number labeled Illustrative/Estimated/Sample
- [ ] Every client-facing mockup carries brand wordmark + "Concept sample"
- [ ] No em dashes in any copy
- [ ] Images visually reviewed at full size; decks reviewed slide-by-slide as images
- [ ] The asset would not embarrass us printed on paper next to the client's own brand book
