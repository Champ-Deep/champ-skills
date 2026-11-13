# Diagram connectors: fan-in, fan-out, beams

Depth for showcase-page rule 19 and the "second rendering" bullet in Step 5. The kit has no connector class; this is the pattern to build against brand tokens.

## Geometry: cubic, anchored at distinct heights

A hub-and-spoke stage (input cards left, hub centre, output cards right) draws one path per link. Anchor every end on its own fraction of the shared edge, so three links into one hub land at 0.5, 0.5 and 0.7 of its height rather than all at its centre.

```js
// pairs: [fromId, toId, fromHeightFrac, toHeightFrac, animationDelaySeconds]
var pairs = [['bn-data','bn-hub',.5,.3,0], ['bn-sig','bn-hub',.5,.5,.6],
             ['bn-bed','bn-hub',.5,.7,1.2], ['bn-hub','bn-out',.35,.5,1.8],
             ['bn-hub','bn-mkt',.65,.5,2.4]];
// c = stage rect, a = from rect, b = to rect
var sx = a.right - c.left, sy = a.top - c.top + a.height * p[2];
var ex = b.left  - c.left, ey = b.top  - c.top + b.height * p[3], mx = (sx + ex) / 2;
var d = `M ${sx},${sy} C ${mx},${sy} ${mx},${ey} ${ex},${ey}`;
```

Why cubic: `C mx,sy mx,ey ex,ey` leaves each segment horizontal at both ends, so two links entering one node from opposite sides can never intersect. A quadratic `Q mx,cy ex,ey` with one control point pulls both ends toward the same middle and crosses when the second link enters from the other side or at a different height. That is the defect this recipe exists to prevent: it ships looking fine at a glance and a review pass reports it as fact.

Measure against the container rect on every draw and redraw on `resize` and on `document.fonts.ready` (a font swap reflows the cards after first paint and leaves the beams anchored to stale positions). SVG is `position:absolute; inset:0` over the stage with `overflow:visible`, width and height set from the measured stage.

## Layering and motion

- Base stroke: brand ink at ~0.14 opacity, 2px, no animation.
- Glow stroke: 2.6px, `stroke-linecap:round`, painted from a `linearGradient` in `userSpaceOnUse` across the segment, four stops: transparent, accent, second brand colour, transparent at 100%.
- Travel: SMIL `<animate attributeName="x1|x2" values="0%;100%" dur="4s" begin="delay" repeatCount="indefinite/>`, one delay per link so the beams do not pulse in lockstep.
- Static and reduced motion: skip the SMIL entirely and set `x1="40%" x2="60%"`, so `?static=1` exports a fully drawn diagram with no moving parts.
- Credit the source in a comment. This recipe is a vanilla port of 21st.dev **Animated Beam** (id 919, dillionverma / Magic UI): measured path, faint base stroke, travelling gradient. For React builds the component installs natively instead.

## Second rendering on phones

The stage is `display:grid; grid-template-columns:1fr minmax(220px,.9fr) 1fr` above 900px. Below it: `display:none` on the stage, `display:block` on a numbered list carrying identical content (`li::before` counter, hub rows accent-bordered left). Zero beam paths and one visible list at 390 is the assertion, so a stacked fallback that renders while the drawing is still up (or vice versa) fails the probe rather than reading as a doubled diagram.

## Probe after the build

1. `document.querySelectorAll('.beam-glow').length` equals the pair count at 1440 and equals 0 at 390, where `.beam-list` is `display:block`.
2. One element screenshot of the diagram with `.nav,.progress` hidden, then a vision pass asking specifically whether any two connectors cross and whether each meets a card edge. Ask the crossing question directly: a general "describe this diagram" returns an inventory and misses the crossing.
3. If the pass reports crossings, re-shoot rather than reasoning: the anchors are data, so fix the fractions and count paths again.
