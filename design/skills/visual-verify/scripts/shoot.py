#!/usr/bin/env python3
"""
shoot.py - Render a page and capture the screenshots an agent needs to critique
its own work.

Usage:
    python3 shoot.py <url-or-path> [options]

Examples:
    python3 shoot.py ./index.html
    python3 shoot.py http://localhost:3000 --out .verify --themes light,dark
    python3 shoot.py ./out.html --widths 390,1440 --wait 1200

Output:
    <out>/<theme>-<width>-fold.png    above-the-fold (first viewport)
    <out>/<theme>-<width>-full.png    full page
    <out>/manifest.json               list of what was captured

After running this, READ the PNGs with the Read tool. Do not skip that step.
A screenshot you did not look at has verified nothing.
"""

import argparse
import json
import os
import pathlib
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit(
        "playwright is not installed.\n"
        "  pip install playwright --break-system-packages\n"
        "  (browsers are usually preinstalled; if not: playwright install chromium)"
    )

DEFAULT_WIDTHS = [390, 834, 1440]
HEIGHTS = {390: 844, 834: 1112, 1440: 900, 1920: 1080, 2560: 1440}


def to_url(target: str) -> str:
    if target.startswith(("http://", "https://", "file://", "data:")):
        return target
    p = pathlib.Path(target).expanduser().resolve()
    if not p.exists():
        sys.exit(f"No such file: {p}")
    return p.as_uri()


def main() -> int:
    ap = argparse.ArgumentParser(description="Screenshot a page for design critique.")
    ap.add_argument("target", help="URL, or path to an HTML file")
    ap.add_argument("--out", default=".verify", help="output directory (default: .verify)")
    ap.add_argument("--widths", default=",".join(map(str, DEFAULT_WIDTHS)),
                    help="comma-separated viewport widths (default: 390,834,1440)")
    ap.add_argument("--themes", default="light",
                    help="comma-separated: light, dark (default: light)")
    ap.add_argument("--wait", type=int, default=800,
                    help="ms to wait after load, for fonts and entrance animations")
    ap.add_argument("--selector", default=None,
                    help="optional CSS selector to wait for before shooting")
    ap.add_argument("--no-full", action="store_true", help="skip full-page captures")
    ap.add_argument("--reduced-motion", action="store_true",
                    help="also capture with prefers-reduced-motion: reduce")
    args = ap.parse_args()

    url = to_url(args.target)
    widths = [int(w.strip()) for w in args.widths.split(",") if w.strip()]
    themes = [t.strip() for t in args.themes.split(",") if t.strip()]
    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    motion_modes = ["no-preference"]
    if args.reduced_motion:
        motion_modes.append("reduce")

    shots = []
    console_errors = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--force-color-profile=srgb"])
        for theme in themes:
            for motion in motion_modes:
                for width in widths:
                    height = HEIGHTS.get(width, 900)
                    ctx = browser.new_context(
                        viewport={"width": width, "height": height},
                        device_scale_factor=2,
                        color_scheme=theme,
                        reduced_motion=motion,
                        is_mobile=width < 700,
                        has_touch=width < 700,
                    )
                    page = ctx.new_page()
                    page.on("console", lambda m: console_errors.append(m.text)
                            if m.type == "error" else None)
                    page.on("pageerror", lambda e: console_errors.append(str(e)))
                    try:
                        page.goto(url, wait_until="networkidle", timeout=30000)
                    except Exception:
                        page.goto(url, wait_until="load", timeout=30000)
                    if args.selector:
                        try:
                            page.wait_for_selector(args.selector, timeout=8000)
                        except Exception:
                            print(f"  ! selector never appeared: {args.selector}")
                    try:
                        page.evaluate("document.fonts && document.fonts.ready")
                    except Exception:
                        pass
                    page.wait_for_timeout(args.wait)

                    tag = theme if motion == "no-preference" else f"{theme}-rm"
                    fold = outdir / f"{tag}-{width}-fold.png"
                    page.screenshot(path=str(fold))
                    shots.append(str(fold))
                    print(f"  captured {fold}")

                    if not args.no_full:
                        full = outdir / f"{tag}-{width}-full.png"
                        page.screenshot(path=str(full), full_page=True)
                        shots.append(str(full))
                        print(f"  captured {full}")

                    ctx.close()
        browser.close()

    manifest = {
        "target": url,
        "shots": shots,
        "console_errors": sorted(set(console_errors))[:25],
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    if console_errors:
        print(f"\n  {len(set(console_errors))} console error(s) - these are defects, fix them:")
        for e in sorted(set(console_errors))[:10]:
            print(f"    - {e[:160]}")

    print(f"\nNEXT STEP (required): open every PNG in {outdir} with the Read tool and "
          f"critique it against reference/critique-protocol.md. Do not report done "
          f"until you have actually looked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
