# Dopamine sites: the toy microsite genre

Deep's name for a class of single-purpose brand microsite: one screen, one toy, no
conversion goal, built to be shared. Use this when he asks for a "dopamine site" or a
playful brand toy for any Champions brand.

## The contract

| Property | Rule |
|---|---|
| Loop | Playable in 10 s with no instructions; a full loop 30 to 90 s ending in a result worth screenshotting |
| Conversion | None. No lead form, no email capture, no pricing, no sales copy. The only brand touch is the look, the name and a small footer link to the brand's real site (omitted rather than guessed if the brand skill has no URL) |
| Feedback | Every action gets instant weighted response: motion, an optional sound (off by default, toggle present), `navigator.vibrate` where supported |
| Result | A generated PNG result card (canvas) through the Web Share API with a download fallback, plus OG image and meta so links unfurl |
| Data | Every person, company and number is fictional, generated client side, and labelled as fictional. No real PII. These brands sell data; a toy leaking a real contact is the worst possible failure |
| Privacy | No analytics, cookies, backend, API keys or third-party calls beyond fonts |
| Access | Keyboard playable, `prefers-reduced-motion` gives a calm but working version, 4.5:1 contrast |
| Budget | JS under 250 KB gzipped, 60 fps on a mid-range phone |
| Taste | `ten-out-of-ten` `references/taste.md`. "Dopamine" means saturated brand colour bands, bouncy physics and satisfying micro-feedback, never neon glow, gradient text or purple AI gradients |
| Brand | Load the brand skill. Real logo assets where they exist, otherwise a typeset wordmark. Never invent a logo |
| Hosting | Cloudflare Workers static assets on `<slug>.deep-ae0.workers.dev`. Custom brand domains are a DNS change on a brand domain: stage as a `needs_input` card, never do it unprompted |

## Spec shapes that have worked

- LakeB2B, fishing: cast and reel tension minigame, each catch flips into a fictional
  buyer trading card with rarity tiers from the brand palette, collection persisted in
  localStorage, share line "I landed a <rarity> <role>".
- SPAN, bridge puzzle: daily date-seeded grid, place beams under a budget, physics
  decides hold or collapse, shared as a Wordle-style grid. Bridge matches "span".
- Ampliz, rhythm: ECG trace, tap on beat, streaks, flatline fail state, peak BPM on the
  share card. Copy makes no health or medical claims.
- MetricFox, endless runner: the terrain is a line chart drawing itself, and the score
  card redraws the run as a chart.
- Champions Club, slot machine: three reels (place, ride, company), heavy pull lever,
  gold jackpot confetti, result becomes a postcard. No prices, offers or availability
  claims anywhere.

The metonym matters: when a brand has a family (Champions Club with Ranch and Yacht),
fold the family members into one toy as places inside the umbrella, not one card each.

## Building a family of them

Fan out as parallel frontend cards from one shared spec file using the
`kanban-task-intake` skill's `references/parallel-fan-out.md`, plus one review card
parented to all of them. Brief shape: `model-routing`
`references/frontend-brief-template.md`.
