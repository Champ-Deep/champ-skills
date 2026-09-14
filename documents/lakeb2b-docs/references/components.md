# [[Lake B2B|LakeB2B]]: Component Library

Copy-paste HTML blocks for assembling [[Lake B2B|LakeB2B]] documents. The full stylesheet
lives in the `<head>` of `assets/document_template.html`. Start from that
template (it carries the CSS, the gradient cover, and the footer), then keep,
drop, or duplicate the body blocks below.

## How rendering works

1. Edit an HTML file (start from `assets/document_template.html`).
2. Render: `python scripts/build_pdf.py yourdoc.html yourdoc.pdf`
3. Optional token fill: `python scripts/build_pdf.py yourdoc.html out.pdf --vars vars.json`
   where `vars.json` maps `{"TOKEN":"value"}` for any `{{TOKEN}}` in the HTML.

Dependency: `pip install weasyprint --break-system-packages`. Fonts fall back to
Poppins (for Montserrat) and DejaVu Sans Mono (for JetBrains Mono), so it always
renders. Install Montserrat and JetBrains Mono for exact brand fidelity.

WeasyPrint note: multi-column flex with wrapping is unreliable, so two-up card
grids render as full-width stacked cards. That stacked look is the reliable,
on-brand default. Process flow and single-row chip strips (no wrap) work fine.

## CSS variables (defined in the template)

```
--purple:#6D08BE  --purple-deep:#46067E  --purple-ink:#2C0A4A  --navy:#011A6B
--gold:#FFB703  --red:#E8033A  --magenta:#DD1286  --teal:#0095A0
--orange:#FF6903  --lavender:#7A76DA
--ink:#1C1430  --muted:#6B6480  --line:#E7E2F0  --wash:#F4ECFD  --paper:#FFFFFF
```

## Cover (tokenized)

Keep the `<svg class="cover-bg">` network motif from the template. Snapshot rule:
only show fields you have. Document, Verticals, and Prepared by are always safe.
Add client name, contact, and date only when known. Never ship a visible
`[bracket]` or empty `{{TOKEN}}`.

```html
<div class="cover">
  <!-- keep <svg class="cover-bg"> ... </svg> from the template -->
  <div class="cover-inner">
    <div class="brandrow">
      <!-- keep <svg class="brandmark"> ... </svg> -->
      <span class="brandname">Lake<b>B2B</b></span>
    </div>
    <div class="cover-eyebrow">{{EYEBROW}}</div>
    <h1 class="cover-h1">{{HEAD}} <span class="grad">{{HEAD_ACCENT}}</span></h1>
    <p class="cover-sub">{{SUBHEAD}}</p>
    <div class="cover-promise">ENABLING GROWTH</div>
    <div class="spacer"></div>
    <div class="snap">
      <p class="sh">At a glance</p>
      <table class="snap-grid"><tr>
        <td><span class="k">{{K1}}</span><span class="v big">{{V1}}</span></td>
        <td><span class="k">{{K2}}</span><span class="v">{{V2}}</span></td>
        <td><span class="k">{{K3}}</span><span class="v">{{V3}}</span></td>
      </tr></table>
    </div>
    <div class="cover-foot"><span>LAKEB2B · ENABLING GROWTH</span><span>DEPTH · DATA · PARTNERSHIP</span></div>
  </div>
</div>
```

Accent color on the cover headline span (`.grad`) is solid gold for contrast on
the dark gradient. In section headings, `.grad` is solid magenta.

## Section header

```html
<div class="sheet">
  <div class="kicker"><span class="kdot"></span><span class="kt">Section kicker</span></div>
  <h2 class="section">Section title <span class="grad">accent.</span></h2>
  <div class="rule"></div>
  <!-- body -->
</div>
```

## Intro panel + positioning ladder

