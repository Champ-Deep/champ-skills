# Taste rules

The floor for every build. Other design skills can raise it; nothing lowers it.

## AI tells (never ship these)

- Inter, Roboto, Arial or system-ui as the only typeface.
- A purple/blue gradient hero, neon glows, glowing orbs behind the headline.
- Gradient-filled headline text.
- Everything centred, every section the same width and rhythm.
- The main features as three identical cards in a row, each with an icon on top.
- Emoji as icons (🚀 ✅ ⚡) in UI, buttons or headings.
- Generic avatars (egg silhouettes, initials in circles) standing in for real people.
- Round, invented-looking stats (10x, 99.9%, 500+ happy customers) the business never published.
- Filler copy: "elevate", "seamless", "unleash", "next-gen", "revolutionise", "supercharge", "in today's fast-paced world".
- Pure black (#000) backgrounds or pure grey (#888) body text.
- Stock photos of people pointing at laptops.

## Type

- One characterful sans for the whole site (e.g. Geist, Satoshi, DM Sans, Manrope, Outfit, General Sans), weights 400/500/600/700. Serif only for editorial brands.
- Choose it on purpose: shortlist 3 pairings that fit the brand (Fontshare, Google Fonts, Fonts In Use for real-world examples), say why each fits, and check the licence allows commercial web use. If a CDN won't load, use the closest Google Fonts match and note the swap.
- A monospace (Geist Mono, JetBrains Mono) for numbers, times, phone numbers and small uppercase labels, so figures line up like a spec sheet.
- Headlines bold and tight (letter-spacing around -0.03em to -0.04em, line-height ~1.02-1.1). Control hierarchy with weight and colour as much as size.
- Body 16-18px, line-height 1.5-1.7, max ~65 characters per line, muted ink (not grey-400).
- `text-wrap: balance` on headings.

## Colour

- Build from the logo. One accent family: brand, deep, soft tint, light tint for text on dark.
- Use the brand colour as full-width bands (see `conversion.md` § rhythm), not just on buttons.
- Neutral base tinted toward the brand (warm or cool, never both). Off-black for dark sections.
- Success green only for success states. Never two accent hues fighting each other.
- 4.5:1 contrast for text; check text on the brand band.

## Layout

- Left-aligned headlines over asymmetric grids for most sections; centre only short statement sections (proof line, final CTA).
- Vary the rhythm: a wide lead + narrow column, a diagram, a card grid, a logo wall, a list. No two consecutive sections with the same shape.
- Max content width ~1200px with 16px side gutters on phones.
- Cards only where elevation means something (results, quotes, destinations in a flow). Separate the rest with space or hairlines.
- Consistent radii: small for controls (8-10px), large for panels (16-28px), pill only for status chips.

## Icons & logos

- One line-icon set (Lucide/Phosphor style), one stroke width (1.5-2), sized 16-20px, `currentColor`.
- Every scannable item gets an icon cue: steps, stats, promises, routes.
- Real logos for every client, partner, integration and tool named. White logos on dark tiles, or full-colour on white tiles, never a washed-out low-opacity filter that makes them unreadable.
- Logos with built-in padding: crop the padding so they size consistently.

## Motion

- Only where it explains something: a call card typing out, calls travelling along a flow line, a logo marquee, a stat counting up.
- **No scroll-linked motion.** No parallax, pinned or scroll-scrubbed sections, word-by-word text reveals, cards that stack as you scroll, or content that fades in on scroll. It looks great in a demo and annoys a visitor who just wants the answer: it slows reading, fights the scroll wheel, and leaves blank frames for anyone scrolling fast. Content is visible the moment it's on screen.
- 150-300ms for interactions, transform/opacity only, `prefers-reduced-motion` respected.
- No custom cursors.
