# AI visibility (AEO)

Goal: when someone asks ChatGPT, Claude, Perplexity or Google's AI "who's the best <category> in <city>" or "what does <brand> cost", the AI can read the site, understand it, and quote it.

## Ship these files

### `public/llms.txt`
Plain markdown for language models. Structure:

```
# <Brand>

> One paragraph: what it is, who it's for, where, since when, who operates it (legal name, ABN/registration if public).

Not to be confused with <other companies with similar names>: <one line on how this one differs>.   (only if there's real confusion)

## Traction
Real published numbers only.

## What it does
- **<Capability>** - one line each.

## Who it is for
## Pricing        (only if public; mark the source)
## Integrations
## Results        (named case studies, one line each)
## FAQ            (verbatim)
## Links          (homepage, pricing, contact/booking, docs, login)
```

Also ship `llms-full.txt` if there are guides/docs worth including in full.

### `public/index.md`
The homepage content as clean markdown (headings, the copy, the FAQ, links). Link it from the HTML head: `<link rel="alternate" type="text/markdown" href="/index.md">`. This is the readable copy for crawlers that don't run JavaScript, essential for React/Vite single-page apps.

### JSON-LD in `index.html`
- `Organization` (or `LocalBusiness` / a specific subtype such as `AutoDealer`, `Dentist`, `Plumber` for local businesses): name, url, logo, description, telephone, address, areaServed, sameAs (socials).
- `FAQPage` with the real FAQ.
- `Product`/`Offer` for public pricing if relevant.
- `WebSite` with the site name.

Keep it in sync with the page (if the build has a prebuild script, generate it from the same data files as the page).

### `public/robots.txt`
Allow everything, and explicitly allow the AI crawlers:
GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, anthropic-ai, PerplexityBot, Perplexity-User, Google-Extended, Applebot, Applebot-Extended, meta-externalagent, cohere-ai. Point at the sitemap.

### `public/sitemap.xml`
Every public page.

### Head tags
Real `<title>` (brand + what + for whom, ≤ 60 chars), meta description (≤ 155 chars, the outcome + audience), canonical URL, OG title/description/image (1200×630), Twitter card, `theme-color` matching the nav.

## Check it

1. `curl -s <url> | grep -c "<a phrase from the hero>"`, if it's 0, the content only exists after JavaScript runs. Fix by prerendering, or make sure `index.md` and `llms.txt` carry it.
2. `curl -A GPTBot -I <url>`, should be 200, not 403 (firewalls and bot protection often block AI crawlers).
3. Validate the JSON-LD (it must parse, and the FAQ must match the page).
4. If the `aeo-check` skill is installed, run `/aeo-check <url>` before and after launch for the off-site work (directories, "best of" lists, comparison pages), that's where most AI recommendations actually come from.

## Off-site (tell the owner; don't do without asking)

AI answers lean on third-party pages: Google Business Profile, review sites, industry directories, "best <category> in <city>" lists, and comparison pages. List the gaps and draft the copy; the owner submits them.