```html
<div class="intro">
  <p class="big">A short, confident lead line.</p>
  <p>Supporting paragraph in the growth-stack voice.</p>
</div>

<div class="ladder">
  <div class="lrow top"><span class="llabel">Category</span><span class="lval">The B2B growth stack</span></div>
  <div class="lrow"><span class="llabel">Promise</span><span class="lval"><b>ENABLING GROWTH</b></span></div>
  <div class="lrow"><span class="llabel">Proof</span><span class="lval">Four integrated verticals</span></div>
</div>
```

## Vertical cards (color-coded, full width)

Classes: `v-sales` (purple), `v-mar` (magenta), `v-rec` (teal), `v-growth`
(orange to red).

```html
<div class="vgrid">
  <div class="vcard v-sales">
    <div class="vhead"><div class="vn">SalesTech</div><div class="vtag">Unleashing data-driven lead generation</div></div>
    <div class="vbody"><p>One sentence on the value.</p></div>
  </div>
</div>
```

## Process flow

```html
<div class="flow">
  <div class="fstep"><div class="fi">01 · Source</div><div class="ft">Deep data reservoirs</div></div>
  <div class="farrow">&rarr;</div>
  <div class="fstep"><div class="fi">02 · Refine</div><div class="ft">Intelligence</div></div>
</div>
```

## Stat / outcome chips (single row)

```html
<div class="chips">
  <div class="chip"><div class="cn">Pipeline</div><div class="cl">Sales outcomes</div></div>
</div>
```

## Engagement table, or pricing table with totals

Use plain rows for engagement models. For a proposal with money, add `subtot` and
`grand` rows (the grand row renders as a gradient band, the amount in gold). Add a
right-aligned `amt` cell for figures.

```html
<table class="grid">
  <tr><th>Item</th><th>Detail</th><th class="amt">Amount</th></tr>
  <tr><td class="mname">Data intelligence setup</td><td>Onboarding and enrichment</td><td class="amt num">$X</td></tr>
  <tr class="subtot"><td>Sub-total</td><td></td><td class="amt num">$X</td></tr>
  <tr class="grand"><td>Total investment</td><td></td><td class="amt num">$X</td></tr>
</table>
```

Verify money before rendering: line items sum to the sub-total, taxes or fees are
shown on their own line, the total equals sub-total plus those lines.

## What you get list

```html
<div class="incl">
  <h4>What the stack gives you</h4>
  <ul><li>Benefit line</li></ul>
</div>
```

## Numbered next steps

```html
<ul class="terms">
  <li><span class="tn">1</span><b>Discovery.</b> A short working session.</li>
</ul>
```

## CTA band + lockup

```html
<div class="cta">
  <h3>Let's build your growth stack.</h3>
  <p>One supporting line.</p>
  <div class="promise">ENABLING GROWTH</div>
</div>
<div class="lockup">
  <div class="l1"><b>LakeB2B</b> · The B2B growth stack · Data, MarTech, sales enablement, and talent</div>
  <div class="l2">ENABLING GROWTH</div>
</div>
```

## Motif SVGs

Logo mark (data-dot network, drop into `.brandmark`):

```html
<svg class="brandmark" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#FFFFFF" stroke-width="1.2" opacity="0.5">
    <line x1="9" y1="14" x2="22" y2="9"/><line x1="22" y1="9" x2="31" y2="18"/>
    <line x1="9" y1="14" x2="14" y2="27"/><line x1="14" y1="27" x2="27" y2="31"/>
    <line x1="22" y1="9" x2="14" y2="27"/><line x1="27" y1="31" x2="31" y2="18"/>
  </g>
  <circle cx="9" cy="14" r="3.2" fill="#FFB703"/><circle cx="22" cy="9" r="3.6" fill="#DD1286"/>
  <circle cx="31" cy="18" r="3" fill="#FF6903"/><circle cx="14" cy="27" r="3" fill="#7A76DA"/>
  <circle cx="27" cy="31" r="3.4" fill="#FFFFFF"/>
</svg>
```

For the cover background gradient and curved-line / network motif, copy the
`<svg class="cover-bg">` block from `assets/document_template.html`.
