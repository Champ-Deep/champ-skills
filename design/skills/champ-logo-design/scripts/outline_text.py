#!/usr/bin/env python3
"""Outline text to SVG paths so lockups and wordmarks never depend on installed fonts.

Finished marks must not contain <text> (svg_audit.py fails them). This turns a word set in a real font file
into path data, with variable-font axes, kerning-free advance widths and optional letter-spacing.

Usage:
  python3 scripts/outline_text.py Outfit.ttf "IP Momentum" -o wordmark.svg --size 120 --fill "#0E1A33"
  python3 scripts/outline_text.py "Manrope[wght].ttf" recruitChamp --axis wght=800 --tracking -2 -o wm.svg
  python3 scripts/outline_text.py Font.ttf Word --d-only      # print just the path d, to paste into a lockup

Fonts: use an OFL or other logo-safe licence. Google Fonts variable files live at
https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<File>[axes].ttf . Record the font and licence.
Needs fontTools (pip install fonttools).
"""
import argparse
import math
import sys


def outline(font_path, text, size, axes=None, tracking=0.0):
    """Return (path_d, width, ascent, descent) in px for text set at `size` px."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    font = TTFont(font_path)
    if axes:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, axes)
    upm = font["head"].unitsPerEm
    s = size / upm
    cmap, glyphs, hmtx = font.getBestCmap(), font.getGlyphSet(), font["hmtx"]
    ascent, descent = font["hhea"].ascent * s, -font["hhea"].descent * s
    # shortcut: no GPOS kerning or ligatures; fine for display words, upgrade to uharfbuzz for body text or scripts
    x, parts = 0.0, []
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise SystemExit(f"glyph for {ch!r} not in {font_path}")
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, ascent)))
        parts.append(pen.getCommands())
        x += hmtx[name][0] * s + tracking
    return " ".join(p for p in parts if p), x - tracking, ascent, descent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("font")
    ap.add_argument("text")
    ap.add_argument("-o", "--out", help="write a standalone SVG fitted to the word")
    ap.add_argument("--size", type=float, default=100, help="font size in px (default 100)")
    ap.add_argument("--axis", action="append", default=[], help="variable axis, e.g. wght=800 (repeatable)")
    ap.add_argument("--tracking", type=float, default=0.0, help="extra px between letters (negative tightens)")
    ap.add_argument("--fill", default="#000000")
    ap.add_argument("--d-only", action="store_true", help="print only the path d")
    a = ap.parse_args()
    try:
        import fontTools  # noqa: F401
    except Exception:
        sys.exit("outline_text.py needs fontTools: pip install fonttools")
    axes = {k: float(v) for k, v in (x.split("=", 1) for x in a.axis)}
    d, w, asc, desc = outline(a.font, a.text, a.size, axes or None, a.tracking)
    if a.d_only:
        print(d)
        return 0
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {math.ceil(w)} {math.ceil(asc + desc)}">'
           f"<title>{a.text}</title><path fill=\"{a.fill}\" d=\"{d}\"/></svg>\n")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"wrote {a.out}  {w:.0f}x{asc + desc:.0f}px, {len(a.text)} glyphs, no <text>")
    else:
        sys.stdout.write(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
