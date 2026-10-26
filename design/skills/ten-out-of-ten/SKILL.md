---
name: ten-out-of-ten
description: "Use when scoring or rebuilding a website to 10/10."
license: unspecified (received as a zip from Deep, 2026-10-26; origin not stated)
---

# Ten out of ten

> Original description: Give it a website URL and it builds a 10/10 version , scores the current site out of 10, scrapes its real facts, photos, testimonials and logos, rebuilds it with the design skills, Claude Design, Mobbin and 21st.dev, adds the AI-visibility (AEO) files, re-scores it, then walks you through shipping it to GitHub, Vercel and a domain. First run checks your setup and walks you through any installs and API keys. Use when someone says "/ten-out-of-ten <url>", "make my website a 10/10", "redesign my website", "score my website", "rebuild this landing page", "my site looks like AI made it", or "why doesn't my website convert".

> Hermes notes: scorecard (step 2 and 10) is the part to reuse on any site. Setup paths mention ~/.claude/skills; under Hermes the skill lives in champ-skills. For Champ microsites do not run the full rebuild: the microsite-refresh plugin owns the build, use this only to score before and after.

**Usage:** `/ten-out-of-ten <url>`. No URL? Ask for one. Built and tested on Claude Code with Opus 5.5; high effort is plenty.

Run end to end. Stop for the user only at: setup installs (step 0), the five-direction pick (step 4), paid assets (step 7) and shipping (step 11). Everything else, just do.

Turn a business website into a 10/10. The score is the point: rate the current site honestly, rebuild it, and re-rate it with the same scorecard, so the improvement is measured, not claimed.

Run the steps in order. Each step fixes a reason AI-built websites fail:

| Step | Fixes | Without it |
|---|---|---|
| 0. Setup | Missing tools mid-run | Half the steps silently skipped |
| 1. Facts & assets | Claude has nothing real to say | Invented copy, fake numbers, no logos, generic stock everything |
| 2. Score it | Nobody knows what "better" means | "It looks nicer", with no proof |
| 3. Taste rules | The default AI look | Purple gradient, Inter, centred everything, three equal cards, emoji icons |
| 4. Design system | Inconsistent, brand-less styling | Brand colour on one button, random greys |
| 5. References | Claude's layouts are the average of every site | Looks "designed" but still looks like a template |
| 6. Build to convert | Pretty but nobody acts | No proof near the top, weak CTA, how-it-works as a wall of text |
| 7. Assets (optional) | Real-world imagery the business doesn't have | Empty, abstract sections |
| 8. Mobile & speed | Most visitors are on phones | Tiny logos, horizontal scroll, 5 MB hero |
| 9. AI visibility | ChatGPT can't read or cite the site | Invisible in AI answers |
| 10. Re-score | Proves the result | A claim instead of a score |
| 11. Ship | It only exists on localhost | Nobody ever sees it |

## Ground rules (never break)

- **Never invent.** No made-up stats, testimonials, client logos, prices, awards or phone numbers. Every number, quote and logo on the page comes from step 1. If a section needs proof the business doesn't have, cut the section or leave a clearly marked `TODO` for the owner, don't fill it.
- **Don't touch the live site.** Build in a new local project. Only deploy or push when the user says so.
- **Show money before spending it.** Paid generation (step 7) needs the user's OK on a shot list and cost first.
- **Ask, don't guess, on business facts** (phone number digits, which plan is most popular, what the CTA should do). Guess freely on design.

## Step 0: Setup check

Read `references/onboarding.md` and run its check. It takes under a minute. Show the user the table, offer to install what's missing one item at a time (they say yes or no to each), and help them add any API keys. Required items must pass; everything else is optional, and the steps that need a missing tool fall back as described. If everything passes, say so in one line and move on.

## Step 1: Facts & assets

Read the current site (every page in the main nav, plus results/case-study, about, pricing, FAQ, contact). Write `_brand/facts.md`:

- What they do, for whom, where, since when. Their own words for it.
- Every number they publish, with where it came from.
- Every testimonial verbatim, with name, role, company, and photo/logo if there is one.
- Case studies: who, the problem, the result numbers.
- Client logos, integration/partner logos, awards, press.
- Offer and pricing, primary CTA and where it goes, phone, address, booking links, login link.
- FAQ verbatim.
- Brand: logo files (SVG preferred), colours sampled from the logo, current fonts.
- **Person, Pain, Promise**: one line each, in the customer's words where the site or its reviews use them. Who is this for, what's going wrong for them, what changes. The headline and every section get written from these.
- **Competitors**: the top 3-5 sites in the same niche and city, and how each one words the offer.

