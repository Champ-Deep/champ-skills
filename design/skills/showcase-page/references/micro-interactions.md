# Micro-interactions

Small responses to a hover, focus, tap or scroll that tell the reader the page is alive and built with care. Source library: MicroKit UI (github.com/henriquegpb/microkit, MIT, 49 interactions, CSS and Tailwind variants, shadcn registry `@microkit`). Second source: 21st.dev for larger interactive components. The kit already ports the ones below to vanilla CSS and JS in `core.css` and `core.js`.

## The rules

1. Every interactive element gets a hover state, a `:focus-visible` state that matches it, and a touch equivalent where hover carries meaning.
2. One micro-interaction per element. A button can swap its label and slide its arrow, which reads as one gesture; it does not also bounce, glow and shake.
3. Durations 200 to 500ms, `cubic-bezier(.16,1,.3,1)`. Loops only while hovered.
4. Colours come from the brand. MicroKit's orange accents become the brand primary or gold.
5. Respect `prefers-reduced-motion` and the static export mode; every micro-interaction degrades to a plain colour change.
6. Tap targets stay 44px or more after any scale change.
7. Credit the source in a CSS comment.

## Ported set (in the kit)

| Element | Interaction | MicroKit source | Kit class |
|---|---|---|---|
| Primary buttons | label rises out as an identical copy rises in | project-text-swap-button | `.btn .swap > .cur + .inc` (build with `swap()` in build.py) |
| Arrow squares | arrow slides out right as a second arrow slides in from the left | projects-arrow-button | `.btn .arr > i + i` |
| Dark and light CTAs | two brand-coloured blurred glows follow the pointer across the button | whats-new-glow-button | `.mk-glow > .gl.a + .gl.b`, JS sets `--gx` |
| Ghost button on gradient | a conic highlight traces the border while hovered | subscribe-shine-button | `.mk-shine` |
| Step lists | a glowing brand rail slides to the step nearest the reading line; that step's title takes the brand colour | spotlight-indicator | `.steps` (JS appends `.rail`, toggles `.active`) |
| Pills and chips | lift 2px, brand rail grows across the top edge | social-highlight-cards | `.pill`, `.tag:hover` |
| Floating stat cards | perspective tilt toward the pointer with a lavender sheen; touch-hold works on phones | 21st.dev Optimized Tilt Card (27139) | `.fcard`, JS sets `--rx`, `--ry`, `--px`, `--py` |
| Panels and `.gc` cards | soft spot under the pointer and a lit hairline ring that also brightens on neighbouring cards | 21st.dev spotlight-card (GlowCard), vanilla port | `.panel`, `.gc`; JS sets `--gc-x`, `--gc-y`, `--gc-xp`; see `spotlight-card.md` |
| Sortable tables | rows glide to their new position, the sort arrow flips | 21st.dev Sortable Data Table (35036) | `table.data[data-sortable]` (FLIP in JS) |
| Table rows | brand accent bar appears on the first cell | spotlight-indicator, simplified | `table.data tbody tr:hover` |
| Heat tiles, unit dots | lift and scale on hover, risk outline intensifies | none | `.tile:hover`, `.udots i:hover` |
| Map bubbles | ring springs outward | none | `.map .bub:hover .ring` |
| Panels | shadow deepens toward the brand colour | none | `.panel:hover` |

## Worth adding when the page has the element

| Element | MicroKit item | Notes |
|---|---|---|
| Tabs | sliding-underline-tabs, sliding-content-tabs | underline glides between labels |
| Contact or email CTA | contact-details-reveal, contact-underline-button | show the address as selectable text, not only a mailto |
| Number input | scrub-number-field | calculators and ROI tools |
| Text link "read more" | read-more-swap, pricing-slide-link | arrow swaps sides |
| Newsletter or download | aurora-download-button, floating-newsletter-button | one per page at most |
| Menu | blur-glide-menu | multi-level nav only |

Install the original with `npx shadcn@latest add @microkit/<name>` in a React project, or copy the CSS variant from microkit.co and port it to the kit's tokens for a single-file page.

## Behaviour rules (interior.dev)

The table above covers looks. Behaviour under repeat input is a separate requirement: what happens on a second click mid-animation, on a blocked clipboard, on keyboard alone, and under reduced motion.

1. Reserve the space a stateful control will occupy. Stack every label variant in one grid cell and fade between them, so a button that changes its label never reflows the row.
2. Retarget, never restart. A second action mid-animation aims the motion at the new target from where it is; nothing gets stuck half-transitioned.
3. State without motion: every animation carries its meaning in text and `aria-*` too, so removing the transition removes only the travel.
4. Explicit error state plus a fallback path for anything that touches the clipboard or the network. A silent no-op is a broken control.
5. One timer for transient states, restarted by a repeat action.
6. `role="radiogroup"` with `aria-checked`, one tab stop, Arrow keys, Home and End for any grouped choice control.
7. Announce results to a polite live region: the filtered count, the copy result.
8. The rail's reading line must travel with scroll progress to the viewport bottom, or a short final section can never win the highlight.
9. A clicked rail or nav link keeps its highlight until the scroll lands or the user wheels away, or it flickers through every section it passes.

The vanilla CSS and JS for the copy button (reserved width, error state), the segmented control (clipped travelling thumb, roving focus, live count) and scroll spy, plus the assertion recipe for each, live in `design/skills/frontend-design/reference/interior-rules.md`. Use those ports instead of ad hoc ones, and run the recipe as console probes in Step 6: geometry against the selected button at every width, clicks in rapid succession, the forced failure, and a reduced-motion pass. A control that looks right in a screenshot can still fail all four.
