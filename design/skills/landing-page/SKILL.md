---
name: landing-page
description: "Design and build landing pages, marketing sites, product pages, campaign pages, and pre-launch pages that convert rather than merely look finished. Covers the message hierarchy (what the page has to say before it can be designed), five hero patterns and when each one works, proof and objection handling, section architecture that avoids the same-shape-every-section tell, CTA discipline, mobile-first fold budgeting, and a conversion-specific anti-slop pass. MANDATORY TRIGGER for: landing page, marketing page, product page, homepage, hero section, above the fold, pricing page, waitlist or coming-soon page, campaign or event page, squeeze page, sales page, 'page that converts', 'make our site sell', or rewriting a hero headline. Pairs with frontend-design for the design system, ui-polish for refinement, and visual-verify as the closing gate."
---

# Landing Page

A landing page is not a website that happens to be short. It is an argument, delivered in a fixed order, to a person who has already decided to leave. Everything about it is downstream of one question: **what does this person need to believe, and in what sequence, before acting?**

Most AI-built landing pages fail before a single pixel is placed, because they start with layout. A hero, three feature cards, a testimonial row, a pricing table, a footer. That template is not a design, it is the absence of one. It looks finished, which is what makes it dangerous.

This skill runs the argument first, the layout second, and the render gate last.

---

## Phase 1: The message, before any layout

Answer these five in writing. Ten minutes here saves a rebuild.

**1. Who is arriving, and from where?** A visitor from a founder's LinkedIn post already trusts the person and needs to know what the product does. A visitor from a search for "b2b healthcare data provider" knows what they want and needs to know why you. Same product, different first sentence. If traffic comes from more than one place with genuinely different context, that is an argument for more than one page, not a compromise headline serving neither.

**2. What is the one thing they must believe?** Not five things. One. Everything else on the page supports it or gets cut. Write it as a sentence: *"This is the only data provider that can reach clinical decision-makers at mid-size hospitals, and the data is actually current."*

**3. What do they already believe that is in the way?** Every category carries a default suspicion: it will be a nightmare to integrate, the data will be stale, it will be too expensive, we tried this before and it failed. Name the top two. These are not FAQ material, they are the reason the page has a middle section.

**4. What is the single action?** One. A page offering "book a demo," "start free," "download the report," and "join the newsletter" is a page with no opinion about what happens next, and the visitor resolves that ambiguity by leaving.

**5. What is the strongest true thing you can prove?** A number, a named customer, a screenshot of the product doing the job, a result with a date on it. This is the load-bearing element of the entire page. If the answer is "nothing yet," that is fine and important: a pre-proof page is built differently, leaning on specificity and demonstration rather than social proof, and pretending otherwise with fake logos destroys the trust it borrows.

**Write the answers into the DESIGN.md** alongside the design read and the dials from `frontend-design`. The design decisions that follow are judged against these, not against taste.

---

## Phase 2: The headline

More conversion is won and lost here than in the rest of the page combined, and it is the part most likely to be filled with something that sounds like a headline.

**The test:** could a competitor put their logo on this sentence without it becoming false? If yes, it is not a headline, it is category description. *"Built for modern teams."* *"The all-in-one platform for growth."* *"Where innovation meets execution."* These are placeholders that survived.

**What works, roughly in order of strength:**

| Pattern | Shape | Works when |
|---|---|---|
| Specific outcome | "Reach 40,000 verified hospital decision-makers by Friday" | You can name the outcome and the timeframe |
| Named mechanism | "Verified quarterly by phone, not scraped" | Your differentiator is a method competitors cannot claim |
| Sharp problem statement | "Your CRM is 40% dead contacts" | The pain is felt, unnamed, and you can prove the number |
| Direct definition | "Payroll for Indian startups hiring their first employee" | The category is crowded and clarity beats cleverness |
| Contrarian position | "Stop enriching data you should be deleting" | You have earned an audience and a point of view |

**Rules:** under twelve words if you can. The subhead does the qualifying, not the headline. Say the thing rather than promising to say it ("Here's how we help you grow" says nothing). Cut every intensifier: *seamlessly*, *effortlessly*, *truly*, *simply*. Write it in your customer's words, and if you have their words in a sales call transcript or a support ticket, use those directly. Nothing you invent will beat a sentence a real buyer already said.

