#!/usr/bin/env python3
"""Measure a logo from its pixels, not from a vision model's impression of them.

Renders each SVG on white with render_png.py, then reports what is really on the canvas:
  - an ASCII dump at small sizes (default 16 and 32 px): '#' solid ink, '+' partial, '.' blank,
    so you can see whether gaps stay open and counters survive
  - ink bounding box margins and centring offset measured at 256 px (transforms and strokes included)
  - ink coverage and the centre of mass offset (optical weight)

Why: in every test run the vision model was confidently wrong about fine geometry (called open gaps closed,
eccentric rings concentric, invented details). Use vision for gross reads only and this for small-size claims.

Usage:
  python3 scripts/pixel_check.py mark.svg [more.svg ...]
  python3 scripts/pixel_check.py mark.svg --sizes 16 24 32 --out-dir renders/pixel
  python3 scripts/pixel_check.py mark.svg --json

Needs Pillow (pip install pillow) and any render_png.py backend.
"""
import argparse
import json
import os
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_png  # noqa: E402

MEASURE = 256


def ink_grid(png, thresh=40):
    """Return (w, h, grid) with grid[y][x] = ink amount 0..255 (distance from white)."""
    from PIL import Image  # type: ignore
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = im.load()
    def ink(p):
        v = (765 - sum(p)) // 3  # 0 white .. 255 black
        return v if v * 3 > thresh else 0
    return w, h, [[ink(px[x, y]) for x in range(w)] for y in range(h)]


def ascii_dump(grid):
    return "\n".join("".join("#" if v >= 160 else "+" if v > 0 else "." for v in row) for row in grid)


def measure(grid, w, h):
    ys = [y for y in range(h) if any(grid[y])]
    xs = [x for x in range(w) if any(grid[y][x] for y in range(h))]
    if not ys:
        return {"empty": True}
    total = sum(sum(r) for r in grid)
    cx = sum(x * v for row in grid for x, v in enumerate(row)) / total
    cy = sum(y * v for y, row in enumerate(grid) for v in row) / total
    m = {"left": xs[0], "right": w - 1 - xs[-1], "top": ys[0], "bottom": h - 1 - ys[-1]}
    return {
        "margins_px": m,
        "bbox_offset_pct": {"x": round(100 * (m["left"] - m["right"]) / 2 / w, 1),
                            "y": round(100 * (m["top"] - m["bottom"]) / 2 / h, 1)},
        "mass_offset_pct": {"x": round(100 * (cx - (w - 1) / 2) / w, 1), "y": round(100 * (cy - (h - 1) / 2) / h, 1)},
        "coverage_pct": round(100 * sum(1 for row in grid for v in row if v) / (w * h), 1),
    }


def check(svg, sizes, out_dir):
    res = {"file": svg, "dumps": {}}
    for s in sorted(set(sizes + [MEASURE])):
        png = os.path.join(out_dir, f"{os.path.splitext(os.path.basename(svg))[0]}-{s}.png")
        if not render_png.render(svg, png, s, s, bg="#ffffff"):
            raise RuntimeError(f"could not render {svg}; see render_png.py --which")
        w, h, grid = ink_grid(png)
        if s == MEASURE:
            res.update(measure(grid, w, h))
        if s in sizes:
            res["dumps"][s] = ascii_dump(grid)
    flags = []
    if res.get("empty"):
        flags.append("FAIL empty: nothing rendered")
    else:
        b, mo = res["bbox_offset_pct"], res["mass_offset_pct"]
        if abs(b["x"]) > 2 or abs(b["y"]) > 2:
            flags.append(f"WARN off-centre: ink box offset x {b['x']}%, y {b['y']}% of canvas")
        if abs(mo["x"]) > 4:
            flags.append(f"INFO weight pulls {'right' if mo['x'] > 0 else 'left'} ({mo['x']}%): intentional?")
        if min(res["margins_px"].values()) < MEASURE * 0.04:
            flags.append("WARN tight: ink within 4% of the canvas edge, will crowd in app-icon masks")
    res["flags"] = flags
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--sizes", nargs="*", type=int, default=[16, 32])
    ap.add_argument("--out-dir", help="keep the white renders here (default: temp, deleted)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        import PIL  # type: ignore  # noqa: F401
    except Exception:
        sys.exit("pixel_check.py needs Pillow: pip install pillow")
    tmp = None if a.out_dir else tempfile.mkdtemp(prefix="pixel-check-")
    out_dir = a.out_dir or tmp
    os.makedirs(out_dir, exist_ok=True)
    results = [check(f, a.sizes, out_dir) for f in a.files]
    if a.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"== {r['file']}")
            if not r.get("empty"):
                print(f"margins @{MEASURE}px {r['margins_px']}  ink box offset {r['bbox_offset_pct']}  "
                      f"mass offset {r['mass_offset_pct']}  coverage {r['coverage_pct']}%")
            for s, d in r["dumps"].items():
                print(f"-- {s} px\n{d}")
            print("\n".join(r["flags"]) or "no flags")
    if tmp:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if any(f.startswith("FAIL") for r in results for f in r["flags"]) else 0


if __name__ == "__main__":
    sys.exit(main())
