---
name: "text-art-eggs"
description: "Make ASCII, block-letter and braille art (figlet logos, animated braille pictures, Nike-style robots.txt, humans.txt, agents.txt, console art) plus page eggs. Use for any ASCII art or easter egg."
---

# Text Art and Easter Eggs

Fun that survives as plain text: a block-letter logo at the top of robots.txt the way Nike puts one in theirs, a galloping animal drawn in braille dots, a hello in the browser console, a comment for people who view source, and a small egg on the page that sets it all off. Done well, it is the detail people screenshot and share.

## The pieces

| Piece | Where it lives | Notes |
|---|---|---|
| Block logo | robots.txt, humans.txt, agents.txt, llms.txt (inside a code block), console, view-source comment | figlet, below |
| Picture | the same files plus the page | image to braille, below |
| robots.txt | site root | logo and a one-line joke as `#` comments above the real rules, art at the bottom |
| humans.txt | site root | standard `/* TEAM */ /* THANKS */ /* SITE */` blocks, plus `/* EGGS */` listing the eggs |
| agents.txt | site root | a terminal-style card for AI agents: who, what, where to read, house rules, how to reach a human |
| llms.txt | site root | must stay valid llmstxt.org markdown: H1 first, blockquote summary, then the logo in a fenced code block is allowed |
| Console | the homepage script | `console.log` with `%c` styles, logo in two colours |
| View source | first thing after `<body>` | an HTML comment; it must never contain `--` |
| Page egg | the homepage | typed word, Konami code, a click on a brand detail, a command palette entry |

## Block-letter logos

```python
import pyfiglet                                  # pip install pyfiglet
print(pyfiglet.figlet_format('deep >_', font='dos_rebel', width=200))
```

Render the name in several fonts and pick by look: `dos_rebel` (solid blocks with a light shadow, handles lowercase), `ansi_shadow` (blocks with box-drawing shadow, uppercase only), `bloody`, `delta_corps_priest_1`, `larry3d`, `colossal`, `univers`, `doom`. Pure-ASCII fonts (`doom`, `colossal`, `univers`, `larry3d`) are the safe choice when the file cannot be served as UTF-8. For two-colour console output, find the column where the second word starts and split each line there.

## Image to braille

Braille cells hold 2 by 4 dots, so a 40 column picture is 80 dots wide. It reads like a fine halftone and animates well.

1. **Get a clean silhouette.** Use an original drawing, the user's own photo, or a public-domain image (Muybridge's 1878 *The Horse in Motion* GIF on Wikimedia Commons is 15 frames of a mare at a gallop). Threshold to a mask, remove thin vertical backdrop lines (narrow runs at least 18px tall in one column), close small gaps, and fill holes below a size limit only (filling every hole closes the gaps between legs). Fill light clothing on a rider column by column from the torso down to the next dark pixel.
2. **Scale for square dots.** At line-height 1 with a 0.6em advance, a dot is 0.3em wide and 0.25em tall, so scale height by 1.2: `h = round(H0 * w / W0 * 1.2 / 4) * 4`.
3. **Render.** Bits per cell: (0,0)=1, (0,1)=2, (0,2)=4, (1,0)=8, (1,1)=16, (1,2)=32, (0,3)=64, (1,3)=128; character = `chr(0x2800 + bits)`. Resize with LANCZOS and threshold near 0.38 so thin legs survive.
4. **Keep blanks as U+2800**, never spaces, so every line stays aligned in any font that has braille.
5. **Optional smear.** Speed streaks off the back edge: pick bands of 1 to 3 dot rows, run dots leftwards from the leftmost filled dot, about 97 percent density for the first 55 percent of the run, then thinning; shift a few bands 2 to 5 dots as torn slices. Leave room on the left (about 40 percent of the subject width).

## Animation

- Store frames as arrays of strings in a JSON file and fetch it on first use, not on page load (15 frames at 40 columns is 3KB gzipped; at 100 columns about 10KB).
- **Measure the braille font at runtime.** Braille comes from whichever system font has it, with an advance anywhere from 0.55em to 0.75em. Measure ten `U+28FF` characters in a hidden span, then set `font-size = box / (cols * advance)` and `line-height = font-size * advance * 5 / 3` so the dots keep the pitch the frames were drawn for.
- **Legs follow distance, not time.** For a run across the screen, advance the frame by distance covered (`frame = start + floor(dx / pxPerFrame) % n`), with an ease-out position, so the legs slow down as the body does. Choose `pxPerFrame` so the run lands exactly on the rest frame.
- Park clear of floating widgets: measure what sits bottom right and stop to its left.
- A speech bubble on arrival, a short credit line for any public-domain source, then fade out.
- Reduced motion: show the rest frame where she stops, no movement.

## Files and serving

- Serve every `.txt` as `text/plain; charset=utf-8`. Static hosts often send bare `text/plain`, and browsers then show block letters and braille as mojibake. On Cloudflare Workers with assets, route the `.txt` paths through the Worker (`run_worker_first`) and set the header there. Check with `curl -sI`.
- Prose in these files stays plain: straight quotes, no em or en dashes.
- Generate the files from the same data as the site where numbers appear (day count, streak) so they never go stale. Keep robots.txt hand-written: it is policy.
- Keep robots.txt rules valid: art and jokes only in `#` comment lines.

## Easter eggs on the page

- Triggers: type a word (keep the last N keys, ignore inputs and modifier keys), the Konami code, a click on a brand detail (the cursor block), a command palette entry, a custom window event so other code can fire it.
- Write the hints into humans.txt, the console message and the view-source comment, so the eggs are findable.
- Eggs are decorative: `aria-hidden`, pointer events off unless clickable, never blocking content.

## Guardrails

- Never reproduce a known character, mascot or logo in text art.
- Art from collections keeps its artist's initials (for example "jgs" on Joan Stark's pieces). Prefer original or public-domain sources, and credit public-domain sources in the file.
- No `--` inside HTML comments.
- Test every file in a browser and with curl before calling it done.