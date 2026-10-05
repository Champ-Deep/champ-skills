#!/usr/bin/env python3
"""
Generic site discovery: works on any domain, not just WordPress.

Order of preference:
  1. robots.txt + sitemap.xml (or sitemap_index.xml, nested)
  2. WordPress REST API, if present, for the true published inventory
  3. crawl from the homepage as a fallback

Probes three structurally different sites so the generalisation claim is tested rather
than assumed.
"""
import sys, json, re, time, urllib.request, urllib.error, gzip, io
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
UA += "Chrome/122.0 Safari/537.36"
TIMEOUT = 25


def fetch(url, tries=2):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw, r.geturl(), r.status
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and a + 1 < tries:
                time.sleep(2 + a * 3)
                continue
            return None, url, e.code
        except Exception:
            if a + 1 < tries:
                time.sleep(1.5)
    return None, url, 0


def txt(url):
    got = fetch(url)
    return got[0] or b""


def norm(u):
    u = u.split("#")[0].rstrip("/")
    return u or u


def discover_sitemaps(base):
    """Find every sitemap the site advertises."""
    found, queue = [], [urljoin(base, "/sitemap.xml"),
                        urljoin(base, "/sitemap_index.xml"),
                        urljoin(base, "/wp-sitemap.xml")]
    seen = set()
    while queue:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        body = txt(sm)
        if not body:
            continue
        head = body[:4000].decode("utf8", "ignore").lower()
        if "<sitemapindex" in head:
            found.append(sm)
            try:
                root = ET.fromstring(body)
                for loc in root.iter():
                    if loc.tag.endswith("loc") and loc.text:
                        queue.append(loc.text.strip())
            except Exception:
                pass
        elif "<urlset" in head:
            found.append(sm)
    # robots.txt often names a sitemap the index does not link
    rb = txt(urljoin(base, "/robots.txt"))
    if rb:
        for m in re.finditer(r"Sitemap:\s*(\S+)", rb.decode("utf8", "ignore"), re.I):
            u = m.group(1).strip()
            if u not in seen and u not in found:
                seen.add(u)
                found.append(u)

    # A whole content area can sit OUTSIDE the index. An adversarial review of the Span
    # report found the blog has its own sitemap with 359 pages, none of it referenced by
    # sitemap_index.xml or robots.txt, so the crawl saw 4 blog pages and concluded the site
    # had no research layer. Probe the conventional names a WordPress install uses and keep
    # any that answers. This is a bounded, cheap probe: no crawling off the sitemap.
    for guess in ("/blog/sitemap_index.xml", "/blog/sitemap.xml", "/blog/wp-sitemap.xml",
                  "/news/sitemap_index.xml", "/news/sitemap.xml",
                  "/resources/sitemap_index.xml", "/insights/sitemap_index.xml",
                  "/post-sitemap.xml", "/posts-sitemap.xml"):
        u = urljoin(base, guess)
        if u in seen:
            continue
        body = txt(u)
        if not body:
            continue
        head = body[:2000].decode("utf8", "ignore").lower()
        if "<sitemapindex" not in head and "<urlset" not in head:
            continue
        seen.add(u)
        found.append(u)
        if "<sitemapindex" in head:
            try:
                root = ET.fromstring(body)
                for loc in root.iter():
                    if loc.tag.endswith("loc") and loc.text:
                        c = loc.text.strip()
                        if c not in seen:
                            seen.add(c)
                            found.append(c)
            except Exception:
                pass
    return found


def urls_from_sitemap(sm):
    out = []
    body = txt(sm)
    if not body:
        return out
    try:
        root = ET.fromstring(body)
    except Exception:
        return out
    for loc in root.iter():
        if loc.tag.endswith("loc") and loc.text:
            out.append(loc.text.strip())
    return out


