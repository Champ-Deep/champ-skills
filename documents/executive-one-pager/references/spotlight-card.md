# Spotlight card

Standard card treatment for this skill. A soft spot on the surface and a lit hairline ring follow the pointer, and the ring brightens on neighbouring cards as the pointer approaches. Vanilla port of the 21st.dev `spotlight-card` (GlowCard, React and Tailwind); the page ships as one static HTML file, so the shadcn install path does not apply. Credit the component in a CSS comment.

## What changed from the React original (and why)

| Original | This port | Why |
|---|---|---|
| `background-attachment: fixed` plus viewport coordinates | `--gc-x`, `--gc-y` measured inside each card | Fixed backgrounds stop tracking inside any transformed ancestor, and reveal animations use transforms |
| Unprefixed `--border`, `--size`, `--radius`, `--base`, `--hue` | everything prefixed `--gc-` | Those names collide with page tokens |
| Pointer defaults to 0,0 | defaults to -9999 | Otherwise every card shows a lit corner before the pointer moves |
| Fixed 14px radius, 3px ring, blue, saturated | inherits the card's radius, 1px ring, neutral | Hairline house style; saturation is an opt-in |
| Outer blurred bloom element | dropped | Needs a child element in every card and reads as decoration at this card size |
| Always on | fine pointers only, off in `?static=1` | Touch has no hover; static exports need the plain card |

## Rules

1. The card's own `background-color` and `border-radius` stay as they are; `.gc` adds only a hairline border, a gradient on top, and the ring. The card must not set `overflow:hidden` with a negative-inset child it needs, and must not set its own `::before` or `::after`.
2. The border width equals `--gc-b` (the class sets both).
3. One micro-interaction per element: do not put `.gc` on a card that already tilts (`.fcard`) or carries another pointer effect.
4. Reads on both themes: the dark tokens are wired to `prefers-color-scheme` and `[data-theme="dark"]`; on a dark section of a light page add `.gc-dark`.
5. Colour: `--gc-sat:0%` is a neutral ink glow. A brand hue is set per page with `--gc-base` (hue 0 to 360) and a small `--gc-spread` (the sweep across the viewport width). Reference hues from the original: blue 220/200, purple 280/300, green 120/200, red 0/200, orange 30/200. Keep spread at 40 or less so the glow stays on brand.

## CSS

```css
/* Spotlight card. Vanilla port of 21st.dev "spotlight-card" (GlowCard): a soft spot on the surface plus a lit hairline ring that follow the pointer.
   Needs the page tokens --line (hairline) and the card's own background and border-radius. JS sets --gc-x, --gc-y (px inside the card) and --gc-xp (0 to 1 across the viewport). */
.gc{
  --gc-base:220; --gc-spread:0; --gc-sat:0%;            /* hue, hue sweep across the viewport, saturation. 0% = neutral ink glow */
  --gc-b:1px; --gc-size:220px;                          /* ring width (also the card's border width), spotlight radius */
  --gc-l:38%; --gc-hl:0 0% 0%; --gc-hl-a:.55; --gc-fx:none; --gc-spot-a:.08;
  --gc-hue:calc(var(--gc-base) + var(--gc-xp,0) * var(--gc-spread));
  position:relative; border:var(--gc-b) solid var(--line);
  background-image:radial-gradient(var(--gc-size) var(--gc-size) at calc(var(--gc-x,-9999) * 1px) calc(var(--gc-y,-9999) * 1px),
    hsl(var(--gc-hue) var(--gc-sat) 50% / var(--gc-spot-a)), transparent);
}
.gc::before,.gc::after{
  content:""; position:absolute; inset:calc(var(--gc-b) * -1); border:var(--gc-b) solid transparent; border-radius:inherit; pointer-events:none;
  background-origin:border-box; background-repeat:no-repeat;
  -webkit-mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0); -webkit-mask-composite:xor;
  mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0); mask-composite:exclude;
}
.gc::before{
  background-image:radial-gradient(calc(var(--gc-size) * .75) calc(var(--gc-size) * .75) at calc(var(--gc-x,-9999) * 1px) calc(var(--gc-y,-9999) * 1px),
    hsl(var(--gc-hue) var(--gc-sat) var(--gc-l)), transparent 100%);
  filter:var(--gc-fx);
}
.gc::after{
  background-image:radial-gradient(calc(var(--gc-size) * .5) calc(var(--gc-size) * .5) at calc(var(--gc-x,-9999) * 1px) calc(var(--gc-y,-9999) * 1px),
    hsl(var(--gc-hl) / var(--gc-hl-a)), transparent 100%);
}
/* dark ground: lighter ring, white inner edge. Use .gc-dark on a dark section, or wire to the page's dark tokens. */
.gc-dark{--gc-l:62%; --gc-hl:0 0% 100%; --gc-hl-a:.8; --gc-fx:brightness(1.6); --gc-spot-a:.1}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .gc{--gc-l:62%; --gc-hl:0 0% 100%; --gc-hl-a:.8; --gc-fx:brightness(1.6); --gc-spot-a:.1}}
:root[data-theme="dark"] .gc{--gc-l:62%; --gc-hl:0 0% 100%; --gc-hl-a:.8; --gc-fx:brightness(1.6); --gc-spot-a:.1}
```

## JS (one listener, one frame)

```js
/* spotlight cards: pointer position in each .gc, once per frame. Fine pointers only; touch gets the plain card. */
(function(){
  if(!matchMedia('(hover:hover) and (pointer:fine)').matches||/[?&]static=1/.test(location.search)) return;
  var cards=[].slice.call(document.querySelectorAll('.gc')), p=null, raf=0;
  if(!cards.length) return;
  addEventListener('pointermove',function(e){ p=e; raf=raf||requestAnimationFrame(paint); },{passive:true});
  function paint(){ raf=0; var xp=(p.clientX/innerWidth).toFixed(3),
    rs=cards.map(function(c){return c.getBoundingClientRect();});          // read all, then write all
    cards.forEach(function(c,i){ c.style.setProperty('--gc-x',(p.clientX-rs[i].left).toFixed(1));
      c.style.setProperty('--gc-y',(p.clientY-rs[i].top).toFixed(1)); c.style.setProperty('--gc-xp',xp); }); }
})();
```

## Check

Dispatch a pointer move and assert the variables landed, then screenshot a lit card in light and dark and open it. A real mouse move in Playwright (`page.mouse.move`) is enough; `getComputedStyle(card).getPropertyValue('--gc-x')` is non-empty after it. Zero console errors.

## Where it goes in the executive one-pager

Neutral only: rule 7 reserves the brand accent for the reader's own items, so leave `--gc-sat` at 0%.

| Gets `.gc` | Does not |
|---|---|
| Settled cards, option cards, risk cards, quote cards, Presenter slide cards, boxed number cells | The ask panel (`.desk`), hairline status rows, the verdict band, `<details>` summaries |

Put the JS in the same inline `<script>` as the reveal code. Keep reveal animation off the card itself if you can; this port tolerates transforms, but a transformed card moves under the pointer and the ring lags one frame.
