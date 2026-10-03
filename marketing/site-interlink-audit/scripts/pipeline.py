#!/usr/bin/env python3
"""
Full generic pipeline: discover -> fetch -> extract -> classify -> link graph.

Platform-agnostic. Writes one JSON bundle per site that the report builder consumes.
Handles: sitemap discovery, WordPress REST enrichment, header-stripped body extraction,
boilerplate removal by link-frequency, funnel classification, landing-page scoring and a
contextual internal link graph.
"""
import sys, os, re, json, time, gzip, html, collections, concurrent.futures as cf
from urllib.parse import urljoin, urlparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import (fetch, txt, discover_sitemaps, urls_from_sitemap, wp_types,
                      wp_posts, norm)
from classify import classify, primary_role, content_type, gap_signals, landing_score

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")


from extract import body as body_text, body_title as _btitle  # noqa: E402


def chrome_targets(raw, base):
    """Targets inside nav/header/footer/aside: site furniture, not editorial links."""
    host = urlparse(base).netloc.replace("www.", "")
    pat = re.compile(r"<a[^>]+href=[\"']([^\"'#]+)[\"']", re.I)
    chrome = set()
    for tag in ("nav", "header", "footer", "aside"):
        for blk in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", raw, re.S | re.I):
            for h in pat.findall(blk.group(1)):
                u = norm(urljoin(base, h))
                if host in u:
                    chrome.add(u)
    # fall back to class-name heuristics when the theme has no semantic tags
    for cls in ("sub-menu", "sgs-tabx", "menu-item", "footer-menu", "nav-menu",
                "site-footer", "main-nav", "side-bar", "sidebar", "breadcrumb"):
        for blk in re.finditer(rf"<[a-z]+[^>]*class=[\"'][^\"']*{cls}[^\"']*[\"'][^>]*>(.*?)</[a-z]+>",
                               raw, re.S | re.I):
            for h in pat.findall(blk.group(1)):
                u = norm(urljoin(base, h))
                if host in u:
                    chrome.add(u)
    return chrome


def extract_links(raw, base):
    host = urlparse(base).netloc.replace("www.", "")
    out = []
    for m in re.finditer(r"<a[^>]+href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", raw, re.S | re.I):
        u = norm(urljoin(base, m.group(1)))
        if host not in u:
            continue
        label = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
        out.append((u, label))
    return out


