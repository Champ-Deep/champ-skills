# Logo Usage Guidelines

## Logo Versions

The Lake B2B logo consists of an icon (data dots forming a head/brain pattern) and wordmark.

### Approved Color Variations

1. **Full Color on White/Light** - Primary usage
2. **Full Color on Purple (#6D08BE)** - Dark background
3. **Full Color on Navy (#011A6B)** - Dark background
4. **Full Color on Light Gray** - Neutral background

## Size Specifications

### Minimum Sizes

| Context | Minimum Width |
|---------|---------------|
| Digital | 180px |
| Print (general) | 30mm |
| A5 documents | 30mm |
| A4 documents | 40mm |
| A3 documents | 55mm |

### Clear Space

Maintain clear space equal to the width of the letter "B" in the logo on all sides. This ensures the logo has room to breathe and maintains visual impact.

## Logo Placement on Images

### Do's

- Place on clear areas of images (corners, open spaces)
- Use on darker images with brand color overlays
- Ensure sufficient contrast between logo and background
- Apply curved line graphic elements as framing devices

### Don'ts

- Never place on busy/cluttered image areas
- Never place where logo elements get lost in background details
- Never place on backgrounds with competing colors
- Never reduce contrast to the point of illegibility

## Prohibited Modifications

1. **Altered color** - Never change the gradient or individual colors
2. **Altered font** - Never substitute the Montserrat typeface
3. **Skew/manipulation** - Never stretch, rotate, or distort
4. **Rearrangement** - Never separate or reposition icon and wordmark
5. **Special effects** - Never add shadows, glows, outlines, or 3D effects
6. **Brand merging** - Never combine with other company logos
7. **Inappropriate backgrounds** - Never use on clashing colors (orange, red, bright backgrounds)
8. **Busy backgrounds** - Never use on complex patterns or detailed imagery

## Logo File Formats

Use appropriate file formats:
- **Digital/Web:** PNG (transparent background), SVG
- **Print:** PDF, EPS, AI
- **Presentations:** PNG (high resolution)

## Logo files in this skill

| File | Size | Use |
|---|---|---|
| `assets/LakeB2B_Logo_Transparent.png` | 2042 x 579, transparent | master for decks, documents, print-ready PDFs and anything that needs to scale |
| `assets/LakeB2B_Logo_Transparent_720.png` | 720 x 204, transparent, about 60KB | web pages and single-file HTML on white or light grounds (sharp at 180 to 360px wide on retina screens) |
| `assets/LakeB2B_Logo_Reversed.png`, `assets/LakeB2B_Logo_Reversed_720.png` | master and web, transparent | dark grounds: white wordmark with the full-colour mark and B2B (brand book page 5, navy panel) |
| `assets/LakeB2B_Logo_White.png`, `assets/LakeB2B_Logo_White_720.png` | master and web, transparent | purple and brand-gradient grounds: all-white logo (brand book page 5, gradient panel) |

Both are cropped tight to the artwork with a small margin; add the clear space (width of the letter B) in layout, not in the file. Vault copies live at `Atlas/Context Docs/Lake B2B/Brand Assets/` in the Celsus vault. The older `LakeB2B_Logo_Square.png` has a white box baked in and is low resolution; do not use it for new work.

## Logo on the web

- Embed the 720px PNG as a base64 data URI in single-file pages and Artifacts, set `width="180"` (or larger) and `height` in proportion (3.53 to 1), and give it `alt="LakeB2B, Enabling Growth"`.
- Pick the version by the ground behind it: full colour on white or light grey, reversed on navy and dark heroes, all-white on purple and the brand gradient. Keep the clear space (16px or more around a 180px logo).
- Never box the full-colour logo in a white panel to sit on a dark ground; use the reversed file instead.
- A nav that starts over a dark hero and turns light on scroll carries both files and swaps them with a class (see the `showcase-page` kit).
- Never recolour with CSS filters, never invert it for dark mode, never animate the logo itself.
- Keep it at 180px or wider on every breakpoint, including phones.
