"""Prove a web artifact is self-contained: run it with the browser offline and fail on any external request, console error or storage write.

Usage:
  python3 offline-check.py <file-or-url> [--width 1440] [--selector 'body[data-loaded]'] [--settle 750]

Exits 1 when the artifact reaches the network, throws a page error, logs a console error, or writes
to local/session storage. Opened via file:// the context is forced offline, so anything that really
needs the network fails loudly instead of quietly succeeding against a cache.
"""
import argparse
import json
import sys
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def allowed_prefixes(target: str) -> tuple:
    parts = urlsplit(target)
    if parts.scheme == "file":
        # Subresources sit next to the document, not under its filename.
        return (target.rsplit("/", 1)[0] + "/", "blob:", "data:")
    return (f"{parts.scheme}://{parts.netloc}", "blob:", "data:")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="file:// path or http(s) URL")
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--selector", default=None, help="readiness selector to await")
    parser.add_argument("--settle", type=int, default=750, help="ms to wait after readiness")
    args = parser.parse_args()

    allowed = allowed_prefixes(args.target)
    external, errors = [], []
    storage = None

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": args.width, "height": 1000})
        if args.target.startswith("file:"):
            context.set_offline(True)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.on("request", lambda request: external.append(request.url) if not request.url.startswith(allowed) else None)
        page.goto(args.target)
        if args.selector:
            page.wait_for_selector(args.selector)
        page.wait_for_timeout(args.settle)
        storage = page.evaluate(
            """() => { try { return {local: localStorage.length, session: sessionStorage.length}; }
                       catch (e) { return {unavailable: String(e)}; } }"""
        )
        browser.close()

    writes = bool(storage and (storage.get("local") or storage.get("session")))
    report = {
        "target": args.target,
        "external_requests": external,
        "console_errors": errors,
        "storage": storage,
        "ok": not (external or errors or writes),
    }
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