**The subhead** does one job the headline could not fit: who it is for, or how it works, or the qualifying constraint. One sentence. If the subhead repeats the headline in longer form, delete it.

---

## Phase 3: The hero

The fold is the whole page for most visitors. Budget it deliberately.

**Five patterns, and when each earns its place:**

1. **Product-forward.** Headline, subhead, one CTA, and a large, framed, real screenshot. The default for software, and the strongest choice whenever the product is visually legible in one frame. People believe what they can see working.
2. **Demonstration.** The hero *is* the product: a live input, a working calculator, a real search box, a sample of the output. The highest-converting pattern that exists, and the most expensive to build. Worth it when the value is obvious in three seconds of interaction.
3. **Outcome-forward.** A single large number or result, with the proof attached. Works when the outcome is more compelling than the interface, which is common for services and data products.
4. **Editorial.** Type-led, no image, generous space. Works for strong points of view, developer tools, and premium positioning. Fails without excellent typography, because there is nothing else on screen to carry it.
5. **Split narrative.** Before on one side, after on the other. Works for transformation products where the gap is visual. Overused; make sure the two states genuinely differ.

**Fold budget on mobile.** Most traffic arrives at 390px, and this is where the fold is actually decided. Between a sticky nav, a cookie banner, and an announcement bar, three quarters of the fold can be gone before the headline appears. Render at 390 and check: **the headline, one line of subhead, and the primary CTA must all be visible without scrolling.** If they are not, cut something. The desktop hero is the easy case and the one everyone checks.

**The hero visual.** If it is a product screenshot: frame it, crop to the single moment that proves value rather than showing the whole cluttered app, populate it with real and plausible data, and let it be genuinely large. A screenshot too small to read is decoration. Never a stock illustration of a person at a laptop, never an abstract 3D shape, never a dashboard mockup built from divs pretending to be a screenshot.

---

## Phase 4: Section architecture

**The single strongest structural tell of a generated landing page is that every section has the same shape.** Centred heading, centred subhead, then a grid. Six times down the page. Real pages vary their architecture because different arguments want different containers.

Build the middle of the page as a **sequence of claims**, each with the evidence attached, in the order the visitor needs them. A workable spine:

```
Hero                        the claim
Proof strip                 permission to keep reading
Problem, named              agreement, and the reason to care
How it works                mechanism, so the claim is credible
Evidence in depth           one case, specific, with numbers
Objection handled           the thing they were about to say
Pricing or scope            the risk, made concrete
Close                       the same CTA, restated
```

Then give each one a **different shape**: one full-bleed, one narrow and centred, one asymmetric two-column, one dense table, one large quiet number. Alternating image-left and image-right more than twice reads as a template. Vary the background surface between sections rather than tinting every second one grey.

**On feature grids.** Three identical cards in a row is the default AI layout and the audit flags it. If you use a grid, break its uniformity deliberately: make one card wider, give the most important one a real screenshot while the others carry text, or replace the grid entirely with a numbered sequence when the features have an order. If three features genuinely matter equally, a grid is honest, but check that assumption first.

**Length.** Higher price and higher risk means longer page: an enterprise contract needs the objections handled, a $9 tool does not. A free signup can convert in one screen. Length is a function of what has to be believed, never a target.

---

## Phase 5: Proof

Proof is what the page is made of. Everything else is scaffolding around it.

**Strength order, strongest first:** a live demonstration; a specific customer result with a name, a number and a date; a real screenshot with real data; a named testimonial with a face and a job title; a customer logo row; a raw usage metric; a press mention; a trust badge. Most pages lead with the weakest items on that list because they are the easiest to produce.

**What kills proof:** a testimonial with no name. A logo row for companies that ran a pilot two years ago. A number with no denominator ("10,000+ users" of what, since when). Awards nobody has heard of. Star ratings with no source. Every one of these reads as a substitute for evidence, which is exactly what it is, and a visitor who catches one discounts the rest of the page.

**If you have no proof yet:** say so and compensate with specificity. A precise description of the mechanism, a real screenshot of the working product, a founder's actual name and face, and a concrete guarantee will outperform borrowed credibility every time. "We are three weeks old, here is exactly what it does, here is my email" converts better than a fake logo wall.