def build(base, cap=6000, workers=12, use_sitemap=True, verbose=True,
         keep_text=False, text_limit=6000):
    base = base if base.startswith("http") else "https://" + base
    base = base.rstrip("/") + "/"
    host = urlparse(base).netloc
    t0 = time.time()

    sm_urls, n_sitemaps = [], 0
    if use_sitemap:
        for sm in discover_sitemaps(base):
            n_sitemaps += 1
            sm_urls.extend(urls_from_sitemap(sm))
    smset = {norm(u) for u in sm_urls if u.startswith("http")}

    posts, types = [], None
    types = wp_types(base)
    if types:
        for name, rest in types.items():
            posts.extend(wp_posts(base, rest, cap=cap))
    live = {norm(u): (i, t, ti) for i, u, t, ti in posts}

    targets = set(live) or smset
    if not targets:
        got = fetch(base)
        if got[0]:
            for u, _ in extract_links(got[0].decode("utf8", "ignore"), base):
                targets.add(u)
    # Prioritise: landing pages, then conversion and content, then everything else. A flat
    # alphabetical slice would spend the whole budget on FAQ pages and never reach the
    # commercial or entity URLs, which are the ones worth analysing.
    PRIO = {"home": 0, "conversion": 0, "entity-list": 1, "educational": 1,
            "solution": 1, "content": 2}
    def rank(u):
        pid, ptype, title = live.get(u, (None, None, ""))
        ct = ptype or content_type(u)
        return (PRIO.get(ct, 3), len(u))
    candidates = len(targets)
    targets = sorted(targets, key=rank)[:cap]

    if verbose:
        print(f"  {host}: {n_sitemaps} sitemaps, {len(smset)} urls, "
              f"REST={len(live)}, fetching {len(targets)} pages")

    def get(u):
        g = fetch(u)
        return u, g[0]

    pages, links_raw, chrome_all = {}, {}, collections.Counter()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for u, raw in ex.map(get, targets):
            if not raw:
                continue
            s = raw.decode("utf8", "ignore")
            pages[u] = body_text(s)
            lk = extract_links(s, base)
            links_raw[u] = lk
            for t, _ in lk:
                chrome_all[t] += 1
            ch = chrome_targets(s, base)
            chrome_all.update(ch)

    # ---- remove repeated chrome blocks -------------------------------------
    # A product mega-menu repeats verbatim on every page, so counting brand mentions
    # without removing it reports every product as "mentioned on 420 pages". Detect the
    # repeated line blocks and strip them from each page.
    chrome_lines = set()   # extract.body() already removes footers and menus

    # boilerplate = targets linked from an implausible share of pages
    n_pages = max(len(pages), 1)
    boiler = {t for t, c in chrome_all.items() if c >= max(8, n_pages * 0.25)}

    nodes, idmap = [], {}
    for i, u in enumerate(pages):
        idmap[u] = str(i)
    for u, t in pages.items():
        roles = classify(t)
        g = gap_signals(t)
        pid, ptype, title = live.get(u, (None, None, ""))
        nodes.append({
            "id": idmap[u], "url": u, "in_sitemap": u in smset,
            "type": ptype or content_type(u), "section": section_of(u),
            "title": (title or "")[:120],
            "roles": roles, "role": primary_role(roles),
            "landing": landing_score(g), "gaps": g,
            "words": g["words"], "title_len": len(t),
            # body text is needed downstream for entity mention scanning; it is large, so it
            # is opt-in and truncated
            **({"text": t[:text_limit]} if keep_text else {}),
        })

    edges = []
    for u, lk in links_raw.items():
        for tgt, label in lk:
            if tgt in boiler or tgt not in idmap:
                continue
            if idmap[tgt] == idmap[u]:
                continue
            edges.append([idmap[u], idmap[tgt], label[:80]])

    indeg = collections.Counter(e[1] for e in edges)
    outdeg = collections.Counter(e[0] for e in edges)
    for n in nodes:
        n["in"] = indeg[n["id"]]
        n["out"] = outdeg[n["id"]]

    bundle = {
        "base": base, "host": host, "fetched_at": time.strftime("%Y-%m-%d"),
        "sitemaps": n_sitemaps, "sitemap_urls": len(smset),
        "wp": bool(types), "nodes": nodes, "edges": edges,
        "boilerplate": len(boiler),
        "chrome_lines": len(chrome_lines),
        "cap": cap,
        "candidates": len(targets),
        "truncated": len(targets) < candidates,
        "stats": {
            "pages": len(nodes), "edges": len(edges),
            "in_sitemap": sum(1 for n in nodes if n["in_sitemap"]),
            "roles": dict(collections.Counter(n["role"] for n in nodes)),
            "types": dict(collections.Counter(n["type"] for n in nodes)),
            "zero_in": sum(1 for n in nodes if n["in"] == 0),
            "zero_out": sum(1 for n in nodes if n["out"] == 0),
            "boilerplate": len(boiler),
        "chrome_lines": len(chrome_lines),
        "cap": cap,
        "candidates": len(targets),
        "truncated": len(targets) < candidates,
            "secs": round(time.time() - t0, 1),
        },
    }
    return bundle


def section_of(u):
    seg = [s for s in urlparse(u).path.split("/") if s]
    return seg[0] if seg else "home"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Crawl a site into a graph bundle")
    ap.add_argument("domain")
    ap.add_argument("--cap", type=int, default=6000,
                    help="max pages to fetch (default 6000)")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--no-sitemap", action="store_true")
    a = ap.parse_args()
    host = re.sub(r"^https?://", "", a.domain.strip()).strip("/")
    bundle = build(host, cap=a.cap, workers=a.workers,
                   use_sitemap=not a.no_sitemap)
    print(f"  stats: {json.dumps(bundle['stats'], indent=None)[:400]}")
