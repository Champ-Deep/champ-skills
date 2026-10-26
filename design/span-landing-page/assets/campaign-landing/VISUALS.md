# Campaign landing visual contracts

All copy comes from site.json. Diagrams express relationships or sample structure, never invented measurements. Escape all visible strings and accessible labels. New kinds reject missing, empty or incorrectly sized fields. Required list lengths are composition constraints, not quantities being claimed.

| Kind | When to use | visualData fields | Must never claim |
|---|---|---|---|
| calls | Contrast two outreach openers | beforeLabel, before, afterLabel, after; paired asterisks mark emphasis in after | Response uplift, conversion rates or actual quotes without evidence |
| sources | Explain provenance into a record | sources list, record text, laws list | Legal compliance or verified sourcing without evidence; laws are not decorative badges |
| renewal | Show an evidenced renewal window | window list of month indices, keys list of three labels, pin text | Contract dates, renewal timing or availability without evidence |
| sample | Show a scoped sample offer | card, stamp, ticks list | Free quantity, verification or guaranteed coverage without evidence |
| roles | Relate buyer roles to company types | roles list, at text, companies list | Confirmed contacts, clients or exhaustive coverage |
| fanout | Explain vendor tools to providers to their clients | label accessible summary, tools list of four, hub text, clients list of three | Actual customer counts, named customers or guaranteed reach; repeated client nodes are illustrative |
| loop | Explain possible partner routes | label accessible summary, center text, steps list of three | Confirmed partnerships, an obligatory sequence or commercial outcomes |
| narrow | Explain targeting from broad market to event | label accessible summary, stages list of four, captions list of four | Funnel conversion, relative volumes or market size; widths are qualitative |
| anatomy | Explain fields in an illustrative record; reused in hero and FAQ | label accessible summary, title, fields list of four, pills list of three, custom, note | Real personal data, verified records, field availability for every segment |
| path | Explain a request process | label accessible summary, steps list of three | Delivery deadlines, guaranteed fulfilment or a successful submission from an unwired preview |

## Section contracts

hero.visual is an object with visual and visualData, using the static variant of the FAQ renderer. When sampleRecords exists, the masked record hero takes precedence; the original anatomy metadata remains available as a fallback. PEO/EOR retains its ticks.

picker is an optional top-level block with title, hint and a nonempty items list. Each item requires a unique lowercase id, title, text, size (lg, wide or sm) and formValue matching an existing form segment or form.specific. It uses the same 21st.dev vanilla bento engine as the count boards, with a board-local order and Reset. A tile click, Enter or Space pins one choice, sets the form, scrolls to it and focuses Requirement, or the custom field for form.specific. Tile area expresses composition, not volume. Phones stack the tiles. Reduced motion disables drag/reorder animation while selection remains operable. Pages without picker omit its markup and setup. Picker and compare may coexist without sharing reorder state.

The legacy account.diagram and picker contracts remain available and tested for existing inputs. The MSP example uses orbit instead, without a numbered legend. orbit.items requires id, title, text, icon and formValue. IDs are unique lowercase identifiers, formValue must match a form choice, and icons are allowlisted server, shield, cloud or sliders, never arbitrary SVG markup. Missing orbit omits its CSS, script and markup. Rings express categories, not coverage volume. ArrowLeft/Right cycles; Escape closes; Use this list sets and focuses the form requirement or custom field.

sampleRecords contains six fictional masked records with name, email, jobTitle, company, location, state and segment. jobTitles is the allowed title list. Identifying fields require at least three bullets and no more than three characters before a masked run. No unmasked backing values ship. The first record is the hero's initial director sample; three alternates follow every four seconds with a crossfade and Pause control. Reduced motion and static export retain the first record. The six rows share those records, full titles, per-row Segment and State. The table scrolls inside its own labeled keyboard-focusable region on narrow screens; its bottom request bar scrolls to the form without sending anything.

dossier.sheet independently opts into the sample section and requires label, hint, four fields and two chips. dossier.title labels the window; dossier.tag is the visible illustrative stamp; dossier.footer remains the coverage caveat. Without sampleRecords the six placeholder rows remain available. With records, monograms show only the first letter and sort compares the masked displayed cells, with row order as a stable tie breaker. Header hover/focus traces the column; click/Enter toggles aria-sort. Search/filter chrome remains illustrative. Pointer tilt is capped at 4 degrees with spring return; reduced motion removes tilt, sweep and shimmer but keeps column highlights.

## Interactive FAQ kinds

The five semantic kinds render interactive widgets when used in FAQ; legacy hero anatomy uses the static renderer unless sampleRecords overrides it. Each widget is an accessible group with native buttons, click and keyboard behavior, and visible focus. Widget-only motion uses 420ms cubic-bezier(.2,.9,.25,1.15); bento retains its 620ms landed ring and existing drag physics.

fanout: staggered tool nodes lift on hover/focus; selection highlights the matching curved connector and pulses the route to MSPs. loop: three selectable nodes surround a 12-second progress arc; hover/focus pauses it, reduced motion makes it static. narrow: four bands share one funnel shape; hover/focus expands a band and reveals its caption, click/Enter pins the selection. anatomy: callout buttons trace corresponding contact fields on hover/focus or selection. path: clicking any step or pressing Enter advances the illustrative three-step journey; Reset appears at the end and returns focus to the first step. No widget submits data.

The legacy calls, sources, renewal, sample and roles renderers remain available and the PEO/EOR example data is unchanged. Existing 21st.dev Dither Grid, source stack, bento boards and halftone footer ports remain in use. These semantic diagrams add no framework or runtime dependencies.