Download the assets into `_brand/assets/`: logos, client and partner logos, team and premises photos, case-study images, product screenshots, and any videos (explainer videos, demos, testimonials; note YouTube links rather than downloading them). Screenshot the product itself if it has a public app or demo. Keep originals; optimise copies later.

The facts sheet has **no layout, no section order and no headlines**, just facts. Layout is decided later from the scorecard and references, not inherited from the old site.

## Step 2: Score the current site

Score it with `references/scorecard.md`: 10 checks, 1 point each, each with a pass test you can actually run. Screenshot desktop (1440) and phone (390) first. Write `SCORE-before.md`: the score, one line per check (✅/❌ + the evidence), and the screenshots.

Be honest. A 6/10 site is a 6/10. The rebuild has to earn its points.

## Step 3: Taste rules

Read `references/taste.md` and apply it to everything after this step. Then layer in whichever design skills are installed. The rules in `taste.md` are the floor either way.

- **ui-ux-pro-max:** run its `--design-system` search for the business's product type and industry, and note the recommended type, palette direction and landing pattern in `_brand/DESIGN.md`.
- **Taste** (`design-taste-frontend`): follow it while building.
- **Impeccable:** run its setup once (`/impeccable init`) with the facts from step 1, so its critique knows the audience and brand.
- **Emil Kowalski's `emil-design-eng`:** use it for every interaction that moves (hover, press, menus, the few animations `taste.md` allows): easing, duration, what never to animate.

## Step 4: Design system

Write `_brand/DESIGN.md` and put the tokens into the project's CSS (`@theme` in Tailwind v4, or CSS variables):

- **The brand colour is a field, not a button.** Take it from the logo. Plan the page as a rhythm of full-width bands: dark / light / brand colour. Proof and results sit as white cards *on* the brand band.
- One accent family (brand + a deep shade + a soft tint + one light tint for text on dark). One success colour, used only for success.
- Type: one characterful sans for everything, plus a mono for numbers, times and labels. Tight tracking on headlines.
- Radius, shadow and spacing scales.

**Borrow from real systems.** The awesome-design-md collection (github.com/VoltAgent/awesome-design-md) has DESIGN.md files pulled from real brands (Stripe, Linear, Airbnb, Revolut and more). Pick the two or three closest to this business's feel and borrow their structure and discipline (type scale, spacing rhythm, how colour is rationed), never their colours, fonts or logos. The result is this brand's own `DESIGN.md`.

**Five directions, then pick.** Before locking the system, draft five genuinely different directions for the hero and one more section from the same facts (different type, colour use and layout, not five shades of one idea). On a Claude Design canvas if available, otherwise as three local HTML pages. Show the user, let them pick, and build only from the pick.

If Claude Design is available (claude.ai Artifacts with a "Design System" type), publish the system there too, tokens, a brand README, and components (Button, StatBlock, LogoTile, the hero card), and keep `src` in sync with it. Otherwise `DESIGN.md` is the source of truth.

## Step 5: References

Don't design from nothing. For each section you plan to build (hero, proof band, how it works, results, testimonials, integrations, pricing, FAQ, final CTA), find 1-2 real sites that do that section well, ideally in a similar business.

- With the **Mobbin MCP**: `search_sections` / `search_screens` with a task intent like "Redesign a <business type> marketing homepage for <audience> using real-world references", one search per section.
- **godly.website** and **Awwwards** (filter by industry) for whole-page feel and motion; **Motion Sites** for animated backgrounds; the competitors from step 1 for what this market expects.
- Without any of these: ask the user for 3 sites they love, or pick well-known best-in-class SaaS/service sites and screenshot the sections.

Blend several references per section; never rebuild one site. Take layout and structure from them, not their scroll effects (see `taste.md` § Motion).

Write what you take from each reference in `README.md` (layout and rhythm only, never copy their copy, images or brand).

## Step 6: Build to convert

Read `references/conversion.md` and build the page. Stack: whatever the project uses; default Vite + React + Tailwind v4. Every section must pass its rule in `conversion.md`. The short version:

