# UI polish conventions (ui/)

The shape a polish pass should converge on, so a later pass extends it instead of
introducing a second system. Measurements are the values shipped in `ui/src`.

## Button hierarchy

| Tier | Treatment | Used for |
|---|---|---|
| Primary | solid brand fill, e.g. green | the one true action per view: Connect, Build question, Send |
| Secondary | one tonal fill, soft tint on press, **no hairline outline** | Answer settings, New search, Reset, Find / Compare, Copy, admin ghost buttons |
| Tertiary | text or icon only | inline affordances inside a card |

Hairline grey outlines around secondary buttons read as a second, weaker system and
are the thing a polish pass removes. One tonal fill for every secondary control beats
per-button invention.

## Search surfaces are one pill

Every search entry point shares the pill: leading spark icon, fully rounded shape,
round arrow send on the right. That means the hero input, the header `Search or ask`
trigger, and the answer-page follow-up composer. A boxed trigger or a rectangular
composer is the failure mode, because the hero is the page the user sees first.

Mobile: keep the placeholder short enough to sit between the icons at 390px, and keep
the send target at 44px.

## Theme rules: outline in light, tonal in dark

The two themes carry hierarchy differently, and forcing one treatment across both is
the failure mode.

- **Light**: hairline borders and hard fills read as intentional, retro-brutalist
  craft. Buttons keep their visible outline; this is the look Deep keeps.
- **Dark**: opaque grey hairlines around every card and control make the page read as
  grey-outlined and cheap, which is exactly the premium feel a polish pass is meant to
  create. Replace `--line` with a translucent, accent-tinted hairline (e.g.
  `rgba(166,227,191,.11)` on the green system) and lift surfaces one step so cards
  separate by tone, not by stroke. Buttons drop the outline for a single tonal fill.
- Check the computed colour in both themes before shipping: a line token that is right
  in light will be wrong in dark unless it is declared per `data-theme`.

## Page frame

- Feed max width about 1320px with a fluid gutter shared by header, feed, composer and
  the connect panel, so nothing sits on a different vertical line.
- Hero gap wider than the default grid gap; section rhythm around 44px.
- Answer pages: the asked question is the page title (heading weight, near the top),
  not a small muted line above the content.
- Insight cards, callouts and list requests carry no coloured left stripe. The meter or
  the fill already encodes tone, and the stripe is the second redundant signal.

## Audit triage: FAILs that are not defects

`audit.py` reports per element, so read the element before judging a FAIL:

| Report | Usually means |
|---|---|
| contrast 1:1 on a gradient-filled label (e.g. a status word inside the 21st orb) | the checker reads the clipped gradient stop, not the rendered colour. Cosmetic, pre-existing |
| tap-target reported at exactly 44x44 | rounding on a subpixel border box. Not a real miss |
| ios-zoom on a `select` under 16px at 390 | real. Bump the font in the mobile breakpoint |
| flex-truncation warning on a heading | real only if the label is clipped in the screenshot; otherwise the element just lacks `min-width: 0` |

Report every remaining FAIL as pre-existing with its element name when it is not from
the change, and fix the one-line ones (a font size) while you are there.
