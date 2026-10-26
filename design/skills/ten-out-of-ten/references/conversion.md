# Build to convert

A visitor decides in seconds whether to stay, and in a minute whether to act. Every section answers one question they have, in this order: *What is it? Is it for me? Does it work? How? Can I trust it? What do I do now?*

## Rhythm

Plan the page as bands before writing code, e.g.:

```
dark  , nav + hero (product visual on the right)
glow  , hero fades into the brand colour: proof band (logos + one statement)
light , how it works (heading + optional video), with the flow drawn on a brand-colour panel
brand , integrations (logo tiles around the brand mark)
light , results (white cards with dark logo headers)
brand , testimonials (white cards)
dark  , client logo wall
light , why us, FAQ
brand , final CTA
dark  , footer
```

Where a band has rounded corners, the background *behind* the corners must be the colour of the next section, not black.

## Sections

### Hero
- Headline: the outcome the customer wants, ≤ 8 words. Subhead: who it's for + how, one sentence.
- Primary CTA button + the live action if the product can be tried right now. A phone number answered by the product is a **button**, not small text: "Call our AI receptionist now · 1300 XXX XXX" with a phone icon tile.
- On the right: the product working (a call card with a real-looking exchange, a dashboard screenshot, a before/after). Not stock, not an abstract 3D blob. Label nothing as "Example", it's obvious.
- A small badge above the headline with the single strongest proof point ("Trusted by 300+ local clinics"), only if it's real.

### Proof band (directly under the hero)
- A small uppercase label ("Used by clinics across Sydney") + a slow logo marquee of real clients at full legibility (logos ~56px tall on desktop).
- Then one big statement line with a rotating second half that cycles their benefits ("<Brand> answers every call. / Service calls booked into your DMS. / …"), the brand mark and the CTA again.

### How it works
- Heading + one-paragraph explanation on the left; if they have an explainer video, put it on the right as a click-to-load thumbnail with a play button (never an autoplay iframe in the first view).
- The mechanism drawn on a brand-colour panel: source (icon chip) → the product (brand mark) → destinations (white cards with an icon tile, a title, and the real logos of the systems it plugs into, in an equal-column grid so logos line up). Animated dots travelling along the lines are good; dots must stay round (draw the SVG in real pixels, never `preserveAspectRatio="none"` with circles in it).
- Below: one line per route/step with an icon, the bold result and a sentence of detail.
- On phones: stack it, and let logo grids span the full card width so logos stay legible.

### Integrations / partners
- Grouped logo tiles (e.g. "CRM" | brand mark hub | "Calendar & booking"), groups aligned to the same top line. Notes ("Certified partner") go under the whole grid, not under one column.

### Results
- One card per case study: a dark header strip with the client's logo + "Case study ↗" link, the headline result as a sentence, then 2-3 stats (icon tile + big mono number in the brand colour + a short label).
- Smaller cards for extra one-line results, each with an icon.

### Testimonials
- White quote cards on the brand band: a quote glyph, the quote verbatim, then name, role, company with a face or the company logo.

### Logo wall
- If they have many clients: a big real number ("100+") + a grid of every logo on dark. Biggest single proof point on the page.

### Why us
- 3 differentiators, each an icon tile + bold claim + one sentence. Use an asymmetric layout or a list, not three identical cards.

### FAQ
- Their real questions, accordion, brand-colour toggles. These also become FAQPage JSON-LD (see `aeo.md`).

### Final CTA
- Brand band, brand mark, the closing promise as a two-line headline (second line in a lighter tint), one sentence on what happens when they click, primary CTA + the live action.

### Footer
- Logo, one-line description, phone (tap-to-call link), address, menu and legal links with ≥ 44px tap targets on phones.

## Copy pass

After the build, read every line as the visitor:
- **Lead with the pain** (from Person / Pain / Promise in `facts.md`), then the promise. Concrete scenes beat claims: "It's 9pm and a customer calls about a service" beats "24/7 availability".
- **One ask per screen.** Button text says what happens next ("Book a 15-minute call", not "Get started").
- **Strip AI tells** from the copy (see `taste.md` § AI tells) and anything a competitor could also say word for word.
- Every claim still traces to `facts.md`. Show the user the rewrite as a before/after diff of the lines that changed.

## CTA rules

- One primary action, same words everywhere.
- Repeat it: hero, after the proof statement, mid-page, final band, nav.
- Phone numbers are always `tel:` links. If the business publishes a phoneword (like 1300 FIX NOW), confirm the digits with the owner; don't guess them silently.
- The nav on phones keeps the primary CTA visible next to the menu button, and the menu includes the live action.
