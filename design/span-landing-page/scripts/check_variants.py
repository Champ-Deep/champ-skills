#!/usr/bin/env python3
"""Prove a variant family: serve the folder, assert every expected headline, assert noindex,
confirm the demo switcher really navigates, screenshot each variant.

Fill FAMILIES (html file -> query key or "" for default -> expected #hl text), then:
    python3 check_variants.py
Expects the campaign-landing template's #hl headline element and the demo-only #demo-bar.
Screenshots land in ./shots next to this script.
"""
import functools
import http.server
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PORT = 3147

FAMILIES = {
    "SPAN_msp-us.html": {
        "": "Your Next MSP Customer Starts With The Right Contact.",
        "mssp": "Reach The MSSPs That Sell Managed Security.",
    },
    # add every variant file and each of its ?hl= headline keys
}

shots = HERE / "shots"
shots.mkdir(exist_ok=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    for name, keys in FAMILIES.items():
        for key, want in keys.items():
            url = f"http://127.0.0.1:{PORT}/{name}" + (f"?hl={key}" if key else "")
            page.goto(url, wait_until="load")
            page.wait_for_timeout(300)
            got = page.locator("#hl").inner_text().strip()
            assert got == want, (url, got)
            assert page.locator('meta[name="robots"][content*="noindex"]').count() == 1, f"{url}: noindex missing"
            assert page.locator("#demo-bar").is_visible(), f"{url}: demo switcher missing"
            page.screenshot(path=str(shots / f"{name.removesuffix('.html')}{'-' + key if key else ''}.png"))
            print("PASS", url, "->", got)
    first = next(iter(FAMILIES))
    page.goto(f"http://127.0.0.1:{PORT}/{first}")
    page.locator("#demo-bar a").first.click()
    page.wait_for_load_state("load")
    landed = page.url.split("?")[0].rstrip("/").split("/")[-1]
    assert landed != first, page.url
    print("PASS switcher navigates to another variant:", landed)
    browser.close()
srv.shutdown()