1. **Hero**, the outcome in plain words + for whom, one primary CTA, a second "try it now" action if the product can be tried live (a phone number answered by the product, a demo, a free tool), and a product visual that shows the product working, not a stock image.
2. **Proof band** directly under the hero, real client logos (moving or static) + one plain statement of what they do.
3. **How it works** drawn, not written, icons, flow lines, real partner/system logos, max 3 routes or steps.
4. **Results** as cards: client logo, the headline result, 2-3 real numbers with icons.
5. **Testimonials** as cards with name, role, company and a face or logo.
6. **Integrations / partners** as logo tiles, grouped.
7. **Logo wall** of every client, if they have many.
8. **FAQ** using their real questions.
9. **Final CTA** on the brand band, repeating the primary CTA and the live action.

Use real logo files everywhere a tool, partner or client is named. Every section a visitor scans gets an icon cue (Lucide-style line icons, one stroke width).

**Components.** If the 21st.dev Magic MCP is connected, search it for the moving parts a section needs (logo marquee, integrations orbit, animated border, accordion, number ticker) and adapt each one to the design tokens: never ship a component in its default colours, radius or font. If the MCP isn't connected, use the component's "Copy prompt" button on 21st.dev and give that prompt to Claude, or build it by hand from the same idea.

Run it locally and send the user the link and screenshots after the first full build.

## Step 7: Assets (optional, paid)

Read `references/assets.md`. Only generate imagery where the business is physical and real-world photos would help (cars in a service bay, a clinic, a job site) and the business has none. Never for abstract SaaS concepts, and never to fake product UI. Write the shot list, model and credit cost, and get the user's OK before generating anything.

## Step 8: Mobile & speed

Read `references/qa.md`. Screenshot every section at 390px and 1440px, fix every failure, and re-screenshot. Then run the review skills that are installed, and fix what they find:

- **Vercel's `web-design-guidelines`:** reviews the code against Vercel's interface rules (focus states, forms, accessibility, layout).
- **Impeccable:** its `audit` and `critique` passes for leftover AI tells and weak hierarchy. No horizontal scroll, 44px tap targets, legible logos, the CTA reachable without hunting, images sized for their slot, and nothing heavy in the first view.

## Step 9: AI visibility (AEO)

Read `references/aeo.md` and ship the files: `llms.txt`, `index.md` (the page as markdown), JSON-LD (Organization/LocalBusiness + FAQPage), `robots.txt` allowing the AI crawlers, a sitemap, OG tags, and a check that the core content is readable without JavaScript. If the `aeo-check` skill is installed, run it on the live URL before and after launch.

## Step 10: Re-score

First, a reference check: put each section next to the reference it was built from and mark it pass or fail on one question, does it hold up beside it? Fix the fails, at most two rounds, so the build converges instead of changing forever.

Then score the new build with the same scorecard, the same way. Write `SCORE-after.md` next to the before score, with before/after screenshots. If it isn't 10/10, say which check failed and why, then fix it or tell the user what's needed from them (usually real proof the business hasn't published yet).

## Step 11: Ship

Only when the user says to. Walk them through it, or run it with them:

1. **GitHub:** make a repo and push (`gh repo create <name> --private --source . --push`, or create it on github.com and add the remote). Check nothing secret is committed first.
2. **Vercel:** sign in with GitHub, *Add New → Project*, import the repo. Vite is detected automatically (build `npm run build`, output `dist`). Deploy, and open the `*.vercel.app` URL.
3. **Domain:** *Project → Settings → Domains*, add the domain, then add the DNS records Vercel shows (an A record for the root, a CNAME for `www`) at the domain registrar.

Never point a domain that's serving a live site at the new build without the owner's explicit OK. Use a fresh domain, a subdomain, or the `vercel.app` URL until they say so. Re-run the AI visibility checks (`curl` the live URL, `aeo-check`) once it's live.

## What to hand back

- The local URL and the before/after scores side by side.
- What changed per check, one line each.
- Anything that needs the owner: missing proof, numbers to confirm, the CTA destination, domain/deploy.
- Where the files are: `_brand/facts.md`, `_brand/DESIGN.md`, `README.md` (method + references), `SCORE-before.md`, `SCORE-after.md`.