**Placement.** One light proof element inside or immediately below the fold, so the visitor has permission to continue. The heavy proof goes in the middle, right after the mechanism, where scepticism peaks. One closing proof next to the final CTA, where the decision happens.

---

## Phase 6: Call to action

- **One primary action per page.** Repeat it; do not multiply it. A secondary link (docs, pricing) is fine as a text link, visually subordinate, never as a second button of equal weight.
- **Label the outcome, not the mechanism.** "Get the hospital dataset" beats "Submit". "Start free, no card" beats "Sign up".
- **Reduce the felt cost right at the button.** One short line underneath: no card required, two minutes to set up, cancel anytime, 400 free records. This single line moves more numbers than the button colour ever will.
- **Ask for the minimum.** Every extra form field costs conversions. Email alone if email alone will do. If sales needs company size, ask after the signup, not before.
- **Repeat at natural decision points**, not at fixed intervals: after the hero, after the main evidence, after pricing, at the close.
- **Sticky CTA on mobile**, once the hero has scrolled past. Not before, or it competes with the hero's own button.

---

## Phase 7: Conversion-specific anti-slop

Beyond the general tells in `ui-polish`, these are specific to marketing pages:

| Tell | Fix |
|---|---|
| Headline that any competitor could claim | The swap test. Rewrite until it becomes false for them. |
| Three identical feature cards | Break the uniformity or replace with a sequence |
| Every section the same shape | Vary the architecture: full-bleed, narrow, asymmetric, dense |
| Stock illustration or abstract 3D blob in the hero | Real product, real screenshot, or nothing at all |
| A fake dashboard built out of divs | An actual screenshot of the actual product |
| Unnamed testimonials | Name, role, company, face. Or cut it. |
| Unbacked precision: 99.99%, 10x, +240% | Source it or cut it. Costs more trust than it buys. |
| Invented brand names and people: Nexus, SmartFlow, Jane Doe | Real, or clearly labelled as illustrative |
| An eyebrow label above every heading | One per three sections at most |
| Section numbers as decoration | Cut them |
| Fake ambient detail: live clocks, locale strips, unset version badges | Cut. Texture pretending to be information. |
| Two CTAs meaning the same thing | One intent per screen |
| Gradient text, purple-to-blue, cyan on dark | One considered palette, emphasis via weight and size |
| Feature list where a benefit belongs | Say what it does for them, then how it works |
| "Trusted by teams worldwide" with no names | Name three, or say nothing |
| Copy that hedges: helps you to potentially improve | State the claim |
| Em-dashes in generated copy | A recognisable tell. Restructure the sentence. |

---

## Phase 8: Verify — MANDATORY

A landing page that has not been rendered at 390px has not been designed.

```bash
python3 visual-verify/scripts/audit.py index.html --width 390
python3 visual-verify/scripts/audit.py index.html --width 1440
python3 visual-verify/scripts/shoot.py index.html --widths 390,834,1440 --themes light,dark
```

Then open every screenshot with the Read tool and run these four, in this order:

1. **The five-second test on the 390 fold shot.** What is this, who is it for, what do I do next. If any of the three is unanswerable from the fold alone, the page fails, and no amount of styling fixes it.
2. **The swap test on the full-page shot.** Competitor's logo, nothing else changed. Would it still be true and still look right? If yes, the page has no argument, only a template.
3. **The mobile fold check.** Headline, one line of subhead, primary CTA, all visible at 390 without scrolling. Count what the nav and any banner ate.
4. **The scroll narrative.** Read only the headings, top to bottom, in the full-page shot. Do they tell a coherent story on their own? A visitor who scans nothing else reads exactly that sequence.

Fix, re-render, compare the before and after images directly. Two rounds is normal.

→ Full protocol: the `visual-verify` skill. Design system and tokens: `frontend-design`. General polish: `ui-polish`.

---

## Working with brand skills

If a Champions Group or venture brand skill is loaded (Champions Group, LakeB2B, Ampliz, and others), its tokens and voice win over anything here. This skill supplies the argument structure and the conversion discipline; the brand skill supplies the colour, type, and tone. Where they conflict, brand wins on appearance and this skill wins on structure. A page that is perfectly on-brand and makes no argument is still a page that does not convert.
