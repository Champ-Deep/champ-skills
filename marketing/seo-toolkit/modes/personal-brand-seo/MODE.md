# Mode: personal-brand-seo

Use when a person (Deep first) wants to own the results for their own name and role, and show up when answer engines are asked who they are. Different from a company audit: the unit is an entity, not a keyword set.

## Procedure

1. **Name SERP snapshot.** `web_search` the exact name in quotes, the name plus title, and `domain + name`, top 8 each. Table: rank, URL, who controls it (owned, platform profile, third party data page, company page). Date it and state that the search tool's engine is not a confirmed Google result. Ahrefs `site-explorer-top-pages` on the personal domain says whether any page ranks at all (empty means none in that country's index).
2. **Owned-site crawl.** `scripts/crawl_sitemap.py https://site/ build/`. Read the headline counts, then the pages with no canonical, no JSON-LD, duplicate titles or descriptions, thin pages, and the share of sitemap URLs that redirect.
3. **Entity basics, check each.** Full legal name in the home title tag and H1 text, not only the meta description. A dedicated about or bio page. `Person` JSON-LD on the home page with `name`, `jobTitle`, `worksFor`, `url`, `image`, and `sameAs` listing every real profile (LinkedIn, YouTube, X, GitHub, company page). The same name, headline and photo on every profile. A homepage heading that crawlers read as words: letter-by-letter animation can put each letter in its own element, so read the rendered H1 text.
4. **Technical hygiene.** Sitemap URLs equal the final URLs (no redirect on every entry), canonical equal to the final URL, `lastmod` present, a unique description on every page type that matters, alt text on images that carry meaning.
5. **AI crawler policy is a decision, not a fix.** Read robots.txt before advising. Blocking training crawlers (for example GPTBot, ClaudeBot, Google-Extended) is a legitimate choice; separate search or retrieval agents from them by reading each vendor's current documentation before editing, because the user-agent names change. Present the trade-off, the owner decides.
6. **Owned content that earns the name.** Evergreen pages with first-hand proof: tools shipped, files given away, numbers with a source. A page per signature idea beats a log of weekly posts for search; keep both. Link each from the home and the about page.
7. **Third-party surfaces.** List data-aggregator pages about the person (director databases, directories). Do not try to remove them; make sure the owned and profile results outrank or sit beside them.

## Rules

- No fixes on a live personal site without the owner's yes. Stage a card with exact edits and the check that proves each one.
- Measure from the start: record the name SERP table and the Ahrefs result on day 0, repeat monthly. No ranking promise.
- Never invent profile URLs for `sameAs`; use only ones the owner confirms.
