# Champions Ranch: Component Library

Copy-paste HTML blocks for assembling Champions Ranch documents. The full
stylesheet lives in the `<head>` of `assets/proposal_template.html`. To build a
new document, start from that template (it already carries the CSS, cover, and
footer), then keep, drop, or duplicate the body blocks below.

## How rendering works

1. Edit an HTML file (start from `assets/proposal_template.html`).
2. Render to PDF:
   `python scripts/build_pdf.py yourdoc.html yourdoc.pdf`
3. Optional token fill: `python scripts/build_pdf.py yourdoc.html out.pdf --vars vars.json`
   where `vars.json` maps `{"TOKEN": "value"}` for any `{{TOKEN}}` in the HTML.

Dependency: `pip install weasyprint --break-system-packages`. The CSS has font
fallbacks, so it renders even without Lora and Poppins installed.

## CSS variables (already defined in the template)

```
--green:#2F7D3F  --dark:#1A5C2A  --deep:#143F1E
--gold:#D4AF37   --gold-deep:#B4912A
--brown:#8B6F47  --barn:#C1440B
--cream:#F5EFE0  --paper:#FFFDF8  --ink:#28301F  --muted:#6E6A5C
--charcoal:#2D2D2D  --champgold:#C9A84C   (parent lockup only)
```

## Cover (tokenized version)

The template ships a concrete cover. For a fresh document, this token version is
easy to fill with `--vars`. Keep the `<svg class="scene">` from the template.

```html
<div class="cover">
  <div class="cover-top">
    <p class="eyebrow">An InfraTech Property · Champions Group</p>
    <p class="wordmark">Champions Ranch</p>
    <div class="cover-rule"></div>
  </div>
  <div class="hero-head">
    <h1>{{HERO_LINE1}}<br>{{HERO_LINE2}}</h1>
    <p class="hero-sub">{{SUBTITLE}}</p>
    <p class="hero-tag">&ldquo;{{TAGLINE}}&rdquo;</p>
  </div>
  <!-- keep the <svg class="scene"> ... </svg> from proposal_template.html here -->
  <div class="cover-meta">
    <p class="mh">{{META_HEADING}}</p>
    <table class="meta-grid">
      <tr>
        <td><span class="k">{{K1}}</span><span class="v big">{{V1}}</span></td>
        <td><span class="k">{{K2}}</span><span class="v">{{V2}}</span></td>
        <td><span class="k">{{K3}}</span><span class="v">{{V3}}</span></td>
      </tr>
    </table>
  </div>
  <div class="cover-foot">
    <span>Champions Ranch &middot; Sarjapur Road, Bangalore</span>
    <span>30 Minutes From Your Desk</span>
  </div>
</div>
```

Snapshot rule: only show fields you actually have. Group Size, Stay Format, and
Prepared By are always safe. Add Prepared For, Primary Contact, and Stay Dates
only when known. Never ship a visible `[bracket]` placeholder. If you have six
fields, use two `<tr>` rows of three.

## Section header

Every body section starts on a new page (the `.sheet` wrapper). Swap the SVG for
the horseshoe, house, or compass motif from the template.

```html
<div class="sheet">
  <div class="kicker">
    <svg class="hs" viewBox="0 0 40 40"><path d="M20 4 C10 4 4 12 4 22 C4 31 11 36 11 36 L15 31 C15 31 10 28 10 21 C10 15 14 10 20 10 C26 10 30 15 30 21 C30 28 25 31 25 31 L29 36 C29 36 36 31 36 22 C36 12 30 4 20 4 Z" fill="#D4AF37"/></svg>
    <span class="kt">Section kicker</span>
  </div>
  <h2 class="section">Section title</h2>
  <div class="section-rule"></div>
  <!-- section body -->
</div>
```

## Experience card (title + price + prose + checklist)

Use `.xhead` (Ranch Green) or `.xhead.alt` (Dark Green) to alternate.

