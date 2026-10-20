# Dot-matrix globe with signal arcs

Use for a Boardy-style hero or section globe: a dotted world sphere with great-circle arcs running city to city, drag-to-rotate, in one self-contained HTML file. The reference globe `scroll-journey-kit` points at (LakeKit `LakeB2B_Living_Data_Globe_reference.html`) is WebGL with GSAP pinning; reach for that when the globe is the pinned hero of a scrubbed journey. The recipe below is the 2D canvas path: no WebGL, no animation runtime, no network at view time, so it fits the self-contained single-file gate.

## Step 1: fetch the land data once

```bash
curl -sSL https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json -o land-110m.json   # 55KB TopoJSON
```

`topojson-client` is an npm dependency you do not need: the transform is two lines of Python (Step 2). Keep the file beside the build script so the page stays offline-only.

## Step 2: decode and rasterize to a dot grid

TopoJSON stores delta-encoded arcs plus a `transform`. Decode, then test points against the rings:

```python
topo = json.load(open("land-110m.json"))
sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
def arc(i):
    pts = topo["arcs"][~i if i < 0 else i]      # negative index = reversed arc
    x = y = 0; out = []
    for dx, dy in pts:
        x += dx; y += dy; out.append((x*sx+tx, y*sy+ty))
    return out[::-1] if i < 0 else out
```

- **Rasterize on a latitude-stepped grid, longitude spacing scaled by `cos(lat)`.** A uniform lon/lat grid clusters dots at the poles and gaps the equator: `n = round(360 / (STEP / max(cos(radians(lat)), 0.08)))` per row keeps the density even on the projected sphere.
- **Point-in-polygon needs an even-odd parity test across ALL rings of a polygon**, not a single outer ring: the first ring is the outline, later rings are lakes and inland seas, and a naive test paints the Caspian as land.
- **Assert the dot count.** A 2.0 degree step yields about 2700 dots and reads as a faint ghost; 1.5 degree yields about 4800 and reads as a map. Assert a band (for example 2500 to 12000) in the build script so a broken decode fails the build instead of shipping a blank sphere.
- Serialize as scaled integers (`round(lat*10)`) in a flat array, not objects: about 20KB for 4800 dots versus several times that for `[{lat,lon},...]`.

## Step 3: render and interact

**Projection.** Orthographic, one function: shift `lon` by the current yaw, rotate the result about the x axis by the tilt, then `x = W/2 + cx*R`, `y = W/2 - cy*R`. The z component is the visibility test: `z > 0` is the front hemisphere, so far-side dots and arc segments are skipped by testing z, never by clipping. Size `R` from the canvas width (`0.4 * W`) and set `canvas.width = W * min(devicePixelRatio, 2)` so lines stay crisp on phones without paying 3x fill.

**Arcs are great-circle interpolations, not quadratic curves.** A bezier between two city screen positions floats off the sphere and breaks when a hemisphere rotates into view. Interpolate with the standard spherical formula (slerp: `A = sin((1-t)d)/sin(d)`, `B = sin(td)/sin(d)` applied to the unit vectors), then project each of about 40 samples and lift it by `h * sin(pi*t)` so the arc rises at its midpoint. Lift only points whose projected z is positive, which makes the arc clip cleanly at the horizon.

**Draw arcs segment by segment.** One polyline with far-side points skipped still strokes a line straight through the sphere across the gap. Stroke each segment only when at least one endpoint has `z > 0`, and fade with a per-arc `t` that runs 0 to 1 (draw) then 1 to 1.6 (hold) before recycling.

**Drag must not steal page scroll.** Set `touch-action: pan-y` on the canvas, capture `pointerdown`, add `yaw += dx * 0.4` on horizontal `pointermove`, and release with inertia (`vel *= 0.94`). Vertical gestures then still scroll the page, which is the failure everyone hits first. Auto-rotation is `yaw -= dt * 6` per second inside the rAF loop.

**Drive the loop from visibility and motion preference.** An IntersectionObserver starts and stops the rAF loop so an offscreen globe costs nothing, and `prefers-reduced-motion: reduce` renders every arc fully drawn, once, with no auto-rotation, plus the feed rows pre-populated. Re-render on drag in that mode instead of animating.

## Step 4: honesty and accessibility

- **Label sample arcs as illustrative on the page itself**, beside the globe, not only in the report. Do not borrow reference sites' live counters ("258,944 introductions") when no feed exists, and do not caption the layer "live".
- **Ship a non-canvas twin of every arc.** Canvas pixels are invisible to screen readers and crawlers, so a `<details>` holding a table of signal type / from / to costs ten lines and satisfies the semantics gate.
- Keep the city list and arcs in one JS data structure so the legend chips, the feed, the table and the render loop all read from one source.

## Step 5: verify it in the browser

```python
pg.goto(url); pg.wait_for_timeout(3500)                       # entrance settles
st = pg.evaluate("window.GlobeState()")                       # expose {yaw, running, visible, arcs, dots}
pg.locator("#map").scroll_into_view_if_needed(); pg.wait_for_timeout(4000)
bb = pg.locator("canvas").bounding_box()
pg.mouse.move(bb["x"]+bb["width"]/2, bb["y"]+bb["height"]/2); pg.mouse.down()
pg.mouse.move(bb["x"]+bb["width"]/2+150, bb["y"]+bb["height"]/2, steps=8); pg.mouse.up()
assert pg.evaluate("window.GlobeState().yaw") != y0           # drag really rotated it
pg.click("#legend .chip:nth-child(1)")
assert pg.get_attribute("#legend .chip:nth-child(1)", "aria-pressed") == "false"
```

Also assert: zero console errors, zero requests that are not `file:` or `data:` (the offline claim), and `document.documentElement.scrollWidth === innerWidth` at 390 and 1440. Expose the state hook deliberately; `visual-verify`'s canvas rule applies here, since the DOM audit sees none of these pixels.

**Shoot the element, not the scrolled viewport.** `locator("#map").screenshot()` captures the whole section; a viewport screenshot taken after `scroll_into_view` overlaps the sticky nav across the section top, and a vision pass reports that overlap as "the eyebrow and first list row are clipped", sending you into a fix round for a defect that is only the scroll position. If a shot does show the nav sitting over content, confirm by bounding box before acting. Then look at the shot for the real defects: arcs with no occlusion at the sphere edge, land dots too sparse to name a continent, arcs that all read as one colour, and a globe too small to parse at 390.
