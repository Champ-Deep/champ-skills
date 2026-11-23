#!/usr/bin/env python3
"""Sitemap-wide SEO crawl for a prospect audit. Usage: crawl_sitemap.py https://www.example.com/ [outdir]
Writes crawl.json (per page: title, description, h1, words, bytes, imgs, imgs_noalt, md5, ldjson, lastmod, final url, canonical) and prints the headline counts.
shortcut: reads only the URLs in /sitemap.xml (one index level), no link discovery; upgrade when a site has no sitemap."""
import sys, re, json, html, hashlib, os, urllib.request, concurrent.futures as cf
from collections import Counter
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
site = sys.argv[1].rstrip("/"); out = sys.argv[2] if len(sys.argv) > 2 else "build"
os.makedirs(f"{out}/raw", exist_ok=True)

FINAL = {}  # requested url -> url after redirects

def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30) as r:
        FINAL[u] = r.geturl()
        return r.read().decode("utf-8", "ignore")

def strip(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()

LASTMOD = {}  # url -> lastmod string from the sitemap, when the sitemap carries one

def locs(xml):
    out = []
    for blk in re.findall(r"<url>(.*?)</url>", xml, re.S) or [xml]:
        for u in re.findall(r"<loc>([^<]+)</loc>", blk):
            out.append(u)
            m = re.search(r"<lastmod>([^<]+)</lastmod>", blk)
            if m: LASTMOD[u] = m.group(1).strip()
    return out

sm = get(site + "/sitemap.xml")
urls = sorted(set(locs(sm)))
if urls and urls[0].endswith(".xml"):  # sitemap index: one level down
    urls = sorted({u for s in urls for u in locs(get(s))})

def one(u):
    try: t = get(u)
    except Exception as e: return {"url": u, "error": str(e)}
    slug = u.rsplit("/", 1)[1] or "index.html"
    open(f"{out}/raw/{slug}", "w").write(t)
    g = lambda p: (re.search(p, t, re.S | re.I) or [None, None])[1] or ""
    imgs = re.findall(r"<img[^>]*>", t)
    return {"url": u, "slug": slug, "title": html.unescape(g(r"<title>(.*?)</title>")).strip(),
            "desc": html.unescape(g(r'<meta name="description" content="(.*?)"')).strip(),
            "h1": [strip(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)],
            "words": len(strip(t).split()), "bytes": len(t), "imgs": len(imgs),
            "imgs_noalt": sum(1 for i in imgs if not re.search(r'alt="[^"]+"', i)),
            "md5": hashlib.md5(t.encode()).hexdigest(), "ldjson": t.count("application/ld+json"),
            "lastmod": LASTMOD.get(u, ""), "final": FINAL.get(u, u),
            "canonical": g(r'<link[^>]*rel="canonical"[^>]*href="(.*?)"')}

with cf.ThreadPoolExecutor(8) as ex: pages = list(ex.map(one, urls))
json.dump(pages, open(f"{out}/crawl.json", "w"), indent=1)
ok = [p for p in pages if "error" not in p]
dupe_bodies = sum(c > 1 for c in Counter(p["md5"] for p in ok).values())
print(f"sitemap urls {len(urls)}, fetched {len(ok)}, errors {len(pages)-len(ok)}")
print(f"dup titles {sum(c>1 for c in Counter(p['title'] for p in ok).values())}, dup descriptions {sum(c>1 for c in Counter(p['desc'] for p in ok).values())}, identical bodies {dupe_bodies}")
print(f"title>60 {sum(len(p['title'])>60 for p in ok)}, desc>160 {sum(len(p['desc'])>160 for p in ok)}, missing h1 {sum(not p['h1'] for p in ok)}, multi h1 {sum(len(p['h1'])>1 for p in ok)}")
print(f"imgs without alt {sum(p['imgs_noalt'] for p in ok)} / {sum(p['imgs'] for p in ok)}, pages with ld+json {sum(p['ldjson']>0 for p in ok)}")
print("thin pages (<350 words):", sum(p["words"] < 350 for p in ok))
lm = sorted(p["lastmod"] for p in ok if p["lastmod"])
print(f"sitemap lastmod present on {len(lm)}/{len(ok)}" + (f", oldest {lm[0]}, newest {lm[-1]}" if lm else ""))
print(f"redirected sitemap urls {sum(p['final'] != p['url'] for p in ok)}, canonical missing {sum(not p['canonical'] for p in ok)}, canonical differs from final url {sum(bool(p['canonical']) and p['canonical'].rstrip('/') != p['final'].rstrip('/') for p in ok)}, canonical differs only by trailing slash {sum(bool(p['canonical']) and p['canonical'] != p['final'] and p['canonical'].rstrip('/') == p['final'].rstrip('/') for p in ok)}")
print("url prefixes:", Counter(re.sub(r"[-_].*", "", p["slug"]) for p in ok).most_common(8))
assert len(ok) > 0, "nothing fetched: check robots, UA block, or sitemap path"
