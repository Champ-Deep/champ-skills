# Slide patterns and copy budgets

Read this while writing the slide JSON. It covers how many slides, what each slide does, how much text fits, and which visual block to reach for.

## Length

8 to 12 slides. Under 8 the carousel reads as a teaser and people do not save it. Over 12 the swipe-through rate collapses after slide 6 anyway. Ten is the sweet spot: hook, eight points, CTA.

For a long-form asset with N chapters, one slide per chapter is the default. If a chapter has two ideas that each need a visual, give it two slides and drop the weakest chapter.

## The three slide types

Every carousel is one hook, several points, one CTA. Nothing else.

**Hook (slide 1).** One claim, in the reader's language, that the rest of the carousel proves. Dark background so it stops the scroll, and one object from the buyer's world under the title (a `uicard` of their queue, a `stats` pair, an `account` card) so the cover is never type on a flat field. Title under 14 words, sub under 25. The kicker tells them what they are getting ("The Intent Signal Playbook, in 9 slides") so the swipe feels finite. This slide is also the document thumbnail in the feed, so the title must work with no context at all.

Hook shapes that work for B2B: a reframe ("You don't have a lead problem. You have a timing problem."), a number with a consequence ("412 accounts. No idea which 40 matter."), a rule ("Use intent to pick the account. Never to write the message."). Hooks that fail: questions, "X tips for Y", anything with "ultimate" or "secrets".

**Point (slides 2 to N-1).** One idea per slide. Number it. The title states the idea as a sentence (not a label: "One signal is close to worthless", not "Signal strength"). Then either a body paragraph OR a visual block, rarely both at full length. The optional "after" line is the takeaway in one sentence.

**CTA (last slide).** Brand background. Tells them exactly what they get and where. A `page` block renders a browser-window mock of the landing page (URL, title, chips such as "8 chapters", "12 min read", "Free, no form") so the reader sees the destination before they go looking for the link. The link goes in the first comment, so the slide says so in words. A "save this" pill is the second ask, because saves are the strongest ranking signal on LinkedIn documents. Never put a QR code, a form, or three different CTAs here.

## Copy budgets at 1080 wide

These are hard ceilings. The renderer scales a slide down when it overflows and warns you below 85 percent. A warning means cut words, not accept the scale.

| Element | Ceiling |
|---|---|
| Hook title | 14 words |
| Hook sub | 25 words |
| Point title | 12 words |
| Body paragraph | 45 words |
| After line | 25 words |
| Bars | 6 rows, 12 word notes |
| Columns | 5 columns, 3 word labels |
| Bento | 4 cards, 20 words of text each |
| Timeline | 5 steps, 14 words each |
| Messages | 2 bubbles, 40 words each |
| uicard | 5 rows, 6 word meta |
| Stats | 3 tiles, 14 word labels |
| Whole slide | 90 words including everything |

Sentences never go below 22px at 1080 wide, and uppercase tracked labels (chips, axis) never below 15px. On a phone the carousel renders at roughly 380px, so 28px becomes 10px, which is the floor for a glance.

## Visual blocks, and when to use each

Pick the block that matches the shape of the idea. A slide may carry one or two blocks (`"visual"` or `"visuals": [...]`). If none fits, use body text. Do not force a chart onto a sentence, and do not put two charts on one slide.

| Block | Use when the idea is | Example from the playbook |
|---|---|---|
| `uicard` | the buyer's own screen: a list, a queue, a saved view. Hot rows get the gold tint, the rest go dim | the 412-account saved view on the cover |
| `stats` | one to three numbers with a consequence, as tiles (`cls: "gold"` on the one that matters) | 412 in the view, 40 worth a call |
| `bars` | a ranking, weights, a ladder, or a count narrowing through gates. Set `hi: true` on exactly one row | signal stack; scorecard weights; the 100 to 5 funnel |
| `columns` | a value over ordered buckets, especially decay or growth | recency score by days |
| `bento` | two to four buckets with a rule and an action each | Tier 1, 2, 3, disqualify |
| `timeline` | a numbered procedure with a time or stage label per step | five minutes, five questions |
| `messages` | a bad example against a good one, in the medium they happen in | never write vs same signal, better |
| `account` | one entity scored on several dimensions | Kelso Freight Systems, 92 |
| `card` | one sentence or template that deserves a frame, with a chip label | the hypothesis sentence |
| `quote` | one sentence that deserves the whole slide | "Intent tells you the timing. Fit tells you whether the timing is worth anything." |
| `table` | a lookup that is truly tabular and will not read as a chart. Last resort | none in the example any more |
| `list` | three to five parallel points, no order | four signal families |

Chart rules (from `dataviz`): one series per chart, one highlighted mark in gold, values and labels in ink or muted (never in the series colour), no gradients or effects on any bar, zero values still visible as a stub, categorical hues never cycled. Two measures never share one chart.

Vary the architecture slide to slide. Two consecutive slides with the same block is the strongest structural tell; the example runs title over UI card, tiles, bars, bars (different label widths and a different story), columns, bento, timeline plus card, messages, bars plus account card, CTA with page mock.

## Reading order on each slide

Eye lands on the number, then the title, then the visual, then the after line. Write the title so that someone who reads only titles across all ten slides gets the whole argument. Test this by reading the titles in sequence before rendering.

## Type and colour are locked by the brand skill

The template ships in LakeB2B's faces (Montserrat display, Alata labels) and palette. Another brand changes the four colour tokens in the JSON `brand` block and, if its brand skill names different faces, `display_font` and `label_font`. No serif display faces on any Champions Group data brand: they read as the AI-editorial default. See `references/design-system.md` for the full contract and the trend register.

## Bold inside text

`**text**` inside any string renders bold in the brand colour. Use it for the one phrase per slide that carries the idea. More than one bold phrase per block and none of them stand out.

## Theme overrides

Any slide accepts `"theme": "dark" | "brand" | ""`. Default is dark for the hook, brand for the CTA, paper for points. Dark and brand slides carry the dot-grid texture; paper slides are flat by design because they hold the data.

## What not to do

No stock photos or AI-generated imagery on B2B document carousels. They read as an ad and the post gets scrolled. No emojis in slide copy. No hashtags on slides. No page-one logo bigger than the wordmark in the chrome. No coloured side-stripe borders on cards (the single most recognisable AI-dashboard tell). No serif display type. No "swipe" arrow on any slide except the first. No em dashes or en dashes anywhere; the renderer refuses the file if it finds one.
