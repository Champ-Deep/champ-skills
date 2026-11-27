# Artwork hotspot audit

Grading interactive hotspots drawn over an illustration, usually in someone else's
build. The gate is placement, not wiring: "clicking X opens card X" can be completely
green while every box floats above the subject it names, because no assertion ever
read a pixel of the art.

## 1. Freeze the render first

Playwright, one run per shipping width, `reduced_motion='reduce'`, and wait past the
entrance choreography. Read the SVG/scene container's `getBoundingClientRect()` and
its `viewBox` twice, 500ms apart, and require the y to be identical before you use it:
an entrance transform still running shifts every coordinate you read afterwards and
makes correctly placed boxes look 40px high.

## 2. Read subject coordinates off the raw asset

When you did not write the build, there are no source coordinates, so build them:

- Crop the raw asset from disk (the `.webp`/`.png`, never the screenshot) around the
  subject at 3 to 4x.
- Draw a ruler onto the crop: red horizontal lines every 20 art units labelled with the
  art `y`, blue vertical lines every 20 labelled with `x`.
- One `vision_analyze` per crop, asking literally: between which labelled lines does the
  subject lie, and at which `y` does it make contact with the ground, the water, or the
  fingertip.

Ask for the **contact point**, not the subject's centre: a hit target belongs where the
thing touches its surface, and a centre read on a tall subject puts the box in the
wrong place even when the read is right. Ask for the label numbers, never "roughly 60%
down". Keep the crops in scratch, not beside the deliverable.

A vision read is a hypothesis. Confirm each one against the probe in step 4, and name
in the report the reads you dropped for failing to hold: a review that reports only its
confirmed findings reads as if every first impression was correct.

## 3. Map art coordinates to CSS

```
scale = rect.width / viewBox.width          # object-fit: cover crops, so use
                                            # max(rect.w/vb.w, rect.h/vb.h) and
                                            # subtract the crop offsets
cssX  = rect.x + (artX - vb.x) * scale
cssY  = rect.y + (artY - vb.y) * scale
```

## 4. Probe placement, not wiring

```python
el = page.evaluate("([x,y]) => { const e = document.elementFromPoint(x,y);
        return e.getAttribute('aria-label') || e.tagName }", [cssX, cssY])
```

Require each subject's own hotspot label at its converted centre, at every shipping
width. `use` / `svg` / `div` back means the click lands on background: the target does
not cover its subject, and the size and wiring gates will both still pass. Probe every
target, not the suspicious ones: a consistent 30-unit offset across the left half of a
scene is one mapping bug, and sampling two targets hides it.

## 5. Diff a claimed asset edit

A claimed "removed" or "moved" region is proved against the previous version of the
asset: same dimensions, both converted to `L`, then `np.abs(A-B) > 15` and report the
hit count plus the `min/max` of x and y. Quote the bounding box and the count, never
"the edit landed": a 17x16 patch of 173 changed pixels is a blur where an object used
to be, and only the box makes that visible.

## 6. Figure scale, occlusion, gait

- **Proportion** is judged against an object in the same art with a known real relation
  (a gate, a door, an adult figure), not against the figure's own pixel height. A sprite
  that measures fine in isolation and reads smaller than a midground human is wrong.
- **Occlusion** needs the depth band to run from the feet up past the head. A band that
  ends above the feet paints the legs in front of the occluder and the torso behind it,
  which no single-frame screenshot shows as broken.
- **Gait**: travel per full stride cycle should be on the order of half the figure's
  height. Measure it as two shots N seconds apart, not by eye: far less than that means
  the feet slide, and a figure that walks for a fixed time then freezes forever is a
  loop defect worth naming.
- **Provenance census**: count the rendering sources on one page (base raster art,
  code-drawn props, sprite animation, UI chrome). Any code-drawn layer over base art has
  to match its edge quality, texture and scale, or it reads as a second art direction
  stacked on the first, which is the jarring the eye reports before any measurement
  does.

## 7. Label honesty

Every hotspot name must name something visible in the art. A target labelled for a
building that is not drawn, or a scene feature renamed to fit a card, is a content
defect of the same class as a wrong caption: change the label or paint the subject.
