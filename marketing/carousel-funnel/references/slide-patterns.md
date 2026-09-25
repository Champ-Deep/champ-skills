# Slide patterns and copy budgets

Read this while writing the slide JSON. It covers how many slides, what each slide does, how much text fits, and which visual block to reach for.

## Length

8 to 12 slides. Under 8 the carousel reads as a teaser and people do not save it. Over 12 the swipe-through rate collapses after slide 6 anyway. Ten is the sweet spot: hook, eight points, CTA.

For a long-form asset with N chapters, one slide per chapter is the default. If a chapter has two ideas that each need a visual, give it two slides and drop the weakest chapter.

## The three slide types

Every carousel is one hook, several points, one CTA. Nothing else.

**Hook (slide 1).** One claim, in the reader's language, that the rest of the carousel proves. Dark background so it stops the scroll. Title under 14 words, sub under 25. The kicker tells them what they are getting ("The Intent Signal Playbook, in 9 slides") so the swipe feels finite. This slide is also the document thumbnail in the feed, so the title must work with no context at all.

Hook shapes that work for B2B: a reframe ("You don't have a lead problem. You have a timing problem."), a number with a consequence ("412 accounts. No idea which 40 matter."), a rule ("Use intent to pick the account. Never to write the message."). Hooks that fail: questions, "X tips for Y", anything with "ultimate" or "secrets".

**Point (slides 2 to N-1).** One idea per slide. Number it. The title states the idea as a sentence (not a label: "One signal is close to worthless", not "Signal strength"). Then either a body paragraph OR a visual block, rarely both at full length. The optional "after" line is the takeaway in one sentence.

**CTA (last slide).** Brand background. Tells them exactly what they get and where. The link goes in the first comment, so the slide says so in words and shows the display URL. A "save this" pill is the second ask, because saves are the strongest ranking signal on LinkedIn documents. Never put a QR code, a form, or three different CTAs here.

## Copy budgets at 1080 wide

These are hard ceilings. The renderer scales a slide down when it overflows and warns you below 85 percent. A warning means cut words, not accept the scale.

| Element | Ceiling |
|---|---|
| Hook title | 14 words |
| Hook sub | 25 words |
| Point title | 12 words |
| Body paragraph | 45 words |
| After line | 25 words |
| Table | 6 rows, 3 columns, 8 words per cell |
| Steps list | 5 items, 14 words each |
| Tiers | 4 items, 20 words in "what" |
| Compare cards | 2 cards, 40 words each |
| Funnel | 6 rows, 6 word labels |
| Ladder | 4 rungs, 16 word notes |
| Whole slide | 90 words including everything |

Type never goes below 28px at 1080 wide. On a phone the carousel renders at roughly 380px, so 28px becomes 10px, which is the floor for a glance.

## Visual blocks, and when to use each

Pick the block that matches the shape of the idea. If none fits, use body text. Do not force a chart onto a sentence.

| Block | Use when the idea is | Example from the playbook |
|---|---|---|
| `stat` | one or two numbers with a consequence | 412 accounts to 40 |
| `ladder` | something gets stronger or weaker in stages | weak, better, strong, very strong signals |
| `table` | a scoring rubric, a mapping, a lookup | six dimensions and weights; recency days to score |
| `steps` | a numbered procedure the reader will follow | five minutes, five questions |
| `tiers` | buckets with a rule and an action each | Tier 1, 2, 3, disqualify |
| `compare` | a bad example against a good one | never write vs same account, better |
| `funnel` | a count narrowing through gates | 100 to 60 to 25 to 12 to 7 to 5 |
| `quote` | one sentence that deserves the whole slide | "Intent tells you the timing. Fit tells you whether the timing is worth anything." |
| `list` | three to five parallel points, no order | four signal families |

## Reading order on each slide

Eye lands on the number, then the title, then the visual, then the after line. Write the title so that someone who reads only titles across all ten slides gets the whole argument. Test this by reading the titles in sequence before rendering.

## Bold inside text

`**text**` inside any string renders bold in the brand colour. Use it for the one phrase per slide that carries the idea. More than one bold phrase per block and none of them stand out.

## Theme overrides

Any slide accepts `"theme": "dark" | "brand" | "soft" | ""`. Default is dark for the hook, brand for the CTA, white for points. Use `soft` (light tint) on at most one mid-carousel slide to reset the eye, typically the quote slide.

## What not to do

No stock photos or AI-generated imagery on B2B document carousels. They read as an ad and the post gets scrolled. No emojis in slide copy. No hashtags on slides. No page-one logo bigger than the wordmark in the chrome. No "swipe" arrow on any slide except the first. No em dashes or en dashes anywhere; the renderer refuses the file if it finds one.
