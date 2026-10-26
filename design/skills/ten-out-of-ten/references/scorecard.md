# The 10/10 scorecard

Ten checks, one point each. A check passes only if its test passes; no half points. Score the old site and the new build the same way, from screenshots at 1440px and 390px plus the source.

## 1. Five-second clarity
**Test:** show only the first screen (desktop and phone). Can a stranger say what the business does, for whom, and what to do next? The headline names an outcome the customer wants, in their words; the subhead says who it's for and how.
**Fails:** a slogan with no product in it ("The future of X"), jargon, or the "what" only appearing below the fold.

## 2. One clear action
**Test:** there is one primary CTA, it's visible in the first screen on desktop *and* phone, it says what happens ("Book a call", not "Submit"), and it repeats at least at the middle and end of the page. If the product can be tried instantly (call the AI, open a demo, run a free check), that's offered as a second action next to it.
**Fails:** three competing primary buttons, a CTA only in the nav, or no CTA in the first phone screen.

## 3. Proof near the top
**Test:** within one scroll of the top there is real proof: client logos, a specific number, or a named result.
**Fails:** proof only appears halfway down, or the only "proof" is generic ("trusted by thousands").

## 4. Specific, named proof
**Test:** results name the client and give specific numbers ("412 jobs booked in March for Harbourside Plumbing"); testimonials have a name, role, company and a face or logo.
**Fails:** anonymous quotes, round invented-looking numbers, or no results at all. (If the business has no proof yet, this check fails honestly, report it as the owner's to-do.)

## 5. Shown, not told
**Test:** how it works / the product is shown visually: a diagram, flow, real UI, or a live demo, with icons and real partner logos. A reader who skips every paragraph still understands it.
**Fails:** how-it-works is a block of text or three numbered paragraphs.

## 6. Doesn't look AI-made
**Test:** none of the tells in `taste.md` § "AI tells" appear: default fonts (Inter/Roboto/Arial as the only face), a purple-blue gradient hero, centred-everything layout, three identical cards in a row as the main feature section, emoji used as icons, gradient headline text, invented-looking avatars.
**Fails:** two or more tells.

## 7. On-brand
**Test:** the brand colour comes from the logo and is used with intent across the page (bands, accents, numbers), with a consistent set of tokens (one radius scale, one shadow, one type pairing). The logo is crisp.
**Fails:** brand colour only on a button, mismatched greys, mixed radii, a blurry logo.

## 8. Works on a phone
**Test:** at 390px: no horizontal scroll, body text ≥ 15px, tap targets ≥ 44px, logos and numbers legible, nothing overlapping, the menu works, and the primary CTA (or the phone number) is reachable from the menu or first screen.
**Fails:** any one of those.

## 9. Fast
**Test:** the first screen has no image over ~200 KB, below-the-fold images are lazy-loaded, logos are sized for their slot (not 2000px PNGs), video is lazy or click-to-load, and the JS bundle is reasonable for the stack (a landing page under ~300 KB gzipped total for the first view).
**Fails:** a multi-megabyte hero, an embedded video iframe in the first view, or unoptimised logo walls.

## 10. Findable by AI
**Test:** the core content (what they do, where, prices if public, FAQ) is readable without JavaScript (server-rendered HTML, or a linked markdown copy), and the site ships `llms.txt`, JSON-LD (Organization or LocalBusiness + FAQPage), a `robots.txt` that doesn't block GPTBot / OAI-SearchBot / ClaudeBot / PerplexityBot / Google-Extended, a sitemap, and a real title, meta description and OG image.
**Fails:** a JS-only page with no markdown copy, crawlers blocked, or no structured data.

## Writing the score

```
# <Site>: 6/10 (before)

| # | Check | | Evidence |
|---|---|---|---|
| 1 | Five-second clarity | ✅ | "Emergency plumbing in 60 minutes" + "for homes in Sydney's inner west" in the first screen |
| 2 | One clear action | ❌ | "Book a Call" hidden in the nav on phones |
...
```

Evidence is something a reader can check: a quote from the page, a measurement, a screenshot reference. Never "looks good".
