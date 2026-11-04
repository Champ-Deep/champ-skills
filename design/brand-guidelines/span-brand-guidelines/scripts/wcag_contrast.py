#!/usr/bin/env python3
"""WCAG contrast checker for hex pairs. Use it on any claimed contrast table.

Usage:
  python3 wcag_contrast.py '#3AA84C #FFFFFF' '#1A5C28 #FFFFFF'
  python3 wcag_contrast.py --list pairs.txt   # one "#fg #bg" pair per line

Prints ratio plus AA/AAA verdicts. Pass thresholds:
  4.5 AA body text, 3.0 AA large text (24px, or 18.7px bold) and icons, 7.0 AAA.
A ratio is computed from the hex, never from what a document claims it is.
"""
import sys


def _lum(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(fg, bg):
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def verdict(r):
    aa = 'AA pass' if r >= 4.5 else ('AA large only' if r >= 3.0 else 'FAIL')
    aaa = 'AAA' if r >= 7.0 else ('AAA large' if r >= 4.5 else '-')
    return f"{aa:14} {aaa}"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == '--list':
        lines = open(args[1]).read().splitlines()
        pairs = [tuple(l.split()) for l in lines if l.strip() and not l.startswith('#')]
    else:
        pairs = [tuple(a.split()) for a in args]
    bad = 0
    for fg, bg in pairs:
        r = ratio(fg, bg)
        if r < 4.5:
            bad += 1
        print(f"{fg} on {bg}  {r:5.2f}  {verdict(r)}")
    print(f"{len(pairs)} pairs, {bad} under 4.5")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
