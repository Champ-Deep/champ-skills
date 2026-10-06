# LakeB2B on the web

How the brand carries into web pages, case studies, reports and Artifacts. Built from the LakeB2B case study v2 pages (Oct 2026), which Deep approved as the reference look.

## Colour roles on screen

| Role | Value | Notes |
|---|---|---|
| Brand gradient | `linear-gradient(100deg, #6D08BE 0%, #A10FA8 45%, #E8033A 78%, #FF6903 100%)` | progress bars, chart fills for "ours", CTA panel; keep the 60/20/20 purple, red, gold balance across the page |
| Night hero | `#0B031D` to `#4E0C8E` to `#C8146F` to `#FF7A3A` to `#FFB64F` top to bottom | dark sky into a sunset; twinkling stars and soft clouds; white text only |
| Page ground | `#FDFCF8` (warm paper) and `#F2EDE5` (sand) for alternate sections | white cards sit on these |
| Ink | `#1A1230` text, `#463F5C` secondary, `#857E94` muted | purple-biased neutrals, never pure black on tinted grounds |
| Accent text | `#6D08BE` | eyebrows, active states, the brand word in a label |
| Risk | `#E8033A` outline or pill | a flag, never a fill behind body text |
| Data neutral | `#E4DEEE` | "to go", "missing" or "removed" marks |

White text passes on purple `#6D08BE` and navy `#011A6B`. Gold `#FFB703` takes dark ink text (`#0C0420`), never white.

## Type on screen

- Body and UI: Montserrat 400 to 700 (brand primary). Alata is allowed for short display labels.
- Display headlines on showcase pages: a soft serif is approved for headlines to match the editorial references (Fraunces, `SOFT` 100, weight 350 to 450). Everything else stays Montserrat.
- Data labels: IBM Plex Mono, uppercase, letter-spacing 0.12 to 0.16em.
- Google Fonts link: `Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1`, `Montserrat:wght@400;500;600;700`, `IBM+Plex+Mono:wght@400;500;600`, with Georgia, Arial and monospace fallbacks.

## Layout and components

- Full width: content to 1600px with a fluid gutter (`clamp(16px, 4.2vw, 72px)`); never a narrow centered column.
- The showcase kit (`Other/Skills/showcase-page/kit/` in the Celsus vault, skill `showcase-page`) carries the tokens, the logo pill nav, floating stat cards, charts, motion and micro-interactions already on brand. Start there for any LakeB2B case study, results page or campaign page.
- Buttons: dark ink pill with a gold arrow square (primary), white pill on gradients, translucent outline (ghost).
- CTA default: "Book a 20 minute data review" linking to `https://www.lakeb2b.com/contact-us`; secondary link `lakeb2b.com`.

## Client-facing rules that travel with the brand

- A client works with LakeB2B or SPAN, never both; never show both brands to one client.
- Never name an outside delivery vendor; vendors are "we" or "our team".
- Case studies anonymize the client by industry, size and region and never name the client's target accounts.
- Zero em dashes and en dashes in any LakeB2B output.
