# SSR-First Rendering and Vibe-Coded SEO Pitfalls

Canonical technical SEO floor for every public, indexable page built or audited across Champions Group. Load or reference this from page-building, frontend-brief, audit and QA skills instead of duplicating it.

## Default rendering rule

- **Public, indexable pages default to SSR or build-time SSG/prerendering** (Next.js App Router with Server Components, Astro, static HTML builds, or Worker-rendered HTML). Primary copy, headings, metadata, canonicals, internal links and JSON-LD MUST exist in the first-byte HTML response with JavaScript disabled.
- **Client-side SPAs (bare Vite + React) are restricted to authenticated apps, dashboards and internal tools** behind login, and those shells must send `noindex`. Never default to a CSR SPA for a marketing site, landing page, blog, docs hub, catalog or programmatic SEO surface.
- **Markdown alternates (`index.md`, `llms.txt`) complement SSR HTML for AI readers.** They never excuse a JS-only empty `<div id="root"></div>` page.

## Vibe-coded SEO pitfalls (block on sight)

| Pitfall | What breaks | Required fix |
|---|---|---|
| Empty JS shell / `useEffect` copy | `curl` gets `<div id="root"></div>` or spinners; crawlers index blank pages or delay indexing | Render full primary copy, H1, FAQ and links server-side or at build time |
| SPA catch-all / soft 404 | `not_found_handling: "single-page-application"` or `/* /index.html 200` serves HTTP 200 + homepage HTML on bogus slugs and sibling routes | Return real HTTP 404/410 on unknown routes; emit distinct server-rendered HTML per URL |
| Client-mutated `<head>` / boilerplate meta | `document.title` or client Helmet swaps tags post-hydration, or every route shares one title/description | Server-render unique `<title>` (<=60 chars), `<meta name="description">` (<=155 chars), OG/Twitter tags and self-referencing `<link rel="canonical">` matching the final URL |
| Non-crawlable JS navigation | `<div onClick>`, `<button>`, or `#/hash` routes used for page navigation; crawlers cannot follow links | Use real `<a href="/clean-path">` for every route; keep `<button>` for in-page actions |
| Broken heading outline / split-text H1 | Zero or multiple `<h1>`s, `<h1>` on navbar logo, skipped levels, or animation JS splitting `<h1>` into per-letter `<span>`s | Exactly one semantic `<h1>` matching page intent; keep plain text intact in SSR HTML and split progressively with `aria-label` intact |
| Copy trapped in `opacity: 0` or `<canvas>` | Scroll-reveal defaults hide text until JS fires, or specs/headlines live only inside WebGL/canvas/images | Default content visible in CSS/HTML; gate reveal hides behind a JS-ready class, and pair canvas/3D scenes with semantic HTML copy |
| Accidental `noindex` or preview leaks | Staging `noindex` or `Disallow: /` copied to prod, or preview domains indexed | Isolate preview `X-Robots-Tag: noindex` from prod; verify live `robots.txt` and headers after deploy |
| Sitemap / canonical / host drift | Sitemap contains redirecting URLs, trailing-slash mismatches, `http://`, non-canonical hosts or thank-you/test pages | Emit only 200 canonical final URLs in `sitemap.xml` with `lastmod`; 301-enforce one protocol and host (`https` + apex or `www`) |
| Detached or invalid JSON-LD | Missing, broken JSON, or schema claiming FAQ/Offer/Review not present in visible HTML | Generate JSON-LD from the same server data source that renders the page and validate JSON parsing |
| Unsized hero media / eager bloat | Missing `alt`, `width`/`height` (CLS), multi-MB hero assets, or heavy client libraries loaded on first paint | Meaningful `alt`, explicit dimensions, `fetchpriority="high"` on LCP image, `loading="lazy"` below the fold, lazy-load heavy interactive libraries |
| Swapped-noun programmatic pages | Identical template pages with only a city/industry token replaced | Ship a route only when it holds distinct, verified data or proof; otherwise consolidate |

## 5-command raw-HTML verification gate

Run against the built/deployed URL before claiming a public page is done (no JavaScript):

```bash
# 1. Raw HTML has HTTP 200, real H1, hero copy, title, description, canonical, and no accidental noindex
curl -sSL -A 'Mozilla/5.0' <url> | grep -iE '<title>|<meta[^>]+description|rel="canonical"|<h1|noindex'
curl -sSL -A 'Mozilla/5.0' <url> | grep -c '<distinct hero phrase>'   # must be >= 1

# 2. Bogus URL returns a real 404/410 (never a 200 SPA shell)
curl -s -o /dev/null -w '%{http_code}\n' <url>/__nonexistent-seo-check__

# 3. Sibling routes serve distinct raw HTML (not identical shell hashes)
for u in <route-a> <route-b>; do echo "$u $(curl -sSL <origin>$u | md5 -q)"; done

# 4. Robots and sitemap resolve cleanly and carry canonical URLs
curl -sSL <origin>/robots.txt
curl -sSL <origin>/sitemap.xml | head -30

# 5. JSON-LD blocks parse cleanly
curl -sSL <url> | python3 -c "import sys,re,json; bs=re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',sys.stdin.read(),re.S|re.I); assert bs, 'no json-ld'; [json.loads(b) for b in bs]; print(len(bs), 'valid json-ld blocks')"
```