```html
<div class="xcard">
  <div class="xhead">
    <span class="xt">Card title</span>
    <span class="xp">150 guests &times; &#8377;1,500<b>&#8377; 2,25,000</b></span>
  </div>
  <div class="xbody">
    <p>One or two sentences of grounded, warm description.</p>
    <table class="checks">
      <tr><td>Item one</td><td>Item two</td><td>Item three</td></tr>
    </table>
  </div>
</div>
```

## Line-item / rooms table

```html
<table class="rooms">
  <tr><th>Item</th><th class="r">Qty</th><th class="r">Guests</th><th class="r">Amount (&#8377;)</th></tr>
  <tr><td class="roomname"><b>Name</b> <span>detail</span></td><td class="r">4</td><td class="r">12</td><td class="r num">18,000</td></tr>
  <tr class="sub"><td>Subtotal</td><td class="r">15</td><td class="r">~50</td><td class="r num">80,995</td></tr>
</table>
```

## Checklist grid

```html
<table class="checks">      <!-- add class "two" for two columns -->
  <tr><td>Welcome drinks</td><td>Buffet lunch</td><td>Buffet dinner</td></tr>
</table>
```

## Commercial summary + per-person highlight

```html
<table class="bill">
  <tr><td class="lbl">Line item</td><td class="amt num">&#8377; 80,995</td></tr>
  <tr class="subtot"><td>Sub-total</td><td class="amt num">&#8377; 6,55,230</td></tr>
  <tr class="gst"><td>GST @ 18%</td><td class="amt num">&#8377; 1,17,941</td></tr>
  <tr class="grand"><td>Grand Total</td><td class="amt num">&#8377; 7,73,171</td></tr>
</table>

<div class="pp">
  <div class="ppl">All-in, per guest<span>150 guests · inclusive of GST</span></div>
  <div class="ppv">&#8377;5,154<small> / pax</small></div>
</div>
```

Always verify money before rendering: line items sum to the sub-total, GST is
18% of the sub-total, grand total is sub-total plus GST, per-person is grand
total divided by headcount.

## What is included (cream list)

```html
<div class="incl">
  <h4>What is included</h4>
  <ul><li>Inclusion line</li></ul>
</div>
```

## Numbered terms

```html
<ul class="terms">
  <li><span class="tn">1</span><b>Validity.</b> Holds for 30 days from issue.</li>
</ul>
```

## Closing quote + sign-off + lockup

```html
<div class="closing-quote">
  <p>The warm closing thought (Lora, on deep green).</p>
  <p class="small">A short final line. Looking forward to hosting you.</p>
</div>
<div class="sign">
  <p class="sr">Warm regards,</p>
  <p class="sn">Champions Ranch Team</p>
  <p class="so">Champions Ranch &middot; Sarjapur Road, Bangalore</p>
</div>
<div class="lockup">
  <div class="l1">Champions Ranch &middot; An InfraTech Property &middot; A <span class="gd">Champions Group</span> Experience</div>
  <div class="l2">Time Worth Spending.</div>
</div>
```

## Stat chips (single row)

```html
<div class="callout-distance row4">
  <div class="chip"><div class="cn">30 min</div><div class="cl">From Sarjapur Road</div></div>
  <!-- repeat; row4 keeps them on one line -->
</div>
```

## Motif SVGs (drop into `.kicker .hs` or the cover)

- Horseshoe: `<path d="M20 4 C10 4 4 12 4 22 C4 31 11 36 11 36 L15 31 C15 31 10 28 10 21 C10 15 14 10 20 10 C26 10 30 15 30 21 C30 28 25 31 25 31 L29 36 C29 36 36 31 36 22 C36 12 30 4 20 4 Z" fill="#D4AF37"/>`
- House: `<path d="M20 6 L34 17 L34 34 L24 34 L24 24 L16 24 L16 34 L6 34 L6 17 Z" fill="#D4AF37"/>`
- Compass: `<circle cx="20" cy="20" r="15" fill="none" stroke="#D4AF37" stroke-width="3"/><path d="M20 9 L20 31 M9 20 L31 20" stroke="#D4AF37" stroke-width="3" stroke-linecap="round"/>`
