# Verification and rendering

Lessons from eight test runs: two skills, two brands, two models. Every item below cost a real run time or produced a wrong claim.

## Seeing the work

- **Do not trust a vision model on fine geometry.** In every run the vision checker was confidently wrong at least once. It called open gaps closed, called eccentric rings "perfectly concentric", invented a vine and carved letters that were not in the pixels, and contradicted its own centring verdict between calls. Use vision for gross reads only: what letter is this, is anything clipped, is the layout broken. Settle every small-size, gap, centring and weight claim with `scripts/pixel_check.py`, which renders on white and prints an ASCII dump plus measured margins.
- **Render on white before you look.** Transparent PNGs are composited onto black by some viewers, so a black mark looks like a black square. Use `--bg "#ffffff"` for any render you inspect, and keep transparent renders for deliverables only.
- **One size per file name.** Batch renders now write `name-<size>.png`. If you use `-o`, use one folder per size; an older version silently overwrote the 512 px renders with the 16 px ones.
- **Long HTML sheets:** `render_png.py page.html` without `--height` shoots tall and trims the empty tail. Passing a small `--height` crops at the fold.
- **Lockups do not belong in square size folders.** Render them at their own aspect with `--width`.

## Renderers on Deep's Mac

- System Python has no cairosvg, so `render_png.py` falls back to headless Chrome. Chrome is slow: about 3 minutes for one batch, and it once hung a shell for 180 s. cairosvg in a venv did the same batch in 1.9 s:
  ```bash
  python3 -m venv ~/.hermes/cache/scratch/logo-venv && ~/.hermes/cache/scratch/logo-venv/bin/pip install cairosvg pillow fonttools
  export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib   # lets cairocffi find Homebrew's libcairo
  ~/.hermes/cache/scratch/logo-venv/bin/python scripts/render_png.py --which
  ```
  The scratch venv is pruned when idle. Recreate it rather than assuming it exists.
- macOS has no `timeout` command. Use Python subprocess timeouts.
- HTML screenshots always need Chrome. cairosvg cannot render HTML.

## SVG pitfalls that render differently per engine

- **cairosvg silently ignores `<mask>`.** Masked cut-outs render as solid shapes with no error. Build knockouts as compound paths with `fill-rule="evenodd"` instead. They behave the same everywhere and pass `svg_audit.py`.
- **`currentColor` renders black in cairosvg** unless the root sets `color="#HEX"`. Set it on brand-colour exports.
- **Arc flags** (`A rx ry rot large-arc sweep x y`): `0 0` is the small arc counter-clockwise, `0 1` small clockwise, `1 0` large counter-clockwise, `1 1` large clockwise. A full circle as a path needs two arcs: `M cx (cy-r) A r r 0 1 1 cx (cy+r) A r r 0 1 1 cx (cy-r) Z`.
- **Margins in `svg_audit.py` ignore transforms and stroke width.** It now says so (`geometry-approx`); measure with `pixel_check.py`.
- **Stroked finals must be expanded** to filled outlines before delivery. Note it in the report if a concept is still stroke-based.

## Before saying "done"

- Every final renders, and you have looked at the 512 px render on white plus the 16 and 32 px pixel dumps.
- `svg_audit.py` shows no FAIL on any final symbol. Lockups pass once the text is outlined (`outline_text.py`).
- No `<text>`, `<image>`, `<mask>` or filters in `final/`.
- No em or en dashes in the output folder.
- `report.md` lists what passed, what changed between iterations, every tool issue, and what was not done (trademark search, Phase 7, human redraw).