def wp_types(base):
    """Detect WordPress and enumerate its public post types."""
    got = fetch(urljoin(base, "/wp-json/wp/v2/types"))
    if got[2] != 200 or not got[0]:
        return None
    try:
        types = json.loads(got[0].decode("utf8", "ignore"))
    except Exception:
        return None
    keep = {}
    for k, v in types.items():
        if not isinstance(v, dict):
            continue
        if v.get("viewable") is False and not v.get("show_in_rest"):
            continue
        rest = v.get("rest_base") or k
        keep[k] = rest
    return keep or None


def wp_posts(base, rest, cap=1200):
    """Page through the REST API. Returns [(id, url, type, title)]."""
    out = []
    for page in range(1, 40):
        url = f"{urljoin(base, '/wp-json/wp/v2/' + rest)}?per_page=100&page={page}&_fields=id,link,title"
        got = fetch(url)
        if got[2] in (400, 404) or not got[0]:
            break
        try:
            rows = json.loads(got[0].decode("utf8", "ignore"))
        except Exception:
            break
        if not isinstance(rows, list) or not rows:
            break
        for r in rows:
            if isinstance(r, dict) and r.get("link"):
                out.append((str(r.get("id")), r["link"], rest,
                            (r.get("title") or {}).get("rendered", "")))
        if len(rows) < 100 or len(out) >= cap:
            break
    return out


class LinkGrab(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.title, self.h1 = [], "", ""
        self._t, self._h1 = False, False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append((d["href"], d.get("rel", ""), d.get("class", "")))
        elif tag == "title":
            self._t = True
        elif tag == "h1":
            self._h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        elif tag == "h1":
            self._h1 = False

    def handle_data(self, data):
        if self._t:
            self.title += data
        elif self._h1:
            self.h1 += data


def crawl(base, seed_urls, cap=400, workers=10):
    """Minimal breadth-first crawl. Used when no sitemap or REST API exists."""
    import concurrent.futures as cf
    host = urlparse(base).netloc.replace("www.", "")
    seen, out = set(), {}
    queue = [u for u in seed_urls][:cap]
    while queue and len(seen) < cap:
        batch, queue = queue[:workers * 3], queue[workers * 3:]
        for u in batch:
            n = norm(u)
            if n in seen:
                continue
            seen.add(n)
            out[n] = None
        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            for n, res in zip(seen, ex.map(lambda u: fetch(u), [norm(u) for u in batch])):
                if res[0]:
                    out[n] = res[0]
    return out


def probe(base):
    base = base if base.startswith("http") else "https://" + base
    base = base.rstrip("/") + "/"
    print(f"\n{'='*68}\n{base}\n{'='*68}")

    sms = discover_sitemaps(base)
    sm_urls = []
    for sm in sms[:40]:
        got = urls_from_sitemap(sm)
        sm_urls.extend(got)
        print(f"  sitemap {sm.replace(base,'')}  -> {len(got)} urls")
    smset = {norm(u) for u in sm_urls if u.startswith("http")}
    print(f"  TOTAL sitemap urls: {len(smset)}")

    types = wp_types(base)
    posts = []
    if types:
        print(f"  WordPress detected, {len(types)} viewable types: {list(types)[:8]}")
        for name, rest in types.items():
            got = wp_posts(base, rest)
            posts.extend(got)
            print(f"     {name:22s} {len(got):5d}")
    else:
        print("  WordPress: no")

    live = {norm(u) for _, u, _, _ in posts}
    print(f"  TOTAL live (REST): {len(live)}")
    print(f"  sitemap coverage: {len(smset & live)}/{len(live) if live else 0} live URLs published")
    if smset and live:
        miss = [u for u in live if u not in smset]
        print(f"  live but NOT in sitemap: {len(miss)}")
        for u in miss[:5]:
            print(f"      {u.replace(base,'')}")
    types_seen = {}
    for _, u, t, _ in posts:
        types_seen[t] = types_seen.get(t, 0) + 1
    print(f"  post types: {types_seen}")
    return {"base": base, "sitemaps": len(sms), "sitemap_urls": len(smset),
            "wp": bool(types), "live": len(live), "types": types_seen}


if __name__ == "__main__":
    for b in sys.argv[1:]:
        probe(b)
