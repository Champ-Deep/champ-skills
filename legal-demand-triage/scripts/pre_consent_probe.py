#!/usr/bin/env python3
"""Probe a live page for tracking that fires BEFORE any consent or interaction.

Usage:
    python3 pre_consent_probe.py https://www.example.com/ [--wait 15]

Answers the factual question behind privacy demand letters and audits: with a
fresh browser, no clicks, no scroll, no consent accepted, what third-party
tracking actually loads? The printout covers:
  1. consent banner present and visible?
  2. cookies set pre-consent
  3. third-party tracker hosts actually requested
  4. tracker hosts declared in page source but not requested (blocked or
     deferred) plus custom loader / fetch-override scripts, which a
     network-only view misses when a site monkeypatches window.fetch/XHR to
     swallow analytics calls

Requires: `pip install playwright` and a real Chrome (channel="chrome"); the
bundled chromium is often absent on managed machines.
"""
import argparse
import asyncio
import re
import sys
from urllib.parse import urlsplit

from playwright.async_api import async_playwright

TRACKER = re.compile(
    r"google|doubleclick|googletagmanager|segment|linkedin|licdn|clarity|ahrefs"
    r"|cloudflareinsights|facebook|fbcdn|hubspot|hotjar|intercom|mixpanel"
    r"|amplitude|criteo|adroll",
    re.I,
)
BANNER_SELECTORS = (
    ".cky-consent-container, .cky-consent-bar, #cookie-law-info-bar, "
    "#onetrust-consent-sdk, #CybotCookiebotDialog"
)


def registrable(host: str) -> str:
    parts = host.lower().split(".")
    return ".".join(parts[-2:])


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--wait", type=int, default=15,
                    help="seconds to observe with no interaction (cover the site's fallback loader)")
    ap.add_argument("--ua", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    args = ap.parse_args()

    requested = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await browser.new_context(user_agent=args.ua, locale="en-US",
                                        timezone_id="America/Los_Angeles")
        page = await ctx.new_page()
        page.on("request", lambda r: requested.append(r.url))
        await page.goto(args.url, wait_until="load", timeout=90000)
        # No scroll, no click, no consent: watch past the site's own fallback
        # loader window (many fire trackers after ~10s idle).
        await page.wait_for_timeout(args.wait * 1000)
        banner = await page.evaluate(
            """(()=>{const e=document.querySelector('%s');if(!e)return false;
               const r=e.getBoundingClientRect();
               return r.width>0&&r.height>0&&getComputedStyle(e).display!=='none';})()"""
            % BANNER_SELECTORS)
        cookies = sorted({c["name"] for c in await ctx.cookies()})
        source = await page.content()
        await browser.close()

    own = registrable(urlsplit(args.url).netloc.split(":")[0])
    req_set = set(requested)
    hit, declared_only = {}, set()
    for u in requested:
        host = urlsplit(u).netloc.split(":")[0]
        if host and not host.endswith(own) and TRACKER.search(host):
            hit[host] = hit.get(host, 0) + 1
    for u in re.findall(r"https?://[^\"'\\ )]+", source):
        host = urlsplit(u).netloc.split(":")[0]
        if host and not host.endswith(own) and TRACKER.search(host) and u not in req_set:
            declared_only.add(host)

    print(f"page: {args.url}  (no interaction, {args.wait}s observation)")
    print(f"consent banner visible: {banner}")
    print(f"cookies set pre-consent: {cookies or 'none'}")
    print("tracker hosts REQUESTED pre-consent:")
    for h, n in sorted(hit.items()):
        print(f"  {h}  x{n}")
    if not hit:
        print("  none")
    print("tracker hosts DECLARED in source but not requested:")
    for h in sorted(declared_only):
        print(f"  {h}")
    if not declared_only:
        print("  none")
    print("\ncustom loader / fetch-override scripts to review by hand:")
    found = False
    for pat in (r"addEventListener\('load'", r"requestIdleCallback",
                r"originalFetch", r"appendChild\(s\)"):
        for m in re.finditer(pat, source):
            found = True
            start = source.rfind("<script", 0, m.start())
            print("  ..." + re.sub(r"\s+", " ",
                                   source[max(start, m.start() - 80):m.start() + 120]))
    if not found:
        print("  none")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
