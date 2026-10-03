import math
#!/usr/bin/env python3
"""
Squarified treemap, straight from Bruls/Huizing/van Wijk 2000.

The recursion invariant that matters:
    the free rectangle is always the one NOT yet filled
    w >= h  ->  take a COLUMN of items, full height h, stacked left to right
                leftover is a narrower rectangle on the RIGHT
    h >  w  ->  take a ROW of items, full width w, stacked top to bottom
                leftover is a shorter rectangle BELOW

Row thickness when filling a column:  t = sum(areas) / h
Item width when filling a column:   w_i = area_i / t

That is the whole algorithm. The earlier version used min(w,h) as the side in both
worst() and place(), which collapsed every layout into a single full-height column.
"""


def _worst(row, side):
    """
    Worst aspect ratio if `row` (list of areas) is laid across a side of length `side`.

    Strip thickness t = sum(row) / side. Each item then occupies t along the side and
    area_i/t across it, so its aspect ratio is:

        max( (side/t) * sqrt(area_i / amax),
            (t/side) * sqrt(amax / area_i) )

    summed as the max over the row. Adding an item to the row makes t grow, which can
    improve every ratio; the row is extended while that keeps helping.
    """
    s = sum(row)
    if s <= 0 or side <= 0:
        return float("inf")
    t = s / side
    amax = max(row)
    worst = 0.0
    for a in row:
        worst = max(worst,
                    max((side / t) * math.sqrt(a / amax),
                        (t / side) * math.sqrt(amax / a)))
    return worst


def squarify(values, x, y, w, h):
    """
    values: sequence of non-negative numbers (area weights).
    Returns [(index, x, y, w, h)] which tile [x, x+w] x [y, y+h] exactly.
    """
    items = sorted(((i, float(v)) for i, v in enumerate(values) if v and v > 0),
                   key=lambda t: -t[1])
    out = []
    if not items or w <= 0 or h <= 0:
        return out

    scale = (w * h) / sum(v for _, v in items)
    items = [(i, v * scale) for i, v in items]

    def rec(seq, x, y, w, h):
        """
        Fill the free rectangle (x, y, w, h). Take the first strip, lay it, recurse on the
        remainder. When w >= h the strip is a column of full height; otherwise a row of full
        width. The strip thickness is sum(area)/h or sum(area)/w respectively, so the items
        exactly fill the strip and the leftover rectangle has exactly the right area.
        """
        if not seq or w <= 0 or h <= 0:
            return
        column = (w >= h)
        side = h if column else w          # the long edge the strip spans

        row, i = [], 0
        while i < len(seq):
            trial = row + [seq[i]]
            if not row or _worst([a for _, a in trial], side) <= _worst([a for _, a in row], side):
                row = trial
                i += 1
            else:
                break
        # if nothing fitted (pathological first item), take one anyway
        if not row:
            row, i = [seq[0]], 1

        # Strip thickness t = sum(row)/side. Each item spans the FULL side (h for a column,
        # w for a row) and covers its own area, so its extent along the strip is
        # area_i / side -- NOT area_i / t. Those sums to exactly t.
        #
        # Float division leaves the last item a few ulps too wide, which shows up as an
        # OVERFLOW of ~1e-14 against the box. Snap the final item to the remaining space so
        # the tiling is exact rather than merely close.
        if column:
            cx = x
            for k, (idx, a) in enumerate(row):
                last = (k == len(row) - 1) and i == len(seq)
                iw = (x + w - cx) if last else a / h
                if iw < 0:
                    iw = 0.0
                out.append((idx, cx, y, iw, h))
                cx += iw
            rec(seq[i:], cx, y, x + w - cx, h)
        else:
            cy = y
            for k, (idx, a) in enumerate(row):
                last = (k == len(row) - 1) and i == len(seq)
                ih = (y + h - cy) if last else a / w
                if ih < 0:
                    ih = 0.0
                out.append((idx, x, cy, w, ih))
                cy += ih
            rec(seq[i:], x, cy, w, y + h - cy)

    rec(items, x, y, w, h)
    return out


if __name__ == "__main__":
    import random

    def verify(vals, W, H, tag):
        rects = squarify(vals, 0, 0, W, H)
        live = [v for v in vals if v and v > 0]
        if len(rects) != len(live):
            return f"{tag}: LOST TILES {len(rects)} vs {len(live)}"
        area = sum(r[3] * r[4] for r in rects)
        if abs(area - W * H) / (W * H) > 1e-9:
            return f"{tag}: AREA {area:.3f} vs {W*H:.3f}"
        # rects are (value_index, x, y, w, h) -- r[0] is the INDEX, not a coordinate.
        for idx, x, y, w, h in rects:
            if w < -1e-9 or h < -1e-9:
                return f"{tag}: NEGATIVE {(idx, x, y, w, h)}"
            if x < -1e-9 or y < -1e-9:
                return f"{tag}: OUT OF BOUNDS {(idx, x, y, w, h)}"
            tolx = abs(W) * 1e-9 + 1e-9
            toly = abs(H) * 1e-9 + 1e-9
            if x + w > W + tolx or y + h > H + toly:
                return (f"{tag}: OVERFLOW {(idx, x, y, w, h)} (box {W}x{H}) "
                        f"dx={x+w-W!r} dy={y+h-H!r}")
        for a in range(len(rects)):
            for b in range(a + 1, len(rects)):
                _, x1, y1, w1, h1 = rects[a]
                _, x2, y2, w2, h2 = rects[b]
                if (min(x1 + w1, x2 + w2) - max(x1, x2) > 1e-6 * max(W, 1) and
                        min(y1 + h1, y2 + h2) - max(y1, y2) > 1e-6 * max(H, 1)):
                    return f"{tag}: OVERLAP {rects[a]} {rects[b]}"
        return None

    # the shape that broke the previous implementation
    shaped = [514, 232, 207, 110, 90, 80, 60, 55, 50, 45, 40, 35]
    e = verify(shaped, 1192, 612, "span-shaped")
    print("span-shaped:", e or "ok")
    if not e:
        for i, x, y, w, h in squarify(shaped, 0, 0, 1192, 612):
            print(f"   {shaped[i]:>5d}  {x:7.1f} {y:7.1f} {w:7.1f} {h:7.1f}  ar={w/h:5.2f}")

    bad = 0
    for t in range(500):
        random.seed(t)
        n = random.randint(1, 50)
        vals = [random.random() ** random.choice([1, 2, 3, 4]) + 0.0005 for _ in range(n)]
        W, H = random.uniform(120, 1400), random.uniform(120, 900)
        err = verify(vals, W, H, f"rand{t}")
        if err:
            print("FAIL", err)
            bad += 1
            break
    if not bad:
        print("random: 500 trials ok (exact area, no overlap, in bounds)")