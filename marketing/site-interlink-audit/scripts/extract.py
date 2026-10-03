#!/usr/bin/env python3
"""
Rewrite body extraction so that page text is a clean run of visible words.

The old extractor replaced every tag with a newline, which produced one token per line and
left pages that were ~90% blank lines. That defeated downstream analysis twice:
  - repeated-line chrome removal could not group the menu, because the menu was split
    into single words
  - mention counts were dominated by nav words ("write", "search", "singapore")

Fix: collapse whitespace, drop a stopword tail that always precedes the footer, and
return a single dense string.
"""
import re, html as _html

# Words that mark the start of footer/boilerplate on virtually every page. body() cuts here
# so the mega-menu and footer never reach mention counting.
CUT_MARKERS = [
    "write for us", "other links", "let's discuss", "lets discuss", "get in touch",
    "all rights reserved", "privacy policy", "terms of service", "terms and conditions",
    "follow us", "subscribe to our", "newsletter", "cookie", "do not sell my data",
    "request for a quote", "send us your requirement", "reseller program",
    "our growth experts", "double your", "summarize with ai",
]

VISIBLE_DROP = re.compile(
    r"(?is)<(script|style|noscript|svg|iframe|template|form|button|select|textarea)[^>]*>"
    r".*?</\1\s*>|<[^>]+>")
# opt-in and hidden widgets: their labels read as body text but never are
WIDGET_DROP = re.compile(
    r"(?is)<(input|label|select|option|textarea|button)[^>]*>.*?</\1\s*>")


def visible_text(html):
    """All visible text, whitespace collapsed to single spaces."""
    s = VISIBLE_DROP.sub(" ", html)
    s = WIDGET_DROP.sub(" ", s)
    s = _html.unescape(s)
    s = s.replace("\xa0", " ").replace("\u200b", " ")
    return re.sub(r"\s+", " ", s).strip()


NAV_LINE = re.compile(
    r"^(?:home|about|contact|blog|resources?|privacy|terms|search|careers?|clients?|"
    r"capabilities?|industries?|solutions?|insights?|write for us|other links|"
    r"engage|resources|menu|homepage)(?:\s*[|/>-]\s*|\s*$)",
    re.I)


def body(html, min_keep=250):
    """
    Return the page's editorial prose as one dense string.

    Anchoring on <h1> is not enough: on this theme the product mega-menu renders BEFORE the
    h1, so every list page carried every brand name 10-15 times. Instead, split visible text
    into sentences and drop the leading run of short, link-like fragments (the menu) by
    finding the first sentence that looks like prose, then cut at the footer markers.
    """
    m = re.search(r"(?is)<h1[^>]*>", html)
    raw = visible_text(html)

    # Prefer the text after <h1> when it is substantial, else use the whole document.
    if m:
        after = visible_text(html[m.end():])
        if len(after.split()) >= 120:
            raw = after

    # Drop the leading nav run: consecutive fragments that are short and menu-shaped.
    parts = re.split(r"(?<=[.!?])\s+", raw)
    start = 0
    seen_prose = 0
    for i, p in enumerate(parts[:60]):
        words = p.split()
        looks_nav = (len(words) <= 9 and (NAV_LINE.match(p.strip()) or
                      (len(words) <= 6 and not p.strip().endswith((".", "!", "?", ":", ";")))))
        if looks_nav:
            continue
        start = i
        seen_prose += 1
        if seen_prose >= 2:
            break
    text = " ".join(parts[start:])

    low = text.lower()
    cut = len(text)
    floor = max(900, int(len(text) * 0.45))
    for mk in CUT_MARKERS:
        i = low.find(mk)
        if floor < i < cut:
            cut = i
    out = text[:cut].strip()
    return out if len(out.split()) >= 40 else raw


def body_title(html):
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    if not m:
        m = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    if not m:
        return ""
    return re.sub(r"\s+", " ", _html.unescape(
        re.sub(r"(?s)<[^>]+>", " ", m.group(1)))).strip()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/Users/deep/.hermes/cache/scratch/sitearch")
    from discover import fetch
    tests = [
        "https://www.spanglobalservices.com/technology-lists/zendesk-users-list",
        "https://www.spanglobalservices.com/healthcare-lists/chiropractor-email-list",
        "https://www.spanglobalservices.com/faq/what-is-a-zendesk-users-list",
    ]
    for u in tests:
        g = fetch(u)
        h = g[0].decode("utf8", "ignore") if g[0] else ""
        t = body(h)
        print(f"\n{u.split('.com')[-1]}")
        print(f"  chars={len(t)}  words={len(t.split())}")
        print(f"  head: {t[:150]!r}")
        for k in ("zendesk", "veterinarian", "write", "singapore"):
            print(f"    {k:14s} {'YES' if k in t.lower() else 'no'}")